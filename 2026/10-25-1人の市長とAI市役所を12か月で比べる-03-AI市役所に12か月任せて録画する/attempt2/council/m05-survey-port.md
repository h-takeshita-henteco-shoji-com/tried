# m05 調査の結果(port)

## s05-1 貨物駅28755の出口の端が道路とつながっていないか

問い: 28755 の出口の Cargo Connection の端 (3497, -1555/-1560) は、道路の点 (3495, -1565) の近くに交差点を作らずに終わっているか。

### 2050-05-11(見回り1)

- `net_near(x=3496, z=-1560, radius=40, service="Road")`: 区間2つ。15733 Small 4 Lane Road、start node 8479 (3495, -1490) → end node 21285 (3495, -1565)、長さ65、各向き2車線。22686 Small 4 Lane Road、start node 21285 (3495, -1565) → end node 15388 (3496, -1610)、長さ47、各向き2車線。service="Road" で絞ったので Cargo Connection の区間は返っていない
- `junction_info(x=3495, z=-1560)`: ok false、"no road junction within 40m"
- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 688。byState は WaitingSpace+Importing+InGrounds 551、WaitingSpace+Importing+OnRoad 70、Importing+Spawned+OnRoad+Blocked 46、GoingBack+Importing+Spawned+OnRoad+Blocked 19、Importing+Spawned+InGrounds 2。byPath は ready 686、none 2。bySeenStopped は <1day 147、7days+ 541。byTarget の1位は building 0(19台)。samples 40台はどれも位置 (3441, -1555)、blockCounter 0。いちばん長い seenStoppedDays は130(車 8、36、307、339、341、467、469)。荷は Goods、Lumber、Petrol、Coal、Food

### 2050-05-31(月末)

- `net_near(x=3496, z=-1560, radius=40, service="Road")`: 05-11 と同じ。15733(node 8479 (3495, -1490) → node 21285 (3495, -1565))と 22686(node 21285 → node 15388 (3496, -1610))、どちらも Small 4 Lane Road、各向き2車線
- `junction_info(x=3495, z=-1560)`: ok false、"no road junction within 40m"(05-11 と同じ)
- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 665。byState は WaitingSpace+Importing+InGrounds 556、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 33、GoingBack+Importing+Spawned+OnRoad+Blocked 10、GoingBack+Importing+Spawned+InGrounds 2。byPath は ready 663、none 2。bySeenStopped は <1day 216、7days+ 449。byTarget の1位は building 0(12台)。samples 40台のうち38台は位置 (3441, -1555)、2台(78、274)は (1903〜1931, -1048) で Blocked。seenStoppedDays 150 は車 8、307、467、469、572、579、589。05-11 の samples にいた車 36 は WaitingSpace+Importing+OnRoad、行き先 32709(338m)に変わり seenStoppedDays 0
