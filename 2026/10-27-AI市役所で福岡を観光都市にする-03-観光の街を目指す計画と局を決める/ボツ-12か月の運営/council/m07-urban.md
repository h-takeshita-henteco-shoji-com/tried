# m07 住宅都市みどり局の案

## 案1: 北東の道路沿いに遊び場 Regular Playground を1棟

### 施策

- 案の id: urban-1
- 施策: 座標 (1752, 1082) に Regular Playground を1棟、入口を東向き(facing east)で置く。入口は基本道路 segment 24911 に 11.7m で面する。道具は `place_building`。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `test_place_building` prefab "Regular Playground", x 1752, z 1082, facing "east" を再実行する(ok、angleUsed 270、取り壊し 0、費用 1,250 を確認済み)。
  2. `place_building` prefab "Regular Playground", x 1752, z 1082, facing "east"。pay は既定の true。
  3. 置いた後、`buildings_near` (x 1752, z 1082, radius 30) で grid の electricity が true か、problems に Road の印がないかを見る。
- 設置条件の確認:
  - `list_building_types`(Beautification): Regular Playground は 5×5、建設費 1,250、維持費 24/週、道路と電気が要る(水・下水は不要)。
  - `test_place_building`(1752, 1082, east): ok=true、placed=false、取り壊し 0、入口の道路は segment 24911 まで 11.7m。
  - `map_layer` electricity_service(1752, 1082, r40, n3): 中心の点は 1。北の行と中段は 1、南の行は西端が 0。
  - `buildings_near`(1752, 1082, r60): 近くの事務所 40736(1800, 1076)の grid は electricity・water・sewage とも true。
- 接続工事: 不要(道路に面している。電気は中心の点で届いている)
- 予備候補: なし。今回確かめられた候補は (1752, 1082) だけ。ほかの候補は、建物の重なり・道路・取り壊しのため採らなかった(捨てたもの)。
- 中止する条件:
  - 実行時の `test_place_building` が ok=false になった(ぶつかった相手を見て、案を見送る)。
  - `test_place_building` の wouldDemolish.count が 0 でなくなった(取り壊しを伴うため見送る)。
  - 置いた後、buildings_near の grid で electricity が false のまま(電気の網を確かめ、見送るか局に戻す)。

### 期待する効果

- 改善の見込み: 4-2 の Beautification の数を +1 する。遊び場は Beautification の種類なので、Beautification の数に入る。今の数は 87 で、目標 100 には遠く、この案だけでは届かない。地価(4-1)への効きは量を見積もれない。
- 数値と期限: 4-2 は Beautification の数 87 → 88(予想、+1 の確定)。期限は次の月例(8か月目)。4-1 は building_stats の住宅(高密度)の地価の平均 59 を基準に、月例で見る。
- 確認方法: `buildings_near`(Beautification)の数を、置く前後で同じ引数で数える。4-1 は `map_layer` landvalue(x 1752, z 1082, radius 150, n 5)の平均を置く前後で比べる。
- 不確かな点: 地価への効きは数値を見積もれない。遊び場が住宅の近くで地価を上げる見込みはあるが、今回は測っていない。週の維持費 24 は、週の収支 +8,818 の範囲に収まる。
- 試し: なし(数の効きは確定。地価の効きは調査で測る)

### 費用

- 建設費: 1,250(`test_place_building` の cost)
- 週の維持費の増え分: 24(`list_building_types` の upkeepPerWeek)

### 戻せるか

戻せる。建てた後は取り壊しで戻せるが、取り壊しには議決が要る。

### 前の月の答え合わせ

- 前の月(6か月目)の urban-1 は m06-2 として採られ、Regular Plaza を (-440, -822) に置いて実行した(ledger の m06-urban-1、市政ノートの 6か月目)。期限は月例。結果: Beautification 86 → 87(目標 100 まで 13)。数の効きは当たり。ただし地価は測っていないので、4-1 への効きは判定前。
- `council/m06-survey-urban.md` はファイルがなく、結果は読めなかった。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い(Beautification の数 87、目標 100)。4-1 都市と自然が調和したコンパクトなまち(住宅(高密度)の地価 59、目標 62)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2 観光、4-4 資源循環、6-4、7-1 企業の立地)。ただし、担当の数字 4-2 の案なので出す。

## 調査

- 調査: あり
- 問い: 遊び場(Regular Playground)を道路沿いの住宅地に置いた周りで、住宅(高密度)の地価を押し上げるか。
- 見る道具と引数: (1) `map_layer` type "landvalue"、x 1752、z 1082、radius 150、n 5。(2) `map_layer` type "attractiveness"、同じ引数。(3) `buildings_near`、x 1752、z 1082、radius 30、brief true。置く前に同じ引数で基準を取る。
- いつ見るか: 見回り1、月末
- 何が分かれば次の手が決まるか: 置いた後の landvalue 平均が基準より +2 以上なら、同じ型の遊び場を住宅地の空きに続けて置く案を次の月に出す。+1 以下なら、地価の効きは小さいと見て、4-2 の増やし方は別の種類を調べる。buildings_near の Beautification が 1 増えていなければ、置き方を見直す。
- 担当の問題: 4-1 都市と自然が調和したコンパクトなまち(住宅(高密度)の地価)、4-2 花や緑による潤い(公園などの数)

## 見たもの

- `city_info`: 人口 179,838、所持金 2,184,832、観光客 1,608/157、週の収支 +8,818、電気・水・下水が来ない市民 0 / 0 / 0
- `demand_breakdown`: 働き口 86,457、空き 3,607、家 55,772、住宅の空き 4,881
- `list_policies`: 政策費用の合計 10,632/週。有効なのは SmokingBan(0)、EducationBoost(7,940)、RecreationalUse(0)、BigBusiness(3,844)。無効のうち Recycling は費用 0 で、住宅税 -5%、ごみ -15%(4-4 に当たる。住宅局の案ではない)。HighTechHousing は 20,252/週で無効。urban の 4-1、4-2 に効く政策は見当たらないため、今月は変えない
- `building_stats`: 住宅(高密度)の地価の平均 59。事務所 3,979 棟(L3 3,273)、放棄された高密度商業 139 棟
- `land_value`: 街の平均 53
- `zone_summary`(grid 1000): 道路に面した空きの区画は、高密度商業と低密度商業が中心。住宅(高密度)で道路に面した空きは見つからなかった
- `zone_map`(中心 1500,300 r1200、中心 2400,650 r300、中心 1350,1000 r350、中心 800,700 r600、中心 2300,1100 r250): 北東は道路沿いの建物が密集、北西は空いた地面と送電線だけで道路がない。2400,650 付近は既存の公園と埋立地
- `net_near`: (1100,850) r150 は道路なし。(1700,1000) r150 は基本道路 segment 24911(1840,1100→1780,1100)、36183(1780,1100→1780,1172)。(2250,-400) r150 は基本道路と中型道路
- `buildings_near`(abandoned、r1500): 71 棟。放棄された店・工場が多く、道路や事務所と重なる
- `list_building_types`(Beautification): Regular Playground は 5×5、1,250、維持費 24/週。Regular Plaza は 5×5、2,500、32/週。Regular Park は 9×8、1,000、8/週。Boulder・Rock・Cliff(100、維持費 0)は景観の岩で、緑の目的に当たらないため使わない
- `test_place_building`(候補の結果):
  - Regular Plaza (1740,1080) north: ok だが入口の道路なし(road null)
  - Regular Park (1700,1150) east: ObjectCollision(University 13142)
  - Regular Plaza (2230,-345) south: ObjectCollision(道路 4530・33530、店)
  - Regular Plaza (1810,1080) north: ObjectCollision(道路 24911、事務所)
  - Regular Plaza (1812,1140) west: ok だが取り壊し 4 棟(事務所、働き口 57)
  - Regular Plaza (1752,1120) east: ObjectCollision(University 13142)
  - Regular Playground (1752,1082) east: ok、取り壊し 0、入口 11.7m、費用 1,250(採用)
  - Regular Playground (1752,1140) east: ObjectCollision(University 13142)
  - Regular Plaza (2381,854) west・south(assume_removed 6690): ObjectCollision(道路 26130・26770、店 40606)
  - Regular Plaza (2172,584) west(assume_removed 9427): ObjectCollision(道路 5473・6706・10663・26764、事務所)
  - Regular Park (2172,584) east(assume_removed 9427): ObjectCollision(同上)
  - Regular Plaza (1856,-451) west(assume_removed 16263): ObjectCollision(道路 7987・36498)
  - Regular Park (1856,-451) west(assume_removed 16263): ObjectCollision(道路 4991・7987・31555・36498)
  - Regular Playground (2381,852) south(assume_removed 6690): ObjectCollision(道路 26130・26770)
  - Regular Playground (1856,-451) east(assume_removed 16263): ObjectCollision(道路 7987・36498)
  - Regular Park (2507,520) north: ObjectCollision(埋立地 3565、事務所)
  - Regular Park (2230,520) north: ObjectCollision(埋立地 45436、事務所)
  - Regular Park (2400,480) north: ObjectCollision(風車 9087・38506、送電線)
- `map_layer`(electricity_service、x 1752、z 1082、r40、n3): 中心 1。北の行 1,1,1、中段 1,1,1、南の行 0,1,1
- `buildings_near`(x 1752、z 1082、r60): 事務所 40736(1800,1076)の grid は electricity・water・sewage とも true

## 判断の根拠

- 担当の数字は、4-2 Beautification 87(目標 100、あと 13)と、4-1 住宅(高密度)の地価 59(目標 62)。4-2 の目標には、同じ型の建物を 13 棟置く必要がある。確認できた道路に面した空きは、ほとんどが建物や道路と重なり、置けた候補は 1 つだけだった。
- 候補の確認は、北東・南東・北西の複数の地区で行った。北西の空き地は道路がなく、道路を引く案は今月は確認していない。
- 案を 1 件にした理由: 置けたのは (1752,1082) だけで、ほかは取り壊し(事務所の働き口を失う)か、道路・建物との重なりで断られた。件数を埋めるための案は出さない。
- 案1 は、取り壊しなし、道路に面し、電気が届く点で確かめた。数の効き(+1)は確定、地価の効きは量が見積もれないので調査で測る。
- 政策は、urban の担当の数字に効く政策が見当たらなかったため、変えない。
- 調査 1 件は、案1 の効き(地価)を測るために出す。

## 捨てたもの

- Regular Plaza (1812,1140) west: ok だが、取り壊しで事務所 4 棟(働き口 57)を失う。戻せないため採らない
- Boulder・Rock・Cliff(建設費 100、維持費 0): Beautification の数だけを増やせるが、緑で潤うという 4-2 の目的に当たらないため採らない
- 放棄建物を壊して広場や遊び場を置く案(2381,854、2172,584、1856,-451): 道路や建物と重なって断られたため採らない
- 北西の空き地に道路を引いて公園を置く案: 道路の接続を先に確かめる必要があるため、今月は見送る。次の月に出し直す候補とする
- 名所(Monument)や観光の手: 観光の名所は economy の担当で、urban は 4-2 の数だけを出す
- HighTechHousing(20,252/週)や税の政策: 地価に効く見込みはあるが、費用が大きく、週の黒字(+8,818)を大きく減らすため採らない。税は議決が要るため、今月は案にしない
