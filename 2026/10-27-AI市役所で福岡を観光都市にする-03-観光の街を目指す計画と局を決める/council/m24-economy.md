# m24 経済観光文化局の案

## 案なし

案なし。担当の数字(観光客 2,011、訪問 179、Tourism 週 89)を動かす手で、場所と実行条件が確認できたものがない。

- 旅客の入口(駅・港・空港): 港湾空港局の案がなく、入口は24月末まで0のまま。計画の調整6に従い、入口なしの計画に切り替えた。
- 名所: 週320以下の未建設の名所はない。ScienceCenter と Servicing Services は建設済みで置けない(test_place_building: AlreadyExists)。残る名所は60,000以上で週960以上。道路沿いの空きは市全体で17マスしかなく(zone_summary の emptyFacingRoad)、候補 (1856,-132)(放棄店 11517 を取り壊す前提)、(2176,256)(放棄店 18733 を取り壊す前提)は道と建物に重なり置けない。
- 峰の2棟目の公園: 1棟目(29231)の Visitors は 11 だが、街全体の訪問は 179 のまま。候補 (1880,305)、(1770,315) は道と重なり置けない。

## 調査

- 調査: なし

## 見たもの

- `city_info`: 観光客 2,011(訪問 179)、所持金 2,697,883、週の収支 +6,823、人口 172,273、幸福度 87
- `list_policies`: 観光に直接かかる政策はない。SmallBusiness は無効(週 319。m02-4 で効きは分からないまま)。BigBusiness は有効(週 4,008)。政策の週の費用の合計は 10,877
- `economy_breakdown`: Tourism 週 89(収入)、Monument 維持費 3,448、Beautification 維持費 7,980
- `buildings_near`(Monument、(1830,330) 半径 300): Countdown Clock、Fountain of LifeDeath の2棟
- `buildings_near`((1862,360) 半径 150): 公園 29231 は Visitors 11、Tourists 3。周りの公園は 18474 が 11、31332 が 12、39519 が 20、46572 が 15
- `map_layer`(attractiveness、(1830,330) 半径 400、n=9): 平均 19、最大 297(1830,330)
- `list_building_types`(Monument、Beautification): 未建設の名所は Grand Mall 85,000 / 週 1,280、Transport Tower 60,000 / 週 960、Stadium 200,000 / 週 4,000 など。Beautification の JapaneseGarden は 4x4、2,500 / 週 40
- `test_place_building`: Official Park、Plaza of Transference、ScienceCenter、Servicing Services は AlreadyExists(建設済み)。Grand Mall は (1477,-3148) で ok だが道路がない。Grand Mall は (1800,418)、(1745,340)、(2180,-60)、(2332,-97)、(2130,-310) で ObjectCollision。Grand Mall は (1856,-132) を取り壊す前提でも ObjectCollision。Transport Tower は (2176,256) を取り壊す前提でも ObjectCollision。JapaneseGarden は (1880,305)、(1770,315) で ObjectCollision
- `net_near`((1800,320) 半径 70): 道は z=330 の東西道と x=1770 の南北道
- `zone_map`((1830,330) 半径 250、(2150,-120) 半径 200): 道路沿いの空きは少なく、大半は建物で埋まる
- `zone_summary`(grid 1000): 道路沿いの空き(emptyFacingRoad)は CommercialHigh の 17 マスだけ
- `buildings_near`(abandoned、(1830,330) 半径 500): 放棄された店 10 棟以上(例: 11517 (1856,-132)、18733 (2176,256))

## 判断の根拠

- 前の月の答え合わせ(m23-economy-1、峰の公園1棟、試し): 半分。公園 29231 の Visitors は 11 で、予想の 10〜15 に入った。一方、街全体の訪問は 179 のまま、Tourism は 130 から 89 に下がった。公園の効きは1棟の周りに限られ、街全体の観光客は動かなかった。前月の調査ファイル(m23-survey-economy.md)はない。
- 入口は24月末まで0。計画の期限のため、入口の事業を閉じ、入口なしの計画に切り替えた(調整6)。
- 名所は、未建設の名所がすべて計画の週320を超えるため、上限を見直した(plan-economy.md の計画の変更)。ただし場所が確かめられていないので、実行はしない。
- 2棟目の公園は、1棟目の効きが街全体に出ず、候補2か所も置けないため、閉じた。
- 案の数は0。確かめた候補は、置ける場所も実行条件も残らなかった。

## 捨てたもの

- 名所 Transport Tower(60,000 / 週 960)と Grand Mall(85,000 / 週 1,280): 取り壊しなしの空きが道沿いになく、放棄店を壊す前提でも道と建物に重なる。週320の上限も超える。
- 峰の2棟目の公園: 候補 (1880,305)、(1770,315) が道と重なり置けない。1棟目の効きも街全体には出ていない。
- SmallBusiness の再試し: m02-4 の結果が分からないまま。今月の Tourism 89 で効きを示す新しい数字がない。
