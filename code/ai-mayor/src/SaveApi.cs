using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using ColossalFramework.IO;
using ColossalFramework.UI;
using UnityEngine;

namespace AIMayor
{
    // 街を保存する窓口。本番は任期が長く、途中で止めて再開するため(#72、#77)。
    // ゲームの保存の画面と同じ処理(SavePanel.SaveGame)を呼ぶ。読み込みは人が行う。
    public static class SaveApi
    {
        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/save"] = Save;
            routes["/saves"] = req => List();
            routes["/sim/health"] = req => Health();
            // 試験用(MCP の道具にはしない)。計算スレッドを、一時停止が解けるまで(最大 ms)ふさぐ。
            // 一時停止のまま保存が止まる様子と、時間切れの命令の取り消しを、狙って起こすため
            routes["/sim/test/block"] = req =>
            {
                int ms;
                int.TryParse(req.QueryString["ms"] ?? "15000", out ms);
                SimulationManager.instance.AddAction(() =>
                {
                    var t = DateTime.Now;
                    while (SimulationManager.instance.SimulationPaused && (DateTime.Now - t).TotalMilliseconds < ms)
                    {
                        Thread.Sleep(50);
                    }
                });
                return "{\"ok\":true,\"blockingMs\":" + ms + "}";
            };
        }

        // /save?name=fukuoka-base-2027-01&overwrite=false
        // 保存が終わるまで待ってから返す(最大60秒)
        private static string Save(HttpListenerRequest req)
        {
            string name = (req.QueryString["name"] ?? "").Trim();
            if (name.Length == 0 || name.IndexOfAny(Path.GetInvalidFileNameChars()) >= 0 || name.IndexOf('/') >= 0)
            {
                return HttpBridge.Error("name is empty or has characters that cannot be used in a file name");
            }

            string path = Path.Combine(DataLocation.saveLocation, name + ".crp");
            bool overwrite = req.QueryString["overwrite"] == "true";
            if (File.Exists(path) && !overwrite)
            {
                return HttpBridge.Error("a save with this name already exists (use overwrite=true): " + path);
            }

            DateTime before = File.Exists(path) ? File.GetLastWriteTime(path) : DateTime.MinValue;
            string date = null;
            string started = HttpBridge.OnMain(() =>
            {
                if (LoadingManager.instance.m_currentlyLoading)
                {
                    return HttpBridge.Error("the game is loading");
                }

                if (SavePanel.isSaving)
                {
                    return HttpBridge.Error("another save is in progress");
                }

                var panel = UIView.library.Get<SavePanel>("SavePanel");
                if (panel == null)
                {
                    return HttpBridge.Error("save panel not found");
                }

                date = SimulationManager.instance.m_currentGameTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
                return panel.SaveGame(name) ? "{\"ok\":true}" : HttpBridge.Error("the game refused to save");
            });
            if (!started.StartsWith("{\"ok\":true", StringComparison.Ordinal))
            {
                return started;
            }

            // 一時停止のまま保存が終わらないことがある(#81 で2回。節目のダイアログを閉じた直後)。
            // ゲームの保存は、水のシミュレーションが計算に追いつくのを待つ(WaterSimulation.Data.Serialize)。
            // 水の処理は描画の進みも待つため、一時停止のままだと追いつかずに止まることがある。
            // そのときは一時停止を解いて描画を進め、保存の直後に計算スレッドの上で止め直す。
            // 止め直しは保存と同じ待ち行列に入れるので、保存が終わってから時間が進む前に効く。ゲーム内の時間は進まない
            var t0 = DateTime.Now;
            bool nudged = false;
            while ((DateTime.Now - t0).TotalSeconds < 60)
            {
                Thread.Sleep(500);
                if (!SavePanel.isSaving && File.Exists(path) && File.GetLastWriteTime(path) > before)
                {
                    var f = new FileInfo(path);
                    return "{\"ok\":true,\"name\":" + Json.Str(name) + ",\"path\":" + Json.Str(path)
                        + ",\"gameDate\":" + Json.Str(date) + ",\"sizeMB\":"
                        + (f.Length / 1048576.0).ToString("0.0", CultureInfo.InvariantCulture)
                        + ",\"seconds\":" + (DateTime.Now - t0).TotalSeconds.ToString("0.0", CultureInfo.InvariantCulture)
                        + ",\"nudged\":" + (nudged ? "true" : "false") + "}";
                }

                if (!nudged && (DateTime.Now - t0).TotalSeconds >= 3)
                {
                    nudged = Nudge();
                }
            }

            return HttpBridge.Error("save did not finish in 60 seconds (isSaving=" + SavePanel.isSaving + ", nudged=" + nudged + ")");
        }

        // 保存が計算スレッドで止まっていて、一時停止中なら、一時停止を解き、保存の直後に止め直す。解いたら true
        private static bool Nudge()
        {
            string r = HttpBridge.OnMain(() =>
            {
                var sim = SimulationManager.instance;
                var task = LoadSaveStatus.activeTask;
                if (!sim.SimulationPaused || task == null || task.completedOrFailed)
                {
                    return "no";
                }

                sim.AddAction(() => { sim.SimulationPaused = true; });
                sim.SimulationPaused = false;
                return "yes";
            });
            if (r == "yes")
            {
                CommandLog.AddDialog("SaveNudge", "save was stuck while paused; unpaused until the save finished");
                return true;
            }

            return false;
        }

        // /sim/health  計算スレッドが命令を受け付けるか(1秒以内に空の命令が終わるか)と、保存・水の処理の様子。
        // 道具が時間切れになったときの切り分けに使う
        private static string Health()
        {
            var t0 = DateTime.Now;
            string ping = HttpBridge.OnSimulation(() => "{\"ok\":true}", 1000);
            bool alive = ping.StartsWith("{\"ok\":true", StringComparison.Ordinal);
            double ms = (DateTime.Now - t0).TotalMilliseconds;
            return HttpBridge.OnMain(() =>
            {
                var sim = SimulationManager.instance;
                var task = LoadSaveStatus.activeTask;
                var water = TerrainManager.instance.WaterSimulation;
                return "{\"ok\":true,\"simulationResponds\":" + (alive ? "true" : "false")
                    + ",\"pingMs\":" + Mathf.RoundToInt((float)ms)
                    + ",\"paused\":" + (sim.SimulationPaused ? "true" : "false")
                    + ",\"forcedPaused\":" + (sim.ForcedSimulationPaused ? "true" : "false")
                    + ",\"saving\":" + (SavePanel.isSaving ? "true" : "false")
                    + ",\"activeTask\":" + Json.Str(task != null && !task.completedOrFailed ? task.name : null)
                    + ",\"frame\":" + sim.m_currentFrameIndex
                    + ",\"waterFrame\":" + Field(water, "m_waterFrameIndex")
                    + ",\"waterTargetFrame\":" + Field(water, "m_simulationFrameIndex") + "}";
            });
        }

        private static string Field(object o, string name)
        {
            var f = o.GetType().GetField(name, System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance);
            return f != null ? Convert.ToString(f.GetValue(o), CultureInfo.InvariantCulture) : "null";
        }

        // /saves  保存した街の一覧(新しい順)
        private static string List()
        {
            var dir = new DirectoryInfo(DataLocation.saveLocation);
            var files = new List<FileInfo>(dir.Exists ? dir.GetFiles("*.crp") : new FileInfo[0]);
            files.Sort((a, b) => b.LastWriteTime.CompareTo(a.LastWriteTime));
            var sb = new StringBuilder("{\"ok\":true,\"dir\":").Append(Json.Str(dir.FullName)).Append(",\"saves\":[");
            for (int i = 0; i < files.Count; i++)
            {
                var f = files[i];
                sb.Append(i > 0 ? "," : "").Append("{\"name\":").Append(Json.Str(Path.GetFileNameWithoutExtension(f.Name)))
                  .Append(",\"savedAt\":").Append(Json.Str(f.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture)))
                  .Append(",\"sizeMB\":").Append((f.Length / 1048576.0).ToString("0.0", CultureInfo.InvariantCulture)).Append('}');
            }

            return sb.Append("]}").ToString();
        }
    }
}
