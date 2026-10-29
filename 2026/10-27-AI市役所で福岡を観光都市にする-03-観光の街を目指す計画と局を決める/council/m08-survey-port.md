# m08 調査 port

## s08-1 貨物センター28755の止まったトラックの出どころ

### 2050-08-09(見回り1)

- 道具: `vehicles_stuck`(kind=truck, building=28755, limit=10)
- 返った数: vehicles 632。byState は WaitingSpace+Importing+InGrounds 506、WaitingSpace+Importing+OnRoad 70、Importing+Spawned+OnRoad+Blocked 44、GoingBack+Importing+Spawned+OnRoad+Blocked 10、ほか2。bySeenStopped は <1day 132、7days+ 500
- samples 10台は全部 source が Cargo Center 28755、Importing。位置は (3441,-1555) が多い。積み荷は Goods 8000(店への配送、行き先の店までの距離 1829〜5604)、Coal 8000(工場 3805 へ 981)、Lumber 8000(工場 34890 へ 2776)。seenStoppedDays は 0〜140
- byTarget 上位は店(Shop03、Shop05a、Shop04 など)が各3台
