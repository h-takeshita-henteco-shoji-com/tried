using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 道路を太くする(種類を差し替える)、一方通行の向きを逆にする窓口(#82)。
    // 育てる期間で、幹線が2車線のまま混み具合100が続き、太くする道具がなかった。
    //
    // ゲームの道路の道具の「アップグレード」と同じ関数(NetTool.CreateNode)を呼ぶ。
    // - 中間の点(middlePoint)に元の区間を渡すと、ゲームは元の区間を消して同じ両端で作り直す
    // - 費用は「新しい種類の建設費 − 元の種類の建設費」。足りなければ断る(NotEnoughMoney)
    // - 高架・橋・トンネルは、ゲームが高さに合う種類(m_elevatedInfo、m_bridgeInfo など)を選ぶ
    // - 区画は保たれる。区間を消すと、その区画のまとまり(ZoneBlock)は ZoneManager.m_cachedBlocks に残る。
    //   同じ計算の中で作り直した区間の新しいまとまりは、残ったまとまりから区画の指定を写す(ZoneBlock.CalculateImplementation2)。
    //   太くした道路の下になったマスと、ぶつかった建物は、ゲームの道具と同じく消える
    public static class UpgradeApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/net/upgrade"] = req => Handle(req, false);
            routes["/net/reverse"] = req => Handle(req, true);
        }

        // POST /net/upgrade?prefab=Large%20Road&tolerance=20&pay=true  本文: "x1,z1;x2,z2;..."
        // POST /net/reverse?tolerance=20  本文: 同じ。一方通行の向きを逆にする(種類は変えない)
        private static string Handle(HttpListenerRequest req, bool reverse)
        {
            string prefab = req.QueryString["prefab"];
            NetInfo target = null;
            if (!reverse)
            {
                target = string.IsNullOrEmpty(prefab) ? null : PrefabCollection<NetInfo>.FindLoaded(prefab);
                if (target == null)
                {
                    return HttpBridge.Error("prefab not found: " + prefab + " (see /net/prefabs)");
                }
            }

            string body;
            using (var r = new StreamReader(req.InputStream, Encoding.UTF8))
            {
                body = r.ReadToEnd();
            }

            List<Vector3> line;
            try
            {
                line = NetApi.Parse(body);
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad points: " + e.Message);
            }

            if (line.Count < 2)
            {
                return HttpBridge.Error("need at least 2 points");
            }

            float tolerance = F(req, "tolerance", 20f);
            bool pay = req.QueryString["pay"] != "false";
            bool demolish = req.QueryString["demolish"] == "true";
            return HttpBridge.OnSimulation(() => Run(line, target, tolerance, pay, reverse, demolish), 30000);
        }

        private static string Run(List<Vector3> line, NetInfo target, float tolerance, bool pay, bool reverse, bool demolish)
        {
            var bm = BuildingManager.instance;
            var demolished = new StringBuilder();
            int demolishedCount = 0;
            var nm = NetManager.instance;
            var segs = nm.m_segments.m_buffer;
            var nodes = nm.m_nodes.m_buffer;

            // 先に対象の区間を集める(作り直すと番号が変わるため)
            var picked = new List<ushort>();
            for (int i = 1; i < segs.Length; i++)
            {
                if ((segs[i].m_flags & NetSegment.Flags.Created) == 0 || (segs[i].m_flags & NetSegment.Flags.Deleted) != 0 || segs[i].Info == null
                    || segs[i].Info.m_class.m_service != ItemClass.Service.Road)
                {
                    continue;
                }

                if (DistanceToLine(nodes[segs[i].m_startNode].m_position, line) <= tolerance
                    && DistanceToLine(nodes[segs[i].m_endNode].m_position, line) <= tolerance)
                {
                    picked.Add((ushort)i);
                }
            }

            int done = 0;
            long cost = 0;
            var skipped = new StringBuilder();
            var buffer = new FastList<NetTool.NodePosition>();
            foreach (ushort seg in picked)
            {
                var s = segs[seg];
                if ((s.m_flags & NetSegment.Flags.Created) == 0)
                {
                    Skip(skipped, seg, "already replaced");
                    continue;
                }

                // ゲームの道具と同じく、建物の一部の区間(Untouchable)は、向きを変えられるか差し替えられる印があるときだけ扱う
                if ((s.m_flags & NetSegment.Flags.Untouchable) != 0
                    && (s.m_flags2 & (NetSegment.Flags2.Invertible | NetSegment.Flags2.Upgradeable)) == 0)
                {
                    Skip(skipped, seg, "part of a building");
                    continue;
                }

                NetInfo info = reverse ? s.Info : target;
                if (!reverse && SameFamily(s.Info, target))
                {
                    Skip(skipped, seg, "already " + s.Info.name);
                    continue;
                }

                if (!reverse && !s.Info.m_netAI.CanUpgradeTo(target))
                {
                    Skip(skipped, seg, "cannot upgrade " + s.Info.name + " to " + target.name);
                    continue;
                }

                NetTool.ControlPoint start, middle, end;
                Points(seg, info, out start, out middle, out end);

                ushort node, newSeg;
                int c, rate;
                var errors = NetTool.CreateNode(info, start, middle, end, buffer, 1000, true, false, true, pay, false, reverse, 0,
                    out node, out newSeg, out c, out rate);
                if ((errors & ToolBase.ToolErrors.ObjectCollision) != 0)
                {
                    // ぶつかった建物を探す(#107)。太くした道路の幅で、区間の線に敷地が重なる建物
                    var pts = new List<Vector3> { start.m_position, middle.m_position, end.m_position };
                    var ids = NetApi.OverlapIds(info, pts, new bool[3], new bool[3]);
                    var bsb = bm.m_buildings.m_buffer;
                    var names = new StringBuilder();
                    bool onlyZoned = true;
                    foreach (var id in ids)
                    {
                        var bi = bsb[id].Info;
                        bool zoned = bi != null && bi.m_buildingAI is PrivateBuildingAI;
                        onlyZoned &= zoned;
                        names.Append(names.Length == 0 ? "" : " ").Append(id).Append('(').Append(bi != null ? bi.name : "?").Append(')');
                    }

                    // demolish=true なら、区画の建物だけを壊してやり直す。サービスの建物は壊さない(病院などを黙って壊さないため)
                    if (demolish && ids.Count > 0 && onlyZoned)
                    {
                        foreach (var id in ids)
                        {
                            demolished.Append(demolishedCount == 0 ? "" : ",").Append("{\"id\":").Append(id)
                              .Append(",\"prefab\":").Append(Json.Str(bsb[id].Info.name)).Append('}');
                            demolishedCount++;
                            bm.ReleaseBuilding(id);
                        }

                        errors = NetTool.CreateNode(info, start, middle, end, buffer, 1000, true, false, true, pay, false, reverse, 0,
                            out node, out newSeg, out c, out rate);
                    }
                    else if (ids.Count > 0)
                    {
                        Skip(skipped, seg, errors + " with buildings " + names + (demolish ? " (not demolished: a service building is in the way)" : " (pass demolish=true to demolish zoned buildings)"));
                        continue;
                    }
                }

                if (errors != ToolBase.ToolErrors.None)
                {
                    Skip(skipped, seg, errors.ToString());
                    continue;
                }

                // 太くした道路の下になる区画の建物は、ゲームが黙って壊す(#107 で確かめた。Large Road にすると6棟が消えた)。
                // 先に探し、demolish=false なら差し替えずに飛ばす。demolish=true なら差し替えて、壊れた建物を返す
                {
                    var pts2 = new List<Vector3> { start.m_position, middle.m_position, end.m_position };
                    var willGo = NetApi.OverlapIds(info, pts2, new bool[3], new bool[3]);
                    if (willGo.Count > 0 && !demolish)
                    {
                        var list = new StringBuilder();
                        foreach (var id in willGo)
                        {
                            var bi = bm.m_buildings.m_buffer[id].Info;
                            list.Append(list.Length == 0 ? "" : " ").Append(id).Append('(').Append(bi != null ? bi.name : "?").Append(')');
                        }

                        Skip(skipped, seg, "would demolish buildings " + list + " (pass demolish=true to widen anyway)");
                        continue;
                    }

                    foreach (var id in willGo)
                    {
                        var bi = bm.m_buildings.m_buffer[id].Info;
                        demolished.Append(demolishedCount == 0 ? "" : ",").Append("{\"id\":").Append(id)
                          .Append(",\"prefab\":").Append(Json.Str(bi != null ? bi.name : null)).Append('}');
                        demolishedCount++;
                    }
                }

                // 本番の呼び出しは費用を0で返す(払うのは中で行う)。試しの呼び出しで出た額を使う(#82。戻り値の cost が0だった)
                int testCost = c;
                errors = NetTool.CreateNode(info, start, middle, end, buffer, 1000, false, false, true, pay, false, reverse, 0,
                    out node, out newSeg, out c, out rate);
                if (errors != ToolBase.ToolErrors.None)
                {
                    Skip(skipped, seg, errors.ToString());
                    continue;
                }

                done++;
                cost += Math.Max(c, testCost);
            }

            return "{\"ok\":true,\"matched\":" + picked.Count + ",\"" + (reverse ? "reversed" : "upgraded") + "\":" + done
                + ",\"skipped\":[" + skipped + "],\"demolishedBuildings\":[" + demolished + "],\"cost\":" + cost / 100 + ",\"paid\":" + (pay ? "true" : "false")
                + ",\"zonesKept\":true}";
        }

        // ゲームの道具が区間を指したときと同じ3つの点(NetTool の raycast の upgrade の処理)
        private static void Points(ushort seg, NetInfo info, out NetTool.ControlPoint start, out NetTool.ControlPoint middle, out NetTool.ControlPoint end)
        {
            var nm = NetManager.instance;
            var s = nm.m_segments.m_buffer[seg];
            start = Point(s.m_startNode, s.m_startDirection);
            end = Point(s.m_endNode, -s.m_endDirection);
            middle = default(NetTool.ControlPoint);
            middle.m_node = 0;
            middle.m_segment = seg;
            middle.m_position = start.m_position + start.m_direction * (info.GetMinNodeDistance() + 1f);
            middle.m_direction = start.m_direction;
            middle.m_elevation = Mathf.Lerp(start.m_elevation, end.m_elevation, 0.5f);
            middle.m_outside = false;
        }

        private static NetTool.ControlPoint Point(ushort node, Vector3 dir)
        {
            var n = NetManager.instance.m_nodes.m_buffer[node];
            var p = default(NetTool.ControlPoint);
            p.m_node = node;
            p.m_segment = 0;
            p.m_position = n.m_position;
            p.m_direction = dir;
            p.m_elevation = n.m_elevation;
            if (n.Info != null && n.Info.m_netAI.IsUnderground())
            {
                p.m_elevation = -p.m_elevation;
            }

            p.m_outside = (n.m_flags & NetNode.Flags.Outside) != 0;
            return p;
        }

        // 同じ種類か(橋・高架・トンネルの種類も、元の種類と同じとみなす)
        private static bool SameFamily(NetInfo a, NetInfo b)
        {
            if (a == b)
            {
                return true;
            }

            foreach (var f in new[] { "m_elevatedInfo", "m_bridgeInfo", "m_slopeInfo", "m_tunnelInfo" })
            {
                var field = b.m_netAI.GetType().GetField(f);
                if (field != null && field.GetValue(b.m_netAI) as NetInfo == a)
                {
                    return true;
                }
            }

            return false;
        }

        private static void Skip(StringBuilder sb, ushort seg, string reason)
        {
            sb.Append(sb.Length > 0 ? "," : "").Append("{\"segment\":").Append(seg).Append(",\"reason\":").Append(Json.Str(reason)).Append('}');
        }

        // 点から、折れ線までの水平の距離(NetApi の同名の処理と同じ)
        private static float DistanceToLine(Vector3 p, List<Vector3> line)
        {
            float best = float.MaxValue;
            p.y = 0f;
            for (int i = 1; i < line.Count; i++)
            {
                var a = line[i - 1];
                var b = line[i];
                a.y = 0f;
                b.y = 0f;
                var ab = b - a;
                float t = ab.sqrMagnitude > 0f ? Mathf.Clamp01(Vector3.Dot(p - a, ab) / ab.sqrMagnitude) : 0f;
                best = Mathf.Min(best, Vector3.Distance(p, a + ab * t));
            }

            return best;
        }

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }
    }
}
