"""Cities: Skylines を Claude から見るための MCP サーバー。

AIMayor Mod がゲームの中に開く HTTP の窓口(http://127.0.0.1:8781/)を呼ぶ。
座標はゲーム上のメートル。x が東、z が北。地図の中心が (0, 0)、端が ±8640。
福岡のマップは水平1/2縮尺なので、ゲーム上の1mは実寸2m。

起動: uv run --directory code/ai-mayor/mcp server.py
"""
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from mcp.server.mcpserver import Image, MCPServer
from PIL import Image as PILImage

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


@mcp.tool()
def city_info() -> dict:
    """街の基本の数字を返す。モード、街の名前、ゲーム内の日付、一時停止中か、速度、人口、幸福度、
    所持金、週の収入と支出、需要(住宅・商業・工業。0〜100)、持っている区画の数。"""
    return call("/info")


@mcp.tool()
def screenshot(view: str = "current", max_width: int = 1280) -> Image:
    """ゲームの画面写真を撮って返す。
    view: "current"(今の視点のまま) / "top"(真上から北を上にして地図全体) / "oblique"(北を向いた斜め45度)。
    max_width: 返す画像の幅の上限(画素)。小さいほど軽い。"""
    r = call("/screenshot", timeout=30, view=view)
    if not r.get("ok"):
        raise RuntimeError(r.get("error"))
    img = PILImage.open(r["path"]).convert("RGB")
    if img.width > max_width:
        img = img.resize((max_width, round(img.height * max_width / img.width)))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return Image(data=buf.getvalue(), format="jpeg")


@mcp.tool()
def move_camera(x: float | None = None, z: float | None = None, size: float | None = None,
                pitch: float | None = None, yaw: float | None = None) -> dict:
    """カメラを動かす。省略した値は今のまま。
    x, z: 見る場所(ゲーム上のm。x が東、z が北)。size: 引きの大きさ(大きいほど広く見える。地図全体は約4800)。
    pitch: 見下ろす角度(90で真下)。yaw: 向き(0で北)。
    ゲーム本編では引きの上限が4000。また引くほど角度の下限が上がる(引き4000で約73度、2000で65度、1000で約58度)。
    戻り値の current が、実際のカメラの値。"""
    return call("/camera", x=x, z=z, size=size, pitch=pitch, yaw=yaw)


@mcp.tool()
def height_at(x: float, z: float) -> dict:
    """指定した場所の地面の高さと、水面を含めた高さを返す(ゲーム上のm。海面は約40m)。"""
    return call("/height", x=x, z=z)


# 福岡のマップの中心(天神駅と博多駅の中間)と縮尺(ゲーム上の1m = 実寸2m)
CENTER = (33.59018, 130.40987)
SCALE = 2.0
R = 6371008.8
GIF_DIR = os.path.expanduser("~/Library/Application Support/Colossal Order/Cities_Skylines/AIMayor/gifs")


@mcp.tool()
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


@mcp.tool()
def latlon_to_game(lat: float, lon: float) -> dict:
    """緯度経度を、福岡のマップのゲーム上の座標(x が東、z が北、m)に直す。水平1/2縮尺。"""
    import math
    north = math.radians(lat - CENTER[0]) * R
    east = math.radians(lon - CENTER[1]) * R * math.cos(math.radians(lat))
    return {"x": round(east / SCALE, 1), "z": round(north / SCALE, 1)}


@mcp.tool()
def list_net_types(service: str | None = None) -> dict:
    """引ける線の種類(道路、線路、高速道路など)の名前の一覧。service で絞れる(例: "Road", "PublicTransport")。"""
    r = call("/net/prefabs")
    if service and r.get("ok"):
        r["prefabs"] = [p for p in r["prefabs"] if p.get("service") == service]
    return r


@mcp.tool()
def build_line(prefab: str, points: list[list[float]], frames: int = 0, gif_name: str | None = None,
               pay: bool = True, follow: bool = False, size: float = 2500) -> dict:
    """座標の並び [[x, z], ...] に沿って、線(道路・線路など)を引く。
    端点の12m以内に同じサービスの点があれば、そこにつなぐ。点がなく16m以内に区間があれば、その区間を途中で分けて
    交差点を作り、つなぐ(既存の道路の途中に突き当てられる)。
    prefab: 種類の名前(例: "Train Track", "Highway", "Basic Road")。list_net_types で調べる。
    frames: 1以上なら、線をその数の区間に分けて順に引き、区間ごとに今の視点で画面写真を撮って GIF にまとめる。
    一方通行の道(高速道路など)は、並びの順が進む向きになる。
    pay: True(既定)なら、ゲームの道具と同じく建設費を予算から差し引く。足りなければ建てずに断る。
    人が置く骨格(#69)だけ False にする。
    follow: True なら、区間を引くたびにカメラをその区間の先端へ動かしてから撮る(長い線を追いかけて撮る)。
    size: follow のときのカメラの引き。"""
    if len(points) < 2:
        return {"ok": False, "error": "points は2点以上"}
    if frames <= 0:
        return call("/net/build", timeout=60, body=";".join(f"{x},{z}" for x, z in points), prefab=prefab,
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
        r = call("/net/build", timeout=60, body=";".join(f"{x},{z}" for x, z in part), prefab=prefab,
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


@mcp.tool()
def remove_line(points: list[list[float]], prefab: str | None = None, tolerance: float = 20) -> dict:
    """座標の並び [[x, z], ...](線)に沿った区間を消す。区間の両端が線から tolerance(m)以内のものが対象。
    prefab を指定すると、その種類だけを消す(例: "Train Track")。省くと種類を問わない。"""
    return call("/net/remove", timeout=60, body=";".join(f"{x},{z}" for x, z in points),
                prefab=prefab, tolerance=tolerance)


@mcp.tool()
def bulldoze(x: float, z: float, radius: float = 50, what: str = "all") -> dict:
    """中心 (x, z) から半径 radius(m)の円の中を取り壊す。
    what: "all"(道路・線路と建物) / "net"(道路・線路だけ) / "building"(建物だけ)。取り壊しの払い戻しはない。"""
    return call("/bulldoze", timeout=60, x=x, z=z, radius=radius, what=what)


# ---- 市政(設計: code/ai-mayor/docs/mcp-interface.md) ----

@mcp.tool()
def economy() -> dict:
    """税率(区画の種類ごと、%)と予算(サービスごと、昼と夜、%)を返す。"""
    return call("/economy")


@mcp.tool()
def set_tax(target: str, rate: int) -> dict:
    """税率を変える。target: residential_low / residential_high / commercial_low / commercial_high / industrial / office。
    rate: 1〜29(%)。"""
    return call("/economy/tax", target=target, rate=rate)


@mcp.tool()
def set_budget(target: str, percent: int) -> dict:
    """サービスの予算を変える(昼と夜の両方)。percent: 50〜150。
    target: electricity / water / garbage / healthcare / fire / police / education / parks / roads /
    bus / metro / train / ship / plane / taxi。"""
    return call("/economy/budget", target=target, percent=percent)


@mcp.tool()
def services() -> dict:
    """サービスの充足状況。電気・水・下水・ごみ・医療・葬祭・警察は capacity(容量)と used(使用量)。
    教育は学校の定員、働き手と働き口の数、犯罪率。"""
    return call("/services")


@mcp.tool()
def list_policies() -> dict:
    """街全体にかけられる政策の一覧(DLCなしで使えるもの)と、今かかっているか。"""
    return call("/policies")


@mcp.tool()
def set_policy(name: str, active: bool = True) -> dict:
    """街全体の政策をかける(active=True)・外す(False)。name は list_policies の名前(例: "Recycling")。"""
    return call("/policies/set", name=name, active=str(active).lower())


@mcp.tool()
def zone_area(x: float, z: float, radius: float, type: str) -> dict:
    """中心 (x, z)、半径 radius(m)の円の中の、道路沿いの区画マスを指定する。区画マスは道路を引くと両側にできる。
    type: residential_low / residential_high / commercial_low / commercial_high / industrial / office / none(解除)。
    建物が建っているマスは変えない。"""
    return call("/zone/area", x=x, z=z, radius=radius, type=type)


@mcp.tool()
def zones_at(x: float, z: float, radius: float = 100) -> dict:
    """円の中の区画マスを、種類ごとに数える(確認用)。"""
    return call("/zone/cells", x=x, z=z, radius=radius)


@mcp.tool()
def list_building_types(service: str | None = None) -> dict:
    """置ける建物(サービス施設、駅、空港など)の一覧。名前、サービス、大きさ(マス)、建設費、維持費。
    service で絞れる(例: "Electricity", "Water", "Garbage", "HealthCare", "FireDepartment", "PoliceDepartment",
    "Education", "Beautification", "PublicTransport", "Monument")。"""
    return call("/building/prefabs", timeout=30, service=service)


@mcp.tool()
def place_building(prefab: str, x: float, z: float, angle: float = 0, pay: bool = True) -> dict:
    """建物を (x, z) に置く。angle は向き(度)。正面(入口)を道路に向けること。建物は道路に面していないと働かない。
    pay: True(既定)なら建設費を予算から払う。足りなければ置かずに断る。人が置く骨格だけ False。"""
    return call("/building/place", prefab=prefab, x=x, z=z, angle=angle, pay=str(pay).lower())


@mcp.tool()
def buildings_near(x: float, z: float, radius: float = 200, limit: int = 50) -> dict:
    """円の中の建物の一覧(id、種類、サービス、位置、放棄されたか、困りごとの印)。total は円の中の総数。"""
    return call("/buildings", x=x, z=z, radius=radius, limit=limit)


@mcp.tool()
def set_time(paused: bool | None = None, speed: int | None = None) -> dict:
    """時間を止める(paused=True)・進める(False)。speed: 1〜3。省いた値は今のまま。"""
    # 速度を変えると一時停止が解除されるので、速度と一時停止を分けて送る
    r = call("/time", speed=speed) if speed is not None else None
    if paused is not None or r is None:
        r = call("/time", paused=None if paused is None else str(paused).lower())
    return r


@mcp.tool()
def advance(days: int = 30, speed: int = 3, max_seconds: int = 600) -> dict:
    """ゲーム内の時間を days 日だけ進めて止める。判断の単位(1か月 = 30日)を作るのに使う。
    max_seconds を過ぎたら、そこで止める。"""
    import datetime
    import time
    start = call("/time", paused="true")
    if not start.get("ok"):
        return start
    d0 = datetime.date.fromisoformat(start["date"])
    target = d0 + datetime.timedelta(days=days)
    call("/time", speed=speed)
    call("/time", paused="false")
    t0 = time.time()
    now = d0
    while time.time() - t0 < max_seconds:
        time.sleep(1)
        r = call("/info")
        if r.get("ok"):
            now = datetime.date.fromisoformat(r["date"])
            if now >= target:
                break
    end = call("/time", paused="true")
    return {"ok": True, "from": str(d0), "to": end.get("date", str(now)), "seconds": round(time.time() - t0, 1),
            "reached": now >= target}


# ---- 市民の声 ----

@mcp.tool()
def citizens_summary() -> dict:
    """住んでいる市民の内訳。年齢層、学歴、豊かさ、就業・失業・学生・病気の数、健康・暮らし向き・幸福度の平均(0〜100)、
    電気・水・下水が来ない、体調が悪い、長く失業している市民の数。"""
    return call("/citizens/summary", timeout=30)


@mcp.tool()
def citizen_voices(n: int = 5) -> dict:
    """住んでいる市民を n 人(1〜20)無作為に選び、その姿を返す。年齢層、学歴、豊かさ、仕事、健康、幸福度、
    住まいの位置と種類と困りごと、電気・水・下水・体調・失業の困りごとの長さ。市民の立場から考える材料にする。"""
    return call("/citizens/sample", timeout=30, n=n)


@mcp.tool()
def complaints() -> dict:
    """建物の困りごとの印(電気、水、ごみ、犯罪、騒音、汚染、税が高すぎる、働き手が足りない など)を種類ごとに数え、
    いちばん多い区画(1.92km四方)の中心の座標を返す。苦情の地図として使う。"""
    return call("/complaints", timeout=30)


@mcp.tool()
def events() -> dict:
    """前回呼んだときから増えたつぶやき(市民の声、節目、警告など)を返す。判断のきっかけに使う。"""
    return call("/events")


if __name__ == "__main__":
    mcp.run()
