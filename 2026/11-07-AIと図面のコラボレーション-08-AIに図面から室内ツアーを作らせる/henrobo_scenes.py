"""#137 の動画の場面と、タイトル画面の文言(code/henrobo/build_video.py と thumbnail.py が読む)。

still(図のファイル)、card(文字, 小見出し)、code(見出し, 等幅の文字)、clip(録画, 始め秒, 終わり秒) と A(assets のパス) は、
build_video.py が渡す。{"kind": "hero"} は、名前と決まり文句のカード。場面の番号は、台本(henrobo-script.md)の見出しの番号。
録画は、公開したページ(docs/137-house-tour/)を chrome-devtools の screencast で撮ったもの(~/henrobo-video/137/)。
"""
V = "~/henrobo-video/137"
TOUR, CUT, EXT, NIGHT = f"{V}/rec-autotour.mp4", f"{V}/rec-cutaway.mp4", f"{V}/rec-exterior.mp4", f"{V}/rec-night.mp4"

TOC = ("1つ目　作らせたものと、1回目の出来\n"
       "2つ目　指示を重ねて、育てる\n"
       "3つ目　図面から立体を作るとき、人が確かめること")

SCENES = {
    1: [clip(TOUR, 2, 60)],
    2: [{"kind": "hero"}, card("AIに図面から\n3Dの室内ツアーを作らせた", "#137 AIと図面のコラボレーション")],
    3: [card(TOC, "今日のお話")],
    4: [card("1つ目\n作らせたものと、1回目の出来"), clip(EXT, 0, 22),
        card("AI　Claude Opus 5.5\n作り方　three.js で Webページ（HTML 1つ）\n\n"
             "渡したもの　図面（DXF）、仕上表\n頼んだもの　外観を回す「パース」と、歩ける「室内ツアー」", "作らせたもの")],
    5: [still("opus-cutaway.png"),
        card("外壁の窓 11 と外の扉 2　位置・幅・高さが一致\n間仕切りと室内の扉　位置が一致\n"
             "天井高 2,400、軒の高さ、勾配 4/10、軒の出 600　一致\n\n人はコードを書いていない", "1回目（10分47秒）を、間取りのデータと照らし合わせた")],
    6: [still("r1-exterior.png")],
    7: [card("2つ目\n指示を重ねて、育てる"), still("fig-r1-r2-exterior.jpg")],
    8: [still("r2-cutaway.png"), still("r2-ldk.png")],
    9: [clip(CUT, 0, 22)],
    10: [clip(TOUR, 0, 67)],
    11: [clip(NIGHT, 0, 18)],
    12: [card("3つ目\n図面から立体を作るとき、人が確かめること"),
          card("1　最初の版で、寸法を確かめる\n　　見た目は、あとから足せる\n\n"
               "2　図面にないものを、分けて示す\n　　設備の高さ、家具、照明は「仮の決め」", "へんロボの見立て")],
    13: [card("作らせたものと、1回目の出来 → 10分ほどで、寸法の正しい家\n"
              "指示を重ねて、育てる → 3回で、家具や自動ツアーまで\n"
              "人が確かめること → 最初の寸法と、図面にないものの区別", "まとめ"),
         card("次回\n同じ指示を、ほかのモデルにも")],
}

# タイトル画面とサムネイル。背景は、3回目の版の間取り(家具と広さ)を暗くして使う。crop は、図の幅に対する (左, 上, 幅) の割合
THUMB = {
    "tag": "【AIと図面】",
    "title": ("AIが図面から", "室内ツアーを作った"),
    "sub": "寸法は、図面とすべて一致",
    "background": f"{A}/r3-cutaway.png",
    "crop": (0.2, 0.12, 0.6),
}
