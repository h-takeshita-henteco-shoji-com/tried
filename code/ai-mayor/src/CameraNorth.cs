using ICities;
using UnityEngine;

namespace AIMayor
{
    // F10: 真上から北を上にして地図全体を見下ろす。Shift+F10: 北を向いて斜め45度から見下ろす。
    // F11 は macOS の「デスクトップを表示」、F7 はゲームのデバッグ出力と重なるため使わない。
    // 標準の操作では真北にぴったり合わせられないため、記事用の画面写真をそろえるのに使う。
    public class CameraNorth : ThreadingExtensionBase
    {
        public override void OnUpdate(float realTimeDelta, float simulationTimeDelta)
        {
            if (!Input.GetKeyDown(KeyCode.F10))
            {
                return;
            }

            bool shift = Input.GetKey(KeyCode.LeftShift) || Input.GetKey(KeyCode.RightShift);
            if (shift)
            {
                Aim(45f, 4500f);
            }
            else
            {
                Aim(90f, 4800f);
            }
        }

        private static void Aim(float pitch, float size)
        {
            var cam = Object.FindObjectOfType<CameraController>();
            if (cam == null)
            {
                return;
            }

            // 角度は x が向き(0 で北)、y が見下ろす角度(90 で真下)
            cam.m_targetAngle = new Vector2(0f, pitch);
            cam.m_targetSize = size;
            cam.m_targetPosition = new Vector3(0f, cam.m_targetPosition.y, 0f);
            Debug.Log(string.Format("[AIMayor] camera angle=({0}, {1}) size={2}", 0f, pitch, size));
        }
    }
}
