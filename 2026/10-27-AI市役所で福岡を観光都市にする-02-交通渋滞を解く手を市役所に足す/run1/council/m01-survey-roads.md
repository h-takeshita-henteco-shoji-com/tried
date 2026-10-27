# m01 調査 s01-1 の結果(道路下水道局)

問い: (-726,-736) の詰まりは、信号か道の幅のどちらが原因か。
見る道具と引数: `traffic`(x=-726、z=-736、radius=150、limit=8)、`junction_info`(x=-722、z=-740)

## 見回り1(2050-01-11)

- `traffic`(x=-726、z=-736、radius=150、limit=8): flow 51、cars 131、blocked 12(道の上12、敷地0)、congestion 17、roadSegments 4、averageDensity 99
  - busiest: 区間30435 Large Road (-611,-740) 100、36115 Large Road (-832,-740) 100、6545 Large Road (-685,-740) 99、10922 Large Road (-759,-740) 98
  - blockedSpots: (-655,-738) 8台、(-852,-734) 4台
- `junction_info`(x=-722、z=-740): ok=false、"no road junction within 40m"

## 見回り2(2050-01-21)

- `traffic`(x=-726、z=-736、radius=150、limit=8): flow 50、cars 97、blocked 50(道の上50、敷地0)、congestion 26、roadSegments 4、averageDensity 73
  - busiest: 区間36115 Large Road (-832,-740) 100、10922 Large Road (-759,-740) 85、6545 Large Road (-685,-740) 57、30435 Large Road (-611,-740) 51
  - blockedSpots: (-734,-737) 26台、(-828,-735) 24台
- `junction_info`(x=-722、z=-740): ok=false、"no road junction within 40m"

### 座標を直すための確かめ(引き継ぎの指示による)

- `net_near`(x=-726、z=-736、radius=150、service=Road、limit=30): 区間5つ。どれも z=-740 の東西の道
  - 30435 Large Road(-574→-648)、6545 Large Road(-648→-722)、10922 Large Road(-722→-796)、36115 Large Road(-796→-870)、3276 Large Road with Median(-870→-920)。どれも carLanes 3 / 3
  - 点5403(-648)、5487(-722)、5154(-796)は、それぞれ2区間だけがつながる。半径150の中に、南北に交わる道はない
- `junction_info`(x=-870、z=-740): ok=true、点20174。区間36115(Large Road、bearing 90)と3276(Large Road with Median、bearing 270)の2方向。trafficLights false、customLights false、canEnableLights true、canSetYield true
- `junction_info`(x=-574、z=-740): ok=false、"no road junction within 40m"

## 月末(2050-01-31)

- `traffic`(x=-726、z=-736、radius=150、limit=8): flow 52、cars 84、blocked 12(道の上12、敷地0)、congestion 22、roadSegments 4、averageDensity 65
  - busiest: 区間36115 Large Road (-832,-740) 100、10922 Large Road (-759,-740) 58、6545 Large Road (-685,-740) 55、30435 Large Road (-611,-740) 50
  - blockedSpots: (-851,-736) 12台
- `junction_info`(x=-722、z=-740): ok=false、"no road junction within 40m"
- `junction_info`(x=-870、z=-740、直した座標): ok=true、点20174。区間36115(Large Road)と3276(Large Road with Median)の2方向。trafficLights false、canEnableLights true、canSetYield true

## 3回の数(まとめ。見立ては書かない)

| 日付 | blocked | averageDensity | 区間36115 | 区間10922 | 区間6545 | 区間30435 |
|---|---|---|---|---|---|---|
| 2050-01-11(見回り1の記録) | 12 | 99 | 100 | 98 | 99 | 100 |
| 2050-01-21 | 50 | 73 | 100 | 85 | 57 | 51 |
| 2050-01-31 | 12 | 65 | 100 | 58 | 55 | 50 |
