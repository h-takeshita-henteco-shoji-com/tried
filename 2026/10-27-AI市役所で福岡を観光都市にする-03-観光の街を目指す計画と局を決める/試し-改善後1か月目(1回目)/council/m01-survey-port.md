# m01 調査 s01-1(port) 貨物駅の枠待ちを見る

問い: 貨物駅 28755 の敷地の中で枠待ちのトラックは、見回りのたびに減るか。隣の貨物駅 13893 は使われるか

## 見回り1 (2050-01-12)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 632。byState は WaitingSpace+Importing+InGrounds 519、WaitingSpace+Importing+OnRoad 61、Importing+Spawned+OnRoad+Blocked 32、GoingBack+Importing+Spawned+OnRoad+Blocked 16、ほか5。bySeenStopped は <1day 159、7days+ 473。サンプル5台のうち4台は敷地内 (3441,-1555) の WaitingSpace。積荷は Goods と Coal
- `vehicles_stuck`(kind="truck", building=13893, limit=5): vehicles 0(byState 空)

## 月末 (2050-02-01)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 589。byState は WaitingSpace+Importing+InGrounds 491、WaitingSpace+Importing+OnRoad 53、Importing+Spawned+OnRoad+Blocked 30、GoingBack+Importing+Spawned+OnRoad+Blocked 14、GoingBack InGrounds 1。bySeenStopped は <1day 113、7days+ 476。vehicle 8、36、120 は同じ位置で seenStoppedDays 31.1
- `vehicles_stuck`(kind="truck", building=13893, limit=5): vehicles 0

## 見回り2 (2050-01-22)

- `vehicles_stuck`(kind="truck", building=28755, limit=5): vehicles 605。byState は WaitingSpace+Importing+InGrounds 498、WaitingSpace+Importing+OnRoad 56、Importing+Spawned+OnRoad+Blocked 37、GoingBack+Importing+Spawned+OnRoad+Blocked 13、GoingBack InGrounds 1。bySeenStopped は <1day 117、7days+ 488。サンプルの vehicle 8、36、120 は同じ位置 (3441,-1555) で seenStoppedDays 21(見回り1の11日から継続)
- `vehicles_stuck`(kind="truck", building=13893, limit=5): vehicles 0
