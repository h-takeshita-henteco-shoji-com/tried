"""利用者ごとの書類を AI(claude -p)に読ませ、計画と提供のずれを挙げさせる。

使い方: python3 run_check.py <model> <mode> [run番号]
  model: haiku / sonnet / opus
  mode : list(点検の観点を渡す) / free(観点を渡さない)
出力: data/out/<model>-<mode>-<run>/Uxx.json
"""
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
import os
DATA = HERE / os.environ.get("DATA", "data")
DOCS = DATA / "docs"

COMMON = """あなたは訪問介護事業所のサービス提供責任者です。運営指導の前に、利用者1人分の書類を点検します。
渡すのは、ケアプラン(居宅サービス計画書)、訪問介護計画書、2026年9月のサービス提供記録です。
ケアプラン・訪問介護計画・実際の提供の間のずれや、手続きの不備を挙げてください。
不備がなければ、空の一覧を返してください。問題のないものを不備として挙げないでください。
"""

LIST = """
点検の観点(category に使う記号):
- A: 曜日や時間を変えて提供しているのに、計画が変わっていない
- B: 計画にない内容を提供している
- C: 訪問介護計画の説明と同意が、提供の開始より後になっている
- D: 訪問介護計画の内容が、ケアプランとずれている
- E: 計画より多い回数を提供している
- F: 計画の期間が切れたまま提供している
- G: その他
"""

FORMAT = """
JSON だけを返してください。形:
{"findings": [{"category": "%s", "where": "どの書類・日付・項目か", "what": "何がずれているか", "evidence": "どの書類のどの記載と比べたか"}]}
"""


BILL = """
各指摘には、介護報酬の算定への影響を impact に付けてください。
- 1: その提供は算定できない(返還の対象になりうる)
- 2: 算定はできるが、計画の見直しが必要
- 3: 運営基準の不備で、算定の可否とは別の問題
- 4: 算定に影響しない
basis には、そう判断した理由(どのルールか)を短く書いてください。
"""

RULES = """
参考にしてよいルール(厚生労働省の基準・通知・Q&A の抜粋):
- 指定居宅サービス等基準 第16条: 居宅サービス計画が作成されている場合は、当該計画に沿った指定訪問介護を提供しなければならない。
- 同 第24条: 訪問介護計画は、既に居宅サービス計画が作成されている場合は、当該計画の内容に沿って作成しなければならない。サービス提供責任者は、訪問介護計画の作成に当たっては、その内容について利用者又はその家族に対して説明し、利用者の同意を得なければならない。作成後は実施状況を把握し、必要に応じて変更する(変更にも説明と同意が要る)。
- 老企36号 第2の2(4): 訪問介護の所要時間は、実際に行われた時間ではなく、訪問介護計画に位置付けられた内容の指定訪問介護を行うのに要する標準的な時間とする。報酬は、その時間がいずれの時間区分に該当するかで決まる。実績が時間区分を下回る状態が1か月以上続くなど常態化した場合は、介護支援専門員と調整の上、訪問介護計画を見直す。
- Q&A(令和6年4月18日 Vol.4): 緊急時訪問介護加算は、利用者や家族の要請を受け、居宅サービス計画にない時間帯に身体介護中心の訪問を行った場合のもの。算定時も、訪問介護計画は必要な修正を行い、居宅サービス計画も変更する(サービス利用票の変更など最小限でよい)。
- Q&A(平成24年3月16日 Vol.1): 当日の状況でサービス内容の変更が必要になったときは、介護支援専門員とサービス提供責任者が連携し、介護支援専門員が認める(事後の判断を含む)範囲で内容を変更し、変更後の内容に応じた所要時間で算定する。
"""


def prompt(mode):
    if mode in ("bill", "billrule"):
        f = FORMAT.replace('"evidence": "どの書類のどの記載と比べたか"', '"evidence": "どの書類のどの記載と比べたか", "impact": 1〜4, "basis": "理由"')
        return COMMON + LIST + BILL + (RULES if mode == "billrule" else "") + f % "A〜G"
    if mode == "list":
        return COMMON + LIST + FORMAT % "A〜G"
    return COMMON + FORMAT % "短い見出し"


def call(model, system, doc):
    cmd = ["claude", "-p", "--model", model, "--output-format", "text", "--tools", "",
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--system-prompt", system]
    for attempt in range(3):
        r = subprocess.run(cmd, input=doc, capture_output=True, text=True, timeout=900, cwd="/tmp")
        t = r.stdout.strip()
        if r.returncode == 0 and t:
            if "```" in t:
                t = t.split("```")[1].removeprefix("json").strip()
            try:
                return json.loads(t[t.find("{"): t.rfind("}") + 1])
            except Exception:
                pass
        time.sleep(5 * (attempt + 1))
    return {"error": r.stdout[-500:] + r.stderr[-500:]}


def main():
    model, mode = sys.argv[1], sys.argv[2]
    run = sys.argv[3] if len(sys.argv) > 3 else "1"
    out = DATA / "out" / f"{model}-{mode}-{run}"
    out.mkdir(parents=True, exist_ok=True)
    if run.startswith("all"):  # 24人分を1回でまとめて渡す
        system = prompt(mode).replace("利用者1人分の書類", "利用者24人分の書類").replace(
            '{"category"', '{"user": "利用者の番号(U01など)", "category"')
        docs = sorted(DOCS.glob("U*.md"))
        if (DOCS / "office.md").exists():  # 事業所全体の形(計画と、全員分の実績の CSV)
            text = (DOCS / "office.md").read_text()
            system = system.replace("2026年9月のサービス提供記録です", "2026年9月のサービス提供の実績(全利用者を日付順にまとめた CSV)です")
            docs = [Path(u + ".md") for u in sorted(json.loads((DATA / "answers.json").read_text()))]
        else:
            text = "\n\n---\n\n".join(p.read_text() for p in docs)
        t0 = time.time()
        res = call(model, system, text)
        sec = round(time.time() - t0, 1)
        (out / "_raw.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
        for p in docs:
            fs = [f for f in res.get("findings", []) if f.get("user") == p.stem]
            (out / f"{p.stem}.json").write_text(json.dumps({"findings": fs, "sec": sec}, ensure_ascii=False, indent=1))
        print("all", len(res.get("findings", [])), sec, res.get("error", "")[:300])
        return
    system = prompt(mode)
    todo = [p for p in sorted(DOCS.glob("U*.md")) if not (out / f"{p.stem}.json").exists()]

    def one(p):
        t0 = time.time()
        res = call(model, system, p.read_text())
        res["sec"] = round(time.time() - t0, 1)
        (out / f"{p.stem}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(p.stem, len(res.get("findings", [])), res["sec"], flush=True)

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(one, todo))


if __name__ == "__main__":
    main()
