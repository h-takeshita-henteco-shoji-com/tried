# 音楽理論の学習と共同作曲の道具

親 #188 で使う、楽譜と音を作る道具です。準備は #189 で行いました。

## 役割の分け方

AIは音を聴けません。そのため、AIが譜と音のファイルを作り、学習者が鳴らして判断します。

- AI: music21 で譜を書き、MusicXML・MIDI・PNG に書き出す
- AI: 平均律から外れた音の高さは、周波数を指定して WAV にする
- 学習者: MuseScore 4 で譜を開いて再生し、WAV を聴いて、良し悪しを返す

## 準備

```bash
brew install --cask musescore          # 譜の表示と再生。mscore コマンドも入る
cd code/music-theory
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python smoke_test.py out     # 動作確認。out/ に4つのファイルができる
```

## ファイル

- `score.py` : 譜を MusicXML・MIDI・PNG に書き出す `export()`
- `tone.py` : 周波数を指定して WAV を作る `write_wav()`。純正律、シュルティ、ガムランなどに使う
- `smoke_test.py` : 上の2つが動くかを確かめる

## 形式の使い分け

- MusicXML: MuseScore で開いて、譜を見て再生する。学習者が手で直すときもこれを使う
- MIDI: 平均律の12音だけを持つ。他の音楽ソフトに渡すときに使う
- PNG: 記事と log.md に貼る譜の画像
- WAV: 平均律から外れた音の高さを聴き比べる。MIDI では表せないため
