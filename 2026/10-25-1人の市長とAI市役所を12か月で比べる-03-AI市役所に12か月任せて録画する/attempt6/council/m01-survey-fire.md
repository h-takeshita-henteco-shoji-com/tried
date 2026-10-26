# m01 調査 s01-3(fire): 火事と犯罪の印が居続けるか

問い: 火事と犯罪の印は、同じ棟に居続けるのか、入れ替わる一時的なものか。

## 見回り1(2050-01-11)

### `complaints`(引数なし)

- Fire 8棟(hotspot (1770,-531) 4棟。例 12882、33283、40021、46911)
- Crime 1棟(29872 (-406,-1844))
- ほか: Death 55、Garbage 13、Pollution 40、Noise 9、NoGoods 235、LandValueLow 1、Water 1

### `buildings_near`(x=3300, z=-300, radius=5000, problem="Fire")

- total 7
- 2002 L3 1x1 Shop07 (3388,-742) Fire, FatalProblem
- 5804 Elementary School (3125,-836) Fire, FatalProblem(Students 0 / 348)
- 8191 H5 2x2 tenement03 (-1492,-366) Fire
- 12882 H3 2x2 Bigfactory06 (2184,-918) Fire, FatalProblem
- 33283 H5 3x3 Tenement03 (1383,-773) Fire
- 40021 H5 3x2 Tenement02 (2307,-144) Fire
- 46911 H2 3x4 Office05a (1206,-290) Fire

### `buildings_near`(x=2255, z=836, radius=5000, problem="Crime")

- total 1
- 29872 H3 2x2 Tenement04 (-406,-1844) Crime, MajorProblem(homes 6、occupied 3)

## 見回り2(2050-01-21)

### `complaints`(引数なし)

- Fire 6棟(hotspot (3422,-557) 3棟。例 2002、5804、44223)
- Crime 2棟(hotspot (-584,-374) 1棟。例 1838)
- ほか: Death 57、Pollution 42、Noise 4、NoGoods 224、Garbage 11、Flood 2、Water 1

### `buildings_near`(x=3300, z=-300, radius=5000, problem="Fire")

- total 6
- 2002 L3 1x1 Shop07 (3388,-742) Fire, FatalProblem(見回り1にもあった)
- 3031 H5 3x2 Tenement02 (-1476,-330) Fire(新)
- 5804 Elementary School (3125,-836) Fire, FatalProblem(見回り1にもあった。Students 0 / 348)
- 8191 H5 2x2 tenement03 (-1492,-366) Fire, MajorProblem(見回り1にもあった。occupied 7→2)
- 12882 H3 2x2 Bigfactory06 (2184,-918) Fire, FatalProblem(見回り1にもあった)
- 44223 L4 2x2 Villa07 (3752,-94) Fire(新)
- 見回り1にあって消えた棟: 33283、40021、46911

### `buildings_near`(x=2255, z=836, radius=5000, problem="Crime")

- total 2
- 1838 H5 4x4 Tenement01 (-584,-374) Crime, Pollution, MajorProblem(homes 25、occupied 2)(新)
- 32211 Cargo Harbor (-640,1074) Garbage, Crime, MajorProblem(新)
- 見回り1にあって消えた棟: 29872

## 月末(2050-01-31)

### `complaints`(引数なし)

- Fire 6棟(hotspot (3422,-557) 3棟。例 2002、5804、44223)
- Crime 3棟(hotspot (908,160) 1棟。例 91)
- ほか: Death 44、Pollution 39、NoGoods 218、Garbage 15、Noise 5、Flood 1、LandValueLow 1、Water 1

### `buildings_near`(x=3300, z=-300, radius=5000, problem="Fire")

- total 6
- 2002 L3 1x1 Shop07 (3388,-742) Fire, FatalProblem(見回り1・2にもあった)
- 5804 Elementary School (3125,-836) Fire, FatalProblem(見回り1・2にもあった。Students 0 / 348)
- 8191 H5 2x2 tenement03 (-1492,-366) Fire, FatalProblem(見回り1・2にもあった。homes の欄なし)
- 12882 H3 2x2 Bigfactory06 (2184,-918) Fire, FatalProblem(見回り1・2にもあった)
- 41241 L3 2x3 Semi-detachedhouse02 (3712,-974) Fire(新。homes 2、occupied 2)
- 44223 L4 2x2 Villa07 (3752,-94) Fire, MajorProblem(見回り2にもあった。occupied 1→0)
- 見回り2にあって消えた棟: 3031

### `buildings_near`(x=2255, z=836, radius=5000, problem="Crime")

- total 3
- 91 H3 1x1 Office01 (908,160) Crime(新。jobs 2/2)
- 27264 H2 2x2 Office08 (4154,-226) Crime(新。jobs 8/8)
- 32211 Cargo Harbor (-640,1074) Garbage, Crime, MajorProblem(見回り2にもあった。workers 62)
- 見回り2にあって消えた棟: 1838
