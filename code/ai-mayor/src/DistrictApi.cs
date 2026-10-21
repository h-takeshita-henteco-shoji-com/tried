using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 地区の窓口: 地区を塗る、一覧、地区の政策と産業の特化、名前の付け替え(#82)。
    // #82 の育てる期間で、AI市長は地区を作れず、特化や地区ごとの政策を使えなかった。
    // 塗りはゲームの地区の道具と同じ DistrictTool.ApplyBrush を呼ぶ(81区画のMODもこの関数を書き換えて広げている)。
    public static class DistrictApi
    {
        private const float CellSize = 19.2f;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/districts"] = req => HttpBridge.OnMain(List);
            routes["/district/paint"] = req => HttpBridge.OnSimulation(() => Paint(req));
            routes["/district/policy"] = req => HttpBridge.OnSimulation(() => Policy(req));
            routes["/district/rename"] = req => HttpBridge.OnSimulation(() => Rename(req));
        }

        // 地区の格子の一辺のマス数。ゲームは512、81区画のMODは900にする。配列の長さから求める
        private static int Resolution()
        {
            return (int)Math.Round(Math.Sqrt(DistrictManager.instance.m_districtGrid.Length));
        }

        // 地区を名前で探す。なければ 0
        private static byte FindByName(string name)
        {
            var dm = DistrictManager.instance;
            for (int i = 1; i < dm.m_districts.m_buffer.Length; i++)
            {
                if ((dm.m_districts.m_buffer[i].m_flags & District.Flags.Created) != 0 && dm.GetDistrictName(i) == name)
                {
                    return (byte)i;
                }
            }

            return 0;
        }

        // 番号(数字)か名前で地区を探す。なければ 0
        private static byte Resolve(string key)
        {
            int id;
            if (int.TryParse(key, NumberStyles.Integer, CultureInfo.InvariantCulture, out id))
            {
                var dm = DistrictManager.instance;
                return id > 0 && id < dm.m_districts.m_buffer.Length && (dm.m_districts.m_buffer[id].m_flags & District.Flags.Created) != 0
                    ? (byte)id : (byte)0;
            }

            return string.IsNullOrEmpty(key) ? (byte)0 : FindByName(key);
        }

        // 地区がいちばん強く塗られたマス(m_district1)の数と、その中心
        private static int CountCells(byte district, out Vector3 center)
        {
            var grid = DistrictManager.instance.m_districtGrid;
            int res = Resolution();
            double sx = 0, sz = 0;
            int n = 0;
            for (int i = 0; i < grid.Length; i++)
            {
                if (grid[i].m_district1 == district && grid[i].m_alpha1 > 0)
                {
                    sx += (i % res - res / 2 + 0.5) * CellSize;
                    sz += (i / res - res / 2 + 0.5) * CellSize;
                    n++;
                }
            }

            center = n > 0 ? new Vector3((float)(sx / n), 0f, (float)(sz / n)) : Vector3.zero;
            return n;
        }

        // /district/paint?x=..&z=..&radius=150&name=博多  円を地区に塗る。name の地区がなければ作る。erase=true で塗りを消す
        private static string Paint(HttpListenerRequest req)
        {
            var center = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float radius = Mathf.Clamp(F(req, "radius", 100f), 20f, 1000f);
            bool erase = req.QueryString["erase"] == "true";
            string name = (req.QueryString["name"] ?? "").Trim();
            var dm = DistrictManager.instance;

            byte district = 0;
            bool created = false;
            if (!erase)
            {
                if (name.Length == 0)
                {
                    return HttpBridge.Error("name is required (or erase=true)");
                }

                district = Resolve(name);
                if (district == 0)
                {
                    if (!dm.CreateDistrict(out district))
                    {
                        return HttpBridge.Error("could not create a district (too many districts?)");
                    }

                    created = true;
                    var e = dm.SetDistrictName(district, name);
                    while (e.MoveNext())
                    {
                    }
                }
            }

            // ゲームの道具と同じ塗り。始点と終点を同じにすると、円を1回塗る
            DistrictTool.ApplyBrush(DistrictTool.Layer.Districts, district, radius, center, center);

            if (erase)
            {
                return "{\"ok\":true,\"erased\":true,\"x\":" + R(center.x) + ",\"z\":" + R(center.z) + ",\"radius\":" + R(radius) + "}";
            }

            Vector3 c;
            int cells = CountCells(district, out c);
            return "{\"ok\":true,\"district\":" + district + ",\"name\":" + Json.Str(dm.GetDistrictName(district))
                + ",\"created\":" + (created ? "true" : "false") + ",\"cells\":" + cells
                + ",\"areaKm2\":" + (cells * CellSize * CellSize / 1e6).ToString("0.00", CultureInfo.InvariantCulture) + "}";
        }

        // /districts  地区の一覧
        private static string List()
        {
            var dm = DistrictManager.instance;
            var sb = new StringBuilder("{\"ok\":true,\"districts\":[");
            bool first = true;
            for (int i = 1; i < dm.m_districts.m_buffer.Length; i++)
            {
                var d = dm.m_districts.m_buffer[i];
                if ((d.m_flags & District.Flags.Created) == 0)
                {
                    continue;
                }

                Vector3 c;
                int cells = CountCells((byte)i, out c);
                sb.Append(first ? "" : ",").Append("{\"district\":").Append(i).Append(",\"name\":").Append(Json.Str(dm.GetDistrictName(i)))
                  .Append(",\"x\":").Append(R(c.x)).Append(",\"z\":").Append(R(c.z)).Append(",\"cells\":").Append(cells)
                  .Append(",\"population\":").Append(d.m_populationData.m_finalCount)
                  .Append(",\"policies\":").Append(SetPolicies((byte)i)).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // 地区にかかっている政策(特化を含む)の名前の配列
        private static string SetPolicies(byte district)
        {
            var dm = DistrictManager.instance;
            var sb = new StringBuilder("[");
            bool first = true;
            foreach (DistrictPolicies.Policies p in Enum.GetValues(typeof(DistrictPolicies.Policies)))
            {
                if (p == DistrictPolicies.Policies.None || !IsDistrictType(p))
                {
                    continue;
                }

                if (dm.IsDistrictPolicySet(p, district))
                {
                    sb.Append(first ? "" : ",").Append(Json.Str(p.ToString()));
                    first = false;
                }
            }

            return sb.Append(']').ToString();
        }

        // 地区にかけられる政策の種類(特化、サービス、税、都市計画)
        private static bool IsDistrictType(DistrictPolicies.Policies p)
        {
            var t = (DistrictPolicies.Types)((int)p >> 5);
            return t == DistrictPolicies.Types.Specialization || t == DistrictPolicies.Types.Services
                || t == DistrictPolicies.Types.Taxation || t == DistrictPolicies.Types.CityPlanning;
        }

        // /district/policy?district=博多&name=Ore&active=true  地区の政策。産業の特化(Forest、Farming、Oil、Ore)は1つだけかかる
        private static string Policy(HttpListenerRequest req)
        {
            byte district = Resolve(req.QueryString["district"]);
            if (district == 0)
            {
                return HttpBridge.Error("district not found: " + req.QueryString["district"] + " (see /districts)");
            }

            string name = req.QueryString["name"] ?? "";
            DistrictPolicies.Policies p;
            try
            {
                p = (DistrictPolicies.Policies)Enum.Parse(typeof(DistrictPolicies.Policies), name, true);
            }
            catch (Exception)
            {
                return HttpBridge.Error("unknown policy: " + name);
            }

            var dm = DistrictManager.instance;
            if (p == DistrictPolicies.Policies.None || !IsDistrictType(p) || !dm.IsPolicyLoaded(p))
            {
                return HttpBridge.Error("this policy cannot be set on a district in this game (DLC or type): " + name);
            }

            if (!ToolsModifierControl.IsUnlocked(p))
            {
                return HttpBridge.Error("this policy is not unlocked yet: " + name);
            }

            bool active = req.QueryString["active"] != "false";
            if (active)
            {
                dm.SetDistrictPolicy(p, district);
            }
            else
            {
                dm.UnsetDistrictPolicy(p, district);
            }

            return "{\"ok\":true,\"district\":" + district + ",\"name\":" + Json.Str(p.ToString())
                + ",\"active\":" + (dm.IsDistrictPolicySet(p, district) ? "true" : "false")
                + ",\"policies\":" + SetPolicies(district) + "}";
        }

        // /district/rename?district=3&name=博多
        private static string Rename(HttpListenerRequest req)
        {
            byte district = Resolve(req.QueryString["district"]);
            string name = (req.QueryString["name"] ?? "").Trim();
            if (district == 0 || name.Length == 0)
            {
                return HttpBridge.Error("district and name are required (see /districts)");
            }

            var e = DistrictManager.instance.SetDistrictName(district, name);
            while (e.MoveNext())
            {
            }

            return "{\"ok\":true,\"district\":" + district + ",\"name\":" + Json.Str(DistrictManager.instance.GetDistrictName(district)) + "}";
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
