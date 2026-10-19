using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using ColossalFramework.IO;
using ColossalFramework.UI;

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

            var t0 = DateTime.Now;
            while ((DateTime.Now - t0).TotalSeconds < 60)
            {
                Thread.Sleep(500);
                if (!SavePanel.isSaving && File.Exists(path) && File.GetLastWriteTime(path) > before)
                {
                    var f = new FileInfo(path);
                    return "{\"ok\":true,\"name\":" + Json.Str(name) + ",\"path\":" + Json.Str(path)
                        + ",\"gameDate\":" + Json.Str(date) + ",\"sizeMB\":"
                        + (f.Length / 1048576.0).ToString("0.0", CultureInfo.InvariantCulture)
                        + ",\"seconds\":" + (DateTime.Now - t0).TotalSeconds.ToString("0.0", CultureInfo.InvariantCulture) + "}";
                }
            }

            return HttpBridge.Error("save did not finish in 60 seconds (isSaving=" + SavePanel.isSaving + ")");
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
