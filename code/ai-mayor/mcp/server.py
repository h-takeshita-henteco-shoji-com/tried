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
import time
import urllib.error
import urllib.parse
import urllib.request

from mcp.server.mcpserver import Image, MCPServer
from PIL import Image as PILImage
from PIL import ImageDraw

BASE = os.environ.get("AIMAYOR_URL", "http://127.0.0.1:8781")

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
    query = urllib.parse.urlencode({"action": action[:200], "reason": reason[:300]})
    try:
        with urllib.request.urlopen(f"{BASE}/ui/note?{query}", timeout=0.5) as r:
            r.read()
    except Exception:
        pass


def _short(v, limit: int = 60) -> str:
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= limit else s[:limit - 3] + "..."


def tool():
    """mcp.tool() の代わり。道具の開始と終了(成否と秒数)をゲーム画面のパネルに知らせる。"""
    def deco(fn):
        sig = inspect.signature(fn)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            cid = str(next(_seq))
            bound = sig.bind(*args, **kwargs)
            shown = " ".join(f"{k}={_short(v)}" for k, v in bound.arguments.items())
            notify(phase="start", id=cid, tool=fn.__name__, args=_short(shown, 200))
            t0 = time.time()
            try:
                result = fn(*args, **kwargs)
            except Exception as e:
                notify(phase="end", id=cid, ok="false", detail=_short(str(e), 120))
                raise
            sec = f"{time.time() - t0:.1f}s"
            if isinstance(result, dict) and result.get("ok") is False:
                notify(phase="end", id=cid, ok="false", detail=_short(f"{result.get('error')} ({sec})", 120))
            else:
                # 建設費を返す道具は、ログにも費用を残す
                cost = result.get("cost") if isinstance(result, dict) else None
                notify(phase="end", id=cid, ok="true", detail=f"{sec} cost={cost}" if cost is not None else sec)
            return result

        return mcp.tool()(wrapper)

    return deco


@tool()
def city_info() -> dict:
    """街の基本の数字を返す。モード、街の名前、ゲーム内の日付、一時停止中か、速度、人口、幸福度、
    所持金、週の収入と支出、需要(住宅・商業・工業。0〜100)、持っている区画の数。
    dialog: ゲームの画面に出ているダイアログ(破産の警告など)。なければ null。
    出ていたら、見出し(texts)とボタン(buttons)を読み、判断の材料にする。
    dialogSeq: 最後に開いたダイアログの連番。前回より増えていたら、dialog_events で閉じたものも読める。"""
    return call("/info")


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
    view: "current"(今の視点のまま) / "top"(真上から北を上にして地図全体) / "oblique"(北を向いた斜め45度)。
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
    blockedSpots: 止まっている車が多い場所(200m四方ごとの車の位置の平均と台数)。"""
    return call("/traffic", timeout=30, x=x, z=z, radius=radius if x is not None else None, limit=limit)


@tool()
def net_near(x: float, z: float, radius: float = 200, service: str | None = None, limit: int = 50) -> dict:
    """円の中の線(道路・水道管・送電線など)の一覧。管や道路をつなぐ前に、既存の線の位置を確かめる。
    service: "Road" / "Water" / "Electricity" などで絞る。省くと全部。
    segments: 区間ごとに segment、prefab、service、start と end(点の番号 node と x, z)、length。
    node が同じ区間どうしはつながっている。build_line の端をその点の座標に合わせると、そこにつながる。
    道路には carLanes(startToEnd / endToStart: その向きに車が走れる車線の数)。片方が0なら一方通行(高速道路など)。"""
    return call("/net/near", timeout=30, x=x, z=z, radius=radius, service=service, limit=limit)


@tool()
def net_reach(x: float | None = None, z: float | None = None, radius: float = 500, limit: int = 10) -> dict:
    """外の街から車で来られるかを確かめる。つなぎ口から道路を一方通行の向きどおりにたどる。
    引っ越してくる人は、つなぎ口から家まで車で来られないと着かず、人口に入らない(citizens_summary の movingIn が減らない)。
    x, z, radius を渡すとその円の中だけ、省くと街全体。
    roads: 道路の区間の数、つなぎ口から入れない数(notEnterable)、つなぎ口へ出られない数(notLeavable)。
    buildings: 建物の数、道路に面していない数(noRoad)、来られない数(notReachable)、出られない数(cannotLeave)。
    noRoad には、風力発電や給水塔など道路の要らない建物も入る。住宅・商業・工業が noRoad なら道路を確かめる。
    badBuildings / badSegments: 問題のある建物と区間(位置つき)。
    交差点で曲がれる向きは見ないので、ゲームより甘い。ここで問題があれば、ゲームでも来られない。"""
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
    線: 道路=濃い灰(太い)、水道管=青、送電線=橙。建物=黒い枠。電気・水・下水のどれかが来ていない建物は赤い枠。
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

    for ax, az, mx, mz, bx, bz, service, raised in d["lines"]:
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
def list_net_types(service: str | None = None) -> dict:
    """引ける線の種類(道路、線路、高速道路など)の名前の一覧。service で絞れる(例: "Road", "PublicTransport")。
    costPerKm: 1kmあたりの建設費(地面の上。高架やトンネルは高くなる)。
    upkeepPerWeekPerKm: 1kmあたりの週の維持費(週の支出と同じ単位、予算100%のとき)。"""
    r = call("/net/prefabs")
    if service and r.get("ok"):
        r["prefabs"] = [p for p in r["prefabs"] if p.get("service") == service]
    return r


@tool()
def build_line(prefab: str, points: list[list[float]], frames: int = 0, gif_name: str | None = None,
               pay: bool = True, follow: bool = False, size: float = 2500) -> dict:
    """座標の並び [[x, z], ...] に沿って、線(道路・線路など)を引く。
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
    insideBuilding は、端が敷地の中にある建物の id。送電線は端が建物の敷地に入れば電気が通る。"""
    if len(points) < 2:
        return {"ok": False, "error": "points は2点以上"}
    if frames <= 0:
        return call("/net/build", timeout=60, body=";".join(",".join(str(v) for v in p) for p in points), prefab=prefab,
                    pay=str(pay).lower())

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
                 pay=str(pay).lower())
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
def bulldoze(x: float, z: float, radius: float = 50, what: str = "all") -> dict:
    """中心 (x, z) から半径 radius(m)の円の中を取り壊す。
    what: "all"(道路・線路と建物) / "net"(道路・線路だけ) / "building"(建物だけ)。取り壊しの払い戻しはない。"""
    return call("/bulldoze", timeout=60, x=x, z=z, radius=radius, what=what)


# ---- 市政(設計: code/ai-mayor/docs/mcp-interface.md) ----

@tool()
def economy() -> dict:
    """税率(区画の種類ごと、%)と予算(サービスごと、昼と夜、%)を返す。"""
    return call("/economy")


@tool()
def economy_breakdown() -> dict:
    """お金の内訳。週の支出が何から来ているかを確かめるのに使う。
    total: 週の収入と支出の合計(city_info と同じ)。services: サービスごとの週の収入と支出
    (Road は道路と高速道路、PublicTransport は subServices に鉄道やバスの内訳)。policyExpenses: 政策の費用。
    networks: 線の種類ごとの本数、長さ(km)、週の維持費(upkeepPerWeek。週の支出と同じ単位、予算100%のとき)。
    freeSegments と freeLengthKm は、マップエディターで置いたなどの理由で維持費がかからない区間。"""
    return call("/economy/breakdown", timeout=30)


@tool()
def set_tax(target: str, rate: int) -> dict:
    """税率を変える。target: residential_low / residential_high / commercial_low / commercial_high / industrial / office。
    rate: 1〜29(%)。"""
    return call("/economy/tax", target=target, rate=rate)


@tool()
def set_budget(target: str, percent: int) -> dict:
    """サービスの予算を変える(昼と夜の両方)。percent: 50〜150。
    target: electricity / water / garbage / healthcare / fire / police / education / parks / roads /
    bus / metro / train / ship / plane / taxi。"""
    return call("/economy/budget", target=target, percent=percent)


@tool()
def services() -> dict:
    """サービスの充足状況。電気・水・下水・ごみ・医療・葬祭・警察は capacity(容量)と used(使用量)。
    教育は学校の定員、働き手と働き口の数、犯罪率。"""
    return call("/services")


@tool()
def list_policies() -> dict:
    """街全体にかけられる政策の一覧(DLCなしで使えるもの)と、今かかっているか。"""
    return call("/policies")


@tool()
def set_policy(name: str, active: bool = True) -> dict:
    """街全体の政策をかける(active=True)・外す(False)。name は list_policies の名前(例: "Recycling")。"""
    return call("/policies/set", name=name, active=str(active).lower())


@tool()
def zone_area(x: float, z: float, radius: float, type: str) -> dict:
    """中心 (x, z)、半径 radius(m)の円の中の、道路沿いの区画マスを指定する。区画マスは道路を引くと両側にできる。
    type: residential_low / residential_high / commercial_low / commercial_high / industrial / office / none(解除)。
    建物が建っているマスは変えない。"""
    return call("/zone/area", x=x, z=z, radius=radius, type=type)


@tool()
def zones_at(x: float, z: float, radius: float = 100) -> dict:
    """円の中の区画マスを、種類ごとに数える(確認用)。"""
    return call("/zone/cells", x=x, z=z, radius=radius)


@tool()
def list_building_types(service: str | None = None) -> dict:
    """置ける建物(サービス施設、駅、空港など)の一覧。名前、サービス、大きさ(マス)、建設費、週の維持費。
    upkeepPerWeek は、建てたときの週の支出の増え分(予算100%のとき。予算を下げると減る)。
    service で絞れる(例: "Electricity", "Water", "Garbage", "HealthCare", "FireDepartment", "PoliceDepartment",
    "Education", "Beautification", "PublicTransport", "Monument")。
    ports: 管・送電線のつなぎ口になりうる点。建物の中心から、正面(入口)を向いて右へ right m、前へ forward m。
    置いた後の正確な位置は place_building の ports で確かめる。"""
    return call("/building/prefabs", timeout=30, service=service)


@tool()
def place_building(prefab: str, x: float, z: float, angle: float = 0, pay: bool = True) -> dict:
    """建物を (x, z) に置く。angle は向き(度)。正面(入口)を道路に向けること。建物は道路に面していないと働かない。
    pay: True(既定)なら建設費を予算から払う。足りなければ置かずに断る。人が置く骨格だけ False。
    entrance: 置いた建物の入口の x, z、正面の向き(facing: north など / bearing: 北0・東90の度)、
    入口から16m以内の道路(road。なければ null)。road が null なら、道路を引くか、向きを変えて置き直す。
    ports: 管・送電線のつなぎ口の x, z と、外の線につながっているか(connected)。管はこの点に端を合わせて引く。"""
    return call("/building/place", prefab=prefab, x=x, z=z, angle=angle, pay=str(pay).lower())


@tool()
def buildings_near(x: float, z: float, radius: float = 200, limit: int = 50) -> dict:
    """円の中の建物の一覧(id、種類、サービス、位置、放棄されたか、困りごとの印)。total は円の中の総数。
    grid: 建物の場所に電気・水・下水が来ているか(electricity / water / sewage)。ゲームの建物が見るのと同じ値。
    時間を進めたときに更新されるので、管や送電線を引いた直後は advance(1) してから見る。
    ports: 建物の管・送電線のつなぎ口(service、x, z)と、外の線につながっているか(connected)。つなぎ口のない建物は []。"""
    return call("/buildings", x=x, z=z, radius=radius, limit=limit)


@tool()
def set_time(paused: bool | None = None, speed: int | None = None) -> dict:
    """時間を止める(paused=True)・進める(False)。speed: 1〜3。省いた値は今のまま。"""
    # 速度を変えると一時停止が解除されるので、速度と一時停止を分けて送る
    r = call("/time", speed=speed) if speed is not None else None
    if paused is not None or r is None:
        r = call("/time", paused=None if paused is None else str(paused).lower())
    return r


@tool()
def advance(days: int = 30, speed: int = 3, max_seconds: int = 600) -> dict:
    """ゲーム内の時間を days 日だけ進めて止める。判断の単位(1か月 = 30日)を作るのに使う。
    max_seconds を過ぎたら、そこで止める。ゲームにダイアログ(破産の警告など)が出たら、その場で止めて
    dialogs に、進めている間に開いたダイアログ(閉じたものも含む)を入れて返す。"""
    import datetime
    import time
    start = call("/time", paused="true")
    if not start.get("ok"):
        return start
    seq0 = call("/ui/dialog").get("seq", 0)  # 動かす前の連番。これより増えたら止まる
    d0 = datetime.date.fromisoformat(start["date"])
    target = d0 + datetime.timedelta(days=days)
    call("/time", speed=speed)
    call("/time", paused="false")
    t0 = time.time()
    now = d0
    stopped = False
    while time.time() - t0 < max_seconds:
        time.sleep(1)
        r = call("/info")
        if r.get("ok"):
            now = datetime.date.fromisoformat(r["date"])
            if r.get("dialog") or r.get("dialogSeq", 0) > seq0:
                stopped = True
                break
            if now >= target:
                break
    end = call("/time", paused="true")
    dialogs = call("/ui/dialog/events", since=seq0).get("events", []) if stopped else []
    return {"ok": True, "from": str(d0), "to": end.get("date", str(now)), "seconds": round(time.time() - t0, 1),
            "reached": now >= target, "dialogs": dialogs}


# ---- 市民の声 ----

@tool()
def citizens_summary() -> dict:
    """住んでいる市民の内訳。年齢層、学歴、豊かさ、就業・失業・学生・病気の数、健康・暮らし向き・幸福度の平均(0〜100)、
    電気・水・下水が来ない、体調が悪い、長く失業している市民の数。
    residents はゲームの人口と同じ数え方で、引っ越しの途中の人を含まない。
    movingIn: 家は決まったが、まだ着いていない人(total)と、そのうち移動中の人(traveling)。
    つなぎ口から家までの道順が見つかると着いて人口に入る。減らないなら、外から街へ道がつながっていない。"""
    return call("/citizens/summary", timeout=30)


@tool()
def citizen_voices(n: int = 5) -> dict:
    """住んでいる市民を n 人(1〜20)無作為に選び、その姿を返す。年齢層、学歴、豊かさ、仕事、健康、幸福度、
    住まいの位置と種類と困りごと、電気・水・下水・体調・失業の困りごとの長さ。市民の立場から考える材料にする。"""
    return call("/citizens/sample", timeout=30, n=n)


@tool()
def complaints() -> dict:
    """建物の困りごとの印(電気、水、ごみ、犯罪、騒音、汚染、税が高すぎる、働き手が足りない など)を種類ごとに数え、
    いちばん多い区画(1.92km四方)の中心の座標を返す。苦情の地図として使う。"""
    return call("/complaints", timeout=30)


@tool()
def save_city(name: str, overwrite: bool = False) -> dict:
    """街を保存する。ゲームの保存の画面と同じ処理で、終わるまで待つ(数秒〜数十秒)。
    name: 保存の名前(例: "fukuoka-base-2027-01")。同じ名前があると失敗する。上書きは overwrite=true。
    読み込みは人が行う。戻り値の gameDate は、保存したゲーム内の日付。"""
    return call("/save", timeout=90, name=name, overwrite="true" if overwrite else None)


@tool()
def list_saves() -> dict:
    """保存した街の一覧(新しい順)。名前、保存した日時、大きさ(MB)。"""
    return call("/saves")


@tool()
def events() -> dict:
    """前回呼んだときから増えたつぶやき(市民の声、節目、警告など)を返す。判断のきっかけに使う。"""
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


if __name__ == "__main__":
    mcp.run()
