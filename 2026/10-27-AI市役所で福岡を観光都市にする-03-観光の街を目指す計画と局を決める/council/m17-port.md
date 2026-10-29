# m17 港湾空港局の案

## 案1: 島Bに旅客の駅(Train Station)を1つ置く

### 施策

- 案の id: port-1
- 施策: 島Bの (-4700,1600) に Train Station を、正面を南(入口 (-4700,1576))に置く。整地(level_terrain、71.5m、polygon [[-4715,1545],[-4685,1545],[-4685,1585],[-4715,1585]])、入口の道(Basic Road、(-4640,1552)→(-4700,1552)→(-4700,1576))、水管(Water Pipe)、電線(Power Line)を1案にする。道具は place_building、build_line、level_terrain
- 議決: 要らない

### 実行計画

- 実行可否: 未確認
- 対象と操作順:
  1. `level_terrain`(polygon [[-4715,1545],[-4685,1545],[-4685,1585],[-4715,1585]]、height 71.5、test=true)で、土と費用を確かめる。現地の地面は (-4700,1590) で 81.1m のため、71.5m は削る量が大きい。削った土は蓄えに入る。test の結果が通れば pay=true で実行する
  2. `place_building`(prefab "Train Station"、x -4700、z 1600、facing "south")。費用 45,000
  3. `build_line`(prefab "Basic Road"、points [[-4640,1552],[-4700,1552],[-4700,1576]])。始点は既存の道の交差点 node 23669 (-4640,1552) につながる。駅の入口 (-4700,1576) に端を合わせる。整地の後に引く(整地なしだと SlopeTooSteep)
  4. `build_line`(prefab "Water Pipe"、points [[-2715,215],[-3600,800],[-4500,1300],[-4700,1560]])。端は駅の ports(place_building の戻り値)に合わせる。端の点は、駅を置いた後に ports の位置へ直す。本土の既存の管は (-2715,50)〜(-2655,190) 付近。経路は economy と1つにまとめる(市長の調整12)
  5. `build_line`(prefab "Power Line"、points [[-4650,1500],[-4700,1560]])。始点は既存の送電線の node 15953 (-4650,1500)。端は駅の ports に合わせる(駅を置いた後に直す)
- 設置条件の確認:
  - 駅: `test_place_building`(Train Station、-4700、1600、south)は ok。angleUsed 180、cost 45,000、enoughMoney true、entrance (-4700,1576)、wouldDemolish 0、取り壊しの働き口と家は 0
  - 駅(整地の仮定あり): `test_place_building`(同じ引数、assume_terrain で level 71.5、同じ polygon)も ok。cost 45,000、wouldDemolish 0
  - 道: `test_build_line`(Basic Road、上の points、整地の仮定あり)は ok。segments 2、cost 440、overlaps []。整地の仮定なしでは gameCheck に SlopeTooSteep(segment 2)が出る
  - 整地: 未確認。`level_terrain` は、この局の道具(読むだけ)に含まれず、test を呼べない。土の量と費用(raisedM3、loweredM3、cost)は分からない
  - 既存の道: `net_near`(-4680、1560、r120)で、node 23669 (-4640,1552) に Basic Road 13902 がある。`net_reach`(-4650、1560、r150)は roads 6、notEnterable 0、notLeavable 0
  - 水: `net_near`(Water、-4700、1600、r150)は 0 件。`water_trace`(-4700、1600)で、近くの水の網は 0、街の水は容量 2,400,000 に対し使用 1,904,208。再調査で `test_build_line`(Water Pipe、[[-2715,215],[-3600,800],[-4500,1300],[-4700,1560]])は ok(segments 32、cost 6,200、overlaps [])。ただし駅の ports は未確認(`list_building_types` の ports は空で、置いた後の戻り値でしか出ない)
  - 電: `net_near`(-4650、1500、r250、Electricity)で Power Line 22680 が node 15953 (-4650,1500) にある。再調査で `test_build_line`(Power Line、[[-4650,1500],[-4700,1560]])は ok(segments 1、cost 200、overlaps [])。駅の ports への接続は未確認
  - 地形: `height_at`(-4700、1590)は地面 81.1m、水面 81.1m(陸)
- 接続工事: 道 440、水管 6,200、電線 200(いずれも `test_build_line` で ok)。駅の ports に端を合わせる作業は、駅を置いた後に確かめる。不要なものはない
- 再調査の結果: 満たせなかった。条件のうち、水管と電線の `test_build_line` は ok になった(6,200 と 200)。整地の `level_terrain`(test=true)は、この局の道具にないため通せず、土と費用が分からない。駅の入口につなぐ ports も未確認。必須条件が残るので実行可否は「未確認」のまま
- 予備候補: なし(駅の向きを変えた候補は未試行。試すなら `test_place_building` で同じ条件を確かめる)
- 中止する条件:
  - `level_terrain` の test が断る、または費用が守る線を割る(週の収支の見込みが +3,000 未満、所持金の見込みが 1,874,000 未満)
  - `test_place_building` の再試しが ok でない
  - 水管または電線の経路が `test_build_line` で断られ、島の経路が見つからない
  - 駅の ports が、水管と電線の端の想定点(上の points の端)から大きく離れ、つなぎ直しができない

### 期待する効果

- 改善の見込み: 駅を1つ置けば、5-1、5-2 の旅客の入口が 0 から 1 になる。入口の数は道具で数えられるため、置いた後の数は確かめられる。観光の数(今いる観光客、Tourism の週の収入)が増えるかは、見積もれない
- 数値と期限: 旅客の入口は 0(今)→ 1(第18月末)。観光客は 1,875(今)、Tourism 週 57(今)。増えた量は見積もれない
- 確認方法: `buildings_near`(service=PublicTransport、x -4700、z 1600、r 200)の旅客の駅の棟数。`transport_reach` で駅が外のつなぎ口につながったか。`city_info` の観光客と訪問、`economy_breakdown` の Tourism。同じ条件で、置く前の今の値と比べる
- 不確かな点: 旅客の駅が外とつながるかは未確認(線路か道路か)。整地の実費と土の量は未確認(局の道具で test できない)。駅の ports への管と電線の接続は、置いた後にしか確かめられない。島へ来る人の数は見積もれない
- 試し: なし

### 費用

- 建設費: 駅 45,000、道 440、水管 6,200、電線 200(いずれも道具で確認)。整地は未確認(地形の費用は局の道具で見積もれない)。整地を除く建設費の合計は 51,840
- 週の維持費の増え分: 駅 960、道 約3、水管 約25(見積もり)、電線 約6(見積もり)。合計 約994。週の収支は +7,468 から約 +6,470 の見込み(守る線 +3,000 の上)。所持金は 2,502,262 から約 2,450,000 の見込み(整地の費用を除く。守る線 1,874,000 の上)

### 戻せるか

戻せない。駅と道と管は取り壊しで戻せるが、取り壊しは議決が要るため、建てた後の戻しは議案になる。

### 前の月の答え合わせ

- 前の月(第16月)は案なし。前の月の調査 s16-1(13893 が車を出さない理由)は、13893 に電車の着きがなく(vehicles 0)、車を出さない原因ではないと分かった。8-1 の止まりは、28755 の敷地内の空き待ちとして扱う(調査)
- 第16月の整地の試しは、仮定の整地で道が通るまで。実際の整地は未確認のまま

### 市の計画

- 当たる施策: 5-1、5-2 観光(入口)
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: あり
- 問い: 貨物センター 28755 の敷地内で空き待ち(WaitingSpace)の車は、何日止まり続け、台数が減るか。
- 見る道具と引数: `vehicles_stuck`(kind "truck"、building 28755、limit 5)、`cargo`(引数なし)
- いつ見るか: 見回り1・月末
- 何が分かれば次の手が決まるか: 月末で、敷地内の WaitingSpace が 500 以上のまま、7日以上止まった車が減らなければ、8-1 は手段がないとして、第18月に目標を下げる案を出す。台数が 400 以下に減れば、同じ見方で続けて測る。見回りごとに台数が大きく変わるなら、第18月に止まりの原因を道路下水道局と確かめる
- 担当の問題: 8-1 物流・人流のゲートウェイ

## 見たもの

- `city_info`: 人口 175,864、所持金 2,502,262、週の収支 +7,468(収入 333,111、支出 325,643)、観光客 1,875(訪問 158)、来ない市民 0/0/0、dialog なし
- `list_policies`: EducationBoost 有効(週 7,940、第16月末の判定で残した)、FreeTransport 有効(週 0、運賃収入は 0)、SmallBusiness と RecreationalUse は無効。旅客の入口に関係する政策は見当たらない。policyExpensesPerWeek 10,766
- `list_building_types`(PublicTransport): Train Station 建設費 45,000、週 960、16×6、needsRoad、電気・水・下水が要る。Harbor 80,000(週 1,600)、Airport 150,000(週 4,800)。ports は空(置く前は出ない)
- `level_terrain`: 呼ぼうとしたが、この局の道具に含まれず使えなかった(No such tool)。整地の土と費用は未確認
- `test_place_building`(Train Station、-4700、1600、south): ok、cost 45,000、entrance (-4700,1576)、road null、wouldDemolish 0
- `test_place_building`(同じ引数、assume_terrain で level 71.5、同じ polygon): ok、cost 45,000、wouldDemolish 0
- `test_build_line`(Basic Road、[[-4640,1552],[-4700,1552],[-4700,1576]]): 整地の仮定あり ok、segments 2、cost 440、overlaps []。仮定なしは gameCheck に SlopeTooSteep(segment 2)
- `test_build_line`(Water Pipe、[[-2715,215],[-3600,800],[-4500,1300],[-4700,1560]]): ok、segments 32、cost 6,200、overlaps []
- `test_build_line`(Power Line、[[-4650,1500],[-4700,1560]]): ok、segments 1、cost 200、overlaps []
- `net_near`(-4680、1560、r120): Basic Road 13902(node 23669 (-4640,1552)、15652 (-4575,1550))、Power Line 22680(node 15953 (-4650,1500))
- `net_near`(-4650、1500、r250、Electricity): Power Line 22680(node 7825 (-4655,1466) から node 15953 (-4650,1500)、34m)
- `net_near`(Water、-4700、1600、r150): 0 件
- `net_near`(Water、-2720、215、r250): 本土の Water Pipe 18 件(例 (-2715,50)〜(-2655,190))。島への経路は未確認
- `water_trace`(-4700、1600): 近くの水の網 0、街の水 容量 2,400,000 使用 1,904,208
- `height_at`(-4700、1590): 地面 81.1m、水面 81.1m
- `map_layer`(landvalue、-4650、1580、r120、n 5): 平均 2(0〜15)
- `net_reach`(-4650、1560、r150): roads 6、notEnterable 0、notLeavable 0
- `vehicles_stuck`(truck、28755、limit 5): vehicles 750。WaitingSpace の InGrounds 596、WaitingSpace の OnRoad 97、OnRoad の Blocked 55、7日以上止まった 491、1日未満 259

## 判断の根拠

島Bの旅客の駅は、5-1、5-2 の旅客の入口を 0 から 1 にする唯一の手で、17か月の観光の重点に当たる。駅と入口の道は道具で通ると確かめた。再調査で、水管(6,200)と電線(200)は test_build_line で通った。ただし整地の実費は、局の道具で test できないため未確認で、必須条件が残る。駅の ports への接続も未確認。実行可否は「未確認」のままとした。案は1件で、ほかの候補(空き地の名所、島の道の接続)は、旅客の入口の数に直接効かないか、同じ整地の条件を持つため、今月は1件に絞った。8-1 は、振り分けの案を取り下げ、止まりの調査を1件出した。

## 捨てたもの

- 貨物センター28755 の横に2つ目の Cargo Center(建設費 60,000、週 1,440): 場所と接続が未確認で、週の維持費も重い。止まりの調査の結果を見てから決める
- 13893 の増車(電車の着きがない): 13893 は電車の着きがなく、車を出さない理由ではない(前の月の調査)。取り上げない
- 島の旅客の駅を、整地なしで置く案: 入口の道が SlopeTooSteep で通らない(test_build_line の gameCheck)。整地を前提にした案1に含める
