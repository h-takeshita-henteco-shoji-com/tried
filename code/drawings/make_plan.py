"""寸法の正解が決まった平面図を DXF で作る(#138)。

#132 の標準詳細図は PDF から変換したため、寸法が「寸法」の部品として入っていない。
座標も用紙上の長さで、図は縮尺どおりに正確ではない。座標から長さを求める問いの正解を厳密に決めるため、
小さな事務所(2部屋)の平面図を、実物の mm 座標で描く。

- 通り芯: X1・X2・X3(3,600 間隔)、Y1・Y2(5,400)
- 壁: 外壁 150、間仕切り 100。どちらも通り芯が壁の中心
- 出入口の扉 900(寸法あり)、部屋の間の扉 800(寸法なし。座標から求める問い用)
- 窓 1,800(寸法あり)。窓から X3 までは図形では 900 だが、寸法の値は「1,200」と書く(食い違いを見つける問い用)
- 寸法は DIMENSION の部品として入れる。単位は mm($INSUNITS=4)

使い方: uv run --with ezdxf python code/drawings/make_plan.py <出力.dxf>
"""
import sys

import ezdxf

JP_STYLE = "kst32b"  # LibreCAD で日本語を出すための文字スタイル名(pdf_to_dxf.py と同じ)
EXT, PART = 150, 100
X1, X2, X3 = 0, 3600, 7200
Y1, Y2 = 0, 5400
DOOR_IN = (600, 1500)       # 出入口(Y1 の壁)
DOOR_MID = (2000, 2800)     # 部屋の間の扉(X2 の壁、y の範囲)
WINDOW = (4500, 6300)       # 窓(Y2 の壁)


def rect(m, x0, y0, x1, y1, layer="WALL"):
    m.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": layer})


def main(out):
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4
    doc.styles.add(JP_STYLE, font="kst32b.lff")
    for name, color, lt in (("WALL", 7, "CONTINUOUS"), ("GRID", 1, "CENTER"), ("DOOR", 3, "CONTINUOUS"),
                            ("WINDOW", 4, "CONTINUOUS"), ("DIM", 2, "CONTINUOUS"), ("TEXT", 7, "CONTINUOUS")):
        doc.layers.add(name, color=color, linetype=lt)
    m = doc.modelspace()
    e, p = EXT / 2, PART / 2

    # 外壁(開口の所で切る)
    rect(m, X1 - e, Y1 - e, DOOR_IN[0], Y1 + e)
    rect(m, DOOR_IN[1], Y1 - e, X3 + e, Y1 + e)
    rect(m, X1 - e, Y2 - e, WINDOW[0], Y2 + e)
    rect(m, WINDOW[1], Y2 - e, X3 + e, Y2 + e)
    rect(m, X1 - e, Y1 + e, X1 + e, Y2 - e)
    rect(m, X3 - e, Y1 + e, X3 + e, Y2 - e)
    # 間仕切り
    rect(m, X2 - p, Y1 + e, X2 + p, DOOR_MID[0])
    rect(m, X2 - p, DOOR_MID[1], X2 + p, Y2 - e)

    # 扉: 開く向きの線と円弧
    x0, x1 = DOOR_IN
    m.add_line((x0, Y1 + e), (x0, Y1 + e + (x1 - x0)), dxfattribs={"layer": "DOOR"})
    m.add_arc((x0, Y1 + e), x1 - x0, 0, 90, dxfattribs={"layer": "DOOR"})
    y0, y1 = DOOR_MID
    m.add_line((X2 + p, y0), (X2 + p + (y1 - y0), y0), dxfattribs={"layer": "DOOR"})
    m.add_arc((X2 + p, y0), y1 - y0, 0, 90, dxfattribs={"layer": "DOOR"})
    # 窓: 壁の中に3本の線
    for dy in (-e, 0, e):
        m.add_line((WINDOW[0], Y2 + dy), (WINDOW[1], Y2 + dy), dxfattribs={"layer": "WINDOW"})

    # 通り芯と符号
    for name, x in (("X1", X1), ("X2", X2), ("X3", X3)):
        m.add_line((x, Y1 - 1800), (x, Y2 + 2000), dxfattribs={"layer": "GRID"})
        m.add_circle((x, Y2 + 2300), 300, dxfattribs={"layer": "GRID"})
        m.add_text(name, height=250, dxfattribs={"layer": "GRID", "style": JP_STYLE}).set_placement(
            (x, Y2 + 2300), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    for name, y in (("Y1", Y1), ("Y2", Y2)):
        m.add_line((X1 - 2000, y), (X3 + 1500, y), dxfattribs={"layer": "GRID"})
        m.add_circle((X1 - 2300, y), 300, dxfattribs={"layer": "GRID"})
        m.add_text(name, height=250, dxfattribs={"layer": "GRID", "style": JP_STYLE}).set_placement(
            (X1 - 2300, y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    # 寸法
    ov = {"dimtxt": 200, "dimasz": 120, "dimexo": 80, "dimgap": 60, "dimtxsty": JP_STYLE, "dimtad": 1, "dimdec": 0}

    def dim(a, b, base, angle=0, text=None):
        # 値は「3,600」の形で書く。部品には実際の長さも残る(DXF の実測値)
        if text is None:
            text = f"{round(abs((b[1] - a[1]) if angle == 90 else (b[0] - a[0]))):,}"
        d = m.add_linear_dim(base=base, p1=a, p2=b, angle=angle, text=text, override=ov,
                             dxfattribs={"layer": "DIM"})
        d.render()

    dim((X1, Y2), (X2, Y2), (0, Y2 + 1300))
    dim((X2, Y2), (X3, Y2), (0, Y2 + 1300))
    dim((X1, Y2), (X3, Y2), (0, Y2 + 1800))
    dim((X1, Y1), (X1, Y2), (X1 - 1300, 0), angle=90)
    dim((X1, Y1), (DOOR_IN[0], Y1), (0, Y1 - 800))
    dim((DOOR_IN[0], Y1), (DOOR_IN[1], Y1), (0, Y1 - 800))
    dim((WINDOW[0], Y2), (WINDOW[1], Y2), (0, Y2 + 700))
    dim((WINDOW[1], Y2), (X3, Y2), (0, Y2 + 700), text="1,200")  # わざと図形(900)と合わない値
    dim((X3 - e, 3800), (X3 + e, 3800), (0, 4300))

    # 文字
    def text(s, at, h=250):
        m.add_text(s, height=h, dxfattribs={"layer": "TEXT", "style": JP_STYLE}).set_placement(
            at, align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)

    text("事務室", (X1 + 1800, 3500))
    text("会議室", (X2 + 1800, 3500))
    text("出入口", (sum(DOOR_IN) / 2, Y1 - 1400), 200)
    text("窓", (sum(WINDOW) / 2, Y2 + 350), 200)
    text("事務所 平面図   S=1/50   単位: mm", (X3 / 2, Y1 - 2500), 300)
    doc.saveas(out)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
