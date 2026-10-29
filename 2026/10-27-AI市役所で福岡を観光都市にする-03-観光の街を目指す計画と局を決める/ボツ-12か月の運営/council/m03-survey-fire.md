# m03 調査 s03-3 火事の印の2棟が消えない理由

## 見回り1(2050-03-13)

- `buildings_near`(x=3125, z=-836, radius=20, limit=5): 学校 5804。problems "Fire, FatalProblem"。電気・水・下水は来ている。Students 0 / 348。vehicles inUse 0
- `buildings_near`(x=3290, z=-604, radius=20, service="FireDepartment"): Fire House 49026。problems None。Fire engines in use 1 / 8
- `complaints`: Fire 5棟(2002 店、5804 学校、38574 Villa01 ほか)。hotspot (3243,-789) 3棟。月例時は 3棟

## 見回り2(2050-03-23)

- `buildings_near`(x=3125, z=-836, radius=20, limit=5): 学校 5804。problems "Fire, FatalProblem"(変わらず)。Students 0 / 348。vehicles inUse 0
- `buildings_near`(x=3290, z=-604, radius=20, service="FireDepartment"): Fire House 49026。problems None。Fire engines in use 1 / 8
- `complaints`: Fire 4棟(2002 店、5804 学校、38574 Villa01 ほか)。hotspot (3243,-789) 3棟

## 月末(2050-04-02)

- `buildings_near`(x=3125, z=-836, radius=20, limit=5): 学校 5804。problems "Fire, FatalProblem"(変わらず)
- `buildings_near`(x=3290, z=-604, radius=20, service="FireDepartment"): Fire House 49026。problems None。Fire engines in use 1 / 8。workers 31
- `complaints`: Fire 5棟(2002 店、5804 学校、38574 Villa01 ほか)。hotspot (3243,-789) 3棟。犯罪 3棟
