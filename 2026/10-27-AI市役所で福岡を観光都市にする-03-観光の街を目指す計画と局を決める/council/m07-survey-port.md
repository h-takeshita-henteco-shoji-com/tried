# m07 調査 s07-1 貨物センター28755の止まりの経過(port)

## 2050-07-10(見回り1)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 666。byState は WaitingSpace+Importing+InGrounds 550、WaitingSpace+Importing+OnRoad 63、Importing+OnRoad+Blocked 41、GoingBack+OnRoad+Blocked 11、GoingBack+InGrounds 1。bySeenStopped は <1day 150、7days+ 516。サンプルは(3441,-1555)で seenStoppedDays 0〜90
- `cargo`: stoppedTrucks 903、stoppedInBuildings 567(28755 が 550、Cargo Harbor 1366 が 16)、stoppedOnRoads 336。stoppedSpots 上位は (3439,-1551) 65台。byCargo の Goods は止まり 583。28755 の vehiclesLeaving 859、vehiclesArriving 12
- `traffic`(x3440 z-1555 r150): blocked 0、cars 18、congestion 1、flow 54、averageDensity 11

## 2050-07-20(見回り2)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 662。byState は WaitingSpace+Importing+InGrounds 542、WaitingSpace+Importing+OnRoad 65、Importing+OnRoad+Blocked 43、GoingBack+OnRoad+Blocked 12。bySeenStopped は <1day 133、7days+ 529。vehicle 88(Lumber)は seenStoppedDays 100、143(Petrol)は 80
- `cargo`: stoppedTrucks 848、stoppedInBuildings 542(すべて 28755)、stoppedOnRoads 306。stoppedSpots 上位は (3441,-1555) 65台。Goods の止まり 534。28755 の vehiclesLeaving 845、vehiclesArriving 10
- `traffic`(x3440 z-1555 r150): blocked 0、cars 16、congestion 1、flow 57、averageDensity 12

## 2050-07-30(月末)

- `vehicles_stuck`(kind=truck, building=28755, limit=3): vehicles 645。byState は WaitingSpace+Importing+InGrounds 514、WaitingSpace+Importing+OnRoad 70、Importing+OnRoad+Blocked 38、GoingBack+OnRoad+Blocked 20、そのほか3。bySeenStopped は <1day 128、7days+ 517。vehicle 8 は seenStoppedDays 80.1
- `cargo`: 月末は呼んでいない(取得失敗ではなく、見回り2の値が最新)
- `traffic`(x3440 z-1555 r150): blocked 0、cars 19、congestion 1、flow 56、averageDensity 10
