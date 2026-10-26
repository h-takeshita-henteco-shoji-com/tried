# m02 住宅都市みどり局の案

## 施策

- 施策: 公園など(Beautification)を2棟置く。Regular Playground を (2672, -330) と (2672, -90) に、`place_building` で置く。
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building(prefab="Regular Playground", x=2672, z=-330, facing="north")`
  2. `place_building(prefab="Regular Playground", x=2672, z=-90, facing="south")`
  - 1 と 2 は敷地が重ならない(南北に240m離れている)
- 設置条件の確認:
  - `test_place_building`(1): ok=true、cost 1,250、入口 (2672, -310) の道路は Basic Road 区間13705(distance 2)、wouldDemolish 0
  - `test_place_building`(2): ok=true、cost 1,250、入口 (2672, -110) の道路は Basic Road 区間2781(distance 2)、wouldDemolish 0
  - `map_layer` の electricity_service: (2672, -330) 周り半径100と (2672, -90) 周り半径40の3×3が全部1。この建物は電気だけが要り、水と下水は要らない
  - `zone_map` と `buildings_near`: 2か所とも空いた区画で、既存の建物は壊れない
- 接続工事: 不要
- 予備候補: なし。ほかに試した場所は、取り壊しが出るか道路にぶつかり、外した((2682,-240)、(2686,-268)、(2672,-420)、(2142,-318/-364/-409) は建物を壊す。(2672,-366)、(2672,-100)、(2672,-146) は道路か火葬場にぶつかる)
- 中止する条件: 実行時に `place_building` が断る、または戻り値の demolished が1以上なら、その1棟を見送る。所持金が出発点(2,082,287)を下回っていたら見送る

## 期待する効果

- 改善の見込み: 4-2 の数え方は Beautification の建物の数なので、2棟置くとその数が確実に2増える。公園は周りの地価を少し上げる見込みで、4-1 にも小さく効くかもしれない。
- 数値と期限: `buildings_near`(service="Beautification")の街全体の数。今 81(2050-01-31)。予想は 83。期限は3か月目の月例。目標100には2棟では届かない
- 確認方法: `buildings_near(x=2500, z=0, radius=5000, service="Beautification", brief=true)` の total を、81 と比べる。地価は `land_value(x=2672, z=-330, radius=100)` の average を置く前後で比べる
- 不確かな点: 地価への効きは数値を見積もれない。置いたあとの `land_value` で確かめる。敷地が小さいので、街全体の高密度住宅の地価58はほとんど動かない見込み。目標100に近づくには、毎月置ける場所を探し続ける必要がある。この月は取り壊しなしで置ける場所が2か所しか見つからなかった
- 試し: なし

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 費用

- 建設費: 2,500(1,250 × 2。`test_place_building` の cost)
- 週の維持費の増え分: 48(24 × 2。`list_building_types` の upkeepPerWeek)

## 戻せるか

戻せる。建物を2棟置くだけで、取り壊しは要らず、壊せば元の区画に戻せる。

## 前の月の答え合わせ

- 前月の案(JapaneseGarden 2棟)は採られなかった。理由は、要る電気と水の届き具合が本文で未確認だったこと
- 今月の手当て: 電気だけが要る Regular Playground に替え、`map_layer` の electricity_service で届き具合を確かめ、`test_place_building` で2か所とも ok を確かめた。取り壊しも0
- 前月の調査はなし(`council/m01-survey-urban.md` は出していない)

## 市の計画

- 当たる施策: 4-2 花や緑による潤い(4-1 にも小さく関わる)
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `list_policies`: 2050-01-31。有効は EducationBoost 7,940、BigBusiness 3,920、IndustrySpace 4,852。ほかは無効。住宅の需要や地価に直接効く政策で、費用の枠(週5,000)に入るものは見当たらない。HighTechHousing は週20,260で枠を超える。Recycling、PetBan などは費用0だが、公園の数や地価には効かない
- `demand_breakdown`: 働き口86,348、空き3,249、大卒の失業7,234、家55,362、空き家4,984
- `building_stats`: 高密度住宅 4,057棟、地価の平均58、高密度商業の放棄106
- `city_info`: 人口178,760、所持金2,111,044、需要 住23・商4・工59、dialog null
- `list_building_types`: service=Beautification。Regular Playground は 1,250 / 週24、電気のみ要る
- `zone_summary`: 空いた区画は Office 1,642、住宅(高密度)709、商業(高密度)596。どれも「道から奥」で、新築は毎月の上限で決まる
- `land_value`: 街の平均52
- `zone_map`: (2500,-500) 半径500、(2650,-250) 半径200、(2500,500) 半径300、(2160,-330) 半径120
- `buildings_near`: (2500,-500) 半径500 の Beautification は JapaneseGarden 2棟、(2682,-240) 周り30mに高層住宅1棟
- `net_near`: (2672,-340) 半径80 の Basic Road。z=-300 と z=-390 に東西の道
- `test_place_building`: 上のとおり。ok は (2672,-330)、(2672,-90) ほか
- `map_layer`: electricity_service 2か所とも1

## 判断の根拠

住宅の需要は23で、空き家は4,984ある。住宅の区画を足しても人口には効かず、働き口の不足(大卒の失業7,234)は経済観光文化局の担当に近い。局の担当の数字で動かせるのは、4-2 の公園の数と、4-1 の地価である。公園は費用と維持費が小さく、取り壊しなしで置ける2か所が確認できたので、それを案にした。

## 捨てたもの

- オフィスの区画を足す: 空きの Office は1,642マスあり、新築は毎月の上限で決まる。区画を足しても働き口は増えない
- JapaneseGarden(前月案): 水も要り、効きは Regular Playground より大きいが、費用は2倍。維持費の枠では足りるが、数を増やすことを優先した
- 高密度住宅の区画を足す: 空き家4,984で需要が23と低く、効かない
- 政策 HighTechHousing: 週20,260で維持費の枠5,000を超える
- (2142,-318)、(2142,-364)、(2142,-409) の公園: 商業と住宅の建物を壊すため外した
