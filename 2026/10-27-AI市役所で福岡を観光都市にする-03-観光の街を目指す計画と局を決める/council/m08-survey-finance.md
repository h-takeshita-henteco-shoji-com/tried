# m08 調査 finance

## s08-3 ごみ収集車は道で止まっているか

### 2050-08-09(見回り1)

- 道具(1): `vehicles_stuck`(kind="garbage", limit=20)。返った数: vehicles 196。byState は Congestion を含むものが大半(Congestion+Spawned+OnRoad 57、Congestion+Spawned+OnRoad+Blocked 37、Congestion+GoingBack+...+Blocked 38、同 OnRoad 27 など)、Blocked のみ 16+13、WaitingSpace+OnRoad 7。bySeenStopped は <1day 188、7days+ 8。byTarget 上位は Combustion Plant 41481 へ12台。samples 20台の source は Landfill Site / Combustion Plant 各所(45436、3565、24569、43676、48698、40097、46633、41481、2267、31232)。blockCounter が高い車: 103(2027、(3146,-435))、75(1776、(2423,559))、50(1444、(-933,-736))、44(2198、(-1071,-576))、37(447、(-1089,-562))、14(926、(-1878,-831))
- 道具(2): `buildings_near`(x -580, z -1307, radius 300, problem "Garbage", brief=true, limit 30)。返った数: total 10。id 4444、5287、8116、12283、14569、16326、33792、34793、37577、48570(いずれも Tenement、x -724〜-370、z -1236〜-1484)

### 2050-08-29(月末)

- 道具(1): `vehicles_stuck`(kind="garbage", limit=5)。返った数: vehicles 151。bySeenStopped は <1day 108、7days+ 43。byState は Congestion を含むもの 122(Blocked 付き 54)、Blocked のみ 24、WaitingSpace+OnRoad 2。samples 5台の blockCounter は 149((2362,559)、source 45436)、77((2204,201)、source 3565)、48((-1821,-965)、source 24569)、18、4
- 道具(2): `buildings_near`(x -580, z -1307, radius 300, problem "Garbage", brief=true, limit 30)。返った数: total 0
- 参考(調査の外): `complaints` の Garbage は10(hotspot (2215,-185)、6棟。西の hotspot (-580,-1307) の棟は印なし)。新しい埋立地 14587 は 3% full、ごみ収集車 4 / 19
