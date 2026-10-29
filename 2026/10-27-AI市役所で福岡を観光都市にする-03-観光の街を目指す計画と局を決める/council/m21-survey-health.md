# m21 調査 s21-2 汚染の印の出どころ(health)

## 2051-09-13 見回り1

- `map_layer` pollution(x=4050, z=-300, radius=350, n=9): average 89、min 0、max 255(maxAt 3788,-212)。西の列(x=3700)と、東の2列(x=4200〜4300付近)で255前後が続く。中央は0
- `buildings_near`(x=4150, z=-250, radius=300, problem="Pollution", brief=true): total 0
- `complaints`: Pollution 26棟(hotspot 3523,156、9棟)。Garbage 15棟(hotspot 3991,-210)、Death 33棟(hotspot 3663,-93)、Fire 3、Crime 4、RoadNotConnected 2(23459 など)

## 2051-09-23 見回り2

- `map_layer` pollution(x=4050, z=-300, radius=350, n=9): average 89、min 0、max 255(maxAt 3788,-300)。分布は見回り1と同じ形(西の列x=3700と、東の2列で250前後。中央は0)
- `buildings_near`(x=4150, z=-250, radius=300, problem="Pollution", brief=true): total 2(39035 の (4180,-531)、48275 の (4184,-402))
- `complaints`: Pollution 37棟(hotspot 3676,-51、15棟)。Garbage 15(hotspot 2386,-151)、Death 39(hotspot 3619,-150)、Fire 2、Crime 4、RoadNotConnected 2(23459 など)

## 2051-10-03 月末

- `map_layer` pollution(x=4050, z=-300, radius=350, n=9): average 89、min 0、max 255(maxAt 3700,-300)。分布は同じ形(西の列x=3700と、東の2列で250前後。中央は0)
- `buildings_near`(x=4150, z=-250, radius=300, problem="Pollution", brief=true): total 1(48275 の (4184,-402)。Garbage と Pollution)
- `complaints`: Pollution 32棟(hotspot 2110,329、10棟)。Garbage 14(hotspot 3946,-189)、Death 32(hotspot 3560,-184)、Fire 4、Crime 3、RoadNotConnected 2(23459 など)
