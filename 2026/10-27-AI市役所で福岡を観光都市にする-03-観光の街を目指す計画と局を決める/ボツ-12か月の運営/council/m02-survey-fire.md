# m02 調査 s02-3(fire)火事の印の繰り返し

## 2050-02-11 見回り1

- `complaints`: Fire 5 棟(hotspot (3256.5,-789) 2棟)。Death 39、Pollution 39、NoGoods 221、Noise 11、Garbage 16(hotspot (1210,-1111))、Water 1。
- `buildings_near`(x=3256, z=-789, radius=300, problem="Fire", brief=true, limit=10): total 2。2002 L3 1x1 Shop07 (3388,-742) Fire, FatalProblem。5804 Elementary School (3125,-836) Fire, FatalProblem。
- `map_layer`(type="fire", x=3250, z=-790, radius=300, n=7): average 201、min 87 (2950,-490)、max 317 (3550,-590)。西端の列は 87〜130 と低く、東は 300 前後。

## 2050-02-21 見回り2

- `complaints`: Fire 4 棟(hotspot (3257.7,-819.3) 3棟)。Garbage 21、Crime 2、Death 45、Pollution 38、NoGoods 224。
- `buildings_near`(x=3256, z=-789, radius=300, problem="Fire", brief=true, limit=10): total 3。2002 L3 1x1 Shop07 (3388,-742) Fire, FatalProblem(前回と同じ建物)。5804 Elementary School (3125,-836) Fire, FatalProblem(前回と同じ建物)。5119 L3_3x4_Detached_10 (3260,-880) Fire(新しく出た)。
- `map_layer`(type="fire", x=3250, z=-790, radius=300, n=7): 前回と同じ値(average 201、min 87、max 317)。

## 2050-03-03 月末

- `complaints`: Fire 3 棟(hotspot (3256.5,-789) 2棟)。Crime の項目なし。Garbage 14、Pollution 44、Death 60、NoGoods 228。
- `buildings_near`(x=3256, z=-789, radius=300, problem="Fire", brief=true, limit=10): total 2。2002 L3 1x1 Shop07 (3388,-742)、5804 Elementary School (3125,-836)。どちらも Fire, FatalProblem。3回とも同じ2棟。5119 は消えた。
- `map_layer`(type="fire", x=3250, z=-790, radius=300, n=7): 前回までと同じ値(average 201、min 87、max 317)。
