# m05 調査 port(s05-1)

問い: 貨物駅28755 の敷地の中の止まった車は、4月の再開後も 249 まで戻るか。どの荷が止まるか

## 見回り1(2050-05-11)

- `cargo()`
  - stoppedTrucks 570、stoppedOnRoads 306、stoppedInBuildings 264(全部が 28755)
  - 荷ごとの止まり: Goods 363、Petrol 62、Lumber 58、Coal 45、Food 42
  - 28755 の vehiclesLeaving 441、vehiclesArriving 14
  - stoppedSpots の最多 (3430,-1535) 58
  - 品物がない店 199、原料がない工場 29
- `vehicles_stuck(kind="truck", building=28755, limit=60)`
  - vehicles 350
  - byState: WaitingSpace+Importing+InGrounds 264、WaitingSpace+Importing+OnRoad 40、Importing+Spawned+OnRoad+Blocked 31、GoingBack+Importing+Spawned+OnRoad+Blocked 14、Importing+Spawned+InGrounds 1
  - byPath: ready 349、none 1
  - bySeenStopped: <1day 113、7days+ 237
  - samples 60台の荷: Goods 32、Coal 9、Petrol 9、Lumber 7、Food 3
  - WaitingSpace の車の位置は (3441,-1555)。samples のうち seenStoppedDays 130.1 の車が8台(664、1717、1746、2380、2396、2677、2692、2710)
  - 道の上で Blocked の車は (1399〜1726,-750〜-831) に多い(blockCounter 9〜56)
- `vehicles_stuck(kind="train", limit=20)`
  - vehicles 14。byTarget は全部 28755
  - byState: Importing+Spawned+OnRoad 10、WaitingCargo+Stopped+Importing+InGrounds 2、Stopped+Importing+Spawned+OnRoad 1、Importing+Spawned+InGrounds 1
  - byPath: ready 12、none 2
  - 駅の中 (3475,-1488) の列車14486 は cargoLoads 0、waitCounter 9

## 見回り2(2050-05-21)

- `cargo()`
  - stoppedTrucks 572、stoppedOnRoads 286、stoppedInBuildings 286(28755 が 285、店39178 が 1)
  - 荷ごとの止まり: Goods 349、Petrol 67、Lumber 61、Food 55、Coal 40
  - 28755 の vehiclesLeaving 498、vehiclesArriving 12
  - stoppedSpots: (3441,-1555) 34、(2706,-1260) 31、(2256,-915) 15、(-1674,106) 10、(1329,-745) 9
  - 品物がない店 212、原料がない工場 30
- `vehicles_stuck(kind="truck", building=28755, limit=60)`
  - vehicles 375
  - byState: WaitingSpace+Importing+InGrounds 285、WaitingSpace+Importing+OnRoad 34、Importing+Spawned+OnRoad+Blocked 30、GoingBack+Importing+Spawned+OnRoad+Blocked 22、ほか各1(GoingBack+InGrounds、InGrounds、InGrounds+Blocked、WaitingTarget+InGrounds)
  - byPath: ready 371、none 4
  - bySeenStopped: <1day 126、7days+ 249
  - samples 60台の荷: Goods 27、Food 10、Coal 8、Petrol 8、Lumber 7
  - 見回り1で WaitingSpace だった車のうち 30、268、398、463、1682、1745、1928、1936、1946、2384、2396、2566、2692 は、道の上 (2680〜2766,-1236〜-1332) で Blocked(blockCounter 8〜32)。2396・2692 は seenStoppedDays 140.1 のまま
  - seenStoppedDays 140.1 で WaitingSpace のまま: 664、1717、1746
- `vehicles_stuck(kind="train", limit=20)`
  - vehicles 12。byTarget は全部 28755
  - byState: Importing+Spawned+OnRoad 10、Stopped+Importing+Spawned+OnRoad 1、WaitingCargo+Stopped+Importing+InGrounds 1
  - byPath: ready 11、none 1
  - 駅の近く (3438,-1786)、(3475,-1640) に2編成(行き先まで 238m、89m)

## 月末(2050-05-31)

- `cargo()`
  - stoppedTrucks 546、stoppedOnRoads 239、stoppedInBuildings 307(全部が 28755)
  - 荷ごとの止まり: Goods 341、Petrol 67、Lumber 57、Coal 53、Food 28
  - 28755 の vehiclesLeaving 532、vehiclesArriving 11
  - stoppedSpots: (3441,-1555) 33、(2262,-1230) 11、(-517,80) 9、(2225,-1099) 9、(1880,-1043) 8
  - 品物がない店 215、原料がない工場 32
- `vehicles_stuck(kind="truck", building=28755, limit=60)`
  - vehicles 382
  - byState: WaitingSpace+Importing+InGrounds 307、WaitingSpace+Importing+OnRoad 33、Importing+Spawned+OnRoad+Blocked 23、GoingBack+Importing+Spawned+OnRoad+Blocked 16、Importing+Spawned+InGrounds 3
  - byPath: ready 379、none 3
  - bySeenStopped: <1day 129、7days+ 253
  - samples 60台の荷: Goods 35、Coal 11、Petrol 8、Lumber 6
  - seenStoppedDays 150 で WaitingSpace のまま: 664、1717、1746、2893、2908。140: 1728、1842。130: 3637
  - 見回り2で道の上 (2680〜2766,-1236〜-1332) にいた車のうち 1745・1928 は (1904〜1910,-1048)、1936・2384・2396 は (2236,-1089〜-1134) で Blocked
- `vehicles_stuck(kind="train", limit=20)`
  - vehicles 11。byTarget は全部 28755
  - byState: Importing+Spawned+OnRoad 9、WaitingCargo+Stopped+Importing+InGrounds 2
  - byPath: ready 9、none 2
  - bySeenStopped: <1day 9、7days+ 2(6253、15521。seenStoppedDays 9.9)
