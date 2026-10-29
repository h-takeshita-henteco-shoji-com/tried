# m08 調査 s08-3 東の幹線の交差点(roads)

## 2050-08-10 見回り1

- `junction_info` x=2700 z=330: node 9244、trafficLights false、canEnableLights true。3方向(segment 19421 bearing 180、4818 bearing 90、2093 bearing 270、すべて Small 4 Lane Road)
- `traffic` x=2700 z=330 radius=80 limit=10: flow 53、cars 58、blocked 13、congestion 23、averageDensity 94。density 100 の区間: 25781(2648,330)、19421(2700,303)、2093(2684,330)、4818(2741,330)。34550(2668,371)90、9781(2700,267)79。blockedSpots (2685,342) 13

## 2050-08-20 見回り2

- `junction_info` x=2700 z=330: 見回り1と同じ(信号なし、3方向、すべて Small 4 Lane Road)
- `traffic` x=2700 z=330 radius=80 limit=10: flow 54、cars 37、blocked 19、congestion 16、averageDensity 73。density 100: 25781(2648,330)、2093(2684,330)。4818(2741,330)94、34550(2668,371)81、19421(2700,303)45、9781(2700,267)19。blockedSpots (2708,341) 19

## 2050-08-30 月末

- `junction_info` x=2700 z=330: 前回と同じ(信号なし、3方向、すべて Small 4 Lane Road)
- `traffic` x=2700 z=330 radius=80 limit=10: flow 52、cars 54、blocked 17、congestion 21、averageDensity 87。density 100: 25781(2648,330)、2093(2684,330)。19421(2700,303)95、34550(2668,371)79、4818(2741,330)76、9781(2700,267)74。blockedSpots (2691,300) 17
