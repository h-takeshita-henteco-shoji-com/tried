"""AIの読者の答えから、全う度合いと読みやすさの指標を出す(measures.md の「4. 役割の全う度合いを出す」)。

文の役割は、AI(Opus 5.5)の1回目の「読み終えた後の役割」を使う。
埋め込みは cl-nagoya/ruri-v3-310m。意味を表す用途なので、プレフィックスは付けない。
使い方: python reader_metrics.py <texts_dir> <reader_dir> <labeling_run_dir> <out_dir>
出力: <out_dir>/reader-metrics.md、steps.tsv、tau-pairs.tsv
"""
import glob
import json
import os
import re
import statistics as st
import sys
from itertools import combinations

import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.insert(0, os.path.dirname(__file__))
from agreement import roles_of  # noqa: E402
from reader import opening_end  # noqa: E402
from segment import load  # noqa: E402

EMB = SentenceTransformer("cl-nagoya/ruri-v3-310m", device="cpu")
CANDIDATES = {"題の主張", "問いへの最後の答え", "書き手の結び"}
# 既読の確かめに使う書き手(文書名の頭の1文字 → 書き手の候補)
AUTHORS = {"A": ["ブラッシュ", "Brush"], "B": ["寺田"], "C": ["気象庁"], "D": ["やってみ太郎"]}


def embed(texts):
    return EMB.encode(list(texts), normalize_embeddings=True, batch_size=32)


def dist(a, b):
    return 1 - float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def sid_num(x):
    m = re.search(r"s(\d{3})", str(x))
    return int(m.group(1)) if m else None


def read_roles(path):
    """文番号 → (読み終えた後の役割の集合, 転[全体]か)"""
    out = {}
    for line in open(path, encoding="utf-8"):
        row = line.rstrip("\n").split("\t")
        if not re.match(r"s\d{3}$", row[0]):
            continue
        after = row[2] if len(row) > 2 else ""
        out[int(row[0][1:])] = (roles_of(after), "転[全体]" in after.replace(" ", ""))
    return out


def remembered(final, doc_id, title):
    """「前に読んだ」と答え、題か書き手が合っていたか。"""
    said = str(final.get("既読", ""))
    if "ある" not in said or "ない" in said:
        return False
    t, w = str(final.get("既読の題", "")), str(final.get("既読の書き手", ""))
    return title[:4] in t or any(a in w for a in AUTHORS.get(doc_id[0], []))


def load_runs(reader_dir, doc_id, title):
    """集計に使う回と、既読で外した回の数を返す。"""
    runs, dropped = [], 0
    for p in sorted(glob.glob(f"{reader_dir}/{doc_id}/run*.jsonl")):
        steps = [json.loads(line) for line in open(p, encoding="utf-8")]
        run = {s["step"]: (s["answer"] or {}) for s in steps}
        if remembered(run.get("final", {}), doc_id, title):
            dropped += 1
            continue
        runs.append(run)
    return runs, dropped


def reacted(ans, kind):
    return {n for n in (sid_num(x) for x in (ans.get("反応", {}) or {}).get(kind, []) or []) if n}


def analyze(doc_id, doc, runs, roles):
    p0 = opening_end(doc)
    pars = sorted({s["par"] for s in doc["sents"] if s["par"] > p0})
    steps = ["title", "opening"] + [f"p{p:02d}" for p in pars]
    n_runs = len(runs)
    # 予想の埋め込み(段ごと、回ごと)
    preds = {k: [r.get(k, {}).get("予想", "") for r in runs] for k in steps}
    E = {k: embed(v) for k, v in preds.items()}
    c = {k: E[k].mean(0) for k in steps}
    S = {k: st.mean(dist(a, b) for a, b in combinations(E[k], 2)) for k in steps}
    M = {steps[i]: dist(c[steps[i - 1]], c[steps[i]]) for i in range(1, len(steps))}
    medM = st.median(M.values())
    medS = st.median(S[k] for k in steps[1:])
    J = {k: v / medM for k, v in M.items()}
    V = {k: S[k] / medS for k in steps}
    X = {k: sum("逆" in str(r.get(k, {}).get("変化", "")) for r in runs) / n_runs for k in steps[1:]}

    def step_of(sent_no):
        par = doc["sents"][sent_no - 1]["par"]
        return "opening" if par <= p0 else f"p{par:02d}"

    def rate(sent_no, kind):
        hits = 0
        for r in runs:
            got = set()
            for k in steps[1:]:
                got |= reacted(r.get(k, {}), kind)
            hits += any(abs(g - sent_no) <= 1 for g in got)
        return hits / n_runs

    turns = sorted(n for n, (_, g) in roles.items() if g)
    ten = []
    for t in turns:
        k = step_of(t)
        i = steps.index(k)
        prev = steps[i - 1]
        temb = embed([doc["sents"][t - 1]["text"]])[0]
        d0 = dist(c["opening"], temb)
        pre = None if k == "opening" else (d0 - dist(c[prev], temb)) / d0
        order = None if pre is None else int(V[prev] < 1 and pre < 0.5)
        ten.append({
            "文": f"s{t:03d}", "位置": doc["sents"][t - 1]["pos"], "段": k,
            "J": J[k], "X": X[k], "驚き率": rate(t, "驚いた"), "V前": V[prev],
            "先取り度": pre, "順番": order,
        })
    # 読みやすさと読後
    n = len(doc["sents"])
    lost, stop = [], []
    for r in runs:
        a, b = set(), set()
        for k in steps[1:]:
            a |= reacted(r.get(k, {}), "迷った")
            b |= reacted(r.get(k, {}), "手が止まった")
        lost.append(len(a) / n)
        stop.append(len(b) / n)
    cand_ids = [i for i, (rs, _) in roles.items() if rs & CANDIDATES]
    cand_emb = embed([doc["sents"][i - 1]["text"] for i in cand_ids]) if cand_ids else None
    finals = [r.get("final", {}) for r in runs]
    recover = []
    if cand_emb is not None:
        for e in embed([f.get("要点", "") for f in finals]):
            recover.append(1 - min(dist(e, ce) for ce in cand_emb))

    def nums(key):
        v = [f.get(key) for f in finals]
        return [float(x) for x in v if isinstance(x, (int, float)) or (isinstance(x, str) and x.strip().isdigit())]

    def rate_of(kind):
        """回ごとに、その反応に挙げた文の数 ÷ 全体の文の数。回の平均"""
        out = []
        for r in runs:
            got = set()
            for k in steps[1:]:
                got |= reacted(r.get(k, {}), kind)
            out.append(len(got) / n)
        return st.mean(out)

    wants = [float(r.get("opening", {}).get("読みたい")) for r in runs
             if str(r.get("opening", {}).get("読みたい", "")).strip().isdigit()
             or isinstance(r.get("opening", {}).get("読みたい"), (int, float))]
    summary = {
        "回数": n_runs,
        "読みたい(冒頭)": st.mean(wants) if wants else float("nan"),
        "予想が外れた割合": sum("外れ" in str(f.get("外れたか", "")) for f in finals) / n_runs,
        "驚いた文の割合": rate_of("驚いた"),
        "納得した文の割合": rate_of("納得した"),
        "迷い率": st.mean(lost), "停止率": st.mean(stop),
        "要点の復元度": st.mean(recover) if recover else float("nan"),
        "面白さ": st.mean(nums("面白さ")), "面白さSD": st.pstdev(nums("面白さ")),
        "読みやすさ": st.mean(nums("読みやすさ")), "読みやすさSD": st.pstdev(nums("読みやすさ")),
        "納得の点": st.mean(nums("納得")),
    }
    step_rows = [(doc_id, k, M.get(k), J.get(k), S[k], V[k], X.get(k)) for k in steps]
    # τ の候補: 問いの文と、その段以降の読者の問い
    q_pairs = []
    for qn, (rs, _) in roles.items():
        if "問い" not in rs:
            continue
        k = step_of(qn)
        i = steps.index(k)
        qs = {q for r in runs for kk in steps[i:i + 2] for q in (r.get(kk, {}).get("問い") or []) if q}
        if not qs:
            continue
        qs = sorted(qs)
        qe = embed([doc["sents"][qn - 1]["text"]])[0]
        for q, e in zip(qs, embed(qs)):
            q_pairs.append((doc_id, f"s{qn:03d}", doc["sents"][qn - 1]["text"], q, 1 - dist(qe, e)))
    return ten, summary, step_rows, q_pairs


def judge(results):
    """#47 の判断を再現したか(criteria.md の決め方)。転が複数あれば最大値、転がなければ0(J は測れない)。"""
    def ten_val(d, key):
        v = [t[key] for t in results[d][0] if t[key] is not None]
        if not results[d][0]:
            return float("nan") if key == "J" else 0.0
        return max(v) if v else float("nan")

    metrics = [("面白さ", "跳ね比 J", lambda d: ten_val(d, "J"), +1),
               ("面白さ", "逆転率 X", lambda d: ten_val(d, "X"), +1),
               ("面白さ", "驚き率", lambda d: ten_val(d, "驚き率"), +1),
               ("面白さ", "順番の決まり", lambda d: ten_val(d, "順番"), +1),
               ("面白さ", "面白さの点(補助)", lambda d: results[d][1]["面白さ"], +1),
               ("読みやすさ", "迷い率", lambda d: results[d][1]["迷い率"], -1),
               ("読みやすさ", "要点の復元度", lambda d: results[d][1]["要点の復元度"], +1),
               ("読みやすさ", "読みやすさの点(補助)", lambda d: results[d][1]["読みやすさ"], +1)]
    out = ["\n## #47 の判断を再現したか\n",
           "| 軸 | 指標 | " + " | ".join(results) + " | 組の向き | 組ごと | C が下位か |",
           "|---|---|" + "---|" * len(results) + "---|---|---|"]
    for axis, name, f, g in metrics:
        val = {d: f(d) for d in results}
        cells = " | ".join("-" if v != v else f"{v:.2f}" for v in val.values())
        hits, c_low = [], ""
        if axis == "面白さ":
            for p in "ABD":
                o, r = val.get(f"{p}-orig"), val.get(f"{p}-rewrite")
                hits.append((p, None if o is None or r is None or o != o or r != r else g * (o - r) > 0))
            ok = [v for v in val.values() if v == v]
            if len(ok) == len(val) == 8:
                ranked = sorted(val, key=lambda d: -g * val[d])
                c_low = "○" if all(ranked.index(f"C-{v}") >= 4 for v in ("orig", "rewrite")) else "×"
        else:
            for p in "ABCD":
                o, r = val.get(f"{p}-orig"), val.get(f"{p}-rewrite")
                if o is None or r is None or o != o or r != r:
                    hits.append((p, None))
                    continue
                same = abs(o - r) <= 0.05 * (abs(o) + abs(r)) / 2
                hits.append((p, same or g * (r - o) > 0))
        each = " ".join(f"{p}{'-' if h is None else ('○' if h else '×')}" for p, h in hits)
        n_ok = sum(1 for _, h in hits if h)
        mark = "再現" if n_ok == len(hits) else f"{n_ok}/{len(hits)}"
        out.append(f"| {axis} | {name} | {cells} | {mark} | {each} | {c_low} |")
    return out


def main(texts, reader_dir, label_dir, out_dir):
    results = {}
    all_steps, all_pairs = [], []
    for path in sorted(glob.glob(f"{texts}/*.txt")):
        doc_id = os.path.basename(path)[:-4]
        doc = load(path)
        runs, dropped = load_runs(reader_dir, doc_id, doc["title"])
        if not runs:
            continue
        ten, summ, steps, pairs = analyze(doc_id, doc, runs, read_roles(f"{label_dir}/{doc_id}.roles.tsv"))
        summ["既読で外した回"] = dropped
        results[doc_id] = (ten, summ)
        all_steps += steps
        all_pairs += pairs
        print("analyzed", doc_id, len(runs), file=sys.stderr)
    with open(f"{out_dir}/steps.tsv", "w") as f:
        f.write("doc\tstep\tM\tJ\tS\tV\tX\n")
        for r in all_steps:
            f.write("\t".join("" if v is None else (f"{v:.4f}" if isinstance(v, float) else str(v)) for v in r) + "\n")
    # τ の判定用に、cos の値が散らばるよう20組を選ぶ
    all_pairs.sort(key=lambda r: r[4])
    if all_pairs:
        idx = sorted({round(i * (len(all_pairs) - 1) / 19) for i in range(20)})
        with open(f"{out_dir}/tau-pairs.tsv", "w") as f:
            f.write("doc\t問いの文番号\t問いの文\t読者の問い\tcos\t同じ問いか(○/×)\n")
            for i in idx:
                d, sn, st_, q, cs = all_pairs[i]
                f.write(f"{d}\t{sn}\t{st_}\t{q}\t{cs:.3f}\t\n")

    def fmt(v, p=2):
        return "-" if v is None or v != v else (f"{v:.{p}f}" if isinstance(v, float) else str(v))

    n_runs = sorted({s["回数"] for _, s in results.values()})
    lines = [f"## 全体の転ごとの指標(AIの読者 Haiku 4.5、各{'〜'.join(map(str, n_runs))}回)\n",
             "| 文書 | 転の文 | 位置(%) | 段 | 跳ね比 J | 逆転率 X | 驚き率 | 直前の散らばり比 V | 先取り度 | 順番の決まり |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for d, (ten, _) in results.items():
        if not ten:
            lines.append(f"| {d} | なし | | | | | | | | |")
        for t in ten:
            lines.append(f"| {d} | {t['文']} | {t['位置']:.0f} | {t['段']} | {fmt(t['J'])} | {fmt(t['X'])} | {fmt(t['驚き率'])} | {fmt(t['V前'])} | {fmt(t['先取り度'])} | {fmt(t['順番'])} |")
    keys = list(next(iter(results.values()))[1])
    lines += ["\n## 文書ごとの読後と読みやすさ\n", "| 文書 | " + " | ".join(keys) + " |", "|---|" + "---|" * len(keys)]
    for d, (_, s) in results.items():
        lines.append(f"| {d} | " + " | ".join(fmt(s[k]) for k in keys) + " |")
    # #47 の判断との照合は、原文と書き直しの組(A-orig など)があるときだけ行う
    if any(d.endswith("-orig") for d in results):
        lines += judge(results)
    open(f"{out_dir}/reader-metrics.md", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:5])
