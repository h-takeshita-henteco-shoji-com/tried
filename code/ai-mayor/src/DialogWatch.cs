using System;
using System.Collections.Generic;
using System.Globalization;
using System.Net;
using System.Text;
using ColossalFramework.UI;
using UnityEngine;

namespace AIMayor
{
    // ゲームの画面に出たダイアログ(破産の警告など、画面を止める窓)を記録する。
    // AI市長は画面を見られないので、見出し・本文・ボタンの文字を JSON にして渡す。
    //
    // 知る方法は2つ。
    // - Harmony があれば、ダイアログを開く・閉じる関数に差し込んだ処理から知らされる(Patcher)
    // - なければ、DialogWatcher が1秒ごとに見に行く
    // 開いたダイアログには連番を振って履歴に残す。見回りの合間に開いて閉じたものも、後から受け取れる。
    public static class DialogWatch
    {
        private class Record
        {
            public int Seq;
            public string Json; // 中身(name, type, texts, buttons)
            public string OpenedAt; // ゲーム内の日付
            public string ClosedAt;
            public UIComponent Component;
        }

        private const int MaxHistory = 50;
        private const int MaxReadTries = 30;

        private static readonly object gate = new object();
        private static readonly List<Record> history = new List<Record>();
        private static Record current;
        private static int seq;

        // 開いた直後は本文がまだ入っていないことがあるので、次のフレームから読む
        private static UIComponent pending;
        private static int pendingTries;

        // Harmony の差し込みが効いているか。Patcher が書く
        public static bool HooksActive;

        public static void Register(Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            // /ui/dialog  今出ているダイアログと、最新の連番
            routes["/ui/dialog"] = req => "{\"ok\":true,\"harmony\":" + (HooksActive ? "true" : "false")
                + ",\"seq\":" + Seq + ",\"dialog\":" + Current + "}";
            // /ui/dialog/events?since=連番  その連番より後に開いたダイアログ(閉じたものも含む)
            routes["/ui/dialog/events"] = Events;
            // /ui/dialog/test?close=false  試験用。ゲーム内蔵のメッセージの窓を開く(close=true で閉じる)。MCP の道具にはしない
            routes["/ui/dialog/test"] = req => HttpBridge.OnMain(() => Test(req.QueryString["close"] == "true"));
        }

        // 今出ているダイアログの JSON。なければ "null"
        public static string Current
        {
            get
            {
                lock (gate)
                {
                    return current != null ? Entry(current) : "null";
                }
            }
        }

        // 最後に開いたダイアログの連番。0 はまだ1つも開いていない
        public static int Seq
        {
            get
            {
                lock (gate)
                {
                    return seq;
                }
            }
        }

        // Harmony の差し込みから呼ばれる(メインスレッド)
        public static void OnPushed(UIComponent c)
        {
            if (c == null || c is CommandPanel)
            {
                return;
            }

            pending = c;
            pendingTries = 0;
        }

        // Harmony の差し込みから呼ばれる(メインスレッド)。閉じた後に一番上に残る画面を確かめる
        public static void OnPopped()
        {
            UIComponent top = UIView.HasModalInput() ? UIView.GetModalComponent() : null;
            lock (gate)
            {
                if (current != null && current.Component != top)
                {
                    current.ClosedAt = GameDate();
                    current = null;
                }
            }

            if (top != null && pending == null && !IsCurrent(top))
            {
                OnPushed(top); // 下に隠れていた別のダイアログが見えるようになった
            }
        }

        // DialogWatcher から毎フレーム呼ぶ。開いたばかりのダイアログの文字を読む
        public static void ReadPending()
        {
            if (pending == null)
            {
                return;
            }

            pendingTries++;
            var c = pending;
            List<string> texts, buttons;
            Collect(c, out texts, out buttons);

            // 本文が入るまで少し待つ。待ちきれなければ、読めた分だけで記録する
            if (texts.Count == 0 && pendingTries < MaxReadTries)
            {
                return;
            }

            pending = null;
            Open(c, texts, buttons);
        }

        // Harmony がないときの見回り。1秒ごとに DialogWatcher から呼ぶ
        public static void Poll()
        {
            UIComponent modal = UIView.HasModalInput() ? UIView.GetModalComponent() : null;
            if (modal == null || !modal.isVisible || modal is CommandPanel)
            {
                lock (gate)
                {
                    if (current != null)
                    {
                        current.ClosedAt = GameDate();
                        current = null;
                    }
                }

                return;
            }

            if (!IsCurrent(modal) && pending == null)
            {
                OnPushed(modal);
            }
        }

        private static string Test(bool close)
        {
            if (close)
            {
                UIView.library.Hide("ExceptionPanel");
                return "{\"ok\":true,\"closed\":true}";
            }

            UIView.library.ShowModal<ExceptionPanel>("ExceptionPanel").SetMessage("AI Mayor test", "Dialog hook test", false);
            return "{\"ok\":true,\"opened\":true}";
        }

        private static bool IsCurrent(UIComponent c)
        {
            lock (gate)
            {
                return current != null && current.Component == c;
            }
        }

        private static void Open(UIComponent c, List<string> texts, List<string> buttons)
        {
            var sb = new StringBuilder("{\"name\":").Append(Json.Str(c.name));
            sb.Append(",\"type\":").Append(Json.Str(c.GetType().Name));
            sb.Append(",\"texts\":").Append(Array(texts));
            sb.Append(",\"buttons\":").Append(Array(buttons)).Append('}');

            lock (gate)
            {
                seq++;
                current = new Record { Seq = seq, Json = sb.ToString(), OpenedAt = GameDate(), Component = c };
                history.Add(current);
                if (history.Count > MaxHistory)
                {
                    history.RemoveAt(0);
                }
            }

            // パネルには画面の名前を出す(型は UIPanel のことが多く、区別できない)
            CommandLog.AddDialog(c.name.Replace("(Library) ", ""), texts.Count > 0 ? texts[0] : c.name);
        }

        private static void Collect(UIComponent c, out List<string> texts, out List<string> buttons)
        {
            texts = new List<string>();
            buttons = new List<string>();
            foreach (var label in c.GetComponentsInChildren<UILabel>())
            {
                if (label.isVisible && !string.IsNullOrEmpty(label.text) && !texts.Contains(label.text))
                {
                    texts.Add(label.text);
                }
            }

            foreach (var button in c.GetComponentsInChildren<UIButton>())
            {
                if (button.isVisible && !string.IsNullOrEmpty(button.text))
                {
                    buttons.Add(button.text);
                }
            }
        }

        private static string Events(HttpListenerRequest req)
        {
            int since;
            int.TryParse(req.QueryString["since"] ?? "0", NumberStyles.Integer, CultureInfo.InvariantCulture, out since);
            var sb = new StringBuilder();
            lock (gate)
            {
                sb.Append("{\"ok\":true,\"harmony\":").Append(HooksActive ? "true" : "false");
                sb.Append(",\"seq\":").Append(seq).Append(",\"events\":[");
                bool first = true;
                foreach (var r in history)
                {
                    if (r.Seq <= since)
                    {
                        continue;
                    }

                    sb.Append(first ? "" : ",").Append(Entry(r));
                    first = false;
                }
            }

            return sb.Append("]}").ToString();
        }

        // 1件の JSON。中身に、連番・開いた日・閉じた日を足す
        private static string Entry(Record r)
        {
            return "{\"seq\":" + r.Seq + ",\"openedAt\":" + Json.Str(r.OpenedAt) + ",\"closedAt\":" + Json.Str(r.ClosedAt)
                + "," + r.Json.Substring(1);
        }

        private static string Array(List<string> items)
        {
            var sb = new StringBuilder("[");
            for (int i = 0; i < items.Count; i++)
            {
                sb.Append(i > 0 ? "," : "").Append(Json.Str(items[i]));
            }

            return sb.Append(']').ToString();
        }

        private static string GameDate()
        {
            return SimulationManager.instance.m_currentGameTime.ToString("yyyy-MM-dd", CultureInfo.InvariantCulture);
        }
    }

    // 毎フレーム動く見張り。ThreadingExtension はダイアログや一時停止の間に止まることがあるので、
    // Unity の Update で、HTTP から頼まれた処理、パネルの描き直し、ダイアログの読み取りを回す。
    public class DialogWatcher : MonoBehaviour
    {
        private static GameObject host;
        private float next;

        public static void Create()
        {
            if (host == null)
            {
                host = new GameObject("AIMayorDialogWatcher");
                host.AddComponent<DialogWatcher>();
            }
        }

        public static void DestroyWatcher()
        {
            if (host != null)
            {
                UnityEngine.Object.Destroy(host);
                host = null;
            }
        }

        public void Update()
        {
            HttpBridge.DrainMainQueue();
            CommandPanel.Tick();
            try
            {
                DialogWatch.ReadPending();

                // Harmony が効いていれば知らされるので、見に行かない
                if (!DialogWatch.HooksActive && Time.realtimeSinceStartup >= next)
                {
                    next = Time.realtimeSinceStartup + 1f;
                    DialogWatch.Poll();
                }
            }
            catch (Exception e)
            {
                Debug.Log("[AIMayor] dialog watch: " + e.Message);
            }
        }
    }
}
