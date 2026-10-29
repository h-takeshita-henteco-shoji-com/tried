# m24 港湾空港局の案

## 案なし

今月は案を出さない。根拠は次のとおり。

- 観光の入口(5-1、5-2): 空き地1 の候補 (1477,-2950) は、道と水の経路が試しで通った。電気の経路が通らず、川の上に線を引けない(CannotBuildOnWater)。電気が確認できないので、実行条件を満たさない。島Bと空き地5は、前の月に経路がなかった。港の候補(-740,1190、-820,1000、-400,1190)は、岸が高すぎる(HeightTooHigh)ため置けない。
- 8-1 の止まり: 調査 s23-1 で、13893 は車が0のまま、28755 の待ちは 613 で動かなかった。計画の止める条件を満たしたので、手を止める。目標 250 は局の手では届かないため、目標の扱いを市長に求める。
- 6-3 の流れ: 路線28 の乗客は 101 で、目標の 92 を超えている。台数は 188 で、予算は 200% のまま。今月は手を足さず、第25月末の2期を見る。

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口172,273、所持金2,697,883、週の収支 +6,823、幸福度87、観光客2,011(訪問179)、需要 住36/商2/工42、来ない市民 0/0/0
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,008)。無効は SmallBusiness(319)、IndustrySpace(4,834)、HighTechHousing(20,244)ほか。6-3 や観光の入口に効く政策はない。政策の費用は policyExpensesPerWeek 10,877
- `cargo`: stoppedInBuildings 631(28755 が613、1366 が18)、stoppedOnRoads 420、noGoods 201、noResources 32。28755 の vehiclesLeaving 898 / vehiclesArriving 11
- `list_transport_lines`: 路線28(line 136)passengersLastPeriod 101、台数188、予算200%、pathFailed 0
- `buildings_near`(PublicTransport、半径9,000m): 旅客の駅・港・空港は0。Cargo Center、Cargo Harbor、Metro Entrance、Bus Depot のみ
- `list_building_types`(PublicTransport、解禁の全部): Train Station(45,000、週960、道路要)、Harbor(80,000、週1,600)、Airport(150,000)が解禁済み
- `net_near`(Road、(1477,-2600) r1000): 道の端は (1000,-2120) 付近と (780,-2120〜-2220) 付近
- `net_near`(Electricity、(1000,-2200) r400): 電線は x 530〜935 の西側にあり、川の東側には見当たらない
- `net_near`(Electricity、(2000,-1500) r500): 電線なし
- `zone_map`(1477,-2900 r700、(1100,-2500) r800): 空き地1の周辺は空き。道・区画なし
- `zone_map`(-600,1050 r350): 貨物港 32211 の周りは道と管があり、岸の空きは少ない
- `test_place_building`: Train Station (1477,-2950) ok(cost 45,000、道路なし、entrance.road null)。(1000,-2350) は CannotBuildOnWater。Harbor (-740,1190)、(-820,1000) は HeightTooHigh。Harbor (-400,1190) は ObjectCollision と HeightTooHigh
- `test_build_line`: Basic Road [(1000,-2120),(1000,-2200),(1477,-2200),(1477,-2915)] ok(cost 8,040、橋2)。Basic Road [(780,-2150)...] は High School 6597 とゴミ発電に当たる。Basic Road [(740,-2220)...] は住宅に当たる。Water Pipe [(960,-2146),(1040,-2146),(1040,-2170),(1420,-2170),(1420,-2930)] ok(cost 3,260)。Power Line [(770,-2268),(1477,-2268),(1477,-2930)] は CannotBuildOnWater。Power Line [(880,-2070)...(1477,-2930)] は University 6597 に当たる。Power Line [(928,-2028),(1020,-2028),(1020,-2190),(1450,-2190),(1450,-2930)] は CannotBuildOnWater(2区間)。Power Line [(935,-1985)...] と [(928,-2028),(1000,-1960)...] は Police Station 19290 と道 33406 に当たる。Power Line [(1700,-1700),(1700,-2300),(1477,-2300),(1477,-2930)] は ok(cost 3,580)だが、北の起点が電線につながらない
- `list_net_types`(解禁済み): Basic Road 5,000/km(維持 40/km/週)、Power Line 2,500/km(維持 60)、Water Pipe 2,500/km(維持 10)。下水の線は解禁の一覧に出ない(service Sewage は空)
- `height_at`: (1477,-2950) は地面 55.7m、水面 55.7m(陸)
- `water_trace`: (960,-2146) の建物(Combustion Plant 25473)は水と下水が届いている。水の取水は西の給水塔群、下水の排水は貨物港の処理場。city 水 capacity 2,400,000 / used 1,868,864

## 判断の根拠

確認した事実は、道と水の経路は試しで通ること、電気の経路は川と既存の線に当たって未確認なこと、8-1 は調査で手を止める条件を満たしたこと。
電気の経路が未確認なので、入口の駅は実行条件を満たさない。案は出さず、次の月に電気の経路を試す。
8-1 の手は、止める条件を満たした。目標の扱いは市長が決める。
6-3 は乗客が目標を超えており、今月は手を足す根拠がない。案の数は0件。

## 捨てたもの

- 空き地1 の駅(道と水は通るが、電気の経路が未確認): 配置の条件が残る。電気の経路が通るまで案にしない
- 旅客の港(Harbor)を岸に置く案: 候補の岸が高すぎ(HeightTooHigh)、置ける場所が確認できない
- 8-1 の別の手(近い店への道): 調査で 13893 に車が来ないと確かめた。手を止める条件を満たした
- 路線28 の予算 180%(今月の乗客 101 で、下げる根拠なし)
