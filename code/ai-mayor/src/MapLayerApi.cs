using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 地図の情報(ゲームの情報画面にあたるもの)を、点の格子で返す(#82)。
    // 育てる期間に、サービスの届く範囲、汚染・騒音、風、天然資源の場所が分からず、
    // 市長は困りごとの印から逆に探していたため。
    //
    // 値はゲームが情報画面や建物の判定に使うものをそのまま読む。
    // - 届き具合・騒音・犯罪・地価など: ImmaterialResourceManager.CheckLocalResource
    // - 地面の汚染・天然資源: NaturalResourceManager の格子(m_naturalResources)
    // - 水の汚れ・水・下水: WaterManager.CheckWater。電気: ElectricityManager.CheckElectricity
    // - 風: WeatherManager.SampleWindSpeed(風車の発電の計算と同じ。天気の影響は除く)
    public static class MapLayerApi
    {
        private class Layer
        {
            public string Meaning;
            public Func<Vector3, int> Sample;
        }

        private static readonly Dictionary<string, Layer> Layers = new Dictionary<string, Layer>();

        static MapLayerApi()
        {
            Imm("health", ImmaterialResourceManager.Resource.HealthCare, "healthcare coverage. raw game value, 0 = not covered, higher = better");
            Imm("fire", ImmaterialResourceManager.Resource.FireDepartment, "fire department coverage. 0 = not covered, higher = better");
            Imm("police", ImmaterialResourceManager.Resource.PoliceDepartment, "police coverage. 0 = not covered, higher = better");
            Imm("education_elementary", ImmaterialResourceManager.Resource.EducationElementary, "elementary school coverage. 0 = none, higher = better");
            Imm("education_high", ImmaterialResourceManager.Resource.EducationHighSchool, "high school coverage. 0 = none, higher = better");
            Imm("education_university", ImmaterialResourceManager.Resource.EducationUniversity, "university coverage. 0 = none, higher = better");
            Imm("deathcare", ImmaterialResourceManager.Resource.DeathCare, "deathcare (cemetery, crematory) coverage. 0 = none, higher = better");
            Imm("entertainment", ImmaterialResourceManager.Resource.Entertainment, "entertainment (parks etc). the info view treats 200 as full. higher = better");
            Imm("public_transport", ImmaterialResourceManager.Resource.PublicTransport, "public transport stop coverage. 0 = none, higher = better");
            Imm("landvalue", ImmaterialResourceManager.Resource.LandValue, "land value, same as the land value info view. higher = better. buildings level up with it");
            Imm("noise", ImmaterialResourceManager.Resource.NoisePollution, "noise pollution 0-255. higher = worse. residents get sick and the Noise problem appears");
            Imm("crime", ImmaterialResourceManager.Resource.CrimeRate, "crime rate. residents are affected above 3. higher = worse");
            Imm("fire_hazard", ImmaterialResourceManager.Resource.FireHazard, "fire hazard. higher = more fires");
            Imm("abandonment", ImmaterialResourceManager.Resource.Abandonment, "abandoned buildings nearby. higher = worse (lowers land value)");
            Imm("cargo", ImmaterialResourceManager.Resource.CargoTransport, "cargo station coverage. higher = better for industry");
            Imm("attractiveness", ImmaterialResourceManager.Resource.Attractiveness, "tourist attractiveness. higher = more tourists");
            Imm("density", ImmaterialResourceManager.Resource.Density, "building density. higher = denser");

            Nat("pollution", c => c.m_pollution, "ground pollution 0-255, same as the pollution info view. higher = worse (sick residents, lower land value)");
            Nat("ore", c => c.m_ore, "ore resource 0-255. higher = better for the Ore industry specialization");
            Nat("oil", c => c.m_oil, "oil resource 0-255. higher = better for the Oil industry specialization");
            Nat("fertility", c => c.m_fertility, "fertile land 0-255. higher = better for the Farming industry specialization");
            Nat("forest", c => c.m_forest, "forest 0-255. higher = better for the Forest industry specialization");

            Layers["water_pollution"] = new Layer
            {
                Meaning = "pollution of the tap water at the point 0-255. 0 = clean. higher = worse (DirtyWater problem, sick residents)",
                Sample = p =>
                {
                    bool w, s;
                    byte pol;
                    WaterManager.instance.CheckWater(p, out w, out s, out pol);
                    return pol;
                },
            };
            Layers["water_service"] = new Layer
            {
                Meaning = "1 = water pipes reach the point now, 0 = not",
                Sample = p =>
                {
                    bool w, s;
                    byte pol;
                    WaterManager.instance.CheckWater(p, out w, out s, out pol);
                    return w ? 1 : 0;
                },
            };
            Layers["sewage_service"] = new Layer
            {
                Meaning = "1 = sewage is taken at the point now, 0 = not",
                Sample = p =>
                {
                    bool w, s;
                    byte pol;
                    WaterManager.instance.CheckWater(p, out w, out s, out pol);
                    return s ? 1 : 0;
                },
            };
            Layers["electricity_service"] = new Layer
            {
                Meaning = "1 = electricity reaches the point now, 0 = not",
                Sample = p =>
                {
                    bool e;
                    ElectricityManager.instance.CheckElectricity(p, out e);
                    return e ? 1 : 0;
                },
            };
            Layers["wind"] = new Layer
            {
                Meaning = "wind speed 0-100 (percent), same as the wind turbine output factor without weather. higher = better for wind turbines",
                Sample = p => Mathf.RoundToInt(WeatherManager.instance.SampleWindSpeed(p, true) * 100f),
            };
        }

        private static void Imm(string name, ImmaterialResourceManager.Resource r, string meaning)
        {
            Layers[name] = new Layer
            {
                Meaning = meaning,
                Sample = p =>
                {
                    int v;
                    ImmaterialResourceManager.instance.CheckLocalResource(r, p, out v);
                    return v;
                },
            };
        }

        // 天然資源の格子は地図全体(17,280m)を等分している。格子の数は配列の長さから求める(81区画の MOD で変わっても合わせるため)
        private static void Nat(string name, Func<NaturalResourceManager.ResourceCell, byte> pick, string meaning)
        {
            Layers[name] = new Layer
            {
                Meaning = meaning,
                Sample = p =>
                {
                    var cells = NaturalResourceManager.instance.m_naturalResources;
                    int res = (int)Math.Sqrt(cells.Length);
                    float size = 17280f / res;
                    int x = Mathf.Clamp((int)(p.x / size + res / 2f), 0, res - 1);
                    int z = Mathf.Clamp((int)(p.z / size + res / 2f), 0, res - 1);
                    return pick(cells[z * res + x]);
                },
            };
        }

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/map/layer"] = req => HttpBridge.OnMain(() => Sample(req));
            routes["/map/layers"] = req => List();
        }

        // /map/layers  使える type と意味
        private static string List()
        {
            var sb = new StringBuilder("{\"ok\":true,\"layers\":[");
            bool first = true;
            foreach (var kv in Layers)
            {
                sb.Append(first ? "" : ",").Append("{\"type\":").Append(Json.Str(kv.Key))
                  .Append(",\"meaning\":").Append(Json.Str(kv.Value.Meaning)).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // /map/layer?type=noise&x=..&z=..&radius=..&n=9
        // 円を囲む四角を n×n の点で測る。x を省くと、建物のある範囲(街全体)を囲む四角
        private static string Sample(HttpListenerRequest req)
        {
            string type = req.QueryString["type"] ?? "";
            Layer layer;
            if (!Layers.TryGetValue(type, out layer))
            {
                return HttpBridge.Error("unknown type: " + type + " (see /map/layers)");
            }

            int n = Mathf.Clamp(I(req, "n", 9), 3, 25);
            float minX, maxX, minZ, maxZ;
            if (req.QueryString["x"] != null)
            {
                float cx = F(req, "x", 0f), cz = F(req, "z", 0f), r = F(req, "radius", 500f);
                minX = cx - r;
                maxX = cx + r;
                minZ = cz - r;
                maxZ = cz + r;
            }
            else if (!CityBounds(out minX, out maxX, out minZ, out maxZ))
            {
                return HttpBridge.Error("no buildings in the city. pass x, z, radius");
            }

            long sum = 0;
            int min = int.MaxValue, max = int.MinValue;
            Vector3 minAt = Vector3.zero, maxAt = Vector3.zero;
            var grid = new StringBuilder("[");
            for (int iz = 0; iz < n; iz++)
            {
                grid.Append(iz > 0 ? ",[" : "[");
                float z = maxZ - (maxZ - minZ) * iz / (n - 1);
                for (int ix = 0; ix < n; ix++)
                {
                    float x = minX + (maxX - minX) * ix / (n - 1);
                    // 高さは地面に合わせる。風(SampleWindSpeed)は点の高さと地面の差で決まり、0 のままだと地面の下になって常に0になる(#82)
                    var p = new Vector3(x, 0f, z);
                    p.y = TerrainManager.instance.SampleRawHeightSmooth(p);
                    int v = layer.Sample(p);
                    grid.Append(ix > 0 ? "," : "").Append(v);
                    sum += v;
                    if (v < min)
                    {
                        min = v;
                        minAt = p;
                    }

                    if (v > max)
                    {
                        max = v;
                        maxAt = p;
                    }
                }

                grid.Append(']');
            }

            grid.Append(']');
            return "{\"ok\":true,\"type\":" + Json.Str(type) + ",\"meaning\":" + Json.Str(layer.Meaning)
                + ",\"bounds\":{\"minX\":" + R(minX) + ",\"maxX\":" + R(maxX) + ",\"minZ\":" + R(minZ) + ",\"maxZ\":" + R(maxZ) + "}"
                + ",\"n\":" + n + ",\"average\":" + (sum / (n * n)) + ",\"min\":" + min + ",\"max\":" + max
                + ",\"minAt\":{\"x\":" + R(minAt.x) + ",\"z\":" + R(minAt.z) + "}"
                + ",\"maxAt\":{\"x\":" + R(maxAt.x) + ",\"z\":" + R(maxAt.z) + "}"
                + ",\"grid\":" + grid + ",\"gridNote\":\"north row first, west to east\"}";
        }

        // 建物のある範囲(区画の建物とサービスの建物。電柱などの線の部品は除く)
        private static bool CityBounds(out float minX, out float maxX, out float minZ, out float maxZ)
        {
            minX = minZ = float.MaxValue;
            maxX = maxZ = float.MinValue;
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            bool any = false;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null || bs[i].m_parentBuilding != 0
                    || MapApi.IsNetPart(ref bs[i]))
                {
                    continue;
                }

                var p = bs[i].m_position;
                minX = Mathf.Min(minX, p.x);
                maxX = Mathf.Max(maxX, p.x);
                minZ = Mathf.Min(minZ, p.z);
                maxZ = Mathf.Max(maxZ, p.z);
                any = true;
            }

            return any;
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

        private static int I(HttpListenerRequest req, string key, int fallback)
        {
            int v;
            string s = req.QueryString[key];
            return s != null && int.TryParse(s, NumberStyles.Integer, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }
    }
}
