# m01 調査 s01-3(economy): 品物がない店が増える道

見立ては書かない。局が翌月に読んで決める。

## 2050-01-31(月末)

- `cargo`: shortages.noGoods 222棟。spots は (-1055,-708) 68棟、(2249,742) 43棟、(1096,307) 35棟。noResources 29棟。stoppedTrucks 807(道の上 314、建物の中 493)。stoppedSpots 上位は (3437,-1543) 65台、(-1714,97) 23台、(5784,-8636) 12台、(-2030,506) 11台、(1499,-759) 11台。荷物別の止まった台数は Goods 521、Lumber 93、Petrol 83、Coal 71、Food 39
- `vehicles_stuck`(kind=truck, limit=10): vehicles 1147。byState は WaitingSpace+Importing+InGrounds 492、Importing+InGrounds 325、Importing+Spawned+OnRoad+Blocked 108、Spawned+OnRoad+Blocked 67、GoingBack 系の Blocked 71、ほか。bySeenStopped は <1day 454、7days+ 693。サンプルの Blocked は (-1688,108) blockCounter 56(Cargo Harbor 1366 発)、(-1935,-1012) blockCounter 58(Bigfactory06 発)

## 2050-01-21(見回り2)

- `cargo`: shortages.noGoods 228棟。spots は (-1097,-785) 73棟、(2217,745) 41棟、(1094,304) 33棟。noResources 26棟。stoppedTrucks 859(道の上 358、建物の中 501)。stoppedSpots 上位は (3441,-1552) 59台、(-1910,118) 23台、(3488,-1328) 18台、(2911,-948) 15台、(3946,-276) 14台。荷物別の止まった台数は Goods 549、Petrol 94、Lumber 87、Coal 77、Food 52
- `vehicles_stuck`(kind=truck, limit=10): vehicles 1187。byState は WaitingSpace+Importing+InGrounds 501、Importing+InGrounds 316、Importing+Spawned+OnRoad+Blocked 129、Spawned+OnRoad+Blocked 94、GoingBack 系の Blocked 75、ほか。bySeenStopped は <1day 496、7days+ 691。サンプルの Blocked は (1921,64) blockCounter 95(Road Connection 発、Shop10 行き。seenStoppedDays 10)

## 2050-01-11(見回り1)

- `cargo`: shortages.noGoods 236棟。spots は (-1076,-767) 77棟、(2223,721) 44棟、(1098,297) 33棟。noResources 23棟。stoppedTrucks 810(道の上 292、建物の中 518)。stoppedSpots 上位は (3440,-1552) 65台、(2233,-1119) 14台、(-1947,126) 13台、(-675,92) 10台、(2269,-1228) 10台。荷物別の止まった台数は Goods 510、Petrol 91、Lumber 87、Coal 71、Food 51
- `vehicles_stuck`(kind=truck, limit=10): vehicles 1121。byState は WaitingSpace+Importing+InGrounds 517、Importing+InGrounds 298、Importing+Spawned+OnRoad+Blocked 83、Spawned+OnRoad+Blocked 65、GoingBack+Spawned+OnRoad+Blocked 46、ほか。bySeenStopped は <1day 657、7days+ 464。サンプルの Blocked は (2086,64) blockCounter 25(Road Connection 発、Shop10 行き)、(4013,-349) blockCounter 16
