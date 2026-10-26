# m01 調査の結果(roads)

## s01-2 止まった車の多い場所が動くか

### 見回り1(2050-01-11)

- `traffic`(x=2309, z=-925, radius=200, limit=5)
  - cars 186、blocked 110、congestion 70、averageDensity 75
  - busiest(density 100): Basic Road 19196 (2194, -950)、Basic Road 20293 (2236, -886)、Small 4 Lane Road 15481 (2430, -950)、Basic Road 14040 (2272, -860)、Small 4 Lane Road 14041 (2490, -950)
  - blockedSpots: (2287, -926) 74、(2446, -947) 20、(2175, -889) 8、(2218, -1030) 7、(2194, -1051) 1
- `traffic`(x=-726, z=-736, radius=200, limit=5)
  - cars 185、blocked 20、congestion 37、averageDensity 93
  - busiest: Small 4 Lane Road 16866 (-920, -712) 100、Large Road 36115 (-832, -740) 100、Large Road with Median 3276 (-895, -740) 100、Large Road 10922 (-759, -740) 98、Large Road 6545 (-685, -740) 95
  - blockedSpots: (-857, -734) 20
- `traffic`(引数なし、limit=10)
  - flow 51、cars 7,661、blocked 813(道 810、建物 3)、congestion 2,526、averageDensity 26
  - blockedSpots の上位10: (2287, -926) 74、(2102, 287) 34、(3152, -309) 34、(1697, 102) 29、(2251, 303) 29、(-868, -728) 24、(2457, -947) 24、(1525, 46) 24、(877, -705) 23、(3171, -129) 23

### 見回り2(2050-01-21)

- `traffic`(x=2309, z=-925, radius=200, limit=5)
  - cars 187、blocked 6、congestion 63、averageDensity 74
  - busiest(density 100): Small 4 Lane Road 15481 (2430, -950)、Basic Road 19196 (2194, -950)、Basic Road 14040 (2272, -860)、Small 4 Lane Road 14041 (2490, -950)、Basic Road 20293 (2236, -886)
  - blockedSpots: (2134, -861) 4、(2229, -742) 2
- `traffic`(x=-726, z=-736, radius=200, limit=5)
  - cars 151、blocked 8、congestion 30、averageDensity 88
  - busiest(density 100): Large Road 10922 (-759, -740)、Small 4 Lane Road 16866 (-920, -712)、Large Road 36115 (-832, -740)、Large Road with Median 3276 (-895, -740)、Small 4 Lane Road 9066 (-920, -768)
  - blockedSpots: (-917, -763) 8
- `traffic`(引数なし、limit=10)
  - flow 52、cars 7,706、blocked 973(道 973、建物 0)、congestion 2,563、averageDensity 26
  - blockedSpots の上位10: (1701, 97) 87、(3123, -275) 50、(1883, 90) 38、(714, -700) 38、(2067, 103) 37、(512, -725) 36、(2090, 287) 30、(1918, -25) 29、(3179, -103) 28、(1303, -741) 27

### 月末(2050-01-31)

- `traffic`(x=2309, z=-925, radius=200, limit=5)
  - cars 180、blocked 42、congestion 66、averageDensity 75
  - busiest(density 100): Basic Road 19196 (2194, -950)、Basic Road 20293 (2236, -886)、Basic Road 14040 (2272, -860)、Small 4 Lane Road 15481 (2430, -950)、Basic Road 22902 (2234, -1088)
  - blockedSpots: (2237, -936) 23、(2162, -927) 16、(2221, -1009) 3
- `traffic`(x=-726, z=-736, radius=200, limit=5)
  - cars 173、blocked 15、congestion 40、averageDensity 88
  - busiest: Small 4 Lane Road 9066 (-920, -768) 100、Small 4 Lane Road 16866 (-920, -712) 100、Large Road with Median 3276 (-895, -740) 100、Large Road 36115 (-832, -740) 100、Large Road 32158 (-537, -740) 85
  - blockedSpots: (-697, -738) 10、(-920, -744) 5
- `traffic`(引数なし、limit=10)
  - flow 53、cars 7,736、blocked 794(道 793、建物 1)、congestion 2,552、averageDensity 27
  - blockedSpots の上位10: (1677, 92) 53、(1487, 58) 36、(2117, -933) 32、(-1744, 93) 28、(1301, 99) 27、(3128, -266) 26、(3087, -476) 26、(2237, -936) 23、(1635, -770) 23、(97, -252) 22
