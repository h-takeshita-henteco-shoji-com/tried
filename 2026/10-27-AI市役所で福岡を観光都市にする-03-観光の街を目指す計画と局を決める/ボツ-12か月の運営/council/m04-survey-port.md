# m04 調査 s04-1 貨物駅28755の敷地内の待ち(port)

## 2050-04-12(見回り1)

- `vehicles_stuck`(kind=truck, building=28755, limit=5): vehicles 597。WaitingSpace+Importing+InGrounds 503、WaitingSpace+Importing+OnRoad 53、Importing+OnRoad+Blocked 30、GoingBack+Blocked 9。byPath は ready 596。bySeenStopped は 7日以上 484、1日未満 113。サンプルは (3441,-1555) で WaitingSpace。cargo は Petrol、Goods など
- `traffic`(x=3417, z=-1558, radius=40): flow 52、cars 6、blocked 0、congestion 1、roadSegments 1、averageDensity 35。busiest は Large Road (3400,-1530) density 35
- `cargo`: stoppedTrucks 778(道の上 275、建物の中 503)。stoppedInBuildings の上位は 28755 のみ 503。28755 の vehiclesLeaving 748、vehiclesArriving 12。stoppedSpots 先頭は (3440,-1552) 54。Goods 輸入 882 のうち止まり 486

## 2050-05-02(月末)

- `vehicles_stuck`(kind=truck, building=28755, limit=5): vehicles 620。WaitingSpace+Importing+InGrounds 530、WaitingSpace+Importing+OnRoad 58、Importing+OnRoad+Blocked 16、GoingBack+Blocked 9。byPath ready 618。bySeenStopped は 7日以上 381、1日未満 239。サンプルは (3441,-1555) で WaitingSpace。vehicle 20(Petrol)は 29.9日止まったまま
- `traffic`(x=3417, z=-1558, radius=40): flow 54、cars 7、blocked 0、congestion 1、averageDensity 44。busiest は Large Road (3400,-1530) density 44
- `cargo`: stoppedTrucks 773(道の上 235、建物の中 538)。28755 の敷地内 530。28755 の vehiclesLeaving 770、vehiclesArriving 10。stoppedSpots 先頭は (3441,-1555) 60
