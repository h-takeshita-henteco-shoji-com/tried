# m01 調査 s01-1(port): 貨物駅28755で止まるトラックの、止まり方の時間変化

実行する市長が、道具の返した数だけを書く。見立ては書かない。

## 見回り1(2050-01-11)

### `vehicles_stuck(kind="truck", building=28755, limit=20)`

- vehicles 615
- byState: WaitingSpace+Importing+InGrounds 505、WaitingSpace+Importing+OnRoad 61、Importing+Spawned+OnRoad+Blocked 33、GoingBack+Importing+Spawned+OnRoad+Blocked 14、GoingBack+Importing+Spawned+InGrounds 1、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 613、none 2
- bySeenStopped: <1day 146、7days+ 469(この道具を初めて呼んだのは月例の前の局の調べ)
- byTarget: 行き先なし(building 0)16台。ほかは店・工場ごとに3〜4台(39876 H3 4x3 Shop03 (1940,854) 4台 など)
- samples 20台: 全部 source 28755、位置 (3441,-1555)。blockCounter 0、waitCounter 0。積み荷は Goods 14、Petrol 4、Coal 1、Food 1、Lumber 1(20台のうち)。seenStoppedDays 10 が15台、0 が5台。行き先までの距離 838〜6,296m

### `cargo()`

- trucks 2,110、stoppedTrucks 809(道の上 287、建物の中 522)
- stoppedInBuildingsTop: 28755 Cargo Center 505、1366 Cargo Harbor 15、46112 Cargo Harbor 2
- 駅28755: vehiclesLeaving 793、vehiclesArriving 11
- 駅13893(3529,-1555): vehiclesLeaving 0、vehiclesArriving 0
- ほかの貨物駅(3940、4740、14580、16572、40031、48243)は出入り0。港1366 は出167・入5、46112 は出42・入2、32211 は出0・入1
- stoppedSpots: (3441,-1555) 61、(2685,-953) 20、(2500,-946) 10、(-669,-734) 8、(869,-705) 7
- byCargo の止まった台数: Goods 521、Petrol 90、Lumber 83、Coal 72、Food 42、Oil 1
- shortages: noGoods 239棟、noResources 23棟

### `traffic(x=3439, z=-1551, radius=60, limit=10)`

- flow 50、cars 10、blocked 0、congestion 1、roadSegments 3、averageDensity 10
- busiest: 20316 Large Road (3400,-1530) density 31
- blockedSpots: なし

## 見回り2(2050-01-21)

### `vehicles_stuck(kind="truck", building=28755, limit=20)`

- vehicles 672
- byState: WaitingSpace+Importing+InGrounds 515、WaitingSpace+Importing+OnRoad 59、Importing+Spawned+OnRoad+Blocked 80、GoingBack+Importing+Spawned+OnRoad+Blocked 11、GoingBack+Importing+Spawned+InGrounds 3、Importing+Spawned+InGrounds 2、Congestion+Importing+Spawned+OnRoad 1、WaitingPath+GoingBack+Importing+Spawned+OnRoad 1
- byPath: ready 667、none 5
- bySeenStopped: <1day 164、7days+ 508
- byTarget: 行き先なし 15台。ほかは店・工場ごとに3台
- samples 20台: 見回り1と同じ車(8、36、120、156、183、307、339、341、377、410)が seenStoppedDays 20 で (3441,-1555) に残る。152、464 は 10。新しく見えた車(34、103、212、229、336、368)は 0。WaitingSpace の車は blockCounter 0、waitCounter 0
- 駅の外で見えた車: 87(Goods、(-809,-732)、Importing+OnRoad+Blocked、blockCounter 22)、304(Goods、(2382,-1238)、Congestion+OnRoad。見回り1では駅の中で WaitingSpace)

### `cargo()`

- trucks 2,090、stoppedTrucks 883(道の上 368、建物の中 515)
- stoppedInBuildingsTop: 28755 Cargo Center 515 のみ
- 駅28755: vehiclesLeaving 799、vehiclesArriving 10
- 駅13893: vehiclesLeaving 0、vehiclesArriving 0
- 港1366 は出164・入5、46112 は出19・入3、32211 は出0・入1。ほかの貨物駅は出入り0
- stoppedSpots: (3434,-1544) 72、(2259,-924) 20、(3948,-274) 19、(3455,-1339) 19、(-1908,98) 17
- byCargo の止まった台数: Goods 566、Lumber 93、Petrol 85、Coal 80、Food 59
- shortages: noGoods 228棟、noResources 26棟

### `traffic(x=3439, z=-1551, radius=60, limit=10)`

- flow 50、cars 15、blocked 0、congestion 1、roadSegments 3、averageDensity 15
- busiest: 20316 Large Road (3400,-1530) density 46
- blockedSpots: なし

## 月末(2050-01-31)

### `vehicles_stuck(kind="truck", building=28755, limit=20)`

- vehicles 611
- byState: WaitingSpace+Importing+InGrounds 498、WaitingSpace+Importing+OnRoad 59、Importing+Spawned+OnRoad+Blocked 41、GoingBack+Importing+Spawned+OnRoad+Blocked 9、GoingBack+Importing+Spawned+InGrounds 2、Importing+Spawned+InGrounds+Blocked 1、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 607、none 4
- bySeenStopped: <1day 120、7days+ 491
- byTarget: 行き先なし 12台。ほかは店・工場ごとに3〜4台
- samples 20台: 8、36、120、156、183、307、339、341、377、410 が seenStoppedDays 30.1 で (3441,-1555) に残る。152、464 は 20。34、103、212、229、336、368 は 10.1。388 は 0。WaitingSpace の車は blockCounter 0、waitCounter 0
- 駅の外で見えた車: 210(Goods 空、(1308,-743)、GoingBack+OnRoad+Blocked、blockCounter 20)

### `cargo()`

- trucks 2,130、stoppedTrucks 847(道の上 344、建物の中 503)
- stoppedInBuildingsTop: 28755 Cargo Center 498、1366 Cargo Harbor 3、10535 Mediumfactory08 1、41933 Shop04 1
- 駅28755: vehiclesLeaving 788、vehiclesArriving 12
- 駅13893: vehiclesLeaving 0、vehiclesArriving 0
- 港1366 は出156・入6、46112 は出26・入3、32211 は出0・入1。ほかの貨物駅は出入り0
- stoppedSpots: (3441,-1555) 59、(2150,-879) 20、(-1708,95) 14、(2762,-1077) 14、(3679,-246) 10
- byCargo の止まった台数: Goods 548、Lumber 98、Petrol 80、Coal 71、Food 50
- shortages: noGoods 225棟、noResources 29棟

### `traffic(x=3439, z=-1551, radius=60, limit=10)`

- flow 53、cars 13、blocked 0、congestion 1、roadSegments 3、averageDensity 10
- busiest: 20316 Large Road (3400,-1530) density 32
- blockedSpots: なし
