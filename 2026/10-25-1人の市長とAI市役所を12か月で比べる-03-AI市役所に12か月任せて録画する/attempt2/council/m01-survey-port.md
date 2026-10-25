# s01-1 貨物駅28755で止まったトラックの原因(port)

問い: 貨物駅28755で止まったトラック492台は、出口の道の詰まりで動けないのか、入口側の空きを待っているのか

## 見回り1(2050-01-11)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 613
- byState: WaitingSpace+Importing+InGrounds 508、WaitingSpace+Importing+OnRoad 63、Importing+Spawned+OnRoad+Blocked 23、GoingBack+Importing+Spawned+OnRoad+Blocked 17、Importing+Spawned+InGrounds 2
- byPath: ready 611、none 2
- bySeenStopped: <1day 134、7days+ 479
- samples 30台: 位置はほぼ全部 (3441, -1555)。blockCounter 0、waitCounter 0。荷は Goods が多く、Coal、Food、Petrol、Lumber も。行き先までの距離 196〜6,296m
- byTarget: building 0(行き先なし)17台。ほかは店・工場ごとに2〜4台

### `cargo()`

- trucks 2,088、stoppedTrucks 835(stoppedOnRoads 307、stoppedInBuildings 528)
- stoppedInBuildingsTop: 28755 Cargo Center 508、1366 Cargo Harbor 16、46112 Cargo Harbor 4
- stations: 28755 vehiclesLeaving 780 / vehiclesArriving 12。同じ種類の Cargo Center 3940、4740、13893、14580、16572、40031、48243 は出入り0
- byCargo の stoppedTrucks: Goods 532、Petrol 91、Lumber 87、Coal 78、Food 47
- stoppedSpots の1位: (3440, -1552) 64台
- shortages: noGoods 241(多い場所 (-1076, -785) 80、(2215, 735) 45、(1098, 297) 33)、noResources 23

### `traffic(x=3449, z=-1555, radius=300)`

- flow 50、cars 51、blocked 1(道の上1、建物の中0)、congestion 7、区間23、averageDensity 33
- busiest: segment 17690 Basic Road (3480, -1315) 98、28970 Basic Road (3440, -1340) 89、31488 Basic Road (3279, -1340) 72、18170 Small 4 Lane Road (3400, -1380) 64、11279 Small 4 Lane Road (3360, -1340) 60
- blockedSpots: (3418, -1417) 1台

## 見回り2(2050-01-21)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 636
- byState: WaitingSpace+Importing+InGrounds 518、WaitingSpace+Importing+OnRoad 63、Importing+Spawned+OnRoad+Blocked 38、GoingBack+Importing+Spawned+OnRoad+Blocked 11、GoingBack+Importing+Spawned+InGrounds 3、Importing+Spawned+InGrounds 2、Congestion+Importing+Spawned+OnRoad 1
- byPath: ready 631、none 5
- bySeenStopped: <1day 127、7days+ 509
- samples 30台: 敷地の中の車は (3441, -1555)、blockCounter 0、waitCounter 0。見回り1と同じ車(8、36、120、156、183、307、339、341 など)が seenStoppedDays 20.1。道の上で Blocked の車は (2670, 720)、(-769, -733)、(-248, -727) で blockCounter 14〜30
- byTarget: building 0 14台。ほかは2〜4台

### `cargo()`

- trucks 2,103、stoppedTrucks 835(stoppedOnRoads 317、stoppedInBuildings 518)
- stoppedInBuildingsTop: 28755 Cargo Center 518(ほかの駅・港は上位に出ない)
- stations: 28755 vehiclesLeaving 788 / vehiclesArriving 13。ほかの Cargo Center 7つは出入り0
- byCargo の stoppedTrucks: Goods 529、Lumber 90、Petrol 89、Coal 79、Food 48
- stoppedSpots: (3438, -1546) 68、(2760, -1092) 17、(3913, -257) 14、(4090, -257) 12、(2110, -885) 12
- shortages: noGoods 238(多い場所 (-1077, -789) 75、(2208, 791) 42、(1030, 295) 34)、noResources 27

### `traffic(x=3449, z=-1555, radius=300)`

- flow 51、cars 54、blocked 0、congestion 6、区間23、averageDensity 36
- busiest: segment 17690 Basic Road (3480, -1315) 91、11279 Small 4 Lane Road (3360, -1340) 85、28970 Basic Road (3440, -1340) 76、18170 Small 4 Lane Road (3400, -1380) 76、31488 Basic Road (3279, -1340) 73
- blockedSpots: なし

## 月末(2050-01-31)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 626
- byState: WaitingSpace+Importing+InGrounds 520、WaitingSpace+Importing+OnRoad 65、GoingBack+Importing+Spawned+OnRoad+Blocked 21、Importing+Spawned+OnRoad+Blocked 18、WaitingPath+GoingBack+Importing+Spawned+OnRoad 1、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 625、none 1
- bySeenStopped: <1day 138、7days+ 488
- samples 30台: 全部 WaitingSpace、位置 (3441, -1555)、blockCounter 0、waitCounter 0。見回り1から見ている車(8、36、120、156、183、307、339、341、377、410、467、469、522、529、535、572、574、575、579)が seenStoppedDays 30.1
- byTarget: building 0 23台。ほかは3〜4台

### `cargo()`

- trucks 2,066、stoppedTrucks 822(stoppedOnRoads 301、stoppedInBuildings 521)
- stoppedInBuildingsTop: 28755 Cargo Center 520、1366 Cargo Harbor 1
- stations: 28755 vehiclesLeaving 792 / vehiclesArriving 12。ほかの Cargo Center 7つは出入り0
- byCargo の stoppedTrucks: Goods 516、Lumber 93、Petrol 89、Coal 75、Food 49
- stoppedSpots: (3441, -1555) 65、(3509, -247) 15、(-1738, 92) 13、(-899, -706) 8、(-1831, -873) 7
- shortages: noGoods 233(多い場所 (-1056, -767) 72、(2241, 788) 43、(1052, 319) 34)、noResources 28

### `traffic(x=3449, z=-1555, radius=300)`

- flow 51、cars 40、blocked 0、congestion 3、区間23、averageDensity 25
- busiest: segment 31488 Basic Road (3279, -1340) 78、17690 Basic Road (3480, -1315) 70、18170 Small 4 Lane Road (3400, -1380) 59、11279 Small 4 Lane Road (3360, -1340) 52、28970 Basic Road (3440, -1340) 49
- blockedSpots: なし
