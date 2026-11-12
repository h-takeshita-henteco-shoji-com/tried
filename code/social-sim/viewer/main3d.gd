extends Node3D
## 公共財ゲームの記録(data/replay.json)を、3D の棒人間で再生する。
## 舞台(テーブル・口座・棒人間・金貨・減点の玉)は 3D、判断の理由は四隅のカード(2D)に出す。
## 書き出し(Movie Maker)では、描いたコマの数で時間を進める。

const MOVIE_FPS := 30.0
const COLORS := [Color("#d1495b"), Color("#00798c"), Color("#edae49"), Color("#66a182")]
const INK := Color("#2b2b2b")
const SUB := Color("#6b6b6b")
const PAPER := Color("#fffdf8")
const GOLD := Color("#e0b23a")

# 棒人間の立ち位置。カメラから見て 左奥・右奥・左手前・右手前 に置き、四隅のカードと合わせる
const SEATS := [Vector3(-0.85, 0, -0.95), Vector3(0.85, 0, -0.95), Vector3(-1.25, 0, 0.55), Vector3(1.25, 0, 0.55)]
const CARD_SIZE := Vector2(470, 400)
const CARD_POS := [Vector2(28, 110), Vector2(1422, 110), Vector2(28, 590), Vector2(1422, 590)]
const POT_POS := Vector3(0, 0.6, 0)

const STEP_LEN := {
	"title": 5.0, "intro": 1.6, "contrib": 2.6, "contrib_talk": 7.0,
	"distribute": 2.6, "punish": 2.4, "punish_talk": 7.0, "result": 2.4, "end": 6.0,
}

var data: Dictionary
var steps: Array = []
var t := 0.0
var start_t := 0.0
var movie := false
var font: SystemFont
var bold: SystemFont

var cam: Camera3D
var hud: Control
var people: Array = []        # [{root, head, head_mat, rarm, larm, label}]
var coins: Array = []         # 飛ぶ金貨
var balls: Array = []         # 減点の玉
var pot_stack: MeshInstance3D
var pot_label: Label3D
var hit_labels: Array = []


func _ready() -> void:
	font = SystemFont.new()
	font.font_names = PackedStringArray(["Hiragino Sans", "Hiragino Kaku Gothic ProN"])
	bold = SystemFont.new()
	bold.font_names = font.font_names
	bold.font_weight = 700
	var f := FileAccess.open("res://data/replay.json", FileAccess.READ)
	data = JSON.parse_string(f.get_as_text())
	_build_steps()
	_build_world()
	_build_hud()
	if OS.has_environment("REPLAY_START"):
		t = float(OS.get_environment("REPLAY_START"))
	start_t = t
	movie = OS.has_environment("REPLAY_MOVIE")


# ---- 場面の並び ----

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


func _current() -> Dictionary:
	for st in steps:
		if t < st["start"] + st["len"]:
			return st
	return steps[-1]


func _ease(x: float) -> float:
	x = clampf(x, 0.0, 1.0)
	return x * x * (3.0 - 2.0 * x)


# ---- 3D の舞台を組む ----

func _mat(c: Color, rough := 0.8) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = c
	m.roughness = rough
	return m


func _mesh(mesh: Mesh, mat: Material, pos := Vector3.ZERO, parent: Node = self) -> MeshInstance3D:
	var mi := MeshInstance3D.new()
	mi.mesh = mesh
	mi.material_override = mat
	mi.position = pos
	parent.add_child(mi)
	return mi


func _build_world() -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.62, 0.84, 0.82)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(1, 1, 1)
	env.ambient_light_energy = 0.55
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)

	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-55, -30, 0)
	sun.light_energy = 1.1
	sun.shadow_enabled = true
	add_child(sun)

	cam = Camera3D.new()
	cam.fov = 45
	add_child(cam)
	_place_camera(0.0)

	var floor_mesh := PlaneMesh.new()
	floor_mesh.size = Vector2(400, 400)
	_mesh(floor_mesh, _mat(Color(0.66, 0.87, 0.85)))

	# テーブル
	var top := CylinderMesh.new()
	top.top_radius = 1.05
	top.bottom_radius = 1.05
	top.height = 0.06
	_mesh(top, _mat(Color("#a9825a"), 0.6), Vector3(0, 0.52, 0))
	var leg := CylinderMesh.new()
	leg.top_radius = 0.08
	leg.bottom_radius = 0.18
	leg.height = 0.5
	_mesh(leg, _mat(Color("#7d5c3c")), Vector3(0, 0.25, 0))

	# グループの口座(器と金貨の山)
	var bowl := CylinderMesh.new()
	bowl.top_radius = 0.34
	bowl.bottom_radius = 0.26
	bowl.height = 0.08
	_mesh(bowl, _mat(Color("#b58b2a"), 0.4), POT_POS + Vector3(0, -0.02, 0))
	var stack := CylinderMesh.new()
	stack.top_radius = 0.24
	stack.bottom_radius = 0.24
	stack.height = 1.0
	pot_stack = _mesh(stack, _mat(GOLD, 0.3), POT_POS)
	pot_stack.scale = Vector3(1, 0.001, 1)
	pot_label = _label3d("", 64, POT_POS + Vector3(0, 0.75, 0))

	# 棒人間
	for i in range(4):
		people.append(_cute_figure(i))

	# 飛ぶ金貨と減点の玉は、先に作って隠しておく
	var coin_mesh := CylinderMesh.new()
	coin_mesh.top_radius = 0.06
	coin_mesh.bottom_radius = 0.06
	coin_mesh.height = 0.02
	for k in range(60):
		var c := _mesh(coin_mesh, _mat(GOLD, 0.3))
		c.visible = false
		coins.append(c)
	var ball_mesh := SphereMesh.new()
	ball_mesh.radius = 0.07
	ball_mesh.height = 0.14
	var red := _mat(Color("#e63946"), 0.4)
	red.emission_enabled = true
	red.emission = Color("#e63946")
	red.emission_energy_multiplier = 0.6
	for k in range(16):
		var b := _mesh(ball_mesh, red)
		b.visible = false
		balls.append(b)
	for i in range(4):
		var lab := _label3d("", 72, Vector3.ZERO)
		lab.modulate = Color("#c1121f")
		hit_labels.append(lab)


func _label3d(text: String, size: int, pos: Vector3) -> Label3D:
	var l := Label3D.new()
	l.text = text
	l.font = bold
	l.font_size = size
	l.pixel_size = 0.004
	l.outline_size = 12
	l.outline_modulate = PAPER
	l.modulate = INK
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	l.no_depth_test = true
	l.position = pos
	add_child(l)
	return l


func _limb(parent: Node3D, from: Vector3, to: Vector3, mat: Material, r := 0.035) -> MeshInstance3D:
	var m := CylinderMesh.new()
	m.top_radius = r
	m.bottom_radius = r
	m.height = from.distance_to(to)
	var mi := _mesh(m, mat, (from + to) / 2.0, parent)
	var dir := (to - from).normalized()
	if absf(dir.dot(Vector3.UP)) < 0.999:
		var axis := Vector3.UP.cross(dir).normalized()
		mi.basis = Basis(axis, Vector3.UP.angle_to(dir))
	return mi


func _ball(parent: Node3D, r: float, mat: Material, pos: Vector3, sc := Vector3.ONE) -> MeshInstance3D:
	var m := SphereMesh.new()
	m.radius = r
	m.height = r * 2.0
	var mi := _mesh(m, mat, pos, parent)
	mi.scale = sc
	return mi


func _capsule(parent: Node3D, r: float, h: float, mat: Material, pos: Vector3) -> MeshInstance3D:
	var m := CapsuleMesh.new()
	m.radius = r
	m.height = h
	return _mesh(m, mat, pos, parent)


func _cute_figure(i: int) -> Dictionary:
	## つるんとした丸い体に、大きな目玉が2つと、先の丸い触角。手は小さい
	var root := Node3D.new()
	add_child(root)
	root.position = SEATS[i]
	# -Z がテーブルの中央を向く。手前の2人は少しカメラ側へ向け、顔が見えるようにする
	root.look_at(Vector3(0, 0, 0.0 if i < 2 else 1.3), Vector3.UP)
	var col: Color = COLORS[i].lightened(0.12)
	var skin := _mat(col, 0.35)
	skin.emission_enabled = true                # 減点を受けたとき赤く光らせる
	skin.emission = Color("#ff3030")
	skin.emission_energy_multiplier = 0.0
	var tip := _mat(col.darkened(0.25), 0.4)
	var white := _mat(Color("#fbfbf6"), 0.15)
	var black := _mat(Color("#1f1a17"), 0.2)
	var shine := _mat(Color.WHITE, 0.1)

	var body := Node3D.new()      # 揺れや跳ねは body を動かす
	root.add_child(body)
	_ball(body, 0.33, skin, Vector3(0, 0.27, 0), Vector3(1, 0.82, 0.95))       # 下のふくらみ
	_capsule(body, 0.27, 1.0, skin, Vector3(0, 0.6, 0))                          # 体
	var head := Node3D.new()      # 目と触角。首をかしげる
	head.position = Vector3(0, 0.9, 0)
	body.add_child(head)
	var eyes := []
	for sx in [-1.0, 1.0]:
		var eye := _ball(head, 0.105, white, Vector3(sx * 0.1, 0.03, -0.2))
		var pupil := _ball(eye, 0.05, black, Vector3(-sx * 0.012, -0.005, -0.075), Vector3(1, 1, 0.6))
		_ball(pupil, 0.016, shine, Vector3(0.012, 0.018, -0.03))
		eyes.append(eye)
		_limb(head, Vector3(sx * 0.06, 0.2, -0.02), Vector3(sx * 0.12, 0.42, 0.0), tip, 0.016)  # 触角
		_ball(head, 0.035, tip, Vector3(sx * 0.12, 0.43, 0.0))
	var mouth := _ball(head, 0.03, _mat(Color("#5b2a2a"), 0.6), Vector3(0, -0.13, -0.255),
		Vector3(1.4, 0.35, 0.5))
	var arms := []
	for sx in [-1.0, 1.0]:
		var pivot := Node3D.new()
		pivot.position = Vector3(sx * 0.27, 0.5, 0)
		body.add_child(pivot)
		var hang := Node3D.new()
		hang.rotation = Vector3(0, 0, sx * 0.25)
		pivot.add_child(hang)
		_capsule(hang, 0.045, 0.2, skin, Vector3(0, -0.08, 0))
		arms.append(pivot)
	return {"root": root, "body": body, "head": head, "head_mat": skin, "eyes": eyes, "mouth": mouth,
		"larm": arms[0], "rarm": arms[1]}


func _place_camera(swing: float) -> void:
	var ang := deg_to_rad(swing)
	var dist := 5.0
	cam.position = Vector3(sin(ang) * dist, 2.7, cos(ang) * dist)
	cam.look_at(Vector3(0, 0.55, -0.1), Vector3.UP)


# ---- 毎コマの動き ----

func _process(delta: float) -> void:
	# 書き出し(--fixed-fps 30)では delta が毎回 1/30 秒になる
	t += delta
	var last: Dictionary = steps[-1]
	if t > last["start"] + last["len"]:
		get_tree().quit()
	_animate()
	hud.queue_redraw()


func _animate() -> void:
	var st := _current()
	var p: float = (t - st["start"]) / st["len"]
	var name: String = st["name"]
	# カメラはゆっくり左右に振る(四隅のカードとの対応が崩れない範囲)
	var swing := sin(t * 0.25) * 8.0
	if name == "title" or name == "end":
		swing = sin(t * 0.5) * 25.0
	_place_camera(swing)
	for c in coins:
		c.visible = false
	for b in balls:
		b.visible = false
	for l in hit_labels:
		l.visible = false
	for i in range(4):
		_pose_idle(i)
	if st["round"] < 0:
		pot_stack.scale = Vector3(1, 0.001, 1)
		pot_label.text = ""
		return
	var rd: Dictionary = data["rounds"][st["round"]]
	var total := 0
	for c in rd["contribs"]:
		total += int(c)
	var pot_after: float = total * data["game"]["mpcr"] * 4.0
	var pot_now := 0.0
	match name:
		"intro":
			pot_now = 0.0
		"contrib":
			pot_now = total * _ease((p - 0.2) / 0.8)
			_anim_contrib(p, rd)
		"contrib_talk":
			pot_now = total
		"distribute":
			pot_now = lerpf(total, pot_after, _ease(p / 0.3)) * (1.0 - _ease((p - 0.35) / 0.65))
			_anim_distribute(p, rd)
		"punish":
			_anim_punish(p, rd)
		"punish_talk":
			_anim_punish(1.0, rd)
		"result":
			_anim_result(p, rd)
	pot_stack.scale = Vector3(1, maxf(pot_now * 0.006, 0.001), 1)
	pot_stack.position = POT_POS + Vector3(0, pot_now * 0.003, 0)
	pot_label.text = _num(snappedf(pot_now, 0.1)) if pot_now > 0.05 else ""
	pot_label.position = POT_POS + Vector3(0, 0.35 + pot_now * 0.006, 0)


func _pose_idle(i: int) -> void:
	var pp: Dictionary = people[i]
	var body: Node3D = pp["body"]
	body.position = Vector3(0, sin(t * 2.0 + i) * 0.01, 0)
	body.rotation = Vector3.ZERO
	pp["rarm"].basis = Basis()
	pp["larm"].basis = Basis()
	pp["head_mat"].emission_energy_multiplier = 0.0
	pp["head"].rotation = Vector3(0, 0, sin(t * 1.3 + i * 2.0) * 0.05)
	# まばたき: 人ごとにずらして、約3秒に1回
	var ph := fmod(t + i * 0.83, 3.1)
	var open := 0.12 if ph < 0.12 else 1.0
	for e in pp["eyes"]:
		e.scale = Vector3(1, open, 0.85)
	var talking: bool = _current()["name"] in ["contrib_talk", "punish_talk"]
	var m := 0.35 + (absf(sin(t * 9.0 + i)) * 0.9 if talking else 0.0)
	pp["mouth"].scale = Vector3(1.4, m, 0.5)


func _hand(i: int) -> Vector3:
	return people[i]["root"].to_global(Vector3(0.27, 0.5, -0.25))


func _arc(a: Vector3, b: Vector3, q: float, h: float) -> Vector3:
	return a.lerp(b, q) + Vector3(0, sin(q * PI) * h, 0)


func _anim_contrib(p: float, rd: Dictionary) -> void:
	var k := 0
	for i in range(4):
		var reach := _ease(p / 0.25) * (1.0 - _ease((p - 0.8) / 0.2))
		people[i]["rarm"].basis = Basis(Vector3.RIGHT, 1.25 * reach)
		var n := int(round(int(rd["contribs"][i]) / 2.0))
		for c in range(n):
			var q := _ease((p - 0.15 - c * 0.04) / 0.45)
			if q <= 0.0 or q >= 1.0 or k >= coins.size():
				continue
			var coin: MeshInstance3D = coins[k]
			k += 1
			coin.visible = true
			coin.position = _arc(_hand(i), POT_POS + Vector3(0, 0.1, 0), q, 0.6)
			coin.rotation = Vector3(q * 9.0, 0, q * 5.0)


func _anim_distribute(p: float, rd: Dictionary) -> void:
	var k := 0
	for i in range(4):
		var reach := _ease((p - 0.3) / 0.2) * (1.0 - _ease((p - 0.85) / 0.15))
		people[i]["rarm"].basis = Basis(Vector3.RIGHT, 0.9 * reach)
		people[i]["larm"].basis = Basis(Vector3.RIGHT, 0.9 * reach)
		for c in range(6):
			var q := _ease((p - 0.35 - c * 0.05) / 0.4)
			if q <= 0.0 or q >= 1.0 or k >= coins.size():
				continue
			var coin: MeshInstance3D = coins[k]
			k += 1
			coin.visible = true
			coin.position = _arc(POT_POS + Vector3(0, 0.2, 0), _hand(i), q, 0.5)
			coin.rotation = Vector3(q * 7.0, 0, q * 4.0)


func _point_basis(i: int, j: int) -> Basis:
	## i の右腕を j の頭へ向ける(腕は肩の -Y 方向に伸びている)
	var root: Node3D = people[i]["root"]
	var target: Vector3 = people[j]["root"].to_global(Vector3(0, 0.95, 0))
	var shoulder := root.to_global(Vector3(0.27, 0.5, 0))
	var dir_local := root.global_transform.basis.inverse() * (target - shoulder).normalized()
	return Basis.looking_at(dir_local, Vector3.UP) * Basis(Vector3.RIGHT, PI / 2.0)


func _anim_punish(p: float, rd: Dictionary) -> void:
	var k := 0
	var recv := [0, 0, 0, 0]
	for i in range(4):
		# 一番多く減点した相手を指さす
		var best := -1
		var best_pts := 0
		for j in range(4):
			var pts := int(rd["points"][i][j])
			if i != j and pts > best_pts:
				best = j
				best_pts = pts
			if i != j:
				recv[j] += pts
		if best >= 0:
			var q := _ease(p / 0.25)
			var rest := Quaternion(Basis())
			var aim := Quaternion(_point_basis(i, best))
			people[i]["rarm"].basis = Basis(rest.slerp(aim, q))
		for j in range(4):
			var pts := int(rd["points"][i][j])
			if i == j or pts == 0 or k >= balls.size():
				continue
			var q := _ease((p - 0.25) / 0.5)
			if q > 0.0 and q < 1.0:
				var b: MeshInstance3D = balls[k]
				b.visible = true
				b.scale = Vector3.ONE * (0.8 + pts * 0.12)
				b.position = _arc(_hand(i), people[j]["root"].to_global(Vector3(0, 0.95, 0)), q, 0.5)
			k += 1
	var hit := _ease((p - 0.75) / 0.1)
	for j in range(4):
		if recv[j] == 0:
			continue
		var pp: Dictionary = people[j]
		pp["head_mat"].emission_energy_multiplier = 0.45 * hit * (0.6 + 0.4 * sin(t * 12.0))
		if hit > 0.0:
			for e in pp["eyes"]:
				e.scale = Vector3(1.1, 0.3, 0.85)
		if p < 1.0:
			pp["body"].rotation = Vector3(0, 0, sin(t * 30.0) * 0.08 * hit * (1.0 - _ease((p - 0.85) / 0.15)))
		var lab: Label3D = hit_labels[j]
		lab.visible = hit > 0.0
		lab.text = "-%d点" % recv[j]
		lab.position = SEATS[j] + Vector3(0, 1.75, 0)


func _anim_result(p: float, rd: Dictionary) -> void:
	# この回の手元が多かった人ほど、少し高く跳ねる
	var finals: Array = rd["final"]
	var top := -INF
	for v in finals:
		top = maxf(top, float(v))
	for i in range(4):
		var h := 0.0
		if is_equal_approx(float(finals[i]), top):
			h = absf(sin(p * PI * 2.0)) * 0.15
			for e in people[i]["eyes"]:
				e.scale = Vector3(1.05, 0.55, 0.85)
		people[i]["body"].position = Vector3(0, h, 0)


# ---- 2D のカードと見出し ----

func _build_hud() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	hud = Control.new()
	hud.size = Vector2(1920, 1080)
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer.add_child(hud)
	hud.draw.connect(_draw_hud)


func _text(pos: Vector2, s: String, size: int, color := INK, f: Font = null, width := -1.0,
		align := HORIZONTAL_ALIGNMENT_LEFT) -> void:
	hud.draw_string(f if f else font, pos, s, align, width, size, color)


func _wrap(pos: Vector2, s: String, size: int, width: float, color := INK, max_lines := -1) -> void:
	hud.draw_multiline_string(font, pos, s, HORIZONTAL_ALIGNMENT_LEFT, width, size, max_lines, color)


func _draw_hud() -> void:
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
	_draw_header(r, st["name"], rd)
	for i in range(4):
		_draw_card(i, st["name"], r, rd)
	var s := "参加者はすべて架空の人物。演じたAI: %s(claude -p %s)" % [
		str(data["llm"]).trim_prefix("claude:"), str(data["llm_version"]).split(" ")[0]]
	_text(Vector2(28, 1064), s, 22, SUB)


func _panel(rect: Rect2, alpha := 0.88) -> void:
	hud.draw_rect(rect, Color(PAPER, alpha))


func _draw_title(p: float) -> void:
	var a := _ease(p * 3.0)
	var W := 1920.0
	_panel(Rect2(260, 330, 1400, 420), 0.85 * a)
	_text(Vector2(0, 450), data["title"], 84, Color(INK, a), bold, W, HORIZONTAL_ALIGNMENT_CENTER)
	_text(Vector2(0, 535), data.get("subtitle", "AIが演じる4人の参加者が、%d回くり返す" % data["rounds"].size()), 40,
		Color(SUB, a), font, W, HORIZONTAL_ALIGNMENT_CENTER)
	var g: Dictionary = data["game"]
	_text(Vector2(0, 625), "毎回%dポイントを受け取り、グループの口座に入れる量を決める。口座の合計×%sが全員に配られる。" % [
		g["endowment"], str(g["mpcr"])], 30, Color(SUB, a), font, W, HORIZONTAL_ALIGNMENT_CENTER)
	if g["punishment"]:
		var rule := "そのあと、ほかの人に減点を付けられる。付けた人も払い、付けられた人はその回の稼ぎが1点につき10%減る。"
		if g.get("punish_rule", "flat") != "fg2000":
			rule = "そのあと、ほかの人に減点を付けられる。1点付けると自分が%d減り、相手が%d減る。" % [
				g["punish_cost"], g["punish_impact"]]
		_text(Vector2(0, 675), rule, 30, Color(SUB, a), font, W, HORIZONTAL_ALIGNMENT_CENTER)


func _draw_end(p: float) -> void:
	var a := _ease(p * 3.0)
	_panel(Rect2(560, 230, 800, 620), 0.9 * a)
	_text(Vector2(0, 320), "%d回の合計" % data["rounds"].size(), 56, Color(INK, a), bold, 1920,
		HORIZONTAL_ALIGNMENT_CENTER)
	for i in range(4):
		var y := 420 + i * 90
		hud.draw_circle(Vector2(700, y - 14), 22, Color(COLORS[i], a))
		_text(Vector2(750, y), data["members"][i]["name"], 40, Color(INK, a), bold)
		_text(Vector2(1000, y), "%s ポイント" % _num(_total(i, data["rounds"].size())), 40, Color(INK, a))
	_text(Vector2(0, 810), "台詞は、AIが答えた判断の理由をそのまま表示(長いものは途中で省略)", 24,
		Color(SUB, a), font, 1920, HORIZONTAL_ALIGNMENT_CENTER)


func _draw_header(r: int, step: String, rd: Dictionary) -> void:
	var label := {
		"intro": "", "contrib": "口座に入れる", "contrib_talk": "なぜその量にしたか",
		"distribute": "口座の合計×%sを、全員に配る" % str(data["game"]["mpcr"]),
		"punish": "減点を付ける", "punish_talk": "なぜ減点したか", "result": "この回の結果",
	}
	_panel(Rect2(0, 0, 1920, 96), 0.8)
	_text(Vector2(28, 66), "第%d回 / 全%d回" % [r + 1, data["rounds"].size()], 44, INK, bold)
	_text(Vector2(400, 66), label[step], 40, SUB)


func _draw_card(i: int, step: String, r: int, rd: Dictionary) -> void:
	var pos: Vector2 = CARD_POS[i]
	var col: Color = COLORS[i]
	var m: Dictionary = data["members"][i]
	var reason := ""
	if step == "contrib_talk":
		reason = rd["contribute_reasons"][i]
	elif step == "punish_talk":
		reason = rd["punish_reasons"][i]
	var h := CARD_SIZE.y if reason != "" else 200.0
	_panel(Rect2(pos, Vector2(CARD_SIZE.x, h)), 0.92)
	hud.draw_rect(Rect2(pos, Vector2(10, h)), col)
	_text(pos + Vector2(28, 44), m["name"], 32, INK, bold)
	var before := _total(i, r)
	_text(pos + Vector2(290, 44), "合計 %s" % _num(before + (float(rd["final"][i]) if step == "result" else 0.0)),
		24, SUB, font, 160, HORIZONTAL_ALIGNMENT_RIGHT)
	_wrap(pos + Vector2(28, 76), m["persona"], 18, CARD_SIZE.x - 50, SUB, 2)
	var now_txt := ""
	match step:
		"contrib", "contrib_talk":
			now_txt = "手元 %s" % _num(data["game"]["endowment"] - int(rd["contribs"][i]))
		"distribute", "punish", "punish_talk":
			now_txt = "手元 %s" % _num(rd["base"][i])
		"result":
			now_txt = "手元 %s" % _num(rd["final"][i])
	if step != "intro":
		_text(pos + Vector2(28, 150), "入れた %d" % int(rd["contribs"][i]), 28, col.darkened(0.2), bold)
	if now_txt != "":
		_text(pos + Vector2(270, 150), now_txt, 28, INK, bold, 180, HORIZONTAL_ALIGNMENT_RIGHT)
	if step in ["punish", "punish_talk", "result"] and data["game"]["punishment"]:
		var recv := 0
		var gave := 0
		for k in range(4):
			if k != i:
				recv += int(rd["points"][k][i])
				gave += int(rd["points"][i][k])
		_text(pos + Vector2(28, 184), "減点を付けた %d / 受けた %d" % [gave, recv], 22, SUB)
	if reason != "":
		var box := Rect2(pos + Vector2(24, 200), Vector2(CARD_SIZE.x - 44, CARD_SIZE.y - 212))
		hud.draw_rect(box, Color(col, 0.10))
		hud.draw_rect(box, Color(col, 0.5), false, 1.5)
		_wrap(box.position + Vector2(14, 30), "「" + reason + "」", 20, box.size.x - 28, INK, 7)


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
