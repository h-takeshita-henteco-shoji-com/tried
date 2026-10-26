# m04 調査の結果(urban)

## s04-1 人口が増えにくいのは、大学卒の失業と空きの働き口の学歴が合わないためか

### 見回り1(2050-04-11)

- `demand_breakdown()`
  - jobs 86,385、emptyJobs 3,175、unemployed 6,883、homeless 0
  - homes 55,486、emptyHomes 5,112
  - byEducation の unemployed / eligibleWorkers: uneducated 86 / 4,278、elementary 34 / 1,148、highSchool 27 / 311、university 6,736 / 82,579
- `citizens_summary()`
  - residents 178,244、movingIn 4(traveling 0)
  - 年齢: child 10,749、teen 22,306、young 32,280、adult 67,482、senior 45,427
  - 学歴: uneducated 18,884、elementary 25,405、highSchool 12,545、university 121,410
  - employed 83,162、unemployed 5,588(young 2,632、adult 2,956)、students 42,847、sick 1,990
  - unemployedDetail.byEducation: uneducated 48、elementary 30、highSchool 19、university 5,491
  - peopleWithProblems: longUnemployed 4,732、badHealth 2,438、来ない 0/0/0
  - average: health 77、wellbeing 99、happiness 89
- `building_stats()`(x を省く)
  - CommercialHigh 1,046棟(放棄51)、jobs 8,118、L1/L2/L3 47/39/909
  - CommercialLow 164棟(放棄1)、jobs 1,475
  - IndustrialGeneric 806棟(放棄9)、jobs 10,658、L1/L2/L3 40/68/689
  - OfficeGeneric 3,981棟(放棄0)、jobs 53,233、L1/L2/L3 68/680/3,233
  - ResidentialHigh 4,057棟(放棄3)、homes 52,054、地価58
  - ResidentialLow 1,013棟(放棄2)、homes 3,433、地価46

### 月末(2050-05-01)

- `demand_breakdown()`
  - jobs 86,353、emptyJobs 3,232、unemployed 6,959、homeless 0
  - homes 55,511、emptyHomes 5,093
  - byEducation の unemployed / eligibleWorkers: uneducated 104 / 4,213、elementary 32 / 1,144、highSchool 20 / 303、university 6,803 / 82,659
- `citizens_summary()`
  - residents 178,191、movingIn 4(traveling 0)
  - 年齢: child 10,825、teen 22,205、young 32,268、adult 67,422、senior 45,471
  - 学歴: uneducated 18,864、elementary 25,228、highSchool 12,477、university 121,622
  - employed 83,013、unemployed 5,729(young 2,688、adult 3,041)、students 42,786、sick 2,005
  - unemployedDetail.byEducation: uneducated 66、elementary 27、highSchool 43、university 5,593
  - peopleWithProblems: longUnemployed 4,734、badHealth 2,529、来ない 0/0/0
  - average: health 77、wellbeing 99、happiness 89
- `building_stats()`(x を省く)
  - CommercialHigh 1,060棟(放棄67)、jobs 8,075、L1/L2/L3 43/41/909
  - CommercialLow 165棟(放棄2)、jobs 1,461
  - IndustrialGeneric 806棟(放棄8)、jobs 10,663、L1/L2/L3 39/71/688
  - OfficeGeneric 3,981棟(放棄0)、jobs 53,240、L1/L2/L3 67/679/3,235
  - ResidentialHigh 4,057棟(放棄3)、homes 52,079、地価58
  - ResidentialLow 1,013棟(放棄3)、homes 3,428、地価46
