# m02 調査 port(s02-3 貨物センター13893)

## 2050-02-10(見回り1)

- `vehicles_stuck` kind=truck, building=13893, limit=3: vehicles 0、samples なし
- `buildings_near`(x=3529, z=-1555, radius=30, limit=2): 13893 Cargo Center、problems None、電気・水・下水あり、workers 54、vehicles.inUse 0
- `cargo`: trucks 2,130、stoppedTrucks 860(道の上340、建物の中520)。13893 の vehiclesLeaving 0、vehiclesArriving 0。28755 は stoppedTrucks 514、vehiclesLeaving 778、vehiclesArriving 10。止まった場所の上位は (3439,-1550) の55台

## 2050-03-02(月末)

- `vehicles_stuck` kind=truck, building=13893, limit=3: vehicles 0、samples なし
- `buildings_near`(x=3529, z=-1555, radius=30, limit=2): 見回り1の再計測は省略(月末は vehicles_stuck と cargo のみ記録)
- `cargo`: trucks 2,121、stoppedTrucks 862(道の上358、建物の中504)。13893 の vehiclesLeaving 0、vehiclesArriving 0。28755 は stoppedTrucks 504、vehiclesLeaving 777、vehiclesArriving 13。止まった場所の上位は (3440,-1552) の58台
