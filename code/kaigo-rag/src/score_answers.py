"""答えの方式を集計する。答えの正しさ(judge_answers.py の判定)と、挙げた根拠の当たり具合。

- 根拠の再現率: 判定2のチャンクのうち、evidence に挙げた割合(分母は min(判定2の数, 5))
- 根拠の適合率: evidence のうち、判定1以上の割合
evidence に未判定のチャンクがあれば、data/unjudged_answers.json に書き出す(judge_extra.py で判定する)
使い方: uv run python src/score_answers.py llm rag agentic pageindex
"""
import json
import os
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from answer import leaks

ROOT = Path(__file__).resolve().parent.parent


def main(modes):
    set_b = {json.loads(l)["qa_id"]: json.loads(l) for l in open(ROOT / "data/set_b.jsonl")}
    grades = {json.loads(l)["qa_id"]: json.loads(l)["grades"] for l in open(ROOT / os.environ.get("KAIGO_GRADES", "results/answer_grades.jsonl"))}
    same = leaks()
    unjudged = {}
    print("| 方式 | 正しい(2) | 一部(1) | 誤り(0) | 平均点 | 根拠の再現率 | 根拠の適合率 | 道具の呼び出し | 秒/問 |")
    print("|---|---|---|---|---|---|---|---|---|")
    for m in modes:
        ans = [json.loads(l) for l in open(ROOT / f"results/answers_{m}.jsonl")]
        ans = [a for a in ans if a["qa_id"] in grades and m in grades[a["qa_id"]]]
        g = [grades[a["qa_id"]][m] for a in ans]
        rec, prec = [], []
        for a in ans:
            judged = {int(k): v for k, v in set_b[a["qa_id"]]["judged"].items()}
            leak = set(same(a["qa_id"]))
            gold = {c for c, v in judged.items() if v == 2 and c not in leak}
            ev = [c for c in dict.fromkeys(a["evidence"]) if c not in leak]
            for c in ev:
                if c not in judged:
                    unjudged.setdefault(a["qa_id"], []).append(c)
            if m != "llm" and gold:
                rec.append(len(gold & set(ev)) / min(len(gold), 5))
            if ev:
                prec.append(sum(1 for c in ev if judged.get(c, 0) >= 1) / len(ev))
        calls = st.mean(len(a["searches"]) + len(a["reads"]) for a in ans)
        f = lambda xs: f"{st.mean(xs):.2f}" if xs else "-"
        print(f"| {m} | {g.count(2)} | {g.count(1)} | {g.count(0)} | {st.mean(g):.2f} | {f(rec)} | {f(prec)} "
              f"| {calls:.1f} | {st.mean(a['sec'] for a in ans):.0f} |")
    json.dump(unjudged, open(ROOT / "data/unjudged_answers.json", "w"), ensure_ascii=False)
    print("未判定の根拠:", sum(len(v) for v in unjudged.values()))


if __name__ == "__main__":
    main(sys.argv[1:])
