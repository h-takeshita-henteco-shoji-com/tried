# m05 道路下水道局の案

## 施策

- 施策: 交差点 (2155, 330) に信号を付ける(試し)。`set_traffic_lights(x=2155, z=330, active=True)`
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `junction_info(x=2155, z=330)` で node 4709、trafficLights false、canEnableLights true を見る
  2. `traffic(x=2155, z=330, radius=120)` で基準(blocked 26、averageDensity 86)を測り直す
  3. `set_traffic_lights(x=2155, z=330, active=True)`
  4. `junction_info(x=2155, z=330)` で trafficLights true を見る
  5. 見回り1・2と月末に手順2の `traffic` を同じ引数で測る
- 設置条件の確認:
  - `junction_info(x=2155, z=330)`: node 4709 は T字の交差点。segment 1374(bearing 90)、3990(270)、18(358)がつながる。trafficLights false、customLights false、canEnableLights true、canSetYield true
  - `net_near(x=2068, z=284, radius=150, service="Road")`: 3区間とも Small 4 Lane Road(各向き2車線)。道は広げ済みで、詰まりは交差点の捌き方にある
  - 鉄道との交差ではない(canEnableLights true)
- 接続工事: 不要
- 予備候補: (2110, 330) node 30603。`junction_info` で T字、canEnableLights true を確認済み。本体の信号が付けられないときだけ、`set_traffic_lights(x=2110, z=330, active=True)` を使う
- 中止する条件: 直前の `junction_info` で trafficLights が既に true、または canEnableLights が false なら見送る。基準の blocked が 10 未満に下がっていたら見送る

## 期待する効果

- 改善の見込み: 3区間(3990、18、1374)が密度95〜100で一点に集まり、信号のないT字で譲り合いが詰まって見える。信号で通る順番が決まれば、周りの止まった車が減ると予想する。逆に待ち行列が伸びて悪化する恐れもあり、効き目は分からない。
- 数値と期限: `traffic(x=2155, z=330, radius=120)` の blocked 26 → 15以下、averageDensity 86 → 75以下を月末までに。街全体の流れ54%は動かないか1ポイント未満と予想する
- 確認方法: 同じ `traffic(x=2155, z=330, radius=120)` の blocked、averageDensity、busiest の 3990・18・1374 の density を、見回り1・2と月末に比べる
- 不確かな点: 信号が詰まりを減らすか増やすかは見積もれない。周りの blockedSpot (2102, 292) の17台は交差点から約45m離れ、別の原因かもしれない。事務所の区画を足した周りで品物の車も通る
- 試し: 仮説は、3本の太い道が集まる信号のないT字に信号を付けると、待ち合いが減り周りの止まった車が減る。測る数は `traffic(x=2155, z=330, radius=120)` の blocked と averageDensity。場所は (2155, 330)。基準は blocked 26、averageDensity 86。編成方針の「分からないこと」の項目ではない(担当 6-3 の流れを動かす手の効き目を確かめる)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 費用

- 建設費: 0(信号の設置に費用の表示なし。`set_traffic_lights` は建設費を払う道具ではない)
- 週の維持費の増え分: 0(未確認だが、`list_net_types` の線の増設ではない)

## 戻せるか

戻せる。`set_traffic_lights(x=2155, z=330, active=False)` で外せる。

## 前の月の答え合わせ

前の月(m04)は案なし(局の案は採否の対象外)。調査も出さなかったので `m04-survey-roads.md` はない。m01-1(z=-950 の4車線化)は ObjectCollision で打てず、m02-1 の信号案は採られず、m03-1 の4車線化は衝突の事前確認ができず採られなかった。今月は道の幅ではなく信号で、衝突の恐れのない手に替えた。流れは 51% → 54% に上がった(バス台数の減りの月)。

## 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(`traffic` の流れ)
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `traffic`: 街全体 流れ54%、止まった車623、密度100の区間多数(2284 (3330, 330)、2282 (2234, -1132) ほか)。(2068, 284) 半径150 は blocked 56、averageDensity 81。(2155, 330) 半径120 は blocked 26、averageDensity 86、busiest は 3990・6523・18 が100
- `list_policies`: 比較した政策。HeavyTrafficBan(無効、週0)、FreeTransport(無効、週0)、EducationBoost(有効、7,940)、BigBusiness(有効、3,820)、Recycling(無効、週0)。HeavyTrafficBan は品物の車を止めて品物がない店230を悪くする恐れがあり採らない
- `city_info`: 2050-05-01、人口 177,734、所持金 2,261,923、来ない市民 0/0/0、dialog null
- `net_near`: (2068, 284) 半径150 の道22区間はすべて Small 4 Lane Road か Medium Road
- `junction_info`: (2155, 330) node 4709 T字、信号なし、設置可。(2110, 330) node 30603 T字、設置可。(2110, 240) node 24624 T字、設置可。(2110, 285) は交差点なし
- `buildings_near`: (2155, 330) 半径60 に6棟。店 3442 は NoGoods

## 判断の根拠

担当の数字は、来ない市民 0/0/0 で目標を保ち、流れ54%は目標60%に届かない。道の幅は (2068, 284) の周りで既に4車線で、広げる手は衝突で打てなかった実績がある。信号は費用0で戻せ、設置条件を確認できたので、試しとして出す。

## 捨てたもの

- 密度100の Basic Road(2284、2282 など)の4車線化: 衝突の事前確認ができず、過去2回 ObjectCollision で断られた。実行条件が未確認
- HeavyTrafficBan: 品物の車を止め、品物がない店230を悪くする恐れがあるため
- 水・下水・電気の増設: 容量の使用は76〜80%で、来ない市民は0。有効な手がない
- 道路の取り壊しや予算の変更: 効く見込みと確認方法が弱いため
