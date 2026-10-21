using System;
using System.Collections.Generic;
using System.Net;
using System.Text;

namespace AIMayor
{
    // 外とのつながり(輸出入)を返す(#82)。ゲームの情報画面「外部接続」(OutsideConnectionsInfoViewPanel)と同じ値。
    // 量は District の m_importData / m_exportData の m_average を (値 + 99) / 100 で丸めたもの(画面と同じ。週の量)。
    // つなぎ口ごとの量はゲームが持っていないので、今つなぎ口から出入りしている荷物の車(Importing / Exporting の印)を数える
    public static class TradeApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/trade"] = req => HttpBridge.OnMain(Trade);
        }

        private static string Trade()
        {
            var d = DistrictManager.instance.m_districts.m_buffer[0];
            var sb = new StringBuilder("{\"ok\":true,\"import\":");
            Resources(sb, d.m_importData, false);
            sb.Append(",\"export\":");
            Resources(sb, d.m_exportData, true);

            // つなぎ口ごと: 外とのつなぎ口の建物(OutsideConnectionAI)を、道路・鉄道・船・飛行機に分ける
            var kinds = new Dictionary<ushort, string>();
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            for (int i = 1; i < bs.Length; i++)
            {
                var info = bs[i].Info;
                if ((bs[i].m_flags & Building.Flags.Created) != 0 && info != null && info.m_buildingAI is OutsideConnectionAI)
                {
                    kinds[(ushort)i] = Kind(info.m_class);
                }
            }

            var importing = new Dictionary<ushort, int>();
            var exporting = new Dictionary<ushort, int>();
            var vs = VehicleManager.instance.m_vehicles.m_buffer;
            for (int i = 1; i < vs.Length; i++)
            {
                var f = vs[i].m_flags;
                if ((f & Vehicle.Flags.Created) == 0 || vs[i].m_leadingVehicle != 0)
                {
                    continue;
                }

                if ((f & Vehicle.Flags.Importing) != 0 && kinds.ContainsKey(vs[i].m_sourceBuilding))
                {
                    Add(importing, vs[i].m_sourceBuilding);
                }

                if ((f & Vehicle.Flags.Exporting) != 0 && kinds.ContainsKey(vs[i].m_targetBuilding))
                {
                    Add(exporting, vs[i].m_targetBuilding);
                }
            }

            sb.Append(",\"connections\":[");
            bool first = true;
            foreach (var kv in kinds)
            {
                int imp, exp;
                importing.TryGetValue(kv.Key, out imp);
                exporting.TryGetValue(kv.Key, out exp);
                var p = bs[kv.Key].m_position;
                sb.Append(first ? "" : ",").Append("{\"building\":").Append(kv.Key).Append(",\"kind\":").Append(Json.Str(kv.Value))
                  .Append(",\"x\":").Append(Mathf(p.x)).Append(",\"z\":").Append(Mathf(p.z))
                  .Append(",\"importingVehiclesNow\":").Append(imp).Append(",\"exportingVehiclesNow\":").Append(exp).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        private static void Resources(StringBuilder sb, DistrictResourceData r, bool withFish)
        {
            uint goods = (r.m_averageGoods + 99) / 100, oil = (r.m_averageOil + 99) / 100, ore = (r.m_averageOre + 99) / 100;
            uint forestry = (r.m_averageForestry + 99) / 100, agri = (r.m_averageAgricultural + 99) / 100, mail = (r.m_averageMail + 99) / 100;
            uint fish = withFish ? (r.m_averageFish + 99) / 100 : 0;
            sb.Append("{\"total\":").Append(goods + oil + ore + forestry + agri + mail + fish)
              .Append(",\"goods\":").Append(goods).Append(",\"oil\":").Append(oil).Append(",\"ore\":").Append(ore)
              .Append(",\"forestry\":").Append(forestry).Append(",\"agricultural\":").Append(agri).Append(",\"mail\":").Append(mail);
            if (withFish)
            {
                sb.Append(",\"fish\":").Append(fish);
            }

            sb.Append('}');
        }

        private static string Kind(ItemClass c)
        {
            switch (c.m_subService)
            {
                case ItemClass.SubService.PublicTransportTrain: return "train";
                case ItemClass.SubService.PublicTransportShip: return "ship";
                case ItemClass.SubService.PublicTransportPlane: return "plane";
            }

            return c.m_service == ItemClass.Service.Road ? "road" : c.m_subService.ToString();
        }

        private static void Add(Dictionary<ushort, int> d, ushort key)
        {
            int v;
            d.TryGetValue(key, out v);
            d[key] = v + 1;
        }

        private static int Mathf(float v)
        {
            return UnityEngine.Mathf.RoundToInt(v);
        }
    }
}
