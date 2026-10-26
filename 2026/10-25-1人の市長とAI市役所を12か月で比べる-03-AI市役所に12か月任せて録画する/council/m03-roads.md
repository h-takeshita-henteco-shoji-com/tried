# m03 道路下水道局の案

## 施策

- 施策: (2236,-950) の3差路(node 5405)に信号を付ける試し。道具は set_traffic_lights。
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順: `set_traffic_lights(x=2236, z=-950, active=true)` を1回。効かなければ(または blocked が増えたら)月末に `set_traffic_lights(x=2236, z=-950, active=false)` で外す
- 設置条件の確認: `junction_info(2236,-950)` で node 5405、canEnableLights=true、trafficLights=false、入る区間は 3334(bearing 90)、36011(270)、10391(0)の3本。いずれも Basic Road、yield なし
- 接続工事: 不要
- 予備候補: 隣の node 30823 (2220,-950)。`junction_info(2220,-950)` で canEnableLights=true、trafficLights=false。5405 と 16m しか離れないため、両方には付けない。5405 で悪化したときだけ、5405 を外してからこちらを試す
- 中止する条件: 実行前の `junction_info(2236,-950)` で canEnableLights が false、または既に信号がある場合は見送る

## 期待する効果

- 改善の見込み: この3差路は 2月10日・20日・月末の3回とも、周りの Basic Road 区間(3334、36011、19196、10391 側の 20293)が density 100 で、止まった車が出ている。南北の道 10391 と東西の道が信号なしで合流するため、信号で順番を決めれば流れが整うと予想する。
- 数値と期限: `traffic(x=2237, z=-936, radius=150)` の今の値は flow 54、blocked 21、congestion 47、averageDensity 92。予想は blocked が15以下。数値は見積もれない。確かめる期限は30日後の月末。
- 確認方法: 同じ円で `traffic` を見回り1・2と月末に呼び、flow・blocked・congestion を今の値と比べる。街全体の flow(今 54%)も記録するが、効き目の判定には使わない。
- 不確かな点: 16m先の node 30823 との間に車が詰まり、かえって悪くなるおそれがある。道幅を広げる案は、短すぎる区間 36011(16m)が TooShort で断られ、他の道は建物にぶつかるため出せない。
- 試し: 仮説は「信号を付けると、3差路で車が順に進み、blocked が減る」。測る数は `traffic(x=2237, z=-936, radius=150)` の blocked と congestion。場所は (2236,-950) 周辺。基準は blocked 21、congestion 47。編成方針の分からないことの外だが、6-3 の流れ(54%、目標60%)に当たる。

これは局の予測です。ゲームの効果の正解を取得しません。

## 調査

- 調査: なし

## 費用

- 建設費: 0(信号に建設費は付かない。`economy_breakdown` では未確認)
- 週の維持費の増え分: 0 と見込む(未確認)

## 戻せるか

戻せる。`set_traffic_lights(active=false)` で外せるため。

## 前の月の答え合わせ

前月(m02)の道路下水道局は案なし、調査 s02-2 のみ。調査の結果は、4車線から2車線に絞られる3区間のうち 19196 と 36011 は3回とも busiest に出て、3334 は出なかった。blocked は 22→13→21 で、詰まりは続いた。次の手として拡幅を調べたところ、`test_upgrade_road`(Small 4 Lane Road、点 2280→2160)は 36011 が TooShort、3334 と 19196 は 36011 とぶつかり断られた。`test_build_line` で壊してから引き直す形も TooShort で断られた。このため、今月は拡幅を捨てて信号の試しにした。

## 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `traffic`: 街全体 flow 54、cars 7,773、blocked 646。blockedSpots 上位 (-925,-702) 34、(2074,289) 33、(2141,-853) 32。円 (2237,-936) r150 は flow 54、blocked 21、congestion 47、density 92。円 (2160,-860) r150 は blocked 57
- `city_info`: 流れではなく、電気・水・下水が来ない市民 0/0/0。所持金 2,113,828。週 +7,337
- `list_policies`: 比較した政策は PowerSaving(無効、58,353)、WaterSaving(無効、58,353)、HeavyTrafficBan(無効、0)、FreeTransport(無効、0)。道路の流れに直接効く政策は HeavyTrafficBan のみ。商工業の地区の貨物を止めるおそれがあり、品物がない店 178 を悪くするので選ばない
- `net_near`: z=-950 の道は Small 4 Lane Road が並ぶが、2280→2160 の間だけ Basic Road(3334 長さ24、36011 約16、19196 長さ32)
- `list_net_types`: Small 4 Lane Road は 5,000/km、Medium Road は 7,500/km
- `test_upgrade_road`: 2280→2160 の Small 4 Lane Road は3区間とも断られた(36011 TooShort。3334・19196 は 36011 とぶつかる)。(2236,-950)→(2236,-860) は 20293 が Fire House 32853 と Medical Clinic 32923 にぶつかり、10391 は 36011 などとぶつかる。Medium Road は建物8棟にぶつかる
- `test_build_line`: 36011 など3区間を壊したと仮定して Small 4 Lane Road で引き直す形は TooShort で断られた
- `preview_bulldoze`: (2228,-950) 半径5 の道は1区間、失う家と働き口は0
- `junction_info`: node 5405 と node 30823 とも、canEnableLights=true、信号なし

## 判断の根拠

3か月続けて同じ場所が詰まり、街全体の流れは 54% で目標 60% に届かない。道幅を広げる手は、ゲームの道具が断るため出せない。信号は費用がかからず戻せるので、局として試す価値があると見た。効き目は見積もれないため、試しとして出す。

## 捨てたもの

- 2280→2160 を Small 4 Lane Road にする拡幅: TooShort で断られた。
- 壊してから引き直す案: TooShort で断られた。取り壊しの議決も要る。
- 20293 の拡幅: 消防署と診療所を壊すため、失うものが大きい。
- HeavyTrafficBan: 品物がない店 178 を悪くするおそれがある。
- 電気・水・下水: 来ない市民は 0/0/0 で、有効な手を要しない。
