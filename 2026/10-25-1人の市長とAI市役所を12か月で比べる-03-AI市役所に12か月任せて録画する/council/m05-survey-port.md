# m05 調査の結果(port)

## s05-1 貨物駅28755の出口の隙間が、止まったトラックの原因か

問い: 出口(Cargo Connection の端 (3417,-1555))から Large Road(x=3400)までの5〜17mの隙間が、止まったトラック約485台の原因か。止まった車の位置の広がりと先頭の動きで見る。

### 見回り1(2050-05-11)

- `vehicles_stuck(kind="truck", building=28755, limit=100)`
  - vehicles 596
  - byState: WaitingSpace+Importing+InGrounds 489、WaitingSpace+Importing+OnRoad 61、Importing+Spawned+OnRoad+Blocked 36、GoingBack+Importing+Spawned+OnRoad+Blocked 8、WaitingPath+GoingBack+Importing+Spawned+OnRoad 1、WaitingTarget+WaitingSpace+Importing+OnRoad 1
  - byPath: ready 596
  - bySeenStopped: <1day 114、7days+ 482
  - samples 100台のうち99台が (3441,-1555)、blockCounter 0・waitCounter 0。1台(vehicle 291、GoingBack、荷0)は (2079,-954) で blockCounter 14
  - samples の seenStoppedDays: 120日以上が16台(うち130日が12台)
  - byTarget の上位: 行き先なし(building 0)10台、ほかは各2〜3台(店、Coal Power Plant 2992、工場 40270 など)
- `net_near(x=3410, z=-1557, radius=30)`
  - Large Road 20316(node 27757 (3400,-1567) 〜 node 20609 (3400,-1493))、Large Road 30945(node 11790 (3400,-1625) 〜 node 27757)
  - Cargo Connection 25546(node 27256 (3469,-1555) 〜 node 5129 (3417,-1555))、Cargo Connection 30062(node 20745 (3417,-1560) 〜 node 27809 (3469,-1560))
  - Cargo Connection の端 node 5129・20745 と Large Road の node 27757 は別の番号
- `cargo()`
  - stoppedTrucks 838、stoppedOnRoads 349、stoppedInBuildings 489(全部 28755)
  - stations 28755: vehiclesLeaving 705、vehiclesArriving 11
  - stoppedSpots の1位 (3437,-1545) 69台
  - noGoods 182、noResources 35

### 見回り2(2050-05-21)

- `vehicles_stuck(kind="truck", building=28755, limit=100)`
  - vehicles 607
  - byState: WaitingSpace+Importing+InGrounds 506、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 29、GoingBack+Importing+Spawned+OnRoad+Blocked 5、GoingBack+Importing+Spawned+InGrounds 3
  - byPath: ready 603、none 4
  - bySeenStopped: <1day 122、7days+ 485
  - samples 100台のうち93台が (3441,-1555) か (3440,-1560)、blockCounter 0・waitCounter 0(3863 は GoingBack、荷0、path none)
  - samples のほか7台: Large Road x=3400 の北側 (3402〜3408, -1434〜-1449) に5台(3436、3480、3486、3516、3537。Importing+Spawned+OnRoad+Blocked、blockCounter 3〜10)、(2701,289) に1台(1258、blockCounter 52)、(698,-672) に1台(3413、GoingBack、blockCounter 6)
  - samples の seenStoppedDays: 120日以上が19台(うち140日が11台、130日が4台)
  - byTarget の上位: 行き先なし 8台、ほかは各2〜3台(Future Store、Hotel、Coal Power Plant 18887 など)
- `net_near(x=3410, z=-1557, radius=30)`
  - 見回り1と同じ4区間(Large Road 20316・30945、Cargo Connection 25546・30062)。端の node も同じ(5129・20745 と 27757 は別)
- `cargo()`
  - stoppedTrucks 846、stoppedOnRoads 335、stoppedInBuildings 511(28755 が506、港1366 が5)
  - stations 28755: vehiclesLeaving 734、vehiclesArriving 12
  - stoppedSpots の1位 (3438,-1546) 69台
  - noGoods 185、noResources 38

### 月末(2050-05-31)

- `vehicles_stuck(kind="truck", building=28755, limit=100)`
  - vehicles 611
  - byState: WaitingSpace+Importing+InGrounds 514、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 24、GoingBack+Importing+Spawned+OnRoad+Blocked 6、Congestion+Importing+Spawned+OnRoad 1、GoingBack+Importing+Spawned+InGrounds 1、Importing+Spawned+InGrounds 1
  - byPath: ready 608、none 3
  - bySeenStopped: <1day 133、7days+ 478
  - samples 100台のうち97台が (3441,-1555)、blockCounter 0・waitCounter 0
  - samples のほか3台: (3399,-1404) に1台(3117、GoingBack、荷0、blockCounter 1)、(2232,-1064) に1台(2424、blockCounter 13)、(1844,-1004) に1台(1584、blockCounter 1)
  - samples の seenStoppedDays: 120日以上が15台(うち150日が8台、140日が3台、130日が4台)
  - 前回まで長く止まっていた車のうち 891、1180、812、767、2033 は、行き先の建物が変わり、seenStoppedDays 0 と返った(場所は同じ (3441,-1555))
  - byTarget の上位: 行き先なし 7台、ほかは各2〜3台
- `net_near(x=3410, z=-1557, radius=30)`
  - 見回り1・2と同じ4区間・同じ node(5129・20745 と 27757 は別)
- `cargo()`
  - stoppedTrucks 862、stoppedOnRoads 348、stoppedInBuildings 514(全部 28755)
  - stations 28755: vehiclesLeaving 743、vehiclesArriving 11
  - stoppedSpots の1位 (3439,-1551) 66台
  - noGoods 178、noResources 43
  - Goods: import 867、local 692
