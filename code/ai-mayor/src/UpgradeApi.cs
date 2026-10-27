using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Reflection;
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
            // test=true なら、差し替えられるかを確かめて、差し替えずに返す(#105。局と市長が、建てる前に試す)
            bool test = req.QueryString["test"] == "true";
            var assumed = test ? Assumed.Parse(req) : null;
            return HttpBridge.OnSimulation(() => assumed != null ? assumed.Apply(() => Run(line, target, tolerance, pay, reverse, demolish, test, assumed)) : Run(line, target, tolerance, pay, reverse, demolish, test, assumed), 30000);
        }

        private static string Run(List<Vector3> line, NetInfo target, float tolerance, bool pay, bool reverse, bool demolish, bool test, Assumed assumed)
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
                    || segs[i].Info.m_class.m_service != ItemClass.Service.Road
                    || (assumed != null && assumed.Removed(i, segs[i])))
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
                // ゲームが断ったとき、ぶつかった相手(道具の画面で赤く塗られるもの)を返す(#105)
                string coll = null;
                if ((errors & ToolBase.ToolErrors.ObjectCollision) != 0)
                {
                    bool blocking;
                    coll = Colliding(assumed, out blocking);
                    // 試しで、断る相手がすべて「壊したもの」なら、ぶつからないとみなす(#105。壊してから建てる工事を試す)
                    if (assumed != null && assumed.Any && !blocking)
                    {
                        errors &= ~ToolBase.ToolErrors.ObjectCollision;
                    }
                }

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
                    if (test && demolish && ids.Count > 0 && onlyZoned)
                    {
                        // 試し: 壊さずに、壊れる建物と、差し替えられる見込みを返す
                        foreach (var id in ids)
                        {
                            demolished.Append(demolishedCount == 0 ? "" : ",").Append("{\"id\":").Append(id)
                              .Append(",\"prefab\":").Append(Json.Str(bsb[id].Info.name)).Append('}');
                            demolishedCount++;
                        }

                        done++;
                        cost += c;
                        continue;
                    }

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
                        Skip(skipped, seg, errors + " with buildings " + names + (demolish ? " (not demolished: a service building is in the way)" : " (pass demolish=true to demolish zoned buildings)"), coll);
                        continue;
                    }
                }

                if (errors != ToolBase.ToolErrors.None)
                {
                    if ((errors & ToolBase.ToolErrors.ObjectCollision) != 0)
                    {
                        coll = Colliding();
                    }

                    Skip(skipped, seg, errors.ToString(), coll);
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

                if (test)
                {
                    done++;
                    cost += c;
                    continue;
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

            return "{\"ok\":true" + (test ? ",\"test\":true,\"changed\":false" : "") + ",\"matched\":" + picked.Count + ",\"" + (reverse ? "reversed" : "upgraded") + "\":" + done
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

        private static void Skip(StringBuilder sb, ushort seg, string reason, string colliding = null)
        {
            sb.Append(sb.Length > 0 ? "," : "").Append("{\"segment\":").Append(seg).Append(",\"reason\":").Append(Json.Str(reason));
            if (colliding != null)
            {
                sb.Append(",\"colliding\":").Append(colliding);
            }

            sb.Append('}');
        }

        private static readonly FieldInfo CollidingSegments = typeof(ToolController).GetField("m_collidingSegments2", BindingFlags.Instance | BindingFlags.NonPublic);
        private static readonly FieldInfo CollidingBuildings = typeof(ToolController).GetField("m_collidingBuildings2", BindingFlags.Instance | BindingFlags.NonPublic);
        private static readonly MethodInfo ImportantBuilding = typeof(BuildingTool).GetMethod("IsImportantBuilding", BindingFlags.Static | BindingFlags.NonPublic,
            null, new[] { typeof(BuildingInfo), typeof(ushort) }, null);

        // 直前の NetTool.CreateNode(試し)が残した、ぶつかった区間と建物の印(ToolController が赤く塗るのに使う)。
        // blocks は、ゲームが取り除かずに断る相手か(NetTool.CheckCollidingSegments と BuildingTool.CheckCollidingBuildings と同じ決まり)。
        // blocks=false の相手は、ゲームが作るときに取り除く
        internal static string Colliding()
        {
            bool blocking;
            return Colliding(null, out blocking);
        }

        // assumed: 試し(test=true)で「壊したものとして」扱う区間と建物。その相手は blocks にせず assumed=true を付ける。
        // blocking: assumed を除いて、断る相手(blocks=true)が残るか
        internal static string Colliding(Assumed assumed, out bool blocking)
        {
            var props = ToolManager.instance.m_properties;
            var segMask = CollidingSegments != null ? CollidingSegments.GetValue(props) as ulong[] : null;
            var bldMask = CollidingBuildings != null ? CollidingBuildings.GetValue(props) as ulong[] : null;
            return CollidingJson(segMask, bldMask, assumed, out blocking);
        }

        // ぶつかった区間と建物の印から、相手の一覧を JSON にする(建物を置く道具、線を引く道具でも使う)
        internal static string CollidingJson(ulong[] segMask, ulong[] bldMask)
        {
            bool blocking;
            return CollidingJson(segMask, bldMask, null, out blocking);
        }

        internal static string CollidingJson(ulong[] segMask, ulong[] bldMask, Assumed assumed, out bool blocking)
        {
            blocking = false;
            var segs = NetManager.instance.m_segments.m_buffer;
            var blds = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("{\"segments\":[");
            int n = 0;
            foreach (int id in Bits(segMask))
            {
                var info = segs[id].Info;
                if (info == null)
                {
                    continue;
                }

                bool gone = assumed != null && assumed.Removed(id, segs[id]);
                bool blocks = !gone && ((ItemClass.GetPublicServiceIndex(info.m_class.m_service) != -1 && !info.m_autoRemove)
                    || (segs[id].m_flags & NetSegment.Flags.Untouchable) != 0);
                blocking |= blocks;
                var p = segs[id].m_middlePosition;
                sb.Append(n++ == 0 ? "" : ",").Append("{\"segment\":").Append(id).Append(",\"prefab\":").Append(Json.Str(info.name))
                  .Append(",\"service\":").Append(Json.Str(info.m_class.m_service.ToString()))
                  .Append(",\"x\":").Append(Mathf.RoundToInt(p.x)).Append(",\"z\":").Append(Mathf.RoundToInt(p.z))
                  .Append(",\"blocks\":").Append(blocks ? "true" : "false").Append(gone ? ",\"assumedRemoved\":true" : "").Append('}');
            }

            sb.Append("],\"buildings\":[");
            n = 0;
            foreach (int id in Bits(bldMask))
            {
                var info = blds[id].Info;
                if (info == null || info.IgnoreBuildingCollision())
                {
                    continue;
                }

                bool gone = assumed != null && assumed.RemovedBuilding(id);
                bool blocks = !gone && ((blds[id].m_flags & Building.Flags.Untouchable) != 0
                    || (ImportantBuilding != null && (bool)ImportantBuilding.Invoke(null, new object[] { info, (ushort)id })));
                blocking |= blocks;
                var p = blds[id].m_position;
                sb.Append(n++ == 0 ? "" : ",").Append("{\"id\":").Append(id).Append(",\"prefab\":").Append(Json.Str(info.name))
                  .Append(",\"x\":").Append(Mathf.RoundToInt(p.x)).Append(",\"z\":").Append(Mathf.RoundToInt(p.z))
                  .Append(",\"blocks\":").Append(blocks ? "true" : "false").Append(gone ? ",\"assumedRemoved\":true" : "").Append('}');
            }

            return sb.Append("]}").ToString();
        }

        internal static IEnumerable<int> Bits(ulong[] mask)
        {
            if (mask == null)
            {
                yield break;
            }

            for (int i = 0; i < mask.Length; i++)
            {
                if (mask[i] == 0)
                {
                    continue;
                }

                for (int j = 0; j < 64; j++)
                {
                    if ((mask[i] & (1UL << j)) != 0)
                    {
                        yield return (i << 6) | j;
                    }
                }
            }
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

    // 試し(test=true)で「壊したものとして」扱う区間と建物(#105)。
    // 壊してから建てる工事は、2つめの操作を今の街では試せない。壊す相手をここに入れると、その相手とのぶつかりを除いて判定する。
    // 壊した区間の両端の点は残るものとし、建物に付いた線(建物の一部の区間)は、その建物を壊したものとして除く。
    // ゲームの判定そのものは変えない。本番では、先に壊す操作(取り壊しの議決が要る)をしてから建てる
    internal sealed class Assumed
    {
        public readonly HashSet<int> Segments = new HashSet<int>();
        public readonly HashSet<int> Buildings = new HashSet<int>();

        public bool Any
        {
            get { return Segments.Count > 0 || Buildings.Count > 0; }
        }

        public bool Removed(int segment, NetSegment s)
        {
            if (Segments.Contains(segment))
            {
                return true;
            }

            // 建物の一部の区間は、その建物を壊せば消える
            if ((s.m_flags & NetSegment.Flags.Untouchable) != 0 && Buildings.Count > 0)
            {
                var nodes = NetManager.instance.m_nodes.m_buffer;
                ushort b1 = NetNode.FindOwnerBuilding(s.m_startNode, 32f);
                ushort b2 = NetNode.FindOwnerBuilding(s.m_endNode, 32f);
                return Buildings.Contains(b1) || Buildings.Contains(b2);
            }

            return false;
        }

        public bool RemovedBuilding(int building)
        {
            return Buildings.Contains(building);
        }

        // 差し替えたものとする区間と、その道路の種類(#125)。壊す→隣を差し替える→引き直す、の連続の試しに使う
        public readonly Dictionary<int, string> Upgrades = new Dictionary<int, string>();

        // 地形を変えたものとする指定(書式は TerrainGameApi.ApplyVirtual)
        public readonly List<string> Terrain = new List<string>();

        public bool HasVirtual
        {
            get { return Segments.Count > 0 || Buildings.Count > 0 || Upgrades.Count > 0 || Terrain.Count > 0; }
        }

        // 壊したものとした区間を両端の点から外し、差し替えたものとした区間の種類を書き換える(#125)。
        // ゲームの TooShort の判定は、点につながる区間の幅で角の位置を決めるため、壊した扱いを渡すだけでは届かない。
        // 戻す動作の並びを返すので、判定のあとに必ず Restore する。シミュレーションのスレッドで呼ぶ(判定の間に街が進まない)
        public List<Action> Detach()
        {
            var undo = new List<Action>();
            var nm = NetManager.instance;
            var segs = nm.m_segments.m_buffer;
            var nodes = nm.m_nodes.m_buffer;
            // 壊す建物の一部の区間(駅の線路など)も、壊したものとして外す
            var gone = new HashSet<int>(Segments);
            if (Buildings.Count > 0)
            {
                for (int i = 1; i < segs.Length; i++)
                {
                    if ((segs[i].m_flags & NetSegment.Flags.Created) != 0 && Removed(i, segs[i]))
                    {
                        gone.Add(i);
                    }
                }
            }

            var touched = new HashSet<ushort>();
            foreach (var id in gone)
            {
                if (id <= 0 || id >= segs.Length || (segs[id].m_flags & NetSegment.Flags.Created) == 0)
                {
                    continue;
                }

                foreach (var node in new[] { segs[id].m_startNode, segs[id].m_endNode })
                {
                    for (int slot = 0; slot < 8; slot++)
                    {
                        if (nodes[node].GetSegment(slot) == id)
                        {
                            touched.Add(node);
                            int s = slot;
                            ushort nd = node;
                            ushort sg = (ushort)id;
                            SetSlot(ref nodes[nd], s, 0);
                            undo.Add(() => SetSlot(ref NetManager.instance.m_nodes.m_buffer[nd], s, sg));
                        }
                    }
                }
            }

            // 区間を外した点の印(End、Middle、Bend、Junction)を、残った区間の数と向きに合わせる。
            // ゲームは壊した後に点を更新して印を決める。印が古いままだと、角の計算が壊した後の街と食い違う(#125)
            foreach (var node in touched)
            {
                SetNodeFlags(node, undo);
            }

            foreach (var kv in Upgrades)
            {
                int id = kv.Key;
                var target = PrefabCollection<NetInfo>.FindLoaded(kv.Value);
                if (target == null || id <= 0 || id >= segs.Length || (segs[id].m_flags & NetSegment.Flags.Created) == 0
                    || gone.Contains(id))
                {
                    continue;
                }

                ushort before = segs[id].m_infoIndex;
                segs[id].m_infoIndex = (ushort)target.m_prefabDataIndex;
                ushort sg = (ushort)id;
                undo.Add(() => NetManager.instance.m_segments.m_buffer[sg].m_infoIndex = before);
            }

            return undo;
        }

        private static void SetNodeFlags(ushort node, List<Action> undo)
        {
            var nm = NetManager.instance;
            var nodes = nm.m_nodes.m_buffer;
            var segs = nm.m_segments.m_buffer;
            var dirs = new List<Vector3>();
            for (int i = 0; i < 8; i++)
            {
                ushort seg = nodes[node].GetSegment(i);
                if (seg == 0)
                {
                    continue;
                }

                var d = segs[seg].m_startNode == node ? segs[seg].m_startDirection : segs[seg].m_endDirection;
                dirs.Add(d);
            }

            if (dirs.Count == 0)
            {
                return;
            }

            const NetNode.Flags shape = NetNode.Flags.End | NetNode.Flags.Middle | NetNode.Flags.Bend | NetNode.Flags.Junction;
            NetNode.Flags want;
            if (dirs.Count == 1)
            {
                want = NetNode.Flags.End;
            }
            else if (dirs.Count == 2)
            {
                want = dirs[0].x * dirs[1].x + dirs[0].z * dirs[1].z < -0.999f ? NetNode.Flags.Middle : NetNode.Flags.Bend;
            }
            else
            {
                want = NetNode.Flags.Junction;
            }

            var before = nodes[node].m_flags;
            nodes[node].m_flags = (before & ~shape) | want;
            ushort nd = node;
            undo.Add(() => NetManager.instance.m_nodes.m_buffer[nd].m_flags = before);
        }

        // 地形を変えたものとして高さを書き換える。高さを先に読む判定(道路の点の高さなど)の前に呼ぶ。戻す動作の並びを返す
        public List<Action> ApplyTerrain()
        {
            var undo = new List<Action>();
            foreach (var spec in Terrain)
            {
                TerrainGameApi.ApplyVirtual(spec, undo);
            }

            return undo;
        }

        // 地形と、壊した・差し替えた区間を、まとめて反映する。戻す動作の並びを返す
        public List<Action> Begin()
        {
            var undo = ApplyTerrain();
            undo.AddRange(Detach());
            return undo;
        }

        // 判定のあいだだけ、壊した・差し替えたものとして街を見せる。戻す動作は必ず行う
        public string Apply(Func<string> work)
        {
            var undo = HasVirtual ? Begin() : null;
            try
            {
                return work();
            }
            finally
            {
                if (undo != null)
                {
                    Restore(undo);
                }
            }
        }

        public static void Restore(List<Action> undo)
        {
            for (int i = undo.Count - 1; i >= 0; i--)
            {
                undo[i]();
            }
        }

        private static void SetSlot(ref NetNode node, int slot, ushort segment)
        {
            switch (slot)
            {
                case 0: node.m_segment0 = segment; break;
                case 1: node.m_segment1 = segment; break;
                case 2: node.m_segment2 = segment; break;
                case 3: node.m_segment3 = segment; break;
                case 4: node.m_segment4 = segment; break;
                case 5: node.m_segment5 = segment; break;
                case 6: node.m_segment6 = segment; break;
                default: node.m_segment7 = segment; break;
            }
        }

        public static Assumed Parse(HttpListenerRequest req)
        {
            var a = new Assumed();
            Fill(a.Segments, req.QueryString["assumeRemovedSegments"]);
            Fill(a.Buildings, req.QueryString["assumeRemovedBuildings"]);
            string terrain = req.QueryString["assumeTerrain"];
            if (!string.IsNullOrEmpty(terrain))
            {
                foreach (var spec in terrain.Split('|'))
                {
                    if (spec.Trim().Length > 0)
                    {
                        a.Terrain.Add(spec.Trim());
                    }
                }
            }

            // "区間の番号:道路の名前,..." (例 3334:Small 4 Lane Road)
            string up = req.QueryString["assumeUpgraded"];
            if (!string.IsNullOrEmpty(up))
            {
                foreach (var part in up.Split(','))
                {
                    int colon = part.IndexOf(':');
                    int id;
                    if (colon > 0 && int.TryParse(part.Substring(0, colon).Trim(), NumberStyles.Integer, CultureInfo.InvariantCulture, out id) && id > 0)
                    {
                        a.Upgrades[id] = part.Substring(colon + 1).Trim();
                    }
                }
            }

            return a;
        }

        private static void Fill(HashSet<int> set, string csv)
        {
            if (string.IsNullOrEmpty(csv))
            {
                return;
            }

            foreach (var part in csv.Split(','))
            {
                int v;
                if (int.TryParse(part.Trim(), NumberStyles.Integer, CultureInfo.InvariantCulture, out v) && v > 0)
                {
                    set.Add(v);
                }
            }
        }
    }
}
