"""Cities: Skylines を Claude から見るための MCP サーバー。

AIMayor Mod がゲームの中に開く HTTP の窓口(http://127.0.0.1:8781/)を呼ぶ。
座標はゲーム上のメートル。x が東、z が北。地図の中心が (0, 0)、端が ±8640。
福岡のマップは水平1/2縮尺なので、ゲーム上の1mは実寸2m。

起動: uv run --directory code/ai-mayor/mcp server.py
"""
import functools
import inspect
import io
import itertools
import json
import math
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from mcp.server.mcpserver import Image, MCPServer
from PIL import Image as PILImage
from PIL import ImageDraw

BASE = os.environ.get("AIMAYOR_URL", "http://127.0.0.1:8781")

# 道具の出し方(#108)。main は比べる本番の形で、ゲームの式をそのまま見せる道具と欄を外す(council-design.md の10.6)。
# grow は街を育てる期間の形で、全部を出す。既定は main。育て直すときだけ .mcp.json の env で AIMAYOR_MODE=grow にする
MODE = os.environ.get("AIMAYOR_MODE", "main")
# 本番で外す道具(ゲームの計算の中身を返すもの)
MAIN_HIDDEN_TOOLS = {"building_levelup"}

mcp = MCPServer("cities-skylines", instructions="Cities: Skylines の街を見て操作するための道具。座標はゲーム上のメートルで、x が東、z が北、地図の中心が (0, 0)。")


def call(path: str, timeout: float = 15, body: str | None = None, **params) -> dict:
    """Mod の窓口を呼び、JSON を返す。body を渡すと POST で送る。つながらないときは ok=false の辞書を返す。"""
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{BASE}{path}" + (f"?{query}" if query else "")
    data = body.encode("utf-8") if body is not None else None
    try:
        with urllib.request.urlopen(url, data=data, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as e:
        return {"ok": False, "error": f"ゲームの窓口につながらない: {e}. ゲームが起動していて AI Mayor Mod が有効か確認する"}


_seq = itertools.count(1)


def notify(**params) -> None:
    """ゲーム画面のパネルへ、AI市長が呼んだ道具を知らせる。届かなくても道具の処理は止めない。"""
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    try:
        with urllib.request.urlopen(f"{BASE}/ui/command?{query}", timeout=0.5) as r:
            r.read()
    except Exception:
        pass


def notify_note(action: str, reason: str) -> None:
    """判断(何をするか、なぜするか)をパネルに出す。届かなくても止めない。"""
    query = urllib.parse.urlencode({"action": _hide_paths(action)[:200], "reason": _hide_paths(reason)[:300]})
    try:
        with urllib.request.urlopen(f"{BASE}/ui/note?{query}", timeout=0.5) as r:
            r.read()
    except Exception:
        pass


# 空白を含むフォルダ(Application Support など)も1つのパスとして拾う。空白の後に / を含む語が続くときだけ、つなげる
_PATH = re.compile(r"(?:~|/Users|/home|/private|/tmp|/var|/Volumes)/(?:[^\s'\"]| (?=[^\s'\"/]+/))*")


def _hide_paths(v):
    """パネルとログに手元のパスを出さない(ユーザー名が録画に映るため。#92)。ファイル名だけを残す。"""
    if isinstance(v, str):
        if v.startswith(("/", "~")):
            return os.path.basename(v.rstrip("/")) or v
        return _PATH.sub(lambda m: os.path.basename(m.group(0).rstrip("/")), v)
    return v


def _short(v, limit: int = 60) -> str:
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= limit else s[:limit - 3] + "..."


# ---- 操作の前にカメラを向ける(#82) ----
# ゲームの画面は録画して投稿されることが多い。見ている人が「どこを触るか」を先に分かるように、
# 場所を持つ道具は、操作の前にその地点へカメラを寄せ、少し待ってから操作し、結果を少し見せる。
# 市長への指示ではなく MCP 側で行う。指示だと省かれることがあり、市長のトークンも増えるため。
# AIMAYOR_FOLLOW=0 で切れる(人が手で試すとき)
FOLLOW = os.environ.get("AIMAYOR_FOLLOW", "1") != "0"
FOLLOW_BEFORE = 1.0  # 寄ってから操作するまでの秒数
FOLLOW_AFTER = 2.0  # 操作の後に結果を見せる秒数
FOLLOW_PITCH = 45  # 見下ろす角度。真上より街らしく見える
# 画面の左に道具のパネルがあり、対象が隠れる。北を上にして、見る場所を西へずらし、対象を画面の右寄りに出す。
# 画面の幅は引きの約2倍(m)。0.3 ずらすと、対象の中心が画面の左から約65%の所に来る
PANEL_SHIFT = 0.3


def _aim(x: float, z: float, size: float, pitch: int) -> dict:
    return call("/camera", timeout=8, x=round(x - size * PANEL_SHIFT), z=round(z), size=round(size), pitch=pitch, yaw=0)


def _circle(a: dict, default_radius: float) -> tuple[float, float, float]:
    r = float(a.get("radius", default_radius))
    return float(a["x"]), float(a["z"]), r * 2


def _points(a: dict) -> tuple[float, float, float]:
    pts = a["points"]
    xs = [float(p[0]) for p in pts]
    zs = [float(p[1]) for p in pts]
    return (min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2, max(max(xs) - min(xs), max(zs) - min(zs))


# 道具の名前 → 引数から (見る場所 x, z, 収めたい幅 m) を出す関数
FOCUS = {
    "build_line": _points,
    "remove_line": _points,
    "place_building": lambda a: (float(a["x"]), float(a["z"]), 150.0),
    "relocate_building": lambda a: (float(a["x"]), float(a["z"]), 150.0),
    "zone_polygon": _points,
    "zone_rect": lambda a: _points({"points": [[a["x1"], a["z1"]], [a["x2"], a["z2"]]]}),
    "zone_area": lambda a: _circle(a, 100),
    "bulldoze": lambda a: _circle(a, 50),
    "paint_district": lambda a: _circle(a, 150),
    "set_traffic_lights": lambda a: (float(a["x"]), float(a["z"]), 100.0),
    "set_yield_sign": lambda a: (float(a["x"]), float(a["z"]), 100.0),
    "upgrade_road": _points,
    "plant_trees": lambda a: _points({"points": a["polygon"]}),
    "remove_trees": lambda a: _points({"points": a["polygon"]}),
    "level_terrain": lambda a: _points({"points": a["polygon"]}),
    "raise_terrain": lambda a: _points({"points": a["polygon"]}),
    "lower_terrain": lambda a: _points({"points": a["polygon"]}),
    "create_transport_line": lambda a: _points({"points": a["stops"]}),
    "reverse_road": _points,
}


def _focus(name: str, args: dict) -> bool:
    """操作の前に、対象の地点へカメラを寄せる。寄せたら True。失敗しても操作は止めない。"""
    if not FOLLOW or name not in FOCUS:
        return False
    try:
        x, z, extent = FOCUS[name](args)
    except (KeyError, TypeError, ValueError, IndexError):
        return False
    size = min(max(extent * 1.5, 300.0), 4000.0)
    r = _aim(x, z, size, FOLLOW_PITCH)
    if not r.get("ok"):
        return False
    time.sleep(FOLLOW_BEFORE)
    return True


def _overview() -> bool:
    """街の全体をカメラに収める。advance で時間を進める間に、街の全体が育つ様子を映すため(#82)。
    建物の位置の5〜95%の範囲を見る(遠くの取水口などの外れ値で引きすぎないように)。建物がなければ動かさない。"""
    if not FOLLOW:
        return False
    d = call("/buildings", timeout=30, x=0, z=0, radius=9000, limit=20000)
    bs = d.get("buildings") or []
    if not bs:
        return False
    xs = sorted(b["x"] for b in bs)
    zs = sorted(b["z"] for b in bs)
    lo, hi = int(len(xs) * 0.05), max(int(len(xs) * 0.95) - 1, 0)
    x0, x1, z0, z1 = xs[lo], xs[hi], zs[lo], zs[hi]
    size = min(max(max(x1 - x0, z1 - z0) * 1.2, 800.0), 4000.0)
    r = _aim((x0 + x1) / 2, (z0 + z1) / 2, size, 60)
    return bool(r.get("ok"))


def tool():
    """mcp.tool() の代わり。道具の開始と終了(成否と秒数)をゲーム画面のパネルに知らせる。
    場所を持つ道具は、操作の前にカメラを対象へ寄せる(FOCUS)。"""
    def deco(fn):
        sig = inspect.signature(fn)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            cid = str(next(_seq))
            bound = sig.bind(*args, **kwargs)
            shown = " ".join(f"{k}={_short(_hide_paths(v))}" for k, v in bound.arguments.items())
            notify(phase="start", id=cid, tool=fn.__name__, args=_short(shown, 200))
            t0 = time.time()
            # 区画を指定するときは、区画の色を見せてから寄る。どんな区画かを見ている人が分かるように(#82)
            zoning = FOLLOW and fn.__name__ in ("zone_area", "zone_polygon", "zone_rect")
            if zoning:
                call("/ui/zoning", timeout=3, show="true", zone=bound.arguments.get("type"))
            focused = _focus(fn.__name__, dict(bound.arguments))
            try:
                try:
                    result = fn(*args, **kwargs)
                    if focused and not (isinstance(result, dict) and result.get("ok") is False):
                        time.sleep(FOLLOW_AFTER)  # 道路が伸びる、建物が建つ、区画の色が付く、を見せる
                finally:
                    if zoning:
                        call("/ui/zoning", timeout=3, show="false")
            except Exception as e:
                notify(phase="end", id=cid, ok="false", detail=_short(_hide_paths(str(e)), 120))
                raise
            sec = f"{time.time() - t0:.1f}s"
            if isinstance(result, dict) and result.get("ok") is False:
                notify(phase="end", id=cid, ok="false", detail=_short(_hide_paths(f"{result.get('error')} ({sec})"), 120))
            else:
                # 建設費を返す道具は、ログにも費用を残す
                cost = result.get("cost") if isinstance(result, dict) else None
                notify(phase="end", id=cid, ok="true", detail=f"{sec} cost={cost}" if cost is not None else sec)
            return result

        if MODE == "main" and fn.__name__ in MAIN_HIDDEN_TOOLS:
            return wrapper  # 本番では道具として出さない
        return mcp.tool()(wrapper)

    return deco


@tool()
def city_info() -> dict:
    """街の基本の数字を返す。モード、街の名前、ゲーム内の日付、一時停止中か、速度、人口、幸福度、
    所持金、週の収入と支出、需要(住宅・商業・工業。0〜100)、持っている区画の数。
    citizensWithoutService: 電気・水・下水が来ない市民の数(citizens_summary の peopleWithProblems と同じ数え方)。
    市民ごとの数えで、家に来ていないことに少なくとも1回気づいた住民の数。来れば次の更新で0に戻る。
    棟の数(zone_map の赤い枠)とは単位も時点も違う。
    happiness はゲームの画面と同じ街の幸福度。
    tourists: 観光客。now は今いる観光客の数、visits は訪問の平均(ゲームの統計と同じ値)。
    dialog: ゲームの画面に出ているダイアログ(破産の警告など)。なければ null。
    出ていたら、見出し(texts)とボタン(buttons)を読み、判断の材料にする。
    dialogSeq: 最後に開いたダイアログの連番。前回より増えていたら、dialog_events で閉じたものも読める。
    人口の節目のお知らせ(UnlockingPanel)は、MOD が自動で閉じる。dialog には出ず、dialog_events に autoClosed=true で残る。"""
    return call("/info")


@tool()
def sim_health() -> dict:
    """ゲームの計算スレッドが命令を受け付けるかを確かめる。道具が "simulation thread timeout" を返したときに使う。
    simulationResponds: 1秒以内に空の命令が終わったか。false なら、保存などで計算スレッドがふさがっている。
    時間切れを返した命令は取り消され、実行されない(executed=false)。受け付けるようになってから、もう一度呼ぶ。
    saving / activeTask: 保存の途中か。frame と waterFrame: 計算と水の処理のコマ番号(水が遅れると保存が止まる)。"""
    return call("/sim/health", timeout=15)


@tool()
def dialog() -> dict:
    """ゲームの画面に出ているダイアログ(破産の警告など、画面を止める窓)を返す。なければ dialog は null。
    texts は見出しと本文、buttons はボタンの文字。ボタンを押す道具はない(押すのは人)。
    seq は最後に開いたダイアログの連番。harmony は、開閉をゲームから直接知らされているか(false なら1秒ごとの見回り)。"""
    return call("/ui/dialog")


@tool()
def dialog_events(since: int = 0) -> dict:
    """連番 since より後に開いたダイアログを、閉じたものも含めて返す(最大50件)。
    openedAt と closedAt はゲーム内の日付。closedAt が null なら、まだ開いている。
    前回の city_info の dialogSeq を since に渡すと、その後に出たダイアログをすべて読める。"""
    return call("/ui/dialog/events", since=since)


@mcp.tool()
def explain(action: str, reason: str) -> dict:
    """判断を、ゲーム画面のパネルに出す。施策を打つ前に必ず呼ぶ。同じ行がログファイルにも残る。
    action: 何をするか。施策の名前と、どの公約のためか。例: "住宅地を作る(公約1)"
    reason: なぜするか。見た数字と予想。例: "住宅の需要が100で、住める場所が0。11月中旬に人口200人を見込む"
    見ている人に向けた短い説明なので、それぞれ80字以内にする。"""
    notify_note(action, reason)
    return {"ok": True}


@mcp.tool()
def set_panel_title(text: str = "") -> dict:
    """ゲーム画面のパネルの見出しを変える。どの市長が運営しているかを、録画に映すために使う(#92)。
    呼ぶのは親(人と話している Claude)だけ。市長のサブエージェントには渡さない。
    text: 見出し。例: "AI Mayor - Money / お金市長"。空にすると元の見出しに戻す。
    変えたことは、ログファイルにも TITLE の行で残る。"""
    return call("/ui/title", text=text or None)


@tool()
def save_log(save_to: str) -> dict:
    """ゲーム画面のパネルのログ(道具、判断、ダイアログ)を、テキストファイルに写す。
    save_to: 写し先の絶対パス(例: 日付フォルダの command-log.txt)。ログは街を開くたびに新しく始まる。"""
    r = call("/ui/log")
    if not r.get("ok") or not r.get("path"):
        return {"ok": False, "error": "ログファイルがない(街を開いていない、または書けなかった)"}
    import shutil
    os.makedirs(os.path.dirname(save_to), exist_ok=True)
    shutil.copyfile(r["path"], save_to)
    return {"ok": True, "from": r["path"], "to": save_to}


@tool()
def screenshot(view: str = "current", max_width: int = 1280, save_to: str | None = None) -> Image:
    """ゲームの画面写真を撮って返す。
    view: "current"(今の視点のまま) / "top"(真上から北を上にして、地図の中心付近を最大の引きで。地図全体は写らない) / "oblique"(北を向いた斜め45度)。
    max_width: 返す画像の幅の上限(画素)。小さいほど軽い。
    save_to: 同じ画像を JPEG で保存するファイルの絶対パス(例: 日付フォルダの assets/m1-town.jpg)。省くと保存しない。"""
    r = call("/screenshot", timeout=30, view=view)
    if not r.get("ok"):
        raise RuntimeError(r.get("error"))
    img = PILImage.open(r["path"]).convert("RGB")
    if img.width > max_width:
        img = img.resize((max_width, round(img.height * max_width / img.width)))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    if save_to:
        os.makedirs(os.path.dirname(save_to), exist_ok=True)
        with open(save_to, "wb") as f:
            f.write(buf.getvalue())
    return Image(data=buf.getvalue(), format="jpeg")


@tool()
def move_camera(x: float | None = None, z: float | None = None, size: float | None = None,
                pitch: float | None = None, yaw: float | None = None) -> dict:
    """カメラを動かし、動き終わってから実際の値を返す。省略した値は今のまま。
    x, z: 見る場所(ゲーム上のm。x が東、z が北)。size: 引きの大きさ(大きいほど広く見える)。
    pitch: 実際に見下ろす角度(90で真下)。yaw: 向き(0で北)。
    ゲーム本編では引きの上限が sizeMax(約4000)。引くほど浅い角度にできない(pitchMin。引き4000で約55度、2000で40度、1000で約26度)。
    届かない値は届く値に直し、notes に書く。戻り値の current が実際のカメラの値で、settled が false ならまだ動いている。
    current.offset は、指定した x, z と実際に見ている場所の差(m)。地図の端の近くでは、カメラが地図の外に出ないよう
    ゲームが見る場所をずらす。offset が大きいときは、size を小さくするか、端を背にする向き(yaw)にする。"""
    return call("/camera", x=x, z=z, size=size, pitch=pitch, yaw=yaw)


@tool()
def traffic(x: float | None = None, z: float | None = None, radius: float = 500, limit: int = 10) -> dict:
    """交通の詰まりを見る。詰まりは events にも complaints にも出ないので、これで確かめる。
    x, z, radius を渡すとその円の中だけ、省くと街全体。
    flow: 街全体の交通の流れ(%、交通の情報画面と同じ。低いほど詰まっている)。
    cars: 走っている車の数。blocked: 進めずに止まっている車。congestion: 渋滞の印が付いた車。
    averageDensity: 道路の区間の混み具合の平均(0〜100)。
    busiest: 混み具合が高い区間(segment、prefab、中点の x, z、density)。
    blockedSpots: 止まっている車が多い場所(200m四方ごとの車の位置の平均と台数)。道の上で止まった車だけを数える。
    blockedOnRoads と blockedInBuildings: 止まっている車(blocked)を、道の上と、駅・港などの建物の敷地の中に分けた数。
    busiest からは、地図の外とのつなぎ口の区間を外す。外した数は excludedOutside。"""
    return call("/traffic", timeout=30, x=x, z=z, radius=radius if x is not None else None, limit=limit)


@tool()
def net_near(x: float, z: float, radius: float = 200, service: str | None = None, limit: int = 50) -> dict:
    """円の中の線(道路・水道管・送電線など)の一覧。管や道路をつなぐ前に、既存の線の位置を確かめる。
    service: "Road" / "Water" / "Electricity" などで絞る。省くと全部。
    segments: 区間ごとに segment、prefab、service、start と end(点の番号 node と x, z)、length。
    length は区間の長さ(m)。道路は車線の曲線の長さで、交差点の角の分だけ両端の距離より短い。管と送電線は両端の距離。
    node が同じ区間どうしはつながっている。build_line の端をその点の座標に合わせると、そこにつながる。
    道路には carLanes(startToEnd / endToStart: その向きに車が走れる車線の数)。片方が0なら一方通行(高速道路など)。"""
    return call("/net/near", timeout=30, x=x, z=z, radius=radius, service=service, limit=limit)


@tool()
def net_reach(x: float | None = None, z: float | None = None, radius: float = 500, limit: int = 10) -> dict:
    """外の街から車で来られるかを確かめる。つなぎ口から道路を一方通行の向きどおりにたどる。
    x, z, radius を渡すとその円の中だけ、省くと街全体。
    roads: 道路の区間の数、つなぎ口から入れない数(notEnterable)、つなぎ口へ出られない数(notLeavable)。
    buildings: 建物の数、道路に面していない数(noRoad)、来られない数(notReachable)、出られない数(cannotLeave)。
    noRoad には、風力発電や給水塔など道路の要らない建物も入る。住宅・商業・工業が noRoad なら道路を確かめる。
    badBuildings / badSegments: 問題のある建物と区間(位置つき)。
    交差点で曲がれる向きは見ないので、ゲームより甘い。ここで問題があれば、ゲームでも来られない。
    建ち途中の建物、壊れた建物、道路の要らない建物は判定から外し、buildings.skipped に数える。"""
    return call("/net/reach", timeout=60, x=x, z=z, radius=radius if x is not None else None, limit=limit)


# 区画の地図の色(区画の種類ごと)。建物が建ったマスは濃く、空いたマスは薄く塗る
ZONE_COLORS = {
    "RL": ((60, 170, 60), (170, 225, 170)), "RH": ((20, 110, 20), (130, 190, 130)),
    "CL": ((50, 110, 220), (170, 195, 245)), "CH": ((20, 50, 160), (130, 150, 215)),
    "I": ((215, 170, 20), (245, 225, 150)), "O": ((20, 170, 190), (150, 220, 230)),
    "U": ((205, 205, 205), (232, 232, 232)),
}
LINE_STYLES = {"Road": ((70, 70, 70), 3), "Water": ((30, 120, 255), 1), "Electricity": ((255, 120, 0), 1)}


@tool()
def zone_map(x: float, z: float, radius: float = 500, size: int = 900, save_to: str | None = None) -> Image:
    """区画を色分けした地図を、真上から北を上にして描いて返す。画面写真には区画の色が出ないので、これで見る。
    x, z: 地図の中心。radius: 中心から端までの距離(m、50〜2000)。size: 画像の一辺(画素)。
    区画の色: 低密度住宅=緑、高密度住宅=濃い緑、低密度商業=青、高密度商業=紺、工業=黄、オフィス=水色、
    未指定(区画にできるマス)=灰。建物が建ったマスは濃く、空いたマスは薄い。
    線: 道路=濃い灰(太い)、水道管=青、送電線=橙。建物=黒い枠。電気・水・下水のうち、要るのに来ていない建物は赤い枠(風車の水など、要らないものは見ない)。
    100mごとに細い格子線と座標の数字を描く。
    save_to: 同じ画像を JPEG で保存するファイルの絶対パス。省くと保存しない。"""
    d = call("/map/data", timeout=60, x=x, z=z, radius=radius)
    if not d.get("ok"):
        raise RuntimeError(d.get("error"))
    r = d["radius"]
    cx, cz = d["x"], d["z"]
    scale = size / (2 * r)

    def px(wx, wz):
        return ((wx - cx + r) * scale, (cz - wz + r) * scale)

    img = PILImage.new("RGB", (size, size), (250, 250, 245))
    draw = ImageDraw.Draw(img)

    # 100mごとの格子と座標
    step = 100 if r <= 1000 else 500
    for g in range(int((cx - r) // step) * step, int(cx + r) + step, step):
        gx, _ = px(g, cz)
        draw.line([(gx, 0), (gx, size)], fill=(225, 225, 225))
        draw.text((gx + 2, 2), str(g), fill=(150, 150, 150))
    for g in range(int((cz - r) // step) * step, int(cz + r) + step, step):
        _, gz = px(cx, g)
        draw.line([(0, gz), (size, gz)], fill=(225, 225, 225))
        draw.text((2, gz + 2), str(g), fill=(150, 150, 150))

    half = 4 * scale
    for cxw, czw, code, occupied in d["cells"]:
        color = ZONE_COLORS.get(code, ZONE_COLORS["U"])[0 if occupied else 1]
        p = px(cxw, czw)
        draw.rectangle([p[0] - half, p[1] - half, p[0] + half, p[1] + half], fill=color)

    # 道路 → 水道管 → 送電線の順に描く。道路に沿った管が、後から描く太い道路に塗りつぶされないように(#82)
    for ax, az, mx, mz, bx, bz, service, raised in sorted(d["lines"], key=lambda l: {"Road": 0, "Water": 1, "Electricity": 2}.get(l[6], 0)):
        color, width = LINE_STYLES.get(service, ((150, 150, 150), 1))
        if service == "Road":
            width = max(2, round(8 * scale))
        draw.line([px(ax, az), px(mx, mz), px(bx, bz)], fill=color, width=width)

    for bxw, bzw, w, l, angle, service, e, wtr, sew in d["buildings"]:
        cos, sin = math.cos(angle), math.sin(angle)
        corners = []
        for rx, fz in ((-w / 2, -l / 2), (w / 2, -l / 2), (w / 2, l / 2), (-w / 2, l / 2)):
            corners.append(px(bxw + rx * cos - fz * sin, bzw + rx * sin + fz * cos))
        ok = e and wtr and sew
        draw.polygon(corners, outline=(0, 0, 0) if ok else (230, 0, 0), width=1 if ok else 3)

    # 凡例
    legend = [("RL", "res low"), ("RH", "res high"), ("CL", "com low"), ("CH", "com high"), ("I", "industry"),
              ("O", "office"), ("U", "unzoned")]
    for i, (code, label) in enumerate(legend):
        y = size - 14 * (len(legend) - i) - 4
        draw.rectangle([4, y, 14, y + 10], fill=ZONE_COLORS[code][0])
        draw.text((18, y - 1), label, fill=(40, 40, 40))
    draw.text((size - 60, 4), "N up", fill=(40, 40, 40))

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    if save_to:
        os.makedirs(os.path.dirname(save_to), exist_ok=True)
        with open(save_to, "wb") as f:
            f.write(buf.getvalue())
    return Image(data=buf.getvalue(), format="jpeg")


@tool()
def height_at(x: float, z: float) -> dict:
    """指定した場所の地面の高さと、水面を含めた高さを返す(ゲーム上のm。海面は約40m)。"""
    return call("/height", x=x, z=z)


# 福岡のマップの中心(天神駅と博多駅の中間)と縮尺(ゲーム上の1m = 実寸2m)
CENTER = (33.59018, 130.40987)
SCALE = 2.0
R = 6371008.8
GIF_DIR = os.path.expanduser("~/Library/Application Support/Colossal Order/Cities_Skylines/AIMayor/gifs")


@tool()
def unlock_all_areas() -> dict:
    """地図のすべての区画を、お金をかけずに街のものにする。新しい街を始めたら最初に1回呼ぶ。
    実際の市長には区画を買い足すという判断がないため(#70 で決定)。
    ゲームは持っている区画の隣しか解放できないので、増えなくなるまで繰り返す。"""
    first = last = None
    for _ in range(20):
        r = call("/areas/unlock_all", timeout=30)
        if not r.get("ok"):
            return r
        first = first if first is not None else r["before"]
        if last is not None and r["after"] == last:
            break
        last = r["after"]
    return {"ok": True, "before": first, "after": last}


@tool()
def latlon_to_game(lat: float, lon: float) -> dict:
    """緯度経度を、福岡のマップのゲーム上の座標(x が東、z が北、m)に直す。水平1/2縮尺。"""
    import math
    north = math.radians(lat - CENTER[0]) * R
    east = math.radians(lon - CENTER[1]) * R * math.cos(math.radians(lat))
    return {"x": round(east / SCALE, 1), "z": round(north / SCALE, 1)}


@tool()
def list_net_types(service: str | None = None, locked: bool = True) -> dict:
    """引ける線の種類(道路、線路、高速道路など)の名前の一覧。service で絞れる(例: "Road", "PublicTransport")。
    costPerKm: 1kmあたりの建設費(地面の上。高架やトンネルは高くなる)。
    upkeepPerWeekPerKm: 1kmあたりの週の維持費(週の支出と同じ単位、予算100%のとき)。
    既定では、解禁前の線も unlocked=false と解禁の条件(unlock)つきで返す。locked=False で解禁された線だけにする。
    解禁前の線は、条件を満たすと引けるようになる。例: 線路(Train Track)は、駅か貨物駅を1つ建てると解禁される(#100)。
    地下鉄の線路は、手で置く種類でなくても出す(subService=PublicTransportMetro、placement、hasTunnel つき。#107)。
    名前に Bus Lane / Bus lane / Bus Only のある道路は、バスなど一部の車(緊急車など)だけが通れる車線を持つ(ふつうの車とトラックは使えない)。"""
    r = call("/net/prefabs", locked="true" if locked else None)
    if service and r.get("ok"):
        r["prefabs"] = [p for p in r["prefabs"] if p.get("service") == service]
    return r


@tool()
def build_line(prefab: str, points: list[list[float]], frames: int = 0, gif_name: str | None = None,
               pay: bool = True, follow: bool = False, size: float = 2500, demolish: bool = False,
               y: float | None = None) -> dict:
    """座標の並び [[x, z], ...] に沿って、線(道路・線路など)を引く。
    道路と水道管は、線の途中で交わる既存の地上の道路・管にも交差点を作る(戻り値の crossings。一般道は高速道路の本線とは交差点を作らない)。
    端点の12m以内に同じサービスの点があれば、そこにつなぐ。点がなく16m以内に区間があれば、その区間を途中で分けて
    交差点を作り、つなぐ(既存の道路の途中に突き当てられる)。
    prefab: 種類の名前(例: "Train Track", "Highway", "Basic Road")。list_net_types で調べる。
    frames: 1以上なら、線をその数の区間に分けて順に引き、区間ごとに今の視点で画面写真を撮って GIF にまとめる。
    一方通行の道(高速道路など)は、並びの順が進む向きになる。
    川や海を渡る区間は、自動で橋の種類(例: "Basic Road Bridge")になり、水面より3m以上高く架ける。戻り値の bridgeSegments が橋の区間の数。
    点を [x, z, 地面からの高さ(m)] にすると、高さ0.5mを超える点は高架の種類(例: "Highway Elevated")で、その高さに引く。
    高架の区間では、水の上の点を外して川を1区間でまたぐ(水の中に橋脚を立てないため)。
    pay: True(既定)なら、ゲームの道具と同じく建設費を予算から差し引く。足りなければ建てずに断る。
    人が置く骨格(#69)だけ False にする。
    follow: True なら、区間を引くたびにカメラをその区間の先端へ動かしてから撮る(長い線を追いかけて撮る)。
    size: follow のときのカメラの引き。
    戻り値の snapped(既存の点につないだ数)と split(既存の区間を分けてつないだ数)が両方0なら、新しい線はどこにもつながっていない。
    高速道路は上り・下りが別の線なので、間の中央分離帯に端を置くとつながらない。net_near で車線の位置を確かめてから引く。
    ends: 始点と終点が何につながったか。connectedTo は "node"(既存の点)/ "split"(既存の区間を分けた)/ "none"。
    building は、端が建物の管のつなぎ口につながったときの建物の id(なければ 0)。
    insideBuilding は、端が敷地の中にある建物の id。送電線は端が建物の敷地に入れば電気が通る。
    net は、端がつながった線の種類。一般道の端が高速道路の本線につながると warning が付く(つなぐのは止めない)。
    道路・線路が建物の敷地に重なるときは、建てずに断り、overlaps に重なる建物(id、種類、位置)を返す。
    重なった建物はゲームが取り壊す。壊してよければ demolish=True で引く。成功したときも overlaps を返す。
    ゲームの線を引く道具と同じく、取り除けない相手(交差点の近くの別の道路、サービスの建物など)にぶつかる線は引かずに断る。
    そのとき atSegment(ぶつかった区間の両端)と colliding(ぶつかった区間と建物。blocks=true が断る相手)を返す。
    gameCheck: ゲームの道具なら出るそのほかの注意(TooShort など)。引くことは引く。
    点を [x, z, −深さ] にすると、地下にその深さ(8mより浅いと9m)で引く。両端が地下の区間はトンネル、片方だけの区間は坂
    (地上への出入り口)になる。トンネルの種類がない線(管・送電線など)は断る。地下の端は地下の点(地下鉄の駅の乗り場の線路の端を含む)
    にだけつなぐ。地下の区間は地面の建物と重ならない。戻り値の undergroundSegments が地下と坂の区間の数。
    y: 点の高さを固定するとき(m)。地面の高さの代わりにこの高さで引き、橋・高架・トンネルにはしない。
    船の航路(Ship Path)を水面(約40m)に引くときに使う(#100)。省くと地面の高さ。
    解禁前の線は断る。"""
    if len(points) < 2:
        return {"ok": False, "error": "points は2点以上"}
    if frames <= 0:
        return call("/net/build", timeout=60, body=";".join(",".join(str(v) for v in p) for p in points), prefab=prefab,
                    pay=str(pay).lower(), demolish="true" if demolish else None, y=y)

    # 区間の長さがそろうように、点の並びを frames 個に分ける(区間どうしは端点を共有する)
    import math
    acc = [0.0]
    for (x0, z0), (x1, z1) in zip(points, points[1:]):
        acc.append(acc[-1] + math.hypot(x1 - x0, z1 - z0))
    total = acc[-1]
    cuts = [0]
    for k in range(1, frames):
        target = total * k / frames
        i = min(range(1, len(points)), key=lambda j: abs(acc[j] - target))
        if i > cuts[-1] and i < len(points) - 1:
            cuts.append(i)
    cuts.append(len(points) - 1)

    import time

    def aim(x, z):
        if follow:
            call("/camera", x=x, z=z, size=size, pitch=60, yaw=0)
            time.sleep(3)  # カメラが動き終わるのを待つ

    shots, results = [], []
    aim(*points[0])
    first = call("/screenshot", timeout=30)
    if first.get("ok"):
        shots.append(first["path"])
    for a, b in zip(cuts, cuts[1:]):
        part = points[a:b + 1]
        r = call("/net/build", timeout=60, body=";".join(",".join(str(v) for v in p) for p in part), prefab=prefab,
                 pay=str(pay).lower(), demolish="true" if demolish else None, y=y)
        results.append(r)
        if not r.get("ok"):
            break
        aim(*part[-1])
        s = call("/screenshot", timeout=30)
        if s.get("ok"):
            shots.append(s["path"])

    gif = None
    if len(shots) >= 2:
        os.makedirs(GIF_DIR, exist_ok=True)
        gif = os.path.join(GIF_DIR, (gif_name or prefab.replace(" ", "_")) + ".gif")
        imgs = []
        for p in shots:
            im = PILImage.open(p).convert("RGB")
            im = im.resize((960, round(im.height * 960 / im.width)))
            imgs.append(im.convert("P", palette=PILImage.ADAPTIVE, colors=256))
        imgs[0].save(gif, save_all=True, append_images=imgs[1:] + [imgs[-1]] * 3, duration=600, loop=0)
    return {"ok": all(r.get("ok") for r in results), "parts": results, "frames": len(shots), "gif": gif}


@tool()
def remove_line(points: list[list[float]], prefab: str | None = None, tolerance: float = 20) -> dict:
    """座標の並び [[x, z], ...](線)に沿った区間を消す。区間の両端が線から tolerance(m)以内のものが対象。
    prefab を指定すると、その種類だけを消す(例: "Train Track")。省くと種類を問わない。"""
    return call("/net/remove", timeout=60, body=";".join(f"{x},{z}" for x, z in points),
                prefab=prefab, tolerance=tolerance)


@tool()
def upgrade_road(prefab: str, points: list[list[float]], tolerance: float = 20, pay: bool = True,
                 demolish: bool = False) -> dict:
    """道路を別の種類に差し替える(例: "Basic Road" → "Medium Road"、"Large Road")。ゲームの道路の道具の「アップグレード」と同じ。
    points: [[x, z], ...] の線。両端の点が両方とも線から tolerance(m)以内にある道路の区間を差し替える。
    区画の指定と沿道の建物は保たれる。太くした道路の下になったマスは消える。
    太くした道路の下になる区画の建物は、ゲームが壊す。
    既定(demolish=False)では、そうなる区間は差し替えずに飛ばし、skipped に壊れる建物の番号と名前を返す。
    demolish=True なら差し替え、壊れた建物を demolishedBuildings に返す。
    サービスの建物(病院、学校など)や別の道にぶつかる区間は、ゲームが断るので飛ばす(ぶつかった区画の建物があれば、demolish=True で壊してやり直す)。
    同じ幅の種類(Basic Road → Small 4 Lane Road など)への差し替えでは、沿道の建物は壊れない。
    壊す前に preview_bulldoze で、失う家と席を見積もる。
    橋・高架・トンネルの区間は、ゲームが高さに合う種類を選ぶ。費用は新旧の建設費の差。足りなければその区間を飛ばす。
    戻り値: matched(選んだ区間の数)、upgraded(差し替えた数)、skipped(飛ばした区間と理由)、cost。
    ぶつかって断られた区間(reason に ObjectCollision)には colliding を付ける。ゲームの道具の画面で赤く塗られる相手と同じ。
    colliding.segments(区間の番号、種類、中ほどの位置)と colliding.buildings(建物の番号、種類、位置)。
    blocks=true の相手があると断られる。blocks=false の相手は、作るときにゲームが取り除く。
    一方通行の道路に差し替えると向きは元の区間のまま。逆にするときは reverse_road を使う。"""
    return call("/net/upgrade", timeout=60, body=";".join(f"{x},{z}" for x, z in points), prefab=prefab,
                tolerance=tolerance, pay=str(pay).lower(), demolish=str(demolish).lower())


@tool()
def reverse_road(points: list[list[float]], tolerance: float = 20) -> dict:
    """一方通行の道路の向きを逆にする(種類は変えない)。ゲームの道路の道具の右クリックと同じ。両方向の道路は飛ばす(skipped)。
    points と tolerance は upgrade_road と同じ。"""
    return call("/net/reverse", timeout=60, body=";".join(f"{x},{z}" for x, z in points), tolerance=tolerance)


@tool()
def test_upgrade_road(prefab: str, points: list[list[float]], tolerance: float = 20, demolish: bool = False) -> dict:
    """upgrade_road を試すだけ。街は変えず、お金も払わない。ゲームの道具で、クリックする前に赤く出るかを見るのと同じ。
    引数と戻り値は upgrade_road と同じで、test=true、changed=false が付く。upgraded は差し替えられる区間の数。
    断られる区間は skipped に理由と colliding(ぶつかった相手。blocks=true が断る相手)を返す。
    demolish=True なら、区画の建物が壊れる区間も差し替えられる数に入れ、壊れる建物を demolishedBuildings に返す(壊さない)。"""
    return call("/net/upgrade", timeout=60, body=";".join(f"{x},{z}" for x, z in points), prefab=prefab,
                tolerance=tolerance, pay="true", demolish=str(demolish).lower(), test="true")


@tool()
def test_build_line(prefab: str, points: list[list[float]], demolish: bool = False) -> dict:
    """build_line を試すだけ。街は変えず、お金も払わない。ゲームの道具で、引く前に赤く出るかを見るのと同じ。
    points と demolish は build_line と同じ。引けるなら ok=true、test=true、built=false と、
    区間の数(segments)、交差点の数(crossings)、橋・地下の区間の数、費用(cost)、足りるか(enoughMoney)、
    重なる建物(overlaps)、ゲームのそのほかの注意(gameCheck)を返す。
    断られるなら、build_line と同じ形(ok=false、atSegment、colliding、または overlaps)で返す。"""
    if len(points) < 2:
        return {"ok": False, "error": "points は2点以上"}
    return call("/net/build", timeout=60, body=";".join(",".join(str(v) for v in p) for p in points), prefab=prefab,
                pay="true", demolish="true" if demolish else None, test="true")


@tool()
def test_place_building(prefab: str, x: float, z: float, angle: float = 0, facing: str | None = None) -> dict:
    """place_building を試すだけ。街は変えず、お金も払わない。ゲームの道具で、置く前に赤く出るかを見るのと同じ。
    引数は place_building と同じ。置けるなら ok=true、test=true、placed=false と、ゲームが直した位置(x, z)と向き(angleUsed)、
    費用(cost)、足りるか(enoughMoney)、入口(entrance。入口から16m以内の道路 road、なければ null)、
    電気・水・下水が要るか(needs)、取り壊される区画の建物(wouldDemolish)を返す。
    置けないなら、place_building と同じ形(ok=false、reasons、colliding)で返す。"""
    return call("/building/place", prefab=prefab, x=x, z=z, angle=angle, pay="true", facing=facing, test="true")


@tool()
def create_transport_line(type: str, stops: list[list[float]]) -> dict:
    """公共交通の路線を作る。type は bus / metro / train / ship / plane。
    stops は停留所・駅の位置 [[x, z], ...] の並び(2つ以上)で、最後のあと最初の停留所に戻って環状になる。
    バスは各点から64m以内で最も近い道路の区間に停留所を置く。地下鉄・鉄道・船・飛行機は、各点から300m以内で
    最も近いその種類の駅の乗り場を使う(駅は先に place_building で置く)。
    バスの路線は、先にバスの車庫(Bus Depot)を建てないと作れない(ゲームの決まり。地下鉄・鉄道も駅が要る)。
    どれか1つでも置けなければ、路線を作らずに断る(index に置けなかった停留所)。建設費はかからない。
    台数はゲームが決める。道順は数日かけて計算されるので、
    後で list_transport_lines の pathFailed を確かめる。
    バスの停留所は、点に最も近い車線に置かれ、進む向きは見ない。この街は右側通行なので、東へ進む区間は道の南側、
    西へ進む区間は北側に点を置く(北へ進む区間は東側、南へ進む区間は西側)。
    逆の側に置くと、隣の停留所まで遠回りする。"""
    return call("/transport/line/create", timeout=60, body=";".join(f"{x},{z}" for x, z in stops), type=type)


@tool()
def list_transport_lines(type: str | None = None, number: int | None = None, name: str | None = None) -> dict:
    """公共交通の路線の一覧。number は画面の路線の番号、stops は停留所の数、vehicles は今走っている台数、
    targetVehicles はゲームが目指す台数、budget は路線の台数の割合(%)、passengers は乗客(住民と観光客の平均)、
    lengthKm は長さ。complete は環状に閉じたか。pathFailed が1以上なら、停留所の間に道順が見つからない区間がある
    (道がつながっていない、一方通行など)。
    絞り込み(#107): type(bus など)、number(画面の路線の番号)、name(路線の名前の一部。大文字と小文字は問わない)。
    name は路線の名前、ticketPrice は運賃。passengersLastPeriod は前の集計期間の乗客(住民と観光客)。
    fareIncomeEstimate は運賃の収入の見積もり(passengersLastPeriod × ticketPrice)。economy_breakdown の
    PublicTransport の収入と比べて、どの路線が稼いでいるかを見る。"""
    return call("/transport/lines", type=type, number=number, name=name)


@tool()
def transport_depots(type: str | None = None) -> dict:
    """車庫ごとの台数の余裕。type は bus など(省くと全部)。
    vehicles は車庫が今出している車の数、maxVehicles は今出せる上限(上限のない車庫は -1)。
    active は車庫が動いているか。"""
    return call("/transport/depots", type=type)


@tool()
def transport_line(line: int) -> dict:
    """路線を1本詳しく見る。停留所ごとの位置と、次の停留所までの道順の長さ(pathM)、直線の距離(straightM)、
    遠回りの度合い(detour = pathM ÷ straightM)。detour の大きい区間が遠回りしている所。
    道順が見つかる前は、ゲームが直線の距離を入れておく。"""
    return call("/transport/line", line=line)


@tool()
def remove_transport_line(line: int) -> dict:
    """路線を消す。line は list_transport_lines の line(画面の番号 number ではない)。"""
    return call("/transport/line/remove", line=line)


@tool()
def set_transport_line_budget(line: int, percent: int) -> dict:
    """路線ごとの台数の割合を変える(10〜300%)。"""
    return call("/transport/line/budget", line=line, percent=percent)


@tool()
def list_districts() -> dict:
    """地区の一覧。番号、名前、中心のおおよその位置、塗ったマスの数、人口、かかっている政策と特化。"""
    return call("/districts")


@tool()
def paint_district(x: float, z: float, radius: float = 150, name: str | None = None, erase: bool = False) -> dict:
    """円の中を地区に塗る。name の地区がなければ作る。erase=True で塗りを消す。
    地区には政策や産業の特化をかけられる(set_district_policy)。cells は地区のマスの数(1マス19.2m四方)。"""
    return call("/district/paint", x=x, z=z, radius=radius, name=name, erase="true" if erase else None)


@tool()
def set_district_policy(district: str, name: str, active: bool = True) -> dict:
    """地区だけに政策をかける。district は番号か名前。name は list_policies の名前、または産業の特化
    (Forest / Farming / Oil / Ore。工業の区画が資源の産業になる。地面の資源が要る)。税の政策(TaxRaise / TaxLower)も地区にかけられる。
    特化は同じ組で1つだけ。解禁前やDLCのない政策は断る。"""
    return call("/district/policy", district=district, name=name, active=str(active).lower())


@tool()
def rename_district(district: str, name: str) -> dict:
    """地区の名前を付け替える。district は番号か名前。"""
    return call("/district/rename", district=district, name=name)


@tool()
def list_loans() -> dict:
    """融資の枠(3つ)ごとに、借りられる額・利率・週数・週の返済と、今の借入の残り。枠ごとに解禁の節目が違う。"""
    return call("/economy/loans")


@tool()
def take_loan(index: int) -> dict:
    """銀行の申し出どおりに借りる。返済は毎週、自動で支出に入る。"""
    return call("/economy/loan/take", index=index)


@tool()
def repay_loan(index: int) -> dict:
    """融資の残りを今すぐ返す。お金が足りなければ断る。"""
    return call("/economy/loan/repay", index=index)


@tool()
def set_building_active(id: int, active: bool) -> dict:
    """サービスの建物を止める・動かす。止めると維持費と働き手が0になり、サービスもしない。"""
    return call("/building/toggle", id=id, active=str(active).lower())


@tool()
def empty_building(id: int, active: bool = True) -> dict:
    """満ちた埋立地や墓地を空にする。中身はほかの同じ種類の施設へ運ばれる。空にしている間は受け入れない。
    終わったら active=False で戻す。"""
    return call("/building/empty", id=id, active=str(active).lower())


@tool()
def set_historical(id: int, active: bool = True) -> dict:
    """区画の建物を歴史的建造物にする。レベルが上がらず建て替わらない。"""
    return call("/building/historical", id=id, active=str(active).lower())


@tool()
def junction_info(x: float, z: float) -> dict:
    """点 (x, z) に近い(40m以内)道路の交差点の様子。trafficLights: 信号があるか。customLights: 人が決めた信号か
    (false ならゲームが自動で決めた)。canEnableLights: 信号を付けられるか。canSetYield: 譲れの標識を付けられるか。
    roads: 交差点に入る区間ごとに segment、種類、向き(bearing。北0・東90)、車が通るか(cars)、譲れの標識があるか(yield)。"""
    return call("/junction", x=x, z=z)


@tool()
def set_traffic_lights(x: float, z: float, active: bool) -> dict:
    """交差点の信号を付ける(active=True)・外す(False)。ゲームの交通の情報画面の「交差点」のボタンと同じ。
    道路と線路が交わる交差点などは付けられない(junction_info の canEnableLights)。"""
    return call("/junction/lights", x=x, z=z, active=str(active).lower())


@tool()
def set_yield_sign(x: float, z: float, segment: int, active: bool = True) -> dict:
    """交差点に入る区間(segment は junction_info の roads の segment)に「譲れ」の標識を付ける・外す。
    標識のある側の車は、ほかの道の車に譲ってから入る。信号のある交差点には付けられない(先に set_traffic_lights で外す)。"""
    return call("/junction/stop", x=x, z=z, segment=segment, active=str(active).lower())


@tool()
def list_trees() -> dict:
    """植えられる木の種類と1本の費用。unlocked は景観の機能が解禁されているか。"""
    return call("/trees/prefabs")


@tool()
def plant_trees(polygon: list[list[float]], prefab: str | None = None, spacing: float = 12, pay: bool = True) -> dict:
    """多角形 [[x, z], ...] の中に、spacing(m)おきに少しずらして木を植える。1本ごとに建設費を払う。
    建物・道路・水の上には植えない(blocked)。お金が尽きたら止まる。"""
    return call("/trees/plant", timeout=60, body=_poly(polygon), prefab=prefab, spacing=spacing, pay=str(pay).lower())


@tool()
def remove_trees(polygon: list[list[float]]) -> dict:
    """多角形の中の木を取り除く。払い戻しはない。"""
    return call("/trees/remove", timeout=60, body=_poly(polygon))


@tool()
def trade() -> dict:
    """輸出と輸入の量(週。ゲームの外部接続の情報画面と同じ)と、つなぎ口(道路・鉄道・船・飛行機)ごとに今出入りしている
    荷物の車の数。工業の荷物が外へ出ているか、燃料などを輸入に頼っていないかを見る。"""
    return call("/trade")


@tool()
def terrain_dirt() -> dict:
    """地形を変えるための土の蓄え(m³)と1m³の値段。"""
    return call("/terrain/dirt")


@tool()
def level_terrain(polygon: list[list[float]], height: float, pay: bool = True) -> dict:
    """多角形の中の地形を、その高さ(m)にならす。ゲームの景観の道具と同じく、元の地形との差が広がる分に土の値段を払い、
    縮めば払い戻す。盛るには土の蓄えが要り、削ると蓄えに入る。足りなければ何も変えずに断る。
    建物・道路・線路の下と、持っていない区画は変えない(skipped*)。低い土地を盛って浸水を防ぐのに使う。"""
    return call("/terrain/level", timeout=60, body=_poly(polygon), height=height, pay=str(pay).lower())


@tool()
def raise_terrain(polygon: list[list[float]], amount: float, pay: bool = True) -> dict:
    """多角形の中の地形を amount(m)上げる。費用と制限は level_terrain と同じ。"""
    return call("/terrain/raise", timeout=60, body=_poly(polygon), amount=amount, pay=str(pay).lower())


@tool()
def lower_terrain(polygon: list[list[float]], amount: float, pay: bool = True) -> dict:
    """多角形の中の地形を amount(m)下げる。費用と制限は level_terrain と同じ。"""
    return call("/terrain/lower", timeout=60, body=_poly(polygon), amount=amount, pay=str(pay).lower())


@tool()
def bulldoze(x: float, z: float, radius: float = 50, what: str = "all") -> dict:
    """中心 (x, z) から半径 radius(m)の円の中を取り壊す。
    what: "all"(道路・線路と建物) / "net"(道路・線路だけ) / "building"(建物だけ)。取り壊しの払い戻しはない。
    buildings: 壊した建物の id と種類(最大50件)。
    what="abandoned" で、円の中の放棄された建物と、壊れた・焼けた建物(区画の建物だけ)を取り壊す。サービスの建物と道路は残す。
    放棄された建物をまとめて片づけるのに使う。"""
    return call("/bulldoze", timeout=60, x=x, z=z, radius=radius, what=what)


@tool()
def water_trace(x: float, z: float) -> dict:
    """下水や水が来ない建物の原因を探す。点 (x, z) に近い建物(100m以内)の電気・水・下水の様子(grid)と、
    近く(半径200m)の水道管の網ごとに、取水口・給水塔(intakes)と排水口(outlets)につながっているかを返す。
    outlets が空の網に建物がつながっていれば、下水が流れない。intakes が空なら、水が来ない。
    網がつながっているかだけを見て、水の量や圧は見ない。
    100m以内に建物がなければ、点そのもので調べる(building は null)。建物のまだない新しい街区で、管の網がつながったか、
    そのマスに水・下水が届いているかを確かめる。
    cell は、その家のマスに今、水・下水が届いているか。waterPollution はそのマスの水の汚れ(0で汚れなし)。
    city は街全体の水と下水の容量(capacity)と使用量(used)。"""
    return call("/net/water_trace", timeout=30, x=x, z=z)


@tool()
def demand_breakdown() -> dict:
    """街全体の働き口と家の数、失業と家のない人の数を返す。
    jobs と emptyJobs は働き口の総数と空き、homes と emptyHomes は家の総数と空き。
    unemployed は働き口を探している人、homeless は家のない人の数。citizens_summary の unemployed とは数え方が違う。
    byEducation: 学歴(uneducated / elementary / highSchool / university)ごとの unemployed、eligibleWorkers(働ける人)、homeless。
    residential と workplace の欄は、AIMAYOR_MODE=grow のときだけ返す。"""
    r = call("/demand")
    if MODE == "main" and r.get("ok"):
        # 本番では、需要の式の項(base、jobTerm、homeTerm、切る前の値、target)を返さない。働き口・失業・家の数だけ残す(#108)
        r.pop("residential", None)
        r.pop("workplace", None)
    return r


@tool()
def building_stats(x: float | None = None, z: float | None = None, radius: float = 500) -> dict:
    """区画の建物を種類(subService)ごとに数える。x を省くと街全体。
    levels: レベル1〜5の棟数。homes と jobs: 家族と働き口の数。averageLandValue: 建物の場所の地価の平均。
    atMaxLevel: 最上位のレベル(住宅5、ほかは3)の棟数。
    levelUp の欄は、AIMAYOR_MODE=grow のときだけ返す。"""
    r = call("/buildings/stats", timeout=30, x=x, z=z, radius=radius if x is not None else None)
    if MODE == "main" and r.get("ok"):
        # 本番では、レベルが上がらない理由(ゲームの判定の中身)を返さない。最上位の棟数だけ残す(#108)
        for g in r.get("groups", []):
            lu = g.pop("levelUp", None) or {}
            if "atMaxLevel" in lu:
                g["atMaxLevel"] = lu["atMaxLevel"]
    return r


@tool()
def building_levelup(id: int) -> dict:
    """AIMAYOR_MODE=grow のときだけ出す道具(本番の main では出さない)。
    区画の建物1棟の、レベル上げの中身(ゲームの CheckBuildingLevel と同じ計算)。progress は2つの条件の進み具合(0〜15。15で満たした)。
    ゲームは2つがそろっても、問題の印(problems)があるか、同じ大きさの上のレベルの建物がない(upgradeModelExists=false)と建て替えない。
    blockers に上がらない理由。工業・オフィスは services に点数(value)と次のレベルに要る点(オフィス45/90、工業30/60)と、
    項目ごとの点(terms: 公共交通、警察、医療、消防、教育、娯楽などは足す、騒音・放棄・地面の汚染は引く)。mostMissing がいちばん伸ばせる項目。
    住宅・商業は landValue と landValueForLevel(次のレベルに要る地価)。
    商業・工業・オフィスは workers に、働き手の学歴の内訳(byEducation)と、働き口の学歴の段ごとの数(jobsByEducation)、
    ゲームの学歴の点(educationScore。工業・オフィスは15でL2、30でL3)を返す(#107)。"""
    return call("/buildings/levelup", id=id)


@tool()
def cargo() -> dict:
    """品物と原料の流れ。荷物の車を、運ぶもの(Goods、Oil、Ore、Logs、Grain など)と向き(import / export / local)ごとに数え、
    止まっている台数と、止まっている場所の上位(stoppedSpots)を返す。stations は荷物の駅・港(Cargo Harbor を含む)ごとの出入りの台数。
    shortages は品物が届かない店(noGoods)と原料が届かない工場(noResources)の数と多い場所。港や駅を足す前後で比べて効き目を見る。
    stoppedOnRoads と stoppedInBuildings: 止まっているトラックを、道の上と、駅・港などの建物の敷地の中に分けた数。
    stoppedSpots は道の上だけ。stoppedInBuildingsTop は、敷地の中で止まったトラックが多い建物の上位5つ(建物の番号、名前、位置、台数)。"""
    return call("/cargo", timeout=30)


@tool()
def vehicles_stuck(kind: str = "truck", building: int | None = None, limit: int = 30) -> dict:
    """止まった車を1台ずつ見る(#107)。kind は truck(荷物のトラック)/ train(貨物列車)/ ship(貨物船)/ hearse(霊柩車)/ garbage(ごみ収集車)/ bus(バス)。
    bus は、samples に路線(line と画面の番号 lineNumber)と次の停留所(nextStop: 点の番号、位置、距離)を返し、amount は乗っている客の数。
    byTarget は路線ごとの台数になる。停留所で客を乗せているバスは Stopped の印が付く。
    truck・hearse・garbage・bus は、止まっているか、駅・港・施設などの敷地の中にいる車だけを数える(走っている車は数えない)。
    train・ship は台数が少ないので、走っているものも含めて先頭の車両を全部返す。samples に車両の数(cars)と積んでいる荷物の数(cargoLoads)も返す。
    building を渡すと、その建物の敷地の中にいるか、その建物を出発・行き先にする車だけにする(例: 貨物駅や火葬場の番号)。
    byState: 状態ごとの台数。状態は印をつないだ文字列(WaitingPath=道順の計算待ち、WaitingTarget=行き先の決まり待ち、
    WaitingCargo=荷物待ち、WaitingSpace=空き待ち、Congestion=渋滞、Stopped、GoingBack=戻る途中、Importing/Exporting、
    InGrounds=敷地の中、OnRoad=道の上、Blocked=進めずに止まっている)。
    byPath: 道順の状態ごとの台数(none=道順がない、queued/calculating=計算待ち、ready=できた、failed=見つからなかった)。
    bySeenStopped: この道具で最初に止まっているのを見てからの長さごとの台数。初めて呼んだときは全部 <1day。数日後にもう一度呼ぶと、
    止まり続けている車が分かる(ゲームを起動し直すと、見た記録は消える)。byTarget: 行き先の建物ごとの台数(vehicles)の上位10。
    samples: 1台ずつの中身(状態、道順、荷物の種類と量、止まって見えている日数、位置、出発と行き先の建物、行き先までの距離)を limit 台まで。"""
    return call("/vehicles/stuck", timeout=30, kind=kind, building=building, limit=limit)


@tool()
def land_value(x: float | None = None, z: float | None = None, radius: float = 500) -> dict:
    """地価(ゲームの地価の情報画面と同じ値)。x を省くと街の平均(cityAverage)。
    x, z, radius を渡すと、円を囲む四角を9×9の点で測り、average、min、max と grid(北の行から、西から東へ)を返す。"""
    return call("/landvalue", x=x, z=z, radius=radius if x is not None else None)


@tool()
def new_buildings(since: int = 0) -> dict:
    """since より後に建った区画の建物を、種類(subService)ごとに数える。戻り値の index を、次に呼ぶときの since に渡す。
    月例ごとに呼べば、その月に建った棟数が分かる。建て替えも数える。"""
    return call("/buildings/new", timeout=30, since=since)


@tool()
def map_layer(type: str, x: float | None = None, z: float | None = None, radius: float = 500, n: int = 9) -> dict:
    """ゲームの情報画面と同じ値の地図。円を囲む四角を n×n(3〜25)の点で測り、grid(北の行から、西から東へ)、
    average、min、max と、いちばん高い・低い点(maxAt / minAt)を返す。x を省くと街全体(建物のある範囲)。
    type: health / fire / police / education_elementary / education_high / education_university / deathcare /
    entertainment / public_transport(サービスの届き具合。0 は届いていない) / landvalue / noise / crime / pollution /
    water_pollution(高いほど悪い) / wind(0〜100。風車を置く場所を選ぶ) / ore / oil / fertility / forest
    (天然資源。産業の特化を選ぶ) / water_service / sewage_service / electricity_service(今届いているか 1/0) ほか。
    meaning に値の意味と範囲。一覧は list_map_layers。"""
    return call("/map/layer", timeout=30, type=type, x=x, z=z, radius=radius if x is not None else None, n=n)


@tool()
def list_map_layers() -> dict:
    """map_layer で使える type と、その意味の一覧。"""
    return call("/map/layers")


@tool()
def citizens_without_service(type: str = "sewage", limit: int = 20) -> dict:
    """電気・水・下水が来ない住民の住まいを、人数の多い順に返す。type は electricity / water / sewage。
    residents の合計は city_info の citizensWithoutService と同じ数え方。homes に家の id、位置、その家の住民の数、grid。
    住民の数えは7日ごとに更新され、来れば0に戻るので、棟の grid より最大7日遅れる。
    cellNow が true の家は、今は届いていて、次の更新で数えから外れる。"""
    return call("/citizens/without_service", timeout=30, type=type, limit=limit)


# ---- 市政(設計: code/ai-mayor/docs/mcp-interface.md) ----

@tool()
def economy() -> dict:
    """税率(区画の種類ごと、%)と予算(サービスごと、昼と夜、%)を返す。"""
    return call("/economy")


@tool()
def economy_breakdown() -> dict:
    """お金の内訳。週の支出が何から来ているかを確かめるのに使う。
    total: 週の収入と支出の合計(city_info と同じ)。services: サービスごとの週の収入と支出
    (Road は道路と高速道路、PublicTransport は subServices に鉄道やバスの内訳)。
    partOf の付いた行(Citizen、Tourism)は、その行の収入の内訳で、合計に二重には入らない。policyExpenses: 政策の費用。
    networks: 線の種類ごとの本数、長さ(km)、週の維持費(upkeepPerWeek。週の支出と同じ単位、予算100%のとき)。
    freeSegments と freeLengthKm は、マップエディターで置いたなどの理由で維持費がかからない区間。"""
    return call("/economy/breakdown", timeout=30)


@tool()
def set_tax(target: str, rate: int) -> dict:
    """税率を変える。target: residential_low / residential_high / commercial_low / commercial_high / industrial / office。
    rate: 1〜29(%)。"""
    return call("/economy/tax", target=target, rate=rate)


@tool()
def set_budget(target: str, percent: int | None = None, day: int | None = None, night: int | None = None) -> dict:
    """サービスの予算を変える。percent: 50〜150 で、昼と夜の両方を同じ値にする。
    day と night で昼と夜を分けて設定できる(50〜150。どちらかだけでもよい)。
    target: electricity / water / garbage / healthcare / fire / police / education / parks / roads /
    bus / metro / train / ship / plane / taxi。"""
    return call("/economy/budget", target=target, percent=percent, day=day, night=night)


@tool()
def services() -> dict:
    """サービスの充足状況。電気・水・下水・ごみ・医療・葬祭・警察は capacity(容量)と used(使用量)。
    水と下水の used はどちらも週の量で、capacity と同じ単位。
    (#82 の4年目の後に直した。それまで下水の used は1/16に小さく出ていた)
    garbage.full と deathcare.full: 満ちて受け入れを止めた埋立地・墓地の数と id。empty_building で空にするか、置き直す。
    教育は学校の定員、働き手と働き口の数、犯罪率。"""
    return call("/services")


@tool()
def list_policies() -> dict:
    """街全体にかけられる政策の一覧(DLCなしで使えるもの)と、今かかっているか。
    costPerWeek: 今の街でかけたときの週の費用の見積もり。costBasis はその根拠(対象の建物の数 × 1棟の週の額)。
    政策の費用は建物ごとにかかるので、街が育つと増える。policyExpensesPerWeek は、今かかっている政策の実際の週の費用。"""
    return call("/policies")


@tool()
def set_policy(name: str, active: bool = True) -> dict:
    """街全体の政策をかける(active=True)・外す(False)。name は list_policies の名前(例: "Recycling")。
    かける前に list_policies の costPerWeek で週の費用を確かめる。戻り値にも同じ見積もりを返す。"""
    return call("/policies/set", name=name, active=str(active).lower())


@tool()
def zone_polygon(points: list[list[float]], type: str) -> dict:
    """多角形 [[x, z], ...](頂点3つ以上)の中の、道路沿いの区画マスを指定する。type は zone_area と同じ。
    建物が建っているマスは変えない。通りに沿った細長い区画や、街区をまとめて塗るのに使う。"""
    return call("/zone/polygon", body=";".join(f"{x},{z}" for x, z in points), type=type)


@tool()
def zone_rect(x1: float, z1: float, x2: float, z2: float, type: str) -> dict:
    """東西・南北の向きの四角 (x1, z1)〜(x2, z2) の中の、道路沿いの区画マスを指定する。type は zone_area と同じ。"""
    return call("/zone/rect", x1=x1, z1=z1, x2=x2, z2=z2, type=type)


@tool()
def relocate_building(id: int, x: float, z: float, angle: float = 0, facing: str | None = None, pay: bool = True) -> dict:
    """サービスの建物を別の場所へ移す(ゲームの「移す」と同じ)。費用は建設費の1/5。facing / angle は place_building と同じ。
    置けない場所なら reasons に理由を返して断る。ぶつかる区画の建物は取り壊される。
    移した後は、道路・管・送電線のつながりを確かめ直す。
    置けないときは、ぶつかった建物(collidingBuildings)と区間(collidingSegments)の番号を返す。理由は、建物の型の判定(positionReasons)と
    場所の判定(spaceReasons)に分けても返す(#107。相手が空のまま断られたときの手がかり)。移す建物そのものとの重なりは、
    ゲームと同じく数えない。向きを変えると幅と奥行きが入れ替わり、隣の道路にぶつかることがある。"""
    return call("/building/relocate", id=id, x=x, z=z, angle=angle, facing=facing, pay=str(pay).lower())


@tool()
def zone_area(x: float, z: float, radius: float, type: str) -> dict:
    """中心 (x, z)、半径 radius(m)の円の中の、道路沿いの区画マスを指定する。区画マスは道路を引くと両側にできる。
    type: residential_low / residential_high / commercial_low / commercial_high / industrial / office / none(解除)。
    建物が建っているマスは変えない。解禁前の区画の種類は断る。"""
    return call("/zone/area", x=x, z=z, radius=radius, type=type)


@tool()
def zones_at(x: float, z: float, radius: float = 100) -> dict:
    """円の中の区画マスを、種類ごとに数える(確認用)。
    detail: 区画の種類ごとの全部のマス(total)と、建物の建っていない空いたマス(empty)。"""
    return call("/zone/cells", x=x, z=z, radius=radius)


@tool()
def zone_summary(grid: float = 1000) -> dict:
    """街全体の区画マスを、種類ごと・場所ごとに数える。区画の台帳と同じ、統計の道具。
    byType: 種類ごとの全部のマス(total)と、建物の建っていない空いたマス(empty)。
    emptyShallow は、道の側から奥行き1マスしか続かない空き。
    emptyNarrow は、道の側の空きが隣の列とつながらない、幅1列だけの空き。
    emptyBehind は、道の側から続いていない空き(建物の裏の列など)。
    emptyFacingRoad は、道の側から続く空き(empty − emptyBehind)。
    tiles: grid(m)四方の区切りごとの、種類ごとの空いたマス。x, z は区切りの中心。どの地区でマスが切れかけているかを見る。
    区画のある区切りは、空きが0でも返す(empty が空の {})。月どうしで同じ区切りを比べられる。
    円の中だけを数えるなら zones_at を使う。"""
    return call("/zone/summary", timeout=30, grid=grid)


@tool()
def list_building_types(service: str | None = None, locked: bool = False) -> dict:
    """置ける建物(サービス施設、駅、空港など)の一覧。名前、サービス、大きさ(マス)、建設費、週の維持費。
    upkeepPerWeek は、建てたときの週の支出の増え分(予算100%のとき。予算を下げると減る)。
    service で絞れる(例: "Electricity", "Water", "Garbage", "HealthCare", "FireDepartment", "PoliceDepartment",
    "Education", "Beautification", "PublicTransport", "Monument")。
    既定では、解禁された建物だけを返す。locked=True で、解禁前の建物も unlocked=false と解禁の条件(unlock)つきで返す。
    unlock の target は、人口の節目ならその人口。解禁前の建物は place_building で置けない。
    capacity: 建物1つが増やす容量。services の capacity と同じ単位(予算100%、働き手がそろったとき)。
    電気(風車は風で変わる。variesWithWind)、水、下水、ごみ(埋立地のみ)、医療、墓地、警察(留置の定員)、
    教育(elementary / high / university)。分からない種類は null。
    needsRoad: 道路が要るか。needs: 電気・水・下水が要るか。
    ports: 管・送電線のつなぎ口になりうる点。建物の中心から、正面(入口)を向いて右へ right m、前へ forward m。
    置いた後の正確な位置は place_building の ports で確かめる。"""
    return call("/building/prefabs", timeout=30, service=service, locked="true" if locked else None)


@tool()
def place_building(prefab: str, x: float, z: float, angle: float = 0, pay: bool = True,
                   facing: str | None = None) -> dict:
    """建物を (x, z) に置く。正面(入口)を道路に向けること。建物は道路に面していないと働かない(needsRoad が true のとき)。
    facing: 入口の向き(north / northeast / east / southeast / south / southwest / west / northwest、
    または北0・東90の時計回りの度)。angle より優先する。向きを決めるときは facing を使う。
    angle は反時計回りの度で、入口の方位 = (360 − angle) % 360(0で北、90で西、270で東)。angleUsed は実際に使った angle。
    needsRoad が false の建物(風車など)は、entrance.road が null でも働く。needs は電気・水・下水が要るか。
    道路が要る建物の入口のそばに道路がないときは、置いた上で warning を返す。向き(facing)を変えるか、入口の前に道路を引く。
    demolished: 敷地が重なって取り壊される区画の建物の数(count)と id(ids、最大20)。removedNow は置いた直後にもう消えていた数。
    pay: True(既定)なら建設費を予算から払う。足りなければ置かずに断る。人が置く骨格だけ False。
    まだ解禁されていない建物は置かずに断る(unlock に条件を返す)。
    ゲームの建物の道具と同じ判定で、置けない場所(道路やサービスの建物に重なる、買っていない土地、岸がないなど)なら置かずに断る。
    そのとき reasons(理由)と colliding(ぶつかった区間と建物。blocks=true が断る相手)を返す。区画の建物は断る理由にならず、取り壊される。
    岸に置く建物などは、ゲームが位置と向きを直すことがある(angleUsed と entrance で確かめる)。
    "simulation thread timeout" が返ったら、建物は置かれていない(executed=false)。sim_health で確かめてから置き直す。
    entrance: 置いた建物の入口の x, z、正面の向き(facing: north など / bearing: 北0・東90の度)、
    入口から16m以内の道路(road。なければ null)。road が null なら、道路を引くか、向きを変えて置き直す。
    ports: 管・送電線のつなぎ口の x, z と、外の線につながっているか(connected)。管はこの点に端を合わせて引く。"""
    return call("/building/place", prefab=prefab, x=x, z=z, angle=angle, pay=str(pay).lower(), facing=facing)


@tool()
def buildings_near(x: float, z: float, radius: float = 200, limit: int = 50, problems_only: bool = False,
                   problem: str | None = None, service: str | None = None, abandoned: bool = False,
                   brief: bool = False) -> dict:
    """円の中の建物の一覧(id、種類、サービス、位置、放棄されたか、困りごとの印)。total は円の中の総数。
    grid: 建物の場所に電気・水・下水が来ているか(electricity / water / sewage)。ゲームの建物が見るのと同じ値。
    時間を進めたときに更新されるので、管や送電線を引いた直後は advance(1) してから見る。
    grid.needs: その建物が電気・水・下水を要るか。要らないものは来ていなくても困らない。
    jobs: 働き口の数(total)と今の働き手(workers)。homes: 住宅の家族の数(total)と住んでいる数(occupied)。
    vehicles.inUse: サービスの建物が今使っている車の数。storage: 埋立地・墓地のたまり具合(amount / capacity / percent)。
    stats: ゲームの建物の画面の文(使用中の車の数/全部、満杯の割合、処理の量など)。
    収集車が足りないのか、処理場が満杯なのかを見分けるのに使う。
    ports: 建物の管・送電線のつなぎ口(service、x, z)と、外の線につながっているか(connected)。つなぎ口のない建物は []。
    problems_only=True で困りごとの印のある建物だけ。problem="Garbage" などで、その印の建物だけ(名前は complaints の type)。
    service="FireDepartment" などで、サービスの建物を種類で絞る(名前は list_building_types の service)。
    abandoned=True で、放棄・倒壊・焼け跡など取り壊すしかない建物だけを返す。
    brief=True で、1棟を id・種類・位置・印だけの短い形にする(街全体を見るとき)。
    total は絞った後の数。"""
    return call("/buildings", x=x, z=z, radius=radius, limit=limit,
                problems_only="true" if problems_only else None, problem=problem, service=service,
                abandoned="true" if abandoned else None, brief="true" if brief else None)


@tool()
def set_time(paused: bool | None = None, speed: int | None = None) -> dict:
    """時間を止める(paused=True)・進める(False)。speed: 1〜3。省いた値は今のまま。"""
    # 速度を変えると一時停止が解除されるので、速度と一時停止を分けて送る
    r = call("/time", speed=speed) if speed is not None else None
    if paused is not None or r is None:
        r = call("/time", paused=None if paused is None else str(paused).lower())
    return r


@tool()
def advance(days: int = 30, speed: int = 3, max_seconds: int = 600, turbo: int | None = None) -> dict:
    """ゲーム内の時間を days 日だけ進めて止める。判断の単位(1か月 = 30日)を作るのに使う。
    max_seconds を過ぎたら、そこで止める。ゲームにダイアログ(破産の警告など)が出たら、その場で止める。
    dialogs に、進めている間に開いたダイアログ(閉じたものも含む)を入れて返す。
    人口の節目のお知らせは MOD が閉じるので止まらない。dialogs に autoClosed=true で入る。
    turbo: 速度3のときに1回の計算で進めるコマの数(4〜16。4がゲームの既定)。大きいほど早く進む。
    省くと、親や人が前に決めた値のまま。"""
    import datetime
    import time
    start = call("/time", paused="true")
    if not start.get("ok"):
        return start
    seq0 = call("/ui/dialog").get("seq", 0)  # 動かす前の連番。これより増えたら止まる
    d0 = datetime.date.fromisoformat(start["date"])
    target = d0 + datetime.timedelta(days=days)
    _overview()  # 進める間は街の全体を映す
    if turbo is not None:
        call("/time", turbo=turbo)
    call("/time", speed=speed)
    call("/time", paused="false")
    t0 = time.time()
    now = d0
    stopped = False
    seen = seq0  # 読んだ連番。MOD が閉じたお知らせ(autoClosed)では止まらない
    while time.time() - t0 < max_seconds:
        time.sleep(1)
        r = call("/info")
        if r.get("ok"):
            now = datetime.date.fromisoformat(r["date"])
            if r.get("dialog"):
                stopped = True
                break
            if r.get("dialogSeq", 0) > seen:
                new = call("/ui/dialog/events", since=seen).get("events", [])
                seen = max([seen] + [e.get("seq", 0) for e in new])
                if any(not e.get("autoClosed") for e in new):
                    stopped = True
                    break
            if now >= target:
                break
    end = call("/time", paused="true")
    dialogs = call("/ui/dialog/events", since=seq0).get("events", [])
    return {"ok": True, "from": str(d0), "to": end.get("date", str(now)), "seconds": round(time.time() - t0, 1),
            "reached": now >= target, "dialogs": dialogs}


# ---- 市民の声 ----

@tool()
def citizens_summary() -> dict:
    """住んでいる市民の内訳。年齢層、学歴、豊かさ、就業・失業・学生・病気の数、健康・暮らし向き・幸福度の平均(0〜100)、
    電気・水・下水が来ない、体調が悪い、長く失業している市民の数。
    residents はゲームの人口と同じ数え方で、引っ越しの途中の人を含まない。
    movingIn: 家は決まったが、まだ着いていない人(total)と、そのうち移動中の人(traveling)。
    unemployed は、仕事も学校もない若者と大人(10代は入らない)。unemployedDetail で年齢と学歴の内訳を返す。
    average.happiness は住民だけの単純な平均。ゲームの画面の幸福度(city_info の happiness)とは違う。
    公約や採点には city_info の happiness を使う。"""
    return call("/citizens/summary", timeout=30)


@tool()
def citizen_voices(n: int = 5) -> dict:
    """住んでいる市民を n 人(1〜20)無作為に選び、その姿を返す。年齢層、学歴、豊かさ、仕事、健康、幸福度、
    住まいの位置と種類と困りごと、電気・水・下水・体調・失業の困りごとの長さ。市民の立場から考える材料にする。
    job が unemployed なら、今仕事のない若者・大人。troubles.unemployedWeeks は仕事のない週の数
    (0〜7。7日ごとに増え、仕事に就くと次の更新で0に戻る)。"""
    return call("/citizens/sample", timeout=30, n=n)


@tool()
def complaints() -> dict:
    """建物の困りごとの印(電気、水、ごみ、犯罪、騒音、汚染、税が高すぎる、働き手が足りない など)を種類ごとに数え、
    いちばん多い区画(1.92km四方)を返す。苦情の地図として使う。
    hotspot は、その区画の中の、印のある建物の平均の位置。examples にその区画の建物を5件まで(id, x, z, prefab)。
    buildings は街全体の数で、examples(hotspot の区画の中だけ)より多いことがある。ほかの区画は buildings_near(problem=...) で探す。
    その場所を buildings_near(problem=...) で見る。"""
    return call("/complaints", timeout=30)


@tool()
def save_city(name: str, overwrite: bool = False) -> dict:
    """街を保存する。ゲームの保存の画面と同じ処理で、終わるまで待つ(数秒〜数十秒)。
    name: 保存の名前(例: "fukuoka-base-2027-01")。同じ名前があると失敗する。上書きは overwrite=true。
    読み込みは人が行う。戻り値の gameDate は、保存したゲーム内の日付。
    一時停止のまま保存が止まったときは、MOD が一時停止を解いて保存を終わらせ、すぐ止め直す(nudged=true)。
    ゲーム内の時間は進まない。"""
    return call("/save", timeout=90, name=name, overwrite="true" if overwrite else None)


@tool()
def list_saves() -> dict:
    """保存した街の一覧(新しい順)。名前、保存した日時、大きさ(MB)。"""
    return call("/saves")


@tool()
def events() -> dict:
    """前回呼んだときから増えたつぶやき(市民の声、節目、警告など)を返す。判断のきっかけに使う。
    既読はファイルに残るので、ゲームを再起動しても前に読んだつぶやきは返さない。"""
    return call("/events")


# ---- マップエディター(人がマップを整えるための道具。AI市長には渡さない。設計: code/ai-mayor/docs/editor-interface.md) ----


def _poly(points: list[list[float]]) -> str:
    return ";".join(f"{x},{z}" for x, z in points)


@tool()
def editor_state() -> dict:
    """マップの状態。今のモード(エディターか)、地図の外とのつなぎ口の数(道路・鉄道・船・飛行機の入りと出)、
    天然資源の合計(新規ゲーム画面の棒と同じ元の値)、木の本数と上限、水源の数。作業の前後に呼んで確かめる。"""
    return call("/editor/state")


@tool()
def add_outside_connection(prefab: str, points: list[list[float]], y: float | None = None) -> dict:
    """[エディターのみ] 線を引き、地図の端の点を地図の外とのつなぎ口にする。
    points: [[x, z], ...]。最初か最後の点を、地図の端(±8640)から50m以内に置く。その点は端の少し外へ動かす。
    prefab: 線の種類。例: "Train Track"、"Ship Path"(船の航路)、"Airplane Path"(飛行機の経路)。
    端に届く区間だけは、つなぎ口用の線(例: "Train Connection Track")で自動で引く。普通の線ではつなぎ口ができないため。
    つなぎ口の数は少し遅れて更新されるので、after が変わらなくても editor_state で確かめる。
    y: 点の高さを固定するとき(m)。船の航路は水面、飛行機の経路は上空の高さを渡す。省くと地面の高さ。
    線は費用なしで引く。エディターで置いた線は、新しいゲームで維持費がかからない。上限は1種類につき入り4・出4。"""
    return call("/editor/outside", timeout=60, body=_poly(points), prefab=prefab, y=y)


@tool()
def paint_resource(type: str, polygon: list[list[float]], amount: int = 255, mode: str = "set") -> dict:
    """[エディターのみ] 多角形の中の天然資源のマス(33.75m四方)に値を書く。
    type: ore(鉱石) / oil(石油) / fertility(肥えた土地) / sand(砂)。amount: 0〜255。mode: set / clear(0にする)。
    森林のあるマスには肥えた土地を書けない(ゲームの決まり)。森林は plant_forest で木を植えて作る。"""
    return call("/editor/resource", timeout=60, body=_poly(polygon), type=type, amount=amount, mode=mode)


@tool()
def plant_forest(polygon: list[list[float]], density: int = 3, prefab: str | None = None, dry_run: bool = False) -> dict:
    """[エディターのみ] 多角形の中に木を植える。森林の値は、ゲームが木の本数から計算する。
    density: 天然資源の1マス(33.75m四方)あたりの本数(1〜5)。5本でそのマスの森林が最大になる。
    水・道路・建物の上には植えない。木の上限(マップは25万本)を超えるときは植えずに断る。
    dry_run: True なら植えずに、植える本数(candidates)と残りの枠(room)だけ返す。大きな範囲はまずこれで確かめる。"""
    return call("/editor/forest", timeout=150, body=_poly(polygon), density=density, prefab=prefab,
                dry_run=str(dry_run).lower())


@tool()
def resource_map(type: str, save_to: str) -> dict:
    """[エディターのみ] 天然資源の分布を 512×512 の PNG にして保存する。北が上。陸は灰色、水は紺。
    type: forest / fertility / ore / oil / sand。save_to: 保存先の絶対パス。土地利用の地図と並べて確かめるのに使う。"""
    return call("/editor/resource_map", timeout=60, type=type, save_to=save_to)


@tool()
def add_water_source(x: float, z: float, rate: int, target: float) -> dict:
    """[エディターのみ] 水源を置く。水源は、水面が target(m)より低いマスにだけ水を足す。
    rate: 水量(1〜65535)。画面の道具の最小 0.01 は 655 に当たる。小さく始めて、時間を進めながら上げる。
    target: 目標の水面の高さ(m)。川岸より低くすると、水源のまわりであふれない。海面は約40m。
    川が海まで途切れずにつながっていないと、水は target の高さまでたまり続ける。"""
    return call("/editor/water_source", x=x, z=z, rate=rate, target=target)


@tool()
def list_water_sources() -> dict:
    """[エディターのみ] 置いてある水源の一覧(id、位置、地面の高さ、目標の水面の高さ、水量)。"""
    return call("/editor/water_sources")


@tool()
def remove_water_source(id: int) -> dict:
    """[エディターのみ] 水源を取り除く。id は list_water_sources の id。"""
    return call("/editor/water_source/remove", id=id)


@tool()
def carve_channel(points: list[list[float]], width: float = 64, bank: float = 32) -> dict:
    """[エディターのみ] 川筋に沿って地形を掘る。points: [[x, z, 川底の高さ(m)], ...]。点の間の川底は直線で補う。
    width: 川底の幅(m)。bank: 川底から元の地形へなだらかにつなぐ幅(m、片側)。下げるだけで、盛り上げない。
    最初に掘る前の地形を覚えておき、restore_terrain で戻せる。海面は約40m。"""
    body = ";".join(f"{x},{z},{y}" for x, z, y in points)
    return call("/editor/carve", timeout=90, body=body, width=width, bank=bank)


@tool()
def restore_terrain() -> dict:
    """[エディターのみ] carve_channel で最初に掘る前の地形に、まとめて戻す。"""
    return call("/editor/terrain/restore", timeout=90)


@tool()
def water_profile(points: list[list[float]]) -> dict:
    """[エディターのみ] 点ごとの地面の高さ、水面の高さ、水深を返す。川筋や両岸に沿って並べ、水が途切れないか、
    あふれていないかを確かめるのに使う。points: [[x, z], ...]。"""
    return call("/editor/water_profile", timeout=60, body=_poly(points))


@tool()
def rebridge(points: list[list[float]] | None = None, x: float | None = None, z: float | None = None,
             radius: float = 150, prefab: str | None = None) -> dict:
    """[エディターのみ] 既存の道路・線路の区間を、橋の種類(例: "Highway Bridge")に作り替える。
    道路はその下の地形を平らにするので、川を掘っても道路の下だけ埋まり、水がせき止められる。橋は地形を平らにしない。
    points: 川の線 [[x, z], ...]。渡すと、その線と交わる区間をすべて作り替える。
    x, z, radius: 線の代わりに、中心と半径で区間を選ぶ。prefab: 種類で絞る(例: "Highway")。
    作り替えた後、その場所をもう一度 carve_channel で掘ると、溝がつながる。"""
    body = _poly(points) if points else None
    return call("/editor/rebridge", timeout=60, body=body, x=x, z=z, radius=radius, prefab=prefab)



@tool()
def preview_bulldoze(x: float, z: float, radius: float = 50, what: str = "all") -> dict:
    """[読むだけ] bulldoze と同じ円・同じ選び方で、壊したら何が起きるかを見積もる。街は変えない。
    targets: 壊す建物と区間の数、電気の線の区間の数、建物の一覧(id、種類、働き口、家の数。最大50件)。
    lost: 壊す建物が持っていた働き口(jobs)と家(homes)の合計。
    waterFacilities / transportStations: 壊すものに含まれる水の施設と、港・駅・空港。
    power: 壊した後に電気が届かなくなる建物の数(buildingsLosingPower)、その家と働き口、一覧(最大30件)、壊す発電所の数。
    電気の網はゲームと同じ決まりで計算するが、発電所の容量が足りるかは見ない。
    modelAgreement は、見積もりの網がゲームの今の網と一致した割合。低いときは信じすぎない。"""
    return call("/preview/bulldoze", timeout=30, x=x, z=z, radius=radius, what=what)


@tool()
def transport_reach() -> dict:
    """[読むだけ] 港・駅・空港が、地図の外とのつなぎ口まで線でつながっているか。
    stations: 建物ごとに kind(ship / train / plane / metro など)、位置、outsideConnected(船の航路・線路・飛行機の経路で
    外のつなぎ口まで届くか)、outsideLines(ゲームが建物と外の間に自動で作った線の区間の数。0なら外と行き来できていない)。
    viaLaneConnection: 見えない車線のつなぎを通って届いたか。
    つながっていなければ gap に、外へつながる網までのいちばん近いすき間(meters)と両端の座標(from は建物の側、to は外の側)。
    船の航路はプレイヤーには引けない。"""
    return call("/transport/reach", timeout=30)

if __name__ == "__main__":
    mcp.run()
