# m05 保健環境局の案

## 施策

- 施策: ごみの印の集まる西の工場街に、地区だけの Recycling(ごみ -15%)をかける(試し)。`paint_district` で地区「RecycleWest」を塗り、`set_district_policy` で Recycling を有効にする。街全体にはかけない
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `list_districts()` で「RecycleWest」がまだ無いこと、塗る場所が HighTech(481, -323)・Hakata(299, 49)と重ならないことを見る
  2. `paint_district(x=-2450, z=-650, radius=150, name="RecycleWest")`
  3. `paint_district(x=-2450, z=-500, radius=150, name="RecycleWest")`
  4. `paint_district(x=-2450, z=-350, radius=150, name="RecycleWest")`
  5. `paint_district(x=-2450, z=-200, radius=150, name="RecycleWest")`
  6. `paint_district(x=-2450, z=-50, radius=150, name="RecycleWest")`
  7. `set_district_policy(district="RecycleWest", name="Recycling", active=True)`
  8. `list_districts()` で RecycleWest の policies に Recycling が入ったことと、`list_policies` の policyExpensesPerWeek(今 10,526)が増えていないかを見る
- 設置条件の確認:
  - 場所: `zone_map(x=-2393, z=-361, radius=500)` で、x -2560〜-2300 に工場(黄)と事務所(水色)が南北に並ぶ。円5つで、ごみの印の工場24棟中22棟が入る見込み。円の中心から印の工場までの距離を手で計算した(例: 8196 (-2380,-194) は (-2450,-200) から約70m、1453 (-2384,-666) は (-2450,-650) から約68m、15294 (-2516,-22) は (-2450,-50) から約72m)
  - 既存の地区: `list_districts` は HighTech と Hakata の2つだけ。HighTech は中心 (481, -323)で、ここから約2.9km離れている
  - 政策: `list_policies` で Recycling は active=false、costPerWeek 0(直接の費用なし。住宅の税収 -5%、ごみ -15%)
  - 道具の引数: `tool-reference.md` の paint_district(x, z, radius, name, erase)と set_district_policy(district, name, active)で確かめた
  - 円の中の住宅: `building_stats(x=-2393, z=-361, radius=400)` で高密度住宅は77棟・家997。街全体の住宅の税収 260,459 に比べて -5% の影響は数百以下と見る(数値は見積もりで未測定)
  - 地区の塗りは地面と区画に触れず、建物と道路は変えない
- 接続工事: 不要
- 予備候補: 円5つのうち paint_district が断られた円は飛ばし、残りの円だけで進める。予備の場所はなし
- 中止する条件: `list_districts` に RecycleWest が既にある、または既存の地区と重なると返った場合は、名前を「RecycleWest2」にして1回だけ試す。set_district_policy が断られたら、塗った地区は `paint_district(erase=True)` で戻して見送る。`list_policies` の Recycling の costPerWeek が 0 でなくなっていたら見送る

## 期待する効果

- 改善の見込み: ごみの印の集まる区画(-2393, -261)の印の建物は、受け入れ先の満杯と収集車の不足で車が回れず溜まっている。Recycling でその区画のごみの出る量を15%減らせば、同じ収集量でも印の出る建物が減ると予想する(局の予測。ゲーム内の効果は未確認)
- 数値と期限: `buildings_near(x=-2393, z=-261, radius=500, problem="Garbage", limit=60)` の total が今 25。予想は 15〜20 に減る(範囲は根拠が弱い)。期限は月末(30日目)。比べる街全体の印 132 のうち地区の外の107が増えるかも見る
- 確認方法: 見回り1・2・月末に上の `buildings_near` を同じ引数で呼び total を比べる。`complaints` の Garbage の街全体の数を参考にする。`economy_breakdown` の Residential の収入 260,459 が 1,000 以上減っていないかも見る
- 不確かな点: Recycling が建物のごみの出る量に効くか、印は量で付くのか(収集の遅れで付くのか)は、確認していない。満杯の埋立地10と焼却場の車34/34が変わらないので、15%では足りない恐れがある。印が 25 → 23以上なら効かないと見る
- 試し: 仮説は、地区だけの Recycling でごみの出る量が15%減り、収集が追いつかない工場街のごみの印が減る。測る数は `buildings_near(x=-2393, z=-261, radius=500, problem="Garbage", limit=60)` の total と `complaints` の Garbage。場所は (-2450, -350) を中心にした南北約700mの工場街。基準は total 25、街全体 132。編成方針の「分からないこと」の「ごみの印が増え続け、集まる場所が毎月移る原因」に当たる

これは局の予測です。ゲームの効果の正解を取得しません。

## 調査

- 調査: あり
- 問い: 新しい埋立地37856 が30日で 1% しか溜まらないのは、車が渋滞で戻れないためか、回る範囲にごみが少ないためか
- 見る道具と引数: `vehicles_stuck(kind="garbage", building=37856, limit=20)`、`buildings_near(x=-1862, z=-2000, radius=50, service="Garbage")`、`traffic(x=-1862, z=-2000, radius=300)`
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: 車の多くが Congestion や WaitingPath なら、道の詰まりの手当て(来月、道への案)を出す。車が OnRoad で動き、blocked 0 で storage だけが増えないなら、範囲のごみが少ないので、埋立地を足す手はやめて Recycling の広げ方を考える
- 担当の問題: 4-4 資源循環

## 費用

- 建設費: 0
- 週の維持費の増え分: 0(`list_policies` の Recycling は costPerWeek 0。地区の住宅の税収の -5% は費用でなく収入の減り。数百以下と見る)

## 戻せるか

戻せる。`set_district_policy(name="Recycling", active=False)` と `paint_district(erase=True)` で元に戻る。

## 前の月の答え合わせ

- m04-1(埋立地37856と道80mを足す、試し): 外れ。容量 160M → 168M は当たりだが、ごみの印は 74 → 132(予想60以下)、満杯は 8 → 10。今月の `buildings_near(service="Garbage")` で 37856 は 1%(80,000)・車 19 / 19 のまま。受け入れ先を足しても、印の集まる区画は工場街に移っただけだった。今月は受け入れ先を足さず、出るごみの量を減らす手に替えた
- s04-3(汚染の印の集まりの原因、調査): 分かったことがある。255前後の点は、(3604, -30)の焼却場(Combustion Plant 2267、ごみの処理 56,160/週・発電 14MW)の周りと、(3490〜3850, -500〜-690)の工場街と、x=4223 の工場の並びに当たる(今月の `buildings_near` と `map_layer(pollution, x=3604, z=-30, radius=300)` で確認)。汚染の印の家は、この3つの近くの低密度の住宅。ただし、焼却場を壊すと働き口0・家0・停電0だが、ごみの処理が減って4-4が悪化するので壊さない(`preview_bulldoze` で targets 1、lost 0 / 0、停電0)。工場街の汚染は、工場を壊すと働き口が減り公約1と衝突する。次の手は、汚染の印の家の周りに公園や木で地価を保つ手か、保留
- 前の月に採られた他の案: なし

## 市の計画

- 当たる施策: 4-4 資源循環
- 編成方針の重点に当たるか: 当たる(重点2)

## 見たもの

- `citizens_summary`: 住民 177,746、健康77(目標80)、体調が悪い 2,085、badHealth 2,518
- `complaints`: 印の建物450。ごみ132((-2393, -261) に27)、汚染39((3883, -299) に23)、死者34、騒音9
- `list_policies`: Recycling(有効でない、週の費用0。住宅の税収 -5%、ごみ -15%)、PetBan・SmokingBan・RecreationalUse・HeavyTrafficBan(いずれも有効でない、費用0)、EducationBoost(有効、7,940)、BigBusiness(有効、3,820)、PowerSaving・WaterSaving(有効でない、58,363)、SmokeDetectors(有効でない、57,800)、IndustrySpace(有効でない、4,815)、HighTechHousing(有効でない、20,264。HighTech 地区では地区の政策に入っている)、政策の支出 10,526。ごみと汚染に関係するのは Recycling。汚染そのものを下げる政策は見当たらない
- `services`: ごみ 131,951,262 / 168,000,000、満杯10(157、16914、19182、23032、25590、25692、25826、29270、45892、48698)、医療 2,089 / 5,000、葬祭 13,389 / 24,000
- `buildings_near`(service=Garbage, 半径6000): 28棟。埋立地の満杯10、焼却場7棟(車はどれも 30〜34 / 34)、新設37856 は 1%・車 19 / 19。(-2393, -261)の近くで満杯の 48698(-2761, -300)は車 0 / 19
- `buildings_near`(x=-2393, z=-261, radius=500, problem="Garbage"): 25棟。工場 20棟、診療所 2、高層住宅 4、葬祭1
- `buildings_near`(x=3623, z=-583, radius=250)と(x=3623, z=-30, radius=200): 汚染の元は焼却場2267 と工場街
- `map_layer`(pollution, x=3604, z=-30, radius=300, n=13): 255の点は焼却場2267 の周り(x 3454〜3754, z -180〜120)と、工場街(x 3604〜3904, z -330 の南)
- `zone_map`(x=3800, z=-350, radius=600): 工場(黄)と住宅(緑)が x=4000〜4250 で隣り合う
- `zone_map`(x=-2393, z=-361, radius=500): 工場と事務所の街区。印の工場がある
- `building_stats`(x=-2393, z=-361, radius=400): 高密度住宅77棟・家997、工場87棟(うち放棄2)、事務所274棟
- `economy_breakdown`: Residential の収入 260,459、ごみの支出 20,160、政策の支出 10,526
- `preview_bulldoze`(x=3604, z=-30, radius=10, building): 焼却場2267 の1棟、lost 0 / 0、停電0、modelAgreement 1.0
- `list_districts`: HighTech(126)と Hakata(127)の2つ
- `list_building_types`(Electricity): 発電所の一覧(今月は使わない)
- `buildings_near`(service=Electricity, 半径6000): 発電所と風車 64棟

## 判断の根拠

ごみの印は 74 → 132 に増え、満杯の埋立地は10になった。受け入れ先を足しても効かなかったので(m04-1)、今月は出る量を減らす手にした。Recycling は街全体にかけると住宅の税収の -5%(約 -13,000/週)で黒字 +18,289 をほぼ使うため、印の集まる工場街の地区だけにかける。工場街の住宅は少ないので、税収の減りは小さい。
汚染は、元が焼却場と工場街と分かったが、壊すと4-4・公約1が悪くなり、有効な手がない。今月は案にせず、見つかったことを記録する。

## 捨てたもの

- 焼却場2267 の取り壊し(取り壊し): 汚染の印の家の近くの最大の元だが、ごみの処理 56,160/週と発電 14MW を失い、ごみの印が増える。議決も戻せない。4-3 と 4-4 が衝突するので出さない
- Recycling を街全体にかける: 住宅の税収が約 -5% で、週の収支 +18,289 に対して大きい(公約3の黒字を守る線に近づく)。地区の試しで効きを見てから
- 埋立地や焼却場の追加: m04-1 で効かなかった。費用が大きい
- 公園・木で汚染の印の家の地価を保つ手: 住宅都市みどり局の担当と重なり、効き目が分からない
- 病院を足す案: 医療 2,089 / 5,000 で足りている。健康77は汚染と関係が深く、原因の対策が先
