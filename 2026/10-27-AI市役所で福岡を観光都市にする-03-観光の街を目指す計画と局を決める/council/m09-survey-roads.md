# m09 調査 roads(s09-1)

問い: 東の (2114,284) の blocked 40 は、信号の手前の待ちか、区間の途中の詰まりか。

## 2050-09-08(見回り1)

- `traffic` x=2114, z=284, radius=60, limit=5: flow 54, cars 20, blocked 10, congestion 10, averageDensity 70。busiest: 22887 Small 4 Lane Road (2110,303) density 90、5864 (2110,267) 61、3990 (2132,330) 59。blockedSpots (2111,276) 10
- `traffic` x=2110, z=240, radius=60, limit=5: flow 54, cars 20, blocked 10, congestion 11, averageDensity 77。busiest: 4374 Small 4 Lane Road (2110,213) 93、9308 (2069,240) 78、5864 (2110,267) 61。blockedSpots (2101,263) 10

## 2050-09-18(見回り2)

- `traffic` x=2114, z=284, radius=60, limit=5: flow 53, cars 19, blocked 12, congestion 12, averageDensity 72。busiest: 22887 (2110,303) density 84、5864 (2110,267) 82、3990 (2132,330) 51。blockedSpots (2104,286) 12
- `traffic` x=2110, z=240, radius=60, limit=5: flow 53, cars 17, blocked 7, congestion 9, averageDensity 76。busiest: 5864 (2110,267) 82、4374 (2110,213) 77、9308 (2069,240) 71。blockedSpots (2104,262) 7

## 2050-09-28(月末)

- `traffic` x=2114, z=284, radius=60, limit=5: flow 55, cars 18, blocked 0, congestion 8, averageDensity 76。busiest: 22887 (2110,303) density 100、3990 (2132,330) 77、5864 (2110,267) 51。blockedSpots なし
- `traffic` x=2110, z=240, radius=60, limit=5: flow 55, cars 18, blocked 7, congestion 13, averageDensity 78。busiest: 4374 (2110,213) 100、9308 (2069,240) 85、5864 (2110,267) 51。blockedSpots (2114,212) 4、(2114,189) 3
