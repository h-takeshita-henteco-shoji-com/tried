# m01 経済観光文化局の案

## 施策

- 施策: 放棄された区画の建物(店・工場・住宅 計131棟)を、街全体で取り壊す。`bulldoze(x=0, z=0, radius=6000, what="abandoned")`。サービスの建物と道路は残る
- 議決: 取り壊し

## 実行計画

- 実行可否: 確認済み
- 対象と操作順: (1) 実行直前に `buildings_near(x=0, z=0, radius=6000, abandoned=true, brief=true)` で total が131前後か確かめる。(2) `bulldoze(x=0, z=0, radius=6000, what="abandoned")` を1回呼ぶ。(3) 実行後に `cargo` の shortages と `building_stats` の CommercialHigh の abandoned を読む
- 設置条件の確認: `preview_bulldoze(x=0, z=0, radius=6000, what="abandoned")` で、壊す建物131棟、失う働き口0、失う家0、道路の区間0、送電線の区間0、停電する建物0、水の施設0、駅・港0、modelAgreement 1.0。内訳は店・ホテルの多く、工場7、住宅5。ほとんどが NoGoods / NoResources の印がある
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: 実行前の preview で lost の jobs と homes が0でないとき。transportStations か waterFacilities が空でないとき。power.buildingsLosingPower が0でないとき

## 期待する効果

- 改善の見込み: 放棄された店は NoGoods の印を持ったまま残り、`cargo` の品物がない店228に数えられていると見る。壊せば、その数だけ数字が下がる。働き口は0の建物なので失わない
- 数値と期限: `cargo` の品物がない店 228 から、120〜150 に下がる見込み(放棄された NoGoods の店は一覧で約100棟)。原料がない工場 24 から、17前後。期限は実行から10日以内
- 確認方法: `cargo` の shortages.noGoods.buildings と noResources.buildings、`building_stats` の CommercialHigh の abandoned(今114)を、街全体で同じ条件で比べる
- 不確かな点: 根本の原因(貨物駅28755の品物が店に届かない)は直らない。残った店がまた放棄される可能性がある。放棄が印の数にどこまで入っているかは未確認。数値は見積もり。商業の需要が2と低いので、壊した場所に新しい店がすぐ建つ見込みは小さい
- 試し: 仮説は、放棄された建物を壊すと、品物がない店の印の数が下がる。測る数は `cargo` の noGoods と noResources。場所は街全体。基準は 228 / 24。編成方針の「分からないこと」とは別で、数字の中身を確かめる試し

## 調査

- 調査: あり
- 問い: 貨物駅28755の中でトラックが WaitingSpace のまま止まり続けるのは、出口の道が詰まっているからか
- 見る道具と引数: `vehicles_stuck(kind="truck", building=28755, limit=15)`、`traffic(x=3449, z=-1555, radius=300, limit=10)`、`cargo()`
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: bySeenStopped で同じ車が10日以上止まり、周りの道の density が高ければ、出口の道の拡幅(upgrade_road)か別の貨物駅(3529,-1555 の13893など、今は車0)への配分を来月に出す。止まる車が入れ替わっていれば、台数の問題として貨物駅を足す案を考える
- 担当の問題: 6-4、7-1 企業の立地、地場企業(8-1 に関わる)

## 費用

- 建設費: 0(取り壊しに費用の表示なし、払い戻しもなし)
- 週の維持費の増え分: 0

## 戻せるか

戻せない。取り壊しは元に戻せない。

## 前の月の答え合わせ

なし(1か月目)

## 市の計画

- 当たる施策: 6-4、7-1 企業の立地、地場企業(品物がない店・原料がない工場)
- 編成方針の重点に当たるか: 当たる

## 見たもの

- `list_policies`: 比較した政策。BigBusiness 有効・週3,876、SmallBusiness 無効・315、IndustrySpace 無効・4,821、EducationBoost 有効・7,940、税の政策(TaxRaise / TaxLower)無効・0。どれも品物がない店の数を直接減らす政策ではない
- `demand_breakdown`: 働き口86,175、空き3,215、失業7,911(大卒7,720)、空き家4,935
- `cargo`: トラック2,111、止まった802、貨物駅28755で492台(Goods 507台止まり)。品物がない店228、原料がない工場24
- `vehicles_stuck`: 貨物駅28755で589台。492台が WaitingSpace+Importing+InGrounds、62台が WaitingSpace+OnRoad。止まった期間は全部 1日未満(初回)
- `building_stats`: CommercialHigh 1,102棟のうち放棄114、IndustrialGeneric 806棟のうち放棄10、事務所のレベル3は3,227
- `net_near`: 貨物駅28755の周りは Large Road と Small 4 Lane Road。出口の詰まりは道の種類だけでは決められない
- `buildings_near`: 放棄された建物 total 136。内訳は NoGoods の店・ホテルが多数、NoResources の工場、Death・Fire の住宅・学校、StructureDamaged の電柱
- `preview_bulldoze`: radius 6000、what=abandoned。131棟、失う働き口0・家0、停電0

## 判断の根拠

品物がない店228のうち、放棄された店が一覧で約100棟ある。この棟は働き口0で、街の働き口を失わない。壊しても失うものは数字の上でなく、印の数が目標120に近づく。原因の貨物駅の詰まりは調査で追う。

## 捨てたもの

- 貨物駅28755の出口の道の拡幅: 詰まりの原因が未確認。調査の結果を見てから来月に出す
- 政策 SmallBusiness(週315): 品物がない店の原因は小さな店の数でなく、品物の流れ
- 政策 IndustrySpace(週4,821): 原料がない工場24に効く根拠が未確認
- 事務所や商業の税の引き下げ: 商業の需要が2で、働き口は不足でなく学歴のずれが原因とみる
- 観光(5-1、5-2)・事務所のレベル(6-1): 今月は品物の流れを先にした
