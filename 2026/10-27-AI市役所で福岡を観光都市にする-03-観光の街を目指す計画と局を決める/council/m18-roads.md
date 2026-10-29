# m18 道路下水道局の案

## 案1: 止まりの多い幹線 z=10 を4車線にする(試し)

### 施策

- 案の id: roads-1
- 施策: 幹線 z=10(x 1356〜1560)の Basic Road 3区間を Small 4 Lane Road にする。場所は (1424〜1560, 10) 付近。道具は `upgrade_road`
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `upgrade_road`(prefab="Small 4 Lane Road", points=[[1356, 10], [1560, 10]], tolerance=20, pay=true, demolish=false)。1回で3区間を差し替える。区間の番号は 23676(x 1356→1424)、21699(x 1424→1492)、29499(x 1492→1560)
- 設置条件の確認: `test_upgrade_road`(同じ引数)で matched 3、upgraded 3、skipped 0、cost 0、demolishedBuildings 0、zonesKept true。`net_near`(x 1480, z 50, r 90)で3区間の種類(Basic Road、carLanes 1 対 1)を確認。信号の交差点 (1560,10)(node 30875、trafficLights true)は触らない
- 接続工事: 不要
- 予備候補: なし。試しの道具が断ったら見送る
- 中止する条件: 実行前に `test_upgrade_road` を取り直し、skipped が1つでもある、cost が0でない、demolishedBuildings が1つでもある、のいずれかなら見送る

### 期待する効果

- 改善の見込み: 1車線ずつの Basic Road 3区間の密度が 100(`traffic` busiest の確認)で、交差点 (1560,10) へ向かう流れを絞っていると見る。4車線にすると流入が増え、近くの止まりが減ると予想する。確認した事実は、3区間が1車線ずつであることと、密度 100 であること
- 数値と期限: 基準は `traffic`(x 1497、z 62、r 200)の blocked 67(その中心の止まり 43)、街全体の流れ 55%。効きの量は見積もれない。期限は次の月の月末
- 確認方法: `traffic`(x 1497、z 62、r 200)の blocked と blockedSpots(1497,62)、`traffic` の flow。今の値と同じ引数で比べる。止まりは見回りごとに揺れるため、月末の1回で判定せず、見回りの値も見る
- 不確かな点: 4車線化は、ほかの場所で効いたものと増えたものがある(m07-3、m09-2 の見立て)。下流の交差点の容量が足りなければ効かない。効きは数値で見積もれない
- 試し: 仮説: 1車線の幹線が、信号の交差点 (1560,10) の手前で詰まりを作っている。4車線化で、その詰まりが減る。測る数: `traffic`(x 1497、z 62、r 200)の blocked。場所: x 1356〜1560、z 10 の幹線と、その北の (1497,62) 周り。基準: blocked 67、流れ 55%。編成方針の「分からないこと」の「信号の効きの揺れ」に当たる

### 費用

- 建設費: 0(`test_upgrade_road` の cost 0)
- 週の維持費の増え分: 0(Basic Road と Small 4 Lane Road は、どちらも 40/km。区間の合計 約191m)

### 戻せるか

戻せる。`upgrade_road` で Basic Road に戻せる(費用0)。

### 前の月の答え合わせ

- m17-roads-2(送電線の網を名所 11580 と公園 30466 につなぐ、採用・実行済み): 予想は第18月末に電気が届く。結果は、両方の `buildings_near`(x 712、z 1644、r 150)で grid.electricity が true。当たり。両方とも Visitors last week 2。電気の苦情(complaints の Electricity)もなし
- m17-roads-1(交差点 (2155,330) の信号、採用・実行済み): 予想は東の止まりが減る。今月の `traffic`(x 2200、z 260、r 150)は blocked 35、流れ 55%。基準の値を台帳に残していないため、判定前
- m17-roads-3(FreeTransport を外す、採用・実行済み): 予想は運賃収入の戻り約4,800。結果は PublicTransport の収入 4,994(市政ノートの 2051-06-05)。当たり。流れは 52 から 55 に動いたが、1か月の測りで、ほかの変化と切り分けていない

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1・5-2、8-1・6-4、4-4)。6-3 の局の担当の数字として出す

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `city_info`: 人口 175,384、所持金 2,531,972、週の収支 +10,007(収入 338,572、支出 328,565)、観光客 1,783(訪問 159)、電気・水・下水が来ない市民 0 / 0 / 0、dialog なし
- `list_policies`: policyExpensesPerWeek 10,903。SmokingBan(有効、0)、EducationBoost(有効、7,940)、BigBusiness(有効、3,936)。FreeTransport は外れている(0)。HeavyTrafficBan は外れている(0)。SmallBusiness は外れている(313)、RecreationalUse は外れている(0)。交通の流れに効く政策は、今は有効なものがない
- `traffic`(街全体): flow 55、cars 7,490、blocked 896、congestion 2,266。busiest は density 100 の区間が続く(Basic Road 24595(2484,650) ほか)。blockedSpots の上位は (1497,62) 43、(4054,-517) 36、(2290,-950) 36
- `traffic`(x 1497、z 62、r 200): flow 55、blocked 67、congestion 51、blockedSpots (1497,62) 43、(1349,137) 23
- `traffic`(x 2200、z 260、r 150): flow 55、blocked 35、congestion 47、blockedSpots (2108,305) 16、(2255,318) 15
- `junction_info`(1497,62): 40m以内に交差点なし。`junction_info`(1492,10): 40m以内に交差点なし。`junction_info`(1458,10): 40m以内に交差点なし。`junction_info`(-1097,-694): 40m以内に交差点なし
- `junction_info`(1560,37): node 30875(1560,10)、trafficLights true、customLights false、canEnableLights true
- `net_near`(x 1480、z 50、r 90): 区間 23676、21699、29499 は Basic Road(carLanes 1 対 1)、15742 は Small 4 Lane、14033 と 11179 は Medium Road(z=100)
- `test_upgrade_road`(Small 4 Lane Road、[[1356,10],[1560,10]]): ok、matched 3、upgraded 3、skipped 0、cost 0、demolishedBuildings 0
- `test_upgrade_road`(Large Road、[[1378,100],[1535,100]]): matched 2、upgraded 1。区間 11179 は ObjectCollision(29774 Crematory、(1500,124)、blocks true)で飛ばす。cost 200
- `list_net_types`(Road、locked=false): Basic Road 5,000 / 40、Small 4 Lane Road 5,000 / 40、Large Road 10,000 / 120、Medium Road 7,500 / 100(いずれも 1km あたり、建設費 / 週の維持費)
- `zone_summary`(grid 1000): Office の空き 1,642(emptyFacingRoad 0。すべて道に面していない)、ResidentialHigh の空き 747(facingRoad 0)、CommercialHigh の空き 469(facingRoad 36)
- `zone_map`(x -1000、z -500、r 700): 道路で区切られた街区が並ぶ。事務所の空きの量は、`zone_summary` の tiles で見た(空きが多いのは (-500,-500) の197、(-1500,-500) の187)
- `buildings_near`(x 712、z 1644、r 150): 11580 StatueOfWealth(668,1565)、grid.electricity true、Visitors last week 2。30466 Regular Park(762,1600)、grid.electricity true

## 判断の根拠

- 6-3 の担当で、確かめた候補は1つだけ残った。(1497,62) の止まりは、交差点のない幹線の密度 100 の区間に近く、信号の手は使えない。4車線化は試しの道具が通り、費用と維持費は0で、戻せる
- 事務所の道(6-1)は、空きが道に面していないことを確かめた。道を通す効きは見込めるが、区間の受け渡しを経済観光文化局から受けた記録がなく、確かめられない。実行の条件が未確認なので、案にしない
- 名所 11580 と公園 30466 の電気は届いた。事業2は完了し、今月は新しい手を出さない
- 案は1件。6-3 の残りの手は、必須の条件が未確認か、同じ手の繰り返しになるため

## 捨てたもの

- 事務所の空きに面する道(6-1): 空きは道に面していないと確かめた。ただし、区間を経済観光文化局から受けた記録がなく、実行可否が未確認のため。次の月に、受け渡しを経済観光文化局に確かめる
- 交差点 (1497,62) の信号: 40m以内に交差点がないため、信号は付けられない
- 幹線 z=100 の Large Road(区間 11179 を含む、`test_upgrade_road`): 区間 11179 が Crematory 29774 にぶつかる。火葬場は取り壊しの対象にしないため、見送る。試しの費用は 200
- 政策 HeavyTrafficBan(費用0): 貨物の車を減らし、8-1 と 6-4 の目標(品物がない店 191、原料がない工場 31)に逆らう見込み。政策は月1件の上限もあり、今月は出さない
- 信号 (2155,330) の効きの判定: 基準を台帳に残していないため、今月は判定前。別の信号を足すのは、判定の後
