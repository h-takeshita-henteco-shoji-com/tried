# s01-1 貨物駅28755 の空き待ちの原因を見分ける(port)

問い: 貨物駅28755 で約500台が「空き待ち」で敷地に止まるのは、駅の出口の詰まりか、駅の処理の上限か

## 2050-01-11(見回り1)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`
  - vehicles 631
  - byState: WaitingSpace+Importing+InGrounds 510、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 40、GoingBack+Importing+Spawned+OnRoad+Blocked 14、Importing+Spawned+InGrounds 1、GoingBack+Importing+Spawned+InGrounds 1、WaitingTarget+Importing+Spawned+InGrounds 1
  - byPath: ready 628、none 3
  - bySeenStopped: <1day 157、7days+ 474
  - samples の敷地の中の車はすべて x=3441, z=-1555、blockCounter 0、waitCounter 0。荷は Goods と Coal。行き先までの距離 1,541〜6,296m
  - samples の道の上で止まった車: vehicle 24 が 2222,-968(blockCounter 10)、vehicle 210 が 265,-82
- `cargo()`
  - stoppedTrucks 840(道の上311、敷地の中529)
  - stoppedInBuildingsTop: 28755 Cargo Center 510、1366 Cargo Harbor 17、46112 Cargo Harbor 2
  - stations: 28755 は vehiclesLeaving 780・vehiclesArriving 11。ほかの Cargo Center 8つ(3940、4740、13893、14580、16572、40031、48243)は出入り0
  - stoppedSpots: 3440,-1552 が65、2227,-1069 が13、878,-703 が13、-1717,94 が12、-554,-737 が12
  - shortages: noGoods 236、noResources 23
- `traffic(x=3449, z=-1555, radius=300)`
  - flow 50、cars 39、blocked 0、congestion 4、averageDensity 31
  - busiest: 区間28970(Basic Road、3440,-1340)100、17690(Basic Road、3480,-1315)97、31488(Basic Road、3279,-1340)65、18170(Small 4 Lane、3400,-1380)53
  - blockedSpots: なし

## 2050-01-21(見回り2)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`
  - vehicles 597
  - byState: WaitingSpace+Importing+InGrounds 484、WaitingSpace+Importing+OnRoad 62、Importing+Spawned+OnRoad+Blocked 39、GoingBack+Importing+Spawned+OnRoad+Blocked 10、Importing+Spawned+InGrounds 1、WaitingPath+GoingBack+Importing+Spawned+OnRoad 1
  - byPath: ready 596、none 1
  - bySeenStopped: <1day 107、7days+ 490
  - samples の敷地の中の車はすべて x=3441, z=-1555、blockCounter 0、waitCounter 0。vehicle 8、36、120、156、183 は seenStoppedDays 20(見回り1から動いていない)。荷は Goods、Coal、Food
  - samples の道の上: vehicle 210 が 698,-662(blockCounter 10、帰り道)
- `cargo()`
  - stoppedTrucks 775(道の上291、敷地の中484)
  - stoppedInBuildingsTop: 28755 Cargo Center 484 のみ
  - stations: 28755 は vehiclesLeaving 766・vehiclesArriving 13。1366 Cargo Harbor 145・5、46112 は 18・3。ほかの Cargo Center 8つは出入り0
  - stoppedSpots: 3439,-1551 が64、4095,-276 が18、-1729,95 が15、2239,-933 が14、2143,-899 が11
  - shortages: noGoods 232、noResources 25
- `traffic(x=3449, z=-1555, radius=300)`
  - flow 52、cars 49、blocked 0、congestion 4、averageDensity 36
  - busiest: 区間28970(Basic Road、3440,-1340)100、17690(Basic Road、3480,-1315)99、28685(Small 4 Lane、3480,-1265)82、21334(Basic Road、3495,-1378)78
  - blockedSpots: なし

## 2050-01-31(月末)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`
  - vehicles 597
  - byState: WaitingSpace+Importing+InGrounds 496、WaitingSpace+Importing+OnRoad 54、Importing+Spawned+OnRoad+Blocked 38、GoingBack+Importing+Spawned+OnRoad+Blocked 9
  - byPath: ready 597
  - bySeenStopped: <1day 142、7days+ 455
  - samples の敷地の中の車はすべて x=3441, z=-1555、blockCounter 0、waitCounter 0。vehicle 8、36、120、156、183 は seenStoppedDays 30.1(月の初めから動いていない)。荷は Goods、Coal、Lumber
  - samples の道の上: vehicle 189 が -1028,-558(blockCounter 54、行き先まで427m)
- `cargo()`
  - stoppedTrucks 778(道の上282、敷地の中496)
  - stoppedInBuildingsTop: 28755 Cargo Center 496 のみ
  - stations: 28755 は vehiclesLeaving 746・vehiclesArriving 12。1366 Cargo Harbor 135・6、46112 は 24・3。ほかの Cargo Center 8つは出入り0
  - stoppedSpots: 3439,-1551 が56、-1936,122 が22、3314,-248 が17、1743,-860 が13、2092,64 が8
  - shortages: noGoods 231、noResources 27
- `traffic(x=3449, z=-1555, radius=300)`
  - flow 52、cars 37、blocked 0、congestion 3、averageDensity 26
  - busiest: 区間17690(Basic Road、3480,-1315)73、31488(Basic Road、3279,-1340)62、28685(Small 4 Lane、3480,-1265)55、18170(Small 4 Lane、3400,-1380)52。28970 は 39
  - blockedSpots: なし
