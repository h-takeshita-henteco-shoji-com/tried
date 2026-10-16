using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using ColossalFramework;
using ColossalFramework.Math;
using UnityEngine;

namespace AIMayor
{
    // マップエディター用の窓口。出発点のマップを人が整えるために使う(設計: docs/editor-interface.md)。
    // 市長の運営中にマップの条件を変えられないよう、状態の確認(/editor/state)以外はマップエディターの中でだけ動く。
    // 座標はゲームと同じ。x が東、z が北、地図の中心が (0, 0)、端が ±8640。
    public static class EditorApi
    {
        private const float MapHalf = 8640f;
        private const float EdgeTolerance = 50f;
        private const float CellSize = 33.75f; // 天然資源のマス
        private const int Grid = 512;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/editor/state"] = req => HttpBridge.OnMain(State);
            routes["/editor/outside"] = Guard(OutsideConnection);
            routes["/editor/resource"] = Guard(PaintResource);
            routes["/editor/forest"] = Guard(PlantForest);
            routes["/editor/forest_cells"] = Guard(PlantForestCells);
            routes["/editor/resource_map"] = Guard(req => HttpBridge.OnMain(() => ResourceMap(req)));
            routes["/editor/water_source"] = Guard(AddWaterSource);
            routes["/editor/water_sources"] = Guard(req => HttpBridge.OnSimulation(ListWaterSources));
            routes["/editor/water_source/remove"] = Guard(RemoveWaterSource);
            routes["/editor/carve"] = Guard(Carve);
            routes["/editor/terrain/restore"] = Guard(req => HttpBridge.OnSimulation(RestoreTerrain, 60000));
            routes["/editor/water_profile"] = Guard(WaterProfile);
            routes["/editor/rebridge"] = Guard(Rebridge);
        }

        // マップエディターの中でなければ断る
        private static Func<HttpListenerRequest, string> Guard(Func<HttpListenerRequest, string> handler)
        {
            return req => InEditor() ? handler(req) : HttpBridge.Error("map editor only (今のモード: " + ModeName() + ")");
        }

        private static bool InEditor()
        {
            var tm = Singleton<ToolManager>.exists ? ToolManager.instance : null;
            return tm != null && tm.m_properties != null && (tm.m_properties.m_mode & ItemClass.Availability.MapEditor) != 0;
        }

        private static string ModeName()
        {
            var tm = Singleton<ToolManager>.exists ? ToolManager.instance : null;
            return tm != null && tm.m_properties != null ? tm.m_properties.m_mode.ToString() : "none";
        }

        // ---- 状態 ----

        private static string State()
        {
            var sb = new StringBuilder("{\"ok\":true");
            sb.Append(",\"mode\":").Append(Json.Str(ModeName()));
            sb.Append(",\"editor\":").Append(InEditor() ? "true" : "false");

            var bm = BuildingManager.instance;
            sb.Append(",\"outsideConnections\":{");
            Count(sb, bm, "road", ItemClass.Service.Road, ItemClass.SubService.None, true);
            Count(sb, bm, "train", ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportTrain, false);
            Count(sb, bm, "ship", ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportShip, false);
            Count(sb, bm, "plane", ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportPlane, false);
            sb.Append('}');

            uint ore, oil, forest, fertility, water;
            NaturalResourceManager.instance.CalculateTotalResources(out ore, out oil, out forest, out fertility, out water);
            sb.Append(",\"resources\":{\"ore\":").Append(ore).Append(",\"oil\":").Append(oil)
              .Append(",\"forest\":").Append(forest).Append(",\"fertility\":").Append(fertility)
              .Append(",\"water\":").Append(water).Append('}');

            sb.Append(",\"trees\":{\"count\":").Append(TreeManager.instance.m_treeCount)
              .Append(",\"mapLimit\":").Append(TreeManager.MAX_MAP_TREES)
              .Append(",\"gameLimit\":").Append(TreeManager.MAX_TREE_COUNT).Append('}');

            var ws = TerrainManager.instance.WaterSimulation.m_waterSources;
            int sources = 0;
            for (int i = 0; i < ws.m_size; i++)
            {
                if (ws.m_buffer[i].m_type != 0)
                {
                    sources++;
                }
            }

            sb.Append(",\"waterSources\":").Append(sources);
            return sb.Append('}').ToString();
        }

        private static void Count(StringBuilder sb, BuildingManager bm, string key, ItemClass.Service s, ItemClass.SubService sub, bool first)
        {
            int incoming, outgoing;
            bm.CalculateOutsideConnectionCount(s, sub, out incoming, out outgoing);
            sb.Append(first ? "" : ",").Append(Json.Str(key)).Append(":{\"in\":").Append(incoming).Append(",\"out\":").Append(outgoing).Append('}');
        }

        // ---- つなぎ口 ----

        // POST /editor/outside?prefab=..&y=..  本文は "x,z;x,z;..."。最初か最後の点を地図の端から50m以内に置く
        private static string OutsideConnection(HttpListenerRequest req)
        {
            string prefab = req.QueryString["prefab"];
            if (string.IsNullOrEmpty(prefab))
            {
                return HttpBridge.Error("prefab is required");
            }

            float? fixedY = null;
            float y;
            if (float.TryParse(req.QueryString["y"] ?? "", NumberStyles.Float, CultureInfo.InvariantCulture, out y))
            {
                fixedY = y;
            }

            List<Vector3> points;
            try
            {
                points = NetApi.Parse(ReadBody(req));
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad points: " + e.Message);
            }

            if (points.Count < 2)
            {
                return HttpBridge.Error("need at least 2 points");
            }

            return HttpBridge.OnSimulation(() =>
            {
                var info = PrefabCollection<NetInfo>.FindLoaded(prefab);
                if (info == null)
                {
                    return HttpBridge.Error("prefab not found: " + prefab);
                }

                // 端に近い点を、地図の端の少し外へ動かす(ゲームの線を引く道具と同じ位置)
                var edges = new List<int>();
                foreach (int idx in new[] { 0, points.Count - 1 })
                {
                    var p = points[idx];
                    if (MapHalf - Mathf.Max(Mathf.Abs(p.x), Mathf.Abs(p.z)) <= EdgeTolerance)
                    {
                        points[idx] = ToEdge(p, info.m_halfWidth);
                        edges.Add(idx);
                    }
                }

                if (edges.Count == 0)
                {
                    return HttpBridge.Error("最初か最後の点を、地図の端(±8640)から50m以内に置く");
                }

                int inBefore, outBefore;
                BuildingManager.instance.CalculateOutsideConnectionCount(info.m_class.m_service, info.m_class.m_subService, out inBefore, out outBefore);
                if (inBefore >= 4 && outBefore >= 4)
                {
                    return HttpBridge.Error("この種類のつなぎ口は上限(入り4・出4)に達している");
                }

                // 端に届く区間だけ、つなぎ口用の線(例: Train Connection Track)で引く。ゲームの線を引く道具と同じ
                var conn = ConnectedInfo(info);
                string connName = conn != null ? conn.name : prefab;
                int first = edges.Contains(0) ? 1 : 0;
                int last = edges.Contains(points.Count - 1) ? points.Count - 2 : points.Count - 1;
                var builds = new List<string>();
                if (edges.Contains(0))
                {
                    builds.Add(NetApi.BuildOnSimulation(connName, NetApi.Densify(points.GetRange(0, 2)), false, fixedY));
                }

                if (last - first >= 1)
                {
                    builds.Add(NetApi.BuildOnSimulation(prefab, NetApi.Densify(points.GetRange(first, last - first + 1)), false, fixedY));
                }

                if (edges.Contains(points.Count - 1))
                {
                    builds.Add(NetApi.BuildOnSimulation(connName, NetApi.Densify(points.GetRange(points.Count - 2, 2)), false, fixedY));
                }

                foreach (var r in builds)
                {
                    if (r.IndexOf("\"ok\":true", StringComparison.Ordinal) < 0)
                    {
                        return r;
                    }
                }

                string built = "[" + string.Join(",", builds.ToArray()) + "]";
                if (conn != null)
                {
                    info = conn;
                }

                // 端の点に「外」の印を付ける。ゲームがつなぎ口の建物を置く
                var nm = NetManager.instance;
                int marked = 0;
                foreach (int idx in edges)
                {
                    var pos = points[idx];
                    pos.y = fixedY ?? TerrainManager.instance.SampleRawHeightSmooth(pos);
                    ushort node = NetApi.FindNode(pos, info);
                    if (node != 0)
                    {
                        nm.m_nodes.m_buffer[node].m_flags |= NetNode.Flags.Outside;
                        nm.UpdateNode(node);
                        marked++;
                    }
                }

                int inAfter, outAfter;
                BuildingManager.instance.CalculateOutsideConnectionCount(info.m_class.m_service, info.m_class.m_subService, out inAfter, out outAfter);
                return "{\"ok\":true,\"prefab\":" + Json.Str(prefab) + ",\"markedNodes\":" + marked
                    + ",\"before\":{\"in\":" + inBefore + ",\"out\":" + outBefore + "}"
                    + ",\"after\":{\"in\":" + inAfter + ",\"out\":" + outAfter + "}"
                    + ",\"connectionPrefab\":" + Json.Str(connName) + ",\"build\":" + built + "}";
            });
        }

        // つなぎ口用の線。線路と飛行機の経路は m_connectedInfo に持つ。なければ名前から探す(Ship Path → Ship Connection Path)
        private static NetInfo ConnectedInfo(NetInfo info)
        {
            var field = info.m_netAI.GetType().GetField("m_connectedInfo");
            var conn = field != null ? field.GetValue(info.m_netAI) as NetInfo : null;
            if (conn != null)
            {
                return conn;
            }

            if (info.name.EndsWith(" Path", StringComparison.Ordinal))
            {
                return PrefabCollection<NetInfo>.FindLoaded(info.name.Substring(0, info.name.Length - 5) + " Connection Path");
            }

            return null;
        }

        private static Vector3 ToEdge(Vector3 p, float halfWidth)
        {
            float outside = MapHalf + halfWidth * 0.8f;
            float limit = MapHalf - halfWidth;
            if (Mathf.Abs(p.x) >= Mathf.Abs(p.z))
            {
                p.x = Mathf.Sign(p.x) * outside;
                p.z = Mathf.Clamp(p.z, -limit, limit);
            }
            else
            {
                p.z = Mathf.Sign(p.z) * outside;
                p.x = Mathf.Clamp(p.x, -limit, limit);
            }

            return p;
        }

        // ---- 天然資源 ----

        // POST /editor/resource?type=ore|oil|fertility|sand&amount=0..255&mode=set|clear  本文は多角形 "x,z;x,z;..."
        private static string PaintResource(HttpListenerRequest req)
        {
            string type = req.QueryString["type"] ?? "";
            if (type != "ore" && type != "oil" && type != "fertility" && type != "sand")
            {
                return HttpBridge.Error("type は ore / oil / fertility / sand");
            }

            int amount;
            int.TryParse(req.QueryString["amount"] ?? "255", NumberStyles.Integer, CultureInfo.InvariantCulture, out amount);
            amount = Mathf.Clamp(amount, 0, 255);
            if (req.QueryString["mode"] == "clear")
            {
                amount = 0;
            }

            List<Vector3> polygon;
            try
            {
                polygon = NetApi.Parse(ReadBody(req));
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad polygon: " + e.Message);
            }

            if (polygon.Count < 3)
            {
                return HttpBridge.Error("polygon needs at least 3 points");
            }

            return HttpBridge.OnSimulation(() =>
            {
                var cells = NaturalResourceManager.instance.m_naturalResources;
                int minX, minZ, maxX, maxZ;
                CellBounds(polygon, out minX, out minZ, out maxX, out maxZ);
                int changed = 0, skippedForest = 0;
                byte v = (byte)amount;
                for (int z = minZ; z <= maxZ; z++)
                {
                    for (int x = minX; x <= maxX; x++)
                    {
                        if (!Inside(polygon, CellCenter(x), CellCenter(z)))
                        {
                            continue;
                        }

                        var c = cells[z * Grid + x];
                        switch (type)
                        {
                            // 鉱石と石油、肥えた土地と砂は同じマスで食い合う(エディターの筆と同じ)
                            case "ore": c.m_ore = v; if (v > 0) { c.m_oil = 0; } break;
                            case "oil": c.m_oil = v; if (v > 0) { c.m_ore = 0; } break;
                            case "sand": c.m_sand = v; if (v > 0) { c.m_fertility = 0; } break;
                            case "fertility":
                                if (c.m_forest != 0 && v > 0)
                                {
                                    skippedForest++; // 森林のマスには肥えた土地を書けない(ゲームの決まり)
                                    continue;
                                }

                                c.m_fertility = v;
                                if (v > 0)
                                {
                                    c.m_sand = 0;
                                }

                                break;
                        }

                        cells[z * Grid + x] = c;
                        changed++;
                    }
                }

                NaturalResourceManager.instance.AreaModified(minX, minZ, maxX, maxZ);
                return "{\"ok\":true,\"type\":" + Json.Str(type) + ",\"amount\":" + amount
                    + ",\"changedCells\":" + changed + ",\"skippedForestCells\":" + skippedForest + "}";
            });
        }

        // ---- 森林(木を植える) ----

        // POST /editor/forest?density=1..5&prefab=..&dry_run=true  本文は多角形
        private static string PlantForest(HttpListenerRequest req)
        {
            int density;
            int.TryParse(req.QueryString["density"] ?? "3", NumberStyles.Integer, CultureInfo.InvariantCulture, out density);
            density = Mathf.Clamp(density, 1, 5);
            string prefab = req.QueryString["prefab"];
            bool dryRun = req.QueryString["dry_run"] == "true";

            List<Vector3> polygon;
            try
            {
                polygon = NetApi.Parse(ReadBody(req));
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad polygon: " + e.Message);
            }

            if (polygon.Count < 3)
            {
                return HttpBridge.Error("polygon needs at least 3 points");
            }

            return HttpBridge.OnSimulation(() =>
            {
                var infos = TreeInfos(prefab);
                if (infos.Count == 0)
                {
                    return HttpBridge.Error("tree prefab not found: " + prefab);
                }

                var tm = TreeManager.instance;
                var terrain = TerrainManager.instance;
                var rnd = new Randomizer(20261016);
                int minX, minZ, maxX, maxZ;
                CellBounds(polygon, out minX, out minZ, out maxX, out maxZ);

                // 先に植える場所を決める。上限を超えるなら植えない
                var spots = new List<Vector3>();
                for (int z = minZ; z <= maxZ; z++)
                {
                    for (int x = minX; x <= maxX; x++)
                    {
                        float cx = CellCenter(x), cz = CellCenter(z);
                        if (!Inside(polygon, cx, cz))
                        {
                            continue;
                        }

                        CellSpots(cx, cz, density, ref rnd, spots);
                    }
                }

                int room = TreeManager.MAX_MAP_TREES - tm.m_treeCount;
                string head = "{\"ok\":" + (dryRun || spots.Count <= room ? "true" : "false")
                    + ",\"candidates\":" + spots.Count + ",\"treesBefore\":" + tm.m_treeCount + ",\"room\":" + room;
                if (dryRun)
                {
                    return head + ",\"dryRun\":true}";
                }

                if (spots.Count > room)
                {
                    return head + ",\"error\":\"木の上限を超える。範囲を狭めるか density を下げる\"}";
                }

                int planted = 0;
                foreach (var p in spots)
                {
                    uint tree;
                    var info = infos[rnd.Int32((uint)infos.Count)];
                    if (tm.CreateTree(out tree, ref rnd, info, p, false))
                    {
                        planted++;
                    }
                }

                return head + ",\"planted\":" + planted + ",\"treesAfter\":" + tm.m_treeCount + "}";
            }, 120000);
        }

        // 天然資源の1マスの中に、density 本の木を植える場所を選ぶ。水・道路・建物の上は外す
        private static void CellSpots(float cx, float cz, int density, ref Randomizer rnd, List<Vector3> spots)
        {
            var terrain = TerrainManager.instance;
            for (int k = 0; k < density; k++)
            {
                float px = cx + (rnd.Int32(10000) / 10000f - 0.5f) * CellSize * 0.9f;
                float pz = cz + (rnd.Int32(10000) / 10000f - 0.5f) * CellSize * 0.9f;
                var xz = new Vector2(px, pz);
                if (terrain.HasWater(xz))
                {
                    continue;
                }

                var quad = new Quad2
                {
                    a = xz + new Vector2(-4.5f, -4.5f),
                    b = xz + new Vector2(-4.5f, 4.5f),
                    c = xz + new Vector2(4.5f, 4.5f),
                    d = xz + new Vector2(4.5f, -4.5f)
                };
                float py = terrain.SampleRawHeightSmooth(new Vector3(px, 0f, pz));
                var collision = ItemClass.CollisionType.Terrain;
                if (NetManager.instance.OverlapQuad(quad, py, py + 20f, collision, ItemClass.Layer.Default, 0, 0, 0)
                    || BuildingManager.instance.OverlapQuad(quad, py, py + 20f, collision, ItemClass.Layer.Default, 0, 0, 0))
                {
                    continue;
                }

                spots.Add(new Vector3(px, py, pz));
            }
        }

        // POST /editor/forest_cells?density=1..5&seed=..  本文は天然資源のマスの番号 "ix,iz;ix,iz;..."
        // 土地利用のデータから作った森林のマスに、まとめて木を植える(tools/forest_mask.py、plant_forest_cells.py)
        private static string PlantForestCells(HttpListenerRequest req)
        {
            int density, seed;
            int.TryParse(req.QueryString["density"] ?? "2", NumberStyles.Integer, CultureInfo.InvariantCulture, out density);
            density = Mathf.Clamp(density, 1, 5);
            int.TryParse(req.QueryString["seed"] ?? "1", NumberStyles.Integer, CultureInfo.InvariantCulture, out seed);
            var idx = new List<int>();
            try
            {
                foreach (var part in ReadBody(req).Split(new[] { ';' }, StringSplitOptions.RemoveEmptyEntries))
                {
                    var v = part.Split(',');
                    idx.Add(int.Parse(v[0], CultureInfo.InvariantCulture));
                    idx.Add(int.Parse(v[1], CultureInfo.InvariantCulture));
                }
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad cells (ix,iz;...): " + e.Message);
            }

            return HttpBridge.OnSimulation(() =>
            {
                var infos = TreeInfos(req.QueryString["prefab"]);
                if (infos.Count == 0)
                {
                    return HttpBridge.Error("no tree prefab");
                }

                var tm = TreeManager.instance;
                var rnd = new Randomizer(seed);
                var spots = new List<Vector3>();
                for (int i = 0; i + 1 < idx.Count; i += 2)
                {
                    CellSpots(CellCenter(idx[i]), CellCenter(idx[i + 1]), density, ref rnd, spots);
                }

                int room = TreeManager.MAX_MAP_TREES - tm.m_treeCount;
                if (spots.Count > room)
                {
                    return "{\"ok\":false,\"error\":\"木の上限を超える\",\"candidates\":" + spots.Count + ",\"room\":" + room + "}";
                }

                int planted = 0;
                foreach (var p in spots)
                {
                    uint tree;
                    if (tm.CreateTree(out tree, ref rnd, infos[rnd.Int32((uint)infos.Count)], p, false))
                    {
                        planted++;
                    }
                }

                return "{\"ok\":true,\"cells\":" + idx.Count / 2 + ",\"planted\":" + planted + ",\"trees\":" + tm.m_treeCount + "}";
            }, 120000);
        }

        // 木の種類。名前を指定しなければ、読み込まれている木から選ぶ
        private static List<TreeInfo> TreeInfos(string prefab)
        {
            var list = new List<TreeInfo>();
            if (!string.IsNullOrEmpty(prefab))
            {
                var one = PrefabCollection<TreeInfo>.FindLoaded(prefab);
                if (one != null)
                {
                    list.Add(one);
                }

                return list;
            }

            uint n = (uint)PrefabCollection<TreeInfo>.LoadedCount();
            for (uint i = 0; i < n; i++)
            {
                var t = PrefabCollection<TreeInfo>.GetLoaded(i);
                if (t != null)
                {
                    list.Add(t);
                }
            }

            return list;
        }

        // ---- 天然資源の画像 ----

        // GET /editor/resource_map?type=ore|oil|fertility|forest|sand&save_to=/abs/path.png  北が上。陸は灰色、水は紺
        private static string ResourceMap(HttpListenerRequest req)
        {
            string type = req.QueryString["type"] ?? "forest";
            string saveTo = req.QueryString["save_to"];
            if (string.IsNullOrEmpty(saveTo))
            {
                return HttpBridge.Error("save_to is required");
            }

            var cells = NaturalResourceManager.instance.m_naturalResources;
            var terrain = TerrainManager.instance;
            var color = type == "ore" ? new Color(0.85f, 0.45f, 0.2f) : type == "oil" ? new Color(0.1f, 0.1f, 0.1f)
                : type == "fertility" ? new Color(0.95f, 0.85f, 0.2f) : type == "sand" ? new Color(0.9f, 0.8f, 0.6f)
                : new Color(0.2f, 0.75f, 0.25f);
            var tex = new Texture2D(Grid, Grid, TextureFormat.RGB24, false);
            int nonZero = 0;
            for (int z = 0; z < Grid; z++)
            {
                for (int x = 0; x < Grid; x++)
                {
                    var c = cells[z * Grid + x];
                    int v = type == "ore" ? c.m_ore : type == "oil" ? c.m_oil : type == "fertility" ? c.m_fertility
                        : type == "sand" ? c.m_sand : c.m_forest;
                    var p = new Vector3(CellCenter(x), 0f, CellCenter(z));
                    bool water = terrain.SampleRawHeightSmoothWithWater(p, false, 0f) - terrain.SampleRawHeightSmooth(p) > 0.5f;
                    var bg = water ? new Color(0.1f, 0.15f, 0.35f) : new Color(0.35f, 0.35f, 0.35f);
                    if (v > 0)
                    {
                        nonZero++;
                    }

                    // 行 z=0 が南。Texture2D の y=0 は画像の下なので、そのまま書けば北が上になる
                    tex.SetPixel(x, z, Color.Lerp(bg, color, v / 255f));
                }
            }

            tex.Apply();
            Directory.CreateDirectory(Path.GetDirectoryName(saveTo));
            File.WriteAllBytes(saveTo, tex.EncodeToPNG());
            UnityEngine.Object.Destroy(tex);
            return "{\"ok\":true,\"type\":" + Json.Str(type) + ",\"nonZeroCells\":" + nonZero + ",\"path\":" + Json.Str(saveTo) + "}";
        }

        // ---- 水源 ----

        // GET /editor/water_source?x=..&z=..&rate=1..65535&target=水面の高さ(m)
        // 水源は、水面が target より低いマスにだけ水を足す。画面の道具の最小(0.01)は rate 655 に当たる
        private static string AddWaterSource(HttpListenerRequest req)
        {
            float x, z, target;
            int rate;
            var q = req.QueryString;
            if (!float.TryParse(q["x"] ?? "", NumberStyles.Float, CultureInfo.InvariantCulture, out x)
                || !float.TryParse(q["z"] ?? "", NumberStyles.Float, CultureInfo.InvariantCulture, out z)
                || !float.TryParse(q["target"] ?? "", NumberStyles.Float, CultureInfo.InvariantCulture, out target)
                || !int.TryParse(q["rate"] ?? "", NumberStyles.Integer, CultureInfo.InvariantCulture, out rate))
            {
                return HttpBridge.Error("x, z, rate, target are required");
            }

            rate = Mathf.Clamp(rate, 1, 65535);
            return HttpBridge.OnSimulation(() =>
            {
                var pos = new Vector3(x, 0f, z);
                pos.y = TerrainManager.instance.SampleRawHeightSmooth(pos);
                if (target <= pos.y)
                {
                    return HttpBridge.Error("target(" + target.ToString("0.0", CultureInfo.InvariantCulture)
                        + ") が地面(" + pos.y.ToString("0.0", CultureInfo.InvariantCulture) + ")より低い");
                }

                var src = new WaterSource
                {
                    m_type = WaterSource.TYPE_NATURAL,
                    m_inputPosition = pos,
                    m_outputPosition = pos,
                    m_inputRate = (uint)rate,
                    m_outputRate = (uint)rate,
                    m_target = (ushort)Mathf.Clamp(Mathf.RoundToInt(target * 64f), 0, 65535)
                };
                ushort id;
                if (!TerrainManager.instance.WaterSimulation.CreateWaterSource(out id, src))
                {
                    return HttpBridge.Error("CreateWaterSource failed");
                }

                return "{\"ok\":true,\"id\":" + id + ",\"x\":" + N(x) + ",\"z\":" + N(z) + ",\"ground\":" + N(pos.y)
                    + ",\"target\":" + N(target) + ",\"rate\":" + rate + "}";
            });
        }

        private static string ListWaterSources()
        {
            var ws = TerrainManager.instance.WaterSimulation.m_waterSources;
            var sb = new StringBuilder("{\"ok\":true,\"sources\":[");
            bool first = true;
            for (int i = 0; i < ws.m_size; i++)
            {
                var s = ws.m_buffer[i];
                if (s.m_type == 0)
                {
                    continue;
                }

                sb.Append(first ? "" : ",").Append("{\"id\":").Append(i + 1)
                  .Append(",\"type\":").Append(s.m_type)
                  .Append(",\"x\":").Append(N(s.m_inputPosition.x)).Append(",\"z\":").Append(N(s.m_inputPosition.z))
                  .Append(",\"ground\":").Append(N(s.m_inputPosition.y))
                  .Append(",\"target\":").Append(N(s.m_target / 64f))
                  .Append(",\"rate\":").Append(s.m_inputRate)
                  .Append(",\"water\":").Append(s.m_water).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // GET /editor/water_source/remove?id=..
        private static string RemoveWaterSource(HttpListenerRequest req)
        {
            int id;
            if (!int.TryParse(req.QueryString["id"] ?? "", NumberStyles.Integer, CultureInfo.InvariantCulture, out id) || id < 1)
            {
                return HttpBridge.Error("id is required");
            }

            return HttpBridge.OnSimulation(() =>
            {
                var ws = TerrainManager.instance.WaterSimulation;
                if (id > ws.m_waterSources.m_size || ws.m_waterSources.m_buffer[id - 1].m_type == 0)
                {
                    return HttpBridge.Error("no water source " + id);
                }

                ws.ReleaseWaterSource((ushort)id);
                return "{\"ok\":true,\"removed\":" + id + "}";
            });
        }

        // ---- 地形(川を掘る) ----

        private const int RawN = 1081;       // 地形の点の数(1辺)
        private const float RawCell = 16f;   // 点の間隔(m)
        private static ushort[] terrainBackup; // 最初に掘る前の地形。restore で戻す

        // POST /editor/carve?width=..&bank=..  本文は "x,z,川底の高さ;x,z,川底の高さ;..."
        // 線から width/2 以内を川底の高さにし、その外 bank の幅で元の地形へなだらかにつなぐ。下げるだけで、盛り上げない
        private static string Carve(HttpListenerRequest req)
        {
            float width, bank;
            if (!float.TryParse(req.QueryString["width"] ?? "64", NumberStyles.Float, CultureInfo.InvariantCulture, out width))
            {
                width = 64f;
            }

            if (!float.TryParse(req.QueryString["bank"] ?? "32", NumberStyles.Float, CultureInfo.InvariantCulture, out bank))
            {
                bank = 32f;
            }

            var line = new List<Vector3>(); // x, 川底の高さ(y), z
            try
            {
                foreach (var part in ReadBody(req).Split(new[] { ';' }, StringSplitOptions.RemoveEmptyEntries))
                {
                    var v = part.Split(',');
                    line.Add(new Vector3(float.Parse(v[0], CultureInfo.InvariantCulture), float.Parse(v[2], CultureInfo.InvariantCulture),
                        float.Parse(v[1], CultureInfo.InvariantCulture)));
                }
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad line (x,z,bed;...): " + e.Message);
            }

            if (line.Count < 2)
            {
                return HttpBridge.Error("need at least 2 points");
            }

            return HttpBridge.OnSimulation(() =>
            {
                var tm = TerrainManager.instance;
                var raw = tm.RawHeights;
                if (terrainBackup == null)
                {
                    terrainBackup = (ushort[])raw.Clone();
                }

                float reach = width * 0.5f + bank;
                float x0 = float.MaxValue, z0 = float.MaxValue, x1 = float.MinValue, z1 = float.MinValue;
                foreach (var p in line)
                {
                    x0 = Mathf.Min(x0, p.x - reach);
                    z0 = Mathf.Min(z0, p.z - reach);
                    x1 = Mathf.Max(x1, p.x + reach);
                    z1 = Mathf.Max(z1, p.z + reach);
                }

                int ix0 = Mathf.Clamp((int)(x0 / RawCell + 540f), 0, RawN - 1), iz0 = Mathf.Clamp((int)(z0 / RawCell + 540f), 0, RawN - 1);
                int ix1 = Mathf.Clamp((int)(x1 / RawCell + 540f) + 1, 0, RawN - 1), iz1 = Mathf.Clamp((int)(z1 / RawCell + 540f) + 1, 0, RawN - 1);
                int changed = 0;
                float deepest = float.MaxValue;
                for (int iz = iz0; iz <= iz1; iz++)
                {
                    for (int ix = ix0; ix <= ix1; ix++)
                    {
                        float px = (ix - 540f) * RawCell, pz = (iz - 540f) * RawCell;
                        float d, bed;
                        Nearest(line, px, pz, out d, out bed);
                        if (d > reach)
                        {
                            continue;
                        }

                        int idx = iz * RawN + ix;
                        float orig = raw[idx] / 64f;
                        float target = d <= width * 0.5f ? bed : bed + (d - width * 0.5f) / Mathf.Max(bank, 1f) * (orig - bed);
                        if (target < orig)
                        {
                            raw[idx] = (ushort)Mathf.Clamp(Mathf.RoundToInt(target * 64f), 0, 65535);
                            changed++;
                            deepest = Mathf.Min(deepest, target);
                        }
                    }
                }

                UpdateTerrain(ix0, iz0, ix1, iz1);
                return "{\"ok\":true,\"changedPoints\":" + changed + ",\"lowestBed\":" + N(deepest == float.MaxValue ? 0f : deepest)
                    + ",\"area\":[" + ix0 + "," + iz0 + "," + ix1 + "," + iz1 + "]}";
            }, 60000);
        }

        // 線上でいちばん近い点までの距離と、そこの川底の高さ(点の間で直線に補う)
        private static void Nearest(List<Vector3> line, float x, float z, out float dist, out float bed)
        {
            dist = float.MaxValue;
            bed = line[0].y;
            for (int i = 1; i < line.Count; i++)
            {
                var a = line[i - 1];
                var b = line[i];
                float dx = b.x - a.x, dz = b.z - a.z;
                float len2 = dx * dx + dz * dz;
                float t = len2 > 0f ? Mathf.Clamp01(((x - a.x) * dx + (z - a.z) * dz) / len2) : 0f;
                float cx = a.x + t * dx, cz = a.z + t * dz;
                float d = Mathf.Sqrt((x - cx) * (x - cx) + (z - cz) * (z - cz));
                if (d < dist)
                {
                    dist = d;
                    bed = a.y + t * (b.y - a.y);
                }
            }
        }

        // 最初に掘る前の地形に戻す
        private static string RestoreTerrain()
        {
            if (terrainBackup == null)
            {
                return "{\"ok\":true,\"restored\":false}";
            }

            var raw = TerrainManager.instance.RawHeights;
            Array.Copy(terrainBackup, raw, raw.Length);
            terrainBackup = null;
            UpdateTerrain(0, 0, RawN - 1, RawN - 1);
            return "{\"ok\":true,\"restored\":true}";
        }

        // 地形の更新をゲームに知らせる。ゲームは一度に約128点四方しか反映しないので、100点四方ずつに分ける(#73 の検証で判明)
        private static void UpdateTerrain(int x0, int z0, int x1, int z1)
        {
            for (int z = z0; z <= z1; z += 100)
            {
                for (int x = x0; x <= x1; x += 100)
                {
                    TerrainModify.UpdateArea(x, z, Mathf.Min(x + 100, x1), Mathf.Min(z + 100, z1), true, false, false);
                }
            }
        }

        // POST /editor/water_profile  本文は "x,z;x,z;..."。各点の地面と水面の高さ、水深を返す
        private static string WaterProfile(HttpListenerRequest req)
        {
            List<Vector3> pts;
            try
            {
                pts = NetApi.Parse(ReadBody(req));
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad points: " + e.Message);
            }

            return HttpBridge.OnMain(() =>
            {
                var t = TerrainManager.instance;
                var sb = new StringBuilder("{\"ok\":true,\"points\":[");
                for (int i = 0; i < pts.Count; i++)
                {
                    var p = pts[i];
                    float g = t.SampleRawHeightSmooth(p);
                    float w = t.SampleRawHeightSmoothWithWater(p, false, 0f);
                    sb.Append(i > 0 ? "," : "").Append('[').Append(N(p.x)).Append(',').Append(N(p.z)).Append(',')
                      .Append(N(g)).Append(',').Append(N(w)).Append(',').Append(N(w - g)).Append(']');
                }

                return sb.Append("],\"columns\":[\"x\",\"z\",\"ground\",\"water\",\"depth\"]}").ToString();
            });
        }

        // ---- 既存の線を橋に作り替える ----

        // GET /editor/rebridge?x=..&z=..&radius=150&prefab=Highway
        // 中心から radius 以内にかかる区間を、その種類の橋(例: Highway Bridge)に作り替える。
        // 道路はその下の地形を平らにするので、川を掘っても道路の下だけ埋まり、水がせき止められる。橋は地形を平らにしない(#73)
        // 作り替えた後、その場所をもう一度 carve_channel で掘ると、溝がつながる
        private static string Rebridge(HttpListenerRequest req)
        {
            float x = 0f, z = 0f, radius;
            var q = req.QueryString;
            // 本文に川の線("x,z;x,z;...")を渡すと、その線と交わる区間をすべて作り替える
            List<Vector3> river = null;
            string body = req.HttpMethod == "POST" ? ReadBody(req) : "";
            if (!string.IsNullOrEmpty(body))
            {
                try
                {
                    river = NetApi.Parse(body);
                }
                catch (Exception e)
                {
                    return HttpBridge.Error("bad line: " + e.Message);
                }
            }
            else if (!float.TryParse(q["x"] ?? "", NumberStyles.Float, CultureInfo.InvariantCulture, out x)
                || !float.TryParse(q["z"] ?? "", NumberStyles.Float, CultureInfo.InvariantCulture, out z))
            {
                return HttpBridge.Error("x, z (または本文に川の線) が要る");
            }

            if (!float.TryParse(q["radius"] ?? "150", NumberStyles.Float, CultureInfo.InvariantCulture, out radius))
            {
                radius = 150f;
            }

            string only = q["prefab"];
            return HttpBridge.OnSimulation(() =>
            {
                var nm = NetManager.instance;
                var sim = SimulationManager.instance;
                var rnd = sim.m_randomizer;
                var center = new Vector2(x, z);
                var targets = new List<ushort>();
                for (int i = 1; i < nm.m_segments.m_size; i++)
                {
                    var seg = nm.m_segments.m_buffer[i];
                    if ((seg.m_flags & NetSegment.Flags.Created) == 0 || seg.Info == null)
                    {
                        continue;
                    }

                    if (!string.IsNullOrEmpty(only) && seg.Info.name != only)
                    {
                        continue;
                    }

                    var a = VectorUtils.XZ(nm.m_nodes.m_buffer[seg.m_startNode].m_position);
                    var b = VectorUtils.XZ(nm.m_nodes.m_buffer[seg.m_endNode].m_position);
                    bool hit;
                    if (river != null)
                    {
                        hit = false;
                        for (int k = 1; k < river.Count && !hit; k++)
                        {
                            hit = Crosses(a, b, VectorUtils.XZ(river[k - 1]), VectorUtils.XZ(river[k]));
                        }
                    }
                    else
                    {
                        float t = Mathf.Clamp01(Vector2.Dot(center - a, b - a) / Mathf.Max((b - a).sqrMagnitude, 1f));
                        hit = Vector2.Distance(center, a + (b - a) * t) <= radius;
                    }

                    if (hit)
                    {
                        targets.Add((ushort)i);
                    }
                }

                var sb = new StringBuilder();
                int done = 0;
                foreach (ushort id in targets)
                {
                    var seg = nm.m_segments.m_buffer[id];
                    var info = seg.Info;
                    var field = info.m_netAI.GetType().GetField("m_bridgeInfo");
                    var bridge = field != null ? field.GetValue(info.m_netAI) as NetInfo : null;
                    if (bridge == null || bridge == info)
                    {
                        continue;
                    }

                    ushort start = seg.m_startNode, end = seg.m_endNode;
                    var sd = seg.m_startDirection;
                    var ed = seg.m_endDirection;
                    bool invert = (seg.m_flags & NetSegment.Flags.Invert) != 0;
                    nm.ReleaseSegment(id, true);
                    ushort created;
                    if (nm.CreateSegment(out created, ref rnd, bridge, start, end, sd, ed, sim.m_currentBuildIndex, sim.m_currentBuildIndex, invert))
                    {
                        sim.m_currentBuildIndex++;
                        sb.Append(done > 0 ? "," : "").Append(Json.Str(info.name + " -> " + bridge.name));
                        done++;
                    }
                }

                return "{\"ok\":true,\"candidates\":" + targets.Count + ",\"rebuilt\":" + done + ",\"changes\":[" + sb + "]}";
            });
        }

        // 2本の線分が交わるか
        private static bool Crosses(Vector2 p1, Vector2 p2, Vector2 q1, Vector2 q2)
        {
            float d1 = Cross(q2 - q1, p1 - q1), d2 = Cross(q2 - q1, p2 - q1);
            float d3 = Cross(p2 - p1, q1 - p1), d4 = Cross(p2 - p1, q2 - p1);
            return d1 * d2 < 0f && d3 * d4 < 0f;
        }

        private static float Cross(Vector2 a, Vector2 b)
        {
            return a.x * b.y - a.y * b.x;
        }

        // ---- 共通 ----

        private static string ReadBody(HttpListenerRequest req)
        {
            using (var r = new StreamReader(req.InputStream, Encoding.UTF8))
            {
                return r.ReadToEnd();
            }
        }

        private static float CellCenter(int i)
        {
            return (i - Grid * 0.5f + 0.5f) * CellSize;
        }

        private static void CellBounds(List<Vector3> polygon, out int minX, out int minZ, out int maxX, out int maxZ)
        {
            float x0 = float.MaxValue, z0 = float.MaxValue, x1 = float.MinValue, z1 = float.MinValue;
            foreach (var p in polygon)
            {
                x0 = Mathf.Min(x0, p.x);
                z0 = Mathf.Min(z0, p.z);
                x1 = Mathf.Max(x1, p.x);
                z1 = Mathf.Max(z1, p.z);
            }

            minX = Mathf.Clamp((int)(x0 / CellSize + Grid * 0.5f), 0, Grid - 1);
            minZ = Mathf.Clamp((int)(z0 / CellSize + Grid * 0.5f), 0, Grid - 1);
            maxX = Mathf.Clamp((int)(x1 / CellSize + Grid * 0.5f), 0, Grid - 1);
            maxZ = Mathf.Clamp((int)(z1 / CellSize + Grid * 0.5f), 0, Grid - 1);
        }

        // 点が多角形の中か(偶奇規則)
        private static bool Inside(List<Vector3> poly, float x, float z)
        {
            bool inside = false;
            for (int i = 0, j = poly.Count - 1; i < poly.Count; j = i++)
            {
                if ((poly[i].z > z) != (poly[j].z > z)
                    && x < (poly[j].x - poly[i].x) * (z - poly[i].z) / (poly[j].z - poly[i].z) + poly[i].x)
                {
                    inside = !inside;
                }
            }

            return inside;
        }

        private static string N(float v)
        {
            return v.ToString("0.##", CultureInfo.InvariantCulture);
        }
    }
}
