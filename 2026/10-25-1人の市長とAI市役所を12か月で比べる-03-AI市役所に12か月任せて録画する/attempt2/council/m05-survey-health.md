# m05 調査の結果(health)

## s05-3 新しい埋立地37856 が溜まらない原因

問い: 37856 が30日で 1% しか溜まらないのは、車が渋滞で戻れないためか、回る範囲にごみが少ないためか。

### 2050-05-11(見回り1)

- `vehicles_stuck(kind="garbage", building=37856, limit=20)`: vehicles 16。byState は Congestion+Spawned+OnRoad+Blocked 7、Congestion+Spawned+OnRoad 3、Congestion+GoingBack+Spawned+OnRoad 3、Spawned+OnRoad+Blocked 2、Congestion+GoingBack+Spawned+InGrounds 1。byPath は ready 15、none 1。bySeenStopped は <1day 16。行き先は (2042, 764)、(-238, 436)、(2381, -546)、(3719, -596)、(1024, -1184)、(3394, 1336) など、37856 から 1.5〜6km 先の建物。samples の位置は (-668, 92)、(-340, -742)、(-919, -1206)、(196, 96)、(632, -710) など。行き先までの残りは 327〜5,006m。GoingBack の4台は積荷 20,000(満載)
- `buildings_near(x=-1862, z=-2000, radius=50, service="Garbage")`: 37856 Landfill Site、storage 108,309 / 8,000,000(1%)、"Garbage trucks in use: 19 / 19"、problems None
- `traffic(x=-1862, z=-2000, radius=300)`: flow 54、cars 60、blocked 0、congestion 10、roadSegments 31、averageDensity 23。密度の高い区間は 21070 Basic Road (-1998, -1930) 100、28495 Basic Road (-1820, -1725) 85、28506 Small 4 Lane Road (-1960, -1867) 85、21096 (-1960, -1822) 79、13543 (-1820, -1772) 75

### 2050-05-21(見回り2)

- `vehicles_stuck(kind="garbage", building=37856, limit=20)`: vehicles 13。byState は Congestion+Spawned+OnRoad 6、Congestion+GoingBack+Spawned+OnRoad+Blocked 3、Congestion+GoingBack+Spawned+OnRoad 2、Congestion+Spawned+OnRoad+Blocked 2。byPath は ready 13。bySeenStopped は <1day 4、7days+ 9。GoingBack の5台は積荷 20,000(満載)、位置 (-424, -1003)、(-274, -756)、(-274, -879)、(-317, -962)、(-1822, -1993)。行き先へ向かう8台の位置は (-11, 96)、(-916, -818)、(-916, -781)、(-575, 92)、(945, 96)、(-918, -1113)、(1424, -755)、(593, -711)、残りは 481〜4,819m。05-11 と同じ車(443、1162、4162、6837、7425、9936、15943、16080)が10日後も行き先へ向かう途中
- `buildings_near(x=-1862, z=-2000, radius=50, service="Garbage")`: 37856、storage 188,309 / 8,000,000(2%)、"Garbage trucks in use: 19 / 19"、workers 20、problems None
- `traffic(x=-1862, z=-2000, radius=300)`: flow 51、cars 50、blocked 0、congestion 6、roadSegments 31、averageDensity 20。密度の高い区間は 28506 (-1960, -1867) 92、21096 (-1960, -1822) 70、13543 (-1820, -1772) 55、28495 (-1820, -1725) 48、30177 (-1960, -1903) 46、21070 (-1998, -1930) 46

### 2050-05-31(月末)

- `vehicles_stuck(kind="garbage", building=37856, limit=20)`: vehicles 17。byState は Congestion+Spawned+OnRoad+Blocked 7、Congestion+GoingBack+Spawned+OnRoad 5、Congestion+Spawned+OnRoad 4、WaitingPath+Congestion+GoingBack+Spawned+OnRoad 1。byPath は ready 17。bySeenStopped は <1day 7、7days+ 10。行き先に Cargo Center 13893 (3529, -1555)(残り 4,497m)、Police Station 7532 (-20, -2142) が入った。GoingBack の6台は積荷 20,000、位置 (-577, -739)、(-921, -794)、(-836, -738)、(-627, -739)、(-148, 565)、(1975, 738)。行き先へ向かう車の位置は x -923〜2050。(-916〜-923, -838〜-1188) に6台が並ぶ。05-11 からの同じ車 443、1162、4162、9936、15943、16080 は seenStoppedDays 20 で、まだ行き先へ向かう途中(残り 990〜4,269m)
- `buildings_near(x=-1862, z=-2000, radius=50, service="Garbage")`: 37856、storage 208,309 / 8,000,000(2%)、"Garbage trucks in use: 19 / 19"、workers 20、problems None。05-01 から 05-31 の増えは 80,000 → 108,309 → 188,309 → 208,309
- `traffic(x=-1862, z=-2000, radius=300)`: flow 52、cars 54、blocked 0、congestion 4、roadSegments 31、averageDensity 19。密度の高い区間は 28506 (-1960, -1867) 81、21070 (-1998, -1930) 73、4201 (-2069, -1930) 58、30177 (-1960, -1903) 53、21096 (-1960, -1822) 42
