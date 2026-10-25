# s01-2 事務所の空き区画と大卒の失業(urban)

問い: 働き口の需要が60あるのに、事務所の空き区画1,642マスが埋まらず、大卒の失業7,720が残るのはなぜか

## 見回り1(2050-01-11)

### `zone_summary(grid=1000)`

- Office: total 36,793、empty 1,642、emptyShallow 0、emptyNarrow 0、emptyBehind 1,642、emptyFacingRoad 0
- CommercialHigh: total 8,973、empty 575(emptyBehind 435、emptyFacingRoad 140)
- ResidentialHigh: total 37,651、empty 709(emptyBehind 709)
- Industrial: total 6,104、empty 66(emptyBehind 66)
- 事務所の空きの多い区切り: (-500, -500) 197、(-1500, -500) 187、(3500, -500) 123、(-2500, -500) 106、(500, -500) 88、(2500, -500) 86、(500, -1500) 83、(1500, 1500) 82

### `demand_breakdown()`

- jobs 86,247、emptyJobs 3,331、homes 55,288、emptyHomes 4,975、unemployed 7,651、homeless 0
- 学歴ごとの失業 / 働ける人: uneducated 88 / 4,523、elementary 33 / 1,060、highSchool 28 / 339、university 7,502 / 82,933

### `new_buildings(since=0)`

- index 92181
- newBuildings(since=0 のため累計): CommercialHigh 1,106、CommercialLow 166、IndustrialGeneric 806、OfficeGeneric 3,979、ResidentialHigh 4,057、ResidentialLow 1,013

## 見回り2(2050-01-21)

### `zone_summary(grid=1000)`

- Office: total 36,793、empty 1,642、emptyBehind 1,642、emptyFacingRoad 0(見回り1と同じ)
- CommercialHigh: empty 562(emptyBehind 435、emptyFacingRoad 127)
- ResidentialHigh: empty 709、Industrial: empty 66、CommercialLow: empty 90、ResidentialLow: empty 381(見回り1と同じ)
- 事務所の空きの区切りごとの数は、(1500, 1500) の CommercialHigh 12 が消えたほかは見回り1と同じ

### `demand_breakdown()`

- jobs 86,257、emptyJobs 3,333、homes 55,323、emptyHomes 4,990、unemployed 7,619、homeless 0
- 学歴ごとの失業 / 働ける人: uneducated 100 / 4,457、elementary 50 / 1,078、highSchool 26 / 330、university 7,443 / 82,837

### `new_buildings(since=92181)`

- index 92273
- newBuildings: CommercialHigh 17、IndustrialGeneric 3、ResidentialLow 1(OfficeGeneric 0)

## 月末(2050-01-31)

### `zone_summary(grid=1000)`

- Office: total 36,793、empty 1,642、emptyBehind 1,642、emptyFacingRoad 0(見回り1・2と同じ)
- CommercialHigh: empty 549(emptyBehind 437、emptyFacingRoad 112)
- ResidentialHigh 709、Industrial 66、CommercialLow 90、ResidentialLow 381(見回り1・2と同じ)
- 事務所の空きの区切りごとの数は見回り1・2と同じ

### `demand_breakdown()`

- jobs 86,342、emptyJobs 3,201、homes 55,348、emptyHomes 4,939、unemployed 7,409、homeless 0
- 学歴ごとの失業 / 働ける人: uneducated 138 / 4,458、elementary 36 / 1,080、highSchool 30 / 343、university 7,205 / 82,890

### `new_buildings(since=92273)`

- index 92375(来月はこれを since に使う)
- newBuildings: CommercialHigh 18、IndustrialGeneric 2、ResidentialHigh 1(OfficeGeneric 0)
- 今月(since=92181 から)の合計: CommercialHigh 35、IndustrialGeneric 5、ResidentialHigh 1、ResidentialLow 1、OfficeGeneric 0
