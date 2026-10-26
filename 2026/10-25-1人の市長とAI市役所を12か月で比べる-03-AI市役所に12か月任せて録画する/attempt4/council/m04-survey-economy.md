# m04 調査の結果(economy)

## s04-3 品物がない店は、輸入の荷物の車が道の上で詰まって届かないためか

注: 施策 m04-2 で、貨物駅28755 を 2050-04-01 から 2050-04-11 まで止めた。見回り1の数は止めている間の値。

### 見回り1(2050-04-11)

- `cargo()`
  - shortages.noGoods 165(実行前149)。spots (2263,754) 45、(-1071,-929) 41、(835,230) 30
  - byCargo.Goods: import 683、local 389、stoppedTrucks 403
  - stoppedOnRoads 356、stoppedInBuildings 243
- `traffic(x=3440, z=-250, radius=300, limit=10)`
  - flow 54、cars 191、blocked 86(onRoads 85)、congestion 76、averageDensity 51
  - busiest は10区間とも密度100(Basic Road 18692・12337・12091・12005・5851、Small 4 Lane Road 20837・35188・33175・32517・7709)
  - blockedSpots (3286,-282) 42、(3516,-248) 18、(3169,-306) 18、(3623,-245) 7
- `vehicles_stuck(kind="truck", limit=30)`
  - vehicles 842
  - byState: WaitingSpace+Importing+InGrounds 243、Importing+InGrounds 224、Importing+Spawned+OnRoad+Blocked 149、Spawned+OnRoad+Blocked 69、WaitingSpace+Importing+OnRoad 53、GoingBack+Spawned+OnRoad+Blocked 46、GoingBack+Importing+Spawned+OnRoad+Blocked 38、ほか
  - byPath: ready 829、none 13
  - bySeenStopped: <1day 378、7days+ 464
  - byTarget の上位は店(Future Store 44050・45888、Shop04 41185 が各4台など。行き先なし94)
  - samples: Importing+InGrounds の車は (-4030,8619)(地図の外のつなぎ口)にいて、行き先まで 8,757〜13,092m

### 見回り2(2050-04-21。28755 は 04-11 に動かし直した後)

- `cargo()`
  - shortages.noGoods 170。spots (2259,715) 44、(-1066,-950) 44、(830,240) 29
  - byCargo.Goods: import 667、local 406、stoppedTrucks 331
  - stoppedOnRoads 292、stoppedInBuildings 199
- `traffic(x=3440, z=-250, radius=300, limit=10)`
  - flow 56、cars 209、blocked 16(onRoads 16)、congestion 93、averageDensity 57
  - busiest は10区間とも密度100(Basic Road 12337・31248・12005・12091・18692・24288、Small 4 Lane Road 27436・20837・30237・33175)
  - blockedSpots (3460,-255) 12、(3390,-256) 2、(3731,-245) 2
- `vehicles_stuck(kind="truck", limit=30)`
  - vehicles 816
  - byState: Importing+InGrounds 313、WaitingSpace+Importing+InGrounds 199、Importing+Spawned+OnRoad+Blocked 93、Spawned+OnRoad+Blocked 61、WaitingSpace+Importing+OnRoad 48、GoingBack+Spawned+OnRoad+Blocked 45、GoingBack+Importing+Spawned+OnRoad+Blocked 40、ほか
  - byPath: ready 804、none 12
  - bySeenStopped: <1day 353、7days+ 463
  - byTarget: 行き先なし88、店(Future Store 45772・44694・42705、Shop04 41185 が各4台など)
  - samples: Importing+InGrounds の車は (-4030,8619) と (6997,-8618)(地図の外のつなぎ口)にいて、行き先まで 8,757〜12,437m。道の上で Blocked の輸入車は (1881,25) blockCounter 61、(3728,-246) 54 など

### 月末(2050-05-01)

- `cargo()`
  - shortages.noGoods 180。spots (2269,717) 50、(-1056,-881) 43、(803,235) 33
  - byCargo.Goods: import 678、local 424、stoppedTrucks 312
  - stoppedOnRoads 263、stoppedInBuildings 249
- `traffic(x=3440, z=-250, radius=300, limit=10)`
  - flow 56、cars 221、blocked 1(onRoads 1)、congestion 85、averageDensity 53
  - busiest は10区間とも密度100(Basic Road 18692・12337・31248・24288・1920、Small 4 Lane Road 20837・35188・33175・32517・30237)
  - blockedSpots (3509,-254) 1
- `vehicles_stuck(kind="truck", limit=30)`
  - vehicles 873
  - byState: Importing+InGrounds 340、WaitingSpace+Importing+InGrounds 249、Importing+Spawned+OnRoad+Blocked 89、Spawned+OnRoad+Blocked 72、WaitingSpace+Importing+OnRoad 39、GoingBack+Spawned+OnRoad+Blocked 36、GoingBack+Importing+Spawned+OnRoad+Blocked 25、WaitingPath+Importing+OnRoad 5、ほか
  - byPath: ready 864、none 9
  - bySeenStopped: <1day 500、7days+ 373
  - byTarget: 行き先なし66、Future Store 46351 (-1384,-1166) 4台、店 45533・235・41185・44887・40226・40392・418 と Hotel 47622 が各3台
  - samples: Importing+InGrounds の車は (-4030,8619)、(7277,-8616)、(6993,-8619)(地図の外のつなぎ口)にいて、行き先まで 7,820〜12,286m。港1366 発の輸入車は (-1675〜-1766, 92〜96) で Blocked(blockCounter 21〜28)
