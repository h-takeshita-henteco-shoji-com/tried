# m01 経済観光文化局の案

## 施策

- 施策: 名所 Official Park を (1752, 518) に1棟置く。道具は place_building。名所は6棟から7棟になる。試しとして、名所1棟が attractiveness と観光客に効くかを測る
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順: `place_building(prefab="Official Park", x=1752, z=518, facing="north", pay=True)` を1回。置いた後、返り値の entrance.road が null でないことを確かめる
- 設置条件の確認: `test_place_building`(Official Park, 1752, 518, facing north)が ok=true。費用 45,000、入口 (1752, 542)、道路は Medium Road の区間 24321(距離2)、壊れる建物 0、失う家と働き口 0。`map_layer` の electricity_service と sewage_service を (1752, 518) 半径30で見て、3x3 の点がすべて 1(届いている)。`zones_at` (1735, 522) 半径60 は未指定のマス44(空き41)で、区画の建物は壊れない
- 接続工事: 不要(電気・下水が届いている。水は `water_trace` で網がつながっていることを確認)
- 予備候補: なし。z=526 から南は道路の区間 24321 とぶつかって断られた(確認済み)。西の (1660, 522) も道路とぶつかって断られた
- 中止する条件: 実行前の `test_place_building` が ok=false になる。入口の道路が null になる。壊れる建物が 0 でない。所持金が 45,000 に足りない

## 期待する効果

- 改善の見込み: 名所が増えると、その周りの attractiveness が上がり、観光客が増えると予想する。ただ観光客 1,646 人に対し Tourism の収入が 45 しかなく、原因は分からない。名所1棟でこの収入が増えるかは分からない
- 数値と期限: 名所の棟数 6 → 7(置いた直後)。attractiveness の最大 157 と平均 6 が上がるかを30日後までに見る。観光客(now 1,646)と Tourism の週の収入(45)は、数値は見積もれない
- 確認方法: `buildings_near`(x=0, z=0, radius=4000, service=Monument)の棟数。`map_layer`(attractiveness, n=9)の平均。`city_info` の tourists。`economy_breakdown` の Tourism
- 不確かな点: Official Park が観光の魅力を持つかは未確認。ゲームの時間が止まっているので、効果は時間が進んでから出る
- 試し: 試しである。仮説は「名所1棟を足すと、その周りの attractiveness が上がり、観光客が増える」。測る数は attractiveness の平均と (1752, 518) 周りの値、今いる観光客、Tourism の週の収入。場所は (1752, 518)。基準は 平均 6、観光客 1,646、Tourism 45。編成方針の「分からないこと」の1つ目(Tourism の収入が少ない原因)に関わる

これは局の予測です。ゲームの効果の正解を取得しません。

## 調査

- 調査: あり
- 問い: 観光客が 1,646 人いるのに Tourism の収入が 45 なのは、観光客が店に寄らないからか、数え方の問題か
- 見る道具と引数: `economy_breakdown`(引数なし)、`city_info`(引数なし)、`cargo`(引数なし)
- いつ見るか: 見回り1、見回り2、月末
- 何が分かれば次の手が決まるか: 観光客が増えても Tourism が 45 前後のままなら、数え方か店に寄らない問題とみて、翌月は商業の需要や品物がない店(中心 -1069, -770 の74棟)への手を出す。Tourism が増えるなら、名所を足す案を続ける
- 担当の問題: 5-1、5-2 観光

## 費用

- 建設費: 45,000(`test_place_building` の cost)
- 週の維持費の増え分: 128(`list_building_types` の upkeepPerWeek)

## 戻せるか

戻せない。置いた建物は払い戻しがなく、取り壊しには議決が要る。

## 前の月の答え合わせ

なし(1か月目)

## 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる

## 見たもの

- `city_info`: 観光客 1,646、visits 139、所持金 2,082,287、週の収支 +9,965
- `list_policies`: 比較した政策は BigBusiness(有効、週 3,876)、SmallBusiness(無効、週 315)、IndustrySpace(無効、週 4,821)。観光に直接効く政策は一覧に見当たらない。政策の効果は測れないので、今月は政策案にしない
- `economy_breakdown`: Tourism の週の収入 45、商業の収入 41,675、Monument の支出 2,280
- `cargo`: 品物がない店 228(-1069, -770 に74棟)、原料がない工場 24
- `list_building_types`(service=Monument): Official Park 45,000 / 週128、StatueOfWealth 25,000 / 週400、ほか
- `buildings_near`(service=Monument): 6棟(SeaWorld、Countdown Clock、ScienceCenter、Winter Market 01、Fountain of LifeDeath、Plaza of Transference)
- `map_layer`: attractiveness の平均 6、最大 157(2575, 1224)。electricity_service と sewage_service は (1752, 518) で 1
- `zone_map`: (-1350, -650) と (1800, 400) の半径500
- `net_near`: (-1230, -780) と (1780, 520)
- `test_place_building`: Official Park (1752, 518) は ok。Friendly Neighborhood (-1260, -785) は ok だが高密度住宅3棟(家63)が壊れるので外した。そのほかの座標は道路や建物とぶつかった
- `water_trace`: (1752, 518) 付近の水と下水の網はつながっている
- `zones_at`: (1735, 522) 半径60は未指定のマス44

## 判断の根拠

名所は6棟で目標10棟まで遠く、attractiveness の平均も 6 で目標 12 の半分である。Official Park は45,000で枠 520,000 の1割以下、維持費 128 で枠 5,000 に収まり、壊れる建物がない。効き目が分からないので、1棟だけの試しにし、同時に Tourism が 45 しかない原因を調査で追う。

## 捨てたもの

- Friendly Neighborhood (-1260, -785): 高密度住宅3棟、家63が壊れるため
- 名所を複数棟まとめて置く案: 確認できた敷地が1つだけで、効き目も未確認のため
- 政策の有効化: 観光に直接効く政策が一覧に見当たらないため
- 大型の名所(Stadium 200,000 など): 効き目が分からないうちは費用が大きく、週の維持費も 4,000 で枠を使い切るため
