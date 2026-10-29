# m10 港湾空港局の案

## 案なし

今月は案を出さない。旅客の入口の候補は、確認できた条件が足りなかった。

- 旅客の駅 (700,1700)(Train Station、facing south、test_place_building は ok。入口は (700,1676) で、道路はまだない)
  - 水: 空き地3の近くに網がない。直線の水道管 (743,1123)→(700,1640) は test_build_line が通った(1,260)。ここは確認済み
  - 電気: 直線の送電線 (743,1120)→(690,1640) は、風力 19235(760,1185)と公園 473(752,1290)にぶつかり断られた。別の経路は未確認
  - 下水: net_near(半径1,500m、Sewage)で網がなかった。下水の出どころは未確認
  - 外への線路: 最も近い線路の端は 48243(1840,1592)で、外へつながっていない(gap 2,933m)。transport_reach で確認
  - 必須の条件のうち3つが未確認のため、実行対象にしない
- 港の旅客の岸: (-700,1000)、(-620,960)、(-800,1000)、(-860,1080) を test_place_building。HeightTooHigh か、Cargo Harbor の Ship Dock にぶつかる。島Bと埋立地D・空き地1と同じ結果
- 貨物駅28755の増設: 未確認。原因が出口の不足か道の混みか分からないため、先に調査する

案なしの理由: 旅客の入口は、電気・下水・外への線路が1つも確かめられていない。試しの道具で確かめられる範囲は確かめた。次の月に、電気の別経路と下水の出どころを確かめる。

## 調査

- 調査: あり
- 問い: 28755 の敷地の中で待つ540台は、積み出し口の数で頭打ちになっているか。道の混みか。
- 見る道具と引数: `vehicles_stuck`(kind="truck", building=28755, limit=10)、`traffic`(x=3440, z=-1550, radius=150)、`cargo`(引数なし)
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: 敷地の中の待ちが見回りのたびに増減せず溜まり、道の blocked が小さければ、積み出し口の不足と見て、11月に貨物駅を増やす試しを出す。道の blocked が増えていれば、道の差し替えを道路下水道局に求める案を11月に出す。待ちが減れば、経過を見て8-1の目標へ向けて続ける
- 担当の問題: 8-1 物流・人流のゲートウェイ

## 見たもの

- `list_policies`: 港湾空港局の担当に関係する政策は見当たらなかった。有効なのは SmokingBan、BigBusiness。RecreationalUse、SmallBusiness、EducationBoost は外れている。policyExpensesPerWeek 10,774
- `city_info`: 人口 180,117、所持金 2,270,429、週の収支 +8,997(収入 336,274、支出 327,277)、観光客 1,705(訪問 140)、来ない市民 0/0/0、dialog なし
- `list_building_types`(service=PublicTransport): Train Station 建設費 45,000、週 960。Harbor 80,000、週 1,600。Airport 150,000、週 4,800。Harbor02 120,000
- `water_trace`(700,1700): 近くに水の網がなし(networks 0)。街全体の水 容量 2,400,000、使用 1,926,064。下水 容量 2,400,000、使用 1,924,144
- `net_near`(700,1700 r250): 道路 Basic Road 968(712,1644 の端)、送電線 25434(690,1640)→17161(727,1626) の支線だけ。水・下水の網なし
- `net_near`(700,1650 r600, Water): 最も近い水道管は (743,1123)〜(679,1164) の区間
- `net_near`(700,1650 r600, Sewage) と `net_near`(700,1400 r1500, Sewage): 網なし
- `test_place_building`(Train Station、700,1700、facing south): ok。cost 45,000、entrance (700,1676)、road null(道路が要る)。wouldDemolish 0
- `zone_map`(700,1650 r200): 空き地3の道路沿いに区画はあるが、建物の敷地は確認していない
- `height_at`(700,1700): ground 45.3、water 45.3
- `list_net_types`(Water、locked=false): Water Pipe 1km あたり 2,500、維持費 10/週/km。Sewage は解禁された種類なし
- `test_build_line`(Basic Road、[[700,1676],[712,1644]]): ok。cost 160、overlaps なし。入口の道路の候補
- `test_build_line`(Water Pipe、[[743,1123],[700,1640]]): ok。segments 7、cost 1,260、overlaps なし
- `test_build_line`(Power Line、[[743,1120],[690,1640]]): 断られた(ObjectCollision)。ぶつかった相手は風力 19235(760,1185)と公園 473(752,1290)、道・送電線の区間 35227
- `net_near`(700,1400 r400, Electricity): 近くの送電線の本線は (743,1120)、(807,1080) の区間。空き地3に本線はない
- `transport_reach`: 外とつながった駅は 28755、32211、46112、1366、3940、4740、13893、40031。48243(1864,1680)は外とつながっていない(gap 2,933m)。旅客の駅・港・空港はなし
- `test_place_building`(Harbor、(-700,1000)、east): 断られた(ObjectCollision: Cargo Harbor 32211 の Ship Dock、HeightTooHigh)
- `test_place_building`(Harbor、(-800,1000)、east): 断られた(HeightTooHigh、CannotConnect)
- `test_place_building`(Harbor、(-620,960)、north): 断られた(HeightTooHigh、CannotConnect)
- `test_place_building`(Harbor、(-860,1080)、east): 断られた(HeightTooHigh、CannotConnect)
- `height_at`(-700,1000): ground 20.0、water 40.2
- `zone_map`(-640,1000 r300): 港の周りの岸に建物と道がある。建物は Water Outlet 11466(-605,1030)と Cargo Harbor 32211(-640,1074)
- `buildings_near`(-640,1074 r250, brief): Cargo Harbor 32211 の問題は Garbage、Crime、MajorProblem。Water Outlet 11466 の問題は None
- `net_near`(3449,-1555 r150): 貨物駅 28755 の周りの道は Large Road 5655、20316、17311(3 車線)と Small 4 Lane 15733、22686。線路 Train Cargo Track 9082、16924 が通る
- `cargo`: 止まったトラック 882(道の上 342、駅・港の敷地 540)。貨物駅 28755 の敷地で止まった 540 台は全部。出る車は 837、入る車は 12。品物がない店 218、原料がない工場 27
- `vehicles_stuck`(kind=truck, building=28755, limit=5): 敷地の中で WaitingSpace の車が 540、道の上の WaitingSpace が 71。見た日数は 0〜150 日。目的地の店は 555〜5,591 m

## 判断の根拠

- 担当の問題は、観光の入口(0)、貨物駅28755の止まり(540)。前の月の案は、どれも採られていない(9月も案なし)。前の月の調査(m09-survey-port.md)は見つからなかった
- 旅客の入口は、計画の第10月の条件(水・下水・電気の試しが通る)を満たさなかった。水は通ったが、電気の直線は断られ、下水の網はない。外への線路も未確認。実行可否は未確認のため、案にしない
- 港の岸の候補4点は、すべて HeightTooHigh か既存のドックとぶつかった。港の案は出せない
- 28755 の止まりは、原因が出口の不足か道の混みか分からない。道は空いている(s03-1 の記録)が、敷地の中の待ちが続く理由は確かめていない。調査を1件出す
- 政策は、担当の問題に効くものが見当たらなかった。観光の効き(Recreational Use、SmallBusiness)は、前の月に効きが切り分けられなかった(市政ノートの記録)
- 案の数は0。調査1件を出す

## 捨てたもの

- 旅客の駅 (700,1700) の案: 電気の直線が断られ、下水の網がなく、外への線路が未確認。実行対象が確認できないため出せない。11月に電気と下水の別経路が通れば、再提出する
- 港の旅客の岸(4点): HeightTooHigh か既存のドックにぶつかるため、候補にならない
- 空港(Airport 150,000、週 4,800): 平らな空き地は道路と電気・水・下水から遠い。週 4,800 の維持費は、守る線の余裕 約 6,000 のほとんどを使う。条件が未確認のため、出さない
- 貨物駅28755の増設(Cargo Center): 原因が分からないまま増やすと、取り壊しや無駄な建設になる。調査の結果を見てから出す
