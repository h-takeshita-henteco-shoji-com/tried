# m05 道路下水道局の案

## 施策

- 施策: 東の (3162, z) の南北の道(Basic Road 3区間、z=-372〜-210)を Small 4 Lane Road に差し替える試し。`upgrade_road` を使う
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 実行直前に `traffic(x=3154, z=-270, radius=150)` を測り、基準(flow 52、blocked 59、congestion 55、density 78)と同じかを見る
  2. `upgrade_road(prefab="Small 4 Lane Road", points=[[3162,-372],[3162,-300],[3162,-255],[3162,-210]], tolerance=10, pay=True, demolish=False)`
  3. 対象は区間 18692(z -372〜-300、56m)、12337(-300〜-255、27m)、5851(-255〜-210、26m)の3つ。戻り値の upgraded が3、demolishedBuildings が空かを見る
- 設置条件の確認:
  - `test_upgrade_road`(上と同じ引数、tolerance=10)は ok=true、matched 3、upgraded 3、skipped なし、demolishedBuildings なし、zonesKept=true
  - `net_near(3162,-270, radius=130, service="Road")` で3区間とも Basic Road(各1車線ずつ)と確認。東から入る道 30237・32517 は既に Small 4 Lane Road(2車線ずつ)で、この南北の1車線の道が細くなっている
  - `junction_info(3162,-270)` は node 26219(3162,-255)の3差路。信号なし、canEnableLights=true(今回は信号に手を付けない)
  - `zone_map(3162,-300, radius=200)` で、道の両側は住宅・商業・事務所の区画。同じ幅の種類への差し替えのため、建物は壊れない(`tool-reference.md`)
- 接続工事: 不要。既存の道を同じ幅の種類へ差し替える。費用は5,000/km × 約0.109km で約550(`list_net_types`)。維持費の差は Basic Road と同じ週40/km でほぼ0
- 予備候補: なし。短い区間 16182(3145,-390 〜 3162,-372、14m)は TooShort のおそれがあり、対象に含めない
- 中止する条件: 実行直前の `test_upgrade_road` が ok でない、skipped が出る、demolishedBuildings が1以上、または所持金が 2,082,287 を下回る場合は見送る。実行前の blocked が30未満なら基準が変わったので見送る

## 期待する効果

- 改善の見込み: 円 (3154,-270) は blocked 59 が街全体の約8%を占める。東から2車線で入る車が、南北の1車線の道に合流する所で詰まっていると見る。同じ形の差し替え(m04-2、x=450)は同じ円で blocked 84→7 と効いた。この道も差し替えで合流の容量が増えると予想する
- 数値と期限: `traffic(x=3154, z=-270, radius=150)` の blocked 59 → 30以下、congestion 55 → 45以下。期限は6か月目の月例(2050-06-01)。街全体の流れ(基準52%)は、この円が車の約1%なので動かない見込み
- 確認方法: 同じ道具・同じ円(x=3154, z=-270, radius=150)で blocked、congestion、averageDensity を測り、基準 59 / 55 / 78 と比べる
- 不確かな点: 差し替えた道の先(南の z=-390 側の Basic Road)が詰まりを引き継ぐおそれがある。詰まりの原因が合流でなく先の交差点なら、効かない。数値は上の範囲を局の見立てとして置く
- 試し: 仮説は「南北の1車線の道を4車線にすると、東から来た車が流れ、blocked が減る」。測る数は `traffic(x=3154, z=-270, radius=150)` の blocked と congestion。基準 59 / 55。場所は (3162,-372〜-210)。編成方針の「分からないこと」の項目ではない(担当の 6-3 の流れの手)

これは局の予測です。

## 調査

- 調査: あり
- 問い: 大きな道 Large Road の (-710,-737) で、交差点がないのに blocked 47 が続くのは、何で詰まっているのか
- 見る道具と引数: `traffic(x=-710, z=-737, radius=80)`、`buildings_near(x=-710, z=-737, radius=120, problem_only なし、brief=true)`(`problems_only=True`、service は省く)、`vehicles_stuck(kind="truck", limit=15)`
- いつ見るか: 見回り1、見回り2、月末
- 何が分かれば次の手が決まるか: blocked が毎回同じ約47台で、近くに建物の出入口やバス停があれば、それを手当てする案を出す。止まった車が特定の1か所の先頭にいれば、その先の道を差し替える案を出す。値が動き、blocked が一時的なら、案を出さず見るのをやめる
- 担当の問題: 6-3 公共交通を主軸とした交通体系

## 費用

- 建設費: 約550(5,000/km × 0.109km。`test_upgrade_road` の cost は0と返ったため、`list_net_types` の単価から見積もる)
- 週の維持費の増え分: ほぼ0(Basic Road も Small 4 Lane Road も週40/km)

## 戻せるか

戻せる。同じ `upgrade_road` で Basic Road に差し替えれば戻る(取り壊しは伴わない)。

## 前の月の答え合わせ

- m04-2(x=450 の10区間を Small 4 Lane Road にする試し): 採られて実行された(費用2,200)。編成方針によると、円 (521,-708) 半径300 の blocked は 84→7、congestion 67→51(予想は blocked 60以下)。判定は当たり。街全体の流れは52%のままで、全体には効かなかった。今月は同じ形の手を、別の詰まり (3154,-270) に使う
- 前の月の調査: 出していないので、なし(m04-survey-roads.md は存在しない)

## 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `traffic`: 街全体 flow 52、blocked 753、congestion 2,519。blockedSpots 上位は (-710,-737) 47、(3154,-270) 37、(1874,97) 35、(2173,-856) 31。(3154,-270) 半径150 は blocked 59、congestion 55、density 78。(-710,-737) 半径150 は blocked 54、density 89(Large Road 4区間、density 70〜100)
- `city_info`: 2050-05-01、所持金 2,133,798、週 +7,673、電気・水・下水が来ない 0/0/0、dialog null
- `list_policies`: 比較した政策は HeavyTrafficBan(無効、週0)、FreeTransport(無効、週0)。ほかの有効は EducationBoost 7,940、BigBusiness 4,092、IndustrySpace 4,821(渋滞に関係しない)。HeavyTrafficBan は地区にかける政策で、重いトラックを締め出すが、貨物が滞り 6-4・7-1 を悪くするおそれがあり、効き目の確認方法もないので、今月は差し替えを選んだ
- `net_near`: (-710,-737) 付近は Large Road 5区間(各3車線ずつ、node 5487 など)。(3162,-270) 付近は Basic Road 1車線ずつの南北の道と、Small 4 Lane Road の東西の道
- `junction_info`: (-722,-740) は40m以内に交差点なし。(3154,-270) の近くは node 26219、3差路、信号なし、canEnableLights=true
- `zone_map`: (3162,-300) 半径200。道の両側は住宅・商業・事務所の区画
- `test_upgrade_road`: Small 4 Lane Road で (3162,-372)〜(3162,-210)、tolerance=10 は ok、upgraded 3、skipped なし、壊れる建物なし
- `list_net_types`: Basic Road、Small 4 Lane Road とも5,000/km、週40/km

## 判断の根拠

流れの目標60%に対し街全体は52%で、blocked は753。詰まりの多い場所のうち (3154,-270) は、東の2車線が南北の1車線に合流する形で、差し替えが効く見込みがある。同じ形の x=450 の差し替えは blocked 84→7 と当たり、建設費も約550、建物も壊れない。(-710,-737) は交差点がなく原因が分からないので、案でなく調査にした。

## 捨てたもの

- (-710,-737) の Large Road の手当て: 交差点がなく、3車線で既に太い。原因が分からないため案にせず、調査にした
- HeavyTrafficBan: 週0だが、貨物を止めるおそれがあり、道路の流れへの効き目を測る道具の範囲を決められない
- (1874,97)、(2173,-856) の差し替え: 今月は場所の確認が (3154,-270) の1か所だけで、確認できていない場所は対象に含めない
- 電気・水・下水の施設: 0/0/0 で、水・下水の使用率は約80%と容量に余裕があり、当月の問題がない
