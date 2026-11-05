"""#135 の動画の場面と、タイトル画面の文言(code/henrobo/build_video.py と thumbnail.py が読む)。

still(図のファイル)、card(文字, 小見出し)、code(見出し, 等幅の文字) と A(assets のパス) は、build_video.py が渡す。
{"kind": "hero"} は、名前と決まり文句のカード。場面の番号は、台本(henrobo-script.md)の見出しの番号。
"""
SET = "drawings/house-2ldk.png"

TOC = ("1つ目　AIに出した指示\n"
       "2つ目　AIの結果と、問題点\n"
       "3つ目　図面の修正を、どこまで任せられるのか")

SCENES = {
    1: [still("video-argon-east.png"), still("video-haiku-plan.png")],
    2: [{"kind": "hero"}, card("AIに図面の寸法を変更させて、\n10のモデルで比べた", "#135 AIと図面のコラボレーション")],
    3: [card(TOC, "今日のお話")],
    4: [card("1つ目\nAIに出した指示"), still(SET)],
    5: [still("task-map.png"), still("table-must-move.png")],
    6: [card("北の外壁も、動かすのか（10のうち7つ）\n寝室2も、広がってよいか（4つ）", "試しで、AIが聞き返したこと"),
        card("10のAI × 4つの指示\n渡すのはDXFだけ\nDXFを扱うライブラリは入れさせない\n採点は、正解の図面と比べる採点スクリプト", "比べ方")],
    7: [card("2つ目\nAIの結果と、問題点"), still("table-scores.png")],
    8: [card("1　LDKを広げる時の直し漏れ\n2　採点スクリプトがだまされた\n3　直す前に止まったAI", "問題点")],
    9: [still("table-c3-misses.png")],
    10: [still("video-expected-east.png"), still("video-argon-east.png")],
    11: [still("video-expected-plan.png"), still("video-haiku-plan.png")],
    12: [card("寝室を広げる指示で、GPTの3つが止まった\n「DXFを編集するライブラリがない」\n\nGPT　自信がないと、止まる・聞き返す\nClaude、Gemini　自分で判断して進む",
              "問題点3　止まるAI")],
    13: [card("3つ目\n図面の修正を、どこまで任せられるのか"),
         card("寸法の値と長さが一致しているか\n壁の切れ目は、扉か窓か開口か\n変えてはいけない部屋は、変わっていないか\n図どうしの幅と高さは合っているか",
              "直し漏れを検出するルール"),
         card("AIが直す\n↓\nバリデータで検証\n↓\n違反をAIに差し戻す", "ループ"),
         card("データの持ち方を見直す\nバリデータを作る\nAIに差し戻すループを回す", "へんロボの見立て")],
    14: [card("AIに出した指示 → 家の図面一式で4段階\n"
              "AIの結果と、問題点 → 窓は全員、LDKを完全に直せたのは2つ\n"
              "どこまで任せられるのか → 差し戻すループを先に組む", "まとめ"),
         card("次回\nAIに、CADソフトを操作させる\n（LibreCADにMCPを加える）")],
}

# タイトル画面とサムネイル。背景は図面を暗くして使う。crop は、図面の幅に対する (左, 上, 幅) の割合
THUMB = {
    "tag": "【AIと図面】",
    "title": ("10のAIに", "寸法を変えさせた"),
    "sub": "直ったようで、直っていない",
    "background": f"{A}/{SET}",
    "crop": (0.03, 0.02, 0.5),
}
