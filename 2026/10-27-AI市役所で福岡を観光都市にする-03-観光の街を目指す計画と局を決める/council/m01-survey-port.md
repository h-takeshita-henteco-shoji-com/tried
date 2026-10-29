# m01 調査 s01-1(port): 貨物センター28755の止まったトラックの原因

(見回り2では、いつ見るかが「見回り1 / 月末」のため呼んでいない)

見立ては書かない。局が翌月に読んで決める。

## 2050-01-31(月末)

- `vehicles_stuck`(kind=truck, building=28755, limit=6): vehicles 602。byState は WaitingSpace+Importing+InGrounds 492、WaitingSpace+Importing+OnRoad 58、Importing+Spawned+OnRoad+Blocked 31、GoingBack+Importing+Spawned+OnRoad+Blocked 19、ほか2。bySeenStopped は <1day 111、7days+ 491。サンプル6台はすべて (3441,-1555) の敷地内で WaitingSpace、seenStoppedDays 10〜30(最長は見回り1の10日から30日に伸びた)、blockCounter 0
- `traffic`(x=3449, z=-1555, radius=300): flow 50、cars 42、blocked 0、congestion 4、averageDensity 42、roadSegments 23。最大密度は 28970(3440,-1340)と 17690(3480,-1315)の100。blockedSpots は空
- 参考(`cargo`): 28755 の敷地内で止まったトラック 492、stoppedInBuildings 493

## 2050-01-11(見回り1)

- `vehicles_stuck`(kind=truck, building=28755, limit=6): vehicles 602。byState は WaitingSpace+Importing+InGrounds 500、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 25、GoingBack+Importing+Spawned+OnRoad+Blocked 11、ほか2。bySeenStopped は <1day 138、7days+ 464。サンプル6台はすべて x=3441,z=-1555 の敷地内で WaitingSpace、seenStoppedDays 10(1台は0)、荷物は Goods 6000〜8000 と Coal 8000、blockCounter 0、waitCounter 0
- `traffic`(x=3449, z=-1555, radius=300): flow 51、cars 46、blocked 1、congestion 6、averageDensity 30、roadSegments 23。最大密度は segment 17690(3480,-1315)の98。blockedSpots は (3418,-1417) に1台
- 参考(`cargo`): 敷地内で止まったトラック 28755 が 500、stoppedInBuildings 518
