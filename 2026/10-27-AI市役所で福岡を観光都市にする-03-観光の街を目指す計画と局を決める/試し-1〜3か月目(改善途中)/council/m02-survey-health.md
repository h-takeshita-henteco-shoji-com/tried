# m02 調査 s02-2(health)死体とごみの印

## 2050-02-12(見回り1)

- 道具: `vehicles_stuck(kind="garbage", limit=30)`
  - 台数 251(Congestion を含む状態が大半)。bySeenStopped: 1日未満 111、7日以上 140。path は全部 ready
  - 行き先 0(戻る途中)が 85。止まった場所は (2153,442)、(2247,558)、(2195,-810)、(2200〜2560,-946) などに多い
- 道具: `vehicles_stuck(kind="hearse", limit=30)`
  - 台数 174。bySeenStopped: 1日未満 123、7日以上 51。path none 14、ready 160
  - 状態は Congestion+OnRoad 系が大半(67 + 38 + 12 ほか)。WaitingTarget 8
- 道具: `traffic(x=2157, z=400, radius=400, limit=10)`
  - flow 55、cars 340、blocked 75、congestion 190、averageDensity 42
  - blockedSpots: (2156,473) 37、(2206,278) 14、(2275,558) 14、(2156,376) 5、(2080,144) 5
- 道具: `complaints`(2050-02-02): Death 34(月例時 37)、Garbage 23(月例時 24)

## 2050-02-22(見回り2)

- 道具: `vehicles_stuck(kind="garbage", limit=30)`
  - 台数 267。bySeenStopped: 1日未満 106、7日以上 161。path none 4、ready 263。行き先 0 が 89
- 道具: `vehicles_stuck(kind="hearse", limit=30)`
  - 台数 161。bySeenStopped: 1日未満 100、7日以上 61。path none 9、ready 152。Congestion+OnRoad 系が大半(60 + 42 + 16 ほか)
- 道具: `traffic(x=2157, z=400, radius=400, limit=10)`
  - flow 55、cars 381、blocked 136、congestion 187、averageDensity 45
  - blockedSpots: (2250,292) 37、(2089,298) 37、(2153,465) 29、(2497,334) 13、(1970,60) 8

## 2050-03-04(月末)

- 道具: `vehicles_stuck(kind="garbage", limit=30)`
  - 台数 263。bySeenStopped: 1日未満 94、7日以上 169。path none 1、ready 262。行き先 0 が 106
- 道具: `vehicles_stuck(kind="hearse", limit=30)`
  - 台数 140。bySeenStopped: 1日未満 88、7日以上 52。path none 6、ready 134。Congestion+OnRoad 系が大半(44 + 45 + 14 ほか)
- 道具: `traffic(x=2157, z=400, radius=400, limit=10)`
  - flow 56、cars 315、blocked 79、congestion 159、averageDensity 40
  - blockedSpots: (2097,275) 29、(2310,331) 20、(2029,64) 10、(2497,334) 8、(1968,64) 8
