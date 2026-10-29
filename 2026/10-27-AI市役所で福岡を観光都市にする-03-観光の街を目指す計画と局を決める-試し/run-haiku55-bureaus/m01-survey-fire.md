# m01 調査 s01-3(fire)大きな火への消防車

## 月末(2050-01-31)

- `buildings_near`(x=2200, z=-900, radius=250, problem="Fire"): total 2。id 12882 (2184,-918) "Fire, FatalProblem"(3回とも同じ建物)。新たに id 9156 H4 3x4 Tenement07b (2017,-774) "Fire"
- `buildings_near`(x=2253, z=-880, radius=60, service="FireDepartment"): Fire House id 32853、vehicles.inUse 4、"Fire engines in use: 4 / 8"(見回り1と2は 0)
- `traffic`(x=2200, z=-900, radius=300): flow 51、cars 283、blocked 87、congestion 94、averageDensity 54。blockedSpots 先頭 (2274,-932) の 29台、(2182,-741) の 27台、(2162,-841) の 18台

## 見回り2(2050-01-21)

- `buildings_near`(x=2200, z=-900, radius=250, problem="Fire"): total 1。id 12882 (2184,-918)、"Fire, FatalProblem"(前回と同じ)
- `buildings_near`(x=2253, z=-880, radius=60, service="FireDepartment"): Fire House id 32853、vehicles.inUse 0、"Fire engines in use: 0 / 8"
- `traffic`(x=2200, z=-900, radius=300): flow 51、cars 266、blocked 40、congestion 88、averageDensity 58。blockedSpots 先頭 (2195,-727) の 21台、(2179,-837) の 15台

## 見回り1(2050-01-11)

- `buildings_near`(x=2200, z=-900, radius=250, problem="Fire"): total 1。id 12882 H3 2x2 Bigfactory06 (2184,-918)、problems "Fire, FatalProblem"
- `buildings_near`(x=2253, z=-880, radius=60, service="FireDepartment"): Fire House id 32853 (2253,-880)。vehicles.inUse 0、stats "Fire engines in use: 0 / 8"、働き手 29
- `traffic`(x=2200, z=-900, radius=300): flow 51、cars 274、blocked 19、congestion 84、averageDensity 55。busiest 10区間が density 100(例: 区間10391 (2236,-924)、区間9298 (2130,-856))。blockedSpots 先頭 (2123,-843) の 9台
