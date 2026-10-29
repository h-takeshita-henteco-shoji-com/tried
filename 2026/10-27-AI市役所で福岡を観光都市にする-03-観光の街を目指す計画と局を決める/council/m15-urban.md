# m15 住宅都市みどり局の案

## 案1: 放棄された店の跡に JapaneseGarden を置き、公園を1つ増やす(1856,183)

### 施策

- 案の id: urban-1
- 施策: 放棄された店舗2棟(id 32056 ホテル 3×4、id 12473 店 2×3。ともに働き口0、家0、放棄)を取り壊し、その跡 (1856,183) に JapaneseGarden を東向きに置く。入口 (1872,183) は既存の Small 4 Lane Road(segment 5651、(1880,195)→(1880,150))に距離0で面する。道路は引かない。道具: `preview_bulldoze`、`bulldoze`、`place_building`
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `test_place_building`(prefab JapaneseGarden、x 1856、z 183、facing east、assume_removed_buildings [32056, 12473])で ok を確かめる
  2. `preview_bulldoze`(x 1856、z 183、radius 25、what "abandoned")で、壊す対象が 32056 と 12473 だけで、働き口0・家0であることを確かめる
  3. `bulldoze`(x 1856、z 183、radius 25、what "abandoned")で 32056 と 12473 を取り壊す
  4. `test_place_building`(prefab JapaneseGarden、x 1856、z 183、facing east)で、ok、wouldDemolish 0 を確かめる
  5. `place_building`(prefab JapaneseGarden、x 1856、z 183、facing east、pay 既定 true)。建設費 2,500
  6. `buildings_near`(x 1856、z 183、radius 30)で JapaneseGarden の grid(electricity、water が true)を確かめる
- 設置条件の確認:
  - `test_place_building`(JapaneseGarden、x 1856、z 183、facing east、assume_removed 32056): ok、angleUsed 270、cost 2,500、enoughMoney true、入口 (1872,183) の road は segment 5651 で距離0、wouldDemolish は 12473 の1棟(jobs 0、homes 0)、lostByDemolish は働き口0・家0
  - `preview_bulldoze`(x 1856、z 183、radius 25、what abandoned): 対象2棟(12473、32056)、lost jobs 0、homes 0、電気を失う建物0
  - `buildings_near`(x 1856、z 183、radius 30): 12473 と 32056 は abandoned true、grid の electricity、water とも true。近くの 3526(1856,212)は稼働中(働き口15)で、範囲外のため壊さない
  - `buildings_near`(x 2000、z 150、r400、abandoned=true): 放棄店の候補 15 棟を確認(FatalProblem)
- 接続工事: 不要(入口の道路は既存の segment 5651 に距離0、電気と水は両方とも来ている)
- 予備候補: なし。今月の試しで、ほかの7か所はすべて断られるか、失う働き口・家が0にならなかった(下の「判断の根拠」)
- 中止する条件: 手順2の preview で 32056 と 12473 以外の建物が出たら、取り壊さず中止する。手順1の test が ok でないとき、取り壊さず中止する。手順4の test が ok でないとき(取り壊した後に置けない)は、置かずに止めて、市長に報告する

### 期待する効果

- 改善の見込み: 4-2 の公園(Beautification)が1つ増える。JapaneseGarden の入口は道路に面し、電気と水が来る場所なので、公園として数えられると予想する。
- 数値と期限: 今の値は Beautification 89(`buildings_near`、2051-03-07)。予想は 90。期限は置いた後の月末(次の月例)
- 確認方法: `buildings_near`(x 1856、z 183、radius 30)で JapaneseGarden が出ること、grid の電気と水が true であること。`buildings_near`(service "Beautification"、x 0、z 0、radius 5000)の棟数が 89 から 90 に増えたこと
- 不確かな点: 公園の数は、置いた建物が完成してから数える。建設が遅れると、月末では増えないことがある。数値は確定ではない
- 試し: なし

### 費用

- 建設費: 2,500(`list_building_types`、JapaneseGarden)。取り壊しの払い戻しはない
- 週の維持費の増え: 40(同)。守る線の見込みは週の収支 +4,256 → +4,216(守る線 +3,000 の上)

### 戻せるか

戻せない。店舗2棟を取り壊すので、壊した建物は戻らない。

### 前の月の答え合わせ

前の月(14月)の案 urban-1(放棄店 39889 の跡に JapaneseGarden を (1856,306) に置く)は採られ、実行できた(id 39519)。期限は月末の Beautification で、88 から 89 に増えた。期待どおり1増えたので、当たり。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たる(重点3の 4-2 花や緑による潤い)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `city_info`: 人口177,176、所持金2,433,116、週の収支 +4,256(収入339,306、支出335,050)、観光客1,851、需要 住21/商4/工59、dialog なし
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(週7,940)、BigBusiness(週3,832)。無効のうち、4-1 と 4-2 に関係する政策は見当たらない。HighTechHousing は週20,260(守る線の余裕 1,256 を超えるので、採らない)。RecreationalUse、SmallBusiness は無効(0、313)。政策の一覧の効果に関する記述は、効果の実測値として扱わない
- `demand_breakdown`: 働き口 86,636(空き 2,937)、家 56,093(空き 5,478)、大卒の失業 7,229、失業 7,391
- `land_value`: 街の平均 54
- `building_stats`(街全体): 住宅(高密度)の地価の平均 60(目標62)、放棄の商業(高密度)147棟
- `zone_map`(x 2050、z 150、r 350): 区画の色を見た。画像は council/m15-zonemap-urban.jpg に保存した(下の注)
- `buildings_near`(x 2000、z 150、r 400、abandoned=true): 放棄店の候補 15 棟
- `buildings_near`(x 1856、z 183、r 30): 取り壊す2棟の確認
- `net_near`(x 2176、z 306、r 60)、`net_near`(x 2224、z 38、r 60)、`net_near`(x 1856、z 236、r 60): 道路の位置を確認
- `test_place_building`(JapaneseGarden、8か所): (2176,306)、(2224,38)、(1856,183)、(2176,222)、(2168,18)、(2176,-6)、(1856,236)、(2232,-166)。結果は下の「判断の根拠」
- `preview_bulldoze`(x 1856、z 183、r 25、what abandoned): 対象2棟、働き口0・家0
- `list_building_types`(service Beautification): JapaneseGarden 4×4、建設費 2,500、維持費 40、電気と水が要る

注: `zone_map` の `save_to` で、画像を council/m15-zonemap-urban.jpg に保存した。局の書いてよいファイルは案と計画だけなので、この画像は不要。実行前に消す。

## 判断の根拠

- 4-2 は Beautification 89 で、目標100まで11。12か月で1か月1つ(22月は2つ)の計画を続ける。今月は、放棄店の候補を8か所試し、条件を満たしたのは (1856,183) の1か所だけだった。ほかの7か所は、道路やサービスの建物に当たる、または働き口8〜15や家2〜19を失うため、取り壊しでは採れない。
- 案 urban-1 は、取り壊す2棟の働き口と家が0、入口の道路と電気・水が確認でき、費用も守る線の範囲内なので採った。
- 案は1件にした。候補が少ないため、2件目を作っても、同じ放棄店の候補を奪い合う。件数を埋めるための案は作らない。
- 週の収支は +4,216 の見込みで、守る線 +3,000 の上。4-2 以外の手(HighTechHousing など)は、週の費用が余裕を超えるか、4-1 の効きが見積もれないので、今月は採らない。

## 捨てたもの

- Regular Park(9×8、建設費 1,000、維持費 8): 計画では2100〜2250 の場所で道や電線に当たった。今月は試していない。候補が取れれば、次の月に試す価値がある。
- HighTechHousing(政策、週 20,260): 守る線の余裕 1,256 を超える。4-1 の地価への効きも確認できていない。
- 事業2の地価の測り(第16月に予定): 今月は予定にない。計画どおり第16月に測る。
- 放棄店の取り壊し(候補8か所のうち、取り壊しで働き口や家を失うもの): 働き口8〜15または家2〜19を失うので採らない。
