# m20 調査 s20-3 焼却場 2267 の周りの汚染の動き

## 2051-08-14 見回り1

- `map_layer` pollution(x 3600, z -60, radius 300, n 7): average 47、min 0、max 255(最大の点 (3600,40))。255 の点は 5 つ((3500〜3600, 40〜-20)付近と(3700〜3900, -260 付近は 201/255/251))
- `buildings_near`(x 3600, z -60, radius 300, problem Pollution): total 8(6224、16852、17131、23124、32253、35136、46837、47688。46837 は MajorProblem つき)
- `complaints`: Pollution 27棟(hotspot (3878.6,-304.4) 16棟)、Garbage 14、Fire 1、Crime 1

## 2051-08-24 見回り2

- `map_layer` pollution(同じ引数): average 49、min 0、max 255(最大の点 (3600,40))。255 の点は 5 つ前後
- `buildings_near`(Pollution): total 9(6224、16852、17131、17697、23124、35136、36382、45081、47039)
- `complaints`: Pollution 32棟(hotspot (3840.2,-224.2) 18棟)、Garbage 14、Death 35、Fire 1、Crime 3

## 2051-09-03 月末

- `map_layer` pollution(同じ引数): average 49、min 0、max 255(最大の点 (3600,40))。255 の点は 7 つ前後(2行目の中央列と隣)
- `buildings_near`(Pollution): total 6(4378、19443、27535、36382、46837、47039)
- `complaints`: Pollution 25棟(hotspot (3747.1,-94.1) 12棟)、Garbage 9、Death 31、Fire 1、Crime 2
