# m23 港湾空港局の案

## 案1: 路線28の予算を 200% に戻す(試し)

### 施策

- 案の id: port-1
- 施策: 路線28(line 136、画面の番号 28)の予算を 180% から 200% に上げる。台数は 170 から約 189 へ増える
- 議決: 予算

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `set_transport_line_budget(line=136, percent=200)`(予算は +20 で、±20 の上限内)。2. 第25月末まで、`list_transport_lines(type="bus", number=28)` で台数と乗客を毎月見る
- 設置条件の確認: `list_transport_lines`(type=bus)で、line 136、budget 180、vehicles 170、targetVehicles 170、pathFailed 0 を確認。道具の引数は tool-reference の `set_transport_line_budget(line, percent)` で確かめた
- 接続工事: 不要
- 予備候補: なし(予算の変更だけなので、置き場所の候補はない)
- 中止する条件: 議決が否決なら、動かさない。可決のあと、2期(第25月末まで)の乗客が92未満のままなら、`set_transport_line_budget(line=136, percent=180)` で 180% に戻す案を出す

### 期待する効果

- 改善の見込み: 路線28の乗客を92以上に戻せば、6-3 の交通の流れを支える路線として効きを見られる。ただし台数の増えは道の車を増やすので、流れを下げるおそれもある。確認した事実は、乗客が 110 → 53 → 85 → 73(前期 73、今期 85)と期ごとに振れていること
- 数値と期限: 路線28の乗客(`list_transport_lines` の passengersLastPeriod、line 136)。今の値は前期 73、今期 85。目標は2期続けて92以上。期限は第25月末(2期後)。交通の流れ(`traffic` の flow)は今の 52 を下回らないこと
- 確認方法: `list_transport_lines(type="bus", number=28)` の台数・乗客・passengersLastPeriod と、`traffic` の flow(街全体)。同じ道具・同じ範囲で、第23月の値と比べる
- 不確かな点: 数値は見積もれない。台数が乗客を増やすという仮説は、180% と 200% の差を期の振れから切り分けていない。費用は、バス1台の週の平均(約14、概算)に19台を掛けた見積もり
- 試し: 仮説: 路線28の台数(予算)を増やすと、乗客が増え、6-3 の流れの見方が立つ。測る数: `list_transport_lines`(number=28)の passengersLastPeriod と台数、`traffic` の flow。場所: 路線28全体と街全体。基準: 前期 73、今期 85、流れ 52。編成方針の重点3(6-3)の効きが分からない項目に当たる

### 費用

- 建設費: 0
- 週の維持費の増え分: 約 +220〜270(19台 × 約14/週。概算)。`economy_breakdown` の PublicTransportBus の支出 21,615 から出した平均

### 戻せるか

戻せる。予算は 180% に戻すだけで、台数も週の費用も元に戻る。

### 前の月の答え合わせ

- 22月の案 port-1(m22-4、貨物センター 40031 を止める)は採られ、実行 ok。期待は週の維持費 -1,440 と、28755 の止まりを減らすこと。判定: 半分。`economy_breakdown` で 40031 は停止状態(TurnedOff)、維持費は止まった。一方、`cargo` の28755 の止まりは 632 から 635 に増えた(庫内 629)。止まりへの効きは見えない
- 22月の案 port-2(m22-port-2、路線28 を 200% に戻す)は採られなかった。理由は「乗客が 92→29→110→53 と揺れ、1期間の値では根拠にならない」。手当て: 第23月の2期目(前期 73、今期 85)も92未満で、2期続けて下回った。今月は、その条件で再提出する

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(道路下水道局と分け持つ)
- 編成方針の重点に当たるか: 当たる(重点3)

## 調査

- 調査: あり
- 問い: 28755 の隣の貨物センター 13893(車 0、職員 43)が車を受けないのはなぜか。28755 の空き待ち(庫内 629)は、見回りごとに減るか
- 見る道具と引数: `cargo`(引数なし。stations の 13893 と 28755 の vehiclesLeaving / vehiclesArriving を見る)、`vehicles_stuck`(kind="truck", building=28755, limit=3。byState の WaitingSpace+InGrounds の数を見る)、`buildings_near`(x=3529, z=-1555, radius=60, limit=5。13893 の vehicles.inUse と jobs を見る)
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 13893 の車が 0 のままで、28755 の庫内待ち(629)が減らなければ、8-1 の手は隣の貨物センターを使う道の手に絞る(第24月に案)。13893 に車が来始めたら、28755 の待ちが減るかを見て、手を止める。待ちが減らず、ほかの貨物センターにも車が来なければ、8-1 の目標を市長に伝える
- 担当の問題: 8-1 物流・人流のゲートウェイ

## 見たもの

- `city_info`: 人口 172,759、所持金 2,672,278、観光客 2,020(訪問 179)、週の収入 336,105、支出 328,359、需要 住36/商2/工43、来ない市民 0/0/0
- `list_transport_lines`(type=bus): 路線28(line 136、number 28)台数 170、予算 180、乗客 85(前期 73)、pathFailed 0。乗客0〜1の路線: Bus Line 74(line 15、台数 15)、Bus Line 9(line 46、台数 18)、Bus Line 81(line 203、台数 15、pathFailed 1)
- `cargo`: stoppedTrucks 973、道の上 338、建物の中 635(28755 が 629)。noGoods 215、noResources 29。28755 の vehiclesLeaving 915、vehiclesArriving 9。40031 は 0 / 0。隣の 13893 は 0 / 0
- `list_policies`: 有効 EducationBoost(週 7,940)、BigBusiness(週 4,052)、SmokingBan(0)。無効 FreeTransport(0。運賃収入 5,053 を失う)、HeavyTrafficBan(0。貨物トラックも締め出すおそれ)、Recycling(0)、SmallBusiness(319)、IndustrySpace(4,858)、HighTechHousing(20,264)
- `trade`: 輸入 15,448(goods 7,521)、輸出 1(goods 1)。道の接続は 218 + 47 + 153 + 17 台が輸入中
- `economy_breakdown`: PublicTransport 収入 5,053、支出 37,735(バス 21,615、鉄道 10,973、船 4,608、地下鉄 539)。Tourism 週 130
- `buildings_near`(service=PublicTransport、半径 9,000): 旅客の駅・港・空港は 0。Cargo Center 8、Cargo Harbor 3、Metro Entrance 2、Bus Depot 2
- `list_building_types`(service=PublicTransport): 解禁済みは Train Station(45,000 / 週 960)、Harbor(80,000 / 1,600)、Airport(150,000 / 4,800)、Harbor02、Metro 系、Bus Depot、Cargo Center、Cargo Harbor
- `net_near`(x -3000, z 1200, r 1200)、`net_near`(x -4600, z 1500, r 500, Road): 島Bには、橋(Basic Road Bridge、80m 区間)から入る道路の区間がある。風車 44460 が (-4660, 1440) に建つ
- `buildings_near`(x -4600, z 1500, r 600): 風車 44460 のみ
- `zone_map`(x -4000, z 1300, r 1000, size 500): 島Bの道路・橋を確認。区画なし
- `test_place_building`(Train Station): (-4700,1520) 不可(風車と重なる)。(-4650,1600) 不可(道と重なる)。(-4560,1400) 不可(道と重なる、水)。(-4300,1700) 不可(水)。(-4780,1560, east) 置ける(entrance (-4756,1560)、道なし)。(-4740,1680, east) 置ける(entrance (-4716,1680)、道なし)
- `test_place_building`(Harbor, -4800,1700, north): 不可(高さが高すぎ、道に繋げない)
- `height_at`: (-4700,1520) 62.1、(-4640,1552) 58.4、(-4716,1680) 113.8
- `test_build_line`(Basic Road): (-4756,1560)→(-4640,1552) 2区間 cost 560、gameCheck SlopeTooSteep(区間1)。(-4716,1680)→(-4500,1700) 3区間 cost 1,080、gameCheck SlopeTooSteep(3区間すべて)
- `buildings_near`(abandoned=true、半径 5,000): 放棄された店・ホテル・工場が 112 棟。中心部の空きは確認
- `map_layer`(attractiveness、n 9、半径 4,000): 平均 3、最大 85(0,0)。街の中心に集中
- `test_place_building`(Train Station、assume_removed_buildings あり): (544,173) 不可(道2本、店3棟と重なる)。(564,-146) 不可(道6本、事務所と店と重なる)。(96,243) 不可(道8本と重なる)
- `traffic`(x 3449, z -1555, r 300): flow 52、cars 53、blocked 1。混み(density 85)は道 (3480,-1315) など
- `vehicles_stuck`(kind=truck, building=28755, limit 6): vehicles 763。byState: WaitingSpace+Importing+InGrounds 629、WaitingSpace+OnRoad 91、Blocked 27、GoingBack 16。行き先までの距離は 436〜6,014m。止まって見える期間が7日以上の車は 538
- `net_near`(x 3449, z -1555, r 250): 28755 の近くに道路、線路、送電線、水道管あり
- `buildings_near`(x 3529, z -1555, r 60): 13893(Cargo Center)、jobs.workers 43、vehicles.inUse 0、problems None
- `buildings_near`(x 2380, z -1282, r 60): 3940(Cargo Center)、jobs.workers 53、vehicles.inUse 0
- `net_reach`(x 3500, z -1555, r 200): 道路 12 区間、来られない 0、出られない 0。建物 4 棟、来られない 0
- `transport_reach`: 13893、3940、4740 は外とつながる(train)。14580、16572、48243 は外とつながらない(gap 271m、725m、2,933m)
- `net_near`(x 4000, z 2200, r 900, Road): 12 件を見た。すべて高架の高速道路(Highway Elevated)。一般道は見えない
- `test_place_building`(Train Station, 4300, 2350, west): 置ける(entrance (4276,2350)、道なし)
- 整地(`level_terrain`)の道具は、この局の道具一覧にないため、島Bの整地の見積もりは確かめられない

## 判断の根拠

- 6-3 の路線28: 2期続けて乗客が92未満(前期 73、今期 85)で、22月の条件を満たした。乗客が台数に効くかは期の振れで切り分けられていないが、計画の条件どおりに案1を出す。費用は約 +220〜270 で、週の収支 +7,746 と守る線 +3,000 の内に収まる
- 5-1、5-2 の入口: 島B は道の坂が急で断られ(SlopeTooSteep、3 区間)、空き地5 は駅を置けるが一般道がない。中心部は空きがなく、取り壊しの案は失うものを未確認。計画の条件(第23月末までに置ける候補と道の経路)を満たせないので、事業1 を閉じる。案は出さない
- 8-1 の 28755: 止まった車の行き先は 436〜6,014m で散らばり、距離も店への集中も原因ではない。止まりは庫内の空き待ち(629)。隣の 13893 は職員 43 で道にもつながるが車が来ない理由は分からない。原因が切り分けられないので、調査 1 件で見る。施策は出さない
- 案の数: 1件。入口は道の経路が見つからず、8-1 は調査で切り分け中。ほかの手(FreeTransport、HeavyTrafficBan、低乗客路線の削減)は、根拠が弱いか逆効果になるため出さない

## 捨てたもの

- 旅客の駅(島B、(-4780,1560) と (-4740,1680)): 置けるが、道の経路が SlopeTooSteep。道の高さを平らにする道具がない。入口を1つにする条件を満たせないため、今月は案にしない
- 旅客の駅(空き地5、(4300,2350)): 置けるが、一般道が 900m 以内に見えない。高架の高速道路へ出る接続は未確認。道の経路を見つけるまで、案にしない
- 旅客の駅(中心部の空き): 道路 2〜8 本と店・事務所の取り壊しが要る。失う働き口と家を `preview_bulldoze` で確かめていないため、案にしない
- FreeTransport(政策): 運賃収入 5,053/週 を失う。17月に効かず外した経緯があるため、再提出しない
- HeavyTrafficBan(政策): 貨物トラックを締め出すおそれがあり、8-1 に逆効果。案にしない
- 低乗客路線の台数の削減(Bus Line 74、9、81): 台数 -12 程度、週 -170 程度。流れ 52% に効く根拠が見つからず、6-3 への効きが見積もれない。今月は出さない
- 40031 の再開: 22月に止めた後も 28755 の止まりは動かず、再開の根拠がない。出さない
