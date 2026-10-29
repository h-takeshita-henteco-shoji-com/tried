# m19 経済観光文化局の案

## 案1: 空き地3に天文台を置く試し

### 施策

- 案の id: economy-1
- 施策: 空き地3(745,1500)に名所 Observatory(7x6)を1棟。向きは西(facing west)。入口は道路 13359 の東端(721,1500)付近。電気は既存の送電網の節(560,1480)から Power Line で引く(終点は建物の敷地の中)。水と下水は本線から Water Pipe [[743,1123],[745,1470]] で引く
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building`(prefab Observatory、x 745、z 1500、facing west、pay true)。`test_place_building` で ok、cost 85,000、enoughMoney true を確かめた
  2. 置いた後、`place_building` の返り値の ports で、水のつなぎ口の位置を確かめる(下水も同じ管の網)
  3. `build_line`(prefab Power Line、points [[560,1480],[650,1480],[745,1480],[745,1492]])。始点 (560,1480) は既存の送電網の節 24073 につながる。終点 (745,1492) は建物の敷地の中。引く前の `test_build_line` で ok、5区間、cost 520、overlaps なし
  4. `build_line`(prefab Water Pipe、points [[743,1123],[ports の水のつなぎ口]])。端点を、置いた建物の水のつなぎ口に合わせる。引く前に `test_build_line` で確かめる(端点 (745,1470) では ok、5区間、cost 900)
  5. 引いたあと、`water_trace`(x 745、z 1500)で、cell の water、sewage、電気の届きが true になったかを見る
- 設置条件の確認:
  - 敷地: `test_place_building` で ok。wouldDemolish 0、lostByDemolish の働き口と家は 0
  - 道路: entrance は道路 13359(距離1)。前月の `net_reach` で、道路と建物は来られると確認済み
  - 電気(今回確認): 次の経路は、いずれも `test_build_line`(Power Line)で断られた。(633,1575)→(745,1500) は StatueOfWealth 11580 にぶつかる。(727,1626)→(745,1500) は Regular Park 30466 と Pedestrian Gravel にぶつかる。(633,1575) を南回りにした経路も 11580 にぶつかる。採ったのは (560,1480)→(650,1480)→(745,1480)→(745,1492) で、ok。始点は `net_near`(560,1480、半径30)で、既存の送電網の節 24073(区間 13409、22108)と確認した
  - 水: `test_build_line`(Water Pipe、[[743,1123],[745,1470]])は ok、5区間、cost 900、overlaps なし。前月の `water_trace`(743,1123)で、cell の water と sewage は true
  - 下水: `list_net_types`(service Sewage)は空。下水は水道管と同じ網で流れるとして、上の水の経路で確認した
  - 残る確認: 水のつなぎ口の位置。置いた後に ports で確かめる(中止する条件 b)
- 接続工事: Power Line 約0.21km(cost 520、維持費 約12/週)、Water Pipe 5区間(cost 900、維持費 約4/週)。道路は既存の 13359 を使い、新しい道は要らない
- 予備候補: なし。空き地3の別の候補(712,1644)付近は、名所 11580 と近く、同じ区画の確認が要る。今月は試していない
- 中止する条件: (a) 置くときの ok が false になる、(b) 置いた後の水のつなぎ口が (745,1470) から離れ、`test_build_line` で ok が出ないとき、(c) 置いた後の `water_trace` で、cell の water か sewage か電気が false のまま、(d) 市長が週320の枠を外さない(下の「判断の根拠」)。どれかで見送る
- 再調査の結果: 条件を満たした。`test_build_line`(Power Line、[[560,1480],[650,1480],[745,1480],[745,1492]])が ok。下水は水道管の網で、`test_build_line`(Water Pipe、[[743,1123],[745,1470]])が ok

### 期待する効果

- 改善の見込み: 観光の魅力度(attractiveness)の中心を、空き地3に増やす。空き地3の魅力度は、名所 11580 と公園 30466 のおかげで、平均26、最大140と高い。ただし 11580 の訪問は週2と少ない。名所を1棟足すと、周りの魅力度と訪問が増えると予想する。数値は見積もれない
- 数値と期限: 空き地3(745,1500、半径200)の魅力度の平均 26(確認した今の値)。Visitors の新棟は、今の値はなし。Tourism は 61/週(今の値)。期限は月末(30日目)。範囲は見積もれない
- 確認方法: `map_layer`(type=attractiveness、x=745、z=1500、radius=200、n=5)、`buildings_near`(service=Monument、x=745、z=1500、radius=200)で、新棟と 11580 の訪問、`economy_breakdown` の Tourism。見回り1、見回り2、月末に、同じ条件で比べる
- 不確かな点: 空き地3が観光客を呼ぶかは未確認(11580 の訪問が週2)。水と下水の届きは、つなぎ口を確かめて建てた後に `water_trace` で見る。維持費の増えは約1,616/週で、週の収支は +7,740 から約 +6,100 になる(守る線 +3,000 の上)。枠(週320)は超える
- 試し: あり。仮説: 名所を空き地3に置くと、周りの魅力度が上がり、観光客の訪問と Tourism が増える。測る数: 魅力度の平均(半径200)、新棟の Visitors、Tourism。場所: 空き地3(745,1500)。基準: 魅力度の平均 26、最大 140、11580 の訪問 週2、Tourism 61/週。編成方針の分からないこと「観光の名所や入口を足すと、観光客と Tourism が増えるか」に当たる

### 費用

- 建設費: 85,000(Observatory、`test_place_building`)+ 900(Water Pipe、`test_build_line`)+ 520(Power Line、`test_build_line`)= 86,420
- 週の維持費の増え: 1,600(Observatory、`list_building_types` の値)+ 約4(Water Pipe)+ 約12(Power Line、約0.21km × 60/週/km)≈ 約1,616

### 戻せるか

戻せる。取り壊すときは取り壊しの議決が要る。

### 前の月の答え合わせ

18月は案なし。40850 と noGoods を測り、道路下水道局と港湾空港局に求めた。今月の確認では、40850 は `net_reach`(1580、-530、半径300)で、道路の入口(accessSegment)が0のまま来られない。求めの返事は、この局では読まない。

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: あり
- 問い: 空き地3の魅力度は高いのに、名所 11580 の訪問が週2なのはなぜか。空き地3に名所を足して、訪問は増えるか。
- 見る道具と引数: `buildings_near`(service=Monument、x=745、z=1500、radius=300、brief=false)。`map_layer`(type=attractiveness、x=745、z=1500、radius=200、n=5)。`water_trace`(x=745、z=1500)
- いつ見るか: 見回り1、月末
- 何が分かれば次の手が決まるか: 11580 の訪問が増え、魅力度が高いままなら、空き地3は観光の候補として確かだ(案1を進める)。魅力度は高いが訪問が増えないなら、名所を足しても効きは薄い(案1を見送り、入口の案を待つ)。`water_trace` で空き地3の cell が sewage false のままなら、水と下水の管を先に決める
- 担当の問題: 5-1、5-2 観光

## 見たもの

- `list_policies`: 再調査で取得。観光の名所に効く政策は見当たらない。有効なのは SmokingBan(0)、EducationBoost(7,940/週)、BigBusiness(4,044/週)。政策の変更はしない
- `net_near`(745、1500、半径120、service=Electricity): 線の区間は0。空き地3の電線は、この半径では見えない
- `net_near`(745、1500、半径400、service=Electricity): 送電線の区間 20。始点 (560,1480) は節 24073 で、既存の送電網
- `net_near`(560、1480、半径30、service=Electricity): 区間 13409、22108(節 24073 でつながる)
- `net_reach`(745、1500、半径300): 道路8区間、来られない0、建物5件、来られない0。`net_reach`(1580、-530、半径300): 40850 は道路につながらない(accessSegment 0)
- `test_place_building`(Observatory、745、1500、facing west): ok、cost 85,000、道路 13359 距離1、wouldDemolish 0。再調査でも同じ結果
- `test_build_line`(Power Line、[[633,1575],[745,1500]]): 断られた。StatueOfWealth 11580 にぶつかる
- `test_build_line`(Power Line、[[727,1626],[745,1500]]): 断られた。Regular Park 30466 と Pedestrian Gravel にぶつかる
- `test_build_line`(Power Line、[[727,1626],[760,1520],[745,1500]]): 断られた。Pedestrian Gravel 29391、30868 にぶつかる
- `test_build_line`(Power Line、[[633,1575],[630,1530],[700,1500],[745,1500]]): 断られた。StatueOfWealth 11580 にぶつかる
- `test_build_line`(Power Line、[[560,1480],[650,1480],[745,1480]]): ok、4区間、cost 480、overlaps なし
- `test_build_line`(Power Line、[[560,1480],[650,1480],[745,1480],[745,1492]]): ok、5区間、cost 520、overlaps なし。採った経路
- `test_build_line`(Water Pipe、[[743,1123],[745,1470]]): ok、5区間、cost 900、overlaps なし
- `list_net_types`(service=Electricity、Sewage、Water、locked=false): Power Line 2,500/km・60/週/km、Water Pipe 2,500/km・10/週/km。Sewage は空
- `water_trace`(743、1123): 前月に確認。網は1つ。cell の water と sewage は true
- `water_trace`(762、1600、公園 30466): cell の water と sewage は false、網は0
- `map_layer`(attractiveness、745、1500、半径200、n=5): 平均 26、最小0、最大140(745,1300)
- `buildings_near`(service=Monument、半径8000): 10棟。空き地3の 11580(668,1565)、Fountain 41780、Servicing Services 40850 は道路につながらない
- `demand_breakdown`: 働き口 87,331、空き 3,559
- `economy_breakdown`: Tourism 61/週、PublicTransport 収入 4,999
- `zone_summary`(grid 1000): 道に面した空きは少ない(商業高密度の32マスだけ)
- `zone_map`(712、1644、半径400): 空き地3の北の列に、道路に面した空きがある(図のみ)

## 判断の根拠

- 担当の数字: 今いる観光客 1,795、訪問 150、Tourism 61/週、魅力度の平均 2、名所 10棟。入口は0のまま
- 40850 は、今月も道路につながらない。今月の計画(19月)の予定は「40850 が道に来られるかを測る」なので、測った結果、来られないと確かめた
- 入口は0のまま。名所の空きは、所有地の道に面する場所では見つからなかった。市中心は、道路と建物で試しが通らなかった(下の「捨てたもの」)
- 空き地3は、道路と電気に近く、水の本線から管が引ける(test ok、cost 900)。再調査で、電気も (560,1480) の既存の網から引ける経路を test で確かめた(ok、cost 520)。名所の置く場所として、一番現実的
- 案1は1件にした。ほかの名所は、建てる場所が道路と建物で塞がるか、維持費が大きいため
- 維持費と枠: 週320の枠は調整8の数字。調整15で戻り約4,800を枠に足したが、枠の総額は決めていない。Observatory の 1,604 は週320を超えるので、市長に枠を外すか判断してもらう。外さなければ、案1は見送る
- 守る線: 週の収支は +7,740 から約 +6,100 で、+3,000 の上に残る。所持金は 2,555,946 から 2,470,046 で、1,874,000 の上に残る

## 捨てたもの

- 市中心の名所(Transport Tower、Observatory の別の候補): `test_place_building` で、道路・建物と重なって ObjectCollision。除外した(1856,-238、1856,-488、2224,-322、1366,-448.5、2128,793、2623.8,890.4 など)。空いた候補を消すため、取り壊しは今月は使わない
- Transport Tower を空き地3に置く案: 維持費 960/週と安いが、m16 で同じ場所の案が維持費の超過で採られなかった。今月の天文台の試しに代える
- 40850 の道: 道路下水道局の担当。経済観光文化局は測るだけにする(計画の予定どおり)
- 旅客の入口(島B の駅など): 港湾空港局の担当。水管と電線の経路が、局の案と重なる(調整12)。この案には入れない
- 島の名所: 島に置くには橋が要り、`test_build_line` の結果を確かめていない。今月は空き地3を優先した
- 公園、事務所、貨物: 担当外、または編成方針の重点の外。今月は出さない
