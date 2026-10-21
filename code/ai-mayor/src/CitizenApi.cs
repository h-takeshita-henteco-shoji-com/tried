using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 市民の声の窓口: 市民の内訳、無作為に選んだ市民の姿、建物の困りごと(苦情)の集計。
    // 実際の市長が数字だけでなく市民の声を聞いて判断するのと同じ材料を、AI市長に渡す。
    public static class CitizenApi
    {
        // 苦情として集める、建物の困りごとの印
        private static readonly Notification.Problem1[] ComplaintTypes =
        {
            Notification.Problem1.Electricity, Notification.Problem1.Water, Notification.Problem1.Sewage,
            Notification.Problem1.Garbage, Notification.Problem1.Fire, Notification.Problem1.Crime,
            Notification.Problem1.Death, Notification.Problem1.DirtyWater, Notification.Problem1.Pollution,
            Notification.Problem1.Noise, Notification.Problem1.TaxesTooHigh, Notification.Problem1.LandValueLow,
            Notification.Problem1.TooFewServices, Notification.Problem1.NoWorkers, Notification.Problem1.NoEducatedWorkers,
            Notification.Problem1.NoCustomers, Notification.Problem1.NoGoods, Notification.Problem1.RoadNotConnected,
            Notification.Problem1.ElectricityNotConnected, Notification.Problem1.WaterNotConnected, Notification.Problem1.Flood,
        };

        private static readonly System.Random random = new System.Random();

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/citizens/summary"] = req => HttpBridge.OnMain(Summary);
            routes["/citizens/sample"] = req => HttpBridge.OnMain(() => Sample(req));
            routes["/complaints"] = req => HttpBridge.OnMain(Complaints);
            routes["/citizens/without_service"] = req => HttpBridge.OnMain(() => WithoutService(req));
        }

        // /citizens/without_service?type=sewage&limit=20  電気・水・下水が来ない住民の住まい(#82 の4年目の後)。
        // 37〜39か月目、下水が来ない最後の1人の家を探す手段がなかった。
        // 数え方は city_info の citizensWithoutService と同じ(住民のカウンタ NoWater などが1以上)。
        // カウンタは住民の処理(4096コマ = ゲーム内の7日ごと)のときに、家の位置のマス(38.25m)を WaterManager.CheckWater
        // などで調べて、来ていなければ1増え(2で止まる)、来ていれば0に戻る(ResidentAI.UpdateHealth)。
        // そのため棟の grid より最大7日遅れて動き、棟の数と人数はそろわない
        // 住民のカウンタと同じ調べ方で、今その位置に来ているか。true なら、次の住民の処理でカウンタが0に戻る
        private static bool CellNow(string type, Vector3 pos)
        {
            if (type == "electricity")
            {
                bool e;
                ElectricityManager.instance.CheckElectricity(pos, out e);
                return e;
            }

            bool w, sw;
            byte pollution;
            WaterManager.instance.CheckWater(pos, out w, out sw, out pollution);
            return type == "water" ? w : sw;
        }

        private static string WithoutService(HttpListenerRequest req)
        {
            string type = (req.QueryString["type"] ?? "sewage").ToLowerInvariant();
            if (type != "electricity" && type != "water" && type != "sewage")
            {
                return HttpBridge.Error("type must be electricity, water or sewage");
            }

            int limit;
            if (!int.TryParse(req.QueryString["limit"] ?? "20", NumberStyles.Integer, CultureInfo.InvariantCulture, out limit))
            {
                limit = 20;
            }

            limit = Mathf.Clamp(limit, 1, 200);
            var buf = CitizenManager.instance.m_citizens.m_buffer;
            var homes = new Dictionary<ushort, int>();
            int total = 0;
            for (int i = 1; i < buf.Length; i++)
            {
                if (!IsResident(ref buf[i]))
                {
                    continue;
                }

                int counter = type == "electricity" ? buf[i].NoElectricity : type == "water" ? buf[i].NoWater : buf[i].NoSewage;
                if (counter <= 0)
                {
                    continue;
                }

                total++;
                int n;
                homes.TryGetValue(buf[i].m_homeBuilding, out n);
                homes[buf[i].m_homeBuilding] = n + 1;
            }

            var list = new List<KeyValuePair<ushort, int>>(homes);
            list.Sort((a, b) => b.Value != a.Value ? b.Value.CompareTo(a.Value) : a.Key.CompareTo(b.Key));
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("{\"ok\":true,\"type\":").Append(Json.Str(type)).Append(",\"residents\":").Append(total)
                .Append(",\"buildings\":").Append(list.Count).Append(",\"homes\":[");
            for (int k = 0; k < list.Count && k < limit; k++)
            {
                ushort id = list[k].Key;
                var b = bs[id];
                sb.Append(k > 0 ? "," : "").Append("{\"building\":").Append(id)
                  .Append(",\"prefab\":").Append(Json.Str(b.Info != null ? b.Info.name : null))
                  .Append(",\"x\":").Append(N(b.m_position.x)).Append(",\"z\":").Append(N(b.m_position.z))
                  .Append(",\"residents\":").Append(list[k].Value)
                  .Append(",\"grid\":").Append(MapApi.GridJson(ref bs[id]))
                  .Append(",\"cellNow\":").Append(CellNow(type, b.m_position) ? "true" : "false").Append('}');
            }

            return sb.Append("]}").ToString();
        }

        // 住んでいる市民(観光客、亡くなった人、引っ越しの途中の人を除く)か。
        // ゲームの人口も引っ越しの途中の人を数えない(Citizen.GetCitizenHomeBehaviour)ので、それに合わせる
        private static bool IsResident(ref Citizen c)
        {
            return HasHome(ref c) && (c.m_flags & Citizen.Flags.MovingIn) == 0;
        }

        // 家が決まっている市民(引っ越しの途中を含む)か
        private static bool HasHome(ref Citizen c)
        {
            return (c.m_flags & Citizen.Flags.Created) != 0 && (c.m_flags & (Citizen.Flags.Tourist | Citizen.Flags.Dead)) == 0
                && c.m_homeBuilding != 0;
        }

        // 電気・水・下水が来ない市民の数。citizens_summary の peopleWithProblems と同じ数え方。
        // 見回りでは city_info しか見ないため、city_info にも載せる(#81 では公約2を最後の日に破った)
        public static string NoServiceJson()
        {
            var buf = CitizenManager.instance.m_citizens.m_buffer;
            int e = 0, w = 0, s = 0;
            for (int i = 1; i < buf.Length; i++)
            {
                if (!IsResident(ref buf[i]))
                {
                    continue;
                }

                if (buf[i].NoElectricity > 0) e++;
                if (buf[i].NoWater > 0) w++;
                if (buf[i].NoSewage > 0) s++;
            }

            return "{\"electricity\":" + e + ",\"water\":" + w + ",\"sewage\":" + s + "}";
        }

        // /citizens/summary  市民の内訳
        private static string Summary()
        {
            var buf = CitizenManager.instance.m_citizens.m_buffer;
            int total = 0, employed = 0, unemployed = 0, students = 0, sick = 0;
            // 失業の内訳(#82)。若者の失業には、大学の席がなく働き口も合わない人が入る。
            // 働き口は学歴ごとに分かれ(TransferReason.Worker0〜3)、学歴のない人は学歴の要らない働き口しか探さない
            int unemployedYoung = 0, unemployedAdult = 0;
            var unemployedEdu = new int[4];
            long health = 0, wellbeing = 0, happiness = 0;
            var age = new int[5];
            var edu = new int[4];
            var wealth = new int[3];
            var complaintPeople = new Dictionary<string, int>
            {
                { "noElectricity", 0 }, { "noWater", 0 }, { "noSewage", 0 }, { "badHealth", 0 }, { "longUnemployed", 0 },
            };

            // 引っ越しの途中の人。つなぎ口から家までの道順が見つかると、印が外れて人口に入る(HumanAI.PathfindSuccess)
            int movingIn = 0, movingInTraveling = 0;
            for (int i = 1; i < buf.Length; i++)
            {
                if (HasHome(ref buf[i]) && (buf[i].m_flags & Citizen.Flags.MovingIn) != 0)
                {
                    movingIn++;
                    if (buf[i].m_instance != 0 || buf[i].m_vehicle != 0)
                    {
                        movingInTraveling++;
                    }
                }

                if (!IsResident(ref buf[i]))
                {
                    continue;
                }

                total++;
                var group = Citizen.GetAgeGroup(buf[i].m_age);
                age[(int)group]++;
                edu[(int)buf[i].EducationLevel]++;
                wealth[(int)buf[i].WealthLevel]++;
                health += buf[i].m_health;
                wellbeing += buf[i].m_wellbeing;
                happiness += Citizen.GetHappiness(buf[i].m_health, buf[i].m_wellbeing);
                if ((buf[i].m_flags & Citizen.Flags.Sick) != 0)
                {
                    sick++;
                }

                if ((buf[i].m_flags & Citizen.Flags.Student) != 0)
                {
                    students++;
                }
                else if (buf[i].m_workBuilding != 0)
                {
                    employed++;
                }
                else if (group == Citizen.AgeGroup.Young || group == Citizen.AgeGroup.Adult)
                {
                    unemployed++;
                    if (group == Citizen.AgeGroup.Young) unemployedYoung++; else unemployedAdult++;
                    unemployedEdu[(int)buf[i].EducationLevel]++;
                }

                if (buf[i].NoElectricity > 0) complaintPeople["noElectricity"]++;
                if (buf[i].NoWater > 0) complaintPeople["noWater"]++;
                if (buf[i].NoSewage > 0) complaintPeople["noSewage"]++;
                if (buf[i].BadHealth > 0) complaintPeople["badHealth"]++;
                if (buf[i].Unemployed > 2) complaintPeople["longUnemployed"]++;
            }

            var sb = new StringBuilder("{\"ok\":true,\"residents\":").Append(total);
            sb.Append(",\"movingIn\":{\"total\":").Append(movingIn).Append(",\"traveling\":").Append(movingInTraveling).Append('}');
            sb.Append(",\"age\":{\"child\":").Append(age[0]).Append(",\"teen\":").Append(age[1]).Append(",\"young\":").Append(age[2])
              .Append(",\"adult\":").Append(age[3]).Append(",\"senior\":").Append(age[4]).Append('}');
            sb.Append(",\"education\":{\"uneducated\":").Append(edu[0]).Append(",\"elementary\":").Append(edu[1])
              .Append(",\"highSchool\":").Append(edu[2]).Append(",\"university\":").Append(edu[3]).Append('}');
            sb.Append(",\"wealth\":{\"low\":").Append(wealth[0]).Append(",\"medium\":").Append(wealth[1]).Append(",\"high\":").Append(wealth[2]).Append('}');
            sb.Append(",\"employed\":").Append(employed).Append(",\"unemployed\":").Append(unemployed)
              .Append(",\"students\":").Append(students).Append(",\"sick\":").Append(sick);
            sb.Append(",\"unemployedDetail\":{\"young\":").Append(unemployedYoung).Append(",\"adult\":").Append(unemployedAdult)
              .Append(",\"byEducation\":{\"uneducated\":").Append(unemployedEdu[0]).Append(",\"elementary\":").Append(unemployedEdu[1])
              .Append(",\"highSchool\":").Append(unemployedEdu[2]).Append(",\"university\":").Append(unemployedEdu[3]).Append("}}");
            if (total > 0)
            {
                sb.Append(",\"average\":{\"health\":").Append(health / total).Append(",\"wellbeing\":").Append(wellbeing / total)
                  .Append(",\"happiness\":").Append(happiness / total).Append('}');
            }

            sb.Append(",\"peopleWithProblems\":{");
            bool first = true;
            foreach (var kv in complaintPeople)
            {
                sb.Append(first ? "" : ",").Append(Json.Str(kv.Key)).Append(':').Append(kv.Value);
                first = false;
            }

            return sb.Append("}}").ToString();
        }

        // /citizens/sample?n=5  住んでいる市民を無作為に選び、その姿を返す
        private static string Sample(HttpListenerRequest req)
        {
            int n;
            if (!int.TryParse(req.QueryString["n"] ?? "5", out n))
            {
                n = 5;
            }

            n = Mathf.Clamp(n, 1, 20);
            var buf = CitizenManager.instance.m_citizens.m_buffer;
            var ids = new List<int>();
            for (int i = 1; i < buf.Length; i++)
            {
                if (IsResident(ref buf[i]))
                {
                    ids.Add(i);
                }
            }

            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var sb = new StringBuilder("{\"ok\":true,\"residents\":").Append(ids.Count).Append(",\"citizens\":[");
            for (int k = 0; k < n && ids.Count > 0; k++)
            {
                int pick = random.Next(ids.Count);
                int id = ids[pick];
                ids.RemoveAt(pick);
                var c = buf[id];
                var home = bs[c.m_homeBuilding];
                int happy = Citizen.GetHappiness(c.m_health, c.m_wellbeing);

                string job;
                if ((c.m_flags & Citizen.Flags.Student) != 0)
                {
                    job = "student";
                }
                else if (c.m_workBuilding != 0)
                {
                    var w = bs[c.m_workBuilding].Info;
                    job = w != null ? "works:" + w.m_class.m_service : "works";
                }
                else
                {
                    // 仕事を探す年(若者・大人)で仕事がなければ失業。Unemployed のカウンタ(ResidentAI.UpdateHealth)は
                    // 7日ごとの更新でしか動かないので、それで決めると、就いた直後や失った直後に食い違う(#82)
                    var group = Citizen.GetAgeGroup(c.m_age);
                    job = group == Citizen.AgeGroup.Young || group == Citizen.AgeGroup.Adult ? "unemployed" : "none";
                }

                sb.Append(k == 0 ? "" : ",").Append("{\"id\":").Append(id)
                  .Append(",\"ageGroup\":").Append(Json.Str(Citizen.GetAgeGroup(c.m_age).ToString()))
                  .Append(",\"education\":").Append(Json.Str(c.EducationLevel.ToString()))
                  .Append(",\"wealth\":").Append(Json.Str(c.WealthLevel.ToString()))
                  .Append(",\"job\":").Append(Json.Str(job))
                  .Append(",\"health\":").Append(Json.Str(Citizen.GetHealthLevel(c.m_health).ToString()))
                  .Append(",\"happiness\":").Append(Json.Str(Citizen.GetHappinessLevel(happy).ToString()))
                  .Append(",\"home\":{\"x\":").Append(N(home.m_position.x)).Append(",\"z\":").Append(N(home.m_position.z))
                  .Append(",\"type\":").Append(Json.Str(home.Info != null ? home.Info.m_class.m_subService.ToString() : null))
                  .Append(",\"problems\":").Append(Json.Str(home.m_problems.ToString())).Append('}')
                  .Append(",\"troubles\":{\"noElectricity\":").Append(c.NoElectricity).Append(",\"noWater\":").Append(c.NoWater)
                  .Append(",\"noSewage\":").Append(c.NoSewage).Append(",\"badHealth\":").Append(c.BadHealth)
                  // 仕事のない週の数(0〜7)。7日ごとに1ずつ増え、仕事に就くと次の更新で0に戻る。今の仕事の有無は job を見る
                  .Append(",\"unemployedWeeks\":").Append(c.Unemployed).Append("}}");
            }

            return sb.Append("]}").ToString();
        }

        // /complaints  建物の困りごとの印を、種類ごとに数え、多い場所を返す。
        // 場所は、印のいちばん多い区画(1.92km四方)の中の、印のある建物の平均の位置。examples にその区画の建物を5件まで
        private static string Complaints()
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var counts = new Dictionary<Notification.Problem1, int>();
            var spots = new Dictionary<Notification.Problem1, Dictionary<int, int>>();
            // 印のある建物の番号(種類ごと)。hotspot の位置と examples に使う
            var holders = new Dictionary<Notification.Problem1, List<ushort>>();
            int withProblems = 0;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].m_problems.IsNone)
                {
                    continue;
                }

                Notification.Problem1 p = bs[i].m_problems;
                bool any = false;
                foreach (var t in ComplaintTypes)
                {
                    if ((p & t) == 0)
                    {
                        continue;
                    }

                    any = true;
                    int n;
                    counts.TryGetValue(t, out n);
                    counts[t] = n + 1;

                    // 9×9の区画の番号(0〜80)で、場所ごとに数える
                    int tx = Mathf.Clamp((int)((bs[i].m_position.x + 8640f) / 1920f), 0, 8);
                    int tz = Mathf.Clamp((int)((bs[i].m_position.z + 8640f) / 1920f), 0, 8);
                    Dictionary<int, int> s;
                    if (!spots.TryGetValue(t, out s))
                    {
                        s = new Dictionary<int, int>();
                        spots[t] = s;
                    }

                    int key = tz * 9 + tx;
                    int m;
                    s.TryGetValue(key, out m);
                    s[key] = m + 1;

                    List<ushort> list;
                    if (!holders.TryGetValue(t, out list))
                    {
                        list = new List<ushort>();
                        holders[t] = list;
                    }

                    list.Add((ushort)i);
                }

                if (any)
                {
                    withProblems++;
                }
            }

            var sb = new StringBuilder("{\"ok\":true,\"buildingsWithProblems\":").Append(withProblems).Append(",\"complaints\":[");
            bool first = true;
            foreach (var kv in counts)
            {
                // いちばん多い区画(1.92km四方)を選ぶ。同じ数なら番号の小さい区画(呼ぶたびに変わらないように)
                int bestKey = 0, best = -1;
                foreach (var s in spots[kv.Key])
                {
                    if (s.Value > best || (s.Value == best && s.Key < bestKey))
                    {
                        best = s.Value;
                        bestKey = s.Key;
                    }
                }

                // hotspot は、その区画の中の印のある建物の平均の位置(#82)。
                // 以前は区画の中心を返し、街の外や、建物から約500m離れた所を指した
                float sx = 0f, sz = 0f;
                int n = 0;
                var examples = new StringBuilder("[");
                foreach (var id in holders[kv.Key])
                {
                    var pos = bs[id].m_position;
                    int tx = Mathf.Clamp((int)((pos.x + 8640f) / 1920f), 0, 8);
                    int tz = Mathf.Clamp((int)((pos.z + 8640f) / 1920f), 0, 8);
                    if (tz * 9 + tx != bestKey)
                    {
                        continue;
                    }

                    sx += pos.x;
                    sz += pos.z;
                    if (n < 5)
                    {
                        examples.Append(n == 0 ? "" : ",").Append("{\"id\":").Append(id)
                          .Append(",\"x\":").Append(N(pos.x)).Append(",\"z\":").Append(N(pos.z))
                          .Append(",\"prefab\":").Append(Json.Str(bs[id].Info != null ? bs[id].Info.name : null)).Append('}');
                    }

                    n++;
                }

                examples.Append(']');
                float cx = n > 0 ? sx / n : (bestKey % 9) * 1920f - 8640f + 960f;
                float cz = n > 0 ? sz / n : (bestKey / 9) * 1920f - 8640f + 960f;
                sb.Append(first ? "" : ",").Append("{\"type\":").Append(Json.Str(kv.Key.ToString()))
                  .Append(",\"buildings\":").Append(kv.Value)
                  .Append(",\"hotspot\":{\"x\":").Append(N(cx)).Append(",\"z\":").Append(N(cz)).Append(",\"buildings\":").Append(best).Append('}')
                  .Append(",\"examples\":").Append(examples).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        private static string N(float v)
        {
            return v.ToString("0.#", CultureInfo.InvariantCulture);
        }
    }
}
