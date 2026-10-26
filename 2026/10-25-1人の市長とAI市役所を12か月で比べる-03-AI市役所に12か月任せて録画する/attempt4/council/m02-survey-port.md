# m02 調査 s02-1(port): 貨物駅28755 の549台が動かない理由

問い: 貨物駅28755 の敷地の中で549台が同じ位置 (3441,-1555) で動かないのは、出口の道が詰まっているからか、駅の中の車線の作りの問題か

m02-1(z=-1340 の出口の東西路を Small 4 Lane Road に差し替え)は 2050-01-31 に実行済み。新しい区間は segment 11398・15487。

## 見回り1(2050-02-10)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 689
- byState: WaitingSpace+Importing+InGrounds 568、WaitingSpace+Importing+OnRoad 60、Importing+Spawned+OnRoad+Blocked 41、GoingBack+Importing+Spawned+OnRoad+Blocked 19、Congestion+Importing+Spawned+OnRoad+Blocked 1
- byPath: ready 689
- bySeenStopped: <1day 152、7days+ 537
- samples 30台のうち WaitingSpace の車は全部 (3441,-1555)、blockCounter 0、waitCounter 0。seenStoppedDays 40 の車が多い
- 荷物: Goods、Petrol、Lumber。行き先の距離は 196〜6,342m
- OnRoad+Blocked の例: vehicle 546 (2208,-226) blockCounter 36、vehicle 24 (2196,-701) GoingBack blockCounter 8

### `traffic(x=3449, z=-1555, radius=120)`

- flow 52、cars 14、blocked 0、congestion 1、roadSegments 9、averageDensity 7
- busiest: segment 17311 Large Road (3400,-1458) 密度35、20316 Large Road (3400,-1530) 密度28
- blockedSpots なし

### `cargo()`

- trucks 2,145、stoppedTrucks 929、stoppedOnRoads 345、stoppedInBuildings 584
- stoppedInBuildingsTop: 28755 Cargo Center 568、1366 Cargo Harbor 15、1898 Shop 1
- stations 28755: vehiclesLeaving 849、vehiclesArriving 11。ほかの Cargo Center 7つは出入り0
- stoppedSpots: (3441,-1555) 60、(-1944,134) 24、(2231,-1097) 19、(726,-690) 16、(2916,-1244) 14
- shortages: noGoods 218(spots (-1094,-805) 68、(2252,773) 47、(1211,324) 34)、noResources 31(spots (2261,1260) 14、(2868,-903) 12、(1916,1390) 2)

## 見回り2(2050-02-20)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 689
- byState: WaitingSpace+Importing+InGrounds 580、WaitingSpace+Importing+OnRoad 55、Importing+Spawned+OnRoad+Blocked 34、GoingBack+Importing+Spawned+OnRoad+Blocked 16、GoingBack+Importing+Spawned+InGrounds 2、Congestion+Importing+Spawned+OnRoad+Blocked 1、Congestion+GoingBack+Importing+Spawned+OnRoad+Blocked 1
- byPath: ready 687、none 2
- bySeenStopped: <1day 150、7days+ 539
- samples の WaitingSpace の車は全部 (3441,-1555)、blockCounter 0、waitCounter 0。seenStoppedDays 50.1 の車が多い(vehicle 8、36、664、670、675、1030、1063、1137、1180、1189、1202)
- 荷物: Goods、Food、Lumber、Petrol、Coal。行き先の距離は 326〜6,062m
- OnRoad+Blocked の例: vehicle 112 (3272,-1238) blockCounter 1、vehicle 551 (3496,-1358) blockCounter 1、vehicle 24 (2156,-905) GoingBack blockCounter 17、vehicle 260 (1407,-751) GoingBack blockCounter 27
- vehicle 304 GoingBack+InGrounds (3429,-1559) path none

### `traffic(x=3449, z=-1555, radius=120)`

- flow 51、cars 15、blocked 0、congestion 1、roadSegments 9、averageDensity 9
- busiest: segment 17311 Large Road (3400,-1458) 密度45、20316 Large Road (3400,-1530) 密度40
- blockedSpots なし

### `cargo()`

- trucks 2,127、stoppedTrucks 900、stoppedOnRoads 319、stoppedInBuildings 581
- stoppedInBuildingsTop: 28755 Cargo Center 580、3063 Shop 1
- stations 28755: vehiclesLeaving 867、vehiclesArriving 11。1366 Cargo Harbor: leaving 133、arriving 6。ほかの Cargo Center 7つは出入り0
- stoppedSpots: (3441,-1555) 55、(2161,-876) 15、(2880,-946) 13、(2761,-1096) 13、(3100,-234) 12
- shortages: noGoods 222(spots (-1084,-854) 65、(2255,804) 49、(1210,333) 35)、noResources 35(spots (2903,-832) 14、(2260,1249) 13、(3996,-298) 4)

## 月末(2050-03-02)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 678
- byState: WaitingSpace+Importing+InGrounds 575、WaitingSpace+Importing+OnRoad 56、Importing+Spawned+OnRoad+Blocked 25、GoingBack+Importing+Spawned+OnRoad+Blocked 18、GoingBack+Importing+Spawned+InGrounds 3、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 674、none 4
- bySeenStopped: <1day 127、7days+ 551
- samples の WaitingSpace の車は全部 (3441,-1555)、blockCounter 0、waitCounter 0。seenStoppedDays 60 の車が多い(vehicle 8、36、664、670、675、1030、1180、1202、1229)。seenStoppedDays 0 の WaitingSpace の車もある(178、396、625、641、870、988)
- 荷物: Goods、Food、Lumber、Petrol。行き先の距離は 685〜5,846m
- vehicle 24 は GoingBack+InGrounds (3409,-1560) path none、seen 20日
- OnRoad+Blocked の例: vehicle 189 (1423,-752) GoingBack blockCounter 46、vehicle 546 (2196,-774) GoingBack blockCounter 8、vehicle 1207 (-1072,-497) GoingBack blockCounter 6

### `traffic(x=3449, z=-1555, radius=120)`

- flow 51、cars 14、blocked 0、congestion 1、roadSegments 9、averageDensity 9
- busiest: segment 17311 Large Road (3400,-1458) 密度48、20316 Large Road (3400,-1530) 密度38
- blockedSpots なし

### `cargo()`

- trucks 2,129、stoppedTrucks 915、stoppedOnRoads 340、stoppedInBuildings 575
- stoppedInBuildingsTop: 28755 Cargo Center 575 のみ
- stations 28755: vehiclesLeaving 862、vehiclesArriving 12。1366 Cargo Harbor: leaving 144、arriving 6。46112 Cargo Harbor: leaving 23、arriving 3。ほかの Cargo Center 7つは出入り0
- stoppedSpots: (3438,-1547) 60、(-1910,105) 20、(913,-710) 14、(3703,-246) 12、(-1889,-847) 9
- byCargo の stoppedTrucks: Goods 594、Petrol 101、Lumber 92、Coal 66、Food 62
- shortages: noGoods 227(spots (-1106,-916) 70、(2253,795) 45、(1109,317) 36)、noResources 33(spots (2891,-844) 14、(2262,1280) 11、(4029,-306) 3)
