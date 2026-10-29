# m07 調査 s07-3(roads)x=2110 の止まり

## 2050-07-11(見回り1)

- `traffic` x 2096, z 278, radius 40: flow 54、cars 11、blocked 8(すべて道の上)、congestion 6、averageDensity 65。blockedSpots (2110,276) 8台。busiest 22887 (2110,303) density 69、5864 (2110,267) density 62(どちらも Small 4 Lane Road)
- `junction_info` x 2110, z 330: node 30603、trafficLights false、canEnableLights true、canSetYield true。道は3本(3990 bearing 90、22887 bearing 180、26735 bearing 270)、yield はどれも false
- `junction_info` x 2110, z 240: node 24624、trafficLights false、canEnableLights true、canSetYield true。道は3本(5864 bearing 0、4374 bearing 180、9308 bearing 270)、yield はどれも false

## 2050-07-21(見回り2)

- `traffic` x 2096, z 278, radius 40: flow 53、cars 13、blocked 8(すべて道の上)、congestion 8、averageDensity 77。blockedSpots (2110,283) 8台。busiest 22887 (2110,303) density 100、5864 (2110,267) density 55
- `junction_info` x 2110, z 330 と z 240: 信号なし、yield はどの道も false(見回り1と同じ。この日の呼び出しは両方行った)

## 2050-07-31(月末)

- `traffic` x 2096, z 278, radius 40: flow 50、cars 8、blocked 1(道の上)、congestion 6、averageDensity 74。blockedSpots (2091,238) 1台。busiest 22887 (2110,303) density 87、5864 (2110,267) density 61
- `junction_info` x 2110, z 330: node 30603、trafficLights false、yield はどの道も false
- `junction_info` x 2110, z 240: node 24624、trafficLights false、yield はどの道も false
