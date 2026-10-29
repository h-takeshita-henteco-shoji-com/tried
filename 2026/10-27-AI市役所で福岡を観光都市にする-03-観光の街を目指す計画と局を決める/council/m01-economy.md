# m01 経済観光文化局の案

## 案1: 観光の名所(Official Park)を1棟、放棄された建物の跡に置く(B)

### 施策

- 案の id: economy-1
- 施策: 名所(Monument の Official Park、6×6マス)を、B(2118, 482)(東部の中ほど)の1棟に置く。いまの空き区画の跡(放棄された店を壊した後)に置く。名所は観光客の attractiveness を上げ、観光客と Tourism の収入を増やす見込み。A(2286, 972)は住宅都市みどり局の urban-1(Friendly Neighborhood)に譲る(局をまたぐ調整)
- 議決: 取り壊し(`bulldoze` で建物を壊す。5985、41519、44794。戻せない)

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `bulldoze`(x=2128, z=471, radius=30, what="building")。壊す建物は 5985(店、働き口0)、41519(店、働き口15)、44794(店、働き口4)。失う働き口は19、家は0
  2. `place_building`(prefab="Official Park", x=2118, z=482, facing="east", pay=true)。入口は (2142, 482) の道路 segment 6523(Small 4 Lane Road、2m)。建設費 45,000
- 設置条件の確認:
  - B: `test_place_building`(Official Park、x=2118、z=482、facing east、assume_removed_buildings=[5985, 41519, 44794])が ok(是正で再確認)。道路は入口から2m。電気・水・下水は `water_trace` で届いている(案の作成時に確認)。`preview_bulldoze`(x=2128、z=471、radius 30、what=building)で壊す建物は上の3棟だけ、失う働き口19と再確認
  - 費用: 45,000(所持金 2,082,287 から。守る線 1,874,000 以上を保つ)
- 接続工事: 不要(道路と管、送電線は既存。入口の道路は既に通っている)
- 予備候補: なし。置けなければ見送る(本案は1棟だけなので、代わりの場所は出さない)
- 中止する条件: 壊す前に、`preview_bulldoze` の壊す建物の一覧が上と違えば中止する。`test_place_building` が断ったら見送る。電気・水・下水が届かなければ見送る

### 期待する効果

- 改善の見込み: 名所は attractiveness を上げ、観光客が寄る地区を増やす、と局は予想する。B は今の attractiveness 平均が14(半径150m、最大126)。名所を置いた後、平均が上がれば、観光客と Tourism の収入も増えると予想する
- 数値と期限: attractiveness の平均(半径150m、B の周り)と、city_info の tourists.now と visits、economy_breakdown の Tourism。基準は tourists.now 1,646、visits 139、Tourism 週45、名所6棟、B の周り平均14。期限は見回り2(第2月)まで。Tourism が目標の週1,000に届くかは、局の予想では数か月後。量は見積もれない
- 確認方法: `map_layer`(type=attractiveness、x=2118、z=482、radius=150、n=3)。`city_info`(tourists)。`economy_breakdown`(Tourism)。`buildings_near`(service=Monument、radius=3000、brief)で名所の棟数を数える
- 不確かな点: 名所が attractiveness をどれだけ上げるかは、この街では確かめていない。効き目が小さければ、第2月の見回りで2棟目以降を増やさない。取り壊しで働き口が19減る。Tourism の収入は、店に品物が届かない限り増えにくい(品物がない店 228)
- 試し: あり。仮説: 名所を置くと、その周りの attractiveness が上がり、観光客の数と Tourism の収入が増える。測る数は、`map_layer` の attractiveness(B の周り半径150m)と、`city_info` の tourists.now。場所は B(2118, 482)。基準は B の平均14、街全体の tourists.now 1,646。編成方針の分からないこと(1)に当たる

### 費用

- 建設費: 45,000(`list_building_types` の Official Park の cost。是正で再確認)
- 週の維持費の増え分: 128(`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せない。壊した建物は戻らず、名所は取り壊す操作で消す。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 5-1、5-2 観光(今いる観光客、訪問の平均、Tourism の収入、attractiveness、名所の棟数)
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: あり
- 問い: 品物がない店(228)は、どの道で貨物の車が届かないことで増えているか。届かない店の近くの経路を、貨物の車の止まり方から確かめる
- 見る道具と引数: `cargo`(引数なし。shortages.noGoods の spots を見る)、`vehicles_stuck`(kind="truck"、limit=10)
- いつ見るか: 見回り1、見回り2、月末
- 何が分かれば次の手が決まるか: noGoods の店が見回りのたびに減るなら、今の貨物の流れを保つ。増えるか変わらないなら、止まった貨物の車が多い道を、港湾空港局と道路下水道局に求める。貨物の車の止まり先が貨物センター28755に集中していれば、その詰まりの対策を港湾空港局に求める。調べた結果は港湾空港局と共有する
- 担当の問題: 6-4、7-1 企業の立地、地場企業(品物がない店)。市の計画の 8-1 物流・人流のゲートウェイとも関わる

## 見たもの

- `city_info`: 人口178,872、所持金2,082,287、週の収支+9,965(収入342,140、支出332,175)、幸福度85、観光客now 1,646・visits 139、需要(住23/商2/工60)、電気・水・下水が来ない市民0
- `list_policies`: 有効な政策は EducationBoost(週7,940)と BigBusiness(週3,876)。政策の費用は合計 10,665。観光に効く政策は一覧にない(SmallBusiness は無効で週315、TaxLower/Raise は税の政策)。関係する政策の変更は見送り
- `economy_breakdown`: Tourism の収入45、Monument の支出2,280、Beautification の支出7,188、公共交通の支出38,172、Road 支出8,526
- `cargo`: 止まったトラック802(道の上296、敷地の中506。貨物センター28755が492)。品物がない店228(-1069,-770 付近に74、2206,729 付近に46、1004,300 付近に33)。原料がない工場24
- `list_building_types`(service=Monument): 解禁済みの名所は20種類。Official Park は 6×6、45,000、週128。StatueOfWealth は 8×8、25,000、週400(是正で再確認)。SeaWorld は 12×12、20,000、週320。ほかは 8×8 以上で、建設費は 20,000〜200,000
- `buildings_near`(Monument、半径9,000m): 名所6棟(SeaWorld 2、ScienceCenter 1、Winter Market 01 1、Countdown Clock 1、Fountain of LifeDeath 1、Plaza of Transference 1)
- `buildings_near`(abandoned=true、半径3,500m): 106棟(放棄・火事・死亡・品物がない店など)。候補の B、ほか3か所の確かめに使った
- `buildings_near`(半径60m、(2286,986)、(3388,-742)): 近くの建物と、道路の位置
- `map_layer`(attractiveness、街全体 n=9): 平均6、最大157(2575,1224)、最小0
- `map_layer`(attractiveness、A 周り、半径150m、n=3): 平均4、最大44(2286,822)
- `map_layer`(attractiveness、B 周り、半径150m、n=3): 平均14、最大126(2268,332)
- `zone_map`(中心 2400,400、半径350): 東部の商業区画の周りは建物で埋まっている。空いた四角は、多くが埋立地(Landfill Site)で、名所は置けない
- `zone_map`(中心 2600,250、半径250)と(中心 -1100,-500、半径450): 空きの多くは建物の裏か、建物で埋まっている
- `zone_summary`(grid 1000): 空き区画は東部(x 2500 前後)に多い。道に面した空きは商業の高層 156 と少ない。オフィスの空きは建物の裏
- `building_stats`(中心 2575,1224、半径400): 事務所 218 棟(レベル3 197)、商業の高層 44 棟、住宅の高層 9 棟、工業 52 棟
- `preview_bulldoze`(B、半径30、what=building、中心 2128,471): 壊す建物 3(5985、41519、44794)。失う働き口 19、家 0(是正で再確認)
- `test_place_building`(SeaWorld、2280,545 / 2530,555): 道路と事務所に重なり断られた
- `test_place_building`(Official Park、2600,300): 道路と高層住宅に重なり断られた
- `test_place_building`(SeaWorld、2128,471、assume 5985): 道路と店に重なり断られた。SeaWorld は 12×12 で、この場所には大きい
- `test_place_building`(SeaWorld、2176,256、assume 4171): 道路と複数の建物に重なり断られた
- `test_place_building`(Official Park、2680,140 / SeaWorld 2680,140 / StatueOfWealth 2680,140): 道路と医院に重なり断られた
- `test_place_building`(SeaWorld、1377,262、assume 101): 道路と事務所に重なり断られた
- `test_place_building`(SeaWorld、1856,-46、assume 8020 / Official Park、1856,-30、assume 8020、24649、35756): 道路と店に重なり断られた
- `test_place_building`(SeaWorld、564,-146、assume 6384): 道路と公園・歩道に重なり断られた
- `test_place_building`(Friendly Neighborhood、2286,986、assume 5266): 道路に重なり断られた(A は urban-1 に譲った)
- `test_place_building`(Official Park、2286,986、assume 5266): 道路に重なり断られた
- `test_place_building`(Official Park、2118,482、facing east、assume 5985、41519、44794): ok。入口は (2142, 482) の道路(2m)。費用 45,000(是正で再確認)
- `test_place_building`(Official Park、3388,-742、facing west、assume 2002): 道路に重なり断られた
- `test_place_building`(StatueOfWealth、-4862,1731、島B、是正で確認): ok。入口は (-4862, 1763)、道路なし(第8月までに島の道を引く)。費用 25,000
- `water_trace`(B 2118,482): 電気・水・下水が届く。街の水の容量 2,400,000 に対し使用 1,925,008、下水も同じ

## 判断の根拠

- 観光の担当の数字は、今いる観光客1,646、訪問139、Tourism 週45、attractiveness 平均6、名所6棟。目標との差が大きく、名所を増やすのは確かめやすい手
- B は、`test_place_building` が ok で、電気・水・下水も届く。壊す建物は `preview_bulldoze` で確かめた3棟で、失う働き口は19。働き口の目標(90,000)から見ると小さい
- 名所は1棟に絞った。A は住宅都市みどり局の urban-1 と場所が重なり、調整で譲った。局の名所の数は、第3月・第6月・第8月(島B)の計3棟を予定し、12か月後の名所は11棟の見込み
- 名所の効き目は、この街では確かめていない。局は B の効きを第2月に見てから、2棟目を決める
- 観光の入口(旅客の駅・港・空港)は0で、港湾空港局の担当。局は入口を港湾空港局に求め、案にはしない
- 品物がない店(228)は、観光客の消費を Tourism の収入に変えにくくする原因と見る。原因は貨物センターの詰まりと、店の周りの道の流れのどちらかで、まだ確かめていない。そこで調査を1件出す
- 案は1件。島Bの名所は第8月の段階に入れ、今月の案には入れない

## 捨てたもの

- 名所 A(2286, 972): 住宅都市みどり局の urban-1 と場所が重なるため、局の案からは外した(調整)
- 名所(SeaWorld、ScienceCenter、Stadium など、12×12 以上の大きい名所): 確かめた場所(市街の中心の空き)では置けなかった。大きい名所は、取り壊しを増やすので、今月は見送る
- 島Bの名所(StatueOfWealth): 第8月の段階。島の道と風力発電が第5月までにそろってから出す。今月は案にしない
- 島A、島C、埋立地D、空き地1〜5 への名所: 橋・電気・水・下水の工事が要り、今月は実行条件を確かめられない
- 政策(有効化・解除): 観光に効く政策は一覧にない。BigBusiness(週3,876)は既に有効。SmallBusiness(週315)は効き目が分からない。今月は見送る
- 品物の流れ(貨物センター28755の詰まり): 8-1 は港湾空港局の担当。局は求める形で長期計画に書き、案にはしない
