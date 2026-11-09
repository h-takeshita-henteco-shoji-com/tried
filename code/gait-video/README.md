# gait-video

高齢者の歩行動画(Toronto Older Adults Gait Archive)から、MediaPipe の骨格推定で歩く速さと歩調を求め、慣性センサー(Xsens)の値と比べる。#160 の検証に使った。

## データ

すべて figshare から取得する(CC0)。リポジトリには入れない。

- 動画: https://ndownloader.figshare.com/files/35454242 (Videos.zip、2.35GB)
- センサー: https://ndownloader.figshare.com/files/35454227 (Xsens.zip)
- 参加者の表: https://ndownloader.figshare.com/files/35454230 (Table 1.xlsx)
- MediaPipe のモデル: https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task

`/tmp/toaga` に次の形で置く。

```
videos/Videos/OAWxx-bottom.mp4 ...
meta/Xsens/OAWxx.csv
meta/table1.xlsx
models/pose_landmarker_full.task
pose/            (extract_pose.py の出力)
```

## 手順

```bash
# 1. 骨格推定(1本約1分)
uv run --python 3.12 --with mediapipe --with opencv-python-headless \
  python extract_pose.py /tmp/toaga/videos/Videos/OAW01-bottom.mp4 /tmp/toaga/pose/OAW01-bottom.csv /tmp/toaga/models/pose_landmarker_full.task

# 2. 比較(results.csv を書く)
uv run --with pandas --with numpy --with scipy --with openpyxl python compare.py /tmp/toaga /tmp/toaga

# 3. 秒速1.0mの判定と、片道1本だけの精度
uv run --with pandas --with numpy --with scipy --with openpyxl python extra.py

# 4. 図(figures.py は検証用、figures_article.py は note 記事用)
uv run --python 3.12 --with pandas --with numpy --with matplotlib --with opencv-python-headless \
  python figures.py /tmp/toaga <出力先> 1550
uv run --with pandas --with numpy --with matplotlib python figures_article.py /tmp/toaga <出力先>

# 5. 記事用の GIF(骨格と、距離・速さを重ねる。2本を横に並べることもできる)
uv run --python 3.12 --with pandas --with numpy --with scipy --with openpyxl --with opencv-python-headless --with pillow \
  python gifs.py /tmp/toaga <出力先>
```

GIF の速さは、片道の始めからその時点までの距離を、時間で回帰した傾き。歩くほど安定し、最後は片道全体の推定値になる。

## 求め方

- 距離: カメラからの距離 = K × 身長 ÷ 画面上の鼻から足首までの高さ(px)。K は画角を65度と仮定して決めるか、他の10人で校正する。
- 速さ: まっすぐ歩く区間(片道の両端20%を除く)で、距離を時間で回帰した傾き。
- 歩調: 左右の足首の上下差の、自己相関の周期(1周期=2歩)。
- 正解: センサーの骨盤の水平の速さと、足が最も高く上がった瞬間の間隔。動画とセンサーは時刻を合わせていないので、人ごとの平均で比べる。
