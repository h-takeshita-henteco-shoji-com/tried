# m02 調査 s02-1(port): 貨物駅28755で止まった車の位置と出口

問い: 28755で止まった車は、出口の線(Cargo Connection、(3417, -1555)で終わる)の先に進めないのか、同じ駅にある別の出口(東の(3497, -1555))へ回ればよいのか。

## 見回り1(2050-02-10)

### `vehicles_stuck`(kind="truck", building=28755, limit=30)

- vehicles 639
- byState: WaitingSpace+Importing+InGrounds 505、WaitingSpace+Importing+OnRoad 93、Importing+Spawned+OnRoad+Blocked 23、GoingBack+Importing+Spawned+OnRoad+Blocked 15、GoingBack+Importing+Spawned+InGrounds 2、Importing+Spawned+InGrounds 1
- byPath: ready 636、none 3
- bySeenStopped: <1day 179、7days+ 460
- byTarget 上位: 0(行き先なし)17、39087 Future Store (-968,-1574) 4、44663 Shop05a (-840,68) 3、21559 Shop13 (-896,-797) 3、37957 Future Store (1529,392) 3、44050 Future Store (-2340,132) 3
- samples 30台: WaitingSpace の29台はすべて位置 (3441,-1555)、blockCounter 0、waitCounter 0。うち WaitingSpace+OnRoad は2台(103、377)で、位置は同じ (3441,-1555)。seenStoppedDays は 0〜40。荷は Goods 15、Food 7、Petrol 3、Coal 2、Lumber 2。行き先までの距離 831〜6,296m。Blocked の1台(vehicle 316、GoingBack)は (2717,-1244)、blockCounter 26

### `net_near`(x=3417, z=-1557, radius=45)

- 25546 Cargo Connection: (3469,-1555) → (3417,-1555)(node 27256 → 5129)、52m
- 30062 Cargo Connection: (3417,-1560) → (3469,-1560)(node 20745 → 27809)、52m
- 20316 Large Road: (3400,-1567) → (3400,-1493)、76m、3/3車線
- 30945 Large Road: (3400,-1625) → (3400,-1567)、57m、3/3車線
- 1143 Water Pipe: (3480,-1480) → (3455,-1555)
- total 5。Cargo Connection の端 (3417,-1555)・(3417,-1560) と Large Road の点 (3400,-1567) は別の node

### `traffic`(x=3441, z=-1555, radius=60)

- flow 51、cars 11、blocked 0、congestion 1、roadSegments 3、averageDensity 12
- busiest: 20316 Large Road (3400,-1530) 38
- blockedSpots: なし
