using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using ColossalFramework;
using ColossalFramework.Math;
using UnityEngine;

namespace AIMayor
{
    // 線を引く窓口: 道路・線路・高速道路など(ゲームでは「ネットワーク」と呼ぶ)を、座標の並びに沿って作る。
    // 座標はゲーム上のメートル。x が東、z が北。
    public static class NetApi
    {
        private const float MaxSegment = 80f; // 1区間の長さの上限。長いと曲がりきれず見た目が崩れる
        private const float SnapDistance = 12f; // 端点の近くに既存の点があれば、そこにつなぐ
        private const float SplitDistance = 16f; // 点がなくても区間があれば、区間を途中で分けてつなぐ(交差点を作る)

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/net/prefabs"] = req => HttpBridge.OnMain(Prefabs);
            routes["/net/build"] = Build;
            routes["/net/remove"] = Remove;
            // /net/remove_all?prefab=Train%20Track  準備用。その種類の線をすべて消す。MCP の道具にはしない
            routes["/net/remove_all"] = RemoveAll;
            routes["/bulldoze"] = req => HttpBridge.OnSimulation(() => Bulldoze(req));
            routes["/areas/unlock_all"] = req => HttpBridge.OnSimulation(UnlockAllAreas);
        }

        // /net/prefabs  使える種類の名前の一覧(道路、線路など)
        private static string Prefabs()
        {
            var sb = new StringBuilder("{\"ok\":true,\"prefabs\":[");
            int n = PrefabCollection<NetInfo>.LoadedCount();
            for (uint i = 0; i < n; i++)
            {
                var info = PrefabCollection<NetInfo>.GetLoaded(i);
                if (info == null)
                {
                    continue;
                }

                if (sb[sb.Length - 1] != '[')
                {
                    sb.Append(',');
                }

                sb.Append("{\"name\":").Append(Json.Str(info.name))
                  .Append(",\"service\":").Append(Json.Str(info.m_class != null ? info.m_class.m_service.ToString() : null));

                // 1kmあたりの建設費と週の維持費。ゲームは8mごとに数える(PlayerNetAI)。高架やトンネルは建設費が上がる
                var ai = info.m_netAI as PlayerNetAI;
                if (ai != null)
                {
                    sb.Append(",\"costPerKm\":").Append((long)ai.GetConstructionCost() * 125 / 100)
                      .Append(",\"upkeepPerWeekPerKm\":").Append(Money.PerWeek((long)ai.GetMaintenanceCost() * 125));
                }

                sb.Append('}');
            }

            return sb.Append("]}").ToString();
        }

        // /areas/unlock_all  地図のすべての区画を、お金をかけずに街のものにする。
        // 実際の市長には区画を買い足すという判断がないため、街を始めたら最初に呼ぶ(#70)。
        private static string UnlockAllAreas()
        {
            var gam = GameAreaManager.instance;
            int before = gam.m_areaCount;
            int grid = (int)Math.Round(Math.Sqrt(gam.m_areaGrid.Length));
            // ゲームは持っている区画の隣しか解放できないので、増えなくなるまで繰り返す
            int last = -1;
            while (gam.m_areaCount != last)
            {
                last = gam.m_areaCount;
                for (int i = 0; i < gam.m_areaGrid.Length; i++)
                {
                    if (gam.m_areaGrid[i] == 0)
                    {
                        gam.UnlockArea(i);
                    }
                }
            }

            return "{\"ok\":true,\"grid\":" + grid + ",\"before\":" + before + ",\"after\":" + gam.m_areaCount + "}";
        }

        // POST /net/build?prefab=Train%20Track&pay=true  本文: "x1,z1;x2,z2;..."
        // 座標の並びに沿って線を引く。区間が長ければ細かく分ける。
        // pay=true(既定)なら、ゲームの道具と同じく建設費を予算から差し引く。足りなければ建てずに断る。
        private static string Build(HttpListenerRequest req)
        {
            string prefab = req.QueryString["prefab"];
            if (string.IsNullOrEmpty(prefab))
            {
                return HttpBridge.Error("prefab is required");
            }

            string body;
            using (var r = new StreamReader(req.InputStream, Encoding.UTF8))
            {
                body = r.ReadToEnd();
            }

            List<Vector3> points;
            try
            {
                points = Densify(Parse(body));
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad points: " + e.Message);
            }

            if (points.Count < 2)
            {
                return HttpBridge.Error("need at least 2 points");
            }

            bool pay = req.QueryString["pay"] != "false";
            return HttpBridge.OnSimulation(() => BuildOnSimulation(prefab, points, pay));
        }

        private static string BuildOnSimulation(string prefab, List<Vector3> points, bool pay)
        {
            return BuildOnSimulation(prefab, points, pay, null);
        }

        // fixedY を渡すと、地面の高さの代わりにその高さで点を置く(船の航路や飛行機の経路に使う)
        internal static string BuildOnSimulation(string prefab, List<Vector3> points, bool pay, float? fixedY)
        {
            var info = PrefabCollection<NetInfo>.FindLoaded(prefab);
            if (info == null)
            {
                return HttpBridge.Error("prefab not found: " + prefab + " (see /net/prefabs)");
            }

            var nm = NetManager.instance;
            var sim = SimulationManager.instance;
            var terrain = TerrainManager.instance;

            // 高架で引く点(3つ目の値で地面からの高さを指定)があるときは、水の上の点を外して、川を1区間でまたがせる。
            // 水の中に橋脚が立たないようにするため
            var elevatedInfo = fixedY == null ? AiField(info, "m_elevatedInfo") : null;
            bool wantElevated = false;
            foreach (var p in points)
            {
                wantElevated |= p.y > 0.5f;
            }

            if (wantElevated && elevatedInfo != null)
            {
                var kept = new List<Vector3>();
                for (int i = 0; i < points.Count; i++)
                {
                    bool inner = i > 0 && i < points.Count - 1;
                    if (inner && points[i].y > 0.5f && WaterDepth(points[i]) > 0.5f)
                    {
                        continue;
                    }

                    kept.Add(points[i]);
                }

                points = kept;
            }

            // 川や海を渡る区間は、橋の種類で引く(ゲームの線を引く道具と同じ)。高さを固定するとき(船・飛行機)は使わない
            var bridge = fixedY == null ? BridgeInfo(info) : null;
            int n = points.Count;
            var ground = new float[n];
            var ys = new float[n];
            var wet = new bool[n];
            for (int i = 0; i < n; i++)
            {
                ground[i] = fixedY ?? terrain.SampleRawHeightSmooth(points[i]);
                ys[i] = ground[i];
                wet[i] = bridge != null && WaterDepth(points[i]) > 0.5f;
            }

            var onBridge = new bool[n]; // onBridge[i]: points[i-1] から points[i] までの区間
            int bridges = 0;
            if (bridge != null)
            {
                for (int i = 1; i < n; i++)
                {
                    onBridge[i] = wet[i - 1] || wet[i] || CrossesWater(points[i - 1], points[i]);
                    if (onBridge[i])
                    {
                        bridges++;
                    }
                }

                // 水の上の点は、前後のいちばん近い岸の高さと、水面 + 3m の高い方まで持ち上げる
                for (int i = 0; i < n; i++)
                {
                    if (!wet[i])
                    {
                        continue;
                    }

                    float left = ground[0], right = ground[n - 1];
                    for (int k = i - 1; k >= 0; k--)
                    {
                        if (!wet[k]) { left = ground[k]; break; }
                    }

                    for (int k = i + 1; k < n; k++)
                    {
                        if (!wet[k]) { right = ground[k]; break; }
                    }

                    float water = terrain.SampleRawHeightSmoothWithWater(points[i], false, 0f);
                    ys[i] = Mathf.Max(Mathf.Max(left, right), water + 3f);
                }
            }

            // 高架の点は、指定の高さまで持ち上げる。高架の区間は高架の種類で引く(水の上でも、橋ではなく高架にする)
            var useElevated = new bool[n];
            if (wantElevated && elevatedInfo != null)
            {
                for (int i = 0; i < n; i++)
                {
                    if (points[i].y > 0.5f)
                    {
                        ys[i] = Mathf.Max(ys[i], ground[i] + points[i].y);
                    }
                }

                for (int i = 1; i < n; i++)
                {
                    if (points[i - 1].y > 0.5f || points[i].y > 0.5f)
                    {
                        useElevated[i] = true;
                        if (onBridge[i])
                        {
                            onBridge[i] = false;
                            bridges--;
                        }
                    }
                }
            }

            // 先に建設費の合計を計算し、足りるときだけ建てる(途中で止まって中途半端にならないように)
            int cost = 0;
            for (int i = 1; i < n; i++)
            {
                var a = points[i - 1];
                var b = points[i];
                a.y = ys[i - 1];
                b.y = ys[i];
                var segInfo = onBridge[i] ? bridge : useElevated[i] ? elevatedInfo : info;
                // 橋の費用は、地面からの高さで増える
                cost += segInfo.m_netAI.GetConstructionCost(a, b, ys[i - 1] - ground[i - 1], ys[i] - ground[i]);
            }

            if (pay)
            {
                var eco = EconomyManager.instance;
                if (eco.PeekResource(EconomyManager.Resource.Construction, cost) != cost)
                {
                    return "{\"ok\":false,\"error\":\"not enough money\",\"cost\":" + cost / 100
                        + ",\"money\":" + eco.LastCashAmount / 100 + "}";
                }

                eco.FetchResource(EconomyManager.Resource.Construction, cost, info.m_class);
            }
            Randomizer rnd = sim.m_randomizer;

            int nodes = 0, segments = 0, snapped = 0, split = 0;
            ushort prevNode = 0;
            Vector3 prevPos = Vector3.zero;
            for (int i = 0; i < points.Count; i++)
            {
                var pos = points[i];
                pos.y = ys[i];

                ushort node = 0;
                if (i == 0 || i == points.Count - 1)
                {
                    node = FindNode(pos, info);
                    if (node == 0)
                    {
                        // 点がなければ、近くの区間を途中で分けて、交差点を作る
                        ushort seg = FindSegment(pos, info);
                        if (seg != 0)
                        {
                            node = SplitSegment(seg, pos, ref rnd);
                            if (node != 0)
                            {
                                split++;
                            }
                        }
                    }
                    else
                    {
                        snapped++;
                    }

                    if (node != 0)
                    {
                        pos = nm.m_nodes.m_buffer[node].m_position;
                    }
                }

                if (node == 0)
                {
                    bool raised = ys[i] - ground[i] > 0.5f;
                    var nodeInfo = wet[i] && bridge != null && !wantElevated ? bridge : raised && elevatedInfo != null ? elevatedInfo : info;
                    if (!nm.CreateNode(out node, ref rnd, nodeInfo, pos, sim.m_currentBuildIndex))
                    {
                        return HttpBridge.Error("CreateNode failed at point " + i);
                    }

                    if (raised)
                    {
                        // 水の上の点: 地面からの高さを覚えさせる(橋脚はゲームが置く)
                        nm.m_nodes.m_buffer[node].m_elevation = (byte)Mathf.Clamp(Mathf.RoundToInt(ys[i] - ground[i]), 1, 255);
                        nm.m_nodes.m_buffer[node].m_flags &= ~NetNode.Flags.OnGround;
                    }

                    sim.m_currentBuildIndex++;
                    nodes++;
                }

                if (prevNode != 0)
                {
                    var dir = pos - prevPos;
                    dir.y = 0f;
                    dir.Normalize();
                    ushort seg;
                    if (!nm.CreateSegment(out seg, ref rnd, onBridge[i] ? bridge : useElevated[i] ? elevatedInfo : info, prevNode, node, dir, -dir,
                            sim.m_currentBuildIndex, sim.m_currentBuildIndex, false))
                    {
                        return HttpBridge.Error("CreateSegment failed at point " + i);
                    }

                    sim.m_currentBuildIndex++;
                    segments++;
                }

                prevNode = node;
                prevPos = pos;
            }

            return "{\"ok\":true,\"prefab\":" + Json.Str(prefab) + ",\"nodes\":" + nodes + ",\"segments\":" + segments
                + ",\"snapped\":" + snapped + ",\"split\":" + split + ",\"bridgeSegments\":" + bridges
                + ",\"cost\":" + cost / 100 + ",\"paid\":" + (pay ? "true" : "false") + "}";
        }

        // 橋の種類(道路と線路の AI が m_bridgeInfo に持つ)。なければ null
        private static NetInfo BridgeInfo(NetInfo info)
        {
            return AiField(info, "m_bridgeInfo");
        }

        // 道路と線路の AI が持つ、別の種類への参照(m_bridgeInfo、m_elevatedInfo など)。なければ null
        private static NetInfo AiField(NetInfo info, string name)
        {
            var field = info.m_netAI.GetType().GetField(name);
            return field != null ? field.GetValue(info.m_netAI) as NetInfo : null;
        }

        private static float WaterDepth(Vector3 p)
        {
            var t = TerrainManager.instance;
            return t.SampleRawHeightSmoothWithWater(p, false, 0f) - t.SampleRawHeightSmooth(p);
        }

        // 区間の途中に水があるか(8mおきに調べる)。点の間に細い川があっても見落とさないため
        private static bool CrossesWater(Vector3 a, Vector3 b)
        {
            int steps = Mathf.Max(1, Mathf.CeilToInt(Vector3.Distance(a, b) / 8f));
            for (int k = 1; k < steps; k++)
            {
                if (WaterDepth(Vector3.Lerp(a, b, (float)k / steps)) > 0.5f)
                {
                    return true;
                }
            }

            return false;
        }

        // POST /net/remove?prefab=Train%20Track&tolerance=20  本文: "x1,z1;x2,z2;..."
        // 座標の並び(線)に沿った区間を消す。区間の両端が線から tolerance 以内のものが対象。prefab を省くと種類を問わない。
        // 出発点の街を作り直すための準備用。人が curl で呼ぶ。払い戻しはない
        private static string RemoveAll(HttpListenerRequest req)
        {
            string prefab = req.QueryString["prefab"];
            if (string.IsNullOrEmpty(prefab))
            {
                return HttpBridge.Error("prefab is required");
            }

            return HttpBridge.OnSimulation(() =>
            {
                var nm = NetManager.instance;
                var segs = nm.m_segments.m_buffer;
                int removed = 0;
                for (int i = 1; i < segs.Length; i++)
                {
                    if ((segs[i].m_flags & NetSegment.Flags.Created) != 0 && segs[i].Info != null && segs[i].Info.name == prefab)
                    {
                        nm.ReleaseSegment((ushort)i, false);
                        removed++;
                    }
                }

                return "{\"ok\":true,\"prefab\":" + Json.Str(prefab) + ",\"removedSegments\":" + removed + "}";
            });
        }

        private static string Remove(HttpListenerRequest req)
        {
            string prefab = req.QueryString["prefab"];
            float tol;
            if (!float.TryParse(req.QueryString["tolerance"] ?? "20", NumberStyles.Float, CultureInfo.InvariantCulture, out tol))
            {
                tol = 20f;
            }

            string body;
            using (var r = new StreamReader(req.InputStream, Encoding.UTF8))
            {
                body = r.ReadToEnd();
            }

            List<Vector3> line;
            try
            {
                line = Parse(body);
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad points: " + e.Message);
            }

            return HttpBridge.OnSimulation(() =>
            {
                var nm = NetManager.instance;
                var segs = nm.m_segments.m_buffer;
                var nodes = nm.m_nodes.m_buffer;
                int removed = 0;
                for (int i = 1; i < segs.Length; i++)
                {
                    if ((segs[i].m_flags & NetSegment.Flags.Created) == 0 || segs[i].Info == null)
                    {
                        continue;
                    }

                    if (!string.IsNullOrEmpty(prefab) && segs[i].Info.name != prefab)
                    {
                        continue;
                    }

                    var a = nodes[segs[i].m_startNode].m_position;
                    var b = nodes[segs[i].m_endNode].m_position;
                    if (DistanceToLine(a, line) <= tol && DistanceToLine(b, line) <= tol)
                    {
                        nm.ReleaseSegment((ushort)i, false);
                        removed++;
                    }
                }

                return "{\"ok\":true,\"removedSegments\":" + removed + "}";
            });
        }

        // /bulldoze?x=..&z=..&radius=50&what=all|net|building  円の中の道路・線路と建物を消す
        private static string Bulldoze(HttpListenerRequest req)
        {
            var c = new Vector3(Q(req, "x", 0f), 0f, Q(req, "z", 0f));
            float r2 = Q(req, "radius", 50f);
            r2 *= r2;
            string what = req.QueryString["what"] ?? "all";
            int nets = 0, buildings = 0;

            if (what == "all" || what == "net")
            {
                var nm = NetManager.instance;
                var segs = nm.m_segments.m_buffer;
                for (int i = 1; i < segs.Length; i++)
                {
                    if ((segs[i].m_flags & NetSegment.Flags.Created) == 0)
                    {
                        continue;
                    }

                    var d = segs[i].m_middlePosition - c;
                    d.y = 0f;
                    if (d.sqrMagnitude <= r2)
                    {
                        nm.ReleaseSegment((ushort)i, false);
                        nets++;
                    }
                }
            }

            if (what == "all" || what == "building")
            {
                var bm = BuildingManager.instance;
                var bs = bm.m_buildings.m_buffer;
                for (int i = 1; i < bs.Length; i++)
                {
                    if ((bs[i].m_flags & Building.Flags.Created) == 0 || (bs[i].m_flags & Building.Flags.Untouchable) != 0)
                    {
                        continue;
                    }

                    var d = bs[i].m_position - c;
                    d.y = 0f;
                    if (d.sqrMagnitude <= r2)
                    {
                        bm.ReleaseBuilding((ushort)i);
                        buildings++;
                    }
                }
            }

            return "{\"ok\":true,\"removedSegments\":" + nets + ",\"removedBuildings\":" + buildings + "}";
        }

        private static float Q(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }

        // 点から、折れ線までの水平の距離
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

        // 近くにある、同じサービスの区間を探す(両端の点からは離れた所に限る)
        private static ushort FindSegment(Vector3 pos, NetInfo info)
        {
            var nm = NetManager.instance;
            var segs = nm.m_segments.m_buffer;
            ushort best = 0;
            float bestD = SplitDistance;
            for (int i = 1; i < segs.Length; i++)
            {
                if ((segs[i].m_flags & NetSegment.Flags.Created) == 0 || segs[i].Info == null
                    || segs[i].Info.m_class.m_service != info.m_class.m_service)
                {
                    continue;
                }

                var mid = segs[i].m_middlePosition - pos;
                mid.y = 0f;
                if (mid.sqrMagnitude > 200f * 200f)
                {
                    continue; // 区間は最大でも100m前後なので、遠いものは調べない
                }

                var p = segs[i].GetClosestPosition(pos);
                var d = p - pos;
                d.y = 0f;
                if (d.magnitude >= bestD)
                {
                    continue;
                }

                var a = nm.m_nodes.m_buffer[segs[i].m_startNode].m_position - p;
                var b = nm.m_nodes.m_buffer[segs[i].m_endNode].m_position - p;
                a.y = 0f;
                b.y = 0f;
                if (a.magnitude < 8f || b.magnitude < 8f)
                {
                    continue; // 端に近すぎるときは分けない(点につなぐ処理に任せる)
                }

                bestD = d.magnitude;
                best = (ushort)i;
            }

            return best;
        }

        // 区間を、pos にいちばん近い点で2つに分け、新しくできた点を返す。向きと一方通行の向きは引き継ぐ
        private static ushort SplitSegment(ushort segId, Vector3 pos, ref Randomizer rnd)
        {
            var nm = NetManager.instance;
            var sim = SimulationManager.instance;
            var seg = nm.m_segments.m_buffer[segId];
            var info = seg.Info;
            Vector3 at, dir;
            seg.GetClosestPositionAndDirection(pos, out at, out dir);
            dir.y = 0f;
            dir.Normalize();

            ushort startNode = seg.m_startNode;
            ushort endNode = seg.m_endNode;
            var startDir = seg.m_startDirection;
            var endDir = seg.m_endDirection;
            bool invert = (seg.m_flags & NetSegment.Flags.Invert) != 0;
            uint buildIndex = seg.m_buildIndex;

            nm.ReleaseSegment(segId, true);

            ushort mid;
            if (!nm.CreateNode(out mid, ref rnd, info, at, sim.m_currentBuildIndex))
            {
                return 0;
            }

            sim.m_currentBuildIndex++;
            ushort a, b;
            nm.CreateSegment(out a, ref rnd, info, startNode, mid, startDir, -dir, buildIndex, sim.m_currentBuildIndex, invert);
            sim.m_currentBuildIndex++;
            nm.CreateSegment(out b, ref rnd, info, mid, endNode, dir, endDir, buildIndex, sim.m_currentBuildIndex, invert);
            sim.m_currentBuildIndex++;
            return mid;
        }

        // 近くにある、同じ種類の既存の点を探す
        internal static ushort FindNode(Vector3 pos, NetInfo info)
        {
            var buf = NetManager.instance.m_nodes.m_buffer;
            ushort best = 0;
            float bestD = SnapDistance * SnapDistance;
            for (int i = 1; i < buf.Length; i++)
            {
                if ((buf[i].m_flags & NetNode.Flags.Created) == 0 || buf[i].Info == null
                    || buf[i].Info.m_class.m_service != info.m_class.m_service)
                {
                    continue;
                }

                var d = buf[i].m_position - pos;
                d.y = 0f;
                if (d.sqrMagnitude < bestD)
                {
                    bestD = d.sqrMagnitude;
                    best = (ushort)i;
                }
            }

            return best;
        }

        internal static List<Vector3> Parse(string body)
        {
            var list = new List<Vector3>();
            foreach (var part in body.Split(new[] { ';', '\n' }, StringSplitOptions.RemoveEmptyEntries))
            {
                // "x,z" または "x,z,地面からの高さ"。高さは y に入れて運ぶ(高架で引くときに使う)
                var xy = part.Split(',');
                list.Add(new Vector3(
                    float.Parse(xy[0].Trim(), CultureInfo.InvariantCulture),
                    xy.Length > 2 ? float.Parse(xy[2].Trim(), CultureInfo.InvariantCulture) : 0f,
                    float.Parse(xy[1].Trim(), CultureInfo.InvariantCulture)));
            }

            return list;
        }

        // 区間が MaxSegment より長ければ、間に点を足す
        internal static List<Vector3> Densify(List<Vector3> pts)
        {
            var outPts = new List<Vector3>();
            for (int i = 0; i < pts.Count; i++)
            {
                if (i > 0)
                {
                    var a = pts[i - 1];
                    var b = pts[i];
                    int n = Mathf.CeilToInt(Vector3.Distance(a, b) / MaxSegment);
                    for (int k = 1; k < n; k++)
                    {
                        outPts.Add(Vector3.Lerp(a, b, (float)k / n));
                    }
                }

                outPts.Add(pts[i]);
            }

            return outPts;
        }
    }
}
