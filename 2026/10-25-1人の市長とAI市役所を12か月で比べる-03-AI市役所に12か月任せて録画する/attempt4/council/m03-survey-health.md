# m03 調査 s03-2(health)の結果

問い: 死体の印66棟が、霊柩車の渋滞と偏りのどちらで続いているか。
見る道具: `buildings_near(x=2224, z=60, radius=400, service="HealthCare")`、`vehicles_stuck(kind="hearse", building=36841, limit=10)`、`complaints()` の Death。見回り1、見回り2、月末。

## 見回り1(2050-03-12)

- `buildings_near(2224,60,400,HealthCare)`
  - 21521 Medical Clinic (1918,262): Patients 23 / 100、treated last week 6、Ambulances 10 / 10
  - 23747 Crematory (2222,-255): stored 0 / 105、processed last week 3、Hearses 9 / 9
  - 31990 Crematory (2224,60): stored 3 / 105、processed last week 0、Hearses 6 / 9
  - 36841 Crematory (2218,286): stored 0 / 105、processed last week 0、Hearses 8 / 9
- `vehicles_stuck(kind="hearse", building=36841, limit=10)`
  - vehicles 7。byState: GoingBack+Spawned+OnRoad+Blocked 4、Spawned+OnRoad+Blocked 2、Congestion+Spawned+OnRoad+Blocked 1。byPath ready 7
  - bySeenStopped: <1day 2、7days+ 5
  - 帰り道(GoingBack、死体10を積む)の4台は (2204,203〜261)、(2227,244) で止まる。blockCounter 13〜56。車838 は 19.9日
  - 行き道の3台: 車2990 (2154,384) → 32913 (2113,814) まで432m、blockCounter 46。車4269 (2154,531) → 30354 まで422m、blockCounter 63、50日。車9424 (2025,239) → 42079 まで103m、blockCounter 10
- `complaints()` の Death: 58棟。hotspot (2306,27) に25棟。例 3083 (2086,36)、7470 (2444,-468)、7940 (2838,-276)、8420 (1655,-60)、17348 (2540,-926)

## 見回り2(2050-03-22)

- `buildings_near(2224,60,400,HealthCare)`
  - 21521 Medical Clinic: Patients 21 / 100、treated last week 4、Ambulances 10 / 10
  - 23747 Crematory: stored 1 / 105、processed last week 14、Hearses 8 / 9
  - 31990 Crematory: stored 0 / 105、processed last week 2、Hearses 6 / 9
  - 36841 Crematory: stored 14 / 105、processed last week 10、Hearses 4 / 9
- `vehicles_stuck(kind="hearse", building=36841, limit=10)`
  - vehicles 2。byState: Congestion+Spawned+OnRoad 1、Spawned+OnRoad+Blocked 1。byPath ready 2
  - bySeenStopped: <1day 1、7days+ 1
  - 車9424 (2065,239) → 42079 まで63m、blockCounter 67、30日
  - 車4269 (2341,1102) → 36801 まで324m、blockCounter 0、Congestion
  - 見回り1で帰り道に止まっていた4台(838、11038、12529、12722)は一覧にない
- `complaints()` の Death: 56棟。hotspot (2395,189) に21棟。例 980 (2335,716)、1876 (2168,495)、2188 (2613,908)、3083 (2086,36)、7297 (2619,306)

## 月末(2050-04-01)

- `buildings_near(2224,60,400,HealthCare)`
  - 21521 Medical Clinic: Patients 22 / 100、treated last week 2、Ambulances 10 / 10
  - 23747 Crematory: stored 4 / 105、processed last week 6、Hearses 8 / 9
  - 31990 Crematory: stored 0 / 105、processed last week 28、Hearses 4 / 9
  - 36841 Crematory: stored 0 / 105、processed last week 70、Hearses 5 / 9
- `vehicles_stuck(kind="hearse", building=36841, limit=10)`
  - vehicles 3。byState: Congestion+Spawned+OnRoad 1、Congestion+Spawned+OnRoad+Blocked 1、Spawned+OnRoad+Blocked 1。byPath ready 3
  - bySeenStopped: <1day 3(7days+ 0)
  - 車9424 (2114,271) → 37309 まで495m、blockCounter 53。車4269 (2249,1441) → 24066 まで1,186m、blockCounter 0。車12255 (2193,215) → 27674 まで66m、blockCounter 1
- `complaints()` の Death: 52棟。hotspot (3424,-449) に19棟。例 104 (3388,-24)、4069 (3376,-667)、4415 (3088,-596)、7584 (4192,-326)、8188 (3465,-354)
