# m03 調査 s03-1 貨物センター28755の止まったトラック

## 2050-03-12(見回り1)

- `vehicles_stuck`(kind=truck、building=28755、limit=10): vehicles 618。WaitingSpace+Importing+InGrounds 507、WaitingSpace+Importing+OnRoad 61、Blocked(OnRoad)49、GoingBack 1。bySeenStopped は 7日以上 485、1日未満 133。サンプルは全て x3441 z-1555 の敷地内で Importing(Goods/Food/Coal)。止まって70日の車あり
- `cargo`: stoppedTrucks 832(道の上325、建物の中507=すべて28755)。28755 は vehiclesLeaving 793、vehiclesArriving 13。stoppedSpots 先頭は (3438,-1548) 65台。品物がない店226、原料がない工場34
- `traffic`(x=3440、z=-1552、radius=200): flow 52、cars 20、blocked 0、congestion 1、averageDensity 19。busiest は segment 18170(Small 4 Lane Road)密度75

## 2050-03-22(見回り2)

- `vehicles_stuck`(kind=truck、building=28755、limit=10): vehicles 621。WaitingSpace+Importing+InGrounds 500、WaitingSpace+Importing+OnRoad 54、Blocked(OnRoad)63。bySeenStopped は 7日以上 490、1日未満 131。サンプルは前回と同じ車(vehicle 8 は80日)が x3441 z-1555 の敷地内
- `cargo`: stoppedTrucks 831(道の上309、建物の中522。28755 が501、貨物港1366 が21)。28755 は vehiclesLeaving 807、vehiclesArriving 11。品物がない店228、原料がない工場36
- `traffic`(x=3440、z=-1552、radius=200): flow 53、cars 25、blocked 0、congestion 1、averageDensity 16。busiest は segment 18170 密度70

## 2050-04-01(月末)

- `vehicles_stuck`(kind=truck、building=28755、limit=10): vehicles 637。WaitingSpace+Importing+InGrounds 516、WaitingSpace+Importing+OnRoad 57、Blocked(OnRoad)57、GoingBack/InGrounds 6。bySeenStopped は 7日以上 477、1日未満 160。vehicle 8・36・156・183 は90日止まったまま(x3441 z-1555)。Blocked の車は (763,-696) 付近にも出た
- `cargo`: stoppedTrucks 804(道の上287、建物の中517=すべて28755)。28755 は vehiclesLeaving 820、vehiclesArriving 12。品物がない店235、原料がない工場32
- `traffic`(x=3440、z=-1552、radius=200): flow 53、cars 24、blocked 0、congestion 1、averageDensity 19。busiest は segment 18170 密度66

