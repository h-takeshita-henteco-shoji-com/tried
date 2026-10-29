# m01 調査 s01-1(roads)貨物駅28755で待つトラック

## 月末(2050-01-31)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 591。WaitingSpace+Importing+InGrounds 502、WaitingSpace+Importing+OnRoad 55、Importing+Spawned+OnRoad+Blocked 25。bySeenStopped は 7days+ が 483。vehicle 8, 36, 120 は seenStoppedDays 30。5台中3台が WaitingSpace+InGrounds で位置 (3441,-1555) のまま
- `traffic`(x=3417, z=-1557, radius=60): flow 51、cars 9、blocked 0、congestion 1、averageDensity 19。区間20316 density 39
- `cargo`: stoppedTrucks 807、stoppedOnRoads 304、stoppedInBuildings 503。貨物駅28755は 502台。vehiclesLeaving 749、vehiclesArriving 9。stoppedSpots 先頭 (3440,-1552) の 56台。品物がない店 230、原料がない工場 28

## 見回り2(2050-01-21)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 624。WaitingSpace+Importing+InGrounds 503(前回 503)、WaitingSpace+Importing+OnRoad 58、Importing+Spawned+OnRoad+Blocked 50。bySeenStopped は 7days+ が 493。samples のうち vehicle 8, 36, 120 は seenStoppedDays 20.1(前回 10 から継続)
- `traffic`(x=3417, z=-1557, radius=60): flow 51、cars 11、blocked 0、congestion 1、averageDensity 15。区間20316 density 30
- `cargo`: 見回り2では呼んでいない(調査の道具に入っているが、結果は月末にまとめて記録する)

## 見回り1(2050-01-11)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 609。byState は WaitingSpace+Importing+InGrounds 503、WaitingSpace+Importing+OnRoad 61、Importing+Spawned+OnRoad+Blocked 32、GoingBack+Importing+Spawned+OnRoad+Blocked 8。byPath は ready 605、none 4。bySeenStopped は 7days+ が 469、<1day が 140。samples 5台は全部 WaitingSpace+Importing+InGrounds、位置 (3441,-1555)、Goods 3台と Coal 1台と Goods 1台、行き先までの距離 1,541〜6,296
- `traffic`(x=3417, z=-1557, radius=60): flow 51、cars 9、blocked 0、congestion 1、roadSegments 2、averageDensity 18。busiest は区間20316(Large Road、(3400,-1530))で density 36
- `cargo`: stoppedTrucks 793、stoppedOnRoads 273、stoppedInBuildings 520。貨物駅28755は 503台。vehiclesLeaving 792、vehiclesArriving 11。stoppedSpots 先頭は (3439,-1551) の 63台
