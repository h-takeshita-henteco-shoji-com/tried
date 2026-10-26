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
            routes["/zone/polygon"] = ZonePolygon;
            routes["/zone/rect"] = req => HttpBridge.OnSimulation(() => ZoneRect(req));
            routes["/zone/cells"] = req => HttpBridge.OnMain(() => ZoneCells(req));
            routes["/zone/summary"] = req => HttpBridge.OnMain(() => ZoneSummary(req));
            routes["/building/prefabs"] = req => HttpBridge.OnMain(() => BuildingPrefabs(req));
            routes["/building/place"] = req => HttpBridge.OnSimulation(() => PlaceBuilding(req));
            routes["/buildings"] = req => HttpBridge.OnMain(() => BuildingsNear(req));
            routes["/time"] = req => HttpBridge.OnMain(() => Time(req));
            routes["/events"] = req => HttpBridge.OnMain(Events);
            routes["/demand"] = req => HttpBridge.OnMain(Demand);
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

        // /economy/budget?target=education&percent=110  予算は50〜150%。percent は昼と夜の両方に設定する。
        // day= と night= で、昼と夜を分けて設定する(どちらかだけでもよい。#82。ゲームの予算の画面と同じく昼と夜で別の値を持つ)
        private static string SetBudget(HttpListenerRequest req)
        {
            KeyValuePair<ItemClass.Service, ItemClass.SubService> t;
            if (!BudgetTargets.TryGetValue(req.QueryString["target"] ?? "", out t))
            {
                return HttpBridge.Error("target must be one of: " + string.Join(", ", new List<string>(BudgetTargets.Keys).ToArray()));
            }

            var eco = EconomyManager.instance;
            if (req.QueryString["percent"] != null)
            {
                int pct = Mathf.Clamp(I(req, "percent", 100), 50, 150);
                eco.SetBudget(t.Key, t.Value, pct, false);
                eco.SetBudget(t.Key, t.Value, pct, true);
            }

            if (req.QueryString["day"] != null)
            {
                eco.SetBudget(t.Key, t.Value, Mathf.Clamp(I(req, "day", 100), 50, 150), false);
            }

            if (req.QueryString["night"] != null)
            {
                eco.SetBudget(t.Key, t.Value, Mathf.Clamp(I(req, "night", 100), 50, 150), true);
            }

            int day = eco.GetBudget(t.Key, t.Value, false), night = eco.GetBudget(t.Key, t.Value, true);
            return "{\"ok\":true,\"target\":" + Json.Str(req.QueryString["target"]) + ",\"percent\":" + day
                + ",\"day\":" + day + ",\"night\":" + night + "}";
        }

        // ---- サービスの状況 ----

        private static string Services()
        {
            var d = DistrictManager.instance.m_districts.m_buffer[0];
            var sb = new StringBuilder("{\"ok\":true");
            Pair(sb, "electricity", d.GetElectricityCapacity(), d.GetElectricityConsumption());
            Pair(sb, "water", d.GetWaterCapacity(), d.GetWaterConsumption());
            // 下水の used は、以前は内部の値の合計をそのまま返していた。capacity は16倍の値なので、used が1/16に小さく出ていた。
            // #82 の36か月目、used は容量の7%に見えたが、実際は排水口1つの力を超えていて、網の端の家に下水が届かなかった。
            // ゲームの画面と同じ District.GetSewageAccumulation(16倍)を使う。水の used と同じ単位になる
            Pair(sb, "sewage", d.GetSewageCapacity(), d.GetSewageAccumulation());
            // 満ちて受け入れを止めた施設(#82。合計の容量だけでは、満ちた処理場・墓地が見えなかった)。
            // ゲームは満ちた埋立地・墓地に LandfillFull の印を付ける(LandfillSiteAI、CemeteryAI)
            string fullGarbage, fullDeath;
            FullFacilities(out fullGarbage, out fullDeath);
            Pair(sb, "garbage", d.GetGarbageCapacity(), d.GetGarbageAmount(), fullGarbage);
            Pair(sb, "healthcare", d.GetHealCapacity(), d.GetSickCount());
            Pair(sb, "deathcare", d.GetDeadCapacity(), d.GetDeadAmount(), fullDeath);
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

        private static void Pair(StringBuilder sb, string name, int capacity, int used, string full)
        {
            sb.Append(',').Append(Json.Str(name)).Append(":{\"capacity\":").Append(capacity).Append(",\"used\":").Append(used)
              .Append(",\"full\":").Append(full).Append('}');
        }

        // 満ちた施設の数と id(最大20)。ごみは埋立地(LandfillSiteAI)、葬祭は墓地(CemeteryAI)
        private static void FullFacilities(out string garbage, out string death)
        {
            var g = new List<int>();
            var dd = new List<int>();
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int i = 1; i < bs.Length; i++)
            {
                var info = bs[i].Info;
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || info == null)
                {
                    continue;
                }

                Notification.Problem1 p = bs[i].m_problems;
                if ((p & (Notification.Problem1.LandfillFull | Notification.Problem1.WasteTransferFacilityFull)) == 0)
                {
                    continue;
                }

                if (info.m_buildingAI is CemeteryAI)
                {
                    dd.Add(i);
                }
                else if (info.m_buildingAI is LandfillSiteAI)
                {
                    g.Add(i);
                }
            }

            garbage = IdsJson(g);
            death = IdsJson(dd);
        }

        private static string IdsJson(List<int> ids)
        {
            var sb = new StringBuilder("{\"count\":").Append(ids.Count).Append(",\"ids\":[");
            for (int k = 0; k < ids.Count && k < 20; k++)
            {
                sb.Append(k == 0 ? "" : ",").Append(ids[k]);
            }

            return sb.Append("]}").ToString();
        }

        // ---- 政策 ----

        private static string Policies()
        {
            var dm = DistrictManager.instance;
            var counts = CountForPolicies();
            var sb = new StringBuilder("{\"ok\":true,\"policyExpensesPerWeek\":").Append(EconomyManager.instance.GetPolicyExpenses() / 100)
                .Append(",\"policies\":[");
            for (int i = 0; i < BasePolicies.Length; i++)
            {
                var p = (DistrictPolicies.Policies)Enum.Parse(typeof(DistrictPolicies.Policies), BasePolicies[i]);
                sb.Append(i == 0 ? "" : ",").Append("{\"name\":").Append(Json.Str(BasePolicies[i]))
                  .Append(",\"active\":").Append(dm.IsCityPolicySet(p) ? "true" : "false")
                  .Append(',').Append(CostJson(BasePolicies[i], counts)).Append('}');
            }

            return sb.Append("]}").ToString();
        }

        // 政策の週の費用の見積もり。#81 の市長は火災報知器を週200未満と読み、実際は約1,700だった。
        // ゲームは政策の費用を、建物ごとに建物の処理のたびに払う(CommonBuildingAI.HandleFire など)。
        // 1回の額 × 0.16 が週の額(維持費と同じ換算)。対象の建物の数は今の街で数える。
        // 建物が増えれば費用も増える。数字は見積もりで、実際の額は policyExpensesPerWeek で確かめる
        private class PolicyCounts
        {
            public int Fire, Consumers, CommercialLow, CommercialHigh, Industrial, Residential;
            public long SchoolUpkeep; // 学校の維持費(内部の値)
        }

        private static readonly Dictionary<string, KeyValuePair<int, string>> PerBuilding =
            new Dictionary<string, KeyValuePair<int, string>>
            {
                { "SmokeDetectors", new KeyValuePair<int, string>(32, "fire") },
                { "PowerSaving", new KeyValuePair<int, string>(32, "consumers") },
                { "WaterSaving", new KeyValuePair<int, string>(32, "consumers") },
                { "SmallBusiness", new KeyValuePair<int, string>(12, "commercialLow") },
                { "BigBusiness", new KeyValuePair<int, string>(25, "commercialHigh") },
                { "IndustrySpace", new KeyValuePair<int, string>(38, "industrial") },
                { "HighTechHousing", new KeyValuePair<int, string>(25, "residential") },
            };

        private static PolicyCounts CountForPolicies()
        {
            var c = new PolicyCounts();
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int i = 1; i < bs.Length; i++)
            {
                var flags = bs[i].m_flags;
                if ((flags & Building.Flags.Created) == 0 || (flags & (Building.Flags.Deleted | Building.Flags.Abandoned | Building.Flags.Collapsed)) != 0
                    || (flags & Building.Flags.Completed) == 0 || bs[i].Info == null)
                {
                    continue;
                }

                var info = bs[i].Info;
                var ai = info.m_buildingAI;
                int hazard, size, tolerance;
                if (ai.GetFireParameters((ushort)i, ref bs[i], out hazard, out size, out tolerance))
                {
                    c.Fire++;
                }

                if (ai is PrivateBuildingAI)
                {
                    c.Consumers++;
                    var cls = info.m_class;
                    if (cls.isCommercialLowGeneric) c.CommercialLow++;
                    else if (cls.isCommercialHighGenegic || cls.isCommercialWallToWall) c.CommercialHigh++;
                    if (cls.m_service == ItemClass.Service.Industrial && cls.m_subService == ItemClass.SubService.IndustrialGeneric) c.Industrial++;
                    if (cls.m_service == ItemClass.Service.Residential) c.Residential++;
                }
                else if (ai is PlayerBuildingAI)
                {
                    var pai = (PlayerBuildingAI)ai;
                    if (pai.m_electricityConsumption > 0 || pai.m_waterConsumption > 0)
                    {
                        c.Consumers++;
                    }

                    if (ai is SchoolAI)
                    {
                        c.SchoolUpkeep += ai.GetMaintenanceCost();
                    }
                }
            }

            return c;
        }

        private static string CostJson(string name, PolicyCounts c)
        {
            KeyValuePair<int, string> rate;
            if (PerBuilding.TryGetValue(name, out rate))
            {
                int count = rate.Value == "fire" ? c.Fire : rate.Value == "consumers" ? c.Consumers
                    : rate.Value == "commercialLow" ? c.CommercialLow : rate.Value == "commercialHigh" ? c.CommercialHigh
                    : rate.Value == "industrial" ? c.Industrial : c.Residential;
                double perBuilding = rate.Key * 0.16;
                return "\"costPerWeek\":" + Mathf.RoundToInt((float)(perBuilding * count)) + ",\"costBasis\":"
                    + Json.Str(count + " " + rate.Value + " buildings x " + perBuilding.ToString("0.##", CultureInfo.InvariantCulture)
                        + " per week. Grows with the number of buildings");
            }

            if (name == "EducationBoost")
            {
                return "\"costPerWeek\":" + Mathf.RoundToInt((float)(c.SchoolUpkeep * 0.0016 * 0.25))
                    + ",\"costBasis\":\"+25% of school upkeep (shown in education expenses, not policy expenses)\"";
            }

            if (name == "Recycling")
            {
                return "\"costPerWeek\":0,\"costBasis\":\"no direct cost. Residential tax income -5%, garbage -15%\"";
            }

            if (name == "FreeTransport")
            {
                return "\"costPerWeek\":0,\"costBasis\":\"no direct cost. Public transport ticket income becomes 0\"";
            }

            return "\"costPerWeek\":0,\"costBasis\":\"no direct cost\"";
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

            return "{\"ok\":true,\"name\":" + Json.Str(name) + ",\"active\":" + (DistrictManager.instance.IsCityPolicySet(p) ? "true" : "false")
                + "," + CostJson(name, CountForPolicies()) + "}";
        }

        // ---- 区画の指定 ----

        // 区画マスの中心の位置(ゲームの ZoneBlock と同じ計算)
        public static Vector3 CellPosition(ref ZoneBlock block, int x, int z)
        {
            var a = new Vector3(Mathf.Cos(block.m_angle), 0f, Mathf.Sin(block.m_angle)) * 8f;
            var b = new Vector3(a.z, 0f, -a.x);
            return block.m_position + a * (x - 3.5f) + b * (z - 3.5f);
        }

        // /zone/area?x=..&z=..&radius=100&type=residential_low  円の中の、道路沿いの区画マスを指定する
        private static string ZoneArea(HttpListenerRequest req)
        {
            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r = F(req, "radius", 100f);
            return ZoneCellsWhere(req.QueryString["type"], c.x - r, c.z - r, c.x + r, c.z + r, p =>
            {
                var d = p - c;
                d.y = 0f;
                return d.magnitude <= r;
            });
        }

        // POST /zone/polygon?type=..  本文 "x1,z1;x2,z2;..."(多角形の頂点。3つ以上)。#82。
        // 円だけでは、通りに沿った細長い区画や四角い街区をきれいに塗れなかったため。ゲームの区画の道具の「塗りつぶし」に近い
        private static string ZonePolygon(HttpListenerRequest req)
        {
            string body;
            using (var r = new System.IO.StreamReader(req.InputStream, Encoding.UTF8))
            {
                body = r.ReadToEnd();
            }

            List<Vector3> pts;
            try
            {
                pts = NetApi.Parse(body);
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad points: " + e.Message);
            }

            if (pts.Count < 3)
            {
                return HttpBridge.Error("need at least 3 points");
            }

            string type = req.QueryString["type"];
            return HttpBridge.OnSimulation(() => ZoneInPolygon(type, pts));
        }

        // /zone/rect?x1=..&z1=..&x2=..&z2=..&type=..  向きが東西・南北の四角
        private static string ZoneRect(HttpListenerRequest req)
        {
            float x1 = F(req, "x1", 0f), z1 = F(req, "z1", 0f), x2 = F(req, "x2", 0f), z2 = F(req, "z2", 0f);
            var pts = new List<Vector3>
            {
                new Vector3(x1, 0f, z1), new Vector3(x2, 0f, z1), new Vector3(x2, 0f, z2), new Vector3(x1, 0f, z2),
            };
            return ZoneInPolygon(req.QueryString["type"], pts);
        }

        private static string ZoneInPolygon(string type, List<Vector3> pts)
        {
            float minX = float.MaxValue, minZ = float.MaxValue, maxX = float.MinValue, maxZ = float.MinValue;
            foreach (var p in pts)
            {
                minX = Mathf.Min(minX, p.x);
                minZ = Mathf.Min(minZ, p.z);
                maxX = Mathf.Max(maxX, p.x);
                maxZ = Mathf.Max(maxZ, p.z);
            }

            return ZoneCellsWhere(type, minX, minZ, maxX, maxZ, p => InsidePolygon(pts, p.x, p.z));
        }

        // 点が多角形の中か(偶奇の数え方)
        private static bool InsidePolygon(List<Vector3> pts, float x, float z)
        {
            bool inside = false;
            for (int i = 0, j = pts.Count - 1; i < pts.Count; j = i++)
            {
                if ((pts[i].z > z) != (pts[j].z > z)
                    && x < (pts[j].x - pts[i].x) * (z - pts[i].z) / (pts[j].z - pts[i].z) + pts[i].x)
                {
                    inside = !inside;
                }
            }

            return inside;
        }

        // 範囲(minX〜maxX、minZ〜maxZ)の近くの区画の塊を調べ、inside が真のマスを type に指定する。
        // 建物が建っているマスは変えない。円・多角形・四角で同じ処理を使う
        private static string ZoneCellsWhere(string type, float minX, float minZ, float maxX, float maxZ, Func<Vector3, bool> inside)
        {
            ItemClass.Zone zone;
            if (!Zones.TryGetValue(type ?? "", out zone))
            {
                return HttpBridge.Error("type must be one of: " + string.Join(", ", new List<string>(Zones.Keys).ToArray()));
            }

            // 解禁前の区画は断る(#82。オフィスと高密度を Big Town の前から指定できていた)。解除(none)は問わない
            if (zone != ItemClass.Zone.Unzoned && !ToolsModifierControl.IsUnlocked(zone))
            {
                return HttpBridge.Error("this zone type is not unlocked yet: " + type);
            }

            var zm = ZoneManager.instance;
            var blocks = zm.m_blocks.m_buffer;
            int changed = 0, skippedOccupied = 0;
            for (int i = 1; i < blocks.Length; i++)
            {
                if (blocks[i].m_flags == 0)
                {
                    continue;
                }

                // 1つの塊は最大で約64m四方
                var bp = blocks[i].m_position;
                if (bp.x < minX - 64f || bp.x > maxX + 64f || bp.z < minZ - 64f || bp.z > maxZ + 64f)
                {
                    continue;
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

                        if (!inside(CellPosition(ref blocks[i], xx, zz)))
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

            return "{\"ok\":true,\"type\":" + Json.Str(type) + ",\"changedCells\":" + changed
                + ",\"skippedOccupied\":" + skippedOccupied + "}";
        }

        // /zone/summary?grid=1000  街全体の空いた区画マスを、種類ごと・場所ごとに数える(#107)。
        // 12回目に、住宅のマス切れに気づくのが遅れた。zones_at を円ごとに呼ぶしかなかったため。
        // 塊(ZoneBlock)は道に沿って最大8列、奥行き4マス(xx が奥行き、0 が道の側)。
        // 列ごとに、道の側から続く同じ種類の空きの奥行きを見て、細切れを分ける。
        //   shallow: 奥行き1マスしか続かない空き(1マスの奥行きの建物しか建たない)
        //   narrow: 道の側の空きが、隣の列とつながらない1列だけの空き(幅1マスの建物しか建たない)
        private static string ZoneSummary(HttpListenerRequest req)
        {
            float grid = Mathf.Max(250f, F(req, "grid", 1000f));
            var total = new Dictionary<string, int[]>(); // [空き, shallow, narrow, 全部, behind]
            var tiles = new Dictionary<long, Dictionary<string, int>>();
            var blocks = ZoneManager.instance.m_blocks.m_buffer;
            for (int i = 1; i < blocks.Length; i++)
            {
                if (blocks[i].m_flags == 0)
                {
                    continue;
                }

                int rows = blocks[i].RowCount;
                // 列ごとに、道の側から続く空きの奥行きと、その種類
                var depth = new int[rows];
                var front = new ItemClass.Zone[rows];
                for (int zz = 0; zz < rows; zz++)
                {
                    front[zz] = ItemClass.Zone.Unzoned;
                    for (int xx = 0; xx < 4; xx++)
                    {
                        if (!EmptyZoned(ref blocks[i], xx, zz))
                        {
                            break;
                        }

                        var zt = blocks[i].GetZone(xx, zz);
                        if (xx == 0)
                        {
                            front[zz] = zt;
                        }
                        else if (zt != front[zz])
                        {
                            break;
                        }

                        depth[zz] = xx + 1;
                    }
                }

                for (int zz = 0; zz < rows; zz++)
                {
                    bool narrow = depth[zz] > 0
                        && (zz == 0 || front[zz - 1] != front[zz] || depth[zz - 1] == 0)
                        && (zz == rows - 1 || front[zz + 1] != front[zz] || depth[zz + 1] == 0);
                    for (int xx = 0; xx < 4; xx++)
                    {
                        if ((blocks[i].m_valid & (1UL << (zz << 3 | xx))) == 0)
                        {
                            continue;
                        }

                        var zt = blocks[i].GetZone(xx, zz);
                        if (zt == ItemClass.Zone.Unzoned || zt == ItemClass.Zone.Distant)
                        {
                            continue;
                        }

                        string k = zt.ToString();
                        int[] t;
                        if (!total.TryGetValue(k, out t))
                        {
                            t = new int[5];
                            total[k] = t;
                        }

                        t[3]++;
                        // 区画のある区切りは、空きが0でも返す。月どうしで同じ区切りを比べられるように(#107 の13回目)
                        var cp = CellPosition(ref blocks[i], xx, zz);
                        long tkey = ((long)Mathf.FloorToInt(cp.x / grid) << 32) ^ (uint)Mathf.FloorToInt(cp.z / grid);
                        if (!tiles.ContainsKey(tkey))
                        {
                            tiles[tkey] = new Dictionary<string, int>();
                        }

                        if (!EmptyZoned(ref blocks[i], xx, zz))
                        {
                            continue;
                        }

                        t[0]++;
                        bool inFront = xx < depth[zz];
                        if (inFront && depth[zz] == 1)
                        {
                            t[1]++;
                        }

                        if (inFront && narrow)
                        {
                            t[2]++;
                        }

                        // 道の側から続いていない空き(建物の裏の列など)。道に面していないので、建物は建たない(#107 の16回目)
                        if (!inFront)
                        {
                            t[4]++;
                        }

                        var p = CellPosition(ref blocks[i], xx, zz);
                        long key = ((long)Mathf.FloorToInt(p.x / grid) << 32) ^ (uint)Mathf.FloorToInt(p.z / grid);
                        Dictionary<string, int> tile;
                        if (!tiles.TryGetValue(key, out tile))
                        {
                            tile = new Dictionary<string, int>();
                            tiles[key] = tile;
                        }

                        int n;
                        tile.TryGetValue(k, out n);
                        tile[k] = n + 1;
                    }
                }
            }

            var sb = new StringBuilder("{\"ok\":true,\"grid\":").Append((int)grid).Append(",\"byType\":{");
            bool first = true;
            foreach (var kv in total)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(":{\"total\":").Append(kv.Value[3])
                  .Append(",\"empty\":").Append(kv.Value[0]).Append(",\"emptyShallow\":").Append(kv.Value[1])
                  .Append(",\"emptyNarrow\":").Append(kv.Value[2]).Append(",\"emptyBehind\":").Append(kv.Value[4])
                  .Append(",\"emptyFacingRoad\":").Append(kv.Value[0] - kv.Value[4]).Append('}');
                first = false;
            }

            sb.Append("},\"tiles\":[");
            first = true;
            foreach (var kv in tiles)
            {
                int gx = (int)(kv.Key >> 32), gz = (int)(kv.Key & 0xFFFFFFFF);
                sb.Append(first ? "" : ",").Append("{\"x\":").Append(Mathf.RoundToInt((gx + 0.5f) * grid))
                  .Append(",\"z\":").Append(Mathf.RoundToInt((gz + 0.5f) * grid)).Append(",\"empty\":{");
                bool f2 = true;
                foreach (var e in kv.Value)
                {
                    sb.Append(f2 ? "" : ",").Append(Json.Str(e.Key)).Append(':').Append(e.Value);
                    f2 = false;
                }

                sb.Append("}}");
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        private static bool EmptyZoned(ref ZoneBlock b, int xx, int zz)
        {
            if ((b.m_valid & (1UL << (zz << 3 | xx))) == 0 || b.IsOccupied1(xx, zz) || b.IsOccupied2(xx, zz))
            {
                return false;
            }

            var zt = b.GetZone(xx, zz);
            return zt != ItemClass.Zone.Unzoned && zt != ItemClass.Zone.Distant;
        }

        // /zone/cells?x=..&z=..&radius=100  円の中の区画マスを、種類ごとに数える
        private static string ZoneCells(HttpListenerRequest req)
        {
            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r = F(req, "radius", 100f);
            var counts = new Dictionary<string, int>();
            // 種類ごとの空いたマス(建物が建っていないマス)。#82 で市長が「空いたマスを数える道具がない」と書いた
            var empty = new Dictionary<string, int>();
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
                        if (!blocks[i].IsOccupied1(xx, zz) && !blocks[i].IsOccupied2(xx, zz))
                        {
                            int e;
                            empty.TryGetValue(k, out e);
                            empty[k] = e + 1;
                        }
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

            // detail: 種類ごとの全部のマスと、空いたマス。今の cells はそのまま残す
            sb.Append("},\"detail\":{");
            first = true;
            foreach (var kv in counts)
            {
                int e;
                empty.TryGetValue(kv.Key, out e);
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(":{\"total\":").Append(kv.Value)
                  .Append(",\"empty\":").Append(e).Append('}');
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

        // まだ解禁されていない建物か。ゲームの建物の一覧と同じ判定(GeneratedScrollPanel)。
        // #81 では、解禁前の埋立地を市長が置けてしまった
        private static bool IsLocked(BuildingInfo info)
        {
            return !ToolsModifierControl.IsUnlocked(info.GetUnlockMilestone());
        }

        // 解禁の条件。人口の節目なら、その人口
        private static string UnlockJson(BuildingInfo info)
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

        // 道路が要るか。ゲームは PlayerBuildingAI.RequireRoadAccess で決める(ごみを出す、働き手がいる、資源を運ぶ建物)。
        // 風車などは要らない。#82 の試運転で、風車の entrance.road が null で、市長が要らない道路を引きかけた
        private static string NeedsRoadJson(BuildingInfo info)
        {
            var ai = info.m_buildingAI as PlayerBuildingAI;
            return ai == null ? "null" : ai.RequireRoadAccess() ? "true" : "false";
        }

        // 電気・水・下水が要るか(PlayerBuildingAI の消費量が0より大きいか)。
        // #82 の試運転で、給水塔や墓地に電気が要ることが置く前に分からなかった
        private static string NeedsJson(BuildingInfo info)
        {
            var ai = info.m_buildingAI as PlayerBuildingAI;
            bool e = ai != null && ai.m_electricityConsumption > 0;
            bool w = ai != null && ai.m_waterConsumption > 0;
            bool s = ai != null && ai.m_sewageAccumulation > 0;
            return "{\"electricity\":" + (e ? "true" : "false") + ",\"water\":" + (w ? "true" : "false")
                + ",\"sewage\":" + (s ? "true" : "false") + "}";
        }

        // 建物1つが増やす容量。services の capacity と同じ単位(予算100%、働き手がそろったとき)。
        // 換算はゲームと同じ: 電気・水・下水は District.GetElectricityCapacity などが内部の値を16倍して返す。
        // ほかは内部の値のまま(LandfillSiteAI.m_garbageCapacity、HospitalAI.PatientCapacity など)。
        // 分からない種類(焼却場、消防署など)は null。#82 の試運転で、市長は給水塔の効き目を前もって見積もれなかった
        private static string CapacityJson(BuildingInfo info)
        {
            var ai = info.m_buildingAI;
            var pp = ai as PowerPlantAI;
            if (pp != null)
            {
                return "{\"electricity\":" + pp.m_electricityProduction * 16
                    + (ai is WindTurbineAI ? ",\"variesWithWind\":true" : "")
                    + (ai is SolarPowerPlantAI ? ",\"variesWithDaylight\":true" : "") + "}";
            }

            var wf = ai as WaterFacilityAI;
            if (wf != null)
            {
                var parts = new List<string>();
                if (wf.m_waterIntake > 0) parts.Add("\"water\":" + wf.m_waterIntake * 16);
                if (wf.m_sewageOutlet > 0) parts.Add("\"sewage\":" + wf.m_sewageOutlet * 16);
                return parts.Count > 0 ? "{" + string.Join(",", parts.ToArray()) + "}" : "null";
            }

            var lf = ai as LandfillSiteAI;
            if (lf != null)
            {
                // 埋立地だけがたまる容量を持つ。焼却場(m_garbageConsumption > 0)は容量に入らない
                return lf.m_garbageConsumption == 0 ? "{\"garbage\":" + lf.m_garbageCapacity + "}" : "null";
            }

            var h = ai as HospitalAI;
            if (h != null)
            {
                return "{\"healthcare\":" + h.PatientCapacity + "}";
            }

            var c = ai as CemeteryAI;
            if (c != null)
            {
                return c.m_graveCount > 0 ? "{\"deathcare\":" + c.m_graveCount + "}" : "null";
            }

            var ps = ai as PoliceStationAI;
            if (ps != null)
            {
                return "{\"police\":" + ps.JailCapacity + "}";
            }

            var sc = ai as SchoolAI;
            if (sc != null)
            {
                string level = info.m_class.m_level == ItemClass.Level.Level1 ? "elementary"
                    : info.m_class.m_level == ItemClass.Level.Level2 ? "high" : "university";
                return "{\"education\":{\"" + level + "\":" + sc.StudentCount + "}}";
            }

            return "null";
        }

        // 入口の向き(facing)を angle(度)に直す。入口の方位(北0・東90の時計回り)= (360 - angle) % 360。
        // Building.CalculateSidewalkPosition が入口を位置 + (-sin a, cos a) に置くため。#82 の試運転で、
        // 市長は angle を時計回りと思い、ごみ処理場を逆向きに置いた。読めなければ NaN
        internal static float FacingToAngle(string facing)
        {
            string[] names = { "north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest" };
            float bearing;
            int k = Array.IndexOf(names, facing.Trim().ToLowerInvariant());
            if (k >= 0)
            {
                bearing = k * 45f;
            }
            else if (!float.TryParse(facing, NumberStyles.Float, CultureInfo.InvariantCulture, out bearing))
            {
                return float.NaN;
            }

            return ((360f - bearing) % 360f + 360f) % 360f;
        }

        // /building/prefabs?service=Education&locked=false  置ける建物(区画に自然に建つ建物は除く)。
        // 既定では解禁された建物だけ。locked=true で、解禁前の建物も unlocked=false と条件つきで返す
        private static string BuildingPrefabs(HttpListenerRequest req)
        {
            string service = req.QueryString["service"];
            bool withLocked = req.QueryString["locked"] == "true";
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

                // ゲームの建物の一覧と同じく、手で置く建物だけにする。橋脚や建物の部品(Sub)を外す
                if (info.m_placementStyle != ItemClass.Placement.Manual
                    || (info.m_availableIn & ItemClass.Availability.Game) == 0)
                {
                    continue;
                }

                bool locked = IsLocked(info);
                if (locked && !withLocked)
                {
                    continue;
                }

                sb.Append(first ? "" : ",").Append("{\"name\":").Append(Json.Str(info.name))
                  .Append(",\"unlocked\":").Append(locked ? "false" : "true");
                if (locked)
                {
                    sb.Append(",\"unlock\":").Append(UnlockJson(info));
                }

                sb
                  .Append(",\"service\":").Append(Json.Str(info.m_class.m_service.ToString()))
                  .Append(",\"subService\":").Append(Json.Str(info.m_class.m_subService.ToString()))
                  .Append(",\"width\":").Append(info.m_cellWidth).Append(",\"length\":").Append(info.m_cellLength)
                  .Append(",\"cost\":").Append(info.GetConstructionCost() / 100)
                  .Append(",\"upkeepPerWeek\":").Append(Money.PerWeek(info.GetMaintenanceCost()))
                  .Append(",\"capacity\":").Append(CapacityJson(info))
                  .Append(",\"needsRoad\":").Append(NeedsRoadJson(info))
                  .Append(",\"needs\":").Append(NeedsJson(info))
                  .Append(",\"ports\":").Append(MapApi.PrefabPortsJson(info)).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // /building/place?prefab=..&x=..&z=..&facing=south&pay=true
        // facing は入口の向き(north / east / ... / northwest、または北0・東90の時計回りの度)。
        // angle(度)も受け付ける。angle は反時計回りで、入口の方位 = (360 - angle) % 360(0で入口が北)。
        // 以前の説明の「0で正面が南」は誤り(#82)
        private static string PlaceBuilding(HttpListenerRequest req)
        {
            string name = req.QueryString["prefab"];
            var info = PrefabCollection<BuildingInfo>.FindLoaded(name);
            if (info == null)
            {
                return HttpBridge.Error("prefab not found: " + name + " (see /building/prefabs)");
            }

            bool pay = req.QueryString["pay"] != "false";
            // test=true なら、置けるかを確かめて、置かずに返す(#105。局と市長が、建てる前に試す。ゲームの道具の、置く前の赤い表示に当たる)
            bool test = req.QueryString["test"] == "true";
            var assumed = test ? Assumed.Parse(req) : null;
            // 人が置く骨格(pay=false)は、解禁を問わない
            if (pay && IsLocked(info))
            {
                return "{\"ok\":false,\"error\":\"this building is not unlocked yet\",\"unlock\":" + UnlockJson(info) + "}";
            }

            var pos = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            pos.y = TerrainManager.instance.SampleRawHeightSmooth(pos);
            float angleDeg = F(req, "angle", 0f);
            string facing = req.QueryString["facing"];
            if (!string.IsNullOrEmpty(facing))
            {
                angleDeg = FacingToAngle(facing);
                if (float.IsNaN(angleDeg))
                {
                    return HttpBridge.Error("bad facing: " + facing + " (north / northeast / east / ... / northwest, or degrees clockwise from north)");
                }
            }

            float angle = angleDeg * Mathf.Deg2Rad;
            int cost = info.GetConstructionCost();

            var eco = EconomyManager.instance;
            if (pay && !test)
            {
                if (eco.PeekResource(EconomyManager.Resource.Construction, cost) != cost)
                {
                    return "{\"ok\":false,\"error\":\"not enough money\",\"cost\":" + cost / 100 + ",\"money\":" + eco.LastCashAmount / 100 + "}";
                }
            }

            var sim = SimulationManager.instance;
            Randomizer rnd = sim.m_randomizer;
            ushort id = 0;
            // 敷地が重なる区画の建物。ゲームは重なった区画の建物を取り壊す(#82。市長は何棟壊れたか分からなかった)
            var overlapped = OverlappingZoned(info, pos, angle);
            if (pay || test)
            {
                // ゲームの建物の道具と同じ判定で、置ける場所かを調べる(#105)。前は判定を通さずに置いたので、
                // 道路やサービスの建物に重なる場所など、人には置けない場所にも置けた。
                // 建物の型が位置と向きを直すことがある(岸に置く建物など)。試しの判定(test=true)は、
                // 取り除けない相手(道路、サービスの建物など)にぶつかるときだけ断る。区画の建物は本番で取り壊す
                float minY, maxY, buildingY;
                Building.SampleBuildingHeight(pos, angle, info.m_cellWidth, info.m_cellLength, info, out minY, out maxY, out buildingY);
                pos.y = buildingY;
                var seg = default(ColossalFramework.Math.Segment3);
                int productionRate, constructionCost;
                var posErrors = info.m_buildingAI.CheckBuildPosition(0, ref pos, ref angle, 0f, 0f, ref seg, out productionRate, out constructionCost);
                Building.SampleBuildingHeight(pos, angle, info.m_cellWidth, info.m_cellLength, info, out minY, out maxY, out buildingY);
                var segBuf = new ulong[(NetManager.instance.m_segments.m_buffer.Length + 63) >> 6];
                var bldBuf = new ulong[(BuildingManager.instance.m_buildings.m_buffer.Length + 63) >> 6];
                var spaceErrors = BuildingTool.CheckSpace(info, info.m_placementMode, 0, pos, minY, buildingY + info.m_collisionHeight, angle,
                    info.m_cellWidth, info.m_cellLength, true, segBuf, bldBuf);
                bool blocking;
                string coll = UpgradeApi.CollidingJson(segBuf, bldBuf, assumed, out blocking);
                // 試しで、断る相手がすべて「壊したもの」なら、ぶつからないとみなす(#105。壊してから建てる工事を試す)
                if (assumed != null && assumed.Any && !blocking)
                {
                    spaceErrors &= ~ToolBase.ToolErrors.ObjectCollision;
                }

                if ((posErrors | spaceErrors) != ToolBase.ToolErrors.None)
                {
                    return "{\"ok\":false,\"error\":\"cannot place here\",\"reasons\":" + Json.Str((posErrors | spaceErrors).ToString())
                        + ",\"positionReasons\":" + Json.Str(posErrors.ToString()) + ",\"spaceReasons\":" + Json.Str(spaceErrors.ToString())
                        + ",\"colliding\":" + coll + "}";
                }

                // 本番: ゲームの道具と同じく、取り除ける相手(区画の建物など)を取り除いてから置く
                overlapped = new List<ushort>();
                foreach (int b in UpgradeApi.Bits(bldBuf))
                {
                    var bi = BuildingManager.instance.m_buildings.m_buffer[b].Info;
                    if (bi != null && !bi.IgnoreBuildingCollision() && !(assumed != null && assumed.RemovedBuilding(b)))
                    {
                        overlapped.Add((ushort)b);
                    }
                }

                angleDeg = angle * Mathf.Rad2Deg;
                if (test)
                {
                    return "{\"ok\":true,\"test\":true,\"placed\":false,\"prefab\":" + Json.Str(name) + ",\"x\":" + Mathf.RoundToInt(pos.x)
                        + ",\"z\":" + Mathf.RoundToInt(pos.z) + ",\"angleUsed\":" + N(angleDeg) + ",\"cost\":" + cost / 100
                        + ",\"enoughMoney\":" + (eco.LastCashAmount >= cost ? "true" : "false") + ",\"needsRoad\":" + NeedsRoadJson(info)
                        + ",\"needs\":" + NeedsJson(info) + ",\"entrance\":" + Entrance(pos, angle, info.m_cellLength)
                        + ",\"wouldDemolish\":" + DemolishedJson(overlapped) + "}";
                }

                Array.Clear(segBuf, 0, segBuf.Length);
                Array.Clear(bldBuf, 0, bldBuf.Length);
                BuildingTool.CheckSpace(info, info.m_placementMode, 0, pos, minY, buildingY + info.m_collisionHeight, angle,
                    info.m_cellWidth, info.m_cellLength, false, segBuf, bldBuf);
            }

            if (!BuildingManager.instance.CreateBuilding(out id, ref rnd, info, pos, angle, info.m_cellLength, sim.m_currentBuildIndex))
            {
                return HttpBridge.Error("CreateBuilding failed");
            }

            sim.m_currentBuildIndex++;
            if (pay)
            {
                eco.FetchResource(EconomyManager.Resource.Construction, cost, info.m_class);
            }

            // 道路が要るのに入口の前に道路がなければ、置いた上で知らせる(#82。市長が処理場を逆向きに置き、取り壊して置き直した)
            string entrance = Entrance(id);
            string needsRoad = NeedsRoadJson(info);
            string warning = needsRoad == "true" && entrance.Contains("\"road\":null")
                ? ",\"warning\":\"no road at the entrance. Turn it (facing) or build a road in front\"" : "";
            return "{\"ok\":true,\"id\":" + id + ",\"prefab\":" + Json.Str(name) + ",\"cost\":" + cost / 100
                + ",\"paid\":" + (pay ? "true" : "false") + ",\"angleUsed\":" + N(angleDeg)
                + ",\"entrance\":" + entrance + ",\"needsRoad\":" + needsRoad + ",\"needs\":" + NeedsJson(info)
                + ",\"ports\":" + MapApi.PortsJson(id) + warning + ",\"demolished\":" + DemolishedJson(overlapped) + "}";
        }

        // 敷地(回した長方形)が新しい建物の敷地と重なる区画の建物(PrivateBuildingAI)。2つの長方形の分離軸で判定する
        private static List<ushort> OverlappingZoned(BuildingInfo info, Vector3 pos, float angle)
        {
            var hit = new List<ushort>();
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            float reach = (info.m_cellWidth + info.m_cellLength) * 8f + 64f;
            for (int i = 1; i < bs.Length; i++)
            {
                var o = bs[i].Info;
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || (bs[i].m_flags & Building.Flags.Deleted) != 0 || o == null
                    || !(o.m_buildingAI is PrivateBuildingAI) || bs[i].m_parentBuilding != 0)
                {
                    continue;
                }

                var d = bs[i].m_position - pos;
                if (d.x * d.x + d.z * d.z > reach * reach)
                {
                    continue;
                }

                // 境目で接するだけの隣の建物を数えないよう、1m 内側で判定する
                if (RectsOverlap(pos, angle, info.m_cellWidth * 4f - 1f, info.m_cellLength * 4f - 1f,
                        bs[i].m_position, bs[i].m_angle, bs[i].Width * 4f - 1f, bs[i].Length * 4f - 1f))
                {
                    hit.Add((ushort)i);
                }
            }

            return hit;
        }

        // 回した長方形の重なり(水平面)。右の向きは (cos a, sin a)、前の向きは (−sin a, cos a)(NetApi.BuildingAt と同じ)
        private static bool RectsOverlap(Vector3 p1, float a1, float w1, float l1, Vector3 p2, float a2, float w2, float l2)
        {
            var axes = new[]
            {
                new Vector2(Mathf.Cos(a1), Mathf.Sin(a1)), new Vector2(-Mathf.Sin(a1), Mathf.Cos(a1)),
                new Vector2(Mathf.Cos(a2), Mathf.Sin(a2)), new Vector2(-Mathf.Sin(a2), Mathf.Cos(a2)),
            };
            var d = new Vector2(p2.x - p1.x, p2.z - p1.z);
            foreach (var ax in axes)
            {
                float r1 = w1 * Mathf.Abs(Vector2.Dot(axes[0], ax)) + l1 * Mathf.Abs(Vector2.Dot(axes[1], ax));
                float r2 = w2 * Mathf.Abs(Vector2.Dot(axes[2], ax)) + l2 * Mathf.Abs(Vector2.Dot(axes[3], ax));
                if (Mathf.Abs(Vector2.Dot(d, ax)) > r1 + r2)
                {
                    return false;
                }
            }

            return true;
        }

        // 重なった区画の建物。count は数、ids は最大20、removedNow は置いた直後にもう消えていた数(残りはゲームが後で取り壊す)
        private static string DemolishedJson(List<ushort> ids)
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            int removed = 0;
            var sb = new StringBuilder("{\"count\":").Append(ids.Count).Append(",\"ids\":[");
            for (int k = 0; k < ids.Count; k++)
            {
                if ((bs[ids[k]].m_flags & Building.Flags.Created) == 0 || (bs[ids[k]].m_flags & Building.Flags.Deleted) != 0)
                {
                    removed++;
                }

                if (k < 20)
                {
                    sb.Append(k == 0 ? "" : ",").Append(ids[k]);
                }
            }

            return sb.Append("],\"removedNow\":").Append(removed).Append('}').ToString();
        }

        // 置いた建物の入口(正面の歩道の位置)、正面の向き、入口のそばの道路。
        // #81 の市長は angle とどの面が正面かの対応が分からず、ごみ処理場を道路に向けられなかった
        private static string Entrance(ushort id)
        {
            var b = BuildingManager.instance.m_buildings.m_buffer[id];
            return Entrance(b.m_position, b.m_angle, b.Length);
        }

        // 置く前の建物の入口(Building.CalculateSidewalkPosition と同じ計算)。試し(test=true)で使う
        private static string Entrance(Vector3 position, float angle, int length)
        {
            var door = Building.CalculateSidewalkPosition(position, angle, length);
            var dir = door - position;
            // 方位は北が0、東が90(時計回り)
            float bearing = (Mathf.Atan2(dir.x, dir.z) * Mathf.Rad2Deg + 360f) % 360f;
            string[] names = { "north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest" };
            string facing = names[Mathf.RoundToInt(bearing / 45f) % 8];

            // 入口から16m以内でいちばん近い道路。ゲームが建物に道路を割り当てるのは時間を進めた後なので、ここで先に見る
            var nets = NetManager.instance;
            ushort best = 0;
            float bestDist = 16f;
            for (int i = 1; i < nets.m_segments.m_size; i++)
            {
                var seg = nets.m_segments.m_buffer[i];
                if ((seg.m_flags & NetSegment.Flags.Created) == 0 || seg.Info == null
                    || seg.Info.m_class.m_service != ItemClass.Service.Road)
                {
                    continue;
                }

                var p = seg.GetClosestPosition(door);
                float d = new Vector2(p.x - door.x, p.z - door.z).magnitude - seg.Info.m_halfWidth;
                if (d < bestDist)
                {
                    bestDist = d;
                    best = (ushort)i;
                }
            }

            var sb = new StringBuilder("{\"x\":").Append(N(door.x)).Append(",\"z\":").Append(N(door.z))
                .Append(",\"facing\":").Append(Json.Str(facing)).Append(",\"bearing\":").Append(Mathf.RoundToInt(bearing))
                .Append(",\"road\":");
            if (best == 0)
            {
                sb.Append("null");
            }
            else
            {
                var seg = nets.m_segments.m_buffer[best];
                sb.Append("{\"segment\":").Append(best).Append(",\"prefab\":").Append(Json.Str(seg.Info.name))
                  .Append(",\"distance\":").Append(N(Mathf.Max(0f, bestDist))).Append('}');
            }

            return sb.Append('}').ToString();
        }

        // /buildings?x=..&z=..&radius=200&limit=50  円の中の建物の一覧
        private static string BuildingsNear(HttpListenerRequest req)
        {
            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r2 = F(req, "radius", 200f);
            r2 *= r2;
            int limit = I(req, "limit", 50);
            // 困りごとの印で絞る(#82)。半径350で約3,200棟になり、市長が印のある建物を探せなかった
            bool problemsOnly = req.QueryString["problems_only"] == "true";
            string problemName = req.QueryString["problem"];
            // service=FireDepartment などで、サービスの建物を種類で絞る(#82 の48か月目。消防署の場所を探せなかった)
            string serviceName = req.QueryString["service"];
            // abandoned=true で、放棄・倒壊・焼け跡など、取り壊すしかない建物だけに絞る(#82。市長は bulldoze を57回呼んで探した)
            bool abandonedOnly = req.QueryString["abandoned"] == "true";
            // brief=true で、1棟を id・種類・位置・印だけの短い形にする(#82。街全体を limit 200 で呼ぶと67KBで読めなかった)
            bool brief = req.QueryString["brief"] == "true";
            Notification.Problem1 wanted = Notification.Problem1.None;
            if (!string.IsNullOrEmpty(problemName))
            {
                try
                {
                    wanted = (Notification.Problem1)Enum.Parse(typeof(Notification.Problem1), problemName, true);
                }
                catch (ArgumentException)
                {
                    return HttpBridge.Error("unknown problem: " + problemName + " (use a type name from /complaints, e.g. Garbage)");
                }
            }

            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("{\"ok\":true,\"buildings\":[");
            int count = 0, total = 0;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null || MapApi.IsNetPart(ref bs[i]))
                {
                    continue;
                }

                var d = bs[i].m_position - c;
                d.y = 0f;
                if (d.sqrMagnitude > r2)
                {
                    continue;
                }

                if (!string.IsNullOrEmpty(serviceName) && !string.Equals(bs[i].Info.m_class.m_service.ToString(), serviceName, StringComparison.OrdinalIgnoreCase))
                {
                    continue;
                }

                Notification.Problem1 problems = bs[i].m_problems;
                if ((problemsOnly && bs[i].m_problems.IsNone) || (wanted != Notification.Problem1.None && (problems & wanted) == 0))
                {
                    continue;
                }

                if (abandonedOnly && !IsWreck(ref bs[i]))
                {
                    continue;
                }

                total++;
                if (count >= limit)
                {
                    continue;
                }

                var info = bs[i].Info;
                if (brief)
                {
                    sb.Append(count == 0 ? "" : ",").Append("{\"id\":").Append(i)
                      .Append(",\"prefab\":").Append(Json.Str(info.name))
                      .Append(",\"x\":").Append(N(bs[i].m_position.x)).Append(",\"z\":").Append(N(bs[i].m_position.z))
                      .Append(",\"problems\":").Append(Json.Str(bs[i].m_problems.ToString())).Append('}');
                    count++;
                    continue;
                }

                sb.Append(count == 0 ? "" : ",").Append("{\"id\":").Append(i)
                  .Append(",\"prefab\":").Append(Json.Str(info.name))
                  .Append(",\"service\":").Append(Json.Str(info.m_class.m_service.ToString()))
                  .Append(",\"x\":").Append(N(bs[i].m_position.x)).Append(",\"z\":").Append(N(bs[i].m_position.z))
                  .Append(",\"abandoned\":").Append((bs[i].m_flags & Building.Flags.Abandoned) != 0 ? "true" : "false")
                  .Append(",\"problems\":").Append(Json.Str(bs[i].m_problems.ToString()))
                  .Append(",\"grid\":").Append(MapApi.GridJson(ref bs[i]))
                  .Append(",\"ports\":").Append(MapApi.PortsJson((ushort)i))
                  .Append(DetailJson((ushort)i, ref bs[i])).Append('}');
                count++;
            }

            return sb.Append("],\"total\":").Append(total).Append('}').ToString();
        }

        // 取り壊すしかない建物か。放棄(Abandoned)、倒壊(Collapsed)、焼け跡(火事の印が FatalProblem のもの。燃えている途中は MajorProblem)
        private static bool IsWreck(ref Building b)
        {
            if ((b.m_flags & (Building.Flags.Abandoned | Building.Flags.Collapsed)) != 0)
            {
                return true;
            }

            Notification.Problem1 p = b.m_problems;
            return (p & Notification.Problem1.Fire) != 0 && (p & Notification.Problem1.FatalProblem) != 0;
        }

        // 建物の画面と同じ値(#82)。働き口と働き手、家族、車、たまり具合。
        // 市長が「建物ごとの働き口が分からない」「収集車が足りないのか処理場が満杯なのか見分けられない」と書いたため
        private static string DetailJson(ushort id, ref Building b)
        {
            var info = b.Info;
            var ai = info.m_buildingAI;
            var sb = new StringBuilder();
            bool broken = (b.m_flags & (Building.Flags.Abandoned | Building.Flags.Collapsed)) != 0;

            // 働き口の数(ゲームの建物の画面と同じ計算。区画の建物は CalculateWorkplaceCount と AdjustWorkplaceCount、
            // サービスの建物は CountWorkPlaces)
            int jobs = 0;
            var pai = ai as PrivateBuildingAI;
            var player = ai as PlayerBuildingAI;
            if (pai != null && !broken)
            {
                int l0, l1, l2, l3;
                pai.CalculateWorkplaceCount((ItemClass.Level)b.m_level, new Randomizer(id), b.Width, b.Length, out l0, out l1, out l2, out l3);
                pai.AdjustWorkplaceCount(id, ref b, ref l0, ref l1, ref l2, ref l3);
                jobs = l0 + l1 + l2 + l3;
            }
            else if (player != null)
            {
                int l0, l1, l2, l3;
                player.CountWorkPlaces(out l0, out l1, out l2, out l3);
                jobs = l0 + l1 + l2 + l3;
            }

            // 働き手と家族は、建物の市民の単位(CitizenUnit)を数える。亡くなった人と引っ越しの途中の人は除く(画面と同じ)
            var cm = CitizenManager.instance;
            int workers = 0, households = 0, dead = 0;
            uint unit = b.m_citizenUnits;
            int guard = 0;
            while (unit != 0 && guard++ < 524288)
            {
                var u = cm.m_units.m_buffer[unit];
                bool home = (u.m_flags & CitizenUnit.Flags.Home) != 0;
                bool work = (u.m_flags & CitizenUnit.Flags.Work) != 0;
                bool visit = (u.m_flags & CitizenUnit.Flags.Visit) != 0;
                bool anyone = false;
                for (int k = 0; k < 5; k++)
                {
                    uint ci = u.GetCitizen(k);
                    if (ci == 0)
                    {
                        continue;
                    }

                    var c = cm.m_citizens.m_buffer[ci];
                    if (visit && c.Dead && c.CurrentLocation == Citizen.Location.Visit)
                    {
                        dead++;
                    }

                    if (c.Dead || (c.m_flags & Citizen.Flags.MovingIn) != 0)
                    {
                        continue;
                    }

                    if (work)
                    {
                        workers++;
                    }

                    anyone = true;
                }

                if (home && anyone)
                {
                    households++;
                }

                unit = u.m_nextUnit;
            }

            if (jobs > 0 || workers > 0)
            {
                sb.Append(",\"jobs\":{\"total\":").Append(jobs).Append(",\"workers\":").Append(workers).Append('}');
            }

            if (pai != null && info.m_class.m_service == ItemClass.Service.Residential && !broken)
            {
                int homes = pai.CalculateHomeCount((ItemClass.Level)b.m_level, new Randomizer(id), b.Width, b.Length);
                sb.Append(",\"homes\":{\"total\":").Append(homes).Append(",\"occupied\":").Append(households).Append('}');
            }

            if (player == null)
            {
                return sb.ToString();
            }

            // 車: 建物が持つ車の並び(m_ownVehicles)を数える。全部の台数はゲームの画面の文(stats)にある
            int inUse = 0;
            ushort v = b.m_ownVehicles;
            guard = 0;
            var vs = VehicleManager.instance.m_vehicles.m_buffer;
            while (v != 0 && guard++ < 16384)
            {
                inUse++;
                v = vs[v].m_nextOwnVehicle;
            }

            sb.Append(",\"vehicles\":{\"inUse\":").Append(inUse).Append('}');

            // たまり具合: 埋立地(焼却場は m_garbageConsumption > 0 で、たまり具合ではなく処理の量)と墓地
            var landfill = ai as LandfillSiteAI;
            var cemetery = ai as CemeteryAI;
            if (landfill != null && landfill.m_garbageCapacity > 0)
            {
                int amount = landfill.GetGarbageAmount(id, ref b);
                sb.Append(",\"storage\":{\"amount\":").Append(amount).Append(",\"capacity\":").Append(landfill.m_garbageCapacity)
                  .Append(",\"percent\":").Append(amount * 100 / landfill.m_garbageCapacity).Append('}');
            }
            else if (cemetery != null && cemetery.m_graveCount > 0)
            {
                sb.Append(",\"storage\":{\"amount\":").Append(dead).Append(",\"capacity\":").Append(cemetery.m_graveCount)
                  .Append(",\"percent\":").Append(dead * 100 / cemetery.m_graveCount).Append('}');
            }

            // ゲームの建物の画面の文(「使用中の収集車 3/7」など)。全部の台数や処理の量はここで読む
            string stats = null;
            try
            {
                stats = ai.GetLocalizedStats(id, ref b);
            }
            catch (Exception)
            {
                stats = null;
            }

            if (!string.IsNullOrEmpty(stats))
            {
                var lines = stats.Split(new[] { '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
                sb.Append(",\"stats\":[");
                for (int k = 0; k < lines.Length; k++)
                {
                    sb.Append(k > 0 ? "," : "").Append(Json.Str(lines[k].Trim()));
                }

                sb.Append(']');
            }

            return sb.ToString();
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

            // turbo: 速度3のときに1回の計算で進めるコマの数(4〜16。4がゲームの既定)。Harmony がないと効かない
            if (req.QueryString["turbo"] != null)
            {
                SetTurbo(Mathf.Clamp(I(req, "turbo", 4), 4, 16));
            }

            string paused = req.QueryString["paused"];
            if (paused != null)
            {
                sim.SimulationPaused = paused == "true";
            }

            return "{\"ok\":true,\"paused\":" + (sim.SimulationPaused ? "true" : "false") + ",\"speed\":" + sim.SelectedSimulationSpeed
                + ",\"turbo\":" + GetTurbo()
                + ",\"date\":" + Json.Str(sim.m_currentGameTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)) + "}";
        }

        // Patcher(HarmonyLib を使う)には、Harmony が読めたときだけ触る
        private static void SetTurbo(int v)
        {
            if (DialogWatch.HooksActive)
            {
                Patcher.Turbo = v;
            }
        }

        private static int GetTurbo()
        {
            return DialogWatch.HooksActive ? Patcher.Turbo : 4;
        }

        // ---- 需要の内訳 ----

        // /demand  住宅・働き口の需要を、ゲームの計算(ZoneManager.CalculateResidentialDemand など)と同じ項に分けて返す。
        // #82 の育てる期間で、住宅の需要が1年以上0のまま、理由を確かめる道具がなかった
        private static string Demand()
        {
            var d = DistrictManager.instance.m_districts.m_buffer[0];
            long jobs = d.m_commercialData.m_finalHomeOrWorkCount + d.m_industrialData.m_finalHomeOrWorkCount
                + d.m_officeData.m_finalHomeOrWorkCount + d.m_playerData.m_finalHomeOrWorkCount;
            long emptyJobs = d.m_commercialData.m_finalEmptyCount + d.m_industrialData.m_finalEmptyCount
                + d.m_officeData.m_finalEmptyCount + d.m_playerData.m_finalEmptyCount;
            long homes = d.m_residentialData.m_finalHomeOrWorkCount;
            long emptyHomes = d.m_residentialData.m_finalEmptyCount;
            var edu = new[] { d.m_educated0Data, d.m_educated1Data, d.m_educated2Data, d.m_educated3Data };
            long unemployed = 0, homeless = 0;
            var sb = new StringBuilder("{\"ok\":true,\"byEducation\":[");
            string[] names = { "uneducated", "elementary", "highSchool", "university" };
            for (int i = 0; i < 4; i++)
            {
                unemployed += edu[i].m_finalUnemployed;
                homeless += edu[i].m_finalHomeless;
                sb.Append(i > 0 ? "," : "").Append("{\"education\":").Append(Json.Str(names[i]))
                  .Append(",\"unemployed\":").Append(edu[i].m_finalUnemployed)
                  .Append(",\"eligibleWorkers\":").Append(edu[i].m_finalEligibleWorkers)
                  .Append(",\"homeless\":").Append(edu[i].m_finalHomeless).Append('}');
            }

            // 住宅の需要 = 基本(50〜100) + 働き口の項(-50〜50) + 家の項(-50〜50)
            int baseTerm = Mathf.Clamp(100 - (int)homes, 50, 100);
            int jobTerm = Mathf.Clamp((int)((emptyJobs * 200 - unemployed * 200) / Math.Max(jobs, 100)), -50, 50);
            int homeTerm = Mathf.Clamp((int)((homeless * 200 - emptyHomes * 200) / Math.Max(homes, 100)), -50, 50);
            int occupied = (int)(homes - emptyHomes);
            int wBase = Mathf.Clamp(occupied, 0, 50);
            int wJob = Mathf.Clamp((int)((unemployed * 200 - emptyJobs * 200) / Math.Max(jobs, 100)), -50, 50);
            sb.Append("],\"jobs\":").Append(jobs).Append(",\"emptyJobs\":").Append(emptyJobs)
              .Append(",\"homes\":").Append(homes).Append(",\"emptyHomes\":").Append(emptyHomes)
              .Append(",\"unemployed\":").Append(unemployed).Append(",\"homeless\":").Append(homeless)
              .Append(",\"residential\":{\"actual\":").Append(ZoneManager.instance.m_residentialDemand)
              .Append(",\"base\":").Append(baseTerm).Append(",\"jobTerm\":").Append(jobTerm).Append(",\"homeTerm\":").Append(homeTerm)
              // 下限・上限で切る前の値。切れていると、施策で近づいているかが見えないため(#82 の g37〜g42)
              .Append(",\"jobTermRaw\":").Append((emptyJobs * 200 - unemployed * 200) / Math.Max(jobs, 100))
              .Append(",\"homeTermRaw\":").Append((homeless * 200 - emptyHomes * 200) / Math.Max(homes, 100))
              .Append(",\"target\":").Append(Mathf.Clamp(baseTerm + jobTerm + homeTerm, 0, 100)).Append('}')
              .Append(",\"workplace\":{\"actual\":").Append(ZoneManager.instance.m_workplaceDemand)
              .Append(",\"base\":").Append(wBase).Append(",\"jobTerm\":").Append(wJob)
              .Append(",\"target\":").Append(Mathf.Clamp(wBase + wJob, 0, 100)).Append('}');
            return sb.Append('}').ToString();
        }

        // ---- 出来事 ----

        // /events  前回から増えたつぶやき(市民の声、節目、警告など)
        private static string Events()
        {
            LoadSeen();
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

            SaveSeen(msgs);
            return sb.Append("]}").ToString();
        }

        // 既読の印をファイルに残す(#82。ゲームを再起動すると、最初の events で前に読んだつぶやきまで返った)。
        // 残すのは、今ゲームが持っている最近のつぶやきの分だけ(古いものはゲームの一覧から消えるので要らない)
        private static readonly string SeenFile = System.IO.Path.Combine(
            System.IO.Path.GetDirectoryName(CommandLog.LogDir), "events-seen.txt");

        private static bool seenLoaded;

        private static void LoadSeen()
        {
            if (seenLoaded)
            {
                return;
            }

            seenLoaded = true;
            try
            {
                if (System.IO.File.Exists(SeenFile))
                {
                    foreach (var line in System.IO.File.ReadAllLines(SeenFile))
                    {
                        if (line.Length > 0)
                        {
                            seenMessages.Add(line.Replace("\\n", "\n"));
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Debug.Log("[AIMayor] events seen load: " + e.Message);
            }
        }

        private static void SaveSeen(MessageBase[] msgs)
        {
            try
            {
                var lines = new List<string>();
                if (msgs != null)
                {
                    foreach (var m in msgs)
                    {
                        var cm = m as IChirperMessage;
                        if (cm != null)
                        {
                            lines.Add((cm.senderID + "|" + cm.text).Replace("\n", "\\n"));
                        }
                    }
                }

                System.IO.File.WriteAllLines(SeenFile, lines.ToArray());
            }
            catch (Exception e)
            {
                Debug.Log("[AIMayor] events seen save: " + e.Message);
            }
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
