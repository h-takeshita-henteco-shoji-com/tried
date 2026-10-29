# m22 港湾空港局の案

## 案1: 車が来ない貨物センター 40031 を止める

### 施策

- 案の id: port-1
- 施策: 貨物センター 40031(Cargo Center、(-1780,-1605))を止める。維持費と働き手が0になり、8-1 の数字は変わらない見込み
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `set_building_active(id=40031, active=false)` を1回。止めたあと `city_info` の週の収支を見る
- 設置条件の確認: 既存の建物の停止なので設置条件はない。`buildings_near`(x=-1780, z=-1605, radius=120, brief=true)で id 40031 Cargo Center、problems None を確認。`cargo` で 40031 の vehiclesLeaving 0、vehiclesArriving 0 を確認
- 接続工事: 不要
- 予備候補: なし。止めたあとに戻すなら `set_building_active(id=40031, active=true)`
- 中止する条件: 実行の前に 40031 に車が来ている(cargo の vehiclesLeaving か vehiclesArriving が1以上)なら、止めずに市長に返す

### 期待する効果

- 改善の見込み: 40031 は再開(m21-4)のあとも車が0のままで、週の維持費 1,440 だけが出ている。止めれば週の支出が減る。8-1 の 28755 の止まりは減らない見込み(m21-4 の結果)なので、8-1 の数字の改善は見込まない
- 数値と期限: 週の維持費 1,440 の減少。city_info の週の収支は 5,957 から約 7,400 の見込み(第22月末)
- 確認方法: `city_info` の weeklyIncome と weeklyExpenses、`cargo` の 40031 の車の数(0のまま)と 28755 の stoppedInBuildings(632 が基準)
- 不確かな点: 維持費の減りは、建物を止めたときの決まり(維持費と働き手が0になる)から予想。8-1 の改善は見込まない。数値は見積もれない部分はない
- 試し: なし

### 費用

- 建設費: 0
- 週の維持費の増え分: -1,440(`list_building_types` の Cargo Center の upkeepPerWeek)

### 戻せるか

戻せる。`set_building_active(id=40031, active=true)` で動かせる。

### 前の月の答え合わせ

- 前の月の案 port-1(m21-4、40031 の再開、試し)は、外れ。`cargo` の stoppedInBuildings は 605 から 632 に増え、noGoods は 205 から 227 に増えた。40031 の車は今も0
- 前の月の条件(第22月末に車が来ず、28755 の空き待ちが増えたら止める)は、第22月初めの測りで満たした。前倒しで止める

### 市の計画

- 当たる施策: 8-1 物流・人流のゲートウェイ(効きは週の収支の面。8-1 の数字は変えない)
- 編成方針の重点に当たるか: 当たる

## 案2: 路線28の予算を 200% に戻す

### 施策

- 案の id: port-2
- 施策: 路線28(line 136、画面の番号 28)の台数の割合を 180% から 200% に上げる。台数は約170から約189へ
- 議決: 予算

### 実行計画

- 実行可否: 未確認
- 対象と操作順: `set_transport_line_budget(line=136, percent=200)` を1回。戻したあと `list_transport_lines(number=28)` で台数と乗客を見る
- 設置条件の確認: 建設なし。`list_transport_lines(number=28)` で line 136、budget 180、vehicles 170、targetVehicles 170、passengersLastPeriod 53(前は110)、pathFailed 0 を確認
- 接続工事: 不要
- 予備候補: 乗客が戻らないなら `set_transport_line_budget(line=136, percent=180)` に戻す(今の値)
- 再調査の結果: 費用は直した(維持費は約+220/週。約+2,400 は誤り)。乗客の条件は未達。`list_transport_lines`(number=28)の今の値は 53 で、前の期間は 110。2期間続けて92未満ではない。ゲームは止まっていて時間を進められないため、この月に2期目は測れない。第23月の乗客が92未満なら、23月に出し直す。
- 中止する条件: 議決で否決されたら、180% のまま

### 期待する効果

- 改善の見込み: 路線28の乗客は、第21月の110から今月53へ減り、基準の92を下回った。台数を戻して待ちを減らし、乗客を基準へ戻すと予想する。6-3 の交通の流れは、台数の増えで数点下がる見込み
- 数値と期限: 路線28の passengersLastPeriod を92以上へ(第23月末)。交通の流れは55%を保つか、下がっても数点まで(第23月末)
- 確認方法: `list_transport_lines(number=28)` の passengersLastPeriod と vehicles、`traffic`(流れと blocked)。今の値(乗客53、台数170、流れ55%)と同じ範囲で比べる
- 不確かな点: 乗客は期間ごとに大きく揺れる(92→29→110→53)。1期間の値で判断できない。バスの維持費は、`economy_breakdown` の PublicTransportBus の支出 21,618/週 を、`list_transport_lines(type="bus")` の全80路線の台数の合計 1,869 で割った平均(約11.6/台/週)で見積もる。増えは 19台 × 約11.6 で約+220/週と見込む(路線の車両の種類が同じと仮定する)
- 試し: なし(第21月の予算の下げの戻し)

### 費用

- 建設費: 0
- 週の維持費の増え分: 約+220/週(再調査で直した見積もり。バス19台 × 約11.6/台/週)

### 戻せるか

戻せる。`set_transport_line_budget(line=136, percent=180)` で元に戻せる。

### 前の月の答え合わせ

- 前の月の案 port-1(m20-4、路線28 の予算 200%→180%)は、台数 171 は予想どおり。乗客は 110(基準92)で当たり。流れは 53 から 55 へ上がった。
- ただし今月は乗客が 53 に減った。前の月の計画の「やめる条件」(乗客が減る)に当たるため、今月は予算を戻す。判定は半分(台数は当たり、乗客は揺れが大きい)

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: あり
- 問い: 28755 で空き待ちのトラック(約630台)は、どれくらい遠い店へ向かっているか。近い店への輸送を増やす手が要るかどうか
- 見る道具と引数: `vehicles_stuck(kind="truck", building=28755, limit=8)`(行き先の距離、止まった日数、byTarget)、`cargo()`(stoppedInBuildings、noGoods の場所)
- いつ見るか: 見回り1、月末
- 何が分かれば次の手が決まるか: 行き先の距離(distance)の大半が3,000m を超えるなら、近い店の周りに貨物の受け口を置く案を、場所と接続を確かめて出す。大半が3,000m 未満なら、28755 の積み込みの混みが原因なので、8-1 の目標の扱いを市長と決める
- 担当の問題: 8-1 物流・人流のゲートウェイ

## 見たもの

- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,068)。FreeTransport は無効(運賃収入は0になる)。SmallBusiness、RecreationalUse、Recycling は無効。港湾の担当に効く政策は FreeTransport のみ。政策の費用の計は 10,794/週
- `list_transport_lines`(number=28): 路線 136、台数 170(目標 170)、予算 180%、乗客(passengers)80、前の期間 53、運賃収入 53、停留所 40、pathFailed 0、pathWaiting 4
- `cargo`: stoppedInBuildings 632(28755 が 631)、stoppedOnRoads 345、noGoods 227、noResources 29。40031 は vehiclesLeaving 0、vehiclesArriving 0。28755 の vehiclesLeaving 930
- `buildings_near`(x=-1780, z=-1605, r=120): 40031 Cargo Center、problems None
- `buildings_near`(service=PublicTransport、全域): 旅客の駅・港・空港は0。Cargo Center 6、Cargo Harbor 3、Metro Entrance 2、Bus Depot 2、Overground の駅なし
- `list_building_types`(PublicTransport): 解禁済みは Train Station(45,000、週 960、16×6)、Airport(150,000、週 4,800)、Harbor(80,000、週 1,600)、Harbor02、Metro 系、Cargo Center(60,000、週 1,440)、Cargo Harbor、Bus Depot(30,000、週 720)
- `net_near`(x=4000, z=2000, r=900、Road): 東の高速道路(Highway Elevated)が多く、地上の一般道は (3454,1270〜1405) と (3378〜3454,1360) のみ
- `net_near`(x=3330, z=1900, r=350、Road): 地上の道0。高速道路の高架のみ
- `net_near`(x=4276, z=2350, r=350、Road): 0
- `net_near`(x=3000, z=1900, r=300、Road): 0
- `zone_map`(x=3600, z=1400, r=1400, size=500): 東の端は高速道路の高架。東の列(x 3200〜3400, z 1400〜2100)に、オフィスの区画が並ぶ
- `test_place_building`(Train Station, 4300, 2350, facing west): ok、placed=false。entrance.road null(道路なし)、費用 45,000
- `test_place_building`(Train Station, 3300, 1900, facing east): ok、placed=false。entrance.road null、費用 45,000
- `test_place_building`(Train Station, -4700, 1600, facing east): ok、placed=false。entrance.road null(島B)
- `height_at`(4300, 2350): 地面 61.8m
- `height_at`(3300, 1900): 地面 51.7m
- `test_build_line`(Basic Road、[[3324,1900],[3390,1650],[3454,1405]]): ok=false。オフィス3棟(40744、24951、7684)と重なる
- `test_build_line`(Basic Road、[[3324,1900],[3300,1600],[3300,1450],[3378,1360]]): ok=false。オフィス8棟と重なる
- `net_reach`(x=3454, z=1360, r=200): 道路27区間、つなぎ口から入れない0、建物の来られない0
- `economy_breakdown`: 週の収入 335,699、支出 329,742。PublicTransport の支出 39,179(バス 21,618、鉄道 12,413、船 4,608)、収入 5,086(バス 5,084)。Cargo Center の維持費は別
- `city_info`: 人口 173,537、所持金 2,643,814、週の収支 +5,957(収入 335,699、支出 329,742)、幸福度 87、観光客 2,020(訪問 171)、需要 住34/商2/工43、来ない市民 0/0/0
- `vehicles_stuck`(kind=truck、building=28755、limit=8): 777台。WaitingSpace+Importing が 630 台(InGrounds)と 85 台(OnRoad)。bySeenStopped は 7日以上が 631。行き先は 3〜6km の店が多い(例: 5,837m、4,579m、6,014m、3,909m)。近い行き先は 436m、1,468m の2件

## 判断の根拠

- 6-3 の路線28 は、台数 171 で流れは 53 から 55 に上がり、ここまでは効いた。だが乗客は 110 から 53 に減った。第21月の計画が決めた「乗客が減るなら戻す」に当たるため、予算を 200% に戻す(案2)。
- 8-1 の 40031 は、再開から車が来ないまま。計画の条件を満たしたので止める(案1)。週の維持費 1,440 が減り、週の収支は守る線 +3,000 の上に残る。案1と案2をあわせても、週の収支は約 +5,000 の見込み(案2の増えは粗い見積もり)。
- 旅客の入口(5-1、5-2)は、今月も置けない。東の列と空き地5は、置く場所は確かめられたが、道路網まで道を通せない(地上の道が350m以内になく、東の列はオフィスに塞がれる)。島Bは坂。整地の見積もりを局の道具で確かめられないため、案にせず、実行する市長に求める(計画の事業1)。
- 案は2件。8-1 と 6-3 の2つにした。入口は、確かめた道が実行条件を満たさないため、案に含めない。

## 捨てたもの

- 旅客の駅を東の列(3300,1900)に置く: 置く位置は確かめた(test_place_building は ok)が、道路網までの経路がオフィスに塞がれ、test_build_line が2本とも断った。道路を取り壊す案は、失う働き口の数を確かめていない。実行条件が未確認のため出さない
- 旅客の駅を空き地5(4300,2350)に置く: 置く位置は確かめた。350m以内に地上の道がなく、道の経路を引く候補を確かめていない。実行条件が未確認のため出さない
- 旅客の駅を島B(-4700,1600)に置く: 整地が要り、level_terrain の見積もりは局の道具にない。未確認のため出さない
- 政策 FreeTransport を有効にする(乗客を増やす): 運賃収入が0になり、収入の損は週約5,000(前の月の測り 5,086)。m16-4 と m17-4 の測りで、乗客の増えは確かめられなかった。出さない
- 貨物の受け口を足す(40031 の代わりに、近い店の周りに別の貨物駅): 行き先の距離は 3〜6km と見えるが、置く場所と道を確かめていない。s22-1 の結果を見てから考える
- 路線28 の予算を 160% に下げる: 乗客が減っているときに下げると、乗客の減りが続く。出さない
