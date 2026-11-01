"""#132 の動画の場面と、タイトル画面の文言(code/henrobo/build_video.py と thumbnail.py が読む)。

still(図のファイル)、card(文字, 小見出し)、code(見出し, 等幅の文字) と A(assets のパス) は、build_video.py が渡す。
{"kind": "hero"} は、名前と決まり文句のカード。
"""
DRAW = f"{A}/drawings/建築工事標準詳細図"

CODE = """for p in polys:
    pts=[q for q in p['p'] if q[1] is not None]
    if not all(x0<=a<=x1 and y0<=b<=y1 for a,b in pts):continue
    d=' '.join('%.2f,%.2f'%(a,-b) for a,b in pts)
    s.append('<polyline points="%s" fill="none" stroke="black" stroke-width="0.12"/>'%d)
s.append('</svg>')
open('/tmp/o/a.svg','w').write('\\n'.join(s))"""



TOC = ("1つ目　どうやってAIに図面を読ませたのか\n"
       "2つ目　AIはどう答えたのか\n"
       "3つ目　図面の仕事にとって、何を意味するのか")
SCENES = {
    1: [still(f"{DRAW}/001126048-p09.png"), still("crop-open-door.png")],
    2: [{"kind": "hero"}, card("AIに建築の図面を読ませて、\n3社10のモデルで比べた", "#132 AIと図面のコラボレーション")],
    3: [card(TOC, "今日のお話")],
    4: [card("1つ目\nどうやってAIに図面を読ませたのか"), still(f"{DRAW}/001126048-p09.png"),
        still(f"{DRAW}/001126051-p15.png")],
    5: [card("会議室の入口に、ガラスのない両開きの扉を付けたい。\nどの形状番号を選べばよいか\n\n"
             "すべり出し窓の上に、FIXのらんまを付けたい。\nこの図の形状で表せるか", "問いの例"),
        card("2枚の図面 × 14問\nDXF（CADのデータ）と画像\n10のAI × 1問ずつ = 560回", "比べ方")],
    6: [card("2つ目\nAIはどう答えたのか"), still("score-chart.png"), still("question-chart.png")],
    7: [still("table-L-2-1.png"), still("dxf-vs-image.png"), still("dxf-miss-map.png")],
    8: [code("AIが書いたプログラムの一部（DXFの線を、絵に描き直す）", CODE), still("door-symbols.png")],
    9: [still("table-L-3-2.png"), still("crop-c2-c8.png"), still("table-L-5-3.png")],
    10: [still("crop-open-door.png"), still("table-H-5-3.png")],
    11: [card("3つ目\n図面の仕事にとって、何を意味するのか"),
         card("試したのは、2枚の図面と28問だけ\n採点にもAIを使った", "注意点")],
    12: [{"kind": "hero"}, card("文字で書いてあることは、どのAIも読める\n記号や形は、DXFで差がつく\n"
                                "答えがない問いで、言い切るAIと止まるAIが出る", "へんロボの見立て")],
    13: [card("どうやってAIに図面を読ませたのか → 実務の問いを、10のAIに解かせた\n"
              "AIはどう答えたのか → 文字は読めても、記号と答えがない問いで差\n"
              "何を意味するのか → 任せられる範囲は、何を聞くかで決まる", "まとめ"),
         card("次回\n図面の寸法を読む力を試す")],
}


# タイトル画面とサムネイル。背景は図面を暗くして使う。crop は、図面の幅に対する (左, 上, 幅) の割合
THUMB = {
    "tag": "【AIと図面】",
    "title": ("10のAIに", "建築の図面を読ませた"),
    "sub": "単純な図面ほど、つまずいた",
    "background": f"{DRAW}/001126048-p09.png",
    "crop": (0.04, 0.06, 0.62),
}
