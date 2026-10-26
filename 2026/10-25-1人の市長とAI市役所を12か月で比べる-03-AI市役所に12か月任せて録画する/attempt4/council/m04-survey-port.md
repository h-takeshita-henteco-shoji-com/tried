# m04 調査の結果(port)

## s04-2 28755 の止まった車の先頭は、列車の荷が増え続けるせいで動かないのか

注: 施策 m04-2 で、28755 を 2050-04-01 から 2050-04-11 まで止めた。見回り1の数は止めている間の値(測った直後に動かし直した)。

### 見回り1(2050-04-11)

- `vehicles_stuck(kind="train", limit=20)`
  - vehicles 2。どちらも WaitingCargo+Stopped+Importing+InGrounds、path none、bySeenStopped 7days+ 2
  - 2台とも行き先 28755。位置 (7277,-8616) と (6997,-8618)(つなぎ口 34128、32589)。cargoLoads 1 と 2、seenStoppedDays 10
- `cargo()`
  - cargoTrains 13 → 2(実行前 → 見回り1)
  - stoppedInBuildings 243(28755 が231、港1366 が12)、stoppedOnRoads 356
  - 28755 の vehiclesLeaving 493、vehiclesArriving 2
  - stoppedSpots の最多 (3435,-1538) 61
  - Goods の止まり403、品物がない店165、原料がない工場33
- (参考。施策 m04-2 の確かめで呼んだ)`vehicles_stuck(kind="truck", building=28755, limit=60)`: vehicles 374。WaitingSpace+Importing+InGrounds 231、WaitingSpace+Importing+OnRoad 50、Importing+OnRoad+Blocked 68、GoingBack+OnRoad+Blocked 25。byPath ready 374。bySeenStopped <1day 61、7days+ 313。(3441,-1555) の車に seenStoppedDays 100 が多い

### 見回り2(2050-04-21。28755 は 04-11 に動かし直した後)

- `vehicles_stuck(kind="train", limit=20)`
  - vehicles 7。Importing+Spawned+OnRoad 5(path ready、cars 10、cargoLoads 15)、WaitingCargo+Stopped+Importing+InGrounds 2(path none、cars 1、cargoLoads 6 と 2、waitCounter 19 と 21)
  - 7台とも行き先 28755。bySeenStopped <1day 5、7days+ 2
- `cargo()`
  - cargoTrains 7
  - stoppedInBuildings 199(28755 が182、港1366 が17)、stoppedOnRoads 292
  - 28755 の vehiclesLeaving 405、vehiclesArriving 7
  - stoppedSpots の最多 (3436,-1540) 54
  - Goods の止まり331、品物がない店170、原料がない工場30
- (参考。施策 m04-2 の確かめで呼んだ)`vehicles_stuck(kind="truck", building=28755, limit=60)`: vehicles 275。WaitingSpace+Importing+InGrounds 182、WaitingSpace+Importing+OnRoad 47、Importing+OnRoad+Blocked 30、GoingBack+OnRoad+Blocked 15。byPath ready 274、none 1。bySeenStopped <1day 19、7days+ 256。前回 (3441,-1555) にいた車8・229・1030・1180 など(seenStoppedDays 90〜110)は (3384〜3405, -1336〜-1466) の道の上で Blocked に変わった

### 月末(2050-05-01)

- `vehicles_stuck(kind="train", limit=20)`
  - vehicles 12。Importing+Spawned+OnRoad 8、Importing+Spawned+InGrounds 1(12380、(3475,-1488)、行き先まで72m、cargoLoads 0)、Stopped+Importing+Spawned+OnRoad 1、WaitingCargo+Stopped+Importing+InGrounds 2(path none、cars 1、cargoLoads 1 と 5)
  - 12台とも行き先 28755。bySeenStopped <1day 10、7days+ 2
  - 走っている列車は cars 10、cargoLoads 15
- `cargo()`
  - cargoTrains 12
  - stoppedInBuildings 249(28755 が215、港1366 が22、港46112 が12)、stoppedOnRoads 263
  - 28755 の vehiclesLeaving 391、vehiclesArriving 12
  - stoppedSpots の最多 (3433,-1541) 53
  - Goods の止まり312、品物がない店180、原料がない工場28
- (参考。施策 m04-2 の確かめで呼んだ)`vehicles_stuck(kind="truck", building=28755, limit=60)`: vehicles 292。WaitingSpace+Importing+InGrounds 215、WaitingSpace+Importing+OnRoad 39、Importing+OnRoad+Blocked 29、GoingBack+OnRoad+Blocked 9。byPath ready 292。bySeenStopped <1day 76、7days+ 216。(3441,-1555) に seenStoppedDays 120 の車(664、1717、2396 など)が残り、seenStoppedDays 0 の新しい車(Food・Coal・Petrol)も WaitingSpace に入っている
