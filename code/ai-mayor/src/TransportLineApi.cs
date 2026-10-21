using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using ColossalFramework.Math;
using UnityEngine;

namespace AIMayor
{
    // 公共交通の路線(バス、地下鉄、鉄道、船、飛行機)を引く窓口(#82)。
    // 育てる期間に、大学卒の住む地区から博多のオフィスへ通えず、路線を引く道具もなかったため。
    // 手順はゲームの路線の道具(TransportTool)と同じ。停留所の位置を GetStopPosition と同じ計算で決め、
    // TransportManager.CreateLine で路線を作り、TransportLine.AddStop で停留所を足し、最初の停留所に戻して環状にする。
    // 台数は路線ごとの予算(m_budget、%)とサービスの予算の積で決まる(TransportLine.CalculateTargetVehicleCount)。
    public static class TransportLineApi
    {
        private const float BusStopSearch = 64f; // バス停を探す範囲(m)。点から最も近い道路の区間
        private const float StationSearch = 300f; // 駅を探す範囲(m)

        private static readonly Dictionary<string, TransportInfo.TransportType> Types =
            new Dictionary<string, TransportInfo.TransportType>
            {
                { "bus", TransportInfo.TransportType.Bus },
                { "metro", TransportInfo.TransportType.Metro },
                { "train", TransportInfo.TransportType.Train },
                { "ship", TransportInfo.TransportType.Ship },
                { "plane", TransportInfo.TransportType.Airplane },
            };

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/transport/line/create"] = Create;
            routes["/transport/lines"] = req => HttpBridge.OnMain(() => Lines(req));
            routes["/transport/types"] = req => HttpBridge.OnMain(TypesJson);
            routes["/transport/line"] = req => HttpBridge.OnMain(() => Detail(req));
            routes["/transport/line/remove"] = req => HttpBridge.OnSimulation(() => Remove(req));
            routes["/transport/line/budget"] = req => HttpBridge.OnSimulation(() => Budget(req));
        }

        // POST /transport/line/create?type=bus  本文: "x1,z1;x2,z2;..."(停留所・駅の位置の並び)
        // 最後の点のあと、最初の停留所に戻して環状にする。作れなかったら途中のものを消して断る
        private static string Create(HttpListenerRequest req)
        {
            TransportInfo.TransportType type;
            if (!Types.TryGetValue((req.QueryString["type"] ?? "").ToLowerInvariant(), out type))
            {
                return HttpBridge.Error("type must be bus / metro / train / ship / plane");
            }

            string body;
            using (var r = new StreamReader(req.InputStream, Encoding.UTF8))
            {
                body = r.ReadToEnd();
            }

            List<Vector3> points;
            try
            {
                points = NetApi.Parse(body);
            }
            catch (Exception e)
            {
                return HttpBridge.Error("bad points: " + e.Message);
            }

            if (points.Count < 2)
            {
                return HttpBridge.Error("need at least 2 stops");
            }

            return HttpBridge.OnSimulation(() => CreateOnSimulation(type, points));
        }

        // 路線の種類を選ぶ。GetTransportInfo は最初に読み込んだ1種類だけを返し、それが解禁前(DLCの種類など)のことがある(#82)。
        // ゲームの路線の道具の一覧と同じく、手で置ける種類のうち、解禁されたものを選ぶ。なければ GetTransportInfo の値
        // /transport/types  読み込まれた路線の種類と、解禁の様子(#82。バスが解禁前と判定された件を調べるため)
        private static string TypesJson()
        {
            var sb = new StringBuilder("{\"ok\":true,\"types\":[");
            int n = PrefabCollection<TransportInfo>.LoadedCount();
            bool first = true;
            for (uint i = 0; i < n; i++)
            {
                var t = PrefabCollection<TransportInfo>.GetLoaded(i);
                if (t == null)
                {
                    continue;
                }

                var m = t.GetUnlockMilestone();
                sb.Append(first ? "" : ",").Append("{\"name\":").Append(Json.Str(t.name))
                  .Append(",\"type\":").Append(Json.Str(t.m_transportType.ToString()))
                  .Append(",\"placement\":").Append(Json.Str(t.m_placementStyle.ToString()))
                  .Append(",\"milestone\":").Append(Json.Str(m != null ? m.name : null))
                  .Append(",\"unlocked\":").Append(ToolsModifierControl.IsUnlocked(m) ? "true" : "false")
                  .Append(",\"subServiceUnlocked\":").Append(ToolsModifierControl.IsUnlocked(t.GetSubService()) ? "true" : "false").Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // 種類が解禁されているか。ゲームの路線の道具と同じく、路線の種類の節目で決める。
        // 節目は「Bus Line Requirements」など、車庫や駅を建てると満たされる条件(#82 で確かめた)
        private static bool Unlocked(TransportInfo t)
        {
            return ToolsModifierControl.IsUnlocked(t.GetUnlockMilestone());
        }

        private static TransportInfo PickInfo(TransportInfo.TransportType type)
        {
            TransportInfo fallback = TransportManager.instance.GetTransportInfo(type);
            int n = PrefabCollection<TransportInfo>.LoadedCount();
            for (uint i = 0; i < n; i++)
            {
                var t = PrefabCollection<TransportInfo>.GetLoaded(i);
                if (t != null && t.m_transportType == type && t.m_placementStyle == ItemClass.Placement.Manual
                    && Unlocked(t))
                {
                    return t;
                }
            }

            return fallback;
        }

        private static string CreateOnSimulation(TransportInfo.TransportType type, List<Vector3> points)
        {
            var tm = TransportManager.instance;
            var info = PickInfo(type);
            if (info == null)
            {
                return HttpBridge.Error("this transport type is not available: " + type);
            }

            // 路線の種類が解禁されているか(ゲームの道具の一覧と同じ判定)
            if (!Unlocked(info))
            {
                var m = info.GetUnlockMilestone();
                return "{\"ok\":false,\"error\":\"this line type is not available yet. Build its depot or station first"
                    + " (Bus Depot for bus, a metro station for metro, a train station for train)\",\"milestone\":"
                    + Json.Str(m != null ? m.name : null) + "}";
            }

            // 先に停留所の位置をすべて決める。決められない点があれば、路線を作らずに断る
            var stops = new List<Vector3>();
            var fixedPlatforms = new List<bool>();
            var where = new List<string>();
            for (int i = 0; i < points.Count; i++)
            {
                Vector3 pos;
                bool fixedPlatform;
                string what;
                string error = type == TransportInfo.TransportType.Bus
                    ? BusStop(info, points[i], out pos, out fixedPlatform, out what)
                    : StationStop(info, points[i], out pos, out fixedPlatform, out what);
                if (error != null)
                {
                    return "{\"ok\":false,\"error\":" + Json.Str("stop " + i + ": " + error) + ",\"index\":" + i + "}";
                }

                stops.Add(pos);
                fixedPlatforms.Add(fixedPlatform);
                where.Add(what);
            }

            ushort line;
            Randomizer rnd = SimulationManager.instance.m_randomizer;
            if (!tm.CreateLine(out line, ref rnd, info, true))
            {
                return HttpBridge.Error("CreateLine failed (too many lines?)");
            }

            for (int i = 0; i < stops.Count; i++)
            {
                if (!tm.m_lines.m_buffer[line].AddStop(line, -1, stops[i], fixedPlatforms[i]))
                {
                    tm.ReleaseLine(line);
                    return "{\"ok\":false,\"error\":" + Json.Str("AddStop failed at stop " + i + " (same position as the previous stop, or no lane)") + ",\"index\":" + i + "}";
                }
            }

            // 最初の停留所の位置に足すと、ゲームが環状にして完成の印(Complete)を付ける
            var first = NetManager.instance.m_nodes.m_buffer[tm.m_lines.m_buffer[line].m_stops].m_position;
            if (!tm.m_lines.m_buffer[line].AddStop(line, -1, first, fixedPlatforms[0]) || !tm.m_lines.m_buffer[line].Complete)
            {
                tm.ReleaseLine(line);
                return HttpBridge.Error("could not close the loop back to the first stop");
            }

            tm.UpdateLine(line);
            var sb = new StringBuilder("{\"ok\":true,\"line\":").Append(line)
                .Append(",\"number\":").Append(tm.m_lines.m_buffer[line].m_lineNumber)
                .Append(",\"type\":").Append(Json.Str(type.ToString().ToLowerInvariant() == "airplane" ? "plane" : type.ToString().ToLowerInvariant()))
                .Append(",\"stops\":[");
            ushort stop = tm.m_lines.m_buffer[line].m_stops;
            for (int i = 0; i < stops.Count && stop != 0; i++)
            {
                var p = NetManager.instance.m_nodes.m_buffer[stop].m_position;
                sb.Append(i > 0 ? "," : "").Append("{\"index\":").Append(i).Append(",\"x\":").Append(Mathf.RoundToInt(p.x))
                  .Append(",\"z\":").Append(Mathf.RoundToInt(p.z)).Append(',').Append(where[i]).Append('}');
                stop = TransportLine.GetNextStop(stop);
            }

            return sb.Append("],\"vehicles\":").Append(tm.m_lines.m_buffer[line].CountVehicles(line))
                .Append(",\"targetVehicles\":").Append(tm.m_lines.m_buffer[line].CalculateTargetVehicleCount())
                .Append(",\"note\":\"paths are calculated over the next days. Check /transport/lines for pathFailed\"}").ToString();
        }

        // バス停: 点から最も近い、歩道と車の車線のある道路の区間に置く(GetStopPosition の区間の場合と同じ計算)
        private static string BusStop(TransportInfo info, Vector3 point, out Vector3 pos, out bool fixedPlatform, out string what)
        {
            pos = point;
            fixedPlatform = false;
            what = null;
            var nm = NetManager.instance;
            var segs = nm.m_segments.m_buffer;
            ushort best = 0;
            float bestD = BusStopSearch;
            for (int i = 1; i < segs.Length; i++)
            {
                if ((segs[i].m_flags & NetSegment.Flags.Created) == 0 || (segs[i].m_flags & NetSegment.Flags.Untouchable) != 0
                    || segs[i].Info == null || segs[i].Info.m_class.m_service != ItemClass.Service.Road
                    || (segs[i].Info.m_vehicleTypes & info.m_vehicleType) == 0)
                {
                    continue;
                }

                var mid = segs[i].m_middlePosition - point;
                mid.y = 0f;
                if (mid.sqrMagnitude > 250f * 250f)
                {
                    continue;
                }

                var c = segs[i].GetClosestPosition(point) - point;
                c.y = 0f;
                if (c.magnitude < bestD)
                {
                    bestD = c.magnitude;
                    best = (ushort)i;
                }
            }

            if (best == 0)
            {
                return "no road for a bus stop within " + BusStopSearch + "m";
            }

            Vector3 sidewalk;
            uint pedLane;
            int pedIndex;
            float pedOffset;
            if (!segs[best].GetClosestLanePosition(point, NetInfo.LaneType.Pedestrian, VehicleInfo.VehicleType.None, info.vehicleCategory, info.m_vehicleType,
                    out sidewalk, out pedLane, out pedIndex, out pedOffset))
            {
                return "the road " + best + " has no sidewalk for a stop";
            }

            Vector3 carPos;
            uint carLane;
            int carIndex;
            float carOffset;
            if (!segs[best].GetClosestLanePosition(sidewalk, NetInfo.LaneType.Vehicle | NetInfo.LaneType.TransportVehicle, info.m_vehicleType, info.vehicleCategory,
                    out carPos, out carLane, out carIndex, out carOffset))
            {
                return "the road " + best + " has no lane for buses";
            }

            var flags = (NetLane.Flags)nm.m_lanes.m_buffer[pedLane].m_flags & NetLane.Flags.Stops;
            if (flags != NetLane.Flags.None && info.m_stopFlag != NetLane.Flags.None && flags != info.m_stopFlag)
            {
                return "the sidewalk of road " + best + " already has another kind of stop";
            }

            float stopOffset = segs[best].Info.m_lanes[carIndex].m_stopOffset;
            if ((segs[best].m_flags & NetSegment.Flags.Invert) != 0)
            {
                stopOffset = -stopOffset;
            }

            Vector3 dir;
            nm.m_lanes.m_buffer[carLane].CalculateStopPositionAndDirection(128f / 255f, stopOffset, out pos, out dir);
            fixedPlatform = true;
            what = "\"segment\":" + best;
            return null;
        }

        // 駅・港・空港: 点から最も近い、その種類の路線を持つ建物の乗り場に置く(GetStopPosition の建物の場合と同じ計算)
        private static string StationStop(TransportInfo info, Vector3 point, out Vector3 pos, out bool fixedPlatform, out string what)
        {
            pos = point;
            fixedPlatform = false;
            what = null;
            var bs = BuildingManager.instance.m_buildings.m_buffer;
            ushort best = 0;
            float bestD = StationSearch * StationSearch;
            for (int i = 1; i < bs.Length; i++)
            {
                if ((bs[i].m_flags & Building.Flags.Created) == 0 || bs[i].Info == null || bs[i].m_parentBuilding != 0 || !Serves(bs[i].Info, info))
                {
                    continue;
                }

                var d = bs[i].m_position - point;
                d.y = 0f;
                if (d.sqrMagnitude < bestD)
                {
                    bestD = d.sqrMagnitude;
                    best = (ushort)i;
                }
            }

            if (best == 0)
            {
                return "no " + info.m_transportType + " station within " + StationSearch + "m. Place a station first";
            }

            Randomizer sim = SimulationManager.instance.m_randomizer;
            var vehicle = VehicleManager.instance.GetRandomVehicleInfo(ref sim, info.m_class.m_service, info.m_class.m_subService, info.m_class.m_level, info.m_vehicleType);
            if (vehicle == null)
            {
                return "no vehicle model for " + info.m_transportType;
            }

            // 乗り場の候補を12通り出し、点に最も近いものを使う(ゲームの道具と同じく乱数の種を0〜11にする)
            var b = bs[best].Info;
            Vector3 chosen = Vector3.zero;
            bool found = false;
            for (int k = 0; k < 12; k++)
            {
                var r = new Randomizer((ulong)k);
                Vector3 spawn, target;
                b.m_buildingAI.CalculateSpawnPosition(best, ref bs[best], ref r, vehicle, out spawn, out target);
                if (!found || Vector3.SqrMagnitude(spawn - point) < Vector3.SqrMagnitude(chosen - point))
                {
                    chosen = spawn;
                    found = true;
                }
            }

            pos = chosen;
            fixedPlatform = false;
            what = "\"building\":" + best + ",\"station\":" + Json.Str(b.name);
            return null;
        }

        private static bool Serves(BuildingInfo b, TransportInfo info)
        {
            var a = b.m_buildingAI.GetTransportLineInfo();
            var s = b.m_buildingAI.GetSecondaryTransportLineInfo();
            return (a != null && a.m_transportType == info.m_transportType && a.m_vehicleType == info.m_vehicleType)
                || (s != null && s.m_transportType == info.m_transportType && s.m_vehicleType == info.m_vehicleType);
        }

        // GET /transport/lines?type=bus  路線の一覧
        private static string Lines(HttpListenerRequest req)
        {
            string want = (req.QueryString["type"] ?? "").ToLowerInvariant();
            var tm = TransportManager.instance;
            var lines = tm.m_lines.m_buffer;
            var sb = new StringBuilder("{\"ok\":true,\"lines\":[");
            bool first = true;
            for (int i = 1; i < lines.Length; i++)
            {
                if ((lines[i].m_flags & TransportLine.Flags.Created) == 0 || (lines[i].m_flags & TransportLine.Flags.Temporary) != 0
                    || lines[i].Info == null)
                {
                    continue;
                }

                var t = lines[i].Info.m_transportType;
                string name = t == TransportInfo.TransportType.Airplane ? "plane" : t.ToString().ToLowerInvariant();
                if (want.Length > 0 && want != name)
                {
                    continue;
                }

                int failed, waiting;
                PathState((ushort)i, out failed, out waiting);
                var p = lines[i].m_passengers;
                sb.Append(first ? "" : ",").Append("{\"line\":").Append(i).Append(",\"number\":").Append(lines[i].m_lineNumber)
                  .Append(",\"type\":").Append(Json.Str(name))
                  .Append(",\"stops\":").Append(lines[i].CountStops((ushort)i))
                  .Append(",\"vehicles\":").Append(lines[i].CountVehicles((ushort)i))
                  .Append(",\"targetVehicles\":").Append(lines[i].CalculateTargetVehicleCount())
                  .Append(",\"budget\":").Append(lines[i].m_budget)
                  .Append(",\"passengers\":").Append(p.m_residentPassengers.m_averageCount + p.m_touristPassengers.m_averageCount)
                  .Append(",\"lengthKm\":").Append((lines[i].m_totalLength / 1000f).ToString("0.00", CultureInfo.InvariantCulture))
                  .Append(",\"complete\":").Append(lines[i].Complete ? "true" : "false")
                  .Append(",\"pathFailed\":").Append(failed).Append(",\"pathWaiting\":").Append(waiting).Append('}');
                first = false;
            }

            return sb.Append("]}").ToString();
        }

        // GET /transport/line?line=  路線を1本詳しく見る。停留所の座標の並びと、次の停留所までの道順の長さ(#82)。
        // 路線が14〜15kmに回り込んでいて、どこで遠回りしているか分からなかった。
        // 道順の長さは、ゲームが計算した道順(PathUnit)の点を、車線の上の位置でつないで測る(RouteLength)。
        // 道順がまだないときは、区間の m_averageLength(ゲームが直線の距離を入れておく)を使う
        // 道順(PathUnit の連なり)の長さ。各点は (区間, 車線の番号, 区間の上の位置 0〜255)。
        // その車線の上の位置を求め、始点 → 点の並び → 終点を直線でつないだ長さを返す。道順がなければ 0
        private static float RouteLength(uint path, Vector3 from, Vector3 to)
        {
            if (path == 0)
            {
                return 0f;
            }

            var units = PathManager.instance.m_pathUnits.m_buffer;
            var segs = NetManager.instance.m_segments.m_buffer;
            var lanes = NetManager.instance.m_lanes.m_buffer;
            float total = 0f;
            Vector3 prev = from;
            bool any = false;
            int guard = 0;
            while (path != 0 && guard++ < 4096)
            {
                int count = units[path].m_positionCount;
                for (int i = 0; i < count; i++)
                {
                    PathUnit.Position pos;
                    if (!units[path].GetPosition(i, out pos) || pos.m_segment == 0)
                    {
                        continue;
                    }

                    uint lane = segs[pos.m_segment].m_lanes;
                    for (int k = 0; k < pos.m_lane && lane != 0; k++)
                    {
                        lane = lanes[lane].m_nextLane;
                    }

                    if (lane == 0)
                    {
                        continue;
                    }

                    var p = lanes[lane].CalculatePosition(pos.m_offset * (1f / 255f));
                    total += new Vector2(p.x - prev.x, p.z - prev.z).magnitude;
                    prev = p;
                    any = true;
                }

                path = units[path].m_nextPathUnit;
            }

            if (!any)
            {
                return 0f;
            }

            return total + new Vector2(to.x - prev.x, to.z - prev.z).magnitude;
        }

        private static string Detail(HttpListenerRequest req)
        {
            ushort line;
            string error = Line(req, out line);
            if (error != null)
            {
                return HttpBridge.Error(error);
            }

            var nm = NetManager.instance;
            var tl = TransportManager.instance.m_lines.m_buffer[line];
            var sb = new StringBuilder("{\"ok\":true,\"line\":").Append(line).Append(",\"number\":").Append(tl.m_lineNumber)
                .Append(",\"lengthKm\":").Append((tl.m_totalLength / 1000f).ToString("0.00", CultureInfo.InvariantCulture))
                .Append(",\"stops\":[");
            ushort first = tl.m_stops;
            ushort stop = first;
            int guard = 0, index = 0;
            while (stop != 0 && guard++ < 1024)
            {
                var p = nm.m_nodes.m_buffer[stop].m_position;
                ushort next = TransportLine.GetNextStop(stop);
                sb.Append(index > 0 ? "," : "").Append("{\"index\":").Append(index)
                  .Append(",\"x\":").Append(Mathf.RoundToInt(p.x)).Append(",\"z\":").Append(Mathf.RoundToInt(p.z));
                for (int k = 0; k < 8; k++)
                {
                    ushort seg = nm.m_nodes.m_buffer[stop].GetSegment(k);
                    if (seg == 0 || nm.m_segments.m_buffer[seg].m_startNode != stop)
                    {
                        continue;
                    }

                    var f = nm.m_segments.m_buffer[seg].m_flags;
                    var q = nm.m_nodes.m_buffer[nm.m_segments.m_buffer[seg].m_endNode].m_position;
                    float straight = new Vector2(q.x - p.x, q.z - p.z).magnitude;
                    // 道順の長さは、ゲームが計算した道順(PathUnit の点の並び)を、車線の上の位置でたどって測る。
                    // 区間の m_averageLength は、確かめると直線の距離と同じ値のままだった(#82)
                    float path = RouteLength(nm.m_segments.m_buffer[seg].m_path, p, q);
                    if (path <= 0f)
                    {
                        path = nm.m_segments.m_buffer[seg].m_averageLength;
                    }
                    // 道順の長さ ÷ 直線の距離。大きいほど遠回り
                    sb.Append(",\"toNext\":{\"pathM\":").Append(Mathf.RoundToInt(path))
                      .Append(",\"straightM\":").Append(Mathf.RoundToInt(straight))
                      .Append(",\"detour\":").Append((straight > 1f ? path / straight : 1f).ToString("0.0", CultureInfo.InvariantCulture))
                      .Append(",\"pathFailed\":").Append((f & NetSegment.Flags.PathFailed) != 0 ? "true" : "false")
                      .Append(",\"waitingPath\":").Append((f & NetSegment.Flags.WaitingPath) != 0 ? "true" : "false").Append('}');
                    break;
                }

                sb.Append('}');
                index++;
                stop = next;
                if (stop == first)
                {
                    break;
                }
            }

            return sb.Append("]}").ToString();
        }

        // 路線の区間(停留所と停留所の間)のうち、道順が見つからなかった数と、まだ探している数
        private static void PathState(ushort line, out int failed, out int waiting)
        {
            failed = 0;
            waiting = 0;
            var nm = NetManager.instance;
            ushort first = TransportManager.instance.m_lines.m_buffer[line].m_stops;
            ushort stop = first;
            int guard = 0;
            while (stop != 0 && guard++ < 1024)
            {
                for (int k = 0; k < 8; k++)
                {
                    ushort seg = nm.m_nodes.m_buffer[stop].GetSegment(k);
                    if (seg != 0 && nm.m_segments.m_buffer[seg].m_startNode == stop)
                    {
                        var f = nm.m_segments.m_buffer[seg].m_flags;
                        if ((f & NetSegment.Flags.PathFailed) != 0) failed++;
                        if ((f & NetSegment.Flags.WaitingPath) != 0) waiting++;
                        break;
                    }
                }

                stop = TransportLine.GetNextStop(stop);
                if (stop == first)
                {
                    break;
                }
            }
        }

        // GET /transport/line/remove?line=  路線を消す
        private static string Remove(HttpListenerRequest req)
        {
            ushort line;
            string error = Line(req, out line);
            if (error != null)
            {
                return HttpBridge.Error(error);
            }

            TransportManager.instance.ReleaseLine(line);
            return "{\"ok\":true,\"removed\":" + line + "}";
        }

        // GET /transport/line/budget?line=&percent=  路線ごとの台数の割合(ゲームの路線の画面の台数の調整と同じ値)。
        // 台数 = サービスの予算(set_budget の bus など)× この割合 × 路線の長さ ÷ 車の間隔
        private static string Budget(HttpListenerRequest req)
        {
            ushort line;
            string error = Line(req, out line);
            if (error != null)
            {
                return HttpBridge.Error(error);
            }

            int percent;
            if (!int.TryParse(req.QueryString["percent"] ?? "", NumberStyles.Integer, CultureInfo.InvariantCulture, out percent))
            {
                return HttpBridge.Error("percent is required");
            }

            percent = Mathf.Clamp(percent, 10, 300);
            var tm = TransportManager.instance;
            tm.m_lines.m_buffer[line].m_budget = (ushort)percent;
            return "{\"ok\":true,\"line\":" + line + ",\"budget\":" + percent
                + ",\"targetVehicles\":" + tm.m_lines.m_buffer[line].CalculateTargetVehicleCount() + "}";
        }

        private static string Line(HttpListenerRequest req, out ushort line)
        {
            line = 0;
            int v;
            if (!int.TryParse(req.QueryString["line"] ?? "", NumberStyles.Integer, CultureInfo.InvariantCulture, out v) || v <= 0)
            {
                return "line is required (see /transport/lines)";
            }

            var lines = TransportManager.instance.m_lines.m_buffer;
            if (v >= lines.Length || (lines[v].m_flags & TransportLine.Flags.Created) == 0 || (lines[v].m_flags & TransportLine.Flags.Temporary) != 0)
            {
                return "no such line: " + v;
            }

            line = (ushort)v;
            return null;
        }
    }
}
