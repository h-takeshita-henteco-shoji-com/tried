# m03 調査の結果(port)

## s03-1 貨物駅28755の出口の道が、西の Large Road とつながっていないかを確かめる

問い: 貨物駅28755の出口の道(Cargo Connection)の端 (3417,-1555) と (3417,-1560) は、西の Large Road(x=3400)と本当につながっていないのか。
見立ては書かない(局が翌月に読んで決める)。

### 見回り1(2050-03-12)

- `net_near(x=3410, z=-1558, radius=30, service="Road")`: total 2。区間 20316(Large Road、node 27757 (3400,-1567) → node 20609 (3400,-1493)、長さ76、車線 3/3)、区間 30945(Large Road、node 11790 (3400,-1625) → node 27757 (3400,-1567)、長さ57、車線 3/3)。Cargo Connection の区間は返らなかった
- `vehicles_stuck(kind="truck", building=28755, limit=15)`: vehicles 579。byState は WaitingSpace+Importing+InGrounds 477、WaitingSpace+Importing+OnRoad 58、Importing+Spawned+OnRoad+Blocked 36、GoingBack+Importing+Spawned+OnRoad+Blocked 6、GoingBack+Importing+Spawned+InGrounds 1、WaitingPath+GoingBack+Importing+Spawned+OnRoad 1。byPath は ready 578、none 1。bySeenStopped は <1day 126、7days+ 453。サンプル15台のうち13台が (3441,-1555) で WaitingSpace、blockCounter 0、waitCounter 0。荷は Goods、Petrol、Lumber。1台(vehicle 284)は (2236,-1174) で OnRoad+Blocked、blockCounter 5
- `junction_info(x=3400, z=-1555)`: ok=false、"no road junction within 40m"

### 見回り2(2050-03-22)

- `net_near(x=3410, z=-1558, radius=30, service="Road")`: total 2。区間 20316(Large Road、node 27757 (3400,-1567) → node 20609 (3400,-1493))、区間 30945(Large Road、node 11790 (3400,-1625) → node 27757)。見回り1と同じ。Cargo Connection の区間は返らなかった
- `vehicles_stuck(kind="truck", building=28755, limit=15)`: vehicles 594。byState は WaitingSpace+Importing+InGrounds 499、WaitingSpace+Importing+OnRoad 59、Importing+Spawned+OnRoad+Blocked 25、GoingBack+Importing+Spawned+OnRoad+Blocked 11。byPath は ready 594。bySeenStopped は <1day 127、7days+ 467。サンプル15台のうち14台が (3441,-1555) で WaitingSpace、blockCounter 0。見えて80日の車がサンプルに5台(8、36、307、339、341)。vehicle 284 は (1477,-751) で OnRoad+Blocked、blockCounter 9
- `junction_info(x=3400, z=-1555)`: ok=false、"no road junction within 40m"

### 月末(2050-04-01)

- `net_near(x=3410, z=-1558, radius=30, service="Road")`: total 2。区間 20316 と 30945(Large Road、x=3400、境の node 27757 (3400,-1567))。3回とも同じ。Cargo Connection の区間は3回とも返らなかった
- `vehicles_stuck(kind="truck", building=28755, limit=15)`: vehicles 576。byState は WaitingSpace+Importing+InGrounds 486、WaitingSpace+Importing+OnRoad 58、Importing+Spawned+OnRoad+Blocked 18、GoingBack+Importing+Spawned+OnRoad+Blocked 12、Congestion+Importing+Spawned+OnRoad 1、WaitingPath+WaitingSpace+Importing+OnRoad 1。byPath は ready 576。bySeenStopped は <1day 117、7days+ 459。サンプル15台のうち14台が (3441,-1555) で WaitingSpace、blockCounter 0。見えて90日の車がサンプルに6台(8、36、307、339、341、467)。vehicle 361 は (-886,-731) で OnRoad+Blocked、blockCounter 15
- `junction_info(x=3400, z=-1555)`: ok=false、"no road junction within 40m"(3回とも同じ)
