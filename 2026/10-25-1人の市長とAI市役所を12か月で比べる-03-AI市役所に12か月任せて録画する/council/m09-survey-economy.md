# m09 調査の結果(economy)

## s09-1 国境のつなぎ口に止まる輸入トラックが、品物がない店の元か

見立ては書かない。局が翌月に読んで決める。

### 見回り1(2050-09-08)

- `vehicles_stuck(kind="truck", limit=10)`
  - vehicles 679
  - byState: Importing+InGrounds 319、WaitingSpace+Importing+InGrounds 43、Spawned+OnRoad+Blocked 140、Importing+Spawned+OnRoad+Blocked 73、GoingBack+Spawned+OnRoad+Blocked 65、Importing+Spawned+InGrounds 12、GoingBack+Importing+Spawned+OnRoad+Blocked 11、ほか少数
  - byPath: none 17、ready 662
  - bySeenStopped: <1day 421、7days+ 258
  - byTarget: building 0(行き先なし)83、ほかは店とホテルが2〜3台ずつ(39818、40392、3271、38204、5892、40739、41412、40955、45311)
  - samples 10台のうち6台が (-4030,8619) で Importing+InGrounds、blockCounter 0・waitCounter 0、source building 0。荷は Food 2、Goods 2、Petrol 1、Coal 1。行き先は店(40739、43845)と工場(47433、17529、36279、4402)、距離 9,431〜12,674m。seenStoppedDays 10 が5台、0 が1台
  - 残り4台は道の上で Blocked((-921,-693)、(-921,-660)、(248,96)、(94,-262))。うち3台は港1366 発
- `cargo()`
  - trucks 1,920、stoppedTrucks 339(道の上 295、敷地の中 44。港1366 が34、港46112 が10)
  - Goods: import 405、local 684、stoppedTrucks 265
  - noGoods 129(spots (-1098,-871) 39、(2243,782) 36、(1052,295) 20)
  - noResources 33(spots (3066,-793) 19、(2451,1229) 6、(-2205,-605) 4)
  - 港1366 は出220前後・入11、46112 は出47・入2、32211 は入1。貨物駅はどれも出入り0
- `trade()`
  - import total 17,704(goods 5,488、oil 2,900、ore 2,270、forestry 2,721、agricultural 4,325)、export total 1
  - つなぎ口ごとの輸入の車: 道路 8840 (5788,-8649) 323、道路 27833 (5294,8649) 245、道路 19832 67、道路 43980 16、船 17593 (-4000,8653) 14、飛行機 10494 1。鉄道はどれも0

### 見回り2(2050-09-18)

- `vehicles_stuck(kind="truck", limit=10)`
  - vehicles 626
  - byState: Importing+InGrounds 311、WaitingSpace+Importing+InGrounds 32、Spawned+OnRoad+Blocked 95、Importing+Spawned+OnRoad+Blocked 79、GoingBack+Spawned+OnRoad+Blocked 68、GoingBack+Importing+Spawned+OnRoad+Blocked 24、Importing+Spawned+InGrounds 7、ほか少数
  - byPath: none 14、ready 612
  - bySeenStopped: <1day 362、7days+ 264
  - byTarget: building 0(行き先なし)97、ほかは店と工場が2〜4台ずつ(38204 が4、40739・41412 が3)
  - samples 10台のうち5台が (-4030,8619) で Importing+InGrounds、blockCounter 0・waitCounter 0、source building 0。荷は Coal 1、Goods 1、Petrol 1、Food 2。行き先は店40739(見回り1と同じ vehicle 94)と工場(25898、17529、36279、21656)、距離 8,780〜12,428m。seenStoppedDays は 20 が2台(vehicle 94、147)、10 が2台(111、254)、0 が1台
  - 残り5台は道の上で Blocked((3184,-170)、(-1824,-848)、(-1819,-1025)、(-1816,-1011)、(3987,-315))。どれも工場発の Goods(行きと戻り)、blockCounter 3〜34
- `cargo()`
  - trucks 1,946、stoppedTrucks 301(道の上 269、敷地の中 32。港1366 が32)
  - Goods: import 422、local 689、stoppedTrucks 240
  - noGoods 134(spots (-1125,-873) 40、(2241,741) 35、(1208,315) 20)
  - noResources 31(spots (2935,-860) 19、(-2205,-605) 4、(2444,1235) 4)
  - 港1366 は出214・入11、46112 は出54・入2、32211 は入1。貨物駅はどれも出入り0
- `trade()`
  - import total 18,098(goods 5,315、oil 3,053、ore 2,337、forestry 2,954、agricultural 4,439)、export total 1
  - つなぎ口ごとの輸入の車: 道路 8840 325、道路 27833 267、道路 19832 72、道路 43980 14、船 17593 14、鉄道 19489 1。飛行機0

### 月末(2050-09-28)

- `vehicles_stuck(kind="truck", limit=10)`
  - vehicles 685
  - byState: Importing+InGrounds 300、WaitingSpace+Importing+InGrounds 54、Spawned+OnRoad+Blocked 123、Importing+Spawned+OnRoad+Blocked 108、GoingBack+Spawned+OnRoad+Blocked 58、GoingBack+Importing+Spawned+OnRoad+Blocked 25、Importing+Spawned+InGrounds 7、Spawned+InGrounds 6、ほか少数
  - byPath: none 14、ready 671
  - bySeenStopped: <1day 440、7days+ 245
  - byTarget: building 0(行き先なし)85、ほかは店が3台ずつ(44532、42762、36123、724、40392、38204、47716、41412、48389)
  - samples 10台のうち6台が (-4030,8619) で Importing+InGrounds、blockCounter 0・waitCounter 0、source building 0。荷は Petrol 3、Coal 2、Food 1。行き先はどれも工場(15541、25898、33382、17529、21656、27541)、距離 8,780〜12,671m。seenStoppedDays は 20 が2台(vehicle 111、254)、10 が1台(63)、0 が3台
  - vehicle 94(見回り1・2で (-4030,8619) にいた、店40739 行きの Goods)は、港1366 発・(-1968,230) で Importing+Spawned+OnRoad+Blocked、blockCounter 42、行き先まで2,023m。vehicle 137(店43845 行きの Goods)も港1366 発・(-1846,-706) で Blocked、行き先まで966m
  - 残り2台は道の上で Blocked((3280,-258) の戻りの車、(1844,-1005) の工場6743 発の Goods)
- `cargo()`
  - trucks 1,969、stoppedTrucks 370(道の上 316、敷地の中 54。港1366 が54)
  - Goods: import 427、local 694、stoppedTrucks 266
  - noGoods 137(spots (-1115,-877) 42、(2215,720) 35、(1064,303) 20)
  - noResources 32(spots (2781,-921) 20、(2444,1235) 4、(-2168,-538) 3)
  - stoppedSpots: (-1967,298) 36、(-1967,156) 16、(1746,-864) 13、(3718,-249) 13、(-1908,-830) 12
  - 港1366 は出249・入10、46112 は出34・入3、32211 は入1。貨物駅はどれも出入り0
- `trade()`
  - import total 18,220(goods 5,211、oil 3,160、ore 2,416、forestry 2,998、agricultural 4,435)、export total 1
  - つなぎ口ごとの輸入の車: 道路 8840 311、道路 27833 277、道路 19832 86、道路 43980 18、船 17593 14。鉄道・飛行機は0

### 3回の並び(見回り1 → 見回り2 → 月末)

- `vehicles_stuck` の Importing+InGrounds: 319 → 311 → 300
- 同じく WaitingSpace+Importing+InGrounds: 43 → 32 → 54
- 同じく 7days+: 258 → 264 → 245
- `cargo` の noGoods: 129 → 134 → 137(実行前 151、取り壊し直後 121)
- `cargo` の Goods import: 405 → 422 → 427、local 684 → 689 → 694
- 港1366 の敷地の中で止まった車: 34 → 32 → 54
