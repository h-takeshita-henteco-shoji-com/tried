# m03 調査 s03-1 の結果(port)

問い: 28755 の敷地の中で60日動かない車は、出口の点(3441,-1555)の先頭の車が動かないことで列が止まっているのか。
見立ては書かない。局が翌月に読んで決める。

参考(実行の直前、2050-03-02): `cargo()` の stoppedInBuildings 555(28755 は534)、stoppedSpots の先頭 3441,-1555 が51台、28755 の vehiclesLeaving 807。m03-1(放棄された建物121棟の取り壊し)を同じ日に打った。直後の `cargo()` でも stoppedInBuildings 555・28755 は534 のまま。

## 見回り1(2050-03-12)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 668
- byState: WaitingSpace+Importing+InGrounds 531、WaitingSpace+Importing+OnRoad 72、Importing+Spawned+OnRoad+Blocked 43、GoingBack+Importing+Spawned+OnRoad+Blocked 13、GoingBack+Importing+Spawned+InGrounds 4、Importing+Spawned+InGrounds 2、Congestion+Importing+Spawned+OnRoad+Blocked 1、WaitingPath+GoingBack+Importing+Spawned+OnRoad 1、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 661、none 7
- bySeenStopped: <1day 190、7days+ 478
- byTarget(上位10): building 0(行き先なし)19、ほかは 32056 H3 3x4 Hotel(1856,183)、42545 H3 4x3 Shop03(-600,132)、48978 H3 4x4 Shop11(-2136,-1166)、44532 Future Store(-840,-14)、36210 Future Store(-2616,-194)、40392 Future Store(-456,132)、42379 Future Store(2368,986)、43021 H3 3x4 Hotel(2343,854)、35149 H3 4x4 Shop07a(1856,-541)が各3台
- samples 30台: WaitingSpace の車は全部 x 3441, z -1555(同じ点)、blockCounter 0、waitCounter 0、path ready。WaitingSpace+OnRoad の vehicle 664 も同じ点 3441,-1555。seenStoppedDays は 70.1 が8台(8、307、339、341、664、670、675、880)、60.1 が2台(797、891)、50 が3台、30 が2台、20 が1台、10 が2台、0 が7台(WaitingSpace の中)。行き先までの距離は 932〜6026m。荷は Goods・Petrol・Lumber・Food・Coal
- 走っている側: vehicle 87(1584,-768、blockCounter 12)、189(2068,-954、blockCounter 18)、616(3368,-1341、blockCounter 1)、758(2781,-949、blockCounter 5、Congestion)

### `cargo()`

- stoppedInBuildings 531(全部 28755)。stoppedOnRoads 378、stoppedTrucks 909
- stoppedSpots: 3436,-1542 が82台(先頭)、2231,-1080 が18、2148,-881 が14、2246,-908 が13、-1713,98 が12
- 28755: vehiclesLeaving 823、vehiclesArriving 13
- shortages: noGoods 141、noResources 25

### `traffic(x=3441, z=-1555, radius=150)`

- flow 51、cars 27、blocked 0(onRoads 0、inBuildings 0)、congestion 1、roadSegments 11、averageDensity 11
- busiest: 区間17311 Large Road(3400,-1458)52、20316 Large Road(3400,-1530)46、10573 Small 4 Lane Road(3429,-1418)24、14098 Small 4 Lane Road(3467,-1416)6
- blockedSpots: なし

## 見回り2(2050-03-22)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 668
- byState: WaitingSpace+Importing+InGrounds 561、WaitingSpace+Importing+OnRoad 69、Importing+Spawned+OnRoad+Blocked 22、GoingBack+Importing+Spawned+OnRoad+Blocked 9、Congestion+Importing+Spawned+OnRoad 3、GoingBack+Importing+Spawned+InGrounds 2、GoingBack+Importing+Spawned+InGrounds+Blocked 1、Importing+Spawned+InGrounds 1
- byPath: ready 664、none 4
- bySeenStopped: <1day 154、7days+ 514
- byTarget(上位10): building 0(行き先なし)12、41185 H3 4x4 Shop04(-876,132)3、48978 H3 4x4 Shop11(-2136,-1166)3、539 H3 4x3 Shop12(-2216,-1170)3、44532 Future Store(-840,-14)3、47527 H3 3x4 Shop16_c(-1620,-1214)3、36210 Future Store(-2616,-194)3、35149 H3 4x4 Shop07a(1856,-541)3、38221 Future Store(-1340,-584)3、47622 H3 3x4 Hotel(-1364,-1574)2
- samples 30台: WaitingSpace の29台は全部 x 3441, z -1555、blockCounter 0、waitCounter 0、path ready。見回り1と同じ車(8、307、339、341、664、670、675、880)は seenStoppedDays 80 で、同じ点に残る。797・891 は70、229・667 は60、200・308 は40。見回り1で seenStoppedDays 0 だった 235・252・266・273・442・488 は10、343 は10。新しく0日の車は 110・253・294・479・694・924。行き先までの距離は 244〜6329m
- 走っている側: vehicle 909(1800,-934、blockCounter 24、Importing+Spawned+OnRoad+Blocked)

### `cargo()`

- stoppedInBuildings 581(28755 は562、Cargo Harbor 46112 は16、ほか店・工場が各1)。stoppedOnRoads 260、stoppedTrucks 841
- stoppedSpots: 3441,-1555 が69台(先頭)、-1709,98 が18、2133,-891 が8、2228,-930 が8、-649,93 が8
- 28755: vehiclesLeaving 848、vehiclesArriving 11
- shortages: noGoods 145、noResources 26

### `traffic(x=3441, z=-1555, radius=150)`

- flow 55、cars 23、blocked 0(onRoads 0、inBuildings 0)、congestion 1、roadSegments 11、averageDensity 14
- busiest: 区間17311 Large Road(3400,-1458)53、20316 Large Road(3400,-1530)50、10573 Small 4 Lane Road(3429,-1418)31、14098 Small 4 Lane Road(3467,-1416)22
- blockedSpots: なし

## 月末(2050-04-01)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 701
- byState: WaitingSpace+Importing+InGrounds 569、WaitingSpace+Importing+OnRoad 58、Importing+Spawned+OnRoad+Blocked 55、GoingBack+Importing+Spawned+OnRoad+Blocked 15、GoingBack+Importing+Spawned+InGrounds 2、Congestion+Importing+Spawned+OnRoad+Blocked 1、WaitingTarget+Importing+Spawned+InGrounds 1
- byPath: ready 698、none 3
- bySeenStopped: <1day 137、7days+ 564
- byTarget(上位10): building 0(行き先なし)18、48978 H3 4x4 Shop11(-2136,-1166)3、36210 Future Store(-2616,-194)3、47126 Future Store(332,34)3、33597 H3 4x3 Shop13(-2284,-1034)3、44532 Future Store(-840,-14)3、47527 H3 3x4 Shop16_c(-1620,-1214)3、35149 H3 4x4 Shop07a(1856,-541)3、42545 H3 4x3 Shop03(-600,132)3、47716 H3 4x4 Shop17_c(-2564,-104)3
- samples 30台: WaitingSpace の29台は全部 x 3441, z -1555、blockCounter 0、waitCounter 0、path ready。8・307・339・341・664・670・675 は seenStoppedDays 90(見回り1から同じ点に残る。880 はこの30台の中に出ない)。229・667 は70、200・308 は49.9、204・400 は30、235・252・266・273・343・442・488 は19.9、110・253・294・479 は10。新しく0日の車は 27・61・275・316・567。行き先までの距離は 244〜6363m
- 走っている側: vehicle 151(1556,-763、blockCounter 1、GoingBack+OnRoad+Blocked)

### `cargo()`

- stoppedInBuildings 569(全部 28755)。stoppedOnRoads 385、stoppedTrucks 954
- stoppedSpots: 3436,-1541 が67台(先頭)、2230,-1091 が19、2142,-891 が18、2279,-1234 が15、2762,-1094 が14
- 28755: vehiclesLeaving 843、vehiclesArriving 12
- shortages: noGoods 166(-1129,-1102 に39、2257,749 に39、916,263 に28)、noResources 29

### `traffic(x=3441, z=-1555, radius=150)`

- flow 55、cars 24、blocked 0(onRoads 0、inBuildings 0)、congestion 1、roadSegments 11、averageDensity 13
- busiest: 区間17311 Large Road(3400,-1458)46、20316 Large Road(3400,-1530)40、10573 Small 4 Lane Road(3429,-1418)31、14098 Small 4 Lane Road(3467,-1416)28
- blockedSpots: なし

## 3回の並び(事実だけ)

| 日付 | 28755 の敷地の中(cargo) | WaitingSpace+InGrounds | WaitingSpace+OnRoad | 7days+ | <1day | 28755 の vehiclesLeaving | 出口の周り150mの blocked | noGoods / noResources |
|---|---|---|---|---|---|---|---|---|
| 03-02(実行の直前と直後) | 534 | - | - | - | - | 807 | - | 229→123 / 34→24 |
| 03-12 | 531 | 531 | 72 | 478 | 190 | 823 | 0 | 141 / 25 |
| 03-22 | 562 | 561 | 69 | 514 | 154 | 848 | 0 | 145 / 26 |
| 04-01 | 569 | 569 | 58 | 564 | 137 | 843 | 0 | 166 / 29 |
