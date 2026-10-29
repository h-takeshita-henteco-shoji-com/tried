# m01 調査 s01-1(economy): Tourism の収入が低い理由

見立ては書かない。局が翌月に読んで決める。

| ゲーム内の日付 | 区切り | tourists now | visits | Tourism の週の収入 | 名所(Monument)の棟数 |
|---|---|---|---|---|---|
| 2050-01-01 | 基準(実行前) | 1,646 | 139 | 45 | 6 |
| 2050-01-11 | 見回り1 | 1,652 | 141 | 42 | 6 |
| 2050-01-21 | 見回り2 | 1,649 | 142 | 50 | 6 |
| 2050-01-31 | 月末 | 1,584 | 141 | 54 | 6 |

- 道具: `city_info`、`economy_breakdown`(Tourism)、`buildings_near`(service="Monument", x=0, z=0, radius=5000, brief)
- 名所の中身(全回同じ): SeaWorld、Countdown Clock、ScienceCenter、Winter Market 01、Fountain of LifeDeath、Plaza of Transference
- 参考(月末): Commercial の週の収入 42,872 のうち Citizen 42,818、Tourism 54
- 参考(月末): `map_layer` attractiveness の平均 6(月初と同じ)、最大 157(2575, 1224)
