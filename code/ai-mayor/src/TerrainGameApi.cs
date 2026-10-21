using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using ColossalFramework.Math;
using UnityEngine;

namespace AIMayor
{
    // ゲームの中で地形を変える(#82)。ゲーム本編の景観の道具(TerrainTool。DLCは要らず、UnlockManager.Feature.Landscaping で解禁)と
    // 同じ決まりにする。マップエディターの道具(EditorApi)とは別。
    // - 高さの格子は16mおき(1081×1081)。高さの値は1/64m単位
    // - 費用: ゲームと同じく、元の地形(BackupHeights)からの差が広がった分に土の値段(m_dirtPrice)を掛けて払う。差が縮めば払い戻し
    // - 土: 盛るには土の蓄え(DirtBuffer)が要り、削ると蓄えに入る(上限 1,048,576)。足りなければ断る(ゲームは足りる分だけ動かす)
    // - 建物・道路の下と、持っていない区画は変えない(ゲームは建物・道路の下も変えるが、AI市長の操作では壊さないよう外す)
    public static class TerrainGameApi
    {
        private const int Res = 1080;
        private const float Cell = 16f;
        private const int DirtMax = 1048576;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/terrain/level"] = req => Modify(req, "level");
            routes["/terrain/raise"] = req => Modify(req, "raise");
            routes["/terrain/lower"] = req => Modify(req, "lower");
            routes["/terrain/dirt"] = req => HttpBridge.OnMain(Dirt);
        }

        // /terrain/dirt  土の蓄えと、1m³あたりの値段(ゲームの景観の画面と同じ計算)
        private static string Dirt()
        {
            var tm = TerrainManager.instance;
            int price = tm.m_properties != null ? tm.m_properties.m_dirtPrice : 0;
            float perCubic = price * 65536f / 262144f * 512f / 100f / 100f;
            return "{\"ok\":true,\"unlocked\":" + (ToolsModifierControl.IsUnlocked(UnlockManager.Feature.Landscaping) ? "true" : "false")
                + ",\"dirtBuffer\":" + tm.DirtBuffer + ",\"dirtMax\":" + DirtMax
                + ",\"dirtBufferM3\":" + Mathf.RoundToInt(tm.DirtBuffer / 64f * Cell * Cell)
                + ",\"pricePerM3\":" + perCubic.ToString("0.###", CultureInfo.InvariantCulture) + "}";
        }

        // POST /terrain/level?height=..  /terrain/raise?amount=..  /terrain/lower?amount=..  本文 多角形 "x1,z1;..."
        private static string Modify(HttpListenerRequest req, string mode)
        {
            List<Vector3> poly;
            string err = TreeApi.ReadPolygon(req, out poly);
            if (err != null)
            {
                return HttpBridge.Error(err);
            }

            float value;
            string key = mode == "level" ? "height" : "amount";
            if (!float.TryParse(req.QueryString[key] ?? "", NumberStyles.Float, CultureInfo.InvariantCulture, out value))
            {
                return HttpBridge.Error(key + " is required");
            }

            bool pay = req.QueryString["pay"] != "false";
            return HttpBridge.OnSimulation(() => ModifyOnSimulation(poly, mode, value, pay), 30000);
        }

        private static string ModifyOnSimulation(List<Vector3> poly, string mode, float value, bool pay)
        {
            if (!ToolsModifierControl.IsUnlocked(UnlockManager.Feature.Landscaping))
            {
                return HttpBridge.Error("landscaping is not unlocked yet");
            }

            var tm = TerrainManager.instance;
            var raw = tm.RawHeights;
            var backup = tm.BackupHeights;
            var area = GameAreaManager.instance;
            int price = tm.m_properties != null ? tm.m_properties.m_dirtPrice : 0;
            float minX, minZ, maxX, maxZ;
            TreeApi.Bounds(poly, out minX, out minZ, out maxX, out maxZ);
            int x0 = Mathf.Clamp(Mathf.FloorToInt(minX / Cell + Res * 0.5f), 0, Res);
            int x1 = Mathf.Clamp(Mathf.CeilToInt(maxX / Cell + Res * 0.5f), 0, Res);
            int z0 = Mathf.Clamp(Mathf.FloorToInt(minZ / Cell + Res * 0.5f), 0, Res);
            int z1 = Mathf.Clamp(Mathf.CeilToInt(maxZ / Cell + Res * 0.5f), 0, Res);

            // 先に変える点と新しい高さを決め、土と費用を数える。足りなければ何も変えずに断る
            var changes = new List<KeyValuePair<int, ushort>>();
            long up = 0, down = 0, cost = 0;
            int skippedObjects = 0, skippedArea = 0;
            for (int i = z0; i <= z1; i++)
            {
                float z = (i - Res * 0.5f) * Cell;
                for (int j = x0; j <= x1; j++)
                {
                    float x = (j - Res * 0.5f) * Cell;
                    if (!TreeApi.Inside(poly, x, z))
                    {
                        continue;
                    }

                    var p = new Vector3(x, 0f, z);
                    if (area.PointOutOfArea(p, Cell * 0.5f))
                    {
                        skippedArea++;
                        continue;
                    }

                    int idx = i * (Res + 1) + j;
                    int old = raw[idx];
                    float h = old / 64f;
                    if (UnderObject(x, z, h))
                    {
                        skippedObjects++;
                        continue;
                    }

                    float target = mode == "level" ? value : mode == "raise" ? h + value : h - value;
                    int nv = Mathf.Clamp(Mathf.RoundToInt(target * 64f), 0, 65535);
                    if (nv == old)
                    {
                        continue;
                    }

                    if (nv > old)
                    {
                        up += nv - old;
                    }
                    else
                    {
                        down += old - nv;
                    }

                    int b = backup[idx];
                    cost += (long)(Mathf.Abs(nv - b) - Mathf.Abs(old - b)) * price;
                    changes.Add(new KeyValuePair<int, ushort>(idx, (ushort)nv));
                }
            }

            if (changes.Count == 0)
            {
                return "{\"ok\":true,\"changedPoints\":0,\"skippedUnderObjects\":" + skippedObjects + ",\"skippedOutOfArea\":" + skippedArea + "}";
            }

            long dirt = tm.DirtBuffer;
            long dirtAfter = dirt - up + down;
            if (dirtAfter < 0)
            {
                return "{\"ok\":false,\"error\":\"not enough dirt. Lower some land first to get dirt\",\"dirtNeededM3\":"
                    + Mathf.RoundToInt((up - down - dirt) / 64f * Cell * Cell) + "}";
            }

            if (dirtAfter > DirtMax)
            {
                return "{\"ok\":false,\"error\":\"too much dirt. Raise some land first to use dirt\",\"dirtExcessM3\":"
                    + Mathf.RoundToInt((dirtAfter - DirtMax) / 64f * Cell * Cell) + "}";
            }

            var eco = EconomyManager.instance;
            if (pay && cost > 0 && eco.PeekResource(EconomyManager.Resource.Landscaping, (int)cost) != cost)
            {
                return "{\"ok\":false,\"error\":\"not enough money\",\"cost\":" + cost / 100 + ",\"money\":" + eco.LastCashAmount / 100 + "}";
            }

            int cx0 = Res, cz0 = Res, cx1 = 0, cz1 = 0;
            foreach (var c in changes)
            {
                raw[c.Key] = c.Value;
                int ci = c.Key / (Res + 1), cj = c.Key % (Res + 1);
                cx0 = Math.Min(cx0, cj);
                cx1 = Math.Max(cx1, cj);
                cz0 = Math.Min(cz0, ci);
                cz1 = Math.Max(cz1, ci);
            }

            tm.DirtBuffer = (int)dirtAfter;
            if (pay && cost > 0)
            {
                eco.FetchResource(EconomyManager.Resource.Landscaping, (int)cost, ItemClass.Service.Beautification, ItemClass.SubService.None, ItemClass.Level.None);
            }
            else if (pay && cost < 0)
            {
                eco.AddResource(EconomyManager.Resource.RefundAmount, (int)-cost, ItemClass.Service.Beautification, ItemClass.SubService.None, ItemClass.Level.None);
            }

            TerrainModify.UpdateArea(cx0 - 2, cz0 - 2, cx1 + 2, cz1 + 2, true, false, false);
            return "{\"ok\":true,\"mode\":" + Json.Str(mode) + ",\"changedPoints\":" + changes.Count
                + ",\"raisedM3\":" + Mathf.RoundToInt(up / 64f * Cell * Cell) + ",\"loweredM3\":" + Mathf.RoundToInt(down / 64f * Cell * Cell)
                + ",\"cost\":" + cost / 100 + ",\"paid\":" + (pay ? "true" : "false")
                + ",\"dirtBufferM3\":" + Mathf.RoundToInt(dirtAfter / 64f * Cell * Cell)
                + ",\"skippedUnderObjects\":" + skippedObjects + ",\"skippedOutOfArea\":" + skippedArea + "}";
        }

        // 点のまわり(16m四方)に、建物か道路・線路があるか
        private static bool UnderObject(float x, float z, float h)
        {
            float r = Cell * 0.5f;
            var q = new Quad2(new Vector2(x - r, z - r), new Vector2(x - r, z + r), new Vector2(x + r, z + r), new Vector2(x + r, z - r));
            return BuildingManager.instance.OverlapQuad(q, h - 100f, h + 100f, ItemClass.CollisionType.Terrain, ItemClass.Layer.Default, 0, 0, 0)
                || NetManager.instance.OverlapQuad(q, h - 100f, h + 100f, ItemClass.CollisionType.Terrain, ItemClass.Layer.Default, 0, 0, 0);
        }
    }
}
