# m03 調査 s03-1 貨物駅28755の敷地で待つトラックの原因

## 見回り1(2050-03-13)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 609。WaitingSpace+Importing+InGrounds 508、WaitingSpace+Importing+OnRoad 48、OnRoad+Blocked 51。bySeenStopped は 7days+ が467、<1day が142。byPath は ready 607、none 2。見本の1台(vehicle 216、Petrol)は敷地内(3441,-1555)で 40.9日 WaitingSpace
- `traffic`(x=3441, z=-1555, radius=40, limit=5): flow 52、cars 8、blocked 0、congestion 1、roadSegments 0、blockedSpots なし
- 参考 `cargo`: stoppedInBuildings 522(28755が508)、stations の 28755 は vehiclesLeaving 755、vehiclesArriving 11

## 見回り2(2050-03-23)(調査は見回り1と月末のみ。参考)

- `cargo`: stoppedInBuildings 496(28755が496)、28755 は vehiclesLeaving 756、vehiclesArriving 11

## 月末(2050-04-02)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 623。WaitingSpace+Importing+InGrounds 517、WaitingSpace+Importing+OnRoad 50、OnRoad+Blocked 52。bySeenStopped は 7days+ が481、<1day が142。byPath は ready 619、none 4
- `traffic`(x=3441, z=-1555, radius=40, limit=5): flow 53、cars 7、blocked 0、congestion 1、roadSegments 0、blockedSpots なし
- 参考 `cargo`: stoppedInBuildings 518(28755が517)、28755 は vehiclesLeaving 774、vehiclesArriving 12
