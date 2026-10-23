"""作った声を音声認識で文字に戻し、台本の読みと比べる(#98)。

台本の ttsText と、聞き取った文字を、どちらもカタカナの読みに直して比べる。
似ている割合が低い行を、聞き直す候補として出す。

聞き取った文字にも読みの表(tts-readings.tsv)をかけ、「棟」などの読みの差で外れと出ないようにする。

使い方: ~/.venvs/tried-asr/bin/python listen_check.py <voice フォルダ> <読みの表.tsv> [しきい値 0.85]
出力: <voice フォルダ>/listen-check.tsv
"""
import difflib
import json
import re
import sys

import mlx_whisper
import pyopenjtalk

MODEL = "mlx-community/whisper-large-v3-turbo"


READ = []


def kana(t):
    for a, b in READ:
        t = t.replace(a, b)
    t = re.sub(r"[、。,.!?！？…「」『』()（）\s]", "", t)
    return re.sub(r"[’、。？！]", "", pyopenjtalk.g2p(t, kana=True))


def main():
    out = sys.argv[1]
    READ.extend(tuple(l.rstrip("\n").split("\t")) for l in open(sys.argv[2], encoding="utf-8")
                if "\t" in l and not l.startswith("#"))
    th = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
    scenes = json.load(open(f"{out}/lines.json"))
    rows = []
    for sc in scenes:
        for ln in sc["lines"]:
            r = mlx_whisper.transcribe(f"{out}/{ln['file']}", path_or_hf_repo=MODEL, language="ja")
            heard = r["text"].strip()
            a, b = kana(ln["ttsText"]), kana(heard)
            ratio = difflib.SequenceMatcher(None, a, b).ratio()
            rows.append((ratio, ln["file"], ln["ttsText"], heard))
            print(f"{ratio:.2f}", ln["file"], heard, flush=True)
    with open(f"{out}/listen-check.tsv", "w") as f:
        f.write("似ている割合\tファイル\t台本\t聞き取り\n")
        for r in sorted(rows):
            f.write(f"{r[0]:.2f}\t{r[1]}\t{r[2]}\t{r[3]}\n")
    low = [r for r in rows if r[0] < th]
    print("lines", len(rows), "low", len(low))


if __name__ == "__main__":
    main()
