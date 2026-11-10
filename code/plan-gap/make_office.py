"""利用者ごとの書類(data-v2/docs)を、事業所全体の形に組み替える。

- 計画: 24人分のケアプランと訪問介護計画書を並べる
- 記録: 全員のサービス提供記録を1つの CSV(日付と時間の順)にまとめる。介護ソフトから出した実績の一覧を想定
出力: data-v3/docs/office.md と、答えの写し
使い方: python3 make_office.py
"""
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "data-v2"
OUT = HERE / "data-v3"


def main():
    plans, rows = [], []
    for p in sorted((SRC / "docs").glob("U*.md")):
        uid = p.stem
        text = p.read_text()
        head, rec = text.split("## 3. サービス提供記録(2026年9月)")
        plans.append(head.replace("ためし訪問介護ステーション(架空)。対象月は2026年9月。\n\n", "").strip())
        for line in rec.splitlines():
            if not line.startswith("| ") or line.startswith("| 日付") or line.startswith("|---"):
                continue
            c = [x.strip() for x in line.strip("|").split("|")]
            m, d = map(int, c[0].split("/"))
            t = c[2] if c[2][0].isdigit() else "99:99"
            rows.append(((m, d, t, uid), [c[0], c[1], uid] + c[2:]))
    rows.sort(key=lambda r: r[0])
    csv = ["日付,曜日,利用者,時間,担当,区分,実施した内容,特記事項"]
    csv += [",".join(x.replace(",", "、") for x in r) for _, r in rows]
    doc = ("# ためし訪問介護ステーション(架空) 2026年9月の点検用書類\n\n"
           "## 1. 利用者ごとの計画(24人)\n\n" + "\n\n---\n\n".join(plans) +
           "\n\n## 2. サービス提供の実績(介護ソフトから出力、全利用者、日付順)\n\n```csv\n" + "\n".join(csv) + "\n```\n")
    (OUT / "docs").mkdir(parents=True, exist_ok=True)
    (OUT / "docs" / "office.md").write_text(doc)
    shutil.copy(SRC / "answers.json", OUT / "answers.json")
    print(len(rows), "rows", len(doc), "chars")


if __name__ == "__main__":
    main()
