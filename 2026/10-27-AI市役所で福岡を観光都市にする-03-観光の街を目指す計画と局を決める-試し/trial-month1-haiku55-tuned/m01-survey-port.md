# m01 調査 s01-2(port)貨物列車が 40031 などに向かわない理由

## 2050-01-31(月末)

- `vehicles_stuck`(kind="train", limit=12): 11 本、byTarget は 28755 に 11 本(40031 を含め他の駅は 0)。40031 は 10 日目に 0 台のため停止済み(active=false)。byState は Importing+OnRoad 9、WaitingCargo+Stopped+InGrounds 2。出発元は Train Connection 34128 と 32589 だけ
- `cargo`: stoppedInBuildings 605(28755 が 582、1366 が 22)。stoppedTrucks 935。stations の 40031・13893・3940・4740 ほか 28755 以外の貨物駅は vehiclesLeaving 0、vehiclesArriving 0。noGoods 226、noResources 28

## 2050-01-11(見回り1)

- `vehicles_stuck`(kind="train", limit=12): 11 本。byTarget は 28755 に 11 本(40031 と 13893・3940・4740 への列車は 0)。byState は Importing+OnRoad 8、Blocked 1、WaitingCargo+Stopped+InGrounds 2。7日以上止まって見えるのが 3 本(うち 28755 の手前 107m で Blocked、blockCounter 9 が 1 本)。出発元は Train Connection 34128 と 32589 の 2 つだけ
- `cargo`: stoppedInBuildings 525(28755 が 508、1366 が 15、46112 が 2)。stoppedTrucks 868。stations の 40031 は vehiclesLeaving 0、vehiclesArriving 0。13893・3940・4740 も 0。noGoods 235、noResources 23
