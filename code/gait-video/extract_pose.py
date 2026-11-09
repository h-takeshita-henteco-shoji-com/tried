"""動画から MediaPipe Pose Landmarker で骨格の33点を取り出し、CSVに書く。

使い方:
  uv run --python 3.12 --with mediapipe --with opencv-python-headless \
    python extract_pose.py <動画> <出力CSV> <モデル.task>
"""
import csv
import sys

import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (PoseLandmarker,
                                           PoseLandmarkerOptions,
                                           RunningMode)


def main(video, out_csv, model):
    opts = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model),
        running_mode=RunningMode.VIDEO,
        num_poses=1,
        min_pose_detection_confidence=0.3,
        min_tracking_confidence=0.3,
    )
    cap = cv2.VideoCapture(video)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    header = ["frame", "t_ms"]
    for i in range(33):
        header += [f"x{i}", f"y{i}", f"v{i}"]
    last_ts = -1
    with PoseLandmarker.create_from_options(opts) as lm, \
            open(out_csv, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(header)
        n = 0
        while True:
            ok, img = cap.read()
            if not ok:
                break
            ts = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            if ts <= last_ts:  # タイムスタンプは単調増加が必要
                ts = last_ts + 1
            last_ts = ts
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = lm.detect_for_video(
                mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb), ts)
            row = [n, ts]
            if res.pose_landmarks:
                for p in res.pose_landmarks[0]:
                    row += [round(p.x * w, 2), round(p.y * h, 2),
                            round(p.visibility, 3)]
            else:
                row += [""] * 99
            wr.writerow(row)
            n += 1
    print(video, n, "frames")


if __name__ == "__main__":
    main(*sys.argv[1:4])
