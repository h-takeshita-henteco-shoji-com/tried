# m06 道路下水道局の案

## 施策

- 施策: 交差点 (2155, 330) に信号を付ける(試し)。`set_traffic_lights(x=2155, z=330, active=True)`
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `junction_info(x=2155, z=330)` で node 4709、trafficLights false、canEnableLights true を見る
  2. `traffic(x=2155, z=330, radius=120)` で基準(blocked 22、averageDensity 89)を測り直す
  3. `set_traffic_lights(x=2155, z=330, active=True)`
  4. `junction_info(x=2155, z=330)` で trafficLights true を見る
  5. 見回り1・2と月末に手順2の `traffic` を同じ引数で測る
- 設置条件の確認:
  - `junction_info(x=2155, z=330)`(今月): node 4709 は T字。segment 1374(bearing 90)、3990(270)、18(358)がつながり、すべて Small 4 Lane Road。trafficLights false、customLights false、canEnableLights true、canSetYield true
  - 道は既に各向き2車線なので、差し替えの衝突(過去 ObjectCollision)は起きない。道路は変えない
- 接続工事: 不要
- 予備候補: (2110, 330) node 30603。今月の `junction_info` で T字(segment 3990、22887、26735)、trafficLights false、canEnableLights true を確認済み。本体の信号が付けられないときだけ `set_traffic_lights(x=2110, z=330, active=True)` を使う。基準は同じ `traffic` を (2110, 330) 半径120 で測り直す
- 中止する条件: 直前の `junction_info` で trafficLights が既に true、または canEnableLights が false なら予備へ。基準の blocked が 10 未満なら見送る

## 期待する効果

- 改善の見込み: 3区間が密度100で一点に集まり、信号のないT字で譲り合いが詰まっていると見る。信号で通る順番が決まれば、周りの止まった車が減ると予想する。逆に待ち行列が伸びて悪化する恐れもある。
- 数値と期限: `traffic(x=2155, z=330, radius=120)` の blocked 22 → 15以下、averageDensity 89 → 80以下を月末までに。街全体の流れ52%は動かないか1ポイント未満と予想する(街全体への効きは数値を見積もれない)
- 確認方法: 同じ引数の `traffic` の blocked、averageDensity、busiest の 18・22887 など密度の変化を、見回り1・2と月末に比べる
- 不確かな点: 信号が詰まりを減らすか増やすかは見積もれない。blockedSpot (2220, 291) の19台は交差点から約70m離れ、別の原因かもしれない。悪化したら `set_traffic_lights(x=2155, z=330, active=False)` で戻す
- 試し: 仮説は、3本の太い道が集まる信号のないT字に信号を付けると、待ち合いが減り周りの止まった車が減る。測る数は `traffic(x=2155, z=330, radius=120)` の blocked と averageDensity。場所は (2155, 330)。基準は blocked 22、averageDensity 89。編成方針の「分からないこと」の項目ではない(担当 6-3 の流れの手の効き目を確かめる)

これは局の予測です。

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 費用

- 建設費: 0(`set_traffic_lights` は建設費を払う道具ではない)
- 週の維持費の増え分: 0(未確認。線の増設ではない)

## 戻せるか

戻せる。`set_traffic_lights(x=2155, z=330, active=False)` で外せる。

## 前の月の答え合わせ

m05 の信号案は採られなかった(信号の効きが見積もれず、バス台数の手を先にした)。`m05-survey-roads.md` はない(調査を出さなかった)。流れは 54% → 52% に下がり、道の詰まりは残っている。今月は同じ交差点の案を、基準を測り直して再提出する。

## 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(`traffic` の流れ)
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `list_policies`: 比較した政策。HeavyTrafficBan(無効、週0)、FreeTransport(無効、週0)、EducationBoost(有効、7,940)、BigBusiness(有効、3,760)、Recycling(無効、週0)。道の詰まりに直接効く政策はない。HeavyTrafficBan は品物の車を止め、品物がない店を悪くする恐れがあるので採らない
- `traffic`: 街全体 流れ52%、止まった車846、密度100の区間多数。blockedSpots 上位は (2686, 306) 61、(2298, -924) 56。(2155, 330) 半径120 は blocked 22、averageDensity 89、busiest は 13553・6523・22887・16291・18 が100
- `city_info`: 2050-05-31、人口 177,224、来ない市民 0/0/0、所持金 2,332,440、dialog null
- `junction_info`: (2155, 330) node 4709 T字、信号なし、設置可。(2110, 330) node 30603 T字、信号なし、設置可
- `tool-reference.md`: `set_traffic_lights(x, z, active)` の引数を確認

## 判断の根拠

電気・水・下水が来ない市民は 0/0/0 で目標を保つ。流れは 52% で目標60%に遠い。道の差し替えは過去に衝突で断られ、衝突の事前確認ができない。信号は費用0で戻せ、設置条件を今月も確認できたので、試しとして出す。

## 捨てたもの

- 密度100の Basic Road(11218 (-1245, -528) など)の4車線化: 衝突の事前確認ができず、過去 ObjectCollision で断られた。実行条件が未確認
- HeavyTrafficBan: 品物の車を止め、品物がない店を悪くする恐れがあるため
- バス路線の台数の変更: 港湾空港局の担当と重なり、交通の流れの手はそちらで出ている
- 水・下水・電気の増設: 使用は容量の約70〜80%以下で、来ない市民は0。有効な手がない
