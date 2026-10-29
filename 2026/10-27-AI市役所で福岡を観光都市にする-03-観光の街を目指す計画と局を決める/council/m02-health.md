# m02 保健環境局の案

## 案1: 焼却場2267を止めて、住宅近くの汚染を減らす

### 施策

- 案の id: health-1
- 施策: 焼却場(Combustion Plant、id 2267、(3604,-30)、service Garbage)を止める。`set_building_active`(id=2267, active=false)。市の計画 4-3 脱炭素社会の汚染の印を下げる。
- 議決: 要らない(`set_building_active` は議決の種類に入らない)

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `set_building_active`(id=2267, active=false)。2. 2月末に `complaints`、`map_layer`(type=pollution, x=3600, z=-40, radius=150, n=5)、`services` で測る。3. 埋立地の容量は `buildings_near`(x=3300, z=200, radius=900, service=Garbage, limit=15) で見る。
- 設置条件の確認: 建設はない。2267 は `buildings_near`(x=3604, z=-30, radius=150) で、Combustion Plant、処理 60,000/週、reserve 353,033 / 400,000 を確認した。電気は `services` で capacity 2,366,800、used 1,713,776 の余裕がある。15MW を失った後の使用量は、実行後に `services` で確かめる。東の埋立地は 28130(22%)、29266(68%)、3565(82%) が空いている。
- 接続工事: 不要
- 予備候補: なし(止めるだけで、建て直しはしない)
- 中止する条件: 実行後、`services` の garbage.full が1以上、または `complaints` の Garbage が15を超えたら、`set_building_active`(id=2267, active=true) で戻す。電気の used が capacity の90%を超えたら戻す。

### 期待する効果

- 改善の見込み: 汚染の印の出ている住宅(675、4378、6720、9959 など)は、2267 の周り 150m 以内にあり、そこの汚染は 250〜255 と高い。止めれば、この周りの汚染が下がり、印が減ると予想する。
- 数値と期限: `complaints` の Pollution の印。今は 45 棟(出発点 32)。2050-02-28 の月末に、局の予測として 35 以下を見込む。確かな数字ではない。目標 15 以下は、工場群(3700〜3900、-250〜-650)の汚染が残るため、この手だけでは届かないと見る。
- 確認方法: `complaints`(Pollution の buildings 数と hotspot)、`map_layer`(type=pollution, x=3600, z=-40, radius=150, n=5)。今の値は平均 93、最大 255。同じ引数で比べる。
- 不確かな点: 印が減る量は見積もれない。東の埋立地が 2267 の分のごみを受けられるかは未確認(調査で見る)。電気の余裕は、15MW の分を引いても足りる見込みだが、実行後に確かめる。
- 試し: 試し。仮説: 2267 の汚染が、近くの住宅の汚染の印の主な原因で、止めると印が減る。測る数: `complaints` の Pollution の印の数、`map_layer` pollution(3600, -40, r150)。場所: 2267 の周り。基準: 印 45、平均 93。編成方針の分からないこと(3)「汚染の印が増えた原因」の一部を確かめる。

### 費用

- 建設費: 0
- 週の維持費の増え分: -1,440(減る。`list_building_types`(service=Garbage) の Combustion Plant の upkeepPerWeek 1,440)

### 戻せるか

戻せる。`set_building_active`(id=2267, active=true) で元に戻る。

### 前の月の答え合わせ

- m01-4(埋立地の入れ替え): 満杯の埋立地は 7 から 0 になった。当たり。ごみの印は 15 から 11 に減った。
- m01-5(木の試し): 汚染の平均は 159 から 161 で、下がらなかった。外れ。今月は木を続けず、この案の焼却場の手に替える。
- 1か月目の案の残りは、実行の結果を市長が書いた。今月は判定の対象にしない。

### 市の計画

- 当たる施策: 4-3 脱炭素社会(汚染の印)。副次的に 1-2 健やかで心豊かに暮らせる社会(体調の悪い市民が減る見込み)
- 編成方針の重点に当たるか: 当たる(重点3 4-3)

## 調査

- 調査: あり
- 問い: 焼却場 2267 を止めたあと、東の埋立地の容量が詰まらず、ごみの印が増えないか。
- 見る道具と引数: `buildings_near`(x=3300, z=200, radius=900, service="Garbage", limit=15)で東の埋立地の storage を、`services` で garbage.full の数を見る。
- いつ見るか: 見回り1, 見回り2, 月末
- 何が分かれば次の手が決まるか: 東の埋立地の storage が見回りごとに増え、満杯が出るなら、2267 を戻す、または埋立地を足す案を出す。満杯が出ず、ごみの印が 15 以下なら、止めたまま続ける。
- 担当の問題: 4-4 資源循環(ごみの印)、4-3 脱炭素社会

## 見たもの

- `city_info`: 人口 178,859、所持金 2,015,489、週の収支 +8,421(1月末)。来ない市民 0/0/0。
- `services`: 電気 capacity 2,366,800 / used 1,713,776。水と下水に余裕。garbage の full 0(45892 は 94% で Emptying)。deathcare の full 0。警察と医療に余裕。
- `citizens_summary`: 健康の平均 78、体調の悪い市民 2,248、失業 6,144(大卒 5,984)。
- `complaints`: 汚染 45(hotspot (3809,-273)、examples は 675、4378、6720、9959 など 2267 の近くの住宅)、ごみ 11(hotspot (-366,-1138))、火事 7(hotspot (3255,-805))、犯罪 2、品物がない店 222。
- `list_policies`: 有効は EducationBoost(週 7,940)と BigBusiness(週 3,872)。関係する政策: Recycling(費用 0、ごみ -15%、住宅税 -5%)、HeavyTrafficBan(費用 0、トラックの汚染と騒音を減らす。品物の運搬も止まる)、SmokeDetectors(週 57,754、火事向け)。汚染に直接効く費用 0 の政策は、HeavyTrafficBan だけ。
- `buildings_near`(x=3604, z=-30, radius=150): 2267 Combustion Plant(Garbage、Power Output 15MW、reserve 353,033 / 400,000、処理 60,000/週)。近くの住宅 675、4378、6720、9959 に Pollution の印。
- `buildings_near`(x=3300, z=200, radius=900, service=Garbage): 東の埋立地 28130(22%)、29266(68%)、3565(82%)。2267(88%)。
- `buildings_near`(x=3800, z=-300, radius=130): 工場群(BigFactory06、Mediumfactory、Sweatshop など)と事務所。風車 Advanced Wind Turbine 17521、25840、30414(z=-375)。
- `buildings_near`(x=3900, z=-520, radius=150): 工場と事務所、風車 4630、住宅 14175(3976,-555)に Pollution の印、埋立地 16551(3900,-575)。
- `map_layer`(type=pollution, x=3600, z=-100, radius=400, n=9): 2267 の周りが 250〜255、(3700〜3900, -300)が 250〜255、(3500〜3700, -500)が 240〜255。
- `map_layer`(type=pollution, x=3600, z=-40, radius=150, n=5): 平均 93、最大 255。
- `map_layer`(type=pollution, x=3900, z=-450, radius=200, n=5): 平均 133、最大 255。
- `map_layer`(type=wind, x=3600, z=-100, radius=600, n=7): 平均 65、最大 91(4200,-100)。
- `map_layer`(type=health, x=0, z=0, radius=3000, n=9): 平均 60、0〜299。届きの低い区域は(-750,-1500)付近の 39、(-750,-2250)付近の 16。
- `buildings_near`(x=-1000, z=-1585, radius=120, service=HealthCare): 診療所なし。
- `test_place_building`(Medical Clinic, x=-1000, z=-1585, facing=north): ok、cost 10,000、入口は segment 4589(距離 11)、取り壊し 46949(H3 4x4 Shop04、働き口 20)。
- `test_place_building`(Medical Clinic, x=-1040, z=-1515, facing=south): ok、cost 10,000、入口は segment 311(距離 11)、取り壊し 8228(Office03、働き口 27)と 41079(Shop13、働き口 15)。
- `list_building_types`(service=HealthCare): Medical Clinic は cost 10,000、upkeepPerWeek 400、capacity 100。
- `list_building_types`(service=Garbage): Landfill Site は cost 4,000、upkeep 160、capacity 8,000,000。Combustion Plant は cost 30,000、upkeep 1,440。
- `list_building_types`(service=Electricity): Advanced Wind Turbine は cost 12,000、upkeep 200、capacity 20,000(風で変わる)。風力を4基にすると建設費 48,000、週 800。

## 判断の根拠

2267 は発電所ではなく焼却場で、住宅の汚染の印の出ている 4 棟は、その 150m 以内にある。汚染の値も 250〜255 と高い。止めれば、住宅の汚染が下がると見込める。`set_building_active` は議決の種類に入らず、建設費も 0 で、週の維持費が 1,440 減る。戻すのも同じ道具でできる。案は 1 件にした。診療所は、2月の試しを済ませ、4月に健康が 79 未満か確かめてから置くと計画に書いてあるため、今月は案にしない。工場群の汚染は、働き口と 6-4・7-1 の目標に関わるので、この局の案にしない。

## 捨てたもの

- 風力4基(計画の候補A): 2267 は焼却場で発電所ではない。風で電気を替えても、焼却場の汚染は止まらない。
- 工場群(3700〜3900、-250〜-650)の汚染を減らす取り壊し: 働き口が減り、6-4・7-1 と経済の目標に当たる。取り壊しの議決も要るため、原因を調べてから案にする。
- 木を増やす(候補B): 190本で平均 159 から 161 に変わらなかった。効かない。
- Recycling 政策: ごみを 15% 減らす見込みだが、住宅税を 5% 下げる。週の収支は守る線 +3,000 に近づくため、今月は見送る。
- HeavyTrafficBan 政策: 汚染と騒音を減らす見込みだが、貨物トラックが止まり、品物がない店 222 を悪くする。今月は見送る。
- 診療所の案を今月出す: 健康は 78 で、4月に置く条件(79 未満)を満たすか確かめていない。試しは済んでいるので、4月に案を出す。
- 埋立地 45892 を戻す: 2月末も 94% で、空にしている途中。空になってから戻す。
