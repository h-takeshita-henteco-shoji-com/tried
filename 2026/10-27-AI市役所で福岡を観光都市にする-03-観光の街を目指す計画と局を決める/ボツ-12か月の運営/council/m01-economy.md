# m01 経済観光文化局の案

## 案1: 東の商業街に名所 Friendly Neighborhood を1棟置く(道路の支線つき)

### 施策

- 案の id: economy-1
- 施策: 名所(Monument)1棟を座標 (2760, 966) に、向き south(入口が北を向き、支線の道路に面する)で `place_building` で置く。道路は `build_line` で (2822, 940) から (2732, 940) まで Basic Road を引き、既存の道路の節点につなぐ。市の計画の 5-1、5-2 観光(名所の棟数 6 → 10 の一部)に当たる
- 議決: 要らない

### 実行計画

- 実行可否: 未確認
- 対象と操作順:
  1. `build_line` prefab="Basic Road"、points=[[2822, 940], [2732, 940]]、pay=true(建設費 480)。既存の節点 (2822, 940) につなぐ
  2. `build_line` の後、`test_place_building` prefab="Friendly Neighborhood"、x=2760、z=966、facing="south" を再度呼ぶ。入口 (2760, 938) の entrance.road が null でなくなることを確かめる
  3. 確かめたら `place_building` prefab="Friendly Neighborhood"、x=2760、z=966、facing="south"、pay=true(建設費 20,000)
- 設置条件の確認:
  - `test_build_line`(Basic Road、[[2822,940],[2732,940]]): ok=true、overlaps なし、cost 480、enoughMoney=true
  - `test_place_building`(Friendly Neighborhood、2760、966、south): ok=true、wouldDemolish count 0、lostByDemolish 0。ただし entrance.road は null(支線が未施工のため)
  - `test_place_building`(Friendly Neighborhood、2760、914、north): ok=true、wouldDemolish 0、entrance.road は null(同上)
  - 電気・水・下水: `water_trace`(2760, 966)の近くの建物(2830, 1016 のオフィス)は electricity / water / sewage とも true。水の網はつながり、capacity 2,400,000 に対し used 1,925,008(水)、1,923,088(下水)
  - `test_place_building`(Countdown Clock、2765、1010、west): 断られた(AlreadyExists)。この案では使わない
  - 不確かな点: 支線の施工後に entrance.road が認められるかは、施工後の `test_place_building` で確かめる(上の 2)
- 接続工事: Basic Road の支線 1本(約 90m)。建設費 480、週の維持費の増分 約 4(40 / km / 週 × 0.09 km)。道路は既存の節点 (2822, 940) につなぐ
- 予備候補: 確認済みの予備はない。試したが使わないもの: (2705, 835)、(2440, 700)(取り壊しで住宅 52・働き口 42 を失う)、(2240, 522)(埋立地)、(2525, 522)(埋立地)、(2770, -560)(住宅が建っている)、(2765, 1010) の Countdown Clock(断られた)
- 中止する条件:
  - 支線の施工後、`test_place_building` で entrance.road が null のままなら中止する
  - 施工後に電気・水・下水の grid が false の建物があれば、置く前に中止する
  - 費用が 20,480 を超えたら中止する(建設費の枠 300,000 と維持費の枠 4,900 の範囲内)

### 期待する効果

- 改善の見込み: 名所の数を 6 から 7 に増やし、東の商業の近くに魅力度(attractiveness)を足す。これで観光客が寄る店が増え、Tourism の週の収入が増えると予想する。名所の増え分は目標 10 のうち 1 にあたる。ただし名所の魅力度の大きさは道具で確かめられない。
- 数値と期限: 基準は置く前に `map_layer`(type=attractiveness、x=2760、z=966、radius=300、n=9)で測る。期限は月末(30日目)。Tourism の週の収入は今 45。名所の棟数は今 6
- 確認方法: `map_layer` attractiveness(同じ x, z, radius で比べる)、`buildings_near`(service=Monument、radius=5000、brief=true)の棟数、`economy_breakdown` の Tourism
- 不確かな点: 数値は見積もれない。効果が出るには、近くの店に品物が届くことが要る(品物がない店が 228 あり、店が営業しないと観光客が落とすお金は増えない)。効果が出る距離も未確認
- 試し: なし(名所の増加で、魅力度と棟数を測る)

### 費用

- 建設費: 20,480(Friendly Neighborhood 20,000、支線 480)
- 週の維持費の増え分: 約 324(Friendly Neighborhood 320、支線 約 4)

### 戻せるか

戻せる。名所は `bulldoze` で取り壊せるが、取り壊しの払い戻しはない。取り壊しの議決が要る。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 5-1、5-2 観光(名所の棟数 6 → 10)
- 編成方針の重点に当たるか: 当たる

## 案2: 観光の公共政策 RecreationalUse をかける(試し)

### 施策

- 案の id: economy-2
- 施策: 街全体の政策 RecreationalUse を `set_policy`(name="RecreationalUse"、active=true)でかける。週の費用は 0
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `set_policy` name="RecreationalUse"、active=true。かけた後、`list_policies` で有効になったか、週の費用(costPerWeek)が 0 のままかを確かめる
- 設置条件の確認: `list_policies`(この月に取得)で、RecreationalUse は active=false、costPerWeek=0、costBasis「no direct cost」。建設ではないので設置条件は該当なし
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: `list_policies` で costPerWeek が 0 でなくなったら、外す(active=false)。政策の一覧に、ほかの建物の数に応じた費用が出たら中止する。政策は 1 つまでとする

### 期待する効果

- 改善の見込み: 政策一覧には効果の記述がないため、効果の見込みは確かめていない。政策の記述を実測値とは扱わない。観光の魅力度(attractiveness)か、観光客の訪問を増やす政策であるかは、この試しで確かめる
- 数値と期限: 基準は今の値。attractiveness 平均 6(全体、`map_layer` type=attractiveness)、Tourism の週の収入 45(`economy_breakdown`)、今いる観光客 1,646 と訪問 139(`city_info`)。期限は月末(30日目)
- 確認方法: `map_layer` type=attractiveness(n=9、radius=500、今と同じ範囲)、`economy_breakdown` の Tourism、`city_info` の tourists(now と visits)。すべて今の値と同じ条件で比べる
- 不確かな点: 数値は見積もれない。効き目が出るなら、魅力度が上がるか、観光客の訪問が増えるかのどちらかが先に動く。ほかの市民への影響(幸福度、税収など)は未確認
- 試し: あり。
  - 仮説: 街全体の政策で、観光地の魅力度が上がり、観光客の訪問が増え、Tourism の収入が増える
  - 測る数: `map_layer` attractiveness の平均と最大、`city_info` の tourists.now と visits、`economy_breakdown` の Tourism
  - 場所: 街全体
  - 基準: attractiveness 平均 6、最大 157(座標 2575, 1224 付近)。Tourism 45。観光客 1,646、訪問 139
  - 編成方針の「分からないこと」(観光客の週の収入が 45 しかない理由)のうち、attractiveness の項目を確かめる

### 費用

- 建設費: 0
- 週の維持費の増え分: 0(`list_policies` の costPerWeek=0)

### 戻せるか

戻せる。`set_policy` で active=false にすれば外せる。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 5-1、5-2 観光(attractiveness の平均 6 → 12 と、Tourism 45 → 1,000)
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: あり
- 問い: 品物がない店が減らないのは、貨物駅 28755(Cargo Center 3449, -1555)の周りで止まったトラックのせいか。
- 見る道具と引数: `vehicles_stuck`(kind="truck"、building=28755、limit=10)、`cargo`(引数なし)
- いつ見るか: 見回り1、月末
- 何が分かれば次の手が決まるか: 止まったトラックの多くが 28755 の敷地内で待っていれば、その分の荷物の流れを 8-1 の港湾空港局の案として出す。止まったトラックが道の上で待っていれば、道路の混雑を見る案に切り替える。品物がない店の場所(-1069, -770 の 74 棟、2206, 729 の 46 棟)が移れば、その近くの荷物の流れを調べる
- 担当の問題: 6-4、7-1 企業の立地、地場企業(品物がない店 228 → 120 以下)。5-1、5-2 観光(店が営業すると観光の収入が増える)

## 見たもの

- `list_policies`: 有効な政策は EducationBoost(週 7,940)、BigBusiness(週 3,876)。RecreationalUse は無効で costPerWeek 0。政策の週の費用の合計は 10,665。SmokeDetectors、WaterSaving、PowerSaving、IndustrySpace、HighTechHousing、SmallBusiness は無効。観光の効きに直接関わる政策は見当たらない
- `city_info`: 人口 178,872、幸福度 85、所持金 2,082,287、週の収入 342,140、週の支出 332,175(収支 +9,965)、観光客 now 1,646 / visits 139、需要(住 23 / 商 2 / 工 60)。電気・水・下水が来ない市民 0 / 0 / 0
- `economy_breakdown`: Tourism 45(Commercial の内訳)、Citizen 41,630、Commercial 41,675、Office 24,556。Monument の維持費 2,280。政策 10,665
- `list_building_types`(service=Monument、解禁済み): Countdown Clock 37,500(週 80、12×12)、Fountain of LifeDeath 30,000(週 240、7×7)、Friendly Neighborhood 20,000(週 320、8×7)、SeaWorld 20,000(週 320、12×12)、ScienceCenter 20,000(週 320、11×14)、Official Park 45,000(週 128、6×6)、StatueOfWealth 25,000(週 400、8×8、水と下水が不要)ほか
- `buildings_near`(service=Monument、radius=5000): 名所 6 棟(SeaWorld 2374 at -1350,-796、ScienceCenter 29187 at -1130,-804、Winter Market 01 30532 at -1550,-205、Plaza of Transference 45587 at -1560,-855、Countdown Clock 9113 at 1765,622、Fountain 41780 at 1804,170)
- `map_layer`(attractiveness、n=9、radius=500 既定): 平均 6、最大 157(2575, 1224)、次いで 40(2575, 729)、34(795, -263)、30(1684, 1224)、67(-2761, 233)。商業の地区のまわりでは低い
- `map_layer`(landvalue、2400, 900、radius=600、n=5): 平均 56、最大 73
- `building_stats`(radius=5000): 商業(高)1,102 棟(廃墟 114、うちレベル3 880)、商業(低)166 棟、オフィス 3,979 棟(レベル3 3,227)、住宅(高)4,057 棟、住宅(低)1,013 棟、工業 806 棟
- `cargo`: トラック 2,111 台、止まったトラック 802(道の上 296、建物の敷地 506)。敷地内の上位は貨物駅 28755 の 492 台(3449, -1555)と港 1366 の 14 台。品物がない店 228(-1069,-770 に 74、2206,729 に 46、1004,300 に 33)、原料がない工場 24
- `demand_breakdown`: 働き口 86,175(空き 3,215)、住宅 55,253(空き 4,935)、失業 7,911(大学卒が 7,720)、ホームレス 0
- `zone_map`(2400,1000 r700、2450,550 r350、2450,-450 r600、900,-200 r500、2650,700 r300): 東の商業(高)の帯は (2650–2665, 800–1000) 付近。中央の灰色の大区画は埋立地(landfill)。2770,-560 の空きに見えた区画は住宅(villa)
- `zone_summary`(grid=1000): 商業(高)の空き 597、うち道に面した空き 156、廃墟になった商業の棟が多い
- `buildings_near`(abandoned=true、2600,800 r900): 廃墟 33 棟。廃墟の商業は NoGoods(品物がない)。廃墟のホテル 5266(2286,986)、12373(2302,1034)、44162(2068,986)
- `preview_bulldoze`(2294,1010 r45、building): 壊すと 11 棟、働き口 46、住宅 0。働いている店が含まれるので、取り壊しは見送る
- `net_near`(2760,975 r90): 道路 (2822, 940)–(2822, 1000) の縦の道、(2850,920)–(2822,940)、(2822,1000)–(2850,1000)
- `test_build_line`(Basic Road、[[2822,940],[2732,940]]): ok、cost 480、overlaps なし
- `test_build_line`(Basic Road、[[2667,940],[2732,940]]): 断られた(2649,947 と 2658,925 の店と重なる)
- `test_place_building`(Friendly Neighborhood、2760,940、west): ok、wouldDemolish 0、entrance.road null
- `test_place_building`(Friendly Neighborhood、2760,966、south): ok、wouldDemolish 0、entrance.road null
- `test_place_building`(Friendly Neighborhood、2760,914、north): ok、wouldDemolish 0、entrance.road null
- `test_place_building`(Friendly Neighborhood、2760,1010、west): ok、wouldDemolish 0、entrance.road null
- `test_place_building`(Friendly Neighborhood、2790,940、east): 断られた(道路 2822 と 2836 に重なる)
- `test_place_building`(Friendly Neighborhood、2790,985、east、2760,1010 の Fountain の east): 断られた(道路に重なる)
- `test_place_building`(Friendly Neighborhood、2848,965、west): 断られた(道路に重なる)
- `test_place_building`(Friendly Neighborhood、2705,835、west): ok だが、住宅 3129・23093 を取り壊す(住宅 31 を失う)
- `test_place_building`(Official Park、2705,835、west): ok だが、住宅 23093 を取り壊す(住宅 12 を失う)
- `test_place_building`(Friendly Neighborhood、2440,700、south): ok だが、オフィス 3799・13456 と住宅 4376・15520 を取り壊す(働き口 42・住宅 52 を失う)
- `test_place_building`(Countdown Clock、2240,522、north): 断られた(埋立地 45436 に重なる)
- `test_place_building`(Fountain of LifeDeath、2525,522、north): 断られた(埋立地 3565 に重なる)
- `test_place_building`(Fountain of LifeDeath、2770,-560、south): 断られた(住宅 34411、38059、43900)
- `test_place_building`(Countdown Clock、2765,1010、west): 断られた(AlreadyExists。理由は示されず)
- `water_trace`(2760, 966): 近くのオフィス(2830, 1016)は電気・水・下水 true。水の網は取水口・排水口とつながっている。水の使用 1,925,008 / 容量 2,400,000
- `list_net_types`(service=Road、locked=false): Basic Road 5,000 / km、維持費 40 / km / 週
- `vehicles_stuck`、`traffic`、`citizens_summary`、`services`、`economy`: この月は呼んでいない

## 判断の根拠

- 担当の数字: 観光客 1,646 は目標 3,000 に対して低い。Tourism の週の収入は 45 で、目標 1,000 から大きく離れる。名所は 6 で、目標 10 まで 4 つ足りない。attractiveness の平均は 6 で、目標 12 まで届かない。
- 原因の見立て: 商業(高)の廃墟 114 棟のほとんどが品物がない店(NoGoods)で、店が営業しなければ観光客が落とすお金も増えない。品物の流れは 8-1 の港湾空港局の課題に当たるため、この局では調査にして、施策とは分けた。
- 案1(名所): 名所を増やすのは観光の市の計画の施策(5-1、5-2)に当たる。場所は、取り壊しなしで置けて、道路の支線(約 90m)で接続できる東の商業の近くの空きを選んだ。費用は建設費 20,480、維持費の増え分は約 324 / 週で、枠の範囲内。ただし支線の施工後にしか入口の道路は確かめられず、未確認なので実行可否は未確認にした。
- 案2(政策の試し): RecreationalUse は costPerWeek=0 で、議決が要らず、戻せる。政策の一覧には効果の記述しかないので、効き目は試しとして、attractiveness と Tourism で確かめる。
- 案の数を 2 件にした理由: 名所の場所は、取り壊しを避けて置ける場所が少なく、確認できたのは東の 1 か所だけだった。確認できない場所を案にしないため。試しの政策は、ほかの手と別に効きを測れる。
- 調査を 1 件出した理由: 品物がない店が 228 のまま減らない原因が、貨物駅 28755 の周りの渋滞か、道の上の混雑かが分からないため。月末の見る道具で止まったトラックを確かめる。

## 捨てたもの

- 名所 Countdown Clock(37,500、週 80)を東の商業の近くに置く案: 候補の 2765, 1010 は断られ(AlreadyExists)、別の場所では埋立地に重なるため、確認できる場所がなかった
- 名所を 2 棟目以降に増やす案: 1 棟目の効きが分からないうちは、場所の確認ができた範囲で増やさない
- 廃墟のホテル(5266、12373、44162)を取り壊して名所を置く案: 取り壊しの議決が要る。廃墟のホテルの周りには営業中の店が 11 棟あり、一緒に壊すと働き口 46 を失う。確かめた範囲では、取り壊さない手を先にする
- 店の品物を増やすため、貨物駅 28755 の周りに道路や駅を足す案: 8-1 の港湾空港局の課題で、この局の案としては、原因を調査で確かめてから出す
- 政策 BigBusiness や SmallBusiness の変更: 商業の需要は 2 で、店は足りている。品物がない店が増える理由は解消しないので、効き目が見込めない
- 税率の変更: 担当の数字(観光、働き口、品物)に効くと確かめられる根拠がない
