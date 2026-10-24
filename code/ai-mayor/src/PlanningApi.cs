using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using ColossalFramework.Math;
using UnityEngine;

namespace AIMayor
{
    // 計画のための読むだけの道具(#100)。街は変えない。
    // - /preview/bulldoze: bulldoze と同じ円で、壊すと何を失うか、どの建物が停電するかを見積もる
    // - /transport/reach: 港・駅・空港が、地図の外とのつなぎ口まで線でつながっているか
    public static class PlanningApi
    {
        private const int Grid = 256;
        private const float CellSize = 38.25f;

        public static void Register(Dictionary<string, System.Func<HttpListenerRequest, string>> routes)
        {
            routes["/preview/bulldoze"] = req => HttpBridge.OnMain(() => PreviewBulldoze(req));
            routes["/transport/reach"] = req => HttpBridge.OnMain(() => TransportReach(req));
        }

        // /preview/bulldoze?x=..&z=..&radius=50&what=all|net|building|abandoned
        // 選び方は /bulldoze と同じ。壊す前と後で電気の網を計算し直し、電気が届かなくなる建物を数える。
        // 電気の網はゲームの ElectricityManager と同じ決まりで作る(UpdateGrid と SimulationStepImpl を読んで写した)。
        // 発電所の容量(足りるか)は見ない。つながりだけを見る
        private static string PreviewBulldoze(HttpListenerRequest req)
        {
            var c = new Vector3(Q(req, "x", 0f), 0f, Q(req, "z", 0f));
            float r2 = Q(req, "radius", 50f);
            r2 *= r2;
            string what = req.QueryString["what"] ?? "all";
            bool abandonedOnly = what == "abandoned";

            var bm = BuildingManager.instance;
            var bs = bm.m_buildings.m_buffer;
            var nm = NetManager.instance;
            var segs = nm.m_segments.m_buffer;

            // 壊す建物と区間(/bulldoze と同じ選び方)
            var targetBuildings = new HashSet<ushort>();
            if (what == "all" || what == "building" || abandonedOnly)
            {
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
                        targetBuildings.Add((ushort)i);
                    }
                }
            }

            var targetSegments = new HashSet<ushort>();
            if (what == "all" || what == "net")
            {
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
                        targetSegments.Add((ushort)i);
                    }
                }
            }

            // 壊す建物が失うもの
            var sb = new StringBuilder("{\"ok\":true");
            int lostJobs = 0, lostHomes = 0;
            var listed = new StringBuilder();
            var water = new StringBuilder();
            var transport = new StringBuilder();
            int shown = 0;
            foreach (var id in targetBuildings)
            {
                var info = bs[id].Info;
                if (info == null)
                {
                    continue;
                }

                int jobs, homes;
                JobsHomes(id, ref bs[id], out jobs, out homes);
                lostJobs += jobs;
                lostHomes += homes;
                var svc = info.m_class.m_service;
                if (shown < 50)
                {
                    listed.Append(shown == 0 ? "" : ",").Append("{\"id\":").Append(id)
                      .Append(",\"prefab\":").Append(Json.Str(info.name))
                      .Append(",\"service\":").Append(Json.Str(svc.ToString()))
                      .Append(",\"jobs\":").Append(jobs).Append(",\"homes\":").Append(homes).Append('}');
                    shown++;
                }

                if (svc == ItemClass.Service.Water)
                {
                    water.Append(water.Length == 0 ? "" : ",").Append("{\"id\":").Append(id)
                      .Append(",\"prefab\":").Append(Json.Str(info.name)).Append('}');
                }

                if (svc == ItemClass.Service.PublicTransport && bs[id].m_netNode != 0)
                {
                    transport.Append(transport.Length == 0 ? "" : ",").Append("{\"id\":").Append(id)
                      .Append(",\"prefab\":").Append(Json.Str(info.name)).Append('}');
                }
            }

            int powerLines = 0;
            foreach (var s in targetSegments)
            {
                if (segs[s].Info != null && segs[s].Info.m_class.m_service == ItemClass.Service.Electricity)
                {
                    powerLines++;
                }
            }

            sb.Append(",\"targets\":{\"buildings\":").Append(targetBuildings.Count)
              .Append(",\"segments\":").Append(targetSegments.Count)
              .Append(",\"powerLineSegments\":").Append(powerLines)
              .Append(",\"list\":[").Append(listed).Append("]}");
            sb.Append(",\"lost\":{\"jobs\":").Append(lostJobs).Append(",\"homes\":").Append(lostHomes).Append('}');
            sb.Append(",\"waterFacilities\":[").Append(water).Append(']');
            sb.Append(",\"transportStations\":[").Append(transport).Append(']');

            // 電気: 壊す前と後で網を作り、発電所からたどる
            var none = new HashSet<ushort>();
            var condBefore = Conductivity(none);
            var condAfter = targetBuildings.Count > 0 ? Conductivity(targetBuildings) : condBefore;
            var sourcesBefore = Sources(none);
            var sourcesAfter = Sources(targetBuildings);
            var powerBefore = Reach(condBefore, sourcesBefore, none);
            var powerAfter = Reach(condAfter, sourcesAfter, targetSegments);

            // 見積もりの網が、ゲームの今の網とどれだけ合うか(電気を通すマスのうち、届く・届かないが一致した割合)
            // ゲームの網は外から読めないので、マスの中心で CheckElectricity を呼んで比べる
            var em = ElectricityManager.instance;
            int conductive = 0, agree = 0;
            for (int i = 0; i < Grid * Grid; i++)
            {
                if (condBefore[i] == 0)
                {
                    continue;
                }

                conductive++;
                bool on;
                em.CheckElectricity(new Vector3((i % Grid + 0.5f - 128f) * CellSize, 0f, (i / Grid + 0.5f - 128f) * CellSize), out on);
                if (on == powerBefore[i])
                {
                    agree++;
                }
            }

            int losing = 0, losingHomes = 0, losingJobs = 0, listedLosing = 0;
            var losingList = new StringBuilder();
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || targetBuildings.Contains((ushort)i) || !NeedsPower(bs[i].Info))
                {
                    continue;
                }

                int cell = Cell(bs[i].m_position);
                if (!powerBefore[cell] || powerAfter[cell])
                {
                    continue;
                }

                losing++;
                int jobs, homes;
                JobsHomes((ushort)i, ref bs[i], out jobs, out homes);
                losingJobs += jobs;
                losingHomes += homes;
                if (listedLosing < 30)
                {
                    losingList.Append(listedLosing == 0 ? "" : ",").Append("{\"id\":").Append(i)
                      .Append(",\"prefab\":").Append(Json.Str(bs[i].Info.name))
                      .Append(",\"service\":").Append(Json.Str(bs[i].Info.m_class.m_service.ToString()))
                      .Append(",\"x\":").Append(R(bs[i].m_position.x)).Append(",\"z\":").Append(R(bs[i].m_position.z)).Append('}');
                    listedLosing++;
                }
            }

            int plantsRemoved = 0;
            foreach (var id in targetBuildings)
            {
                if (bs[id].Info != null && bs[id].Info.m_buildingAI is PowerPlantAI)
                {
                    plantsRemoved++;
                }
            }

            sb.Append(",\"power\":{\"buildingsLosingPower\":").Append(losing)
              .Append(",\"homesLosingPower\":").Append(losingHomes)
              .Append(",\"jobsLosingPower\":").Append(losingJobs)
              .Append(",\"powerPlantsRemoved\":").Append(plantsRemoved)
              .Append(",\"list\":[").Append(losingList).Append(']')
              .Append(",\"modelAgreement\":").Append(conductive == 0 ? "null" : (agree / (double)conductive).ToString("0.000", CultureInfo.InvariantCulture))
              .Append('}');
            sb.Append(",\"note\":").Append(Json.Str("電気はつながりだけを見る。発電所の容量が足りるかは見ない。modelAgreement が低いときは、見積もりを信じすぎない"));
            return sb.Append('}').ToString();
        }

        // ElectricityManager.UpdateGrid と同じ計算で、マスごとの電気の通りやすさを作る。except の建物は除く
        private static byte[] Conductivity(HashSet<ushort> except)
        {
            var cond = new byte[Grid * Grid];
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int id = 1; id < bs.Length; id++)
            {
                if ((bs[id].m_flags & (Building.Flags.Created | Building.Flags.Deleted)) != Building.Flags.Created || except.Contains((ushort)id))
                {
                    continue;
                }

                BuildingInfo info;
                int width, length;
                bs[id].GetInfoWidthLength(out info, out width, out length);
                if (info == null)
                {
                    continue;
                }

                float radius = info.m_buildingAI.ElectricityGridRadius();
                if (radius <= 0.1f)
                {
                    continue;
                }

                var pos = bs[id].m_position;
                float angle = bs[id].m_angle;
                var v = new Vector3(Mathf.Cos(angle), 0f, Mathf.Sin(angle));
                var v2 = new Vector3(v.z, 0f, -v.x);
                var a = pos - width * 4 * v - length * 4 * v2;
                var b = pos + width * 4 * v - length * 4 * v2;
                var cc = pos + width * 4 * v + length * 4 * v2;
                var d = pos - width * 4 * v + length * 4 * v2;
                float minX = Mathf.Min(Mathf.Min(a.x, b.x), Mathf.Min(cc.x, d.x)) - radius;
                float maxX = Mathf.Max(Mathf.Max(a.x, b.x), Mathf.Max(cc.x, d.x)) + radius;
                float minZ = Mathf.Min(Mathf.Min(a.z, b.z), Mathf.Min(cc.z, d.z)) - radius;
                float maxZ = Mathf.Max(Mathf.Max(a.z, b.z), Mathf.Max(cc.z, d.z)) + radius;
                int x0 = Mathf.Max(0, (int)(minX / CellSize + 128f));
                int x1 = Mathf.Min(Grid - 1, (int)(maxX / CellSize + 128f));
                int z0 = Mathf.Max(0, (int)(minZ / CellSize + 128f));
                int z1 = Mathf.Min(Grid - 1, (int)(maxZ / CellSize + 128f));
                for (int m = z0; m <= z1; m++)
                {
                    for (int n = x0; n <= x1; n++)
                    {
                        var p = new Vector3((n + 0.5f - 128f) * CellSize, pos.y, (m + 0.5f - 128f) * CellSize);
                        float dx = Mathf.Max(0f, Mathf.Abs(Vector3.Dot(v, p - pos)) - width * 4);
                        float dz = Mathf.Max(0f, Mathf.Abs(Vector3.Dot(v2, p - pos)) - length * 4);
                        float dist = Mathf.Sqrt(dx * dx + dz * dz);
                        if (dist < radius + 19.125f)
                        {
                            int value = Mathf.Min(255, Mathf.RoundToInt(((radius - dist) * (2f / 153f) + 0.25f) * 255f));
                            int k = m * Grid + n;
                            if (value > cond[k])
                            {
                                cond[k] = (byte)value;
                            }
                        }
                    }
                }
            }

            return cond;
        }

        // 電気を流し込むマス。発電所(PowerPlantAI とその仲間)の敷地のマスとする。
        // ゲームは発電所の位置のマス(大きな発電所はまわりの数マス)に TryDumpElectricity する
        private static List<int> Sources(HashSet<ushort> except)
        {
            var list = new List<int>();
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int id = 1; id < bs.Length; id++)
            {
                if ((bs[id].m_flags & Building.Flags.Created) == 0 || except.Contains((ushort)id))
                {
                    continue;
                }

                var info = bs[id].Info;
                if (info == null || !(info.m_buildingAI is PowerPlantAI) || bs[id].m_productionRate == 0
                    || (bs[id].m_flags & (Building.Flags.Abandoned | Building.Flags.Collapsed)) != 0)
                {
                    continue;
                }

                var pos = bs[id].m_position;
                float half = Mathf.Max(bs[id].Width, bs[id].Length) * 4f;
                int x0 = Mathf.Clamp((int)((pos.x - half) / CellSize + 128f), 0, Grid - 1);
                int x1 = Mathf.Clamp((int)((pos.x + half) / CellSize + 128f), 0, Grid - 1);
                int z0 = Mathf.Clamp((int)((pos.z - half) / CellSize + 128f), 0, Grid - 1);
                int z1 = Mathf.Clamp((int)((pos.z + half) / CellSize + 128f), 0, Grid - 1);
                for (int m = z0; m <= z1; m++)
                {
                    for (int n = x0; n <= x1; n++)
                    {
                        list.Add(m * Grid + n);
                    }
                }
            }

            return list;
        }

        // ElectricityManager.SimulationStepImpl と同じ決まりで、発電所から届くマスをたどる。
        // マスからは上下左右へ。通りやすさ64未満のマスは、縦と横の両方に64以上の隣があるときだけ入れる。
        // マスの中の電気の線(送電線など)の点に乗り、線をたどって遠くのマスへ降りる。removedSegments の区間は通らない
        private static bool[] Reach(byte[] cond, List<int> sources, HashSet<ushort> removedSegments)
        {
            var nm = NetManager.instance;
            var nodes = nm.m_nodes.m_buffer;
            var segs = nm.m_segments.m_buffer;
            var cellOn = new bool[Grid * Grid];
            var nodeOn = new bool[nodes.Length];
            var cellQueue = new Queue<int>();
            var nodeQueue = new Queue<ushort>();

            foreach (var s in sources)
            {
                if (cond[s] != 0 && !cellOn[s])
                {
                    cellOn[s] = true;
                    cellQueue.Enqueue(s);
                }
            }

            while (cellQueue.Count > 0 || nodeQueue.Count > 0)
            {
                while (cellQueue.Count > 0)
                {
                    int k = cellQueue.Dequeue();
                    int x = k % Grid, z = k / Grid;
                    int limit = cond[k] >= 64 ? 1 : 64;
                    TryCell(cond, cellOn, cellQueue, x, z - 1, limit);
                    TryCell(cond, cellOn, cellQueue, x - 1, z, limit);
                    TryCell(cond, cellOn, cellQueue, x, z + 1, limit);
                    TryCell(cond, cellOn, cellQueue, x + 1, z, limit);

                    // マスの中の電気の線の点
                    float minX = (x - 128f) * CellSize, minZ = (z - 128f) * CellSize;
                    float maxX = minX + CellSize, maxZ = minZ + CellSize;
                    int gx0 = Mathf.Max((int)(minX / 64f + 135f), 0), gz0 = Mathf.Max((int)(minZ / 64f + 135f), 0);
                    int gx1 = Mathf.Min((int)(maxX / 64f + 135f), 269), gz1 = Mathf.Min((int)(maxZ / 64f + 135f), 269);
                    for (int gz = gz0; gz <= gz1; gz++)
                    {
                        for (int gx = gx0; gx <= gx1; gx++)
                        {
                            ushort n = nm.m_nodeGrid[gz * 270 + gx];
                            int guard = 0;
                            while (n != 0 && guard++ < 32768)
                            {
                                var p = nodes[n].m_position;
                                if (p.x >= minX && p.z >= minZ && p.x <= maxX && p.z <= maxZ && ConductsNode(ref nodes[n], segs, removedSegments) && !nodeOn[n])
                                {
                                    nodeOn[n] = true;
                                    nodeQueue.Enqueue(n);
                                }

                                n = nodes[n].m_nextGridNode;
                            }
                        }
                    }
                }

                while (nodeQueue.Count > 0)
                {
                    ushort n = nodeQueue.Dequeue();
                    // 点からそのマスへ降りる(通りやすさ1以上)
                    int k = Cell(nodes[n].m_position);
                    TryCell(cond, cellOn, cellQueue, k % Grid, k / Grid, 1);
                    for (int i = 0; i < 8; i++)
                    {
                        ushort s = nodes[n].GetSegment(i);
                        if (s == 0 || removedSegments.Contains(s))
                        {
                            continue;
                        }

                        ushort other = segs[s].m_startNode != n ? segs[s].m_startNode : segs[s].m_endNode;
                        if (!nodeOn[other] && ConductsNode(ref nodes[other], segs, removedSegments))
                        {
                            nodeOn[other] = true;
                            nodeQueue.Enqueue(other);
                        }
                    }
                }
            }

            return cellOn;
        }

        // ゲームの ConductToCell と同じ入れる条件
        private static void TryCell(byte[] cond, bool[] on, Queue<int> queue, int x, int z, int limit)
        {
            if (x < 0 || z < 0 || x >= Grid || z >= Grid)
            {
                return;
            }

            int k = z * Grid + x;
            if (on[k] || cond[k] == 0 || cond[k] < limit)
            {
                return;
            }

            if (cond[k] < 64)
            {
                bool xOk = (x > 0 && cond[k - 1] >= 64) || (x < Grid - 1 && cond[k + 1] >= 64);
                bool zOk = (z > 0 && cond[k - Grid] >= 64) || (z < Grid - 1 && cond[k + Grid] >= 64);
                if (!xOk || !zOk)
                {
                    return;
                }
            }

            on[k] = true;
            queue.Enqueue(k);
        }

        // 電気を通す点か(電気のサービスの線か、ConcourseAI)。区間が全部壊れる点は通さない
        private static bool ConductsNode(ref NetNode node, NetSegment[] segs, HashSet<ushort> removedSegments)
        {
            if (node.m_flags == NetNode.Flags.None || node.Info == null)
            {
                return false;
            }

            if (node.Info.m_class.m_service != ItemClass.Service.Electricity && !(node.Info.m_netAI is ConcourseAI))
            {
                return false;
            }

            if (removedSegments.Count == 0)
            {
                return true;
            }

            int total = 0, removed = 0;
            for (int i = 0; i < 8; i++)
            {
                ushort s = node.GetSegment(i);
                if (s == 0)
                {
                    continue;
                }

                total++;
                if (removedSegments.Contains(s))
                {
                    removed++;
                }
            }

            return total == 0 || removed < total;
        }

        // /transport/reach  港・駅・空港(公共交通の建物で、自分の線を持つもの)が、地図の外とのつなぎ口まで線でつながっているか。
        // 建物の線(船着き場、ホーム、滑走路など)から、同じ種類(subService)の公共交通の線をたどり、つなぎ口の点に届くかを見る。
        // 船着き場の端の点は、区間がなくても、いちばん近い航路の車線へ見えないつなぎ(NetNode.m_lane)を張る(ShipDockAI.UpdateLaneConnection)。
        // このつなぎもたどる。#100 の初めは区間だけをたどり、港が航路につながっていないと読み違えた
        // つながっていなければ、外へつながる網までのいちばん近いすき間(m)と、その両端の座標を返す。
        // outsideLines: ゲームが建物と外のつなぎ口の間に作った線(Ship Line、Airplane Line など)の区間の数。
        // ゲームは道筋が見つかると、この線を自動で作る(#100 で、つながらない港には作られず、空港には作られた)
        private static string TransportReach(HttpListenerRequest req)
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var nm = NetManager.instance;
            var nodes = nm.m_nodes.m_buffer;
            var segs = nm.m_segments.m_buffer;

            // 種類ごとに、外のつなぎ口から届く点を先に印付けする
            var reachCache = new Dictionary<ItemClass.SubService, bool[]>();
            var sb = new StringBuilder("{\"ok\":true,\"stations\":[");
            int count = 0;
            for (int id = 1; id < bs.Length; id++)
            {
                if ((bs[id].m_flags & Building.Flags.Created) == 0 || bs[id].m_netNode == 0 || bs[id].Info == null
                    || bs[id].Info.m_class.m_service != ItemClass.Service.PublicTransport || bs[id].m_parentBuilding != 0)
                {
                    continue;
                }

                var sub = bs[id].Info.m_class.m_subService;
                bool[] outside;
                if (!reachCache.TryGetValue(sub, out outside))
                {
                    outside = FromOutside(sub);
                    reachCache[sub] = outside;
                }

                // 建物の点から、同じ種類の線をたどる
                var own = new HashSet<ushort>();
                var queue = new Queue<ushort>();
                int guard = 0;
                for (ushort n = bs[id].m_netNode; n != 0 && guard++ < 32768; n = nodes[n].m_nextBuildingNode)
                {
                    if (own.Add(n))
                    {
                        queue.Enqueue(n);
                    }
                }

                bool connected = false;
                bool viaLane = false;
                var lanes = nm.m_lanes.m_buffer;
                while (queue.Count > 0)
                {
                    ushort n = queue.Dequeue();
                    if (outside[n])
                    {
                        connected = true;
                        break;
                    }

                    // 見えない車線のつなぎ(船着き場の端など)
                    uint lane = nodes[n].m_lane;
                    if (lane != 0)
                    {
                        ushort ls = lanes[lane].m_segment;
                        if (ls != 0 && (segs[ls].m_flags & NetSegment.Flags.Created) != 0)
                        {
                            viaLane = true;
                            if (own.Add(segs[ls].m_startNode))
                            {
                                queue.Enqueue(segs[ls].m_startNode);
                            }

                            if (own.Add(segs[ls].m_endNode))
                            {
                                queue.Enqueue(segs[ls].m_endNode);
                            }
                        }
                    }

                    for (int i = 0; i < 8; i++)
                    {
                        ushort s = nodes[n].GetSegment(i);
                        if (s == 0 || !SameKind(segs[s].Info, sub))
                        {
                            continue;
                        }

                        ushort other = segs[s].m_startNode != n ? segs[s].m_startNode : segs[s].m_endNode;
                        if (own.Add(other))
                        {
                            queue.Enqueue(other);
                        }
                    }
                }

                var pos = bs[id].m_position;
                sb.Append(count == 0 ? "" : ",").Append("{\"id\":").Append(id)
                  .Append(",\"prefab\":").Append(Json.Str(bs[id].Info.name))
                  .Append(",\"kind\":").Append(Json.Str(sub.ToString().Replace("PublicTransport", "").ToLowerInvariant()))
                  .Append(",\"x\":").Append(R(pos.x)).Append(",\"z\":").Append(R(pos.z))
                  .Append(",\"outsideConnected\":").Append(connected ? "true" : "false")
                  .Append(",\"viaLaneConnection\":").Append(viaLane ? "true" : "false")
                  .Append(",\"outsideLines\":").Append(OutsideLines(pos, sub));
                if (!connected)
                {
                    // 建物の網と、外へつながる網のいちばん近い点どうし
                    float best = float.MaxValue;
                    Vector3 from = Vector3.zero, to = Vector3.zero;
                    foreach (var a in own)
                    {
                        for (int k = 1; k < nodes.Length; k++)
                        {
                            if (!outside[k])
                            {
                                continue;
                            }

                            var d = nodes[k].m_position - nodes[a].m_position;
                            d.y = 0f;
                            float m = d.sqrMagnitude;
                            if (m < best)
                            {
                                best = m;
                                from = nodes[a].m_position;
                                to = nodes[k].m_position;
                            }
                        }
                    }

                    if (best < float.MaxValue)
                    {
                        sb.Append(",\"gap\":{\"meters\":").Append(R(Mathf.Sqrt(best)))
                          .Append(",\"from\":{\"x\":").Append(R(from.x)).Append(",\"z\":").Append(R(from.z)).Append('}')
                          .Append(",\"to\":{\"x\":").Append(R(to.x)).Append(",\"z\":").Append(R(to.z)).Append("}}");
                    }
                    else
                    {
                        sb.Append(",\"gap\":null");
                    }
                }

                sb.Append('}');
                count++;
            }

            return sb.Append("]}").ToString();
        }

        // 地図の外とのつなぎ口の点(NetNode.Flags.Outside)から、同じ種類の線でたどれる点
        private static bool[] FromOutside(ItemClass.SubService sub)
        {
            var nm = NetManager.instance;
            var nodes = nm.m_nodes.m_buffer;
            var segs = nm.m_segments.m_buffer;
            var on = new bool[nodes.Length];
            var queue = new Queue<ushort>();
            for (int i = 1; i < nodes.Length; i++)
            {
                if ((nodes[i].m_flags & NetNode.Flags.Outside) != 0 && nodes[i].Info != null && SameKind(nodes[i].Info, sub))
                {
                    on[i] = true;
                    queue.Enqueue((ushort)i);
                }
            }

            while (queue.Count > 0)
            {
                ushort n = queue.Dequeue();
                for (int i = 0; i < 8; i++)
                {
                    ushort s = nodes[n].GetSegment(i);
                    if (s == 0 || !SameKind(segs[s].Info, sub))
                    {
                        continue;
                    }

                    ushort other = segs[s].m_startNode != n ? segs[s].m_startNode : segs[s].m_endNode;
                    if (!on[other])
                    {
                        on[other] = true;
                        queue.Enqueue(other);
                    }
                }
            }

            return on;
        }

        // 公共交通の、同じ種類の線か。路線そのもの(TransportLineAI。Ship Line など)は道ではないので外す
        private static bool SameKind(NetInfo info, ItemClass.SubService sub)
        {
            return info != null && info.m_class.m_service == ItemClass.Service.PublicTransport
                && info.m_class.m_subService == sub && !(info.m_netAI is TransportLineAI);
        }

        // 建物のそばに端がある、ゲームが作った外への線(TransportLineAI の区間)の数
        private static int OutsideLines(Vector3 pos, ItemClass.SubService sub)
        {
            var nm = NetManager.instance;
            var nodes = nm.m_nodes.m_buffer;
            var segs = nm.m_segments.m_buffer;
            int n = 0;
            for (int i = 1; i < segs.Length; i++)
            {
                if ((segs[i].m_flags & NetSegment.Flags.Created) == 0 || segs[i].Info == null
                    || !(segs[i].Info.m_netAI is TransportLineAI) || segs[i].Info.m_class.m_subService != sub)
                {
                    continue;
                }

                var a = nodes[segs[i].m_startNode].m_position - pos;
                var b = nodes[segs[i].m_endNode].m_position - pos;
                a.y = 0f;
                b.y = 0f;
                if (a.sqrMagnitude < 200f * 200f || b.sqrMagnitude < 200f * 200f)
                {
                    n++;
                }
            }

            return n;
        }

        private static bool NeedsPower(BuildingInfo info)
        {
            if (info == null)
            {
                return false;
            }

            if (info.m_buildingAI is PrivateBuildingAI)
            {
                return true;
            }

            var player = info.m_buildingAI as PlayerBuildingAI;
            return player != null && player.m_electricityConsumption > 0;
        }

        // 働き口と家の数(建物の画面と同じ計算。CityApi.DetailJson と同じ)
        private static void JobsHomes(ushort id, ref Building b, out int jobs, out int homes)
        {
            jobs = 0;
            homes = 0;
            var info = b.Info;
            if (info == null || (b.m_flags & (Building.Flags.Abandoned | Building.Flags.Collapsed)) != 0)
            {
                return;
            }

            int l0, l1, l2, l3;
            var pai = info.m_buildingAI as PrivateBuildingAI;
            if (pai != null)
            {
                pai.CalculateWorkplaceCount((ItemClass.Level)b.m_level, new Randomizer(id), b.Width, b.Length, out l0, out l1, out l2, out l3);
                pai.AdjustWorkplaceCount(id, ref b, ref l0, ref l1, ref l2, ref l3);
                jobs = l0 + l1 + l2 + l3;
                if (info.m_class.m_service == ItemClass.Service.Residential)
                {
                    homes = pai.CalculateHomeCount((ItemClass.Level)b.m_level, new Randomizer(id), b.Width, b.Length);
                }

                return;
            }

            var player = info.m_buildingAI as PlayerBuildingAI;
            if (player != null)
            {
                player.CountWorkPlaces(out l0, out l1, out l2, out l3);
                jobs = l0 + l1 + l2 + l3;
            }
        }

        private static int Cell(Vector3 p)
        {
            int x = Mathf.Clamp((int)(p.x / CellSize + 128f), 0, Grid - 1);
            int z = Mathf.Clamp((int)(p.z / CellSize + 128f), 0, Grid - 1);
            return z * Grid + x;
        }

        private static float Q(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }

        private static string R(float v)
        {
            return Mathf.RoundToInt(v).ToString(CultureInfo.InvariantCulture);
        }
    }
}
