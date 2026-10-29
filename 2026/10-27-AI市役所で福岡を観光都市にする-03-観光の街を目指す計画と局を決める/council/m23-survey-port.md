# m23 調査 s23-1(port): 28755 の隣の貨物センター 13893 の車

問い: 13893(車 0、職員 43)が車を受けないのはなぜか。28755 の空き待ち(庫内)は見回りごとに減るか。

## 2051-11-12(見回り1)

- `cargo`: stoppedTrucks 961、stoppedInBuildings 619(28755 が618、13634 が1)、stoppedOnRoads 342。stations は 28755 が vehiclesLeaving 908 / vehiclesArriving 9。13893 は vehiclesLeaving 0 / vehiclesArriving 0。stoppedSpots 上位 (3437,-1545) 89台。Goods の stoppedTrucks 615(import 1025、local 472)
- `vehicles_stuck`(kind=truck, building=28755, limit=3): vehicles 758。byState は WaitingSpace+Importing+InGrounds 618、WaitingSpace+Importing+OnRoad 81、Importing+Spawned+OnRoad+Blocked 47 など。bySeenStopped は 7日以上 644、1日未満 114。サンプル: 車10(Goods 8000、目的 901、距離 5837、50日止まり)、車15(Goods 8000、目的 23569、距離 436、40日止まり)
- `buildings_near`(x=3529, z=-1555, r=60): 13893 Cargo Center、problems None、電気・水・下水 true、jobs workers 43、vehicles inUse 0

## 2051-11-22(見回り2)

- `cargo`: stoppedTrucks 1019、stoppedInBuildings 623(28755 が611、1366 が12)、stoppedOnRoads 396。28755 は vehiclesLeaving 918 / vehiclesArriving 11。13893 は 0 / 0。stoppedSpots 上位 (3435,-1540) 88台。Goods の stoppedTrucks 668
- `vehicles_stuck`(kind=truck, building=28755, limit=3): vehicles 759。WaitingSpace+Importing+InGrounds 611、WaitingSpace+Importing+OnRoad 76、Importing+Spawned+OnRoad+Blocked 52。7日以上 636、1日未満 123。車10(5837m)は60日、車15(436m)は50日、車18(2650m)は20日止まり
- `buildings_near`(x=3529, z=-1555, r=60): 13893 problems None、workers 41、vehicles inUse 0

## 2051-12-02(月末)

- `cargo`: stoppedTrucks 1051、stoppedInBuildings 631(28755 が613、1366 が18)、stoppedOnRoads 420。28755 は vehiclesLeaving 898 / vehiclesArriving 11。13893 は 0 / 0。stoppedSpots 上位 (3440,-1551) 80台。Goods の stoppedTrucks 700
- `vehicles_stuck`(kind=truck, building=28755, limit=3): vehicles 756。WaitingSpace+Importing+InGrounds 613、WaitingSpace+Importing+OnRoad 78、Importing+Spawned+OnRoad+Blocked 39、GoingBack+...+Blocked 24。7日以上 608、1日未満 148。車10は70日、車15は60日、車18は30日止まり(同じ車が続けて待っている)
- `buildings_near`(x=3529, z=-1555, r=60): 13893 problems None、workers 39、vehicles inUse 0
