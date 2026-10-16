using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;

namespace AIMayor
{
    // お金の内訳を見る窓口。週の支出が何から来ているかを、AI市長と人が確かめるために使う。
    // - サービスごとの週の収入と支出(ゲームの財務の画面と同じ記録)
    // - 線(道路・線路・管・送電線)の種類ごとの本数、長さ、維持費
    //   ゲームはマップエディターで置いた線(Original の印)と、壊せない線(Untouchable)からは維持費を取らない
    public static class EconomyApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/economy/breakdown"] = req => HttpBridge.OnMain(Breakdown);
        }

        private static string Breakdown()
        {
            var eco = EconomyManager.instance;
            var sb = new StringBuilder("{\"ok\":true");

            long income, expenses;
            eco.GetIncomeAndExpenses(ItemClass.Service.None, ItemClass.SubService.None, ItemClass.Level.None, out income, out expenses);
            sb.Append(",\"total\":{\"income\":").Append(income / 100).Append(",\"expenses\":").Append(expenses / 100).Append('}');
            sb.Append(",\"policyExpenses\":").Append(eco.GetPolicyExpenses() / 100);
            sb.Append(",\"loanExpenses\":").Append(eco.GetLoanExpenses() / 100);

            // サービスごと。ServicePoint と Fishing は、ゲームが Beautification と PlayerIndustry に足し込むので外す
            sb.Append(",\"services\":[");
            bool first = true;
            foreach (ItemClass.Service s in Enum.GetValues(typeof(ItemClass.Service)))
            {
                if (s == ItemClass.Service.None || s == ItemClass.Service.ServicePoint || s == ItemClass.Service.Fishing)
                {
                    continue;
                }

                eco.GetIncomeAndExpenses(s, ItemClass.SubService.None, ItemClass.Level.None, out income, out expenses);
                if (income == 0 && expenses == 0)
                {
                    continue;
                }

                sb.Append(first ? "" : ",").Append("{\"service\":").Append(Json.Str(s.ToString()))
                  .Append(",\"income\":").Append(income / 100).Append(",\"expenses\":").Append(expenses / 100);

                // 公共交通は、鉄道・バスなどの内訳も付ける
                if (s == ItemClass.Service.PublicTransport)
                {
                    sb.Append(",\"subServices\":[");
                    bool f2 = true;
                    foreach (ItemClass.SubService sub in Enum.GetValues(typeof(ItemClass.SubService)))
                    {
                        if (!sub.ToString().StartsWith("PublicTransport", StringComparison.Ordinal))
                        {
                            continue;
                        }

                        long i2, e2;
                        eco.GetIncomeAndExpenses(s, sub, ItemClass.Level.None, out i2, out e2);
                        if (i2 == 0 && e2 == 0)
                        {
                            continue;
                        }

                        sb.Append(f2 ? "" : ",").Append("{\"subService\":").Append(Json.Str(sub.ToString()))
                          .Append(",\"income\":").Append(i2 / 100).Append(",\"expenses\":").Append(e2 / 100).Append('}');
                        f2 = false;
                    }

                    sb.Append(']');
                }

                sb.Append('}');
                first = false;
            }

            sb.Append(']');
            sb.Append(",\"networks\":").Append(Networks());
            return sb.Append('}').ToString();
        }

        private class NetSum
        {
            public string Service;
            public int Segments;
            public int Free; // Original / Untouchable の印があり、維持費を取られない区間
            public double Length;
            public double FreeLength;
            public long Maintenance; // 維持費を取られる区間の GetMaintenanceCost の合計(ゲーム内部の単位)
        }

        // 線の種類ごとに、本数・長さ(km)・維持費を集める。維持費は区間ごとの GetMaintenanceCost の合計で、
        // 週の支出とは単位が違う。種類どうしの比べ合いに使う
        private static string Networks()
        {
            var nets = NetManager.instance;
            var sums = new Dictionary<string, NetSum>();
            for (int i = 1; i < nets.m_segments.m_size; i++)
            {
                var seg = nets.m_segments.m_buffer[i];
                if ((seg.m_flags & NetSegment.Flags.Created) == 0 || seg.Info == null)
                {
                    continue;
                }

                var info = seg.Info;
                NetSum sum;
                if (!sums.TryGetValue(info.name, out sum))
                {
                    sum = new NetSum { Service = info.m_class.m_service + "/" + info.m_class.m_subService };
                    sums[info.name] = sum;
                }

                bool free = (seg.m_flags & (NetSegment.Flags.Original | NetSegment.Flags.Untouchable)) != 0;
                sum.Segments++;
                sum.Length += seg.m_averageLength;
                if (free)
                {
                    sum.Free++;
                    sum.FreeLength += seg.m_averageLength;
                    continue;
                }

                var ai = info.m_netAI as PlayerNetAI;
                if (ai != null)
                {
                    var a = nets.m_nodes.m_buffer[seg.m_startNode].m_position;
                    var b = nets.m_nodes.m_buffer[seg.m_endNode].m_position;
                    sum.Maintenance += ai.GetMaintenanceCost(a, b);
                }
            }

            var list = new List<KeyValuePair<string, NetSum>>(sums);
            list.Sort((x, y) => y.Value.Maintenance.CompareTo(x.Value.Maintenance));
            var sb = new StringBuilder("[");
            for (int i = 0; i < list.Count; i++)
            {
                var s = list[i].Value;
                sb.Append(i > 0 ? "," : "").Append("{\"prefab\":").Append(Json.Str(list[i].Key))
                  .Append(",\"service\":").Append(Json.Str(s.Service))
                  .Append(",\"segments\":").Append(s.Segments)
                  .Append(",\"freeSegments\":").Append(s.Free)
                  .Append(",\"lengthKm\":").Append(Km(s.Length))
                  .Append(",\"freeLengthKm\":").Append(Km(s.FreeLength))
                  .Append(",\"maintenance\":").Append(s.Maintenance).Append('}');
            }

            return sb.Append(']').ToString();
        }

        private static string Km(double meters)
        {
            return (meters / 1000.0).ToString("0.00", CultureInfo.InvariantCulture);
        }
    }
}
