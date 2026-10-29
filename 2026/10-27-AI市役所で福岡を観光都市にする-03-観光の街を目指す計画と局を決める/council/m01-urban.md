# m01 住宅都市みどり局の案

## 案1: 放棄された店の跡に名所(Friendly Neighborhood)を置く

### 施策

- 案の id: urban-1
- 施策: 座標(2290, 972)に名所 Friendly Neighborhood(Monument、8x7)を1棟置く。置く前に、その場所の放棄された店・ホテルを4棟取り壊す(id 5266、42679、45479、49151)。`place_building` で、prefab は Friendly Neighborhood、angle 0、facing north
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 議決のあとに `bulldoze(x=2300, z=975, radius=45, what="building")`。壊す建物は 4 棟(5266、42679、45479、49151)
  2. `place_building(prefab="Friendly Neighborhood", x=2290, z=972, angle=0, facing="north", pay=true)`
  3. 入口は既存の道路 20165(距離 2m)につながる。新しい道路は引かない
  4. 電気・水・下水は既存の網につながる(`water_trace` で確認)
- 設置条件の確認:
  - `test_place_building`(assume_removed_buildings=[5266, 42679, 45479, 49151]、facing north): ok、wouldDemolish 0、入口 道路 20165(距離 2m)、費用 20,000、電気・水・下水が要る
  - `preview_bulldoze`(x=2300, z=975, radius=45, what=building): 壊す建物 4 棟、失う働き口 23(店 3 棟の 5 + 9 + 9。ホテルは 0)、失う家 0
  - `test_build_line`(points=[[2290,1000],[2290,972]]、Basic Road): 5266 とぶつかって断られた。入口は既存道路につながるので、新しい道路は不要
  - `water_trace`(2286, 986): 水 true、下水 true。街全体の水は 1,925,008 / 2,400,000
- 接続工事: 不要
- 予備候補: なし(下の「捨てたもの」で、ほかの候補はすべて不採用か未確認)
- 中止する条件:
  - 議決で取り壊しが通らなければ、案を見送る
  - 取り壊しの直後に `test_place_building` を同じ引数で試し直し、ok でなければ、置かずに止める
  - 入口の道路 20165 が消えていたら、置かずに止める

### 期待する効果

- 改善の見込み: 名所が増えると、観光客が訪れる場所が増え、観光の数字(今いる観光客、訪問)が上がると見込む。この案の名所は観光の施策の数字(名所 6 棟、目標 10 以上)の 1 棟ぶんにあたる。名所の attractiveness が周りの地価を上げるかは、確かめていない。
- 数値と期限: 名所の棟数(`buildings_near` の Monument)は 6 → 7。周り 200m の attractiveness の平均は今 9、最大 78(2290, 772)。12 か月の目標は 4-1 の住宅(高密度)の地価 58 → 62。この案で 4-1 が動くかは数値で見積もれない。確認は 2 か月目と 3 か月目。
- 確認方法: `buildings_near`(problem なし、Monument)、`map_layer`(type=attractiveness、x=2290、z=972、radius=200)、`building_stats`(x=2290、z=972、radius=200、ResidentialHigh の averageLandValue)。今の値は attractiveness 平均 9、住宅(高密度)の地価 73(近くの範囲)。
- 不確かな点:
  - 観光客が増えるかは、名所の効き目しだい。数値は見積もれない
  - 4-2(Beautification)の数は、この案では変わらない。名所は Beautification ではないため
  - 失う働き口 23 は、空き働き口 3,215 の中で吸収できる見込み。失業の数には効きにくい
- 試し: 名所の効き目が分からない。仮説は「名所が attractiveness を上げ、観光客と Tourism の収入を増やす」。測る数は、`map_layer` attractiveness の平均(今 9)と、`city_info` の今いる観光客(今 1,646)。場所は 2290, 972 の半径 200m。基準は 2 か月目で、平均が 9 より上がるか。上がらなければ、次の名所は止める。

### 費用

- 建設費: 20,000(`test_place_building` で確かめた額)。取り壊しの費用は、この道具の返り値に含まれない
- 週の維持費の増え分: 320(`list_building_types` の Monument の upkeepPerWeek)

### 戻せるか

戻せない。取り壊した 4 棟は元に戻らない。

### 前の月の答え合わせ

なし(1 か月目)

### 市の計画

- 当たる施策: 5-1、5-2 観光(担当は経済観光文化局。名所の測り方は観光の施策の数字。この局は、名所を置く場所を確かめる役として関わる)
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口 178,872、所持金 2,082,287、週の収支 +9,965、幸福度 85、観光客 今 1,646・訪問 139、需要(住 23 / 商 2 / 工 60)、ownedTiles 81
- `demand_breakdown`: 働き口 86,175(空き 3,215)、家 55,253(空き 4,935)、失業 7,911(大卒 7,720)
- `land_value`(x=2290、z=972、radius=150): 平均 60、街の平均 52
- `building_stats`(x=2290、z=972、radius=200): 住宅(高密度)の地価 73(25 棟)、商業(高密度)60(39 棟、放棄 5)、事務所 66。街全体の averageLandValue は未取得
- `map_layer`(type=attractiveness、x=2290、z=972、radius=200): 平均 9、最大 78(2290, 772)。街全体の最大 157 は (2575, 1224)
- `list_policies`: 観光に直接の政策はない。有効なのは EducationBoost(7,940/週)と BigBusiness(3,876/週)。無効の政策は、HighTechHousing 20,248/週、PowerSaving と WaterSaving 各 58,281/週、SmokeDetectors 57,718/週、IndustrySpace 4,821/週、SmallBusiness 315/週、Recycling(直接の費用 0。住宅の税を -5%)。今の局の数字に効く政策は、この中にない
- `list_building_types`(Monument): Friendly Neighborhood 8x7 で 20,000、週 320。StatueOfWealth 8x8 で 25,000、週 400。SeaWorld 12x12 で 20,000、週 320。ScienceCenter 11x14 で 20,000、週 320。Fountain of LifeDeath 7x7 で 30,000、週 240。Official Park 6x6 で 45,000、週 128
- `list_building_types`(Beautification): Regular Park 9x8 で 1,000、週 8。Regular Playground 5x5 で 1,250、週 24。Regular Plaza 5x5 で 2,500、週 32。Expensive Park 13x12 で 4,500、週 40
- `buildings_near`(abandoned=true 付近): 放棄されたホテル H3 3x4(id 5266、働き口 0)、店 H3 1x1(id 42679、働き口 5)、店 H1 3x2(id 45479、働き口 9)、店 H1 3x3(id 49151、働き口 9)
- `preview_bulldoze`(x=2300、z=975、radius=45、what=building): 壊す建物 4 棟、失う働き口 23、失う家 0、壊す電気の線 0、電気が止まる建物 0
- `test_place_building`(Friendly Neighborhood、2290, 972、facing north、assume_removed_buildings=[5266, 42679, 45479, 49151]): ok、wouldDemolish 0、入口 道路 20165(距離 2m)、費用 20,000、電気・水・下水が要る
- `test_build_line`(Basic Road、[[2290,1000],[2290,972]]): 5266 とぶつかって断られた。新しい道路は不要
- `water_trace`(2286, 986): 水 true、下水 true、街全体の水 1,925,008 / 2,400,000
- `test_place_building`(Regular Playground、2286, 980、north): 取り壊しの対象は 49151(働き口 9)。取り壊しが要る
- `test_place_building`(Regular Playground、2296, 980、north): 取り壊しの対象は 42679(働き口 5)。取り壊しが要る
- `test_place_building`(Regular Park、712, 1644): 置けるが、500m 以内に道路がないため、今月は見送る(空き地3)
- `test_place_building`(ほか、(2800, 682)、(2700, 700)、(2930, 700)、(2574, 1264)、(2525, 525)、(2242, 525)、(3388, -742)、(2606, 1444)、(2184, -918)、(2176, 256)、(2168, -166)、(2128, 470)、(1916, 850)、(2286, 972)、(2302, 1040)): すべてぶつかりで断られた(道路、歩道、既存の建物、埋立地 Landfill Sites)。この場所は、今月の候補から外す
- `list_net_types`(Road): Basic Road 5,000/km、週 40/km。Small 4 Lane Road も同じ額
- 是正の段で追加(2026-10-29): `buildings_near`(abandoned=true、2290, 972、半径200): 放棄の建物 5 棟(5266、12373、23391、27586、47695)。`test_place_building`(Regular Playground、2296, 980、assume_removed=[42679, 5266, 45479, 49151]): ok、取り壊しなし(A の取り壊しに含まれる)。ただし A の敷地と重なるため使わない。`test_place_building`(Regular Playground、2328, 1034、assume_removed=[47695]): 道路 19287、20165 と重なり断られた。`test_place_building`(Regular Playground、2138, 986、assume_removed=[27586]): 道路 30829 と重なり断られた。`test_place_building`(Regular Playground、2352, 958): 働き口 29 の店(42379、45479)を壊す。`test_place_building`(Regular Playground、2232, 962): 働き口 34 の店(3037、5153、49151)を壊す。`test_place_building`(Regular Playground、2228, 972、assume_removed=[23391, 49151]): 働き口 25 の店(3037、5153)を壊す。`test_place_building`(Regular Playground、2138, 970、assume_removed=[27586]): 働き口 22 の店(17281、35733)を壊す。`test_place_building`(Regular Playground、2314, 1046、assume_removed=[47695, 12373]): 働き口 33 の店(9152、28136)を壊す。`test_place_building`(Regular Playground、2230, 1215、facing south): 道路 6048、30833、36804 と、診療所 16112 とぶつかって断られた。`zone_map`(2290, 990、半径250): 空き地は道路と既存の建物に囲まれ、放棄店跡以外の候補を見つけられなかった

## 判断の根拠

確かめた事実は次のとおり。(1) 観光の名所は 6 棟で、目標 10 以上まで 4 棟足りない。(2) 空いた平らな場所は、道路の近くにほぼなく、名所を置ける場所は、放棄された店の跡だけだった。(3) 2290, 972 の 1 か所だけが、取り壊し 4 棟(失う働き口 23、家 0)と、既存の道路と水・下水で、置けると確かめられた。この案は、名所を 1 棟増やすことで観光の数字を動かす手として出す。効き目は試しとして、2 か月目に attractiveness で測る。案は 1 件にした。ほかの候補は、ぶつかりか、道路のない場所か、取り壊しの対象が増える場所で、今月は確かめられなかった。是正の段で、第3月の公園の候補を探したが、重ならず働き口を失わない候補は見つからなかった。この案の是正はなく、第1月の予定は変わらない。

## 捨てたもの

- 公園 Regular Playground(2286, 980 と 2296, 980): 置けるが、取り壊しが必要。失う働き口は 9(49151)と 5(42679)。この案の名所と同じ場所の取り壊しを増やすので、今月は見送る。公園の数(4-2)の手として、次の月に別の場所を探す
- 是正の段で外した第3月の Playground(2296, 980): 名所A(2290, 972)と重なるため外す。ほかの放棄店跡の候補も、道路と重なるか、働き口のある店を壊すため使わない。計画の事業2は公園 19 か所(目標 100)に直した
- 空き地3(712, 1644)の公園と道路: 置ける公園はあるが、近い道路が 500m 以内にないため、道路を引く費用と距離が未確認。12 か月の計画の事業 2 として、4 か月目までに道路の距離を確かめる
- 島 A、B、C と埋立地 D: 橋を架けて名所を置く手は、`test_build_line` で未確認。今月は試していない
- 観光の入口(旅客の駅・港・空港): 港湾空港局の担当。この局は出さない
- 政策の案: 観光に直接の政策がなく、今の局の数字に効く政策は一覧にない。政策の案は出さない
- 地区の政策(地区に税や政策をかける案): 数字に効くとする根拠がないため、出さない
