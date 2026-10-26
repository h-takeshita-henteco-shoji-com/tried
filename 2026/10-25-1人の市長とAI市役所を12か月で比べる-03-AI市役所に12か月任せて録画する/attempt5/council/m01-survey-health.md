# m01 調査 s01-2(health): 死体の印が(2240, 186)に集まる理由

実行する市長が、道具の返した数だけを書く。見立ては書かない。

## 見回り1(2050-01-11)

### `vehicles_stuck(kind="hearse", limit=30)`

- vehicles 187
- byState(主なもの): Congestion+Spawned+OnRoad+Blocked 52、Congestion+Spawned+OnRoad 41、Spawned+OnRoad+Blocked 41、Stopped+Spawned+OnRoad 18、Congestion+GoingBack+Spawned+OnRoad 5、Congestion+GoingBack+Spawned+OnRoad+Blocked 5、GoingBack+Spawned+OnRoad+Blocked 5、Spawned+InGrounds 4、WaitingTarget+Stopped+Spawned+InGrounds 4
- byPath: ready 173、none 14
- bySeenStopped: <1day 187
- byTarget: 行き先なし 25台、ほかは1台ずつ
- (2240,186)の近くのサンプル: 1040(火葬場17188→3969、(2112,-3)、Congestion+Blocked、blockCounter 14)、1795(火葬場23747→1748、(2204,-138)、Congestion+Blocked)、2271(火葬場29774→6558、(1884,86)、Congestion+Blocked、blockCounter 123)、1816(火葬場7547 から戻る途中、(2666,610)、Congestion+Blocked)

### `buildings_near(x=2240, z=186, radius=500, service="HealthCare", brief=false, limit=20)`

- total 6
- 火葬場23747(2222,-255): 保管 0 / 105、先週の処理 0、霊柩車 8 / 9
- 火葬場31990(2224,60): 保管 0 / 105、先週の処理 13、霊柩車 5 / 9
- 火葬場36841(2218,286): 保管 0 / 105、先週の処理 0、霊柩車 7 / 9
- 火葬場41597(2680,200): 保管 0 / 105、先週の処理 20、霊柩車 8 / 9
- 診療所12648(2676,125): 患者 20 / 100、救急車 10 / 10
- 診療所21521(1918,262): 患者 24 / 100、救急車 10 / 10

### `traffic(x=2240, z=186, radius=500)`

- flow 50、cars 591、blocked 224、congestion 307、roadSegments 164、averageDensity 37
- busiest(density 100): 6523 (2152,443)、29165 (1797,330)、7468 (2668,370)、6010 (1800,103)、4414 (1770,290)、30427 (2336,560)、5473 (2190,560)、7469 (2152,522)、22169 (1880,82)、20592 (2110,34)
- blockedSpots: (2264,294) 40、(2096,311) 39、(2153,462) 33、(1889,327) 21、(1942,66) 20、(2518,334) 18、(2648,352) 15、(2024,64) 10、(1902,-30) 9、(1754,93) 9

## 見回り2(2050-01-21)

### `vehicles_stuck(kind="hearse", limit=30)`

- vehicles 171
- byState(主なもの): Congestion+Spawned+OnRoad 48、Congestion+Spawned+OnRoad+Blocked 44、Spawned+OnRoad+Blocked 31、Stopped+Spawned+OnRoad 15、Congestion+Stopped+Spawned+OnRoad 9、Congestion+GoingBack+Spawned+OnRoad+Blocked 5
- byPath: ready 163、none 8
- bySeenStopped: <1day 112、7days+ 59
- byTarget: 行き先なし 21台、ほかは1台ずつ
- (2240,186)の近くのサンプル: 20(火葬場31990→2513、(2205,265)、Congestion)、1040(火葬場17188→3969、(2114,192)、Congestion+Blocked、blockCounter 19、seenStoppedDays 10)、1795(火葬場23747→20216、(2112,-123)、Congestion)、2271(火葬場29774→37572、(2044,-121)、Congestion)、1816(火葬場7547 へ戻る途中、(2682,326)、Congestion+Blocked、seenStoppedDays 10)
- 火事の印の地点の近く: 289(火葬場21324→6880、(3163,-332)、Blocked、blockCounter 94、seenStoppedDays 10)、357(火葬場39843 へ戻る途中、(3272,-316)、Congestion+Blocked、seenStoppedDays 10)

### `buildings_near(x=2240, z=186, radius=500, service="HealthCare", brief=false, limit=20)`

- total 6
- 火葬場23747: 保管 0 / 105、先週の処理 4、霊柩車 7 / 9
- 火葬場31990: 保管 1 / 105、先週の処理 7、霊柩車 4 / 9
- 火葬場36841: 保管 0 / 105、先週の処理 0、霊柩車 7 / 9
- 火葬場41597: 保管 0 / 105、先週の処理 0、霊柩車 8 / 9
- 診療所12648: 患者 23 / 100、救急車 10 / 10
- 診療所21521: 患者 25 / 100、救急車 10 / 10

### `traffic(x=2240, z=186, radius=500)`

- flow 50、cars 596、blocked 33、congestion 284、roadSegments 164、averageDensity 40
- busiest(density 100): 2093 (2684,330)、2152 (1880,133)、30427 (2336,560)、6523 (2152,443)、29165 (1797,330)、24873 (2263,560)、25781 (2648,330)、5473 (2190,560)、23279 (1852,330)、18127 (2557,560)
- blockedSpots: (2244,289) 14、(2204,175) 8、(2060,238) 8、(2227,-118) 2、(2223,-208) 1

## 月末(2050-01-31)

### `vehicles_stuck(kind="hearse", limit=30)`

- vehicles 189
- byState(主なもの): Congestion+Spawned+OnRoad 52、Congestion+Spawned+OnRoad+Blocked 51、Spawned+OnRoad+Blocked 36、Stopped+Spawned+OnRoad 8、Congestion+GoingBack+Spawned+OnRoad 8、GoingBack+Spawned+OnRoad+Blocked 7、Spawned+InGrounds 6
- byPath: ready 176、none 13
- bySeenStopped: <1day 129、7days+ 60
- byTarget: 行き先なし 29台、ほかは1台ずつ
- (2240,186)の近くのサンプル: 20(火葬場31990→2513、(2205,309)、Congestion+Blocked、blockCounter 60、seenStoppedDays 10.1)、1040(火葬場17188→3969、(2114,268)、Congestion+Blocked、blockCounter 56、seenStoppedDays 20)、1526(火葬場36841→11280、(1964,149)、Blocked、blockCounter 32)
- 火事の印の地点の近く: 289(火葬場21324→45284、(3146,-302)、Blocked、blockCounter 59)、357(火葬場39843 へ戻る途中、(3221,-316)、Congestion+Blocked、blockCounter 52、seenStoppedDays 20)

### `buildings_near(x=2240, z=186, radius=500, service="HealthCare", brief=false, limit=20)`

- total 6
- 火葬場23747: 保管 0 / 105、先週の処理 0、霊柩車 7 / 9
- 火葬場31990: 保管 0 / 105、先週の処理 20、霊柩車 3 / 9
- 火葬場36841: 保管 0 / 105、先週の処理 0、霊柩車 7 / 9
- 火葬場41597: 保管 0 / 105、先週の処理 3、霊柩車 7 / 9
- 診療所12648: 患者 21 / 100、救急車 10 / 10
- 診療所21521: 患者 27 / 100、救急車 10 / 10

### `traffic(x=2240, z=186, radius=500)`

- flow 53、cars 542、blocked 105、congestion 290、roadSegments 164、averageDensity 36
- busiest(density 100): 6010 (1800,103)、6523 (2152,443)、30427 (2336,560)、2093 (2684,330)、19619 (2606,330)、5473 (2190,560)、12970 (1850,107)、25781 (2648,330)、24873 (2263,560)、7469 (2152,522)
- blockedSpots: (2078,277) 33、(1913,71) 15、(2069,159) 14、(2205,276) 13、(1939,328) 10、(2529,558) 7、(1751,92) 7、(2207,-230) 2、(1895,-25) 2、(2204,127) 2
- 参考(同じ日の `complaints`): Death 40、hotspot (2214,198) 17棟
