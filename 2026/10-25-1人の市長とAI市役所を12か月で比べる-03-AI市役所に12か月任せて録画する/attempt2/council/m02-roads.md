# m02 道路下水道局の案

## 施策

- 施策: 東西の道 z=-950 の交差点 (2236, -950)(node 5405)に信号を付ける(試し)。`set_traffic_lights` を使う
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `junction_info(x=2236, z=-950)` で trafficLights=false、canEnableLights=true を見る
  2. `set_traffic_lights(x=2236, z=-950, active=True)`
  3. 見回りと月末に `traffic(x=2236, z=-950, radius=60)` を測る
  4. 悪化したら `set_traffic_lights(x=2236, z=-950, active=False)` で外す
- 設置条件の確認: `junction_info(2236, -950)` で node 5405 は 3方向(segment 3334 東、36011 西、10391 北)、信号なし、canEnableLights=true。`junction_info(2220, -950)` の node 30823 も同じく付けられるが、今月は1か所だけにする
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: 実行前の `junction_info` で canEnableLights が false、または信号がすでにあるとき見送る

## 期待する効果

- 改善の見込み: 前月、道を広げる手(`upgrade_road`)が打てなかった。`net_near` で 36011(9m)は短すぎ、3334 と 19196 は沿道の建物(店・事務所・工場)にぶつかる。広げると働き口が減るため今月は使わない。この交差点では 15 台が (2248, -955) で止まっており、車が譲り合えず詰まっている可能性がある。信号で入る順を決めれば減るかもしれない
- 数値と期限: `traffic(x=2236, z=-950, radius=60)` の blocked 16、averageDensity 100(今の値)。予想は blocked 16 → 8 以下。期限は月末。街全体の flow 51% は動かないか1ポイント未満と予想する
- 確認方法: 同じ円(x=2236, z=-950, radius=60)の `traffic` の blocked と averageDensity を、見回り1・2と月末に比べる
- 不確かな点: 信号が詰まりを減らすか、待ち行列を逆に伸ばすかは分からない。近い交差点 (2220, -950) との間は16mで、信号が連動せず悪化する恐れがある。数値は見積もれない。悪化したら外す
- 試し: 仮説は、近接した3方向交差点に信号を付けると、譲り合いの詰まりが減り blocked が減る。測る数は `traffic(x=2236, z=-950, radius=60)` の blocked と averageDensity。場所は (2236, -950)。基準は blocked 16、averageDensity 100。編成方針の「分からないこと」の項目ではない

## 調査

- 調査: なし

## 費用

- 建設費: 0(`set_traffic_lights` は費用の記載なし。道具の説明に費用の項はない)
- 週の維持費の増え分: 0(確認できた範囲。道具の説明に維持費の項はない)

## 戻せるか

戻せる。`set_traffic_lights(active=False)` で信号を外せる。

## 前の月の答え合わせ

m01-1(z=-950 の3区間を4車線に)は打てなかった(skipped: 3334・19196 ObjectCollision、36011 TooShort)。測る数は動いていないので判定なし。今月 `buildings_near(x=2230, z=-950, radius=70)` で、道沿いに店 L2 Shop08(45225)、事務所 Office07(10916)、工場 14595 などが並ぶと確かめた。広げると壊れる見込みで、働き口を減らす。そこで今月は広げずに、信号の試しに替えた。調査 m01-survey-roads.md はなかった。

## 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(流れ)
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `traffic`: 街全体 flow 51%、blocked 1,027、congestion 2,587。(2240, -950, 半径200)は blocked 33、密度80。(2236, -950, 半径60)は blocked 16、密度100、blockedSpots は (2248, -955) に15台
- `list_policies`: 比較した政策は HeavyTrafficBan(無効、週0)、FreeTransport(無効、週0)、EducationBoost(有効、7,940)、BigBusiness(有効、3,896)。流れに直接効く確かな政策は見当たらない。HeavyTrafficBan は工業の荷物の車を減らす見込みだが、品物の流れを止めうるので今月は出さない
- `city_info`: 2050-01-31、来ない市民 0/0/0、週の収支 +9,798、所持金 2,121,650
- `net_near`(x=2240, z=-950, 半径200, Road): 3334(24m)、19196(32m)、36011(9m)が Basic Road。前後は Small 4 Lane Road
- `junction_info`(2236, -950)(2220, -950): 両方 信号なし、canEnableLights=true、canSetYield=true
- `buildings_near`(x=2230, z=-950, 半径70, brief): 20棟。12882 は焼け、14595 は NoResources
- `tool-reference.md`: `set_traffic_lights`、`upgrade_road` の引数を確認

## 判断の根拠

担当の電気・水・下水は 0/0/0 で守れている。流れ 51% の最大の詰まりは z=-950 の絞られた区間で、広げる手は建物を壊すため働き口の重点と食い違う。費用0で戻せる信号の試しなら、枠に収まり、効き目の分からない手を安全に測れる。

## 捨てたもの

- `upgrade_road(demolish=True)` で 3334・19196 を広げる: 沿道の店・事務所を壊し、`preview_bulldoze` で失う働き口を見積もっていない。働き口が重点なので今月は出さない
- 政策 HeavyTrafficBan: 荷物の車が減り、品物がない店が増える恐れがある
- 他の渋滞地点((2107, 310) blocked 56 など): 道路の種類・交差点・沿道を今月は確認していない。実行条件を確認していないため対象にしない
- 水・下水・電気の増設: 来ない市民は 0。水の使用は容量の76%、下水80%で足りている
