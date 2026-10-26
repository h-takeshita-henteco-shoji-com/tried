# m10 調査の結果(economy)

## s10-1 品物がない店の群 (-1115,-877) に向かう品物のトラックが、どこで止まっているか

問い: 品物がない店の最大の群 (-1115,-877) の店に向かう品物のトラックは、どこで止まっているのか。
見る道具と引数は議案のとおり。見立ては書かない(局が翌月に読む)。

### 見回り1(2050-10-08)

- `vehicles_stuck(kind="truck", building=1366, limit=30)`
  - vehicles 111
  - byState: WaitingSpace+Importing+InGrounds 31、Importing+Spawned+OnRoad+Blocked 56、GoingBack+Importing+Spawned+OnRoad+Blocked 19、Importing+Spawned+InGrounds 4、Congestion+Importing+Spawned+OnRoad 1
  - byPath: ready 111
  - bySeenStopped: <1day 60、7days+ 51(この道具で初めて見たのは m09 の調査)
  - byTarget の上位: 行き先なし(0)19、40739 H3 3x2 Shop04 (-1052,-1574) 3、36654 Shop03 (-2024,-1170) 2、38403 工場 (3388,-1216) 2、39818 Future Store (324,251) 2、20102 工場 (2126,1484) 2、42207 Shop04 (1924,1063) 2、40421 Shop04 (-508,-56) 2
  - samples 30台のうち、港の敷地 (-2000,589) 付近で WaitingSpace / InGrounds が13台(荷は Coal、Lumber、Petrol、Goods)
  - samples の Goods を積んで道の上で Blocked の車: (-1846,-782) 40739行き blockCounter 5・9.9日、(-1846,-774) 40739行き 5・9.9日、(-1846,-821) 36654行き 10・9.9日、(-1834,92) 40916行き 13・9.9日、(-950,-562) 45382行き(残り34m)27・9.9日、(233,96) 44477行き 7
  - samples のほかの道の上の Blocked: (-941,92) Food 42、(-1294,92) Petrol 20・9.9日、(-961,92) Coal 41・9.9日、(-921,-586) Petrol 49、(-1282,-399) Lumber 1・9.9日
  - 帰り(GoingBack)の Blocked: (-1818,-1302)、(-1941,107)、(-505,12)、(-1960,445)、(2220,-1162)、(113,-78)
- `buildings_near(x=-1115, z=-877, radius=500, problem="NoGoods", brief=true, limit=50)`
  - total 10: 9360 (-1384,-1166)、18547 (-1404,-1214)、20760 (-896,-838)、21481 (-1014,-536)、26357 (-1305,-1124)、26764 (-1180,-1214) FatalProblem、33087 (-896,-1178)、35577 (-896,-1083)、38627 (-1468,-1166)、42813 (-1264,-1218) FatalProblem
- `traffic(x=-877, z=-724, radius=300, limit=10)`
  - flow 55、cars 324、blocked 42(道の上42、建物の中0)、congestion 88、区間40、averageDensity 73
  - density 100 の区間: 15602 Basic Road (-1101,-560)、16866 Small 4 Lane (-920,-712)、17082 Basic Road (-1018,-920)、11266 Small 4 Lane (-1060,-920)、10370 Small 4 Lane (-960,-740)、9066 Small 4 Lane (-920,-768)、30891 Small 4 Lane (-920,-942)、3276 Large Road with Median (-895,-740)、36115 Large Road (-832,-740)、30366 Small 4 Lane (-1070,-713)
  - blockedSpots: (-931,-678) 13、(-918,-963) 12、(-1066,-681) 11、(-923,-579) 6

### 見回り2(2050-10-18)

- `vehicles_stuck(kind="truck", building=1366, limit=30)`
  - vehicles 135
  - byState: WaitingSpace+Importing+InGrounds 87、Importing+Spawned+OnRoad+Blocked 31、GoingBack+Importing+Spawned+OnRoad+Blocked 9、Importing+Spawned+InGrounds 6、WaitingTarget+Importing+Spawned+InGrounds 1、Congestion+Importing+Spawned+OnRoad 1
  - byPath: ready 134、none 1
  - bySeenStopped: <1day 102、7days+ 33
  - byTarget の上位: 行き先なし(0)10、11690 工場 (2606,1354) 2、ほかは各1(48568 Shop01 (-1616,-1516)、44017 Shop01 (324,-27)、34836 Shop01 (-832,-240)、44568 Shop01 (-2144,-96)、工場4棟)
  - samples 30台のうち、港の敷地 (-2000,589) で WaitingSpace+InGrounds が18台(荷は Petrol、Coal、Goods、Lumber、Food)。Goods は 43908 (1,771m)、44532 (1,307m)、42739 (4,432m)、41412 (3,869m)、38204 (653m)、44333 (1,357m) 行き
  - samples の道の上の Blocked: (-1969,122) Coal 4、(-1107,-654) Food 45、(-1847,-831) Food 26、(-98,-728) Food 27、(-1882,93) Lumber 10・10日、(352,96) Lumber 7、(257,96) Goods 34964行き 10、(-1896,94) Petrol 1・10日、(231,96) Lumber 7、(-1102,-379) Food 2
  - 帰り(GoingBack)の Blocked: (-1816,-995) blockCounter 42・10日、(-1957,446) 23
- `buildings_near(x=-1115, z=-877, radius=500, problem="NoGoods", brief=true, limit=50)`
  - total 10(見回り1と同じ10棟)。FatalProblem は 18547、21481、26357、26764、42813 の5棟(見回り1は2棟)。MajorProblem は 9360、33087、35577、38627
- `traffic(x=-877, z=-724, radius=300, limit=10)`
  - flow 55、cars 285、blocked 61(道の上61、建物の中0)、congestion 106、区間40、averageDensity 64
  - density 100 の区間: 16866 (-920,-712)、11266 (-1060,-920)、8646 (-920,-677)、9066 (-920,-768)、33761 Basic Road (-959,-560)、3276 Large Road with Median (-895,-740)、819 (-960,-650)、4744 Basic Road (-920,-988)、36115 Large Road (-832,-740)。30891 (-920,-942) は96
  - blockedSpots: (-940,-703) 32、(-1069,-685) 24、(-920,-876) 5

### 月末(2050-10-28)

- `vehicles_stuck(kind="truck", building=1366, limit=30)`
  - vehicles 115
  - byState: WaitingSpace+Importing+InGrounds 58、Importing+Spawned+OnRoad+Blocked 35、GoingBack+Importing+Spawned+OnRoad+Blocked 16、Importing+Spawned+InGrounds 5、WaitingTarget+WaitingSpace+Importing+InGrounds 1
  - byPath: ready 115
  - bySeenStopped: <1day 77、7days+ 38
  - byTarget の上位: 行き先なし(0)17、工場 3201 (2716,-1126) 2、15538 (2160,-1136) 2、27955 (2584,1169) 2、10927 (3640,-1170) 2、ほかは各1(48568 Shop01 (-1616,-1516) と工場4棟)
  - samples 30台のうち、港の敷地 (-2000,589) で WaitingSpace / InGrounds が16台。Goods は 39178 (528m)、44583 (1,051m)、44333 (1,357m、10.1日)行き。ほかは Coal、Lumber、Petrol、Food と、Oil Power Plant 7737 行きの Petrol 1台
  - samples の道の上の Blocked: (-916,-897) Food blockCounter 15・10.1日、(-630,92) Goods 40916行き 70、(-1342,-442) Lumber 69・20.1日、(-774,92) Goods 42762行き 27、(973,96) Goods 34964行き 23・10.1日、(-793,92) Coal 18、(-1968,124) Petrol 3・10.1日、(-1968,139) Goods 38204行き(残り208m)2・10.1日、(-1282,-424) Petrol 79・20.1日、(-1313,-441) Coal 72、(488,95) Petrol 17
  - 帰り(GoingBack)の Blocked: (-1956,416) 18・20.1日、(-1957,422) 27、(-1960,434) 29
- `buildings_near(x=-1115, z=-877, radius=500, problem="NoGoods", brief=true, limit=50)`
  - total 10(3回とも同じ10棟)。FatalProblem は 18547、21481、26357、26764、38627、42813 の6棟。MajorProblem は 9360、33087、35577。印が NoGoods だけは 20760
- `traffic(x=-877, z=-724, radius=300, limit=10)`
  - flow 54、cars 291、blocked 50(道の上50、建物の中0)、congestion 104、区間40、averageDensity 67
  - density 100 の区間: 15602 Basic Road (-1101,-560)、16866 (-920,-712)、11266 (-1060,-920)、15533 Basic Road (-954,-1010)、23469 Basic Road (-1070,-528)、32683 (-920,-808)、33761 Basic Road (-959,-560)、28337 Basic Road (-1031,-560)、30891 (-920,-942)、9066 (-920,-768)
  - blockedSpots: (-939,-725) 43、(-915,-807) 4、(-1006,-735) 2、(-1089,-563) 1
