# m19 調査 s19-3(economy)空き地3の名所の訪問

問い: 空き地3の魅力度は高いのに、名所 11580 の訪問が週2なのはなぜか。空き地3に名所を足して、訪問は増えるか。

## 2051-07-15(見回り1)

- `buildings_near`(service Monument, x 745, z 1500, radius 300, brief false): total 1。11580 StatueOfWealth(668,1565)。grid electricity true、water false、sewage false(needs は電気のみ)。problems None。workers 5。stats: Visitors last week 5、Tourists last week 2
- `map_layer`(attractiveness, x 745, z 1500, radius 200, n 5): average 26、min 0、max 140(maxAt 745,1300)。grid(北の行から): [0,0,0,0,0] / [0,30,139,0,0] / [0,16,15,0,0] / [78,53,96,0,0] / [62,35,140,0,0]
- `water_trace`(x 745, z 1500): building null、cell water false、sewage false、waterPollution 0。networks 空(networkCount 0)。city の water used 1,895,632 / capacity 2,400,000、sewage used 1,892,368 / capacity 2,400,000

## 2051-08-04(月末)

- `buildings_near`(service Monument, x 745, z 1500, radius 300, brief false): total 1。11580 StatueOfWealth(668,1565)。grid electricity true、water false、sewage false(needs は電気のみ)。problems None。workers 5。stats: Visitors last week 3、Tourists last week 2
- `map_layer`(attractiveness, x 745, z 1500, radius 200, n 5): average 26、min 0、max 140(maxAt 745,1300)。grid は見回り1と同じ: [0,0,0,0,0] / [0,30,139,0,0] / [0,16,15,0,0] / [78,53,96,0,0] / [62,35,140,0,0]
- `water_trace`(x 745, z 1500): building null、cell water false、sewage false、waterPollution 0。networks 空(networkCount 0)。city の water used 1,891,360 / capacity 2,400,000、sewage used 1,888,096 / capacity 2,400,000
