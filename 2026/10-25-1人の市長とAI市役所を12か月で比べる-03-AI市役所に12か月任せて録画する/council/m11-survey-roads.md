# m11 調査の結果(roads)

## s11-2 信号を付けた (2700,330) の近くで blocked が61のまま残る理由

問い: 信号を付けた (2700,330) の近くで blocked が61のまま残るのは、一時的な混みか、信号の待ち行列か。
見る道具と引数は議案のとおり。見立ては書かない(局が翌月に読む)。
同じ月の m11-2 で、2050-10-28 にバスの予算を110%から130%に戻した。

### 見回り1(2050-11-07)

- `traffic(x=2704, z=297, radius=120)`
  - flow 54、cars 104、blocked 45(道の上45、建物の中0)、congestion 62、区間10、averageDensity 92
  - density: 22938 Small 4 Lane (2818,330) 100、19421 Small 4 Lane (2700,303) 100、19619 Small 4 Lane (2606,330) 100、7468 Basic Road (2668,370) 100、2093 Small 4 Lane (2684,330) 100、25781 Small 4 Lane (2648,330) 100、4818 Small 4 Lane (2741,330) 100、9781 Small 4 Lane (2700,267) 86、2176 Small 4 Lane (2700,213) 80、35020 Small 4 Lane (2741,240) 54
  - blockedSpots: (2708,304) 35、(2701,188) 5、(2807,334) 4、(2666,402) 1
- `junction_info(x=2700, z=330)`
  - node 9244、trafficLights true、customLights true、canEnableLights true、canSetYield false
  - roads: 19421 Small 4 Lane bearing 180、4818 Small 4 Lane bearing 90、2093 Small 4 Lane bearing 270。どれも cars true、yield false

### 見回り2(2050-11-17)

- `traffic(x=2704, z=297, radius=120)`
  - flow 54、cars 110、blocked 38(道の上38、建物の中0)、congestion 72、区間10、averageDensity 92
  - density: 19421 (2700,303) 100、25781 (2648,330) 100、22938 (2818,330) 100、19619 (2606,330) 100、2093 (2684,330) 100、4818 (2741,330) 100、7468 Basic Road (2668,370) 100、2176 (2700,213) 82、9781 (2700,267) 73、35020 (2741,240) 69
  - blockedSpots: (2715,326) 33、(2666,402) 2、(2812,334) 2、(2594,334) 1
- `junction_info(x=2700, z=330)`
  - node 9244、trafficLights true、customLights true、canEnableLights true、canSetYield false
  - roads: 19421 bearing 180、4818 bearing 90、2093 bearing 270。どれも cars true、yield false(見回り1と同じ)

### 月末(2050-11-27)

- `traffic(x=2704, z=297, radius=120)`
  - flow 54、cars 101、blocked 41(道の上41、建物の中0)、congestion 54、区間10、averageDensity 92
  - density: 19619 (2606,330) 100、19421 (2700,303) 100、25781 (2648,330) 100、22938 (2818,330) 100、9781 (2700,267) 100、2093 (2684,330) 100、4818 (2741,330) 100、7468 Basic Road (2668,370) 100、2176 (2700,213) 90、35020 (2741,240) 34
  - blockedSpots: (2693,318) 35、(2701,188) 4、(2666,404) 2
- `junction_info(x=2700, z=330)`
  - node 9244、trafficLights true、customLights true、canEnableLights true、canSetYield false
  - roads: 19421 bearing 180、4818 bearing 90、2093 bearing 270。どれも cars true、yield false(3回とも同じ)
- 参考(調査の道具ではなく m11-2 の測る数として呼んだ街全体の `traffic()`): blockedSpots の2番目が (2693,318) 35
