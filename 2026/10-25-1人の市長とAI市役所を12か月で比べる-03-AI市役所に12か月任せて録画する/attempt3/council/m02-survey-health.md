# s02-2 焼却場33797 の収集車は、南西の印の家に向かっているか(health)

問い: 焼却場33797 の収集車が、南西のごみの印の家(-724〜-350,-1236〜-1446)に行かず遠い家へ向かっているのか。それとも向かっても渋滞で着かないのか。

## 見回り1(2050-02-10)

- `vehicles_stuck(kind="garbage", building=33797, limit=40)`: vehicles 10。Spawned+OnRoad+Blocked 6、Congestion+Spawned+OnRoad 3、GoingBack+Spawned+OnRoad+Blocked 1。bySeenStopped <1day 8、7days+ 2。行き先は 44943(-1476,540)、31509(-2270,-610)、6822(-998,-986)、2379(-2564,-2046)、14170(-1424,-626)、37564(1053,-1184)、29901(-2161,-2190)、20830(-969,-1124)、1103(-2076,-2100)、なし1。止まった位置は x -274(z -825〜-995)に4台、z -738〜-739(x -556〜-727)に4台、-1596,108 と -1961,-780 に各1台。行き先が南西の印の範囲(-724〜-350,-1236〜-1446)に入る車は0台
- `buildings_near(x=-540, z=-1340, radius=400, problem="Garbage", brief=true)`: total 4。2031(-676,-1426)、21897(-354.5,-1384)、28554(-724,-1446)、39450(-595,-1046)
- `traffic(x=-550, z=-1600, radius=400)`: flow 55、cars 60、blocked 0、congestion 13、averageDensity 13。busiest は x -425 の Basic Road の列(13870 が -425,-1372 で density 90、34049 が -1242 で59、18471 が -1285 で44)。blockedSpots なし

## 見回り2(2050-02-20)

- `vehicles_stuck(kind="garbage", building=33797, limit=40)`: vehicles 11。Congestion+Spawned+OnRoad 4、Spawned+OnRoad+Blocked 3、Congestion+GoingBack+Spawned+OnRoad+Blocked 2、Congestion+GoingBack+Spawned+OnRoad 1、WaitingTarget+Spawned+InGrounds 1(path none、337,-1062)。bySeenStopped <1day 7、7days+ 4。行き先は 17658(-2141,-2140)、2379(-2564,-2046)、15222(-1048,-1436)、37564(1053,-1184)、18125(-2016,-2140)、44566(-2432,-806)、29901(-2161,-2190)、なし4。行き先が南西の印の範囲(-724〜-350,-1236〜-1446)に入る車は0台。止まった位置は -590,-739、538,-713、-1077,-1006、-944,-919、-1023,-1012、-274,-764、-340,-1360、-1058,-923、-921,-1222、-1821,-978
- `buildings_near(x=-540, z=-1340, radius=400, problem="Garbage", brief=true)`: total 2。38642 Fire House(-200,-1380)、44151 Police Station(-200,-1480)。見回り1の4棟(2031、21897、28554、39450)は出ていない
- `traffic(x=-550, z=-1600, radius=400)`: flow 52、cars 41、blocked 0、congestion 14、averageDensity 10。busiest は 13870(-425,-1372)が density 100、34049(-425,-1242)が49、4664(-425,-1448)が47。blockedSpots なし

## 月末(2050-03-02)

- `vehicles_stuck(kind="garbage", building=33797, limit=40)`: vehicles 12。Congestion+GoingBack+Spawned+OnRoad+Blocked 5、Spawned+OnRoad+Blocked 3、GoingBack+Spawned+OnRoad+Blocked 2、Congestion+GoingBack+Spawned+OnRoad 1、Congestion+Spawned+OnRoad 1。bySeenStopped <1day 6、7days+ 6。行き先なし(戻る途中、積み荷20000)が8台。行き先ありは 31509(-2270,-610)、15222(-1048,-1436)、18125(-2016,-2140)、17658(-2141,-2140)。行き先が南西の印の範囲(-724〜-350,-1236〜-1446)に入る車は0台。止まった位置は -938,-1188、-1819,-1816、-940,-921、-700,-748、-767,-738、-1809,-1008、-1071,-617、-1071,-609、-426,-736、-352,-743、-916,-787、-1685,-1012
- `buildings_near(x=-540, z=-1340, radius=400, problem="Garbage", brief=true)`: total 2。34793 H4 3x2 tenement07(-370.5,-1484)、44151 Police Station(-200,-1480)
- `traffic(x=-550, z=-1600, radius=400)`: flow 53、cars 46、blocked 0、congestion 9、averageDensity 9。busiest は 13870(-425,-1372)が density 91、34049(-425,-1242)が54、18468(-425,-1578)が37。blockedSpots なし
