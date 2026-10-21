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
                .Append(",\"cargoShips\":").Append(ships).Append(",\"stoppedTrucks\":").Append(stoppedTrucks).Append(",\"byCargo\":{");
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
