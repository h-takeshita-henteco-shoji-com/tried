# 14か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 17:25〜17:26)

- 元のファイル: [m14-policy.md](m14-policy.md)
- ゲーム内の日付: 2051-02-05、保存: fukuoka-plan-m14
- 重点: 5-1・5-2 観光、8-1 物流・人流のゲートウェイ、6-4・7-1 企業の立地、地場企業

- 見たもの: [m14-policy.md の「見たもの」](m14-policy.md#見たもの)(16 行)
- 判断の根拠:

  観光は人数も収入も増えたが、入口0と attractiveness 平均2が動かず、目標から遠いので、毎月の重点にする。8-1 は621で目標の2.5倍と、数字で最も遠い。3つ目は、品物がない店が272に悪化し、人口減と空き働き口の背景にあるため、6-4・7-1 を選ぶ。

- 捨てたもの:

  - 4-2 公園(88、目標100): 置き場所の確認が要る。重点の外の案として受ける
  - 4-3 汚染(18、目標15以下): 印が29→18に減り、目標に近づいた。原因は不明なので試しの案で扱う
  - 6-3 交通(52%、目標60): 局所の差し替えは効くが街全体は動かない。重点の外の案として受ける
  - 3-4(火事0、犯罪3): 合計3で目標4以下を達成
  - 1-2、2-3、3-3: 目標を達成か保っている

## 2. 長期計画

- 市長がまとめた計画: [plan-city.md](plan-city.md)
- 住宅都市みどり局の計画: [plan-urban.md](plan-urban.md)
- 道路下水道局の計画: [plan-roads.md](plan-roads.md)
- 港湾空港局の計画: [plan-port.md](plan-port.md)
- 経済観光文化局の計画: [plan-economy.md](plan-economy.md)
- 保健環境局の計画: [plan-health.md](plan-health.md)
- 教育委員会の計画: [plan-education.md](plan-education.md)
- 消防局の計画: [plan-fire.md](plan-fire.md)
- 財政局の計画: [plan-finance.md](plan-finance.md)

## 3. 8つの局の案

### 住宅都市みどり局(urban)(hooks の記録で 17:27〜17:29)

- 元のファイル: [m14-urban.md](m14-urban.md)
- 案 urban-1: 放棄された店の跡に JapaneseGarden を置き、公園を1つ増やす(西の道沿い)
  - 建設費 2500、週の維持費 +40、戻せない
  - 市の計画: 4-2
  - 議決: 要る(取り壊し)

- 見たもの: [m14-urban.md の「見たもの」](m14-urban.md#見たもの)(16 行)
- 判断の根拠:

  - 4-2 は 88 で、目標 100 まで12。第14月に1つ置く計画で、JapaneseGarden が唯一、道と電気・水を確かめて置けた
  - 2100〜2250 の帯の放棄店の跡は、道路(x 2200)と稼働中の建物に当たり、Regular Park も置けなかった。候補を x 1800〜2250 に広げ、(1856,306) を選んだ。取り壊しで失うものは0
  - 維持費は週 40 増え、守る線 +3,000 を割らない。議決は取り壊しの1種類

- 捨てたもの:

  - JapaneseGarden (2176,306): 道 segment 31201 に当たり、稼働中の住宅 17474(家2)と店 3442(働き口11)に重なる。取り壊しで家を失うため捨てた
  - JapaneseGarden (1856,236): 取り壊しで働き口25、家2を失う。失う家が0の条件に合わない
  - JapaneseGarden (2160,18): 取り壊しで働き口18を失う。1か所10以下の条件を超える
  - JapaneseGarden (2224,38): 火葬場 31990 と道に当たる
  - JapaneseGarden (2136,560)、(2128,446.7)、(2180,-138): 道か公園 46934 に当たる。電気と道は確かめた上で捨てた
  - Regular Park (2168,40): 道 segment 4243、7298、32407 と、電線に当たる
  - Tropical Garden 6×6、6,500/104: 維持費が週 104 と重く、今月の4-2の1か所には見合わない
  - Regular Playground 5×5、1,250/24: 遊具の公園で、花や緑の趣旨が薄い。今月は使わない
  - 岩の装飾(Rock Formation など、100/0): 数だけ増えるが、花や緑による潤いの趣旨に合わないため、捨てた
  - HighTechHousing(政策、週 20,272): 住宅の地価に効く見込みはあるが、週の収支が負になるため捨てた
  - 税の変更(TaxLowerResHigh など): 地価への効きを確かめられず、税は財政局の担当のため、この案では出さない

### 道路下水道局(roads)(hooks の記録で 17:27〜17:33)

- 元のファイル: [m14-roads.md](m14-roads.md)
- 案 roads-1: 名所 40850 の入口へ南回りの道をつなぐ
  - 建設費 520、週の維持費 +4.2、戻せる
  - 市の計画: 5-1、5-2 観光
  - 議決: 要らない
- 案 roads-2: 交差点 (-1640,-1100) に信号を置く
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m14-roads.md の「見たもの」](m14-roads.md#見たもの)(20 行)
- 判断の根拠:

  - 案1 は、重点1(5-1、5-2 観光)の名所 40850 が、道がないため Visitors 週5のまま動かないことを根拠にした。南回りの test は ok(520)で、週 4.2 は道の枠 12 に収まる。入口の位置と向きは道具で確かめられないため、実行可否は未確認にした。確かめられるまで、道は引かない
  - 案2 は、13月の信号が効いた(51→30)のと、(-1640,-1100) の canEnableLights が true で置けることを根拠にした。6-3 は編成方針の重点の外だが、長期計画の事業1の次の一手で、交通の流れ 52% を 60% に近づける手
  - 案の数を2件にした理由: 観光の道(案1)と、交通の信号(案2)は別の手。ほかの候補は、確かめられていないか、次の月に回す事業のため、件数を埋めない
  - 電線の直線 (3250,-1420)→(3237,-1293) は test ok(320)。道路下水道局の案には入れず、結果を港湾空港局に渡す(調整4)
  - 週の収支は +3,922 で守る線 +3,000 の上に残る。案1 の 4.2 を入れても +3,918 程度。ただし、2か月続けて下がっているため、15月にもう一度下がると下降規則の対象になる

- 捨てたもの:

  - 名所 40850 の東の道の延長(1640→1624 の区間): test_build_line で、建物の外形に重なると断られた。外形の手前まで道を伸ばす案は作れない
  - 南回り 1,320(経済観光文化局の経路の概算): test で 104m(520)の経路が確かめられたため、長い経路は出さない
  - 信号 (1710,97)(blocked 46): 交差点 (1692,100) は canEnableLights true。ただし、15月の判定で次に出す予備とし、今月は1つだけにした(案2)
  - 信号 (-1640,-1010): 案2 の予備。両方を同時に置くと、同じ手の2件になり、効きが混ざるため出さない
  - 2257・3297 周りの手: 長期計画の17月に回す。13月の調査の結果が、まだ1回の測りだけのため
  - 太くする手(Large Road): 13月に、医療所 10289 と電柱にぶつかるため採らない
  - HeavyTrafficBan: 13月に採らない(品物がない店を悪化させるおそれ)。今月も、6-4・7-1 と合わせて採らない

### 港湾空港局(port)(hooks の記録で 17:27〜17:28)

- 元のファイル: [m14-port.md](m14-port.md)
- 案: なし

- 見たもの: [m14-port.md の「見たもの」](m14-port.md#見たもの)(17 行)
- 判断の根拠:

  - 駅は、今月の週の収支(+3,922)のまま足すと +2,960 になり、守る線 +3,000 を割る。第17月の案の条件(Boost 判定と 2267 の停止)は、計画の調整3のとおりに据え置く。
  - 空き地5は、電気・水・下水の網が300m内になく、最寄りの道まで900m超。道を引く試しも重なりで断られた。今月は候補から外し、島Bに絞る。
  - 北の列は、駅(16×6)の空きがなく閉じた。
  - 8-1 は、710台の止まりが敷地内の空き待ちと分かった。振り分けの試しは第15月の予定どおり。
  - 案を5件まで出す条件に届く手がないため、案なしにする。

- 捨てたもの:

  - 旅客の駅を北の列に置く案: Train Station の試し2回が ObjectCollision、空きが見当たらないため。閉じた。
  - 旅客の駅を空き地5に置く案: 電気・水・下水が 0 で、道も900m超。道の試しは事務所に重なる。経路を組み直すのに費用と月数がかかるため、今月は出さない。
  - 島Bの駅を今月出す案: 水が届かず、水源(Water Intake)の置き場所と、電線・水管の試しが未確認。第15月に試す。
  - 駅を今月出す案: 守る線 +3,000 を割るため。第17月の案に回す。
  - 8-1 の振り分けの案: 振り分け先の 3940、4740 の確認が第15月の予定のため、今月の案にできる条件がない。

### 経済観光文化局(economy)(hooks の記録で 17:27〜17:28)

- 元のファイル: [m14-economy.md](m14-economy.md)
- 案: なし

- 見たもの: [m14-economy.md の「見たもの」](m14-economy.md#見たもの)(9 行)
- 判断の根拠:

  - 14月の予定(計画の第14月)は、40850 の測り、noGoods の基準、事務所の空きの候補探しの3つ。3つとも確認済みで、案ではない。
  - 40850 の道は roads の担当。14月末も届かないので、南回りは roads の案にする(調整2)。経済は測りを渡すだけにした。
  - 事務所の空きは、道に面する空きが0で、働き口を増やす手は道だけ。道は roads が16月以降に引く(調整10)。今月は試しを前倒ししない。
  - 週の収支 +3,922 は、計画の見込み +4,420 より約500低い。守る線 +3,000 の余裕は 922 で、名所の1棟目(320)は入るが、場所が確定していない。計画の変更(14月)に書いた。
  - 13月の経済の案(南回りの道)は採られなかった。答え合わせの対象は、ほかにない。
  - 案の数は0。担当の問題に効く手のうち、今月に確認できて実行できるものはない。

- 捨てたもの:

  - 名所 40850 の南回りの道(約1,320): roads の担当(調整2)。経済は出さない。
  - 名所の候補地の試し(今月): 計画は15月。今月は場所が確定しておらず、前倒しすると確認が足りない。
  - SmallBusiness の再有効化(観光の収入): 3月と5月の判定で、政策の効きと別の要因を分けられなかった。分けられる形を取るまで出さない。
  - RecreationalUse の再有効化: 4月の判定で attractiveness が動かなかった。
  - 事務所税の変更: 11月と12月の判定で、事務所 L3 と大卒の失業に効かなかった。

### 保健環境局(health)(hooks の記録で 17:27〜17:29)

- 元のファイル: [m14-health.md](m14-health.md)
- 案 health-1: ごみの印の集まりの近くに埋立地を1つ足す(1800,-570)
  - 建設費 4240、週の維持費 +162、戻せる
  - 市の計画: 4-4
  - 議決: 要らない

- 見たもの: [m14-health.md の「見たもの」](m14-health.md#見たもの)(18 行)
- 判断の根拠:

  - ごみの印 14 は目標 0 から遠く、1月の空けの停止で 12→14 に増えた。2267 の停止は、ごみの印が 9 以下になるまで待つ条件なので、2月は止めない。計画の変更に理由を書いた。
  - ごみの印の 10 棟は (1967,-536) の周りに集まり、近くに埋立地がない。収集車は 3,000m を超える運搬をしている(`vehicles_stuck`)。近い埋立地を足す手は、確かめた道具で置ける場所が見つかった(1800,-570)。費用 4,240、取り壊しなし。
  - 案は1件だけにした。2267 の停止は条件未達、Recycling は住宅税の損が大きく守る線を割る、死体の印 41 は 3 か月前の 60 から減っており墓地の容量は足りる。汚染の出どころは 2267 と確かめたが、停止の条件が未達なので今月は手を出さない。
  - 調査を1件出した。埋立地の効きと、2267 の停止の条件(ごみの印 9 以下)が、見回りで動くかを見るため。

- 捨てたもの:

  - 2267 の停止(計画の事業2): 2/5 のごみの印は 14 で、条件の 9 以下に届かない。止めると、m02-3 のようにごみの印が増える見込み。3月へ送った。
  - Recycling 政策(ごみ -15%): 住宅税が 264,852 / 週あるため、5% の損で約 -13,000 / 週。守る線 +3,000 を割る。採らない。
  - 2267 を別の場所へ移す(relocate_building): 汚染の印の出どころは 2267 と見えるが、移すと運搬が長くなり、ごみの印が増える見込み。確かめる道具の試しが足りないため、今月は出さない。
  - 埋立地 (1800,-500) の案: 道を引くのに商店 3 棟(働き口 45)を取り壊す必要がある。取り壊しは議決が要り、ごみの印の効きが分からないうちは出さない。
  - 死体の印(Death 41、hotspot (2285,32)): 墓地の容量 14,283 / 24,000 で余裕があり、印は 60→41 に減っている。収集の遅れの原因は未確認。調査の枠を、ごみの印に使う。
  - 汚染の印の別の手(工場の周りの木、政策): 汚染の印 18 は目標 15 に近く、原因の 2267 の停止は条件待ち。木は 190 本で効かなかった(m01-5)。今月は出さない。

### 教育委員会(education)(hooks の記録で 17:27〜17:27)

- 元のファイル: [m14-education.md](m14-education.md)
- 案: なし

- 見たもの:

  - `services`: 小学校の定員 14,268、高校 24,360、大学 36,540。電気・水・下水は余裕あり(used/capacity 約80%)
  - `citizens_summary`: 子ども 8,924(前月 9,008)、10代 19,797(前月 20,256)、失業 7,403(大卒 7,279)。来ない市民 0/0/0
  - `city_info`: 人口 178,202、所持金 2,419,253、週の収支 +3,922(収入 338,692、支出 334,770)、dialog なし
  - `list_policies`: EducationBoost 有効、週 7,940(学校の維持費の +25%。政策の費用とは別の教育の支出)。ほかに教育に関わる政策の変更はなし。政策一覧の取得は成功した
  - `list_building_types`(service=Education): Elementary School 建設費 10,000、週 160、定員 300。High School 建設費 24,000、週 560、定員 1,000

- 判断の根拠:

  2-3 の数字は、どちらも目標を満たしている。子どもと10代は減っており、学校の定員の余裕は広がっている。計画の前提(子どもと10代が減る)と、今月の数字は一致した。
  小学校の余剰を止める案は、計画の事業では15月の確認から出す。14月は観察のみと決まっている。止めると週 -160 の維持費が減るが、2-3 の目標の数字は変わらない。今月の守る線(週の収支 +3,000 以上)にも余裕がある。よって今月は、止める案を前倒しにしない。
  政策の変更(EducationBoost の解除など)は、2-3 の数字を動かさない。EducationBoost は、大卒の失業を見る施策で、教育委員会の担当ではない。今月は手を付けない。
  案の数は0件。有効な手段は、計画どおり15月まで出せない。

- 捨てたもの:

  - 高校1校の追加: 余裕 4,563 は 2,000 以上。建設費 24,000、週 560 の増えに見合わない
  - 小学校1校の停止(`set_building_active` false): 計画の15月の確認まで待つ。今月は前倒ししない。見込みは週 -160 で、2-3 の数字は変えない
  - EducationBoost の解除: 教育の担当の数字には効かない。大卒の失業の施策で、経済の局と市長の判断に任せる

### 消防局(fire)(hooks の記録で 17:27〜17:29)

- 元のファイル: [m14-fire.md](m14-fire.md)
- 案 fire-1: 貨物港 32211 の横に警察署を置く
  - 建設費 12000、週の維持費 +480、戻せる
  - 市の計画: 3-4
  - 議決: 要らない

- 見たもの: [m14-fire.md の「見たもの」](m14-fire.md#見たもの)(15 行)
- 判断の根拠:

  - 3-4 は、火事0と犯罪3の合計3で、目標の4以下に入っている。ただし、10月には火事2と犯罪4で合計6となったことがあり、余裕は1しかない
  - 火事の印は街全体で0。焼け跡の事業1は、焼け跡が出ない今月は案なし
  - 犯罪の印3棟のうち、貨物港 32211 は警察の届きが0。届きが0の場所の印を、届きで消す手は、道具で確かめられる。警察署は置く場所が試しで通り、電気・水・下水も届く。費用は建設費 12,000、週 480 で、守る線の上に残る
  - 犯罪の印13893 は届きが38あるので、警察署を足す理由は弱い。捨てた
  - 案は1件。事業2(同じ場所の火事)は、火事の印が0なので今月の案なし
  - 政策 SmokeDetectors は週 57,912 で、費用の上限を大きく超えるので捨てた

- 捨てたもの:

  - 政策 SmokeDetectors(火事を減らす): 週 57,912 で、守る線(週の収支 +3,000)を大きく割る。費用の上限に収まらない
  - 警察本部 Police Headquarters: 建設費 60,000、週 1,600。犯罪の印は3棟で、届きの足りない場所は1つだけなので、費用に見合わない
  - 13893(Cargo Center)の周りの警察署: 届きは38あり、今の印の原因が届きとは見えない
  - 焼け跡の取り壊し(事業1): 焼け跡の印が出ていないので、今月の案なし
  - 火事の追跡の調査(事業2): 火事の印が街全体で0なので、今月は見る対象がない

### 財政局(finance)(hooks の記録で 17:27〜17:28)

- 元のファイル: [m14-finance.md](m14-finance.md)
- 案: なし

- 見たもの:

  - `list_policies`: EducationBoost は active=true、costPerWeek 7,940。BigBusiness は active=true、3,948。SmokingBan は active=true、0。SmallBusiness は active=false、315。RecreationalUse は active=false、0。SmokeDetectors、PowerSaving、WaterSaving、IndustrySpace、HighTechHousing は active=false。policyExpensesPerWeek 10,594
  - `city_info`: 人口 178,202、所持金 2,419,253、週の収入 338,692、週の支出 334,770、週の収支 +3,922。観光客 1,847(訪問 143)。来ない市民 0/0/0。dialog なし
  - `economy`: 税は住宅(低)9、住宅(高)7、商業(低)9、商業(高)3、工業3、事務所3。予算は医療 150、警察 150、ごみ 150、公園 150、バス 150、消防 140、教育 120、道路 120
  - `economy_breakdown`: Tourism 週 49、Office 24,460、HealthCare の週の支出 76,440、Education の週の支出 48,120、policyExpenses 10,594
  - `list_loans`: 融資の枠は3つとも未借入。loanExpensesPerWeek 0
  - `citizens_summary`: 大卒の失業 7,279(unemployed 全体 7,403)。健康の平均 89。electricity・water・sewage が来ない市民は 0 / 0 / 0

- 判断の根拠:

  - 週の収支 +3,922 は守る線 +3,000 の上で、余裕は 922。計画の見込み 4,464 より 542 低い。差の原因は未確認で、収入の揺れとみる(見立て)。
  - 下降規則は2回目(4,464 → 3,922。どちらも +4,900 を切る)。3回目の第15月末で効く。
  - 案を0件にした理由: 税・予算は、長期計画で第18月に決めると決めてある。今月の数字で計画の前提が変わったのは引き金の一点だけで、決める時期を前倒しする根拠がない。新しい維持費は、余裕 922 に入らない。

- 捨てたもの:

  - 予算: 医療を 150 から 120 に下げる。道具の週の支出 76,440 から見積もると、およそ 15,000 の維持費が減る見込み(見積もり。実測ではない)。ただし、健康 89(目標 80)への効きを測っていない。第18月の見直しで候補にする。
  - 政策 BigBusiness を外す: 週 3,948 が減るが、商業(高)の効きと、観光・働き口への影響が確かめられていない。政策一覧の記述は効果の実測値ではない。
  - 税: 事務所税の試し(m09、m11)で、L3 と大卒の失業に効かなかった。住宅・商業の税は、観光と働き口へ効く見込みを確かめていない。
  - 政策 SmallBusiness を入れる: 週 315。Tourism への効きは m02-4 で切り分けられず、5-1・5-2 の目標に効くと言えない。
  - 融資: 所持金 2,419,253 で足りるので、借りる理由がない。返済が週に増える。

## 4. 差し戻しと再調査

- 道路下水道局: roads-1(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m14-bill.md](m14-bill.md)
- 採った m14-1: 放棄された店の跡に JapaneseGarden を置く(元 urban-1、議決が要る(取り壊し))
- 採った m14-2: 交差点 (-1640,-1100) に信号(元 roads-2、議決は要らない)
- 採った m14-3: ごみの印の近くに埋立地と道(元 health-1、議決は要らない)
- 採らなかった fire-1: 3-4 は目標を満たしており、週480で守る線の余裕が240になる。
- 採らなかった roads-1: 名所 40850 の入口の位置と向きが未確認で、支線の費用も不明。

- 見たもの:

  - `m14-urban.md`、`m14-roads.md`、`m14-health.md`、`m14-fire.md`、`m14-finance.md`、`m14-port.md`、`m14-economy.md`、`m14-education.md`、`m14-policy.md`: 局の案、調査、編成方針を読んだ(道具は呼んでいない)
  - `city_info`(局の案の値を引用): 週の収支 +3,922(収入 338,692、支出 334,770)、所持金 2,419,253、人口 178,202、観光客 1,847
  - `mayor-note.md`: 14か月目の数字の表と答え合わせ

- 判断の根拠:

  週の収支 +3,922 は守る線 +3,000 の上で、余裕は 922 しかない。維持費が増える案は、合計の増えを 922 に収める必要がある。m14-1(40)、m14-3(約162)、m14-2(未確認だが前回は 0)の合計は約 202 で、週の収支は約 +3,720、所持金は約 2,412,500 に残る。建設費の合計は 6,740。fire-1(480)を加えると余裕が 240 になるので、目標をすでに満たしている 3-4 の案を外した。roads-1 は実行条件が未確認なので採らず、条件付きで局に調べ直させる。
  重点の 5-1・5-2、8-1、6-4・7-1 では、確認済みの実行案が出なかった(port、economy は案なし、roads-1 は未確認)。そのため、重点の外の確認済みの案から、費用が小さく失うものがないものを採った。分からないことの一覧の項目のうち、試しの案を出した局はなかった。

- 捨てたもの:

  - fire-1: 上のとおり。目標を満たしており、余裕を使い切る。
  - roads-1: 入口の位置と向きが未確認。
  - 政策の変更(Recycling、SmokeDetectors、HighTechHousing など): 局が週の収支を守る線の下に割ると示した。
  - 予備候補(urban-1 の (2160,102)、(1856,183)): 稼働中の店を壊すため、今月は使わない。
  - 計画の変更: 局が長期計画の変更を知らせていないので、`plan-city.md` は変えない。

## 6. 議会: 可決と否決(hooks の記録で 17:34〜17:34)

- 元のファイル: [m14-assembly.md](m14-assembly.md)
- m14-1 取り壊し: 可決。対象は放棄の店 39889 だけで、働き口0、家0。代わりの手との比較も書かれ、週 40 の増えは守る線に収まる。
- m14-2 財政: 可決。建設費0、維持費の増えは前回の同型で0。守る線に響かない。
- m14-3 財政: 可決。建設費 4,240、週 約 162。3施策の合計でも週の収支は約 +3,720、所持金は約 2,412,500 で線を守れる。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `preview_bulldoze`: (1856,306) r10 abandoned で 39889 のみ、jobs 0、homes 0、停電0
  - `city_info`: 週の収入 338,692、支出 334,770、所持金 2,419,253
  - `economy`: 税と予算を確認。変更案は議案になし
  - `m14-bill.md`、`mayor-note.md`: 案と数字の表を読んだ

- 判断の根拠:

  3施策の建設費 6,740 と維持費の増え 202 を足しても、週の収支は +3,000 を上回り、所持金も 1,874,000 を大きく上回る。余裕は約 720 だが、線は破らない。取り壊しは失うものが0で、点1の備えがそろっている。

- 捨てたもの:

  - m14-3: 余裕が小さい中で維持費が最大の施策だが、守る線は破らず、重点外でも否決の理由にならないので可決した。

## 7. 実行する市長: 実行と見回り(hooks の記録で 17:35〜17:41)

- 実行してよい施策: m14-1、m14-2、m14-3
- 実行した: m14-1、m14-2、m14-3
- 失敗した: なし
- 臨時: なし
- 見回り 2051-02-15: 人口 177735、所持金 2419768、週の収支 5359、幸福度 88
- 見回り 2051-02-25: 人口 177522、所持金 2426637、週の収支 4368、幸福度 88
- 報告:

  m14-1から3は3件とも実行できた。予備候補は使っていない。
  - m14-1: 放棄店39889を壊し、JapaneseGarden(id 39519)を置いた。費用は2,500。Beautification は88から89に増えた。
  - m14-2: 交差点(-1640,-1100)に信号を付けた。費用は0。blocked は62から、見回り1で1、見回り2で8、月末で33になった。揺れが大きい。
  - m14-3: 埋立地44370を置いた(費用4,000)。議案の道は埋立地に重なって断られた。端を12m東の(1844,-570)に動かし、test が通ってから引いた(費用200、端(1880,-570)は節点31276につながった)。西端は入口まで12m空いている。ごみの印は14から8に減った。
  月末は2051-03-07で、人口177,176(6か月連続で減少)、所持金2,433,116、週の収支は+4,256。守る線+3,000の上だが、+4,900は下回っている。観光客は1,851、Tourism は週37。見回り2回と月末に境目はなく、臨時もなかった。hooks に止められた手もなかった。
  調査の結果は council/m14-survey-roads.md、m14-survey-health.md、m14-survey-finance.md に書いた。市政ノートとcommand-log.txtも更新した。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m14、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 17:24〜17:51(hooks の記録の時刻から)、道具の行 220
- 議会が可決した種類: 取り壊し
- 議決が要る道具の呼び出し: 1 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 606 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m14-urban-map-east.jpg`

#### 運営のフォルダで、決まりの外の変更(git status)

- `council/m01-port-zonemap-east.jpg`
- `council/m01-roads-zonemap.jpg`
- `council/m01-zonemap-east.jpg`
- `council/m03-zone-a.jpg`
- `council/m05-port-map-south.jpg`
- `council/m06-economy-zonemap-east.jpg`
- `council/m06-port-map-2480.jpg`
- `council/m06-port-map-cargo.jpg`
- `council/m06-port-map-east.jpg`
- `council/m06-port-map-south.jpg`
- `council/m06-roads-map-electric.jpg`
- `council/m07-port-islandB-map.jpg`
- `council/m08-map-city.jpg`
- `council/m08-map-park.jpg`
- `council/m09-economy-map-east.jpg`
- `council/m09-health-map-pollution.jpg`
- `council/m09-port-islandB.jpg`
- `council/m11-port-map-north.jpg`
- `council/m12-port-zonemap.jpg`
- `council/m13-port-zonemap-cargo.jpg`
- `council/m13-port-zonemap-west.jpg`
- `ボツ-12か月の運営/command-log.txt`
- `ボツ-12か月の運営/council/_tmp_health_m02_west.jpg`
- `ボツ-12か月の運営/council/ledger.jsonl`
- `ボツ-12か月の運営/council/m01-assembly.json`
- `ボツ-12か月の運営/council/m01-assembly.md`
- `ボツ-12か月の運営/council/m01-bill.md`
- `ボツ-12か月の運営/council/m01-economy.md`
- `ボツ-12か月の運営/council/m01-education.md`
- `ボツ-12か月の運営/council/m01-finance.md`
- `ボツ-12か月の運営/council/m01-fire.md`
- `ボツ-12か月の運営/council/m01-guide.md`
- `ボツ-12か月の運営/council/m01-health.md`
- `ボツ-12か月の運営/council/m01-hooks.log`
- `ボツ-12か月の運営/council/m01-minutes.md`
- `ボツ-12か月の運営/council/m01-policy.md`
- `ボツ-12か月の運営/council/m01-port.md`
- `ボツ-12か月の運営/council/m01-roads.md`
- `ボツ-12か月の運営/council/m01-run.json`
- `ボツ-12か月の運営/council/m01-survey-health.md`
- `ボツ-12か月の運営/council/m01-survey-port.md`
- `ボツ-12か月の運営/council/m01-survey-roads.md`
- `ボツ-12か月の運営/council/m01-urban.md`
- `ボツ-12か月の運営/council/m02-assembly.json`
- `ボツ-12か月の運営/council/m02-assembly.md`
- `ボツ-12か月の運営/council/m02-bill.md`
- `ボツ-12か月の運営/council/m02-economy.md`
- `ボツ-12か月の運営/council/m02-education.md`
- `ボツ-12か月の運営/council/m02-finance.md`
- `ボツ-12か月の運営/council/m02-fire.md`
- `ボツ-12か月の運営/council/m02-guide.md`
- `ボツ-12か月の運営/council/m02-health.md`
- `ボツ-12か月の運営/council/m02-hooks.log`
- `ボツ-12か月の運営/council/m02-minutes.md`
- `ボツ-12か月の運営/council/m02-policy.md`
- `ボツ-12か月の運営/council/m02-port-map-cargo.jpg`
- `ボツ-12か月の運営/council/m02-port.md`
- `ボツ-12か月の運営/council/m02-roads.md`
- `ボツ-12か月の運営/council/m02-run.json`
- `ボツ-12か月の運営/council/m02-survey-fire.md`
- `ボツ-12か月の運営/council/m02-survey-health.md`
- `ボツ-12か月の運営/council/m02-survey-port.md`
- `ボツ-12か月の運営/council/m02-urban.md`
- `ボツ-12か月の運営/council/m03-bill.md`
- `ボツ-12か月の運営/council/m03-economy.md`
- `ボツ-12か月の運営/council/m03-education.md`
- `ボツ-12か月の運営/council/m03-finance.md`
- `ボツ-12か月の運営/council/m03-fire.md`
- `ボツ-12か月の運営/council/m03-guide.md`
- `ボツ-12か月の運営/council/m03-health.md`
- `ボツ-12か月の運営/council/m03-hooks.log`
- `ボツ-12か月の運営/council/m03-minutes.md`
- `ボツ-12か月の運営/council/m03-policy.md`
- `ボツ-12か月の運営/council/m03-port-cargo-map.jpg`
- `ボツ-12か月の運営/council/m03-port.md`
- `ボツ-12か月の運営/council/m03-roads.md`
- `ボツ-12か月の運営/council/m03-run.json`
- `ボツ-12か月の運営/council/m03-survey-economy.md`
- `ボツ-12か月の運営/council/m03-survey-fire.md`
- `ボツ-12か月の運営/council/m03-survey-port.md`
- `ボツ-12か月の運営/council/m03-urban.md`
- `ボツ-12か月の運営/council/m04-bill.md`
- `ボツ-12か月の運営/council/m04-economy.md`
- `ボツ-12か月の運営/council/m04-education.md`
- `ボツ-12か月の運営/council/m04-finance.md`
- `ボツ-12か月の運営/council/m04-fire.md`
- `ボツ-12か月の運営/council/m04-guide.md`
- `ボツ-12か月の運営/council/m04-health.md`
- `ボツ-12か月の運営/council/m04-hooks.log`
- `ボツ-12か月の運営/council/m04-minutes.md`
- `ボツ-12か月の運営/council/m04-policy.md`
- `ボツ-12か月の運営/council/m04-port.md`
- `ボツ-12か月の運営/council/m04-roads.md`
- `ボツ-12か月の運営/council/m04-run.json`
- `ボツ-12か月の運営/council/m04-survey-economy.md`
- `ボツ-12か月の運営/council/m04-survey-health.md`
- `ボツ-12か月の運営/council/m04-survey-port.md`
- `ボツ-12か月の運営/council/m04-urban.md`
- `ボツ-12か月の運営/council/m05-assembly.json`
- `ボツ-12か月の運営/council/m05-assembly.md`
- `ボツ-12か月の運営/council/m05-bill.md`
- `ボツ-12か月の運営/council/m05-economy.md`
- `ボツ-12か月の運営/council/m05-education.md`
- `ボツ-12か月の運営/council/m05-finance.md`
- `ボツ-12か月の運営/council/m05-fire.md`
- `ボツ-12か月の運営/council/m05-guide.md`
- `ボツ-12か月の運営/council/m05-health.md`
- `ボツ-12か月の運営/council/m05-hooks.log`
- `ボツ-12か月の運営/council/m05-minutes.md`
- `ボツ-12か月の運営/council/m05-policy.md`
- `ボツ-12か月の運営/council/m05-port.md`
- `ボツ-12か月の運営/council/m05-roads.md`
- `ボツ-12か月の運営/council/m05-run.json`
- `ボツ-12か月の運営/council/m05-survey-health.md`
- `ボツ-12か月の運営/council/m05-survey-port.md`
- `ボツ-12か月の運営/council/m05-survey-roads.md`
- `ボツ-12か月の運営/council/m05-urban.md`
- `ボツ-12か月の運営/council/m06-assembly.json`
- `ボツ-12か月の運営/council/m06-assembly.md`
- `ボツ-12か月の運営/council/m06-bill.md`
- `ボツ-12か月の運営/council/m06-economy.md`
- `ボツ-12か月の運営/council/m06-education.md`
- `ボツ-12か月の運営/council/m06-finance.md`
- `ボツ-12か月の運営/council/m06-fire.md`
- `ボツ-12か月の運営/council/m06-guide.md`
- `ボツ-12か月の運営/council/m06-health.md`
- `ボツ-12か月の運営/council/m06-hooks.log`
- `ボツ-12か月の運営/council/m06-minutes.md`
- `ボツ-12か月の運営/council/m06-policy.md`
- `ボツ-12か月の運営/council/m06-port.md`
- `ボツ-12か月の運営/council/m06-roads.md`
- `ボツ-12か月の運営/council/m06-run.json`
- `ボツ-12か月の運営/council/m06-survey-economy.md`
- `ボツ-12か月の運営/council/m06-survey-health.md`
- `ボツ-12か月の運営/council/m06-survey-port.md`
- `ボツ-12か月の運営/council/m06-urban.md`
- `ボツ-12か月の運営/council/m07-assembly.json`
- `ボツ-12か月の運営/council/m07-assembly.md`
- `ボツ-12か月の運営/council/m07-bill.md`
- `ボツ-12か月の運営/council/m07-economy.md`
- `ボツ-12か月の運営/council/m07-education.md`
- `ボツ-12か月の運営/council/m07-finance.md`
- `ボツ-12か月の運営/council/m07-fire.md`
- `ボツ-12か月の運営/council/m07-guide.md`
- `ボツ-12か月の運営/council/m07-health-zonemap-west.jpg`
- `ボツ-12か月の運営/council/m07-health.md`
- `ボツ-12か月の運営/council/m07-hooks.log`
- `ボツ-12か月の運営/council/m07-minutes.md`
- `ボツ-12か月の運営/council/m07-policy.md`
- `ボツ-12か月の運営/council/m07-port.md`
- `ボツ-12か月の運営/council/m07-roads.md`
- `ボツ-12か月の運営/council/m07-run.json`
- `ボツ-12か月の運営/council/m07-survey-economy.md`
- `ボツ-12か月の運営/council/m07-survey-health.md`
- `ボツ-12か月の運営/council/m07-survey-roads.md`
- `ボツ-12か月の運営/council/m07-urban.md`
- `ボツ-12か月の運営/council/m08-assembly.json`
- `ボツ-12か月の運営/council/m08-assembly.md`
- `ボツ-12か月の運営/council/m08-bill.md`
- `ボツ-12か月の運営/council/m08-economy.md`
- `ボツ-12か月の運営/council/m08-education.md`
- `ボツ-12か月の運営/council/m08-finance.md`
- `ボツ-12か月の運営/council/m08-fire.md`
- `ボツ-12か月の運営/council/m08-guide.md`
- `ボツ-12か月の運営/council/m08-health.md`
- `ボツ-12か月の運営/council/m08-hooks.log`
- `ボツ-12か月の運営/council/m08-minutes.md`
- `ボツ-12か月の運営/council/m08-policy.md`
- `ボツ-12か月の運営/council/m08-port-cargo-map.jpg`
- `ボツ-12か月の運営/council/m08-port.md`
- `ボツ-12か月の運営/council/m08-roads.md`
- `ボツ-12か月の運営/council/m08-run.json`
- `ボツ-12か月の運営/council/m08-survey-economy.md`
- `ボツ-12か月の運営/council/m08-survey-education.md`
- `ボツ-12か月の運営/council/m08-survey-roads.md`
- `ボツ-12か月の運営/council/m08-urban.md`
- `ボツ-12か月の運営/council/m09-bill.md`
- `ボツ-12か月の運営/council/m09-economy.md`
- `ボツ-12か月の運営/council/m09-education.md`
- `ボツ-12か月の運営/council/m09-finance.md`
- `ボツ-12か月の運営/council/m09-fire.md`
- `ボツ-12か月の運営/council/m09-guide.md`
- `ボツ-12か月の運営/council/m09-health.md`
- `ボツ-12か月の運営/council/m09-hooks.log`
- `ボツ-12か月の運営/council/m09-minutes.md`
- `ボツ-12か月の運営/council/m09-policy.md`
- `ボツ-12か月の運営/council/m09-port.md`
- `ボツ-12か月の運営/council/m09-roads.md`
- `ボツ-12か月の運営/council/m09-run.json`
- `ボツ-12か月の運営/council/m09-survey-economy.md`
- `ボツ-12か月の運営/council/m09-survey-health.md`
- `ボツ-12か月の運営/council/m09-survey-port.md`
- `ボツ-12か月の運営/council/m09-urban.md`
- `ボツ-12か月の運営/council/m10-assembly.json`
- `ボツ-12か月の運営/council/m10-assembly.md`
- `ボツ-12か月の運営/council/m10-bill.md`
- `ボツ-12か月の運営/council/m10-economy.md`
- `ボツ-12か月の運営/council/m10-education.md`
- `ボツ-12か月の運営/council/m10-finance.md`
- `ボツ-12か月の運営/council/m10-fire.md`
- `ボツ-12か月の運営/council/m10-guide.md`
- `ボツ-12か月の運営/council/m10-health-zone-west.jpg`
- `ボツ-12か月の運営/council/m10-health.md`
- `ボツ-12か月の運営/council/m10-hooks.log`
- `ボツ-12か月の運営/council/m10-minutes.md`
- `ボツ-12か月の運営/council/m10-policy.md`
- `ボツ-12か月の運営/council/m10-port.md`
- `ボツ-12か月の運営/council/m10-roads.md`
- `ボツ-12か月の運営/council/m10-run.json`
- `ボツ-12か月の運営/council/m10-survey-economy.md`
- `ボツ-12か月の運営/council/m10-survey-health.md`
- `ボツ-12か月の運営/council/m10-survey-urban.md`
- `ボツ-12か月の運営/council/m10-urban.md`
- `ボツ-12か月の運営/council/m11-assembly.json`
- `ボツ-12か月の運営/council/m11-assembly.md`
- `ボツ-12か月の運営/council/m11-bill.md`
- `ボツ-12か月の運営/council/m11-economy.md`
- `ボツ-12か月の運営/council/m11-education.md`
- `ボツ-12か月の運営/council/m11-finance.md`
- `ボツ-12か月の運営/council/m11-fire.md`
- `ボツ-12か月の運営/council/m11-guide.md`
- `ボツ-12か月の運営/council/m11-health-map-garbage.jpg`
- `ボツ-12か月の運営/council/m11-health.md`
- `ボツ-12か月の運営/council/m11-hooks.log`
- `ボツ-12か月の運営/council/m11-minutes.md`
- `ボツ-12か月の運営/council/m11-policy.md`
- `ボツ-12か月の運営/council/m11-port.md`
- `ボツ-12か月の運営/council/m11-roads.md`
- `ボツ-12か月の運営/council/m11-run.json`
- `ボツ-12か月の運営/council/m11-survey-economy.md`
- `ボツ-12か月の運営/council/m11-survey-fire.md`
- `ボツ-12か月の運営/council/m11-survey-port.md`
- `ボツ-12か月の運営/council/m11-urban.md`
- `ボツ-12か月の運営/council/m12-assembly.json`
- `ボツ-12か月の運営/council/m12-assembly.md`
- `ボツ-12か月の運営/council/m12-bill.md`
- `ボツ-12か月の運営/council/m12-economy.md`
- `ボツ-12か月の運営/council/m12-education.md`
- `ボツ-12か月の運営/council/m12-finance.md`
- `ボツ-12か月の運営/council/m12-fire.md`
- `ボツ-12か月の運営/council/m12-guide.md`
- `ボツ-12か月の運営/council/m12-health-zone-w.jpg`
- `ボツ-12か月の運営/council/m12-health.md`
- `ボツ-12か月の運営/council/m12-hooks.log`
- `ボツ-12か月の運営/council/m12-minutes.md`
- `ボツ-12か月の運営/council/m12-policy.md`
- `ボツ-12か月の運営/council/m12-port.md`
- `ボツ-12か月の運営/council/m12-roads.md`
- `ボツ-12か月の運営/council/m12-run.json`
- `ボツ-12か月の運営/council/m12-survey-economy.md`
- `ボツ-12か月の運営/council/m12-survey-port.md`
- `ボツ-12か月の運営/council/m12-urban.md`
- `ボツ-12か月の運営/mayor-note.md`
- `ボツ-12か月の運営/transcripts/m01-assembly.md`
- `ボツ-12か月の運営/transcripts/m01-economy.md`
- `ボツ-12か月の運営/transcripts/m01-education.md`
- `ボツ-12か月の運営/transcripts/m01-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m01-finance.md`
- `ボツ-12か月の運営/transcripts/m01-fire.md`
- `ボツ-12か月の運営/transcripts/m01-health.md`
- `ボツ-12か月の運営/transcripts/m01-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m01-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m01-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m01-port.md`
- `ボツ-12か月の運営/transcripts/m01-roads.md`
- `ボツ-12か月の運営/transcripts/m01-urban.md`
- `ボツ-12か月の運営/transcripts/m02-assembly.md`
- `ボツ-12か月の運営/transcripts/m02-economy.md`
- `ボツ-12か月の運営/transcripts/m02-education.md`
- `ボツ-12か月の運営/transcripts/m02-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m02-finance.md`
- `ボツ-12か月の運営/transcripts/m02-fire.md`
- `ボツ-12か月の運営/transcripts/m02-health.md`
- `ボツ-12か月の運営/transcripts/m02-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m02-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m02-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m02-port.md`
- `ボツ-12か月の運営/transcripts/m02-roads.md`
- `ボツ-12か月の運営/transcripts/m02-urban.md`
- `ボツ-12か月の運営/transcripts/m03-economy.md`
- `ボツ-12か月の運営/transcripts/m03-education.md`
- `ボツ-12か月の運営/transcripts/m03-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m03-finance.md`
- `ボツ-12か月の運営/transcripts/m03-fire.md`
- `ボツ-12か月の運営/transcripts/m03-health.md`
- `ボツ-12か月の運営/transcripts/m03-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m03-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m03-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m03-port.md`
- `ボツ-12か月の運営/transcripts/m03-roads.md`
- `ボツ-12か月の運営/transcripts/m03-urban.md`
- `ボツ-12か月の運営/transcripts/m04-economy.md`
- `ボツ-12か月の運営/transcripts/m04-education.md`
- `ボツ-12か月の運営/transcripts/m04-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m04-finance.md`
- `ボツ-12か月の運営/transcripts/m04-fire.md`
- `ボツ-12か月の運営/transcripts/m04-health.md`
- `ボツ-12か月の運営/transcripts/m04-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m04-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m04-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m04-port.md`
- `ボツ-12か月の運営/transcripts/m04-roads.md`
- `ボツ-12か月の運営/transcripts/m04-urban.md`
- `ボツ-12か月の運営/transcripts/m05-assembly.md`
- `ボツ-12か月の運営/transcripts/m05-economy.md`
- `ボツ-12か月の運営/transcripts/m05-education.md`
- `ボツ-12か月の運営/transcripts/m05-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m05-finance.md`
- `ボツ-12か月の運営/transcripts/m05-fire.md`
- `ボツ-12か月の運営/transcripts/m05-health.md`
- `ボツ-12か月の運営/transcripts/m05-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m05-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m05-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m05-port.md`
- `ボツ-12か月の運営/transcripts/m05-roads.md`
- `ボツ-12か月の運営/transcripts/m05-urban.md`
- `ボツ-12か月の運営/transcripts/m06-assembly.md`
- `ボツ-12か月の運営/transcripts/m06-economy.md`
- `ボツ-12か月の運営/transcripts/m06-education.md`
- `ボツ-12か月の運営/transcripts/m06-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m06-finance.md`
- `ボツ-12か月の運営/transcripts/m06-fire.md`
- `ボツ-12か月の運営/transcripts/m06-health.md`
- `ボツ-12か月の運営/transcripts/m06-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m06-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m06-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m06-port.md`
- `ボツ-12か月の運営/transcripts/m06-roads.md`
- `ボツ-12か月の運営/transcripts/m06-urban.md`
- `ボツ-12か月の運営/transcripts/m07-assembly.md`
- `ボツ-12か月の運営/transcripts/m07-economy.md`
- `ボツ-12か月の運営/transcripts/m07-education.md`
- `ボツ-12か月の運営/transcripts/m07-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m07-finance.md`
- `ボツ-12か月の運営/transcripts/m07-fire.md`
- `ボツ-12か月の運営/transcripts/m07-health.md`
- `ボツ-12か月の運営/transcripts/m07-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m07-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m07-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m07-port.md`
- `ボツ-12か月の運営/transcripts/m07-roads.md`
- `ボツ-12か月の運営/transcripts/m07-urban.md`
- `ボツ-12か月の運営/transcripts/m08-assembly.md`
- `ボツ-12か月の運営/transcripts/m08-economy.md`
- `ボツ-12か月の運営/transcripts/m08-education.md`
- `ボツ-12か月の運営/transcripts/m08-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m08-finance.md`
- `ボツ-12か月の運営/transcripts/m08-fire.md`
- `ボツ-12か月の運営/transcripts/m08-health.md`
- `ボツ-12か月の運営/transcripts/m08-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m08-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m08-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m08-port.md`
- `ボツ-12か月の運営/transcripts/m08-roads.md`
- `ボツ-12か月の運営/transcripts/m08-urban.md`
- `ボツ-12か月の運営/transcripts/m09-economy.md`
- `ボツ-12か月の運営/transcripts/m09-education.md`
- `ボツ-12か月の運営/transcripts/m09-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m09-finance.md`
- `ボツ-12か月の運営/transcripts/m09-fire.md`
- `ボツ-12か月の運営/transcripts/m09-health.md`
- `ボツ-12か月の運営/transcripts/m09-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m09-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m09-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m09-port.md`
- `ボツ-12か月の運営/transcripts/m09-roads.md`
- `ボツ-12か月の運営/transcripts/m09-urban.md`
- `ボツ-12か月の運営/transcripts/m10-assembly.md`
- `ボツ-12か月の運営/transcripts/m10-economy.md`
- `ボツ-12か月の運営/transcripts/m10-education.md`
- `ボツ-12か月の運営/transcripts/m10-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m10-finance.md`
- `ボツ-12か月の運営/transcripts/m10-fire.md`
- `ボツ-12か月の運営/transcripts/m10-health.md`
- `ボツ-12か月の運営/transcripts/m10-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m10-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m10-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m10-port.md`
- `ボツ-12か月の運営/transcripts/m10-roads.md`
- `ボツ-12か月の運営/transcripts/m10-urban.md`
- `ボツ-12か月の運営/transcripts/m11-assembly.md`
- `ボツ-12か月の運営/transcripts/m11-economy.md`
- `ボツ-12か月の運営/transcripts/m11-education.md`
- `ボツ-12か月の運営/transcripts/m11-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m11-finance.md`
- `ボツ-12か月の運営/transcripts/m11-fire.md`
- `ボツ-12か月の運営/transcripts/m11-health.md`
- `ボツ-12か月の運営/transcripts/m11-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m11-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m11-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m11-port.md`
- `ボツ-12か月の運営/transcripts/m11-roads.md`
- `ボツ-12か月の運営/transcripts/m11-urban.md`
- `ボツ-12か月の運営/transcripts/m12-assembly.md`
- `ボツ-12か月の運営/transcripts/m12-economy.md`
- `ボツ-12か月の運営/transcripts/m12-education.md`
- `ボツ-12か月の運営/transcripts/m12-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m12-finance.md`
- `ボツ-12か月の運営/transcripts/m12-fire.md`
- `ボツ-12か月の運営/transcripts/m12-health.md`
- `ボツ-12か月の運営/transcripts/m12-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m12-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m12-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m12-port.md`
- `ボツ-12か月の運営/transcripts/m12-roads.md`
- `ボツ-12か月の運営/transcripts/m12-urban.md`
- `試し-1〜3か月目(改善途中)/command-log.txt`
- `試し-1〜3か月目(改善途中)/council/ledger-older.md`
- `試し-1〜3か月目(改善途中)/council/ledger-recent.jsonl`
- `試し-1〜3か月目(改善途中)/council/ledger.jsonl`
- `試し-1〜3か月目(改善途中)/council/m01-assembly.json`
- `試し-1〜3か月目(改善途中)/council/m01-assembly.md`
- `試し-1〜3か月目(改善途中)/council/m01-bill.md`
- `試し-1〜3か月目(改善途中)/council/m01-economy.md`
- `試し-1〜3か月目(改善途中)/council/m01-education.md`
- `試し-1〜3か月目(改善途中)/council/m01-finance.md`
- `試し-1〜3か月目(改善途中)/council/m01-fire.md`
- `試し-1〜3か月目(改善途中)/council/m01-health.md`
- `試し-1〜3か月目(改善途中)/council/m01-hooks.log`
- `試し-1〜3か月目(改善途中)/council/m01-minutes.md`
- `試し-1〜3か月目(改善途中)/council/m01-policy.md`
- `試し-1〜3か月目(改善途中)/council/m01-port.md`
- `試し-1〜3か月目(改善途中)/council/m01-roads.md`
- `試し-1〜3か月目(改善途中)/council/m01-run.json`
- `試し-1〜3か月目(改善途中)/council/m01-survey-economy.md`
- `試し-1〜3か月目(改善途中)/council/m01-survey-port.md`
- `試し-1〜3か月目(改善途中)/council/m01-survey-roads.md`
- `試し-1〜3か月目(改善途中)/council/m01-urban.md`
- `試し-1〜3か月目(改善途中)/council/m02-assembly.json`
- `試し-1〜3か月目(改善途中)/council/m02-assembly.md`
- `試し-1〜3か月目(改善途中)/council/m02-bill.md`
- `試し-1〜3か月目(改善途中)/council/m02-economy.md`
- `試し-1〜3か月目(改善途中)/council/m02-education.md`
- `試し-1〜3か月目(改善途中)/council/m02-finance.md`
- `試し-1〜3か月目(改善途中)/council/m02-fire.md`
- `試し-1〜3か月目(改善途中)/council/m02-health.md`
- `試し-1〜3か月目(改善途中)/council/m02-hooks.log`
- `試し-1〜3か月目(改善途中)/council/m02-minutes.md`
- `試し-1〜3か月目(改善途中)/council/m02-policy.md`
- `試し-1〜3か月目(改善途中)/council/m02-port.md`
- `試し-1〜3か月目(改善途中)/council/m02-roads.md`
- `試し-1〜3か月目(改善途中)/council/m02-run.json`
- `試し-1〜3か月目(改善途中)/council/m02-survey-finance.md`
- `試し-1〜3か月目(改善途中)/council/m02-survey-health.md`
- `試し-1〜3か月目(改善途中)/council/m02-survey-roads.md`
- `試し-1〜3か月目(改善途中)/council/m02-urban.md`
- `試し-1〜3か月目(改善途中)/council/m03-assembly.json`
- `試し-1〜3か月目(改善途中)/council/m03-assembly.md`
- `試し-1〜3か月目(改善途中)/council/m03-bill.md`
- `試し-1〜3か月目(改善途中)/council/m03-economy.md`
- `試し-1〜3か月目(改善途中)/council/m03-education.md`
- `試し-1〜3か月目(改善途中)/council/m03-finance.md`
- `試し-1〜3か月目(改善途中)/council/m03-fire.md`
- `試し-1〜3か月目(改善途中)/council/m03-health.md`
- `試し-1〜3か月目(改善途中)/council/m03-hooks.log`
- `試し-1〜3か月目(改善途中)/council/m03-minutes.md`
- `試し-1〜3か月目(改善途中)/council/m03-policy.md`
- `試し-1〜3か月目(改善途中)/council/m03-port.md`
- `試し-1〜3か月目(改善途中)/council/m03-roads.md`
- `試し-1〜3か月目(改善途中)/council/m03-run.json`
- `試し-1〜3か月目(改善途中)/council/m03-survey-economy.md`
- `試し-1〜3か月目(改善途中)/council/m03-urban.md`
- `試し-1〜3か月目(改善途中)/council/plan-city.md`
- `試し-1〜3か月目(改善途中)/council/plan-economy.md`
- `試し-1〜3か月目(改善途中)/council/plan-education.md`
- `試し-1〜3か月目(改善途中)/council/plan-finance.md`
- `試し-1〜3か月目(改善途中)/council/plan-fire.md`
- `試し-1〜3か月目(改善途中)/council/plan-health.md`
- `試し-1〜3か月目(改善途中)/council/plan-port.md`
- `試し-1〜3か月目(改善途中)/council/plan-review.md`
- `試し-1〜3か月目(改善途中)/council/plan-roads.md`
- `試し-1〜3か月目(改善途中)/council/plan-urban.md`
- `試し-1〜3か月目(改善途中)/mayor-note.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-assembly.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-economy-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-economy-fix2.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-economy.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-education-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-education.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-finance-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-finance.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-fire-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-fire.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-health-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-health-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-health.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-review0.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-review1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-review2.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-see.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-field.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-port-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-port-fix2.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-port.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-roads-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-roads.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-urban-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-urban.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-assembly.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-economy-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-economy.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-education.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-finance.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-fire.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-health.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-desk-rebill.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-desk-see.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-desk.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-field.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-port.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-roads.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-urban.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-assembly.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-economy.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-education.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-finance.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-fire.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-health.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-desk-rebill.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-desk-see.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-desk.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-field.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-port-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-port.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-roads.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-urban.md`
- `試し-改善後1か月目(1回目)/command-log.txt`
- `試し-改善後1か月目(1回目)/council/ledger-older.md`
- `試し-改善後1か月目(1回目)/council/ledger-recent.jsonl`
- `試し-改善後1か月目(1回目)/council/ledger.jsonl`
- `試し-改善後1か月目(1回目)/council/m01-assembly.json`
- `試し-改善後1か月目(1回目)/council/m01-assembly.md`
- `試し-改善後1か月目(1回目)/council/m01-bill-2.md`
- `試し-改善後1か月目(1回目)/council/m01-bill.md`
- `試し-改善後1か月目(1回目)/council/m01-economy.md`
- `試し-改善後1か月目(1回目)/council/m01-education-map.jpg`
- `試し-改善後1か月目(1回目)/council/m01-education.md`
- `試し-改善後1か月目(1回目)/council/m01-finance.md`
- `試し-改善後1か月目(1回目)/council/m01-fire.md`
- `試し-改善後1か月目(1回目)/council/m01-health.md`
- `試し-改善後1か月目(1回目)/council/m01-hooks.log`
- `試し-改善後1か月目(1回目)/council/m01-minutes.md`
- `試し-改善後1か月目(1回目)/council/m01-policy.md`
- `試し-改善後1か月目(1回目)/council/m01-port-map-coast.jpg`
- `試し-改善後1か月目(1回目)/council/m01-port.md`
- `試し-改善後1か月目(1回目)/council/m01-roads.md`
- `試し-改善後1か月目(1回目)/council/m01-run.json`
- `試し-改善後1か月目(1回目)/council/m01-survey-economy.md`
- `試し-改善後1か月目(1回目)/council/m01-survey-port.md`
- `試し-改善後1か月目(1回目)/council/m01-survey-roads.md`
- `試し-改善後1か月目(1回目)/council/m01-urban.md`
- `試し-改善後1か月目(1回目)/council/plan-city.md`
- `試し-改善後1か月目(1回目)/council/plan-economy.md`
- `試し-改善後1か月目(1回目)/council/plan-education.md`
- `試し-改善後1か月目(1回目)/council/plan-finance.md`
- `試し-改善後1か月目(1回目)/council/plan-fire.md`
- `試し-改善後1か月目(1回目)/council/plan-health.md`
- `試し-改善後1か月目(1回目)/council/plan-port.md`
- `試し-改善後1か月目(1回目)/council/plan-review.md`
- `試し-改善後1か月目(1回目)/council/plan-roads.md`
- `試し-改善後1か月目(1回目)/council/plan-urban.md`
- `試し-改善後1か月目(1回目)/mayor-note.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-assembly.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-education-recheck.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-education.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-fire.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-health-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-health-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-health.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-fix.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-planadj.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review0.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-see.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-field.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-urban-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-urban.md`

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 9)
