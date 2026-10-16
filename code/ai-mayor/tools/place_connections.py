"""マップエディターで、鉄道・船・飛行機の地図の外とのつなぎ口を置く(#73)。Mod の窓口を直接呼ぶ。

- 鉄道: JR鹿児島本線の北と南、西鉄天神大牟田線の南に、地図の端から短い線路を置く(rail_game.json の座標)。
  街の中へ延ばすかは、市長が決める
- 船: 博多湾の湾口から博多港まで、海の中だけを通る航路(ship_route.json。高さマップの海のマスを探して作った)
- 飛行機: 福岡空港の上を、滑走路の向き(北北西から南南東)に沿って地図を横切る経路
端に届く区間は、つなぎ口の道具が専用の線(Train Connection Track など)で引く。

使い方: python3 place_connections.py
"""
import json
import math
import os

from lay_expressway import call

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
STUB = 400.0          # 鉄道の線路を地図の端から延ばす長さ(ゲーム上m)
SEA = 40.0            # 船の航路の高さ(水面)
FLIGHT = 440.0        # 飛行機の経路の高さ
AIRPORT = (1911.0, -238.0)   # 福岡空港(33.5859, 130.4511)をゲーム座標にしたもの
RUNWAY_DEG = -20.0           # 滑走路の向き(北から西へ20度、北北西)


def stub(edge, toward):
    """地図の端の点から toward へ STUB m の線路。"""
    dx, dz = toward[0] - edge[0], toward[1] - edge[1]
    n = math.hypot(dx, dz)
    return [edge, (edge[0] + dx / n * STUB, edge[1] + dz / n * STUB)]


def body(pts):
    return ";".join(f"{x:.1f},{z:.1f}" for x, z in pts)


def main():
    rail = json.load(open(f"{SRC}/rail_game.json"))
    jr, nishi = rail["JR鹿児島本線"], rail["西鉄天神大牟田線"]
    lines = {
        "JR north": stub((jr[0][0], 8630.0), jr[1]),
        "JR south": stub((jr[-1][0], -8630.0), jr[-2]),
        "Nishitetsu south": stub((nishi[-1][0], -8630.0), nishi[-2]),
    }
    for name, pts in lines.items():
        r = call("/editor/outside", body=body(pts), prefab="Train Track")
        print(name, {k: r.get(k) for k in ("ok", "connectionPrefab", "markedNodes", "error")})

    ship = json.load(open(f"{SRC}/ship_route.json"))["ship"]
    r = call("/editor/outside", body=body(ship), prefab="Ship Path", y=SEA)
    print("ship", {k: r.get(k) for k in ("ok", "connectionPrefab", "markedNodes", "error")})

    ux, uz = math.sin(math.radians(RUNWAY_DEG)), math.cos(math.radians(RUNWAY_DEG))
    t_n = (8630.0 - AIRPORT[1]) / uz
    t_s = (-8630.0 - AIRPORT[1]) / uz
    flight = [(AIRPORT[0] + ux * t_n, 8630.0), AIRPORT, (AIRPORT[0] + ux * t_s, -8630.0)]
    r = call("/editor/outside", body=body(flight), prefab="Airplane Path", y=FLIGHT)
    print("plane", {k: r.get(k) for k in ("ok", "connectionPrefab", "markedNodes", "error")})
    print(call("/editor/state")["outsideConnections"])


if __name__ == "__main__":
    main()
