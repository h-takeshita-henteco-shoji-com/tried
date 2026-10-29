# m04 消防局の案

## 案1: 火事の印の近く(3243,-789)に Fire House を1棟置く(住宅3棟を取り壊す)

### 施策

- 案の id: fire-1
- 施策: 火事の印の集まり(3243,-789)の北東 102m、(3330,-735) に Fire House を1棟置く。入口は南向き(道路 segment 24255 に面する)。道路の Basic Road は入口から15m。道具は `place_building`(prefab "Fire House"、x 3330、z -735、facing "south"、pay true)。
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 議決(取り壊し)が通ったあと、`place_building` を prefab "Fire House"、x 3330、z -735、facing "south"、pay true で1回呼ぶ。区画の建物 5246(L3 2x3 Semi-detachedhouse02)、8314(L3 3x4 Semi-detachedhouse03a)、45408(L4 3x2 Villa02b)が取り壊される(家 11 を失う。働き口 0)。
  2. 置いた後、`place_building` の戻り値の entrance.road と demolished を確かめる。
  3. `advance` は取り壊しの前に呼ばない(m02-1 の失敗と同じ)。
- 設置条件の確認:
  - `test_place_building`(Fire House、3330,-735、south): ok。位置と向きは直されない(angleUsed 180)。費用 12,000、所持金は足りる。
  - 取り壊しは `wouldDemolish` の 3 棟(5246、8314、45408)だけ。`preview_bulldoze`(半径20、what building)は 3330 付近ではなく、3250,-728 の候補で 1 棟(35964)を見た。同じ候補の判定は採らない。
  - 入口: entrance.road は segment 24255(Basic Road、距離15m)。16m以内なので道路に面する。
  - 電気・水・下水: `buildings_near`(3330,-735、r40)の周りの棟は困りごとなし。`citizens_without_service` の全市は 0 / 0 / 0(`city_info`)。Fire House 49026(3290,-604)は grid が true。
  - 敷地の重なり: 障害は取り壊しの3棟だけ(`test_place_building` の colliding なし)。
- 接続工事: 不要
- 予備候補: なし(確認済みの予備はない。(3250,-728) は入口の道路がなく、(3150,-700) は入口の道路まで 76m 以上あるため採らない)
- 中止する条件: `test_place_building` が ok でなくなる。wouldDemolish が 5246、8314、45408 以外を含む。entrance.road が null になる。費用が 12,000 を超える。どれかに当たれば、実行せず見送る。

### 期待する効果

- 改善の見込み: 火事の印は (3243,-789) の 3 棟に集まる。今の一番近い消防署 49026(3290,-604)は約 190m 離れ、火事の覆いは印の場所で 200 を超えている。その署は 8 台のうち 1 台しか動いておらず、印の学校 5804 には消防車が 0 台のまま。署を印の近くに置けば、出動までの距離が約 90m 縮まる。火事の印が減るかは、覆いの高さでなく出動の速さで決まると見る(局の予測。確証はない)。
- 数値と期限: 火事の印(`complaints` の Fire、今の 5 棟。hotspot の 3 棟)。期限は次の月例(約30日後)。見込みは、hotspot の火事の印が 3 棟から 1 棟以下に減ること。量は見積もれない。
- 確認方法: `complaints`(type Fire の buildings と hotspot)と `buildings_near`(x 3243、z -789、r150、problem "Fire")。新しい Fire House(3330,-735)の `buildings_near` の vehicles.inUse と stats("Fire engines in use")。基準は今の値(火事 5 棟、hotspot 3 棟、学校 5804 の vehicles.inUse 0、Fire House 49026 の 1/8)。
- 不確かな点: 印が消えない原因は、覆いの高さではなく出動の不具合かもしれない(学校 5804 は生徒 0 のまま燃え続け、消防車が 0 台)。署を足しても出動しなければ効かない。取り壊し 3 棟・家 11 を戻せない。
- 試し: 仮説: 火事の印の近くに署を置くと、出動が早まり、火事の印が減る。測る数: `complaints` の Fire 棟数(hotspot (3243,-789) r150)、`buildings_near` の problem Fire の棟数(x 3243、z -789、r150)、新しい署の vehicles.inUse。場所: (3330,-735) の署の周り r150。基準: 火事 5 棟、hotspot 3 棟、Fire House 49026 の 1/8、学校 5804 の inUse 0。編成方針の分からないこと「消防署をどこに置けば火事の印が減るのか」に当たる。

### 費用

- 建設費: 12,000(`list_building_types` の Fire House。`test_place_building` の cost と同じ)
- 週の維持費の増え分: 560(`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せない。取り壊した住宅 3 棟(家 11)は元に戻せない。

### 前の月の答え合わせ

なし(前の月の案は出ていない。m03 は案なし)。前にこの課題で出た m01-fire-1(Fire House を (3300,600) に置いた案)は外れ。火事の印 (3256,-789) から約 1,400m 離れていた。今月は印の 100m 付近に置く形に直した。

### 市の計画

- 当たる施策: 3-4 日常生活の安全・安心
- 編成方針の重点に当たるか: 当たらない(重点外の案。編成方針が消防局に求める案)

## 案2: 犯罪の印の近く(3695,-90)に Police Station を1棟置く

### 施策

- 案の id: fire-2
- 施策: 犯罪の印の集まり(3695,-90)の南東 90m、(3770,-140) に Police Station を1棟置く。入口は北向き(道路 segment 32778 に面する、距離10m)。道具は `place_building`(prefab "Police Station"、x 3770、z -140、facing "north"、pay true)。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building` を prefab "Police Station"、x 3770、z -140、facing "north"、pay true で1回呼ぶ。取り壊しはない。
  2. 置いた後、戻り値の entrance.road(segment 32778)と demolished が 0 であることを確かめる。
- 設置条件の確認:
  - `test_place_building`(Police Station、3770,-140、north): ok。位置と向きは直されない(angleUsed 0)。費用 12,000、所持金は足りる。wouldDemolish 0。
  - 入口: entrance.road は segment 32778(Basic Road、距離10m)。
  - 最初の試し(3770,-128、north)は道路 segment 32778 と重なり断られた。そのため 12m 南(z -140)に下げた。
  - 電気・水・下水: `buildings_near`(3770,-140、r60)の周りの棟(小学校 2030、Villa 29205、44223)は困りごとなし。`city_info` の citizensWithoutService は 0 / 0 / 0。
- 接続工事: 不要
- 予備候補: なし(確認済みの別の候補はない)
- 中止する条件: `test_place_building` が ok でなくなる。entrance.road が null になる。wouldDemolish が 0 でなくなる。費用が 12,000 を超える。どれかに当たれば、実行せず見送る。

### 期待する効果

- 改善の見込み: 犯罪の印 3 棟のうち 2 棟が (3695,-90) の近く(2 棟)。今の警察の覆いはこの地点で 145(9 点の 5×5 の中央付近)で、既に届いている。新しい署が近くにあれば、覆いの高さが上がり、犯罪の印が減ると見る(局の予測。覆いの増え方は量を見積もれない)。m01-6 の Police Station(犯罪の印 3→1、覆いのある区域で効いた)と同じ手。
- 数値と期限: 犯罪の印(`complaints` の Crime、今 3 棟。hotspot 2 棟)。期限は次の月例(約30日後)。見込みは、hotspot の犯罪の印が 2 棟から 0〜1 棟になること。量は見積もれない。
- 確認方法: `complaints`(type Crime)と `map_layer`(type police、x 3695、z -90、radius 150、n 5)。基準は今の値(犯罪 3 棟、警察の覆い 中心 145、平均 122)。
- 不確かな点: 犯罪の印は 3 棟と少なく、効きの大きさは小さい見込み。hotspot の位置から 90m の場所に置くので、覆いの増え方は分からない。
- 試し: なし(m01-6 と同じ手。効きは見積もれないが、置く条件は確認済み)

### 費用

- 建設費: 12,000(`list_building_types` の Police Station。`test_place_building` の cost と同じ)
- 週の維持費の増え分: 480(`list_building_types` の Police Station の upkeepPerWeek。m01-6 と同じ額)

### 戻せるか

戻せる(建物を取り壊せば戻る。取り壊しには議決が要る)。

### 前の月の答え合わせ

なし(前の月の案は出ていない。m03 は案なし)。前の月の関連: m02-fire-1(港の Police Station (-572,1090))は犯罪の印 1→0 で効いた(m02-3)。今月の案は、同じ手を犯罪の印の近くに当てる。

### 市の計画

- 当たる施策: 3-4 日常生活の安全・安心
- 編成方針の重点に当たるか: 当たらない(重点外の案)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `city_info`: 人口180,759、所持金2,145,261、観光客1,625/161、週の収支+10,033(収入346,977、支出336,944)、需要25/2/57、電気・水・下水が来ない市民 0 / 0 / 0、dialog null
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940/週)、RecreationalUse(0)、BigBusiness(3,952/週)。SmokeDetectors は無効で 57,784/週(上限 5,000 を超えるため採らない)。PowerSaving、WaterSaving は無効で 58,353/週。火事と犯罪に効く政策は費用が大きいか、効きの見込みがない
- `complaints`: 火事 5 棟(hotspot (3243,-789) 3 棟)、犯罪 3 棟(hotspot (3695,-90) 2 棟)、ごみ 28、汚染 26、死亡 42、品物がない店 228
- `events`: 対象外のつぶやき 0 件
- `map_layer`(type fire、x 3243、z -789、radius 300、n 5): 平均 196、min 87、max 314(印の周りは 200 前後)
- `map_layer`(type police、x 3695、z -90、radius 300、n 5): 平均 122、中心付近 145(5×5 の中央列 145〜170)
- `buildings_near`(x 3290、z -604、r30、service FireDepartment): Fire House 49026、problems None、engines in use 1 / 8、workers 31
- `buildings_near`(x 3243、z -789、r120、problems_only): 住宅 37109(Garbage)、38574(Fire, FatalProblem)、45275(Garbage)
- `buildings_near`(x 3125、z -836、r20): 小学校 5804、problems "Fire, FatalProblem"、vehicles inUse 0、生徒 0 / 348
- `buildings_near`(x 3330、z -735、r40、brief): 5246、8314、45408(取り壊しの 3 棟。困りごとなし)
- `buildings_near`(x 3770、z -140、r60、brief): 小学校 2030、Villa 29205、44223(困りごとなし)
- `services`: 警察 385/1000、埋立地満杯 8、犯罪率 5
- `economy`: 税は前月と同じ。予算 fire 140 / police 150(昼夜)
- `traffic`(x 3230、z -700、r250): 流れ 53、blocked 0、火事の区域は詰まりなし
- `net_reach`(x 3150、z -780、r200): 道路 18 区間、入口から入れない 0、建物の来られない 0。火事の区域は車で来られる
- `list_building_types`(FireDepartment): Fire House 12,000 / 560 / 4×3、Fire Station 60,000 / 1,440
- `zone_map`(x 3230、z -740、r200): 印の周りの配置を確認(Fire House 49026 は上部)
- `test_place_building`: Fire House (3250,-728) south は入口の道路なし(断る条件ではないが採らない)。Fire House (3330,-735) south は ok(取り壊し 3)。Fire House (3300,-870) north は道路と建物で断られた。Fire House (3380,-770) west は道路と建物で断られた。Fire House (3150,-700) north は ok だが入口の道路なし(採らない)。Police Station (3770,-128) north は道路で断られた。Police Station (3770,-140) north は ok
- `preview_bulldoze`(x 3250、z -728、r20、what building): 35964 の 1 棟(家 4)。候補 (3250,-728) は採らないため、参考だけ
- `zone_map`(x 3690、z -90、r150): 犯罪の印の周りの配置を確認
- `vehicles_stuck`(kind hearse、limit 3): 霊柩車の止まり 141 台(消防局の案と関係なし。参考だけ)

## 判断の根拠

- 火事の印 5 棟のうち 3 棟は (3243,-789) に集まり、最寄りの消防署 49026 までは約 190m ある。前の月の署は 1,400m 離れて効かなかった。今月は印の 100m 付近に置く案を出す。(3330,-735) は入口の道路があり、取り壊しは 3 棟のみで、必須条件は確認済み。
- 火事の出動の不具合(学校 5804 に消防車 0 台、署は 8 台中 1 台)は原因が分からない。そのため案1は試しの形で出す。
- 犯罪の印 3 棟は、警察の覆いが 145 で既に届いている。それでも近くに置く案は、m01-6 で効いた手で、条件は (3770,-140) で確認済み。火事と犯罪の合わせて 8 を 4 以下へ戻す手として、別の手の案2を出す。
- 政策は、SmokeDetectors(57,784/週)などが上限を超えるため、どれも採らない。
- 案は2件。3件目以降は、同じ手の言い換えか、効きの見込みがない手になるため出さない。

## 捨てたもの

- SmokeDetectors(火事の政策): 週の費用 57,784 で、維持費の上限 5,000 を超える。採らない
- Fire House (3250,-728): 入口の道路が 16m 以内にない。道路を引く工事は確認できていないため採らない
- Fire House (3150,-700): 入口の道路まで 76m 以上あり、道路を引くと建物の取り壊しを伴う見込み。確認できていない
- Fire House (3300,-870) north、(3380,-770) west: 道路と既存の建物にぶつかり、断られた
- Fire Station(60,000 / 1,440/週): 建設費が大きく、効きの見込みも Fire House と同じ出動の問題のため、今月は採らない
- 消防車の予算を 140%→150% へ上げる: 出動の不具合の原因が分からないため、効果の見込みが立たない。費用は小さいが採らない
