# m10 調査 health

## s10-2 死体の印の原因

### 2050-10-18(見回り1)

- `buildings_near`(x 2213, z -139, radius 300, problem Death, brief, limit 40): total 1(id 3083、H5 4x4 Highrise07、(2086,36))
- `vehicles_stuck`(kind hearse, limit 10): 116台。Congestion を含む状態が多数(Congestion+Spawned+OnRoad+Blocked 28、Spawned+OnRoad+Blocked 26 など)。byPath none 10、ready 106。bySeenStopped: <1day 108、7days+ 8。サンプルの出どころは火葬場・墓地(Crematory 29774、46000、46144、11163、39843、12290、2762、Cemetery 16836、30856)。3146,-402 付近で49.9日止まった車1台
- `services`: deathcare capacity 24,000、used 13,949、full 0。healthcare capacity 5,100、used 1,215
- 参考(`complaints`): Death 37棟、hotspot (2267,-92.7) の15棟

### 2050-10-28(見回り2)

- `buildings_near`(x 2213, z -139, radius 300, problem Death, brief, limit 40): total 0
- `vehicles_stuck`(kind hearse, limit 3): 121台。bySeenStopped: <1day 86、7days+ 35。byPath none 9、ready 112。Congestion を含む状態が多い(Congestion+Spawned+OnRoad 33、+Blocked 27)。サンプルは Crematory 31839、Cemetery 16836、Crematory 46144
- `services`: deathcare capacity 24,000、used 13,989、full 0
- 参考(`complaints`): Death 28棟、hotspot (2199.7,-71.3) の11棟(10/18 は37棟)

### 2050-11-07(月末)

- `buildings_near`(x 2213, z -139, radius 300, problem Death, brief, limit 40): total 0
- `services`: deathcare capacity 24,000、used 14,019、full 0
- 参考(`complaints`): Death 34棟、hotspot (2325.4,-175.9) の13棟。`vehicles_stuck` hearse は月末は呼んでいない(調査の引数は見回り時点)
