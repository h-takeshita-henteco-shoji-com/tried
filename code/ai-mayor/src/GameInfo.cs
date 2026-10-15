using System.Globalization;
using System.Text;

namespace AIMayor
{
    // /info の中身。今のモードと、街の基本の数字を返す。メインスレッドで呼ぶ。
    public static class GameInfo
    {
        public static string Read()
        {
            var sim = SimulationManager.instance;
            var meta = sim.m_metaData;
            var city = DistrictManager.instance.m_districts.m_buffer[0];
            var zone = ZoneManager.instance;
            var eco = EconomyManager.instance;

            long income, expenses;
            eco.GetIncomeAndExpenses(new ItemClass(), out income, out expenses);

            var sb = new StringBuilder("{\"ok\":true");
            sb.Append(",\"mode\":").Append(Json.Str(meta != null ? meta.m_updateMode.ToString() : "none"));
            sb.Append(",\"city\":").Append(Json.Str(meta != null ? meta.m_CityName : null));
            sb.Append(",\"date\":").Append(Json.Str(sim.m_currentGameTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture)));
            sb.Append(",\"paused\":").Append(sim.SimulationPaused ? "true" : "false");
            sb.Append(",\"speed\":").Append(sim.SelectedSimulationSpeed);
            sb.Append(",\"population\":").Append(city.m_populationData.m_finalCount);
            sb.Append(",\"happiness\":").Append(city.m_finalHappiness);
            sb.Append(",\"money\":").Append(Num(eco.LastCashAmount / 100));
            sb.Append(",\"weeklyIncome\":").Append(Num(income / 100));
            sb.Append(",\"weeklyExpenses\":").Append(Num(expenses / 100));
            sb.Append(",\"demand\":{\"residential\":").Append(zone.m_residentialDemand)
              .Append(",\"commercial\":").Append(zone.m_commercialDemand)
              .Append(",\"workplace\":").Append(zone.m_workplaceDemand).Append('}');
            sb.Append(",\"ownedTiles\":").Append(GameAreaManager.instance.m_areaCount);
            return sb.Append('}').ToString();
        }

        private static string Num(long v)
        {
            return v.ToString(CultureInfo.InvariantCulture);
        }
    }
}
