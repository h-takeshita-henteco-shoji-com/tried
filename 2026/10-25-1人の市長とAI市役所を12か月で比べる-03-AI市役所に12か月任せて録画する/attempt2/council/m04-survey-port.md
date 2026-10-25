# m04 調査 s04-1(port)

問い: 貨物駅28755の敷地で30日以上止まった車と、新しく出ていく車は別の車か。出口が全く通らないのか、一部だけ通るのか。

## 見回り1(2050-04-11)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 710。byState は WaitingSpace+Importing+InGrounds 591、WaitingSpace+Importing+OnRoad 73、Importing+Spawned+OnRoad+Blocked 35、GoingBack+Importing+Spawned+OnRoad+Blocked 6、GoingBack+Importing+Spawned+InGrounds 4、Importing+Spawned+InGrounds 1。byPath ready 705、none 5。bySeenStopped <1day 135、7days+ 575。byTarget の1位は building 0(行き先なし)10台、ほかは店と工場で各3〜4台
  - samples 40台の seenStoppedDays: 100日 10台(vehicle 8、36、307、339、341、467、469、522、529、535)、90日 1台(464)、79.9日 5台(229、237、369、524、557)、40日 4台(81、246、377、418)、30日 4台(55、410、461、536)、20日 4台(185、274、444、449)、9.9日 3台(210、240、417)、0日 9台(113、248、371、448、460、463、478、526、571)。30日以上は24台
  - samples の状態: 37台が WaitingSpace+Importing(InGrounds 35、OnRoad 2: 377、410)、path ready、blockCounter 0、waitCounter 0、位置 (3441, -1555)。248 は GoingBack+Importing+Spawned+InGrounds、Goods 0、path none、行き先なし、位置 (3441, -1560)、0日
  - samples の荷: Goods 17、Lumber 8、Petrol 8、Food 3、Coal 3(248 を含む)
- `cargo()`: trucks 2,104、stoppedTrucks 905(道の上 304、敷地の中 601)。stoppedInBuildingsTop は 28755 が591、港1366 が9、工場19745 が1。stations の 28755 は vehiclesLeaving 852、vehiclesArriving 11。港1366 は 147 / 5、港46112 は 25 / 2、港32211 は 0 / 1。ほかの Cargo Center 7つは 0 / 0。stoppedSpots は (3441, -1555) 73台が1位。byCargo の stoppedTrucks は Goods 563、Petrol 99、Lumber 97、Coal 76、Food 70。noGoods 231、noResources 35
- `traffic(x=3430, z=-1555, radius=120)`: flow 54、cars 19、blocked 0、congestion 1、roadSegments 8、averageDensity 7。busiest は Large Road 20316 (3400,-1530) 密度31、17311 (3400,-1458) 密度30。blockedSpots なし

## 見回り2(2050-04-21)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 686。byState は WaitingSpace+Importing+InGrounds 577、WaitingSpace+Importing+OnRoad 74、Importing+Spawned+OnRoad+Blocked 28、GoingBack+Importing+Spawned+OnRoad+Blocked 4、Importing+Spawned+InGrounds 1、WaitingTarget+Importing+Spawned+OnRoad 1、WaitingTarget+WaitingSpace+Importing+InGrounds 1。byPath ready 685、none 1。bySeenStopped <1day 122、7days+ 564。byTarget の1位は building 0 が6台
  - samples 40台の seenStoppedDays: 110.1日 10台(8、36、307、339、341、467、469、572、579、589)、100.1日 1台(464)、90日 4台(229、237、369、524)、50.1日 5台(81、246、377、418、575)、40日 3台(55、410、461)、30.1日 5台(185、274、444、449、574)、20日 3台(210、240、417)、10.1日 4台(113、371、448、460)、0日 5台(190、316、413、701、707)。30日以上は28台
  - 見回り1の samples にいて、今回の samples にいない車: 248(GoingBack)、463(Goods、見回り1で0日)、478(Coal、0日)、522(Goods、100日)、526(Lumber、0日)、529(Petrol、100日)、535(Goods、100日)、536(Lumber、30日)、557(Goods、79.9日)、571(Goods、0日)。見回り1で limit 40 の外だった 572・574・575・579・589 が今回入った
  - vehicle 524(Goods、見回り1で WaitingSpace+Importing+InGrounds、79.9日)は、今回 Importing+Spawned+OnRoad+Blocked、blockCounter 6、位置 (2761, -1059)、行き先 40448 Shop01 まで 5,395m(見回り1は 6,155m)
  - ほかの samples は WaitingSpace+Importing(InGrounds、OnRoad は 377、410、574、575)、path ready、blockCounter 0、位置 (3441, -1555)
- `cargo()`: trucks 2,119、stoppedTrucks 918(道の上 312、敷地の中 606)。stoppedInBuildingsTop は 28755 が578、港1366 が17、港46112 が10、店3096 が1。stations の 28755 は vehiclesLeaving 842、vehiclesArriving 9。港1366 は 153 / 5、港46112 は 37 / 2、港32211 は 0 / 1。ほかの Cargo Center 7つは 0 / 0。stoppedSpots は (3440, -1551) 76台、(4074, -287) 16台、(3696, -246) 15台、(-1715, 100) 15台、(3534, -248) 14台。byCargo の stoppedTrucks は Goods 576、Petrol 95、Lumber 90、Coal 84、Food 73。noGoods 241、noResources 32
- `traffic(x=3430, z=-1555, radius=120)`: flow 52、cars 10、blocked 0、congestion 1、roadSegments 8、averageDensity 7。busiest は Large Road 20316 (3400,-1530) 密度33、17311 (3400,-1458) 密度23。blockedSpots なし

## 月末(2050-05-01)

- `vehicles_stuck(kind="truck", building=28755, limit=40)`: vehicles 659。byState は WaitingSpace+Importing+InGrounds 563、WaitingSpace+Importing+OnRoad 74、Importing+Spawned+OnRoad+Blocked 12、GoingBack+Importing+Spawned+OnRoad+Blocked 9、GoingBack+Importing+Spawned+InGrounds 1。byPath ready 658、none 1。bySeenStopped <1day 106、7days+ 553。byTarget の1位は building 0 が10台
  - samples 40台の seenStoppedDays: 120日 10台(8、36、307、339、341、467、469、572、579、589)、110日 1台(464)、99.9日 3台(229、237、369)、60日 5台(81、246、377、418、575)、50日 3台(55、410、461)、40日 5台(185、274、444、449、574)、30日 3台(210、240、417)、20日 4台(113、371、448、460)、9.9日 3台(190、316、413)、0日 3台(112 Petrol、396 Goods、495 Goods)。30日以上は30台
  - 見回り2の samples にいて、今回いない車: 524(見回り2で道の上 Blocked)、701(Goods、見回り2で0日)、707(Goods、0日)。見回り2で0日だった 190・316・413 は 9.9日で残る
  - samples はどれも WaitingSpace+Importing(InGrounds、OnRoad は 377、410、574、575)、path ready、blockCounter 0、waitCounter 0、位置 (3441, -1555)
- `cargo()`: trucks 2,142、stoppedTrucks 871(道の上 286、敷地の中 585)。stoppedInBuildingsTop は 28755 が563、港1366 が22。stations の 28755 は vehiclesLeaving 825、vehiclesArriving 11。港1366 は 157 / 7、港46112 は 22 / 3、港32211 は 0 / 1。ほかの Cargo Center 7つは 0 / 0。stoppedSpots は (3441, -1555) 74台、(3926, -263) 16台、(-1700, 97) 15台、(4054, -246) 9台、(2684, -958) 8台。byCargo の stoppedTrucks は Goods 553、Lumber 98、Petrol 82、Coal 73、Food 65。noGoods 230、noResources 30
- `traffic(x=3430, z=-1555, radius=120)`: flow 54、cars 17、blocked 0、congestion 1、roadSegments 8、averageDensity 12。busiest は Large Road 17311 (3400,-1458) 密度51、20316 (3400,-1530) 密度47。blockedSpots なし
- 3回の推移: 28755 に紐づくトラック 710 → 686 → 659、WaitingSpace+Importing+InGrounds 591 → 577 → 563、7days+ 575 → 564 → 553、<1day 135 → 122 → 106。28755 の vehiclesLeaving 852 → 842 → 825。出口近くの blocked 0 → 0 → 0
