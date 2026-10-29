# m01 調査 s01-3(health) 死体の印の原因

道具: `vehicles_stuck`(kind="hearse", building=36841, limit=10)、`buildings_near`(x=2240, z=186, radius=300, problem="Death", brief=true, limit=20)

| ゲーム内の日付 | 霊柩車(屋外で数えた台数) | Blocked を含む台数 | 7日以上止まっている | Death の印(半径300) |
|---|---|---|---|---|
| 2050-01-11(見回り1) | 3 | 2 | 0(すべて 1日未満) | 3 棟(130、11280、48338) |
| 2050-01-21(見回り2) | 2 | 2(うち Congestion 1) | 1(車 1526 が 10日) | 1 棟(11280) |
| 2050-01-31(月末) | 5 | 4(うち Congestion 1) | 2(車 1526 が 20日) | 2 棟(11280、44015) |

- 車 1526 は 3 回とも同じ目的 11280 へ向かい、blockCounter 68 → 24 → 76 で止まったまま。
- 月末の `services`: deathcare capacity 24000、used 12873、full 0。
- 月末の `complaints`: Death 38 棟(月初 52)。
