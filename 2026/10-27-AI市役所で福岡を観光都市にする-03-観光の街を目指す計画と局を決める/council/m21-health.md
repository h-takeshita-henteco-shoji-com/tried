# m21 保健環境局の案

## 案1: 道のない埋立地 33216 に北から道をつなぐ

### 施策

- 案の id: health-1
- 施策: 埋立地 33216(3499,650)の北側に、Basic Road を1本引き、x=3465 の既存の道(節点 5040)につなぐ。道具は build_line
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `build_line`(prefab="Basic Road", points=[[3499, 692], [3465, 720]])。試しの道具 `test_build_line` で ok、cost 240、overlaps 0 を確認済み
  2. `net_reach`(x=3499, z=650, radius=200) で、33216 が reachable になったか確かめる
  3. `buildings_near`(x=3499, z=650, radius=10) で、33216 の problems から RoadNotConnected が消えたか確かめる
- 設置条件の確認:
  - 33216: Landfill Site、外形の中心 (3499,650)、幅 80(x)・長さ 64(z)、angle 0。0% full、grid の電気・水・下水は true、needs は false(道だけが要る)。ports は空。`buildings_near` と `net_reach` で RoadNotConnected、到達不可を確認
  - 外形の範囲: x 3459〜3539、z 618〜682。道の始点 (3499,692) は北の縁から 10m 外
  - 道の終点 (3465,720) は既存の節点 5040 と一致(`net_near`。区間 3404 と 26045 の端)
  - 試しの道具: `test_build_line` で ok。overlaps なし
  - 入口の向き: 確認済み(再調査)。`test_place_building`(prefab="Landfill Site", x=3499, z=650, angle=0, assume_removed_buildings=[33216])の entrance は (3499, 682)、facing north、road null。北の道の始点 (3499, 692) は入口から 10m で、16m 以内
- 再調査の結果: 条件を満たした。入口は (3499, 682) の北向きで、北の道の始点まで 10m。`test_build_line`(Basic Road, [[3499,692],[3465,720]], assume_removed_buildings=[33216])も ok、cost 240、overlaps なし。南案は入口から遠いため使わない
- 接続工事: 道1本(建設費 240)。ほかの接続は不要
- 予備候補: 南案 `build_line`(prefab="Basic Road", points=[[3530, 604], [3530, 580]])。試しの道具で ok、cost 120、overlaps 0。終点は既存の東西の道(区間 11564、z=580)の上で、交差点を作る。入口が南にあったときに使う。北案が `net_reach` で届かず、入口が南と確かめられたときだけ使う
- 中止する条件: `build_line` が断ったら、`test_build_line` を取り直す。北と南の両方で 33216 が届かなければ、この埋立地は閉じる(事業1のやめる条件)

### 期待する効果

- 改善の見込み: 33216 は道がないため、収集車が入れず、0% のまま受け入れていない。道がつけば受け入れに入り、ごみの印(4-4)が下がる見込み。確認した事実は、RoadNotConnected 3件のうち 33216 が1件であること
- 数値と期限: RoadNotConnected 3 → 2(22月末)。33216 の storage amount が 0 から増える。ごみの印は 9 から下がる見込み(量は見積もれない)
- 確認方法: `buildings_near`(x=3499, z=650, radius=10) の problems と storage、`buildings_near`(x=0, z=0, radius=6000, problem="RoadNotConnected") の件数、`complaints` の Garbage の件数(今 9)。同じ条件で比べる
- 不確かな点: 入口の向きは試しで確認済み。建てた後に道が入口へつながったかは、`net_reach` で確かめる。届かなければ南を使う。ごみの印の減る量は見積もれない
- 試し: なし

### 費用

- 建設費: 240(道1本。`test_build_line` の cost)
- 週の維持費の増え分: 約 2(Basic Road 40/km/週、`list_net_types`)

### 戻せるか

戻せる。道は取り壊せば元に戻るが、建設費は戻らない。取り壊しには議決が要る。

### 前の月の答え合わせ

前の月(20月)は案なし。20月の調査 s20-3(2267 の周りの汚染)の結果は次のとおり。
中心の最大は3回とも 255 で、(3600,40) 付近に残った。平均は 47→49→49 で下がらず、Pollution の印は 27→32→25。2267 が出どころと言い切れない。判定: 下がらず、見立ては半分(2267 の周りが出どころの一部とは言えるが、そこで止めても効きは見えない)。次の扱い: 22月の候補探しは、東側の調査 s21-1 の結果を見てから決める。

### 市の計画

- 当たる施策: 4-4 資源循環
- 編成方針の重点に当たるか: 当たらない

## 調査

- 調査: あり
- 問い: 汚染の印の出どころは2267だけか。東の 255 の一帯(x 3850〜4250、z -550〜-250)は、2267 と別に続くか。
- 見る道具と引数:
  - `map_layer`(type="pollution", x=4050, z=-300, radius=350, n=9)
  - `buildings_near`(x=4150, z=-250, radius=300, problem="Pollution", brief=true)
  - `complaints`(Pollution の件数と hotspot)
- いつ見るか: 見回り1, 見回り2, 月末
- 何が分かれば次の手が決まるか: 東の 255 の点が3回続き、Pollution の hotspot が東へ動くなら、22月は2267 の移転より東の出どころを先に当てる。東の 255 が消え、hotspot が 2267 の近くに残るなら、22月に 2267 の移す先の候補を試す。
- 担当の問題: 4-3 脱炭素社会

## 見たもの

- `city_info`: 人口174,078、所持金2,616,061、週の収支 +8,868(収入337,184、支出328,316)、幸福度88、観光客1,837、dialog なし
- `citizens_summary`: 健康の平均87、体調の悪い市民 1,204、電気・水・下水が来ない 0/0/0
- `complaints`: Garbage 9(hotspot (3946,-189) 5棟)、Pollution 25(hotspot (3747,-94) 12棟)、RoadNotConnected 3(23459 が hotspot)、Fire 1、Crime 2
- `services`: ごみの容量 184,000,000、使用 81,033,767、満杯 1(3565)。墓地は満杯 0
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,088)。SmallBusiness は無効(317)。Recycling は無効で週の費用 0 だが、説明は「住宅税 -5%、ごみ -15%」。政策の費用の計 10,852/週
- `buildings_near`(problem="RoadNotConnected", r=6000): 23459、33216、公園 23298(urban の担当)
- `buildings_near`(service="Garbage", r=6000, brief): 3565 は LandfillFull、12880 と 45892 は Emptying、23459 と 33216 は RoadNotConnected、焼却場 2267 は稼働中
- `buildings_near`(x=3499, z=650, r=10): 33216 は 0% full、RoadNotConnected、grid の電気・水・下水 true、ports 空
- `buildings_near`(x=3499, z=650, r=150, brief): 26 棟。道に面した建物は北に小学校 41220(3488,750)、南に火葬場 12290(3500,568)
- `buildings_near`(x=2712, z=-1602, r=10): 23459 は 0% full、RoadNotConnected、ports 空
- `net_near`(x=3499, z=650, r=200): 33216 の周りの道は、x=3440 の南北道(z 620〜720)、z=580 の東西道(区間 11564)、北の x=3465 の道(z 720〜770)
- `net_near`(x=3490, z=705, r=70, service="Road"): 北側の節点 5040 (3465,720)、25039 (3440,695)、26184 (3440,720)
- `net_reach`(x=3499, z=650, r=200): 33216 は reachable false、canLeave false(道がない)
- `list_net_types`(service="Road", locked=false): Basic Road 5,000/km、維持 40/km/週
- `test_build_line`(Basic Road, [[3459,650],[3440,650]]): 33216 と重なり断り
- `test_build_line`(Basic Road, [[3499,618],[3499,580]]): 33216 と火葬場 12290 と重なり断り
- `test_build_line`(Basic Road, [[3530,612],[3530,580]]): 33216 と重なり断り
- `test_build_line`(Basic Road, [[3499,692],[3445,692],[3440,695]]): ObjectCollision(区間 7123、26045、31990)で断り
- `test_build_line`(Basic Road, [[3499,692],[3499,720],[3465,720]]): 小学校 41220 と重なり断り
- `test_build_line`(Basic Road, [[3499,692],[3465,720]]): ok、cost 240、overlaps なし(案1)
- `test_build_line`(Basic Road, [[3530,604],[3530,580]]): ok、cost 120、overlaps なし(予備)
- `zone_map`(x=3499, z=650, r=120, size=500): 33216 の外形と、南の東西道、西の南北道を確認
- `map_layer`(type="pollution", x=4150, z=-250, r=300, n=7): 平均 46、最大 255(3850,-250)。255 の点は東の一帯に複数(南の行 x 4150〜4250、z -550 付近)
- `buildings_near`(x=4150, z=-250, r=300, problem="Pollution", brief=true): 1 棟(42536、(4184,-503)、Pollution と MajorProblem)
- (再調査)`test_place_building`(prefab="Landfill Site", x=3499, z=650, angle=0, assume_removed_buildings=[33216]): ok、angleUsed 0、cost 4,000、entrance (3499,682) facing north、road null、wouldDemolish 0、lostByDemolish 0
- (再調査)`test_build_line`(prefab="Basic Road", points=[[3499,692],[3465,720]], assume_removed_buildings=[33216]): ok、cost 240、overlaps なし

## 判断の根拠

- 第21月の予定は、33216 の入口の道を試しで探すこと。北(240)が試しを通ったので、案1にする。南(120)は入口の向きが南だった場合の予備。入口の向きは道具で確かめられず、建てた後の `net_reach` で確かめる
- 再調査で、入口の向きを道具で確かめた。entrance は (3499,682) の北向きで、北の道の始点は 10m。16m 以内なので、北案で道が入口に届く条件を満たした
- 23459 の道は、予定どおり23月に回す。今月は出さない
- 満杯の 3565 の空けは出さない。12880 と 45892 がまだ Emptying のため、計画どおり終わるまで待つ
- 汚染(印 25): 20月の調査で、2267 の周りの最大 255 は3回とも横ばい。2267 が出どころと決められないため、22月の候補探しは東側の調査を見てから決める。調査を1件出す
- 政策 Recycling(ごみ -15%、住宅税 -5%)は採らない。住宅税 -5% は、今の住宅税の収入(約 261,000/週、m19 の計算)で約 -13,000/週。週の収支 +8,868 では守る線 +3,000 を割るため
- 案は1件。担当の問題のうち、確かめられる手は道の1本だけで、ほかは前提が未確認のため出さない

## 捨てたもの

- 満杯の 3565 を空にする(`empty_building`): 12880 と 45892 がまだ Emptying。終わるまで待つ(計画どおり)
- 2267 の移す先の候補探し(22月の予定): 20月の調査で、2267 が出どころと決められない。東側の調査の結果を見てから決める
- 政策 Recycling: 上記の守る線の理由。週の収支に大きく響く
- 南の道(120): 予備にした。入口が北と確かめられた後は使わない
- 23459 の道: 23月の予定。今月は道具の試しをしない
