# m05 調査 s05-1(port)貨物駅28755の敷地内の待ちの原因

## 2050-05-12(見回り1)

- `vehicles_stuck` kind=train、limit=10: 列車11本、すべて目的地は 28755。Importing+OnRoad 8、Importing+InGrounds 1、WaitingCargo+Stopped+Importing+InGrounds 2(path none、waitCounter 32 と 13、位置は外の接続点付近 (6997,-8618)、(7281,-8615))。出発元は Train Connection 34128 と 32589。1本は10両で荷15
- `cargo`: stoppedTrucks 830、stoppedInBuildings 508(28755 が 506)、stoppedOnRoads 322。stations: 28755 は vehiclesLeaving 740、vehiclesArriving 11。13893 は vehiclesLeaving 0、vehiclesArriving 0。Goods 止まり541、Petrol 88、Lumber 82、Coal 63、Food 56
- `vehicles_stuck` kind=truck、building=13893、limit=3: vehicles 0

## 2050-06-01(月末)

- `vehicles_stuck` kind=train、limit=10: 列車10本、すべて目的地は 28755。Importing+OnRoad 8、WaitingCargo+Stopped+Importing+InGrounds 2(path none、waitCounter 18 と 44、位置は外の接続点付近 (6997,-8618)、(7277,-8616))。1本は10両で荷15
- `cargo`: stoppedTrucks 816、stoppedInBuildings 482(28755 が 478)、stoppedOnRoads 334。stations: 28755 は vehiclesLeaving 749、vehiclesArriving 10。13893 は vehiclesLeaving 0、vehiclesArriving 0。Goods 止まり522、Petrol 90、Lumber 81、Coal 65、Food 58。stoppedSpots 先頭は (3438,-1547) 67台
- `vehicles_stuck` kind=truck、building=13893、limit=3: vehicles 0
