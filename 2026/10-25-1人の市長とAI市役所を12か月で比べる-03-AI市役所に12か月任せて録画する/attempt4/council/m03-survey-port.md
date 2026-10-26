# m03 調査 s03-1(port)の結果

問い: 28755 の敷地の中で道順(path)が none の車が、出口の車線をふさぐ元になっているか。
見る道具: `vehicles_stuck(kind="truck", building=28755, limit=60)`、`cargo()`。見回り1、見回り2、月末。

参考(実行の段の直前、2050-03-02): `cargo` の stoppedInBuildings 575(全部28755)、stoppedOnRoads 340、28755 の vehiclesLeaving 862・vehiclesArriving 12。m03-3 で 2050-03-02 に28755 を止めた。

## 見回り1(2050-03-12)

28755 は止めたまま測った。測った後に `set_building_active(28755, active=True)` で動かし直した(m03-3)。

- `cargo()`
  - stoppedInBuildings 431(28755 が 430、274 の工場が 1)。stoppedOnRoads 370。stoppedTrucks 801
  - 28755 の vehiclesLeaving 754、vehiclesArriving 2
  - stoppedSpots の最多 (3439,-1550) 90台
  - Goods の import 846・local 421、止まり 526
  - 品物がない店 132、原料がない工場 26
- `vehicles_stuck(kind="truck", building=28755, limit=60)`
  - vehicles 584
  - byState: WaitingSpace+Importing+InGrounds 430、WaitingSpace+Importing+OnRoad 86、Importing+Spawned+OnRoad+Blocked 44、GoingBack+Importing+Spawned+OnRoad+Blocked 21、WaitingPath+GoingBack+Importing+Spawned+OnRoad 1、GoingBack+Importing+Spawned+InGrounds 1、WaitingTarget+Importing+Spawned+InGrounds 1
  - byPath: none 2、ready 582
  - bySeenStopped: <1day 90、7days+ 494
  - samples(60台)のうち path none は車857(GoingBack+Importing+Spawned+InGrounds、Food 0、(3406,-1560)、seenStoppedDays 0)の1台
  - WaitingSpace の車はどれも (3441,-1555)、path ready、blockCounter 0。seenStoppedDays 70 の車が多数(車8、36、664、670、675、1030、1180、1202、1229、1449、1717、1746 など)。10日の車も多数(車178、396、625、641、870 など)
  - 道の上で Blocked の車は (465〜1152,-696〜-726)、(2204,-62〜-137)、(1837,-967)、(-1247〜-1374,-441〜-495) など、駅から離れた場所

## 見回り2(2050-03-22)

28755 は 2050-03-12 に動かし直してから10日。

- `cargo()`
  - stoppedInBuildings 361(28755 が 342、港1366 が 18、店516 が 1)。stoppedOnRoads 334。stoppedTrucks 695
  - 28755 の vehiclesLeaving 657、vehiclesArriving 6
  - stoppedSpots の最多 (3440,-1553) 76台
  - Goods の import 826・local 439、止まり 469
  - 品物がない店 144、原料がない工場 32
- `vehicles_stuck(kind="truck", building=28755, limit=60)`
  - vehicles 481
  - byState: WaitingSpace+Importing+InGrounds 342、WaitingSpace+Importing+OnRoad 75、Importing+Spawned+OnRoad+Blocked 43、GoingBack+Importing+Spawned+OnRoad+Blocked 16、Importing+Spawned+InGrounds 3、GoingBack+Importing+Spawned+InGrounds 2
  - byPath: none 5、ready 476
  - bySeenStopped: <1day 39、7days+ 442
  - samples(60台)に path none の車は出なかった
  - WaitingSpace の車はどれも (3441,-1555)、path ready、blockCounter 0。見回り1で70日だった車(8、36、664、670、675、1030、1180、1202、1229、1449、1717、1746)は80日になり、同じ位置に残る
  - 道の上で Blocked の車は (-771〜-857,-732〜-736)、(886〜1081,-712〜-721)、(172,-259)、(1642,-773)、(1922,-838) など、駅から離れた場所

## 月末(2050-04-01)

- `cargo()`
  - stoppedInBuildings 295(28755 が 294、店46369 が 1)。stoppedOnRoads 314。stoppedTrucks 609
  - 28755 の vehiclesLeaving 600、vehiclesArriving 13
  - stoppedSpots の最多 (3434,-1542) 70台
  - Goods の import 842・local 415、止まり 396
  - 品物がない店 149、原料がない工場 30
- `vehicles_stuck(kind="truck", building=28755, limit=60)`
  - vehicles 406
  - byState: WaitingSpace+Importing+InGrounds 294、WaitingSpace+Importing+OnRoad 58、Importing+Spawned+OnRoad+Blocked 41、GoingBack+Importing+Spawned+OnRoad+Blocked 13
  - byPath: ready 406(none 0)
  - bySeenStopped: <1day 67、7days+ 339
  - WaitingSpace の車はどれも (3441,-1555)、path ready、blockCounter 0。90日の車(8、36、664、670、675、1030、1180、1202、1229、1443、1449、1717、1746、2380、2396、2677、2692、2710)が同じ位置に残る。0日の新しい車(374、663、1217、1806、2502)も WaitingSpace に入っている
  - 道の上で Blocked の車は (-1789,-348)、(-1547,-1098)、(202,-299〜-305)、(298,-194) など、駅から離れた場所
