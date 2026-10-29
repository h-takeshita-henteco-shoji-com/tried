# m09 調査 health(s09-2)

問い: 汚染の印の中心(3700,-100)の汚染は、z=-274 の工場列と、z=-506〜-596 の工場群のどちらが主な原因か。

## 2050-09-08(見回り1)

- `map_layer` pollution x=3700, z=-300, radius=350, n=8: average 85, min 0, max 255(最大の点 (3550,-550))。北から2行目まで(z -650〜-50 のうち北側の行 z 約50〜-50)に 253〜254 の点が (3550〜3650, z 50〜-50) にある。z=-450 付近(5行目)は全部0。南の3行(z -350〜-650 の南側、z約-500〜-650)は 177〜255 が x 3550〜3900 に広がる
- `complaints`: Pollution 32棟、hotspot (3689,-84.7) 17棟。例: 675 (3482,-96)、3573 (3664,76)、4378 (3532,24)、5662 (3556,-44)、9959 (3513,-96)。全体の buildingsWithProblems 310
- `buildings_near` x=3760, z=-520, radius=160, service=Industrial, brief=true: total 31。NoResources は 3953、10741、17915(17915 は FatalProblem も)の3棟。残りは None

## 2050-09-18(見回り2)

- `map_layer` pollution(同じ引数): average 86, min 0, max 255(最大の点 (3550,50))。北2行は x 3550〜3650 が 255。5行目(z約-450)は全部0。南の3行は x 3550〜3900 に 164〜255
- `complaints`: Pollution 20棟、hotspot (2072.5,607.3) 8棟(住宅。前回の hotspot (3689,-85) 17棟から移った)。buildingsWithProblems 288
- `buildings_near` x=3760, z=-520, radius=160, service=Industrial, brief=true, problems_only=true: total 4。NoResources は 3953、4623、10741、17915(17915 は FatalProblem も)

## 2050-09-28(月末)

- `map_layer` pollution(同じ引数): average 86, min 0, max 255(最大の点 (3550,50))。北2行の x 3550〜3650 は 255。5行目は全部0。南の3行は x 3550〜3900 に 146〜255
- `complaints`: Pollution 23棟、hotspot (2090.9,808.2) 9棟(住宅)。buildingsWithProblems 289
- `buildings_near` x=3760, z=-520, radius=160, service=Industrial, brief=true, problems_only=true: total 6。NoResources は 3953、4623、10741、17915(FatalProblem も)、32689、44616
