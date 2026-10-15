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
        }

        // 住んでいる市民(観光客と亡くなった人を除く)か
        private static bool IsResident(ref Citizen c)
        {
            return (c.m_flags & Citizen.Flags.Created) != 0 && (c.m_flags & (Citizen.Flags.Tourist | Citizen.Flags.Dead)) == 0
                && c.m_homeBuilding != 0;
        }

        // /citizens/summary  市民の内訳
        private static string Summary()
        {
            var buf = CitizenManager.instance.m_citizens.m_buffer;
            int total = 0, employed = 0, unemployed = 0, students = 0, sick = 0;
            long health = 0, wellbeing = 0, happiness = 0;
            var age = new int[5];
            var edu = new int[4];
            var wealth = new int[3];
            var complaintPeople = new Dictionary<string, int>
            {
                { "noElectricity", 0 }, { "noWater", 0 }, { "noSewage", 0 }, { "badHealth", 0 }, { "longUnemployed", 0 },
            };

            for (int i = 1; i < buf.Length; i++)
            {
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
                }

                if (buf[i].NoElectricity > 0) complaintPeople["noElectricity"]++;
                if (buf[i].NoWater > 0) complaintPeople["noWater"]++;
                if (buf[i].NoSewage > 0) complaintPeople["noSewage"]++;
                if (buf[i].BadHealth > 0) complaintPeople["badHealth"]++;
                if (buf[i].Unemployed > 2) complaintPeople["longUnemployed"]++;
            }

            var sb = new StringBuilder("{\"ok\":true,\"residents\":").Append(total);
            sb.Append(",\"age\":{\"child\":").Append(age[0]).Append(",\"teen\":").Append(age[1]).Append(",\"young\":").Append(age[2])
              .Append(",\"adult\":").Append(age[3]).Append(",\"senior\":").Append(age[4]).Append('}');
            sb.Append(",\"education\":{\"uneducated\":").Append(edu[0]).Append(",\"elementary\":").Append(edu[1])
              .Append(",\"highSchool\":").Append(edu[2]).Append(",\"university\":").Append(edu[3]).Append('}');
            sb.Append(",\"wealth\":{\"low\":").Append(wealth[0]).Append(",\"medium\":").Append(wealth[1]).Append(",\"high\":").Append(wealth[2]).Append('}');
            sb.Append(",\"employed\":").Append(employed).Append(",\"unemployed\":").Append(unemployed)
              .Append(",\"students\":").Append(students).Append(",\"sick\":").Append(sick);
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
                    job = c.Unemployed > 0 ? "unemployed" : "none";
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
                  .Append(",\"unemployed\":").Append(c.Unemployed).Append("}}");
            }

            return sb.Append("]}").ToString();
        }

        // /complaints  建物の困りごとの印を、種類ごとに数え、多い場所(1.92km四方の区画)を返す
        private static string Complaints()
        {
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            var counts = new Dictionary<Notification.Problem1, int>();
            var spots = new Dictionary<Notification.Problem1, Dictionary<int, int>>();
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
                // いちばん多い区画の中心の座標
                int bestKey = 0, best = -1;
                foreach (var s in spots[kv.Key])
                {
                    if (s.Value > best)
                    {
                        best = s.Value;
                        bestKey = s.Key;
                    }
                }

                float cx = (bestKey % 9) * 1920f - 8640f + 960f;
                float cz = (bestKey / 9) * 1920f - 8640f + 960f;
                sb.Append(first ? "" : ",").Append("{\"type\":").Append(Json.Str(kv.Key.ToString()))
                  .Append(",\"buildings\":").Append(kv.Value)
                  .Append(",\"hotspot\":{\"x\":").Append(N(cx)).Append(",\"z\":").Append(N(cz)).Append(",\"buildings\":").Append(best).Append("}}");
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
