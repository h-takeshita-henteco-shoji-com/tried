# m01 調査 s01-1(port) 貨物駅28755の空き待ちと13893の受け入れ

## 月末 (2050-01-31)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 611。WaitingSpace+Importing+InGrounds 520、WaitingSpace+Importing+OnRoad 62、Blocked 28。bySeenStopped は7日以上 527、1日未満 84。サンプル8台は (3441,-1555) の敷地内で WaitingSpace、最長 seenStoppedDays 30.1。
- `vehicles_stuck`(kind=truck, building=13893, limit=8): vehicles 0。
- `cargo`: stoppedTrucks 798(道の上 277、建物の中 521)。28755 の敷地内 520。stations の 28755 は vehiclesLeaving 789、vehiclesArriving 11。13893 は両方 0。

## 見回り2 (2050-01-21)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 653。WaitingSpace+Importing+InGrounds 531、WaitingSpace+Importing+OnRoad 61、Blocked 56。bySeenStopped は7日以上 503、1日未満 150。サンプルのうち敷地内の車は (3441,-1555) で WaitingSpace、最長 seenStoppedDays 20.1。
- `vehicles_stuck`(kind=truck, building=13893, limit=8): vehicles 0。
- `cargo`: stoppedTrucks 871(道の上 340、建物の中 531)。28755 の敷地内 531。stations の 28755 は vehiclesLeaving 812、vehiclesArriving 11。13893 は両方 0。

## 見回り1 (2050-01-11)

- `vehicles_stuck`(kind=truck, building=28755, limit=8): vehicles 615。WaitingSpace+Importing+InGrounds 505、WaitingSpace+Importing+OnRoad 64、Blocked 45。bySeenStopped は7日以上 472、1日未満 143。サンプル8台はすべて (3441,-1555) の敷地内で WaitingSpace。
- `vehicles_stuck`(kind=truck, building=13893, limit=8): vehicles 0。
- `cargo`: stoppedTrucks 809(道の上 286、建物の中 523)。28755 の敷地内 505。stations の 28755 は vehiclesLeaving 789、vehiclesArriving 11。13893 は両方 0。
