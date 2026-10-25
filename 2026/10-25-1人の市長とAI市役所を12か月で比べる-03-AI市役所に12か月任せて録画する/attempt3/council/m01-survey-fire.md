# s01-3 火事と犯罪の印の場所の偏りを見る(fire)

問い: 火事と犯罪の印の建物は、消防・警察の届き具合が低い場所に集まっているか

## 2050-01-11(見回り1)

- `complaints()`
  - buildingsWithProblems 362
  - Fire 4: hotspot 3256.5,-789(2棟)。examples 2002 L3 1x1 Shop07(3388,-742)、5804 Elementary School(3125,-836)
  - Crime 2: hotspot -406,-1844(1棟)。example 29872 H3 2x2 Tenement04(-406,-1844)
  - ほか: Death 55、Garbage 19、Pollution 34、NoGoods 236、Noise 11、Water 1
- `buildings_near(x=3272, z=-311, radius=600, problem="Fire")`
  - total 2: 2002 L3 1x1 Shop07(3388,-742、Fire+FatalProblem)、5804 Elementary School(3125,-836、Fire+FatalProblem、生徒 0/348)
- `buildings_near(x=2255, z=836, radius=500, problem="Crime")`
  - total 0

## 2050-01-21(見回り2)

- `complaints()`
  - buildingsWithProblems 349
  - Fire 3: hotspot 3256.5,-789(2棟)。examples 2002 L3 1x1 Shop07(3388,-742)、5804 Elementary School(3125,-836)
  - Crime 1: hotspot -640,1074。example 32211 Cargo Harbor(-640,1074)
  - ほか: Death 52、NoGoods 232、Garbage 19、Noise 8、Pollution 34、Flood 1、Water 1
- `buildings_near(x=3272, z=-311, radius=600, problem="Fire")`
  - total 2: 2002 L3 1x1 Shop07(3388,-742、Fire+FatalProblem)、5804 Elementary School(3125,-836、Fire+FatalProblem、生徒 0/348)
- `buildings_near(x=2255, z=836, radius=500, problem="Crime")`
  - total 0

## 2050-01-31(月末)

- `complaints()`
  - buildingsWithProblems 369
  - Fire 3: hotspot 3256.5,-789(2棟)。examples 2002 L3 1x1 Shop07(3388,-742)、5804 Elementary School(3125,-836)
  - Crime 3: hotspot 908,160(1棟)。example 91 H3 1x1 Office01(908,160)
  - ほか: Death 49、NoGoods 231、Garbage 33、Pollution 37、Noise 10、Flood 1、LandValueLow 1、Water 1
- `buildings_near(x=3272, z=-311, radius=600, problem="Fire")`
  - total 2: 2002 L3 1x1 Shop07(3388,-742、Fire+FatalProblem)、5804 Elementary School(3125,-836、Fire+FatalProblem、生徒 0/348)
- `buildings_near(x=2255, z=836, radius=500, problem="Crime")`
  - total 0
- 3回とも、Fire の2棟は同じ建物(2002、5804)で、FatalProblem が付いたまま
