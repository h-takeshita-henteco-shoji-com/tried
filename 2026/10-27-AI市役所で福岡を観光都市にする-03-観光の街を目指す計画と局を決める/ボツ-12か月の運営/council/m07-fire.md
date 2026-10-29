# m07 消防局の案

## 案1: 消防の予算を140%から150%に上げる(試し)

### 施策

- 案の id: fire-1
- 施策: 消防の予算を昼夜とも 140 から 150 に上げる。火事の印の近くの消防署(Fire House 49026 at (3290,-604)、18411 at (3595,-604))を含む消防全体が対象。道具は `set_budget`(target `fire`、percent 150)。
- 議決: 予算

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `set_budget(target="fire", percent=150)`。昼と夜を同じ 150 にする。変更値は +10 で、予算の動かせる幅 ±20 の内。上限 150 にちょうど収まる。
- 設置条件の確認: 該当なし(建設なし)。`economy` で fire の予算が現在 day 140 / night 140 と確認。`economy_breakdown` の FireDepartment の週の支出 32,704(予算 140%)から、150% の支出は 32,704 × 150/140 ≒ 35,040(増え分 約 +2,336/週)。
- 接続工事: 不要
- 予備候補: なし(予算の変更のみ)
- 中止する条件: 議決が否決されたら見送る。実行後、`economy_breakdown` の週の収支が 0 を下回るなら `set_budget(target="fire", percent=140)` で戻す。

### 期待する効果

- 改善の見込み: 火事の印は街全体で 4 棟あり、火事と犯罪の合計 4 以下の目標を超えている。火事の印の近くの消防署 49026 は「Fire engines in use: 0 / 8」で、出動中の消防車が見えない。予算を上げると消防車の出動が増え、火事が早く消えると予想する。これは予想で、確認した事実ではない。
- 数値と期限: 今の火事は街全体で 4 棟(hotspot (3243,-789) の 3 棟を含む)。予想は、月末までに火事の印が 2 棟以下に減ること。期限は 1 か月後の月末(30 日目)。消防署 49026 の「Fire engines in use」が 0 から上がるかも同時に見る。数値の見積もりは確かめられていない。
- 確認方法: `complaints` の Fire の buildings 数(街全体)と hotspot の位置。範囲 r150 の `buildings_near(x=3217, z=-790, radius=150, problems_only=true)` の Fire の印。`buildings_near(x=3290, z=-604, radius=15)` の stats「Fire engines in use」。今の値は、街全体の火事 4 棟、r150 の中の Fire 印 2 棟(5804 の学校 (3125,-836)、38574 の住宅 (3217,-790))、消防署 49026 は 0 / 8、18411 は 0 / 8。残りの火事は 2002 の店 (3388,-742) など、r150 の外。
- 不確かな点: 予算が消防の出動の数や消火の速さに効くかは、道具の説明では確かめられていない。消防車が 0 / 8 のままなら、予算は効かないと分かる。予算を上げると財政の枠にも響く(週 +2,336)。
- 試し: あり。仮説: 消防の予算を上げると、消防署の出動(消防車の稼働)が増え、火事の印が減る。測る数: `complaints` の Fire の buildings 数と、`buildings_near` の消防署 49026 の「Fire engines in use」。場所: 火事の hotspot (3243,-789) 周辺 r150 と、消防署 49026 (3290,-604)。基準: 街全体の火事 4 棟、r150 の Fire 印 2 棟、消防車 0 / 8。編成方針の「分からないこと」にはない項目だが、局の 3-4 の効きを確かめる試し。

### 費用

- 建設費: 0
- 週の維持費の増え分: 約 +2,336(FireDepartment の週の支出 32,704 を 140% から 150% に比例して計算。`economy_breakdown` の値から算出)

### 戻せるか

戻せる。`set_budget(target="fire", percent=140)` で元に戻せる。

### 前の月の答え合わせ

なし(前の月の案は出していない。m06 の fire は案なし)

### 市の計画

- 当たる施策: 3-4 日常生活の安全・安心
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2、4-4、6-4、7-1。3-4 は重点外だが、案は歓迎と書かれている)

## 案なし

(案1 を出すため、この見出しは書かない)

## 調査

- 調査: あり
- 問い: 消防署 49026 と 18411 の消防車(0 / 8)は、火事の印(38574、5804、2002 の近く)に向けて出ているか。出ていないなら、出動が止まる原因は何か。
- 見る道具と引数: (1) `buildings_near`(x=3290, z=-604, radius=15, brief=false)の stats「Fire engines in use」と vehicles.inUse。(2) `complaints`(引数なし)の Fire の buildings 数と hotspot。(3) `buildings_near`(x=3217, z=-790, radius=150, problems_only=true)の Fire の印の棟。
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 消防車が見回りのどれかで 1 以上出て、火事の印が減るなら、予算の試し(案1)の効きを待つ。消防車が 0 のまま火事の印が残るなら、消防署の道や接続を調べる次の手にする(建物の入口の道路、交通の流れ、消防署の稼働)。火事の印が 3 以上に増えるなら、予算の試しは外れと判断する。
- 担当の問題: 3-4 日常生活の安全・安心(火事の印)

## 見たもの

- `city_info`: 人口 179,838、幸福度 87、所持金 2,184,832、週の収入 348,600 / 支出 339,782、観光客 1,608 / 157、電気・水・下水が来ない市民 0 / 0 / 0、dialog なし
- `complaints`: 火事 4 棟(hotspot (3243.3,-789.3) 3 棟)、犯罪 2 棟(hotspot (1206,-1136) 1 棟)、汚染 38、ごみ 231、品物がない店 256、死亡 44
- `events`: 新しいつぶやきなし(2050-07-01)
- `list_policies`: 政策一覧を取得。有効なのは SmokingBan(0)、EducationBoost(7,940/週)、RecreationalUse(0)、BigBusiness(3,844/週)。火事に効く候補は SmokeDetectors(無効、57,692/週で、上限 4,000 を大きく超える)のみ。政策費用の合計 10,632/週。
- `services`: 電気・水・下水は容量内。警察 342 / 1,020。満杯の埋立地 9。働き手 82,782 / 働き口 86,457。犯罪率 5。
- `citizens_summary`: 健康 86、幸福度 93、失業 4,689(大学卒 4,597)、badHealth 2,233
- `buildings_near`(x=3290, z=-604, r=15): 消防署 49026(Fire House)の stats「Fire engines in use: 0 / 8」、vehicles.inUse 0、grid は電気・水・下水すべて true、problems None。
- `buildings_near`(x=3595, z=-604, r=15): 消防署 18411(Fire House)も「Fire engines in use: 0 / 8」。
- `buildings_near`(x=3290, z=-604, r=250, service=FireDepartment): 消防署は 49026 と 18411 の 2 棟のみ。
- `buildings_near`(x=3243, z=-789, r=400, service=FireDepartment): 2 棟(同上)。
- `buildings_near`(x=1206, z=-1136, r=400, service=PoliceDepartment): 警察 0 棟。
- `buildings_near`(x=3243, z=-789, r=120, problems_only=true): 38574(L4 4x3 Villa01 (3217,-790)、「Fire, FatalProblem」)、36371(Death, MajorProblem)。
- `buildings_near`(x=3217, z=-790, r=150, problems_only=true): 5804(Elementary School (3125,-836)、「Fire, FatalProblem」)、38574(Fire, FatalProblem)、36371(Death)。
- `buildings_near`(x=3388, z=-742, r=40, brief=true): 2002(L3 1x1 Shop07 (3388,-742)、「Fire, FatalProblem」)。ほかは問題なし。
- `list_building_types`(FireDepartment): Fire Station 建設費 60,000、維持費 1,440/週(解禁済み)。Fire House 建設費 12,000、維持費 560/週。
- `list_building_types`(PoliceDepartment): Police Headquarters 60,000 / 1,600/週、Police Station 建設費 12,000、維持費 480/週、定員 20。
- `map_layer`(type=fire, x=3243, z=-789, r=400, n=9): 消防の覆いは平均 188、hotspot 付近は 250〜300 で高い。
- `map_layer`(type=fire, x=3290, z=-700, r=200, n=5): 範囲内の覆いは 163〜310。
- `map_layer`(type=police, x=1206, z=-1136, r=400, n=9): 警察の覆いは平均 57。hotspot (1206,-1136) 付近は 45 と低い。
- `net_reach`(x=3250, z=-700, r=250): 道路 23 区間、つなぎ口から入れない・出られない 0。建物の到達不可 0。消防署への道はつながっている。
- `net_near`(x=3290, z=-604, r=120): 消防署 49026 の周りは Basic Road(z=-620)と水道管。道はつながっている。
- `traffic`(x=3250, z=-680, r=200): 流れ 53、blocked 0、blockedSpots なし。消防車の詰まりは見えない。
- `zone_map`(x=3240, z=-720, r=180): 火事の印の周辺は住宅(高密度)と商業が密集。空いた区画は見当たらない。
- `test_place_building`(Fire House, 3240,-700, south): ok。ただし入口の道路が null(道路なし)なので、置く案には使えない。
- `test_place_building`(Fire House, 3240,-632, north): ObjectCollision(道路 5173・13598 と Villa 3 棟)。取り壊しが要るため候補から外す。
- `test_place_building`(Fire House, 3140,-632, north): ObjectCollision(道路 29327 と Villa 2 棟)。取り壊しが要るため候補から外す。
- `test_place_building`(Police Station, 1070,-1125, south): ObjectCollision(Library 01 37605 と重なる)。
- `test_place_building`(Police Station, 1100,-1140, south): ObjectCollision(H4 4x4 Tenement12 22230 と Library 01)。
- `test_place_building`(Police Station, 1150,-1135, south): ObjectCollision(Basic Road 1418、Tenement 2 棟)。
- `test_place_building`(Police Station, 1100,-1000, south): ok だが、取り壊し 2 棟(家 36)を伴う。取り壊しは議決が要るため候補から外す。
- `test_place_building`(Police Station, 1075,-1095, north): ObjectCollision(Library 01)。
- `test_place_building`(Police Station, 1255,-1290, north): ObjectCollision(Nuclear Power Plant 32405)。
- `test_place_building`(Police Station, 1040,-1140, east): ObjectCollision(Basic Road 19702・25701、Library 01)。
- `economy`: 税 住宅低9・高7、商業低9・高3、工業3、事務所3。予算 fire は day 140 / night 140、police 150、healthcare 150。
- `economy_breakdown`: FireDepartment の週の支出 32,704、PoliceDepartment 41,583、政策費用 10,632、Tourism 53。
- `vehicles_stuck`(kind=hearse、limit 3): 霊柩車の止まりは 136 台。消防車とは別の車で、消防車の状態はこの道具では見られない。

## 判断の根拠

- 担当の数字は火事 4 棟と犯罪 2 棟で、合計 6。目標 4 以下を 2 超えている。火事が大半で、犯罪は少ない。
- 火事の印の近く(hotspot (3243,-789))には消防署が 186m 先の 49026 にある。覆いは 250〜300 と高く、覆いが足りないとは言えない。消防署 49026 と 18411 は、どちらも「Fire engines in use: 0 / 8」。道はつながり(net_reach で到達可)、交通も詰まっていない(traffic の blocked 0)。原因は道具では確かめられない。
- 消防署を新しく置く案は、火事の印の周りが住宅の密集で、空いた場所がなく、置くには取り壊し(Villa 2〜3 棟)が要る。取り壊しは戻せず、覆いが高いので効きも小さいと見る。候補から外す。
- 警察署は犯罪の印 1 棟の近くに置きたいが、候補の場所はすべてぶつかった(Library、Tenement、道路)。取り壊しを伴う場所 1 つだけ確認できたが、家 36 を失うため採らない。犯罪は 2 棟で、火事の効きより小さい。案なし。
- 政策の SmokeDetectors は週 57,692 で、上限 4,000 を大きく超える。取らない。
- 案1(消防の予算 140 → 150)は、道具で確かめた週の支出 32,704 から、週 +2,336 で、予算の幅 ±20 と維持費の幅 4,000 の内。消防車が 0 / 8 のままの原因が予算で動くかは、道具では分からないため、試しにする。前の月(5 か月目)に予算案が採られなかった理由は「出動の根拠がない」だった。今月は 2 棟の消防署の 0 / 8 を基準として記録し、測る数を消防車の稼働と火事の数にした。根拠はまだ弱いため、試しとして出す。
- 案は 1 件にした。取り壊しや建設を伴う候補は、確認した条件で採れないため。件数を埋めるための案は出さない。
- 調査を 1 件出す。消防車が出ていないかを見回りと月末で追う。原因が分かれば、次の月に手を決める。

## 捨てたもの

- 火事の印の近くに Fire House を新設(3240,-632 north、3140,-632 north): 道路と Villa 2〜3 棟の取り壊しが要る。戻せない。覆いは 250 以上あり効きが小さい見込み。
- Fire Station(建設費 60,000、維持費 1,440/週): 覆いは十分に高く、消防車が出ない原因が分からないまま大きく投資するのは根拠がない。
- 犯罪の印の近くに Police Station を新設(1100,-1000 south): 取り壊しの家 36 が戻せない。ほかの場所(1070,-1125、1100,-1140、1150,-1135、1075,-1095、1040,-1140、1255,-1290)は ObjectCollision で置けない。犯罪は 2 棟で、効きは小さい。
- SmokeDetectors(政策): 週 57,692、上限を大きく超える。
- 消防署 49026 の移設(relocate_building): 近くに空いた場所がなく、移す先の候補を確かめられなかった。費用は建設費の 1/5(約 2,400)で安いが、移す先が未確認のため見送る。
