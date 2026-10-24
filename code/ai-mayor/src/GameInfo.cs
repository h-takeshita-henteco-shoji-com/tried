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
            // 観光客(#100)。now は今いる観光客、visits は訪問の平均(ゲームの統計 TouristVisits と同じ値)。豊かさ3段の合計
            sb.Append(",\"tourists\":{\"now\":").Append(city.m_tourist1Data.m_finalCount + city.m_tourist2Data.m_finalCount + city.m_tourist3Data.m_finalCount)
              .Append(",\"visits\":").Append(city.m_tourist1Data.m_averageVisits + city.m_tourist2Data.m_averageVisits + city.m_tourist3Data.m_averageVisits).Append('}');
            sb.Append(",\"money\":").Append(Num(eco.LastCashAmount / 100));
            sb.Append(",\"weeklyIncome\":").Append(Num(income / 100));
            sb.Append(",\"weeklyExpenses\":").Append(Num(expenses / 100));
            sb.Append(",\"demand\":{\"residential\":").Append(zone.m_residentialDemand)
              .Append(",\"commercial\":").Append(zone.m_commercialDemand)
              .Append(",\"workplace\":").Append(zone.m_workplaceDemand).Append('}');
            // 電気・水・下水が来ない市民の数(公約2の測り方と同じ)
            sb.Append(",\"citizensWithoutService\":").Append(CitizenApi.NoServiceJson());
            sb.Append(",\"ownedTiles\":").Append(GameAreaManager.instance.m_areaCount);
            // ゲームに出ているダイアログ(破産の警告など)。なければ null
            sb.Append(",\"dialog\":").Append(DialogWatch.Current);
            // 最後に開いたダイアログの連番。前回より増えていたら、閉じたものも /ui/dialog/events で読める
            sb.Append(",\"dialogSeq\":").Append(DialogWatch.Seq);
            return sb.Append('}').ToString();
        }

        private static string Num(long v)
        {
            return v.ToString(CultureInfo.InvariantCulture);
        }
    }
}
