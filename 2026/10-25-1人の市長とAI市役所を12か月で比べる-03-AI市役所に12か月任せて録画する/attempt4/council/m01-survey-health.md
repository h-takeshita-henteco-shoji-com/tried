# m01 調査 s01-2(health): 死体の印が52棟に出る理由

問い: 墓地の容量は半分なのに、死体の印が52棟に出る理由は、霊柩車の不足か道の詰まりか

## 見回り1(2050-01-11)

### `buildings_near(x=2240, z=186, radius=600, service="DeathCare", limit=20)`

- total 0(半径600mの中に DeathCare の建物なし)

### `vehicles_stuck(kind="hearse", limit=30)`

- vehicles 186
- byState: Congestion+Spawned+OnRoad+Blocked 58、Spawned+OnRoad+Blocked 47、Congestion+Spawned+OnRoad 35、Stopped+Spawned+OnRoad 16、Congestion+GoingBack+Spawned+OnRoad 6、Spawned+InGrounds 5、Congestion+GoingBack+Spawned+OnRoad+Blocked 4、Congestion+Stopped+Spawned+OnRoad 3、Stopped+GoingBack+Spawned+OnRoad 3、GoingBack+Spawned+OnRoad+Blocked 2、Congestion+Stopped+GoingBack+Spawned+OnRoad 2、WaitingTarget+Stopped+Spawned+InGrounds 2、WaitingTarget+Congestion+Stopped+Spawned+InGrounds 2、Congestion+Spawned+InGrounds 1
- Congestion の印のある車の合計 111、Blocked の印のある車の合計 111
- byPath: ready 176、none 10
- bySeenStopped: <1day 186(初めて呼んだため)
- byTarget: building 0(行き先なし)21台。ほかは1台ずつ
- samples(30台): 出発は Crematory と Cemetery のさまざまな建物(31990、18954、21324、39843、21962、41597、31667、11163、19894、1641、17188、12290、46144、4748、43145、2762、14375、7315、4270、9364、36841、16836、15611、23747)。行き先までの距離は 19〜995m。blockCounter が大きい例: 506 (3183,-78) 126、1124 (-1933,-1805) 92、1526 (1950,149) 46

### `complaints()`

- buildingsWithProblems 356
- Death 55(hotspot (2173, 94.5) の区画に28棟)
- Pollution 36、NoGoods 237、Noise 11、Fire 5、Garbage 9、LandValueLow 1、Crime 2、Water 1

## 見回り2(2050-01-21)

### `buildings_near(x=2240, z=186, radius=600, service="DeathCare", limit=20)`

- total 0

### `vehicles_stuck(kind="hearse", limit=30)`

- vehicles 182
- byState: Congestion+Spawned+OnRoad+Blocked 56、Congestion+Spawned+OnRoad 42、Spawned+OnRoad+Blocked 39、Stopped+Spawned+OnRoad 19、Congestion+GoingBack+Spawned+OnRoad 8、Congestion+GoingBack+Spawned+OnRoad+Blocked 5、Congestion+Stopped+Spawned+OnRoad 3、Congestion+Spawned+InGrounds 2、WaitingSpace+OnRoad 2、ほか1台ずつ5種
- Congestion の印のある車の合計 117、Blocked の印のある車の合計 102
- byPath: ready 177、none 5
- bySeenStopped: <1day 114、7days+ 68
- byTarget: building 0 18台。ほかは1台ずつ
- samples: blockCounter が大きい例: 1055 (-1458,-664) 57、1080 (2761,-1003) 56、1737 (-1818,-1302) 47、289 (3163,-343) 45、1109 (-845,-738) 44。1888 は (2326,-946) で Blocked(blockCounter 36)。行き先までの距離は 15〜919m

### `complaints()`

- buildingsWithProblems 349
- Death 53(hotspot (2233.4, 41.4) の区画に20棟)
- Crime 5、Pollution 35、NoGoods 235、Noise 7、Fire 5、Garbage 7、Flood 2、LandValueLow 1、Water 1

## 月末(2050-01-31)

### `buildings_near(x=2240, z=186, radius=600, service="DeathCare", limit=20)`

- total 0

### `vehicles_stuck(kind="hearse", limit=30)`

- vehicles 204
- byState: Congestion+Spawned+OnRoad 54、Congestion+Spawned+OnRoad+Blocked 54、Spawned+OnRoad+Blocked 46、Stopped+Spawned+OnRoad 19、Congestion+GoingBack+Spawned+OnRoad 9、Congestion+GoingBack+Spawned+OnRoad+Blocked 8、Congestion+Stopped+Spawned+OnRoad 5、Spawned+InGrounds 4、Congestion+Spawned+InGrounds 2、ほか1台ずつ3種
- Congestion の印のある車の合計 132、Blocked の印のある車の合計 110
- byPath: ready 197、none 7
- bySeenStopped: <1day 142、7days+ 62
- byTarget: building 0 19台。ほかは1台ずつ
- samples: blockCounter が大きい例: 1526 (2020,149) 51、824 (2761,-1003) 47、1650 (2854,-492) 45、1233 (-924,-776) 44、1141 (474,-706) 37。行き先までの距離は 18〜1,429m

### `complaints()`

- buildingsWithProblems 347
- Death 56(hotspot (2189.9, 27.2) の区画に18棟)
- NoGoods 229、Fire 4、Noise 7、Garbage 10、Pollution 36、Flood 1、Crime 1、LandValueLow 2、Water 1
