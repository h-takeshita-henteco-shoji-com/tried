# m23 経済観光文化局の案

## 案1: 峰の近くに公園を1棟(試し)

### 施策

- 案の id: economy-1
- 施策: 道沿いの空き (1862,360) に JapaneseGarden を1棟、入口を南(south)に向けて置く。観光客が集まる峰 (1830,330) の近くに、行き先を1つ足す。試し
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building`(prefab="JapaneseGarden", x=1862, z=360, facing="south", pay=true)。建物が先
  2. 道路は新しく引かない。入口は既存の道路 segment 23279(Small 4 Lane Road、z=330 付近)につながる
  3. 置いた後に `buildings_near`(x=1862, z=360, radius=20)で、新しい公園の grid(electricity、water)が true か確かめる
- 設置条件の確認:
  - `test_place_building`(JapaneseGarden, 1862, 360, facing south): ok、置けない理由なし、cost 2,500、enoughMoney true、入口 (1862,344)、道 segment 23279 から距離6、壊れる建物 0、失う働き口・家 0
  - `list_building_types`(service=Beautification): JapaneseGarden は幅4・長さ4、建設費 2,500、週の維持費 40、needsRoad true、電気と水が要る、下水は不要
  - `map_layer`(electricity_service, 1832〜1892 / 330〜390): 9点すべて 1(電気が届く)
  - `map_layer`(water_service, 同じ範囲): 9点すべて 1(水が届く)
  - `water_trace`(1897, 354): 網は1つ、水と下水の cell が true
- 接続工事: 不要(既存の道路 segment 23279 と、電気・水の網に入る)
- 予備候補: `test_place_building`(JapaneseGarden, 1862, 356, facing south)も通った(入口 (1862,340)、道 segment 23279 から距離2、壊れる建物 0)。360 が断られたら 356 を使う
- 中止する条件: 実行時の `test_place_building` が断る、入口の道路が null、壊れる建物が1以上、または建てた後の grid の electricity か water が false のとき、予備候補を使い、それも断られたら見送る

### 期待する効果

- 改善の見込み: 公園は観光客の行き先になる。既存の峰の公園3棟は、2051-11-02 の `buildings_near` で Visitors last week が 13〜17、Tourists last week が 3〜8 だった。新しい1棟も同じ範囲で観光客を集めると予想し、訪問の平均を増やす(5-1、5-2)。
- 数値と期限: 新しい公園の Visitors last week は、予想 10〜15(既存3棟の範囲からの局の予測)。訪問の平均は 179 から 185 以上(局の予測。幅あり)。判定は 24月末
- 確認方法: `buildings_near`(x=1862, z=360, radius=30, brief=false)の新しい公園の stats(Visitors last week、Tourists last week)、`city_info` の tourists.visits、`economy_breakdown` の Tourism。今の値は、訪問 179、Tourism 週 130、既存3棟の Visitors 13〜17
- 不確かな点: 新しい公園の観光客は、近くの既存の公園から移るかもしれず、増えきらないことがある。効きの量は数値で見積もれない幅がある。Tourism の増えは、近くの店の品物(NoGoods)に左右される
- 試し: 仮説は「峰の近くの公園が観光客を集め、訪問の平均を増やす」。測る数は `city_info` の tourists.visits と、新しい公園の stats の Visitors last week。場所は峰 (1830,330) の周り。基準は訪問 179、Visitors 13〜17。編成方針の分からないこと「観光の名所を足すと、訪問と Tourism が増えるか」の項目に当たる

### 費用

- 建設費: 2,500(`test_place_building` の cost、`list_building_types` の cost)
- 週の維持費の増え分: 40(`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せる。取り壊すこともできるが、取り壊しには議決が要る。

### 前の月の答え合わせ

前の月(22月)は、経済観光文化局の案なし(場所が確かめられず、名所の事業を閉じた)。
22月の調査 s22-1 の結果を読んだ。
- `buildings_near`(1818, 332、r80)は4棟。公園 JapaneseGarden 3棟(31332、39519、46572)と、放棄された店 34259(NoGoods、FatalProblem)
- `map_layer`(attractiveness、r150)の最大 295 は (1818,332) にあり、3回の見回りと月末で動かなかった
- 判定: 店の周りではなく、公園の周りに峰がある。23月の予定どおり「その近くの手」を、公園の試しにした

### 市の計画

- 当たる施策: 5-1、5-2 観光(今いる観光客、訪問の平均、attractiveness、名所の棟数)。4-2 花や緑による潤い(公園の数。urban の案と数える)
- 編成方針の重点に当たるか: 当たる(重点1: 5-1・5-2 観光。島・空き地の名所の代わりに、峰の公園)

## 調査

- 調査: なし

## 見たもの

- `list_policies`: 政策の一覧を取得した。有効なのは SmokingBan(0)、EducationBoost(7,940、教育の支出に入る)、BigBusiness(4,052)。無効で関係するもの: RecreationalUse(0)、SmallBusiness(319)、FreeTransport(0、運賃の収入が0になる)。RecreationalUse と SmallBusiness は、前の試しで観光の数字が分からなかった(市政ノート)。今月は採らない
- `city_info`: 人口 172,759、所持金 2,672,278、週の収入 336,105、支出 328,359(収支 +7,746)、観光客 2,020(訪問 179)、需要 住 36 / 商 2 / 工 43、来ない市民 0 / 0 / 0
- `buildings_near`(1818, 332、r120、limit 30): 20棟を取得。公園 JapaneseGarden 31332(1820,300、Visitors 17)、39519(1856,306、Visitors 13)、46572(1820,355、Visitors 16)、店 34259(1856,273、放棄、NoGoods、FatalProblem)、店 Shop01 20654(1856,253)と Shop13 48524(1856,236)は problems なし
- `zone_map`(中心 1830,300、r160、size 640): 道路 (z 330 付近)の北に空きを確認。空きは (1840〜1880, 337〜370) にある
- `test_place_building`: JapaneseGarden を (1862,360) south で ok、(1862,356) south で ok。(1862,352) south は、道路 segment 18523、23279、26867 に重なり断られた。(1790,300) east は、道路 segment 4414 と公園 31332 に重なり断られた。試しの道具の結果で、街は変えていない
- `water_trace`(点 1862,360 の近く、建物 16664 の位置 1897,354): 網は1つ。水と下水の cell が true。city の水は容量 2,520,000 / 使用 1,878,688、下水は 2,400,000 / 1,874,848
- `map_layer`(attractiveness、中心 1830,330、r150、n=7): 最大 295 は (1830,330)、平均 43
- `map_layer`(electricity_service、中心 1862,360、r30、n=3): 9点すべて 1
- `map_layer`(water_service、中心 1862,360、r30、n=3): 9点すべて 1
- `list_building_types`(service=Beautification): JapaneseGarden は 4x4、建設費 2,500、週の維持費 40、needsRoad true、電気と水が要る、下水は不要。Regular Park(1,000 / 8)など他の公園も解禁済み

## 判断の根拠

- 担当の問題は、観光(5-1・5-2)の訪問の平均 179 と Tourism 週 130 が、目標 250 と 1,000 から遠いこと。名所は週320の上限と空きで置けず、入口は0のまま。
- 調査 s22-1 の結果で、魅力度の峰は店の周りではなく、公園の周りにある。そのため、公園を峰の近くに1棟置く試しを選んだ。費用は建設 2,500、週 40 で、週の収支 +7,746 と守る線の中に収まる。
- 場所は、`test_place_building` と `map_layer` の電気・水で確かめた (1862,360) を選んだ。既存の道路に入口がつき、道路や管の新設が要らない。
- 案の数は1件。ほかの候補(商業の税、店の品物、政策)は、当月の確かめた事実で効く見込みが薄い(下の捨てたもの)。件数を埋めるための案は作らなかった。

## 捨てたもの

- 名所(Monument)の再開: 未建設の最安は Transport Tower(建設費 60,000、週 960)で、週320の上限を超える。置ける空きも22月の5地点で見つからなかった。閉じたまま
- 放棄された店 34259 の取り壊しと跡の再利用: 取り壊しは議決が要り、跡は商業の需要 2 では店が建つ見込みが薄い。放棄地の公園は urban の 4-2 の手と重なる
- 商業(低)の税を下げて店を増やす: 商業の需要は 2 で、店が増えても品物がない店 215 が残るため、観光の収入に効く見込みが薄い。税は finance の担当で、過去にも不採用(m01-finance-3)
- 政策 SmallBusiness(週 319): 試しの結果で Tourism が揺れ、因果が切り分けられない(市政ノート)。同じ試しを繰り返さない
- 政策 RecreationalUse(0): 4回の試しで attractiveness の平均が 2 から動かなかった。効かない見立て
- 旅客の入口: 港湾空港局の担当。経済観光文化局は「求めること」として計画に書いた
- 峰の西側 (1790,300) の公園: 道路と既存の公園に重なり、置けない
