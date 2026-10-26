# m03 調査の結果(economy)

## s03-2 原料がない工場33棟に原料が届かない理由を切り分ける

問い: 原料がない工場33棟は、原料の車が着かないのか(貨物駅28755の空き待ち)、原料の産地が足りないのか。
見立ては書かない(局が翌月に読んで決める)。

### 見回り1(2050-03-12)

- `cargo()`: trucks 2,276、stoppedTrucks 879(道路380、敷地の中499。28755 が477、港1366 が22)。原料・材料の import / 止まった台数は Coal 131/57、Food 241/45、Lumber 178/80、Petrol 192/87、Oil 5/0、Ore 2/0、Grain 2/0。どれも local 0、export 0。Goods は import 873、local 652、止まった610。noResources 33棟(場所の上位 (2765,-893) 17棟、(2164,1269) 10棟、(3992,-493) 3棟)。noGoods 174棟。28755 は vehiclesLeaving 708、vehiclesArriving 11
- `vehicles_stuck(kind="truck", building=3805, limit=10)`: vehicles 2。どちらも荷は Coal 8,000、出発は 28755、行き先は工場3805(H3 4x4 Mediumfactory07、(2540,-1174)、距離981)。状態は WaitingSpace+Importing+InGrounds 1台(見えて10日)、WaitingSpace+Importing+OnRoad 1台(見えて70日)。位置はどちらも (3441,-1555)。道順は ready
- `buildings_near(x=2784, z=-834, radius=250, problems_only=true, brief=true, limit=30)`: total 1。40341(L4 3x4 Villa01、(2668,-884)、Death)。原料がない印の建物は円の中に0

### 見回り2(2050-03-22)

- `cargo()`: trucks 2,273、stoppedTrucks 939(道路435、敷地の中504。28755 が499、港46112 が4、店7162 が1)。原料・材料の import / 止まった台数は Coal 137/73、Food 236/60、Lumber 174/83、Petrol 185/95、Oil 4/0、Ore 1/0、Logs 2/0。どれも local 0、export 0。Goods は import 866、local 668、止まった628。noResources 37棟(場所の上位 (2853,-903) 20棟、(2165,1282) 12棟、(3992,-493) 3棟)。noGoods 170棟。28755 は vehiclesLeaving 716、vehiclesArriving 12
- `vehicles_stuck(kind="truck", building=3805, limit=10)`: vehicles 2。見回り1と同じ2台(12919、15218)。荷は Coal 8,000、出発 28755、行き先 3805(距離981)。WaitingSpace+Importing+InGrounds(見えて20日)と WaitingSpace+Importing+OnRoad(見えて80日)。位置はどちらも (3441,-1555)
- `buildings_near(x=2784, z=-834, radius=250, problems_only=true, brief=true, limit=30)`: total 1。43900(L4 4x3 Villa01、(2784,-596)、Death)。原料がない印の建物は円の中に0

### 月末(2050-04-01)

- `cargo()`: trucks 2,271、stoppedTrucks 868(道路378、敷地の中490。28755 が486、港1366 が4)。原料・材料の import / 止まった台数は Coal 146/70、Food 251/56、Lumber 175/83、Petrol 186/88、Oil 5/0、Ore 1/0、Logs 3/0、Grain 1/0。どれも local 0、export 0。Goods は import 872、local 631、止まった571。noResources 35棟(場所の上位 (2805,-889) 17棟、(2192,1249) 12棟、(3992,-493) 3棟)。noGoods 169棟。28755 は vehiclesLeaving 714、vehiclesArriving 12
- `vehicles_stuck(kind="truck", building=3805, limit=10)`: vehicles 2。3回とも同じ2台(12919、15218)。荷は Coal 8,000、出発 28755、行き先 3805(距離981)。WaitingSpace+Importing+InGrounds(見えて30日)と WaitingSpace+Importing+OnRoad(見えて90日)。位置はどちらも (3441,-1555)
- `buildings_near(x=2784, z=-834, radius=250, problems_only=true, brief=true, limit=30)`: total 0
