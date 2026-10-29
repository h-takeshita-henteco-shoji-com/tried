# m16 港湾空港局の案

## 案なし

今月は案を出しません。

- 旅客の入口(島B の駅): 計画の第16月は「整地の試しと判定」で、駅の案は第17月です。駅は Boost の判定(16月末)の後に議案にするため(調整3)。今月の試しで、駅本体は傾きで断られず、入口の道は仮定の整地で通ることを確かめました。残りは、実際の整地の試し(level_terrain)の費用で、これは実行する市長が第17月の前に行います。
- 8-1(貨物センター28755の止まり): 空き待ちは 632 → 684 → 659 → 685 と減らず、周辺の道は blocked 0 です。入口の道は x=3495 と x=3400 の2本ですでにつながっており、道を足す根拠がありません。道を足す案は根拠が弱いため、出しません。代わりに、近くの貨物駅 13893 が車を出していない理由を調査します。

調べた候補と根拠は「判断の根拠」と「捨てたもの」に書きます。

## 調査

- 調査: あり
- 問い: 貨物センター13893(28755の隣。車0、職員50、電気・水・下水は届く)は、列車の着きがなく車を出せないのか。出せるなら、28755 の貨物を分けられるか
- 見る道具と引数: `vehicles_stuck`(kind=train、building=13893、limit=5)、`cargo`(stations の 13893 の vehiclesLeaving と vehiclesArriving)、`buildings_near`(x=3529、z=-1555、radius=30)
- いつ見るか: 見回り1・月末
- 何が分かれば次の手が決まるか: 列車が着いていて車を出していなければ、積み下ろしの設定が原因。17月の8-1 の手段の候補にする。列車が着いていなければ、28755 に分けるのは無理で、8-1 は目標を下げて終える(18月までの期限)
- 担当の問題: 8-1 物流・人流のゲートウェイ

## 見たもの

- `city_info`: 人口176,528、所持金2,473,305、週の収支+12,150(収入337,563、支出325,413)、幸福度88、観光客1,937(訪問160)、需要 住24/商2/工53、来ない市民0/0/0、dialog なし
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(3,824)。RecreationalUse は無効(0)、SmallBusiness は無効(313)、TaxLower・TaxRaise は全部無効(0)。政策の policyExpensesPerWeek は 10,591。観光に効く政策は、RecreationalUse と SmallBusiness の単独の試しで効きが切り分けられなかった(m03〜m05)。今月は変えない
- `list_building_types`(service=PublicTransport): Train Station 45,000(維持費960、16×6、道が要る)、Harbor 80,000、Cargo Center 60,000(維持費1,440)、Bus Depot 30,000 は解禁済み
- `buildings_near`(x=-4700、z=1600、radius=300): 風車 44460(-4660,1440)のみ。駅の敷地に建物なし
- `height_at`: (-4700,1600) 84.9m、(-4700,1620) 91.2m、(-4700,1576) 75.5m、(-4700,1552) 67.3m、(-4640,1552) 58.4m
- `net_near`(x=-4700、z=1600、radius=250): 道 Basic Road 6区間(端 (-4640,1552)=node 23669 は segment 13902 の西端)、橋 segment 11260、電線 segment 22680(-4655,1466)-(-4650,1500)
- `zone_map`(x=-4650、z=1600、radius=250): 駅の敷地の周りは空き。道は z 1552 の横と x -4600 の縦
- `test_place_building`(Train Station、x=-4700、z=1600、facing=south): ok=true、placed=false、cost 45,000、angleUsed 180、entrance (-4700,1576) south、road null(道はまだない)、wouldDemolish 0。傾き・整地の理由は出ない
- `test_build_line`(Basic Road、[[-4640,1552],[-4700,1552],[-4700,1576]]、整地なし): 断られず、cost 440、gameCheck segment 2 が SlopeTooSteep
- `test_build_line`(Basic Road、[[-4640,1552],[-4660,1552],[-4680,1560],[-4700,1576]]、整地なし): cost 360、gameCheck segment 3 が SlopeTooSteep
- `test_build_line`(Basic Road、[[-4640,1552],[-4700,1552],[-4700,1576]]、assume_terrain=level 71.5、polygon [[-4715,1545],[-4685,1545],[-4685,1585],[-4715,1585]]): ok、cost 440、enoughMoney true、overlaps なし、gameCheck なし。仮定の整地で傾きが消えた
- `test_place_building`(Train Station、x=-4700、z=1600、facing=south、assume_terrain=level 85、polygon [[-4730,1580],[-4670,1580],[-4670,1625],[-4730,1625]]): ok。整地を仮定しても、整地なしと同じ結果(入口は (-4700,1576))
- `cargo`: 止まったトラック1,049(道の上378、建物の中671)。28755 が659(vehiclesLeaving 974、arriving 9)。品物がない店266、原料がない工場39。上位の止まり: 28755 の敷地(3438,-1548)106台
- `vehicles_stuck`(truck、building=28755、limit=5): 824台。WaitingSpace+InGrounds 659、WaitingSpace+OnRoad 98、Blocked 52(道)。seenStopped 7日以上 701。サンプルの目的地は2.5〜4.6km の店
- `traffic`(x=3430、z=-1560、radius=120): flow 53、blocked 0、cars 15、blockedSpots なし。道の混みは見えない
- `net_near`(x=3600、z=-1560、radius=120、Road): 28755 の東側は道がなく、x=3495 の Small 4 Lane のみ
- `net_near`(x=3449、z=-1555、radius=120): 28755 の敷地の内側に Cargo Connection が8本(z -1555/-1560)。入口は x=3495 の Small 4 Lane と x=3400 の Large Road につながる
- `transport_reach`: 28755 は outsideConnected true。3940 と 4740 も true だが車は0。13893 は true で車0。14580、16572、48243 は gap あり
- `buildings_near`(x=3449、z=-1555、radius=60): 28755 は Cargo Center、workers 59、vehicles inUse 974、problems None
- `buildings_near`(x=3529、z=-1555、radius=30): 13893 は Cargo Center、workers 50、vehicles inUse 0、problems None、grid 電気・水・下水 true
- `vehicles_stuck`(truck、building=13893): vehicles 0。車は出ていない

## 判断の根拠

- 駅(島B): 第16月の試しで、駅本体は断られず、入口の道は傾きが原因で断られると分かった。仮定の整地(71.5m)で道が通ると確かめた。実際の整地の費用と土は未確認。駅の案は、Boost の判定(16月末)の後の第17月に出す(調整3)。
- 8-1: 空き待ちは減らない。道の混みではなく、敷地の内側の受け入れが詰まっていると見る。入口はすでに2本あり、東側に道もないため、入口の道を足す根拠がない。13893 が車を出していない理由を見るのが、いまの最も近い手段になる。
- 案の数: 今月は0件。駅は第17月の計画、8-1 は調査の結果を待つ。

## 捨てたもの

- 28755 に入口の道を足す案: 道の混みが見えず(blocked 0)、入口はすでに2本あるため効く根拠がない。道を試すのは、13893 の調査の結果が出てから
- 28755 の振り分けを 3940 や 4740 へ移す案: 両方とも車が0で、振り分けの道がない(第15月の確認)
- 新しい貨物駅の建設(Cargo Center 60,000、維持費1,440): 置く場所と鉄道の接続が未確認。列車がつながらなければ車は出ず、週の維持費だけ増える
- 政策 RecreationalUse・SmallBusiness の有効化: m03〜m05 の試しで、観光の数字と切り分けられなかった。今月は動かさない
