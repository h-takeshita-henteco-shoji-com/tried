# 10か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 15:58〜15:58)

- 元のファイル: [m10-policy.md](m10-policy.md)
- ゲーム内の日付: 2050-10-08、保存: fukuoka-plan-m10
- 重点: 5-1・5-2 観光(名所と attractiveness、Tourism の収入)、5-1・5-2(入口) 旅客の駅・港・空港、6-1 都心部の機能強化

- 見たもの: [m10-policy.md の「見たもの」](m10-policy.md#見たもの)(17 行)
- 判断の根拠:

  公約4の2つの数字(観光客1,705、Tourism 週42)が前月より減り、入口は10か月0のままである。観光は市長の方針なので、名所と入口を重点の1と2にする。人口は180,168から180,117に減り、大卒の失業が増えたため、残る重点は6-1とする。汚染は37から27、ごみは10から7に下がり、火事も2に減ったので、今月は重点から外す。

- 捨てたもの:

  - 4-3 脱炭素社会(汚染27): 前月から下がり、原因も分からないまま。局が案を出すのは自由
  - 6-3 交通の流れ(54%): 4車線化は当たりと外れが半々で、流れは目標60に近づいている。局所の手は続くため、重点にしない
  - 8-1 貨物センター28755の止まり(540台): 6か月試しても動かず、重点にしない
  - 4-2 公園85棟: 目標100に遠いが、観光と大卒の失業を先にする

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

### 住宅都市みどり局(urban)(hooks の記録で 15:59〜16:03)

- 元のファイル: [m10-urban.md](m10-urban.md)
- 案 urban-1: 電気の届く道沿いに公園を1か所足す(762,1368)
  - 建設費 1000、週の維持費 +8、戻せる
  - 市の計画: 4-2
  - 議決: 要らない

- 見たもの: [m10-urban.md の「見たもの」](m10-urban.md#見たもの)(21 行)
- 判断の根拠:

  4-2 の公園などの数は 85 で、目標 100 まで 15 足りない。道沿いに電気が届き、入口の道があり、置ける空きは (762,1368) の1か所だけが確かめられた。この案は1,000 の建設費で、週 8 の維持費を増やすだけなので、守る線の内に収まる。事業2の月1か所を、第10月に進める。4-1 の高密度住宅の地価は、2250 付近の街区に空きがなく、道沿いの候補5か所がすべて取れなかったため、今月は案にしない。案の数は1件。ほかの候補は、道と電気の条件で確かめられず、出せなかった。

- 捨てたもの:

  - 公園 23298 の道(RoadNotConnected): 3回断られ、東の隙間は約10m で道が通らない。風力 19235 を取り壊す案は、電気と取り壊しの議決が要り、数は増えない。4-2 の数に効かないため、今月は出さない
  - 4-1 の南の空き(2250,955 N): 歩道と名所 7856(Friendly Neighborhood)にぶつかる
  - 4-1 の (2250,852) S、(2150,852) S: ObjectCollision。建物と道が重なる
  - 4-1 の (2150,955) N: 試しは通るが、取り壊す4棟(働き50)を失う。放棄された建物ではないため、取り壊しの案にしない
  - (530,1350) E: 公園 100 と風力 7015 にぶつかる
  - (664,1330) E: 道 24564 にぶつかる
  - (660,1398) E: 電気が 0。公園が動かない
  - (762,1390) W: 試しは通るが電気が未確認。(762,1368) の案と近すぎて、同じ場所の言い換え
  - 岩、石、崖などの Beautification の装飾(建設 100、維持費 0): Beautification には入るが、花や緑による潤いの施策の意図に合わない。数を稼ぐ手として使わない
  - 政策: 公園・緑に効く政策が一覧にない。観光の政策は市長の編成方針の外の施策で、局が出す案ではない

### 道路下水道局(roads)(hooks の記録で 16:00〜16:05)

- 元のファイル: [m10-roads.md](m10-roads.md)
- 案 roads-1: 旅客の駅(空き地3)への道・水道管・送電線
  - 建設費 2220、週の維持費 +30、戻せる
  - 市の計画: 6-3、5-1、5-2
  - 議決: 要らない
- 案 roads-2: 本土の名所(1580,-530)に送電線を通す
  - 建設費 280、週の維持費 +6、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m10-roads.md の「見たもの」](m10-roads.md#見たもの)(11 行)
- 判断の根拠:

  - 旅客の入口(駅)が今月の重点2に当たる。駅の道・水・電気の試しは通ったので、駅が決まれば道路下水道局が接続を担える。ただし、駅の場所と下水は未確認のため、案1は未確認とした。
  - 名所(1580,-530)の送電線は、試しで通り、費用 280 で安い。名所の建物がすでにあることは、試しの道具が AlreadyExists で確かめた。電力ポートの位置は未確認のため、案2も未確認とした。
  - 9月の4車線化(案1)は外れ寄りで、戻す条件はまだ満たさない。そのため、今月は4車線化の追加をしない。
  - 東の (1868,95) の blocked 37 は、今の情報では原因が分からないので、調査を1件出す。交差点の信号を足すかは、調査の結果で決める。
  - 統計像 11580 の電気は、局の経路では解けない。経済観光文化局の取り壊しの判断に任せる(計画の調整に従う)。
  - 案は2件にした。残りの候補は、確認が届いていない。

- 捨てたもの:

  - 統計像 11580 の電気の経路(4方向): 統計像にぶつかり、断られた。取り壊しの議案になるため、今月は局の案にしない。
  - z=-560 系の Basic Road への差し戻し: 戻す条件(2か月続けて増える)を満たさないため、今月は出さない。11月の見回りで決める。
  - 公園 23298 (690,1190) の道: RoadNotConnected の経路は、前の月に3回断られた。今月は試していない。次の月の候補にする。
  - (736,94) 42、(-932,-680) 38: 今月は試していない。測る場所が、ほかの案と重ならないかを先に確かめる。
  - 政策 HeavyTrafficBan: 大型車を減らす政策だが、貨物の不足とのつながりを読めない。今月は出さない。

### 港湾空港局(port)(hooks の記録で 15:59〜16:01)

- 元のファイル: [m10-port.md](m10-port.md)
- 案: なし

- 見たもの: [m10-port.md の「見たもの」](m10-port.md#見たもの)(26 行)
- 判断の根拠:

  - 担当の問題は、観光の入口(0)、貨物駅28755の止まり(540)。前の月の案は、どれも採られていない(9月も案なし)。前の月の調査(m09-survey-port.md)は見つからなかった
  - 旅客の入口は、計画の第10月の条件(水・下水・電気の試しが通る)を満たさなかった。水は通ったが、電気の直線は断られ、下水の網はない。外への線路も未確認。実行可否は未確認のため、案にしない
  - 港の岸の候補4点は、すべて HeightTooHigh か既存のドックとぶつかった。港の案は出せない
  - 28755 の止まりは、原因が出口の不足か道の混みか分からない。道は空いている(s03-1 の記録)が、敷地の中の待ちが続く理由は確かめていない。調査を1件出す
  - 政策は、担当の問題に効くものが見当たらなかった。観光の効き(Recreational Use、SmallBusiness)は、前の月に効きが切り分けられなかった(市政ノートの記録)
  - 案の数は0。調査1件を出す

- 捨てたもの:

  - 旅客の駅 (700,1700) の案: 電気の直線が断られ、下水の網がなく、外への線路が未確認。実行対象が確認できないため出せない。11月に電気と下水の別経路が通れば、再提出する
  - 港の旅客の岸(4点): HeightTooHigh か既存のドックにぶつかるため、候補にならない
  - 空港(Airport 150,000、週 4,800): 平らな空き地は道路と電気・水・下水から遠い。週 4,800 の維持費は、守る線の余裕 約 6,000 のほとんどを使う。条件が未確認のため、出さない
  - 貨物駅28755の増設(Cargo Center): 原因が分からないまま増やすと、取り壊しや無駄な建設になる。調査の結果を見てから出す

### 経済観光文化局(economy)(hooks の記録で 16:00〜16:07)

- 元のファイル: [m10-economy.md](m10-economy.md)
- 案 economy-1: 名所 Servicing Services を (1580, -530) に置き、道と電気と水をつなぐ
  - 建設費 21200、週の維持費 +348、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m10-economy.md の「見たもの」](m10-economy.md#見たもの)(17 行)
- 判断の根拠:

  - 観光の数字(観光客 1,705、Tourism 週 42、attractiveness 平均 2)は、いずれも目標から遠い。名所の棟数は 9 で、目標 10 に1棟足りない。名所を1棟足すのが、確かめられた手の中で最も直接に効く
  - 候補地は街の中の4か所(1580,-530、1430,-640、1930,-260、2520,-440)を試した。1580,-530 だけが建物の置き場所として通った
  - 1580,-530 は、名所の数と attractiveness の両方に効く見込みがある。電気と水は、経路を (1683,-514) から引き直せば通る見込みがある
  - 実行可否は「未確認」。電気と水のつなぎ口は、建物を置いてからでないと分からない。試しの道具で確かめた線も、つなぎ口の位置が違えば試し直しになる。このため executionReady は false
  - 費用は 21,200(建設)、約 348/週(維持)。守る線(週の収支 +3,000、所持金 1,874,000)と、10月の維持費の上限(3,700)に収まる
  - 案は1件にした。候補地の空きが少なく、2件目は同じ地区で試すしかないため、件数を埋めるための案は出さない
  - 調査は1件。名所を置いたあとの attractiveness の変化を、置く前の基準と比べて確かめる。効き目が分からない手なので、次の月の手を決めるために必要

- 捨てたもの:

  - 島Bへの名所(StatueOfWealth は AlreadyExists。島Bの電気・水は風力 44460 のみで、名所を置く場所に網がない): 配管と電気の延長が要り、費用と操作が多い。今月は見送る
  - 空き地3の名所 11580 の電気の修理: 前月まで5回、同じ手を続けた。6回目は打たない(編成方針)
  - 旅客の入口(港湾空港局の担当): 局の担当外。港湾空港局に求める事業として計画に残す
  - 政策 RecreationalUse の有効化: 前月の実測で効きが分からないまま外した(4月)。効きの記述は一覧にない。今月は出さない
  - 政策 SmallBusiness の有効化(317/週): 観光の収入の効きが実測されておらず、前月まで採られた実績でも効果が見えない。今月は出さない
  - 公園 23298 の道の接続: 担当が道路下水道局と住宅都市みどり局。局の担当外

### 保健環境局(health)(hooks の記録で 15:59〜16:03)

- 元のファイル: [m10-health.md](m10-health.md)
- 案 health-1: 焼却場 10351 を止めて、北東の汚染の印を減らす(試し)
  - 建設費 0、週の維持費 +-1440、戻せる
  - 市の計画: 4-3
  - 議決: 要らない

- 見たもの: [m10-health.md の「見たもの」](m10-health.md#見たもの)(13 行)
- 判断の根拠:

  - 9月に立てた計画の前提(工場の2列が汚染の出どころ)は、今月の確かめで外れた。汚染の集まりは2か所あり、どちらも焼却場の近くにある。1か所(2096,822)は 10351、もう1か所(3689,-85)は 2267。どちらの集まりにも、100m 以内に工場はなかった。計画を直し、理由を計画の変更に書いた。
  - 案1 は、道具で確かめた対象(10351)に、既存の道具 `set_building_active` を使う。建設も接続もないので、実行条件は確認済みにした。効きの量は見積もれないため、試しとして出す。
  - 2267 は貯蔵 96%。先に止めるとごみの行き先が遠くなるので、今月は止めない。
  - 件数は1件。政策の手(Recycling)は週 -13,000 の見込みで守る線に届かず、工場の手は道具で確かめられない。死体の印は原因が未確認なので、調査に回した。

- 捨てたもの:

  - 政策 Recycling(汚染とごみに効く見込み): 住宅税の収入 267,164 の -5% は、週 約 -13,400。週の収支 +8,997 から守る線 +3,000 を引くと余裕は約6,000で、超える。
  - 政策 HeavyTrafficBan(費用0): トラックを止めると、品物がない店 218 がさらに増える。6-4・7-1 の数字に悪い。
  - 工場の列を止める手: `set_building_active` はサービスの建物用と道具の説明にあり、工場に効くかを確かめられない。
  - 焼却場 2267 の停止(今月): 貯蔵 96% で、ごみの行き先が遠くなる。3月に同じ手でごみが 11 から 22 に増えた。11月の判定に回す。
  - 埋立地の受け皿(今月): ごみの印は 7 で、15 を超えていない。計画の条件を満たさない。
  - 木を植える(汚染): 1月の試し(m01-5)で効かなかった。
  - 死体の印の手(今月の案): 原因が分からないため、調査で確かめる。

### 教育委員会(education)(hooks の記録で 15:59〜15:59)

- 元のファイル: [m10-education.md](m10-education.md)
- 案: なし

- 見たもの:

  - `services`: 小学校 14,268、高校 24,360、大学 36,540。働き手 84,162、働き口 87,009
  - `citizens_summary`: 子ども 9,609、10代 21,303(6月は 22,029 で減少中)、大卒の失業 8,293、失業 8,401。来ない市民は0(下水・水・電気)
  - `city_info`: 人口 180,117、所持金 2,270,429、週の収入 336,274、支出 327,277(収支 +8,997)、dialog なし
  - `list_policies`: EducationBoost は active=false、costPerWeek 7,940(学校の維持費の+25%)。SmokingBan と BigBusiness は active=true。policyExpensesPerWeek 10,774。EducationBoost は定員を増やさず、教育の質に効くだけなので、担当の数字には効かない

- 判断の根拠:

  2-3 の目標(小学校の定員が子ども以上、高校の定員が10代以上)は、今月も満たしています。高校の余裕は6月の 2,331 から 3,057 に増え、10代が減っている分だけ広がっています。計画の第7〜12月は「余裕を見る。1,000を切ったら置く」なので、今月は見るだけです。
  EducationBoost を入れる案は、週 7,940 の増えで週の収支が約 +1,057 になり、守る線 +3,000 を下回るため採りません。大卒の失業 8,293 は働き口の不足が原因で、学校の定員の数字ではないため、教育委員会の案の対象にしません。
  前の月(9か月目)は教育委員会の案がなかったため、答え合わせはありません。計画の変更はありません。

- 捨てたもの:

  - 高校1校(建設費 24,000、週 +560): 余裕が 3,057 あり、計画の条件(1,000を切る)に当たらないため。
  - 小学校1校(建設費 10,000、週 +160): 余裕が 4,659 あり、計画の条件に当たらないため。
  - EducationBoost を有効にする(週 7,940): 守る線 +3,000 を割るため。また、定員の数字に効かないため。

### 消防局(fire)(hooks の記録で 15:59〜16:00)

- 元のファイル: [m10-fire.md](m10-fire.md)
- 案: なし

- 見たもの: [m10-fire.md の「見たもの」](m10-fire.md#見たもの)(14 行)
- 判断の根拠:

  10月(10/8)の数字は、火事2、犯罪4で、合計6。目標の4以下を外れた。ただし、犯罪の印が3以上なのは10月が初めてで(8月末は1)、事業1の条件(3か月続けて3以上)は未達。移す手は、前提の「警察の効きが届いていない」が外れたため、今月は根拠がない。火事2は、1棟ずつで場所が違い、続いた場所ではない(同じ場所の2か月続きの条件は未達)。よって案は出さず、調査を1件出す。
  答え合わせ(前の月): 9月は案なし。前の月の案はない。事業2の閉じた判断は、8月末の火事0で当たっていた。10月も、火事は同じ場所に続いていない。
  12か月の計画は、10月を「調査のみ」に替えた(plan-fire.md の計画の変更)。11月に、調査の結果で事業1を動かすか決める。

- 捨てたもの:

  - 犯罪の印の移し(45584 を (3704,-73) 付近へ): 移す前提の「届いていない」が外れた。移すと西の犯罪が出る見込み(西の警察の効きが落ちる)。取り壊しと同じく戻せない手なので、今月は出さない。
  - 犯罪の印の新設(12,000、週 480): 届いている場所に足す効きは見積もれない。原因が分かってから出す。
  - Fire House を (-2144,-244) に置く: 火事の効きは届いている(43〜222)。1棟の火事で、続いていない。
  - 政策 SmokeDetectors: 週 57,882 で守る線を大きく割る。

### 財政局(finance)(hooks の記録で 16:00〜16:00)

- 元のファイル: [m10-finance.md](m10-finance.md)
- 案: なし

- 見たもの: [m10-finance.md の「見たもの」](m10-finance.md#見たもの)(8 行)
- 判断の根拠:

  前の月の答え合わせ: 9月の案 m09-4(事務所税 3%から 2%)は採られ、実行できた。期限は11月の月例で、今月は判定前。今月の数字は、事務所 L3 が 3,274 のまま、大卒の失業は citizens_summary で 6,849(8月末)から 8,293 に増えた。demand_breakdown の数えでは 7,703 から 9,185 に増えた。Office 収入は 24,451 から 16,470 に下がった。事務所の建て替えは数週かかるため、まだ分からない(1回目)。
  計画との照合: 週の収支は +8,997 で、計画の見込み +6,718 より高い。守る線 +3,000 の上で、計画の前提は崩れていない。計画は10月を見回りと月末の観察と定めているので、計画は直さない。
  案を出さない理由: 上の「案なし」の3点のとおり。EducationBoost は、同じ大卒の失業を測る試しに重なるため、今は入れない。予算の減り(例: healthcare 150 を 120 へ)で枠を作る手は、健康(目標80 に対し 89)と治安(火事2、犯罪4、目標4以下)への効きが分からない。試しとして出すには、測る数と基準を揃える必要があるが、2か月しか残らないため、今月は出さない。

- 捨てたもの:

  - 政策 EducationBoost の再投入(週 7,940): 守る線の余裕 約 5,997 を超える。調整19の10月の上限(週 3,700)にも入らない。事務所税の試しと同じ大卒の失業を測るため、切り分けられない。
  - 予算 healthcare 150 を 120 にして枠を作る案(週の減り 約 15,000 の見込み): 健康と死者の印への効きが未確認。試しとして出すと、測る数(健康の平均)が 89 から目標 80 のどこまで下がるかを、12月まで見るしかない。残り2か月では判定できない。
  - 事務所税を 3% に戻す案: 11月の判定の前に戻すと、事務所税の試しが1か月で打ち切られる。11月の月例で判定する。
  - 道路の予算 120 を 100 に戻す案(週の減り 約 1,483): 6-3 の交通の流れに効くが、保留の条件(流れが60に届き、維持費の枠が足りないとき)を満たしていない。
  - 税の変更(住宅・商業): 住宅需要 17、商業需要 2 で、事業の入口と名所に直接効く見込みがない。効きの量も見積もれない。

## 4. 差し戻しと再調査

- 経済観光文化局: economy-1(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m10-bill.md](m10-bill.md)
- 採った m10-1: 公園を(762,1368)に1か所置く(元 urban-1、議決は要らない)
- 採った m10-2: 焼却場10351を止める試し(元 health-1、議決は要らない)
- 採らなかった roads-1: 駅の場所が決まらず下水の網もないため、線だけ引いても無駄になる。
- 採らなかった roads-2: economy-1と同じ(1580,-530)で、電気待ちの建物がある根拠が道具で確かめられていない。
- 採らなかった economy-1: 電気と水のつなぎ口の位置と、入口の道路が既存道路につながる形が未確認。

- 見たもの:

  - `Read`: 8つの局の案、plan-health、plan-city、mayor-note、編成方針
  - 道具の再実行はしていない。局の案に書かれた `test_place_building` と `test_build_line` の結果を使った

- 判断の根拠:

  採れる案は urban-1 と health-1 の2件で、どちらも対象と操作が確認済みである。費用は建設費 1,000、週の維持費は +8 と -1,440 で、守る線(週の収支 +3,000 以上、所持金 1,874,000 以上)に収まる。観光の案 economy-1 は、つなぎ口が未確認なので、条件付きにして今月のうちに調べ直させる。調査は、分からないことの一覧に残る事務所税、死体の印、犯罪の印の3件を採った。

- 捨てたもの:

  - 観光の入口(旅客の駅): 港湾空港局の案がなく、roads-1 は駅の場所が決まらない。10か月続けて0のまま
  - 港湾空港局の調査(28755): 重点でなく、上限3件のため見送り
  - 道路下水道局の調査(東の blocked 37): 上限3件のため見送り。6-3 は流れ54%で目標に近い
  - 経済観光文化局の調査: economy-1 を採っていないので、置く前後の比べが成り立たない

## 6. 議会: 可決と否決(hooks の記録で 16:08〜16:08)

- 元のファイル: [m10-assembly.md](m10-assembly.md)
- m10-1 財政: 可決。建設費1,000、週の維持費+8で守る線に収まる。
- m10-2 財政: 可決。週の維持費-1,440で収支は良くなる。守る線に収まる。
- 可決した種類(hooks が見る): なし

- 見たもの:

  - `economy`: 税と予算の今の値。変更の議案はない
  - `city_info`: 週の収支 +8,997、所持金 2,270,429
  - `Read`: council/m10-bill.md

- 判断の根拠:

  2件とも議決の要らない施策なので、点5だけで確かめた。収支は +3,000 を上回り、所持金も 1,874,000 を大きく上回る。税、予算、融資、取り壊しの議案は今月にない。

- 捨てたもの:

  - m10-2: ごみの印が増える恐れがあるが、戻す条件と手が書かれ、議会の4点には当たらないので可決した

## 7. 実行する市長: 実行と見回り(hooks の記録で 16:09〜16:15)

- 実行してよい施策: m10-1、m10-2
- 実行した: m10-1、m10-2
- 失敗した: なし
- 臨時: なし
- 見回り 2050-10-18: 人口 180059、所持金 2284474、週の収支 10705、幸福度 89
- 見回り 2050-10-28: 人口 179947、所持金 2298936、週の収支 10145、幸福度 89
- 報告:

  m10-1 と m10-2 を打ち、境目に当たらず臨時もなかった。hooks に止められた手はなく、取り壊しもしていない。
  - m10-1: 公園 19278 を (762,1368) に置いた。費用 1,000、入口の道 15421 に距離10、電気あり。Beautification は 85 から 86 棟になった。
  - m10-2: 焼却場 10351 を停止した。月末(11/7)の Pollution は 27 から 30 に増えた。ただし、集まりは (3665,-85) に移っていて、10351 の周りではない。map_layer の平均は 78 から 72 に下がった。
  - Garbage は 7 から 9、13、8 と動いたが、15 を超えなかったので戻していない。
  - 月末の数字は、人口 179,848、所持金 2,313,772、週の収支 +10,680、観光客 1,763、Tourism 週 27。人口は 10/8 の 180,117 から減り、Tourism は 10/8 の 42 から減った。
  - 調査 s10-1〜3 は council の m10-survey-finance.md、m10-survey-health.md、m10-survey-fire.md に書いた。
  - 手順のずれ: 月末(11/7)の計測は 3 回目の advance の後で行った。調査の引数は見回り時点のもので、月末は一部(hearse、crime のマップ)を呼んでいない。
  - ログは command-log.txt に写した。市政ノートは追記済み。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m10、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 15:57〜16:25(hooks の記録の時刻から)、道具の行 274
- 議会が可決した種類: なし
- 議決が要る道具の呼び出し: 0 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 601 件
- hooks の拒否: 0 回

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
