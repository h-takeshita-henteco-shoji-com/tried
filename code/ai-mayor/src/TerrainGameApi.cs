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
            // test=true なら、変えずに、土と費用の見積もりだけ返す(#125)
            bool test = req.QueryString["test"] == "true";
            return HttpBridge.OnSimulation(() => ModifyOnSimulation(poly, mode, value, pay, test), 30000);
        }

        private static string ModifyOnSimulation(List<Vector3> poly, string mode, float value, bool pay, bool test)
        {
            if (!ToolsModifierControl.IsUnlocked(UnlockManager.Feature.Landscaping))
            {
                return HttpBridge.Error("landscaping is not unlocked yet");
            }

            var tm = TerrainManager.instance;
            var raw = tm.RawHeights;
            var area = GameAreaManager.instance;
            long up, down, cost;
            int skippedObjects, skippedArea;
            var changes = Plan(poly, mode, value, out up, out down, out cost, out skippedObjects, out skippedArea);

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
            if (test)
            {
                return "{\"ok\":true,\"test\":true,\"changed\":false,\"mode\":" + Json.Str(mode) + ",\"changedPoints\":" + changes.Count
                    + ",\"raisedM3\":" + Mathf.RoundToInt(up / 64f * Cell * Cell) + ",\"loweredM3\":" + Mathf.RoundToInt(down / 64f * Cell * Cell)
                    + ",\"cost\":" + cost / 100 + ",\"enoughMoney\":" + (cost <= 0 || eco.LastCashAmount >= cost ? "true" : "false")
                    + ",\"dirtBufferM3\":" + Mathf.RoundToInt(dirtAfter / 64f * Cell * Cell)
                    + ",\"skippedUnderObjects\":" + skippedObjects + ",\"skippedOutOfArea\":" + skippedArea + "}";
            }

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

        // 多角形の中で変える点と新しい高さを決め、土と費用を数える。街は変えない(#125 で、変える処理と試しで共有する)
        internal static List<KeyValuePair<int, ushort>> Plan(List<Vector3> poly, string mode, float value,
            out long up, out long down, out long cost, out int skippedObjects, out int skippedArea)
        {
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

            var changes = new List<KeyValuePair<int, ushort>>();
            up = 0;
            down = 0;
            cost = 0;
            skippedObjects = 0;
            skippedArea = 0;
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

            return changes;
        }

        // 試しの判定のあいだだけ、地形を変えたものとして高さを書き換える(#125)。
        // 書式は "モード:値@x1,z1;x2,z2;..."(モードは level / raise / lower)。細かい形(詳細高さ)は更新しない
        // 戻す動作を返す。シミュレーションのスレッドで呼ぶ
        internal static void ApplyVirtual(string spec, List<Action> undo)
        {
            int at = spec.IndexOf('@');
            int colon = spec.IndexOf(':');
            float value;
            if (at < 0 || colon < 0 || colon > at
                || !float.TryParse(spec.Substring(colon + 1, at - colon - 1), NumberStyles.Float, CultureInfo.InvariantCulture, out value))
            {
                return;
            }

            string mode = spec.Substring(0, colon).Trim();
            if (mode != "level" && mode != "raise" && mode != "lower")
            {
                return;
            }

            var poly = new List<Vector3>();
            foreach (var part in spec.Substring(at + 1).Split(';'))
            {
                var xz = part.Split(',');
                float x, z;
                if (xz.Length == 2 && float.TryParse(xz[0], NumberStyles.Float, CultureInfo.InvariantCulture, out x)
                    && float.TryParse(xz[1], NumberStyles.Float, CultureInfo.InvariantCulture, out z))
                {
                    poly.Add(new Vector3(x, 0f, z));
                }
            }

            if (poly.Count < 3)
            {
                return;
            }

            long up, down, cost;
            int so, sa;
            var changes = Plan(poly, mode, value, out up, out down, out cost, out so, out sa);
            if (changes.Count == 0)
            {
                return;
            }

            // ゲームが高さを読む配列は RawHeights2(RawHeights の写し。本番の地形の道具は RawHeights を書き、UpdateArea で写しが後から更新される)。
            // 試しでは、同じ値を両方に書き、戻すときも両方を戻す。UpdateArea は呼ばない(詳細高さは更新しない)
            var raw = TerrainManager.instance.RawHeights;
            var raw2 = TerrainManager.instance.RawHeights2;
            foreach (var c in changes)
            {
                int idx = c.Key;
                ushort before = raw[idx];
                ushort before2 = raw2[idx];
                raw[idx] = c.Value;
                raw2[idx] = c.Value;
                undo.Add(() =>
                {
                    TerrainManager.instance.RawHeights[idx] = before;
                    TerrainManager.instance.RawHeights2[idx] = before2;
                });
            }
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
