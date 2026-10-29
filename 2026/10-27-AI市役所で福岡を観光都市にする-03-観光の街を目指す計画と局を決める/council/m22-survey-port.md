# m22 調査 s22-2 (port) 28755 で空き待ちのトラックの行き先の遠さ

## 2051-10-13(見回り1)

- `vehicles_stuck`(kind="truck", building=28755, limit=8): vehicles 753。byState: WaitingSpace+Importing+InGrounds 633、WaitingSpace+Importing+OnRoad 80、Importing+Spawned+OnRoad+Blocked 28、GoingBack 9、Congestion 1、InGrounds 2。bySeenStopped: <1day 117、7days+ 636
- samples 8台の行き先までの距離(m)と荷: 5837(Goods 8000)、436(Goods 8000)、4579(Goods 6000)、6014(Lumber 8000)、3140(Lumber 8000)、1133(Goods 6000、走行中)、1307(Lumber 8000)、5882(Lumber 8000)。止まって見えている日数は 0 から 100.1
- byTarget 上位は 1 行き先あたり 3 から 4 台で、特定の店への集中はない
- `cargo()`: stoppedTrucks 966(道の上 333、建物の中 633)。28755 は vehiclesLeaving 917、vehiclesArriving 11。stoppedInBuildingsTop は 28755 の 633 のみ。noGoods 229、noResources 29。40031 は vehiclesLeaving 0、vehiclesArriving 0

## 2051-11-02(月末)

- `vehicles_stuck`(kind="truck", building=28755, limit=8): vehicles 763。byState: WaitingSpace+Importing+InGrounds 629、WaitingSpace+Importing+OnRoad 91、Importing+Spawned+OnRoad+Blocked 27、GoingBack 16。bySeenStopped: <1day 225、7days+ 538
- samples 8台の行き先までの距離(m)と荷: 5837(Goods 8000)、1438(Food 8000)、436(Goods 8000)、1541(Food 8000)、2650(Goods 8000)、4927(Goods 6000)、4579(Goods 6000)、6014(Lumber 8000)。車 10、15、31、51 は見回り1と同じ車で、止まった日数が 20.1→40.1、10.1→30.1、40.1→60.1、80→100 と増えた
- `cargo()`: stoppedTrucks 973(道の上 338、建物の中 635)。28755 は vehiclesLeaving 915、vehiclesArriving 9、stoppedTrucks 629。noGoods 215、noResources 29。40031 は vehiclesLeaving 0、vehiclesArriving 0
