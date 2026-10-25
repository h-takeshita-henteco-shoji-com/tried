# m06 調査の結果(port)

## s06-1 貨物駅28755の出口の端が道路から離れているのが原因か

問い: 貨物駅28755の出口の Cargo Connection の端(西 (3417, -1555/-1560)、東 (3477, -1555/-1560))が道路から17〜18m離れて終わっているのが、車が一部しか出ない原因か。

### 見回り1(2050-06-10)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 684。byState は WaitingSpace+Importing+InGrounds 590、WaitingSpace+Importing+OnRoad 66、Importing+Spawned+OnRoad+Blocked 18、GoingBack+Importing+Spawned+OnRoad+Blocked 8、GoingBack+Importing+Spawned+InGrounds 1、Congestion+Importing+Spawned+OnRoad 1。byPath は ready 683、none 1。bySeenStopped は <1day 145、7days+ 539。samples 40台はどれも位置 (3441, -1555)、blockCounter 0、waitCounter 0。seenStoppedDays 160.1 の車は 8、307、467、469、572、589。byTarget の1位は building 0(行き先なし)9台
- `traffic(x=3440, z=-1560, radius=150)`: flow 53、cars 18、blocked 0、blockedOnRoads 0、blockedInBuildings 0、congestion 1、roadSegments 11、averageDensity 10。busiest は 17311 Large Road (3400, -1458) 51、20316 Large Road (3400, -1530) 43、14098 Small 4 Lane Road (3467, -1416) 11、10573 Small 4 Lane Road (3429, -1418) 7。blockedSpots なし
- `junction_info(x=3400, z=-1567)`: ok false、"no road junction within 40m"

### 見回り2(2050-06-20)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 685。byState は WaitingSpace+Importing+InGrounds 578、WaitingSpace+Importing+OnRoad 66、Importing+Spawned+OnRoad+Blocked 25、GoingBack+Importing+Spawned+OnRoad+Blocked 14、Importing+Spawned+InGrounds 1、WaitingTarget+Importing+Spawned+InGrounds 1。byPath は ready 683、none 2。bySeenStopped は <1day 130、7days+ 555。byTarget の1位は building 0 15台。samples 40台のうち37台は位置 (3441, -1555)・blockCounter 0。敷地の外の3台は 35 (2830, -949) blockCounter 5、572 (2622, -1239) blockCounter 1、888 (1726, -829) blockCounter 82。seenStoppedDays 170 の車は 8、467、469、589(572 は敷地の外へ出た)
- `traffic(x=3440, z=-1560, radius=150)`: flow 52、cars 20、blocked 0、blockedOnRoads 0、blockedInBuildings 0、congestion 1、roadSegments 11、averageDensity 13。busiest は 17311 (3400, -1458) 56、20316 (3400, -1530) 47、10573 (3429, -1418) 23、14098 (3467, -1416) 19。blockedSpots なし
- `junction_info(x=3400, z=-1567)`: ok false、"no road junction within 40m"

### 月末(2050-06-30)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 651。byState は WaitingSpace+Importing+InGrounds 555、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 19、GoingBack+Importing+Spawned+OnRoad+Blocked 10、GoingBack+Importing+Spawned+InGrounds 2、Importing+Spawned+InGrounds 1。byPath は ready 648、none 3。bySeenStopped は <1day 106、7days+ 545。byTarget の1位は building 0 12台。samples 40台はどれも位置 (3441, -1555)、blockCounter 0。seenStoppedDays 180.1 の車は 8、467、469、589
- `traffic(x=3440, z=-1560, radius=150)`: flow 54、cars 22、blocked 0、blockedOnRoads 0、blockedInBuildings 0、congestion 1、roadSegments 11、averageDensity 10。busiest は 20316 (3400, -1530) 36、17311 (3400, -1458) 33、10573 (3429, -1418) 25、14098 (3467, -1416) 24。blockedSpots なし
- `junction_info(x=3400, z=-1567)`: ok false、"no road junction within 40m"
