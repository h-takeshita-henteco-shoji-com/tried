# m05 道路下水道局の案

## 案1: 島Bに橋と風力と送電線を引く

### 施策

- 案の id: roads-1
- 施策: 島Bの道を本土の道につなぐ橋(Basic Road、約2.4km、28区間が橋)、島の風力(Wind Turbine、(-4660,1440))、名所の電気の送電線(Power Line、(-4655,1462)→(-4650,1500))を引く。島の名所の材料。5-1、5-2 観光(島Bと空き地を含む)
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building`: prefab "Wind Turbine"、x -4660、z 1440、facing "north"、pay true(建設費 6,000、週 80)
  2. `build_line`: prefab "Power Line"、points [[-4655,1462],[-4650,1500]]、pay true(建設費 100)。両端は風力と名所(第8月に置く StatueOfWealth)の敷地に入れる
  3. `build_line`: prefab "Basic Road"、points [[-2720,100],[-4500,1700]]、pay true(建設費 38,680)。始点は本土の交差点 node 31642(-2720,100)、終点は島の道の端 node 30414(-4500,1700)につなぐ
- 設置条件の確認:
  - 風力: `test_place_building`(Wind Turbine, -4660, 1440, facing north)ok。wouldDemolish 0、needsRoad false(入口の道は不要)。
  - 送電線: `test_build_line`(Power Line, [[-4655,1462],[-4650,1500]])ok。segments 1、cost 100、overlaps なし。両端が敷地に入るかは、建てたあと `buildings_near`(x -4650、z 1480、radius 80)で grid の electricity を確かめる。
  - 橋: `test_build_line`(Basic Road, [[-2720,100],[-4500,1700]])ok。segments 30、bridgeSegments 28、cost 38,680、enoughMoney true、overlaps なし。始点は `junction_info`(-2720,100)で node 31642(Medium Road と Basic Road の交差点)。終点は `net_near`(-4600,1600,r300)の node 30414 と同じ座標。
  - 名所の位置(経済観光文化局へ渡す用): `test_place_building`(StatueOfWealth, -4650, 1512, north)ok。entrance road 13902(距離 4.8)。(-4640,1520) は `test_place_building` で road 13902 とぶつかり断られた。
  - 島の高さ: `height_at`(-4560,1450)は ground 58.1。風力の置き場所の高さは問題なし。
- 接続工事: 橋の両端がつながるかは、引いたあと `net_near`(-2720,100、r100)と `net_near`(-4500,1700、r50)で確かめる。送電線は、風力の追加で島の電気網が風力を中心に作られる。本土とはつながない。費用は上の建設費に含む。
- 予備候補: なし(主案が試しで通った)。橋の起点を (-2610,215) に替える案は、公園 27141(Expensive Park)にぶつかるので使わない。
- 中止する条件: 実行の時点で `test_build_line` が断られたら、橋を引かない(風力と送電線だけ先に引く)。風力の `test_place_building` が断られたら、風力と送電線を引かない。

### 期待する効果

- 改善の見込み: 島Bに道・電気が通り、経済観光文化局が第8月に名所を置ける状態になる。名所が置かれると、観光の入口が増えて、観光客と Tourism の収入が上がると見込む(局の予測。政策だけでは動かなかった前例がある)。
- 数値と期限: 今の値(5/1): 島の道 7区間、島の建物 0、名所 8棟(島は0)、Tourism 週 24。期限は第8月末。その時点の島の名所の数と、島の電気が来ているかを見る。Tourism の数値の予想は見積もれない。
- 確認方法: `net_near`(x -4600、z 1600、r300)で橋と道の区間数。`buildings_near`(x -4650、z 1512、r100)で名所の grid の electricity(第8月)。`economy_breakdown` で、Basic Road Bridge と Wind Turbine の週の維持費の増え。
- 不確かな点: 橋の週の維持費は、単価(Basic Road Bridge 約134/km/週、5/1 の実測)から約320と計算した。建てた後の `economy_breakdown` で確かめる。風力の出力は風で変わる(0〜8,000)。名所の電気の量は未確認。経済観光文化局の名所が置けるかは、この案の範囲外。
- 試し: なし

### 費用

- 建設費: 44,780(橋 38,680、風力 6,000、送電線 100)。`test_build_line` と `test_place_building` の値
- 週の維持費の増え: 約400(風力 80、橋 約320、送電線 約2)。実行後の `economy_breakdown` で確かめる
- 守る線: 週の収支 10,614 → 約 10,200(+3,000 以上)。所持金 2,111,160 → 約 2,066,000(1,874,000 以上)。建設費の累計 約 192,000(上限 350,000 以内)

### 戻せるか

戻せる。建てたものは、あとで取り壊せる(取り壊しは議決が要る)。

### 前の月の答え合わせ

- 前の月(m04)の答え合わせ: m04-roads-3(空き地3の道と送電線)は当たり。道5区間、送電線の始点 node 4380(690,1640)が segment 36842 につながることを、今月の `net_near`(690,1640、r40)で確かめた。前の月の「始点が none」は、つながっていた。島の案とは別の場所。

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる(重点1: 5-1・5-2 観光、島Bと空き地を含む)

## 案2: 交差点(2700,330)に信号を付ける

### 施策

- 案の id: roads-2
- 施策: 交差点 node 9244(2700,330)に信号を付ける(`set_traffic_lights` x 2700、z 330、active true)。3本の Small 4 Lane Road が交わる。6-3
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `set_traffic_lights`(x 2700、z 330、active true)を1回。費用 0。
- 設置条件の確認: `junction_info`(2700,330)で、trafficLights false、customLights false、canEnableLights true。道 3本(segment 19421、4818、2093)すべて cars true。
- 接続工事: 不要
- 予備候補: なし(対象は1か所で、確認済み)
- 中止する条件: 実行前に `junction_info`(2700,330)で canEnableLights が false、または trafficLights が既に true なら、見送る。

### 期待する効果

- 改善の見込み: 止まった車が多い(2703,309)周りは、交差点から出る車が詰まっている(blocked 59。周りの 21 と 16 を足すと 96)。同じ型の信号は、過去に止まった車を減らした(1月 m01-7 は 91→64、2月 m02-2 は 159→41、4月 m04-2 は 254→92)。この交差点にも効くと予想する(局の予測)。
- 数値と期限: 今の値(5/1、`traffic` x 2703、z 309、r 250): blocked 96、congestion 92、cars 163、flow 54(街全体は 54)。予想は第6月末までに blocked 40〜60(確かな数字ではない)。期限は第6月末の月末。
- 確認方法: `traffic`(x 2703、z 309、radius 250)の blocked と congestion を、同じ引数で見回り1・見回り2・月末に測る。街全体の flow(`traffic` 引数なし)も見る。
- 不確かな点: 信号の効きは、3本の道の交通量の偏りによる。前の3例は効いたが、この交差点の効きの量は見積もれない。街全体の流れ(54%)はこの1か所では大きく動かないと見込む(数値は見積もれない)。
- 試し: なし(前の3例で、同じ型の信号の効きは確認済み)

### 費用

- 建設費: 0(信号は建設費 0 と実測。m02-2、m04-2 と同じ)
- 週の維持費の増え: 未確認。月末の `economy_breakdown` で確かめる

### 戻せるか

戻せる。`set_traffic_lights`(active false)で外せる。取り壊しの議決は要らない。

### 前の月の答え合わせ

- 前の月(m04)の答え合わせ: m04-roads-2(東の交差点2か所の信号)は当たり。予想は blocked 254→150〜200。結果は 92(`traffic` x 2050、z 200、r 400)。m04-roads-1(z=-1010 の4車線化)は小さく当たり(blocked 14→11)。
- 今月の見たもの: 残った blocked 86 の集まり(1694,93)は、東の信号(1770,100)と西の信号(1560,100)の間の道にある。今回は信号を足さず、調査で原因を見る。

### 市の計画

- 当たる施策: 6-3 交通の流れ
- 編成方針の重点に当たるか: 当たる(重点2: 6-3 交通)

## 調査

- 調査: あり
- 問い: (1694,93) 付近の止まり(blocked 86)は、両端の信号の待ちが伸びた列か、道幅の詰まりか。
- 見る道具と引数: `traffic`(x 1694、z 93、radius 200、limit 5)、`traffic`(x 1560、z 100、radius 150、limit 5)
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 西の信号(1560,100)の周りでも blocked が20以上で、列が伸びていれば、西側の道が詰まりの根。西側の道は学校(1226)と車庫(30483)に当たるので、取り壊しの案を議決に出す前に、学校の影響を `preview_bulldoze` で確かめる。西の blocked が低く、(1694,93) だけ高いなら、道幅(Medium Road)の詰まり。その場合は、流れを変える手(一方通行の見直しなど)を次に調べる。
- 担当の問題: 6-3 交通の流れ

## 見たもの

- `city_info`: 人口 178,380、所持金 2,111,160、週の収支 +10,614(収入 345,801、支出 335,187)、観光客 1,811(訪問 138)、来ない市民 0/0/0
- `traffic`(街全体、x・z 指定なし): flow 54、cars 7,570、blocked 889、congestion 2,426。blockedSpots の上位は (1694,93) 86、(2703,309) 59、(3316,-261) 35
- `traffic`(x 2703、z 309、r 250): flow 54、cars 163、blocked 96、congestion 92
- `traffic`(x 1694、z 93、r 200): flow 54、blocked 133、congestion 130。blockedSpots (1694,93) 86、(1559,83) 20
- `list_policies`: 有効は EducationBoost(7,940)、BigBusiness(3,908)、SmallBusiness(311)。政策の週の費用の合計は 10,960。交通に関係する政策は HeavyTrafficBan(費用 0)、FreeTransport(費用 0、運賃の収入 0)。どちらも案にしない(捨てたものを見る)
- `economy_breakdown`: Road 維持費 8,623(週)。Basic Road Bridge 1.5km で 201.6/週(単価 約134/km/週)。Wind Turbine の週の維持費は 80
- `net_near`(x -4600、z 1600、r 300、Road): 島の道 7区間。(-4500,1700) node 30414 と (-4600,1400) node 29429 が未接続の端
- `net_near`(x -2720、z 215、r 150): (-2720,215) に道の端はない。近くの道は (-2720,100) node 31642
- `net_near`(x -4000、z 800、r 1200、Road): 島の道7区間だけ(本土の道は半径の外)
- `net_near`(x 690、z 1640、r 40、Electricity): 空き地3の送電線 segment 36842 が node 4380(690,1640)につながる
- `list_building_types`(Electricity): Wind Turbine 建設費 6,000、週 80、needsRoad false、needs なし
- `list_building_types`(Monument): StatueOfWealth 建設費 25,000、週 400、needsRoad true、needs electricity true、water false、sewage false
- `zone_map`(x -4600、z 1700、r 400)、`zone_map`(x -3600、z 900、r 1300): 島Bは空き地(unzoned)。島の道は細い線
- `buildings_near`(x -4600、z 1600、r 300、brief): 建物 0。島に建物はない
- `buildings_near`(x -4640、z 1520、r 120、brief): 建物 0
- `test_build_line`(Basic Road、[[-2720,215],[-4500,1700]]): ok、segments 29、bridgeSegments 29、cost 39,540、overlaps なし(旧案の起点。(-2720,215) には道の端がない)
- `test_build_line`(Basic Road、[[-2610,215],[-4500,1700]]): ok false、overlaps Expensive Park 27141(id 27141)
- `test_build_line`(Basic Road、[[-2720,100],[-4500,1700]]): ok、segments 30、bridgeSegments 28、cost 38,680、overlaps なし
- `test_build_line`(Power Line、[[-4655,1462],[-4650,1500]]): ok、segments 1、cost 100、overlaps なし
- `test_place_building`(Wind Turbine、-4660、1440、facing north): ok、cost 6,000、wouldDemolish 0、needsRoad false
- `test_place_building`(StatueOfWealth、-4640、1520、north): ok false、ObjectCollision with segment 13902
- `test_place_building`(StatueOfWealth、-4650、1512、north): ok、cost 25,000、entrance road 13902(距離 4.8)
- `junction_info`(-2610,215): node 25421、道 3本、canEnableLights true(旧案の起点。使わない)
- `junction_info`(-2720,100): node 31642、Medium Road と Basic Road、canEnableLights true
- `junction_info`(2700,330): node 9244、trafficLights false、canEnableLights true、道 3本(Small 4 Lane Road)
- `junction_info`(1770,100): node 4718、trafficLights true(既に信号あり)
- `junction_info`(1560,100): node 24441、trafficLights true(既に信号あり)
- `junction_info`(1694,93)、(1730,100): 40m以内に交差点なし
- `test_upgrade_road`(Large Road、[[1770,100],[1560,100]]): matched 3、upgraded 1、skipped 2(segment 109 は学校 1226 と車庫 30483 にぶつかる。segment 3239 は学校 1226 の取り壊しが要る)
- `net_reach`(x -4600、z 1550、r 400): 島の道 7区間は、来られない・出られない。島は本土とつながっていない(橋が必要)
- `height_at`(-4560, 1450): ground 58.1、water 58.1

## 判断の根拠

- 5月の予定は「島の橋・風力・送電線」(計画の事業2)。島の道(7区間)は引いてあり、本土とはつながっていない。橋の試しが通った(38,680、overlaps なし)ので、案1にした。島の名所は経済観光文化局の材料で、観光の入口の手(5-1、5-2)に効く。
- 名所の位置は、調整9の (-4640,1520) が道 13902 とぶつかるので、試しで通った (-4650,1512) を経済観光文化局に求める。
- 案2は、6-3 の blocked が多い交差点に信号を足す計画どおりの手。前の3例で効いた型で、建設費 0。(1694,93) の集まりは、既存の信号の間にあり、道幅を広げる手は学校にぶつかるので、案にせず調査にした。
- 案は2件(案1 観光の材料、案2 交通)。調査は1件。実行できる手は2件に絞れた。

## 捨てたもの

- 1770→1560 の4車線化(Large Road): 学校 1226 と車庫 30483 にぶつかる。学校の取り壊しは、教育の定員(2-3)を下げるため、見送る。調査 1件の結果で判断する。
- 橋の起点 (-2720,215): 道の端がない。(-2720,100) に替えた。
- 橋の起点 (-2610,215): 公園 27141(Expensive Park、104×96)にぶつかる。公園を壊すと 4-2 の数字(81→100)に逆に効くため、見送る。
- 島の送電線を本土へつなぐ案: 前の月(m02-1)に、電線が道 14667 とぶつかって断られた。島の中で風力から名所まで引く案に替えた。
- 水道管(5,800): StatueOfWealth は水を要らない。今月は引かない。
- HeavyTrafficBan(政策、費用 0): トラックを締め出すと、貨物の止まりは減るが、品物がない店 239、原料がない工場 33 が増える恐れがある(経済観光文化局の数字)。案にしない。
- FreeTransport(政策、費用 0): 運賃の収入が 0 になり、バスの収入 5,470 を失う。案にしない。
- 1694付近の道幅の広げ: 学校と車庫にぶつかる。調査で原因を見てから出す。
- 旅客の駅への道・水・電気(事業3): 港湾空港局の場所が届いていないので、今月は試さない。
