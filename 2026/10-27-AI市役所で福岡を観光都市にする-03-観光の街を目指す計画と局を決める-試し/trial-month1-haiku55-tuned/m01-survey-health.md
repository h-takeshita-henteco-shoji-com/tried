# m01 調査 s01-3(health)霊柩車の詰まりは交通の詰まりと一緒に減るか

## 2050-01-31(月末)

- `vehicles_stuck`(kind="hearse", limit=5): 183 台。7日以上止まって見えるのが 68 台。Congestion の印付きが大半、path none 16
- `complaints`: Death 63(hotspot 2183.6,118.6 に 21)、Pollution 42、NoGoods 226、Garbage 15、Noise 7、Crime 2、Flood 1、LandValueLow 1、Water 1
- `traffic`(x=2150, z=300, radius=400, limit=5): flow 52、cars 450、blocked 180、congestion 227、averageDensity 50。blockedSpot (2098,309) に 44、(2158,479) に 35、(1876,120) に 25

## 2050-01-21(見回り2)

- `vehicles_stuck`(kind="hearse", limit=5): 174 台。7日以上止まって見えるのが 68 台(見回り1は全部 1日未満)。Congestion の印付きが大半、path none 13
- `complaints`: Death 59(hotspot 2227.9,-0.9 に 23)、Pollution 39、NoGoods 233、Garbage 10、Noise 8、Crime 4、Flood 2、Water 1
- `traffic`(x=2150, z=300, radius=400, limit=5): flow 51、cars 433、blocked 182、congestion 230、averageDensity 49。blockedSpot (2113,295) に 43、(2155,485) に 40、(2273,318) に 25

## 2050-01-11(見回り1)

- `vehicles_stuck`(kind="hearse", limit=5): 176 台。Congestion の印が付くのが大半(Congestion+OnRoad+Blocked 57、Congestion+OnRoad 39、Blocked のみ 38)。path none 13、ready 163
- `complaints`: Death 55(hotspot 2219.8,127 に 29)、Pollution 36、NoGoods 235、Garbage 12、Noise 8、Crime 3
- `traffic`(x=2150, z=300, radius=400, limit=5): flow 49、cars 432、blocked 115、congestion 233、averageDensity 50。blockedSpot (2105,287) に 35、(2153,462) に 33、(2306,328) に 17
