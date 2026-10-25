using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 品物と原料の流れ(#82)。育てる期間の市長は、品物が届かない店(NoGoods)と原料が届かない工場(NoResources)を見て、
    // Cargo Harbor を置けばどれだけ減るかを見積もれなかった。
    //
    // 荷物の車(CargoTruckAI)を、運んでいるもの(Vehicle.m_transferType)と向き(Importing / Exporting の印、なければ街の中)で数える。
    // 鉄道・船は、荷台の車(m_cargoParent が親の車)を同じように数える。
    // 止まっている車は、m_blockCounter が0でないか、渋滞(Congestion)・空き待ち(WaitingSpace)の印があるもの。
    public static class CargoApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/cargo"] = req => HttpBridge.OnMain(Cargo);
            routes["/vehicles/stuck"] = req => HttpBridge.OnMain(() => Vehicles(req));
        }

        private class Flow
        {
            public int Import, Export, Local, Stopped;
        }

        // /cargo
        private static string Cargo()
        {
            var vs = VehicleManager.instance.m_vehicles.m_buffer;
            var flows = new SortedDictionary<string, Flow>();
            var stopCells = new Dictionary<long, int[]>(); // 200m四方 → {台数, x の合計, z の合計}
            var stations = new Dictionary<ushort, int[]>(); // 荷物の駅・港 → {出る, 入る}
            int trucks = 0, trains = 0, ships = 0, stoppedTrucks = 0;
            int stoppedInBuildings = 0;
            var inBuildingBy = new Dictionary<int, int>();
            for (int i = 1; i < vs.Length; i++)
            {
                var v = vs[i];
                if ((v.m_flags & Vehicle.Flags.Created) == 0 || v.Info == null)
                {
                    continue;
                }

                var ai = v.Info.m_vehicleAI;
                bool truck = ai is CargoTruckAI;
                bool carrier = ai is CargoTrainAI || ai is CargoShipAI;
                bool cargoCar = v.m_cargoParent != 0; // 鉄道・船の荷台
                if (!truck && !carrier && !cargoCar)
                {
                    continue;
                }

                if (carrier && v.m_leadingVehicle == 0)
                {
                    if (ai is CargoTrainAI)
                    {
                        trains++;
                    }
                    else
                    {
                        ships++;
                    }

                    CountStation(stations, v.m_sourceBuilding, v.m_targetBuilding);
                }

                if (!truck && !cargoCar)
                {
                    continue; // 鉄道・船の車両そのものは数えた。荷物は荷台で数える
                }

                string what = ((TransferManager.TransferReason)v.m_transferType).ToString();
                Flow f;
                if (!flows.TryGetValue(what, out f))
                {
                    f = new Flow();
                    flows[what] = f;
                }

                if ((v.m_flags & Vehicle.Flags.Importing) != 0)
                {
                    f.Import++;
                }
                else if ((v.m_flags & Vehicle.Flags.Exporting) != 0)
                {
                    f.Export++;
                }
                else
                {
                    f.Local++;
                }

                if (!truck)
                {
                    continue;
                }

                trucks++;
                CountStation(stations, v.m_sourceBuilding, v.m_targetBuilding);
                bool stopped = v.m_blockCounter != 0 || (v.m_flags & (Vehicle.Flags.Congestion | Vehicle.Flags.WaitingSpace)) != 0;
                if (stopped)
                {
                    f.Stopped++;
                    stoppedTrucks++;
                    // 駅や港の敷地の中で待つトラックは、道の詰まりと分けて数える(#107)
                    if (TrafficApi.InBuildingGrounds(ref v))
                    {
                        stoppedInBuildings++;
                        int bid = NearerBuilding(v.GetLastFramePosition(), v.m_sourceBuilding, v.m_targetBuilding);
                        int seen;
                        inBuildingBy.TryGetValue(bid, out seen);
                        inBuildingBy[bid] = seen + 1;
                        continue;
                    }

                    var p = v.GetLastFramePosition();
                    long key = ((long)Mathf.FloorToInt(p.x / 200f) << 32) ^ (uint)Mathf.FloorToInt(p.z / 200f);
                    int[] c;
                    if (!stopCells.TryGetValue(key, out c))
                    {
                        c = new int[3];
                        stopCells[key] = c;
                    }

                    c[0]++;
                    c[1] += Mathf.RoundToInt(p.x);
                    c[2] += Mathf.RoundToInt(p.z);
                }
            }

            var sb = new StringBuilder("{\"ok\":true,\"trucks\":").Append(trucks).Append(",\"cargoTrains\":").Append(trains)
                .Append(",\"cargoShips\":").Append(ships).Append(",\"stoppedTrucks\":").Append(stoppedTrucks)
                .Append(",\"stoppedOnRoads\":").Append(stoppedTrucks - stoppedInBuildings).Append(",\"stoppedInBuildings\":").Append(stoppedInBuildings)
                .Append(",\"stoppedInBuildingsTop\":").Append(InBuildingTop(inBuildingBy)).Append(",\"byCargo\":{");
            bool first = true;
            foreach (var kv in flows)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(":{\"import\":").Append(kv.Value.Import)
                  .Append(",\"export\":").Append(kv.Value.Export).Append(",\"local\":").Append(kv.Value.Local)
                  .Append(",\"stoppedTrucks\":").Append(kv.Value.Stopped).Append('}');
                first = false;
            }

            sb.Append("},\"stoppedSpots\":").Append(Spots(stopCells));
            sb.Append(",\"stations\":").Append(StationsJson(stations));
            sb.Append(",\"shortages\":").Append(Shortages());
            return sb.Append('}').ToString();
        }

        // 荷物の駅・港(CargoStationAI。Cargo Harbor を含む)ごとに、そこから出る車と、そこへ入る車を数える
        private static void CountStation(Dictionary<ushort, int[]> stations, ushort source, ushort target)
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            if (source != 0 && bs[source].Info != null && bs[source].Info.m_buildingAI is CargoStationAI)
            {
                Get(stations, source)[0]++;
            }

            if (target != 0 && bs[target].Info != null && bs[target].Info.m_buildingAI is CargoStationAI)
            {
                Get(stations, target)[1]++;
            }
        }

        private static int[] Get(Dictionary<ushort, int[]> d, ushort id)
        {
            int[] c;
            if (!d.TryGetValue(id, out c))
            {
                c = new int[2];
                d[id] = c;
            }

            return c;
        }

        private static string StationsJson(Dictionary<ushort, int[]> stations)
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            // 車の行き来がない駅・港も一覧に出す
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) != 0 && bs[i].Info != null && bs[i].Info.m_buildingAI is CargoStationAI
                    && bs[i].m_parentBuilding == 0)
                {
                    Get(stations, (ushort)i);
                }
            }

            var sb = new StringBuilder("[");
            bool first = true;
            foreach (var kv in stations)
            {
                var b = bs[kv.Key];
                sb.Append(first ? "" : ",").Append("{\"id\":").Append(kv.Key).Append(",\"prefab\":").Append(Json.Str(b.Info.name))
                  .Append(",\"x\":").Append(Mathf.RoundToInt(b.m_position.x)).Append(",\"z\":").Append(Mathf.RoundToInt(b.m_position.z))
                  .Append(",\"vehiclesLeaving\":").Append(kv.Value[0]).Append(",\"vehiclesArriving\":").Append(kv.Value[1]).Append('}');
                first = false;
            }

            return sb.Append(']').ToString();
        }

        // 止まっている荷物の車が多い200m四方の上位5つ(車の位置の平均と台数)
        // 止まったトラックを最初に見た時刻(シミュレーションのコマ)。/cargo/vehicles を呼ぶたびに更新する。
        // 車の番号は使い回されるので、出発と行き先の建物が変わったら見直す(#107)
        private struct Seen
        {
            public uint Frame;
            public ushort Source, Target;
        }

        private static readonly Dictionary<ushort, Seen> FirstStopped = new Dictionary<ushort, Seen>();

        // /vehicles/stuck?kind=truck&building=9447&limit=30  止まった車を1台ずつ見る(#107)。
        // 14回目の後、貨物駅9447の中の約460台が何を待っているかを、数だけの cargo では見分けられなかった。
        // building を渡すと、その建物の敷地の中にいるか、その建物を出発・行き先にするトラックだけを数える。
        private static string Vehicles(HttpListenerRequest req)
        {
            int building = 0;
            int.TryParse(req.QueryString["building"] ?? "0", out building);
            int limit = 30;
            int.TryParse(req.QueryString["limit"] ?? "30", out limit);
            limit = Mathf.Clamp(limit, 0, 1000);
            // 車の種類(#107): truck(荷物のトラック)/ train(貨物列車)/ ship(貨物船)/ hearse(霊柩車)/ garbage(ごみ収集車)
            string kind = (req.QueryString["kind"] ?? "truck").ToLowerInvariant();
            if (kind != "truck" && kind != "train" && kind != "ship" && kind != "hearse" && kind != "garbage" && kind != "bus")
            {
                return HttpBridge.Error("kind must be truck / train / ship / hearse / garbage / bus");
            }

            // 列車と船は台数が少ないので、走っているものも含めて全部を返す
            bool all = kind == "train" || kind == "ship";

            var vs = VehicleManager.instance.m_vehicles.m_buffer;
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var units = PathManager.instance.m_pathUnits.m_buffer;
            uint now = SimulationManager.instance.m_currentFrameIndex;
            // 1コマのゲーム内の時間(SimulationManager.m_timePerFrame。約148秒で、1日は約585コマ)
            double daysPerFrame = SimulationManager.instance.m_timePerFrame.TotalDays;

            var byState = new SortedDictionary<string, int>();
            var byTarget = new Dictionary<int, int>();
            var byPath = new SortedDictionary<string, int>();
            var byAge = new SortedDictionary<string, int>();
            var samples = new StringBuilder("[");
            int count = 0, sampled = 0;
            var alive = new HashSet<ushort>();
            for (int i = 1; i < vs.Length; i++)
            {
                var v = vs[i];
                if ((v.m_flags & Vehicle.Flags.Created) == 0 || v.Info == null || !IsKind(v.Info.m_vehicleAI, kind))
                {
                    continue;
                }

                if ((kind == "train" || kind == "ship") && v.m_leadingVehicle != 0)
                {
                    continue; // 列車は先頭の車両だけを数える
                }

                bool inGrounds = TrafficApi.InBuildingGrounds(ref v);
                var pos = v.GetLastFramePosition();
                if (building != 0)
                {
                    bool related = v.m_sourceBuilding == building || v.m_targetBuilding == building;
                    bool insideHere = inGrounds && NearerBuilding(pos, v.m_sourceBuilding, v.m_targetBuilding) == building;
                    if (!related && !insideHere)
                    {
                        continue;
                    }
                }

                bool stopped = v.m_blockCounter != 0 || (v.m_flags & (Vehicle.Flags.Congestion | Vehicle.Flags.WaitingSpace
                    | Vehicle.Flags.WaitingPath | Vehicle.Flags.WaitingTarget | Vehicle.Flags.WaitingCargo | Vehicle.Flags.Stopped)) != 0;
                if (!stopped && !inGrounds && !all)
                {
                    continue; // 走っている車は数えない(列車と船は除く)
                }

                count++;
                var id = (ushort)i;
                alive.Add(id);

                // 状態: 待ちの印と、敷地の中か道の上か
                var states = new List<string>();
                foreach (Vehicle.Flags f in new[] { Vehicle.Flags.WaitingPath, Vehicle.Flags.WaitingTarget, Vehicle.Flags.WaitingCargo,
                    Vehicle.Flags.WaitingSpace, Vehicle.Flags.Congestion, Vehicle.Flags.Stopped, Vehicle.Flags.GoingBack,
                    Vehicle.Flags.Importing, Vehicle.Flags.Exporting, Vehicle.Flags.Spawned })
                {
                    if ((v.m_flags & f) != 0)
                    {
                        states.Add(f.ToString());
                    }
                }

                states.Add(inGrounds ? "InGrounds" : "OnRoad");
                if (v.m_blockCounter != 0)
                {
                    states.Add("Blocked");
                }

                string state = string.Join("+", states.ToArray());
                Bump(byState, state);

                // 道順: 道順がない / 計算待ち / 計算中 / できた / 失敗
                string path;
                if (v.m_path == 0)
                {
                    path = "none";
                }
                else
                {
                    byte pf = units[v.m_path].m_pathFindFlags;
                    path = (pf & PathUnit.FLAG_FAILED) != 0 ? "failed" : (pf & PathUnit.FLAG_READY) != 0 ? "ready"
                        : (pf & PathUnit.FLAG_CALCULATING) != 0 ? "calculating" : (pf & PathUnit.FLAG_QUEUED) != 0 ? "queued" : "unknown";
                }

                Bump(byPath, path);

                // バスの m_targetBuilding は建物ではなく、次の停留所の点(NetNode)の番号。バスは路線ごとに数える(#107)
                bool bus = kind == "bus";
                int tgt = bus ? -v.m_transportLine : v.m_targetBuilding;
                int seenT;
                byTarget.TryGetValue(tgt, out seenT);
                byTarget[tgt] = seenT + 1;

                // 止まって見えている長さ(この道具で最初に見た時から)
                Seen seen;
                if (!FirstStopped.TryGetValue(id, out seen) || seen.Source != v.m_sourceBuilding || seen.Target != v.m_targetBuilding)
                {
                    seen = new Seen { Frame = now, Source = v.m_sourceBuilding, Target = v.m_targetBuilding };
                    FirstStopped[id] = seen;
                }

                double days = (now - seen.Frame) * daysPerFrame;
                string age = days < 1 ? "a <1day" : days < 3 ? "b 1-3days" : days < 7 ? "c 3-7days" : "d 7days+";
                Bump(byAge, age);

                if (sampled < limit)
                {
                    var src = v.m_sourceBuilding != 0 ? bs[v.m_sourceBuilding].Info : null;
                    var dst = !bus && v.m_targetBuilding != 0 ? bs[v.m_targetBuilding].Info : null;
                    var stopPos = bus && v.m_targetBuilding != 0 ? NetManager.instance.m_nodes.m_buffer[v.m_targetBuilding].m_position : Vector3.zero;
                    float dist = bus ? (v.m_targetBuilding != 0 ? Vector3.Distance(pos, stopPos) : -1f)
                        : v.m_targetBuilding != 0 ? Vector3.Distance(pos, bs[v.m_targetBuilding].m_position) : -1f;
                    samples.Append(sampled > 0 ? "," : "").Append("{\"vehicle\":").Append(i)
                      .Append(",\"state\":").Append(Json.Str(state)).Append(",\"path\":").Append(Json.Str(path))
                      .Append(",\"cargo\":").Append(Json.Str(((TransferManager.TransferReason)v.m_transferType).ToString()))
                      .Append(",\"amount\":").Append(v.m_transferSize)
                      .Append(all ? ",\"cars\":" + CountTrailers(vs, id) + ",\"cargoLoads\":" + CountCargo(vs, id) : "")
                      .Append(kind == "bus" ? ",\"line\":" + v.m_transportLine + ",\"lineNumber\":"
                          + TransportManager.instance.m_lines.m_buffer[v.m_transportLine].m_lineNumber : "")
                      .Append(",\"blockCounter\":").Append(v.m_blockCounter).Append(",\"waitCounter\":").Append(v.m_waitCounter)
                      .Append(",\"seenStoppedDays\":").Append(Math.Round(days, 1).ToString(CultureInfo.InvariantCulture))
                      .Append(",\"x\":").Append(Mathf.RoundToInt(pos.x)).Append(",\"z\":").Append(Mathf.RoundToInt(pos.z))
                      .Append(",\"source\":{\"building\":").Append(v.m_sourceBuilding).Append(",\"prefab\":").Append(Json.Str(src != null ? src.name : null)).Append('}')
                      .Append(bus
                          ? ",\"nextStop\":{\"node\":" + v.m_targetBuilding + ",\"x\":" + Mathf.RoundToInt(stopPos.x) + ",\"z\":" + Mathf.RoundToInt(stopPos.z)
                            + ",\"distance\":" + Mathf.RoundToInt(dist) + "}}"
                          : ",\"target\":{\"building\":" + v.m_targetBuilding + ",\"prefab\":" + Json.Str(dst != null ? dst.name : null)
                            + ",\"distance\":" + Mathf.RoundToInt(dist) + "}}");
                    sampled++;
                }
            }

            // 消えた車と、走り出した車の記録は捨てる。この呼び出しで数えなかった種類や建物の車は残す
            // (前は、別の種類や建物で呼ぶと、その車の記録まで消していた。#107 の分析2)
            var gone = new List<ushort>();
            foreach (var k in FirstStopped.Keys)
            {
                var kv = vs[k];
                bool exists = (kv.m_flags & Vehicle.Flags.Created) != 0 && kv.Info != null;
                bool stillStopped = exists && (kv.m_blockCounter != 0 || TrafficApi.InBuildingGrounds(ref kv)
                    || (kv.m_flags & (Vehicle.Flags.Congestion | Vehicle.Flags.WaitingSpace | Vehicle.Flags.WaitingPath
                        | Vehicle.Flags.WaitingTarget | Vehicle.Flags.WaitingCargo | Vehicle.Flags.Stopped)) != 0);
                if (!stillStopped && !alive.Contains(k))
                {
                    gone.Add(k);
                }
            }

            foreach (var k in gone)
            {
                FirstStopped.Remove(k);
            }

            var sb = new StringBuilder("{\"ok\":true,\"kind\":").Append(Json.Str(kind)).Append(",\"building\":").Append(building).Append(",\"vehicles\":").Append(count)
                .Append(",\"byState\":").Append(DictJson(byState)).Append(",\"byPath\":").Append(DictJson(byPath))
                .Append(",\"bySeenStopped\":").Append(DictJson(byAge)).Append(",\"byTarget\":[");
            var tl = new List<KeyValuePair<int, int>>(byTarget);
            tl.Sort((a, b) => b.Value.CompareTo(a.Value));
            for (int k = 0; k < Math.Min(10, tl.Count); k++)
            {
                int bid = tl[k].Key;
                if (bid < 0)
                {
                    // バスは路線ごと
                    int line = -bid;
                    sb.Append(k > 0 ? "," : "").Append("{\"line\":").Append(line)
                      .Append(",\"lineNumber\":").Append(TransportManager.instance.m_lines.m_buffer[line].m_lineNumber)
                      .Append(",\"vehicles\":").Append(tl[k].Value).Append('}');
                    continue;
                }

                var info = bid != 0 ? bs[bid].Info : null;
                sb.Append(k > 0 ? "," : "").Append("{\"building\":").Append(bid).Append(",\"prefab\":").Append(Json.Str(info != null ? info.name : null))
                  .Append(",\"x\":").Append(bid != 0 ? Mathf.RoundToInt(bs[bid].m_position.x) : 0)
                  .Append(",\"z\":").Append(bid != 0 ? Mathf.RoundToInt(bs[bid].m_position.z) : 0)
                  .Append(",\"vehicles\":").Append(tl[k].Value).Append('}');
            }

            return sb.Append("],\"samples\":").Append(samples.Append(']')).Append('}').ToString();
        }

        private static bool IsKind(VehicleAI ai, string kind)
        {
            switch (kind)
            {
                case "truck": return ai is CargoTruckAI;
                case "train": return ai is CargoTrainAI;
                case "ship": return ai is CargoShipAI;
                case "hearse": return ai is HearseAI;
                case "garbage": return ai is GarbageTruckAI;
                case "bus": return ai is BusAI;
            }

            return false;
        }

        // 列車の車両の数(先頭を含む)
        private static int CountTrailers(Vehicle[] vs, ushort lead)
        {
            int n = 0;
            ushort cur = lead;
            while (cur != 0 && n < 64)
            {
                n++;
                cur = vs[cur].m_trailingVehicle;
            }

            return n;
        }

        // 列車・船が積んでいる荷物の数(どの車両かの荷台につながった荷物の車)
        private static int CountCargo(Vehicle[] vs, ushort lead)
        {
            int n = 0, guard = 0;
            ushort car = lead;
            while (car != 0 && guard++ < 64)
            {
                ushort c = vs[car].m_firstCargo;
                int g2 = 0;
                while (c != 0 && g2++ < 1024)
                {
                    n++;
                    c = vs[c].m_nextCargo;
                }

                car = vs[car].m_trailingVehicle;
            }

            return n;
        }

        private static void Bump(SortedDictionary<string, int> d, string k)
        {
            int n;
            d.TryGetValue(k, out n);
            d[k] = n + 1;
        }

        private static string DictJson(SortedDictionary<string, int> d)
        {
            var sb = new StringBuilder("{");
            bool first = true;
            foreach (var kv in d)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(':').Append(kv.Value);
                first = false;
            }

            return sb.Append('}').ToString();
        }

        // 敷地の中で止まったトラックが、出発と行き先のどちらの建物に近いか
        private static int NearerBuilding(Vector3 p, ushort a, ushort b)
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            float da = a != 0 ? (bs[a].m_position - p).sqrMagnitude : float.MaxValue;
            float db = b != 0 ? (bs[b].m_position - p).sqrMagnitude : float.MaxValue;
            return da <= db ? a : b;
        }

        // 敷地の中で止まったトラックが多い建物の上位5つ(建物の番号、名前、位置、台数)
        private static string InBuildingTop(Dictionary<int, int> by)
        {
            var list = new List<KeyValuePair<int, int>>(by);
            list.Sort((x, y) => y.Value.CompareTo(x.Value));
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("[");
            for (int i = 0; i < Math.Min(5, list.Count); i++)
            {
                int id = list[i].Key;
                var info = id != 0 ? bs[id].Info : null;
                sb.Append(i > 0 ? "," : "").Append("{\"building\":").Append(id)
                  .Append(",\"prefab\":").Append(Json.Str(info != null ? info.name : null))
                  .Append(",\"x\":").Append(id != 0 ? Mathf.RoundToInt(bs[id].m_position.x) : 0)
                  .Append(",\"z\":").Append(id != 0 ? Mathf.RoundToInt(bs[id].m_position.z) : 0)
                  .Append(",\"stoppedTrucks\":").Append(list[i].Value).Append('}');
            }

            return sb.Append(']').ToString();
        }

        private static string Spots(Dictionary<long, int[]> cells)
        {
            var list = new List<int[]>(cells.Values);
            list.Sort((a, b) => b[0].CompareTo(a[0]));
            var sb = new StringBuilder("[");
            for (int i = 0; i < Math.Min(5, list.Count); i++)
            {
                var c = list[i];
                sb.Append(i > 0 ? "," : "").Append("{\"x\":").Append(c[1] / c[0]).Append(",\"z\":").Append(c[2] / c[0])
                  .Append(",\"stoppedTrucks\":").Append(c[0]).Append('}');
            }

            return sb.Append(']').ToString();
        }

        // 品物が届かない店(NoGoods)と原料が届かない工場(NoResources)の数と、多い1.92km四方の上位3つ
        private static string Shortages()
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("{");
            var kinds = new[] { Notification.Problem1.NoGoods, Notification.Problem1.NoResources };
            string[] names = { "noGoods", "noResources" };
            for (int k = 0; k < kinds.Length; k++)
            {
                int total = 0;
                var cells = new Dictionary<long, int[]>();
                for (int i = 1; i < bs.Length; i++)
                {
                    if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null)
                    {
                        continue;
                    }

                    Notification.Problem1 p = bs[i].m_problems;
                    if ((p & kinds[k]) == Notification.Problem1.None)
                    {
                        continue;
                    }

                    total++;
                    var pos = bs[i].m_position;
                    long key = ((long)Mathf.FloorToInt(pos.x / 1920f) << 32) ^ (uint)Mathf.FloorToInt(pos.z / 1920f);
                    int[] c;
                    if (!cells.TryGetValue(key, out c))
                    {
                        c = new int[3];
                        cells[key] = c;
                    }

                    c[0]++;
                    c[1] += Mathf.RoundToInt(pos.x);
                    c[2] += Mathf.RoundToInt(pos.z);
                }

                var list = new List<int[]>(cells.Values);
                list.Sort((a, b) => b[0].CompareTo(a[0]));
                sb.Append(k > 0 ? "," : "").Append(Json.Str(names[k])).Append(":{\"buildings\":").Append(total).Append(",\"spots\":[");
                for (int i = 0; i < Math.Min(3, list.Count); i++)
                {
                    var c = list[i];
                    sb.Append(i > 0 ? "," : "").Append("{\"x\":").Append(c[1] / c[0]).Append(",\"z\":").Append(c[2] / c[0])
                      .Append(",\"buildings\":").Append(c[0]).Append('}');
                }

                sb.Append("]}");
            }

            return sb.Append('}').ToString();
        }
    }
}
