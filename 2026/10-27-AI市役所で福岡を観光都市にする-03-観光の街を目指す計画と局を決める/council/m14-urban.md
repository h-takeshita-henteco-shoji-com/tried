# m14 住宅都市みどり局の案

## 案1: 放棄された店の跡に JapaneseGarden を置き、公園を1つ増やす(西の道沿い)

### 施策

- 案の id: urban-1
- 施策: 放棄された店 39889(H3 4x4 Shop17_c、(1856,306))を取り壊し、同じ場所に JapaneseGarden を東向き(入口 (1872,306) が道 segment 26867 に面する)で置く。4-2 の公園を88から89にする
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `bulldoze(x=1856, z=306, radius=10, what="abandoned")` で、放棄された店 39889 を取り壊す。この円の中で取り壊されるのは 39889 だけ(`preview_bulldoze` の radius 10 で確認)
  2. `test_place_building(prefab="JapaneseGarden", x=1856, z=306, facing="east")` を、取り壊しの後にもう一度試す。ok と wouldDemolish 0 が出ることを確かめる
  3. `place_building(prefab="JapaneseGarden", x=1856, z=306, facing="east", pay=true)` で置く(建設費 2,500)
  4. 道路は引かない。入口の道は既存の Small 4 Lane Road(segment 26867)で、入口から距離 0
- 設置条件の確認:
  - 39889 の敷地: `buildings_near`(radius 120)で abandoned=true、problems は NoGoods, FatalProblem。電気・水・下水の grid は、いずれも true
  - 取り壊しの損失: `preview_bulldoze`(x 1856、z 306、r 10)で、働き口0、家0
  - 置く試し: `test_place_building`(JapaneseGarden、x 1856、z 306、facing east、assume_removed_buildings [39889])で ok。cost 2,500、enoughMoney true、wouldDemolish 0、入口の道 segment 26867 の距離0
  - 水と下水: `water_trace`(1856,306)で、セルの水と下水が true、水の網に取水口と排水口がつながる。JapaneseGarden は下水が要らない
  - 道路のつながり: `net_reach`(1856,306、r 60)で、道路の notEnterable 0、notLeavable 0、建物の notReachable 0
- 接続工事: 不要(入口の道は既存)
- 予備候補(使う順。取り壊しの議決は、予備の分も含めて1件ずつ取る):
  1. JapaneseGarden(2160,102)東向き。取り壊しは 48785(放棄、働き口0)と 14008(稼働中の店、働き口8)。`test_place_building`(assume_removed_buildings [48785])で ok、入口の道 segment 15869 の距離 8。電気と水は、この場所では未確認(`water_trace` で確かめてから使う)
  2. JapaneseGarden(1856,183)東向き。取り壊しは 32056(放棄、働き口0)と 12473(稼働中の店、働き口10)。`test_place_building`(assume_removed_buildings [32056])で wouldDemolish 12473 の ok。電気と水は未確認
- 中止する条件: 取り壊しの後に `test_place_building` が断る(ObjectCollision など)か、wouldDemolish が1件以上出たら、置かずに予備候補1へ移る。電気か水が来ないと `buildings_near` の grid で分かったら、置かない

### 期待する効果

- 改善の見込み: 4-2 の公園(Beautification)が1つ増える。JapaneseGarden の入口が道に面し、電気と水が来ているので、置けば公園として数えられると予想する。4-1 への効きは、この1か月では見積もれない
- 数値と期限: Beautification は 88(`buildings_near` の service Beautification の total、確認済み)。第14月末に89になると予想する(確かな予想)。4-1 の住宅(高密度)の地価は、今 60(基準)。数値は見積もれない
- 確認方法: `buildings_near`(x 0、z 0、radius 10000、service Beautification、brief)の total を、第14月末に88と比べる。地価は事業2の `land_value`(2168,194)で、第16月に測る
- 不確かな点: 取り壊しの議決が通ること。西の場所は、東の高密度住宅の地価の基準(2168,194)から離れているため、4-1 への効きは確かめにくい。維持費は週 40 増える
- 試し: なし

### 費用

- 建設費: 2,500(`list_building_types` の JapaneseGarden)。取り壊しは費用なし(`bulldoze` の払い戻しなし)
- 週の維持費の増え分: 40(`list_building_types` の upkeepPerWeek)。置いた後の週の収支の見込みは約 +3,880(今 +3,922)。守る線 +3,000 の上

### 戻せるか

戻せない。取り壊した建物は元に戻せないため。

### 前の月の答え合わせ

前の月(第13月)の案 urban-1(放棄された店の跡に JapaneseGarden を置く、(2168,194))は採られ、実行できた。期限は第13月末。`buildings_near` の Beautification は、第13月の初めの 87 から 88 に増えた(確認済み。`buildings_near` の JapaneseGarden 12077 が grid で電気・水が true)。期待の1増えたので、当たり。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たらない(編成方針の重点は 5-1・5-2、8-1、6-4・7-1)。ただし、市の計画の目標 4-2 を進める案で、局の担当に当たる

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口 178,202、所持金 2,419,253、週の収支 +3,922(収入 338,692、支出 334,770)、幸福度 88、需要 住19/商2/工61、来ない市民 0/0/0、観光客 1,847(訪問 143)、dialog なし
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(3,948)。住宅に関係する HighTechHousing は無効で、週 20,272(週の収支 +3,922 では置けない)。ほかの政策は無効、または費用0で、4-1・4-2 に当たるものはない。policyExpensesPerWeek 10,594
- `buildings_near`(x 2170、z 250、r 120、brief なし): 放棄された建物 31399 を含む。ほかは稼働中の店と住宅。grid は、放棄されない建物はすべて電気・水・下水が true
- `buildings_near`(x 2168、z 194、r 400、abandoned=true、brief): 放棄された店12、ホテル2を含む(NoGoods, FatalProblem)。候補の一覧にした
- `buildings_near`(x 0、z 0、r 10000、service Beautification、brief、limit 3): total 88(確認済み)
- `buildings_near`(x 2160、z 470、r 80、brief): 放棄された店 35594、40203、ホテル 23062 の位置を確認
- `building_stats`(x 2168、z 194、r 200): 住宅(高)の平均地価 72(近く)、事務所以外の放棄された店 4
- `land_value`(x 2168、z 194、r 200): 平均 65、街の平均 54
- `zone_map`(x 2150、z 200、r 300、size 700): 道と、放棄建物の空き。保存先 council/m14-urban-map-east.jpg(下の注)
- `demand_breakdown`: 働き口 87,129、空き 2,892、家 56,085、空き家 5,322、大卒の失業 8,506
- `net_near`(x 2170、z 250、r 120、service Road): 道路 segment 26867(西の入口の道)などを確認。x 2200 の Medium Road(中心)は 2100〜2250 の候補に当たる
- `list_building_types`(service Beautification): Regular Park 9×8 1,000/8、JapaneseGarden 4×4 2,500/40、Regular Playground 5×5 1,250/24、Tropical Garden 6×6 6,500/104 など。岩の装飾は100/0
- `test_place_building`: 9件を試した。JapaneseGarden (1856,306) east、(1856,183) east、(2160,102) east、(2160,18) east、(2176,306) north、(2224,38) west、(2136,560) south、(2128,446.7) west、(2180,-138) east、Regular Park (2168,40) north
- `preview_bulldoze`: (1856,306) r10 は 39889 だけ、働き口0、家0。(1856,183) r10 は 32056 だけ、働き口0、家0
- `water_trace`(1856,306): セルの水と下水が true。水の網(2,445区間)に取水口と排水口がつながる
- `net_reach`(1856,306、r 60): 道路と建物はすべて届く

## 判断の根拠

- 4-2 は 88 で、目標 100 まで12。第14月に1つ置く計画で、JapaneseGarden が唯一、道と電気・水を確かめて置けた
- 2100〜2250 の帯の放棄店の跡は、道路(x 2200)と稼働中の建物に当たり、Regular Park も置けなかった。候補を x 1800〜2250 に広げ、(1856,306) を選んだ。取り壊しで失うものは0
- 維持費は週 40 増え、守る線 +3,000 を割らない。議決は取り壊しの1種類

## 捨てたもの

- JapaneseGarden (2176,306): 道 segment 31201 に当たり、稼働中の住宅 17474(家2)と店 3442(働き口11)に重なる。取り壊しで家を失うため捨てた
- JapaneseGarden (1856,236): 取り壊しで働き口25、家2を失う。失う家が0の条件に合わない
- JapaneseGarden (2160,18): 取り壊しで働き口18を失う。1か所10以下の条件を超える
- JapaneseGarden (2224,38): 火葬場 31990 と道に当たる
- JapaneseGarden (2136,560)、(2128,446.7)、(2180,-138): 道か公園 46934 に当たる。電気と道は確かめた上で捨てた
- Regular Park (2168,40): 道 segment 4243、7298、32407 と、電線に当たる
- Tropical Garden 6×6、6,500/104: 維持費が週 104 と重く、今月の4-2の1か所には見合わない
- Regular Playground 5×5、1,250/24: 遊具の公園で、花や緑の趣旨が薄い。今月は使わない
- 岩の装飾(Rock Formation など、100/0): 数だけ増えるが、花や緑による潤いの趣旨に合わないため、捨てた
- HighTechHousing(政策、週 20,272): 住宅の地価に効く見込みはあるが、週の収支が負になるため捨てた
- 税の変更(TaxLowerResHigh など): 地価への効きを確かめられず、税は財政局の担当のため、この案では出さない
