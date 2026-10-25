# s01-2 ごみ車と霊柩車が止まる場所を見る(health)

問い: ごみの印(南西 -458,-1468 付近)と死体の印(2240,186 付近)は、容量不足ではなく収集車の渋滞や詰まりで出ているのか

## 2050-01-11(見回り1)

- `vehicles_stuck(kind="garbage", limit=30)`
  - vehicles 247。byPath ready 247。bySeenStopped <1day 247
  - byState: Congestion+Spawned+OnRoad+Blocked 63、Congestion+GoingBack+Spawned+OnRoad+Blocked 49、Congestion+GoingBack+Spawned+OnRoad 45、Spawned+OnRoad+Blocked 41、Congestion+Spawned+OnRoad 25、GoingBack+Spawned+OnRoad+Blocked 14、WaitingSpace+OnRoad 10
  - byTarget: 行き先なし(帰り道)108、ほかは1〜2台ずつ
  - samples の位置(一部): 2155,-933、2165,-917、2155,-911、2389,-949、2406,-946(5台が 2150〜2410,-950 付近)。-1818,-1587、-1818,-1699(blockCounter 95、88)、-1822,-1732、-1956,-1867。-576,-748、-708,-738。-426,-1838(33797 Combustion Plant 発)
- `vehicles_stuck(kind="hearse", limit=30)`
  - vehicles 182。byPath ready 167、none 15。bySeenStopped <1day 119、7days+ 63
  - byState: Congestion+Spawned+OnRoad+Blocked 52、Spawned+OnRoad+Blocked 42、Congestion+Spawned+OnRoad 36、Stopped+Spawned+OnRoad 11、ほか少数。WaitingTarget+…+InGrounds 7(path none)
  - byTarget: 行き先なし29、ほかは1台ずつ
  - samples の位置(一部): 2178,-34、2204,-111、1895,148(blockCounter 91)、2112,-842、2430,-946。3108,-392、3183,-81(blockCounter 125)、3339,-317
- `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`
  - 33797 Combustion Plant: storage 396,250 / 400,000(99%)、Processing rate 60,000 / week、収集車 9 / 34 使用中、働き手30
- 参考(同じ日の s01-3 の `complaints`): Death 55(hotspot 2155.8,91.7 に28)、Garbage 19(hotspot -465.7,-1356.7 に10)

## 2050-01-21(見回り2)

- `vehicles_stuck(kind="garbage", limit=30)`
  - vehicles 241。byPath ready 239、none 2。bySeenStopped <1day 88、7days+ 153
  - byState: Congestion+Spawned+OnRoad+Blocked 61、Congestion+GoingBack+Spawned+OnRoad+Blocked 52、Congestion+Spawned+OnRoad 49、Congestion+GoingBack+Spawned+OnRoad 36、Spawned+OnRoad+Blocked 22、GoingBack+Spawned+OnRoad+Blocked 11、WaitingSpace+OnRoad 8、Congestion+GoingBack+Spawned+InGrounds 2
  - byTarget: 行き先なし(帰り道)101、ほかは1台ずつ
  - samples の位置(一部): 2296,-949、2301,-946、2635,-946、2648,-949、2803,-949(-950 の東西の道に5台)。1845,-1040、1861,-1048、1844,-1017。-918,-1004、-916,-893、-702,-1299(41481 発、南西)。-1306,-442、-1386,-442(blockCounter 75、68)
- `vehicles_stuck(kind="hearse", limit=30)`
  - vehicles 164。byPath ready 152、none 12。bySeenStopped <1day 101、7days+ 63
  - byState: Congestion+Spawned+OnRoad 54、Congestion+Spawned+OnRoad+Blocked 34、Spawned+OnRoad+Blocked 22、Stopped+Spawned+OnRoad 16、ほか少数。WaitingTarget+Stopped+Spawned+InGrounds 4
  - byTarget: 行き先なし24、ほかは1台ずつ
  - samples の位置(一部): 2204,-115、1991,-121、1973,-114、2017,144、2196,-802、2196,-754、2156,-931、2330,-946。3163,-340、3261,-316、2912,-496
- `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`
  - 33797 Combustion Plant: storage 388,750 / 400,000(97%)、Processing rate 60,000 / week、収集車 4 / 34 使用中、働き手30
- 参考(同じ日の s01-3 の `complaints`): Death 52(hotspot 2170.2,-76.8 に20)、Garbage 19(hotspot -587.1,-1490 に9)

## 2050-01-31(月末)

- `vehicles_stuck(kind="garbage", limit=30)`
  - vehicles 260。byPath ready 256、none 4。bySeenStopped <1day 101、7days+ 159
  - byState: Congestion+Spawned+OnRoad+Blocked 71、Congestion+GoingBack+Spawned+OnRoad+Blocked 51、Congestion+Spawned+OnRoad 44、Spawned+OnRoad+Blocked 38、Congestion+GoingBack+Spawned+OnRoad 31、GoingBack+Spawned+OnRoad+Blocked 10、WaitingSpace+OnRoad 8、WaitingPath 3、InGrounds 4
  - byTarget: 行き先なし(帰り道)96、ほかは1台ずつ
  - samples の位置(一部): 2212,-950、2455,-949、2525,-946、2611,-949、2641,-949、2912,-946(blockCounter 92)、3017,-946、3025,-946(-950 の東西の道に8台)。-440,-746、-452,-746、-387,-744、-343,-733、-629,-739(-740 付近に5台)。1142,-725、1150,-726。-1818,-1354、-1790,-1282、-1638,-1207、-1818,-1650
  - 34(seenStoppedDays 20.1)、436・953・1392(20.1)は見回り1から止まって見える
- `vehicles_stuck(kind="hearse", limit=30)`
  - vehicles 167。byPath ready 156、none 11。bySeenStopped <1day 112、7days+ 55
  - byState: Congestion+Spawned+OnRoad 53、Congestion+Spawned+OnRoad+Blocked 36、Spawned+OnRoad+Blocked 29、Stopped+Spawned+OnRoad 16、ほか少数
  - byTarget: 行き先なし21、ほかは1台ずつ
  - samples の位置(一部): 2156,-934(blockCounter 78)、2521,-949、2260,-862、2761,-1087、2761,-996、2581,-1242。1967,149(blockCounter 108)、2455,125。3201,-313(blockCounter 85、seenStoppedDays 30.1)、3014,-492
- `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`
  - 33797 Combustion Plant: storage 322,500 / 400,000(80%)、Processing rate 60,000 / week、収集車 21 / 34 使用中、働き手29
- 参考(同じ日の s01-3 の `complaints`): Death 49(hotspot 2215.2,-37.9 に18)、Garbage 33(hotspot -466.6,-1465.9 に14)
