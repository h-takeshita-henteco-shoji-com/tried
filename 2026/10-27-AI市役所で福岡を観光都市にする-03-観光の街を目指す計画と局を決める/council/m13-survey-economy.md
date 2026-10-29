# m13 調査結果(economy)

## s13-1 名所 40850 の訪問と観光客

道具: `buildings_near`(x 1580, z -530, radius 20)、`city_info`

| ゲーム内の日付 | 区切り | 40850 の problems | Visitors last week | Tourists last week | 今いる観光客(訪問) |
|---|---|---|---|---|---|
| 2051-01-06 | 基準(実行後、見回りの前) | RoadNotConnected | 5 | 1 | 1,765(132) |
| 2051-01-16 | 見回り1(調査の対象外。city_info のみ) | - | - | - | 1,788(134) |
| 2051-01-26 | 見回り2 | RoadNotConnected | 5 | 2 | 1,742(140) |
| 2051-02-05 | 月末 | RoadNotConnected | 5 | 2 | 1,847(143) |

- 道は Basic Road (1703,-536)→(1640,-530)。終点 (1640,-530) は connectedTo none。名所の中心 (1580,-530) との距離は 60m
- 電気・水・下水は3回とも true
