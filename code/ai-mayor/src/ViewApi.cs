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
            routes["/camera"] = Camera;
            routes["/height"] = req => HttpBridge.OnMain(() => Height(req));
            routes["/screenshot"] = Screenshot;
        }

        // /camera?x=0&z=0&size=4800&pitch=90&yaw=0  (省略した値は今のまま)
        // ゲームは引くほど角度を真下に寄せる(実際の角度 = 90 - (90 - 指定) * k、k = 2500 / (2500 + 引き))。
        // ここでは逆算して、指定した角度がそのまま実際の角度になるようにする。届かない角度は、届く一番浅い角度にする。
        // カメラは少しずつ動くので、動き終わるまで待ってから実際の値を返す(最大4秒)。
        private static string Camera(HttpListenerRequest req)
        {
            string set = HttpBridge.OnMain(() => AimCamera(req));
            if (set.StartsWith("{\"ok\":false", StringComparison.Ordinal))
            {
                return set;
            }

            // 見る場所の目標。地図の端の近くでは、カメラが地図の外に出ないようにゲームが目標をずらす
            var want = new Vector2(Mathf.Clamp(F(req, "x", float.NaN), -8640f, 8640f), Mathf.Clamp(F(req, "z", float.NaN), -8640f, 8640f));
            string now = null;
            for (int i = 0; i < 40; i++)
            {
                Thread.Sleep(100);
                bool settled = false;
                now = HttpBridge.OnMain(() => ReadCamera(want, out settled));
                if (settled)
                {
                    break;
                }
            }

            return set.Substring(0, set.Length - 1) + ",\"current\":" + now + "}";
        }

        // 引き size のときに届く一番浅い角度
        public static float MinPitch(CameraController cam, float size)
        {
            return 90f - 90f * TiltFactor(cam, size);
        }

        // 実際に見下ろしたい角度から、ゲームに渡す角度を逆算する
        public static float RawPitch(CameraController cam, float size, float pitch)
        {
            return Mathf.Clamp(90f - (90f - pitch) / TiltFactor(cam, size), 0f, 90f);
        }

        private static float TiltFactor(CameraController cam, float size)
        {
            float half = cam.m_maxTiltDistance * 0.5f;
            return half / (half + size);
        }

        private static string AimCamera(HttpListenerRequest req)
        {
            var cam = UnityEngine.Object.FindObjectOfType<CameraController>();
            if (cam == null)
            {
                return HttpBridge.Error("camera not found");
            }

            cam.ClearTarget(); // 車や建物を追いかけていると、指定した場所に動かないため
            float size = Mathf.Clamp(F(req, "size", cam.m_targetSize), cam.m_minDistance, cam.m_maxDistance);
            float minPitch = MinPitch(cam, size);
            float nowPitch = 90f - (90f - cam.m_targetAngle.y) * TiltFactor(cam, cam.m_targetSize);
            float pitch = Mathf.Clamp(F(req, "pitch", nowPitch), minPitch, 90f);
            var pos = cam.m_targetPosition;
            pos.x = Mathf.Clamp(F(req, "x", pos.x), -8640f, 8640f);
            pos.z = Mathf.Clamp(F(req, "z", pos.z), -8640f, 8640f);
            cam.m_targetPosition = pos;
            cam.m_targetSize = size;
            cam.m_targetAngle = new Vector2(F(req, "yaw", cam.m_targetAngle.x), RawPitch(cam, size, pitch));
            var sb = new StringBuilder("{\"ok\":true,\"x\":").Append(N(pos.x)).Append(",\"z\":").Append(N(pos.z))
                .Append(",\"size\":").Append(N(size)).Append(",\"yaw\":").Append(N(cam.m_targetAngle.x))
                .Append(",\"pitch\":").Append(N(pitch)).Append(",\"pitchMin\":").Append(N(minPitch))
                .Append(",\"sizeMax\":").Append(N(cam.m_maxDistance));
            var notes = new System.Collections.Generic.List<string>();
            string reqSize = req.QueryString["size"];
            if (reqSize != null && Math.Abs(F(req, "size", size) - size) > 0.5f)
            {
                notes.Add("size は " + N(cam.m_minDistance) + "〜" + N(cam.m_maxDistance) + " に収めた");
            }

            if (req.QueryString["pitch"] != null && F(req, "pitch", pitch) < minPitch - 0.5f)
            {
                notes.Add("この引きでは pitch " + N(minPitch) + " より浅くできない。浅く見るには size を小さくする");
            }

            sb.Append(",\"notes\":[");
            for (int i = 0; i < notes.Count; i++)
            {
                sb.Append(i > 0 ? "," : "").Append(Json.Str(notes[i]));
            }

            return sb.Append("]}").ToString();
        }

        // 今のカメラの値。settled は、目標の値に追いついたか
        // offset は、指定した見る場所と実際の見る場所の差(m)。x, z を指定しなかったときは出さない
        private static string ReadCamera(Vector2 want, out bool settled)
        {
            var cam = UnityEngine.Object.FindObjectOfType<CameraController>();
            var p = cam.m_currentPosition;
            float offX = float.IsNaN(want.x) ? 0f : p.x - want.x;
            float offZ = float.IsNaN(want.y) ? 0f : p.z - want.y;
            string offset = float.IsNaN(want.x) && float.IsNaN(want.y) ? ""
                : ",\"offset\":" + N(Mathf.Round(new Vector2(offX, offZ).magnitude));
            float pitch = 90f - (90f - cam.m_targetAngle.y) * TiltFactor(cam, cam.m_targetSize);
            var d = cam.m_currentPosition - cam.m_targetPosition;
            settled = new Vector2(d.x, d.z).magnitude < 2f
                && Mathf.Abs(cam.m_currentSize - cam.m_targetSize) < 2f
                && Mathf.Abs(Mathf.DeltaAngle(cam.m_currentAngle.x, cam.m_targetAngle.x)) < 0.5f
                && Mathf.Abs(cam.m_currentAngle.y - pitch) < 0.5f;
            return "{\"x\":" + N(cam.m_currentPosition.x) + ",\"z\":" + N(cam.m_currentPosition.z)
                + ",\"size\":" + N(cam.m_currentSize) + ",\"yaw\":" + N(cam.m_currentAngle.x)
                + ",\"pitch\":" + N(cam.m_currentAngle.y) + offset + ",\"settled\":" + (settled ? "true" : "false") + "}";
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
                    cam.ClearTarget();
                    cam.m_targetSize = view == "top" ? 4800f : 4500f;
                    float size = Mathf.Clamp(cam.m_targetSize, cam.m_minDistance, cam.m_maxDistance);
                    cam.m_targetAngle = new Vector2(0f, view == "top" ? 90f : RawPitch(cam, size, 45f));
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
