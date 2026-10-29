# m18 住宅都市みどり局の案

## 案1: 道に面した空き(1795,250)に公園 JapaneseGarden を1つ置く

### 施策

- 案の id: urban-1
- 施策: 道に面した空きに JapaneseGarden を1棟(座標 (1795, 250)、向き west)。4-2 の公園を 92 から 93 へ増やす。長期計画の 18 月の予定どおり
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: (1) `place_building` prefab=JapaneseGarden、x=1795、z=250、facing=west(angleUsed は 90)、pay=true。(2) 置いたあと、`buildings_near`(x 1795、z 250、r 30、brief)で建ったことを確かめる。道路をつなぐ工事はない(入口は既存の道路 16524 に面する)
- 設置条件の確認:
  - `test_place_building`(prefab JapaneseGarden、x 1795、z 250、facing west)を2回通した。ok=true、placed=false。cost 2,500、enoughMoney=true。entrance は (1779, 250)、road は segment 16524(Basic Road、距離 1)。wouldDemolish は 0 件、lostByDemolish は 働き口 0・家 0。
  - 電気: `map_layer` electricity_service(x 1795、z 250、r 40、n 3)で 9点とも 1。
  - 水: `map_layer` water_service(同じ範囲)で 9点とも 1。sewage は needs に含まれない(needs: electricity true、water true、sewage false)。
  - 重なり: 試しの道具が ObjectCollision を返さなかった。近くの 31332 JapaneseGarden(1820,300)とは重ならない位置。
- 接続工事: 不要
- 予備候補: なし。下の「捨てたもの」の候補は、どれも失うもの(働き口・家)があるか、置けなかった。予備には使わない
- 中止する条件: 実行前に `test_place_building`(同じ引数)を再度通す。ok=false になる、wouldDemolish に建物が出る、または entrance.road が null になったら、置かずに見送る。その場合は案なしの扱いにし、予備はない

### 期待する効果

- 改善の見込み: 4-2(公園など Beautification の数)を1つ増やす。今の 92 は目標 100 に8足りない。1つ増えれば 93 になる見込み。公園の数は、16 月の案で 90→91、17 月の案で 91→92 と、1つずつ増えた(確認した事実)。
- 数値と期限: 今の値 92(`buildings_near` service=Beautification、18 月)。予想は 93。期限は 18 月末
- 確認方法: `buildings_near`(service=Beautification、x 0、z 0、r 8000、brief=true)の total を、今の 92 と比べる。同じ道具・同じ範囲で測る
- 不確かな点: 効果の量は確かめた事実(置けて、数が1増える)で足りる。地価(4-1)への効きは、この案では見ない(事業2で測る)
- 試し: なし

### 費用

- 建設費: 2,500(`test_place_building` の cost。`list_building_types` の JapaneseGarden の cost と一致)
- 週の維持費の増え: 40(`list_building_types` の upkeepPerWeek)。週の収支 +10,007 は約 +9,967 になる

### 戻せるか

戻せる。ただし取り壊すときは議決が要る。

### 前の月の答え合わせ

- m17 の案 urban-1(道に面した空き (1820, 300) に JapaneseGarden を1つ、m17-1)は採られ、実行 ok(建設費 2,500)。期待は公園の数の1増加。
- 結果: 当たり。Beautification は、16 月の 91(`buildings_near` の total)から、18 月に 92 になった。(1820,300) の JapaneseGarden 31332 が一覧にある。
- 事業2の基準の地価は、今月の測り(`land_value` 2168,194 r200)で平均 67。基準 66 から +1 で、動きは小さい。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2、8-1、6-4、4-4)。重点の外の案として出す

## 案なし

案は1件だけ。案2 以降はない。候補の探し方の結果は「捨てたもの」と「判断の根拠」に書く。

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口 175,384、所持金 2,531,972、週の収入 338,572、週の支出 328,565(収支 +10,007)、観光客 1,783(訪問 159)、需要 住 28/商 2/工 52、citizensWithoutService 0/0/0、dialog なし
- `list_policies`: 有効は SmokingBan(費用 0)、EducationBoost(週 7,940)、BigBusiness(週 3,936)。公園の数を増やす政策はない。RecreationalUse と FreeTransport は無効(費用 0)。政策の変更は案にしない
- `land_value`(2168, 194、r 200): 平均 67、min 38、max 79、cityAverage 53
- `demand_breakdown`: 働き口 87,258(空き 3,480)、家 56,114(空き 5,647)、失業 4,349(大卒 4,161)、homeless 0
- `buildings_near`(service=Beautification、x 0、z 0、r 8000、brief): total 92(JapaneseGarden 31332 が (1820,300) にある。17 月の案の分)
- `buildings_near`(x 1800、z 320、r 160、brief): 29棟。周りは住宅と店で埋まっている
- `buildings_near`(abandoned=true、x 1800、z 300、r 1500、brief): 放棄 66棟。道に面していても、取り壊すと働き口か家を失うものが多い
- `zone_map`(中心 1820,300、r 300、size 600)、`zone_map`(2350,400、r 400、size 700)、`zone_map`(3400,400、r 350、size 700): 空きの位置を見た。白く空いた区画の多くは、建物の空きではなく、サービス建物、風車、道路で、置けない
- `zone_summary`(grid 1000): 道に面した空き区画(emptyFacingRoad)は、商業(高密度)36 だけ。住宅(高・低)、事務所、工業はゼロ
- `net_near`(1800、320、r 160): 道路 16524(Basic Road、x 1770、z 177〜253)、道路 4414(Basic Road、x 1770、z 253〜330)、送電線と水道管(x 1775〜1830、z 325)
- `test_place_building`(JapaneseGarden): 1795,250 facing west → ok(2 回)。1800,285 → 31332 と重なり断られた。1800,212 → 噴水 41780 と重なり断られた。1880,110 → 道路と重なり断られた。2290,540(north)→ 道路と埋立地 45436 と重なり断られた。2450,520(north)→ ok だが entrance.road null、取り壊す事務所 3棟(働き口 55)。2350,480 → 風力 38506 と重なり断られた。2224,170 / 2224,310 / 2224,-452 / 1588,483(放棄店の取り壊しを仮定)→ 道路や別の建物と重なり断られた。1856,48(放棄店 16316 の取り壊しを仮定)→ 家 2 を失い、entrance.road null。1856,-107(east)→ 道路 3915 に面するが、取り壊す建物 2682、11517 で働き口 24 を失う。3560,552 / 3500,552 / 3620,590 → 埋立地、火葬場、墓地と重なり断られた
- `test_place_building`(Regular Plaza、1795,285、west)→ 道路と公園 31332 と重なり断られた
- `list_building_types`(service=Beautification): JapaneseGarden 4×4、2,500、週 40、道が要る、電気と水が要る。Regular Park 9×8(1,000、週 8)は、この空きには大きすぎる
- `water_trace`(1795, 250): 近くの水道の網は1つ。建物 31332 の水・下水は届いている。city の水 used 1,894,576 / capacity 2,400,000
- `map_layer`(water_service、electricity_service、x 1795、z 250、r 40、n 3): 9点とも 1

## 判断の根拠

- 4-2 の公園は 92 で、目標 100 まで 8 足りない。残り 7 か月で 8 つを置くには、月1つ以上の空きが要る。今月は (1795, 250) の1か所を、確かめた条件で案にした。道路の入口、電気、水、重なりを、試しの道具と map_layer で確かめた。
- 道に面した空きは少ない(zone_summary で商業高密度の36マスだけ)。放棄店の跡は、働き口か家を失うものが多く、今月は使わない。長期計画の取り壊しの枠は、12か月で働き口 30 以下に収める。
- 4-1 の地価は 67(基準 66、+1)。公園の効きとは言えない。事業2の判定は第20月に延ばした(計画の変更)。
- 案は1件にした。ほかの候補は、試しで置けないか、働き口・家を失うため、確かめた条件を満たさない。件数を埋めるための案は作らない。

## 捨てたもの

- JapaneseGarden を (1856, -107) に、east で置く案: 道路 3915 に面して置けるが、取り壊す建物(ホテル 2682、店 11517)で働き口が 24 減る。放棄建物ではないため、今月は見送り
- JapaneseGarden を (2450, 520) に、north で置く案: 取り壊す事務所 3棟で働き口が 55 減る。入口の道もない。見送り
- JapaneseGarden を (1856, 48) に、north で置く案: 取り壊す建物で家が 2 減り、入口の道がない。見送り
- (1800, 285)、(1800, 212)、(2290, 540)、(2224, 170)、(2224, 310)、(2224, -452)、(1588, 483)、(2350, 480)、(1880, 110)、(3560, 552)、(3500, 552)、(3620, 590): 試しで、他の建物、道路、サービス建物、風車と重なり、置けなかった
- Regular Plaza、Regular Playground(5×5)、ParadoxPlaza(5×5): 1795, 285 で重なった。5×5 は 4×4 の JapaneseGarden より大きく、空きに入りにくい。今月は使わない
- 装飾の駐車場(Decoration Concrete Parking Lot 01、2×4)など: 4-2 の数える対象は公園なので、置く案にはしない
- 政策の変更: 4-2 に効く政策は一覧にない。今月は政策の案なし
