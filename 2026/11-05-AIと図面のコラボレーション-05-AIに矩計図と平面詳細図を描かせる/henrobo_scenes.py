"""#136 の動画の場面と、タイトル画面の文言(code/henrobo/build_video.py と thumbnail.py が読む)。

still(図のファイル)、card(文字, 小見出し)、code(見出し, 等幅の文字)、clip(録画, 始め秒, 終わり秒) と A(assets のパス) は、
build_video.py が渡す。{"kind": "hero"} は、名前と決まり文句のカード。場面の番号は、台本(henrobo-script.md)の見出しの番号。
録画は ~/henrobo-video/136/K-1-opus.mp4(作図の早送り。0:12〜1:56 が本編、前後は札)。
"""
REC = "~/henrobo-video/136/K-1-opus.mp4"

TOC = ("1つ目　作図の条件と、AIが描く様子\n"
       "2つ目　7つのAIの結果と、違い\n"
       "3つ目　AIに図面を描かせるとき、人が決めること")

SCENES = {
    1: [clip(REC, 22, 112)],
    2: [{"kind": "hero"}, card("AIにCADを操作させて矩計図を描かせ、\n7つのモデルで比べた", "#136 AIと図面のコラボレーション")],
    3: [card(TOC, "今日のお話")],
    4: [card("1つ目\n作図の条件と、AIが描く様子"), still("fig-conditions.png")],
    5: [card("高さ　基礎上端 GL+400、床 GL+561\n　　　天井 床+2,400、軒の高さ 床+2,750\n"
             "床・壁・天井・屋根の材料と厚み（20ほど）\n勾配 4/10、軒の出 600\n\n"
             "「仕様と既存の図面が食い違うときは、描く前に聞いてください」", "AIに渡した仕様"),
        card("MCP　AIが LibreCAD を操作して描く\nDXFを直接書く　ファイルの中身をテキストとして書く\n\n"
             "AIは7つ（Claude 4、GPT 1、Gemini 2）", "描き方は2通り")],
    6: [clip(REC, 12, 33)],
    7: [clip(REC, 33, 116)],
    8: [card("2つ目\n7つのAIの結果と、違い"), still("fig-behavior.png")],
    9: [still("fig-wall.png")],
    10: [still("fig-behavior.png")],
    11: [still("fig-insulation.png")],
    12: [still("video-dimpoints.png"), still("video-dimpoints-eave.png")],
    13: [card("3つ目\nAIに図面を描かせるとき、人が決めること"),
         card("1　仕様に不足があったときの動き方\n　　止まって聞くか、仮に決めて書き出すか\n　　黙って決めることは、させない\n\n"
              "2　寸法を、どの面で測るか\n　　数字だけでなく、測る面まで指示に書く", "へんロボの見立て")],
    14: [card("作図の条件と、AIが描く様子 → 読み、描き、見直して保存した\n"
              "7つのAIの結果と、違い → 数字は合い、違いは寸法の取り方に\n"
              "人が決めること → 不足のときの動き方と、測る面", "まとめ"),
         card("次回\nAIに、平面詳細図を描かせる")],
}

# タイトル画面とサムネイル。背景は、Opus が MCP で描いた矩計図を暗くして使う。crop は、図の幅に対する (左, 上, 幅) の割合
THUMB = {
    "tag": "【AIと図面】",
    "title": ("AIがCADで", "矩計図を描いた"),
    "sub": "寸法の取り方が、AIで違った",
    "background": f"{A}/kanabakari-opus-mcp.png",
    "crop": (0.0, 0.2, 1.0),
}
