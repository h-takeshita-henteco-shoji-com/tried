# m02 調査 s02-2(roads): 4車線が2車線に絞られる所で詰まりが続くか

問い: (2237, -936) 付近の詰まりは、Small 4 Lane Road が Basic Road に絞られる3区間(3334、36011、19196)で起きているか。

## 見回り1(2050-02-10)

- `traffic(x=2237, z=-936, radius=150, limit=8)`: flow 52、cars 120、blocked 22、congestion 42、roadSegments 17、averageDensity 89
  - busiest(すべて density 100): 19196 Basic Road (2194,-950)、20293 Basic Road (2236,-886)、13096 Small 4 Lane Road (2370,-950)、14040 Basic Road (2272,-860)、36011 Basic Road (2228,-950)、36773 Basic Road (2227,-1058)、29545 Basic Road (2220,-978)、30068 Small 4 Lane Road (2313,-950)
  - blockedSpots: (2168,-869) 22台
  - 3区間のうち 19196 と 36011 は busiest に出た。3334 は出なかった
- `traffic(limit=10)`: flow 52、cars 7,729、blocked 809、congestion 2,554、roadSegments 3,794、averageDensity 26
  - blockedSpots の上位: (-1698,-1068) 54、(705,-701) 47、(3304,-286) 42、(2080,287) 37、(-700,-734) 36、(2137,-856) 34、(-292,-944) 34、(247,-294) 32、(1692,91) 29、(97,-252) 27
- `junction_info(x=2236, z=-950)`: node 5405、信号なし(trafficLights false、canEnableLights true)。入る区間は 3334 Basic Road(bearing 90)、36011 Basic Road(270)、10391 Basic Road(0)。どれも yield false

## 見回り2(2050-02-20)

- `traffic(x=2237, z=-936, radius=150, limit=8)`: flow 54、cars 153、blocked 13、congestion 41、roadSegments 17、averageDensity 88
  - busiest(すべて density 100): 20293 Basic Road (2236,-886)、19196 Basic Road (2194,-950)、13096 Small 4 Lane Road (2370,-950)、29545 Basic Road (2220,-978)、36773 Basic Road (2227,-1058)、36011 Basic Road (2228,-950)、30068 Small 4 Lane Road (2313,-950)、10391 Basic Road (2236,-924)
  - blockedSpots: (2151,-899) 13台
  - 3区間のうち 19196 と 36011 は busiest に出た。3334 は出なかった
- `traffic(limit=10)`: flow 54、cars 7,805、blocked 754、congestion 2,556、averageDensity 27
  - busiest に 36011 Basic Road (2228,-950) が入った
  - blockedSpots の上位: (1700,92) 73、(1889,87) 44、(-851,-734) 34、(-1676,-1460) 33、(-1682,-1309) 29、(3097,-474) 29、(1567,-89) 28、(2153,472) 27、(2093,301) 27、(243,-276) 26
- `junction_info(x=2236, z=-950)`: 見回り1と同じ。node 5405、信号なし、入る区間 3334・36011・10391(すべて Basic Road、yield false)

## 月末(2050-03-02)

- `traffic(x=2237, z=-936, radius=150, limit=8)`: flow 54、cars 148、blocked 21、congestion 47、roadSegments 17、averageDensity 92
  - busiest(すべて density 100): 20169 Medium Road (2160,-914)、20293 Basic Road (2236,-886)、14040 Basic Road (2272,-860)、19196 Basic Road (2194,-950)、36011 Basic Road (2228,-950)、36773 Basic Road (2227,-1058)、29545 Basic Road (2220,-978)、30068 Small 4 Lane Road (2313,-950)
  - blockedSpots: (2171,-866) 21台
  - 3区間のうち 19196 と 36011 は busiest に出た。3334 は出なかった(3回とも同じ)
- `traffic(limit=10)`: flow 54、cars 7,773、blocked 646、congestion 2,556、averageDensity 26
  - busiest に 15481 Small 4 Lane Road (2430,-950) が入った
  - blockedSpots の上位: (-925,-702) 34、(2074,289) 33、(2141,-853) 32、(2163,-729) 30、(1731,-842) 28、(-1484,-673) 27、(2291,322) 24、(-1704,-1072) 18、(-2135,-712) 18、(1709,-520) 18
- `junction_info(x=2236, z=-950)`: 見回り1・2と同じ。node 5405、信号なし、入る区間 3334・36011・10391(すべて Basic Road、yield false)
