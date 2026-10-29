# m02 調査 s02-2(health)西のごみ収集車

注記: m02-1(西の埋立地の新設)は実行されていない(下の市政ノート参照)。以下は埋立地なしの状態の記録。

## 2050-02-11 見回り1

- `vehicles_stuck`(kind="garbage", building=33797, limit=10): vehicles 10。byState は Congestion+GoingBack 3、Congestion 4、Congestion+Blocked 1、Blocked 2。bySeenStopped は 7日以上 7、1日未満 3。byPath は ready 10。積荷は GarbageMove(埋立地23032→焼却33797へ移送、amount 20000)が4台、Garbage が6台。blockCounter が大きいのは車7328(34、(-274,-893))と車15610(22、(-924,-875))。
- `traffic`(x=-531, z=-1280, radius=500): flow 54、cars 209、blocked 31、congestion 90、averageDensity 22。density 100 の Basic Road が (-920,-1226)、(-920,-988)、(-920,-1264)、(-961,-1190)、(-275,-871) など。blockedSpots は (-948,-1293) 12台、(-273,-898) 11台、(-972,-1168) 4台、(-1012,-1191) 4台。
- `buildings_near`(x=-531, z=-1280, radius=600, problem="Garbage", brief=true, limit=30): total 4。1420 (-652,-1336)、20830 (-969,-1124、MajorProblem)、21271 (-973,-1076)、21897 (-354.5,-1384)。基準は 14 棟。

## 2050-02-21 見回り2

- `vehicles_stuck`(kind="garbage", building=33797, limit=10): vehicles 10。Congestion 7(うち Blocked 2)、Blocked のみ 2、Congestion+GoingBack+Blocked 1 など。7日以上止まり 6、1日未満 4。積荷は GarbageMove 3台(23032→33797)、Garbage 7台。(-274,-817)(-274,-880) で blockCounter 28 と 16。
- `traffic`(x=-531, z=-1280, radius=500): flow 52、cars 181、blocked 0、congestion 72、averageDensity 19。density 100 の Basic Road は (-275,-988)(-275,-921)(-920,-1036)(-275,-871)(-961,-1190) など。blockedSpots なし。
- `buildings_near`(x=-531, z=-1280, radius=600, problem="Garbage", brief=true, limit=30): total 3。21897 (-354.5,-1384)、44151 Police Station (-200,-1480)、44697 (-1036,-1484)。

## 2050-03-03 月末

- `vehicles_stuck`(kind="garbage", building=33797, limit=10): vehicles 7。Congestion 4、Blocked のみ 2、GoingBack+Blocked 1。7日以上止まり 3、1日未満 4。積荷はすべて Garbage(GarbageMove なし)。(-619,-739) の車1954 は blockCounter 25。
- `traffic`(x=-531, z=-1280, radius=500): flow 54、cars 146、blocked 0、congestion 48、averageDensity 17。density 100 は (-920,-988)(-961,-1190)(-275,-871)(-920,-1036)。blockedSpots なし。
- `buildings_near`(x=-531, z=-1280, radius=600, problem="Garbage", brief=true, limit=30): total 0(基準 14、見回り2は 3)。
- 参考 `complaints`: Garbage 14 棟(hotspot (1246,-1111) 4棟。西の範囲の外)。
