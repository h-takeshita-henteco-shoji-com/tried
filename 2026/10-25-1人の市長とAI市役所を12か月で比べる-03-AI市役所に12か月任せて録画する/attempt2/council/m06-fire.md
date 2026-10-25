# m06 消防局の案

## 施策

- 施策: 火事の印が残る焼けた事務所3棟(10582、19149、24230)を、bulldoze(what="building")で取り壊す
- 議決: 取り壊し

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 直前に `buildings_near(x=2941, z=1335, radius=300, problem="Fire")` で3棟が Fire, FatalProblem のままか見る
  2. `bulldoze(x=2961, z=1286, radius=5, what="building")` で 10582 (H2 3x2 Office08)
  3. `bulldoze(x=2981, z=1286, radius=5, what="building")` で 24230 (H2 2x2 Office08)
  4. `bulldoze(x=2882, z=1434, radius=5, what="building")` で 19149 (H2 2x2 Office04)
  5. 各回で removedBuildings が1で、id が上の番号かを見る。`complaints` で火事の印を見る
  - 19320 (3130, -320) の店は働き口6が働いており、MajorProblem のため対象に入れない
- 設置条件の確認: `preview_bulldoze`(what="building", radius=5)を3棟それぞれに実行。どれも targets 1、jobs 0、homes 0、segments 0、停電0、水の施設・駅なし、modelAgreement 1.0。`buildings_near(problem="Fire")` で3棟とも electricity・water・sewage が来ており、Fire, FatalProblem
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: 直前の `buildings_near` で3棟のいずれかの Fire が消えている、または bulldoze の removedBuildings が2以上、または id が違う場合は、その1棟を見送る。働き口や家を持つ建物が混ざったら見送る

## 期待する効果

- 改善の見込み: 3-4 の火事の印4のうち3つは、焼けた事務所(働き口0)に残っている。壊すと印が数えから外れ、火事は1(店19320)に減ると予想する。ただし m02 で壊した焼け跡も、別の建物の火事で新しい印が付いた。
- 数値と期限: `complaints` の火事 4 → 1、犯罪 1 のまま。合計 5 → 2(目標4以下)。期限は月末(見回り1で確認)
- 確認方法: `complaints` の Fire と Crime の buildings。同じ道具、街全体で比べる
- 不確かな点: 新しい火事が月内に起きれば数は戻る。消防署の増設ではなく、残った焼け跡を片づける手であり、火事そのものを減らす効果は見積もれない。犯罪は港32211の1件で、手は打たない
- 試し: なし

## 調査

- 調査: なし

## 費用

- 建設費: 0(bulldoze は費用0。m02 の実行で所持金が変わらなかった)
- 週の維持費の増え分: 0

## 戻せるか

戻せない。取り壊しは元に戻せないが、壊すのは働き口0・家0の焼けた建物だけである。

## 前の月の答え合わせ

- m05-fire(焼けた事務所19149を取り壊す): 採られなかった(理由は、目標との差が1と小さく、施策の枠を重点に使ったため)。今月は火事の印が焼けた事務所3棟(10582、19149、24230)に増えたので、3棟に広げて出し直す。`complaints` の火事は 4 のまま、犯罪は 3 → 1 に減った。合計 5。前の月の調査 `m05-survey-fire.md` はない(調査を出していない)

## 市の計画

- 当たる施策: 3-4 日常生活の安全・安心
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `complaints`: 印のある建物479。火事4(事務所10582、19149、24230と店19320)、犯罪1(Cargo Harbor 32211)、ごみ146、品物なし239、汚染45
- `events`: 0件
- `list_policies`: SmokeDetectors 無効・週57,728、ほか Recycling 0、EducationBoost 有効 7,940、BigBusiness 有効 3,760。火事の政策は SmokeDetectors だけで、費用が上限6,000を超えるため比べて外した
- `buildings_near`(x=2941, z=1335, 半径8000, problem=Fire): 4棟。事務所3棟は Fire, FatalProblem、店19320 は Fire, MajorProblem(働き口6)
- `buildings_near`(x=-640, z=1074, 半径100, service=PoliceDepartment): 0棟
- `preview_bulldoze`(3棟、what=building、半径5): どれも targets 1、lost 0 / 0、停電0、modelAgreement 1.0
- `tool-reference.md`: bulldoze(x, z, radius, what) の引数を確認

## 判断の根拠

火事の印4のうち3つは、働き口0の焼けた事務所で、壊しても失うものがない。壊せば合計が5から2になる見込みで、目標の4以下に入る。費用0で、維持費も増えない。

## 捨てたもの

- SmokeDetectors の有効化: 週57,728で、維持費の増え分の上限6,000を超える
- 消防署の増設: 火事の印は焼け跡の3棟で、署の不足を示す数字がなく、建設費と維持費もかかる
- 店19320の取り壊し: 働き口6が働いており、失うものがある。MajorProblem で火事の最中の可能性がある
- 犯罪の手(警察署): 印は港の1件で、目標との差に影響しない
