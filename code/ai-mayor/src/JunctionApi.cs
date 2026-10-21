using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Reflection;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 交差点の信号と、譲れ(一時停止)の標識の窓口(#82)。
    // ゲーム本編の交通の情報画面の「交差点」で、プレイヤーが交差点のボタンを押す操作(RoadBaseAI.ClickNodeButton)と同じ処理をする。
    // - 信号: ボタン -1。TrafficLights を入れ替え、CustomTrafficLights(人が決めた印)を付けて、点の印を計算し直す
    // - 譲れの標識: ボタン 1〜8(区間ごと)。区間の YieldStart / YieldEnd を入れ替え、車線を計算し直す
    // ゲームの処理は、情報画面が開いているときだけ受け付ける。ここでは画面を開かずに、同じ中身を直接行う
    public static class JunctionApi
    {
        private const float SearchRadius = 40f;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/junction"] = req => HttpBridge.OnMain(() => Info(req));
            routes["/junction/lights"] = req => HttpBridge.OnSimulation(() => Lights(req));
            routes["/junction/stop"] = req => HttpBridge.OnSimulation(() => Yield(req));
        }

        // /junction?x=..&z=..  点に近い交差点の様子
        private static string Info(HttpListenerRequest req)
        {
            ushort node = FindJunction(req);
            if (node == 0)
            {
                return HttpBridge.Error("no road junction within " + SearchRadius + "m");
            }

            return "{\"ok\":true," + NodeJson(node).Substring(1);
        }

        // /junction/lights?x=..&z=..&active=true|false  信号を付ける・外す
        private static string Lights(HttpListenerRequest req)
        {
            ushort node = FindJunction(req);
            if (node == 0)
            {
                return HttpBridge.Error("no road junction within " + SearchRadius + "m");
            }

            var nodes = NetManager.instance.m_nodes.m_buffer;
            var ai = nodes[node].Info.m_netAI as RoadBaseAI;
            bool want = req.QueryString["active"] != "false";
            bool has = (nodes[node].m_flags & NetNode.Flags.TrafficLights) != 0;
            if (want != has)
            {
                if (want && !Can(ai, "CanEnableTrafficLights", node))
                {
                    return "{\"ok\":false,\"error\":\"traffic lights cannot be enabled at this junction (the game does not allow it: road meets a railway, a one-way exit only, or too few roads)\",\"junction\":"
                        + NodeJson(node) + "}";
                }

                // ゲームの ClickNodeButton(-1) と同じ
                nodes[node].m_flags ^= NetNode.Flags.TrafficLights;
                nodes[node].m_flags |= NetNode.Flags.CustomTrafficLights;
                ai.UpdateNodeFlags(node, ref nodes[node]);
                NetManager.instance.UpdateNodeRenderer(node, true);
            }

            return "{\"ok\":true,\"changed\":" + (want != has ? "true" : "false") + ",\"junction\":" + NodeJson(node) + "}";
        }

        // /junction/stop?x=..&z=..&segment=..&active=true|false  交差点に入る区間に、譲れの標識を付ける・外す。
        // ゲーム本編の標識は「譲れ(Yield)」で、止まって譲る。信号のある交差点や、一方通行の出口だけの交差点には付けられない
        private static string Yield(HttpListenerRequest req)
        {
            ushort node = FindJunction(req);
            if (node == 0)
            {
                return HttpBridge.Error("no road junction within " + SearchRadius + "m");
            }

            int segInt;
            int.TryParse(req.QueryString["segment"] ?? "0", NumberStyles.Integer, CultureInfo.InvariantCulture, out segInt);
            var nm = NetManager.instance;
            var nodes = nm.m_nodes.m_buffer;
            ushort seg = 0;
            for (int i = 0; i < 8; i++)
            {
                if (nodes[node].GetSegment(i) == segInt && segInt != 0)
                {
                    seg = (ushort)segInt;
                }
            }

            if (seg == 0)
            {
                return "{\"ok\":false,\"error\":\"segment is not one of this junction's roads (see /junction)\",\"junction\":" + NodeJson(node) + "}";
            }

            var ai = nodes[node].Info.m_netAI as RoadBaseAI;
            if (!Can(ai, "CanEnableYield", node))
            {
                return "{\"ok\":false,\"error\":\"yield signs cannot be set here (the junction has traffic lights, is a one-way exit only, or has too few roads)\",\"junction\":"
                    + NodeJson(node) + "}";
            }

            var segs = nm.m_segments.m_buffer;
            if ((segs[seg].Info.m_vehicleTypes & (VehicleInfo.VehicleType.Car | VehicleInfo.VehicleType.Tram | VehicleInfo.VehicleType.Trolleybus)) == 0)
            {
                return "{\"ok\":false,\"error\":\"this segment has no car lanes\",\"junction\":" + NodeJson(node) + "}";
            }

            // ゲームの ClickNodeButton(1〜8) と同じ。この交差点の側の端の印を入れ替える
            var flag = segs[seg].m_startNode == node ? NetSegment.Flags.YieldStart : NetSegment.Flags.YieldEnd;
            bool want = req.QueryString["active"] != "false";
            bool has = (segs[seg].m_flags & flag) != 0;
            if (want != has)
            {
                segs[seg].m_flags ^= flag;
                segs[seg].UpdateLanes(seg, true);
            }

            return "{\"ok\":true,\"changed\":" + (want != has ? "true" : "false") + ",\"junction\":" + NodeJson(node) + "}";
        }

        // ゲームの判定(RoadBaseAI の private な CanEnableTrafficLights / CanEnableYield)を呼ぶ
        private static bool Can(RoadBaseAI ai, string method, ushort node)
        {
            if (ai == null)
            {
                return false;
            }

            var m = typeof(RoadBaseAI).GetMethod(method, BindingFlags.Instance | BindingFlags.NonPublic);
            if (m == null)
            {
                return false;
            }

            var args = new object[] { node, NetManager.instance.m_nodes.m_buffer[node] };
            return (bool)m.Invoke(ai, args);
        }

        // 点 (x, z) から40m以内でいちばん近い、道路の交差点の点。なければ 0
        private static ushort FindJunction(HttpListenerRequest req)
        {
            var pos = new Vector3(F(req, "x"), 0f, F(req, "z"));
            var nodes = NetManager.instance.m_nodes.m_buffer;
            ushort best = 0;
            float bestD = SearchRadius * SearchRadius;
            for (int i = 1; i < nodes.Length; i++)
            {
                if ((nodes[i].m_flags & NetNode.Flags.Created) == 0 || (nodes[i].m_flags & NetNode.Flags.Junction) == 0
                    || nodes[i].Info == null || !(nodes[i].Info.m_netAI is RoadBaseAI))
                {
                    continue;
                }

                var d = nodes[i].m_position - pos;
                d.y = 0f;
                if (d.sqrMagnitude < bestD)
                {
                    bestD = d.sqrMagnitude;
                    best = (ushort)i;
                }
            }

            return best;
        }

        // 交差点の JSON。信号の有無、人が決めた信号か、付け外しできるか、入る区間ごとの譲れの標識
        private static string NodeJson(ushort node)
        {
            var nm = NetManager.instance;
            var nodes = nm.m_nodes.m_buffer;
            var segs = nm.m_segments.m_buffer;
            var ai = nodes[node].Info.m_netAI as RoadBaseAI;
            var flags = nodes[node].m_flags;
            bool lights = (flags & NetNode.Flags.TrafficLights) != 0;
            var sb = new StringBuilder("{\"node\":").Append(node)
                .Append(",\"x\":").Append(Mathf.RoundToInt(nodes[node].m_position.x))
                .Append(",\"z\":").Append(Mathf.RoundToInt(nodes[node].m_position.z))
                .Append(",\"trafficLights\":").Append(lights ? "true" : "false")
                .Append(",\"customLights\":").Append((flags & NetNode.Flags.CustomTrafficLights) != 0 ? "true" : "false")
                .Append(",\"canEnableLights\":").Append(Can(ai, "CanEnableTrafficLights", node) ? "true" : "false")
                .Append(",\"canSetYield\":").Append(Can(ai, "CanEnableYield", node) ? "true" : "false")
                .Append(",\"roads\":[");
            bool first = true;
            for (int i = 0; i < 8; i++)
            {
                ushort s = nodes[node].GetSegment(i);
                if (s == 0)
                {
                    continue;
                }

                bool atStart = segs[s].m_startNode == node;
                var dir = atStart ? segs[s].m_startDirection : segs[s].m_endDirection;
                float bearing = (Mathf.Atan2(dir.x, dir.z) * Mathf.Rad2Deg + 360f) % 360f;
                var flag = atStart ? NetSegment.Flags.YieldStart : NetSegment.Flags.YieldEnd;
                bool cars = (segs[s].Info.m_vehicleTypes & (VehicleInfo.VehicleType.Car | VehicleInfo.VehicleType.Tram | VehicleInfo.VehicleType.Trolleybus)) != 0;
                sb.Append(first ? "" : ",").Append("{\"segment\":").Append(s)
                  .Append(",\"prefab\":").Append(Json.Str(segs[s].Info.name))
                  .Append(",\"bearing\":").Append(Mathf.RoundToInt(bearing))
                  .Append(",\"cars\":").Append(cars ? "true" : "false")
                  .Append(",\"yield\":").Append((segs[s].m_flags & flag) != 0 ? "true" : "false").Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        private static float F(HttpListenerRequest req, string key)
        {
            float v;
            return float.TryParse(req.QueryString[key], NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : 0f;
        }
    }
}
