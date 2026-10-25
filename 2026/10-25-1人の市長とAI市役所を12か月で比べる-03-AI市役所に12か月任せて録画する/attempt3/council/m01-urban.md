# m01 住宅都市みどり局の案

## 施策

- 施策: 4-2 の公園などを2棟増やす。JapaneseGarden を (2134,-320) と (2134,-365) に置く。place_building を使う。
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building(prefab="JapaneseGarden", x=2134, z=-320, facing="west", pay=true)`
  2. `place_building(prefab="JapaneseGarden", x=2134, z=-365, facing="west", pay=true)`
  - 戻り値の entrance.road が null でないこと、ports や needs の電気・水が来ていることを見る。
- 設置条件の確認:
  - `zone_map`(2150,-340,r100): 2134 付近は幅32m×高さ40mの空き区画が南北に並ぶ。(2134,-320) と (2134,-365) の区画は空き。3つ目 (z=-410) は南端に住宅があり使わない。
  - `zones_at`(2134,-365,r18): 区画マス16、すべて Unzoned で空き。建物なし。
  - `buildings_near`(2140,-340,r70): この区画に建物なし。最も近い建物は西 2094 と東 2168 より外。
  - `net_near`(2140,-340,r80,Road): 西側 x=2110 に Basic Road(z -300〜-345、-345〜-390)。入口は西向きでここに面する。
  - `map_layer`(electricity_service): 2080〜2200 × -400〜-280 の25点すべて電気あり。
  - `water_trace`(2134,-320): 近くの建物で water/sewage ともに届いている。garden の water 要否は list_building_types で electricity と water が要る。
  - 大きさ: `list_building_types` で JapaneseGarden は 4x4 マス(8m で 32m×32m)。Regular Park は 9x8 マスで、既存公園(3250,482)の zone_map の枠も約72m×64m。ここの区画には入らないので使わない。
- 接続工事: 不要
- 予備候補: なし(同じ条件を確認できた場所は2か所だけ)
- 中止する条件: 戻り値の entrance.road が null のとき。reasons で断られたとき。water や electricity が未接続の警告が出たとき。

## 期待する効果

- 改善の見込み: 4-2 の公園など(Beautification)の数が2棟増える。目標100に対し大きさは小さく、単独では届かない。
- 数値と期限: `buildings_near` の Beautification 数。今81。予想は83。実行直後に確かめる。12か月後の目標100には、今月の2棟だけでは足りない。
- 確認方法: `buildings_near(x=2140,z=-340,radius=1500,service="Beautification")` の total を、実行前の値と比べる。
- 不確かな点: 周りの地価(4-1)への効きは数値を見積もれない。2棟では住宅(高密度)の地価の平均(58)は動かないと見る。数の増え方は今の count の定義(岩・崖を含むか)に依存し、81 の内訳は未確認。
- 試し: なし

## 調査

- 調査: なし

## 費用

- 建設費: 5,000(JapaneseGarden 2,500 × 2)
- 週の維持費の増え分: 80(40 × 2)。週の収支 +9,965 に対し約0.8%。収支の見積もりは +9,885。

## 戻せるか

戻せる。置いた庭はあとで取り壊せるが、費用の払い戻しはない。

## 前の月の答え合わせ

なし(1か月目)

## 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `list_policies`: 取得済み。有効は EducationBoost 7,940、BigBusiness 3,876 のみ。ほか HighTechHousing 20,248、IndustrySpace 4,821、SmallBusiness 315 など。地価・公園に直接効く政策は一覧になく、維持費の幅5,000を超えるものもある。比較の結果、案は建設にした。
- `demand_breakdown`: 家55,253、空き家4,935、働き口86,175、失業7,911
- `list_building_types`: Beautification の大きさ・費用・維持費
- `building_stats`: 住宅(高密度)の地価の平均58、4,057棟
- `zone_summary`: 空きマスの分布
- `zone_map`: (2500,-500)r500、(2830,-62)r100、(3250,482)r100、(2150,-340)r100
- `zones_at`: (2140,-340)r40、(2134,-365)r18
- `net_near`: (2140,-340)r80 Road
- `buildings_near`: (2140,-340)r70、Beautification r1500
- `map_layer`: electricity_service (2140,-340)
- `water_trace`: (2134,-320)

## 判断の根拠

重点の外だが、担当の4-2は81で目標100から遠い。公園類は大きく、街は埋まっていて、72m×64mの Regular Park が入る空きは確認できなかった。32m角に入る JapaneseGarden を、条件を確認できた2か所に絞った。費用は枠内で、効果は小さい。

## 捨てたもの

- Regular Park(1,000): 72m×64mの空きを確認できず、置ける場所がない。
- 岩・崖(100 前後、維持費0): 数は稼げるが、花や緑の潤いにならない。また空き地の条件を確認できていない。
- HighTechHousing 政策(週20,248): 維持費の幅5,000を超える。
- 住宅の地価を上げる手(4-1): 地価を直接上げる政策や手が見つからなかった。
