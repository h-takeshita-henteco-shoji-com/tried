# s04-2 貨物駅28755 の敷地の線の端が道路につながっているか(port)

問い: 貨物駅28755 の敷地の西の線(3417,-1555 と 3417,-1560)と東の線(3477,-1555 と 3477,-1560)は、道路につながっているか

## 見回り1(2050-04-11)

- `net_near(x=3417, z=-1557, radius=30)`: total 4。Cargo Connection 25546(node 27256 3469,-1555 → node 5129 3417,-1555)、Cargo Connection 30062(node 20745 3417,-1560 → node 27809 3469,-1560)。道路は Large Road 20316(node 27757 3400,-1567 → node 20609 3400,-1493)と Large Road 30945(node 11790 3400,-1625 → node 27757 3400,-1567)。西の端の node 5129・20745 を持つ道路の区間は、この円の中に出なかった
- `net_near(x=3477, z=-1557, radius=30)`: total 10。Cargo Connection 11402(node 18552 3477,-1555 → node 27256 3469,-1555)、22871(node 27809 3469,-1560 → node 17426 3477,-1560)、25137(node 4316 3497,-1560 → node 11449 3549,-1560)、26146(node 13128 3549,-1555 → node 16839 3497,-1555)、25546、30062。道路は Small 4 Lane Road 15733(node 8479 3495,-1490 → node 21285 3495,-1565)と 22686(node 21285 → node 15388 3496,-1610)。ほかに Water Pipe 1143、Train Cargo Track 9082(3473,-1643 → 3473,-1467)。東の端の node 18552・17426 を持つ道路の区間は、この円の中に出なかった
- `vehicles_stuck(kind="truck", building=28755, limit=5)`: vehicles 664。byState: WaitingSpace+Importing+InGrounds 579、WaitingSpace+Importing+OnRoad 55、Importing+Spawned+OnRoad+Blocked 17、GoingBack+Importing+Spawned+OnRoad+Blocked 9、GoingBack+Importing+Spawned+InGrounds 3、Congestion+Importing+Spawned+OnRoad+Blocked 1。byPath ready 661・none 3。bySeenStopped <1day 125・7days+ 539。samples 5台は全部 3441,-1555、blockCounter 0・waitCounter 0(seenStoppedDays 100、10、0、0、19.9。荷は Goods 3台・Petrol 2台)

## 月末(2050-05-01)

- `net_near(x=3417, z=-1557, radius=30)`: 見回り1と同じ4区間(Cargo Connection 25546・30062、Large Road 20316・30945)。西の端の node 5129・20745 を持つ道路の区間は出なかった
- `net_near(x=3477, z=-1557, radius=30)`: 見回り1と同じ10区間。東の端の node 18552・17426 を持つ道路の区間は出なかった
- `vehicles_stuck(kind="truck", building=28755, limit=5)`: vehicles 643。byState: WaitingSpace+Importing+InGrounds 553、WaitingSpace+Importing+OnRoad 55、Importing+Spawned+OnRoad+Blocked 20、GoingBack+Importing+Spawned+OnRoad+Blocked 14、GoingBack+Importing+Spawned+InGrounds 1。byPath ready 642・none 1。bySeenStopped <1day 205・7days+ 438。samples 5台は全部 3441,-1555、blockCounter 0・waitCounter 0(seenStoppedDays 120、0、30、20、0。荷は全部 Goods)
