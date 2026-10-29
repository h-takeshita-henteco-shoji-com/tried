# m05 調査 s05-3(roads)東西の幹線 z=330 の詰まりの原因

## 2050-05-12(見回り1)

- `traffic` x 2700、z 320、radius 60: flow 53、cars 36、blocked 6、congestion 17、roadSegments 6、averageDensity 98。busiest はすべて Small 4 Lane Road: 19421 (2700,303) 100、25781 (2648,330) 100、34550 (2668,371) 100、2093 (2684,330) 100、4818 (2741,330) 98、9781 (2700,267) 92。blockedSpots (2657,343) 6
- `junction_info` x 2700、z 330: node 9244、trafficLights false、canEnableLights true、canSetYield true。入る道は3本(segment 19421 bearing 180、4818 bearing 90、2093 bearing 270、すべて Small 4 Lane Road、cars true、yield false)

## 2050-06-01(月末)

- `traffic` x 2700、z 320、radius 60: flow 54、cars 41、blocked 3、congestion 19、roadSegments 6、averageDensity 92。busiest: 34550 (2668,371) 100、25781 (2648,330) 100、2093 (2684,330) 100、4818 (2741,330) 100、19421 (2700,303) 91、9781 (2700,267) 62。blockedSpots (2716,334) 3
- `junction_info` x 2700、z 330: node 9244、trafficLights false、customLights false、canEnableLights true、canSetYield true。入る道は3本とも cars true、yield false(見回り1と同じ)
