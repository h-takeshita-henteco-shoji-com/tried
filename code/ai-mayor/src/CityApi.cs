using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using ColossalFramework.Math;
using ICities;
using UnityEngine;

namespace AIMayor
{
    // 市政の窓口: 税と予算、政策、区画の指定、建物の配置、時間、出来事、サービスの状況。
    // 設計は code/ai-mayor/docs/mcp-interface.md。
    public static class CityApi
    {
        // 税率の対象。名前 → (サービス, 小分類)
        private static readonly Dictionary<string, KeyValuePair<ItemClass.Service, ItemClass.SubService>> TaxTargets =
            new Dictionary<string, KeyValuePair<ItemClass.Service, ItemClass.SubService>>
            {
                { "residential_low", P(ItemClass.Service.Residential, ItemClass.SubService.ResidentialLow) },
                { "residential_high", P(ItemClass.Service.Residential, ItemClass.SubService.ResidentialHigh) },
                { "commercial_low", P(ItemClass.Service.Commercial, ItemClass.SubService.CommercialLow) },
                { "commercial_high", P(ItemClass.Service.Commercial, ItemClass.SubService.CommercialHigh) },
                { "industrial", P(ItemClass.Service.Industrial, ItemClass.SubService.IndustrialGeneric) },
                { "office", P(ItemClass.Service.Office, ItemClass.SubService.OfficeGeneric) },
            };

        // 予算の対象。名前 → (サービス, 小分類)
        private static readonly Dictionary<string, KeyValuePair<ItemClass.Service, ItemClass.SubService>> BudgetTargets =
            new Dictionary<string, KeyValuePair<ItemClass.Service, ItemClass.SubService>>
            {
                { "electricity", P(ItemClass.Service.Electricity, ItemClass.SubService.None) },
                { "water", P(ItemClass.Service.Water, ItemClass.SubService.None) },
                { "garbage", P(ItemClass.Service.Garbage, ItemClass.SubService.None) },
                { "healthcare", P(ItemClass.Service.HealthCare, ItemClass.SubService.None) },
                { "fire", P(ItemClass.Service.FireDepartment, ItemClass.SubService.None) },
                { "police", P(ItemClass.Service.PoliceDepartment, ItemClass.SubService.None) },
                { "education", P(ItemClass.Service.Education, ItemClass.SubService.None) },
                { "parks", P(ItemClass.Service.Beautification, ItemClass.SubService.None) },
                { "roads", P(ItemClass.Service.Road, ItemClass.SubService.None) },
                { "bus", P(ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportBus) },
                { "metro", P(ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportMetro) },
                { "train", P(ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportTrain) },
                { "ship", P(ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportShip) },
                { "plane", P(ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportPlane) },
                { "taxi", P(ItemClass.Service.PublicTransport, ItemClass.SubService.PublicTransportTaxi) },
            };

        // 区画マスの種類。名前 → ゲームの値
        private static readonly Dictionary<string, ItemClass.Zone> Zones = new Dictionary<string, ItemClass.Zone>
        {
            { "none", ItemClass.Zone.Unzoned },
            { "residential_low", ItemClass.Zone.ResidentialLow },
            { "residential_high", ItemClass.Zone.ResidentialHigh },
            { "commercial_low", ItemClass.Zone.CommercialLow },
            { "commercial_high", ItemClass.Zone.CommercialHigh },
            { "industrial", ItemClass.Zone.Industrial },
            { "office", ItemClass.Zone.Office },
        };

        // DLCなしで使える、街全体の政策
        private static readonly string[] BasePolicies =
        {
            "PowerSaving", "WaterSaving", "SmokeDetectors", "PetBan", "Recycling", "SmokingBan", "EducationBoost",
            "RecreationalUse", "FreeTransport", "BigBusiness", "SmallBusiness", "IndustrySpace", "HighTechHousing",
            "HeavyTrafficBan", "TaxRaiseResLow", "TaxRaiseResHigh", "TaxRaiseComLow", "TaxRaiseComHigh", "TaxRaiseOffice",
            "TaxLowerResLow", "TaxLowerResHigh", "TaxLowerComLow", "TaxLowerComHigh", "TaxLowerOffice",
        };

        // 出来事(つぶやき)の既読の印
        private static readonly HashSet<string> seenMessages = new HashSet<string>();

        private static KeyValuePair<ItemClass.Service, ItemClass.SubService> P(ItemClass.Service s, ItemClass.SubService ss)
        {
            return new KeyValuePair<ItemClass.Service, ItemClass.SubService>(s, ss);
        }

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/economy"] = req => HttpBridge.OnMain(Economy);
            routes["/economy/tax"] = req => HttpBridge.OnSimulation(() => SetTax(req));
            routes["/economy/budget"] = req => HttpBridge.OnSimulation(() => SetBudget(req));
            routes["/services"] = req => HttpBridge.OnMain(Services);
            routes["/policies"] = req => HttpBridge.OnMain(Policies);
            routes["/policies/set"] = req => HttpBridge.OnSimulation(() => SetPolicy(req));
            routes["/zone/area"] = req => HttpBridge.OnSimulation(() => ZoneArea(req));
            routes["/zone/cells"] = req => HttpBridge.OnMain(() => ZoneCells(req));
            routes["/building/prefabs"] = req => HttpBridge.OnMain(() => BuildingPrefabs(req));
            routes["/building/place"] = req => HttpBridge.OnSimulation(() => PlaceBuilding(req));
            routes["/buildings"] = req => HttpBridge.OnMain(() => BuildingsNear(req));
            routes["/time"] = req => HttpBridge.OnMain(() => Time(req));
            routes["/events"] = req => HttpBridge.OnMain(Events);
        }

        // ---- 税と予算 ----

        private static string Economy()
        {
            var eco = EconomyManager.instance;
            var sb = new StringBuilder("{\"ok\":true,\"tax\":{");
            bool first = true;
            foreach (var kv in TaxTargets)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(':')
                  .Append(eco.GetTaxRate(kv.Value.Key, kv.Value.Value, ItemClass.Level.Level1));
                first = false;
            }

            sb.Append("},\"budget\":{");
            first = true;
            foreach (var kv in BudgetTargets)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(":{\"day\":")
                  .Append(eco.GetBudget(kv.Value.Key, kv.Value.Value, false)).Append(",\"night\":")
                  .Append(eco.GetBudget(kv.Value.Key, kv.Value.Value, true)).Append('}');
                first = false;
            }

            return sb.Append("}}").ToString();
        }

        // /economy/tax?target=residential_low&rate=12  税率は1〜29
        private static string SetTax(HttpListenerRequest req)
        {
            KeyValuePair<ItemClass.Service, ItemClass.SubService> t;
            if (!TaxTargets.TryGetValue(req.QueryString["target"] ?? "", out t))
            {
                return HttpBridge.Error("target must be one of: " + string.Join(", ", new List<string>(TaxTargets.Keys).ToArray()));
            }

            int rate = Mathf.Clamp(I(req, "rate", 9), 1, 29);
            for (int lv = (int)ItemClass.Level.Level1; lv <= (int)ItemClass.Level.Level5; lv++)
            {
                EconomyManager.instance.SetTaxRate(t.Key, t.Value, (ItemClass.Level)lv, rate);
            }

            return "{\"ok\":true,\"target\":" + Json.Str(req.QueryString["target"]) + ",\"rate\":" + rate + "}";
        }

        // /economy/budget?target=education&percent=110  予算は50〜150%。昼と夜の両方に設定する
        private static string SetBudget(HttpListenerRequest req)
        {
            KeyValuePair<ItemClass.Service, ItemClass.SubService> t;
            if (!BudgetTargets.TryGetValue(req.QueryString["target"] ?? "", out t))
            {
                return HttpBridge.Error("target must be one of: " + string.Join(", ", new List<string>(BudgetTargets.Keys).ToArray()));
            }

            int pct = Mathf.Clamp(I(req, "percent", 100), 50, 150);
            EconomyManager.instance.SetBudget(t.Key, t.Value, pct, false);
            EconomyManager.instance.SetBudget(t.Key, t.Value, pct, true);
            return "{\"ok\":true,\"target\":" + Json.Str(req.QueryString["target"]) + ",\"percent\":" + pct + "}";
        }

        // ---- サービスの状況 ----

        private static string Services()
        {
            var d = DistrictManager.instance.m_districts.m_buffer[0];
            var sb = new StringBuilder("{\"ok\":true");
            Pair(sb, "electricity", d.GetElectricityCapacity(), d.GetElectricityConsumption());
            Pair(sb, "water", d.GetWaterCapacity(), d.GetWaterConsumption());
            Pair(sb, "sewage", d.GetSewageCapacity(), (int)d.m_residentialConsumption.m_finalSewageAccumulation
                + (int)d.m_commercialConsumption.m_finalSewageAccumulation + (int)d.m_industrialConsumption.m_finalSewageAccumulation
                + (int)d.m_officeConsumption.m_finalSewageAccumulation + (int)d.m_playerConsumption.m_finalSewageAccumulation);
            Pair(sb, "garbage", d.GetGarbageCapacity(), d.GetGarbageAmount());
            Pair(sb, "healthcare", d.GetHealCapacity(), d.GetSickCount());
            Pair(sb, "deathcare", d.GetDeadCapacity(), d.GetDeadAmount());
            Pair(sb, "police", d.GetCriminalCapacity(), d.GetCriminalAmount());
            sb.Append(",\"education\":{\"elementary\":").Append(d.GetEducation1Capacity())
              .Append(",\"high\":").Append(d.GetEducation2Capacity())
              .Append(",\"university\":").Append(d.GetEducation3Capacity()).Append('}');
            sb.Append(",\"workers\":").Append(d.GetWorkerCount())
              .Append(",\"workplaces\":").Append(d.GetWorkplaceCount())
              .Append(",\"crimeRate\":").Append(d.m_finalCrimeRate);
            return sb.Append('}').ToString();
        }

        private static void Pair(StringBuilder sb, string name, int capacity, int used)
        {
            sb.Append(',').Append(Json.Str(name)).Append(":{\"capacity\":").Append(capacity).Append(",\"used\":").Append(used).Append('}');
        }

        // ---- 政策 ----

        private static string Policies()
        {
            var dm = DistrictManager.instance;
            var sb = new StringBuilder("{\"ok\":true,\"policies\":[");
            for (int i = 0; i < BasePolicies.Length; i++)
            {
                var p = (DistrictPolicies.Policies)Enum.Parse(typeof(DistrictPolicies.Policies), BasePolicies[i]);
                sb.Append(i == 0 ? "" : ",").Append("{\"name\":").Append(Json.Str(BasePolicies[i]))
                  .Append(",\"active\":").Append(dm.IsCityPolicySet(p) ? "true" : "false").Append('}');
            }

            return sb.Append("]}").ToString();
        }

        // /policies/set?name=Recycling&active=true
        private static string SetPolicy(HttpListenerRequest req)
        {
            string name = req.QueryString["name"] ?? "";
            if (Array.IndexOf(BasePolicies, name) < 0)
            {
                return HttpBridge.Error("unknown policy: " + name + " (see /policies)");
            }

            var p = (DistrictPolicies.Policies)Enum.Parse(typeof(DistrictPolicies.Policies), name);
            bool active = req.QueryString["active"] != "false";
            if (active)
            {
                DistrictManager.instance.SetCityPolicy(p);
            }
            else
            {
                DistrictManager.instance.UnsetCityPolicy(p);
            }

            return "{\"ok\":true,\"name\":" + Json.Str(name) + ",\"active\":" + (DistrictManager.instance.IsCityPolicySet(p) ? "true" : "false") + "}";
        }

        // ---- 区画の指定 ----

        // 区画マスの中心の位置(ゲームの ZoneBlock と同じ計算)
        private static Vector3 CellPosition(ref ZoneBlock block, int x, int z)
        {
            var a = new Vector3(Mathf.Cos(block.m_angle), 0f, Mathf.Sin(block.m_angle)) * 8f;
            var b = new Vector3(a.z, 0f, -a.x);
            return block.m_position + a * (x - 3.5f) + b * (z - 3.5f);
        }

        // /zone/area?x=..&z=..&radius=100&type=residential_low  円の中の、道路沿いの区画マスを指定する
        private static string ZoneArea(HttpListenerRequest req)
        {
            ItemClass.Zone zone;
            if (!Zones.TryGetValue(req.QueryString["type"] ?? "", out zone))
            {
                return HttpBridge.Error("type must be one of: " + string.Join(", ", new List<string>(Zones.Keys).ToArray()));
            }

            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r = F(req, "radius", 100f);
            var zm = ZoneManager.instance;
            var blocks = zm.m_blocks.m_buffer;
            int changed = 0, skippedOccupied = 0;
            for (int i = 1; i < blocks.Length; i++)
            {
                if (blocks[i].m_flags == 0)
                {
                    continue;
                }

                var dc = blocks[i].m_position - c;
                dc.y = 0f;
                if (dc.magnitude > r + 64f)
                {
                    continue; // 1つの塊は最大で約64m四方
                }

                bool any = false;
                int rows = blocks[i].RowCount;
                for (int zz = 0; zz < rows; zz++)
                {
                    for (int xx = 0; xx < 4; xx++)
                    {
                        if ((blocks[i].m_valid & (1UL << (zz << 3 | xx))) == 0)
                        {
                            continue;
                        }

                        var p = CellPosition(ref blocks[i], xx, zz) - c;
                        p.y = 0f;
                        if (p.magnitude > r)
                        {
                            continue;
                        }

                        if (blocks[i].IsOccupied1(xx, zz) || blocks[i].IsOccupied2(xx, zz))
                        {
                            skippedOccupied++;
                            continue;
                        }

                        if (blocks[i].SetZone(xx, zz, zone))
                        {
                            changed++;
                            any = true;
                        }
                    }
                }

                if (any)
                {
                    blocks[i].RefreshZoning((ushort)i);
                    zm.UpdateBlock((ushort)i);
                }
            }

            return "{\"ok\":true,\"type\":" + Json.Str(req.QueryString["type"]) + ",\"changedCells\":" + changed
                + ",\"skippedOccupied\":" + skippedOccupied + "}";
        }

        // /zone/cells?x=..&z=..&radius=100  円の中の区画マスを、種類ごとに数える
        private static string ZoneCells(HttpListenerRequest req)
        {
            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r = F(req, "radius", 100f);
            var counts = new Dictionary<string, int>();
            var blocks = ZoneManager.instance.m_blocks.m_buffer;
            for (int i = 1; i < blocks.Length; i++)
            {
                if (blocks[i].m_flags == 0)
                {
                    continue;
                }

                var dc = blocks[i].m_position - c;
                dc.y = 0f;
                if (dc.magnitude > r + 64f)
                {
                    continue;
                }

                for (int zz = 0; zz < blocks[i].RowCount; zz++)
                {
                    for (int xx = 0; xx < 4; xx++)
                    {
                        if ((blocks[i].m_valid & (1UL << (zz << 3 | xx))) == 0)
                        {
                            continue;
                        }

                        var p = CellPosition(ref blocks[i], xx, zz) - c;
                        p.y = 0f;
                        if (p.magnitude > r)
                        {
                            continue;
                        }

                        string k = blocks[i].GetZone(xx, zz).ToString();
                        int n;
                        counts.TryGetValue(k, out n);
                        counts[k] = n + 1;
                    }
                }
            }

            var sb = new StringBuilder("{\"ok\":true,\"cells\":{");
            bool first = true;
            foreach (var kv in counts)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(':').Append(kv.Value);
                first = false;
            }

            return sb.Append("}}").ToString();
        }

        // ---- 建物 ----

        private static bool IsZoned(ItemClass.Service s)
        {
            return s == ItemClass.Service.Residential || s == ItemClass.Service.Commercial
                || s == ItemClass.Service.Industrial || s == ItemClass.Service.Office;
        }

        // /building/prefabs?service=Education  置ける建物(区画に自然に建つ建物は除く)
        private static string BuildingPrefabs(HttpListenerRequest req)
        {
            string service = req.QueryString["service"];
            var sb = new StringBuilder("{\"ok\":true,\"prefabs\":[");
            bool first = true;
            int n = PrefabCollection<BuildingInfo>.LoadedCount();
            for (uint i = 0; i < n; i++)
            {
                var info = PrefabCollection<BuildingInfo>.GetLoaded(i);
                if (info == null || info.m_class == null || IsZoned(info.m_class.m_service)
                    || info.m_class.m_service == ItemClass.Service.None)
                {
                    continue;
                }

                if (!string.IsNullOrEmpty(service) && info.m_class.m_service.ToString() != service)
                {
                    continue;
                }

                sb.Append(first ? "" : ",").Append("{\"name\":").Append(Json.Str(info.name))
                  .Append(",\"service\":").Append(Json.Str(info.m_class.m_service.ToString()))
                  .Append(",\"subService\":").Append(Json.Str(info.m_class.m_subService.ToString()))
                  .Append(",\"width\":").Append(info.m_cellWidth).Append(",\"length\":").Append(info.m_cellLength)
                  .Append(",\"cost\":").Append(info.GetConstructionCost() / 100)
                  .Append(",\"maintenance\":").Append(info.GetMaintenanceCost() / 100).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // /building/place?prefab=..&x=..&z=..&angle=0&pay=true  angle は度(0で正面が南、道路に面する側を合わせる)
        private static string PlaceBuilding(HttpListenerRequest req)
        {
            string name = req.QueryString["prefab"];
            var info = PrefabCollection<BuildingInfo>.FindLoaded(name);
            if (info == null)
            {
                return HttpBridge.Error("prefab not found: " + name + " (see /building/prefabs)");
            }

            var pos = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            pos.y = TerrainManager.instance.SampleRawHeightSmooth(pos);
            float angle = F(req, "angle", 0f) * Mathf.Deg2Rad;
            bool pay = req.QueryString["pay"] != "false";
            int cost = info.GetConstructionCost();

            var eco = EconomyManager.instance;
            if (pay)
            {
                if (eco.PeekResource(EconomyManager.Resource.Construction, cost) != cost)
                {
                    return "{\"ok\":false,\"error\":\"not enough money\",\"cost\":" + cost / 100 + ",\"money\":" + eco.LastCashAmount / 100 + "}";
                }
            }

            var sim = SimulationManager.instance;
            Randomizer rnd = sim.m_randomizer;
            ushort id = 0;
            if (!BuildingManager.instance.CreateBuilding(out id, ref rnd, info, pos, angle, info.m_cellLength, sim.m_currentBuildIndex))
            {
                return HttpBridge.Error("CreateBuilding failed");
            }

            sim.m_currentBuildIndex++;
            if (pay)
            {
                eco.FetchResource(EconomyManager.Resource.Construction, cost, info.m_class);
            }

            return "{\"ok\":true,\"id\":" + id + ",\"prefab\":" + Json.Str(name) + ",\"cost\":" + cost / 100
                + ",\"paid\":" + (pay ? "true" : "false") + "}";
        }

        // /buildings?x=..&z=..&radius=200&limit=50  円の中の建物の一覧
        private static string BuildingsNear(HttpListenerRequest req)
        {
            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r2 = F(req, "radius", 200f);
            r2 *= r2;
            int limit = I(req, "limit", 50);
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("{\"ok\":true,\"buildings\":[");
            int count = 0, total = 0;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null)
                {
                    continue;
                }

                var d = bs[i].m_position - c;
                d.y = 0f;
                if (d.sqrMagnitude > r2)
                {
                    continue;
                }

                total++;
                if (count >= limit)
                {
                    continue;
                }

                var info = bs[i].Info;
                sb.Append(count == 0 ? "" : ",").Append("{\"id\":").Append(i)
                  .Append(",\"prefab\":").Append(Json.Str(info.name))
                  .Append(",\"service\":").Append(Json.Str(info.m_class.m_service.ToString()))
                  .Append(",\"x\":").Append(N(bs[i].m_position.x)).Append(",\"z\":").Append(N(bs[i].m_position.z))
                  .Append(",\"abandoned\":").Append((bs[i].m_flags & Building.Flags.Abandoned) != 0 ? "true" : "false")
                  .Append(",\"problems\":").Append(Json.Str(bs[i].m_problems.ToString())).Append('}');
                count++;
            }

            return sb.Append("],\"total\":").Append(total).Append('}').ToString();
        }

        // ---- 時間 ----

        // /time?paused=true|false&speed=1..3  省いた値は今のまま
        private static string Time(HttpListenerRequest req)
        {
            var sim = SimulationManager.instance;

            // 速度を変えると一時停止が解除されるので、速度を先に変えてから一時停止を指定する
            if (req.QueryString["speed"] != null)
            {
                sim.SelectedSimulationSpeed = Mathf.Clamp(I(req, "speed", 1), 1, 3);
            }

            string paused = req.QueryString["paused"];
            if (paused != null)
            {
                sim.SimulationPaused = paused == "true";
            }

            return "{\"ok\":true,\"paused\":" + (sim.SimulationPaused ? "true" : "false") + ",\"speed\":" + sim.SelectedSimulationSpeed
                + ",\"date\":" + Json.Str(sim.m_currentGameTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)) + "}";
        }

        // ---- 出来事 ----

        // /events  前回から増えたつぶやき(市民の声、節目、警告など)
        private static string Events()
        {
            var msgs = MessageManager.instance.GetRecentMessages();
            var sb = new StringBuilder("{\"ok\":true,\"date\":")
                .Append(Json.Str(SimulationManager.instance.m_currentGameTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)))
                .Append(",\"messages\":[");
            int n = 0;
            if (msgs != null)
            {
                foreach (var m in msgs)
                {
                    var cm = m as IChirperMessage;
                    if (cm == null)
                    {
                        continue;
                    }

                    string key = cm.senderID + "|" + cm.text;
                    if (!seenMessages.Add(key))
                    {
                        continue;
                    }

                    sb.Append(n == 0 ? "" : ",").Append("{\"sender\":").Append(Json.Str(cm.senderName))
                      .Append(",\"text\":").Append(Json.Str(cm.text)).Append('}');
                    n++;
                }
            }

            return sb.Append("]}").ToString();
        }

        // ---- 共通 ----

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

        private static string N(float v)
        {
            return v.ToString("0.#", CultureInfo.InvariantCulture);
        }
    }
}
