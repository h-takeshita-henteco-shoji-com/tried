# m05 財政局の案

## 案1: 政策 SmallBusiness を外す(観光の収入の試し、やめる条件の判定)

### 施策

- 案の id: finance-1
- 施策: 政策 SmallBusiness を外す(街全体)。道具は `set_policy`
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: (1) `list_policies` で SmallBusiness が active=true、costPerWeek 311 のままかを確かめる。(2) `set_policy(name="SmallBusiness", active=False)`。(3) `list_policies` で active=false、`policyExpensesPerWeek` が 10,960 から約 10,649 になったことを確かめる
- 設置条件の確認: 該当なし。今月 `list_policies` で、SmallBusiness が active=true、costPerWeek 311、policyExpensesPerWeek 10,960 を確認した
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: 実行前に SmallBusiness がすでに active=false なら、何もしない。実行直前の Tourism の週の収入が 66 以上に戻っていたら、やめる条件の根拠が消えたので見送り、6月末の判定に回す

### 期待する効果

- 改善の見込み: 確認した事実として、週の維持費が 311 減り、週の収支が同じだけ上がる。観光への効きは局の予測。SmallBusiness は3月に Tourism を 42→66 へ上げたが、観光客の増えと切り分けられなかった。4月末は 24 まで下がった。外しても観光の数字は大きく動かないと予測する
- 数値と期限: 週の維持費は 311 減(確定)。Tourism の週の収入は、5月1日の 24 を基準に、6月末の月例で判定する。予想は 24 前後のまま(数値は見積もれない。3月と4月の振れが 24〜74 と大きい)
- 確認方法: `economy_breakdown` の policyExpenses と Tourism の週の収入、`city_info` の tourists.now と週の収支。5月末と6月末を同じ道具で比べる
- 不確かな点: 1か月の判定では効きは決まらない。3月の 66〜74 と4月の 58→24 が示すとおり、Tourism は政策の外し以外の要因でも動く
- 試し: 仮説は、SmallBusiness が商業の収入を経由して Tourism の収入に効く、というもの。外したあとも Tourism が 24 前後のままなら、効きは見えないと読む。測る数は `economy_breakdown` の Tourism の週の収入。場所は街全体。基準は5月1日の 24(4月末)。編成方針の「分からないこと」の SmallBusiness の効きの項目に当たる

### 費用

- 建設費: 0
- 週の維持費の増え分: -311(`list_policies` の SmallBusiness の costPerWeek)

### 戻せるか

戻せる。`set_policy` で有効に戻すと、週 311 が再び出る。

### 前の月の答え合わせ

前月(4か月目)は、局の案がなかった。調査 s04-3(大卒の失業と事務所の税)の結果は、下の判断の根拠で使う。

### 市の計画

- 当たる施策: 5-1、5-2 観光(政策の効きを切り分ける)。財政の守る線(維持費の減り)
- 編成方針の重点に当たるか: 当たる(重点1 観光)

## 案なし

(案1を出すため、この見出しは書かない)

## 調査

- 調査: なし

## 見たもの

- `list_policies`: SmallBusiness active=true、costPerWeek 311(162 commercialLow × 1.92)。RecreationalUse active=false、0。policyExpensesPerWeek 10,960。Recycling(0、住宅の税の収入が約5%減)、HeavyTrafficBan(0)、IndustrySpace(4,846)、FreeTransport(0、運賃収入が0になる)などは inactive
- `economy`: 税 residential_low 9、residential_high 7、commercial_low 9、commercial_high 3、industrial 3、office 3。予算 roads 120、parks 150、garbage 150、healthcare 150、police 150、fire 140、education 120、ship 120。ほかは 100
- `city_info`: 人口 178,380、所持金 2,111,160、週の収入 345,801、週の支出 335,187(収支 +10,614)、観光客 1,811(訪問 138)、需要 住24・商4・工58
- `economy_breakdown`: Tourism 週 24(Commercial の内訳)、Commercial 収入 45,637、Office 収入 24,525、Residential 収入 264,668、policyExpenses 10,960、Road 維持費 8,623

## 判断の根拠

- 長期計画のやめる条件「4月末も Tourism の週の収入が 66 を下回る」を、4月末の 24 で満たした。計画どおり、SmallBusiness を外す案を出す。
- 事務所の税(3→2)は見送った。調査 s04-3 で、大卒の失業は 6,881→6,919→6,930 とほぼ動いていない(計画の「動かないとき案を出さない」)。税を下げると約 -8,200 /週の見込み(局の見積もり、道具で未確認)。打ったあとの週の収支は約 +2,400 で、守る線 +3,000 を割る。
- 商業(低密度)の税 9→8 は、今月は出さない。調整15により、街全体の政策・予算は名所と道の結果の後の月に回す。今月は SmallBusiness を外す案と測る範囲が重なるため、6月末に回す。
- 案は1件にした。今月の観光の手は、名所と入口(経済観光文化局と港湾空港局)が本筋で、財政局の手は政策の切り分けに限る。
- 守る線: 所持金 2,111,160(下限 1,874,000 の上)、週の収支 +10,614(下限 +3,000 の上)。案の後は、週の収支が約 +10,925 になる見込み。

## 捨てたもの

- 事務所の税 3→2(大卒の失業と働き口): 大卒の失業は動いていない。打ったあとの収支の見込みは約 +2,400 で、守る線 +3,000 を割る。
- 商業(低密度)の税 9→8(Tourism の収入の元): 同じ月の政策の外しと測る範囲が重なり、結果を切り分けられない。6月末に回す。
- Recycling(政策、費用0): 住宅の税の収入が約 5% 減る。住宅の収入 264,668 の5%で、上限約 -13,000 /週と見込まれ、守る線を割る恐れがある。ごみ 14 の4-4 に効く見込みはあるが、費用を確かめられない。
- HeavyTrafficBan(政策、費用0): トラックを道から締め出す。貨物の流れ(NoGoods 239、8-1 の 539 台の止まり)を悪くする恐れがあり、出さない。
- IndustrySpace(政策、週 4,846): 工業の効きが観光と6-4に出る見込みを確かめられない。週の維持費の増えも大きく、重点の外。
- FreeTransport(政策): 運賃収入を0にし、バスの収入 5,470 が消える。出さない。
