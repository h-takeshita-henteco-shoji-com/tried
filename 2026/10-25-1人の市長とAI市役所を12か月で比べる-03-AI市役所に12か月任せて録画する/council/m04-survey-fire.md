# m04 調査の結果(fire)

## s04-3 工場12882の火事が残る理由

問い: 工場12882(2184,-918)の火事と FatalProblem が、消防車の不足と届き具合のどちらで残っているか。
見立ては書かない。局が翌月に読んで決める。

### 見回り1(2050-04-11)

- `buildings_near(x=2184, z=-918, radius=300, service="FireDepartment")`
  - total 1。32853 Fire House (2253,-880)。電気・水・下水 true、印なし。働き手 31。消防車 0 / 8(Fire engines in use)
- `buildings_near(x=2184, z=-918, radius=60, problems_only=true)`
  - total 1。12882 H3 2x2 Bigfactory06 (2184,-918)、problems "Fire, FatalProblem"、abandoned false、電気・水・下水 true
- `map_layer(type="fire", x=2184, z=-918, radius=300, n=9)`
  - average 105、min 42((1884,-1218))、max 135((2109,-618))
  - 中央の点 (2184,-918) の値は 124(grid の5行目・5列目)

### 見回り2(2050-04-21)

- `buildings_near(x=2184, z=-918, radius=300, service="FireDepartment")`
  - total 1。32853 Fire House (2253,-880)。印なし。働き手 31。消防車 1 / 8
- `buildings_near(x=2184, z=-918, radius=60, problems_only=true)`
  - total 1。12882 H3 2x2 Bigfactory06 (2184,-918)、problems "Fire, FatalProblem"
- `map_layer(type="fire", x=2184, z=-918, radius=300, n=9)`
  - average 105、min 42、max 135。中央の点は 124。grid は見回り1と同じ

### 月末(2050-05-01)

- `buildings_near(x=2184, z=-918, radius=300, service="FireDepartment")`
  - total 1。32853 Fire House (2253,-880)。印なし。働き手 29。消防車 1 / 8
- `buildings_near(x=2184, z=-918, radius=60, problems_only=true)`
  - total 1。12882 H3 2x2 Bigfactory06 (2184,-918)、problems "Fire, FatalProblem"
- `map_layer(type="fire", x=2184, z=-918, radius=300, n=9)`
  - average 105、min 42、max 135。中央の点は 124。grid は見回り1・2と同じ
