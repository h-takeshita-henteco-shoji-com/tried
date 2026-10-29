# m01 住宅都市みどり局の案

## 案1: 放棄された店の跡に広場を置く(1850,-150)

### 施策

- 案の id: urban-1
- 施策: 放棄された店(id 14155、H3 3x2 Shop04)と、住んでいる高層住宅1棟(id 5113、住宅1)を取り壊し、その跡に Regular Plaza を (1850,-150) に東向きで置く。入口は既存の Small 4 Lane Road(segment 21007)につながる
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 置く前に `land_value`(x=1850, z=-150, radius=200)と `map_layer`(type=attractiveness、x=1850、z=-150、radius=200、n=5)で基準を測る(基準: 地価の平均 62、attractiveness の平均 19)
  2. `preview_bulldoze`(x=1862, z=-152, radius=22, what="building")で、壊す建物を再確認する。想定は 5113 と 14155 の2棟だけ
  3. 議決のあと `bulldoze`(x=1862, z=-152, radius=22, what="building")。道路は壊さない
  4. `test_place_building`(prefab="Regular Plaza", x=1850, z=-150, facing="east")で、壊れた後の状態を確かめる。想定は ok、入口の道路が segment 21007(距離2m)
  5. `place_building`(prefab="Regular Plaza", x=1850, z=-150, facing="east")。建設費は予算から払う
  6. `buildings_near`(x=1850, z=-150, radius=30)で、置いた広場の grid(electricity)を見る
- 設置条件の確認:
  - `list_building_types`(service=Beautification): Regular Plaza、5x5、建設費 2,500、週の維持費 32、道路と電気が要る
  - `test_place_building`(facing=east、assume_removed_buildings=[5113, 14155]): ok、cost 2500、入口の道路 segment 21007(距離2)、壊れる建物なし
  - `test_place_building`(assume_removed_buildings=[5113] だけ、または [14155] だけ): 両方が要る。どちらか一方だと、もう一方の建物にぶつかる
  - `preview_bulldoze`(x=1862, z=-152, radius=22, what="building"): 壊す建物は 5113 と 14155 の2棟。失う働き口 0、家 1(5113 の1家)。14155 は放棄された店で、失うものはない
  - `buildings_near`(x=1896, z=-136, radius=30): 隣の高層住宅3棟は electricity、water、sewage がすべて true。電気は隣の建物から届いている
- 接続工事: 不要(入口の道路は既存)
- 予備候補: なし(1850,-150 の広場だけが確認できた。ほかの候補は下の「捨てたもの」を参照)
- 中止する条件:
  - 議決が取り壊しを通らない
  - 直前の `preview_bulldoze` で、壊す建物が5113と14155の2棟より増えた(または、ほかの建物が含まれた)
  - 直前の `test_place_building` が断った(reasons、colliding を読んで、置けるかを確かめ直す)
  - 置いた後、`buildings_near` で広場の electricity が false(原因を確かめるまで、次の広場を置かない)

### 期待する効果

- 改善の見込み: 4-2 の Beautification の数を 81 から 82 に増やす。広場が近くの高層住宅の地価(4-1)を上げる見込みもあるが、量は見積もれない(数値は見積もれない)
- 数値と期限: 4-2 は `buildings_near`(service=Beautification)の数。今 81。置いた月の月末に 82 を確かめる。4-1 の判定は、2月に `land_value`(x=1850, z=-150, radius=200)の平均を、基準 62 と比べる(2以上の上がりで効きありとする)
- 確認方法: `land_value`(x=1850, z=-150, radius=200)、`map_layer`(type=attractiveness、x=1850、z=-150、radius=200、n=5)。置く前の基準と同じ条件で比べる
- 不確かな点: 広場1か所の地価と名所への効きは、量を見積もれない(数値は見積もれない)。政策の変更は、この案に含めない(RecreationalUse は経済観光文化局の担当)
- 試し: なし

### 費用

- 建設費: 2,500(`list_building_types` の Regular Plaza。`test_place_building` の cost と一致)
- 週の維持費の増え分: 32(`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せない。取り壊した建物は戻らない。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 4-2 花や緑による潤い(主)、4-1 都市と自然が調和したコンパクトなまち(副)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2 と 8-1、6-3。4-2 は捨てたものに入る。観光の名所の仮説は、経済観光文化局の政策案で測る)

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口 178,872、所持金 2,082,287、週の収入 342,140・支出 332,175、幸福度 85、観光客 1,646(visits 139)、需要 住23・商2・工60、来ない市民 0
- `buildings_near`(abandoned=true、x=1850、z=-150、radius=3000、brief): 放棄された建物 89棟。店の列(1856 付近)のほか、14155、19566、8020、14298、4109、4171、6384、5985 などを候補に見た
- `test_place_building`(Regular Plaza、(1850,-150)、facing east、assume_removed_buildings=[5113, 14155]): ok、cost 2500、入口の道路 segment 21007(距離2)、壊れる建物なし
- `test_place_building`(Regular Plaza、(1850,-46)、facing east、assume_removed_buildings=[8020]): ok。ただし壊れる建物に 16176(高層住宅、家 2)が含まれる
- `test_place_building`(Regular Plaza、(1850,-218)、assume_removed_buildings=[19566]): ok だが、壊れる建物に 2403、6115 が含まれ、働き口 35 を失う
- `test_place_building`(Regular Plaza、(1850,-758)、assume_removed_buildings=[14298]): ok だが、壊れる建物に 4808、24703 が含まれ、働き口 35 を失う
- `test_place_building`(Regular Plaza、(2168,-166)、assume_removed_buildings=[4109]): 断られた。Medium Road(segment 22521、33129)にぶつかる
- `test_place_building`(Regular Plaza、(2176,256)、assume_removed_buildings=[4171]): 断られた。Medium Road、Small 4 Lane Road(segment 4412、10893、13553、31201)にぶつかる
- `test_place_building`(Regular Plaza、(564,-146)、assume_removed_buildings=[6384]): 断られた。Basic Road(segment 13481、35986)にぶつかる
- `test_place_building`(Regular Plaza、(2128,470)、assume_removed_buildings=[5985]): 断られた。Small 4 Lane Road、Basic Road(segment 6523、7469)にぶつかる
- `land_value`(x=1850, z=-150, radius=200): 平均 62(最小 36、最大 80)。街の平均 52。広場を置く前の基準
- `list_building_types`(service=Beautification): Regular Plaza 5x5、建設費 2,500、週 32。Regular Playground 5x5、建設費 1,250、週 24。Regular Park 9x8、建設費 1,000、週 8。Expensive Plaza 5x7、12,000、週 120。道路と電気が要る
- `list_policies`: 有効 EducationBoost(週 7,940)、BigBusiness(週 3,876)。RecreationalUse は active=false、costPerWeek=0(経済観光文化局の担当。この案では使わない)。HighTechHousing は無効で週 20,248

## 判断の根拠

- 4-2 の Beautification は 81 で、目標 100 まで 19 足りない。街の中は詰まっており、道路に面した空きはほとんどない。放棄された建物を壊して置く手が、実行できる数少ない形だった
- 案1は、取り壊しが2棟(放棄1棟、住宅1棟)で、失う働き口は 0、家は 1。`test_place_building` が、入口の道路を確かめ、置けると返した
- 案を1件だけにした。政策の変更(RecreationalUse)は、局をまたぐ調整Aのとおり経済観光文化局が持つ。局は attractiveness と地価を同じ範囲で測るだけにする
- 広場の候補は、今月の確認で1件(1850,-150)だけが、取り壊しの損失なしで通った。残りの候補は、道路との衝突か働き口・家の損失で断られた。毎月の確認数は計画に書く

## 捨てたもの

- 名所型 Expensive Plaza(2575,1224 付近): 最大の名所の地点に置く場所がない。Regular Plaza(2574,1262)は、事務所 12349 と道路 segment 7056 にぶつかり断られた。取り壊しの対象を増やすと、働き口を失う
- 放棄された店の候補の残り(4109、4171、6384、5985): 道路の中心線と当たるため、今月は断られた。位置と向きを変えて試し直すのは、次の月に計画の中で行う
- 19566、14298、8020: 壊れる建物に、働き口 35 を失う店(19566、14298)や、家 2 を失う住宅(8020)が含まれる。失うものを増やすため、今月は見送る
- 南の空き地(-520,-520)の広場: `test_place_building` は、入口の道路が null。道路 z=-440 から引く道は、オフィス2棟(id 9325、33018)を壊す必要がある。失う働き口を増やすので、今月は見送る
- 木の植栽による地価の手: 効き目の量は見積もれない。事業3として3月以降に試す。今月は案にしない
- 公園の数を、装飾の駐車場(Decoration Concrete Parking Lot、1,000)で増やす手: 4-2 の数は増えるが、緑による潤いの施策の中身に合わない。出さない
- 4-1 の高密度住宅の地価を上げる政策(HighTechHousing 週 20,248): 週の収支の守る線を割るおそれがある。今月は出さない
