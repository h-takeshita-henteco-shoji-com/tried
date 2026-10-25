# s04-1 空き家があるのに人口が減る原因(urban)

問い: 空き家が5,000超あるのに人口が減るのは、大学卒の失業(働き口の不足)が住宅の需要を押さえているからか

## 見回り1(2050-04-11)

- `demand_breakdown()`: jobs 86,393、emptyJobs 3,277、homes 55,533、emptyHomes 5,134、unemployed 7,006、homeless 0。byEducation の unemployed: uneducated 135、elementary 33、highSchool 31、university 6,807(eligibleWorkers 82,650)。戻り値に residential / workplace の項(base、jobTerm、homeTerm)は入っていなかった
- `citizens_summary()`: residents 178,087、movingIn 14(traveling 0)。employed 83,108、unemployed 5,696(young 2,686・adult 3,010、大学卒 5,587)、students 42,772。年齢 child 10,775・teen 22,277・young 32,201・adult 67,557・senior 45,277。peopleWithProblems の longUnemployed 4,733、badHealth 2,423。average health 77
- `city_info()`: population 178,030、demand 住24・商4・工57、money 2,197,789、週の収入339,885・支出331,763

## 見回り2(2050-04-21)

- `demand_breakdown()`: jobs 86,399、emptyJobs 3,240、homes 55,551、emptyHomes 5,200、unemployed 7,044、homeless 0。byEducation の unemployed: uneducated 141、elementary 30、highSchool 32、university 6,841(eligibleWorkers 82,710)。residential / workplace の項は戻り値になし
- `citizens_summary()`: residents 177,945、movingIn 5(traveling 0)。employed 83,119、unemployed 5,671(young 2,661・adult 3,010、大学卒 5,577)、students 42,670。年齢 child 10,773・teen 22,206・young 32,203・adult 67,481・senior 45,282。longUnemployed 4,726、badHealth 2,349。average health 77
- `city_info()`: population 177,953、demand 住24・商2・工58、money 2,208,585、週の収入338,835・支出331,709

## 月末(2050-05-01)

- `demand_breakdown()`: jobs 86,382、emptyJobs 3,287、homes 55,576、emptyHomes 5,226、unemployed 6,970、homeless 0。byEducation の unemployed: uneducated 108、elementary 33、highSchool 19、university 6,810(eligibleWorkers 82,692)。residential / workplace の項は戻り値になし
- `citizens_summary()`: residents 177,871、movingIn 12(traveling 0)。employed 82,993、unemployed 5,783(young 2,694・adult 3,089、大学卒 5,656)、students 42,557。年齢 child 10,730・teen 22,196・young 32,190・adult 67,396・senior 45,359。longUnemployed 4,684、badHealth 2,363。average health 78
- `city_info()`: population 177,854、demand 住24・商2・工58、money 2,217,819、週の収入338,193・支出331,676
