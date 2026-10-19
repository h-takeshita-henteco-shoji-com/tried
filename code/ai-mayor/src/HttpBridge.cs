using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using ICities;
using UnityEngine;

namespace AIMayor
{
    // 自分のパソコン(127.0.0.1)からだけ受け付ける HTTP の窓口。MCP サーバーがここを呼ぶ。
    // 受付は別スレッドで行い、ゲームの中身に触る処理はメインスレッドに渡して、終わるまで待つ。
    public static class HttpBridge
    {
        public const string Prefix = "http://127.0.0.1:8781/";

        private static HttpListener listener;
        private static Thread thread;

        // メインスレッドで実行してほしい処理の待ち行列
        private static readonly Queue<Action> mainQueue = new Queue<Action>();

        // パスごとの処理。戻り値は JSON 文字列
        private static readonly Dictionary<string, Func<HttpListenerRequest, string>> routes =
            new Dictionary<string, Func<HttpListenerRequest, string>>();

        public static void Start()
        {
            if (listener != null)
            {
                return;
            }

            routes["/ping"] = req => "{\"ok\":true,\"mod\":\"AIMayor\"}";
            routes["/info"] = req => OnMain(GameInfo.Read);
            ViewApi.Register(routes);
            NetApi.Register(routes);
            CityApi.Register(routes);
            CitizenApi.Register(routes);
            EconomyApi.Register(routes);
            EditorApi.Register(routes);
            CommandLog.Register(routes);
            DialogWatch.Register(routes);
            SaveApi.Register(routes);
            TrafficApi.Register(routes);
            NetworkApi.Register(routes);
            MapApi.Register(routes);

            listener = new HttpListener();
            listener.Prefixes.Add(Prefix);
            listener.Start();
            thread = new Thread(Loop) { IsBackground = true, Name = "AIMayor.HttpBridge" };
            thread.Start();
            Debug.Log("[AIMayor] HTTP bridge listening on " + Prefix);
        }

        public static void Stop()
        {
            if (listener == null)
            {
                return;
            }

            try
            {
                listener.Stop();
                listener.Close();
            }
            catch (Exception e)
            {
                Debug.Log("[AIMayor] HTTP bridge stop: " + e.Message);
            }

            listener = null;
            thread = null;
            Debug.Log("[AIMayor] HTTP bridge stopped");
        }

        // メインスレッドから毎フレーム呼ぶ
        public static void DrainMainQueue()
        {
            while (true)
            {
                Action a;
                lock (mainQueue)
                {
                    if (mainQueue.Count == 0)
                    {
                        return;
                    }

                    a = mainQueue.Dequeue();
                }

                a();
            }
        }

        // 処理をメインスレッドで実行し、結果を待って返す(最大5秒)
        public static string OnMain(Func<string> work)
        {
            string result = null;
            Exception error = null;
            var done = new ManualResetEvent(false);
            lock (mainQueue)
            {
                mainQueue.Enqueue(() =>
                {
                    try
                    {
                        result = work();
                    }
                    catch (Exception e)
                    {
                        error = e;
                    }
                    finally
                    {
                        done.Set();
                    }
                });
            }

            if (!done.WaitOne(5000))
            {
                return Error("main thread timeout (is the game paused in a menu?)");
            }

            return error != null ? Error(error.Message) : result;
        }

        // 処理をゲームの計算スレッド(シミュレーション)で実行し、結果を待って返す(最大10秒)。
        // 道路や建物を作る処理は、このスレッドで行う決まり。
        public static string OnSimulation(Func<string> work)
        {
            return OnSimulation(work, 10000);
        }

        // 時間のかかる処理(木をたくさん植えるなど)は、待つ時間を延ばす
        public static string OnSimulation(Func<string> work, int timeoutMs)
        {
            string result = null;
            Exception error = null;
            var done = new ManualResetEvent(false);
            SimulationManager.instance.AddAction(() =>
            {
                try
                {
                    result = work();
                }
                catch (Exception e)
                {
                    error = e;
                }
                finally
                {
                    done.Set();
                }
            });

            if (!done.WaitOne(timeoutMs))
            {
                return Error("simulation thread timeout");
            }

            return error != null ? Error(error.ToString()) : result;
        }

        private static void Loop()
        {
            while (listener != null && listener.IsListening)
            {
                HttpListenerContext ctx;
                try
                {
                    ctx = listener.GetContext();
                }
                catch (Exception)
                {
                    return; // Stop() で閉じられた
                }

                ThreadPool.QueueUserWorkItem(_ => Handle(ctx));
            }
        }

        private static void Handle(HttpListenerContext ctx)
        {
            string body;
            int status = 200;
            Func<HttpListenerRequest, string> handler;
            if (routes.TryGetValue(ctx.Request.Url.AbsolutePath, out handler))
            {
                try
                {
                    body = handler(ctx.Request);
                }
                catch (Exception e)
                {
                    status = 500;
                    body = Error(e.Message);
                }
            }
            else
            {
                status = 404;
                body = Error("not found: " + ctx.Request.Url.AbsolutePath);
            }

            var bytes = Encoding.UTF8.GetBytes(body);
            ctx.Response.StatusCode = status;
            ctx.Response.ContentType = "application/json; charset=utf-8";
            ctx.Response.ContentLength64 = bytes.Length;
            using (Stream s = ctx.Response.OutputStream)
            {
                s.Write(bytes, 0, bytes.Length);
            }
        }

        public static string Error(string message)
        {
            return "{\"ok\":false,\"error\":" + Json.Str(message) + "}";
        }
    }

    // メインスレッドで待ち行列を処理する
    public class HttpBridgePump : ThreadingExtensionBase
    {
        public override void OnUpdate(float realTimeDelta, float simulationTimeDelta)
        {
            HttpBridge.DrainMainQueue();
        }
    }

    // 最小限の JSON の組み立て(.NET 3.5 には標準の JSON ライブラリがない)
    public static class Json
    {
        public static string Str(string s)
        {
            if (s == null)
            {
                return "null";
            }

            var sb = new StringBuilder("\"");
            foreach (char c in s)
            {
                switch (c)
                {
                    case '"': sb.Append("\\\""); break;
                    case '\\': sb.Append("\\\\"); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default:
                        if (c < 0x20)
                        {
                            sb.AppendFormat("\\u{0:x4}", (int)c);
                        }
                        else
                        {
                            sb.Append(c);
                        }

                        break;
                }
            }

            return sb.Append('"').ToString();
        }
    }
}
