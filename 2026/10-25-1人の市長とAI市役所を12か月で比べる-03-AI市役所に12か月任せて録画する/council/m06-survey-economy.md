# m06 調査 s06-2 の結果(economy)

問い: 原料がない工場の印は、貨物駅28755 の中で止まった原料の車(石炭・木材・石油)の行き先と重なるか。
見る道具: `vehicles_stuck(kind="truck", building=28755, limit=30)`、`cargo()`。見立ては書かない。
28755 の位置は (3449,-1555)。

## 見回り1(2050-06-10)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 611。byState は WaitingSpace+Importing+InGrounds 474、WaitingSpace+Importing+OnRoad 96、Importing+Spawned+OnRoad+Blocked 30、GoingBack+Importing+Spawned+OnRoad+Blocked 9、Congestion+…+Blocked 1、WaitingTarget+…+InGrounds 1
- byPath は ready 609、none 2。bySeenStopped は <1day 164、7days+ 447
- byTarget の上位は行き先0(なし)10台。ほかは店と工場で各2〜3台。工場は 36132 Bigfactory06 (2606,1476) 2台、27955 Bigfactory06 (2584,1169) 2台
- samples 30台はすべて (3441,-1555)、WaitingSpace+Importing+InGrounds、blockCounter 0、waitCounter 0
- samples のうち原料など(Goods 以外)の車 15台の行き先と、28755 からの距離(m)
  - Lumber: 3722 Bigfactory06 1,348 / 18084 Mediumfactory08 1,471 / 7029 Bigfactory06 5,657 / 25139 Bigfactory06 545 / 28136 Mediumfactory08 2,868 / 32707 Mediumfactory08 1,289
  - Petrol: 47265 sweatshop01 873 / 32407 Mediumfactory08 1,419 / 44174 L3 1x1 Shop07 932 / 2912 Sweatshop07 915 / 11796 Facility05 706
  - Coal: 37721 Bigfactory06 3,223
  - Food: 12056 Mediumfactory07 389 / 39531 Mediumfactory08 303 / 15404 Mediumfactory08 793
- samples の止まって見えた日数は 0〜160日

### `cargo()`

- noResources 31棟。spots は (2670,-1041) 19棟、(2328,1279) 8棟、(-2374,-731) 3棟
- noGoods 110棟。spots は (-971,-834) 28棟、(2262,666) 26棟、(1076,275) 20棟
- byCargo の stoppedTrucks は Coal 71、Lumber 94、Petrol 99、Food 48、Goods 614。import は Coal 142、Lumber 191、Petrol 176、Food 227
- stoppedInBuildings 491(28755 が474、港1366 が17)
- 参考: (2670,-1041) は 28755 から約930m

## 見回り2(2050-06-20)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 617。byState は WaitingSpace+Importing+InGrounds 489、WaitingSpace+Importing+OnRoad 88、Importing+Spawned+OnRoad+Blocked 32、GoingBack+…+OnRoad+Blocked 5、Importing+Spawned+InGrounds 2、GoingBack+…+InGrounds 1
- byPath は ready 614、none 3。bySeenStopped は <1day 125、7days+ 492
- byTarget の上位は行き先0(なし)6台。工場は 17603 Bigfactory06 (2888,-1126) 2台。ほかは店
- samples 30台はすべて (3441,-1555)、blockCounter 0、waitCounter 0(OnRoad の3台を含む)
- samples のうち原料など(Goods 以外)の車 16台の行き先と、28755 からの距離(m)
  - Lumber: 29136 Bigfactory06 1,283 / 3722 Bigfactory06 1,348 / 18084 Mediumfactory08 1,471 / 7029 Bigfactory06 5,657 / 25139 Bigfactory06 545 / 32707 Mediumfactory08 1,289 / 40623 Bigfactory06 1,379(170日) / 14183 Bigfactory06 859 / 27180 Bigfactory 04 391
  - Petrol: 47265 sweatshop01 873 / 32407 Mediumfactory08 1,419 / 2912 Sweatshop07 915(160日) / 541 Facility06 1,280 / 11796 Facility05 706 / 27987 Mediumfactory08 847
  - Coal: 11915 Mediumfactory07 275(150日)
- 見回り1の samples と同じ車(113、149、215、219、237、464、496、561、95)は、同じ行き先のまま止まって見える日数が10日増えた

### `cargo()`

- noResources 32棟。spots は (2678,-1076) 19棟、(2328,1279) 8棟、(-2374,-731) 3棟
- noGoods 114棟。spots は (-922,-712) 31棟、(2224,639) 26棟、(964,275) 21棟
- byCargo の stoppedTrucks は Coal 69、Lumber 92、Petrol 98、Food 49、Goods 607
- stoppedInBuildings 492(28755 が489、港1366 が3)
- stoppedSpots に (2761,-1094) 22台、(2232,-1098) 21台

## 月末(2050-06-30)

### `vehicles_stuck(kind="truck", building=28755, limit=30)`

- vehicles 598。byState は WaitingSpace+Importing+InGrounds 483、WaitingSpace+Importing+OnRoad 81、Importing+Spawned+OnRoad+Blocked 26、GoingBack+…+OnRoad+Blocked 4、Importing+Spawned+InGrounds 2、WaitingPath+…+OnRoad 2
- byPath は ready 596、none 2。bySeenStopped は <1day 109、7days+ 489
- byTarget の上位は行き先0(なし)4台。工場は 12176 Mediumfactory08 (3843,-644) 2台、27955 Bigfactory06 (2584,1169) 2台。ほかは店
- samples 30台はすべて (3441,-1555)、blockCounter 0、waitCounter 0
- samples のうち原料など(Goods 以外)の車 19台の行き先と、28755 からの距離(m)
  - Lumber: 29136 Bigfactory06 1,283 / 3722 Bigfactory06 1,348 / 18084 Mediumfactory08 1,471 / 7029 Bigfactory06 5,657 / 25139 Bigfactory06 545 / 36151 Bigfactory06 1,308 / 32707 Mediumfactory08 1,289 / 40623 Bigfactory06 1,379(180日)
  - Petrol: 47265 sweatshop01 873 / 32407 Mediumfactory08 1,419(100日) / 44387 Facility06 453 / 2912 Sweatshop07 915(170日) / 541 Facility06 1,280 / 11796 Facility05 706
  - Coal: 3446 Bigfactory06 244
  - Food: 21824 Bigfactory06 3,235 / 21589 Mediumfactory08 1,307 / 48960 Bigfactory06 5,850 / 1801 Mediumfactory06 306
- 見回り1・2から続けて samples に出た原料の車(95、113、149、215、219、237、464、496、561、670 ほか)は、行き先が変わらず、止まって見える日数がさらに10日増えた

### `cargo()`

- noResources 38棟。spots は (2834,-1005) 22棟、(2362,1288) 9棟、(-2347,-578) 5棟
- noGoods 116棟。spots は (-915,-728) 33棟、(2230,649) 28棟、(1144,281) 19棟
- byCargo の stoppedTrucks は Coal 69、Lumber 97、Petrol 96、Food 49、Goods 590
- stoppedInBuildings 492(28755 が483、港1366 が9)

### 3回の並び(参考。基準 2050-05-31 は議案の値)

| 日付 | noResources | noGoods | 28755 の中で止まった車 | 原料(Coal+Lumber+Petrol)の止まった車 |
|---|---|---|---|---|
| 05-31 | 43 | 178 | 514 | 260 |
| 06-10 | 31 | 110 | 474 | 264 |
| 06-20 | 32 | 114 | 489 | 259 |
| 06-30 | 38 | 116 | 483 | 262 |
