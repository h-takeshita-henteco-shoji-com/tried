# m17 調査 s17-1(port) 貨物センター 28755 の空き待ちの車

## 2051-05-16(見回り1)

- `vehicles_stuck`(kind truck、building 28755、limit 5): 車 724。WaitingSpace+Importing+InGrounds 587、WaitingSpace+Importing+OnRoad 98、Importing+OnRoad+Blocked 20、GoingBack+OnRoad+Blocked 15。bySeenStopped は「7日以上」591、「1日未満」133。代表の車 15 は 130 日止まり
- `cargo`: stoppedTrucks 927、stoppedInBuildings 603(28755 が 587)、stoppedOnRoads 324。stoppedSpots 先頭は (3441,-1555) の 98 台。Goods の stopped 589

## 2051-06-05(月末)

- `vehicles_stuck`(同じ引数): 車 719。WaitingSpace+Importing+InGrounds 588、WaitingSpace+Importing+OnRoad 94、Importing+OnRoad+Blocked 24、GoingBack+OnRoad+Blocked 11。bySeenStopped は「7日以上」489、「1日未満」230。車 15 は 150 日止まり、車 10 は 30 日、車 106 は 60 日
- `cargo`: stoppedTrucks 953、stoppedInBuildings 589(28755 が 588)、stoppedOnRoads 364。stoppedSpots 先頭は (3440,-1552) の 96 台。Goods の stopped 620

(見立ては書かない。局が翌月に読む)
