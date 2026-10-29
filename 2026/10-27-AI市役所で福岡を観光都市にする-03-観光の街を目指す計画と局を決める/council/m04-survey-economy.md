# m04 調査 s04-2 品物がない店235軒の原因(economy)

見立ては書かない。局が翌月に読んで決める。

## 2050-04-11(見回り1)

- `cargo`: trucks 2,155、stoppedTrucks 850(道の上 328、建物の中 522)。Goods は import 980、local 397、export 0、stoppedTrucks 545。noGoods の店 229(集まり: (-1129,-1054) 62、(2207,810) 52、(830,243) 39)。noResources の工場 34
- `traffic`(x=-1132, z=-1065, radius=400): flow 54、cars 243、blocked 66、congestion 127、averageDensity 38。blockedSpots は (-915,-905) 27、(-927,-1058) 26、(-916,-780) 8
- `vehicles_stuck`(kind="truck", building=null, limit=10): vehicles 1,223。byState は WaitingSpace+Importing+InGrounds 522、Importing+InGrounds 359、Importing+Spawned+OnRoad+Blocked 112、Spawned+OnRoad+Blocked 86 ほか。byPath は ready 1,207、none 16。bySeenStopped は 7days+ が 492、<1day が 731。Goods のサンプルで 28755 の敷地内に20〜100日止まった車が複数

## 2050-04-21(見回り2)

- `cargo`: trucks 2,099、stoppedTrucks 776(道の上 244、建物の中 532。28755 が 518、貨物港1366 が 14)。Goods は import 962、local 389、export 0、stoppedTrucks 466。noGoods の店 230(集まり: (-1122,-1026) 59、(2198,773) 58、(832,243) 37)。noResources の工場 32
- `traffic`(x=-1132, z=-1065, radius=400): flow 56、cars 235、blocked 6、congestion 100、averageDensity 37。blockedSpots は (-1095,-735) 6
- `vehicles_stuck`(kind="truck", building=null, limit=5): vehicles 1,111。byState は WaitingSpace+Importing+InGrounds 532、Importing+InGrounds 316、Importing+Spawned+OnRoad+Blocked 83、GoingBack+Importing+Spawned+OnRoad+Blocked 45 ほか。byPath は ready 1,095、none 16。bySeenStopped は 7days+ が 663、<1day が 448

## 2050-05-01(月末)

- `cargo`: trucks 2,083、stoppedTrucks 842(道の上 279、建物の中 563。28755 が 539、貨物港1366 が 24)。Goods は import 943、local 380、export 0、stoppedTrucks 537。noGoods の店 239(集まり: (2220,746) 61、(-1129,-967) 59、(782,229) 40)。noResources の工場 33
- `traffic`(x=-1132, z=-1065, radius=400): flow 54、cars 284、blocked 75、congestion 121、averageDensity 40。blockedSpots は (-933,-919) 35、(-952,-742) 14、(-918,-1043) 10
- `vehicles_stuck`(kind="truck", building=null, limit=5): vehicles 1,148。byState は WaitingSpace+Importing+InGrounds 563、Importing+InGrounds 291、Importing+Spawned+OnRoad+Blocked 102、Spawned+OnRoad+Blocked 72 ほか。byPath は ready 1,132、none 16。bySeenStopped は 7days+ が 644、<1day が 504。貨物港1366 の敷地内でも WaitingSpace の車(vehicle 53、行き先 distance 1,552)
