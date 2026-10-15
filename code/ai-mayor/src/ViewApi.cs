using System;
using System.Globalization;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;
using UnityEngine;

namespace AIMayor
{
    // 見るための窓口: 画面写真、カメラ、地点の高さ。
    // 座標はゲーム上のメートル。x が東、z が北。地図の中心が (0, 0)、端が ±8640。
    public static class ViewApi
    {
        public static readonly string ShotDir = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.Personal),
            "Library/Application Support/Colossal Order/Cities_Skylines/AIMayor/screenshots");

        public static void Register(System.Collections.Generic.Dictionary<string, Func<HttpListenerRequest, string>> routes)
        {
            routes["/camera"] = req => HttpBridge.OnMain(() => Camera(req));
            routes["/height"] = req => HttpBridge.OnMain(() => Height(req));
            routes["/screenshot"] = Screenshot;
        }

        // /camera?x=0&z=0&size=4800&pitch=90&yaw=0  (省略した値は今のまま)
        private static string Camera(HttpListenerRequest req)
        {
            var cam = UnityEngine.Object.FindObjectOfType<CameraController>();
            if (cam == null)
            {
                return HttpBridge.Error("camera not found");
            }

            var pos = cam.m_targetPosition;
            pos.x = F(req, "x", pos.x);
            pos.z = F(req, "z", pos.z);
            cam.m_targetPosition = pos;
            cam.m_targetSize = F(req, "size", cam.m_targetSize);
            cam.m_targetAngle = new Vector2(F(req, "yaw", cam.m_targetAngle.x), F(req, "pitch", cam.m_targetAngle.y));
            return "{\"ok\":true,\"x\":" + N(pos.x) + ",\"z\":" + N(pos.z) + ",\"size\":" + N(cam.m_targetSize)
                + ",\"yaw\":" + N(cam.m_targetAngle.x) + ",\"pitch\":" + N(cam.m_targetAngle.y)
                + ",\"current\":{\"x\":" + N(cam.m_currentPosition.x) + ",\"z\":" + N(cam.m_currentPosition.z)
                + ",\"size\":" + N(cam.m_currentSize) + ",\"yaw\":" + N(cam.m_currentAngle.x)
                + ",\"pitch\":" + N(cam.m_currentAngle.y) + "}}";
        }

        // /height?x=..&z=..  地面と、水面を含めた高さ
        private static string Height(HttpListenerRequest req)
        {
            var p = new Vector3(F(req, "x", 0f), 0f, F(req, "z", 0f));
            var t = TerrainManager.instance;
            return "{\"ok\":true,\"ground\":" + N(t.SampleRawHeightSmooth(p))
                + ",\"water\":" + N(t.SampleRawHeightSmoothWithWater(p, false, 0f)) + "}";
        }

        // /screenshot?view=top|oblique|current  画面写真を撮ってファイルに保存し、場所を返す
        private static string Screenshot(HttpListenerRequest req)
        {
            string view = req.QueryString["view"] ?? "current";
            if (view != "current")
            {
                HttpBridge.OnMain(() =>
                {
                    var cam = UnityEngine.Object.FindObjectOfType<CameraController>();
                    cam.m_targetPosition = new Vector3(0f, cam.m_targetPosition.y, 0f);
                    cam.m_targetAngle = view == "top" ? new Vector2(0f, 90f) : new Vector2(0f, 45f);
                    cam.m_targetSize = view == "top" ? 4800f : 4500f;
                    return "{}";
                });
                Thread.Sleep(2500); // カメラが動き終わるのを待つ
            }

            Directory.CreateDirectory(ShotDir);
            string path = Path.Combine(ShotDir, DateTime.Now.ToString("yyyyMMdd-HHmmss-fff", CultureInfo.InvariantCulture) + ".png");
            HttpBridge.OnMain(() =>
            {
                Application.CaptureScreenshot(path);
                return "{}";
            });

            // 書き出しはフレームの終わりに行われるので、ファイルができるまで待つ
            for (int i = 0; i < 50 && !File.Exists(path); i++)
            {
                Thread.Sleep(100);
            }

            if (!File.Exists(path))
            {
                return HttpBridge.Error("screenshot was not written");
            }

            Thread.Sleep(200); // 書き込みの完了を待つ
            return "{\"ok\":true,\"path\":" + Json.Str(path) + "}";
        }

        private static float F(HttpListenerRequest req, string key, float fallback)
        {
            float v;
            string s = req.QueryString[key];
            return s != null && float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out v) ? v : fallback;
        }

        private static string N(float v)
        {
            return v.ToString("0.###", CultureInfo.InvariantCulture);
        }
    }
}
