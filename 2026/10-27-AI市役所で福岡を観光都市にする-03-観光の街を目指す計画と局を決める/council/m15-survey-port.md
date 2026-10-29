# m15 調査 s15-1 貨物センター28755の空き待ちの追跡(port)

## 2051-03-07(施策後・進める前の初回の計測)

- `vehicles_stuck`(truck、building 28755、limit 30): vehicles 766。WaitingSpace+Importing+InGrounds 632、WaitingSpace+Importing+OnRoad 88、OnRoad+Blocked 35+7。seenStopped 7日以上 453
- `cargo`: stoppedTrucks 964、stoppedInBuildings 653(28755が632)、stoppedOnRoads 311。品物がない店 265、原料がない工場 49

## 2051-03-17(見回り1)

- `vehicles_stuck`(同じ引数): vehicles 802。WaitingSpace+Importing+InGrounds 684、WaitingSpace+Importing+OnRoad 89、Blocked 29。seenStopped 7日以上 657
- `cargo`: stoppedTrucks 1,009、stoppedInBuildings 708(28755が684)、stoppedOnRoads 301。品物がない店 259、原料がない工場 46

## 2051-04-06(月末)

- `vehicles_stuck`(同じ引数): vehicles 824。WaitingSpace+Importing+InGrounds 659、WaitingSpace+Importing+OnRoad 98、Blocked 66。seenStopped 7日以上 701
- `cargo`: stoppedTrucks 1,049、stoppedInBuildings 671(28755が659)、stoppedOnRoads 378。品物がない店 266、原料がない工場 39

## 2051-03-27(見回り2)

- `vehicles_stuck`(同じ引数): vehicles 830。WaitingSpace+Importing+InGrounds 684(+1)、WaitingSpace+Importing+OnRoad 95、Blocked 50。seenStopped 7日以上 690
- `cargo`: stoppedTrucks 1,090、stoppedInBuildings 693(28755が685)、stoppedOnRoads 397。品物がない店 260、原料がない工場 43
