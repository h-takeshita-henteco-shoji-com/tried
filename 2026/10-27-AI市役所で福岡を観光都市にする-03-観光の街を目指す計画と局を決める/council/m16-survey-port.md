# m16 調査 s16-1(port): 貨物センター 13893 が車を出さない理由

## 2051-04-16(見回り1)

- `vehicles_stuck`(kind train、building 13893、limit 5): vehicles 0、samples なし
- `cargo` の stations 13893: vehiclesLeaving 0、vehiclesArriving 0。28755 は vehiclesLeaving 960、vehiclesArriving 11。stoppedInBuildings の 28755 は 641台
- `buildings_near`(x3529 z-1555 r30): 13893 は problems None、電気・水・下水 true、jobs.workers 50、vehicles.inUse 0

## 2051-05-06(月末)

- `vehicles_stuck`(kind train、building 13893、limit 5): vehicles 0、samples なし
- `cargo` の stations 13893: vehiclesLeaving 0、vehiclesArriving 0。28755 は vehiclesLeaving 918、vehiclesArriving 12。stoppedInBuildings の 28755 は 596台(街全体の stoppedInBuildings 605)
- `buildings_near`(x3529 z-1555 r30): 13893 は problems None、電気・水・下水 true、jobs.workers 49、vehicles.inUse 0
