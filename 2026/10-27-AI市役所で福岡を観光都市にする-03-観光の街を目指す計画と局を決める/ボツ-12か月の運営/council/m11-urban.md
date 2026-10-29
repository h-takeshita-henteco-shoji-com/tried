# m11 住宅都市みどり局の案

## 案なし

今月は、4-2(公園など Beautification 91 → 目標100)と4-1(住宅(高密度)の地価 59 → 目標62)に効く案を、実行できる形にまで確認できなかった。

- 検討した候補: Regular Playground(5x5)と Regular Plaza(5x5)を、既存の空き店舗の撤去つきで、または空きに、計8か所で試した。
- 結果: 7か所は ObjectCollision で断られた(道路、高層住宅、事務所、学校、墓地などとぶつかった)。
- 残った2か所も実行条件が残る: (-600,-600) の Regular Plaza は ok=true だが、道路が半径80m内にない(net_near の結果 0区間)。(1200,-200) の Regular Playground は ok=true だが、入口の道路が見つからず(road=null)、撤去の対象に事務所2棟(働き口32)が入る。
- 必須の接続(道路への面)が確認できた場所が1つもないため、案の対象にできない。
- 1つでも確認できる候補を見つけるまで、実行対象には含めない。

## 調査

- 調査: あり
- 問い: 住宅(高密度)の地価は、近くに置いた公園や遊び場で上がるか。m10 に置いた遊び場の周りで、地価が上がるかを確かめる。
- 見る道具と引数: `map_layer` type=landvalue、x=2845, z=600, radius=150 と x=1655, z=-520, radius=150(m10 の基準は 64 と 53)。`building_stats` で住宅(高密度)の地価の平均(基準は 59)。
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 2地点の平均が基準より上がり続けるなら、遊び場を地価の低い住宅地に置く案を次月に出す。動かないなら、地価を上げる手を別に探す(4-1 の手は保留)。
- 担当の問題: 4-1 都市と自然が調和したコンパクトなまち、4-2 花や緑による潤い

## 見たもの

- `city_info`: 人口 176,967、所持金 2,333,385、週の収支 +9,588、観光客 1,645 / 訪問 149、幸福度 86、需要(住宅 31・商業 4・工業 52)
- `demand_breakdown`: 空き家 4,877、働き口 86,923(空き 4,018)、大学卒の失業 4,824
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940/週)、RecreationalUse(0)、BigBusiness(3,924/週)、SmallBusiness(313/週)。政策費用は合計 11,006/週。Recycling は直接の費用 0 だが、住宅の税収を約 13,000/週減らすため採らない。HeavyTrafficBan は費用 0 で、今月の課題に当たらない
- `building_stats`: 住宅(高密度)地価 59(4,060棟、放棄 12)、住宅(低)地価 48、事務所 L3 3,284棟
- `land_value`: 街の平均 54
- `list_building_types`(Beautification、解禁済み): Regular Park 1,000 / 8 週、Regular Playground 1,250 / 24 週、Regular Plaza 2,500 / 32 週(電気が要る)、ParadoxPlaza 1,000 / 16 週(水・下水が要る)、JapaneseGarden 2,500 / 40 週(水が要る)
- `zone_summary`(grid 1000): 住宅(高密度)の空き 717 はすべて道路に面していない(emptyBehind)。事務所の空き 1,633 も同様
- `zone_map`(2600,300 r700、2500,-450 r350、500,-500 r300、2140,-100 r120、2150,710 r100、-1300,-500 r250): 灰色の部分の多くは学校、墓地、警察、火葬場などの施設で、空き地ではなかった
- `net_near`(2200,-100 r120 Road): 2200 の南北の中型道路、-30 と -120 の東西の小型道路。(-600,-600) r80 の Road は 0 件
- `buildings_near`(abandoned=true、2500,300 r1200、brief): 56棟。大半は品物がない店(NoGoods)の店舗
- `test_place_building`(すべて test のみ。何も置いていない):
  - Regular Park (2520,-440): ObjectCollision(University 17574、H5 高層 12081・12264・17016)
  - Regular Park (2340,-325): ObjectCollision(Basic Road 593・20299、小学校 37622)
  - Regular Park (2530,-275): ObjectCollision(Basic Road 7420・21833、JapaneseGarden 16247)
  - Regular Park (2125,-75) west: ObjectCollision(Basic Road 15020・28558、住宅 1748 ほか)
  - Regular Park (2232,-166) west, 撤去 [8942]: ObjectCollision(Medium Road 22521・33129、店舗 15063・29302、高層 15195・23416、住宅 32975・44493)
  - Regular Park (2176,-190) east, 撤去 [28270]: ObjectCollision(道路 4528・4692・33129、建物 7件)
  - Regular Park (1856,-287) west, 撤去 [4371]: ObjectCollision(道路 482・2399・19030・20450、消防署 7003)
  - Regular Playground (720,-500) west: ObjectCollision(Small 4 Lane 3268・34446、火葬場 1641)
  - Regular Playground (675,-585) east: ObjectCollision(Basic Road 8748・14535)
  - Regular Park (745,-290) west: ObjectCollision(墓地 21962)
  - Regular Playground (2222,670) south: ObjectCollision(小学校 7795、Basic Road 12619・20545)
  - Regular Playground (-1190,-283) south: ObjectCollision(高校 47279、Basic Road 3707)
  - Regular Playground (-1395,-372) east: ObjectCollision(高校 34421、Basic Road 18668・36748)
  - Regular Playground (-1400,-458) east: ObjectCollision(警察 13823、Basic Road 5272・36732)
  - Regular Playground (2128,692) east, 撤去 [14631, 21083]: ObjectCollision(Basic Road 602・35124、店舗 3327・4777、事務所 7320)
  - Regular Playground (2290,-200) west, 撤去 [29302]: ObjectCollision(Basic Road 24673、高層 15991・20887・40011、住宅 30909)
  - Regular Playground (480,-420) south: ObjectCollision(Basic Road 28565、事務所 36378・43872)
  - Regular Plaza (-600,-600) north: ok=true、費用 2,500、入口の道路 null、道路が半径80m内にない(net_near)
  - Regular Playground (1200,-200) west: ok=true、費用 1,250、入口の道路 null、撤去 2件(事務所 22443・23588、働き口 32 を失う)

## 判断の根拠

確認した事実: 公園の候補 14 か所は、道路・高層住宅・施設とぶつかり、置けなかった。残る2か所は、入口の道路が確認できず、または撤去で働き口を失う。道路に面した空きは、地図上で見当たらなかった。必須の接続(道路への面)が確認できた場所が0のため、実行可の案は作れない。

試しの案も、今月は出さなかった。地価を上げる手(木を植える)は、道具で配置を試せず、効き目の量を測る基準もないため、実行条件が確認できない。

## 捨てたもの

- Regular Playground / Regular Plaza を、空きの住宅地へ: 道路に面した空きが確認できず、実行条件が未確認のため。
- (-600,-600) の Regular Plaza: 半径80m内に道路がなく、道路を新しく引く工事が要る。工事の費用と経路を確かめていないため。
- (1200,-200) の Regular Playground: 入口の道路がなく、事務所2棟(働き口32)を失う取り壊しが要るため。
- 木を植えて地価を上げる試し(plant_trees): 試しの道具がなく、置く前に確かめられないため。地価の効き目も確認していないため。
- Recycling 政策: 直接の費用は0だが、住宅の税収を約13,000/週減らし、黒字の線(週の収支 +9,588)を守れないため。
