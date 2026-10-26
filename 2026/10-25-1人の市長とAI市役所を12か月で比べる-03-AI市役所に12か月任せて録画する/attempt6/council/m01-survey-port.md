# m01 調査 s01-1(port): 貨物駅28755の敷地で止まるトラックの原因

問い: 貨物駅28755の敷地で WaitingSpace のまま動かないのは、出口の道が詰まるからか、駅の車の出し方の上限か。

## 見回り1(2050-01-11)

### `vehicles_stuck`(kind="truck", building=28755, limit=15)

- vehicles 619
- byState: WaitingSpace+Importing+InGrounds 511、WaitingSpace+Importing+OnRoad 63、Importing+Spawned+OnRoad+Blocked 27、GoingBack+Importing+Spawned+OnRoad+Blocked 16、WaitingTarget+Importing+Spawned+InGrounds 1、GoingBack+Importing+Spawned+InGrounds 1
- byPath: ready 617、none 2
- bySeenStopped: <1day 147、7days+ 472
- samples 15台: うち WaitingSpace の14台はすべて位置 (3441,-1555)、blockCounter 0、waitCounter 0。荷は Goods 9、Coal 1、Food 1、Petrol 2、Lumber 1。行き先までの距離 971〜6,296m。Blocked の1台(vehicle 260)は (1594,-763)、blockCounter 12

### `traffic`(x=3420, z=-1555, radius=150)

- flow 51、cars 19、blocked 0、congestion 1、roadSegments 11、averageDensity 10
- busiest: 17311 Large Road (3400,-1458) 31、20316 Large Road (3400,-1530) 27、14098 Small 4 Lane Road (3467,-1416) 27、10573 Small 4 Lane Road (3429,-1418) 25
- blockedSpots: なし

### `cargo`(引数なし)

- trucks 2,264、stoppedTrucks 857、stoppedOnRoads 329、stoppedInBuildings 528
- stoppedInBuildingsTop: 28755 Cargo Center 511、1366 Cargo Harbor 15、46112 Cargo Harbor 2
- stations: 28755 leaving 783 / arriving 12、1366 leaving 161 / arriving 5、46112 leaving 42 / arriving 2、32211 0/1。ほかの Cargo Center 7棟(3940、4740、13893、14580、16572、40031、48243)は 0/0
- byCargo: Goods import 915 / local 592 / stopped 553、Coal import 133 / stopped 75、Food import 231 / stopped 54、Lumber import 193 / stopped 87、Petrol import 177 / stopped 87
- stoppedSpots 上位: (3440,-1552) 64、(1662,-759) 19、(2145,-882) 13、(1498,-757) 12、(2228,-1073) 11
- shortages: noGoods 235、noResources 25

## 見回り2(2050-01-21)

### `vehicles_stuck`(kind="truck", building=28755, limit=15)

- vehicles 645
- byState: WaitingSpace+Importing+InGrounds 517、WaitingSpace+Importing+OnRoad 63、Importing+Spawned+OnRoad+Blocked 43、GoingBack+Importing+Spawned+OnRoad+Blocked 19、GoingBack+Importing+Spawned+InGrounds 2、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 642、none 3
- bySeenStopped: <1day 130、7days+ 515
- samples 15台: WaitingSpace の13台はすべて位置 (3441,-1555)、blockCounter 0、waitCounter 0。うち8台(vehicle 8、36、120、156、183、307 ほか)は seenStoppedDays 20(見回り1と同じ車)、vehicle 152 は10、5台は0。Blocked の2台: vehicle 189 (45,-717) blockCounter 14、vehicle 260 (1653,-201) blockCounter 65(見回り1では (1594,-763))

### `traffic`(x=3420, z=-1555, radius=150)

- flow 48、cars 20、blocked 0、congestion 1、roadSegments 11、averageDensity 11
- busiest: 17311 Large Road (3400,-1458) 48、20316 Large Road (3400,-1530) 35、10573 Small 4 Lane (3429,-1418) 23、14098 Small 4 Lane (3467,-1416) 17
- blockedSpots: なし

### `cargo`(引数なし)

- trucks 2,240、stoppedTrucks 893、stoppedOnRoads 376、stoppedInBuildings 517
- stoppedInBuildingsTop: 28755 Cargo Center 517 のみ
- stations: 28755 leaving 774 / arriving 11、1366 155/5、46112 22/3、32211 0/1。ほかの Cargo Center 7棟は 0/0
- byCargo: Goods import 890 / local 596 / stopped 573、Coal import 135 / stopped 77、Food import 229 / stopped 60、Lumber import 194 / stopped 91、Petrol import 176 / stopped 92
- stoppedSpots 上位: (3437,-1543) 70、(-1922,117) 27、(-1733,97) 22、(3943,-268) 17、(4058,-304) 13
- shortages: noGoods 224、noResources 27

## 月末(2050-01-31)

### `vehicles_stuck`(kind="truck", building=28755, limit=15)

- vehicles 622
- byState: WaitingSpace+Importing+InGrounds 513、WaitingSpace+Importing+OnRoad 68、Importing+Spawned+OnRoad+Blocked 30、GoingBack+Importing+Spawned+OnRoad+Blocked 8、Importing+Spawned+InGrounds 2、WaitingPath+Importing+Spawned+OnRoad 1
- byPath: ready 620、none 2
- bySeenStopped: <1day 114、7days+ 508
- samples 15台: WaitingSpace の13台はすべて位置 (3441,-1555)、blockCounter 0、waitCounter 0。seenStoppedDays 30.1 が5台(vehicle 8、36、120、156、183。見回り1から同じ車)、20 が1台(152)、10 が6台、0 が1台(169)。Blocked の2台: vehicle 210 (2137,-1052) blockCounter 9、vehicle 260 (1467,11) blockCounter 32、seenStoppedDays 20

### `traffic`(x=3420, z=-1555, radius=150)

- flow 50、cars 22、blocked 0、congestion 1、roadSegments 11、averageDensity 12
- busiest: 17311 Large Road (3400,-1458) 43、20316 Large Road (3400,-1530) 34、10573 Small 4 Lane (3429,-1418) 34、14098 Small 4 Lane (3467,-1416) 29
- blockedSpots: なし

### `cargo`(引数なし)

- trucks 2,310、stoppedTrucks 868、stoppedOnRoads 355、stoppedInBuildings 513
- stoppedInBuildingsTop: 28755 Cargo Center 513 のみ
- stations: 28755 leaving 775 / arriving 12、1366 158/5、46112 23/3、32211 0/1。ほかの Cargo Center 7棟は 0/0
- byCargo: Goods import 903 / local 649 / stopped 562、Coal import 138 / stopped 75、Food import 229 / stopped 49、Lumber import 192 / stopped 91、Petrol import 177 / stopped 91
- stoppedSpots 上位: (3436,-1541) 78、(-1940,110) 25、(2528,-947) 16、(3884,-269) 13、(2764,-1100) 11
- shortages: noGoods 218(上位 (-1032,-752) 67、(2209,729) 42、(1077,312) 33)、noResources 30(上位 (2298,1305) 13、(2774,-942) 10、(3901,-351) 3)
