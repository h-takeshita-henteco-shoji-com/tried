"""#133 の正解(建具の一覧と建具表)を、図面のもとの間取りのデータ(make_house.py)から作る。

AI には渡さない。正解の記録(answer-key/T-house.md)の「正解」の節に貼る。
扉は、開き戸(DOORS)、引き戸(SLIDES)、折れ戸(FOLDS)。扉のない開口(OPENINGS)は数えない。
幅は壁の開口の幅。高さは、外壁の窓と扉だけが立面図にある(OPENING_H)。室内の扉の高さは、図面から決まらない。
部屋は、建具がある壁の両側の部屋。

使い方: uv run --with ezdxf --with shapely python code/drawings/answer_133.py
"""
import sys
from collections import Counter, defaultdict

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import make_house as H  # noqa: E402

# 部屋の範囲 (x0, y0, x1, y1)。make_house.py の壁の中心線から読んだ
ROOMS = {
    "LDK": (0, 0, 4550, 5460), "玄関": (4550, 0, 6370, 1820), "ホール": (4550, 1820, 6370, 5460),
    "寝室1": (6370, 0, 10010, 3640), "廊下": (6370, 3640, 7280, 4550), "クローゼット": (7280, 3640, 10010, 4550),
    "寝室2": (6370, 4550, 10010, 7280), "トイレ": (4550, 3640, 5460, 5460), "パントリー": (0, 5460, 910, 7280),
    "浴室": (910, 5460, 2730, 7280), "洗面脱衣": (2730, 5460, 4550, 7280), "ファミクロ": (4550, 5460, 6370, 7280),
}


def room_at(x, y):
    for n, (x0, y0, x1, y1) in ROOMS.items():
        if x0 < x < x1 and y0 < y < y1:
            # 玄関とホールの境は上がり框(y=1,820)。トイレはホールの中の部屋
            if n == "ホール" and 4550 < x < 5460 and 3640 < y < 5460:
                return "トイレ"
            return n
    return "屋外"


def sides(o, at, a, b):
    m = (a + b) / 2
    pts = [(m, at - 100), (m, at + 100)] if o == "h" else [(at - 100, m), (at + 100, m)]
    return sorted({room_at(*p) for p in pts}, key=lambda r: r == "屋外")


def window_kind(n):
    lo, hi = H.OPENING_H[n]
    return "掃き出し窓" if lo == 0 else "高窓" if lo >= 1400 else "腰窓"


def items():
    out = []
    for n, o, at, a, b, *_ in H.DOORS:
        h = H.OPENING_H.get(n)
        out.append(("扉", "開き戸", n, b - a, (h[1] - h[0]) if h else None, sides(o, at, a, b), (o, at, a, b)))
    for n, o, at, a, b, *_ in H.SLIDES:
        out.append(("扉", "引き戸", n, b - a, None, sides(o, at, a, b), (o, at, a, b)))
    for n, o, at, a, b, *_ in H.FOLDS:
        out.append(("扉", "折れ戸", n, b - a, None, sides(o, at, a, b), (o, at, a, b)))
    for n, o, at, a, b in H.WINDOWS:
        lo, hi = H.OPENING_H[n]
        out.append(("窓", window_kind(n), n, b - a, hi - lo, sides(o, at, a, b), (o, at, a, b)))
    return out


def main():
    its = items()
    print("## 建具の一覧(平面図の座標。X1・Y1 の交点が原点)\n")
    for k, kind, n, w, h, rs, (o, at, a, b) in its:
        pos = f"y={at}, x={a}〜{b}" if o == "h" else f"x={at}, y={a}〜{b}"
        print(f"- {k} {kind} {n}: 幅 {w}、高さ {h if h else '不明'}、{'|'.join(rs)}、{pos}")
    print(f"\n合計 {len(its)}(扉 {sum(i[0] == '扉' for i in its)}、窓 {sum(i[0] == '窓' for i in its)})")
    print("種類別:", dict(Counter(i[1] for i in its)))
    by_room = defaultdict(int)
    for i in its:
        for r in i[5]:
            if r != "屋外":
                by_room[r] += 1
    print("部屋別(室内の扉は両側の部屋に数える):", dict(by_room))
    print("\n## 建具表(同じ種類・同じ寸法をまとめる)\n")
    groups = defaultdict(list)
    for i in its:
        groups[(i[0], i[1], i[3], i[4])].append(i)
    for (k, kind, w, h), g in sorted(groups.items(), key=lambda kv: (kv[0][0] != "窓", kv[0][1], -kv[0][2])):
        rooms = "、".join("|".join(i[5]) for i in g)
        print(f"- {k} {kind} 幅 {w} × 高さ {h if h else '不明'} … {len(g)} か所({rooms})")
    print("\n扉のない開口(数えない): パントリー(LDK|パントリー、幅 700)、寝室1のクローゼット(幅 2,500)")


if __name__ == "__main__":
    main()
