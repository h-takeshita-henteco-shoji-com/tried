# m06 調査 s06-1 の結果(urban)

問い: 人口が減る月と増える月を分けるのは、空き家(5,259)、大卒の失業(6,359)、引っ越しの途中の人のどれか。
見る道具: `demand_breakdown`、`citizens_summary`、`city_info`(どれも引数なし)。見立ては書かない。

## 見回り1(2050-06-10)

- `city_info`: population 178,106、demand 住宅25 / 商業7 / 働き口41、happiness 85、citizensWithoutService 0/0/0
- `demand_breakdown`: homes 55,708、emptyHomes 5,249、jobs 87,091、emptyJobs 3,356、unemployed 6,418、homeless 0。byEducation の unemployed は uneducated 140、elementary 32、highSchool 32、university 6,214
- `citizens_summary`: residents 178,118、movingIn total 7(traveling 0)。age は child 10,668、teen 21,973、young 32,456、adult 67,331、senior 45,690。unemployed 5,052(うち university 4,923)、longUnemployed 4,195、employed 83,677、students 42,440、sick 2,260

## 見回り2(2050-06-20)

- `city_info`: population 177,937、demand 住宅26 / 商業2 / 働き口56、happiness 85、citizensWithoutService 0/0/0
- `demand_breakdown`: homes 55,731、emptyHomes 5,296、jobs 87,161、emptyJobs 3,291、unemployed 6,249、homeless 0。byEducation の unemployed は uneducated 122、elementary 30、highSchool 32、university 6,065
- `citizens_summary`: residents 177,990、movingIn total 7(traveling 0)。age は child 10,619、teen 21,881、young 32,551、adult 67,175、senior 45,764。unemployed 4,841(うち university 4,765)、longUnemployed 4,081、employed 83,846、students 42,383、sick 2,265

## 月末(2050-06-30)

- `city_info`: population 178,004、demand 住宅26 / 商業4 / 働き口56、happiness 85、citizensWithoutService 0/0/0
- `demand_breakdown`: homes 55,725、emptyHomes 5,270、jobs 87,074、emptyJobs 3,291、unemployed 6,297、homeless 0。byEducation の unemployed は uneducated 159、elementary 26、highSchool 33、university 6,079
- `citizens_summary`: residents 178,016、movingIn total 7(traveling 0)。age は child 10,728、teen 21,817、young 32,533、adult 67,163、senior 45,775。unemployed 5,021(うち university 4,884)、longUnemployed 4,047、employed 83,680、students 42,290、sick 2,265

## 3回の並び(参考。月初 2050-05-31 の値は月例の記録から)

| 日付 | population | emptyHomes | university の unemployed(demand_breakdown) | movingIn |
|---|---|---|---|---|
| 05-31 | 178,138 | 5,259 | 6,359 | (見ていない) |
| 06-10 | 178,106 | 5,249 | 6,214 | 7 |
| 06-20 | 177,937 | 5,296 | 6,065 | 7 |
| 06-30 | 178,004 | 5,270 | 6,079 | 7 |
