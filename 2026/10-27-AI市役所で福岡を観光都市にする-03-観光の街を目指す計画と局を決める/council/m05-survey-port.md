# m05 調査 s05-1(port): 貨物センター13893 への行き先

問い: 28755 の WaitingSpace のトラックは、13893 へ行き先が付くと減るか。13893 にトラックが来るか。

## 2050-05-11(見回り1)

- `cargo`: stations 28755 は vehiclesLeaving 793、vehiclesArriving 10。13893 は leaving 0、arriving 0。stoppedInBuildings 535(28755 が 525)、stoppedTrucks 764
- `vehicles_stuck`(truck, building=28755, limit=10): vehicles 612。WaitingSpace+Importing+InGrounds 524、WaitingSpace+Importing+OnRoad 41、Blocked(道の上)42。bySeenStopped は 7days+ が 494、<1day が 118。サンプルは Goods/Coal/Lumber/Petrol の輸入で、目標の距離 555〜6296

## 2050-05-21(見回り2)

- `cargo`: 28755 は leaving 772、arriving 12。13893 は 0/0。stoppedInBuildings 516(28755 が 504)、stoppedTrucks 778
- `vehicles_stuck`: vehicles 588。WaitingSpace+Importing+InGrounds 504、OnRoad 49。7days+ が 460、<1day が 128

## 2050-05-31(月末)

- `cargo`: 28755 は leaving 778、arriving 13。13893 は 0/0。stoppedInBuildings 520(28755 が 500)、stoppedTrucks 843
- `vehicles_stuck`: vehicles 603。WaitingSpace+Importing+InGrounds 500、OnRoad 51、Blocked 48。7days+ が 467、<1day が 136。path none が 4
