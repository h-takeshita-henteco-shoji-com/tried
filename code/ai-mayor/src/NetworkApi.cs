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
    public static class NetworkApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/net/near"] = req => HttpBridge.OnMain(() => Near(req));
            routes["/net/reach"] = req => HttpBridge.OnMain(() => Reach(req));
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
                  .Append(",\"length\":").Append(R(seg.m_averageLength));
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
              .Append(",\"notReachable\":").Append(notReachable).Append(",\"cannotLeave\":").Append(cannotLeave).Append('}');

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
