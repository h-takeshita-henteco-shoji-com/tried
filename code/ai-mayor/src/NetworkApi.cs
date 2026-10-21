using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 線のつながりを見る窓口。#81 の1回目では、住宅に引っ越してくる人が2か月着かず、人口が0のままだった。
    // 引っ越しの印は、つなぎ口から家までの道順が見つかると外れる(HumanAI.PathfindSuccess)。
    // 市長は道路や管の位置を画面写真から割り出していたため、どこで切れているかを探せなかった。
    // - /net/near: 円の中の道路・管・送電線を、種類と両端の座標と点の番号で返す。点の番号が同じ線どうしはつながっている
    // - /net/reach: つなぎ口から道路を一方通行の向きどおりにたどり、たどり着けない建物と道路を返す
    // - /net/water_trace: 建物の近くの水道管の網をたどり、取水口・給水塔と排水口まで届くかを返す(#82)
    public static class NetworkApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/net/near"] = req => HttpBridge.OnMain(() => Near(req));
            routes["/net/reach"] = req => HttpBridge.OnMain(() => Reach(req));
            routes["/net/water_trace"] = req => HttpBridge.OnMain(() => WaterTrace(req));
        }

        // /net/near?x=..&z=..&radius=200&service=Road|Water|Electricity&limit=50
        private static string Near(HttpListenerRequest req)
        {
            var center = new Vector2(F(req, "x", 0f), F(req, "z", 0f));
            float radius = F(req, "radius", 200f);
            int limit = (int)F(req, "limit", 50f);
            string service = req.QueryString["service"];
            var nets = NetManager.instance;
            var sb = new StringBuilder("{\"ok\":true,\"segments\":[");
            int count = 0, total = 0;
            for (int i = 1; i < nets.m_segments.m_size; i++)
            {
                var seg = nets.m_segments.m_buffer[i];
                if ((seg.m_flags & NetSegment.Flags.Created) == 0 || seg.Info == null)
                {
                    continue;
                }

                if (!string.IsNullOrEmpty(service) && seg.Info.m_class.m_service.ToString() != service)
                {
                    continue;
                }

                // 中点だけでなく両端も見る。長い区間は中点が円の外でも、端が円に入ることがある
                var a = nets.m_nodes.m_buffer[seg.m_startNode].m_position;
                var b = nets.m_nodes.m_buffer[seg.m_endNode].m_position;
                var m = seg.m_middlePosition;
                if (Dist(a, center) > radius && Dist(b, center) > radius && Dist(m, center) > radius)
                {
                    continue;
                }

                total++;
                if (count >= limit)
                {
                    continue;
                }

                int forward, backward;
                CarLanes(ref seg, out forward, out backward);
                sb.Append(count == 0 ? "" : ",").Append("{\"segment\":").Append(i)
                  .Append(",\"prefab\":").Append(Json.Str(seg.Info.name))
                  .Append(",\"service\":").Append(Json.Str(seg.Info.m_class.m_service.ToString()))
                  .Append(",\"start\":{\"node\":").Append(seg.m_startNode).Append(",\"x\":").Append(R(a.x)).Append(",\"z\":").Append(R(a.z)).Append('}')
                  .Append(",\"end\":{\"node\":").Append(seg.m_endNode).Append(",\"x\":").Append(R(b.x)).Append(",\"z\":").Append(R(b.z)).Append('}')
                  .Append(",\"length\":").Append(R(Length(ref seg, a, b)));
                if (seg.Info.m_class.m_service == ItemClass.Service.Road)
                {
                    // 車が start→end に走れる車線の数と、end→start の数。片方が0なら一方通行
                    sb.Append(",\"carLanes\":{\"startToEnd\":").Append(forward).Append(",\"endToStart\":").Append(backward).Append('}');
                }

                sb.Append('}');
                count++;
            }

            return sb.Append("],\"total\":").Append(total).Append('}').ToString();
        }

        // /net/reach?x=..&z=..&radius=..&limit=10  x, z, radius を省くと街全体
        // つなぎ口の点(NetNode.Flags.Outside)から、車の車線の向きどおりに道路の区間をたどる。
        // 入れるか: つなぎ口から来て、その区間を走れるか。出られるか: その区間からつなぎ口へ行けるか。
        // 交差点で曲がれる向きの制限は見ない。ゲームの道順探しより甘い判定になる
        private static string Reach(HttpListenerRequest req)
        {
            bool area = req.QueryString["x"] != null && req.QueryString["z"] != null;
            var center = new Vector2(F(req, "x", 0f), F(req, "z", 0f));
            float radius = F(req, "radius", 500f);
            int limit = (int)F(req, "limit", 10f);

            var nets = NetManager.instance;
            var segs = nets.m_segments.m_buffer;
            var nodes = nets.m_nodes.m_buffer;
            int nodeCount = nodes.Length;

            // つなぎ口から行ける点(順にたどる)と、つなぎ口へ行ける点(逆にたどる)
            var fromOutside = new bool[nodeCount];
            var toOutside = new bool[nodeCount];
            var queue = new Queue<ushort>();
            int outsideNodes = 0;
            for (int i = 1; i < nodeCount; i++)
            {
                if ((nodes[i].m_flags & NetNode.Flags.Created) != 0 && (nodes[i].m_flags & NetNode.Flags.Outside) != 0
                    && HasRoad(ref nodes[i]))
                {
                    outsideNodes++;
                    fromOutside[i] = true;
                    toOutside[i] = true;
                }
            }

            Walk(fromOutside, queue, nodes, segs, true);
            Walk(toOutside, queue, nodes, segs, false);

            // 道路の区間ごとの判定
            int roads = 0, notEnterable = 0, notLeavable = 0;
            var badSegments = new List<ushort>();
            for (int i = 1; i < segs.Length; i++)
            {
                if (!IsRoad(ref segs[i]))
                {
                    continue;
                }

                if (area && Dist(segs[i].m_middlePosition, center) > radius)
                {
                    continue;
                }

                roads++;
                bool enter = CanEnter(ref segs[i], fromOutside);
                bool leave = CanLeave(ref segs[i], toOutside);
                if (!enter)
                {
                    notEnterable++;
                }

                if (!leave)
                {
                    notLeavable++;
                }

                if ((!enter || !leave) && badSegments.Count < limit)
                {
                    badSegments.Add((ushort)i);
                }
            }

            // 建物ごとの判定。建物が使う道路の区間(m_accessSegment)で決める
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            int buildings = 0, noRoad = 0, notReachable = 0, cannotLeave = 0;
            int underConstruction = 0, collapsed = 0, noRoadNeeded = 0;
            var badBuildings = new List<ushort>();
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null || bs[i].m_parentBuilding != 0
                    || MapApi.IsNetPart(ref bs[i]))
                {
                    continue;
                }

                if (area && Dist(bs[i].m_position, center) > radius)
                {
                    continue;
                }

                // ゲームは建物が建ち終わったとき(Completed)に道路を割り当てる(CommonBuildingAI.CheckRoadAccess)。
                // 建ち途中と、壊れた・焼けた建物(Collapsed。割り当てを0にする)は、道路がないのではないので別に数える(#82)。
                // 道路の要らない建物(風車など。RequireRoadAccess が false)も数えない
                if ((bs[i].m_flags & Building.Flags.Collapsed) != 0)
                {
                    collapsed++;
                    continue;
                }

                if ((bs[i].m_flags & Building.Flags.Completed) == 0)
                {
                    underConstruction++;
                    continue;
                }

                var pai = bs[i].Info.m_buildingAI as PlayerBuildingAI;
                if (pai != null && !pai.RequireRoadAccess())
                {
                    noRoadNeeded++;
                    continue;
                }

                buildings++;
                ushort access = bs[i].m_accessSegment;
                bool bad = false;
                if (access == 0 || !IsRoad(ref segs[access]))
                {
                    noRoad++;
                    bad = true;
                }
                else
                {
                    if (!CanEnter(ref segs[access], fromOutside))
                    {
                        notReachable++;
                        bad = true;
                    }

                    if (!CanLeave(ref segs[access], toOutside))
                    {
                        cannotLeave++;
                        bad = true;
                    }
                }

                if (bad && badBuildings.Count < limit)
                {
                    badBuildings.Add((ushort)i);
                }
            }

            var sb = new StringBuilder("{\"ok\":true");
            sb.Append(",\"outsideNodes\":").Append(outsideNodes);
            sb.Append(",\"roads\":{\"segments\":").Append(roads).Append(",\"notEnterable\":").Append(notEnterable)
              .Append(",\"notLeavable\":").Append(notLeavable).Append('}');
            sb.Append(",\"buildings\":{\"checked\":").Append(buildings).Append(",\"noRoad\":").Append(noRoad)
              .Append(",\"notReachable\":").Append(notReachable).Append(",\"cannotLeave\":").Append(cannotLeave)
              .Append(",\"skipped\":{\"underConstruction\":").Append(underConstruction).Append(",\"collapsed\":").Append(collapsed)
              .Append(",\"noRoadNeeded\":").Append(noRoadNeeded).Append("}}");

            sb.Append(",\"badBuildings\":[");
            for (int k = 0; k < badBuildings.Count; k++)
            {
                ushort id = badBuildings[k];
                ushort access = bs[id].m_accessSegment;
                bool road = access != 0 && IsRoad(ref segs[access]);
                sb.Append(k > 0 ? "," : "").Append("{\"id\":").Append(id)
                  .Append(",\"prefab\":").Append(Json.Str(bs[id].Info.name))
                  .Append(",\"x\":").Append(R(bs[id].m_position.x)).Append(",\"z\":").Append(R(bs[id].m_position.z))
                  .Append(",\"accessSegment\":").Append(road ? (int)access : 0)
                  .Append(",\"reachable\":").Append(road && CanEnter(ref segs[access], fromOutside) ? "true" : "false")
                  .Append(",\"canLeave\":").Append(road && CanLeave(ref segs[access], toOutside) ? "true" : "false").Append('}');
            }

            sb.Append("],\"badSegments\":[");
            for (int k = 0; k < badSegments.Count; k++)
            {
                ushort id = badSegments[k];
                var mid = segs[id].m_middlePosition;
                sb.Append(k > 0 ? "," : "").Append("{\"segment\":").Append(id)
                  .Append(",\"prefab\":").Append(Json.Str(segs[id].Info.name))
                  .Append(",\"x\":").Append(R(mid.x)).Append(",\"z\":").Append(R(mid.z))
                  .Append(",\"enterable\":").Append(CanEnter(ref segs[id], fromOutside) ? "true" : "false")
                  .Append(",\"leavable\":").Append(CanLeave(ref segs[id], toOutside) ? "true" : "false").Append('}');
            }

            return sb.Append("]}").ToString();
        }

        // 幅優先でたどる。forward=true なら車の向きどおり、false なら逆向き(つなぎ口へ行ける点を探す)
        private static void Walk(bool[] seen, Queue<ushort> queue, NetNode[] nodes, NetSegment[] segs, bool forward)
        {
            queue.Clear();
            for (int i = 1; i < seen.Length; i++)
            {
                if (seen[i])
                {
                    queue.Enqueue((ushort)i);
                }
            }

            while (queue.Count > 0)
            {
                ushort n = queue.Dequeue();
                for (int k = 0; k < 8; k++)
                {
                    ushort s = nodes[n].GetSegment(k);
                    if (s == 0 || !IsRoad(ref segs[s]))
                    {
                        continue;
                    }

                    ushort other = segs[s].m_startNode == n ? segs[s].m_endNode : segs[s].m_startNode;
                    bool ok = forward ? CanDrive(ref segs[s], n, other) : CanDrive(ref segs[s], other, n);
                    if (ok && !seen[other])
                    {
                        seen[other] = true;
                        queue.Enqueue(other);
                    }
                }
            }
        }

        // 区間 s を点 from から点 to へ車で走れるか
        private static bool CanDrive(ref NetSegment s, ushort from, ushort to)
        {
            int forward, backward;
            CarLanes(ref s, out forward, out backward);
            return s.m_startNode == from && s.m_endNode == to ? forward > 0 : backward > 0;
        }

        // つなぎ口から来て、この区間を走れるか
        private static bool CanEnter(ref NetSegment s, bool[] fromOutside)
        {
            return (fromOutside[s.m_startNode] && CanDrive(ref s, s.m_startNode, s.m_endNode))
                || (fromOutside[s.m_endNode] && CanDrive(ref s, s.m_endNode, s.m_startNode));
        }

        // この区間を走って、つなぎ口へ行けるか
        private static bool CanLeave(ref NetSegment s, bool[] toOutside)
        {
            return (toOutside[s.m_endNode] && CanDrive(ref s, s.m_startNode, s.m_endNode))
                || (toOutside[s.m_startNode] && CanDrive(ref s, s.m_endNode, s.m_startNode));
        }

        // 車が走れる車線の数。forward は start→end。Invert の区間は向きを入れ替える(NetSegment.CountLanes と同じ)
        private static void CarLanes(ref NetSegment s, out int forward, out int backward)
        {
            forward = 0;
            backward = 0;
            var lanes = s.Info != null ? s.Info.m_lanes : null;
            if (lanes == null)
            {
                return;
            }

            bool invert = (s.m_flags & NetSegment.Flags.Invert) != 0;
            foreach (var lane in lanes)
            {
                if ((lane.m_laneType & NetInfo.LaneType.Vehicle) == 0 || (lane.m_vehicleType & VehicleInfo.VehicleType.Car) == 0)
                {
                    continue;
                }

                var dir = invert ? NetInfo.InvertDirection(lane.m_finalDirection) : lane.m_finalDirection;
                if ((dir & NetInfo.Direction.Forward) != 0)
                {
                    forward++;
                }

                if ((dir & NetInfo.Direction.Backward) != 0)
                {
                    backward++;
                }
            }
        }

        // 区間の長さ(m)。ゲームの m_averageLength は車線の曲線の長さの平均で、交差点の角の分だけ短い。
        // 車線のない線(水道管、送電線)では0になるので、両端の水平の距離を使う(#82 の試運転で0が返った)
        private static float Length(ref NetSegment seg, Vector3 a, Vector3 b)
        {
            if (seg.m_averageLength > 0f)
            {
                return seg.m_averageLength;
            }

            return new Vector2(b.x - a.x, b.z - a.z).magnitude;
        }

        // /net/water_trace?x=..&z=..  点に近い建物から、近く(半径200m)の水道管の網をたどる。
        // #82 の試運転で、下水だけが来ない家が96人分出たが、管の網のどこで切れているかを探す手段がなかった。
        // 管の区間を点でつないで網に分け、網ごとに、取水口・給水塔(m_waterIntake > 0)と排水口(m_sewageOutlet > 0)の
        // つなぎ口の点を含むかを見る。施設のつなぎ口は Building.m_netNode の並びにある点。
        // ゲームの水の流れ(WaterManager の圧の計算)そのものではない。網がつながっているかだけを見る
        private static string WaterTrace(HttpListenerRequest req)
        {
            var center = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var nodes = NetManager.instance.m_nodes.m_buffer;
            var segs = NetManager.instance.m_segments.m_buffer;

            // 点に近い建物(100m以内)
            ushort target = 0;
            float bestD = 100f;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null || bs[i].m_parentBuilding != 0
                    || MapApi.IsNetPart(ref bs[i]))
                {
                    continue;
                }

                float d = Dist(bs[i].m_position, new Vector2(center.x, center.z));
                if (d < bestD)
                {
                    bestD = d;
                    target = (ushort)i;
                }
            }

            // 100m以内に建物がなければ、点そのもので調べる(#82。建物のまだない新しい街区で、管がつながったかを確かめるため)

            // 水の施設のつなぎ口の点 → 施設
            var facility = new Dictionary<ushort, ushort>();
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || !(bs[i].Info != null && bs[i].Info.m_buildingAI is WaterFacilityAI))
                {
                    continue;
                }

                ushort n = bs[i].m_netNode;
                int guard = 0;
                while (n != 0 && guard++ < 1024)
                {
                    facility[n] = (ushort)i;
                    n = nodes[n].m_nextBuildingNode;
                }
            }

            // 建物の近くの水道管の区間から、網をたどる
            var pos = target != 0 ? bs[target].m_position : center;
            var at = new Vector2(pos.x, pos.z);
            var seen = new HashSet<ushort>();
            var nets = new List<string>();
            int networks = 0;
            for (int i = 1; i < segs.Length; i++)
            {
                if (!IsPipe(ref segs[i]) || seen.Contains((ushort)i))
                {
                    continue;
                }

                var a = nodes[segs[i].m_startNode].m_position;
                var b = nodes[segs[i].m_endNode].m_position;
                float near = Mathf.Min(Mathf.Min(Dist(a, at), Dist(b, at)), Dist(segs[i].m_middlePosition, at));
                if (near > 200f)
                {
                    continue;
                }

                // 1つの網をたどる
                int count = 0;
                float nearest = near;
                var intakes = new List<ushort>();
                var outlets = new List<ushort>();
                var stack = new Stack<ushort>();
                var visitedNodes = new HashSet<ushort>();
                stack.Push((ushort)i);
                seen.Add((ushort)i);
                while (stack.Count > 0 && count < 50000)
                {
                    ushort sid = stack.Pop();
                    count++;
                    var sa = nodes[segs[sid].m_startNode].m_position;
                    var sb2 = nodes[segs[sid].m_endNode].m_position;
                    nearest = Mathf.Min(nearest, Mathf.Min(Mathf.Min(Dist(sa, at), Dist(sb2, at)), Dist(segs[sid].m_middlePosition, at)));
                    foreach (ushort nid in new[] { segs[sid].m_startNode, segs[sid].m_endNode })
                    {
                        if (!visitedNodes.Add(nid))
                        {
                            continue;
                        }

                        ushort fb;
                        if (facility.TryGetValue(nid, out fb))
                        {
                            var ai = (WaterFacilityAI)bs[fb].Info.m_buildingAI;
                            if (ai.m_waterIntake > 0 && !intakes.Contains(fb)) intakes.Add(fb);
                            if (ai.m_sewageOutlet > 0 && !outlets.Contains(fb)) outlets.Add(fb);
                        }

                        for (int k = 0; k < 8; k++)
                        {
                            ushort next = nodes[nid].GetSegment(k);
                            if (next != 0 && IsPipe(ref segs[next]) && seen.Add(next))
                            {
                                stack.Push(next);
                            }
                        }
                    }
                }

                networks++;
                nets.Add("{\"segments\":" + count + ",\"nearestPipe\":" + R(nearest)
                    + ",\"intakes\":" + Facilities(intakes) + ",\"outlets\":" + Facilities(outlets) + "}");
            }

            var sb = new StringBuilder("{\"ok\":true,\"point\":{\"x\":").Append(R(pos.x)).Append(",\"z\":").Append(R(pos.z)).Append('}');
            if (target != 0)
            {
                var tb = bs[target];
                bool e, w, sw;
                MapApi.Grid(ref bs[target], out e, out w, out sw);
                sb.Append(",\"building\":{\"id\":").Append(target)
                  .Append(",\"prefab\":").Append(Json.Str(tb.Info.name))
                  .Append(",\"x\":").Append(R(tb.m_position.x)).Append(",\"z\":").Append(R(tb.m_position.z))
                  .Append(",\"grid\":{\"electricity\":").Append(e ? "true" : "false").Append(",\"water\":").Append(w ? "true" : "false")
                  .Append(",\"sewage\":").Append(sw ? "true" : "false").Append("}}");
            }
            else
            {
                sb.Append(",\"building\":null");
            }
            // 網の届き具合(#82 の4年目の後)。水と下水は、施設から管の網を幅優先で広がる「パルス」で届く
            // (WaterManager.SimulationStepImpl)。256コマごとに、排水口は自分の点に吸う力(1回の処理で m_sewageOutlet × 稼働率)を
            // 置き、それが網を近い順に流れて、38.25m の格子のマスにたまった下水(負の圧)を埋めていく。力を使い切ると、
            // 遠いマスには届かず m_hasSewage が false になる。網がつながっていても、街の下水の量が排水口の力を超えると、
            // 網の端の家から下水が来なくなる。ここでは、その家のマスに今パルスが届いているかを返す
            bool cw, cs;
            byte pollution;
            WaterManager.instance.CheckWater(pos, out cw, out cs, out pollution);
            var d0 = DistrictManager.instance.m_districts.m_buffer[0];
            sb.Append(",\"cell\":{\"water\":").Append(cw ? "true" : "false").Append(",\"sewage\":").Append(cs ? "true" : "false")
              .Append(",\"waterPollution\":").Append(pollution).Append('}');
            sb.Append(",\"city\":{\"water\":{\"capacity\":").Append(d0.GetWaterCapacity()).Append(",\"used\":").Append(d0.GetWaterConsumption())
              .Append("},\"sewage\":{\"capacity\":").Append(d0.GetSewageCapacity()).Append(",\"used\":").Append(d0.GetSewageAccumulation())
              .Append("}}");
            // 近い網から並べる(nearestPipe の小さい順)
            nets.Sort((x, y) => NearestOf(x).CompareTo(NearestOf(y)));
            sb.Append(",\"networks\":[");
            for (int i = 0; i < nets.Count && i < 5; i++)
            {
                sb.Append(i > 0 ? "," : "").Append(nets[i]);
            }

            return sb.Append("],\"networkCount\":").Append(networks).Append('}').ToString();
        }

        private static bool IsPipe(ref NetSegment s)
        {
            return (s.m_flags & NetSegment.Flags.Created) != 0 && s.Info != null && s.Info.m_class.m_service == ItemClass.Service.Water;
        }

        // 網の JSON から nearestPipe の値を読む(並べ替え用)
        private static int NearestOf(string json)
        {
            int i = json.IndexOf("\"nearestPipe\":", StringComparison.Ordinal) + 14;
            int j = json.IndexOf(',', i);
            int v;
            int.TryParse(json.Substring(i, j - i), out v);
            return v;
        }

        private static string Facilities(List<ushort> ids)
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("[");
            for (int i = 0; i < ids.Count; i++)
            {
                var b = bs[ids[i]];
                sb.Append(i > 0 ? "," : "").Append("{\"id\":").Append(ids[i]).Append(",\"prefab\":").Append(Json.Str(b.Info.name))
                  .Append(",\"x\":").Append(R(b.m_position.x)).Append(",\"z\":").Append(R(b.m_position.z)).Append('}');
            }

            return sb.Append(']').ToString();
        }

        private static bool IsRoad(ref NetSegment s)
        {
            return (s.m_flags & NetSegment.Flags.Created) != 0 && s.Info != null && s.Info.m_class.m_service == ItemClass.Service.Road;
        }

        private static bool HasRoad(ref NetNode n)
        {
            var segs = NetManager.instance.m_segments.m_buffer;
            for (int k = 0; k < 8; k++)
            {
                ushort s = n.GetSegment(k);
                if (s != 0 && IsRoad(ref segs[s]))
                {
                    return true;
                }
            }

            return false;
        }

        private static float Dist(Vector3 p, Vector2 c)
        {
            return (new Vector2(p.x, p.z) - c).magnitude;
        }

        private static string R(float v)
        {
            return Mathf.RoundToInt(v).ToString(CultureInfo.InvariantCulture);
        }

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }
    }
}
