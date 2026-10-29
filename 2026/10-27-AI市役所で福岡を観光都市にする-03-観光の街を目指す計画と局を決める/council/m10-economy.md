# m10 経済観光文化局の案

## 案1: 名所 Servicing Services を (1580, -530) に置き、道と電気と水をつなぐ

### 施策

- 案の id: economy-1
- 施策: 名所(Monument)の Servicing Services を、座標 (1580, -530) に、向き south(angle 180)で置く。道は (1580, -582) から (1700, -582) へ引き、電気は (1683, -514) から、水は (1694, -536) から、置いた建物のつなぎ口へつなぐ。道具は place_building、build_line
- 議決: 要らない

### 実行計画

- 実行可否: 未確認
- 再調査の結果: 条件は満たせなかった。`list_building_types`(service Monument と Electricity)の ports は、解禁済みの全種類で [] だった。`buildings_near`(service Monument、半径 5000)の既存の名所の ports も [] で、ports の値は得られない。`test_place_building`(Servicing Services、1580、-530、south)の戻り値にも ports はなく、電気と水のつなぎ口の座標は計算できない。`test_build_line`(Basic Road、[[1580,-582],[1700,-582]])は ok だが、戻り値に接続先(ends)がなく、入口の道路が既存の Medium Road(`net_near`、x 1640、z -550、半径 120 で見た segment 11011、x 約 1705 の区間)につながるかは確かめられなかった。この区間は道路の端から約 5m の位置にある。建物を置く前は接続を確かめられず、置くと街が変わるため、再調査では置かなかった。
- 対象と操作順:
  1. `place_building`: prefab Servicing Services、x 1580、z -530、facing south(angle 180)。戻り値の ports(電気と水のつなぎ口)と entrance を記録する
  2. `build_line`: prefab Basic Road、points [[1580, -582], [1700, -582]]。入口の道路として、建物の entrance に合わせる
  3. `build_line`: prefab Power Line、points [[1683, -514], [1580, -530]] の終点を、手順1の電気のつなぎ口に合わせて直す。引く前に `test_build_line` で確かめる
  4. `build_line`: prefab Water Pipe、points [[1694, -536], [1580, -530]] の終点を、手順1の水のつなぎ口に合わせて直す。引く前に `test_build_line` で確かめる
- 設置条件の確認:
  - `test_place_building`(Servicing Services、1580、-530、south): ok。cost 20,000。entrance (1580,-582)、road null、wouldDemolish 0
  - `test_build_line`(Basic Road、[[1580,-582],[1700,-582]]): ok。segments 2、cost 640、overlaps []
  - `test_build_line`(Power Line、[[1683,-514],[1580,-530]]): ok。cost 280、overlaps []
  - `test_build_line`(Water Pipe、[[1694,-536],[1580,-530]]): ok。cost 280、overlaps []
  - 未確認: 電気と水のつなぎ口の位置(手順1の戻り値でしか分からない)。上の2本の線は、終点を (1580, -530) に置いて試したので、つなぎ口が違えば試し直しが要る
  - 未確認: 入口の道路が既存の道路(Medium Road、x 約1704)に接続する形。test_build_line は接続の形を返さない
  - 確認済み: 1485,-460 から (1580,-530) への送電線は、道路 z=-470 の ObjectCollision で断られる。このため経路を (1683,-514) からに替えた
  - `water_trace`(1517, -494 付近の建物で確かめた網): 水と下水の網は1つで、取水口と排水口につながる。(1580,-530) は、この網の中の未接続の点
  - `map_layer`(attractiveness、x 1580、z -530、radius 150、n 5): 基準の平均 6、最大 117(1430, -680 付近)、最小 0
- 接続工事: 道路 [[1580,-582],[1700,-582]] 640、送電線 [[1683,-514],[1580,-530]] 280、水道管 [[1694,-536],[1580,-530]] 280(建設費の合計 1,200)
- 予備候補: なし。電気・水のつなぎ口が (1580,-530) と合わない場合は、置いた建物の位置の変更を、市長に戻す。今月は案を増やさない
- 中止する条件:
  - 手順1の `place_building` が断られた、または ports が出ない → 中止
  - 電気・水のつなぎ口が (1580,-530) から 10m 以上離れ、送電線と水道管の試しが断られる → 中止し、市長へ戻す
  - 所持金が 1,874,000 を割る、または週の収支の見込みが +3,000 を割る → 中止

### 期待する効果

- 改善の見込み: 名所(Monument)は1種類1棟なので、名所の数(9 → 10)と attractiveness の平均(2付近)を増やす。観光客が寄る範囲は名所のまわりに広がると予想するが、効き目の大きさは見積もれない。
- 数値と期限: 名所の棟数 9 → 10(目標 10 以上を達成)。attractiveness の平均は、今の値を基準に、名所の周り 300m の範囲で増えるかを見る。期限は第11月末
- 確認方法: `buildings_near`(service=Monument)の棟数。`map_layer`(attractiveness、x 1580、z -530、radius 300、n 5)を、置く前と同じ条件で測り比べる。`city_info` の tourists(now と visits)、`economy_breakdown` の Tourism
- 不確かな点: 電気と水のつなぎ口が未確認(実行可否が未確認の理由)。効き目の大きさは見積もれない。名所の周りの空きが少ないため、attractiveness の変化は見えにくいかもしれない。観光客の増減は、入口(旅客の駅・港)がないと出にくい(市の計画の注記)
- 試し: 効き目が分からないため、試しとして出す。仮説: 名所が attractiveness を上げ、観光客が寄り、Tourism の収入が増える。測る数: `map_layer` の attractiveness(x 1580、z -530、radius 300)と `buildings_near` の Monument。場所: (1580, -530)。基準: 平均 6(radius 150 の範囲)。編成方針の分からないこと「観光の名所・入口で観光客と Tourism は増えるか」に当たる

### 費用

- 建設費: 21,200(名所 20,000、道路 640、送電線 280、水道管 280)。`test_place_building` と `test_build_line` で確かめた額
- 週の維持費の増え分: 約 348 以上(名所 320、道路 0.64km × 40 = 25.6、水道管 0.28km × 10 = 2.8)。送電線の維持費は `list_net_types` で未確認(小さい見込み)
- 週の収支の見込み: 8,997 − 約348 = 約8,650(守る線 +3,000 以上)。所持金の見込み: 2,270,429 − 21,200 = 2,249,229(守る線 1,874,000 以上)。10月の維持費の増え分の上限 3,700 以内

### 戻せるか

戻せる。置いた名所は、取り壊しの議決で戻せる。議決は取り壊しとして扱う。建設そのものは、議決なしで行う。

### 前の月の答え合わせ

なし(9か月目は案を出さず、名所の事業を停止中にした。確かめた事実: 1580,-530 は電気が届かず、送電線が要る。9月に案を出さなかったため、前の月の期限の判定はない)

### 市の計画

- 当たる施策: 5-1、5-2 観光(名所の棟数と attractiveness、Tourism の収入)
- 編成方針の重点に当たるか: 当たる(重点1: 5-1・5-2 観光)

## 調査

- 調査: あり
- 問い: 名所 Servicing Services を (1580, -530) に置いたあと、attractiveness の平均が、置く前の基準より増えるか。
- 見る道具と引数: `map_layer` の type attractiveness、x 1580、z -530、radius 300、n 5(置く前の値を基準に比べる)。`buildings_near` の service Monument、x 1580、z -530、radius 300
- いつ見るか: 月末
- 何が分かれば次の手が決まるか: attractiveness が増えたら、2棟目の名所を別の場所で試す(第11月の予定)。増えなければ、観光客の多い店の近くに置く案を第11月に試す。Monument の数が増えていなければ、置けなかった理由を `buildings_near` の problem で確かめる
- 担当の問題: 5-1、5-2 観光

## 見たもの

- `city_info`: 人口 180,117、所持金 2,270,429、週の収支 +8,997、観光客 1,705(訪問 140)、来ない市民 0/0/0、dialog なし
- `list_policies`: 有効は SmokingBan(費用 0)と BigBusiness(3,952/週)。RecreationalUse は無効(費用 0)。SmallBusiness は無効(317/週)。政策の費用合計 10,774/週。観光に効く政策の効きは、一覧に記述がなく、実測もない
- `list_building_types`(service Monument、解禁済み): 24種類、建設費 20,000〜200,000。Servicing Services は 20,000、維持費 320/週、12×13。このリストは建物の建ち具合を含まないので、建て済みの名所(SeaWorld、ScienceCenter、Friendly Neighborhood など)は、置くと AlreadyExists になる
- `buildings_near`(service=Monument): 9棟(今月の計画の前提と同じ)
- `zone_map` / `zone_summary` / `zones_at`: 街の中心は道路と建物でふさがり、道に面した空きが少ない(前月の記録と同じ)
- `test_place_building`(Servicing Services、1580、-530、south): ok。cost 20,000、entrance (1580,-582)、road null、wouldDemolish 0
- `test_place_building`(Servicing Services、1430、-640): ObjectCollision(Expensive Park 2849、Pedestrian Pavement)。候補から外す
- `test_place_building`(Servicing Services、1930、-260): ObjectCollision(道路と集合住宅、JapaneseGarden 27477)。候補から外す
- `test_place_building`(Servicing Services、2520、-440)、(2780、-150): ObjectCollision。候補から外す
- `test_build_line`(Basic Road、[[1580,-582],[1700,-582]]): ok。segments 2、cost 640、overlaps []
- `test_build_line`(Power Line、[[1485,-460],[1580,-530]]): ObjectCollision(Basic Road 24553、34893、z 約 -470)。断られた
- `test_build_line`(Power Line、[[1683,-514],[1580,-530]]): ok。cost 280、overlaps []
- `test_build_line`(Water Pipe、[[1694,-536],[1580,-530]]): ok。cost 280、overlaps []
- `list_net_types`(service Water): Water Pipe 2,500/km、維持費 10/km/週。Sewage は該当なし
- `list_net_types`(Road): Basic Road 5,000/km、維持費 40/km/週。Medium Road 7,500/km、維持費 100/km/週
- `water_trace`(1580、-530 の近く): 水と下水の網は1つで、取水口と排水口につながる。都市の容量は水 2,400,000 中 1,926,064、下水も同じ
- `map_layer`(attractiveness、x 1580、z -530、radius 150、n 5): 平均 6、最大 117、最小 0。基準値

## 判断の根拠

- 観光の数字(観光客 1,705、Tourism 週 42、attractiveness 平均 2)は、いずれも目標から遠い。名所の棟数は 9 で、目標 10 に1棟足りない。名所を1棟足すのが、確かめられた手の中で最も直接に効く
- 候補地は街の中の4か所(1580,-530、1430,-640、1930,-260、2520,-440)を試した。1580,-530 だけが建物の置き場所として通った
- 1580,-530 は、名所の数と attractiveness の両方に効く見込みがある。電気と水は、経路を (1683,-514) から引き直せば通る見込みがある
- 実行可否は「未確認」。電気と水のつなぎ口は、建物を置いてからでないと分からない。試しの道具で確かめた線も、つなぎ口の位置が違えば試し直しになる。このため executionReady は false
- 費用は 21,200(建設)、約 348/週(維持)。守る線(週の収支 +3,000、所持金 1,874,000)と、10月の維持費の上限(3,700)に収まる
- 案は1件にした。候補地の空きが少なく、2件目は同じ地区で試すしかないため、件数を埋めるための案は出さない
- 調査は1件。名所を置いたあとの attractiveness の変化を、置く前の基準と比べて確かめる。効き目が分からない手なので、次の月の手を決めるために必要

## 捨てたもの

- 島Bへの名所(StatueOfWealth は AlreadyExists。島Bの電気・水は風力 44460 のみで、名所を置く場所に網がない): 配管と電気の延長が要り、費用と操作が多い。今月は見送る
- 空き地3の名所 11580 の電気の修理: 前月まで5回、同じ手を続けた。6回目は打たない(編成方針)
- 旅客の入口(港湾空港局の担当): 局の担当外。港湾空港局に求める事業として計画に残す
- 政策 RecreationalUse の有効化: 前月の実測で効きが分からないまま外した(4月)。効きの記述は一覧にない。今月は出さない
- 政策 SmallBusiness の有効化(317/週): 観光の収入の効きが実測されておらず、前月まで採られた実績でも効果が見えない。今月は出さない
- 公園 23298 の道の接続: 担当が道路下水道局と住宅都市みどり局。局の担当外
