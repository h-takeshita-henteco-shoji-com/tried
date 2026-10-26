# m02 調査 s02-2(health): 死体の印が火葬場の近くで出る理由

問い: 火葬場が近くにあるのに死体の印が出るのは、霊柩車が遠い家へ回されて渋滞に捕まるためか

m02-2(交差点 (2110,330) の信号)は 2050-01-31 に実行済み。

## 見回り1(2050-02-10)

### `buildings_near(x=2224, z=60, radius=400, service="HealthCare")`

- total 4
- 23747 Crematory (2222,-255): Deceased stored 1 / 105、processed last week 0、Hearses in use 9 / 9、働き手26
- 31990 Crematory (2224,60): Deceased stored 1 / 105、processed last week 32、Hearses in use 6 / 9、働き手29
- 36841 Crematory (2218,286): Deceased stored 0 / 105、processed last week 0、Hearses in use 7 / 9、働き手30
- 21521 Medical Clinic (1918,262): Patients 23 / 100、Ambulances 10 / 10

### `vehicles_stuck(kind="hearse", building=31990, limit=10)`

- vehicles 2。byState: Spawned+OnRoad+Blocked 1、WaitingTarget+Congestion+Stopped+Spawned+InGrounds 1
- byPath: ready 1、none 1。bySeenStopped: <1day 2
- vehicle 5755 (2114,127) blockCounter 36、行き先 19588 (2126,142) まで19m、Dead 9
- vehicle 7791 (2349,66) 行き先なし、waitCounter 12、Dead 6

### `vehicles_stuck(kind="hearse", building=36841, limit=10)`

- vehicles 5。byState: Spawned+OnRoad+Blocked 4、Congestion+Spawned+OnRoad+Blocked 1
- byPath: ready 5。bySeenStopped: <1day 2、7days+ 3
- vehicle 1526 (2062,149) blockCounter 84、行き先 11280 (2046,354) まで206m、seen 10日
- vehicle 4269 (1905,328) blockCounter 129、行き先 30354 (2533,716) まで738m、seen 20日
- vehicle 11038 (2205,277) blockCounter 27、行き先 21301 (2094,81) まで225m、seen 10日
- vehicle 12529 (2205,255) blockCounter 22、行き先 33137 (2054,264) まで151m
- vehicle 12722 (2042,148) blockCounter 83、行き先 17474 (2164,318) まで209m

### `complaints()` の Death

- Death 75棟(前回の月例 56)。hotspot (3348.5,-332.4) 21棟
- examples: 104 (3388,-24)、3825 (3416,-635)、4415 (3088,-596)、6747 (2999,126)、7370 (3356,-840)

## 見回り2(2050-02-20)

### `buildings_near(x=2224, z=60, radius=400, service="HealthCare")`

- total 4
- 23747 Crematory (2222,-255): Deceased stored 3 / 105、processed last week 10、Hearses in use 8 / 9
- 31990 Crematory (2224,60): Deceased stored 0 / 105、processed last week 20、Hearses in use 5 / 9
- 36841 Crematory (2218,286): Deceased stored 0 / 105、processed last week 0、Hearses in use 7 / 9
- 21521 Medical Clinic (1918,262): Patients 22 / 100、Ambulances 10 / 10

### `vehicles_stuck(kind="hearse", building=31990, limit=10)`

- vehicles 3。byState: Congestion+Spawned+OnRoad 1、Spawned+OnRoad+Blocked 1、Stopped+Spawned+OnRoad 1
- byPath: ready 3。bySeenStopped: <1day 3
- vehicle 7791 (2083,-571) Congestion、行き先 17348 (2540,-926) まで579m、Dead 8
- vehicle 7921 (2108,-827) blockCounter 66、行き先 14243 (2176,-628) まで210m
- vehicle 10062 (2054,-204) Stopped、行き先 44723 (2283,36) まで332m

### `vehicles_stuck(kind="hearse", building=36841, limit=10)`

- vehicles 6。byState: Spawned+OnRoad+Blocked 3、Congestion+Spawned+OnRoad 1、Stopped+GoingBack+Spawned+OnRoad 1、WaitingTarget+Stopped+Spawned+InGrounds 1
- byPath: ready 5、none 1。bySeenStopped: <1day 4、7days+ 2
- vehicle 1526 (1879,262) blockCounter 125、行き先 28248 (1973,-96) まで370m
- vehicle 4269 (2075,329) Congestion、行き先 30354 (2533,716) まで599m、seen 30.1日
- vehicle 9424 (1879,255) blockCounter 128、行き先 42079 (2126,257) まで247m
- vehicle 11038 (2104,81) WaitingTarget、path none、Dead 5
- vehicle 12722 (2114,175) blockCounter 2、行き先 17474 (2164,318) まで152m、seen 10日
- vehicle 838 (2278,-126) GoingBack、Dead 10

### `complaints()` の Death

- Death 66棟。hotspot (2166,92.1) 21棟
- examples: 101 (1376.8,261.7)、754 (1494,456.1)、1551 (1477.4,430.6)、3083 (2086,36)、8420 Expensive Park (1655,-60)

## 月末(2050-03-02)

### `buildings_near(x=2224, z=60, radius=400, service="HealthCare")`

- total 4
- 23747 Crematory (2222,-255): Deceased stored 0 / 105、processed last week 27、Hearses in use 7 / 9
- 31990 Crematory (2224,60): Deceased stored 0 / 105、processed last week 0、Hearses in use 7 / 9
- 36841 Crematory (2218,286): Deceased stored 0 / 105、processed last week 0、Hearses in use 8 / 9
- 21521 Medical Clinic (1918,262): Patients 22 / 100、Ambulances 10 / 10

### `vehicles_stuck(kind="hearse", building=31990, limit=10)`

- vehicles 3。byState: WaitingTarget+Stopped+Spawned+InGrounds 1、Congestion+Spawned+OnRoad+Blocked 1、Spawned+OnRoad+Blocked 1
- byPath: ready 2、none 1。bySeenStopped: <1day 2、7days+ 1
- vehicle 5034 (2404,-36) WaitingTarget、path none、waitCounter 8、Dead 1
- vehicle 7791 (2155,-928) blockCounter 47、行き先 17348 (2540,-926) まで385m、seen 10日、Dead 8
- vehicle 7921 (2180,-836) blockCounter 3、行き先 18938 (2134,-443) まで396m

### `vehicles_stuck(kind="hearse", building=36841, limit=10)`

- vehicles 6。byState: GoingBack+Spawned+OnRoad+Blocked 2、Spawned+OnRoad+Blocked 2、Congestion+Spawned+OnRoad+Blocked 1、WaitingSpace+OnRoad 1
- byPath: ready 6。bySeenStopped: <1day 3、7days+ 3
- vehicle 838 (2205,197) GoingBack blockCounter 14、Dead 10、seen 10日
- vehicle 2990 (2204,286) WaitingSpace、行き先 32913 (2113,814) まで536m
- vehicle 4269 (2153,421) blockCounter 11、行き先 30354 (2533,716) まで481m、seen 40.1日
- vehicle 9424 (1972,239) blockCounter 17、行き先 42079 (2126,257) まで155m、seen 10日
- vehicle 11038 (2231,244) blockCounter 21、行き先 27670 (2404,306) まで183m
- vehicle 12529 (2204,191) GoingBack blockCounter 4、Dead 10

### `complaints()` の Death

- Death 66棟。hotspot (2165.2,-69.5) 25棟
- examples: 101 (1376.8,261.7)、754 (1494,456.1)、1551 (1477.4,430.6)、3083 (2086,36)、8420 Expensive Park (1655,-60)
