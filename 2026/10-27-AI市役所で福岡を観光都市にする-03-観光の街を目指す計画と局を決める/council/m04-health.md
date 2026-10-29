# m04 保健環境局の案

## 案1: 第1候補に診療所を1棟置く(放棄された商店を取り壊す)

### 施策

- 案の id: health-1
- 施策: 診療所(Medical Clinic)を (-1000, -1585) に、向き north で1棟置く。その前に、放棄された商店 46949(H3 4x4 Shop04)を取り壊す。
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `preview_bulldoze`(x -1000, z -1585, radius 20, what "building")で、壊す対象が 46949 だけ、働き0、家0と確かめる(確認済み)。
  2. 議決が通ったら `bulldoze`(x -1000, z -1585, radius 20, what "building")で 46949 を取り壊す。
  3. `place_building`(prefab "Medical Clinic", x -1000, z -1585, facing "north")で置く。置く前に `test_place_building` で同じ引数を試す(確認済み。入口 (-1000, -1569)、道路 segment 4589 の Basic Road、距離 11)。
- 設置条件の確認:
  - 敷地: `test_place_building`(assume なし)で ok。壊す対象は 46949 の1棟だけ(wouldDemolish 1、ids [46949])。
  - 放棄: `buildings_near`(x -1000, z -1585, radius 300, abandoned true)で、46949 が放棄された建物に入る(NoGoods、FatalProblem)。
  - 失うもの: `preview_bulldoze` で、働き0、家0。
  - 道路: 入口の道路は segment 4589(Basic Road、距離 11)。道を引く必要はない。
  - 電気・水・下水: Medical Clinic は3つとも要る。置いた後に `buildings_near` の grid で確かめる。
- 接続工事: 不要(入口の道路 segment 4589 が既にある)
- 予備候補: 確認済みの候補はなし。試した別の場所は、入口の道路がない(-1068, -1526)、または家を38戸失う(-1244, -1526)ので使わない。
- 中止する条件: 議決が否決されたら置かない。取り壊し後の `test_place_building` で入口の道路が消えていたら、置かず見送る。電気・水・下水が来ないときは、置いた後に報告する。

### 期待する効果

- 改善の見込み: 健康の平均(78)を上げる。第1候補の周りは医療の届きが薄い(`map_layer` health で、周りは約80〜90。最大254の尺度)。診療所の容量は 100 で、街全体の医療の使用は 1,760 / 5,000 と余裕があるが、局所の届きは薄い。
- 数値と期限: 健康の平均 78 → 目標80以上。効果を確かめる期限は8月(計画の第8月)。量は見積もれない(数値は見積もれない)。
- 確認方法: `citizens_summary` の健康の平均と病気の人数(今 1,761)、`map_layer`(type health、x -1000、z -1585、radius 300)の平均。今の値と同じ範囲で比べる。
- 不確かな点: 取り壊す商店は放棄されているため、働きと家の損失は0と見込む。診療所の効きが健康の平均に出るまで、数か月かかる可能性がある。
- 試し: なし

### 費用

- 建設費: 10,000(Medical Clinic。`list_building_types`)
- 週の維持費の増え分: 400(`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せない。取り壊した商店は戻らない。

### 前の月の答え合わせ

なし(3月は保健環境局の案なし)。3月の調査 s03-2 の結果は、「判断の根拠」にある。

### 市の計画

- 当たる施策: 1-2 健やかで心豊かに暮らせる社会
- 編成方針の重点に当たるか: 当たらない(重点は 5-1・5-2 観光、6-4・7-1 企業、6-3・8-1 交通。保健は計画の目標として担当する)

## 案2: 満杯の埋立地2つを取り壊して、同じ場所に建て直す

### 施策

- 案の id: health-2
- 施策: 満杯の埋立地 25692(738, -590)と 157(-1860, -1880)を取り壊し、ずらした位置に Landfill Site を1つずつ建て直す。
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `preview_bulldoze`(x 738, z -590, radius 12, what "building")で、壊す対象が 25692 だけ、働き0、家0と確かめる(確認済み)。
  2. 議決が通ったら `bulldoze`(x 738, z -590, radius 12, what "building")で 25692 を取り壊す。
  3. `place_building`(prefab "Landfill Site", x 745, z -600, angle 90)で1つ目を建てる。`test_place_building`(同じ引数、assume_removed_buildings [25692])で ok。入口は west、道路 segment 14535(Basic Road)距離 5。
  4. `preview_bulldoze`(x -1860, z -1880, radius 20, what "building")で、壊す対象が 157 だけと確かめる(実行時の確認)。続いて `bulldoze`(x -1860, z -1880, radius 20, what "building")で 157 を取り壊す。
  5. `place_building`(prefab "Landfill Site", x -1862, z -1880, facing "east")で2つ目を建てる。`test_place_building`(同じ引数、assume_removed_buildings [157])で ok。入口は east、道路 segment 31714(Basic Road)距離 2。
- 設置条件の確認:
  - 25692: `test_place_building`(x 745, z -600, angle 90, assume_removed [25692])で ok、wouldDemolish 0。電気・水・下水は要らない。`preview_bulldoze` で、働き0、家0。
  - 157: `test_place_building`(x -1862, z -1880, facing east, assume_removed [157])で ok、wouldDemolish 0、入口の道路 segment 31714 距離 2。`buildings_near` で、157 の jobs.total 0。
  - 元の位置(738, -590)と(-1860, -1880)に建て直すと ObjectCollision(道路 segment 8748、14535、31714、36741)で断られたため、少しずらした位置を使う。
- 接続工事: 不要(入口の道路 segment 14535 と 31714 が既にある)。
- 予備候補: なし(ずらした位置は、道路と重ならないことを確かめた。ほかの位置は未確認)。
- 中止する条件: 議決が否決されたら取り壊さない。取り壊し後の `test_place_building` が ok でなければ、その1か所は見送る。もう1か所は、そのまま進めてよい。
- 45892 との関係: 45892 は空にする途中(85%)なので、この案に入れない。

### 期待する効果

- 改善の見込み: 満杯の埋立地は、ごみを受けられないため、ごみの印を増やしている可能性がある。1月に満杯の埋立地6つを建て直したところ、ごみの印は 15 → 11 に減った(1月の当たり)。同じ手で、満杯の2つを空けると見込む。ごみの印が0になるとは見込まない。
- 数値と期限: `services` の garbage.full を 2 → 0(建て直した直後に確かめる)。ごみの印(`complaints` の Garbage)を 18 → 15以下、期限は5月末。量は見積もれない。
- 確認方法: `services`(garbage.full の数)と `complaints`(Garbage の印の数)。今の値は、garbage.full 2、ごみの印 18(4月)。
- 不確かな点: 取り壊すと、中にあるごみは失われる(各 8,000,000 が満杯)。1月の入れ替えでも同じだった。ごみの印の残りは、工場群の近く(3917, -456)の貨物の混みが原因の可能性もある。その場合は効きが小さい。
- 試し: なし

### 費用

- 建設費: 8,000(Landfill Site 4,000 × 2。`list_building_types`)
- 週の維持費の増え分: 320(160 × 2。`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せない。満杯のごみは取り壊しとともに失われ、建て直した埋立地も取り壊しの議案になる。

### 前の月の答え合わせ

なし(3月は保健環境局の案なし)。

### 市の計画

- 当たる施策: 4-4 資源循環
- 編成方針の重点に当たるか: 当たらない

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `city_info`: 人口 178,486、所持金 2,110,220、週の収支 +9,303(収入 347,484、支出 338,181)、幸福度 85、観光客 1,742(訪問 139)、来ない市民 0/0/0、dialog なし
- `citizens_summary`: 健康の平均 78、病気 1,761、体調の悪い人 2,066、失業 5,761(大卒 5,667)
- `complaints`: 汚染 35(hotspot (3952, -372)、19棟)、ごみ 18(hotspot (3917, -457)、9棟)、火事 8、死亡 38、品物がない店 235
- `services`: 埋立地の満杯 2(157、25692)、ごみの使用 83,458,885 / 160,000,000、医療 1,760 / 5,000、警察 369 / 980
- `list_policies`: policyExpensesPerWeek 10,980。SmokingBan は active=false、costPerWeek 0。Recycling は active=false、costPerWeek 0(税-5%の効きがある)。RecreationalUse は active=true、costPerWeek 0。SmallBusiness は active=true、315/週。Recycling は税-5%のため採らない(「捨てたもの」)
- `buildings_near`(x 2272, z -1115, radius 60): 45892 Landfill Site、Emptying。storage 6,860,000 / 8,000,000(85%)、ごみ収集車 19 / 19。3月の 94% から減っている
- `buildings_near`(x -1000, z -1585, radius 60): 商店 10962、39087、40739、46949 などが NoGoods。46949 は FatalProblem
- `buildings_near`(x -1000, z -1585, radius 300, abandoned true): 放棄された建物 7 件(商店)。46949 を含む
- `buildings_near`(service Garbage, problem LandfillFull, radius 6000): 満杯は 157(-1860, -1880)と 25692(738, -590)の2つ。どちらも 8,000,000 / 8,000,000、ごみ収集車 0 / 19
- `buildings_near`(service Garbage, radius 6000): 2267 Combustion Plant は貯蔵 251,468 / 400,000、処理 60,000 / 週、収集車 15 / 34(処理は動いている)
- `list_building_types`(service HealthCare): Medical Clinic 建設 10,000、週 400、容量 100、道路と電気・水・下水が要る
- `list_building_types`(service Garbage): Landfill Site 建設 4,000、週 160、容量 8,000,000、道路が要る
- `test_place_building`(Medical Clinic, -1000, -1585): ok。入口 (-1000, -1569)、道路 segment 4589(距離 11)、wouldDemolish 46949 の1棟、失う働き0、家0
- `test_place_building`(Medical Clinic, -60, -698, south): 不可(ObjectCollision、住宅 1346、6388 と道路 12674、16819)
- `test_place_building`(Medical Clinic, 2150, -1180, north): 不可(ObjectCollision、道路 22831、建物 3716、19164)
- `test_place_building`(Medical Clinic, 2040, -1180, north): 不可(ObjectCollision、道路 18099、建物 18295、28659)
- `test_place_building`(Medical Clinic, -1068, -1526, north, assume_removed [32019]): ok だが入口の道路が null。失う働き0、家0。使わない
- `test_place_building`(Medical Clinic, -1244, -1526, north, assume_removed [27721]): ok だが入口の道路が null。取り壊しで家38戸を失う。使わない
- `test_place_building`(Landfill Site, 738, -590, assume_removed [25692]): 不可(ObjectCollision、道路 8748、14535)
- `test_place_building`(Landfill Site, 745, -600, angle 90, assume_removed [25692]): ok。入口 west、道路 14535 距離 5、wouldDemolish 0
- `test_place_building`(Landfill Site, -1860, -1880, assume_removed [157]): 不可(ObjectCollision、道路 31714、36741)
- `test_place_building`(Landfill Site, -1900, -1880, angle 90, assume_removed [157]): ok だが入口の道路が null。使わない
- `test_place_building`(Landfill Site, -1862, -1880, facing east, assume_removed [157]): ok。入口 east、道路 31714 距離 2、wouldDemolish 0
- `preview_bulldoze`(x -1000, z -1585, radius 20, what building): 46949 の1棟、働き0、家0
- `preview_bulldoze`(x 738, z -590, radius 12, what building): 25692 の1棟、働き0、家0
- `map_layer`(type health, n 9): 平均 84、最大 254(2575, 1224)、最小 0(-2761, 1720)。北西と南東の隅は0。候補の周りは約80〜90
- `net_near`(x 1700, z -1250, radius 150, Road): 道路なし。候補にしない
- `net_near`(x -94, z -755, radius 150, Road): 道路 Large Road(-50,-725)など。ただし test_place_building で置けなかったため候補にしない
- `net_near`(x 2100, z -1300, radius 200, Road): Basic Road(z -1160)。ただし test_place_building で置けなかった

## 判断の根拠

- 健康の平均は 78 で、79未満の条件を満たす。計画の第4月の案で、第1候補(-1000, -1585)に1棟を置く。確認済みで、放棄された商店を取り壊すだけで、働きと家の損失は0(`preview_bulldoze`)。議決は取り壊しの1種類。
- 満杯の埋立地が 157 と 25692 の2つになった。計画にない変化なので、計画の変更に書いた。1月に満杯の入れ替えで当たった手と同じで、取り壊し後の建て直しは試しの道具で ok。費用は小さく、週の収支は +9,303 から約 +8,583 になるが、守る線 +3,000 の上で収まる。
- 3月の調査 s03-2 は、2267 の処理が動き、貯蔵が 333,750 → 251,468 と減ったことを示す。焼却場の手は、次の手として出さない。
- 汚染の印 35(目標15以下)は、工場群の原因が未確認のため、今月は案を出さない(計画の5〜7月)。
- 案は2件。今月の確認済みの手の数で決めた。確認できなかった候補(入口の道がない候補など)は入れない。

## 捨てたもの

- 政策 Recycling(税-5%、ごみ-15%): 税の減り(約 13,200 / 週)で、守る線の週の収支 +3,000 を、今の +9,303 から割り込むおそれがあるため。
- 政策 SmokingBan(費用0): 健康への効きが分からない。診療所と同じ月に入れると、健康の平均の変化の原因を分けられない。診療所の効きが出る8月以降に、試しとして検討する。
- 診療所の候補(-1068, -1526)と(-1244, -1526): 入口の道路がなく、(-1244, -1526)は家38戸を失う。調整12(入口の道路がある候補だけ)に従い、使わない。
- 診療所の候補(-60, -698)、(2150, -1180)、(2040, -1180): ObjectCollision で置けない。
- 45892 の active=false: まだ空になっていない(85%、emptying)。空になったら計画どおり行う。
- 2267 を止める案: ごみの印が15を超える(2月の経験)。
