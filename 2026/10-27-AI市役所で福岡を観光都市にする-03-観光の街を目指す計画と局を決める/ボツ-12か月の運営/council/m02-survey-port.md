# m02 調査 s02-1(port)貨物駅28755の出口

## 2050-02-11 見回り1

- `vehicles_stuck`(kind="truck", building=28755, limit=3): vehicles 609。byState は WaitingSpace+Importing+InGrounds 507、WaitingSpace+Importing+OnRoad 56、Importing+Blocked(道の上)23、GoingBack+Importing+Blocked 22、InGrounds 1。bySeenStopped は 7日以上 463、1日未満 146。byPath は ready 608、none 1。サンプル: 車210(Goods、amount 0、道の上 Blocked、(2086,-1052))、車216(Petrol 8000、WaitingSpace InGrounds、(3441,-1555)、止まって10.9日、行き先 26254 まで1165m)、車229(Goods 8000、WaitingSpace InGrounds、(3441,-1555)、20.9日、行き先 32257 まで5253m)
- `vehicles_stuck`(kind="truck", building=13893, limit=3): vehicles 0。byState 空。
- `traffic`(x=3400, z=-1555, radius=60, limit=5): flow 54、cars 7、blocked 0、congestion 1、averageDensity 16。busiest は segment 20316(Large Road、(3400,-1530))density 32。blockedSpots なし。

## 2050-02-21 見回り2

- `vehicles_stuck`(kind="truck", building=28755, limit=3): vehicles 598。WaitingSpace+Importing+InGrounds 502、WaitingSpace+Importing+OnRoad 56、道の上 Blocked 36(GoingBack 21、Importing 15)。7日以上止まり 478、1日未満 120。byPath は ready 595、none 3。車216(Petrol)は止まって21日、車229(Goods)は31日、どちらも (3441,-1555)。
- `vehicles_stuck`(kind="truck", building=13893, limit=3): vehicles 0。
- `traffic`(x=3400, z=-1555, radius=60, limit=5): flow 52、cars 13、blocked 0、congestion 1。segment 20316(Large Road)density 52。blockedSpots なし。

## 2050-03-03 月末

- `vehicles_stuck`(kind="truck", building=28755, limit=3): vehicles 584。WaitingSpace+Importing+InGrounds 500、WaitingSpace+Importing+OnRoad 49、道の上 Blocked 34(GoingBack 14、Importing 20)。7日以上止まり 469、1日未満 115。byPath は ready 584。車216(Petrol)は止まって31日、(3441,-1555)。
- `vehicles_stuck`(kind="truck", building=13893, limit=3): vehicles 0。
- `traffic`(x=3400, z=-1555, radius=60, limit=5): flow 54、cars 7、blocked 0、congestion 1。segment 20316(Large Road)density 28。blockedSpots なし。
