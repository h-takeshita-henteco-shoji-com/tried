# m06 住宅都市みどり局の案

## 案1: 南西の空きに広場 Regular Plaza を1棟

### 施策

- 案の id: urban-1
- 施策: 南西の道路沿い (-440,-822) に Regular Plaza を1棟置く。道路 (Basic Road、segment 11125) に面させる。4-2 の Beautification を 86 から 87 にする
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `test_place_building` を prefab "Regular Plaza"、x -440、z -822、facing "south" で再確認する(ほかの建物が増えていないか)
  2. `map_layer` type "landvalue"、x -440、z -822、radius 150、n 5 を、置く前の基準として取る
  3. `place_building` を prefab "Regular Plaza"、x -440、z -822、facing "south"、pay 既定(true)で置く
  4. 置いた後に `buildings_near` を x -440、z -822、radius 300、brief true で呼び、建った棟を確かめる
- 設置条件の確認:
  - `test_place_building`(Regular Plaza、-440,-822、south): ok=true、placed=false。entrance (-440,-842) の道路 segment 11125 Basic Road、距離1m。cost 2,500、enoughMoney true。wouldDemolish 0、lostByDemolish は jobs 0・homes 0
  - `map_layer` electricity_service(x -440、z -822、radius 30、n 3): 9点すべて 1(電気が届いている)
  - 同じ区域の `water_trace`(点 -480,-819 の近くの建物)は electricity・water・sewage とも true。Plaza は電気だけ要る
- 接続工事: 不要(道路に面し、電気は届いている。建設費は下の 2,500 だけ)
- 予備候補: なし。確認できた空きは、この1か所だけ。下の「捨てたもの」の候補は、道路・既存の建物との重なり、または電気が届かないため使えない
- 中止する条件: 実行前の `test_place_building` が ok=false になったら見送る(ぶつかった相手を読んで、ほかの手は探さない)。`wouldDemolish.count` が 0 でなければ見送る(取り壊しを伴う案ではないため)。電気の確認(map_layer)が 0 の点を含むなら見送る

### 期待する効果

- 改善の見込み: 4-2 の Beautification は 86 で、目標 100 まで 14 足りない。この1棟は +1 にとどまり、目標には届かない。m05 に置いた Regular Plaza(1640,596)は、Beautification を 85 から 86 に1だけ増やした(確認した事実)。同じ手なので、+1 は見込める。周りの地価は、m05 の広場で 34 から 36 に上がったが、他の要因と分けていない
- 数値と期限: Beautification 86 → 87(予想)。期限は 2050-07-01 の月末
- 確認方法: `buildings_near` を service "Beautification"、x -440、z -822、radius 2000、brief true で呼び、total を数える(今の値 86 と比べる)。地価は `map_layer` landvalue、x -440、z -822、radius 150、n 5 の平均を、実行前の基準と比べる
- 不確かな点: 数値の予想は 1 棟分の +1 だけ。地価の効きは見積もれない(数は見積もれない)。目標 100 は、この案だけでは届かない。残りは別の手が要る
- 試し: なし

### 費用

- 建設費: 2,500(`test_place_building` の cost)
- 週の維持費の増え分: 32(`list_building_types` の Regular Plaza の upkeepPerWeek)

### 戻せるか

戻せる。取り壊しの議決を取れば、建物を壊して元に戻せる。議決なしでは壊せない点に注意。

### 前の月の答え合わせ

- 前の月の案 urban-1(m05-2、Regular Plaza (1640,596))は採られ、実行された。期限は 2050-06-01(5か月目の月末)
- 結果: Beautification 85 → 86(予想どおり +1)。周りの地価 34 → 36(他の要因と分けていない)
- 判定: 半分。数は当たり。地価は切り分けていないので判定前の扱い
- 同じ月の urban-2(公園、取り壊し9棟)は採られなかった。理由は、取り壊しで家51・働き口50を失うのに効果が +1 だけだったため。今月の案は取り壊しを含まない

### 市の計画

- 当たる施策: 4-2 花や緑による潤い、4-1 都市と自然が調和したコンパクトなまち(地価を介して)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2 観光、4-4、8-1)。ただし局の担当の数字(4-2)に効く案として出す

## 案なし

(案1 を出すため、この見出しは書かない)

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口180,778、所持金2,197,627、観光客1,631/155、週の収支 +8,944、需要 住宅27・商業2・工業56、電気・水・下水が来ない市民 0/0/0
- `demand_breakdown`: 働き口 86,674(空き3,607)、家 55,724(空き4,754)、失業 6,436(大学卒 6,227)、ホームレス 0
- `land_value`: 街の平均 54
- `list_policies`: 有効なのは SmokingBan(0/週)、EducationBoost(7,940/週)、RecreationalUse(0/週、効きは m01 で外れ)、BigBusiness(3,872/週)。無効: Recycling(0/週、税収 -5%・ごみ -15%)、SmallBusiness(309/週)、IndustrySpace(4,828/週)、HighTechHousing(20,248/週)、PowerSaving・WaterSaving・SmokeDetectors(約5万〜5.8万/週)、ほかの税の政策は 0/週で無効。観光に直接効く政策は RecreationalUse のみ(効きは見えていない)。公園・広場の数を増やす政策はなし
- `building_stats`: 住宅(高密度)の地価の平均 59、事務所 L3 3,270棟、高密度商業は放棄 124 棟を含む 1,112 棟(レベル3が 886)
- `list_building_types`(Beautification、解禁済み): Regular Park(9x8、1,000、維持費 8/週)、Regular Plaza(5x5、2,500、32/週)、Regular Playground(5x5、1,250、24/週)、ParadoxPlaza(5x5、1,000、16/週、水・下水が要る)ほか。岩・石の装飾(100、0/週)は、数だけ増やすもので緑の目的に当たらないため使わない
- `zone_map`(1700,500 r300 / 2300,500 r700 / -600,-700 r300 / 2750,950 r250 / -1150,-450 r250): 空きの候補を探した。道路沿いで空きに見えた場所の大半は、道路・既存の建物・ほかの Beautification と重なった
- `test_place_building`(Regular Park / Regular Plaza)の結果:
  - 成功(ok=true、取り壊しなし): Regular Plaza (-440,-822) south、entrance 道路 11125 距離1m、cost 2,500。Regular Plaza (-440,-870) は north で ObjectCollision のため不可(-440,-870 の試しは断られた)。Regular Plaza (2770,972) north は ok だが電気が届かない(下の map_layer)。Regular Plaza (2715,972) north も ok(電気は未確認)。Regular Plaza (1800,-280) west は入口に道路がなく不可
  - 断られた(ObjectCollision、道路・ほかの建物・Beautification と重なる): Regular Park (1700,590)、(1700,606)、(1790,590)、(-520,-815)、(-420,-815)、(2830,1100) 付近、Regular Plaza (1700,584)、(1640,584)、(1700,600)、(-500,-870)、(2770,1000)、(2770,982)。入口に道路がない(road null): (2770,935)、(2770,953)、(-440,-820 north)
  - 取り壊しを含む試し(放棄された建物を assume_removed で外した): Regular Park (2128,447)、Regular Plaza (2432,256)、(1856,236)、Regular Park (2176,-330)、(2168,560)。いずれも道路・ほかの建物と重なり断られた
- `buildings_near`(abandoned=true、x 2000、z 500、r 1200、brief): 放棄 53 件を確認(ほとんど放棄された高密度商業)。取り壊しの候補にしたが、道路との重なりで置けなかった
- `map_layer`(electricity_service): (-440,-822) r30 n3 は 9点すべて 1。(-440,-822) r45 の -470,-880 付近も 9点すべて 1。(2770,972) r20 n3 は 0 が多く(0,0,0 / 0,0,0 / 1,0,0)、電気が届かない
- `water_trace`(-440,-822): 近くの建物(Expensive Plaza 18400、-480,-819)は電気・水・下水とも true。水の網はつながっている

## 判断の根拠

- 4-2 の Beautification は 86 で、目標 100 まで 14 足りない。取り壊しなしで置けて、道路と電気の条件を確かめられた場所は、南西の (-440,-822) の1か所だけだった
- 候補は、東の北(2770,972 周辺)、中央北(1700,590 周辺)、南西(-440,-822 周辺)、放棄された商業の跡(2128,447、2432,256、1856,236、2176,-330、2168,560)の6つの区域で試した。確認が通ったのは南西の1か所だけ
- 案は1件にした。確認できていない候補を案に入れないため。件数を埋めるための案は出さない
- 取り壊しを伴う公園の案(放棄された商業の跡)は、置けない形しか見つからなかった
- 観光(5-1、5-2)は市長の重点だが、局の担当は公園・木と地価。名所の案は economy の担当で、ここでは出さない。前の月までの公園の増設(m04-1、m05-2)では、観光客は増えなかった。今月の案は観光の数を見込まない

## 捨てたもの

- Regular Park 3棟を東の北(2770,972 周辺)に置く案: 道は (2770,1000) の Basic Road で取れるが、電気が届かない(map_layer で 0)。電気の接続工事(送電線)は費用と道の確認が要り、今月の確認では必須条件が揃わない
- 放棄された商業(H3 Shop 系)を取り壊して公園を置く案: 放棄の建物は失う働き口・家が 0 だが、置ける形が見つからなかった(道路・ほかの建物と重なる)。取り壊しの議決を取る前の確認で断られた
- 岩・石の装飾(Rock Area、Cliff、100 each、0/週)で Beautification の数を増やす案: 数だけ増え、緑による潤いの目的に当たらない
- 公園 Regular Park 1棟を南西 (-520,-815) や (-420,-815) に置く案: ObjectCollision(道路・ほかの Beautification・電線)で不可
- 政策の変更(公園の数や魅力度に効く政策): 一覧に、Beautification の数を増やす政策はない。RecreationalUse は効きが見えていない(m01、m02 で外れ)
- 税・予算の変更: 4-1、4-2 の数を動かす根拠が、今月の数字にない
