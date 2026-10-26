# m02 調査 s02-3(economy): 事務所の空きマスが建たず大卒の失業が残る理由

問い: 空きの事務所マス1,642が建たないのに、大卒の失業7,234が残るのはなぜか(需要か、立地か、建築の上限か)。

## 見回り1(2050-02-10)

- `demand_breakdown()`: jobs 86,290、emptyJobs 3,216、homes 55,376、emptyHomes 4,989、unemployed 7,442、homeless 0
  - byEducation の失業: uneducated 119、elementary 45、highSchool 23、university 7,255(eligibleWorkers 82,803)
  - 戻り値に residential と workplace の項(base、jobTerm など)は入っていなかった
- `new_buildings(since=92383)`: index 92486。CommercialHigh 18、CommercialLow 1、IndustrialGeneric 1、ResidentialHigh 1、ResidentialLow 2。Office 0
- `zones_at(x=-1000, z=-1000, radius=700)`: ResidentialHigh 8,227(空き78)、CommercialHigh 925(空き42)、Office 1,777(空き161)、Unzoned 765(空き248)
- 参考(同じ見回りの `city_info`): 需要 住23 / 商2 / 工59

## 見回り2(2050-02-20)

- `demand_breakdown()`: jobs 86,365、emptyJobs 3,233、homes 55,404、emptyHomes 5,032、unemployed 7,323、homeless 0
  - byEducation の失業: uneducated 104、elementary 41、highSchool 31、university 7,147(eligibleWorkers 82,740)
- `new_buildings(since=92383)`: index 92584。CommercialHigh 36、CommercialLow 1、IndustrialGeneric 2、ResidentialHigh 1、ResidentialLow 3。Office 0
- `zones_at(x=-1000, z=-1000, radius=700)`: 見回り1と同じ。ResidentialHigh 8,227(空き78)、CommercialHigh 925(空き42)、Office 1,777(空き161)、Unzoned 765(空き248)
- 参考(同じ見回りの `city_info`): 需要 住23 / 商2 / 工59

## 月末(2050-03-02)

- `demand_breakdown()`: jobs 86,426、emptyJobs 3,341、homes 55,428、emptyHomes 5,118、unemployed 7,247、homeless 0
  - byEducation の失業: uneducated 127、elementary 29、highSchool 26、university 7,065(eligibleWorkers 82,673)
- `new_buildings(since=92383)`: index 92685。CommercialHigh 52、CommercialLow 2、IndustrialGeneric 6、ResidentialHigh 1、ResidentialLow 3。Office 0(1か月で0)
- `zones_at(x=-1000, z=-1000, radius=700)`: 3回とも同じ。ResidentialHigh 8,227(空き78)、CommercialHigh 925(空き42)、Office 1,777(空き161)、Unzoned 765(空き248)
