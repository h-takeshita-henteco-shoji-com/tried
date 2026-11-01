"""#132 の記事用に、特徴的な問いの「答えの型」を表の画像にする。

note では表を使えないため、表は画像にする。
答えの型と、該当したLLM、判定は、results/2026-11-01 の採点の記録から人が読んでまとめたもの。

使い方: uv run --with matplotlib python answer_tables.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parents[2] / "2026/10-29-AIと図面のコラボレーション-01-AIに図面が何を表すか説明させる/assets"
TEXT, MUTED, SURFACE, LINE, HEAD = "#0b0b0b", "#52514e", "#fcfcfb", "#d9d8d2", "#f0efec"
GRADE_COLOR = {"正答": "#0ca30c", "適切な保留": "#0ca30c", "部分正答": "#fab219", "誤答": "#d03b3b",
               "誤った断定": "#ec835a", "不要な保留": "#8f8d87"}

TABLES = [
    ("table-L-2-1.png",
     "L-2-1 会議室の入口に、ガラスのない両開きの扉を付けたい。どの形状番号を選べばよいか",
     "正解: A-3（フラッシュ戸の区分の、両開きの形）",
     [("A-3。一部は「がらり付きなら A-6」と添えた", "17件（下の3件以外のすべて）", "正答"),
      ("A-4（がらり付きの片開き）", "Claude Sonnet 5.5（DXF）", "誤答"),
      ("D-1（ふすまの片開き）", "GPT-6 Luna（DXF）", "誤答"),
      ("形状番号だけでは特定できない", "GPT-6 Luna（画像）", "不要な保留")]),
    ("table-L-3-2.png",
     "L-3-2 すべり出し窓の上に、FIX のらんまを付けたい。この図の形状で表せるか",
     "正解: 表せない。すべり出し（C-8）にはらんまがなく、らんま付きの形にもすべり出しはない。別に検討・確認が要る",
     [("表せない。理由を挙げ、別に指定・確認が要ると述べた",
       "Claude Fable 5.1（両方）、Sonnet 5.5（両方）、Opus 5.5（画像）、GPT-6 Astra（両方）、6.1 Sol（DXF）", "正答"),
      ("表せない。理由は正しいが、次にどうするかを言わない",
       "Gemini 3.8 Flash（両方）、4 Argon（両方）、GPT-6.1 Sol（画像）、Claude Haiku 5.5（DXF）", "部分正答"),
      ("表せる。らんま付きの C-2 を、すべり出し窓と読み違えた",
       "Claude Opus 5.5（DXF）、Haiku 5.5（画像）、GPT-6.1 Terra（DXF）、6 Luna（両方）", "誤答"),
      ("この図では、表せるかどうか分からない", "GPT-6.1 Terra（画像）", "不要な保留")]),
    ("table-L-5-3.png",
     "L-5-3 会議室の入口に A-3 を使う。扉の幅は何 mm になるか",
     "正解: この図では決まらない。両開きの標準は 1,800 と 1,900 の2つで、W は特記事項 2）で決める",
     [("決まらない。候補の2つと、特記で決めることを挙げた",
       "Claude Fable 5.1（DXF）、Gemini 4 Argon（両方）、3.8 Flash（画像）", "適切な保留"),
      ("候補の2つ（1,800 と 1,900）は挙げたが、特記で決めることを言わない",
       "Claude Opus 5.5（両方）、Fable 5.1（画像）、Sonnet 5.5（画像）、GPT-6.1 Sol（両方）、6 Astra（画像）、6.1 Terra（画像）、Gemini 3.8 Flash（DXF）",
       "部分正答"),
      ("決まらないとだけ言い、候補を挙げない", "Claude Haiku 5.5（両方）、GPT-6 Astra（DXF）、6 Luna（画像）", "部分正答"),
      ("A-3 を片開きや親子開きと読み違えた。または幅を言い切った",
       "Claude Sonnet 5.5（DXF）、GPT-6.1 Terra（DXF）、6 Luna（DXF）", "誤答")]),
    ("table-H-5-3.png",
     "H-5-3 引き戸を開けたとき、戸が寄る部分の下にも基礎は必要か",
     "正解（採点の途中で広げた）: 戸車がレールを走るので必要と判断でき、範囲だけが特記事項 3）で決まる。決まらないと保留しても可",
     [("必要と考えられる。範囲は特記で決まる",
       "Claude Opus 5.5（両方）、Fable 5.1（画像）、Sonnet 5.5（画像）、Gemini 4 Argon（両方）、GPT-6 Astra（両方）、6.1 Sol（画像）", "正答"),
      ("この図では決まらない。範囲は特記で決まる",
       "Claude Fable 5.1（DXF）、Sonnet 5.5（DXF）、Haiku 5.5（両方）、GPT-6.1 Sol（DXF）、6.1 Terra（両方）", "適切な保留"),
      ("必要。図面にそう描かれている、と言い切った", "Gemini 3.8 Flash（両方）、GPT-6 Luna（両方）", "誤った断定")]),
]


def wrap(s, n):
    """日本語を文字数で折り返す（英字の語は途中で切らない）。"""
    lines, cur = [], ""
    for tok in __import__("re").findall(r"[A-Za-z0-9.\-]+|.", s):
        if len(cur) + len(tok) > n and cur:
            lines.append(cur)
            cur = tok.lstrip()
        else:
            cur += tok
    return "\n".join(lines + [cur])


def models(s):
    """「Claude Opus 5.5（両方）、Fable 5.1（画像）」のように省いた会社名を補い、1行に1つにする。"""
    out, prefix = [], ""
    for item in s.split("、"):
        if item.startswith("Claude "):
            prefix = "Claude "
        elif item.startswith("GPT-"):
            prefix = "GPT-"
        elif item.startswith("Gemini "):
            prefix = "Gemini "
        elif prefix:
            item = prefix + item
        out.append(item)
    return "\n".join(out)


def draw(fname, title, correct, rows):
    cols = [("答えの型", 0.0, 0.40, 22), ("答えたLLM（渡し方）", 0.40, 0.84, 24), ("判定", 0.84, 1.0, 8)]
    cell = [[wrap(r[0], 24), models(r[1]), r[2]] for r in rows]
    heights = [max(c.count("\n") + 1 for c in row[:2]) for row in cell]
    unit = 0.36
    total = 1.3 + unit * (1 + sum(h + 0.5 for h in heights))
    fig = plt.figure(figsize=(12, total), facecolor=SURFACE)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(0, 1)
    ax.set_ylim(total, 0)
    ax.axis("off")
    ax.text(0, 0.2, wrap(title, 52), fontsize=13, color=TEXT, va="top", weight="bold")
    ax.text(0, 0.62, wrap(correct, 88), fontsize=10.5, color=MUTED, va="top")
    y = 1.3
    ax.add_patch(Rectangle((0, y), 1, unit, facecolor=HEAD, edgecolor="none"))
    for name, x0, x1, _ in cols:
        ax.text(x0 + 0.01, y + unit / 2, name, fontsize=10.5, color=TEXT, va="center")
    y += unit
    for row, h in zip(cell, heights):
        rh = unit * (h + 0.5)
        ax.plot([0, 1], [y + rh, y + rh], color=LINE, linewidth=1)
        ax.text(0.01, y + rh / 2, row[0], fontsize=10.5, color=TEXT, va="center", linespacing=1.5)
        ax.text(0.41, y + rh / 2, row[1], fontsize=10, color=TEXT, va="center", linespacing=1.5)
        c = GRADE_COLOR[row[2]]
        ax.add_patch(FancyBboxPatch((0.85, y + rh / 2 - 0.15), 0.012, 0.3, boxstyle="round,pad=0",
                                    facecolor=c, edgecolor="none"))
        ax.text(0.87, y + rh / 2, row[2], fontsize=10.5, color=TEXT, va="center")
        y += rh
    fig.savefig(OUT / fname, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def main():
    for f in font_manager.findSystemFonts():
        if "NotoSansJP" in f:
            font_manager.fontManager.addfont(f)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
    for t in TABLES:
        draw(*t)
    print("ok")


if __name__ == "__main__":
    main()
