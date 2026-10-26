# m01 調査 s01-2(roads): 交通の流れを下げる詰まりの場所

問い: 流れ51%を下げている詰まりは、貨物駅28755の周りと、(-726,-736) の大通りのどちらが主で、日がたつと動くか。

## 見回り1(2050-01-11)

### `traffic`(x=2309, z=-925, radius=300, limit=10)

- flow 51、cars 273、blocked 56(すべて道の上)、congestion 102、roadSegments 48、averageDensity 61
- busiest(すべて density 100): 15481 Small 4 Lane (2430,-950)、17090 Basic (2110,-816)、19196 Basic (2194,-950)、13096 Small 4 Lane (2370,-950)、14040 Basic (2272,-860)、14041 Small 4 Lane (2490,-950)、20293 Basic (2236,-886)、30068 Small 4 Lane (2313,-950)、36011 Basic (2228,-950)、36773 Basic (2227,-1058)
- blockedSpots: (2249,-896) 25、(2104,-881) 24、(2101,-750) 7

### `traffic`(x=-726, z=-736, radius=200, limit=10)

- flow 51、cars 186、blocked 18(すべて道の上)、congestion 35、roadSegments 8、averageDensity 96
- busiest: 10922 Large (-759,-740) 100、30435 Large (-611,-740) 100、36115 Large (-832,-740) 100、6545 Large (-685,-740) 100、3276 Large with Median (-895,-740) 100、16866 Small 4 Lane (-920,-712) 95、9066 Small 4 Lane (-920,-768) 88、32158 Large (-537,-740) 88
- blockedSpots: (-898,-736) 11、(-563,-747) 7

### `vehicles_stuck`(kind="truck", limit=30)

- vehicles 1,181
- byState 主なもの: WaitingSpace+Importing+InGrounds 528、Importing+InGrounds 305、Spawned+OnRoad+Blocked 101、Importing+Spawned+OnRoad+Blocked 72、WaitingSpace+Importing+OnRoad 64、GoingBack+Spawned+OnRoad+Blocked 50、GoingBack+Importing+Spawned+OnRoad+Blocked 40
- byPath: ready 1,168、none 13
- bySeenStopped: <1day 709、7days+ 472
- samples の道の上で Blocked の車の位置: (-1873,93)、(118,108)、(1726,-825)、(2057,64)、(1459,358)、(2168,-895)、(1594,-763)、(-1815,-1087)、(1991,-954)

## 見回り2(2050-01-21)

### `traffic`(x=2309, z=-925, radius=300, limit=10)

- flow 48、cars 274、blocked 60(すべて道の上)、congestion 89、roadSegments 48、averageDensity 58
- busiest(すべて density 100): 14040 Basic (2272,-860)、15481 Small 4 Lane (2430,-950)、13096 Small 4 Lane (2370,-950)、10391 Basic (2236,-924)、12301 Basic (2234,-1200)、19196 Basic (2194,-950)、20293 Basic (2236,-886)、22902 Basic (2234,-1088)、28251 Basic (2070,-840)、17090 Basic (2110,-816)
- blockedSpots: (2195,-737) 17、(2366,-941) 15、(2430,-946) 14、(2179,-837) 14

### `traffic`(x=-726, z=-736, radius=200, limit=10)

- flow 48、cars 173、blocked 135(すべて道の上)、congestion 35、roadSegments 8、averageDensity 96
- busiest: 10922 Large (-759,-740) 100、36115 Large (-832,-740) 100、9066 Small 4 Lane (-920,-768) 100、6545 Large (-685,-740) 100、16866 Small 4 Lane (-920,-712) 97、3276 Large with Median (-895,-740) 95、30435 Large (-611,-740) 90、32158 Large (-537,-740) 89
- blockedSpots: (-711,-735) 84、(-851,-741) 28、(-562,-736) 23

### `vehicles_stuck`(kind="truck", limit=30)

- vehicles 1,215
- byState 主なもの: WaitingSpace+Importing+InGrounds 517、Importing+InGrounds 312、Importing+Spawned+OnRoad+Blocked 132、Spawned+OnRoad+Blocked 108、WaitingSpace+Importing+OnRoad 63、GoingBack+Importing+Spawned+OnRoad+Blocked 37、GoingBack+Spawned+OnRoad+Blocked 35
- byPath: ready 1,202、none 13
- bySeenStopped: <1day 488、7days+ 727
- samples の道の上で Blocked の車の位置: (-2014,-1364)、(-1572,108)、(-1724,92)、(1954,64) blockCounter 80、(45,-717)、(-2200,-709)、(-1576,-1549)、(1653,-201) blockCounter 65、(-1816,-965)、(3927,-246)

## 月末(2050-01-31)

### `traffic`(x=2309, z=-925, radius=300, limit=10)

- flow 50、cars 326、blocked 77(すべて道の上)、congestion 69、roadSegments 48、averageDensity 60
- busiest(すべて density 100): 17090 Basic (2110,-816)、19196 Basic (2194,-950)、20293 Basic (2236,-886)、13096 Small 4 Lane (2370,-950)、14040 Basic (2272,-860)、14041 Small 4 Lane (2490,-950)、34194 Small 4 Lane (2550,-950)、36011 Basic (2228,-950)、36773 Basic (2227,-1058)、22902 Basic (2234,-1088)
- blockedSpots: (2131,-872) 44、(2177,-741) 29、(2229,-721) 4

### `traffic`(x=-726, z=-736, radius=200, limit=10)

- flow 50、cars 162、blocked 6(すべて道の上)、congestion 47、roadSegments 8、averageDensity 91
- busiest: 10922 Large (-759,-740) 100、36115 Large (-832,-740) 100、9066 Small 4 Lane (-920,-768) 100、3276 Large with Median (-895,-740) 100、6545 Large (-685,-740) 99、16866 Small 4 Lane (-920,-712) 93、32158 Large (-537,-740) 83、30435 Large (-611,-740) 58
- blockedSpots: (-916,-765) 6

### `vehicles_stuck`(kind="truck", limit=30)

- vehicles 1,212
- byState 主なもの: WaitingSpace+Importing+InGrounds 513、Importing+InGrounds 332、Spawned+OnRoad+Blocked 119、Importing+Spawned+OnRoad+Blocked 110、WaitingSpace+Importing+OnRoad 68、GoingBack+Spawned+OnRoad+Blocked 33、GoingBack+Importing+Spawned+OnRoad+Blocked 24
- byPath: ready 1,198、none 14
- bySeenStopped: <1day 504、7days+ 708
- samples の道の上で Blocked の車の位置: (2819,-949)、(1165,96)、(-1948,97) blockCounter 33、(2137,-1052)、(-2220,-589) blockCounter 28、(1467,11) blockCounter 32
