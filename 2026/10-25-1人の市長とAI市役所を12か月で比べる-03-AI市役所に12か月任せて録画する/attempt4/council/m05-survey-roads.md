# m05 調査 roads(s05-3)

問い: 交差点でない場所で blocked が多い (2498,-946) 周辺の列は、西の信号(2236,-950)の先で細くなる区間(Basic Road、2280〜2160)のせいで伸びているか

## 見回り1(2050-05-11)

- `traffic(x=2498, z=-946, radius=300)`
  - flow 56、cars 254、blocked 5、congestion 84、roadSegments 43、averageDensity 59
  - busiest(密度100): 15481 Small 4 Lane (2430,-950)、36773 Basic (2227,-1058)、14041 Small 4 Lane (2490,-950)、13096 Small 4 Lane (2370,-950)、14040 Basic (2272,-860)、19456 Small 4 Lane (2760,-981)、34194 Small 4 Lane (2550,-950)、36011 Basic (2228,-950)、30068 Small 4 Lane (2313,-950)、20293 Basic (2236,-886)
  - blockedSpots: (2256,-948) 5
- `traffic(x=2236, z=-950, radius=100)`
  - cars 76、blocked 5、congestion 25、roadSegments 10、averageDensity 96
  - busiest: 29545 Basic (2220,-978) 100、20293 Basic (2236,-886) 100、36011 Basic (2228,-950) 100、30068 Small 4 Lane (2313,-950) 100、19196 Basic (2194,-950) 100、10391 Basic (2236,-924) 100、3334 Basic (2258,-950) 100、14040 Basic (2272,-860) 100、20169 Medium (2160,-914) 94、6223 Basic (2220,-1022) 75
  - blockedSpots: (2256,-948) 5

## 見回り2(2050-05-21)

- `traffic(x=2498, z=-946, radius=300)`
  - flow 56、cars 218、blocked 1、congestion 86、roadSegments 43、averageDensity 55
  - busiest(密度100): 15481 Small 4 Lane (2430,-950)、20293 Basic (2236,-886)、22902 Basic (2234,-1088)、13096 Small 4 Lane (2370,-950)、14040 Basic (2272,-860)、14041 Small 4 Lane (2490,-950)、34194 Small 4 Lane (2550,-950)、36011 Basic (2228,-950)、36773 Basic (2227,-1058)、24275 Basic (2550,-1240)
  - blockedSpots: (2563,-1236) 1
- `traffic(x=2236, z=-950, radius=100)`
  - cars 79、blocked 0、congestion 31、roadSegments 10、averageDensity 98
  - busiest: 29545 Basic (2220,-978) 100、20293 Basic (2236,-886) 100、36011 Basic (2228,-950) 100、30068 Small 4 Lane (2313,-950) 100、19196 Basic (2194,-950) 100、6223 Basic (2220,-1022) 100、3334 Basic (2258,-950) 100、10391 Basic (2236,-924) 100、14040 Basic (2272,-860) 100、20169 Medium (2160,-914) 85
  - blockedSpots: なし

## 月末(2050-05-31)

- `traffic(x=2498, z=-946, radius=300)`
  - flow 56、cars 215、blocked 59、congestion 91、roadSegments 43、averageDensity 55
  - busiest(密度100): 14041 Small 4 Lane (2490,-950)、15481 Small 4 Lane (2430,-950)、14040 Basic (2272,-860)、13096 Small 4 Lane (2370,-950)、13690 Basic (2484,-1240)、20293 Basic (2236,-886)、30068 Small 4 Lane (2313,-950)、36773 Basic (2227,-1058)、29545 Basic (2220,-978)、22902 Basic (2234,-1088)
  - blockedSpots: (2330,-946) 34、(2458,-945) 25
- `traffic(x=2236, z=-950, radius=100)`
  - cars 69、blocked 18、congestion 24、roadSegments 10、averageDensity 97
  - busiest: 20293 Basic (2236,-886) 100、19196 Basic (2194,-950) 100、30068 Small 4 Lane (2313,-950) 100、29545 Basic (2220,-978) 100、6223 Basic (2220,-1022) 100、3334 Basic (2258,-950) 100、10391 Basic (2236,-924) 100、14040 Basic (2272,-860) 100、36011 Basic (2228,-950) 90、20169 Medium (2160,-914) 85
  - blockedSpots: (2296,-946) 18
