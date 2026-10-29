# m06 調査 s06-1(port): 貨物駅28755の敷地内で待つ車

見立ては書かない。局が翌月に読む。

## 2050-06-11(見回り1)

- `vehicles_stuck` kind=truck、building=28755、limit=5: vehicles 577。byState は WaitingSpace+Importing+InGrounds 472、WaitingSpace+Importing+OnRoad 56、Importing+OnRoad+Blocked 31、GoingBack+Importing+OnRoad+Blocked 15 ほか。byPath は ready 574、none 3。bySeenStopped は 7日以上 458、1日未満 119。samples 5台はすべて (3441,-1555) で WaitingSpace+Importing+InGrounds、積荷は Goods 6000/8000、Petrol 8000、Coal 8000、blockCounter 0、waitCounter 0、seenStoppedDays 0〜69.9
- `traffic` x=3449、z=-1555、radius=60、limit=5: flow 53、cars 9、blocked 0、congestion 1、roadSegments 3、averageDensity 11。busiest は segment 20316(Large Road)(3400,-1530) density 33。blockedSpots なし
- `cargo`: stoppedTrucks 734(道の上 262、建物の中 472)。stoppedInBuildingsTop は 28755 が 472。stations の 28755 は vehiclesLeaving 741、vehiclesArriving 12。13893 は 0/0。shortages は noGoods 258、noResources 32

## 2050-06-21(見回り2)

- `vehicles_stuck` kind=truck、building=28755、limit=5: vehicles 594。byState は WaitingSpace+Importing+InGrounds 474、WaitingSpace+Importing+OnRoad 58、Importing+OnRoad+Blocked 48、GoingBack+Importing+OnRoad+Blocked 11、Congestion 2 ほか。byPath は ready 593、none 1。bySeenStopped は 7日以上 462、1日未満 132。samples 5台のうち4台は (3441,-1555) で WaitingSpace+InGrounds(seenStoppedDays 0〜80)、1台は (2236,-1135) で OnRoad+Blocked(blockCounter 5)
- `traffic` x=3449、z=-1555、radius=60、limit=5: flow 53、cars 10、blocked 0、congestion 1、averageDensity 10。busiest は 20316(Large Road)density 31。blockedSpots なし
- `cargo`: stoppedTrucks 812(道の上 318、建物の中 494)。stoppedInBuildingsTop は 28755 が 474、1366 が 20。stations の 28755 は vehiclesLeaving 753、vehiclesArriving 10。13893 は 0/0。stoppedSpots 先頭は (3434,-1538) 72台。shortages は noGoods 265、noResources 35

## 2050-07-01(月末)

- `vehicles_stuck` kind=truck、building=28755、limit=5: vehicles 594。byState は WaitingSpace+Importing+InGrounds 495、WaitingSpace+Importing+OnRoad 57、GoingBack+Importing+OnRoad+Blocked 20、Importing+OnRoad+Blocked 19 ほか。byPath は ready 591、none 3。bySeenStopped は 7日以上 449、1日未満 145。samples 5台はすべて (3441,-1555) で WaitingSpace+InGrounds(seenStoppedDays 0〜89.9)
- `traffic` x=3449、z=-1555、radius=60、limit=5: flow 53、cars 11、blocked 0、congestion 1、averageDensity 15。busiest は 20316(Large Road)density 41。blockedSpots なし
- `cargo`: stoppedTrucks 728(道の上 233、建物の中 495)。stoppedInBuildingsTop は 28755 が 495 のみ。stations の 28755 は vehiclesLeaving 759、vehiclesArriving 12。13893 は 0/0。shortages は noGoods 256、noResources 31
