# m01 調査 s01-3(health) ごみの印の原因

## 見回り1(2050-01-11)

- `complaints`(引数なし): Garbage 13 棟(hotspot (-247.5,-1351.6) 5 棟)。Pollution 38 棟(hotspot (3854.7,-242.4) 20 棟)。Crime 1 棟(貨物港 32211)。Fire 4 棟。
- `buildings_near`(x=-500、z=-1500、radius=500、problem="Garbage"): total 4(2717、5049、16326、33255)。
- `vehicles_stuck`(kind="garbage"、limit=30): 244 台。byState は Congestion を含むもの 179、Blocked を含むもの 163、WaitingSpace 10。すべて道の上。seenStoppedDays は全部 <1day。サンプル30台のうち、積荷 20000 で GoingBack が多数。

## 月末(2050-01-31)

- `complaints`(引数なし): Garbage 15 棟(hotspot (-1979.1,-271.5) 4 棟)。Pollution 49 棟(hotspot (3759.3,-207.1) 22 棟)。Crime 1 棟((3296,24))。Fire 1 棟。
- `buildings_near`(x=-500、z=-1500、radius=500、problem="Garbage"): total 0。
- `vehicles_stuck`(kind="garbage"、limit=5): 213 台。Congestion を含むもの 166、Blocked を含むもの 110、WaitingSpace 8。bySeenStopped は <1day 78、7days+ 135。

## 見回り2(2050-01-21)

- `complaints`(引数なし): Garbage 9 棟(hotspot (1532.8,-582) 3 棟)。Pollution 41 棟(hotspot (3794.3,-194.9) 22 棟)。Crime 1 棟(hotspot (-584,-374)、貨物港 32211 の印は消えた)。Fire 2 棟。
- `buildings_near`(x=-500、z=-1500、radius=500、problem="Garbage"): total 0。
- `vehicles_stuck`(kind="garbage"、limit=30): 228 台。byState は Congestion を含むもの 188、Blocked を含むもの 143、WaitingSpace 7。bySeenStopped は <1day 76、7days+ 152。サンプルは積荷 20000 の GoingBack(焼却場や埋立地へ戻る途中)が多数、すべて道の上。
