"""#146 の動画の場面と、タイトル画面の文言(code/henrobo/build_video.py と thumbnail.py が読む)。

still(図のファイル)、card(文字, 小見出し)、code(見出し, 等幅の文字)、clip(録画, 始め秒, 終わり秒) と A(assets のパス) は、
build_video.py が渡す。{"kind": "hero"} は、名前と決まり文句のカード。場面の番号は、台本(henrobo-script.md)の見出しの番号。
録画は ~/henrobo-video/146/P-1-opus.mp4(作図の早送り。0:12〜2:01 が本編、前後は札)。
0:12 図面を読む、0:23 外壁の層と柱、0:59 通り芯・文字・寸法、1:44 画像で見直して直す、2:01 保存と結果。
"""
REC = "~/henrobo-video/146/P-1-opus.mp4"

TOC = ("1つ目　作図の条件と、AIが描く様子\n"
       "2つ目　外壁の厚みに、誰が気づいたか\n"
       "3つ目　AIに図面を任せるとき、人が確かめること")

SCENES = {
    1: [clip(REC, 23, 115)],
    2: [{"kind": "hero"}, card("AIにCADで平面詳細図を描かせ、\n7つのモデルで比べた", "#146 AIと図面のコラボレーション")],
    3: [card(TOC, "今日のお話")],
    4: [card("1つ目\n作図の条件と、AIが描く様子"), still("fig-conditions-p1.png")],
    5: [still("fig-try1.jpg"),
        card("1　柱を置く交点のうち4つが、窓の開口の中にある\n"
             "2　南と西の窓が、範囲の端（X3・Y3）をまたいでいる\n"
             "3　文字の高さ 30 は、1/50 で印刷すると 0.6mm", "Opus が挙げた「確認したいこと」")],
    6: [clip(REC, 12, 59)],
    7: [clip(REC, 59, 121), still("librecad-P-1-opus.png")],
    8: [card("2つ目\n外壁の厚みに、誰が気づいたか"), still("compare-P-1-librecad.jpg")],
    9: [still("fig-wall.png")],
    10: [still("fig-behavior-p1.png")],
    11: [still("fig-behavior-p1.png")],
    12: [card("3つ目\nAIに図面を任せるとき、人が確かめること"), still("fig-p2-cut.jpg"),
         card("9\n$HANDSEED\nD　← 値の種類を表す番号が入るはずの行\n20000",
              "Gemini 3.8 Flash が書いた DXF の一部（CADはこの行で読むのをやめる）")],
    13: [card("1　最初に1回だけ試し、「確認したいこと」を読む\n\n"
              "2　何も書き出さずに進んだ図は、人が仕様と照らし合わせる\n\n"
              "3　保存したファイルが開けるかを、道具か人で確かめる", "へんロボの見立て")],
    14: [card("作図の条件と、AIが描く様子 → 指示文の誤りを指摘され、直して描いた\n"
              "外壁の厚みに、誰が気づいたか → Claude は気づき、GPT は聞き、Gemini は触れず\n"
              "人が確かめること → 最初の答え、黙った所、ファイルが開けるか", "まとめ"),
         card("次回\n食い違いを仕込んで、気づけるかを比べる")],
}

# タイトル画面とサムネイル。背景は、Opus が MCP で描いた平面詳細図を暗くして使う。crop は、図の幅に対する (左, 上, 幅) の割合
THUMB = {
    "tag": "【AIと図面】",
    "title": ("AIがCADで", "平面詳細図を描いた"),
    "sub": "食い違いに、誰が気づいたか",
    "background": f"{A}/librecad-P-1-opus.png",
    "crop": (0.0, 0.1, 1.0),
}
