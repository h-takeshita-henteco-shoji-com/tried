using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;

namespace AIMayor
{
    // ゲーム画面のパネルに流す記録。3種類ある。
    // - 道具: AI市長が MCP 経由で呼んだ道具。MCP サーバーが /ui/command で開始と終了を知らせる
    // - 判断: AI市長が施策を打つ前に書く「何をするか(DO)」と「なぜするか(WHY)」。MCP サーバーが /ui/note で知らせる
    // - ダイアログ: ゲームに出た警告など。DialogWatch が見つけて足す
    // 同じ行をテキストファイルにも書き足す(LogDir)。受付スレッドとメインスレッドの両方が触るので、lock で守る。
    public static class CommandLog
    {
        public static readonly string LogDir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.Personal),
            "Library/Application Support/Colossal Order/Cities_Skylines/AIMayor/logs");

        private class Entry
        {
            public string Id;
            public DateTime At;
            public string GameDate;
            public string Kind; // tool / note / dialog
            public string Tool;
            public string Args;
            public string State; // running / ok / error
            public string Detail;
            public string Action; // note の DO
            public string Reason; // note の WHY
        }

        private const int Max = 100;
        private static readonly List<Entry> entries = new List<Entry>();
        private static int version;
        private static bool newStart;
        private static string logPath;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            // /ui/command?phase=start&id=..&tool=..&args=..
            // /ui/command?phase=end&id=..&ok=true|false&detail=..
            routes["/ui/command"] = Receive;
            // /ui/note?action=..&reason=..  判断。日本語は UTF-8 の URL エンコードで送る
            routes["/ui/note"] = ReceiveNote;
            // /ui/log  今のログファイルの場所
            routes["/ui/log"] = req =>
            {
                lock (entries)
                {
                    return "{\"ok\":true,\"path\":" + Json.Str(logPath) + "}";
                }
            };
        }

        // 街を開いたときに呼ぶ。ログファイルを新しく始める(街を開くたびに1ファイル)
        public static void StartLogFile(string city)
        {
            lock (entries)
            {
                try
                {
                    Directory.CreateDirectory(LogDir);
                    logPath = Path.Combine(LogDir, DateTime.Now.ToString("yyyyMMdd-HHmmss", CultureInfo.InvariantCulture) + ".txt");
                    File.AppendAllText(logPath, "# AI Mayor log  city=" + city + "  started=" + Now() + "\n"
                        + "# 実時間\tゲーム内の日付\t種類\t内容\n", Encoding.UTF8);
                }
                catch (Exception e)
                {
                    UnityEngine.Debug.Log("[AIMayor] log file: " + e.Message);
                    logPath = null;
                }
            }
        }

        // 記録が変わるたびに増える番号。パネルは変わったときだけ描き直す
        public static int Version
        {
            get
            {
                lock (entries)
                {
                    return version;
                }
            }
        }

        // 前回呼んでから新しい行が増えたか(閉じたパネルを開き直す合図)
        public static bool TakeNewStart()
        {
            lock (entries)
            {
                bool b = newStart;
                newStart = false;
                return b;
            }
        }

        public static void AddDialog(string name, string title)
        {
            var e = new Entry { Kind = "dialog", Tool = name, Args = title, State = "dialog" };
            Add(e);
            Write(e, "DIALOG", name + ": " + title);
        }

        // 新しいものを上にして、最後の n 件を返す。色はパネルのマークアップで付ける
        public static string Render(int n)
        {
            var sb = new StringBuilder();
            lock (entries)
            {
                for (int i = entries.Count - 1; i >= Math.Max(0, entries.Count - n); i--)
                {
                    var e = entries[i];
                    string time = "<color #a0a0a0>" + e.At.ToString("HH:mm:ss", CultureInfo.InvariantCulture) + "</color> ";
                    if (e.Kind == "note")
                    {
                        sb.Append(time).Append("<color #ffffff>DO ").Append(Plain(e.Action)).Append("</color>\n");
                        if (!string.IsNullOrEmpty(e.Reason))
                        {
                            sb.Append("<color #6fc8ff>         WHY ").Append(Plain(e.Reason)).Append("</color>\n");
                        }

                        continue;
                    }

                    sb.Append(time);
                    if (e.Kind == "dialog")
                    {
                        sb.Append("<color #ff9f40>DIALOG ").Append(Plain(e.Tool)).Append(": ").Append(Plain(e.Args)).Append("</color>\n");
                        continue;
                    }

                    switch (e.State)
                    {
                        case "ok": sb.Append("<color #7fd47f>OK</color> "); break;
                        case "error": sb.Append("<color #ff7070>NG</color> "); break;
                        default: sb.Append("<color #ffd24d>..</color> "); break;
                    }

                    sb.Append("<color #c8c8c8>").Append(Plain(e.Tool));
                    if (!string.IsNullOrEmpty(e.Args))
                    {
                        sb.Append(' ').Append(Plain(e.Args));
                    }

                    sb.Append("</color>");
                    if (!string.IsNullOrEmpty(e.Detail))
                    {
                        string color = e.State == "error" ? "#ff7070" : "#a0a0a0";
                        sb.Append(" <color ").Append(color).Append('>').Append(Plain(e.Detail)).Append("</color>");
                    }

                    sb.Append('\n');
                }
            }

            return sb.ToString();
        }

        private static void Add(Entry e)
        {
            e.At = DateTime.Now;
            e.GameDate = GameDate();
            lock (entries)
            {
                entries.Add(e);
                if (entries.Count > Max)
                {
                    entries.RemoveAt(0);
                }

                newStart = true;
                version++;
            }
        }

        private static string Receive(HttpListenerRequest req)
        {
            var q = req.QueryString;
            string id = q["id"] ?? "";
            if (q["phase"] == "end")
            {
                Entry done = null;
                lock (entries)
                {
                    done = entries.FindLast(x => x.Kind == "tool" && x.Id == id);
                    if (done != null)
                    {
                        done.State = q["ok"] == "true" ? "ok" : "error";
                        done.Detail = q["detail"];
                    }

                    version++;
                }

                // 道具の行は、終わったときに成否つきで1行だけ書く
                if (done != null)
                {
                    Write(done, done.State == "ok" ? "OK" : "NG",
                        done.Tool + (string.IsNullOrEmpty(done.Args) ? "" : " " + done.Args) + (string.IsNullOrEmpty(done.Detail) ? "" : "  -> " + done.Detail));
                }
            }
            else
            {
                Add(new Entry { Kind = "tool", Id = id, Tool = q["tool"] ?? "?", Args = q["args"], State = "running" });
            }

            return "{\"ok\":true}";
        }

        private static string ReceiveNote(HttpListenerRequest req)
        {
            // QueryString の復号は環境によって UTF-8 にならないので、生の URL から自分で復号する
            string action = Query(req.Url.Query, "action") ?? Query(req.Url.Query, "text");
            string reason = Query(req.Url.Query, "reason");
            if (string.IsNullOrEmpty(action))
            {
                return HttpBridge.Error("action is required");
            }

            var e = new Entry { Kind = "note", Action = action, Reason = reason, State = "note" };
            Add(e);
            Write(e, "DO", action);
            if (!string.IsNullOrEmpty(reason))
            {
                Write(e, "WHY", reason);
            }

            return "{\"ok\":true}";
        }

        // ログファイルに1行書き足す。書けなくてもパネルの表示は止めない
        private static void Write(Entry e, string kind, string text)
        {
            lock (entries)
            {
                if (logPath == null)
                {
                    return;
                }

                try
                {
                    File.AppendAllText(logPath, e.At.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture) + "\t" + e.GameDate
                        + "\t" + kind + "\t" + (text ?? "").Replace("\n", " ").Replace("\t", " ") + "\n", Encoding.UTF8);
                }
                catch (Exception ex)
                {
                    UnityEngine.Debug.Log("[AIMayor] log write: " + ex.Message);
                }
            }
        }

        private static string Query(string query, string key)
        {
            foreach (var part in query.TrimStart('?').Split('&'))
            {
                int eq = part.IndexOf('=');
                if (eq > 0 && part.Substring(0, eq) == key)
                {
                    return Uri.UnescapeDataString(part.Substring(eq + 1).Replace('+', ' '));
                }
            }

            return null;
        }

        private static string GameDate()
        {
            try
            {
                return SimulationManager.instance.m_currentGameTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
            }
            catch (Exception)
            {
                return "-";
            }
        }

        private static string Now()
        {
            return DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss", CultureInfo.InvariantCulture);
        }

        // マークアップの記号として読まれないようにする
        private static string Plain(string s)
        {
            return s == null ? "" : s.Replace("<", "(").Replace(">", ")").Replace("\n", " ");
        }
    }
}
