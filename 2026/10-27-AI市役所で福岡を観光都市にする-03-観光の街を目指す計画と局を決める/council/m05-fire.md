# m05 消防局の案

## 案1: 工場 12882 の地区に煙探知機(SmokeDetectors)を試す

### 施策

- 案の id: fire-1
- 施策: 工場 12882 (2184,-918) の周り半径150m を地区「工場」に塗り(`paint_district`)、その地区だけに政策 SmokeDetectors をかける(`set_district_policy`)。3-4 の火事の印を減らす試し
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `paint_district(x=2184, z=-918, radius=150, name="工場")`(地区を作る。erase は使わない)
  2. `list_districts` で、地区「工場」の番号と cells を確かめる。HighTech(126、中心 481,-323)と重なれば、重なりを記録する
  3. `set_district_policy(district="工場", name="SmokeDetectors", active=true)`
  4. 戻り値の週の費用と、`list_policies` の policyExpensesPerWeek を確かめる
- 設置条件の確認:
  - `list_policies`(5月): SmokeDetectors は active=false、costPerWeek 57,743(街全体の見積もり。11,278棟 × 5.12)。地区だけなら、地区内の棟数で決まる
  - `buildings_near`(x=2184, z=-918, radius=150): 67棟。Fire の印は工場 12882 の1棟(FatalProblem)
  - `zone_map`(x=2184, z=-918, radius=200): 工場、事務所、住宅が混在。道路沿いに区画がある
  - `list_districts`: 工場周りに地区はなし。HighTech(126)、Hakata(127)のみ
- 接続工事: 不要
- 予備候補: 半径を100m に縮める(同じ道具、中心は同じ)。週の費用が 500 を超えたときに使う
- 中止する条件: `set_district_policy` の週の費用が 500 を超え、かつ半径100m でも超えるとき。週の収支が +3,000 を割るとき

### 期待する効果

- 改善の見込み: 工場 12882 の Fire の印(FatalProblem)が消えると予想する。確認した事実として、消防車は 0/8 台しか使われておらず、工場の近くに消防署が2つある(25877 と 32853)。消防車の数は足りているので、火元の起こりやすさを下げる手を試す
- 数値と期限: 工場 12882 周り150m の Fire の印は、今 1(5月1日)。6月の見回り1・見回り2・月末で 0 を見込む。確かな数字ではない
- 確認方法: `buildings_near`(x=2184, z=-918, radius=150, problem="Fire", brief=true)の件数。`complaints` の Fire(全体は 6)。今の値と同じ範囲で比べる
- 不確かな点: 道具の説明に、SmokeDetectors の火事への効きの記述はない(`list_policies` は費用だけ)。効きの量は見積もれない。地区の棟数で週の費用が変わる
- 試し: 試し。仮説: 煙探知機が地区の棟の火事の起こりやすさを下げ、工場 12882 の Fire の印が消える。測る数: `buildings_near` の Fire の件数(半径150m)。場所: 工場 12882 周り150m。基準: 1棟(5月1日)。編成方針の「分からないこと」のうち、火事の印の原因(Fire House の効き)に当たる

### 費用

- 建設費: 0
- 週の維持費の増え分: 約343(67棟 × 5.12 の上限の見積もり。地区の棟数で変わる)。`paint_district` の費用は道具の説明に記載がないため未確認。実行前後の所持金で確かめる

### 戻せるか

戻せる。`set_district_policy` で active=false、`paint_district` で erase=true にすれば戻る。

### 前の月の答え合わせ

- m04-5 Fire House(消防署 25877、(2262,-1190)): 予想は周り200m の火事 1→0。結果は 1 のまま(工場 12882 が FatalProblem)。外れ。理由の見立て: 消防車は足りており(0/8 台)、火元の起こりやすさが残っている。覆いは 107→173 に上がった(事実)。次の扱い: 消防署を足す手(候補B)は今月は出さない。工場の火事は、この案で火元の側から試す

### 市の計画

- 当たる施策: 3-4 日常生活の安全・安心
- 編成方針の重点に当たるか: 当たらない(重点は観光、交通、環境。火事は重点の外だが、担当の数字(火事6、目標の合計4以下)のため出す)

## 調査

- 調査: あり
- 問い: 3255・-805 周りの3棟(2002、5804、13425)が、消防車が空いているのに燃え続けるのはなぜか。
- 見る道具と引数:
  1. `buildings_near`(x=3255, z=-805, radius=120, problem="Fire"): 燃えている棟と印
  2. `buildings_near`(x=3290, z=-604, radius=400, service="FireDepartment"): 消防署の消防車の使用(stats の Fire engines in use)
  3. `map_layer`(type="fire", x=3255, z=-805, radius=150, n=3): 消防署の覆い
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか:
  - 燃えが消え、覆いが高いまま → 調査を閉じ、事業3を終える
  - 燃えが続き、消防車の使用が7/8以上 → 消防署の候補(3255 周りに消防署を足す)を6月の案に出す
  - 燃えが続き、消防車の使用が0〜6/8 → `net_reach`(x=3255, z=-805, radius=120)で道を確かめる。道が原因なら、道路下水道局に道の手を求める
- 担当の問題: 3-4 日常生活の安全・安心

## 見たもの

- `city_info`: 人口 178,380、所持金 2,111,160、週の収支 +10,614(収入 345,801、支出 335,187)、観光客 1,811、来ない市民 0/0/0、需要 住24・商4・工58
- `complaints`: Fire 6棟(hotspot (3255,-805) の3棟: 2002、5804、13425)、Crime 1棟(16718)、Pollution 29、Garbage 14、NoGoods 239、Death 52
- `services`: 電気・水・下水に余裕、garbage.full 0、deathcare.full 0、police 366 / 980、crimeRate 5
- `list_policies`: SmokeDetectors active=false、costPerWeek 57,743(街全体の見積もり、11,278棟 × 5.12)。RecreationalUse active=false。SmallBusiness active=true(311)。BigBusiness active=true(3,908)。policyExpensesPerWeek 10,960
- `events`: messages 0件
- `buildings_near`: 
  - (3255,-805)、radius 400、FireDepartment: Fire House 49026(3290,-604)、18411(3595,-604)
  - 同、radius 250、problem=Fire: 2002、5804、13425 が Fire、FatalProblem
  - (3290,-604)、radius 30、FireDepartment: 49026 の Fire engines in use 0/8
  - (3595,-604)、radius 30、FireDepartment: 18411 の Fire engines in use 0/8
  - (2262,-1190)、radius 60: Fire House 25877 の Fire engines in use 0/8
  - (2253,-880)、radius 20: Fire House 32853 の Fire engines in use 0/8
  - (2184,-918)、radius 250、FireDepartment: 32853 と 25877 の2棟
  - (2184,-918)、radius 150、problem=Fire: 工場 12882 のみ(Fire、FatalProblem)
  - (0,0)、radius 5000、problem=Fire: 6棟(2002、5804、12882、13425、26395、31698)
  - (2184,-918)、radius 150: 67棟(total)
- `list_building_types`(FireDepartment): Fire House 12,000(週 560)、Fire Station 60,000(週 1,440)。どちらも解禁済み
- `list_building_types`(Police): 一覧は空(解禁の警察系の返りなし。警察署 45584 は既存)
- `map_layer`(fire): (3255,-805) 半径300、n=7: 平均 200(88〜317)。(2184,-918) 半径200、n=5: 平均 180(137〜218)
- `net_reach`(x=3255, z=-805, radius=200): 道路21区間、届かない0。建物98、届かない0
- `vehicles_stuck`(kind=hearse、limit=3): 霊柩車159台。今回の判断には使わず(誤って呼んだ)
- `list_districts`: HighTech(126、中心 481,-323、8,244 cells)、Hakata(127、299,49)。工場周りに地区はない
- `zone_map`(x=2184, z=-918, radius=200, size=500): 工場、事務所、住宅が混在

## 判断の根拠

- 3255周りの3棟は、消防車が 0/8 台しか使われていない消防署(49026、18411)の覆いの中にある。消防車の数が足りないとは言えない。候補B(消防署を足す)は、トリガー(7/8以上)に当たらないため出さない
- 工場 12882 も、消防署 25877(約290m)と 32853(約80m)の覆いの中で、消防車は 0/8 台。4月の消防署は、この工場の火事を減らさなかった。事業2の閉じる条件(減らず、出動に問題がない)を満たしたため、消防署の手を閉じる
- 工場の火事は、火元の側から試す。地区の煙探知機(SmokeDetectors)を工場の地区にだけかける。街全体の 57,743 は週の収支(+10,614)を超えるため使わない
- 案は1件。火事の印(6)のうち工場の1棟に効く見込みがある唯一の確認済みの手。3255 の3棟は調査にとどめる。政策は月1件の上限があるため、2件目は出さない
- 調査は1件。3255 の燃え続けの原因(消防車が空いているのに燃え続ける理由)が分からないため

## 捨てたもの

- 候補B(3255 周りに消防署を足す): 消防車が 0/8 台しか使われておらず、トリガー(7/8以上)に当たらない
- 工場周りに消防車(Fire Station、60,000、週 1,440)を足す: 工場の近くに消防署が2つあり、消防車は空いている。効きの見込みがない
- 街全体の SmokeDetectors(週 約57,743): 週の収支 +10,614 を超え、守る線を破る
- 3255 の3棟に地区の煙探知機: 調査の結果が出る前に、政策の上限(月1件)を使うことになる。調査の結果で次の月に出す
- 警察署の追加: 犯罪の印は1で、目標(合計4以下)の範囲。犯罪の印の事業1を続ける
