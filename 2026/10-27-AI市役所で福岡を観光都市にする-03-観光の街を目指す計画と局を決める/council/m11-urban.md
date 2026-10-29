# m11 住宅都市みどり局の案

## 案1: 電気の届く道沿いに公園を1か所足す(658,1400)

### 施策

- 案の id: urban-1
- 施策: 公園(Regular Park)を (658,1400) に東向きで置く。道は既存の Basic Road segment 15421 に入口でつなぐ。地区は直接の対象にしない
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `test_place_building` を、実行と同じ引数で再度呼ぶ(prefab "Regular Park"、x 658、z 1400、facing "east")。断られたら、下の予備候補を見ずに見送る
  2. `place_building`(prefab "Regular Park"、x 658、z 1400、facing "east")。pay は既定の true。建設費 1,000
  3. 置いたあと `buildings_near`(x 658、z 1400、radius 30、brief false)で、電気が来ているか(grid.electricity)と問題の印を確かめる
- 設置条件の確認:
  - `test_place_building`(Regular Park、658,1400、east): ok=true、placed=false、cost 1,000、enoughMoney true、entrance (690,1400) の道 segment 15421(距離14)、wouldDemolish 0、lostByDemolish 0(働き0、家0)
  - `map_layer`(electricity_service、x 710、z 1460、radius 120、n 5): z=1400 の行は x 590・650・710・770・830 すべて 1(電気が届く)。近い点 (650,1400) が 1 のため、(658,1400) も届くとみなす。実行後の `buildings_near` で確かめる
  - `net_near`(x 690、z 1400、radius 90、Electricity): 送電線は近くにない。電気は網の中の既存の線で届いている(`map_layer` の結果による)
  - 道路: `net_near`(x 710、z 1460、radius 160、Road): 入口の道 segment 15421(x 712、z 1350〜1424)は存在する。新しい道は引かない
- 接続工事: 不要(入口の道は既存の segment 15421。水・下水は要らない)
- 予備候補: なし。確認したほかの候補は使わない
  - `test_place_building` で通った (668,1460) と (752,1460) は、`map_layer` の z=1460 の行が電気 0 のため、電気が届かない見込み。使わない
- 中止する条件: 実行前の `test_place_building` が断る、または `map_layer`(electricity_service、x 658、z 1400、radius 10)が 0 を返す。そのときは案を見送る(別の場所は、この案の確認に入っていない)

### 期待する効果

- 改善の見込み: 4-2 の公園などの数を1つ増やす。公園は電気が届けば問題の印が付かず、4-2 の数に入る。確認した事実: 今の Beautification は 86 棟(`buildings_near` で全体を数えた)。電気の届く (658,1400) に1棟置けば、数は 87 になる(予想)
- 数値と期限: 4-2 は 86 → 87(予想)。期限は12か月目の月末(第11月末の見回りと、第12月の月例)
- 確認方法: `buildings_near`(service "Beautification"、brief true、x 0、z 0、radius 5000)の total。今の値 86 と同じ条件で比べる。加えて `buildings_near`(x 658、z 1400、radius 30)で、新しい公園の problems が None、grid.electricity が true であること
- 不確かな点: 数値は1棟の増え分だけで、目標 100 には届かない(予想: 12か月の末で 88 程度)。電気が届くかは、置いたあとに確かめる必要がある。量を見積もれるのは 4-2 の数だけ
- 試し: なし

### 費用

- 建設費: 1,000(`list_building_types` の Regular Park の cost)
- 週の維持費の増え分: 8(`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せる。公園は取り壊しの議案にしない。戻すときは、必要になれば `bulldoze`(公園だけ)で壊す。ただし、取り壊しには議決が要る。

### 前の月の答え合わせ

- 前の月の案 urban-1(10月、公園 (762,1368) 西向き、台帳 m10-urban-1)は採られ、実行できた(費用 1,000)。期限は第11月の初め。確かめた結果: 公園 19278 は problems None、電気が届いている。Beautification の数は 85(10/29、計画の値)→ 86(11/7、今月の `buildings_near` で全体を数えた)で +1。判定: 当たり。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たらない(重点は 5-1・5-2 観光、5-1・5-2(入口)、8-1。4-2 は、市の計画の目標を保つための案)

## 案なし

(案1を出すため、この見出しは書かない)

## 調査

- 調査: なし

## 見たもの

- `list_policies`: 政策名、有効状態、週の費用を確認。有効なのは SmokingBan(0)、BigBusiness(4,012)。週の政策費用は 10,812。RecreationalUse は active=false(0)。HighTechHousing は active=false で 20,252/週。SmallBusiness は active=false(317)。urban の数字(4-1、4-2)に効く政策は、HighTechHousing だけ候補として比べた(捨てたものを参照)
- `city_info`: 人口 179,848、所持金 2,313,772、週の収入 335,847、支出 325,167(収支 +10,680)、観光客 1,763(訪問 138)、幸福度 89、dialog なし
- `demand_breakdown`: 働き口 87,275(空き 2,602)、家 55,945(空き 5,080)、大卒の失業 9,227
- `land_value`: 街の平均 54
- `building_stats`: 住宅(高密度)の地価の平均 59(4,058 棟)
- `buildings_near`(x 762、z 1368、radius 400、Beautification、brief): 公園 6 棟(19278 は None、23298 は RoadNotConnected、30466 は電気の印)
- `buildings_near`(x 0、z 0、radius 5000、Beautification、brief): Beautification 全体 86 棟
- `buildings_near`(x 690、z 1460、radius 120): 近くの建物は 11580(電気の印)と 19278 のみ
- `zone_map`(x 700、z 1300、radius 400): 道 x=712 の西側と、斜めの道の北側に、空いた区画(unzoned)が見える。区画の色は付いていない
- `zone_map`(x 640、z 1380、radius 120): 空いた区画の位置を確かめた
- `net_near`(x 710、z 1450、radius 160、Road): 道 segment 968、13359、15421、24564、29045、34363、34548 を確認
- `net_near`(x 690、z 1400、radius 90、Electricity): 送電線はなし
- `test_place_building`: (668,1460) east、(752,1460) west、(658,1400) east、(766,1408) west、(668,1530) east、(612,1366) south、(754,1432) west、ParadoxPlaza (690,1372) east、Regular Plaza (735,1320) north。ok は (668,1460)、(752,1460)、(658,1400)。他は ObjectCollision
- `list_building_types`(service Beautification): 公園・広場・遊び場などの種類、費用、週の維持費、道の要否
- `map_layer`(electricity_service、x 710、z 1460、radius 120、n 5): 北の行(z 1580、1520、1460)は 0、南の行(z 1400、1340)は 1
- `map_layer`(electricity_service、x 750、z 1432、radius 30、n 3): z 1432 の行は 1、x 720 の z 1432 の点は 0(北の行 z 1462 が 0)

## 判断の根拠

- 4-2 は、今の 86 棟から目標 100 に届かない。電気が届き、道に面する空きが、確かめた範囲で (658,1400) の1か所だけだった。他の候補は、電気が z=1460 の行で届かないか、既存の公園や歩道にぶつかった
- 4-1 の高密度住宅(地価 59、目標 62)は、高密度住宅の近くの空きが取れなかった。残り1か月で地価に効く見込みが薄いため、事業3を見送った
- 政策の比べ: HighTechHousing は 20,252/週で、週の収支が +10,680 から −9,572 になる。守る線(+3,000)を大きく割るので採らない。SmokingBan は有効のまま。政策の変更は、urban の数字には効かない
- 案は1件。電気と道の条件を確かめた場所は1か所だけなので、予備を置かず、案を1件にする

## 捨てたもの

- 公園 (668,1460) east、(752,1460) west: 置ける(`test_place_building` が ok)が、`map_layer` の z=1460 の行は電気 0。電気が届かないため、実行の条件を満たせない
- 公園 (766,1408) west、(754,1432) west: 既存の公園 19278 と歩道にぶつかる(ObjectCollision)
- 公園 (668,1530) east: 取り壊し対象の StatueOfWealth 11580 にぶつかる(電気の印の名所。取り壊しは議決が要る)
- ParadoxPlaza (690,1372)、Regular Plaza (735,1320): 道と歩道にぶつかる
- 事業3(高密度住宅の近くの公園、地価の手): 高密度の空きが取れず、残り1か月で効く見込みが薄い(予想)
- HighTechHousing: 20,252/週で守る線を割る
