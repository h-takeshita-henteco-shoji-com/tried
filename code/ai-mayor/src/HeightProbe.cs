using System.Text;
using ICities;
using UnityEngine;

namespace AIMayor
{
    // F9 を押すと、主な地点の地形の高さと水面の高さを Player.log に書き出す。
    // 高さマップが期待どおりに読み込まれたか(高さの対応、海面、向き)を数値で確かめるために使う。
    public class HeightProbe : ThreadingExtensionBase
    {
        private struct Probe
        {
            public readonly string Name;
            public readonly float X;   // 東向き(ゲーム上のm)
            public readonly float Z;   // 北向き(ゲーム上のm)

            public Probe(string name, float x, float z)
            {
                Name = name;
                X = x;
                Z = z;
            }
        }

        // 実寸の位置を水平1/2縮尺でゲーム上の座標にしたもの(中心は天神駅と博多駅の中間)
        private static readonly Probe[] Probes =
        {
            new Probe("Tenjin", -466f, 7f),
            new Probe("Aburayama", -2103f, -4347f),
            new Probe("Sefurisan", -1910f, -8550f),
            new Probe("Wakasugiyama", 6249f, 424f),
            new Probe("Tachibanayama", 2699f, 4983f),
            new Probe("Nokonoshima", -4813f, 1791f),
            new Probe("HakataBay", -2309f, 2214f),
            // 海沿いの低地(水につかっていないかを見る)
            new Probe("HakataSta", 465f, -10f),
            new Probe("Nakasu", -198f, 185f),
            new Probe("HakataPort", -559f, 785f),
            new Probe("Hakozaki", 256f, 1519f),
            new Probe("Momochi", -2532f, 290f),
            new Probe("Meinohama", -3926f, -360f),
            new Probe("IslandCity", 506f, 4126f),
            new Probe("Kashii", 1584f, 3865f),
        };

        public override void OnUpdate(float realTimeDelta, float simulationTimeDelta)
        {
            if (Input.GetKeyDown(KeyCode.F9))
            {
                LogHeights();
            }
        }

        private static void LogHeights()
        {
            var terrain = TerrainManager.instance;
            var sb = new StringBuilder("[AIMayor] heights (terrain / with water)\n");
            foreach (var p in Probes)
            {
                var pos = new Vector3(p.X, 0f, p.Z);
                float ground = terrain.SampleRawHeightSmooth(pos);
                float water = terrain.SampleRawHeightSmoothWithWater(pos, false, 0f);
                sb.AppendFormat("  {0,-14} x={1,6:F0} z={2,6:F0}  {3,7:F1} m / {4,7:F1} m\n",
                    p.Name, p.X, p.Z, ground, water);
            }
            Debug.Log(sb.ToString());
        }
    }
}
