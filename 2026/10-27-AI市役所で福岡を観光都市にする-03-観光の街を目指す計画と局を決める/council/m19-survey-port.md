# m19 調査 s19-2(port)13893 に列車が来ない理由と、28755 の空き待ち

問い: 13893 に列車が来ない理由は何か。28755 の敷地内の空き待ちは減るか。

## 2051-07-15(見回り1)

- `vehicles_stuck`(kind train, limit 20): vehicles 11。行き先はすべて 28755(Cargo Center)で、13893 を行き先にする列車は 0。byState: Importing+Spawned+OnRoad 8、Importing+Spawned+InGrounds 1、WaitingCargo+Stopped+Importing+InGrounds 2。byPath: ready 9、none 2。bySeenStopped: <1day 7、7days+ 4。出発元は Train Connection 32589 と 34128。28755(3475,-1530)の敷地内に 1 台(vehicle 9930、10 日止まり)
- `vehicles_stuck`(kind truck, building 28755, limit 5): vehicles 769。byState: WaitingSpace+Importing+InGrounds 620、WaitingSpace+Importing+OnRoad 102、Importing+Spawned+OnRoad+Blocked 30、GoingBack+Importing+Spawned+OnRoad+Blocked 16、GoingBack+Importing+Spawned+InGrounds 1。bySeenStopped: <1day 144、7days+ 625。サンプル 5 台は WaitingSpace、積み荷 8000(Goods、Food、Lumber、Coal)、70〜190 日止まり

## 2051-07-25(見回り2)

- `vehicles_stuck`(kind train, limit 20): vehicles 12。行き先はすべて 28755 で、13893 を行き先にする列車は 0。byState: Importing+Spawned+OnRoad 9、Stopped+Importing+Spawned+OnRoad 1、WaitingCargo+Stopped+Importing+InGrounds 2。byPath: ready 10、none 2。bySeenStopped: <1day 10、7days+ 2。出発元は Train Connection 32589 と 34128
- `vehicles_stuck`(kind truck, building 28755, limit 5): vehicles 759。byState: WaitingSpace+Importing+InGrounds 609、WaitingSpace+Importing+OnRoad 102、Importing+Spawned+OnRoad+Blocked 35、GoingBack+Importing+Spawned+OnRoad+Blocked 11、GoingBack+Importing+Spawned+InGrounds 2。bySeenStopped: <1day 132、7days+ 627。サンプルの積み荷は 8000(Goods、Lumber、Food)、80〜200 日止まり

## 2051-08-04(月末)

- `vehicles_stuck`(kind train, limit 20): vehicles 10。行き先はすべて 28755 で、13893 を行き先にする列車は 0。byState: Importing+Spawned+OnRoad 8、Stopped+Importing+Spawned+OnRoad 1、WaitingCargo+Stopped+Importing+InGrounds 1。byPath: ready 9、none 1。bySeenStopped: <1day 7、7days+ 3。出発元は Train Connection 32589 と 34128
- `vehicles_stuck`(kind truck, building 28755, limit 5): vehicles 754(7/15 は 769、7/25 は 759)。byState: WaitingSpace+Importing+InGrounds 617、WaitingSpace+Importing+OnRoad 100、Importing+Spawned+OnRoad+Blocked 26、GoingBack+Importing+Spawned+OnRoad+Blocked 10、GoingBack+Importing+Spawned+InGrounds 1。bySeenStopped: <1day 134、7days+ 620。サンプルの積み荷は 8000(Goods、Lumber)、10〜210 日止まり
