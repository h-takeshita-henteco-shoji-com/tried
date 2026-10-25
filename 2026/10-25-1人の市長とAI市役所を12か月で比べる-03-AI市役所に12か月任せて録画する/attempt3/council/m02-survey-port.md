# s02-1 貨物駅28755 の出口で、出し入れの速さが止めているか(port)

問い: 空き待ちの約500台は、出口の1点(3441,-1555)での出し入れの速さで止まっているのか。予算の試し(m02-2、鉄道 100→120%、2050-01-31 に実行)の前後で流れる量が変わるか。

## 実行前の基準(2050-01-31、m02-2 の確かめとして測った)

- `cargo()`: stoppedInBuildings 496(全部28755)、stoppedTrucks 778、stoppedOnRoads 282、28755 の vehiclesLeaving 746・vehiclesArriving 12、stoppedSpots 先頭 3439,-1551 が56、noGoods 231、noResources 27
- `vehicles_stuck(kind="truck", building=28755, limit=10)`: vehicles 597、WaitingSpace+Importing+InGrounds 496、WaitingSpace+Importing+OnRoad 54、Importing+Spawned+OnRoad+Blocked 38、GoingBack+…+Blocked 9。bySeenStopped <1day 142、7days+ 455。標本の InGrounds は全部 3441,-1555

## 見回り1(2050-02-10)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`: vehicles 601。WaitingSpace+Importing+InGrounds 519、WaitingSpace+Importing+OnRoad 50、Importing+Spawned+OnRoad+Blocked 14、GoingBack+Importing+Spawned+OnRoad+Blocked 15、Importing+Spawned+InGrounds 2、WaitingPath+Importing+Spawned+OnRoad 1。byPath ready 599・none 2。bySeenStopped <1day 148、7days+ 453。標本の InGrounds は全部 3441,-1555、seenStoppedDays 40.1 が4台(vehicle 8、36、156、183)
- `cargo()`: stoppedInBuildings 527(28755 が519、港1366 が8)、stoppedTrucks 809、stoppedOnRoads 282。28755 の vehiclesLeaving 772・vehiclesArriving 12。stoppedSpots 先頭 3441,-1555 が50。noGoods 218、noResources 32。cargoTrains 12
- `buildings_near(x=3449, z=-1555, radius=120, service="PublicTransport", brief=false, limit=5)`: 28755 は workers 55、vehicles.inUse 772、problems None。13893(3529,-1555)は workers 50、vehicles.inUse 0、problems None

## 見回り2(2050-02-20)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`: vehicles 628。WaitingSpace+Importing+InGrounds 526、WaitingSpace+Importing+OnRoad 51、Importing+Spawned+OnRoad+Blocked 32、GoingBack+Importing+Spawned+OnRoad+Blocked 19。byPath ready 628。bySeenStopped <1day 141、7days+ 487。標本の InGrounds は全部 3441,-1555、seenStoppedDays 50.1 が4台(vehicle 8、36、156、183)
- `cargo()`: stoppedInBuildings 527(28755 が526、38371 が1)、stoppedTrucks 827、stoppedOnRoads 300。28755 の vehiclesLeaving 791・vehiclesArriving 14。stoppedSpots 先頭 3441,-1555 が51。noGoods 224、noResources 37。cargoTrains 14
- `buildings_near(x=3449, z=-1555, radius=120, service="PublicTransport", brief=false, limit=5)`: 28755 は workers 54、vehicles.inUse 791、problems None。13893 は workers 49、vehicles.inUse 0、problems None

## 月末(2050-03-02)

- `vehicles_stuck(kind="truck", building=28755, limit=10)`: vehicles 634。WaitingSpace+Importing+InGrounds 534、WaitingSpace+Importing+OnRoad 51、Importing+Spawned+OnRoad+Blocked 28、GoingBack+Importing+Spawned+OnRoad+Blocked 20、Importing+Spawned+InGrounds 1。byPath ready 633・none 1。bySeenStopped <1day 149、7days+ 485。標本の InGrounds は全部 3441,-1555、seenStoppedDays 60 が2台(vehicle 8、183)
- `cargo()`: stoppedInBuildings 555(28755 が534、港1366 が20、46939 が1)、stoppedTrucks 874、stoppedOnRoads 319。28755 の vehiclesLeaving 807・vehiclesArriving 14。stoppedSpots 先頭 3441,-1555 が51。noGoods 229、noResources 34。cargoTrains 14
- `buildings_near(x=3449, z=-1555, radius=120, service="PublicTransport", brief=false, limit=5)`: 28755 は workers 53、vehicles.inUse 807、problems Garbage。13893 は workers 50、vehicles.inUse 0、problems None
- 参考(m02-2 の確かめで測った `economy_breakdown`): PublicTransportTrain の支出 10,973 → 12,701
