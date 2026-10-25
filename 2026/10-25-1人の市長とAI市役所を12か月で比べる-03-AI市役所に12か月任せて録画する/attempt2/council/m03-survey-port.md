# m03 調査 s03-1(port)

問い: 貨物駅28755の敷地で、輸入の荷のトラックが空き待ち(WaitingSpace)のまま動かないのは、駅の出口の車線のつながりが原因か。

## 見回り1(2050-03-12)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`: vehicles 636。byState は WaitingSpace+Importing+InGrounds 533、WaitingSpace+Importing+OnRoad 76、Importing+Spawned+OnRoad+Blocked 11、GoingBack+Importing+Spawned+OnRoad+Blocked 14、Importing+Spawned+InGrounds 1、GoingBack+Importing+Spawned+InGrounds 1。byPath ready 634、none 2。bySeenStopped <1day 130、7days+ 506。samples 10台はすべて WaitingSpace+Importing+InGrounds、path ready、blockCounter 0、waitCounter 0、位置 (3441, -1555)。荷は Goods 5、Lumber 2、Petrol 2、Coal 1。seenStoppedDays 70.1 が5台、50 が2台、10 が2台、0 が1台
- `net_near(x=3495, z=-1558, radius=40)`: 9区間。Small 4 Lane Road 15733((3495,-1490)〜(3495,-1565)、node 8479・21285、各向き2車線)と 22686((3495,-1565)〜(3496,-1610)、node 21285・15388、各向き2車線)。Cargo Connection 6区間: 11402((3477,-1555)〜(3469,-1555))、22871((3469,-1560)〜(3477,-1560))、25137((3497,-1560)〜(3549,-1560)、node 4316)、25546((3469,-1555)〜(3417,-1555))、26146((3549,-1555)〜(3497,-1555)、node 16839)、30062((3417,-1560)〜(3469,-1560))。Train Cargo Track 9082((3473,-1643)〜(3473,-1467))。Cargo Connection の端 (3497, -1555/-1560) の node 4316・16839 は、道路の node 21285 (3495,-1565) と別の点
- `traffic(x=3430, z=-1555, radius=120)`: flow 55、cars 19、blocked 0、congestion 1、roadSegments 8、averageDensity 12。busiest は Large Road 17311 (3400,-1458) 密度58、20316 (3400,-1530) 密度43。blockedSpots なし

## 見回り2(2050-03-22)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`: vehicles 688。byState は WaitingSpace+Importing+InGrounds 553、WaitingSpace+Importing+OnRoad 78、Importing+Spawned+OnRoad+Blocked 36、GoingBack+Importing+Spawned+OnRoad+Blocked 17、GoingBack+Importing+Spawned+InGrounds 3、WaitingTarget+Importing+Spawned+InGrounds 1。byPath ready 684、none 4。bySeenStopped <1day 125、7days+ 563。samples 10台はすべて WaitingSpace+Importing+InGrounds、path ready、blockCounter 0、waitCounter 0、位置 (3441, -1555)。seenStoppedDays 80 が3台(vehicle 8、36、307)、60 が2台、20 が2台、10 が1台、0 が2台(新しく見た 185 Coal → 石炭発電所2992、274 Goods)
- `net_near(x=3495, z=-1558, radius=40)`: 見回り1と同じ9区間・同じ点(道路 15733・22686 の node 21285 (3495,-1565)、Cargo Connection の端 node 4316 (3497,-1560)・16839 (3497,-1555))
- `traffic(x=3430, z=-1555, radius=120)`: flow 53、cars 22、blocked 16(すべて道の上、blockedInBuildings 0)、congestion 1、roadSegments 8、averageDensity 11。busiest は Large Road 17311 (3400,-1458) 密度45、20316 (3400,-1530) 密度43。blockedSpots (3410,-1511) 16台

## 月末(2050-04-01)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`: vehicles 719。byState は WaitingSpace+Importing+InGrounds 583、WaitingSpace+Importing+OnRoad 76、Importing+Spawned+OnRoad+Blocked 43、GoingBack+Importing+Spawned+OnRoad+Blocked 15、Importing+Spawned+InGrounds 2。byPath ready 717、none 2。bySeenStopped <1day 129、7days+ 590。samples 10台はすべて WaitingSpace+Importing+InGrounds、path ready、blockCounter 0、waitCounter 0、位置 (3441, -1555)。seenStoppedDays 90.1 が2台(vehicle 8、36)、70 が2台(229、237)、30 が2台(81、246)、20 が1台(55)、10 が1台(185)、0 が2台(210 Goods、240 Food)
- `net_near(x=3495, z=-1558, radius=40)`: 見回り1・2と同じ9区間・同じ点
- `traffic(x=3430, z=-1555, radius=120)`: flow 51、cars 9、blocked 0、congestion 1、roadSegments 8、averageDensity 13。busiest は Large Road 17311 (3400,-1458) 密度61、20316 (3400,-1530) 密度47。blockedSpots なし
- 3回の推移: 28755 に紐づくトラック 636 → 688 → 719、WaitingSpace+Importing+InGrounds 533 → 553 → 583、7days+ 506 → 563 → 590。出口近くの blocked 0 → 16 → 0
