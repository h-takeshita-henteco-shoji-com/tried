using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using ColossalFramework.Math;
using UnityEngine;

namespace AIMayor
{
    // ゲームの中で木を植える・取り除く(#82)。ゲームの景観の画面の木の道具(TreeTool)と同じ結果・同じ費用にする。
    // - 植える: 1本ごとに建設費を払う(TreeInfo.GetConstructionCost。ゲームの1本植えと同じ)。
    //   置けるかはゲームの判定(TreeTool.CheckPlacementErrors)で決める。建物・道路・ほかの木・水の上・区画の外には植えない
    // - 取り除く: ゲームのブルドーザーと同じく ReleaseTree。払い戻しはない(BulldozeTool.DeleteTreeImpl)。燃えている木は飛ばす
    // 木は騒音を減らし(ImmaterialResourceManager で騒音 × (100 − 木の近さ%))、地価を上げる(騒音の減りと、魅力の加点)
    public static class TreeApi
    {
        private const int MaxTrees = 3000;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/trees/prefabs"] = req => HttpBridge.OnMain(Prefabs);
            routes["/trees/plant"] = Plant;
            routes["/trees/remove"] = Remove;
        }

        // ゲームの木の一覧と同じく、手で置けてゲームで使える木
        private static bool Placeable(TreeInfo t)
        {
            return t != null && t.m_placementStyle == ItemClass.Placement.Manual
                && (t.m_availableIn & ItemClass.Availability.Game) != 0;
        }

        // 木の道具は景観(Landscaping)の機能として解禁される(GameMainToolbar)
        private static bool Unlocked()
        {
            return ToolsModifierControl.IsUnlocked(UnlockManager.Feature.Landscaping);
        }

        // /trees/prefabs  植えられる木の種類と、1本の費用
        private static string Prefabs()
        {
            var sb = new StringBuilder("{\"ok\":true,\"unlocked\":").Append(Unlocked() ? "true" : "false").Append(",\"prefabs\":[");
            bool first = true;
            int n = PrefabCollection<TreeInfo>.LoadedCount();
            for (uint i = 0; i < n; i++)
            {
                var t = PrefabCollection<TreeInfo>.GetLoaded(i);
                if (!Placeable(t))
                {
                    continue;
                }

                sb.Append(first ? "" : ",").Append("{\"name\":").Append(Json.Str(t.name))
                  .Append(",\"cost\":").Append((t.GetConstructionCost() / 100f).ToString("0.##", CultureInfo.InvariantCulture)).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // POST /trees/plant?prefab=..&spacing=12&pay=true  本文 "x1,z1;x2,z2;..."(多角形)
        // 多角形の中に spacing(m)おきに、少しずらして植える。1回に3,000本まで
        private static string Plant(HttpListenerRequest req)
        {
            List<Vector3> poly;
            string err = ReadPolygon(req, out poly);
            if (err != null)
            {
                return HttpBridge.Error(err);
            }

            string prefab = req.QueryString["prefab"];
            float spacing = Mathf.Clamp(F(req, "spacing", 12f), 4f, 100f);
            bool pay = req.QueryString["pay"] != "false";
            return HttpBridge.OnSimulation(() => PlantOnSimulation(poly, prefab, spacing, pay), 30000);
        }

        private static string PlantOnSimulation(List<Vector3> poly, string prefab, float spacing, bool pay)
        {
            if (!Unlocked())
            {
                return HttpBridge.Error("trees are not unlocked yet (Landscaping)");
            }

            TreeInfo info = null;
            if (!string.IsNullOrEmpty(prefab))
            {
                info = PrefabCollection<TreeInfo>.FindLoaded(prefab);
                if (!Placeable(info))
                {
                    return HttpBridge.Error("tree prefab not found or not placeable: " + prefab + " (see /trees/prefabs)");
                }
            }
            else
            {
                int n = PrefabCollection<TreeInfo>.LoadedCount();
                for (uint i = 0; i < n && info == null; i++)
                {
                    var t = PrefabCollection<TreeInfo>.GetLoaded(i);
                    if (Placeable(t))
                    {
                        info = t;
                    }
                }

                if (info == null)
                {
                    return HttpBridge.Error("no placeable tree");
                }
            }

            float minX, minZ, maxX, maxZ;
            Bounds(poly, out minX, out minZ, out maxX, out maxZ);
            var sim = SimulationManager.instance;
            var eco = EconomyManager.instance;
            var tm = TreeManager.instance;
            var terrain = TerrainManager.instance;
            Randomizer rnd = sim.m_randomizer;
            int planted = 0, blocked = 0;
            long paid = 0;
            bool noMoney = false;
            for (float z = minZ + spacing * 0.5f; z <= maxZ && planted < MaxTrees && !noMoney; z += spacing)
            {
                for (float x = minX + spacing * 0.5f; x <= maxX && planted < MaxTrees; x += spacing)
                {
                    // 並びが格子に見えないよう、間隔の3割までずらす
                    var p = new Vector3(x + (rnd.Int32(10000u) / 10000f - 0.5f) * spacing * 0.6f, 0f,
                        z + (rnd.Int32(10000u) / 10000f - 0.5f) * spacing * 0.6f);
                    if (!Inside(poly, p.x, p.z))
                    {
                        continue;
                    }

                    p.y = terrain.SampleDetailHeight(p);
                    TreeInfo variation = info.GetVariation(ref rnd);
                    uint nextId = tm.m_trees.NextFreeItem(ref rnd);
                    if (TreeTool.CheckPlacementErrors(variation, p, false, nextId, null, null) != ToolBase.ToolErrors.None)
                    {
                        blocked++;
                        continue;
                    }

                    int cost = variation.GetConstructionCost();
                    if (pay && cost != 0)
                    {
                        if (eco.PeekResource(EconomyManager.Resource.Construction, cost) != cost)
                        {
                            noMoney = true;
                            break;
                        }
                    }

                    uint tree;
                    if (!tm.CreateTree(out tree, ref rnd, variation, p, true))
                    {
                        blocked++;
                        continue;
                    }

                    if (pay && cost != 0)
                    {
                        eco.FetchResource(EconomyManager.Resource.Construction, cost, variation.m_class);
                        paid += cost;
                    }

                    planted++;
                }
            }

            return "{\"ok\":true,\"prefab\":" + Json.Str(info.name) + ",\"planted\":" + planted + ",\"blocked\":" + blocked
                + ",\"cost\":" + (paid / 100) + ",\"paid\":" + (pay ? "true" : "false")
                + ",\"stoppedForMoney\":" + (noMoney ? "true" : "false")
                + ",\"limitReached\":" + (planted >= MaxTrees ? "true" : "false") + "}";
        }

        // POST /trees/remove  本文 多角形。中の木を取り除く(払い戻しなし。燃えている木は飛ばす)
        private static string Remove(HttpListenerRequest req)
        {
            List<Vector3> poly;
            string err = ReadPolygon(req, out poly);
            if (err != null)
            {
                return HttpBridge.Error(err);
            }

            return HttpBridge.OnSimulation(() =>
            {
                var tm = TreeManager.instance;
                var trees = tm.m_trees.m_buffer;
                var grid = tm.m_treeGrid;
                int res = Mathf.RoundToInt(Mathf.Sqrt(grid.Length));
                float cell = TreeManager.TREEGRID_CELL_SIZE;
                float minX, minZ, maxX, maxZ;
                Bounds(poly, out minX, out minZ, out maxX, out maxZ);
                int x0 = Mathf.Clamp((int)(minX / cell + res * 0.5f), 0, res - 1);
                int x1 = Mathf.Clamp((int)(maxX / cell + res * 0.5f), 0, res - 1);
                int z0 = Mathf.Clamp((int)(minZ / cell + res * 0.5f), 0, res - 1);
                int z1 = Mathf.Clamp((int)(maxZ / cell + res * 0.5f), 0, res - 1);
                int removed = 0, burning = 0;
                for (int gz = z0; gz <= z1; gz++)
                {
                    for (int gx = x0; gx <= x1; gx++)
                    {
                        uint t = grid[gz * res + gx];
                        int guard = 0;
                        while (t != 0 && guard++ < 262144)
                        {
                            uint next = trees[t].m_nextGridTree;
                            var pos = trees[t].Position;
                            if (trees[t].m_flags != 0 && Inside(poly, pos.x, pos.z))
                            {
                                if ((trees[t].m_flags & (ushort)TreeInstance.Flags.Burning) != 0)
                                {
                                    burning++;
                                }
                                else
                                {
                                    tm.ReleaseTree(t);
                                    removed++;
                                }
                            }

                            t = next;
                        }
                    }
                }

                return "{\"ok\":true,\"removed\":" + removed + ",\"skippedBurning\":" + burning + ",\"refund\":0}";
            }, 30000);
        }

        internal static string ReadPolygon(HttpListenerRequest req, out List<Vector3> poly)
        {
            poly = null;
            string body;
            using (var r = new StreamReader(req.InputStream, Encoding.UTF8))
            {
                body = r.ReadToEnd();
            }

            try
            {
                poly = NetApi.Parse(body);
            }
            catch (Exception e)
            {
                return "bad points: " + e.Message;
            }

            return poly.Count < 3 ? "need a polygon with at least 3 points" : null;
        }

        internal static void Bounds(List<Vector3> poly, out float minX, out float minZ, out float maxX, out float maxZ)
        {
            minX = minZ = float.MaxValue;
            maxX = maxZ = float.MinValue;
            foreach (var p in poly)
            {
                minX = Mathf.Min(minX, p.x);
                maxX = Mathf.Max(maxX, p.x);
                minZ = Mathf.Min(minZ, p.z);
                maxZ = Mathf.Max(maxZ, p.z);
            }
        }

        // 点が多角形の中か(偶奇の規則)
        internal static bool Inside(List<Vector3> poly, float x, float z)
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

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }
    }
}
