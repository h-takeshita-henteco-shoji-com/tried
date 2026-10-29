# m09 調査 s09-2 貨物駅28755の敷地内のトラック(port)

問い: 敷地内で「空き待ち」になっているトラック464台は、時間がたつと減るか、増えるか、同じか。見立ては書かない。

## 2050-08-30(月例の実行直後。基準)

- `vehicles_stuck`(truck, building=28755): 564台。WaitingSpace+Importing+InGrounds 464、WaitingSpace+Importing+OnRoad 55、Blocked の道の上 44。7日以上止まっている 319
- `cargo`: stoppedInBuildings 465(28755 が 464)、stoppedTrucks 778、stoppedOnRoads 313。28755 の vehiclesLeaving 710、vehiclesArriving 11
- `traffic`(3441,-1555 r60): flow 52、blocked 0、cars 8、density 31(Large Road 20316)

## 2050-09-09(見回り1)

- `vehicles_stuck`(truck, building=28755): 551台。WaitingSpace+Importing+InGrounds 452、WaitingSpace+Importing+OnRoad 55、Blocked の道の上 42。7日以上止まっている 439。vehicle 2 は 40.1日、vehicle 45 は 80日止まったまま(位置 3441,-1555)
- `cargo`: stoppedInBuildings 452(28755 が 452)、stoppedTrucks 780、stoppedOnRoads 328。28755 の vehiclesLeaving 684、vehiclesArriving 10
- `traffic`(3441,-1555 r60): flow 51、blocked 0、cars 8、density 31

## 2050-09-19(見回り2)

- `vehicles_stuck`(truck, building=28755): 534台。WaitingSpace+Importing+InGrounds 447、WaitingSpace+Importing+OnRoad 57、Blocked の道の上 25。7日以上止まっている 427。vehicle 2 は 50.1日、vehicle 20 は 50.1日止まったまま
- `cargo`: stoppedInBuildings 457(28755 が 447、Cargo Harbor 1366 が 6、46112 が 4)、stoppedTrucks 700、stoppedOnRoads 243。28755 の vehiclesLeaving 668、vehiclesArriving 11
- `traffic`(3441,-1555 r60): flow 53、blocked 0、cars 9、density 47

## 2050-09-29(月末)

- `vehicles_stuck`(truck, building=28755): 546台。WaitingSpace+Importing+InGrounds 463、WaitingSpace+Importing+OnRoad 46、Blocked の道の上 33。7日以上止まっている 430。sample の 147 と 151 は 30日止まったまま(位置 3441,-1555)
- `cargo`: stoppedInBuildings 463(すべて 28755)、stoppedTrucks 766、stoppedOnRoads 303。28755 の vehiclesLeaving 662、vehiclesArriving 11
- `traffic`(3441,-1555 r60): flow 53、blocked 0、cars 10、density 50
- 3回の測定(28755 の敷地内): 464(8/30)→452(9/9)→447(9/19)→463(9/29)
