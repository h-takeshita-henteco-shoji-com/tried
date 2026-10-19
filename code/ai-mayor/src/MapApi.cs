using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 地図と、建物のつながりを見る窓口(#81)。
    // 市長は区画を画面写真で見られず、管や送電線が建物につながったかも分からなかった。
    // - /map/data: 円の中の区画マス、線、建物を返す。MCP サーバーが絵にする(描き方を変えてもゲームの再起動が要らない)
    // - Grid: 建物の場所に電気・水・下水が来ているか。ゲームの建物が見るのと同じ格子の値(ElectricityManager, WaterManager)
    // - Ports: 建物の管のつなぎ口と、外の管につながっているか
    public static class MapApi
    {
        private static readonly Dictionary<ItemClass.Zone, string> ZoneCodes = new Dictionary<ItemClass.Zone, string>
        {
            { ItemClass.Zone.Unzoned, "U" },
            { ItemClass.Zone.ResidentialLow, "RL" }, { ItemClass.Zone.ResidentialHigh, "RH" },
            { ItemClass.Zone.CommercialLow, "CL" }, { ItemClass.Zone.CommercialHigh, "CH" },
            { ItemClass.Zone.Industrial, "I" }, { ItemClass.Zone.Office, "O" },
        };

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/map/data"] = req => HttpBridge.OnMain(() => Data(req));
        }

        // /map/data?x=..&z=..&radius=500
        private static string Data(HttpListenerRequest req)
        {
            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r = Mathf.Clamp(F(req, "radius", 500f), 50f, 2000f);
            var sb = new StringBuilder("{\"ok\":true,\"x\":").Append(R(c.x)).Append(",\"z\":").Append(R(c.z)).Append(",\"radius\":").Append(R(r));

            // 区画マス: [x, z, 種類, 建物が建っているか(1/0)]
            sb.Append(",\"cells\":[");
            var blocks = ZoneManager.instance.m_blocks.m_buffer;
            bool first = true;
            for (int i = 1; i < blocks.Length; i++)
            {
                if (blocks[i].m_flags == 0 || Flat(blocks[i].m_position - c) > r + 64f)
                {
                    continue;
                }

                for (int zz = 0; zz < blocks[i].RowCount; zz++)
                {
                    for (int xx = 0; xx < 4; xx++)
                    {
                        ulong bit = 1UL << (zz << 3 | xx);
                        if ((blocks[i].m_valid & bit) == 0 || (blocks[i].m_shared & bit) != 0)
                        {
                            continue;
                        }

                        string code;
                        if (!ZoneCodes.TryGetValue(blocks[i].GetZone(xx, zz), out code))
                        {
                            continue;
                        }

                        var p = CityApi.CellPosition(ref blocks[i], xx, zz);
                        if (Flat(p - c) > r)
                        {
                            continue;
                        }

                        bool occupied = (blocks[i].m_occupied1 & bit) != 0 || (blocks[i].m_occupied2 & bit) != 0;
                        sb.Append(first ? "" : ",").Append('[').Append(R(p.x)).Append(',').Append(R(p.z))
                          .Append(",\"").Append(code).Append("\",").Append(occupied ? 1 : 0).Append(']');
                        first = false;
                    }
                }
            }

            // 線: [始点x, 始点z, 中点x, 中点z, 終点x, 終点z, サービス, 高架や橋か(1/0)]
            sb.Append("],\"lines\":[");
            var nets = NetManager.instance;
            first = true;
            for (int i = 1; i < nets.m_segments.m_size; i++)
            {
                var seg = nets.m_segments.m_buffer[i];
                if ((seg.m_flags & NetSegment.Flags.Created) == 0 || seg.Info == null)
                {
                    continue;
                }

                var a = nets.m_nodes.m_buffer[seg.m_startNode].m_position;
                var b = nets.m_nodes.m_buffer[seg.m_endNode].m_position;
                var m = seg.m_middlePosition;
                if (Flat(a - c) > r && Flat(b - c) > r && Flat(m - c) > r)
                {
                    continue;
                }

                // 建物の中の管などは描かない。高架の点は橋脚(線の一部の建物)とひも付くので、それは除く
                if (InsideBuilding(nets.m_nodes.m_buffer[seg.m_startNode].m_building)
                    && InsideBuilding(nets.m_nodes.m_buffer[seg.m_endNode].m_building))
                {
                    continue;
                }

                string name = seg.Info.name;
                bool raised = name.Contains("Elevated") || name.Contains("Bridge");
                sb.Append(first ? "" : ",").Append('[').Append(R(a.x)).Append(',').Append(R(a.z)).Append(',')
                  .Append(R(m.x)).Append(',').Append(R(m.z)).Append(',').Append(R(b.x)).Append(',').Append(R(b.z))
                  .Append(',').Append(Json.Str(seg.Info.m_class.m_service.ToString())).Append(',').Append(raised ? 1 : 0).Append(']');
                first = false;
            }

            // 建物: [x, z, 幅(m), 奥行き(m), 向き(ラジアン), サービス, 電気, 水, 下水(1/0)]
            sb.Append("],\"buildings\":[");
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            first = true;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null || bs[i].m_parentBuilding != 0
                    || IsNetPart(ref bs[i]) || Flat(bs[i].m_position - c) > r)
                {
                    continue;
                }

                bool e, w, s;
                Grid(ref bs[i], out e, out w, out s);
                var info = bs[i].Info;
                sb.Append(first ? "" : ",").Append('[').Append(R(bs[i].m_position.x)).Append(',').Append(R(bs[i].m_position.z))
                  .Append(',').Append(info.m_cellWidth * 8).Append(',').Append(info.m_cellLength * 8)
                  .Append(',').Append(bs[i].m_angle.ToString("0.###", CultureInfo.InvariantCulture))
                  .Append(',').Append(Json.Str(info.m_class.m_service.ToString()))
                  .Append(',').Append(e ? 1 : 0).Append(',').Append(w ? 1 : 0).Append(',').Append(s ? 1 : 0).Append(']');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // 建物の場所に電気・水・下水が来ているか。格子は時間を進めたときに更新されるので、建てた直後は古い値になる
        public static void Grid(ref Building b, out bool electricity, out bool water, out bool sewage)
        {
            byte pollution;
            ElectricityManager.instance.CheckElectricity(b.m_position, out electricity);
            WaterManager.instance.CheckWater(b.m_position, out water, out sewage, out pollution);
        }

        // "grid":{"electricity":..,"water":..,"sewage":..}
        public static string GridJson(ref Building b)
        {
            bool e, w, s;
            Grid(ref b, out e, out w, out s);
            return "{\"electricity\":" + B(e) + ",\"water\":" + B(w) + ",\"sewage\":" + B(s) + "}";
        }

        // 建物の管・送電線のつなぎ口(建物の中の線の端)と、外の線につながっているか。なければ "[]"
        public static string PortsJson(ushort id)
        {
            var nodes = NetManager.instance.m_nodes.m_buffer;
            var segs = NetManager.instance.m_segments.m_buffer;
            var sb = new StringBuilder("[");
            bool first = true;
            ushort n = BuildingManager.instance.m_buildings.m_buffer[id].m_netNode;
            int guard = 0;
            while (n != 0 && guard++ < 256)
            {
                var info = nodes[n].Info;
                if (info != null && (info.m_class.m_service == ItemClass.Service.Water || info.m_class.m_service == ItemClass.Service.Electricity))
                {
                    int own = 0, outside = 0;
                    for (int k = 0; k < 8; k++)
                    {
                        ushort s = nodes[n].GetSegment(k);
                        if (s == 0)
                        {
                            continue;
                        }

                        ushort other = segs[s].m_startNode == n ? segs[s].m_endNode : segs[s].m_startNode;
                        if (nodes[other].m_building == id)
                        {
                            own++;
                        }
                        else
                        {
                            outside++;
                        }
                    }

                    // 建物の中の線の端だけを、つなぎ口として返す
                    if (own <= 1)
                    {
                        var p = nodes[n].m_position;
                        sb.Append(first ? "" : ",").Append("{\"service\":").Append(Json.Str(info.m_class.m_service.ToString()))
                          .Append(",\"x\":").Append(R(p.x)).Append(",\"z\":").Append(R(p.z))
                          .Append(",\"connected\":").Append(B(outside > 0)).Append('}');
                        first = false;
                    }
                }

                n = nodes[n].m_nextBuildingNode;
            }

            return sb.Append(']').ToString();
        }

        // 置く前のつなぎ口: 建物の型の中の管・送電線の端。right は正面を向いて右、forward は正面(入口)の向き(m)。
        // 型の中の z は正面と逆向き(Building.CalculatePosition は z を (sin, -cos) に回す)なので、符号を変える
        public static string PrefabPortsJson(BuildingInfo info)
        {
            var sb = new StringBuilder("[");
            if (info.m_paths == null)
            {
                return "[]";
            }

            // 型の中の点が、いくつの線に使われているか。1つだけの点が線の端
            var uses = new Dictionary<string, int>();
            foreach (var path in info.m_paths)
            {
                if (!IsPort(path))
                {
                    continue;
                }

                foreach (var p in Ends(path))
                {
                    string key = Key(p);
                    int k;
                    uses.TryGetValue(key, out k);
                    uses[key] = k + 1;
                }
            }

            bool first = true;
            foreach (var path in info.m_paths)
            {
                if (!IsPort(path))
                {
                    continue;
                }

                foreach (var p in Ends(path))
                {
                    if (uses[Key(p)] != 1)
                    {
                        continue;
                    }

                    var net = path.m_finalNetInfo ?? path.m_netInfo;
                    sb.Append(first ? "" : ",").Append("{\"service\":").Append(Json.Str(net.m_class.m_service.ToString()))
                      .Append(",\"right\":").Append(R(p.x)).Append(",\"forward\":").Append(R(-p.z)).Append('}');
                    first = false;
                }
            }

            return sb.Append(']').ToString();
        }

        // 線の両端。点が1つだけの線(給水塔など)は、その点がつなぎ口
        private static Vector3[] Ends(BuildingInfo.PathInfo path)
        {
            var n = path.m_nodes;
            return n.Length == 1 ? new[] { n[0] } : new[] { n[0], n[n.Length - 1] };
        }

        // 点がひも付く建物が、市長の建てる建物か(橋脚や電柱でないか)
        private static bool InsideBuilding(ushort id)
        {
            return id != 0 && !IsNetPart(ref BuildingManager.instance.m_buildings.m_buffer[id]);
        }

        // 線の一部としてゲームが置く建物(電柱、管の継ぎ目、橋脚)か。市長が建てる建物ではないので、一覧から外す
        public static bool IsNetPart(ref Building b)
        {
            return (b.m_flags & Building.Flags.Untouchable) != 0;
        }

        private static bool IsPort(BuildingInfo.PathInfo path)
        {
            var net = path.m_finalNetInfo ?? path.m_netInfo;
            return net != null && path.m_nodes != null && path.m_nodes.Length >= 1
                && (net.m_class.m_service == ItemClass.Service.Water || net.m_class.m_service == ItemClass.Service.Electricity);
        }

        private static string Key(Vector3 p)
        {
            return R(p.x) + "," + R(p.z);
        }

        private static float Flat(Vector3 d)
        {
            return new Vector2(d.x, d.z).magnitude;
        }

        private static string B(bool v)
        {
            return v ? "true" : "false";
        }

        private static string R(float v)
        {
            return Mathf.RoundToInt(v).ToString(CultureInfo.InvariantCulture);
        }

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }
    }
}
