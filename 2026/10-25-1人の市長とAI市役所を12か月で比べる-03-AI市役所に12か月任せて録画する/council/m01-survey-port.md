# m01 調査の結果(port)

## s01-1 貨物駅28755で止まった車が入れ替わっているか

### 見回り1(2050-01-11)

- `vehicles_stuck`(kind="truck", building=28755, limit=10)
  - vehicles 600
  - byState: WaitingSpace+Importing+InGrounds 501、WaitingSpace+Importing+OnRoad 62、Importing+Spawned+OnRoad+Blocked 22、GoingBack+Importing+Spawned+OnRoad+Blocked 12、そのほか各1(InGrounds 2、WaitingTarget 1)
  - byPath: ready 597、none 3
  - bySeenStopped: <1day 140、7days+ 460(この道具で初めて見たのは今回の起動の前。今回の起動で初めて呼んだ)
  - byTarget の上位: 行き先なし(building 0)14、ほかは店ごとに3台ずつ
  - samples 10台: 9台が WaitingSpace+Importing+InGrounds で位置 (3441, -1555)。荷は Goods 7、Coal 1、Food 1。seenStoppedDays は 10 が7台、0 が2台。行き先までの距離 1,541〜6,296
- `cargo`(引数なし)
  - stoppedTrucks 854、stoppedOnRoads 336、stoppedInBuildings 518
  - stoppedInBuildingsTop: 28755 が501、Cargo Harbor 1366 が15、46112 が2
  - Goods: import 912、local 559、stoppedTrucks 557
  - stations: 28755 は vehiclesLeaving 770、vehiclesArriving 11
  - shortages: noGoods 233、noResources 24
- `traffic`(x=3449, z=-1555, radius=150)
  - flow 51、cars 22、blocked 0、congestion 1、averageDensity 10
  - busiest: Large Road 17311 (3400, -1458) 37、Large Road 20316 (3400, -1530) 35
  - blockedSpots なし

### 見回り2(2050-01-21)

- `vehicles_stuck`(kind="truck", building=28755, limit=10)
  - vehicles 599
  - byState: WaitingSpace+Importing+InGrounds 496、WaitingSpace+Importing+OnRoad 57、Importing+Spawned+OnRoad+Blocked 33、GoingBack+Importing+Spawned+OnRoad+Blocked 11、そのほか各1(InGrounds 1、WaitingTarget 1)
  - byPath: ready 597、none 2
  - bySeenStopped: <1day 118、7days+ 481
  - byTarget の上位: 行き先なし(building 0)13、ほかは店・工場ごとに2〜3台
  - samples 10台: 全部 WaitingSpace+Importing+InGrounds、位置 (3441, -1555)。見回り1と同じ車が6台(8、36、120、156、183 は seenStoppedDays 20、152 は 10)。新しく見えた車が4台(103、208、212、229。seenStoppedDays 0)
- `cargo`(引数なし)
  - stoppedTrucks 854、stoppedOnRoads 356、stoppedInBuildings 498
  - stoppedInBuildingsTop: 28755 が496、工場 13809 が1、店 48780 が1
  - Goods: import 918、local 583、stoppedTrucks 554
  - stations: 28755 は vehiclesLeaving 756、vehiclesArriving 11。Cargo Harbor 1366 は leaving 170
  - shortages: noGoods 223、noResources 26
- `traffic`(x=3449, z=-1555, radius=150)
  - flow 52、cars 22、blocked 0、congestion 1、averageDensity 12
  - busiest: Large Road 17311 (3400, -1458) 42、Small 4 Lane Road 14098 (3467, -1416) 35、10573 (3429, -1418) 34、Large Road 20316 (3400, -1530) 30
  - blockedSpots なし

### 月末(2050-01-31)

- `vehicles_stuck`(kind="truck", building=28755, limit=10)
  - vehicles 586
  - byState: WaitingSpace+Importing+InGrounds 488、WaitingSpace+Importing+OnRoad 53、Importing+Spawned+OnRoad+Blocked 25、GoingBack+Importing+Spawned+OnRoad+Blocked 17、そのほか各1(Congestion 1、GoingBack InGrounds 1、WaitingPath 1)
  - byPath: ready 585、none 1
  - bySeenStopped: <1day 111、7days+ 475
  - byTarget の上位: 行き先なし(building 0)19、ほかは店・工場ごとに2〜3台
  - samples 10台: 全部 WaitingSpace+Importing+InGrounds、位置 (3441, -1555)。seenStoppedDays 30 が5台(8、36、120、156、183)、20 が1台(152)、10 が3台(103、208、212)、0 が1台(61。Food、行き先 3795 まで366m)
- `cargo`(引数なし)
  - stoppedTrucks 835、stoppedOnRoads 347、stoppedInBuildings 488
  - stoppedInBuildingsTop: 28755 が488(ほかはなし)
  - Goods: import 924、local 615、stoppedTrucks 535
  - stations: 28755 は vehiclesLeaving 726、vehiclesArriving 11。Cargo Harbor 1366 は leaving 174、46112 は 24
  - shortages: noGoods 215、noResources 27
- `traffic`(x=3449, z=-1555, radius=150)
  - flow 53、cars 14、blocked 0、congestion 1、averageDensity 8
  - busiest: Large Road 20316 (3400, -1530) 30、Large Road 17311 (3400, -1458) 29、Small 4 Lane Road 14098 15、10573 14
  - blockedSpots なし
