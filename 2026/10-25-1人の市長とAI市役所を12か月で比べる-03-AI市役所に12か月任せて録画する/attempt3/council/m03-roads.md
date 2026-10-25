# m03 道路下水道局の案

## 施策

- 施策: 1716,-771 の交差点(node 16205、Large Road と Medium Road の T 字)の信号を外す(試し)。道具は `set_traffic_lights(x=1716, z=-771, active=false)`
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 実行前に `junction_info(x=1716, z=-771)` を呼び、node 16205・trafficLights true・customLights false・canEnableLights true を確かめる
  2. 実行前に `traffic(x=1644, z=-770, radius=250)` を呼び、基準(blocked と blockedSpots、segment 36747 の density)を記録する
  3. `set_traffic_lights(x=1716, z=-771, active=false)`
  4. 実行直後に `junction_info(x=1716, z=-771)` で trafficLights が false になったか確かめる
  5. 見回り1・見回り2・月末に、2 と同じ引数の `traffic` で測る(調査と同じ)
- 設置条件の確認: `junction_info(1716,-771)` は node 16205、trafficLights true、customLights false(ゲームの自動の信号)、canEnableLights true、roads は 11126(Medium、bearing 357)、29888(Medium、177)、36747(Large、275)の3本。`net_near(1650,-770、r90、Road)` で3本の種類と車線数(Large は片側3車線、Medium は片側2車線)を確認した。建物は置かない。信号の外し方は `set_traffic_lights` で `tool-reference.md` を確認した
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: (a) 実行前の `junction_info` で trafficLights が false、または canEnableLights が false。(b) 実行前の `traffic(1644,-770、r250)` で 1644,-770 の blocked が 10 未満(詰まりが消えている)。(c) 実行直後の `junction_info` で trafficLights が false にならない。見回りで blocked が基準の2倍超(60以上)になったら、`set_traffic_lights(x=1716, z=-771, active=true)` で戻す

## 期待する効果

- 改善の見込み: 事実として、1644,-770 に止まった車が29台あり、直近の Large Road 36747(density 100)は片側3車線で、先の信号付き T 字(Medium 2本、片側2車線)へ流れ込む。信号の待ちが列の元なら、信号を外すと列が短くなると予想する(予想であり、確かめていない)。
- 数値と期限: `traffic(1644,-770、r250)` の blocked 38(うち 1644,-770 が29)、segment 36747 の density 100。予想は blocked 25 以下、36747 の density 90 未満。期限は月末(2050-04-01)。街全体の流れ(53%)は1ポイント以内の動きと見て、街全体の数は効き目の判定に使わない
- 確認方法: `traffic(x=1644, z=-770, radius=250)` を実行前、見回り1、見回り2、月末に同じ引数で呼ぶ。blocked、blockedSpots、segment 36747 の density を比べる
- 不確かな点: 前の月の s02-3 では、何もしなくても blocked が 28→48→21 と揺れた。1回の差では効きを見分けられない。信号を外すと Medium 側の車が入りにくくなり、列が南側(29888)へ移るおそれがある。効きの量は見積もれない。見回り2回と月末の3回が、基準より低い状態で続くかを見る
- 試し: 仮説「信号の待ちが Large Road 36747 の列の元なら、信号を外すと列が減る」。測る数は `traffic(1644,-770、r250)` の blocked と segment 36747 の density。場所は 1644,-770 付近。基準は blocked 38、1644,-770 が29、density 100。編成方針の「分からないこと」では「m01-3 で大型バスを減らしたとき、交通の流れや止まった車に効くか」の近くだが、直接の項目はない(信号の効きを測る)

これは局の予測です。ゲームの効果の正解を取得しません。

## 調査

- 調査: なし

## 費用

- 建設費: 0
- 週の維持費の増え分: 0

## 戻せるか

戻せる。`set_traffic_lights(x=1716, z=-771, active=true)` で信号を付け直せる。

## 前の月の答え合わせ

- m02-roads(2236,-950 と 2220,-950 の譲れの標識、試し)は採られなかった。理由は、止まった車が何もせず 86→24 と揺れ、効きを見分けにくいため、調査 s02-3 で揺れを先に測ること。
- s02-3 の結果: `traffic(2250,-950、r200)` の blocked は 28→48→21。1か月内でも2倍以上揺れ、1回の比べでは効きを見分けられない。点も 2309,-925 から 2160,-877、2179,-846 と動いた。次の手: 同じ場所の標識案は出さない。今月は止まった車の列が1点に29台と固まる 1644,-770 を選び、基準を実行前・見回り1・見回り2・月末の4回測る
- m01-1(4車線化)は打てなかった(upgraded 0)。今月も再提出しない。区間 36011 は9mで TooShort だった。

## 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `traffic`: 街全体 flow 53、cars 7,508、blocked 688、congestion 2,495。blockedSpots 上位は -1675,-1302 が30、1644,-770 が29、530,-706 が28。(1644,-770、r250)は flow 53、cars 176、blocked 38、1644,-770 が29、1580,-765 が8。segment 36747(Large、1673,-768)density 100、29888(Medium、1718,-815)95、3113(Medium、1779,-916)94、10331(Large、1605,-762)92
- `list_policies`: 比べた政策は HeavyTrafficBan(無効、0)、FreeTransport(無効、0。切符の収入が0になる)。HeavyTrafficBan は地区の指定が要り、重い車の止まる場所の根拠がないので見送った。PowerSaving・WaterSaving(無効、各58,373)は担当の問題(電気・水・下水の不足 0)に効かないので見送った。有効なのは EducationBoost(7,940)と BigBusiness(3,900)で、担当外
- `city_info`: 人口178,630、週の収入341,780・支出333,745(+8,035)、citizensWithoutService 0/0/0、dialog null
- `net_near`: (1650,-770、r90、Road)5区間。3327・10331・36747 は Large Road(片側3車線)、11126・29888 は Medium Road(片側2車線)
- `junction_info`: (1716,-771)node 16205、trafficLights true、customLights false、canEnableLights true、canSetYield false。(1642,-765)は40m以内に交差点なし
- `citizens_without_service`: water は residents 0、homes 0

## 判断の根拠

3-3 は来ない市民が 0/0/0 で、目標を保っている。6-3 は流れ 53% で目標60%まで7ポイント遠い。止まった車が1点に29台固まる 1644,-770 は、先の信号付き T 字の列と見た。信号の外しは費用0で戻せ、建設の確認も要らない。揺れが大きいので試しとして出し、見回りごとに同じ引数で測る。

## 捨てたもの

- 1716,-771 の譲れの標識: canSetYield が false で、信号を外さないと付けられない。信号を外す案に含めた
- 2236,-950 付近の譲れの標識(前月案): s02-3 で止まった車が 28→48→21 と揺れ、効きが見分けられない
- 2160〜2280,-950 の4車線化(m01-1): 区間 36011 が9m で TooShort、実行条件を満たせない
- HeavyTrafficBan、FreeTransport などの政策: 止まる場所の根拠がない、または収入が減る。電気・水・下水は不足 0 で、追加の手は不要
- 電気・水・下水の施設の追加: 容量に余裕があり(電気 1,708,832/2,492,896、水 1,920,000/2,520,000、下水 1,917,696/2,400,000)、来ない市民 0
