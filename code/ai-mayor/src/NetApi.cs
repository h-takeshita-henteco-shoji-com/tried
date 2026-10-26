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
            routes["/net/prefabs"] = req => HttpBridge.OnMain(() => Prefabs(req.QueryString["locked"] == "true"));
            routes["/net/build"] = Build;
            routes["/net/remove"] = Remove;
            // /net/remove_all?prefab=Train%20Track  準備用。その種類の線をすべて消す。MCP の道具にはしない
            routes["/net/remove_all"] = RemoveAll;
            routes["/bulldoze"] = req => HttpBridge.OnSimulation(() => Bulldoze(req));
            routes["/areas/unlock_all"] = req => HttpBridge.OnSimulation(UnlockAllAreas);
        }

        // /net/prefabs?locked=false  使える種類の名前の一覧(道路、線路など)。
        // ゲームの道具の一覧と同じく、手で引く線だけにする(GeneratedScrollPanel.IsPlacementRelevant)。
        // 既定では解禁された線だけ。locked=true で、解禁前の線も unlocked=false と条件つきで返す(#82)。
        // #82 の試運転で、市長が解禁前の道路まで約140種を受け取っていた
        private static string Prefabs(bool withLocked)
        {
            var sb = new StringBuilder("{\"ok\":true,\"prefabs\":[");
            int n = PrefabCollection<NetInfo>.LoadedCount();
            for (uint i = 0; i < n; i++)
            {
                var info = PrefabCollection<NetInfo>.GetLoaded(i);
                if (info == null || (info.m_availableIn & ItemClass.Availability.Game) == 0)
                {
                    continue;
                }

                // 地下鉄の線路は、手で置く種類(Manual)に入っていないことがある。地下鉄だけは種類を問わず出す(#107)
                bool metro = info.m_class != null && info.m_class.m_subService == ItemClass.SubService.PublicTransportMetro;
                if (info.m_placementStyle != ItemClass.Placement.Manual && !metro)
                {
                    continue;
                }

                bool locked = !ToolsModifierControl.IsUnlocked(info.GetUnlockMilestone());
                if (locked && !withLocked)
                {
                    continue;
                }

                if (sb[sb.Length - 1] != '[')
                {
                    sb.Append(',');
                }

                sb.Append("{\"name\":").Append(Json.Str(info.name))
                  .Append(",\"service\":").Append(Json.Str(info.m_class != null ? info.m_class.m_service.ToString() : null))
                  .Append(",\"unlocked\":").Append(locked ? "false" : "true");
                if (metro)
                {
                    sb.Append(",\"subService\":\"PublicTransportMetro\",\"placement\":").Append(Json.Str(info.m_placementStyle.ToString()))
                      .Append(",\"hasTunnel\":").Append(AiField(info, "m_tunnelInfo") != null ? "true" : "false");
                }
                if (locked)
                {
                    sb.Append(",\"unlock\":").Append(UnlockJson(info));
                }

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

        // 解禁の条件。人口の節目なら、その人口(CityApi.UnlockJson と同じ形)
        private static string UnlockJson(PrefabInfo info)
        {
            var m = info.GetUnlockMilestone();
            if (m == null)
            {
                return "null";
            }

            var p = m.GetLocalizedProgress();
            return "{\"milestone\":" + Json.Str(m.GetLocalizedName()) + ",\"current\":" + Mathf.RoundToInt(p.m_current)
                + ",\"target\":" + Mathf.RoundToInt(p.m_max) + ",\"description\":" + Json.Str(p.m_description) + "}";
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
            bool demolish = req.QueryString["demolish"] == "true";
            // test=true なら、引けるかを確かめて、引かずに返す(#105。局と市長が、建てる前に試す。ゲームの道具の、引く前の赤い表示に当たる)
            bool test = req.QueryString["test"] == "true";
            var assumed = test ? Assumed.Parse(req) : null;
            // y を渡すと、地面の高さの代わりにその高さで点を置く。船の航路を水面に引くため(#100)
            float? fixedY = null;
            string ys = req.QueryString["y"];
            if (!string.IsNullOrEmpty(ys))
            {
                fixedY = float.Parse(ys, System.Globalization.CultureInfo.InvariantCulture);
            }

            return HttpBridge.OnSimulation(() => BuildOnSimulation(prefab, points, pay, fixedY, demolish, test, assumed));
        }

        // fixedY を渡すと、地面の高さの代わりにその高さで点を置く(船の航路や飛行機の経路に使う)。
        // マップエディターの道具から呼ぶ。重なる建物は確かめない
        internal static string BuildOnSimulation(string prefab, List<Vector3> points, bool pay, float? fixedY)
        {
            return BuildOnSimulation(prefab, points, pay, fixedY, true, false, null);
        }

        // demolish=false なら、建物に重なるときは建てずに断る(#82)
        // 試しで「壊したもの」とする区間。つなぐ先と交差点を探すときに除く(#105)。シミュレーションのスレッドで1件ずつ呼ぶ
        [ThreadStatic]
        private static HashSet<int> skipSegments;

        private static string BuildOnSimulation(string prefab, List<Vector3> points, bool pay, float? fixedY, bool demolish, bool test, Assumed assumed)
        {
            skipSegments = assumed != null && assumed.Any ? assumed.Segments : null;
            try
            {
                return BuildCore(prefab, points, pay, fixedY, demolish, test, assumed);
            }
            finally
            {
                skipSegments = null;
            }
        }

        private static string BuildCore(string prefab, List<Vector3> points, bool pay, float? fixedY, bool demolish, bool test, Assumed assumed)
        {
            var info = PrefabCollection<NetInfo>.FindLoaded(prefab);
            if (info == null)
            {
                return HttpBridge.Error("prefab not found: " + prefab + " (see /net/prefabs)");
            }

            // 解禁前の線は断る(#82)。人が置く骨格(pay=false)とマップエディターの道具は問わない
            if (pay && !ToolsModifierControl.IsUnlocked(info.GetUnlockMilestone()))
            {
                return HttpBridge.Error("this network is not unlocked yet: " + prefab);
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

            // 地下に引く点(3つ目の値が負。地面からの深さ)。#82。
            // ゲームの NetTool は、地面より8m以上深い点を地下の点(Underground)にし、区間は NetAI.GetInfo で選ぶ。
            // 両端が地下ならトンネルの種類(m_tunnelInfo)、片方だけなら坂の種類(m_slopeInfo)。同じ決まりにする
            var tunnelInfo = fixedY == null ? AiField(info, "m_tunnelInfo") : null;
            var slopeInfo = fixedY == null ? AiField(info, "m_slopeInfo") : null;
            bool wantTunnel = false;
            foreach (var p in points)
            {
                wantTunnel |= p.y < -0.5f;
            }

            if (wantTunnel && tunnelInfo == null)
            {
                return HttpBridge.Error("this line type cannot go underground (no tunnel type): " + prefab);
            }

            // 途中で交わる既存の道路・水道管に交差点を作る(#82)。ゲームの線を引く道具と同じ動き。
            // 前は端だけをつないだので、途中の交わりは重なるだけだった(g01 から何度も実害。g84 は24区間を引き直した)
            var joins = new HashSet<int>();
            int crossings = 0;
            if (fixedY == null && !wantElevated && !wantTunnel
                && (info.m_class.m_service == ItemClass.Service.Road || info.m_class.m_service == ItemClass.Service.Water))
            {
                points = InsertCrossings(points, info, joins);
                crossings = joins.Count;
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

            // 地下の点は、地面から指定の深さ(8mより浅ければ9m)に置く。水の上でも橋にしない
            var under = new bool[n];
            for (int i = 0; i < n; i++)
            {
                if (wantTunnel && points[i].y < -0.5f)
                {
                    under[i] = true;
                    wet[i] = false;
                    ys[i] = ground[i] - Mathf.Max(-points[i].y, 9f);
                }
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

            // 地下の区間(片方でも地下の点)の種類。両端が地下ならトンネル、片方なら坂(なければトンネル)
            var undergroundInfo = new NetInfo[n]; // undergroundInfo[i]: points[i-1] から points[i] までの区間。地上なら null
            int tunnels = 0;
            for (int i = 1; i < n; i++)
            {
                if (!under[i - 1] && !under[i])
                {
                    continue;
                }

                undergroundInfo[i] = under[i - 1] && under[i] ? tunnelInfo : (slopeInfo ?? tunnelInfo);
                tunnels++;
                if (onBridge[i])
                {
                    onBridge[i] = false;
                    bridges--;
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

            // 道路や線路が建物の敷地に重なると、ゲームはその建物を壊す。戻り値には出ないため、
            // #82 の試運転では市長が人口の減りで初めて気づいた。費用を払う前に、重なる建物を探す
            // 両端が地下の区間は地面の建物と重ならないので、高架と同じく調べない
            var skipOverlap = new bool[n];
            for (int i = 0; i < n; i++)
            {
                skipOverlap[i] = useElevated[i] || (i > 0 && under[i - 1] && under[i]);
            }

            string overlaps = Overlaps(info, points, onBridge, skipOverlap, assumed);
            if (overlaps != "[]" && !demolish)
            {
                return "{\"ok\":false,\"error\":\"the line overlaps buildings. They would be demolished. Pass demolish=true to build anyway\""
                    + ",\"overlaps\":" + overlaps + "}";
            }

            // ゲームの線を引く道具と同じ判定で、区間ごとに引けるかを試す(#105)。前は判定を通さずに引いたので、
            // 取り除けない相手(別の道路の交差点の近く、サービスの建物、建物の一部の線など)に重なっても引けた。
            // 人が引くと断られる「ぶつかる」(ObjectCollision)だけで断る。ほかの理由(短すぎ、坂が急すぎなど)は、
            // この窓口の引き方(直線の区間、橋の高さの決め方)がゲームの道具と少し違うため、gameCheck に返すだけにする
            var gameCheck = new StringBuilder();
            if ((pay || test) && fixedY == null)
            {
                var buffer = new FastList<NetTool.NodePosition>();
                for (int i = 1; i < n; i++)
                {
                    var a = TestPoint(points[i - 1], ys[i - 1], ground[i - 1], info, under[i - 1], i - 1 == 0 || joins.Contains(i - 1));
                    var b = TestPoint(points[i], ys[i], ground[i], info, under[i], i == n - 1 || joins.Contains(i));
                    var dir = b.m_position - a.m_position;
                    dir.y = 0f;
                    if (dir.sqrMagnitude < 0.01f)
                    {
                        continue;
                    }

                    dir.Normalize();
                    a.m_direction = dir;
                    b.m_direction = dir;
                    var mid = default(NetTool.ControlPoint);
                    mid.m_position = (a.m_position + b.m_position) * 0.5f;
                    mid.m_direction = dir;
                    mid.m_elevation = Mathf.Lerp(a.m_elevation, b.m_elevation, 0.5f);
                    ushort tn, ts;
                    int tc, tr;
                    var errors = NetTool.CreateNode(info, a, mid, b, buffer, 1000, true, false, true, false, false, false, 0, out tn, out ts, out tc, out tr);
                    string coll = null;
                    if ((errors & ToolBase.ToolErrors.ObjectCollision) != 0)
                    {
                        bool blocking;
                        coll = UpgradeApi.Colliding(assumed, out blocking);
                        // 試しで、断る相手がすべて「壊したもの」なら、ぶつからないとみなす(#105)
                        if (assumed != null && assumed.Any && !blocking)
                        {
                            errors &= ~ToolBase.ToolErrors.ObjectCollision;
                        }
                    }

                    if ((errors & ToolBase.ToolErrors.ObjectCollision) != 0)
                    {
                        return "{\"ok\":false,\"error\":\"the game refuses this line: it collides with something that cannot be removed (ObjectCollision)\""
                            + ",\"atSegment\":{\"from\":" + i + ",\"fromX\":" + Mathf.RoundToInt(a.m_position.x) + ",\"fromZ\":" + Mathf.RoundToInt(a.m_position.z)
                            + ",\"toX\":" + Mathf.RoundToInt(b.m_position.x) + ",\"toZ\":" + Mathf.RoundToInt(b.m_position.z) + "}"
                            + ",\"reasons\":" + Json.Str(errors.ToString()) + ",\"colliding\":" + coll + "}";
                    }

                    if (errors != ToolBase.ToolErrors.None)
                    {
                        gameCheck.Append(gameCheck.Length == 0 ? "" : ",").Append("{\"segment\":").Append(i)
                            .Append(",\"reasons\":").Append(Json.Str(errors.ToString())).Append('}');
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
                var segInfo = undergroundInfo[i] ?? (onBridge[i] ? bridge : useElevated[i] ? elevatedInfo : info);
                // 橋の費用は、地面からの高さで増える。トンネルは深さ(負の高さ)で決まる
                cost += segInfo.m_netAI.GetConstructionCost(a, b, ys[i - 1] - ground[i - 1], ys[i] - ground[i]);
            }

            if (test)
            {
                var money = EconomyManager.instance.LastCashAmount;
                return "{\"ok\":true,\"test\":true,\"built\":false,\"prefab\":" + Json.Str(prefab) + ",\"segments\":" + (n - 1)
                    + ",\"crossings\":" + crossings + ",\"bridgeSegments\":" + bridges + ",\"undergroundSegments\":" + tunnels
                    + ",\"cost\":" + cost / 100 + ",\"enoughMoney\":" + (money >= cost ? "true" : "false") + ",\"overlaps\":" + overlaps
                    + (gameCheck.Length > 0 ? ",\"gameCheck\":[" + gameCheck + "]" : "") + "}";
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
            var ends = new StringBuilder();
            ushort prevNode = 0;
            Vector3 prevPos = Vector3.zero;
            for (int i = 0; i < points.Count; i++)
            {
                var pos = points[i];
                pos.y = ys[i];

                ushort node = 0;
                bool isEnd = i == 0 || i == points.Count - 1;
                if (isEnd || joins.Contains(i))
                {
                    string how = "none";
                    // 地下の端は地下の点・区間に、地上の端は地上の点・区間にだけつなぐ(#82)
                    node = FindNode(pos, info, under[i]);
                    if (node == 0)
                    {
                        // 点がなければ、近くの区間を途中で分けて、交差点を作る
                        ushort seg = FindSegment(pos, info, under[i]);
                        if (seg != 0)
                        {
                            node = SplitSegment(seg, pos, ref rnd);
                            if (node != 0)
                            {
                                split++;
                                how = "split";
                            }
                        }
                    }
                    else
                    {
                        snapped++;
                        how = "node";
                    }

                    if (node != 0)
                    {
                        pos = nm.m_nodes.m_buffer[node].m_position;
                    }

                    // 端が何につながったか。#81 の市長は、管や送電線が建物につながったかを知る手段がなかった
                    if (isEnd)
                    {
                        ends.Append(ends.Length == 0 ? "" : ",").Append(EndJson(pos, node, how, info));
                    }
                }

                if (node == 0)
                {
                    bool raised = ys[i] - ground[i] > 0.5f;
                    var nodeInfo = under[i] ? tunnelInfo
                        : wet[i] && bridge != null && !wantElevated ? bridge : raised && elevatedInfo != null ? elevatedInfo : info;
                    if (!nm.CreateNode(out node, ref rnd, nodeInfo, pos, sim.m_currentBuildIndex))
                    {
                        return HttpBridge.Error("CreateNode failed at point " + i);
                    }

                    if (under[i])
                    {
                        // 地下の点: ゲームの NetTool と同じく、高さ0・Underground の印・地面の印なし
                        nm.m_nodes.m_buffer[node].m_elevation = 0;
                        nm.m_nodes.m_buffer[node].m_flags |= NetNode.Flags.Underground;
                        nm.m_nodes.m_buffer[node].m_flags &= ~NetNode.Flags.OnGround;
                    }
                    else if (raised)
                    {
                        // 水の上の点: 地面からの高さを覚えさせる(橋脚はゲームが置く)
                        nm.m_nodes.m_buffer[node].m_elevation = (byte)Mathf.Clamp(Mathf.RoundToInt(ys[i] - ground[i]), 1, 255);
                        nm.m_nodes.m_buffer[node].m_flags &= ~NetNode.Flags.OnGround;
                    }
                    else if (fixedY == null)
                    {
                        // 地面の点: ゲームの NetTool と同じく OnGround の印を付ける(#82。前は付けていなかった)
                        nm.m_nodes.m_buffer[node].m_flags |= NetNode.Flags.OnGround;
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
                    if (!nm.CreateSegment(out seg, ref rnd, undergroundInfo[i] ?? (onBridge[i] ? bridge : useElevated[i] ? elevatedInfo : info), prevNode, node, dir, -dir,
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
                + ",\"snapped\":" + snapped + ",\"split\":" + split + ",\"crossings\":" + crossings + ",\"ends\":[" + ends + "],\"bridgeSegments\":" + bridges
                + ",\"undergroundSegments\":" + tunnels
                + ",\"cost\":" + cost / 100 + ",\"paid\":" + (pay ? "true" : "false") + ",\"overlaps\":" + overlaps
                + (gameCheck.Length > 0 ? ",\"gameCheck\":[" + gameCheck + "]" : "") + "}";
        }

        // 試しに引くときの点(ゲームの道具が点や区間を指したときと同じ)。端と交差点は、既存の点か区間につなぐ
        private static NetTool.ControlPoint TestPoint(Vector3 p, float y, float ground, NetInfo info, bool under, bool connect)
        {
            var cp = default(NetTool.ControlPoint);
            p.y = y;
            cp.m_position = p;
            cp.m_elevation = y - ground;
            if (connect)
            {
                ushort node = FindNode(p, info, under);
                if (node != 0)
                {
                    var nn = NetManager.instance.m_nodes.m_buffer[node];
                    cp.m_node = node;
                    cp.m_position = nn.m_position;
                    cp.m_elevation = under ? -nn.m_elevation : nn.m_elevation;
                    cp.m_outside = (nn.m_flags & NetNode.Flags.Outside) != 0;
                }
                else
                {
                    cp.m_segment = FindSegment(p, info, under);
                }
            }

            return cp;
        }

        // 線が敷地に重なる建物の JSON の配列。重ならなければ "[]"。
        // 衝突する線(道路、線路、歩道)の地面の区間だけを調べる。橋と高架は建物の上を通れるので調べない。
        // 区間を4mおきの点で調べ、建物の長方形を線の半幅だけ広げた中に入るかで判定する。
        // 区画の建物は道路の端(中心から半幅)に接して建つので、広げる幅は2m控え、沿って引いた道路を重なりと数えない
        private static string Overlaps(NetInfo info, List<Vector3> points, bool[] onBridge, bool[] useElevated, Assumed assumed = null)
        {
            var hit = OverlapIds(info, points, onBridge, useElevated);
            if (assumed != null)
            {
                hit.RemoveAll(id => assumed.RemovedBuilding(id));
            }

            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("[");
            for (int i = 0; i < hit.Count; i++)
            {
                var b = bs[hit[i]];
                sb.Append(i > 0 ? "," : "").Append("{\"id\":").Append(hit[i]).Append(",\"prefab\":").Append(Json.Str(b.Info.name))
                  .Append(",\"service\":").Append(Json.Str(b.Info.m_class.m_service.ToString()))
                  .Append(",\"x\":").Append(Mathf.RoundToInt(b.m_position.x)).Append(",\"z\":").Append(Mathf.RoundToInt(b.m_position.z))
                  // 敷地の幅と奥行き(m)と向き。中心だけでは避ける線を決められない(#82 の42か月目)
                  .Append(",\"width\":").Append(b.Info.m_cellWidth * 8).Append(",\"length\":").Append(b.Info.m_cellLength * 8)
                  .Append(",\"angle\":").Append(Mathf.RoundToInt(b.m_angle * Mathf.Rad2Deg)).Append('}');
            }

            return sb.Append(']').ToString();
        }

        // 線が敷地に重なる建物の番号。upgrade_road でも使う(#107)
        internal static List<ushort> OverlapIds(NetInfo info, List<Vector3> points, bool[] onBridge, bool[] useElevated)
        {
            var svc = info.m_class.m_service;
            if (!info.m_canCollide || (svc != ItemClass.Service.Road && svc != ItemClass.Service.PublicTransport
                && svc != ItemClass.Service.Beautification))
            {
                return new List<ushort>();
            }

            float pad = Mathf.Max(0f, info.m_halfWidth - 2f);
            float minX = float.MaxValue, maxX = float.MinValue, minZ = float.MaxValue, maxZ = float.MinValue;
            foreach (var p in points)
            {
                minX = Mathf.Min(minX, p.x);
                maxX = Mathf.Max(maxX, p.x);
                minZ = Mathf.Min(minZ, p.z);
                maxZ = Mathf.Max(maxZ, p.z);
            }

            // 線の近く(外接の四角 + 100m)の建物だけを先に集める
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var near = new List<ushort>();
            for (int i = 1; i < bs.Length; i++)
            {
                var f = bs[i].m_flags;
                if ((f & Building.Flags.Created) == 0 || (f & Building.Flags.Deleted) != 0 || bs[i].Info == null
                    || bs[i].m_parentBuilding != 0 || MapApi.IsNetPart(ref bs[i]))
                {
                    continue;
                }

                var q = bs[i].m_position;
                if (q.x < minX - 100f || q.x > maxX + 100f || q.z < minZ - 100f || q.z > maxZ + 100f)
                {
                    continue;
                }

                near.Add((ushort)i);
            }

            var hit = new List<ushort>();
            for (int i = 1; i < points.Count; i++)
            {
                if (onBridge[i] || useElevated[i])
                {
                    continue;
                }

                var a = points[i - 1];
                var b = points[i];
                int steps = Mathf.Max(1, Mathf.CeilToInt(new Vector2(b.x - a.x, b.z - a.z).magnitude / 4f));
                for (int k = 0; k <= steps; k++)
                {
                    var p = Vector3.Lerp(a, b, (float)k / steps);
                    foreach (var id in near)
                    {
                        if (!hit.Contains(id) && InsideLot(ref bs[id], p, pad))
                        {
                            hit.Add(id);
                        }
                    }
                }
            }

            return hit;
        }

        // 点が、建物の敷地(長方形を pad だけ広げたもの)に入るか。向きの回し方は BuildingAt と同じ
        private static bool InsideLot(ref Building b, Vector3 pos, float pad)
        {
            var d = pos - b.m_position;
            float a = b.m_angle;
            float right = d.x * Mathf.Cos(a) + d.z * Mathf.Sin(a);
            float forward = -d.x * Mathf.Sin(a) + d.z * Mathf.Cos(a);
            return Mathf.Abs(right) <= b.Info.m_cellWidth * 4f + pad && Mathf.Abs(forward) <= b.Info.m_cellLength * 4f + pad;
        }

        // 端の様子: {"x","z","connectedTo":"node"|"split"|"none","net":つながった線の種類,"building":つなぎ口の建物,"insideBuilding":端が敷地に入っている建物}
        // 管は建物のつなぎ口の点につながる(building)。送電線は端が建物の敷地に入れば電気が通る(insideBuilding)。
        // 一般道の端が高速道路の本線につながったら warning を足す。#82 の試運転で、北へ延ばした道路が本線の点につながった。
        // 街の出入りに使うこともあるので、つなぐのは止めない
        private static string EndJson(Vector3 pos, ushort node, string how, NetInfo built)
        {
            ushort owner = node != 0 ? OwnerBuilding(node) : (ushort)0;
            var net = node != 0 ? NetManager.instance.m_nodes.m_buffer[node].Info : null;
            var sb = new StringBuilder("{\"x\":").Append(Mathf.RoundToInt(pos.x)).Append(",\"z\":").Append(Mathf.RoundToInt(pos.z))
                .Append(",\"connectedTo\":").Append(Json.Str(how)).Append(",\"net\":").Append(Json.Str(net != null ? net.name : null))
                .Append(",\"building\":").Append(owner).Append(",\"insideBuilding\":").Append(BuildingAt(pos));
            if (net != null && !IsHighwayMain(built) && IsHighwayMain(net))
            {
                sb.Append(",\"warning\":\"connected to a highway main line\"");
            }

            return sb.Append('}').ToString();
        }

        // 高速道路の本線か(ランプは除く)
        private static bool IsHighwayMain(NetInfo info)
        {
            return info.name.IndexOf("Highway", StringComparison.Ordinal) >= 0 && info.name.IndexOf("Ramp", StringComparison.Ordinal) < 0;
        }

        // 点を持つ建物(つなぎ口の点なら、その建物)。なければ 0。
        // NetNode.m_building は、電柱や管の継ぎ目など、点の飾りの建物を指す(#81 で電柱の番号が返った)。
        // 建物が持つ点は Building.m_netNode からたどれるので、近くの建物の並びに入っているかで持ち主を決める
        internal static ushort OwnerBuilding(ushort node)
        {
            var nodes = NetManager.instance.m_nodes.m_buffer;
            var pos = nodes[node].m_position;
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].m_netNode == 0 || MapApi.IsNetPart(ref bs[i]))
                {
                    continue;
                }

                var d = pos - bs[i].m_position;
                if (d.x * d.x + d.z * d.z > 40000f)
                {
                    continue;
                }

                ushort n = bs[i].m_netNode;
                int guard = 0;
                while (n != 0 && guard++ < 1024)
                {
                    if (n == node)
                    {
                        // 建物の一部(サブ建物)なら、親の建物を返す
                        return bs[i].m_parentBuilding != 0 ? bs[i].m_parentBuilding : (ushort)i;
                    }

                    n = nodes[n].m_nextBuildingNode;
                }
            }

            return 0;
        }

        // その点を敷地に含む建物。なければ 0
        private static ushort BuildingAt(Vector3 pos)
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null || bs[i].m_parentBuilding != 0
                    || MapApi.IsNetPart(ref bs[i]))
                {
                    continue;
                }

                var d = pos - bs[i].m_position;
                if (d.x * d.x + d.z * d.z > 10000f)
                {
                    continue;
                }

                // 建物の向きに合わせて回す。前は (-sin, cos)、右は (cos, sin)(Building.CalculateSidewalkPosition と同じ向き)
                float a = bs[i].m_angle;
                float right = d.x * Mathf.Cos(a) + d.z * Mathf.Sin(a);
                float forward = -d.x * Mathf.Sin(a) + d.z * Mathf.Cos(a);
                if (Mathf.Abs(right) <= bs[i].Info.m_cellWidth * 4f && Mathf.Abs(forward) <= bs[i].Info.m_cellLength * 4f)
                {
                    return (ushort)i;
                }
            }

            return 0;
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
            // 壊した建物の一覧(最大50件)。#82 の試運転で、市長は何を壊したかを数でしか知れなかった
            var removed = new StringBuilder();

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

            // what=abandoned: 放棄された建物と、壊れた・焼けた建物(Collapsed)だけを壊す。区画の建物だけで、サービスの建物と道路は残す。
            // #82 の育てる期間で、市長は放棄された建物を1棟ずつ57回 bulldoze した
            bool abandonedOnly = what == "abandoned";
            if (what == "all" || what == "building" || abandonedOnly)
            {
                var bm = BuildingManager.instance;
                var bs = bm.m_buildings.m_buffer;
                for (int i = 1; i < bs.Length; i++)
                {
                    if ((bs[i].m_flags & Building.Flags.Created) == 0 || (bs[i].m_flags & Building.Flags.Untouchable) != 0)
                    {
                        continue;
                    }

                    if (abandonedOnly && ((bs[i].m_flags & (Building.Flags.Abandoned | Building.Flags.Collapsed)) == 0
                        || bs[i].Info == null || !(bs[i].Info.m_buildingAI is PrivateBuildingAI) || bs[i].m_parentBuilding != 0))
                    {
                        continue;
                    }

                    var d = bs[i].m_position - c;
                    d.y = 0f;
                    if (d.sqrMagnitude <= r2)
                    {
                        if (buildings < 50 && bs[i].Info != null)
                        {
                            removed.Append(removed.Length == 0 ? "" : ",").Append("{\"id\":").Append(i)
                              .Append(",\"prefab\":").Append(Json.Str(bs[i].Info.name))
                              .Append(",\"service\":").Append(Json.Str(bs[i].Info.m_class.m_service.ToString())).Append('}');
                        }

                        bm.ReleaseBuilding((ushort)i);
                        buildings++;
                    }
                }
            }

            return "{\"ok\":true,\"removedSegments\":" + nets + ",\"removedBuildings\":" + buildings + ",\"buildings\":[" + removed + "]}";
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
            return FindSegment(pos, info, null);
        }

        // underground を渡すと、地下の区間(または地上の区間)だけを探す。地下と地上の線は高さが違い、つなげないため(#82)
        private static ushort FindSegment(Vector3 pos, NetInfo info, bool? underground)
        {
            var nm = NetManager.instance;
            var segs = nm.m_segments.m_buffer;
            ushort best = 0;
            float bestD = SplitDistance;
            for (int i = 1; i < segs.Length; i++)
            {
                if ((segs[i].m_flags & NetSegment.Flags.Created) == 0 || segs[i].Info == null
                    || !SameKind(segs[i].Info, info)
                    || (underground != null && segs[i].Info.m_netAI.IsUnderground() != underground.Value)
                    || (skipSegments != null && skipSegments.Contains(i)))
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

            // 分けた点の高さの印を、ゲームの NetTool(区間を分ける処理)と同じに付ける。
            // 地下の区間を分けた点に Underground を付けないと、地上の点として扱われる(#82)
            var nodes = nm.m_nodes.m_buffer;
            if (info.m_netAI.IsUnderground())
            {
                nodes[mid].m_elevation = (byte)((nodes[startNode].m_elevation + nodes[endNode].m_elevation) / 2);
                nodes[mid].m_flags |= NetNode.Flags.Underground;
                nodes[mid].m_flags &= ~NetNode.Flags.OnGround;
            }
            else if (info.m_netAI.IsOverground())
            {
                float terrainY = TerrainManager.instance.SampleRawHeightSmooth(at);
                nodes[mid].m_elevation = (byte)Mathf.Clamp(Mathf.RoundToInt(at.y - terrainY), 1, 255);
                nodes[mid].m_flags &= ~NetNode.Flags.OnGround;
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
            return FindNode(pos, info, null);
        }

        // つないでよい種類か。サービスが同じで、公共交通は小分類(地下鉄と鉄道など)も同じ。
        // 以前はサービスだけを見ていたので、地下鉄の線路が鉄道の点につながりえた(#82)
        private static bool SameKind(NetInfo a, NetInfo b)
        {
            if (a.m_class.m_service != b.m_class.m_service)
            {
                return false;
            }

            return a.m_class.m_service != ItemClass.Service.PublicTransport || a.m_class.m_subService == b.m_class.m_subService;
        }

        // underground を渡すと、地下の点(Underground の印)か地上の点だけを探す。
        // 地下鉄の駅の乗り場(駅の建物の中の地下の線路の端)も地下の点なので、端をそこに置けばつながる(#82)
        internal static ushort FindNode(Vector3 pos, NetInfo info, bool? underground)
        {
            var buf = NetManager.instance.m_nodes.m_buffer;
            ushort best = 0;
            float bestD = SnapDistance * SnapDistance;
            for (int i = 1; i < buf.Length; i++)
            {
                if ((buf[i].m_flags & NetNode.Flags.Created) == 0 || buf[i].Info == null
                    || !SameKind(buf[i].Info, info)
                    || (underground != null && ((buf[i].m_flags & NetNode.Flags.Underground) != 0) != underground.Value))
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
        // 線の途中で、同じサービスの既存の区間(地上のもの)と交わる点を求め、点の並びに足す。足した点の番号を joins に入れる。
        // 交わる点では、既存の点につなぐか、既存の区間を分けて交差点を作る(端と同じ処理)。
        // 一般道は高速道路の本線とは交差点を作らない(本線を平面で横切らせないため)
        private static List<Vector3> InsertCrossings(List<Vector3> pts, NetInfo info, HashSet<int> joins)
        {
            var nm = NetManager.instance;
            var segs = nm.m_segments.m_buffer;
            var nodes = nm.m_nodes.m_buffer;
            bool isHighway = info.name.Contains("Highway");
            var result = new List<Vector3> { pts[0] };
            for (int k = 1; k < pts.Count; k++)
            {
                Vector3 a = pts[k - 1], b = pts[k];
                var hits = new List<KeyValuePair<float, Vector3>>();
                float minX = Mathf.Min(a.x, b.x) - 20f, maxX = Mathf.Max(a.x, b.x) + 20f;
                float minZ = Mathf.Min(a.z, b.z) - 20f, maxZ = Mathf.Max(a.z, b.z) + 20f;
                float len = new Vector2(b.x - a.x, b.z - a.z).magnitude;
                for (int i = 1; i < segs.Length; i++)
                {
                    if ((segs[i].m_flags & NetSegment.Flags.Created) == 0 || segs[i].Info == null
                        || segs[i].Info.m_class.m_service != info.m_class.m_service
                        || (skipSegments != null && skipSegments.Contains(i)))
                    {
                        continue;
                    }

                    var other = segs[i].Info;
                    if (!isHighway && other.name.Contains("Highway") && !other.name.Contains("Ramp"))
                    {
                        continue;
                    }

                    var n0 = nodes[segs[i].m_startNode];
                    var n1 = nodes[segs[i].m_endNode];
                    // 道路は地上の区間だけ(高架・橋・トンネルとは平面で交わらない)。水道管はすべて地下なので問わない。
                    // OnGround の印は MOD が引いた点に付いていないことがあるので、高さと地下の印で見る
                    if (info.m_class.m_service == ItemClass.Service.Road
                        && (n0.m_elevation > 0 || n1.m_elevation > 0
                            || (n0.m_flags & NetNode.Flags.Underground) != 0 || (n1.m_flags & NetNode.Flags.Underground) != 0))
                    {
                        continue;
                    }

                    Vector3 c = n0.m_position, d = n1.m_position;
                    if (Mathf.Max(c.x, d.x) < minX || Mathf.Min(c.x, d.x) > maxX || Mathf.Max(c.z, d.z) < minZ || Mathf.Min(c.z, d.z) > maxZ)
                    {
                        continue;
                    }

                    float t, u;
                    if (!Intersect(a, b, c, d, out t, out u))
                    {
                        continue;
                    }

                    // 線全体の両端の近くは除く(端の処理に任せる)。相手の区間の端(既存の交差点)で交わるときも拾い、
                    // 既存の点につなぐ(FindNode)。前は除いていたので、既存の交差点を通る線がつながらなかった(#82 の g93)
                    if ((k == 1 && t * len < 10f) || (k == pts.Count - 1 && (1f - t) * len < 10f))
                    {
                        continue;
                    }

                    var p = Vector3.Lerp(a, b, t);
                    p.y = 0f;
                    hits.Add(new KeyValuePair<float, Vector3>(t, p));
                }

                hits.Sort((x, y) => x.Key.CompareTo(y.Key));
                float lastT = -1f;
                Vector3? endJoin = null;
                foreach (var h in hits)
                {
                    if ((h.Key - lastT) * len < 8f)
                    {
                        continue; // 近すぎる交わりは1つにまとめる
                    }

                    lastT = h.Key;
                    if (h.Key * len < 8f)
                    {
                        // 区切りの点(Densify の点や途中の点)のすぐそばで交わる: その点を交わりへ動かしてつなぐ
                        result[result.Count - 1] = h.Value;
                        joins.Add(result.Count - 1);
                        continue;
                    }

                    if ((1f - h.Key) * len < 8f)
                    {
                        endJoin = h.Value; // 次の区切りの点を交わりへ動かす
                        continue;
                    }

                    result.Add(h.Value);
                    joins.Add(result.Count - 1);
                }

                result.Add(endJoin ?? b);
                if (endJoin != null)
                {
                    joins.Add(result.Count - 1);
                }
            }

            return result;
        }

        // 2本の線分 a-b と c-d の交わり(水平面)。t は a-b の上の位置、u は c-d の上の位置(0〜1)
        private static bool Intersect(Vector3 a, Vector3 b, Vector3 c, Vector3 d, out float t, out float u)
        {
            t = u = 0f;
            float rx = b.x - a.x, rz = b.z - a.z, sx = d.x - c.x, sz = d.z - c.z;
            float denom = rx * sz - rz * sx;
            if (Mathf.Abs(denom) < 1e-4f)
            {
                return false;
            }

            float qx = c.x - a.x, qz = c.z - a.z;
            t = (qx * sz - qz * sx) / denom;
            u = (qx * rz - qz * rx) / denom;
            // 相手の区間の端をわずかに外れても拾う(点の座標は丸められるため)
            return t > 0f && t < 1f && u >= -0.02f && u <= 1.02f;
        }

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
