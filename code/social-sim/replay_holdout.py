"""#181 粘り(holdout)ゲームの記録を、期ごとに再生する HTML を作る。

使い方: python3 replay_holdout.py runs/c181n30 -o <出力.html>
各実行フォルダの manifest.json と events.jsonl を読み、1つの HTML に埋め込む。
画面はDOMを組み立てて作り、AIの文章はテキストとしてだけ入れる。
"""
import argparse
import json
from pathlib import Path

HUMAN = {  # Cadigan et al. 2009 の10期の条件
    ("buyer", False): "1期目の額 34.28 / 断った回数 10.8 / 効率 100%",
    ("buyer", True): "1期目の額 35.82 / 断った回数 2.9 / 効率 85.3%",
    ("seller", False): "1期目の額 46.73 / 断った回数 11.0 / 効率 96.7%",
    ("seller", True): "1期目の額 44.17 / 断った回数 3.3 / 効率 83.3%",
}


def load(run_dir):
    runs = []
    for d in sorted(Path(run_dir).iterdir()):
        if not (d / "events.jsonl").exists():
            continue
        game = json.loads((d / "manifest.json").read_text())["config"]["game"]
        groups = [json.loads(l) for l in (d / "events.jsonl").read_text().splitlines() if l.strip()]
        groups.sort(key=lambda g: g["group"])
        p, delay = game["proposer"], game["delay"]
        title = f"{'買い手' if p == 'buyer' else '売り手'}が提示・遅れの損{'あり' if delay else 'なし'}"
        runs.append({"title": title, "proposer": p, "delay": delay, "step": game["delay_step"],
                     "human": HUMAN.get((p, delay), ""), "groups": groups})
    return runs


PAGE = r"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<title>土地をまとめる交渉の再生(#181)</title>
<style>
:root{--bg:#fafaf8;--card:#fff;--ink:#1d1d1f;--muted:#6b6b70;--line:#e3e3e0;--ok:#1f7a4d;--ng:#b3261e;--rule:#7a4fb3}
@media (prefers-color-scheme:dark){:root{--bg:#18181a;--card:#222225;--ink:#ececec;--muted:#a0a0a6;--line:#38383c;--ok:#5fc48f;--ng:#f08a80;--rule:#b99cf0}}
body{margin:0;font-family:-apple-system,"Hiragino Sans",sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}
header{padding:12px 20px;border-bottom:1px solid var(--line);display:flex;gap:12px;flex-wrap:wrap;align-items:center}
header h1{font-size:16px;margin:0 12px 0 0}
select,button{font:inherit;padding:4px 10px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink)}
button{cursor:pointer}
main{max-width:1100px;margin:0 auto;padding:16px 20px}
.summary{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;color:var(--muted);margin-bottom:12px}
.summary b{color:var(--ink)}
.timeline{display:flex;gap:4px;margin:8px 0 16px}
.timeline span{flex:1;height:10px;border-radius:3px;background:var(--line);cursor:pointer}
.timeline span.cur{outline:2px solid var(--ink);outline-offset:1px}
.timeline span.done{background:var(--ok)}
.timeline span.rej{background:var(--ng)}
h2{font-size:18px;margin:0 0 4px}
.status{font-size:14px;color:var(--muted);margin-bottom:12px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
@media (max-width:800px){.cards{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.card h3{font-size:15px;margin:0 0 6px}
.price{font-size:22px;font-weight:600}
.tag{font-size:12px;padding:1px 8px;border-radius:10px;border:1px solid currentColor;margin-right:6px}
.ok{color:var(--ok)}.ng{color:var(--ng)}.rule{color:var(--rule)}
.belief{font-size:13px;margin:6px 0;padding:6px 8px;border-left:3px solid var(--line)}
.reason{font-size:13px;color:var(--muted);white-space:pre-wrap;margin-top:6px}
.final{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px;margin-top:16px;font-size:14px}
.legend{font-size:12px;color:var(--muted);margin-top:20px}
</style></head><body>
<header>
<h1>土地をまとめる交渉の再生</h1>
<label>条件 <select id="run"></select></label>
<label>組 <select id="grp"></select></label>
<button id="prev">◀ 前の期</button><button id="next">次の期 ▶</button><button id="play">自動再生</button>
</header>
<main>
<div class="summary" id="summary"></div>
<div class="timeline" id="timeline"></div>
<div id="period"></div>
<div class="final" id="final"></div>
<p class="legend">買い手は2つの品物を両方買えたときだけ90ドルの価値を得ます。売り手は手放すと30ドルの費用がかかります。
帯の色は、その期に全部決まったか(緑)、誰かが断ったか(赤)です。
「決まりで変更」は、AI自身の答えと組み合わせ型の決まりの判断が違った場面です。決まりは、AIが書いた次の値段の予想から断ったときの増え方を計算し、しきい値θを超えたら断ります。最後の期はAIの答えのままです。左右の矢印キーでも期を動かせます。</p>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const RUNS = JSON.parse(document.getElementById("data").textContent);
const $ = id => document.getElementById(id);
// 要素を作る。子は文字列ならテキストとして入れる
function h(tag, attrs, ...kids){
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k === "class") e.className = v; else if (k === "on") e.onclick = v; else e.setAttribute(k, v);
  }
  for (const k of kids.flat()) if (k !== null && k !== undefined && k !== false)
    e.append(typeof k === "string" || typeof k === "number" ? document.createTextNode(String(k)) : k);
  return e;
}
const put = (id, ...kids) => $(id).replaceChildren(...kids.flat());
let run, grp, t = 0, timer = null;

RUNS.forEach((r, i) => $("run").add(new Option(r.title, i)));
function setRun(i){ run = RUNS[i]; $("grp").replaceChildren();
  run.groups.forEach((g, j) => $("grp").add(new Option(`${g.group + 1}組目(断った回数 ${g.rejections})`, j)));
  setGrp(0); }
function setGrp(j){ grp = run.groups[j]; t = 0; render(); }

function render(){
  const R = grp.rounds, r = R[t], buyerProposes = run.proposer === "buyer";
  put("summary",
    h("span", {}, "人間(論文): ", h("b", {}, run.human)),
    h("span", {}, "この組: 値段 ", h("b", {}, grp.prices.map(p => p ?? "未決").join(" / ")), " ドル、断った回数 ",
      h("b", {}, grp.rejections), "、効率 ", h("b", {}, Math.round(grp.efficiency * 100) + "%")),
    h("span", {}, "しきい値θ(買い手/売り手1/売り手2): " + grp.theta.map(x => x.toFixed(2)).join(" / ") + " ドル"));
  put("timeline", R.map((x, i) => h("span", {
    class: (i === t ? "cur " : "") + (Object.values(x.accepted).every(Boolean) ? "done" : "rej"),
    title: x.period + "期目", on: () => { t = i; render(); } })));

  const before = t ? R[t - 1].rejections_total : 0;
  const m = run.delay ? Math.max(0, 1 - run.step * before) : 1;
  const decision = (s, yes, no, prefix) => {
    const a = r.accepted[s], ai = r.ai_accepted ? r.ai_accepted[s] : a;
    return h("div", {}, prefix || "", h("span", {class: "tag " + (a ? "ok" : "ng")}, a ? yes : no),
      ai !== a ? h("span", {class: "tag rule"}, `決まりで変更(AIは「${ai ? yes : no}」)`) : null);
  };
  const belief = (s, dir) => r.beliefs && r.beliefs[s]
    ? h("div", {class: "belief"}, (buyerProposes ? "" : s + "に") + "断ったら、次は ", h("b", {}, r.beliefs[s].next_price),
        ` ドルに${dir}と予想(その見込み ${r.beliefs[s].chance}%)`) : null;
  const card = (who, body, reason) => h("div", {class: "card"}, h("h3", {}, who), body,
    reason ? h("div", {class: "reason"}, reason) : null);

  const sellers = Object.keys(r.offers);
  const buyerBody = buyerProposes
    ? sellers.map(s => h("div", {}, s + "に ", h("span", {class: "price"}, r.offers[s]), " ドル"))
    : [...sellers.map(s => decision(s, "買う", "断る", s + ": ")), ...sellers.map(s => belief(s, "下がる"))];
  const cards = [card("買い手", buyerBody, r.reasons.buyer)];
  ["売り手1", "売り手2"].forEach((s, i) => {
    if (!(s in r.offers)) { cards.push(card(s, h("div", {class: "reason"}, `売り買いは決まっています(${grp.prices[i]} ドル)`))); return; }
    const body = buyerProposes
      ? [h("div", {}, "提示された値段 ", h("span", {class: "price"}, r.offers[s]), " ドル"), decision(s, "売る", "断る"), belief(s, "上がる")]
      : [h("div", {}, "出した値段 ", h("span", {class: "price"}, r.offers[s]), " ドル")];
    cards.push(card(s, body, r.reasons[s]));
  });
  put("period", h("h2", {}, r.period + "期目"),
    h("div", {class: "status"}, `この期までに断られた回数 ${before} 回` + (run.delay ? `、稼ぎは本来の ${Math.round(m * 100)}%` : "") + "。" +
      (buyerProposes ? "買い手が値段を出し、売り手が売るか断るかを決めます。" : "売り手が値段を出し、買い手が買うか断るかを決めます。")),
    h("div", {class: "cards"}, cards));

  put("final", t === R.length - 1
    ? [h("b", {}, "結末: "), grp.complete ? "両方の売り買いが決まりました。" : "売り買いがそろわず、全員0ドルです。",
       ` 稼ぎは 買い手 ${grp.payoffs[0].toFixed(1)} / 売り手1 ${grp.payoffs[1].toFixed(1)} / 売り手2 ${grp.payoffs[2].toFixed(1)} ドル。`]
    : [`${t + 1} / ${R.length} 期目を表示中。`]);
}
$("run").onchange = e => setRun(+e.target.value);
$("grp").onchange = e => setGrp(+e.target.value);
$("prev").onclick = () => { if (t > 0) { t--; render(); } };
$("next").onclick = () => { if (t < grp.rounds.length - 1) { t++; render(); } };
$("play").onclick = () => {
  if (timer) { clearInterval(timer); timer = null; $("play").textContent = "自動再生"; return; }
  $("play").textContent = "止める";
  timer = setInterval(() => { if (t < grp.rounds.length - 1) { t++; render(); } else $("play").click(); }, 2500);
};
document.addEventListener("keydown", e => { if (e.key === "ArrowRight") $("next").click(); if (e.key === "ArrowLeft") $("prev").click(); });
setRun(0);
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("-o", "--out", default="replay_holdout.html")
    a = ap.parse_args()
    data = json.dumps(load(a.run_dir), ensure_ascii=False).replace("</", "<\\/")
    Path(a.out).write_text(PAGE.replace("__DATA__", data), encoding="utf-8")
    print(a.out)


if __name__ == "__main__":
    main()
