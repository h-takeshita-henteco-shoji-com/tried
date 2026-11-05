# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=2.3,<3"]
# ///
"""LibreCAD を操作する MCP server。

LibreCAD の中で plugin(plugin/)を動かしておき、127.0.0.1:7471 に1行1件の JSON を送る。
測る・検証する・差分を取る道具は、plugin から読んだ図形を使って、この server の側で計算する。
起動: uv run code/librecad-mcp/server.py (MCP の stdio で話す)

座標は [x, y] の配列。角度は度。単位は図面の単位(多くは mm)。
図形の id は、移動・伸縮・元に戻すのあとで変わる。結果の new_ids を使うか、読み直す。
"""
import json
import math
import os
import re
import socket
from collections import Counter, defaultdict

from mcp.server.mcpserver import MCPServer

HOST = "127.0.0.1"
PORT = int(os.environ.get("LIBRECAD_MCP_PORT", "7471"))

Point = list[float]

mcp = MCPServer(
    "librecad",
    instructions=(
        "LibreCAD の中の図面を操作する。座標は [x, y]、角度は度。"
        "描いたり直したりしたら、list_entities や screenshot で読み戻して確かめる。"
        "直したあとは validate で直し漏れを調べる。"
    ),
)
_seq = 0
_snapshots: dict[str, list[dict]] = {}


def call(cmd: str, **args) -> dict:
    """plugin に命令を1つ送り、返事を1つ受け取る。"""
    global _seq
    _seq += 1
    args = {k: v for k, v in args.items() if v is not None}
    req = json.dumps({"id": _seq, "cmd": cmd, "args": args}, ensure_ascii=False) + "\n"
    try:
        with socket.create_connection((HOST, PORT), timeout=60) as s:
            s.sendall(req.encode())
            buf = b""
            while not buf.endswith(b"\n"):
                chunk = s.recv(1 << 20)
                if not chunk:
                    break
                buf += chunk
    except OSError as e:
        return {"ok": False, "error": f"LibreCAD に繋がりません({e})。LibreCAD のメニュー「プラグイン → MCP bridge」で待ち受けを始めてください。"}
    if not buf:
        return {"ok": False, "error": "LibreCAD から返事がありません。LibreCAD が落ちた可能性があります。"}
    r = json.loads(buf)
    r.pop("id", None)
    return r


def entities(**filters) -> list[dict]:
    r = call("list_entities", **filters)
    if not r.get("ok"):
        raise RuntimeError(r.get("error"))
    return r["entities"]


# ---------------------------------------------------------------- 状態とファイル

@mcp.tool()
def ping() -> dict:
    """LibreCAD の plugin が待ち受けているか確かめる。"""
    return call("ping")


@mcp.tool()
def doc_info() -> dict:
    """開いている図面の情報。ファイル名、未保存か、単位($INSUNITS 4=mm)、範囲、図形の数、画層、ブロック、寸法の設定。"""
    return call("doc_info")


@mcp.tool()
def open_drawing(path: str) -> dict:
    """DXF を開く。開いた図面が、以後の操作の対象になる。"""
    return call("open", path=os.path.abspath(path))


@mcp.tool()
def new_drawing() -> dict:
    """新しい図面を開く。以後の操作の対象になる。"""
    return call("new")


@mcp.tool()
def save() -> dict:
    """開いている図面を上書き保存する。名前のない図面では失敗するので、save_as を使う。"""
    return call("save")


@mcp.tool()
def save_as(path: str, overwrite: bool = False) -> dict:
    """図面を DXF として path に保存する。path は .dxf で終える。同じ名前があれば overwrite=true が要る。"""
    return call("save_as", path=os.path.abspath(path), overwrite=overwrite)


@mcp.tool()
def set_vars(vars: dict) -> dict:
    """図面の設定を変える。例: {"$DIMTXT": 250, "$DIMASZ": 150, "$DIMDEC": 0, "$INSUNITS": 4}。
    mm の住宅図面なら、寸法の文字 $DIMTXT と矢印 $DIMASZ を 100〜300 にしないと小さすぎて見えない。"""
    return call("set_vars", vars=vars)


@mcp.tool()
def operation_log() -> dict:
    """この接続で受けた命令の記録(時刻、命令、成否)。"""
    return call("log")


# ---------------------------------------------------------------- 読み取り

@mcp.tool()
def list_entities(layer: str | None = None, types: list[str] | None = None,
                  window: list[Point] | None = None, expand_blocks: bool = False) -> dict:
    """図形の一覧。どの図形にも id、種類、画層、色、外形 bbox が付く。
    types で種類を絞れる(line, polyline, arc, circle, text, mtext, insert, hatch, dim_linear, dim_aligned など)。
    window=[[x1,y1],[x2,y2]] で範囲を絞れる。寸法は label(書かれた文字)、measured(表示の値)、distance(線の長さ)を返す。"""
    return call("list_entities", layer=layer, types=types, window=window, expand_blocks=expand_blocks)


@mcp.tool()
def get_entity(id: str) -> dict:
    """図形1つの詳細。ブロックの挿入なら、中の図形も返す。"""
    return call("get_entity", id=id)


@mcp.tool()
def list_blocks(contents: bool = False) -> dict:
    """ブロック(扉・窓などの部品)の一覧と、挿入された数。contents=true で中の図形も返す。"""
    return call("list_blocks", contents=contents)


@mcp.tool()
def list_fonts() -> dict:
    """使える書体。日本語は unicode か kst32b。"""
    return call("fonts")


# ---------------------------------------------------------------- 描く

@mcp.tool()
def add_line(p1: Point, p2: Point, layer: str | None = None, color: str | None = None) -> dict:
    """線を描く。layer がなければ作る。color は "#ff0000" の形。"""
    return call("add_line", p1=p1, p2=p2, layer=layer, color=color)


@mcp.tool()
def add_polyline(points: list[Point], closed: bool = False, layer: str | None = None, color: str | None = None) -> dict:
    """ポリラインを描く。closed=true で閉じる(壁や部屋の輪郭に使う)。"""
    return call("add_polyline", points=points, closed=closed, layer=layer, color=color)


@mcp.tool()
def add_circle(center: Point, r: float, layer: str | None = None, color: str | None = None) -> dict:
    """円を描く。"""
    return call("add_circle", center=center, r=r, layer=layer, color=color)


@mcp.tool()
def add_arc(center: Point, r: float, a1: float, a2: float, reversed: bool = False,
            layer: str | None = None, color: str | None = None) -> dict:
    """円弧を描く。a1 から a2 へ反時計回り(度)。扉の開きの軌跡に使う。"""
    return call("add_arc", center=center, r=r, a1=a1, a2=a2, reversed=reversed, layer=layer, color=color)


@mcp.tool()
def add_text(text: str, p: Point, height: float = 250, align: str = "left", valign: str = "baseline",
             angle: float = 0, font: str = "unicode", layer: str | None = None, color: str | None = None) -> dict:
    """文字を置く。align は left/center/right、valign は baseline/bottom/middle/top。
    部屋の中央に置くなら align=center, valign=middle で、p に部屋の中心を渡す。結果の bbox で大きさを確かめられる。"""
    return call("add_text", text=text, p=p, height=height, align=align, valign=valign, angle=angle,
                font=font, layer=layer, color=color)


@mcp.tool()
def add_dim_linear(p1: Point, p2: Point, line: Point, angle: float = 0, text: str | None = None,
                   layer: str | None = None) -> dict:
    """長さの寸法を描く。p1, p2 は測る2点。line は寸法線が通る点。angle は寸法線の向き(0 で水平、90 で垂直)。
    text を渡すと、その文字を書く(渡さなければ測った値)。"""
    return call("add_dim_linear", p1=p1, p2=p2, line=line, angle=angle, text=text, layer=layer)


@mcp.tool()
def add_dim_aligned(p1: Point, p2: Point, line: Point, text: str | None = None, layer: str | None = None) -> dict:
    """平行寸法を描く。p1-p2 に平行な寸法線を、line を通る位置に引く。"""
    return call("add_dim_aligned", p1=p1, p2=p2, line=line, text=text, layer=layer)


@mcp.tool()
def add_hatch(points: list[Point], pattern: str = "SOLID", scale: float = 1, angle: float = 0,
              layer: str | None = None, color: str | None = None) -> dict:
    """閉じた境界を塗る。pattern は SOLID か ANSI31 など。"""
    return call("add_hatch", points=points, pattern=pattern, scale=scale, angle=angle, layer=layer, color=color)


@mcp.tool()
def define_block(name: str, base: Point, ids: list[str], replace: bool = False) -> dict:
    """ids の図形から、部品(ブロック)を作る。base は部品の基点。replace=true で、元の図形をその部品の挿入に置き換える。"""
    return call("define_block", name=name, base=base, ids=ids, replace=replace)


@mcp.tool()
def add_insert(block: str, p: Point, angle: float = 0, scale: Point | None = None, layer: str | None = None) -> dict:
    """部品(ブロック)を置く。p に基点が来る。"""
    return call("add_insert", block=block, p=p, angle=angle, scale=scale, layer=layer)


# ---------------------------------------------------------------- 直す

@mcp.tool()
def set_props(id: str, layer: str | None = None, color: str | None = None, text: str | None = None,
              height: float | None = None, p1: Point | None = None, p2: Point | None = None) -> dict:
    """図形の属性を変える。text は文字・寸法の文字を書き換える(寸法で "" にすると測った値に戻る)。
    p1, p2 は線の端。元に戻せる。id は新しくなる(結果の entity.id)。"""
    return call("set_props", id=id, layer=layer, color=color, text=text, height=height, p1=p1, p2=p2)


@mcp.tool()
def move(ids: list[str], offset: Point) -> dict:
    """図形を offset だけ動かす。結果の new_ids が、動かした後の id。"""
    return call("move", ids=ids, offset=offset)


@mcp.tool()
def copy(ids: list[str], offset: Point) -> dict:
    """図形を offset だけずらして複写する。"""
    return call("copy", ids=ids, offset=offset)


@mcp.tool()
def rotate(ids: list[str], center: Point, angle: float, keep_original: bool = False) -> dict:
    """図形を center を中心に angle 度回す。"""
    return call("rotate", ids=ids, center=center, angle=angle, keep_original=keep_original)


@mcp.tool()
def scale(ids: list[str], center: Point, factor: float, keep_original: bool = False) -> dict:
    """図形を center を中心に factor 倍する。"""
    return call("scale", ids=ids, center=center, factor=factor, keep_original=keep_original)


@mcp.tool()
def mirror(ids: list[str], p1: Point, p2: Point, keep_original: bool = False) -> dict:
    """図形を p1-p2 の線で鏡写しにする。扉の吊り元を変えるときに使う。"""
    return call("mirror", ids=ids, p1=p1, p2=p2, keep_original=keep_original)


@mcp.tool()
def delete(ids: list[str]) -> dict:
    """図形を消す。"""
    return call("delete", ids=ids)


@mcp.tool()
def stretch(p1: Point, p2: Point, offset: Point) -> dict:
    """窓 [p1, p2] の中にある端点を offset だけ動かす(LibreCAD のストレッチ)。
    壁を外へ動かすとき、窓で壁の端と寸法の端をまとめて囲むと、寸法も一緒に伸びる。
    寸法の文字を手で書いている(label が空でない)寸法は、文字が古いまま残るので、set_props で直す。"""
    return call("stretch", p1=p1, p2=p2, offset=offset)


@mcp.tool()
def undo(steps: int = 1) -> dict:
    """直前の操作を元に戻す。戻したあとは id が変わるので、読み直す。"""
    return call("undo", steps=steps)


@mcp.tool()
def redo(steps: int = 1) -> dict:
    """元に戻した操作をやり直す。"""
    return call("redo", steps=steps)


# ---------------------------------------------------------------- 画層

@mcp.tool()
def layers() -> dict:
    """画層の一覧(色、線種、表示)と、今の画層。"""
    return call("layers")


@mcp.tool()
def set_layer(name: str, color: str | None = None, linetype: str | None = None,
              visible: bool | None = None, current: bool = False) -> dict:
    """画層を作るか直す。linetype は solid/dash/dot/center/dashdot。current=true で今の画層にする。"""
    return call("set_layer", name=name, color=color, linetype=linetype, visible=visible, current=current)


# ---------------------------------------------------------------- 確かめる(画面)

@mcp.tool()
def zoom(window: list[Point] | None = None) -> dict:
    """表示を合わせる。window がなければ全体。"""
    return call("zoom", window=window)


@mcp.tool()
def screenshot(path: str, window: list[Point] | None = None) -> dict:
    """図面を映している部分を PNG に保存する。window で範囲を指定できる(なければ全体)。
    保存した画像は Read などで開いて、目で確かめる。"""
    return call("screenshot", path=os.path.abspath(path), window=window)


# ---------------------------------------------------------------- 測る(この server で計算)

def _area(pts: list[Point]) -> float:
    s = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def _length(e: dict) -> float:
    t = e["type"]
    if t == "line":
        return math.dist(e["p1"], e["p2"])
    if t == "polyline":
        pts = e["points"] + (e["points"][:1] if e.get("closed") else [])
        return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    if t == "circle":
        return 2 * math.pi * e["r"]
    if t == "arc":
        a = (e["a2"] - e["a1"]) % 360
        if e.get("reversed"):
            a = 360 - a
        return math.radians(a) * e["r"]
    return 0.0


@mcp.tool()
def measure(ids: list[str] | None = None, points: list[Point] | None = None) -> dict:
    """長さと面積を測る。points だけなら、各区間の距離・合計・閉じた形としての面積。
    ids なら、各図形の長さと、閉じたポリラインの面積(mm² と ㎡、畳=1.62㎡ 換算)、全体の外形。"""
    out: dict = {"ok": True}
    if points:
        segs = [math.dist(a, b) for a, b in zip(points, points[1:])]
        out["segments"] = segs
        out["total"] = sum(segs)
        if len(points) >= 3:
            a = _area(points)
            out["area"] = a
            out["area_m2"] = a / 1e6
    if ids:
        want = set(ids)
        items, mins, maxs = [], [], []
        for e in entities():
            if e["id"] not in want:
                continue
            it = {"id": e["id"], "type": e["type"], "length": _length(e)}
            if e["type"] == "polyline" and e.get("closed"):
                a = _area(e["points"])
                it.update(area=a, area_m2=a / 1e6, tatami=a / 1e6 / 1.62)
            if e["type"] == "hatch":
                it.update(area=e.get("area"))
            items.append(it)
            mins.append(e["bbox"][0])
            maxs.append(e["bbox"][1])
        out["items"] = items
        if mins:
            lo = [min(p[0] for p in mins), min(p[1] for p in mins)]
            hi = [max(p[0] for p in maxs), max(p[1] for p in maxs)]
            out["bbox"] = [lo, hi]
            out["size"] = [hi[0] - lo[0], hi[1] - lo[1]]
        missing = want - {i["id"] for i in items}
        if missing:
            out["missing_ids"] = sorted(missing)
    return out


def _point_seg_dist(p, a, b) -> float:
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L))
    return math.dist(p, (ax + t * dx, ay + t * dy))


def _dist_to(e: dict, p: Point) -> float:
    t = e["type"]
    if t == "line":
        return _point_seg_dist(p, e["p1"], e["p2"])
    if t == "polyline":
        pts = e["points"] + (e["points"][:1] if e.get("closed") else [])
        return min((_point_seg_dist(p, a, b) for a, b in zip(pts, pts[1:])), default=math.inf)
    if t in ("circle", "arc"):
        return abs(math.dist(p, e["center"]) - e["r"])
    (x1, y1), (x2, y2) = e["bbox"]
    dx = max(x1 - p[0], 0, p[0] - x2)
    dy = max(y1 - p[1], 0, p[1] - y2)
    return math.hypot(dx, dy)


@mcp.tool()
def find_near(p: Point, radius: float = 200, layer: str | None = None, types: list[str] | None = None) -> dict:
    """点 p から radius 以内にある図形を、近い順に返す。「この壁」「この扉」を id で指すために使う。"""
    w = [[p[0] - radius, p[1] - radius], [p[0] + radius, p[1] + radius]]
    hits = []
    for e in entities(layer=layer, types=types, window=w):
        d = _dist_to(e, p)
        if d <= radius:
            hits.append({"distance": round(d, 3), **e})
    hits.sort(key=lambda h: h["distance"])
    return {"ok": True, "entities": hits}


def _segments(es: list[dict]):
    """線とポリラインを、端点のある区間に分ける。"""
    for e in es:
        if e["type"] == "line":
            yield e["id"], e["p1"], e["p2"]
        elif e["type"] == "polyline":
            pts = e["points"] + (e["points"][:1] if e.get("closed") else [])
            for a, b in zip(pts, pts[1:]):
                yield e["id"], a, b
        elif e["type"] == "arc":
            yield e["id"], e["p1"], e["p2"]


def _open_ends(es: list[dict], tol: float):
    """どの区間の線上にも乗っていない端点を返す。壁の切れ目や隙間の候補。"""
    segs = list(_segments(es))
    ends = []
    for i, (eid, a, b) in enumerate(segs):
        for p in (a, b):
            touching = any(
                j != i and _point_seg_dist(p, c, d) <= tol for j, (_, c, d) in enumerate(segs)
            )
            if not touching:
                ends.append({"id": eid, "p": [round(p[0], 3), round(p[1], 3)]})
    return ends


@mcp.tool()
def check_connectivity(layer: str, tol: float = 1.0, gap_max: float = 1000) -> dict:
    """画層の線がつながっているかを調べる。どこにもつながらない端点(open_ends)と、
    gap_max 以内で向かい合う端点の組(gaps)を返す。壁の画層で使うと、壁の隙間や切れ目が分かる。
    扉や窓の開口も切れ目として出るので、扉・窓の位置と照らし合わせて判断する。"""
    es = entities(layer=layer)
    ends = _open_ends(es, tol)
    gaps = []
    for i in range(len(ends)):
        for j in range(i + 1, len(ends)):
            d = math.dist(ends[i]["p"], ends[j]["p"])
            if d <= gap_max:
                gaps.append({"a": ends[i], "b": ends[j], "distance": round(d, 3)})
    gaps.sort(key=lambda g: g["distance"])
    return {"ok": True, "open_ends": ends, "gaps": gaps}


# ---------------------------------------------------------------- 検証と差分(この server で計算)

def _num(label: str) -> float | None:
    m = re.search(r"-?\d[\d,]*\.?\d*", label or "")
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _rp(p) -> tuple:
    return tuple(round(c, 1) for c in p)


def _signature(e: dict) -> tuple:
    """図形の形を表すキー。id が変わっても、同じ形なら同じキーになる。"""
    t, layer = e["type"], e["layer"]
    if t == "line":
        return (t, layer, tuple(sorted([_rp(e["p1"]), _rp(e["p2"])])))
    if t == "polyline":
        return (t, layer, tuple(_rp(p) for p in e["points"]), e.get("closed"))
    if t in ("arc", "circle"):
        return (t, layer, _rp(e["center"]), round(e["r"], 1), round(e.get("a1", 0), 1), round(e.get("a2", 0), 1))
    if t in ("text", "mtext"):
        return (t, layer, e.get("text"), _rp(e["p"]), round(e.get("height", 0), 1))
    if t == "insert":
        return (t, layer, e.get("block"), _rp(e["p"]), round(e.get("angle", 0), 1))
    if t.startswith("dim_") and "p1" in e:
        return (t, layer, _rp(e["p1"]), _rp(e["p2"]), _rp(e["defpoint"]), e.get("label"))
    return (t, layer, tuple(_rp(p) for p in e["bbox"]))


@mcp.tool()
def validate(wall_layer: str | None = None, orthogonal_layers: list[str] | None = None,
             dim_tol: float = 1.0, gap_max: float = 1000, angle_tol: float = 0.1) -> dict:
    """図面の直し漏れを調べる。
    - dim_mismatch: 寸法の書かれた文字と、線の長さが食い違う(文字だけ古い寸法)
    - duplicates: 同じ形の図形が重なっている(消し忘れ)
    - wall_gaps: wall_layer の線の切れ目(扉・窓・開口でなければ隙間)
    - skewed: orthogonal_layers の線のうち、縦でも横でもないもの(stretch で片端だけ動いた線)
      通り芯・壁・寸法補助線など、縦横しかないはずの画層を渡す。屋根など斜めの線がある画層は渡さない
    違反があれば直し、もう一度 validate する。stretch のあとは screenshot も撮って目で確かめる。"""
    es = entities()
    problems: dict = {}
    mism = []
    for e in es:
        if not e["type"].startswith("dim_") or "distance" not in e:
            continue
        label = e.get("label") or ""
        if label in ("", "<>"):
            continue
        n = _num(label)
        if n is not None and abs(n - e["distance"]) > dim_tol:
            mism.append({"id": e["id"], "label": label, "distance": round(e["distance"], 3),
                         "p1": e["p1"], "p2": e["p2"], "layer": e["layer"]})
    problems["dim_mismatch"] = mism
    sig = defaultdict(list)
    for e in es:
        sig[_signature(e)].append(e["id"])
    problems["duplicates"] = [{"type": k[0], "layer": k[1], "ids": v} for k, v in sig.items() if len(v) > 1]
    if wall_layer:
        problems["wall_gaps"] = check_connectivity(wall_layer, gap_max=gap_max)["gaps"]
    if orthogonal_layers:
        skew = []
        for e in es:
            if e["layer"] not in orthogonal_layers:
                continue
            for eid, a, b in _segments([e]):
                if e["type"] == "arc" or math.dist(a, b) < 1e-6:
                    continue
                ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 90
                off = min(ang, 90 - ang)
                if off > angle_tol:
                    skew.append({"id": eid, "layer": e["layer"], "p1": a, "p2": b, "off_axis_deg": round(off, 3)})
        problems["skewed"] = skew
    count = sum(len(v) for v in problems.values())
    return {"ok": True, "problem_count": count, **problems}


@mcp.tool()
def snapshot(name: str) -> dict:
    """今の図面の形を name で覚える。直す前に撮っておき、直した後に diff で比べる。"""
    es = entities()
    _snapshots[name] = es
    return {"ok": True, "name": name, "count": len(es)}


@mcp.tool()
def diff(name: str, window: list[Point] | None = None, layer: str | None = None) -> dict:
    """snapshot(name) の時点と今を比べ、消えた図形(removed)と増えた図形(added)を返す。
    id ではなく形で比べるので、動かした図形は「消えて増えた」と出る。
    window や layer で、変わってはいけない場所だけを比べられる。"""
    if name not in _snapshots:
        return {"ok": False, "error": f"snapshot がありません: {name}"}

    def keep(e):
        if layer and e["layer"] != layer:
            return False
        if window:
            (x1, y1), (x2, y2) = window
            lo, hi = [min(x1, x2), min(y1, y2)], [max(x1, x2), max(y1, y2)]
            (a, b), (c, d) = e["bbox"]
            if c < lo[0] or a > hi[0] or d < lo[1] or b > hi[1]:
                return False
        return True

    before = [e for e in _snapshots[name] if keep(e)]
    after = [e for e in entities() if keep(e)]
    cb = Counter(_signature(e) for e in before)
    ca = Counter(_signature(e) for e in after)

    def pick(es, sigs):
        out, left = [], Counter(sigs)
        for e in es:
            s = _signature(e)
            if left[s] > 0:
                left[s] -= 1
                out.append(e)
        return out

    return {"ok": True, "removed": pick(before, cb - ca), "added": pick(after, ca - cb),
            "unchanged": sum((cb & ca).values())}


if __name__ == "__main__":
    mcp.run()
