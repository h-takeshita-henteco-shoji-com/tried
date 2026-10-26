# m02 調査 s02-1(port): 貨物駅28755の出口が道路につながっているか

問い: 貨物駅28755の出口の道は、本当に道路につながっているか。先頭の車が (3441, -1555) で30日動かない理由を絞る。

## 見回り1(2050-02-10)

- `net_near(x=3417, z=-1557, radius=40, service="Road")`: total 2。segment 20316 Large Road(node 27757 (3400,-1567) → node 20609 (3400,-1493)、長さ76、車線 3/3)。segment 30945 Large Road(node 11790 (3400,-1625) → node 27757 (3400,-1567)、長さ57、車線 3/3)。半径40の中に、駅の出口の道(Harbor Road など)の区間は出なかった
- `junction_info(x=3417, z=-1555)`: ok=false、"no road junction within 40m"
- `vehicles_stuck(kind="truck", building=28755, limit=15)`: vehicles 567
  - byState: WaitingSpace+Importing+InGrounds 491、WaitingSpace+Importing+OnRoad 53、Importing+Spawned+OnRoad+Blocked 11、GoingBack+Importing+Spawned+OnRoad+Blocked 9、GoingBack+Importing+Spawned+InGrounds 2、WaitingTarget+Importing+Spawned+InGrounds 1
  - byPath: ready 564、none 3
  - bySeenStopped: <1day 117、7days+ 450
  - byTarget: 行き先なし(building 0)12、ほかは各2〜3台(店と工場)
  - samples 15台: 全部 (3441, -1555)、source 28755 Cargo Center。14台が WaitingSpace+Importing+InGrounds、1台(377)が WaitingSpace+Importing+OnRoad。blockCounter と waitCounter はすべて0。seenStoppedDays は 40 が7台、30 が1台、20 が2台、10 が1台、0 が4台。荷は Goods 10、Petrol 3、Food 1、Lumber 1。行き先までの距離 366〜6,026m

## 見回り2(2050-02-20)

- `net_near(x=3417, z=-1557, radius=40, service="Road")`: total 2。見回り1と同じ(20316 と 30945 の Large Road、node 27757 (3400,-1567) でつながる)
- `junction_info(x=3417, z=-1555)`: ok=false、"no road junction within 40m"
- `vehicles_stuck(kind="truck", building=28755, limit=15)`: vehicles 585
  - byState: WaitingSpace+Importing+InGrounds 497、WaitingSpace+Importing+OnRoad 52、Importing+Spawned+OnRoad+Blocked 29、GoingBack+Importing+Spawned+OnRoad+Blocked 6、GoingBack+Importing+Spawned+InGrounds 1
  - byPath: ready 584、none 1
  - bySeenStopped: <1day 135、7days+ 450
  - byTarget: 行き先なし 7、ほかは各3台(店)
  - samples 15台: 14台が (3441,-1555) で WaitingSpace+Importing+InGrounds、blockCounter 0、waitCounter 0。seenStoppedDays は 50.1 が4台(8、36、307、339)、30.1 が2台、20.1 が1台、10 が3台、0 が4台。1台(87)は GoingBack+Importing+Spawned+OnRoad+Blocked で (-1071,-654) にいて blockCounter 24、行き先なし

## 月末(2050-03-02)

- `net_near(x=3417, z=-1557, radius=40, service="Road")`: total 2。見回り1・2と同じ(20316 と 30945 の Large Road、node 27757 (3400,-1567))
- `junction_info(x=3417, z=-1555)`: ok=false、"no road junction within 40m"
- `vehicles_stuck(kind="truck", building=28755, limit=15)`: vehicles 594
  - byState: WaitingSpace+Importing+InGrounds 491、WaitingSpace+Importing+OnRoad 54、Importing+Spawned+OnRoad+Blocked 36、GoingBack+Importing+Spawned+OnRoad+Blocked 11、GoingBack+Importing+Spawned+InGrounds 1、Congestion+Importing+Spawned+OnRoad 1
  - byPath: ready 593、none 1
  - bySeenStopped: <1day 122、7days+ 472
  - byTarget: 行き先なし 12、ほかは各2〜4台(店と工場)
  - samples 15台: 12台が (3441,-1555) で WaitingSpace(InGrounds 11、OnRoad 1)、blockCounter 0、waitCounter 0。seenStoppedDays は 60 が7台(8、36、307、339、341、377、410)、50 が1台、40 が2台、9.9 が1台、0 が1台
  - 道の上で Blocked の3台: 87 (882,-715) blockCounter 5、189 (1245,-741) blockCounter 6(どちらも GoingBack、行き先なし)、400 (3404,-1356) blockCounter 15(Goods、行き先 40570)
