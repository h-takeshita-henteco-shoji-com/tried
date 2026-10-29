# m05 経済観光文化局の案

## 案1: 東の空き地に名所 Friendly Neighborhood を1棟、道路の支線つきで置く(試し)

### 施策

- 案の id: economy-1
- 施策: 座標 (2760, 1012) に名所 Friendly Neighborhood を1棟(facing west)。入口の前に、既存の道路 (2822,1000) から西へ支線を引く。道具は `build_line`(支線)と `place_building`(名所)
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `build_line`(prefab "Basic Road"、points [[2822, 1000], [2728, 1000]])。道路の支線。試しの道具 `test_build_line` は ok(segments 2、crossings 0、overlaps なし、cost 480)
  2. `test_place_building`(prefab "Friendly Neighborhood"、x 2760、z 1012、facing "west")。支線が引けた後に、入口の道路(entrance.road)が null でないことを確かめる。null なら置かず、中止する
  3. `place_building`(prefab "Friendly Neighborhood"、x 2760、z 1012、facing "west")。建設費 20,000
  - 名所の数は 6 → 7 になる。ほかの建物は動かさない
- 設置条件の確認:
  - 試し `test_place_building`(支線の前): ok、placed false、cost 20,000、enoughMoney true、取り壊し 0(wouldDemolish count 0、lostByDemolish jobs 0 / homes 0)。入口の道路は null(支線の前のため。支線を引けば入口から約12m の道路 (2728〜2822, 1000) に入る)
  - `map_layer` electricity_service(x 2760、z 1012、radius 40、n 3): 中心の点 (2760,1012) は 1。電気が届く
  - `map_layer` water_service と sewage_service(同じ範囲): 中心の列 (2760) は 3 点とも 1。水と下水が届く
  - `net_reach`(x 2800、z 1000、radius 150): 周りの道路 10 区間は、つなぎ口から入れる・出られる(notEnterable 0、notLeavable 0)。支線の先は既存の道路の端 (2822,1000) とつながる
  - 支線の位置は `test_build_line` で重なりなし(overlaps [])。ほかの建物との重なりは未確認の部分あり(支線は建物の敷地の外を通る前提)。実行時に `test_build_line` の結果が変わったら中止
  - 候補地の比べ(同じ地区でない別の地区を試したもの): 候補 (2880,700)、(2880,540)、(2450,1000)、(2300,600)、(2600,600)、(2172,666) 周り、(2648,481)、(2237,854)、(2760,1010) の東西 は、建物や道路と重なって断られた(「捨てたもの」を見る)。(2760,1012) は、建物も道路も重ならず、電気・水・下水の中心が届く、唯一確認できた候補
- 接続工事: 支線 `build_line` Basic Road、points [[2822, 1000], [2728, 1000]]、建設費 480(test の cost)、週の維持費の増え約4(40/km/週 × 0.094 km)。既存の道路 (2822,1000)〜(2850,1000) の西端につなぐ。電気・水・下水の管は、中心の点が既に届いているため、新しい線は要らない
- 予備候補: なし。今月確認できた候補は (2760,1012) だけ。ほかの候補は、建物や道路との重なりで断られた
- 中止する条件:
  - 支線を引く `build_line` が断られた、または `overlaps` が出た
  - 支線の後の `test_place_building` で、入口の道路が null のまま
  - 置く前の `map_layer` で、中心の点 (2760,1012) の electricity / water / sewage のどれかが 0
  - 費用が 20,480 を超える、または週の収支が黒字でなくなる

### 期待する効果

- 改善の見込み: 観光の目標(今いる観光客 1,533、訪問 152、Tourism 48)は、公園・広場の周りの魅力度を上げても動かなかった。名所(Monument)は、ゲームで観光の対象になる建物で、名所の数が 6 のまま増えていない。名所を1つ足すと、観光客の数が増える見込みがある。効き目は、確認した事実からは予想できない。
- 数値と期限: 今の値(月末、2050-05-02): 観光客 1,533、訪問 152、Tourism 48、名所 6 棟、魅力度の平均 6(中心 (2760,1012) r150 の平均 22)。予想値は見積もれない。期限は 見回り1(10日後)、見回り2(20日後)、月末(30日後)
- 確認方法: `city_info` の tourists(now と visits)、`economy_breakdown` の Tourism、`buildings_near` の service=Monument の棟数(名所 7 棟になったか)、`map_layer` attractiveness の (2760,1012) r150 n5(基準 平均 22、max 134)。比べるのは同じ道具・同じ範囲・同じ引数
- 不確かな点: 観光客の数が名所の数でどれだけ決まるかは、この街では確かめていない。魅力度は場所の値で、人数は街全体の別の要因で決まるかもしれない(公園3棟の試しでは人数が増えなかった)。量は見積もれない。名所の周りの人が来る経路(道路の接続)も効く可能性がある。数値は見積もれない。確認する変化は、名所の数 7 と、観光客の数が見回りの基準(1,533 → 見回り2 の数)より増えるか
- 試し: 効き目が分からない案のため試しとして出す。
  - 仮説: 名所(Monument)を街の端のつなぎ口に近い空き地に1棟足すと、観光客が来る数(tourists.now)が増える
  - 測る数: `city_info` の tourists.now と visits(道具と項目)。場所は (2760,1012) の周り。基準は今の 1,533 と 152(2050-05-02)
  - 場所: (2760,1012)、東の商業と事務所の地区
  - 基準: 置く前の tourists.now 1,533、visits 152、Tourism 48、名所 6 棟。人数が見回りと月末で基準より増えたら効いた、減れば外れ。増減の幅は、前の調査(s04-2)の 10日で 20〜53 の減りを目安にする
  - 編成方針の「分からないこと」: 「観光客が1,533に減り続けた原因(魅力度は上がったのに人数が増えない原因)」に当たる

### 費用

- 建設費: 20,000(Friendly Neighborhood、`list_building_types` の cost)+ 480(支線 Basic Road、`test_build_line` の cost)= 20,480
- 週の維持費の増え分: 320(名所、`list_building_types` の upkeepPerWeek)+ 約4(支線、40/km/週 × 0.094 km)= 約324

### 戻せるか

戻せる。名所は `bulldoze` で取り壊せるが、取り壊しは議決が要る。支線は `remove_line` で消せる。建設費の払い戻しはない。

### 前の月の答え合わせ

- 前月(4か月目)の economy-1(北の道路沿いの StatueOfWealth、試し)は非採択。理由は、電気の網が発電所につながるかが未確認だったこと
- 今月の扱い: 場所を (2760,1012) に替え、電気・水・下水を `map_layer` で確かめた。電気の不足の理由は、前の場所の確認が足りなかったため。StatueOfWealth は今月の案にしない(電気が未確認の場所のため)
- 前月の調査(s04-2、観光客の数の幅)の結果: 10日ごとに観光客が 20〜53 減り、Tourism が 86 → 48 に下がった。今月の案は、この減りを止める手として出す

### 市の計画

- 当たる施策: 5-1、5-2 観光(今いる観光客、訪問の平均、Tourism の週の収入、魅力度、名所の棟数)
- 編成方針の重点に当たるか: 当たる(重点1「5-1、5-2 観光」)

## 案なし

(案1を出したため、この見出しは書かない)

## 調査

- 調査: なし

## 見たもの

- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940/週、教育費に入る)、RecreationalUse(0)、BigBusiness(3,920/週)。政策の費用の合計 10,627/週。観光に効く政策は一覧にない(RecreationalUse は有効のまま、m01 で効かなかった)。政策の変更は今月なし
- `list_building_types`(service=Monument): 解禁済み。最安は SeaWorld、ScienceCenter、Servicing Services、Friendly Neighborhood の 20,000(維持費 320/週)。Fountain of LifeDeath 30,000(240/週)、Countdown Clock 37,500(80/週)、Official Park 45,000(128/週)
- `buildings_near`(service=Monument、街全体): 名所 6 棟(SeaWorld 2374、ScienceCenter 29187、Plaza of Transference 45587、Winter Market 01 30532、Countdown Clock 9113、Fountain of LifeDeath 41780)。問題なし
- `city_info`: 人口 180,993、観光客 1,533 / 152、所持金 2,161,625、週の収支 +8,218(収入 348,060 / 支出 339,842)、幸福度 87、需要 26 / 2 / 56、電気・水・下水が来ない市民 0 / 0 / 0
- `zone_map`(x 2600、z 700、r500): 東の密集した事務所と住宅の地区。空いた道路沿いの土地は少ない
- `map_layer`(attractiveness、x 2600、z 700、r500、n9): 平均 10、max 157(2600, 1200)
- `zone_summary`(grid 1000): CommercialHigh の道路に面した空き 156 マス。空きは (2500, 500) の区画に多い
- `buildings_near`(abandoned=true、(2600,700) r450): 放棄された建物 11 棟(Shop04 と Hotel)。Hotel 43021、46995 は働き口を失うため外した
- `net_near`(service=Road、(2760,1010) r70): 既存の道路は (2822,1000)〜(2850,1000) と (2822,940)〜(2822,1000)
- `test_place_building`: (2880,700) SeaWorld、(2880,540) ScienceCenter、(2450,1000) Servicing Services、(2300,600) Friendly Neighborhood、(2800,400) SeaWorld、(2600,600) Friendly Neighborhood、(2880,600)、(2172,666) SeaWorld(放棄 37092、8571 を取り壊す前提)、(2648,481) ScienceCenter(放棄 8208、31251 を取り壊す前提)、(2237,854) Servicing Services(放棄 48335 を取り壊す前提)、(2176,703) Friendly Neighborhood(放棄 8571 を取り壊す前提)、(2760,1010) Friendly Neighborhood(入口の道路なし)、(2760,1012) Friendly Neighborhood(入口の道路なし、ok)、(2800,1000)、(2800,956)、(2790,1040)、(2760,1060)。断られた理由は建物と道路との重なり
- `test_build_line`(Basic Road、[[2822,1000],[2728,1000]]): ok、segments 2、cost 480、overlaps なし
- `map_layer`(attractiveness、x 2760、z 1012、r150、n5): 平均 22、max 134(基準)
- `map_layer`(electricity_service、x 2760、z 1012、r40、n3): 中心 (2760,1012) = 1
- `map_layer`(water_service、sewage_service、同じ範囲): 中心の列 (2760) は 1
- `water_trace`(2760,1012): 近くの事務所 (2830,1016) で水・下水・電気が届く。水の網は取水口(給水塔)と排水口につながる
- `net_reach`(x 2800、z 1000、r150): 道路 10 区間、つなぎ口から入れる・出られる。建物 24 棟、来られない 0

## 判断の根拠

- 観光の目標は、今いる観光客 1,533(出発点 1,646、目標 3,000)、Tourism 48(目標 1,000)。名所は 6 棟のままで、公園と広場の周りの魅力度は上がったが、人数は増えなかった。今の手は、名所の数を増やす一手に絞る
- 名所(Monument)は、建設費 20,000 の最安から、取り壊しなしで置ける場所を探した。放棄された建物を壊す候補は、道路や学校との重なりで断られた。建物を壊さずに置けた候補は (2760,1012) の1つだけ
- 費用は、建設費 20,480、週の維持費の増え約 324。建設費の上限 79,000、維持費の幅 4,000 の内に収まる。週の収支は黒字のまま
- 案の数を1件にした理由: 名所を置ける場所は (2760,1012) の1つしか確認できなかった。ほかの候補は重なり、または電気・水・下水の条件が未確認のため出さない。件数を埋めるための案は作らない
- 政策の変更は、観光に効く政策が一覧にないため見送った。RecreationalUse は費用 0 で続ける

## 捨てたもの

- 名所 SeaWorld (2880,700)、ScienceCenter (2880,540): 道路(Basic Road)と建物(Expensive Park、Elementary School)と重なり、断られた
- 名所 Servicing Services (2450,1000): 道路 8494、31803 と重なり、断られた
- 名所 Friendly Neighborhood (2300,600): 警察署 43533 と重なり、断られた
- 名所 SeaWorld (2172,666)、ScienceCenter (2648,481)、Servicing Services (2237,854)、Friendly Neighborhood (2176,703): 放棄された建物を壊す前提で試したが、道路と学校、ほかの建物の重なりで断られた。取り壊しを伴うため、議決の対象になり、今月は採らない
- 名所 Friendly Neighborhood (2880,600)、(2600,600)、(2800,1000)、(2800,956)、(2790,1040)、SeaWorld (2760,1060)、(2800,400): 道路・建物・公園の重なりで断られた
- 名所 Friendly Neighborhood (2760,1010): 入口の道路がなく、支線を引く案の前に確かめた候補。(2760,1012) の案に替えた
- 放棄された建物の取り壊し(Hotel 43021、46995 を含む): 働き口を失うため、取り壊しの議決が要る。今月は取り壊しを含まない案にした
- 政策の変更(観光に効く政策なし): `list_policies` に観光の政策がない
- 観光客の数を直接増やす案(旅行の政策など): 一覧にないため、出せない
