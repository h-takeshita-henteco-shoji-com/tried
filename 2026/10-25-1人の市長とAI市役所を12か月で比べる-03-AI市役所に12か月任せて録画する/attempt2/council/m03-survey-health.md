# m03 調査 s03-3(health)

問い: ごみの印が (-2126, -1842) に移ったのは、焼却場41481の収集車が回れないためか、受け入れ先が満ちたためか。

## 見回り1(2050-03-12)

- `vehicles_stuck(kind="garbage", building=41481, limit=20)`: vehicles 7。byState は Congestion+GoingBack+Spawned+OnRoad 3、Congestion+GoingBack+Spawned+OnRoad+Blocked 1、Congestion+Spawned+OnRoad 1、Congestion+Spawned+OnRoad+Blocked 1、Spawned+OnRoad+Blocked 1。byPath ready 7。bySeenStopped <1day 7。行き先は戻り(0)4台、47466 (-212,394) 1台、48829 (-2016,-2100) 1台、警察 8104 (-1700,490) 1台。位置は (-1641,-1411)、(-1086,11)、(-1818,76)、(-1496,-1369)、(-1087,-1279)、(-1816,-1208)、(-1265,-1549)。blockCounter は 13、17、56 の3台、ほか0
- `buildings_near(x=-1796, z=-1745, radius=300, service="Garbage")`: 4棟。焼却場41481 は reserves 392,500 / 400,000(98%)、処理 60,000 / 週、車 10 / 34。埋立地157 (-1860,-1880) は 99%(7,972,641 / 8,000,000)、車 2 / 19、印なし。埋立地23032 (-1860,-1650) は 100%、LandfillFull、車 0 / 19。埋立地29270 (-1780,-1880) は 100%、LandfillFull、車 0 / 19
- `complaints()`: 印のある建物337。Garbage 72(hotspot (-2171,-1882) に42棟。例 167、1263、2379、3745、8338)。ほか NoGoods 187、Death 39、Pollution 29、Noise 7、Crime 2、Water 2、Fire 1、Flood 1

## 見回り2(2050-03-22)

- `vehicles_stuck(kind="garbage", building=41481, limit=20)`: vehicles 7。byState は Congestion+GoingBack+Spawned+OnRoad 2、Congestion+GoingBack+Spawned+OnRoad+Blocked 1、Congestion+Spawned+OnRoad 1、Congestion+Spawned+OnRoad+Blocked 1、Spawned+OnRoad+Blocked 2。byPath ready 7。bySeenStopped <1day 3、7days+ 4。行き先は戻り(0)3台、42678 (-1064,-1484) 1台、27951 (3587,-554) 1台、48829 (-2016,-2100) 1台、47466 (-212,394) 1台。位置は (-1846,-699)、(-1665,182)、(-1961,-2023)、(-1660,-1102)、(-1736,-1458)、(-1667,-1462)、(-1738,-1282)。seenStoppedDays 10 が4台(1736、4293、6334、14637)。blockCounter は 47、10、44、12 の4台、ほか0。4293 は 48829 まで残り94m(見回り1は1,240m)
- `buildings_near(x=-1796, z=-1745, radius=300, service="Garbage")`: 4棟。焼却場41481 は reserves 383,750 / 400,000(95%)、処理 60,000 / 週、車 12 / 34。埋立地157 は 100%(8,000,000)、LandfillFull、車 0 / 19(見回り1は99%・車2)。埋立地23032・29270 は 100%、LandfillFull、車 0 / 19
- `complaints()`: 印のある建物345。Garbage 61(hotspot (-2193,-1802) に31棟。例 167、2379、3745、4464 (-998,-1076)、8338)。ほか NoGoods 204、Death 43、Pollution 32、Noise 3、Water 3、Crime 1、Fire 1

## 月末(2050-04-01)

- `vehicles_stuck(kind="garbage", building=41481, limit=20)`: vehicles 11。byState は Spawned+OnRoad+Blocked 4、Congestion+GoingBack+Spawned+OnRoad 2、Congestion+Spawned+OnRoad+Blocked 2、GoingBack+Spawned+OnRoad+Blocked 2、Congestion+Spawned+OnRoad 1。byPath ready 11。bySeenStopped <1day 7、7days+ 4。行き先は戻り(0)4台、ほか 32317 (1241,-1236)、46823 (319,-1836)、27951 (3587,-554)、44687 (-212,346)、48874 (-2336,-512)、3577 (3108,-1316)、47466 (-212,394) が1台ずつ。位置は (-1822,-1689)、(-1846,-683)、(-1816,-1268)、(-1819,-1387)、(-1223,-442)、(-1817,-1295)、(-1638,-1526)、(-916,-905)、(-1846,-706)、(-1816,-1255)、(-1668,-1282)。x≈-1816〜-1819、z≈-1255〜-1387 に4台(blockCounter 46、23、46、57)。seenStoppedDays 20 が2台(1736、6334)、10 が2台(2350、16230)
- `buildings_near(x=-1796, z=-1745, radius=300, service="Garbage")`: 4棟。焼却場41481 は reserves 396,250 / 400,000(99%)、処理 60,000 / 週、車 16 / 34。埋立地157・23032・29270 は3つとも 100%、LandfillFull、車 0 / 19
- `complaints()`: 印のある建物389。Garbage 74(hotspot (-2430,-1807) に26棟。例 167、1076 Medical Clinic (-1350,-1620)、2379、3745、8338)。ほか NoGoods 222、Death 45、Pollution 41、Noise 5、Water 3、Fire 1、NoEducatedWorkers 1、Crime 1
- 3回の推移: ごみの印 72 → 61 → 74。41481 の reserves 98% → 95% → 99%、車 10 → 12 → 16 / 34。埋立地157 は 99% → 100% → 100%(この円の3つの埋立地が全部満杯になった)。41481 の車のうち Blocked を含む状態 4 → 4 → 8
