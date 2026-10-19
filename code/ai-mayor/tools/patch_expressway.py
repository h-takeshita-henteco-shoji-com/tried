"""九州自動車道の福岡インターの結び目を、その区間だけ引き直す(#77)。Mod の窓口を直接呼ぶ。

fukuoka-v2 の九州自動車道は、福岡インターで輪を描いていた。expressway_line.py が、通る地点をランプの点に寄せたため。
expressway_line.py を直して中心線を作り直したが、全線を引き直すと川や森との位置合わせをやり直すことになる。
そこで、結び目の前後の点(ANCHORS)はそのまま残し、その間だけを新しい中心線の点で引き直す。

- 古い中心線: expressway_kyushu.before-77.json(fukuoka-v2 を作ったときのもの)
- 新しい中心線: expressway_kyushu.json(直した expressway_line.py の出力)
- 上りと下りの線は、lay_expressway.py と同じく中心線から左右に OFFSET m ずらす

使い方: python3 patch_expressway.py plan|apply
  plan: 消す線と引く線を表示するだけ
  apply: 古い線を消して、新しい線を引く(費用なし)
"""
import json
import math
import os
import sys

from lay_expressway import EDGE_GAP, OFFSET, TRIM_NORTH, call, extend_to_edge, offset_line

SRC = os.path.expanduser("~/.cache/ai-mayor-dem")
ANCHORS = (149, 159)  # 古い中心線で残す点。この間(150〜158)が結び目
TOLERANCE = 6.0       # 消す区間の両端が、古い線からこの距離以内なら消す


def lanes(points, heights):
    """lay_expressway.py と同じ手順で、南へ向かう線と北へ向かう線を作る。中心線の添字との対応も返す。"""
    pts, h = [tuple(p) for p in points][TRIM_NORTH:], heights[TRIM_NORTH:]
    full, fh = extend_to_edge(pts, h)
    south = offset_line(full, OFFSET)
    north = offset_line(full[::-1], OFFSET)[::-1]  # 中心線と同じ並びにそろえる
    (nx, nz), (sx, sz) = full[0], full[-1]
    south[0], south[-1] = (nx + EDGE_GAP, nz), (sx + EDGE_GAP, sz)
    north[-1], north[0] = (sx - EDGE_GAP, sz), (nx - EDGE_GAP, nz)
    shift = full.index(pts[0]) - TRIM_NORTH  # 古い中心線の添字 k は、full の k + shift
    return south, north, fh, shift


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "plan"
    old = json.load(open(f"{SRC}/expressway_kyushu.before-77.json"))
    new = json.load(open(f"{SRC}/expressway_kyushu.json"))
    a, b = ANCHORS
    pa, pb = old["points"][a], old["points"][b]

    # 新しい中心線のうち、2つの残す点の間にある点(線に沿って pa から pb の間)
    npts = new["points"]
    ia = min(range(len(npts)), key=lambda i: math.dist(npts[i], pa))
    ib = min(range(len(npts)), key=lambda i: math.dist(npts[i], pb))
    mid = [i for i in range(ia, ib + 1) if math.dist(npts[i], pa) > 24 and math.dist(npts[i], pb) > 24]

    # 古い中心線の結び目を、新しい点で置き換えた中心線を作り、そこから上りと下りを作り直す
    pts = old["points"][:a + 1] + [npts[i] for i in mid] + old["points"][b:]
    hs = old["heightData"][:a + 1] + [new["heightData"][i] for i in mid] + old["heightData"][b:]
    o_south, o_north, o_h, shift = lanes(old["points"], old["heightData"])
    n_south, n_north, n_h, _ = lanes(pts, hs)
    s0, s1 = a + shift, b + shift              # 古い線での残す点
    t1 = s0 + len(mid) + 1                     # 新しい線での後ろの残す点

    plan = {
        "remove_south": o_south[s0:s1 + 1], "remove_north": o_north[s0:s1 + 1],
        # 両端は古い線の点そのものにして、既存の点につなぐ
        "build_south": [o_south[s0]] + n_south[s0 + 1:t1] + [o_south[s1]],
        "build_north": [o_north[s0]] + n_north[s0 + 1:t1] + [o_north[s1]],
        "heights": [o_h[s0]] + n_h[s0 + 1:t1] + [o_h[s1]],
    }
    for k, v in plan.items():
        print(k, [tuple(round(c) for c in p) if isinstance(p, tuple) or isinstance(p, list) else p for p in v])
    if mode != "apply":
        return

    def body(line, heights=None):
        heights = heights or [0.0] * len(line)
        return ";".join(f"{x:.1f},{z:.1f},{h:.1f}" for (x, z), h in zip(line, heights))

    for lane in ("south", "north"):
        r = call("/net/remove", body=body(plan[f"remove_{lane}"]), tolerance=TOLERANCE)
        print(lane, "remove", r)
    # 南へ向かう線は北から南へ、北へ向かう線は南から北へ引く(一方通行の向き)
    s = call("/net/build", body=body(plan["build_south"], plan["heights"]), prefab="Highway", pay="false")
    n = call("/net/build", body=body(plan["build_north"][::-1], plan["heights"][::-1]), prefab="Highway", pay="false")
    for lane, r in (("south", s), ("north", n)):
        print(lane, "build", {k: r.get(k) for k in ("ok", "nodes", "segments", "snapped", "split", "error")})


if __name__ == "__main__":
    main()
