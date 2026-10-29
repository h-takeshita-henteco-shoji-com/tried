# m12 住宅都市みどり局の案

## 案1: 電気の届く空き(440,1150)に公園を1か所置き、入口の道をつなぐ

### 施策

- 案の id: urban-1
- 施策: (440,1150) に Regular Park を北向きに1棟。入口の道は (440,1182)→(437,1217) の Basic Road 1区間で、既存の node 8139(437,1217)につなぐ。道は公園を置いた後に引く
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building`(prefab="Regular Park", x=440, z=1150, facing="north", pay=true)。建設費 1,000。試しの `test_place_building` は ok、angleUsed 0、entrance (440,1182)、道なし(road null)、取り壊しなし
  2. `build_line`(prefab="Basic Road", points=[[440,1182],[437,1217]], pay=true)。試しの `test_build_line` は ok、segments 1、crossings 0、cost 160、overlaps なし。端 (437,1217) は既存の node 8139 につながる
  3. 完了後に `map_layer`(type="electricity_service", x=440, z=1150, radius=20, n=3) で中央の値を見る(1 なら電気あり)
- 設置条件の確認:
  - 敷地: `test_place_building` で ok(ObjectCollision なし)。`buildings_near`(x=440, z=1150, radius=60)は建物 0。近くの道 segment 17915 は、外形の北西の角から約15m離れる
  - 電気: `map_layer`(electricity_service, x=440, z=1150, radius=32, n=5)の中央は 1。西の端の列(x=408)だけ 0
  - 道: `test_build_line` で ok。道は建物の後に引く
  - 水・下水: 公園は要らない(`list_building_types` の needs)
- 接続工事: 入口の道 Basic Road 1区間(長さ約35m。建設費 160、週 1.4。`list_net_types` の Basic Road 5,000/km、40/週/km で算出)
- 予備候補: なし。試しで断られた候補は、(760,1432)、(610,1345)、(520,1308)、(672,1280)、(470,1192)、(400,1168)、(430,1158)、(432,1164)、(466,1160)。どれも道か遊歩道か風力と重なった
- 中止する条件: (1) `place_building` が断る、(2) `build_line` が断る、(3) 置いた後の `map_layer` の中央の値が 0 のまま(電気が来ない。公園を残し、道は引かない。費用は公園の1,000のみ)

### 期待する効果

- 改善の見込み: 公園 Regular Park を1棟増やし、Beautification の数を 86 から 87 にする。Beautification は 4-2 の測り方そのもの。電気の届く場所で、道もつなぐため、前回の (690,1190) のように道がつながらない公園にはならない見込み(予想)
- 数値と期限: `buildings_near`(service="Beautification"、全体)の total。今の値 86(12/7)。予想 87。期限は月末(12月末)
- 確認方法: 月末に `buildings_near`(service="Beautification", x=0, z=0, radius=9000, brief=true, limit=1)の total を見る。同時に新しい公園の problems が "None" か、`buildings_near`(x=440, z=1150, radius=60)で見る
- 不確かな点: 100 の目標には届かない(12か月で届かない見込み。予想)。公園の数は 1 増えるだけ。電気の西端の列が 0 なので、公園の中の一部に電気が来ない可能性がある(建物の判定点の電気で決まる)
- 試し: なし

### 費用

- 建設費: 1,160(公園 1,000 + 道 160。`test_place_building`、`test_build_line` で確かめた額)
- 週の維持費の増え分: 9.4(公園 8 + 道 1.4。`list_building_types` の upkeepPerWeek と `list_net_types` の upkeepPerWeekPerKm から算出)

### 戻せるか

戻せる。公園も道も、取り壊しの議決なしで置き直せる。ただし、この案は最終月の施策なので、戻す必要は通常ない。

### 前の月の答え合わせ

- 11月の案 urban-1(公園 (658,1400))は採られたが、実行前の確認(`map_layer` electricity_service の中央が 0)で見送られた。期限は12月末。12月の確認(`buildings_near` Beautification)は 86 で、増えていない。判定: 外れ(公園は増えなかった)。理由: 公園の場所の電気の確認が、採択後の実行の前にしか取れなかった。今月は、置く前に `map_layer`(radius 20 と 32)で電気を確かめ、採択の条件に入れた。
- 10月の案 urban-1(公園 (762,1368))は当たり(台帳 m10-urban-1)。9月の案 urban-1(公園 (690,1190))は道が通らず半分(RoadNotConnected のまま)。今月は、道を公園の後に引き、道の試しを通した形にする。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たらない(重点は5-1・5-2、5-1・5-2(入口)、8-1。4-2 は重点の外。編成方針の「重点の外の案も出してよい」に従う)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `list_policies`: 政策の一覧を取得。有効なのは SmokingBan(費用0)と BigBusiness(週 4,004)。RecreationalUse は inactive(費用0)、SmallBusiness は inactive(週 313)。urban に関係する政策(公園・緑の効きを上げるもの)は見当たらない。RecreationalUse は、3月と4月の試しで attractiveness が動かなかった(m03-1 外れ)。今月は政策を変えない。policyExpensesPerWeek 10,786
- `city_info`: 人口 179,547、所持金 2,358,955、週の収支 +13,509、幸福度 88、観光客 1,725(訪問 133)、需要 住16/商2/工66、dialog なし
- `demand_breakdown`: 働き口 87,426(空き 2,525)、家 56,024(空き 5,108)、失業 9,812(大卒 9,301)
- `land_value`: 街の平均 54
- `list_building_types`(service=Beautification): 公園 Regular Park は 1,000、週 8、電気のみ必要、道が要る。解禁済み
- `buildings_near`(x=0, z=0, radius=9000, service=Beautification, brief, limit=1): total 86
- `buildings_near`(x=650, z=1100, radius=250, brief): 風力 5 基(15888、19235、32919、39796、41134)、公園 23298(690,1190)は RoadNotConnected、公園 473(752,1290)と 32260(588,1232)は問題なし
- `buildings_near`(x=700, z=1450, radius=160, brief): 公園 100(585,1365)、石像 11580(668,1565)は Electricity と MajorProblem、公園 19278(762,1368)は問題なし
- `buildings_near`(x=440, z=1150, radius=60, brief): 建物 0
- `zone_map`(x=700, z=1300, r400, size700)、`zone_map`(x=650, z=1100, r250, size600): 道の沿いの空きは、道の北東と南東に少しある。(440,1150) の周りは空き
- `map_layer`(electricity_service): (700,1300,r400,n9)、(700,1450,r150,n7)、(760,1460,r40,n5)、(660,1400,r40,n5)、(610,1345,r40,n5)、(672,1280,r32,n5)、(650,1080,r150,n7)、(400,1168,r50,n5)、(430,1158,r20,n3)、(440,1150,r32,n5)、(560,1290,r40,n5)。中央 (440,1150) は 1
- `net_near`(x=700, z=1450, r160, Road)、(x=620, z=1200, r200, Road)、(x=760, z=1080, r150, Road): 道の一覧。(440,1150) の東の道は、(437,1217) の node 8139 につながる。(760,1080) の周りには道がない
- `test_place_building`: Regular Park を (760,1432) west ObjectCollision、(760,1460) west ok(entrance 道 segment 29045 距離8。電気の中央は 0 のため不採用)、(610,1345) south ObjectCollision、(470,1192) north ObjectCollision、(400,1168) north ObjectCollision、(430,1158) north ObjectCollision、(432,1164) north ObjectCollision、(466,1160) north ObjectCollision、(440,1150) north ok(entrance road null)、(520,1308) south ObjectCollision、(672,1280) north ObjectCollision
- `test_build_line`: Basic Road [[440,1182],[437,1217]] ok(cost 160、segments 1、crossings 0、overlaps なし)
- `list_net_types`(service=Road): Basic Road は 5,000/km、週 40/km

## 判断の根拠

- 12か月目の最終月で、4-2 の数は 86 で目標 100 に届かない。残り1か月で届く数は、置ける公園の数で決まる。1棟の差は小さいが、確かめた候補は1か所だけで、それを置くのが最も確実。
- 候補の中で、(440,1150) は試しが ok で、電気の中央が 1、入口の道を1区間(35m)で結べる。(760,1460) は試しが ok だったが、電気の中央が 0 のため外した。
- 道を公園の後に引く順にした。試しは道の前の状態で判定するため、道を先に引くと、置く試しが通っても道とぶつかる失敗が出やすいため。
- 装飾(岩、石、駐車場の装飾)の Beautification は、1基100〜1,000で置けるが、公園の数を増やすためだけの置き方になる。4-2 の目的(公園など)に合わないため、案にしない。
- 島と空き地(地形の資料の空き地1〜5)は、道と電気の距離が遠く、最終月の月末判定に間に合わないと判断し、今月は試していない。
- 案は1件。ほかの候補を増やすと、同じ手の言い換えになるため。

## 捨てたもの

- 公園 (760,1460)(西向き): 試しは ok だが、電気の中央が 0 で、置いた後に電気が来ない見込みが高いため。
- 装飾の岩や石(Rock、Cliff、Boulder など、100)と駐車場の装飾: Beautification の数は増えるが、公園として街に効かない。数だけを増やす手になるため。
- 公園 23298(690,1190)の道の接続: Beautification の数は変わらない(4-2 に効かない)。道を通すのは、今月の試しの範囲外。
- RecreationalUse の再有効化(政策): 費用は0だが、3月と4月の試しで attractiveness 平均2のまま動かなかった(m03-1 外れ、m04-1 で外した)。観光の政策は経済観光文化局の担当で、urban の4-2 に当たらない。
- 島・空き地の公園: 橋や送電線、道が要り、最終月の月末判定に間に合わない見込み。
