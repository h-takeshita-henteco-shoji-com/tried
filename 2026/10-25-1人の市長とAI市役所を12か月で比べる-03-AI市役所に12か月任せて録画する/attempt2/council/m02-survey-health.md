# m02 調査の結果(health)

## s02-1 埋立地の中身を運ぶ車が空にならない原因

問い: 満杯の埋立地の中身を運ぶ車が、遠い焼却場へ渋滞の中を向かい、いつまでも空にならないのは、行き先の遠さと道の詰まりのどちらが原因か。

前提: 2050-01-31 の実行で、m02-2 により 16914 を `empty_building(active=False)` で受け入れに戻した。直後は problems None、stats "Garbage trucks in use: 0 / 19"、95%。

### 見回り1(2050-02-10)

- `vehicles_stuck(kind="garbage", building=16914, limit=20)`
  - vehicles 24。byPath ready 24
  - byState: Congestion+GoingBack+Spawned+OnRoad+Blocked 5、Congestion+Spawned+OnRoad 7、Congestion+Spawned+OnRoad+Blocked 6、GoingBack+Spawned+OnRoad+Blocked 1、Spawned+OnRoad+Blocked 5
  - bySeenStopped: <1day 10、7days+ 14
  - byTarget: 行き先なし(building 0、戻る途中)6、焼却場31232 (3613, -1365) 6、焼却場33797 (-570, -1840) 4、焼却場41481 (-1796, -1745) 1、焼却場10351 (2070, 866) 1、住宅への収集 6(46244、15344、30938、38383、361 など各1)
  - samples の荷: GarbageMove(空ける荷)の車は行き先まで 141〜5,414m。31232 行きは 4,910〜5,414m、33797 行きは 1,268〜1,289m。止まった位置は (-1818〜-1639, -1619〜-1282) に多い。blockCounter は 0〜49
  - samples の荷: Garbage(収集)の車 5台は amount 464〜4,185、行き先の住宅まで 856〜1,877m。位置 (-1377〜-772, -747〜-523)
- `buildings_near(x=-650, z=-490, radius=50, service="Garbage")`
  - 16914: problems None、storage 7,640,000 / 8,000,000(95%)、stats "Garbage trucks in use: 17 / 19"、vehicles.inUse 36
- `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`
  - 33797 Combustion Plant: storage 343,750 / 400,000(85%)、処理 60,000 / 週、車 29 / 34、problems None

### 見回り2(2050-02-20)

- `vehicles_stuck(kind="garbage", building=16914, limit=20)`
  - vehicles 21。byPath ready 21
  - byState: Congestion+GoingBack+Spawned+OnRoad 3、Congestion+GoingBack+Spawned+OnRoad+Blocked 3、Congestion+Spawned+OnRoad 8、Congestion+Spawned+OnRoad+Blocked 6、Spawned+OnRoad+Blocked 1
  - bySeenStopped: <1day 5、7days+ 16
  - byTarget: 焼却場31232 (3613, -1365) 6、行き先なし(戻る途中)6、焼却場33797 (-570, -1840) 4、焼却場10351 (2070, 866) 1、住宅への収集 4(361、8496、45485、23325 各1)
  - samples の荷: GarbageMove の車は seenStoppedDays 19.9 のものが多い(775、1778、1831、2970、3134、5415、7414、11392、14010、15443、15501)。31232 行きの残り距離は 4,091〜5,280m(見回り1は 4,910〜5,414m)。33797 行きは 682〜1,158m(見回り1は 1,268〜1,289m)。10351 行き(775)は 4,339m(見回り1は 4,574m)
  - 止まった位置は (-1666〜-1638, -1394〜-1261) と、(-659〜-431, -748〜-730) に多い。blockCounter は 0〜78
- `buildings_near(x=-650, z=-490, radius=50, service="Garbage")`
  - 16914: problems None、storage 7,676,250 / 8,000,000(95%)、stats "Garbage trucks in use: 17 / 19"、vehicles.inUse 34
- `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`
  - 33797 Combustion Plant: storage 400,000 / 400,000(100%)、処理 60,000 / 週、車 30 / 34、problems Death

### 月末(2050-03-02)

- `vehicles_stuck(kind="garbage", building=16914, limit=20)`
  - vehicles 22。byPath ready 22
  - byState: Congestion+GoingBack+Spawned+OnRoad 3、Congestion+GoingBack+Spawned+OnRoad+Blocked 4、Congestion+Spawned+OnRoad 7、Congestion+Spawned+OnRoad+Blocked 7、GoingBack+Spawned+OnRoad+Blocked 1
  - bySeenStopped: <1day 4、7days+ 18
  - byTarget: 行き先なし(戻る途中)8、焼却場31232 (3613, -1365) 6、焼却場33797 (-570, -1840) 4、焼却場10351 (2070, 866) 1、収集 3(23325、7673、45485 各1)
  - samples の荷: GarbageMove の車で seenStoppedDays 30 のもの 775、1778、1831、3134、5415、7414、11392、14010、15443
  - 31232 行きの残り距離: 1831 は 3,473m(見回り2 4,316m、見回り1 4,910m)、7414 は 4,058m(4,548m、5,252m)、11392 は 5,087m(5,280m、5,414m)、10634 は 2,612m(4,091m)
  - 33797 行きの残り距離: 5415 は 1,093m(791m、1,289m)、14010 は 1,099m(682m、1,279m)、15443 は 682m(1,095m、-)、6970 は 1,138m(1,158m、1,268m)
  - 10351 行き(775)は 4,191m(4,339m、4,574m)
  - 戻る途中で荷 20,000 を積んだ収集の車(Garbage)が 4477、7883、14208 の3台
  - 止まった位置は (-1656〜-1461, -1102〜-884) と、(-613〜-397, -748〜-744) に多い
- `buildings_near(x=-650, z=-490, radius=50, service="Garbage")`
  - 16914: problems None、storage 7,696,250 / 8,000,000(96%)、stats "Garbage trucks in use: 16 / 19"、vehicles.inUse 32
- `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`
  - 33797 Combustion Plant: storage 366,250 / 400,000(91%)、処理 60,000 / 週、車 28 / 34、problems None
