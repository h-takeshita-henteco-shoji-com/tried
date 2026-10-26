# m04 調査の結果(port)

## s04-1 貨物駅28755の出口の列の先頭が動いているか

問い: 貨物駅28755の出口の端 (3417,-1555) の近くで、止まった車は列の先頭まで詰まっているのか、先頭が進んでいるのか。
見立ては書かない。局が翌月に読んで決める。

### 見回り1(2050-04-11)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`
  - vehicles 597
  - byState: WaitingSpace+Importing+InGrounds 502、WaitingSpace+Importing+OnRoad 59、Importing+Spawned+OnRoad+Blocked 24、GoingBack+Importing+Spawned+OnRoad+Blocked 7、WaitingTarget+Importing+Spawned+InGrounds 2、Congestion+Importing+Spawned+OnRoad 1、GoingBack+Importing+Spawned+InGrounds 1、Importing+Spawned+InGrounds 1
  - byPath: ready 593、none 4
  - bySeenStopped: <1day 143、7days+ 454
  - samples 40台のうち38台は位置 (3441,-1555)、blockCounter 0、waitCounter 0。seenStoppedDays は 0〜100(100日が8台)
  - 位置が (3441,-1555) でない2台: vehicle 535(Importing+Spawned+OnRoad+Blocked、(2236,-1086)、blockCounter 17)、vehicle 1134(Congestion+Importing+Spawned+OnRoad、(2342,-1238))
  - 荷物の種類(samples): Goods が主。ほかに Petrol、Lumber、Food、Coal
- `traffic(x=3417, z=-1557, radius=40)`
  - flow 54、cars 8、blocked 0、blockedOnRoads 0、blockedInBuildings 0、congestion 1、roadSegments 1、averageDensity 28
  - busiest: segment 20316(Large Road、(3400,-1530))density 28
  - blockedSpots なし
- `net_near(x=3417, z=-1557, radius=25)`(service の指定なし)
  - 20316 Large Road: node 27757 (3400,-1567) — node 20609 (3400,-1493)、片側3車線
  - 30945 Large Road: node 11790 (3400,-1625) — node 27757 (3400,-1567)、片側3車線
  - 25546 Cargo Connection(service Beautification): node 27256 (3469,-1555) — node 5129 (3417,-1555)、length 52
  - 30062 Cargo Connection(service Beautification): node 20745 (3417,-1560) — node 27809 (3469,-1560)、length 52
  - Cargo Connection の端の node 5129・20745 は、Large Road の node 27757 と別の番号

### 見回り2(2050-04-21)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`
  - vehicles 572
  - byState: WaitingSpace+Importing+InGrounds 484、WaitingSpace+Importing+OnRoad 63、Importing+Spawned+OnRoad+Blocked 15、GoingBack+Importing+Spawned+OnRoad+Blocked 6、GoingBack+Importing+Spawned+InGrounds 2、Congestion+Importing+Spawned+OnRoad 1、Importing+Spawned+InGrounds 1
  - byPath: ready 569、none 3
  - bySeenStopped: <1day 113、7days+ 459
  - samples 40台のうち39台は位置 (3441,-1555)、blockCounter 0、waitCounter 0。seenStoppedDays は 0〜110(110日が8台)
  - 見回り1と同じ車の例: vehicle 36・307・339・341・467・469・664・670 は 100日 → 110日。vehicle 2・8 は samples から消えた
  - 位置が (3441,-1555) でない1台: vehicle 291(Importing+Spawned+OnRoad+Blocked、(1844,-1005)、blockCounter 24)
- `traffic(x=3417, z=-1557, radius=40)`
  - flow 53、cars 12、blocked 0、blockedOnRoads 0、blockedInBuildings 0、congestion 1、roadSegments 1、averageDensity 43
  - busiest: segment 20316(Large Road、(3400,-1530))density 43
  - blockedSpots なし
- `net_near(x=3417, z=-1557, radius=25)`
  - 見回り1と同じ4区間(20316、30945 の Large Road。25546、30062 の Cargo Connection)。node の番号と座標も同じ

### 月末(2050-05-01)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`
  - vehicles 588
  - byState: WaitingSpace+Importing+InGrounds 485、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 32、GoingBack+Importing+Spawned+OnRoad+Blocked 4、Congestion+Importing+Spawned+OnRoad 1、Importing+Spawned+InGrounds 1、WaitingTarget+Importing+Spawned+InGrounds 1
  - byPath: ready 586、none 2
  - bySeenStopped: <1day 136、7days+ 452
  - samples 40台のうち38台は位置 (3441,-1555)、blockCounter 0、waitCounter 0。seenStoppedDays は 0〜120(120日が8台: 307、467、469、664、670、1180、1202、339)
  - vehicle 339(Petrol、工場44294行き)は見回り2で (3441,-1555) の WaitingSpace+Importing+InGrounds、月末は Importing+Spawned+OnRoad+Blocked で位置 (2823,-1239)、blockCounter 1、行き先まで 1,116
  - 位置が (3441,-1555) でない2台: vehicle 339 と vehicle 885(Importing+Spawned+OnRoad+Blocked、(2836,-1239)、blockCounter 1)
- `traffic(x=3417, z=-1557, radius=40)`
  - flow 52、cars 7、blocked 0、blockedOnRoads 0、blockedInBuildings 0、congestion 1、roadSegments 1、averageDensity 28
  - busiest: segment 20316(Large Road、(3400,-1530))density 28
  - blockedSpots なし
- `net_near(x=3417, z=-1557, radius=25)`
  - 見回り1・2と同じ4区間。node の番号と座標も同じ
