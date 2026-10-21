using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using ColossalFramework.Math;
using UnityEngine;

namespace AIMayor
{
    // 区画の建物のレベル、レベルが上がらない理由、地価、新しく建った建物の数を返す(#82)。
    // 育てる期間に「建物のレベルを上げる手が効いたか」を確かめる道具がなかったため。
    //
    // レベルが上がる条件はゲームの CheckBuildingLevel(ResidentialBuildingAI など)と同じ。
    // Building.m_levelUpProgress の下4ビットと上4ビットに、2つの条件の進み具合(1〜15)が入る。15 で満たした。
    // - 住宅: 下 = 住民の学歴、上 = 地価
    // - 商業: 下 = 客の豊かさ、上 = 地価
    // - 工業・オフィス: 下 = 働き手の学歴、上 = サービスの届き具合
    public static class BuildingStatsApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/buildings/stats"] = req => HttpBridge.OnMain(() => Stats(req));
            routes["/landvalue"] = req => HttpBridge.OnMain(() => LandValue(req));
            routes["/buildings/new"] = req => HttpBridge.OnMain(() => NewBuildings(req));
            routes["/buildings/levelup"] = req => HttpBridge.OnMain(() => LevelUp(req));
        }

        private class Group
        {
            public int Buildings, Abandoned, Homes, Jobs, Ready, LowFirst, LowSecond;
            public long LandValue;
            // ready なのに上がらない理由(問題の印がある、同じ大きさの上のレベルの建物がない)
            public int ReadyBlockedByProblems, ReadyNoUpgradeModel;
            // サービスで止まっている工業・オフィスの、いちばん足りない項目ごとの棟数
            public readonly Dictionary<string, int> MissingService = new Dictionary<string, int>();
            public readonly int[] Levels = new int[5];
        }

        // /buildings/stats?x=..&z=..&radius=..  区画の建物を種類ごとに数える。x を省くと街全体
        private static string Stats(HttpListenerRequest req)
        {
            bool area = req.QueryString["x"] != null;
            var c = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            float r = F(req, "radius", 500f);
            var groups = new SortedDictionary<string, Group>();
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int i = 1; i < bs.Length; i++)
            {
                var flags = bs[i].m_flags;
                var info = bs[i].Info;
                if ((flags & Building.Flags.Created) == 0 || (flags & Building.Flags.Deleted) != 0 || info == null
                    || !(info.m_buildingAI is PrivateBuildingAI) || bs[i].m_parentBuilding != 0)
                {
                    continue;
                }

                if (area)
                {
                    var d = bs[i].m_position - c;
                    if (d.x * d.x + d.z * d.z > r * r)
                    {
                        continue;
                    }
                }

                string key = info.m_class.m_subService.ToString();
                Group g;
                if (!groups.TryGetValue(key, out g))
                {
                    g = new Group();
                    groups[key] = g;
                }

                g.Buildings++;
                if ((flags & Building.Flags.Abandoned) != 0)
                {
                    g.Abandoned++;
                    continue;
                }

                g.Levels[Mathf.Clamp(bs[i].m_level, 0, 4)]++;
                var ai = (PrivateBuildingAI)info.m_buildingAI;
                var rnd = new Randomizer(i);
                g.Homes += ai.CalculateHomeCount((ItemClass.Level)bs[i].m_level, rnd, bs[i].Width, bs[i].Length);
                int l0, l1, l2, l3;
                ai.CalculateWorkplaceCount((ItemClass.Level)bs[i].m_level, new Randomizer(i), bs[i].Width, bs[i].Length, out l0, out l1, out l2, out l3);
                g.Jobs += l0 + l1 + l2 + l3;
                int local;
                ImmaterialResourceManager.instance.CheckLocalResource(ImmaterialResourceManager.Resource.LandValue, bs[i].m_position, out local);
                g.LandValue += local;

                // レベルが上がらない理由。最上位でない建物で、2つの条件のうち低い方を数える
                int first = bs[i].m_levelUpProgress & 0xF;
                int second = bs[i].m_levelUpProgress >> 4;
                if (first == 15 && second == 15)
                {
                    // 上のレベルを満たしているのに上がっていない。ゲームは問題の印がないことと、
                    // 同じ大きさの上のレベルの建物があることを、建て替えの条件にしている(CheckBuildingLevel)
                    g.Ready++;
                    if (!bs[i].m_problems.IsNone)
                    {
                        g.ReadyBlockedByProblems++;
                    }
                    else if (ai.GetUpgradeInfo((ushort)i, ref bs[i]) == null)
                    {
                        g.ReadyNoUpgradeModel++;
                    }
                }
                else if (first != 0 || second != 0)
                {
                    if (first <= second)
                    {
                        g.LowFirst++;
                    }
                    else
                    {
                        g.LowSecond++;
                        var terms = ServiceTerms(bs[i].m_position, info.m_class.m_service);
                        if (terms != null)
                        {
                            string worst = WorstTerm(terms);
                            int seen;
                            g.MissingService.TryGetValue(worst, out seen);
                            g.MissingService[worst] = seen + 1;
                        }
                    }
                }
            }

            var sb = new StringBuilder("{\"ok\":true,\"groups\":[");
            bool firstGroup = true;
            foreach (var kv in groups)
            {
                var g = kv.Value;
                int alive = g.Buildings - g.Abandoned;
                string[] names = Names(kv.Key);
                sb.Append(firstGroup ? "" : ",").Append("{\"subService\":").Append(Json.Str(kv.Key))
                  .Append(",\"buildings\":").Append(g.Buildings).Append(",\"abandoned\":").Append(g.Abandoned)
                  .Append(",\"levels\":[").Append(string.Join(",", Array.ConvertAll(g.Levels, v => v.ToString(CultureInfo.InvariantCulture)))).Append(']')
                  .Append(",\"homes\":").Append(g.Homes).Append(",\"jobs\":").Append(g.Jobs)
                  .Append(",\"averageLandValue\":").Append(alive > 0 ? g.LandValue / alive : 0)
                  .Append(",\"levelUp\":{\"ready\":").Append(g.Ready)
                  .Append(",").Append(Json.Str("limitedBy_" + names[0])).Append(':').Append(g.LowFirst)
                  .Append(",").Append(Json.Str("limitedBy_" + names[1])).Append(':').Append(g.LowSecond)
                  .Append(",\"readyBlockedByProblems\":").Append(g.ReadyBlockedByProblems)
                  .Append(",\"readyNoUpgradeModel\":").Append(g.ReadyNoUpgradeModel);
                if (g.MissingService.Count > 0)
                {
                    var list = new List<KeyValuePair<string, int>>(g.MissingService);
                    list.Sort((x, y) => y.Value.CompareTo(x.Value));
                    sb.Append(",\"servicesMostMissing\":{");
                    for (int k = 0; k < list.Count; k++)
                    {
                        sb.Append(k > 0 ? "," : "").Append(Json.Str(list[k].Key)).Append(':').Append(list[k].Value);
                    }

                    sb.Append('}');
                }

                sb.Append("}}");
                firstGroup = false;
            }

            return sb.Append("]}").ToString();
        }

        // ---- レベル上げの内訳(#82。ready なのに上がらない建物と、サービスの何が足りないかを見るため) ----

        private class Term
        {
            public string Name;
            public int Rate, Effect, MaxEffect;
            public bool Minus;
        }

        // オフィス・工業の「サービスの点数」の項目。ゲームの CalculateServiceValue(OfficeBuildingAI、IndustrialBuildingAI)と同じ。
        // 項目 = CalculateResourceEffect(その場所の資源の値, 真ん中, 上限, 真ん中の効果, 上限の効果) ÷ 割る数。
        // 足す項目と引く項目(騒音、放棄、地面の汚染)がある。商業・住宅は null(地価で決まる)
        private static List<Term> ServiceTerms(Vector3 pos, ItemClass.Service service)
        {
            bool office = service == ItemClass.Service.Office;
            if (!office && service != ItemClass.Service.Industrial)
            {
                return null;
            }

            ushort[] res;
            int idx;
            ImmaterialResourceManager.instance.CheckLocalResources(pos, out res, out idx);
            var t = new List<Term>();
            // (名前, 資源の番号, 割る数)。番号は ImmaterialResourceManager.Resource の値
            Add(t, "publicTransport", res[idx + 7], 3, false);
            Add(t, "police", res[idx + 2], 5, false);
            Add(t, "healthcare", res[idx + 0], 5, false);
            Add(t, "deathcare", res[idx + 6], 5, false);
            Add(t, "postService", res[idx + 25], 5, false);
            Add(t, "fire", res[idx + 1], office ? 5 : 2, false);
            Add(t, "entertainment", res[idx + 13], office ? 6 : 8, false);
            Add(t, "educationElementary", res[idx + 3], office ? 7 : 8, false);
            Add(t, "educationHighSchool", res[idx + 4], office ? 7 : 8, false);
            Add(t, "educationUniversity", res[idx + 5], office ? 7 : 8, false);
            if (!office)
            {
                Add(t, "cargoTransport", res[idx + 19], 1, false);
            }

            AddCustom(t, "radioCoverage", res[idx + 20], 50, 100, 80, 100, 5, false);
            AddCustom(t, "firewatchCoverage", res[idx + 21], 100, 1000, 0, 100, 5, false);
            AddCustom(t, "disasterCoverage", res[idx + 23], 50, 100, 80, 100, 5, false);
            Add(t, "noise", res[idx + 8], office ? 4 : 7, true);
            Add(t, "abandonment", res[idx + 18], office ? 3 : 7, true);
            byte pollution;
            NaturalResourceManager.instance.CheckPollution(pos, out pollution);
            AddCustom(t, "groundPollution", pollution, 50, 255, 50, 100, office ? 4 : 6, true);
            return t;
        }

        private static void Add(List<Term> t, string name, int rate, int div, bool minus)
        {
            AddCustom(t, name, rate, 100, 500, 50, 100, div, minus);
        }

        private static void AddCustom(List<Term> t, string name, int rate, int mid, int max, int midEffect, int maxEffect, int div, bool minus)
        {
            t.Add(new Term
            {
                Name = name,
                Rate = rate,
                Effect = ImmaterialResourceManager.CalculateResourceEffect(rate, mid, max, midEffect, maxEffect) / div,
                MaxEffect = maxEffect / div,
                Minus = minus,
            });
        }

        private static int ServiceValue(List<Term> t)
        {
            int v = 0;
            foreach (var x in t)
            {
                v += x.Minus ? -x.Effect : x.Effect;
            }

            return v;
        }

        // いちばん点を伸ばせる項目(足す項目は上限までの残り、引く項目は今引かれている分)。DLC の項目(ラジオなど)は除く
        private static string WorstTerm(List<Term> t)
        {
            string best = null;
            int gain = -1;
            foreach (var x in t)
            {
                if (x.Name == "radioCoverage" || x.Name == "firewatchCoverage" || x.Name == "disasterCoverage" || x.Name == "postService")
                {
                    continue;
                }

                int g = x.Minus ? x.Effect : x.MaxEffect - x.Effect;
                if (g > gain)
                {
                    gain = g;
                    best = x.Name;
                }
            }

            return best ?? "none";
        }

        // /buildings/levelup?id=..  1棟のレベル上げの中身(ゲームの CheckBuildingLevel と同じ計算)
        private static string LevelUp(HttpListenerRequest req)
        {
            ushort id;
            if (!ushort.TryParse(req.QueryString["id"] ?? "", out id))
            {
                return HttpBridge.Error("id is required");
            }

            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var b = bs[id];
            var info = b.Info;
            if ((b.m_flags & Building.Flags.Created) == 0 || info == null || !(info.m_buildingAI is PrivateBuildingAI))
            {
                return HttpBridge.Error("not a zoned building: " + id);
            }

            var service = info.m_class.m_service;
            string[] names = Names(info.m_class.m_subService.ToString());
            int first = b.m_levelUpProgress & 0xF;
            int second = b.m_levelUpProgress >> 4;
            int level = b.m_level + 1;
            int maxLevel = service == ItemClass.Service.Residential ? 5 : 3;
            var upgrade = ((PrivateBuildingAI)info.m_buildingAI).GetUpgradeInfo(id, ref b);
            var sb = new StringBuilder("{\"ok\":true,\"id\":").Append(id).Append(",\"prefab\":").Append(Json.Str(info.name))
                .Append(",\"subService\":").Append(Json.Str(info.m_class.m_subService.ToString()))
                .Append(",\"level\":").Append(level).Append(",\"maxLevel\":").Append(maxLevel)
                .Append(",\"progress\":{").Append(Json.Str(names[0])).Append(':').Append(first)
                .Append(',').Append(Json.Str(names[1])).Append(':').Append(second).Append('}')
                .Append(",\"problems\":").Append(Json.Str(b.m_problems.ToString()))
                .Append(",\"upgradeModelExists\":").Append(upgrade != null ? "true" : "false");

            // 上がらない理由の見立て
            var blockers = new List<string>();
            if (level >= maxLevel)
            {
                blockers.Add("already max level");
            }
            else
            {
                if (first == 15 && second == 15)
                {
                    if (!b.m_problems.IsNone)
                    {
                        blockers.Add("both conditions met but the building has problem icons (" + b.m_problems + "). The game upgrades only buildings without problems");
                    }

                    if (upgrade == null)
                    {
                        blockers.Add("no higher-level building of the same size exists. Rezone or rebuild with a different size");
                    }
                }

                if (first < 15)
                {
                    blockers.Add(names[0] + " is not enough (" + first + "/15)");
                }

                if (second < 15)
                {
                    blockers.Add(names[1] + " is not enough (" + second + "/15)");
                }
            }

            int local;
            ImmaterialResourceManager.instance.CheckLocalResource(ImmaterialResourceManager.Resource.LandValue, b.m_position, out local);
            sb.Append(",\"landValue\":").Append(local);
            if (service == ItemClass.Service.Residential)
            {
                // 住宅の地価の段: 6未満 L1、21未満 L2、41未満 L3、61未満 L4、それ以上 L5
                sb.Append(",\"landValueForLevel\":[0,6,21,41,61]");
            }
            else if (service == ItemClass.Service.Commercial)
            {
                // 商業の地価の段: 21未満 L1、41未満 L2、それ以上 L3
                sb.Append(",\"landValueForLevel\":[0,21,41]");
            }

            var terms = ServiceTerms(b.m_position, service);
            if (terms != null)
            {
                bool office = service == ItemClass.Service.Office;
                int value = ServiceValue(terms);
                // オフィスは 45未満 L1、90未満 L2、それ以上 L3。工業は 30未満 L1、60未満 L2、それ以上 L3
                int need = level >= maxLevel ? 0 : office ? (level == 1 ? 45 : 90) : (level == 1 ? 30 : 60);
                sb.Append(",\"services\":{\"value\":").Append(value).Append(",\"neededForNextLevel\":").Append(need)
                  .Append(",\"mostMissing\":").Append(Json.Str(WorstTerm(terms))).Append(",\"terms\":[");
                for (int k = 0; k < terms.Count; k++)
                {
                    var x = terms[k];
                    sb.Append(k > 0 ? "," : "").Append("{\"name\":").Append(Json.Str(x.Name)).Append(",\"rate\":").Append(x.Rate)
                      .Append(",\"points\":").Append(x.Minus ? -x.Effect : x.Effect)
                      .Append(",\"maxPoints\":").Append(x.Minus ? 0 : x.MaxEffect).Append('}');
                }

                sb.Append("]}");
            }

            sb.Append(",\"blockers\":[");
            for (int k = 0; k < blockers.Count; k++)
            {
                sb.Append(k > 0 ? "," : "").Append(Json.Str(blockers[k]));
            }

            return sb.Append("]}").ToString();
        }

        // 2つの条件の名前(m_levelUpProgress の下4ビット、上4ビット)
        private static string[] Names(string subService)
        {
            if (subService.StartsWith("Residential", StringComparison.Ordinal))
            {
                return new[] { "education", "landValue" };
            }

            if (subService.StartsWith("Commercial", StringComparison.Ordinal))
            {
                return new[] { "wealth", "landValue" };
            }

            return new[] { "education", "services" };
        }

        // /landvalue?x=..&z=..&radius=..  円の中の地価(ゲームの地価の情報画面と同じ値)を、9×9の点で測る。
        // x を省くと、街の平均(DistrictManager の地区0)
        private static string LandValue(HttpListenerRequest req)
        {
            if (req.QueryString["x"] == null)
            {
                return "{\"ok\":true,\"cityAverage\":" + DistrictManager.instance.m_districts.m_buffer[0].GetLandValue() + "}";
            }

            float cx = F(req, "x", 0f), cz = F(req, "z", 0f), r = F(req, "radius", 500f);
            int n = 0, min = int.MaxValue, max = int.MinValue;
            long sum = 0;
            var rows = new StringBuilder("[");
            for (int iz = 0; iz < 9; iz++)
            {
                rows.Append(iz > 0 ? ",[" : "[");
                for (int ix = 0; ix < 9; ix++)
                {
                    var p = new Vector3(cx - r + r * ix / 4f, 0f, cz + r - r * iz / 4f);
                    int v;
                    ImmaterialResourceManager.instance.CheckLocalResource(ImmaterialResourceManager.Resource.LandValue, p, out v);
                    rows.Append(ix > 0 ? "," : "").Append(v);
                    n++;
                    sum += v;
                    min = Mathf.Min(min, v);
                    max = Mathf.Max(max, v);
                }

                rows.Append(']');
            }

            rows.Append(']');
            return "{\"ok\":true,\"average\":" + (sum / n) + ",\"min\":" + min + ",\"max\":" + max
                + ",\"cityAverage\":" + DistrictManager.instance.m_districts.m_buffer[0].GetLandValue()
                + ",\"grid\":" + rows + ",\"gridNote\":\"9x9 points, north row first, west to east\"}";
        }

        // /buildings/new?since=..  建物の通し番号(m_buildIndex)が since より新しい区画の建物を、種類ごとに数える。
        // 戻り値の index を、次に呼ぶときの since に渡す。前の月例から建った数が分かる
        private static string NewBuildings(HttpListenerRequest req)
        {
            uint since;
            uint.TryParse(req.QueryString["since"] ?? "0", NumberStyles.Integer, CultureInfo.InvariantCulture, out since);
            var counts = new SortedDictionary<string, int>();
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int i = 1; i < bs.Length; i++)
            {
                var info = bs[i].Info;
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || info == null || !(info.m_buildingAI is PrivateBuildingAI)
                    || bs[i].m_buildIndex <= since || bs[i].m_parentBuilding != 0)
                {
                    continue;
                }

                string key = info.m_class.m_subService.ToString();
                int k;
                counts.TryGetValue(key, out k);
                counts[key] = k + 1;
            }

            var sb = new StringBuilder("{\"ok\":true,\"index\":").Append(SimulationManager.instance.m_currentBuildIndex)
                .Append(",\"since\":").Append(since).Append(",\"newBuildings\":{");
            bool first = true;
            foreach (var kv in counts)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(':').Append(kv.Value);
                first = false;
            }

            return sb.Append("}}").ToString();
        }

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }
    }
}
