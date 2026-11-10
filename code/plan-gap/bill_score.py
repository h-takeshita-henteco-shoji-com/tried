"""不備ごとの「算定への影響」の答えを採点する。

正解(IMPACT)は、厚労省の基準・通知・Q&A から付けた。判断が分かれるものは、許す答えを2つにした。
  1 算定できない / 2 算定できるが計画の見直しが必要 / 3 運営基準の不備(算定とは別) / 4 影響しない
指摘が仕込んだ不備と同じものかは、score.py の判定(data*/judge/)を使う。
使い方: DATA=data-v2 python3 bill_score.py sonnet-bill-1 sonnet-billrule-1 ...
"""
import json
import os
import sys
from pathlib import Path

import score

HERE = Path(__file__).parent
DATA = HERE / os.environ.get("DATA", "data")
ANS = json.loads((DATA / "answers.json").read_text())

# 主な正解と、許す答え
IMPACT = {
    "A": (2, {1, 2}),  # 計画にない日時の提供を、計画を直さずに続けた。算定の根拠が崩れると見れば1
    "B": (1, {1}),     # 計画にない内容。ケアマネジャーが認めた記録もない
    "C": (3, {3}),     # 計画の説明と同意(基準第24条)。返還まで及ぶかは自治体の判断
    "D": (1, {1}),     # ケアプランにない項目の提供(基準第16条)
    "E": (1, {1}),     # 計画にない日の訪問。要請・身体介護中心の記録がなく、緊急時訪問介護加算にも当たらない
    "F": (1, {1, 3}),  # 期間の切れた計画のまま提供。運営基準の問題と見れば3
}


def main():
    for cond in sys.argv[1:]:
        score.score(cond)  # 判定を作る(済んでいれば読むだけ)
        judge = json.loads((DATA / "judge" / f"{cond}.json").read_text())
        ok = main_ok = n = 0
        detail = []
        for uid, a in sorted(ANS.items()):
            if a["type"] not in IMPACT:
                continue
            fs = json.loads((DATA / "out" / cond / f"{uid}.json").read_text()).get("findings", [])
            hits = [f for f, l in zip(fs, judge[uid]) if l == "hit"]
            if not hits:
                detail.append((uid, a["type"], "見落とし"))
                continue
            n += 1
            imp = {int(str(f.get("impact", "0"))[0]) for f in hits if str(f.get("impact", "")).strip()}
            main_, allow = IMPACT[a["type"]]
            if imp & allow:
                ok += 1
            if main_ in imp:
                main_ok += 1
            if not imp & allow or main_ not in imp:
                detail.append((uid, a["type"], sorted(imp)))
        flagged = sum(1 for uid, a in ANS.items() if a["type"] in ("trap", "clean")
                      and json.loads((DATA / "out" / cond / f"{uid}.json").read_text()).get("findings"))
        print(json.dumps({"cond": cond, "found": n, "impact_ok": f"{ok}/{n}", "impact_main": f"{main_ok}/{n}",
                          "trap_clean_flagged": flagged, "diff": detail}, ensure_ascii=False))


if __name__ == "__main__":
    main()
