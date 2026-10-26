# m02 住宅都市みどり局の案

## 施策

- 施策: 高密度住宅街の空き街区(西の通り沿い、座標 (2135,-322) と (2135,-365))に、Decoration Concrete Parking Lot 01(Beautification)を2棟置く。place_building で置く。
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building(prefab="Decoration Concrete Parking Lot 01", x=2135, z=-365, facing="west")`
  2. `place_building(prefab="Decoration Concrete Parking Lot 01", x=2135, z=-322, facing="west")`
- 設置条件の確認:
  - (2135,-365): `test_place_building` で ok、取り壊し 0、入口 (2119,-365)、道路 segment 32172 に距離1。
  - (2135,-322): `test_place_building` で ok、取り壊し 0、入口 (2119,-322)、道路 segment 13569 に距離1。
  - 電気: `map_layer`(electricity_service、中心 (2135,-365)、半径100、n=5)の25点が全部1。この建物は水・下水が要らない。
  - 敷地: `zone_map`(中心 (2200,-380)、半径150)で、2か所とも区画の指定がない空き地。
- 接続工事: 不要
- 予備候補: なし。(2135,-408) は壊れる建物が1棟(44025)あるため使わない。
- 中止する条件: 実行前の test_place_building が断る、または wouldDemolish が0でないなら、その1棟を見送る。

## 期待する効果

- 改善の見込み: 担当の 4-2 は、公園など(Beautification)の数が目標100に届かない。この案は数を2棟増やす。地価への効きは見込めるが小さいと予想する。
- 数値と期限: `buildings_near`(service=Beautification、全街)で今 81。予想は 83。期限は m02 の月末。
- 確認方法: `buildings_near`(service=Beautification)の total を同じ条件で数える。周辺の地価は `land_value`(中心 (2135,-345)、半径100)で比べる。
- 不確かな点: 駐車場の飾りが、公園と同じに周辺の地価を上げるかは確かめられていない。地価の変化は数値を見積もれない。目標100まで 17 棟足りず、この案だけでは届かない。
- 試し: 仮説は「Beautification の建物を街区の空きに置くと、周辺の地価が上がる」。測る数は `land_value`(中心 (2135,-345)、半径100)の average と Beautification の数。基準は Beautification 81、地価の average は実行前に市長が測る。編成方針の「分からないこと」の項目には当たらない。

これは局の予測です。

## 調査

- 調査: なし

## 費用

- 建設費: 2,000(test_place_building の cost 1,000 × 2)
- 週の維持費の増え分: 32(list_building_types の upkeepPerWeek 16 × 2)

## 戻せるか

戻せる。建物2棟は bulldoze で取り除けるが、建設費の払い戻しはない。

## 前の月の答え合わせ

- m01-urban(空き街区に行き止まりの道と公園4つ): 採られなかった。理由は公園の電気が未確認だったこと。今月は電気を `map_layer` で確かめ、道路を引かず既存の道路に面した敷地だけにした。公園(Regular Park)は、確かめた敷地に入らないか、周りの建物を壊すため、駐車場の飾りに替えた。

## 市の計画

- 当たる施策: 4-2 花や緑による潤い(4-1 の地価にも関わる)
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `list_policies`: 比較した政策は PowerSaving、WaterSaving、HighTechHousing(週の費用 20,252、有効でない)、Recycling(0、無効)、BigBusiness(3,888、有効)、EducationBoost(7,940、有効)。公園や地価に直接効く政策は見当たらず、維持費の枠5,000にも合わないため選ばない。
- `city_info`: 人口 178,643、所持金 2,107,542、週の収支 +6,569、需要 24/2/59
- `demand_breakdown`: 働き口 86,355、空き 3,273、家 55,345、空き家 4,926、失業 7,450(大学卒7,254)
- `building_stats`: 住宅(高密度)の地価の平均 58、高密度商業の放棄 110
- `list_building_types`: Beautification の建物。Regular Park は 1,000・週8、駐車場の飾り01は 1,000・週16。
- `zone_summary`: 空きマスは、ほぼすべて道の奥側で、建物は建たない。
- `zone_map`: (2500,-500) 半径500と、(2200,-380) 半径150。空き地を探した。
- `land_value`: (2500,-500) 半径500で average 51、min 25、max 74。
- `test_place_building`: 上の2か所は ok。Regular Park・Plaza・Playground は、道路にぶつかるか、周りの建物を2〜5棟壊す。
- `map_layer`: electricity_service は敷地周辺25点が全部1。
- `buildings_near`: (2135,-365) 半径120に Beautification は0。

## 判断の根拠

高密度住宅街は敷地が詰まり、公園は周りの建物を壊すか道路にぶつかる。壊さずに置けたのは、区画の指定がない小さな空き地2か所だけだった。そこに置けるのは駐車場の飾りで、4-2 の数を2棟増やす。地価への効きは確かめていないため試しとし、費用は2,000と維持費32に抑えた。

## 捨てたもの

- Regular Park を空き街区に置く: 空き地に入らず、周りの建物を壊す。
- Regular Plaza (2142,-365): 店2棟(3579、7209)を壊す。
- 駐車場の飾りを (2135,-408) に置く: 建物 44025 を壊す。
- 放棄された高密度商業110棟の取り壊し: 放棄の原因を確かめておらず、取り壊しは戻せない。調査も今月は出さず、経済観光文化局の担当と重なる。
- 住宅の税や政策の変更: 需要24は空き家4,926が主因で、税では動かないと見る。HighTechHousing は週20,252で枠5,000を超える。
