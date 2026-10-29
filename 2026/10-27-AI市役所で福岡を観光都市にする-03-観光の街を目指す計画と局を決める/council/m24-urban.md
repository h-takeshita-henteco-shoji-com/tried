# m24 住宅都市みどり局の案

## 案1: 放棄建物 30881 の跡に公園 JapaneseGarden を置き、4-2 を100にする

### 施策

- 案の id: urban-1
- 施策: 放棄された Commercial の建物 30881(H3 4x3 Shop03、中心 (2128,423))を取り壊し、同じ場所に JapaneseGarden(Beautification)を1棟置く。入口 (2128,407) から道(Basic Road)を (2152,407) の既存の交差点へつなぐ
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `bulldoze` x=2128, z=423, radius=16, what="building"(建物 30881 だけ。`preview_bulldoze` で 1棟、失う働き口 0、家 0 を確認)
  2. `place_building` prefab="JapaneseGarden", x=2128, z=423, facing="south"(入口 (2128,407)。angleUsed 180)。置いた後に `buildings_near` で grid を確かめる
  3. `test_build_line` prefab="Basic Road", points=[[2128,407],[2152,407]](cost 120、overlaps 0)
  4. `build_line` prefab="Basic Road", points=[[2128,407],[2152,407]](終点の (2152,407) は既存の交差点 node 23837 につながる)
- 設置条件の確認:
  - 建物 30881 の跡: `test_place_building` JapaneseGarden (2128,423) facing south、assume_removed_buildings=[30881] で ok=true。取り壊しで失う働き口・家は 0
  - 入口の道: `net_near` (2128,430 r120) で、(2152,407) に Small 4 Lane Road の端(segment 18 と 6523 の接点)があると確認。`test_build_line` で Basic Road (2128,407)→(2152,407) が ok、overlaps 0
  - 電気・水・下水: `water_trace` (2128,423) で、建物 30881 の grid が electricity / water / sewage ともに true、cell の water / sewage も true
  - 「道路が先」ではない(建物を先に置き、道を後に引く)
  - 37481(H3 2x2 Shop01、(2128,447)、働き手 8)は道と重ならない位置に残る。`test_build_line` の overlaps で、取り壊しの対象にならないことを確認
- 接続工事: 道 Basic Road 24m。建設費 120、週 約1
- 予備候補:
  - (1856,-132) の JapaneseGarden facing east。`test_place_building` で ok。ただし取り壊す 1110(H1 2x2 Shop01、働き口 6、放棄ではない)を含むため、働き口を6失う。今月の第一候補ではなく、2128 が断られたときだけ使う
  - 確認して外したもの: (2224,170)、(2224,-190)、(2176,256)、(2228,90) は Medium Road に重なる。(2128,423) の north 向きは入口が 37481 に塞がれる。Regular Park(9x8)と Regular Playground は、(1856,-132) と (2128,423) のどちらも道と重なる
- 中止する条件: `bulldoze` の後に `test_place_building` が断ったとき(道に重なる、建物が増えた)、または取り壊しの議決が否決されたとき。その場合は予備候補の (1856,-132) を、`test_place_building` で取り直してから使うか、見送る

### 期待する効果

- 改善の見込み: 4-2 の Beautification の数を 99 から 100 に上げる。今の値 99 は市政ノートの24月の値で、今回の道具では数え直していない。放棄の跡に置いた公園は、21〜23月の答え合わせで +1 になった(当たり)
- 数値と期限: Beautification 99 → 100(24月末の確認)。建設に日数がかかるため、完成は24月末の見回りまで待つ。最終月のため、効果は24月末の測りで確かめる
- 確認方法: `buildings_near` (x=2128, z=423, radius=40、または街全体で Beautification の数)。今の値 99 と同じ数え方
- 不確かな点: 取り壊しの議決が必要。道がつながるかは、置いた後の `buildings_near` の grid と `net_reach` で確かめる。地価(4-1)は、公園1棟ではほぼ動かない見込み(数値は見積もれない)
- 試し: なし

### 費用

- 建設費: 2,620(JapaneseGarden 2,500 + Basic Road 24m 120。`list_building_types` と `list_net_types` の値)
- 週の維持費の増え分: 41(JapaneseGarden 40 + Basic Road 約1。`upkeepPerWeekPerKm` 40 × 0.024km)

### 戻せるか

戻せない。取り壊した建物 30881 は戻らない。

### 前の月の答え合わせ

- 23月の案1(urban-1、放棄店 10258 の跡 (1856,-46) に公園)は採られ、実行 ok。期待は Beautification 97 → 98(24月末)。市政ノートの24月の値は 99 で、予想より1多い(当たり)。ほかの公園の完成が混ざった可能性は残る
- 23月の案2(urban-2、空き2か所に木3本の試し、4-1)は採られ、実行 ok。期待は近くの騒音と住宅(高)地価の差が小さいこと。24月末の測りで、騒音は平均 33 → 30、住宅(高)地価 67 → 67。騒音は下がったが地価は動かず、半分。木の効きは小さく、事業2を閉じた

### 市の計画

- 当たる施策: 4-2 花や緑による潤い(Beautification 99 → 100、目標 100 以上)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1・5-2、6-3、4-3。4-2 は編成方針で「案が出れば比べる」)

## 案なし

(案1だけを出すので、この見出しは書きません)

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口172,273、所持金2,697,883、週の収支+6,823、幸福度87、観光客2,011(訪問179)、需要 住36/商2/工42、来ない市民 0/0/0
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,008)。無効は RecreationalUse(0)、SmallBusiness(319)、HighTechHousing(20,244)、Recycling(0)など。4-2 の公園には政策の変更が要らず、4-1 の地価に効く政策は見当たらない。HighTechHousing は週 20,244 のため、守る線(週の収支 +3,000)を割るので不採用。RecreationalUse は 0 だが、m04 で効きが見えず外した経緯があり、4-1 にも関係しない
- `demand_breakdown`: 働き口 87,063(空き 6,408)、家 56,237(空き 6,120)、大卒の失業 2,380
- `building_stats`: 住宅(高)の地価の平均 59(radius 3000)、事務所L3 3,286、住宅(低)46
- `land_value`: 街の平均 53(cityAverage)
- `buildings_near`: 放棄された建物の一覧(abandoned=true、中心 (2050,0) r700)。候補は 30881(2128,423)、32543(2168,-166)、18733(2176,256)、9542(2224,170)、7002(2224,-190)、26762・27320(2228,80〜102)、11517(1856,-132)。Beautification の数は、今回は数え直していない(市政ノートの24月の値 99 を使う)
- `list_building_types`: service=Beautification。JapaneseGarden 2,500 / 40、Regular Park 1,000 / 8、Regular Playground 1,250 / 24、Regular Plaza 2,500 / 32 ほか。Regular Park と Playground は (1856,-132) と (2128,423) で道に重なり不採用
- `zone_map`: (1900,-100) r250 と (2128,430) r120。道の位置と空きの確認
- `test_place_building`: JapaneseGarden (1856,-132) facing east(11517 取り壊し、1110 を含む。働き口 6 失う)、(2128,423) facing south(30881 取り壊し、ok)、(2168,-166) west(45283 取り壊し、働き口 8 失う、入口に道なし)、(2224,170)・(2224,-190)・(2176,256)・(2228,90) は道と重なり不可、(2128,423) north は入口が 37481 に重なり道が引けず
- `preview_bulldoze`: (1856,-132) r50 の放棄 11517(働き口 0、家 0)。(2128,423) r16 の 30881 の取り壊し(働き口 0、家 0)
- `net_near`: (2128,430) r120。Small 4 Lane の x=2152 の南北道(node 23837 at (2152,407)、1057 at (2152,483))
- `test_build_line`: Basic Road [[2128,407],[2152,407]](ok、cost 120、overlaps 0。取り壊し前の判定で、元の建物 30881 を assume_removed で外す)。Basic Road [[2128,438.7],[2152,438.7]] は 30881 と 37481 に重なり断られた
- `list_net_types`: Basic Road は 5,000 / km、維持費 40 / km / 週
- `water_trace`: (2128,423) の建物 30881 の grid は electricity / water / sewage ともに true。cell は water / sewage true、waterPollution 0。水の網は1つ、取水口 Water Tower が多数

## 判断の根拠

- 4-2 の Beautification は、市政ノートの24月の値で 99 で、100 まであと1。案1は、放棄建物 30881 の跡に JapaneseGarden を1棟置き、100 にする。道は入口から既存の交差点へ1本(24m)で、確認した。Regular Park や Playground は、道と重なって置けなかった
- 4-1 の住宅(高)地価 59 は、目標 62 まで3足りない。23月の木の試しは地価を動かさず、24月で最終月のため、今月の案で 62 に届く手は見つからなかった。事業2は閉じる
- 案は1件に絞った。4-2 はあと1で、ほかの手(政策、木)は効きが小さいか、守る線を割るため
- 観光(5-1・5-2)は重点だが、公園は Visitors 11 程度で街全体の観光客を動かさなかった(23月の測り)。今月の観光の案は、economy と port の担当に任せる

## 捨てたもの

- 1856,-132 の JapaneseGarden(facing east): 4-2 の効きは案1と同じだが、取り壊す 1110 が働き口 6 を失う。放棄の 30881 で置けるため、予備にとどめた
- 2168,-166 の JapaneseGarden(facing west): 取り壊す 45283 が働き口 8 を失い、入口に道がない。案1より悪い
- Regular Park(1,000 / 8)・Regular Playground(1,250 / 24): 安いが、(1856,-132) と (2128,423) で道に重なり、置けない
- 木を増やす(4-1): 23月の試しで地価は動かず、騒音の効きも3だけ。24月で閉じた
- HighTechHousing(政策、週 20,244): 4-1 に効く見込みはあるが、週の収支 +6,823 を割るため不採用(守る線 +3,000 を割る)
- RecreationalUse(政策、0): 観光の効きが見えず、4-1 にも関係しないため見送り
