# m12 調査 port(s12-1)

## 2050-11-28(実行直後、見回り1の前の基準)

- `vehicles_stuck` kind=truck building=28755 limit=10: vehicles 554。byState は WaitingSpace+Importing+InGrounds 458、WaitingSpace+Importing+OnRoad 49、Importing+OnRoad+Blocked 35、GoingBack+Importing+OnRoad+Blocked 11、InGrounds 1。bySeenStopped は 7days+ が 397、<1day が 157。byPath は ready 553。荷物は Goods(6000〜8000)、Lumber、Petrol。行き先は市内の店・工場で、距離は 411〜6222m。位置はどれも (3441,-1555)
- `cargo`: stoppedInBuildings 489(28755 が 458)、stoppedOnRoads 268。28755 の vehiclesLeaving 704、vehiclesArriving 12。stoppedSpots の先頭は (3440,-1552) 50台。shortages は noGoods 253、noResources 29
- `buildings_near` x=3449 z=-1555 radius=60 brief=true: 28755 のみ。problems は "Garbage, MajorProblem"

## 2050-12-28(月末)

- `vehicles_stuck` kind=truck building=28755 limit=3: vehicles 589。WaitingSpace+Importing+InGrounds 500、WaitingSpace+Importing+OnRoad 48、Importing+OnRoad+Blocked 30、GoingBack+Blocked 11。7days+ 465、<1day 124。byPath は ready 589。位置は (3441,-1555)。先頭の2台は止まって 59.9 日
- `cargo`: stoppedInBuildings 500(28755 が 500)、stoppedOnRoads 290。28755 の vehiclesLeaving 731、vehiclesArriving 12。Goods の stoppedTrucks 489。noGoods 267、noResources 33
- `buildings_near` x=3449 z=-1555 radius=60 brief=true: 28755 のみ。problems は "Garbage, MajorProblem"

## 2050-12-18(見回り2)

- `vehicles_stuck` kind=truck building=28755 limit=10(limit 3 で呼んだ): vehicles 596。WaitingSpace+Importing+InGrounds 511、WaitingSpace+Importing+OnRoad 49、Importing+OnRoad+Blocked 26、GoingBack+Blocked 10。7days+ 437、<1day 159。byPath は ready 596。位置は (3441,-1555)
- `cargo`: stoppedInBuildings 514(28755 が 511)、stoppedOnRoads 245。28755 の vehiclesLeaving 733、vehiclesArriving 13。Goods の stoppedTrucks 463
- `buildings_near` x=3449 z=-1555 radius=60 brief=true: 28755 のみ(次の呼びで確認)

## 2050-12-08(見回り1)

- `vehicles_stuck` kind=truck building=28755 limit=10: vehicles 551。WaitingSpace+Importing+InGrounds 468、WaitingSpace+Importing+OnRoad 47、Importing+OnRoad+Blocked 24、GoingBack+Blocked 12。bySeenStopped は 7days+ 422、<1day 129。byPath は ready 551。位置は (3441,-1555)。荷物は Goods、Food、Lumber、Petrol
- `cargo`: stoppedInBuildings 469(28755 が 468)、stoppedOnRoads 250。28755 の vehiclesLeaving 718、vehiclesArriving 12。stoppedSpots 先頭 (3438,-1546) 51台
- `buildings_near` x=3449 z=-1555 radius=60 brief=true: 28755 のみ。problems は "Garbage, MajorProblem"
