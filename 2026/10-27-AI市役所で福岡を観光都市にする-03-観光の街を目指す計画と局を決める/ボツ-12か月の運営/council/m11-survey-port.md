# m11 調査 port

## s11-2 貨物センター28755の空き待ちと 13893 の接続

### 見回り2(2050-11-18)

- `vehicles_stuck` kind=truck building=28755 limit=30: vehicles 515。byState は WaitingSpace+Importing+InGrounds 426、WaitingSpace+Importing+OnRoad 49、Importing+Spawned+OnRoad+Blocked 27、GoingBack+Importing+Spawned+OnRoad+Blocked 10、Congestion+Importing+Spawned+OnRoad 2、Importing+Spawned+InGrounds 1。byPath は ready 514、none 1。bySeenStopped は <1day 178、7days+ 337。samples の待ち位置は (3441,-1555)。積荷は Goods、Lumber、Food、Coal、Petrol
- `buildings_near` x=3529, z=-1555, radius=15: 13893 Cargo Center、problems "Garbage"、electricity/water/sewage すべて true、jobs total 0・workers 49、vehicles inUse 0
- `cargo`: stoppedTrucks 680、stoppedOnRoads 254、stoppedInBuildings 426(すべて 28755)。28755 の vehiclesLeaving 665、vehiclesArriving 13。13893 の vehiclesLeaving 0、vehiclesArriving 0。ほかの Cargo Center(3940、4740、14580、16572、40031、48243)も 0/0
