# m01 調査 s01-3(fire): 火事の印が残る理由

実行する市長が、道具の返した数だけを書く。見立ては書かない。

## 見回り1(2050-01-11)

### `complaints()`

- Fire: buildings 6、hotspot (3312.8,-226.5) 4棟
- examples: 2002 L3 1x1 Shop07 (3388,-742)、5804 Elementary School (3125,-836)、37028 L5 3x2 Villa06 (3232,436)、38134 H3 3x3 Office15 (3506,236)
- 参考(同じ戻り値): Crime 3、Death 56、Pollution 40、Garbage 19、NoGoods 239

### `buildings_near(x=3273, z=-311, radius=400, problem="Fire", brief=true)`

- total 0、buildings []

### `map_layer(type="fire", x=3273, z=-311, radius=500, n=9)`

- average 172、min 38((2773,-436))、max 315((3648,-561))
- 西の列(x=2773)は38〜137、東の半分(x=3273〜3773)は101〜315

## 見回り2(2050-01-21)

### `complaints()`

- Fire: buildings 4、hotspot (2462,-781) 2棟
- examples: 12165 L4 3x4 Villa01 (2740,-644)、12882 H3 2x2 Bigfactory06 (2184,-918)
- 見回り1の examples(2002、5804、37028、38134)は今回の examples に出ていない
- 参考: Crime 1(32211 Cargo Harbor (-640,1074))、Death 53、Pollution 46、Garbage 24、Flood 1

### `buildings_near(x=3273, z=-311, radius=400, problem="Fire", brief=true)`

- total 0、buildings []

### `map_layer(type="fire", x=3273, z=-311, radius=500, n=9)`

- average 172、min 38((2773,-436))、max 315((3648,-561))。grid は見回り1と同じ値

## 月末(2050-01-31)

### `complaints()`

- Fire: buildings 4、hotspot (2462,-781) 2棟
- examples: 12165 L4 3x4 Villa01 (2740,-644)、12882 H3 2x2 Bigfactory06 (2184,-918)
- 参考: Crime 2(48627 H3 3x4 Office11a (-2156,-512) など)、Death 40、Pollution 43、Garbage 31、Noise 4、Flood 1

### `buildings_near(x=3273, z=-311, radius=400, problem="Fire", brief=true)`

- total 0、buildings []

### `map_layer(type="fire", x=3273, z=-311, radius=500, n=9)`

- average 172、min 38((2773,-436))、max 315((3648,-561))。grid は見回り1・2と同じ値
