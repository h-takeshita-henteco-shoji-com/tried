# m01 調査 s01-1(port): 貨物駅28755 の敷地でトラックが止まり続けるか

問い: 貨物駅28755 の敷地で、トラック492台はなぜ出られず WaitingSpace のまま動かないのか

## 見回り1(2050-01-11)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 629
- byState: WaitingSpace+Importing+InGrounds 509、WaitingSpace+Importing+OnRoad 61、Importing+Spawned+OnRoad+Blocked 45、GoingBack+Importing+Spawned+OnRoad+Blocked 11、GoingBack+Importing+Spawned+InGrounds 2、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 626、none 3
- bySeenStopped: <1day 153、7days+ 476
- byTarget の上位: building 0(行き先なし)14台。ほかは店ごとに3〜4台
- samples(30台): WaitingSpace の車は全部 位置 (3441, -1555)、blockCounter 0、waitCounter 0、path ready。荷は Goods が多く、ほかに Coal、Food、Petrol、Lumber。行き先までの距離は 196〜6,296m。Blocked の車の例は (2168, -924)(blockCounter 73)、(78, -155)

### `cargo()`

- trucks 2,104、stoppedTrucks 847(道の上 320、敷地の中 527)
- stoppedInBuildingsTop: 貨物駅28755 509、Cargo Harbor 1366 16、Cargo Harbor 46112 2
- byCargo の stoppedTrucks: Goods 554、Petrol 89、Lumber 85、Coal 72、Food 46、Oil 1
- stoppedSpots: (3437, -1543) 69、(898, -707) 20、(2146, -909) 14、(2706, -949) 13、(-678, -734) 11
- stations: 28755 は出 792 / 入 11。Cargo Harbor 1366 出 172 / 入 5、46112 出 40 / 入 2、32211 出 0 / 入 1。ほかの Cargo Center 7つ(3940、4740、13893、14580、16572、40031、48243)は出入り 0
- shortages: noGoods 237(多い場所 (-1079,-783) 82、(2214,747) 44、(1098,297) 33)、noResources 23((2331,1293) 10、(2868,-806) 8、(1916,1390) 2)

### `traffic(x=3449, z=-1555, radius=400)`

- cars 98、blocked 0、congestion 14、roadSegments 35、averageDensity 35
- busiest: segment 28970 Basic Road (3440,-1340) 100、12917 (3120,-1340) 85、27961 (3200,-1340) 85、31488 (3279,-1340) 84、19358 (3439,-1240) 80、17690 (3480,-1315) 79、28685 Small 4 Lane (3480,-1265) 63
- blockedSpots: なし

## 見回り2(2050-01-21)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 702
- byState: WaitingSpace+Importing+InGrounds 564、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 55、GoingBack+Importing+Spawned+OnRoad+Blocked 17、Congestion+GoingBack+Importing+Spawned+OnRoad+Blocked 1、WaitingPath+Importing+Spawned+OnRoad 1
- byPath: ready 702
- bySeenStopped: <1day 162、7days+ 540
- byTarget の上位: building 0 18台。ほかは店ごとに3〜4台
- samples(30台): WaitingSpace の車は全部 (3441, -1555)、blockCounter 0、waitCounter 0。見回り1と同じ車(8、36、307、339、341、377、410、467、469、522、529、535、550、551、572、574)が seenStoppedDays 20 で同じ位置。Blocked の車の位置は (3495,-1343)、(3404,-1362)、(3404,-1370)、(-706,-732)、(-696,-732)

### `cargo()`

- trucks 2,062、stoppedTrucks 954(道の上 390、敷地の中 564)
- stoppedInBuildingsTop: 貨物駅28755 564 のみ
- byCargo の stoppedTrucks: Goods 606、Petrol 102、Lumber 98、Coal 75、Food 72、Ore 1
- stoppedSpots: (3439,-1547) 68、(3463,-1317) 25、(2142,-893) 22、(-1933,120) 20、(4067,-293) 16
- stations: 28755 出 819 / 入 10。1366 出 166 / 入 5、46112 出 13 / 入 3、32211 出 0 / 入 1。ほかの Cargo Center 7つは出入り 0
- shortages: noGoods 235((-1089,-817) 77、(2207,785) 43、(1065,302) 34)、noResources 25((2308,1313) 12、(2863,-794) 6、(3901,-351) 3)

### `traffic(x=3449, z=-1555, radius=400)`

- cars 101、blocked 9、congestion 15、roadSegments 35、averageDensity 37
- busiest: 19358 Basic Road (3439,-1240) 100、17690 Basic Road (3480,-1315) 100、28685 Small 4 Lane (3480,-1265) 100、31488 (3279,-1340) 100、28970 (3440,-1340) 100、682 (3489,-1340) 100、11279 Small 4 Lane (3360,-1340) 93
- blockedSpots: (3473,-1246) 9

## 月末(2050-01-31)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 683
- byState: WaitingSpace+Importing+InGrounds 549、WaitingSpace+Importing+OnRoad 63、Importing+Spawned+OnRoad+Blocked 59、GoingBack+Importing+Spawned+OnRoad+Blocked 11、Importing+Spawned+InGrounds 1
- byPath: ready 682、none 1
- bySeenStopped: <1day 122、7days+ 561
- byTarget の上位: building 0 11台。ほかは店ごとに3〜4台
- samples(30台): WaitingSpace の車は全部 (3441, -1555)、blockCounter 0、waitCounter 0。見回り1から同じ車(8、36、307、339、341、377、410、467、469、522、529、535、550、551、572、574、575、579、589、601、607)が seenStoppedDays 30。Blocked の車の位置は (1759,-887)、(1722,-805)、(1725,-801)、(2214,-950)

### `cargo()`

- trucks 2,115、stoppedTrucks 914(道の上 364、敷地の中 550)
- stoppedInBuildingsTop: 貨物駅28755 549、Cargo Harbor 1366 1
- byCargo の stoppedTrucks: Goods 565、Petrol 107、Lumber 106、Coal 68、Food 68
- stoppedSpots: (3433,-1539) 83、(2163,-898) 18、(-1718,93) 16、(-1930,107) 15、(3887,-251) 14
- stations: 28755 出 837 / 入 11。1366 出 151 / 入 5、46112 出 23 / 入 2、32211 出 0 / 入 1。ほかの Cargo Center 7つは出入り 0
- shortages: noGoods 229((-1085,-799) 73、(2239,754) 47、(1117,318) 35)、noResources 27((2304,1294) 12、(2842,-915) 9、(3901,-351) 3)

### `traffic(x=3449, z=-1555, radius=400)`

- cars 86、blocked 0、congestion 18、roadSegments 35、averageDensity 40
- busiest: 11279 Small 4 Lane (3360,-1340) 100、31488 Basic (3279,-1340) 100、17690 Basic (3480,-1315) 98、28970 Basic (3440,-1340) 95、27961 (3200,-1340) 80、19358 (3439,-1240) 80
- blockedSpots: なし
