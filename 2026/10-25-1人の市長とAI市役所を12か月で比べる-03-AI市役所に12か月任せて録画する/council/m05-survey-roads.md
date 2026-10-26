# m05 調査の結果(roads)

## s05-3 交差点のない Large Road (-710,-737) が詰まる理由

問い: Large Road の (-710,-737) で、交差点がないのに blocked 47 が続くのは、何で詰まっているのか。

### 見回り1(2050-05-11)

- `traffic(x=-710, z=-737, radius=80)`
  - flow 53、cars 44、blocked 9、congestion 15、roadSegments 2、averageDensity 60
  - busiest: 10922 Large Road (-759,-740) density 64、6545 Large Road (-685,-740) density 57
  - blockedSpots: (-763,-738) 9台
- `buildings_near(x=-710, z=-737, radius=120, problems_only=True, brief=True)`
  - total 1: 32297 H4 2x2 Tenement09 (-680,-708) Noise
- `vehicles_stuck(kind="truck", limit=15)`
  - vehicles 1,197
  - byState の主なもの: WaitingSpace+Importing+InGrounds 489、Importing+InGrounds 344、Spawned+OnRoad+Blocked 105、Importing+Spawned+OnRoad+Blocked 101、WaitingSpace+Importing+OnRoad 61、GoingBack+Spawned+OnRoad+Blocked 40、GoingBack+Importing+Spawned+OnRoad+Blocked 37
  - byPath: ready 1,183、none 14
  - bySeenStopped: <1day 491、7days+ 706
  - samples 15台: 28755 の (3441,-1555) が6台、地図の外のつなぎ口 (-4030,8619) が6台・(6993,-8619) が2台(Importing+InGrounds)、港46112 の (-2485,313) が1台。(-710,-737) の近くの車は samples にない

### 見回り2(2050-05-21)

- `traffic(x=-710, z=-737, radius=80)`
  - flow 52、cars 71、blocked 0、congestion 7、roadSegments 2、averageDensity 84
  - busiest: 10922 Large Road (-759,-740) density 92、6545 Large Road (-685,-740) density 76
  - blockedSpots: なし
- `buildings_near(x=-710, z=-737, radius=120, problems_only=True, brief=True)`
  - total 1: 30692 H4 3x4 tenement05a (-766,-708) Death
- `vehicles_stuck(kind="truck", limit=15)`
  - vehicles 1,213
  - byState の主なもの: WaitingSpace+Importing+InGrounds 511、Importing+InGrounds 345、Spawned+OnRoad+Blocked 112、Importing+Spawned+OnRoad+Blocked 81、WaitingSpace+Importing+OnRoad 64、GoingBack+Spawned+OnRoad+Blocked 46、GoingBack+Importing+Spawned+OnRoad+Blocked 28
  - byPath: ready 1,196、none 17
  - bySeenStopped: <1day 511、7days+ 702
  - samples 15台: 地図の外のつなぎ口(-4030,8619 など)7台、28755 の (3441,-1555) 5台、港1366 発の2台が (-1969,132)・(-1968,146) で Blocked(blockCounter 28・26)、工場11659 発の1台が (2761,-1025) で Blocked。(-710,-737) の近くの車は samples にない

### 月末(2050-05-31)

- `traffic(x=-710, z=-737, radius=80)`
  - flow 53、cars 43、blocked 0、congestion 14、roadSegments 2、averageDensity 80
  - busiest: 10922 Large Road (-759,-740) density 95、6545 Large Road (-685,-740) density 65
  - blockedSpots: なし
- `buildings_near(x=-710, z=-737, radius=120, problems_only=True, brief=True)`
  - total 2: 16156 H4 3x2 tenement07 (-708,-768) Death、49103 H4 4x4 Tenement09a (-704,-708) Death
- `vehicles_stuck(kind="truck", limit=15)`
  - vehicles 1,228
  - byState の主なもの: WaitingSpace+Importing+InGrounds 514、Importing+InGrounds 359、Spawned+OnRoad+Blocked 125、Importing+Spawned+OnRoad+Blocked 91、WaitingSpace+Importing+OnRoad 66、GoingBack+Spawned+OnRoad+Blocked 36、GoingBack+Importing+Spawned+OnRoad+Blocked 20
  - byPath: ready 1,216、none 12
  - bySeenStopped: <1day 528、7days+ 700
  - samples 15台: 28755 の (3441,-1555) 6台、地図の外のつなぎ口 5台、Blocked の4台は (2207,-1052)(工場1645 発、blockCounter 18)、(-1910,-438)(港1366 発、15)、(2640,-946)(工場11659 発、37)、(1898,1151)(工場22635 発、23)。(-710,-737) の近くの車は samples にない
