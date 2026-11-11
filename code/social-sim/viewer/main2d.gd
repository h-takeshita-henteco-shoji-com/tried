extends Node2D
## 公共財ゲームの記録(data/replay.json)を、場面ごとに再生する。
## 絵はすべて _draw() で描く。時間は _process の delta だけで進めるので、
## Movie Maker(決まった fps で書き出す)でも、画面で見ても同じ流れになる。

const W := 1920
const H := 1080
const POT := Vector2(960, 560)
const POT_R := 120.0
const CARD_SIZE := Vector2(600, 430)
const CARD_POS := [Vector2(40, 115), Vector2(1280, 115), Vector2(40, 570), Vector2(1280, 570)]
const ANCHOR := [Vector2(640, 330), Vector2(1280, 330), Vector2(640, 785), Vector2(1280, 785)]
const COLORS := [Color("#d1495b"), Color("#00798c"), Color("#edae49"), Color("#66a182")]
const MOVIE_FPS := 30.0
const INK := Color("#2b2b2b")
const SUB := Color("#6b6b6b")
const PAPER := Color("#fffdf8")

# 場面の名前と長さ(秒)
const STEP_LEN := {
	"title": 4.0, "intro": 1.6, "contrib": 2.2, "contrib_talk": 7.0,
	"distribute": 2.2, "punish": 2.2, "punish_talk": 7.0, "result": 2.4, "end": 5.0,
}

var data: Dictionary
var steps: Array = []      # [{name, round, start, len}]
var t := 0.0
var font: SystemFont
var bold: SystemFont


func _ready() -> void:
	font = SystemFont.new()
	font.font_names = PackedStringArray(["Hiragino Sans", "Hiragino Kaku Gothic ProN"])
	bold = SystemFont.new()
	bold.font_names = font.font_names
	bold.font_weight = 700
	var f := FileAccess.open("res://data/replay.json", FileAccess.READ)
	data = JSON.parse_string(f.get_as_text())
	_build_steps()
	# 確認用: 環境変数 REPLAY_START で、途中の秒から再生を始める
	if OS.has_environment("REPLAY_START"):
		t = float(OS.get_environment("REPLAY_START"))
	start_t = t
	movie = OS.get_cmdline_args().has("--write-movie") or OS.get_cmdline_user_args().has("--write-movie") \
		or OS.has_environment("REPLAY_MOVIE")


func _build_steps() -> void:
	var s := 0.0
	var names := ["intro", "contrib", "contrib_talk", "distribute"]
	if data["game"]["punishment"]:
		names += ["punish", "punish_talk"]
	names.append("result")
	steps.append({"name": "title", "round": -1, "start": s, "len": STEP_LEN["title"]})
	s += STEP_LEN["title"]
	for r in range(data["rounds"].size()):
		for n in names:
			steps.append({"name": n, "round": r, "start": s, "len": STEP_LEN[n]})
			s += STEP_LEN[n]
	steps.append({"name": "end", "round": -1, "start": s, "len": STEP_LEN["end"]})


var start_t := 0.0
var movie := false


func _process(delta: float) -> void:
	# 書き出し(--fixed-fps 30)では delta が毎回 1/30 秒になる
	t += delta
	var last: Dictionary = steps[-1]
	if t > last["start"] + last["len"]:
		get_tree().quit()
	queue_redraw()


func _current() -> Dictionary:
	for st in steps:
		if t < st["start"] + st["len"]:
			return st
	return steps[-1]


func _ease(x: float) -> float:
	x = clampf(x, 0.0, 1.0)
	return x * x * (3.0 - 2.0 * x)


# ---- 描く ----

func _draw() -> void:
	var st := _current()
	var p: float = (t - st["start"]) / st["len"]
	if st["name"] == "title":
		_draw_title(p)
		return
	if st["name"] == "end":
		_draw_end(p)
		return
	var r: int = st["round"]
	var rd: Dictionary = data["rounds"][r]
	_draw_header(r, st["name"])
	_draw_pot(st["name"], p, rd)
	for i in range(4):
		_draw_card(i, st["name"], r, rd)
	match st["name"]:
		"contrib":
			_draw_coins(p, rd)
		"punish", "punish_talk":
			_draw_arrows(p if st["name"] == "punish" else 1.0, rd)
	_draw_footer()


func _text(pos: Vector2, s: String, size: int, color := INK, f: Font = null, width := -1.0,
		align := HORIZONTAL_ALIGNMENT_LEFT) -> void:
	draw_string(f if f else font, pos, s, align, width, size, color)


func _wrap(pos: Vector2, s: String, size: int, width: float, color := INK, max_lines := -1) -> void:
	draw_multiline_string(font, pos, s, HORIZONTAL_ALIGNMENT_LEFT, width, size, max_lines, color)


func _draw_title(p: float) -> void:
	var a := _ease(p * 3.0)
	_text(Vector2(0, 430), data["title"], 84, Color(INK, a), bold, W, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(0, 520), "AIが演じる4人の参加者が、%d回くり返す" % data["rounds"].size(), 40,
		Color(SUB, a), font, W, HORIZONTAL_ALIGNMENT_CENTER)
	var g: Dictionary = data["game"]
	var rule := "毎回%dポイントを受け取り、グループの口座に入れる量を決める。口座の合計×%sが全員に配られる。" % [
		g["endowment"], str(g["mpcr"])]
	_text(Vector2(0, 620), rule, 30, Color(SUB, a), font, W, HORIZONTAL_ALIGNMENT_CENTER)
	if g["punishment"]:
		var pun := "そのあと、ほかの人に減点を付けられる。1点付けると自分が%d減り、相手が%d減る。" % [
			g["punish_cost"], g["punish_impact"]]
		_text(Vector2(0, 670), pun, 30, Color(SUB, a), font, W, HORIZONTAL_ALIGNMENT_CENTER)


func _draw_end(p: float) -> void:
	var a := _ease(p * 3.0)
	_text(Vector2(0, 300), "3回の合計", 56, Color(INK, a), bold, W, HORIZONTAL_ALIGNMENT_CENTER)
	for i in range(4):
		var total := _total(i, data["rounds"].size())
		var y := 400 + i * 90
		draw_circle(Vector2(700, y - 14), 22, Color(COLORS[i], a))
		_text(Vector2(750, y), data["members"][i]["name"], 40, Color(INK, a), bold)
		_text(Vector2(1000, y), "%s ポイント" % _num(total), 40, Color(INK, a))
	_text(Vector2(0, 860), "台詞は、AIが答えた判断の理由をそのまま表示している(長いものは途中で省略)", 26,
		Color(SUB, a), font, W, HORIZONTAL_ALIGNMENT_CENTER)


func _draw_header(r: int, step: String) -> void:
	var label := {
		"intro": "", "contrib": "口座に入れる", "contrib_talk": "なぜその量にしたか",
		"distribute": "口座から全員に配る", "punish": "減点を付ける", "punish_talk": "なぜ減点したか",
		"result": "この回の結果",
	}
	_text(Vector2(40, 70), "第%d回 / 全%d回" % [r + 1, data["rounds"].size()], 44, INK, bold)
	_text(Vector2(420, 70), label[step], 40, SUB)


func _draw_footer() -> void:
	var s := "参加者はすべて架空の人物。演じたAI: %s(claude -p %s)" % [
		str(data["llm"]).trim_prefix("claude:"), str(data["llm_version"]).split(" ")[0]]
	_text(Vector2(40, 1062), s, 22, SUB)


func _draw_pot(step: String, p: float, rd: Dictionary) -> void:
	var total := 0
	for c in rd["contribs"]:
		total += int(c)
	var shown := 0.0
	match step:
		"intro":
			shown = 0.0
		"contrib":
			shown = total * _ease(p)
		"contrib_talk":
			shown = total
		_:
			shown = total * data["game"]["mpcr"] * 4.0
	var fill := Color("#f3e3b5")
	if step == "distribute":
		fill = fill.lerp(Color("#f7d774"), sin(p * PI))
	draw_circle(POT, POT_R, fill)
	draw_arc(POT, POT_R, 0, TAU, 64, Color("#b58b2a"), 4.0)
	_text(POT + Vector2(-POT_R, -30), "グループの口座", 26, SUB, font, POT_R * 2, HORIZONTAL_ALIGNMENT_CENTER)
	_text(POT + Vector2(-POT_R, 30), _num(snappedf(shown, 0.1)), 56, INK, bold, POT_R * 2,
		HORIZONTAL_ALIGNMENT_CENTER)
	if step in ["distribute", "punish", "punish_talk", "result"]:
		var each: float = total * data["game"]["mpcr"]
		_text(POT + Vector2(-200, POT_R + 50), "%d × %s = 1人あたり %s" % [total, str(data["game"]["mpcr"]), _num(each)],
			28, SUB, font, 400, HORIZONTAL_ALIGNMENT_CENTER)


func _draw_card(i: int, step: String, r: int, rd: Dictionary) -> void:
	var pos: Vector2 = CARD_POS[i]
	var col: Color = COLORS[i]
	var m: Dictionary = data["members"][i]
	draw_rect(Rect2(pos, CARD_SIZE), PAPER)
	draw_rect(Rect2(pos, Vector2(12, CARD_SIZE.y)), col)
	draw_rect(Rect2(pos, CARD_SIZE), Color(col, 0.6), false, 2.0)
	_text(pos + Vector2(32, 48), m["name"], 34, INK, bold)
	_wrap(pos + Vector2(32, 82), m["persona"], 19, 360, SUB, 3)
	# 右上: これまでの合計と、この回の手元
	var before := _total(i, r)
	var now_txt := ""
	match step:
		"contrib", "contrib_talk":
			now_txt = "手元 %s" % _num(data["game"]["endowment"] - int(rd["contribs"][i]))
		"distribute", "punish", "punish_talk":
			now_txt = "手元 %s" % _num(rd["base"][i])
		"result":
			now_txt = "手元 %s" % _num(rd["final"][i])
	_text(pos + Vector2(420, 48), "合計 %s" % _num(before + (rd["final"][i] if step == "result" else 0.0)),
		26, SUB, font, 160, HORIZONTAL_ALIGNMENT_RIGHT)
	if now_txt != "":
		_text(pos + Vector2(380, 92), now_txt, 30, INK, bold, 200, HORIZONTAL_ALIGNMENT_RIGHT)
	# 入れた量
	if step != "intro":
		_text(pos + Vector2(32, 186), "口座に入れた: %d" % int(rd["contribs"][i]), 30, col.darkened(0.2), bold)
	if step in ["punish", "punish_talk", "result"] and data["game"]["punishment"]:
		var recv := 0
		var gave := 0
		for k in range(4):
			if k != i:
				recv += int(rd["points"][k][i])
				gave += int(rd["points"][i][k])
		_text(pos + Vector2(330, 186), "付けた %d / 受けた %d" % [gave, recv], 24, SUB)
	# 吹き出し(判断の理由)
	var reason := ""
	if step == "contrib_talk":
		reason = rd["contribute_reasons"][i]
	elif step == "punish_talk":
		reason = rd["punish_reasons"][i]
	if reason != "":
		var box := Rect2(pos + Vector2(28, 206), Vector2(CARD_SIZE.x - 56, CARD_SIZE.y - 222))
		draw_rect(box, Color(col, 0.10))
		draw_rect(box, Color(col, 0.5), false, 1.5)
		_wrap(box.position + Vector2(18, 36), "「" + reason + "」", 22, box.size.x - 36, INK, 7)


func _draw_coins(p: float, rd: Dictionary) -> void:
	for i in range(4):
		var n := int(round(int(rd["contribs"][i]) / 2.0))
		for k in range(n):
			var delay := k * 0.06
			var q := _ease((p - delay) / 0.6)
			if q <= 0.0 or q >= 1.0:
				continue
			var a: Vector2 = ANCHOR[i]
			var pos := a.lerp(POT, q) + Vector2(0, -sin(q * PI) * 60)
			draw_circle(pos, 12, Color("#e0b23a"))
			draw_arc(pos, 12, 0, TAU, 24, Color("#a07a1c"), 2.0)


func _bezier(a: Vector2, c: Vector2, b: Vector2, u: float) -> Vector2:
	return a.lerp(c, u).lerp(c.lerp(b, u), u)


func _draw_arrows(p: float, rd: Dictionary) -> void:
	var q := _ease(p)
	for i in range(4):
		for j in range(4):
			var pts := int(rd["points"][i][j])
			if i == j or pts == 0:
				continue
			var a: Vector2 = ANCHOR[i]
			var b: Vector2 = ANCHOR[j]
			var dir := (b - a).normalized()
			var perp := Vector2(-dir.y, dir.x)
			var mid := (a + b) / 2.0
			# 口座から離れる側へふくらませる。行きと帰りは別の側に出るので重ならない
			var bulge := 150.0 if (mid - POT).length() < 60.0 else 90.0
			var c := mid + perp * bulge
			if (c - POT).length() < (mid - perp * bulge - POT).length() and (mid - POT).length() >= 60.0:
				c = mid - perp * bulge
			var line := PackedVector2Array()
			var n := 32
			for k in range(int(n * q) + 1):
				line.append(_bezier(a, c, b, float(k) / n))
			if line.size() >= 2:
				draw_polyline(line, COLORS[i], 5.0, true)
			if q > 0.95:
				var tip := b
				var back := (_bezier(a, c, b, 0.92) - tip).normalized()
				var side := Vector2(-back.y, back.x)
				draw_colored_polygon(PackedVector2Array([tip, tip + back * 28 + side * 13,
					tip + back * 28 - side * 13]), COLORS[i])
				var lab := _bezier(a, c, b, 0.5)
				draw_circle(lab, 26, PAPER)
				draw_arc(lab, 26, 0, TAU, 32, COLORS[i], 2.0)
				_text(lab + Vector2(-40, 10), "-%d" % pts, 28, COLORS[i].darkened(0.2), bold, 80,
					HORIZONTAL_ALIGNMENT_CENTER)


func _total(i: int, upto: int) -> float:
	var s := 0.0
	for r in range(upto):
		s += float(data["rounds"][r]["final"][i])
	return s


func _num(x) -> String:
	var v := float(x)
	if is_equal_approx(v, round(v)):
		return str(int(round(v)))
	return "%.1f" % v
