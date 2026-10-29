# m06 調査 economy

## s06-2 東の街の電気・水が名所の敷地まで届くか

### 2050-06-10(見回り1)

- `map_layer`(electricity_service, x 1720, z 1050, radius 120, n 5): 平均0、最小0、最大1。北から5行(西から東): 0,0,1,1,1 / 0,0,1,1,1 / 0,0,0,1,1 / 0,0,0,0,1 / 0,0,0,0,1
- `map_layer`(water_service, 同じ範囲): 平均0、最小0、最大1。0,1,1,1,1 / 0,1,1,1,1 / 0,0,1,1,1 / 0,0,0,0,1 / 0,0,0,0,1
- `buildings_near`(service Monument, x 668, z 1565, radius 40): StatueOfWealth id 11580。grid.electricity false、problems Electricity, MajorProblem。Visitors last week 2、Tourists 0

### 2050-06-30(月末)

- `map_layer`(electricity_service, x 1720, z 1050, radius 120, n 5): 平均0、最小0、最大1。見回り1と同じ並び(0,0,1,1,1 / 0,0,1,1,1 / 0,0,0,1,1 / 0,0,0,0,1 / 0,0,0,0,1)
- `map_layer`(water_service, 同じ範囲): 平均0、最小0、最大1。見回り1と同じ並び(0,1,1,1,1 / 0,1,1,1,1 / 0,0,1,1,1 / 0,0,0,0,1 / 0,0,0,0,1)
- `buildings_near`(service Monument, x 668, z 1565, radius 40): StatueOfWealth id 11580。grid.electricity false、problems Electricity, MajorProblem。Visitors last week 0、Tourists 0
