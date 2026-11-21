extends Control
## #181 土地をまとめる交渉の再生。data.json(export_data.py で作る)の組を、ターンごとに動かして見せる。
## 録画: godot --path . --write-movie out.avi --fixed-fps 30

const W := 1280.0
const H := 720.0
const C_BG := Color("f6f4ee")
const C_INK := Color("1d1d1f")
const C_MUTED := Color("6b6b70")
const C_CARD := Color("ffffff")
const C_LINE := Color("d9d6cc")
const C_BUYER := Color("2f6db5")
const C_SELLER := Color("b8732a")
const C_LAND := Color("8fbf6a")
const C_OK := Color("1f7a4d")
const C_NG := Color("b3261e")
const C_RULE := Color("7a4fb3")

const BUYER_POS := Vector2(170, 300)
const LAND_X := 690.0
const ROW_Y := [170.0, 430.0]
const TABLE_X := 900.0   # 右側の、提示した値段の表
const SELLERS := ["売り手1", "売り手2"]

var font: Font
var bold: Font
var data: Dictionary
var stage: Control      # 1つの場面の部品
var period_layer: Control   # 1つのターンだけの部品
var fader: ColorRect
var show_cards := true


func _ready() -> void:
	font = _load_font()
	var fv := FontVariation.new()
	fv.base_font = font
	fv.variation_embolden = 0.9
	bold = fv
	var bg := ColorRect.new()
	bg.color = C_BG
	bg.size = Vector2(W, H)
	add_child(bg)
	stage = Control.new()
	add_child(stage)
	fader = ColorRect.new()
	fader.color = Color(C_BG, 1.0)
	fader.size = Vector2(W, H)
	add_child(fader)
	# 録画の中身は、コマンドの -- の後で選ぶ: --data=data_hook.json(読むデータ) --no-cards(タイトルとまとめの画面を出さない)
	var data_file := "res://data.json"
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--data="):
			data_file = "res://" + a.trim_prefix("--data=")
		elif a == "--no-cards":
			show_cards = false
	data = JSON.parse_string(FileAccess.get_file_as_string(data_file))
	_run()


func _load_font() -> Font:
	var paths := [OS.get_environment("HOME") + "/Library/Fonts/NotoSansJP-Variable.ttf",
		"/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"]
	for p in paths:
		if FileAccess.file_exists(p):
			var f := FontFile.new()
			f.load_dynamic_font(p)
			return f
	return ThemeDB.fallback_font


# --- 部品 ---
func wait(s: float) -> void:
	await get_tree().create_timer(s).timeout


func fade(to: float, s := 0.5) -> void:
	var tw := create_tween()
	tw.tween_property(fader, "color:a", to, s)
	await tw.finished


func lbl(parent: Node, text: String, pos: Vector2, size: Vector2, fsize: int, color := C_INK,
		align := HORIZONTAL_ALIGNMENT_LEFT, is_bold := false) -> Label:
	var l := Label.new()
	l.text = text
	l.position = pos
	l.size = size
	l.clip_text = true
	l.add_theme_font_override("font", bold if is_bold else font)
	l.add_theme_font_size_override("font_size", fsize)
	l.add_theme_color_override("font_color", color)
	l.horizontal_alignment = align
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	parent.add_child(l)
	return l


func box(parent: Node, pos: Vector2, size: Vector2, color: Color, radius := 12,
		border := Color(0, 0, 0, 0), bw := 0) -> Panel:
	var p := Panel.new()
	var sb := StyleBoxFlat.new()
	sb.bg_color = color
	sb.set_corner_radius_all(radius)
	if bw > 0:
		sb.border_color = border
		sb.set_border_width_all(bw)
	p.add_theme_stylebox_override("panel", sb)
	p.position = pos
	p.size = size
	parent.add_child(p)
	return p


func tag(parent: Node, text: String, center: Vector2, color: Color, fsize := 22, w := 120.0, h := 44.0) -> Panel:
	var p := box(parent, center - Vector2(w, h) / 2, Vector2(w, h), color, int(h / 2))
	lbl(p, text, Vector2.ZERO, Vector2(w, h), fsize, Color.WHITE, HORIZONTAL_ALIGNMENT_CENTER, true)
	p.pivot_offset = Vector2(w, h) / 2
	return p


func pop(node: Control) -> void:
	node.pivot_offset = node.size / 2
	node.scale = Vector2(0.2, 0.2)
	var tw := create_tween()
	tw.tween_property(node, "scale", Vector2.ONE, 0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)


func person(parent: Node, center: Vector2, r: float, color: Color, mark: String) -> void:
	box(parent, center - Vector2(r, r), Vector2(r, r) * 2, color, int(r))
	lbl(parent, mark, center - Vector2(r, r), Vector2(r, r) * 2, int(r * 0.8), Color.WHITE, HORIZONTAL_ALIGNMENT_CENTER, true)


func clear(node: Node) -> void:
	for c in node.get_children():
		c.queue_free()


# --- 流れ ---
func _run() -> void:
	if show_cards:
		await title_card()
	for sc in data["scenes"]:
		await play_scene(sc)
	if show_cards:
		await closing_card()
	get_tree().quit()


func title_card() -> void:
	clear(stage)
	lbl(stage, "土地をまとめる交渉を AI で再現する", Vector2(0, 170), Vector2(W, 70), 44, C_INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	var lines := [
		"買い手は、2人の持ち主の土地を両方まとめると 90 ドルの価値を得ます。",
		"持ち主(売り手)は、土地を手放すと 30 ドルの費用がかかります。",
		"10 ターンの交渉のうちに両方まとまらなければ、3 人とも 0 ドルです。",
	]
	for i in lines.size():
		lbl(stage, lines[i], Vector2(0, 290 + i * 46), Vector2(W, 40), 24, C_INK, HORIZONTAL_ALIGNMENT_CENTER)
	lbl(stage, "3 人とも AI(Claude Haiku 5.5)。断るかどうかと、出す側の譲り幅は、プログラムで補った版", Vector2(0, 480), Vector2(W, 36), 20, C_MUTED, HORIZONTAL_ALIGNMENT_CENTER)
	lbl(stage, "人間のデータ: Cadigan ほか (2009) の実験", Vector2(0, 520), Vector2(W, 36), 20, C_MUTED, HORIZONTAL_ALIGNMENT_CENTER)
	await fade(0.0, 0.6)
	await wait(5.0)
	await fade(1.0, 0.5)


func closing_card() -> void:
	clear(stage)
	lbl(stage, "分かったこと", Vector2(0, 150), Vector2(W, 60), 40, C_INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	var lines := [
		"AI だけでは、値上がりを予想できても「確実だから」と受けてしまい、粘らなかった",
		"断るかをプログラムが決めると、断る回数が人間に近づいた",
		"値段を出す AI は大きく譲るので、譲る幅をプログラムで抑えると稼ぎの偏りが消えた",
		"遅れの損があるときの粘りすぎは、まだ人間と違う",
	]
	for i in lines.size():
		lbl(stage, "・" + lines[i], Vector2(150, 250 + i * 60), Vector2(W - 300, 50), 24, C_INK)
	await fade(0.0, 0.6)
	await wait(6.5)
	await fade(1.0, 0.6)


func land_point(i: int) -> Vector2:
	return Vector2(LAND_X, ROW_Y[i])


func on_line(i: int, t: float) -> Vector2:
	var start := BUYER_POS + Vector2(80, -80 if i == 0 else 80)   # 2本の線を買い手の近くで離す
	return start.lerp(land_point(i) - Vector2(60, 0), t)


func play_scene(sc: Dictionary) -> void:
	clear(stage)
	var buyer_proposes: bool = sc["proposer"] == "buyer"
	# 見出し
	lbl(stage, sc["title"], Vector2(40, 18), Vector2(800, 44), 28, C_INK, HORIZONTAL_ALIGNMENT_LEFT, true)
	var period_lbl := lbl(stage, "", Vector2(W - 340, 18), Vector2(300, 44), 28, C_INK, HORIZONTAL_ALIGNMENT_RIGHT, true)
	var rej_lbl := lbl(stage, "断った回数 合計 0 回", Vector2(W - 340, 60), Vector2(300, 30), 18, C_MUTED, HORIZONTAL_ALIGNMENT_RIGHT)
	var meter_fill: Panel = null
	var meter_lbl: Label = null
	if sc["delay"]:
		lbl(stage, "全員の稼ぎ", Vector2(40, 64), Vector2(110, 26), 18, C_MUTED)
		box(stage, Vector2(150, 70), Vector2(300, 16), C_LINE, 8)
		meter_fill = box(stage, Vector2(150, 70), Vector2(300, 16), C_NG, 8)
		meter_lbl = lbl(stage, "本来の 100%", Vector2(462, 64), Vector2(200, 26), 18, C_MUTED)
	else:
		lbl(stage, "遅れの損なし(何回断っても稼ぎは減らない)", Vector2(40, 64), Vector2(600, 26), 18, C_MUTED)
	# 結ぶ線
	for i in 2:
		var ln := Line2D.new()
		ln.points = [on_line(i, 0.0), on_line(i, 1.0)]
		ln.width = 3
		ln.default_color = C_LINE
		stage.add_child(ln)
	# 買い手
	person(stage, BUYER_POS, 62, C_BUYER, "買")
	lbl(stage, "買い手", BUYER_POS + Vector2(-100, 70), Vector2(200, 30), 22, C_INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	lbl(stage, "土地をまとめたい", BUYER_POS + Vector2(-100, 100), Vector2(200, 26), 17, C_MUTED, HORIZONTAL_ALIGNMENT_CENTER)
	# 売り手と土地
	var lands := []
	var land_lbls := []
	for i in 2:
		var lp := land_point(i)
		var land := box(stage, lp - Vector2(45, 45), Vector2(90, 90), C_LAND, 8)
		lands.append(land)
		land_lbls.append(lbl(land, "土地%d" % (i + 1), Vector2.ZERO, Vector2(90, 90), 20, Color.WHITE, HORIZONTAL_ALIGNMENT_CENTER, true))
		person(stage, lp + Vector2(115, 0), 36, C_SELLER, "売")
		lbl(stage, SELLERS[i], lp + Vector2(65, 40), Vector2(100, 28), 18, C_INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	lbl(stage, ("買い手が値段を出し、売り手が売るか断るかを決める" if buyer_proposes else "売り手が値段を出し、買い手が買うか断るかを決める"),
		Vector2(40, 96), Vector2(800, 26), 18, C_MUTED, HORIZONTAL_ALIGNMENT_LEFT)
	# 理由の欄
	box(stage, Vector2(30, 540), Vector2(W - 60, 160), C_CARD, 12, C_LINE, 1)
	lbl(stage, "AI が書いた理由(最初の1文)", Vector2(50, 546), Vector2(400, 26), 16, C_MUTED)
	var reason_lbls := {}
	var who_list := ["buyer", "売り手1", "売り手2"]
	for j in 3:
		var who_name: String = "買い手" if who_list[j] == "buyer" else who_list[j]
		lbl(stage, who_name, Vector2(50, 576 + j * 38), Vector2(90, 34), 18, C_BUYER if j == 0 else C_SELLER, HORIZONTAL_ALIGNMENT_LEFT, true)
		reason_lbls[who_list[j]] = lbl(stage, "", Vector2(140, 576 + j * 38), Vector2(W - 200, 34), 18, C_INK)
	# 提示した値段の表(ターンごと。○はまとまった、×は断られた)
	box(stage, Vector2(TABLE_X, 110), Vector2(W - TABLE_X - 30, 420), C_CARD, 12, C_LINE, 1)
	lbl(stage, "提示した値段", Vector2(TABLE_X + 16, 116), Vector2(200, 28), 18, C_INK, HORIZONTAL_ALIGNMENT_LEFT, true)
	lbl(stage, "○ まとまった  × 断られた", Vector2(TABLE_X + 150, 116), Vector2(190, 28), 14, C_MUTED, HORIZONTAL_ALIGNMENT_RIGHT)
	var cols := [TABLE_X + 16, TABLE_X + 110, TABLE_X + 230]
	var heads := ["ターン", "売り手1", "売り手2"]
	for c in 3:
		lbl(stage, heads[c], Vector2(cols[c], 148), Vector2(110, 26), 16, C_MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
	var row_hl := box(stage, Vector2(TABLE_X + 8, 0), Vector2(W - TABLE_X - 46, 34), Color(C_BUYER, 0.12), 6)
	row_hl.visible = false
	var cells := []
	for k in int(sc["periods"]):
		var y: float = 178.0 + k * 34.0
		var row := []
		row.append(lbl(stage, "", Vector2(cols[0], y), Vector2(80, 34), 17, C_MUTED))
		row.append(lbl(stage, "", Vector2(cols[1], y), Vector2(110, 34), 18, C_INK, HORIZONTAL_ALIGNMENT_LEFT, true))
		row.append(lbl(stage, "", Vector2(cols[2], y), Vector2(110, 34), 18, C_INK, HORIZONTAL_ALIGNMENT_LEFT, true))
		cells.append(row)
	period_layer = Control.new()
	stage.add_child(period_layer)
	await fade(0.0, 0.5)

	for r in sc["rounds"]:
		clear(period_layer)
		period_lbl.text = "%d ターン目 / %d ターン" % [r["period"], sc["periods"]]
		for who in who_list:
			reason_lbls[who].text = r["reasons"].get(who, "(売り買いは決まっている)")
		# 1. 値段が動く
		var tags := {}
		for i in 2:
			var s: String = SELLERS[i]
			if not r["offers"].has(s):
				continue
			var from_t := 0.0 if buyer_proposes else 1.0
			var to_t := 0.42 if buyer_proposes else 0.62
			var tg := tag(period_layer, "%d ドル" % int(r["offers"][s]), on_line(i, from_t), C_BUYER if buyer_proposes else C_SELLER)
			tags[s] = tg
			var tw := create_tween()
			tw.tween_property(tg, "position", on_line(i, to_t) - tg.size / 2, 0.7).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
		await wait(0.9)
		# 2. 出す側のプログラム(譲る幅を抑えた)
		for i in 2:
			var s: String = SELLERS[i]
			if r["damp"].has(s):
				var d: Dictionary = r["damp"][s]
				var bd := lbl(period_layer, "AI の案 %d ドル → プログラムで %d ドル" % [int(d["ai"]), int(d["sent"])],
					on_line(i, 0.42 if buyer_proposes else 0.62) + Vector2(-150, -56), Vector2(300, 28), 17, C_RULE, HORIZONTAL_ALIGNMENT_CENTER, true)
				pop(bd)
		if not r["damp"].is_empty():
			await wait(0.8)
		# 3. 受ける側が決める
		for i in 2:
			var s: String = SELLERS[i]
			if not r["offers"].has(s):
				continue
			var ok: bool = r["accepted"][s]
			var ai_ok: bool = r["ai_accepted"].get(s, ok)
			var yes := "売る" if buyer_proposes else "買う"
			var at := on_line(i, 0.86 if buyer_proposes else 0.16)
			var note_x := -150.0 if buyer_proposes else -75.0   # 下の注記を、土地や買い手の絵にかからない側へずらす
			var st := tag(period_layer, yes if ok else "断る", at, C_OK if ok else C_NG, 22, 96, 44)
			pop(st)
			if ai_ok != ok:
				var ch := lbl(period_layer, "プログラムが変更(AI は「%s」)" % (yes if ai_ok else "断る"), at + Vector2(note_x, 26), Vector2(210, 26), 15, C_RULE, HORIZONTAL_ALIGNMENT_CENTER, true)
				pop(ch)
			if r["beliefs"].has(s):
				var dy := 54 if ai_ok != ok else 28
				lbl(period_layer, "断れば次は %d ドルと予想" % int(r["beliefs"][s]), at + Vector2(note_x, dy), Vector2(210, 24), 15, C_MUTED, HORIZONTAL_ALIGNMENT_CENTER)
		rej_lbl.text = "断った回数 合計 %d 回" % int(r["rejections_total"])
		var ri: int = int(r["period"]) - 1
		row_hl.position.y = 178.0 + ri * 34.0
		row_hl.visible = true
		cells[ri][0].text = "%dターン目" % int(r["period"])
		for i in 2:
			var s: String = SELLERS[i]
			var cell: Label = cells[ri][i + 1]
			if r["offers"].has(s):
				var ok2: bool = r["accepted"][s]
				cell.text = "%d ドル %s" % [int(r["offers"][s]), "○" if ok2 else "×"]
				cell.add_theme_color_override("font_color", C_OK if ok2 else C_NG)
			else:
				cell.text = "—"
				cell.add_theme_color_override("font_color", C_MUTED)
		if meter_fill:
			var m := maxf(0.0, 1.0 - 0.05 * r["rejections_total"])
			var tw := create_tween()
			tw.tween_property(meter_fill, "size:x", 300.0 * m, 0.4)
			meter_lbl.text = "本来の %d%%" % int(round(m * 100))
		await wait(1.0)
		# 4. 決まった土地は買い手の色に
		for i in 2:
			var s: String = SELLERS[i]
			if r["offers"].has(s) and r["accepted"][s]:
				var sb: StyleBoxFlat = lands[i].get_theme_stylebox("panel").duplicate()
				sb.bg_color = C_BUYER
				lands[i].add_theme_stylebox_override("panel", sb)
				land_lbls[i].text = "%d ドルで\nまとまった" % int(r["offers"][s])
				land_lbls[i].add_theme_font_size_override("font_size", 16)
				pop(lands[i])
		await wait(1.2)

	# 結末
	clear(period_layer)
	var card := box(stage, Vector2(40, 130), Vector2(830, 330), C_CARD, 16, C_LINE, 2)
	lbl(card, "結末", Vector2(0, 14), Vector2(830, 44), 30, C_INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	var p: Array = sc["payoffs"]
	var hm: Dictionary = sc["human"]
	var rows := [
		["", "この組(AI)", "人間の平均"],
		["買い手の稼ぎ", "%.1f ドル" % p[0], "%.2f ドル" % hm["buyer"]],
		["売り手の稼ぎ", "%.1f ・ %.1f ドル" % [p[1], p[2]], "1人 %.2f ドル" % hm["seller"]],
		["断った回数", "%d 回" % int(sc["rejections"]), "%.1f 回" % hm["rejections"]],
	]
	for k in rows.size():
		var c := C_MUTED if k == 0 else C_INK
		lbl(card, rows[k][0], Vector2(60, 80 + k * 56), Vector2(220, 44), 22, c, HORIZONTAL_ALIGNMENT_LEFT, k > 0)
		lbl(card, rows[k][1], Vector2(290, 80 + k * 56), Vector2(240, 44), 22, c, HORIZONTAL_ALIGNMENT_CENTER)
		lbl(card, rows[k][2], Vector2(530, 80 + k * 56), Vector2(240, 44), 22, c, HORIZONTAL_ALIGNMENT_CENTER)
	pop(card)
	await wait(5.0)
	await fade(1.0, 0.5)
