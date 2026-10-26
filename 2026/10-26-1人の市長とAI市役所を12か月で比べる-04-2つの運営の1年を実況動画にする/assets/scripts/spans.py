"""録画の時刻の対応表と、施策を打った場面の一覧を作る(#106)。#98 の do_spans.py にならう。

- 録画はファイル名が録画を始めた実時間(OBS の既定)。長さは ffprobe で測る
- パネルのログ(command-log*.txt)の DO の行から、続く操作が終わるまでを1場面にする
- 出力: video-timeline.json(録画ごとの実時間と長さ)、spans.json(場面ごとの録画と秒)

使い方: python3 assets/scripts/spans.py
"""
import datetime as dt
import glob
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
ROOT = HERE.parent.parent
REC = Path.home() / "ai-mayor-recordings"
RUNS = {
    "base": (REC / "base", ["2026-10-25 17-59-06.mp4", "2026-10-25 19-07-19.mp4"],
             ROOT / "2026/10-25-1人の市長とAI市役所を12か月で比べる-02-基準の市長に12か月任せて録画する/command-log-m07-m12.txt"),
    "council": (REC / "council", sorted(os.path.basename(p) for p in glob.glob(str(REC / "council/2026-10-26 1[3-7]-*.mp4"))),
                ROOT / "2026/10-25-1人の市長とAI市役所を12か月で比べる-03-AI市役所に12か月任せて録画する/command-log.txt"),
}
ACT = {"place_building", "build_line", "bulldoze", "zone_area", "zone_rect", "zone_polygon", "set_tax", "set_budget",
       "set_policy", "upgrade_road", "create_transport_line", "set_building_active", "paint_district",
       "set_district_policy", "remove_line", "relocate_building", "empty_building", "set_traffic_lights",
       "set_transport_line_budget", "plant_trees"}
P = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout
    return float(out)


def main():
    timeline, spans = [], {}
    for run, (folder, files, log) in RUNS.items():
        tl = []
        for f in files:
            start = dt.datetime.strptime(f[:19], "%Y-%m-%d %H-%M-%S")
            tl.append(dict(run=run, file=str(folder / f), real_start=start.strftime("%Y-%m-%d %H:%M:%S"),
                           duration=round(duration(folder / f), 2)))
        timeline += tl

        def where(t):
            for s in tl:
                d = (t - P(s["real_start"])).total_seconds()
                if 0 <= d <= s["duration"]:
                    return s["file"], round(d, 1)
            return None, None

        lines = [l.split("\t") for l in open(log, encoding="utf-8-sig").read().splitlines()]
        lines = [p for p in lines if len(p) >= 4 and p[0][:2] == "20"]
        rows, seen = [], set()
        for i, p in enumerate(lines):
            if p[2] != "DO" or (p[0], p[3]) in seen:
                continue
            seen.add((p[0], p[3]))
            t0, last, n = P(p[0]), P(p[0]), 0
            for q in lines[i + 1:]:
                if q[2] in ("DO", "TITLE"):
                    break
                tool = q[3].split(" ")[0]
                if tool == "advance" and q[2] == "OK":
                    break
                if q[2] == "OK" and tool in ACT and (P(q[0]) - t0).total_seconds() < 900:
                    last, n = P(q[0]), n + 1
            f0, v0 = where(t0)
            f1, v1 = where(last)
            rows.append(dict(t=p[0], date=p[1], do=p[3], file=f0, v0=v0, v1=v1 if f1 == f0 else v0, ops=n))
        spans[run] = rows
        for r in rows:
            name = os.path.basename(r["file"]) if r["file"] else "-"
            print(run, r["date"], name, r["v0"], r["v1"], r["ops"], r["do"][:50], sep="\t")
    (HERE / "video-timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1))
    (HERE / "spans.json").write_text(json.dumps(spans, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
