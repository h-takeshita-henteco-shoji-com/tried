# m01 経済観光文化局の案

## 案1: 観光の政策 Recreational Use をかける

### 施策

- 案の id: economy-1
- 施策: 街全体に政策 RecreationalUse をかける。場所は指定しない(街全体)
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `list_policies` で RecreationalUse が active=false、costPerWeek=0 であることを確かめる
  2. `set_policy(name="RecreationalUse", active=true)` をかける。戻り値の costPerWeek が 0 であることを確かめる
- 設置条件の確認: 該当なし(政策は場所を取らない)
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: `set_policy` の戻り値の costPerWeek が 0 より大きい、またはエラーが返った場合は見送る。`list_policies` の policyExpensesPerWeek が 10,665 から 1,000 以上増えた場合も見送る

### 期待する効果

- 改善の見込み: 政策一覧の説明は「no direct cost」とだけ書かれ、観光への効果は書かれていない。観光の数字を上げる効き目は確認できていない。試しとして、効き目があるかを見る。
- 数値と期限: 街全体の attractiveness の平均(今 6、最大 157)。今いる観光客(今 1,646)、訪問の平均(今 139)、Tourism の週の収入(今 45)。次の月末に確かめる。数値は見積もれない
- 確認方法: `map_layer`(type=attractiveness、x=0、z=0、radius=2000、n=9)の average と max。`city_info` の tourists(now と visits)。`economy_breakdown` の Tourism。今の値と同じ条件で比べる
- 不確かな点: 政策の効果の大きさは分からない。効き目が出なければ、次の月に解除(`set_policy` で active=false)するかを決める。政策の効果の記述は実測値ではないので、確認は上の数字で行う
- 試し: 仮説は、RecreationalUse が観光地の魅力(attractiveness)を上げ、観光客と Tourism の収入を増やすこと。測る数は上の attractiveness の平均と観光客の数。場所は街全体。基準は attractiveness の平均 6、観光客 1,646、訪問の平均 139、Tourism 45。編成方針の「分からないこと」には当たらないが、5-1、5-2 観光の効き目を測る試しとする

### 費用

- 建設費: 0(政策)
- 週の維持費の増え分: 0(`list_policies` の costPerWeek=0)

### 戻せるか

戻せる。`set_policy` で active=false にすれば外せる。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる

## 案2: 名所 Official Park を北東の商業地(2104,446)に建てる

### 施策

- 案の id: economy-2
- 施策: 名所(Monument)の Official Park を (2104, 446) に、入口を東に向けて建てる。その前に、同じ位置の建物 3 棟を取り壊す(放棄された店 2 棟、店 1 棟)
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み(取り壊しの議決が通ったあとに実行する)
- 対象と操作順:
  1. `preview_bulldoze(x=2128, z=446, radius=30, what="building")` で、壊す建物が 5985(H3 2x3 Shop04、放棄)、14566(Future Store 4x4 Level 3、放棄)、41519(H3 4x3 Shop13、働き口 15)の 3 棟だけであることを確かめる
  2. 議決のあと `bulldoze(x=2128, z=446, radius=30, what="building")` で 3 棟を取り壊す
  3. `test_place_building(prefab="Official Park", x=2104, z=446, facing="east")` を、取り壊しのあとの状態で確かめる(ok=true、cost=45000 を確認)
  4. `place_building(prefab="Official Park", x=2104, z=446, facing="east")` で建てる(建設費 45,000 を払う)
  5. `buildings_near(x=2104, z=446, radius=60, brief=true)` で、Official Park が建ったことを確かめる
- 設置条件の確認:
  - `test_place_building`(assume_removed_buildings=[5985, 14566, 41519])で ok=true。angleUsed=270、入口は (2128, 446)、東向き、道路は segment 6523(Small 4 Lane Road、x=2152 の南北道路)から 16m。費用 45,000、enoughMoney=true
  - `test_place_building`(assume_removed_buildings=[5985, 14566])で、壊す対象は 41519 だけ(wouldDemolish.count=1)
  - `preview_bulldoze`(x=2128, z=446, radius=12)で、41519 は働き口 15、家 0
  - `water_trace`(x=2104, z=446)で、水・下水の網は取水口と排水口につながっている。電気・水・下水は周辺の 41519 で grid が true、problems が None
  - `net_near`(x=2128, z=446, radius=90)で、道路 segment 6523 が入口の近くにあることを確かめた
- 接続工事: 不要(入口の道路 segment 6523 に面している)。電気・水・下水の接続は周辺で確認済み
- 予備候補: Friendly Neighborhood(8x7、建設費 20,000、週の維持費 320)を同じ位置・同じ向き・同じ取り壊し(5985、14566、41519)で試し、ok=true を確認済み(入口の道路 segment 6523 から 12m)。Official Park で建設できない場合は、この予備を使う。ほかの場所は、この案では未確認のため使わない
- 中止する条件:
  - 取り壊しの前の `preview_bulldoze` で、壊す対象が 3 棟以外(別の建物や区間)に増えた場合は見送る
  - 取り壊しのあとの `test_place_building` が ok=false の場合は、予備の Friendly Neighborhood を試す。それも断られたら見送る
  - 働き口の損失が 30 を超えたら見送る
  - 入口の道路 segment 6523 が取り壊しや工事で途切れた場合は見送る

### 期待する効果

- 改善の見込み: 観光の魅力の地図(attractiveness)は、この場所で 0 と確認した(radius 150、n=5 の平均 0、最大 0)。名所を置けば、この場所の魅力が上がり、観光客が寄ることが見込まれる。観光客と Tourism の収入が増えるかは、この案では見積もれない。
- 数値と期限: 2104,446 の半径 150 の attractiveness の平均(今 0)。Monument の棟数(今 6)を 7 にする。街全体の観光客(今 1,646)と Tourism の週の収入(今 45)を、次の月末に確かめる。
- 確認方法: `map_layer`(type=attractiveness、x=2104、z=446、radius=150、n=5)の average と max。`buildings_near`(x=0、z=0、radius=5000、service=Monument)で棟数。`city_info` の tourists と `economy_breakdown` の Tourism。今の値と同じ条件で比べる
- 不確かな点:
  - 名所の効き目の大きさは確認できていない。この場所の魅力が上がっても、街全体の数字は小さく動く可能性がある
  - 入口の道路 segment 6523 は、今の交通で density 100、止まった車が (2157, 474) 付近に 36 台ある(`traffic`)。名所に人が来れば、この道路の混雑が増える。道路の担当と調整が要る
  - 水の使用は今 80%(water used 1,925,008 / capacity 2,400,000)。名所の分は増える
  - 取り壊しで、働き口 15 を失う。店 41519 の分
- 試し: 仮説は、Monument を未開の商業地に置くと、その場所の魅力(attractiveness)が 0 から上がり、観光客が寄って Tourism の収入が増えること。測る数は、2104,446 の半径 150 の attractiveness の平均と、Monument の棟数。場所は (2104, 446) の北東の商業地。基準は attractiveness の平均 0、Monument 6 棟、Tourism 45。編成方針の「分からないこと」の中の、観光の名所の効き目に当たる

### 費用

- 建設費: 45,000(`list_building_types` の Official Park の cost。予備の Friendly Neighborhood は 20,000)
- 週の維持費の増え分: 128(`list_building_types` の upkeepPerWeek。予備は 320)
- 取り壊し: 払い戻しなし(`bulldoze` の説明)。取り壊しで失う働き口は 15、家は 0

### 戻せるか

戻せない。取り壊した 3 棟は元に戻せない(取り壊し)。名所は、あとで `bulldoze` で外せる。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: あり
- 問い: 貨物駅 40031(-1780, -1605)が品物を運ぶ車を一台も出していないのは、列車が来ないからか、道順がないからか。
- 見る道具と引数: `cargo`(引数なし。stations の 40031 の vehiclesLeaving と、shortages.noGoods の数を見る)、`vehicles_stuck`(kind=truck、building=40031、limit=3)、`buildings_near`(x=-1069、z=-770、radius=150、problem=NoGoods、brief=true、limit=20)
- いつ見るか: 見回り1 / 月末
- 何が分かれば次の手が決まるか:
  - 40031 の vehiclesLeaving が 0 のままで、NoGoods の数が減らない場合は、40031 に品物が来ていない。次に、40031 の線の道順と、列車の行き先を調べる
  - 40031 のトラックが道順の計算待ち(WaitingPath など)か、道順なし(none)の場合は、40031 から店へ道をつなぐ案を出す
  - NoGoods の数が減っていれば、40031 以外の貨物駅が効いている。その場合は、この調査を閉じる
- 担当の問題: 6-4、7-1 企業の立地、地場企業(品物がない店 228)

## 見たもの

- `list_policies`: 23 件。RecreationalUse は active=false、costPerWeek=0(no direct cost)。ほか、EducationBoost が active で 7,940、BigBusiness が active で 3,876。SmallBusiness は inactive で 315、IndustrySpace は inactive で 4,821、HighTechHousing は inactive で 20,248、HeavyTrafficBan は inactive で 0。政策の費用は週 10,665(policyExpensesPerWeek)。観光に直接の効果を書いた政策は見当たらない
- `city_info`: 人口 178,872。観光客 now 1,646、visits 139。所持金 2,082,287。週の収入 342,140、支出 332,175。需要 住宅 23 / 商業 2 / 工業 60
- `demand_breakdown`: 働き口 86,175、空き 3,215。働き手が要る大卒の失業 7,720(総数 7,911)。空き家 4,935
- `economy_breakdown`: Tourism 45(Commercial の内訳)。Commercial 41,675。Monument の週の支出 2,280
- `list_building_types`(service=Monument): 解禁済み 23 種。Official Park 45,000 / 週 128、Friendly Neighborhood 20,000 / 週 320、SeaWorld 20,000 / 週 320、ScienceCenter 20,000 / 週 320、Countdown Clock 37,500 / 週 80、Fountain of LifeDeath 30,000 / 週 240、StatueOfWealth 25,000 / 週 400
- `buildings_near`(x=0、z=0、radius=5000、service=Monument): 6 棟。SeaWorld(-1350,-796)、Countdown Clock(1765,622)、ScienceCenter(-1130,-804)、Winter Market 01(-1550,-205)、Fountain(1804,170)、Plaza of Transference(-1560,-855)
- `buildings_near`(x=0、z=0、radius=5000、abandoned=true): 136 件。多くは店で、problems は NoGoods と FatalProblem。放棄された建物は働き口を持たない(取り壊しの損失 0)
- `cargo`: 止まったトラック 802(道の上 296、建物の中 506。うち 28755 が 492)。Goods の import 904、止まり 507。noGoods 228(最大の場所 (-1069, -770) の 74 棟)、noResources 24。40031(-1780, -1605)は vehiclesLeaving 0、vehiclesArriving 0
- `building_stats`: CommercialHigh 1,102(放棄 114)、CommercialLow 166、OfficeGeneric 3,979(レベル3 3,227)、ResidentialHigh 4,057、ResidentialLow 1,013、IndustrialGeneric 806
- `map_layer`(type=attractiveness、x=0、z=0、radius=2000、n=9): average 6、min 0、max 157(2575, 1224)
- `map_layer`(type=attractiveness、x=2575、z=1224、radius=400、n=5): average 23、max 188(2375, 1624)。この周りに Monument はない
- `map_layer`(type=attractiveness、x=2104、z=446、radius=150、n=5): average 0、max 0
- `zone_summary`(grid=1000): Office の空き 1,642 は全部道に面していない(emptyFacingRoad=0)。CommercialHigh の空き 597 のうち道に面する 156。ResidentialHigh の空き 709 は全部道に面していない
- `zone_map`(x=2575、z=1150、radius=450、size=600): 北東は事務所の密集地。空きは少ない
- `zone_map`(x=2750、z=1000、radius=200、size=500): 事務所と道の密集。Monument を置ける空きは見当たらない
- `zone_map`(x=2500、z=500、radius=250、size=500): 空きの白い区画は、風力発電と事務所で埋まっていた
- `land_value`(x=2750、z=1000、radius=200): 平均 61、最小 47、最大 83
- `net_near`(x=2575、z=1224、radius=300、service=Road): 道路 50 区間。(2850,1180)〜(2925,1180) など
- `net_near`(x=2300、z=1010、radius=110、service=Road): 道路 10 区間。z=1010 の道が shop の密集地を通る
- `net_near`(x=2400、z=480、radius=110、service=Road): z=560 の道。風力発電 2 基と給水塔 1 基がある
- `net_near`(x=2128、z=446、radius=90、service=Road): 南北の道 segment 6523(x=2152、z=407〜483、Small 4 Lane Road)、segment 1057〜1854 など
- `buildings_near`(x=2575、z=1224、radius=300): 186 件のうち 30 件を表示。事務所と工場。Monument はない
- `buildings_near`(x=2300、z=1010、radius=90): 25 件。shop の密集。Hotel 2 棟(5266、12373)は放棄
- `buildings_near`(x=2400、z=480、radius=90): 8 件。事務所、風力発電 2 基、給水塔 1 基
- `buildings_near`(x=2128、z=446、radius=70): 8 件。放棄された 5985、14566。店 41519 は働き口 15、問題なし
- `buildings_near`(x=2128、z=446、radius=12): 41519 のみ。grid は電気・水・下水が true、problems は None
- `buildings_near`(x=-1780、z=-1605、radius=150、limit=10): 21 件のうち 10 件。事務所と店と住宅。問題は NoGoods の店が 1 件
- `transport_reach`: 40031 は外とつながる(outsideConnected=true)。14580、16572、48243 は外とつながらない(gap 271m、725m、2933m)。地下鉄の入口 19036 と 25106 は外とつながらない
- `test_place_building`(Friendly Neighborhood、2900、1120、north): ObjectCollision(事務所と道)
- `test_place_building`(SeaWorld、2960、1010、west): ObjectCollision(道と事務所)
- `test_place_building`(ScienceCenter、2790、1400、north): AlreadyExists(事務所)
- `test_place_building`(Friendly Neighborhood、2294、1010、south、assume_removed_buildings=[5266、12373]): ObjectCollision(道 segment 19287、20165 が z=1010 を通る)
- `test_place_building`(Plaza of Transference、2294、1010、south、同じ取り壊し): ObjectCollision(同じ)
- `test_place_building`(Countdown Clock、2112、446、east、assume_removed_buildings=[5985、14566]): ObjectCollision(道 segment 6523 と周りの建物)
- `test_place_building`(Countdown Clock、2100、446、east): ObjectCollision(同じ)
- `test_place_building`(Official Park、2104、446、east、assume_removed_buildings=[5985、14566、41519]): ok=true、cost=45000、enoughMoney=true、入口は道 segment 6523 から 16m
- `test_place_building`(Official Park、2104、446、east、assume_removed_buildings=[5985、14566]): ok=true、wouldDemolish は 41519 の 1 棟、働き口 15
- `test_place_building`(Friendly Neighborhood、2104、446、east、assume_removed_buildings=[5985、14566、41519]): ok=true、cost=20000、入口は道 segment 6523 から 12m
- `preview_bulldoze`(x=2294、z=1010、radius=25、what=building): 2 棟(店 20356、34367)、働き口 4、家 0
- `preview_bulldoze`(x=2128、z=451、radius=12、what=building): 1 棟(41519)、働き口 15、家 0
- `vehicles_stuck`(kind=train、building=40031): 0 台
- `vehicles_stuck`(kind=truck、building=40031): 0 台
- `traffic`(x=2104、z=446、radius=300): 流れ 51%、走っている車 246、止まった車 154。最も混む区間は segment 6523(2152, 443)、density 100。止まりの多い場所は (2157, 474) の 36 台
- `water_trace`(x=2104、z=446): 水の網は取水口(給水塔)と排水口(処理場)につながる。市の水の使用 1,925,008 / 容量 2,400,000。下水の使用 1,923,088 / 容量 2,400,000

## 判断の根拠

- 担当の数字: 観光客 1,646、visits 139、Tourism 45、attractiveness の平均 6、Monument 6 棟。どれも目標から遠い。重点の 5-1、5-2 に効く案を 2 件出す。
- 台帳 `council/ledger.jsonl` は見つからなかった。1か月目として扱う。
- 案1 は、費用が 0 の政策で、議決も要らない。効き目は分からないので、試しとした。政策一覧に観光の効果は書かれていないため、確認できた事実(費用 0、有効でない)だけを根拠にした。
- 案2 は、Monument の Official Park を、観光の魅力が 0 の商業地に置く。空きがない街区で、3 つの候補地の試しのうち、建てられた場所。ほかの候補地(北東の事務所密集、商業の密集)は、道か建物で断られた。取り壊しの議決が要るが、壊す 3 棟は放棄された店 2 棟と働き口 15 の店 1 棟だけ。
- 案の数を 2 件にした理由: ほかの手(Monument を複数の場所に置く、政策を別に 2 つ)は、同じ手の言い換えになるため採らなかった。残りの候補は、根拠が足りないか実行条件が未確認のため、調査に回した。
- 調査を 1 件出した理由: 品物がない店 228 が、6-4 の大きな問題。貨物駅 40031 は外とつながっているのに、車が一台も出ていない。原因が分からないため、見る道具だけで調べる。

## 捨てたもの

- 北東の観光の高い地区(2575, 1224 付近、魅力 157〜188)に名所を置く案: 空きが見当たらず、3 候補地の(2900, 1120)、(2960, 1010)、(2790, 1400)は、道か事務所に断られた。(2294, 1010)は道が z=1010 を通るため不可。
- 事務所の働き口を増やす案(6-4、7-1): 事務所の空き 1,642 は全部、道に面していない(emptyFacingRoad=0)。増やすには新しい道が要り、道路の案として、道の担当と組む必要がある。今月は実行条件が未確認のため出さない。
- 商業の税を下げて店を増やす案: 商業(高)の税は今 3%。下げる幅は ±2 の範囲で、1% にすると税収が大きく減り、週の黒字 +9,965 が消える可能性がある。商業の需要も 2 と低く、税を下げても店が増える見込みが薄い。
- SmallBusiness の政策(週 315): 効き目を確認する材料が政策一覧にない。ほかの効き目の案と比べる根拠がない。
- HeavyTrafficBan(費用 0): 重い車を街の中から締め出す。トラックの運びを止めるおそれがあり、品物がない店の問題を悪くするため見送る。
- FreeTransport(費用 0): 公共交通の運賃をなくすと、バスの収入 5,179 が 0 になる。観光の効きは確認できないため見送る。
- 名所 Friendly Neighborhood の別案(20,000、同じ場所): 案2 の予備に入れた。
- 融資: 所持金 2,082,287 が十分で、借りる理由がない。
