# m01 保健環境局の案

## 案1: 発電所2267の周りに木を植え、汚染の印を測る

### 施策

- 案の id: health-1
- 施策: 汚染の発生源(Combustion Plant、id 2267、座標 x 3604 / z -30)のまわりに、道具 `plant_trees` で木を植える。植える範囲は四角 x 3520〜3760、z -150〜110。木は Tree2(1本10)、間隔 16。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `plant_trees(polygon=[[3520,-150],[3760,-150],[3760,110],[3520,110]], prefab="Tree2", spacing=16, pay=true)` を1回呼ぶ。戻り値の植えた本数と費用を記録する。
  2. 植えた後、`map_layer(type="pollution", x=3604, z=-30, radius=150, n=5)` と `buildings_near(x=3604, z=-30, radius=200, problem="Pollution")` を、基準と同じ条件で呼ぶ。
- 設置条件の確認:
  - `buildings_near(x=3604, z=-30, radius=200)`: 発電所2267(3604,-30)があり、その周りに住宅が約80棟ある。汚染の印の棟は6棟(id 10822, 14620, 16852, 28089, 36382, 45081)。
  - `list_trees`: Tree2 は1本10。
  - 木は建物と道路の上に植えられない(道具の説明どおり)。範囲の中の空きに植わる。植えた本数は戻り値で確かめる。
- 接続工事: 不要
- 予備候補: 木の種類を Alder01(1本10、`list_trees` で確認)に替えて、同じ範囲に植える。種類以外の変更は不要。
- 中止する条件: `plant_trees` の戻り値で植えた本数が50本未満なら、範囲を広げて呼び直す。費用が2,400を超えたら止める。道具が "simulation thread timeout" を返したら、`sim_health` を確かめてから呼び直す。

### 期待する効果

- 改善の見込み: 発電所2267の周りの汚染の印は、`buildings_near` で6棟に集まっている。木が地面の汚染を吸うなら、この6棟の汚染が下がり、汚染の印が減ると予想する。木が汚染を吸う効果は、この街では未確認。
- 数値と期限: 汚染の印 32(`complaints`)。目標は 15 以下。発電所の周りの6棟は、植えてから30日後(月末)に見る。数は見積もれない。
- 確認方法: `map_layer(type="pollution", x=3604, z=-30, radius=150, n=5)` の平均と最大、`buildings_near(x=3604, z=-30, radius=200, problem="Pollution")` の棟数、`complaints` の Pollution の棟数。基準は、中心付近の格子で最大 255(3550〜3700、z -50 付近)、棟数 6。
- 不確かな点: 効果の量は見積もれない。発電所の汚染が強いなら、木だけでは足りないおそれがある。効かなければ、発電所の移設を次の案の候補にする。
- 試し: 仮説は「木が地面の汚染を下げ、発電所の周りの汚染の印が減る」。測る数は `map_layer` の pollution の平均と最大、と汚染の印の棟数(`buildings_near` の problem="Pollution")。場所は (3604, -30) の半径150m。基準は、最大 255、棟数 6。編成方針の「分からないこと」のうち、原因の見立てを試しにする項目に当たる。

### 費用

- 建設費: 最大 2,400(Tree2 1本10 × 最大240本。建物と道路の上は植えないので、実際はこれより少ない)
- 週の維持費の増分: 0 と見積もるが未確認(`list_trees` は1本の費用だけを返し、維持費の項目がない)

### 戻せるか

戻せる。`remove_trees` で取り除ける。払い戻しはない。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 4-3 脱炭素社会
- 編成方針の重点に当たるか: 当たらない

## 案2: 南西のごみの印の地区に、ごみを減らす政策をかける

### 施策

- 案の id: health-2
- 施策: 地区を1つ作り(`paint_district`、中心 x -547 / z -1410、半径 260、名前「南西ごみ」)、その地区だけに政策 Recycling をかける(`set_district_policy`)。Recycling の説明では、ごみの量が -15%、その地区の住宅税が -5%。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `paint_district(x=-547, z=-1410, radius=260, name="南西ごみ")` を1回呼ぶ。戻り値の cells を記録する。
  2. `set_district_policy(district="南西ごみ", name="Recycling", active=true)` を1回呼ぶ。
  3. `list_districts` で、地区「南西ごみ」と Recycling がかかったことを確かめる。
- 設置条件の確認:
  - `list_policies`: Recycling は active=false、costPerWeek=0。
  - `list_districts`: 地区は HighTech(126)と Hakata(127)の2つ。新しい地区の名前は重ならない。
  - `buildings_near(x=-459, z=-1468, radius=400, problem="Garbage")` の結果の8棟(id 1724, 2717, 8317, 10101, 22784, 28680, 33792, 45106)は、すべて中心 (-547, -1410) の半径260m の中に入る。
  - 地区の塗りを試す道具はないため、手順2の戻り値と手順3の `list_districts` で確かめる。
- 接続工事: 不要
- 予備候補: 半径を 300 に広げて、同じ手順を行う。中心は変えない。
- 中止する条件: `paint_district` の cells が0なら止める。`set_district_policy` が断ったら、`list_districts` で地区名の重なりを見て、名前を変えて呼び直す。

### 期待する効果

- 改善の見込み: 地区の中ではごみの量が下がるので、ごみの印の8棟の負担が減り、印が消えると予想する。Recycling の -15% は政策の説明文の数字で、この街での実測はまだない。
- 数値と期限: ごみの印 15(`complaints`)。目標は 0。地区の8棟は、30日後(月末)に見る。数は見積もれない。
- 確認方法: `buildings_near(x=-547, z=-1410, radius=260, problem="Garbage")` の棟数と、`complaints` の Garbage の棟数。基準は、地区の中の棟が8、街全体が15。
- 不確かな点: ごみの印の原因が収集の遅れなら、発生が減っても印は残るおそれがある。収集の遅れには、交通の詰まりが効いている可能性がある(ごみ収集車 234 台のうち多くが渋滞で止まっている。`vehicles_stuck`)。地区に入る区画は、HighTech 地区の政策(HighTechHousing など)が外れる。この影響は、財政と住宅の局が判断する。
- 試し: 仮説は「地区のごみの発生を減らすと、ごみの印の棟が減る」。測る数は、地区の中の Garbage の棟数(`buildings_near`)と、街全体の Garbage の棟数(`complaints`)。場所は (-547, -1410) の半径260m。基準は、地区の中が8棟、街全体が15棟。

### 費用

- 建設費: 0
- 週の維持費の増分: 0(`list_policies` の Recycling の costPerWeek=0)。地区の住宅税の減り(-5%)は、この地区の分だけで、未測定。

### 戻せるか

戻せる。`set_district_policy` で active=false にし、`paint_district` で erase=true にすれば元に戻る。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 4-4 資源循環
- 編成方針の重点に当たるか: 当たらない

## 案3: 市全体で喫煙規制をかけ、健康の平均を測る

### 施策

- 案の id: health-3
- 施策: 政策 SmokingBan を街全体にかける(`set_policy(name="SmokingBan", active=true)`)。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `set_policy(name="SmokingBan", active=true)` を1回呼ぶ。戻り値の週の費用の見積もりを記録する。
  2. 30日後に `citizens_summary`(average.health、peopleWithProblems.badHealth)と `city_info`(happiness)を見る。
- 設置条件の確認:
  - `list_policies`: SmokingBan は active=false、costPerWeek=0(説明は "no direct cost")。
  - 政策の操作に建物や線の条件はない。
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: `set_policy` の戻り値の週の費用が0より大きければ、外す(`set_policy(name="SmokingBan", active=false)`)。`city_info` の happiness が85から5以上下がったら外す。

### 期待する効果

- 改善の見込み: 喫煙を規制すると、市民の病気が減り、健康の平均が上がると予想する。この予想は政策の説明文から立てたもので、この街での効果は未確認。
- 数値と期限: 健康の平均 78(`citizens_summary`)。目標は 80 以上。体調の悪い市民は 2,391(peopleWithProblems.badHealth)。30日後(月末)に見る。数は見積もれない。
- 確認方法: `citizens_summary` の average.health と peopleWithProblems.badHealth、`city_info` の happiness。基準は、健康 78、体調の悪い市民 2,391、幸福度 85。
- 不確かな点: 政策の効果は見積もれない。幸福度が下がるおそれがある。政策の説明に費用が0とあるが、効果の内容は説明文に書かれていない。
- 試し: 仮説は「喫煙規制が病気を減らし、健康の平均が上がる」。測る数は、`citizens_summary` の average.health と badHealth の数。場所は街全体。基準は、健康 78、体調の悪い市民 2,391。編成方針の「分からないこと」に当たる、健康の平均が上がらない原因の確かめ。

### 費用

- 建設費: 0
- 週の維持費の増分: 0(`list_policies` の SmokingBan の costPerWeek=0)

### 戻せるか

戻せる。`set_policy(name="SmokingBan", active=false)` で外せる。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 1-2 健やかで心豊かに暮らせる社会
- 編成方針の重点に当たるか: 当たらない

## 案なし

(案1から3を出すので、この見出しは書かない)

## 調査

- 調査: あり
- 問い: 死体の印が、火葬場2か所の近くの(2240, 186)周りに残るのは、霊柩車が渋滞で止まるためか。
- 見る道具と引数: `vehicles_stuck(kind="hearse", building=36841, limit=10)`、`buildings_near(x=2240, z=186, radius=250, problem="Death", brief=true)`
- いつ見るか: 見回り1 / 月末
- 何が分かれば次の手が決まるか: 霊柩車の多くが Congestion か Blocked なら、渋滞の解消を交通の局へ回す(この局の手にはしない)。霊柩車が Stopped や WaitingTarget で止まり、死体の印が残るなら、火葬場 36841 と 31990 の霊柩車の数を確かめて、次の月に案を出す。
- 担当の問題: 1-2 健やかで心豊かに暮らせる社会(死体の印は保健環境局の担当の困りごと)

## 見たもの

- `city_info`: 人口 178,872、幸福度 85、所持金 2,082,287、週の収入 342,140 と支出 332,175、観光客 1,646、電気・水・下水が来ない市民 0 / 0 / 0
- `citizens_summary`: 住民 178,916、健康の平均 78、幸福度 89、体調の悪い市民 2,391(peopleWithProblems.badHealth)、病気 1,955(sick)、失業 6,584(大学卒 6,483)
- `complaints`: 印のある棟 341。死体 52、品物がない店 228、汚染 32、ごみ 15、騒音 7、火事 4、犯罪 3。ごみの hotspot は (-459, -1468)、汚染の hotspot は (3882, -296)、死体の hotspot は (2240, 186)
- `list_policies`: 有効なのは EducationBoost(週 7,940)、BigBusiness(週 3,876)。政策の費用は合わせて 10,665。SmokingBan は active=false、costPerWeek=0。Recycling は active=false、costPerWeek=0(説明: 住宅税 -5%、ごみ -15%)。SmokeDetectors、PowerSaving、WaterSaving、HighTechHousing は費用が大きい。HeavyTrafficBan は0だが、大型車を止めるため案にしない。
- `services`: 電気 2,430,368 に対し使用 1,712,096。水と下水は約 80%。埋立地が満杯 7(16914, 19182, 23032, 25590, 25826, 29270, 45892)。火葬場・墓地は容量 24,000 に対し使用 12,791(満杯なし)。医療 5,000 に対し使用 1,953。
- `buildings_near(x=-459, z=-1468, r=600, service="Garbage")` と `buildings_near(x=0, z=0, r=5000, service="Garbage", brief)`: 埋立地 20、ごみ焼却(Combustion Plant)7。焼却 33797(-570, -1840)は保管 373,750 / 400,000(93%)、収集車 9 / 34 が出ている。
- `buildings_near(x=3604, z=-30, r=300, problem_only)`、`buildings_near(x=3604, z=-30, r=200, brief)`、`buildings_near(x=3604, z=-30, r=100, service="Garbage")`: 焼却 2267(3604, -30)は保管 328,033 / 400,000(82%)、収集車 24 / 34。周りに住宅(別荘など)が約80棟。汚染の印は 6棟(id 10822, 14620, 16852, 28089, 36382, 45081)。
- `buildings_near(x=-459, z=-1468, r=400, problem="Garbage")`: ごみの印の棟 8(id 1724, 2717, 8317, 10101, 22784, 28680, 33792, 45106)。
- `buildings_near(x=0, z=0, r=5000, service="HealthCare", brief)`: 医療の建物 85。火葬場(Crematory)と墓地(Cemetery)も HealthCare の service に入っている。
- `buildings_near(x=2240, z=186, r=250, service="HealthCare")`: 火葬場 31990(2224, 60)と 36841(2218, 286)。どちらも保管 0、霊柩車 6 / 9 が出ている。
- `buildings_near(x=2240, z=186, r=300, problem="Death")`: 死体の印の棟 3(id 130、20191(空き家)、48338)。
- `buildings_near(x=3900, z=-1000, r=350, brief)`: 住宅と工場が混ざる。工場は x 3600〜4180 に多い。
- `buildings_near(x=1684, z=-1253, r=400, brief)`: 健康のカバーが 0 の場所は、ほぼ工場(sweatshop、bigfactory)。住宅はほぼない。
- `buildings_near(x=-1000, z=1600, r=400, brief)`: 建物 0。健康のカバーが 0 の北西は、住む人がいない。
- `map_layer(type="health", n=9, radius=2500)`: 平均 84。カバー 0 は北西(z 1720 付近)と南東(x 1684〜4354、z -758〜-2244)。
- `map_layer(type="health", x=2240, z=186, n=9, radius=800)`: 平均 152、最小 51。この区域は十分にカバーされている。
- `map_layer(type="pollution", n=9, radius=2500)`: 平均 45。高いのは北西(z 1720 付近)と、東の工場の周り(x 3550〜4000、z -500〜-650)。
- `map_layer(type="pollution", x=3700, z=-200, n=9, radius=600)`: 最大 255 が、(3550〜3700、z -50〜100)の発電所 2267 の周り。
- `map_layer(type="pollution", x=3600, z=-30, n=9, radius=300)`: 最大 255 が、(3550〜3700、z -50 付近)。基準として記録する。
- `vehicles_stuck(kind="garbage", limit=30)`: ごみ収集車 234 台。多くが Congestion か Blocked。行き先のない車が 109 台あり、(0,0) 付近に多い。
- `vehicles_stuck(kind="hearse", limit=15)`: 霊柩車 160 台。Congestion+OnRoad が 36、Congestion+Blocked が 50、Spawned+OnRoad+Blocked が 37。
- `test_place_building(prefab="Landfill Site", x=-280, z=-2000, facing="north")`: ObjectCollision。公園の小道と線路にぶつかる。
- `test_place_building(prefab="Landfill Site", x=-330, z=-1995, facing="north")`: ObjectCollision。道路、小道、線路にぶつかる。
- `list_trees`: 植えられる木 40 種、1本 10(Tree2、Alder01 など)。
- `list_districts`: HighTech(126、人口 75,326、政策 EducationBoost・BigBusiness・HighTechHousing)、Hakata(127、人口 2,820、政策 EducationBoost・BigBusiness)。
- `list_building_types(service="Garbage")`: 埋立地(4,000、維持費 160/週、容量 8,000,000)、焼却(30,000、維持費 1,440/週)。
- `list_building_types(service="HealthCare")`: 診療所(10,000、400/週)、病院(65,000、2,400/週)、火葬場(25,000、720/週)、墓地(8,000、160/週)。
- `list_building_types(service="Deathcare")`、`list_building_types(service="DeathCare")`、`list_building_types(service="Cemetery")`、`list_building_types(service="DeadCare")`: 0件。火葬場と墓地は service が HealthCare。
- `zone_map(x=-459, z=-1468, radius=400)`: 住宅が詰まり、空いた土地はない。この呼び出しで save_to を付けたため、画像 council/m01-health-garbage-map.jpg が1つ残った(下の注意を見る)。
- `zone_map(x=3750, z=-150, radius=500)`: 発電所 2267 の周りは住宅、東は工場と事務所。
- `zone_map(x=-400, z=-1850, radius=350)`: 南の縁は公園と線路。埋立地を置く空きは見当たらない。

## 判断の根拠

- 目標との差は、汚染の印が 32 に対し 15 以下(差 17)、ごみの印が 15 に対し 0(差 15)、健康の平均が 78 に対し 80 以上(差 2)。
- 汚染は、発電所 2267 の周りの6棟に集まっている。発電所の保管が82%で、近くに住宅が約80棟ある。木を植える案を試しとして出した。木が汚染を下げるかは未確認なので、測る数を決めた。
- ごみは、ごみの印の8棟が、焼却 33797 から約380m、非満杯の埋立地から1,000m以上離れている。収集車が渋滞で止まっているのが主な原因と見る。埋立地を近くに置く案は、候補の空きが見つからず出せなかった。代わりに、ごみの量を地区だけで減らす政策(Recycling)を案にした。全市の Recycling は住宅税の -5%(約13,000/週)で週の収支が赤字になるため、地区だけにした。
- 健康の平均は、健康のカバーが0の区域が工場地帯か人のいない北西にあり、住宅の隙間は確かめられなかった。喫煙規制(SmokingBan、費用0)を試しにした。
- 死体の印は、火葬場が近くに2つあるのに残っている。原因が分からないので、調査にした。
- 案は3件にした。担当の4-3、4-4、1-2 に効く手を、費用0か小さい範囲で選んだ。編成方針の重点(観光、物流、交通)には当たらない。
- 前の月の答え合わせはない(1か月目)。台帳もない。

## 捨てたもの

- 埋立地をごみの印の地区の近くに新設: 候補の (-280, -2000) と (-330, -1995) は、公園の小道と線路にぶつかり置けなかった(test_place_building)。ほかの空きは、地図上で確かめられなかった。
- 発電所 2267 を移す(relocate_building、費用は建設費の1/5 = 6,000): 効きは大きいと見込むが、移す先の水・下水の接続と道路が未確認。次の月に候補として調べる。
- 全市の Recycling: 住宅税の -5% は、住宅の税収 265,121/週 の 5% で約 13,000/週。週の収支 +9,965 が赤字になるため、公約3に反する。
- 病院・診療所の追加: 健康のカバーが 0 の区域は工場地帯で、住む人が少ない。効く人が確かめられない。
- 満杯の埋立地を空にする(empty_building): 満杯 7 か所は1,000m 以上離れた区域にある。空にした中身は、ほかの埋立地へ運ばれ、残りの容量は約 3,500 万しかない。溢れるおそれがある。
- HeavyTrafficBan: 大型車(ごみ収集車、霊柩車)を止めてしまうため、案にしない。
- 観光・物流・交通: 編成方針の重点だが、担当外。この局では扱わない。

---

注意: 地図の確認で `zone_map` に save_to を付けたため、`council/m01-health-garbage-map.jpg` が1つ残っている。局の書き込みは本来このファイル1つだけ。取り除きが必要。
