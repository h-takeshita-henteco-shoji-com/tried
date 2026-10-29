# m10 住宅都市みどり局の案

## 案1: 空き地に遊び場 Regular Playground を2棟(4-2 の公園などの数を増やす)

### 施策

- 案の id: urban-1
- 施策: 2棟の Regular Playground を、東の空き地(2845,600)と北の空き地(1655,-520)に置く。どちらも道路に面した空きを test_place_building で確かめた。取り壊しはなし
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building` prefab "Regular Playground"、x 2845、z 600、facing "north"、pay true(建設費 1,250。入口の道路 Basic Road segment 10928 が 4.8m)
  2. `place_building` prefab "Regular Playground"、x 1655、z -520、facing "east"、pay true(建設費 1,250。入口の道路 Medium Road segment 8836 が 11m)
  - 両方とも `test_place_building` で ok、wouldDemolish 0、lostByDemolish 0(jobs 0、homes 0)を確認済み
- 設置条件の確認:
  - (2845,600) facing north: `test_place_building` ok、入口の道路 10928(4.8m)、取り壊し 0。`map_layer` electricity_service(x 2845、z 600、r30、n3)の中心は 1。電気は届いている
  - (1655,-520) facing east: `test_place_building` ok、入口の道路 8836(11m)、取り壊し 0。`map_layer` electricity_service(x 1655、z -520、r30、n3)の中心は 1。電気は届いている
  - 水・下水は要らない(Regular Playground は電気だけ)
- 接続工事: 不要(入口の道路が 16m 以内にある)
- 予備候補: なし。どちらか1つが実行時に断られたら、その1棟だけ見送る(もう1棟は置く)。ほかの候補は下の「捨てたもの」に書いた理由で使わない
- 中止する条件: 実行前に `test_place_building` が ObjectCollision などで断ったら、その棟を見送る。入口の道路が 16m 以内に無いと出たら見送る。建設費の合計が 2,500 を超えたら見送る

### 期待する効果

- 改善の見込み: 4-2 の Beautification は 89 棟で、目標 100 まで 11 棟足りない。遊び場を2棟足すと 91 棟になり、目標への差が 9 になる。数の増えは置いた分だけ確実に出る(確認した事実)。地価は、近くの公園の効きとして 4-1 に少し効くと見込むが、量は見積もれない。
- 数値と期限: Beautification 数(`buildings_near` service Beautification)は 89 → 91(見込み)。期限は月末(2050-10-29 の見回り後)。地価(住宅(高密度)の平均、`building_stats`)は 59 → 目標 62。今月の効果は小さいと見て、判定は 12 か月後まで続けて見る
- 確認方法: `buildings_near`(x 2845、z 600、r150、service Beautification)と(x 1655、z -520、r150、service Beautification)で、置いた棟の problems が None であることを見る。`buildings_near` の Beautification 数を、置く前の 89 と比べる。`building_stats` の住宅(高密度)の averageLandValue を、置く前の 59 と比べる
- 不確かな点: 遊び場の地価への効きは、今の数では確かめられない(m07-2 の遊び場も地価は他の要因と切り分けていない)。観光の魅力度への効きは見込まない。12 か月の目標(Beautification 100)には、今月の2棟だけでは届かない
- 試し: なし

### 費用

- 建設費: 2,500(Regular Playground 1,250 × 2。`list_building_types` の Beautification の cost)
- 週の維持費の増え分: 48(Regular Playground の upkeepPerWeek 24 × 2)

### 戻せるか

戻せる。置いた遊び場は、必要になれば取り壊せる。ただし取り壊しは議決が要る。

### 前の月の答え合わせ

- m09-urban-1(Regular Playground (3190,-345)、m09-2 として採られ実行): 期限は 2050-09-29(9か月目の月末)。結果: Beautification 88 → 89(予想どおり +1)。置いた棟の problems は None、電気 true。周りの地価・魅力度は未測定。判定: 半分(数は当たり、地価は判定前)。
- m09-roads-1、m09-health-2 は urban の案ではないので、ここでは扱わない。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い、4-1 都市と自然が調和したコンパクトなまち
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2 観光、4-4 資源循環、6-4、7-1 企業の立地・地場企業)。ただし、4-2 の数と 4-1 の地価を前へ進める手として、方針の「重点の外の案も出してかまいません」に当たる

## 調査

- 調査: あり
- 問い: 人口減の中で、住宅の空き(emptyHomes)は見回りごとに減るか、増えるか、変わらないか。
- 見る道具と引数: (1) `demand_breakdown`(引数なし)の emptyHomes、homes、unemployed、emptyJobs。(2) `city_info`(引数なし)の population。(3) `building_stats`(引数なし)の住宅(高密度)の averageLandValue。
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 空き(emptyHomes)が 4,835 から見回りごとに減り、人口が増えれば、今の住宅の流れは戻るので、手を足さない。空きが 4,800 前後で動かず、人口が減り続けるなら、次の月に住宅(高密度)の周りの公園・地価を変える試しを出す(測る数は emptyHomes と人口)。空きが増え、住宅の地価が 59 から下がるなら、地価を上げる手(公園の置き場)を先に確かめる。
- 担当の問題: 4-1 都市と自然が調和したコンパクトなまち(住宅(高密度)の地価と、住宅の需要)

## 見たもの

- `city_info`: 人口 178,055、所持金 2,293,533、観光客 1,652/143、週の収支 +9,425(収入 351,699、支出 342,274)、需要 住宅 30 / 商業 2 / 工業 51、電気・水・下水が来ない市民 0 / 0 / 0
- `demand_breakdown`: 働き口 86,777、空き 3,656、家 55,802、空き 4,835、失業 5,196(大学卒 5,039)、homeless 0
- `land_value`: 街の平均 53
- `building_stats`: 住宅(高密度)の averageLandValue 59、住宅(低)48、事務所 59、商業(高)56。住宅(高密度)の放棄 6 棟
- `list_policies`: 有効なのは SmokingBan(0)、EducationBoost(7,940/週)、RecreationalUse(0)、BigBusiness(3,940/週)、SmallBusiness(309/週)。無効で費用が大きいのは HighTechHousing(20,236/週)、IndustrySpace(4,779/週)。Recycling(0、住宅税収を -5% と説明)は無効。urban の目標に効く新しい政策は、費用と税収減から見て今月は採らない。政策費用の合計 10,960/週
- `list_building_types`(service Beautification): Regular Park 1,000 / 8、Regular Playground 1,250 / 24、Regular Plaza 2,500 / 32、Expensive Plaza 12,000 / 120 ほか。すべて道路が要る
- `zone_summary`(grid 1000): 住宅(高密度)の空き 717 のうち、道路に面する空きは 0(emptyFacingRoad 0、残りは裏)。商業(高)は道路に面する空き 77、商業(低)17。住宅(低)の道路に面する空きは 0
- `buildings_near`(x 2795、z 1180、r250、service Beautification): 4 棟。Regular Park 19591(2795,1100)と 42155(2795,1260) は problems None。Regular Park 44507(2795,1180) は RoadNotConnected。Expensive Plaza 25283(2582,1222) は None
- `buildings_near`(x 2795、z 1100、r150、problems_only): 2 件。Garbage(15135、オフィス)と RoadNotConnected(44507)
- `net_near`(x 2795、z 1180、r120、Road): 道路は x=2850 の南北の Basic Road(node 8720 が (2850,1180))。公園 44507 の入口の向きは道路に面していない
- `test_place_building`(Regular Park、2795,1180、facing east と west、assume_removed_buildings [44507]): 両方とも ObjectCollision。園路の Pedestrian Gravel(segment 3177、5873、28143 が blocks true)が残る。公園 44507 の作り直しは、今の園路の扱いでは置けないため、案にしない
- `zone_map`(2500,600、r500)、(2750,650、r200)、(1500,-500、r250)、(-700,700、r250)、(3400,-400、r200): 空き地の場所を見た。(-700,700) は道路がなく空き地のみ。(3400,-400) は大きな建物の並びで、空きの帯は 15m 以下
- `test_place_building`(Regular Playground、2845,600、facing north): ok。入口の道路 10928(4.8m)、取り壊し 0、費用 1,250
- `map_layer`(electricity_service、x 2845、z 600、r30、n3): 中心の点は 1(9 点のうち 8 点が 1)
- `test_place_building`(Regular Park、2790,590、facing north): ObjectCollision。道路 segment 8314 と High School 15042(2795,598)
- `test_place_building`(Regular Playground、1655,-520、facing east): ok。入口の道路 8836(11m)、取り壊し 0、費用 1,250
- `net_near`(x 1690、z -520、r60、Road): Medium Road 8836 と 11011 が南北に通る
- `map_layer`(electricity_service、x 1655、z -520、r30、n3): 中心の点は 1
- `test_place_building`(Regular Playground、1600,-545、facing east): ok だが、入口の道路が 16m 以内に無い(road null)。採らない
- `test_place_building`(Regular Park、1600,-415、facing north): ObjectCollision。道路 2234、16485 と、オフィス 2634、14576、17349(取り壊し対象)
- `test_place_building`(Regular Playground、2962,650、facing west): 入口の道路が無い(road null)。取り壊しで住宅 2 棟(家 10)を失う。採らない
- `test_place_building`(Regular Playground、1880,-300、facing south): ObjectCollision。Fire House 7003 と道路 482、2399、19030
- `net_near`(x 2500、z 600、r120、Road): 道路は z=560 と z=650 の東西の Basic Road(区間 452、18127、24595 など)
- `zones_at`(x 2500、z 600、r120): オフィス 308(空き 4)、住宅(高)33(空き 7)、未指定 71
- `test_place_building`(Regular Playground、2500,605、facing north): ObjectCollision。Medical Clinic 34937(2480,630、blocks true)と事務所 11152、30263、46398。採らない

## 判断の根拠

- 4-2 の Beautification は 89 で、目標 100 まで 11 棟足りない。遊び場 1 棟は 1 棟の増えになり、確かめた設置条件(道路、電気、取り壊しなし)を通ったのは 2 地区だけ。そこで、この 2 棟を案にした。
- 候補地は 4 地区(東、北中央、中央の (2500,605)、北西の (1880,-300) など)で試した。東の (2845,600) と北の (1655,-520) は ok で、どちらも電気が届く。ほかは建物・道路の衝突か、入口の道路が無かった。3 地区以上で試したが、通ったのは 2 か所だけなので、案は 2 棟に絞った。
- 戻せるかは、建てた後の取り壊しで決まる。今月は取り壊しを含まない。
- 人口減の原因は、今の数では分からない。空きの住宅は道路に面していない裏の空きが多く、urban の手で新しく住宅を足す場所がない(emptyFacingRoad 0)。そこで、原因を見る調査を 1 件出し、案は 1 件にした。
- 案の数は 1 件。件数を埋めるための案は出さない。

## 捨てたもの

- 公園 44507 の道路接続の修復(RoadNotConnected): 作り直しは園路(Pedestrian Gravel)にぶつかって置けない(`test_place_building` の ObjectCollision)。道路の枝を引く案は、公園の入口の向きが確かめられないため採らない
- Regular Park(9×8、1,000 / 8)の候補: 2 か所とも断られた(1600,-415 は取り壊し、2790,590 は学校と道路)。Regular Park を置ける空きは、今月は確認できなかった
- Regular Playground(1600,-545): 入口の道路が 16m 以内に無く、道路を引く費用と操作が増えるため、今月は採らない
- Regular Playground(2962,650): 入口の道路が無く、住宅 2 棟(家 10)を取り壊す。取り壊しは議決が要り、戻せないため採らない
- Regular Playground(2500,605): 医療所と事務所に重なり断られた。ほかの候補がある中で、移す手間を増やすため採らない
- 装飾の岩や木(Boulder、Rock、Cliff 100 / 0)で Beautification の数を増やす案: 数だけを増やすもので、担当の目的(緑による潤い)に当たらないため採らない
- Expensive Plaza(12,000 / 120/週): 維持費が増え分の幅に収まるが、同じ 1 棟の効きに対し費用が大きいため採らない
- 住宅(高密度)の空きを埋めるための政策(Recycling、HighTechHousing、税の減税の政策): Recycling は住宅税収を -5% し週の収支が赤字になる見込み。HighTechHousing は 20,236/週で上限を超える。税の政策は税収減が大きく、黒字の守る線に触れるため採らない
