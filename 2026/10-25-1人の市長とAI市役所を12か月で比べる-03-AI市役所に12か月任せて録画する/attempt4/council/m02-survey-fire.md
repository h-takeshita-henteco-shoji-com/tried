# m02 調査 s02-3(fire): 火事の印が減らない理由

問い: 火事の印の建物は、消防の届き具合が低い場所にあるのか、それとも建物ごとに入れ替わるだけなのか

## 見回り1(2050-02-10)

### `complaints()` の Fire

- Fire 4棟。hotspot (3256.5,-789) 2棟
- examples: 2002 L3 1x1 Shop07 (3388,-742)、5804 Elementary School (3125,-836)

### `buildings_near(x=3212, z=-498, radius=600, problem="Fire")`

- total 2
- 2002 L3 1x1 Shop07 (3388,-742): problems Fire, FatalProblem
- 5804 Elementary School (3125,-836): problems Fire, FatalProblem。Students 0 / 348

### `map_layer(type="fire", x=3212, z=-498, radius=600, n=9)`

- average 162、min 26 (2612,-348)、max 312 (3662,-648)
- 範囲 x 2612〜3812、z -1098〜102。北の行から、西から東へ:
  - 123 119 93 94 114 127 151 152 119
  - 69 66 65 102 143 180 204 188 144
  - 37 45 69 108 171 229 256 231 176
  - 26 32 63 131 198 261 301 275 226
  - 39 44 67 147 224 282 307 295 252
  - 67 75 84 157 236 292 310 312 274
  - 98 105 107 160 222 254 267 278 258
  - 116 120 125 152 188 209 205 220 211
  - 126 122 132 142 161 165 153 157 165

## 見回り2(2050-02-20)

### `complaints()` の Fire

- Fire 3棟。hotspot (3256.5,-789) 2棟
- examples: 2002 L3 1x1 Shop07 (3388,-742)、5804 Elementary School (3125,-836)

### `buildings_near(x=3212, z=-498, radius=600, problem="Fire")`

- total 2
- 2002 L3 1x1 Shop07 (3388,-742): problems Fire, FatalProblem
- 5804 Elementary School (3125,-836): problems Fire, FatalProblem。Students 0 / 348

### `map_layer(type="fire", x=3212, z=-498, radius=600, n=9)`

- average 162、min 26 (2612,-348)、max 312 (3662,-648)。grid は見回り1と同じ値

## 月末(2050-03-02)

### `complaints()` の Fire

- Fire 4棟。hotspot (1749.3,-342.7) 2棟(見回り1・2の hotspot (3256.5,-789) から変わった)
- examples: 12882 H3 2x2 Bigfactory06 (2184,-918)、24662 H3 2x2 Office16 (1314.5,232.7)

### `buildings_near(x=3212, z=-498, radius=600, problem="Fire")`

- total 2
- 2002 L3 1x1 Shop07 (3388,-742): problems Fire, FatalProblem
- 5804 Elementary School (3125,-836): problems Fire, FatalProblem。Students 0 / 348

### `map_layer(type="fire", x=3212, z=-498, radius=600, n=9)`

- average 162、min 26 (2612,-348)、max 312 (3662,-648)。grid は見回り1と同じ値
