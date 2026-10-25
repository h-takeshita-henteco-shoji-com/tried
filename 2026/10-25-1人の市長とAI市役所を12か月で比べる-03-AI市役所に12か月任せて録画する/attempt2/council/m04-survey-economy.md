# m04 調査 s04-2(economy)

問い: 貨物駅28755に溜まった Goods のトラックのうち、店が品物を待つ分(輸入の荷)はどれだけで、品物がない店の3つ目の集まり (961, 264) の店の行き先の荷と重なるか。

## 見回り1(2050-04-11)

- `buildings_near(x=961, z=264, radius=300, problem="NoGoods", limit=30)`: total 0(返った建物なし)
- `vehicles_stuck(kind="truck", building=28755, limit=30)`: vehicles 710。byState は WaitingSpace+Importing+InGrounds 591、WaitingSpace+Importing+OnRoad 73、Importing+Spawned+OnRoad+Blocked 35、GoingBack+Importing+Spawned+OnRoad+Blocked 6、GoingBack+Importing+Spawned+InGrounds 4、Importing+Spawned+InGrounds 1。byPath ready 705、none 5。bySeenStopped <1day 135、7days+ 575
  - byTarget(上位10): building 0 が10台、39818 Future Store (324, 251) 4台、45912 (-84, 132)、46772 (-2040, -1346)、36174 (2176, 467)、48389 (-1376, -1214)、47716 (-2564, -104)、785 (-1928, -1346)、44333 (-784, -14)、654 (-2256, -1346) が各3台。(961, 264) から300m以内の行き先は上位10にない
  - samples 30台のうち Goods は13台(8、36、55、210、229、248、274、307、377、418、461、463、467)。248 は空(amount 0)で GoingBack。ほかの12台の行き先と距離: 42705 Future Store 3,122m、46268 Shop13 5,637m、654 Shop05a 5,701m、48748 Future Store 2,960m、32257 Shop01 5,253m、43387 Shop04 3,205m、35557 Shop01 5,146m、31445 Shop15_c 6,121m、42057 Shop01 4,332m、41886 Shop01 5,050m、38221 Future Store 4,880m、48581 Shop01 4,422m。荷はどれも Importing
- `cargo()`: byCargo の Goods は import 933、export 0、local 375、stoppedTrucks 563。stoppedInBuildings 601(28755 が591)。noGoods 231。spots は (-1147, -1007) 54棟、(2220, 703) 51棟、(921, 257) 36棟。noResources 35

## 見回り2(2050-04-21)

- `buildings_near(x=961, z=264, radius=300, problem="NoGoods", limit=30)`: total 0(返った建物なし)
- `vehicles_stuck(kind="truck", building=28755, limit=30)`: vehicles 686。byState は WaitingSpace+Importing+InGrounds 577、WaitingSpace+Importing+OnRoad 74、Importing+Spawned+OnRoad+Blocked 28、GoingBack+Importing+Spawned+OnRoad+Blocked 4、ほか3台。byPath ready 685、none 1。bySeenStopped <1day 122、7days+ 564
  - byTarget(上位10): building 0 が6台、32387 Shop13 (2590, 968) 4台、47716 (-2564, -104) 4台、37571 (104, 34)、45677 (-2128, 68)、785 (-1928, -1346)、44583 (-1053, 132)、36174 (2176, 467)、654 (-2256, -1346)、39818 (324, 251) が各3台。(961, 264) から300m以内の行き先は上位10にない
  - samples 30台のうち Goods は10台(8、36、55、210、229、274、307、377、418、461)。行き先と距離は見回り1と同じ店(42705 3,122m、46268 5,637m、654 5,701m、48748 2,960m、32257 5,253m、43387 3,205m、35557 5,146m、31445 6,121m、42057 4,332m、41886 5,050m)。荷はどれも Importing。見回り1の samples にいた Goods の 248(空)と 463 は今回いない
- `cargo()`: byCargo の Goods は import 941、export 0、local 388、stoppedTrucks 576。stoppedInBuildings 606(28755 が578)。noGoods 241。spots は (-1164, -984) 60棟、(2229, 734) 50棟、(878, 243) 38棟。noResources 32

## 月末(2050-05-01)

- `buildings_near(x=961, z=264, radius=300, problem="NoGoods", limit=30)`: total 0(返った建物なし)
- `vehicles_stuck(kind="truck", building=28755, limit=30)`: vehicles 659。byState は WaitingSpace+Importing+InGrounds 563、WaitingSpace+Importing+OnRoad 74、Importing+Spawned+OnRoad+Blocked 12、GoingBack+Importing+Spawned+OnRoad+Blocked 9、GoingBack+Importing+Spawned+InGrounds 1。byPath ready 658、none 1。bySeenStopped <1day 106、7days+ 553
  - byTarget(上位10): building 0 が10台、37957 Future Store (1529, 392) 4台、47716 (-2564, -104) 4台、32056 Hotel (1856, 183)、42379 Future Store (2368, 986)、45677 (-2128, 68)、48978 (-2136, -1166)、785 (-1928, -1346)、654 (-2256, -1346)、38221 Future Store (-1340, -584) が各3台。(961, 264) から300m以内の行き先は上位10にない
  - samples 30台のうち Goods は11台(8、36、55、210、229、274、307、377、396、418、461)。行き先は 42705、46268、654、48748、32257、43387、35557、31445、48141 Shop10(2,665m、新しく0日)、42057、41886。荷はどれも Importing
- `cargo()`: byCargo の Goods は import 988、export 0、local 397、stoppedTrucks 553。stoppedInBuildings 585(28755 が563)。noGoods 230。spots は (-1159, -961) 61棟、(2219, 744) 50棟、(923, 258) 37棟。noResources 30
- 3回の推移: (961, 264) 半径300の NoGoods の印の建物 0 → 0 → 0。cargo の3つ目の spot は (921, 257) 36 → (878, 243) 38 → (923, 258) 37棟。Goods の止まったトラック 563 → 576 → 553
