# m01 調査 s01-3(economy) 品物がない店の荷の道

## 月末 (2050-01-31)

- `cargo`: noGoods の buildings 219(hotspot (-1063,-755) が 69、(2221,775) が 46、(1086,328) が 29)。noResources 27。trucks 2,182、stoppedTrucks 798。Goods は import 986、local 433、止まり 500。(-1063,-755) の近くに貨物の駅・港はない。
- `net_near`(x=-1069, z=-770, radius=300, service=Road): 見回り1から道路の変更はしていない(同じ格子)。再取得は省いた。
- `traffic`(x=-1069, z=-770, radius=300, limit=5): flow 55、cars 312、blocked 31、congestion 120、averageDensity 60。busiest 5本の density は 100。blockedSpots は (-855,-728) が 14、(-929,-906) が 9。

## 見回り1 (2050-01-11)

- `cargo`: noGoods の buildings 232(hotspot (-1083,-767) が 75、(2212,741) が 46、(1098,297) が 33)。noResources 23。trucks 2,104、stoppedTrucks 809。Goods は import 923、local 422、止まり 516。stations のうち (-1083,-767) の近くに貨物の駅・港はない(最寄りは Cargo Harbor 1366 (-2000,605) と Cargo Center 40031 (-1780,-1605))。
- `net_near`(x=-1069, z=-770, radius=300, service=Road): 67区間。Basic Road と Small 4 Lane Road の格子で、(-920,-740) に Large Road with Median(3車線ずつ)、(-722,-740)〜(-796,-740) に Large Road がある。
- `traffic`(x=-1069, z=-770, radius=300, limit=5): flow 51、cars 294、blocked 33、congestion 101、averageDensity 53。busiest 5本の density は 100。blockedSpots は (-910,-727) が 21、(-1294,-651) が 10。
