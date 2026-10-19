using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using UnityEngine;

namespace AIMayor
{
    // 交通の詰まりを見る窓口。試運転(#73)では高速の出入口に車が詰まって見えたが、
    // events にも complaints にも出なかった。ゲームの交通の画面と同じ数字を返す。
    // - flow: 街全体の交通の流れ(%)。交通の情報画面の「平均の交通の流れ」
    // - 道路の区間ごとの混み具合(m_trafficDensity、0〜100)。交通の情報画面の色
    // - 進めずに止まっている車(m_blockCounter が増えた車)と、その多い場所
    public static class TrafficApi
    {
        // 止まっていると数える m_blockCounter の下限。ゲームは255に届いた車を消す
        private const int BlockedFrom = 32;
        private const float Cell = 200f;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/traffic"] = req => HttpBridge.OnMain(() => Traffic(req));
        }

        // /traffic?x=..&z=..&radius=..&limit=10  x, z, radius を省くと街全体
        private static string Traffic(HttpListenerRequest req)
        {
            bool area = req.QueryString["x"] != null && req.QueryString["z"] != null;
            var center = new Vector2(F(req, "x", 0f), F(req, "z", 0f));
            float radius = F(req, "radius", 500f);
            int limit = (int)F(req, "limit", 10f);

            // 車
            var vm = VehicleManager.instance;
            int cars = 0, blocked = 0, congestion = 0;
            var cells = new Dictionary<long, int[]>(); // 200m のマスごとの [止まっている車, x合計, z合計]
            for (int i = 1; i < vm.m_vehicles.m_size; i++)
            {
                var v = vm.m_vehicles.m_buffer[i];
                if ((v.m_flags & (Vehicle.Flags.Created | Vehicle.Flags.Spawned)) != (Vehicle.Flags.Created | Vehicle.Flags.Spawned)
                    || v.m_leadingVehicle != 0 || v.Info == null || !(v.Info.m_vehicleAI is CarAI))
                {
                    continue;
                }

                var p = v.GetLastFramePosition();
                if (area && (new Vector2(p.x, p.z) - center).magnitude > radius)
                {
                    continue;
                }

                cars++;
                if ((v.m_flags & Vehicle.Flags.Congestion) != 0)
                {
                    congestion++;
                }

                if (v.m_blockCounter < BlockedFrom)
                {
                    continue;
                }

                blocked++;
                long key = ((long)Mathf.FloorToInt(p.x / Cell) << 32) ^ (uint)Mathf.FloorToInt(p.z / Cell);
                int[] c;
                if (!cells.TryGetValue(key, out c))
                {
                    c = new int[3];
                    cells[key] = c;
                }

                c[0]++;
                c[1] += (int)p.x;
                c[2] += (int)p.z;
            }

            // 道路の区間
            var nets = NetManager.instance;
            var segs = new List<KeyValuePair<int, ushort>>();
            int roads = 0;
            long densitySum = 0;
            for (int i = 1; i < nets.m_segments.m_size; i++)
            {
                var seg = nets.m_segments.m_buffer[i];
                if ((seg.m_flags & NetSegment.Flags.Created) == 0 || seg.Info == null
                    || seg.Info.m_class.m_service != ItemClass.Service.Road)
                {
                    continue;
                }

                var mid = seg.m_middlePosition;
                if (area && (new Vector2(mid.x, mid.z) - center).magnitude > radius)
                {
                    continue;
                }

                roads++;
                densitySum += seg.m_trafficDensity;
                if (seg.m_trafficDensity > 0)
                {
                    segs.Add(new KeyValuePair<int, ushort>(seg.m_trafficDensity, (ushort)i));
                }
            }

            segs.Sort((a, b) => b.Key.CompareTo(a.Key));

            var sb = new StringBuilder("{\"ok\":true");
            sb.Append(",\"flow\":").Append(vm.m_lastTrafficFlow);
            sb.Append(",\"cars\":").Append(cars).Append(",\"blocked\":").Append(blocked)
              .Append(",\"congestion\":").Append(congestion);
            sb.Append(",\"roadSegments\":").Append(roads)
              .Append(",\"averageDensity\":").Append(roads > 0 ? densitySum / roads : 0);

            sb.Append(",\"busiest\":[");
            for (int i = 0; i < segs.Count && i < limit; i++)
            {
                var seg = nets.m_segments.m_buffer[segs[i].Value];
                var mid = seg.m_middlePosition;
                sb.Append(i > 0 ? "," : "").Append("{\"segment\":").Append(segs[i].Value)
                  .Append(",\"prefab\":").Append(Json.Str(seg.Info.name))
                  .Append(",\"x\":").Append(Mathf.RoundToInt(mid.x)).Append(",\"z\":").Append(Mathf.RoundToInt(mid.z))
                  .Append(",\"density\":").Append(segs[i].Key).Append('}');
            }

            sb.Append(']');

            var spots = new List<int[]>(cells.Values);
            spots.Sort((a, b) => b[0].CompareTo(a[0]));
            sb.Append(",\"blockedSpots\":[");
            for (int i = 0; i < spots.Count && i < limit; i++)
            {
                var c = spots[i];
                sb.Append(i > 0 ? "," : "").Append("{\"x\":").Append(c[1] / c[0]).Append(",\"z\":").Append(c[2] / c[0])
                  .Append(",\"blocked\":").Append(c[0]).Append('}');
            }

            return sb.Append("]}").ToString();
        }

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }
    }
}
