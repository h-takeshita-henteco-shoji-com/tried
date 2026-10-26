# m02 調査 s02-2(roads): 交通の詰まりが同じ場所に居続けるか

問い: 流れ50%を下げる詰まりのうち、(1689, 91) の東西の道と、貨物駅西の (2131, -872) は、日がたつと同じ場所に居続けるか。

## 見回り1(2050-02-10)

### `traffic`(x=1689, z=91, radius=200, limit=10)

- flow 51、cars 239、blocked 158(道路 158、建物 0)、congestion 111、roadSegments 17、averageDensity 82
- busiest(density 100 の10区間): 15881 Medium (1597,-79)、12970 Large (1850,107)、12875 Basic (1560,70)、25620 Medium (1572,-20)、34060 Medium (1543,100)、30867 Basic (1560,36)、29499 Basic (1523,10)、6010 Large (1800,103)、3239 Medium (1589,100)、109 Medium (1652,100)
- blockedSpots: (1695,95) 111、(1831,101) 24、(1565,66) 12、(1574,-43) 11

### `traffic`(x=2131, z=-872, radius=250, limit=10)

- flow 51、cars 251、blocked 10(道路 10)、congestion 56、roadSegments 39、averageDensity 66
- busiest(density 100 の10区間): 20169 Medium (2160,-914)、20293 Basic (2236,-886)、20648 Basic (2110,-776)、14040 Basic (2272,-860)、17090 Basic (2110,-816)、19196 Basic (2194,-950)、30068 Small 4 Lane (2313,-950)、36011 Basic (2228,-950)、36773 Basic (2227,-1058)、22902 Basic (2234,-1088)
- blockedSpots: (2118,-839) 8、(2222,-741) 1、(2108,-765) 1

### `junction_info`(x=1692, z=100)

- 失敗: "no road junction within 40m"
