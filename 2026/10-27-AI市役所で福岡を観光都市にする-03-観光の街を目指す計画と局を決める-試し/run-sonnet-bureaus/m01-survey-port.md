# m01 調査 s01-2(port) 貨物駅 28755 で492台が止まる理由

## 見回り1(2050-01-11)

- `vehicles_stuck`(kind="truck"、building=28755、limit=10): 643 台。byState は WaitingSpace+Importing+InGrounds 483、WaitingSpace+Importing+OnRoad 93、Importing+OnRoad+Blocked 45、GoingBack+OnRoad+Blocked 18。byPath は ready 639、none 4。bySeenStopped は <1day 193、7days+ 450。サンプル10台のうち7台が (3441,-1555) の敷地内で WaitingSpace(積荷は Goods と Coal、seenStoppedDays 10)。
- `traffic`(x=3449、z=-1555、radius=150): flow 48、cars 16、blocked 0、congestion 1、averageDensity 11、blockedSpots なし。
- `cargo`(引数なし): 駅 28755 の stoppedTrucks 483(stoppedInBuildings 計 501)、vehiclesLeaving 782、vehiclesArriving 13。stoppedSpots 先頭 (3440,-1553) 94 台(道の上)。

## 見回り2(2050-01-21)

- `vehicles_stuck`(kind="truck"、building=28755、limit=10): 616 台。byState は WaitingSpace+Importing+InGrounds 484、WaitingSpace+Importing+OnRoad 78、Importing+OnRoad+Blocked 42、GoingBack+OnRoad+Blocked 11。byPath は ready 616。bySeenStopped は <1day 116、7days+ 500。サンプルの敷地内 WaitingSpace は seenStoppedDays 20(見回り1と同じ車 8、36、120、156、183)。
- `traffic`(x=3449、z=-1555、radius=150): flow 50、cars 21、blocked 0、congestion 1、blockedSpots なし。
- `cargo`(引数なし): 駅 28755 の stoppedTrucks 484(stoppedInBuildings 計 484)、vehiclesLeaving 772、vehiclesArriving 12。stoppedSpots 先頭 (3436,-1545) 89 台。

## 月末(2050-01-31)

- `vehicles_stuck`(kind="truck"、building=28755、limit=10): 626 台。byState は WaitingSpace+Importing+InGrounds 506、WaitingSpace+Importing+OnRoad 74、Importing+OnRoad+Blocked 32、GoingBack+OnRoad+Blocked 10。byPath は ready 624、none 2。bySeenStopped は <1day 131、7days+ 495。サンプルの敷地内 WaitingSpace は seenStoppedDays 30.1(車 8、36、120、156 が同じ位置 (3441,-1555) で30日)。
- `traffic`(x=3449、z=-1555、radius=150): flow 53、cars 22、blocked 0、congestion 1、blockedSpots なし。
- `cargo`(引数なし): 駅 28755 の stoppedTrucks 506(stoppedInBuildings 計 506)、vehiclesLeaving 790、vehiclesArriving 12。stoppedSpots 先頭 (3441,-1555) 75 台。
