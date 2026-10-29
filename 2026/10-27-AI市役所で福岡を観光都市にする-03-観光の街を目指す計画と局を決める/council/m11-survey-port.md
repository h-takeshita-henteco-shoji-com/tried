# m11 調査 s11-1(port): 貨物センター28755 の空き待ちの原因

## 2050-12-07(月末)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 726。WaitingSpace+Importing+InGrounds 626、WaitingSpace+Importing+OnRoad 71、Importing+OnRoad+Blocked 16、GoingBack+Blocked 9+1。7days+ が 615、<1day が 111。サンプルは敷地 (3441,-1555) の中で WaitingSpace、seenStoppedDays 29.9〜159.9
- `traffic`(x=3440, z=-1555, radius=150): flow 53、cars 17、blocked 0、congestion 1、averageDensity 13。busiest は Large Road 17311 の density 50

## 2050-11-27(見回り2)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 776。WaitingSpace+Importing+InGrounds 607、WaitingSpace+Importing+OnRoad 67、Importing+OnRoad+Blocked 60、GoingBack+Blocked 42。7days+ が 603、<1day が 173。サンプル8台は (3441,-1555) の敷地の中で WaitingSpace、seenStoppedDays 10〜149.9
- `traffic`(x=3440, z=-1555, radius=150): flow 50、cars 20、blocked 0、congestion 1、averageDensity 10。busiest は Large Road 17311 の density 50

## 2050-11-17(見回り1)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 713。WaitingSpace+Importing+InGrounds 568、WaitingSpace+Importing+OnRoad 67、Importing+OnRoad+Blocked 57、GoingBack+Blocked 20。bySeenStopped は 7days+ が 595、<1day が 118。サンプル8台はすべて (3441,-1555) の敷地の中で WaitingSpace。path は ready
- `traffic`(x=3440, z=-1555, radius=150): flow 53、cars 23、blocked 2、congestion 1、averageDensity 11。busiest は Large Road 17311 の density 48
