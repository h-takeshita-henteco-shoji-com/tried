# m01 経済観光文化局の案

## 案なし

案なし。検討した候補と根拠は次のとおり。

- 観光の名所(Monument)の候補は、道路に面した空きで試した。SeaWorld と Official Park は、道路や建物と重なって置けなかった。Friendly Neighborhood の1候補は、商業の取り壊しで働き口を50失うため除いた。もう1候補は、道路に面していなかった。実行条件を満たす配置が1つも確認できていない。
- 品物がない店 228 の原因とみられる貨物駅 28755 の出口は、道路の拡張を試した。Large Road は勾配の上限と建物との重なりで不可だった。直す手が確認できていない。
- 原因が未確定の問題は、施策ではなく調査で確かめる。

## 調査

- 調査: あり
- 問い: 貨物駅 28755 の敷地で止まるトラック(WaitingSpace)は、時間がたっても減らないか。
- 見る道具と引数: `vehicles_stuck` の kind=truck、building=28755、limit=30 と、`cargo`(引数なし)
- いつ見るか: 見回り1、月末
- 何が分かれば次の手が決まるか: WaitingSpace が続くなら、貨物駅の出口を別の道路につなぐ案を次月に検討する。減るなら詰まりは一時的とみて、品物がない店の別の原因(店と工場の距離)を調べる。
- 担当の問題: 6-4、7-1 企業の立地・地場企業 の「品物がない店」、8-1 物流・人流のゲートウェイ

## 見たもの

- `city_info`: 観光客 1,646、visits 139、所持金 2,082,287、週の収支 +9,965、電気・水・下水が来ない市民 0 / 0 / 0
- `economy`: 税は住宅(低)9、住宅(高)7、商業(低)9、商業(高)3、工業3、事務所3。予算は医療・ごみ・警察・公園・バスが150
- `economy_breakdown`: Tourism の収入 45、政策の費用 10,665
- `demand_breakdown`: 働き口 86,175、空き 3,215
- `cargo`: 品物がない店 228、原料がない工場 24、貨物駅 28755 の敷地で止まったトラック 492
- `building_stats`: 事務所レベル3 は 3,227
- `buildings_near`(Monument): 6棟。visitors は 8 から 37
- `map_layer`(attractiveness): 平均 6、最大 157(2575, 1224)
- `complaints`: 品物がない店 228、死亡 52、汚染 32、ごみ 15、火事 4、犯罪 3、騒音 7
- `list_policies`: かかっている政策は EducationBoost(週 7,940)と BigBusiness(週 3,876)。RecreationalUse は週 0 で、効果は未確認
- `list_building_types`(Monument、Beautification): SeaWorld 20,000 / 320、Official Park 45,000 / 128、Regular Park 1,000 / 8、Regular Plaza 2,500 / 32
- `list_net_types`(Road): Large Road 10,000/km、維持費 120/km/週
- `vehicles_stuck`(building 28755): 589台。WaitingSpace 492
- `test_place_building`: SeaWorld 4候補、Official Park 3候補、Friendly Neighborhood 3候補を試した。通ったものは取り壊しを伴うか入口の道路がなく、実行可能な候補はなし
- `test_upgrade_road`(Large Road、貨物駅の出口): SlopeTooSteep と ObjectCollision で不可
- `net_near`(3449, -1555、半径200): 貨物駅 28755 と道路の接続を確認
- `zones_at`(2880, 870 ほか): 空きは未区画(Unzoned)のみ。事務所と住宅の敷地に空きなし
- `zone_summary`(grid 1000): 商業(高)の空きのうち道路に面するのは 156 マス

## 判断の根拠

- 観光の収入が低い理由は、名所が事務所の多い地区にあり、観光客の消費先が少ないためとみられる。ただし、これは未確認の仮説。
- 名所を置く候補は、道路に面した空きがなく、試せる配置が残っていない。実行条件を確認できないため、案は出さない。
- 物流は、貨物駅 28755 の出口道路の拡張が勾配と建物の重なりでできないため、直す手がない。原因を確かめるため、調査を1件出す。
- 案の数は0件。実行条件を確認できた案がないため。

## 捨てたもの

- 観光の名所(SeaWorld、Official Park、Friendly Neighborhood): 道路や建物と重なる、取り壊しで働き口を失う、入口の道路がない。いずれも実行条件を満たさない。
- 貨物駅 28755 の出口道路の拡張(Large Road): 勾配の上限と建物との重なりで不可。
- 政策 RecreationalUse: 週の費用は0と見えるが、効果が確認できない。試しにするには測る数と基準が要るため、今月は出さない。
- 政策 SmallBusiness(週 315): 商業の店を増やす効果は見込みにとどまるため、今月は出さない。
