# 4か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 13:54〜13:55)

- 元のファイル: [m04-policy.md](m04-policy.md)
- ゲーム内の日付: 2050-04-01、保存: fukuoka-plan-m04
- 重点: 5-1、5-2 観光、6-4、7-1 企業の立地、地場企業、6-3 公共交通を主軸とした交通体系、8-1 物流・人流のゲートウェイ

- 見たもの: [m04-policy.md の「見たもの」](m04-policy.md#見たもの)(15 行)
- 判断の根拠:

  公約1(人口)と公約4(観光)が、どちらも前月より減って未達である。観光は市長の方針で毎月の重点に入れ、残りの2つは、人口減に効く働き口(6-4、7-1)と、目標から遠い交通・物流(6-3、8-1)を選んだ。街の地形の資料にある島と空き地は、これまで一度も名所の置き場所として確かめられていないため、局に伝えた。

- 捨てたもの:

  - 4-3 脱炭素(汚染35)、4-4 資源循環(ごみ18): 焼却場を止める手が外れ、別の手が出ていない。局の案が出れば、重点外でも採る
  - 3-4 日常生活の安全・安心(火事8、犯罪1): 合わせて9で目標4以下に遠いが、原因が分からず、調査の案を待つ
  - 1-2 健康、4-1 地価、4-2 公園、6-1 事務所L3: 目標に近いか、今月は公約1と4への効きが小さい
  - 3-3、2-3: 守る数字で、今月は問題がない

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

### 住宅都市みどり局(urban)(hooks の記録で 13:56〜13:58)

- 元のファイル: [m04-urban.md](m04-urban.md)
- 案: なし

- 見たもの: [m04-urban.md の「見たもの」](m04-urban.md#見たもの)(23 行)
- 判断の根拠:

  確かめた事実は次のとおりです。空き地3の道と電気は、道路下水道局の第4月と第5月の予定で、今月は進められません。空き地3の周りに住宅が0棟なので、長期計画の4-1の狙いは外しました。公園が4-2の数を増やす効きは残ります。街の中の空いた土地は、放棄店跡の撤去で働き口を失うか、稼働中の店や道路とぶつかり、置けませんでした。名所Aの周りの地価は66前後で、街の平均52より高く、公園や名所が地価を上げる見込みは残ります。
  4-1 の 58 が 62 に届かない原因は、どこが低いかを見ていません。そのため、施策は出さず、調査を1件出します。案の数は0です。件数を埋めるための案は作りません。

- 捨てたもの:

  - 放棄店跡 17281 と 29785 の跡に Regular Park: 稼働中の店 3608、15826、3037 がぶつかり、道路 29053、30829 も blocks=true で断られた。働き口も15失う。
  - 2240, 522 の空いた所: 埋立地(Landfill Site 45436)で塞がっている。
  - 岩や石の飾り(Boulder、Rock、100 と維持0): 公園などの数は増えるが、花や緑の潤いにはならない。数だけを増やすため、出さない。
  - HighTechHousing(週 20,228): 4-1 の地価との関係を確かめられず、維持費が大きすぎる。
  - 名所の追加: 経済観光文化局の担当。局は名所の位置を決めない。

### 道路下水道局(roads)(hooks の記録で 13:56〜14:01)

- 元のファイル: [m04-roads.md](m04-roads.md)
- 案 roads-1: z=-1010 の幹線3区間を4車線にする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 東の交差点2か所に信号を付ける
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-3: 空き地3(712,1644)に道と送電線を引く
  - 建設費 11520、週の維持費 +55、戻せる
  - 市の計画: 3-3
  - 議決: 要らない

- 見たもの: [m04-roads.md の「見たもの」](m04-roads.md#見たもの)(17 行)
- 判断の根拠:

  - 案1: 計画の4月の条件(流れが55%未満で、blocked が前より減った)は満たした(流れ53%、blocked 990→774)。計画どおり3区間を広げる。ただし、対象の周りの blocked は14で小さく、効きは小さい見込みと書く。費用は0で、残すことにした。
  - 案2: 4月の blocked は東の (2000,200) 周りに254台集まっている。前の信号の型(2か所で blocked を半分以下に減らした)を、この集まりに足す。費用は0で、交差点は2か所とも付けられることを確かめた。
  - 案3: 公園19の窓(第4〜5月)に合わせて、道と送電線を今月引く。建設費は11,520で、30,000 の上限に収まる。道と送電線の経路は、試しの道具で断られた経路を避けて、通る形を確かめた。
  - 案の数を3件にした理由: 担当の問題(6-3)に効く手は、東の信号、z=-1010 の広げ、の2つ。3件目は、計画の調整6(空き地3の前提)で、今月の窓に入るため。件数を埋めるための案は作っていない。
  - 案を出さなかった手: 下の「捨てたもの」を参照。

- 捨てたもの:

  - 政策 HeavyTrafficBan(トラックの通行を止める): 0円で流れを変えうる。しかし、トラックは品物を店に運ぶ。品物がない店は235で、6-4、7-1 の数字を悪くする。効きの見込みも確かめられていない。採らない。
  - 政策 FreeTransport(公共交通を無料にする): 0円で交通手段を変えうる。しかし、運賃の収入が0になる。収入の減りを確かめる道具がなく、効きも見込めない。採らない。
  - 幹線の Large Road 化(例: 10,000 / km): 6010、12970 は既に Large Road。Small 4 Lane の区間を広げる余地はあるが、今月は東の信号を先にする。費用の上限を守るため、次の月に見る。
  - 信号の予備 (1880,150): 案2の予備として残す。今月は付けない。
  - 駅への道と送電線(旅客の入口): 港湾空港局が駅の場所を届けていない。`test_build_line` の対象がないので、今月は出さない。
  - 島Bの橋: 計画の5月に引く。島の道と風力がそろうまで橋を引かない(計画の是正)。
  - 貨物センター28755の道の差し替え: 原因が道かどうかを港湾空港局が調べる。計画の第6月に出す。

### 港湾空港局(port)(hooks の記録で 13:56〜13:58)

- 元のファイル: [m04-port.md](m04-port.md)
- 案: なし

- 見たもの: [m04-port.md の「見たもの」](m04-port.md#見たもの)(13 行)
- 判断の根拠:

  - 入口の事業(港): 計画の閉じる条件(4月末までに岸の候補が1つも通らない)を満たした。港は閉じる。試した候補は11地点、落ちた理由は高さと建物。港の候補が通らないと分かったので、5月の港の試しは取りやめ
  - 駅の候補(貨物線の近く): 今月は試せる空きがなかった。計画に残すが、案にはしない
  - 貨物の止まり(8-1): 道は原因でない。止まりは敷地の中の待ち。道の差し替え(6月)は見送る。次の手は調査の結果で決める
  - 案の数: 0件。執行できる案がなく、実行条件が未確認のため

- 捨てたもの:

  - 旅客の港(岸の候補11地点): HeightTooHigh、ObjectCollision、CannotConnect で全部落ちた。場所の条件を変えても、今の街の岸では置けそうにない
  - 旅客の空港(Airport): 建設費 150,000、週 4,800。週の余裕(約 6,965)を超え、場所も未確認
  - Harbor02(120,000、週 1,920): 岸の条件が Harbor と同じで、置ける場所がない
  - 貨物センターの増設(60,000、週 1,440): 場所と接続が未確認。調査の結果を見てから出す
  - 道の差し替え(28755 の周りを太くする): 道が原因でないと確かめたので、出さない
  - 政策の変更(RecreationalUse、SmallBusiness): 観光の政策は経済観光文化局の担当。今月は港湾空港局の案に入れない

### 経済観光文化局(economy)(hooks の記録で 13:56〜13:59)

- 元のファイル: [m04-economy.md](m04-economy.md)
- 案 economy-1: 政策 RecreationalUse を外す(第4月の判定)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m04-economy.md の「見たもの」](m04-economy.md#見たもの)(18 行)
- 判断の根拠:

  第3月に試した政策 RecreationalUse は、4月末の判定で、観光の数字がどれも動かなかった(attractiveness 平均2、観光客1,742、Tourism 58)。政策の効きは見えないので、外すのが計画の判定どおりである(案1)。この案は費用0で戻せるが、観光の数字を上げる見込みはない。名所の2棟目は、市街の道に面した空きが名所の大きさに足りず、試しの道具でどの候補も道路か既存の建物と重なった。空き地3の道を待つのが計画どおりで、今月の案にはできない。品物がない店235軒の原因は、道、量、店の位置のどれか分からないので、調査で見る(政策の案は1件まで)。

- 捨てたもの:

  - 名所の2棟目(放棄された店の跡、7016・9072・9170・4226・11199・17223): 試しの道具で、どれも道路か既存の建物と重なった。名所の大きさ(6〜16マス)に、店を外しても空きが足りない。空き地3の道が引かれる第5月まで待つ
  - 名所を空き地2・4・5 に置く案: 道路から400m以内に道がなく、道を引く工事は道路下水道局の担当。今の案にはできない
  - 島Bの名所(StatueOfWealth): 橋と電線が未確認。第7〜8月の計画どおり
  - 政策 SmallBusiness を外す案: Tourism は42→66→74→68→58と動き、重なりが切れないため、外すと判定できない。月1件の政策の変更を RecreationalUse に使うため、次の月に回す
  - 働き口(6-4): 道に面した空きが少なく、税も既に低い。計画の見送りのまま
  - 品物の対策の案: 原因が決まっていないので、調査の結果を待つ。港湾空港局の貨物と道路下水道局の道は、他局の担当なので、案を書かず、調査の結果を基に求める

### 保健環境局(health)(hooks の記録で 13:56〜13:59)

- 元のファイル: [m04-health.md](m04-health.md)
- 案 health-1: 第1候補に診療所を1棟置く(放棄された商店を取り壊す)
  - 建設費 10000、週の維持費 +400、戻せない
  - 市の計画: 1-2
  - 議決: 要る(取り壊し)
- 案 health-2: 満杯の埋立地2つを取り壊し、ずらした位置に建て直す
  - 建設費 8000、週の維持費 +320、戻せない
  - 市の計画: 4-4
  - 議決: 要る(取り壊し)

- 見たもの: [m04-health.md の「見たもの」](m04-health.md#見たもの)(29 行)
- 判断の根拠:

  - 健康の平均は 78 で、79未満の条件を満たす。計画の第4月の案で、第1候補(-1000, -1585)に1棟を置く。確認済みで、放棄された商店を取り壊すだけで、働きと家の損失は0(`preview_bulldoze`)。議決は取り壊しの1種類。
  - 満杯の埋立地が 157 と 25692 の2つになった。計画にない変化なので、計画の変更に書いた。1月に満杯の入れ替えで当たった手と同じで、取り壊し後の建て直しは試しの道具で ok。費用は小さく、週の収支は +9,303 から約 +8,583 になるが、守る線 +3,000 の上で収まる。
  - 3月の調査 s03-2 は、2267 の処理が動き、貯蔵が 333,750 → 251,468 と減ったことを示す。焼却場の手は、次の手として出さない。
  - 汚染の印 35(目標15以下)は、工場群の原因が未確認のため、今月は案を出さない(計画の5〜7月)。
  - 案は2件。今月の確認済みの手の数で決めた。確認できなかった候補(入口の道がない候補など)は入れない。

- 捨てたもの:

  - 政策 Recycling(税-5%、ごみ-15%): 税の減り(約 13,200 / 週)で、守る線の週の収支 +3,000 を、今の +9,303 から割り込むおそれがあるため。
  - 政策 SmokingBan(費用0): 健康への効きが分からない。診療所と同じ月に入れると、健康の平均の変化の原因を分けられない。診療所の効きが出る8月以降に、試しとして検討する。
  - 診療所の候補(-1068, -1526)と(-1244, -1526): 入口の道路がなく、(-1244, -1526)は家38戸を失う。調整12(入口の道路がある候補だけ)に従い、使わない。
  - 診療所の候補(-60, -698)、(2150, -1180)、(2040, -1180): ObjectCollision で置けない。
  - 45892 の active=false: まだ空になっていない(85%、emptying)。空になったら計画どおり行う。
  - 2267 を止める案: ごみの印が15を超える(2月の経験)。

### 教育委員会(education)(hooks の記録で 13:56〜13:56)

- 元のファイル: [m04-education.md](m04-education.md)
- 案: なし

- 見たもの:

  - `services`: 小学校の定員 14,268、高校 24,360、大学 36,540。電気・水・下水は余裕あり、crimeRate 4、満杯の埋立地 2(157、25692)、墓地の満杯 0
  - `citizens_summary`: 子ども 10,870、10代 22,226、若者 32,330、成人 67,750。失業 5,761(大卒 5,667)、病気 1,761、健康の平均 78
  - `city_info`: 人口 178,486、所持金 2,110,220、週の収支 +9,303(収入 347,484、支出 338,181)、観光客 1,742(訪問 139)、来ない市民 0 / 0 / 0、dialog なし
  - `list_policies`: 政策の名前と有効状態を確認。学校に関係する政策は EducationBoost(有効、週 7,940。学校の維持費の +25%。政策の費用ではなく教育の支出に入る)。RecreationalUse(有効、0)、SmallBusiness(有効、315)、BigBusiness(有効、3,928)、ほかは無効。政策一覧の全体の費用は 10,980(policyExpensesPerWeek)

- 判断の根拠:

  - 担当の数字は、どちらも長期計画の目標を満たしている。子どもと10代の数は、前月からも減っている。今月の予定どおり、置く基準(余裕1,000未満)に入っていないので、建設は出さない。
  - 編成方針の重点(5-1・5-2 観光、6-4・7-1 企業と働き口、6-3・8-1 交通)に、教育の施策は入っていない。教育の案は、重点の外にあたる。
  - 政策で増やせる学校の定員はない。EducationBoost は学校の維持費を増やす政策で、定員は変えない。教育の施策を増やす手は、今月の数字では要らない。
  - 前の月(3月)の教育は案なしだった。今月も案なしのため、答え合わせの対象はない。

- 捨てたもの:

  - 高校を1校置く(建設費 24,000、週の維持費 +560): 余裕が 2,134 あり、置く基準の 1,000 を超えている。今月に置くと、10代が増えていない時点での維持費の増えになる。計画の第7月以降の判断に残す。
  - 小学校を1校置く(建設費 10,000、週の維持費 +160): 余裕が 3,398 あり、基準の 1,000 を超えている。子どもは減っている。
  - 高校の候補地の試し(zone_map と test_place_building): 計画の第3月の作業だったが、第3月は案を出さず候補地の試しも行っていない。今月は置かない見込みのため、試しは行わない。計画の第6月に、増え方が続くときに確かめ直す。
  - EducationBoost の解除: 週 7,940 の教育支出を減らせるが、学校の運営に効く施策の変更で、担当の数字の目標に直接の効きがない。議会の予算の範囲で、教育の数字を見ながら判断する。

### 消防局(fire)(hooks の記録で 13:56〜13:57)

- 元のファイル: [m04-fire.md](m04-fire.md)
- 案 fire-1: 工場周りの火事に Fire House を1つ足す(2262,-1190)
  - 建設費 12000、週の維持費 +560、戻せる
  - 市の計画: 3-4
  - 議決: 要らない

- 見たもの: [m04-fire.md の「見たもの」](m04-fire.md#見たもの)(20 行)
- 判断の根拠:

  - 火事の印は8で、目標の合計4以下に対し、犯罪の1と合わせて9。3-4 の残りは、ほぼ火事。
  - 3月の調査は実行されず、結果がない。そのため、候補AかBを決める前提が欠けた。道具で確かめ直すと、消防署 49026 の消防車は1/8台しか使われておらず、候補Bのトリガー(7台以上使用中)に当たらない。候補Bは外す。
  - 工場 12882 は3月と4月の2回とも燃えていて、最寄りの消防署からは約1,150m。候補Aは試しの道具で通り、電気・水・下水も届く。このため、今月の案として出す。効き目は1棟分で小さい。
  - 3棟の燃え続け(2002、5804、13425)は、道が来ていて、消防車も空いている。原因は道具では決まらない。調査で、同じ3棟が消防車の到着と合わせて消えるかを見る。
  - 案は1件。調査を1件。警察署は犯罪の1で足さない。SmokeDetectors は週の費用が収支を超えるため採らない。

- 捨てたもの:

  - 候補B(消防署を (3255,-805) 付近に足す): 消防車が1/8台しか使われておらず、トリガーに当たらない。覆いは231と高い。調査の結果で、5月に出し直す
  - 候補A を (2100,-1000) に置く: 事務所 12386 を壊し、働き口13を失う。入口の道路もない。不採用
  - Fire Station(建設費 60,000、週 1,440)を置く: 工場の燃え1棟に対して、費用が大きい。今は不要
  - 政策 SmokeDetectors: 週の費用 57,748。週の収支を赤字にするため、採らない
  - 警察署を移す: 犯罪の印は1で、警察の定員(980 のうち使用は389)に余裕がある。今は不要

### 財政局(finance)(hooks の記録で 13:56〜13:56)

- 元のファイル: [m04-finance.md](m04-finance.md)
- 案: なし

- 見たもの:

  - `city_info`: 人口 178,486、所持金 2,110,220、週の収支 +9,303(収入 347,484、支出 338,181)、幸福度 85、観光客 1,742(訪問 139)、来ない市民 0/0/0、需要 住23・商2・工58、dialog なし
  - `economy`: 税 住低9・住高7・商低9・商高3・工3・事務所3。予算 道路120、ごみ・医療・警察・公園・バス150、消防140、教育120、港120(ごみ・医療・警察・公園は上限の150)
  - `list_policies`: 有効は EducationBoost(週 7,940、教育の支出の内訳)、RecreationalUse(週 0)、BigBusiness(週 3,928)、SmallBusiness(週 315)。ほかは無効。policyExpensesPerWeek 10,980。費用0の RecreationalUse は有効のまま
  - `economy_breakdown`: Tourism 週 58(Commercial の内訳)、Office 収入 24,465、道路の維持費 8,541(Basic Road 6,115、Small 4 Lane 694、Medium 763、Large 422 など)、政策の費用 10,980
  - `traffic`(x -500、z -300、r 300): flow 53、cars 48、blocked 0、congestion 18
  - `demand_breakdown`: 働き口 86,569、空き働き口 3,329、空き家 5,062、失業 7,090(大卒 6,897、大卒の働ける人 82,724)、高卒 26、小卒 29、無学 138

- 判断の根拠:

  - 守る線: 週の収支は +9,303 で +3,000 を超え、所持金は 2,110,220 で 1,874,000 を超える。3か月続けて下がる規則も当たらない(3月 +12,912、4月 +9,303)
  - 道路 120 の判定: 基準 51 に対し 53。1月末の 50 から上がり、街全体の flow も 53% に上がった。ただし、測り方の差が2程度ありうる。計画の「動かないとき戻す」には当たらないので、120 を続ける
  - SmallBusiness: 3月まで 42→66→74→68 と動いたが、4月の 58 で基準の 42 より上を保っている。効きは RecreationalUse と観光客の増えと重なり、切り分けられていない。計画の「4月末も下回る」を見てから外すか決める
  - 事務所の税: 大卒の失業は 6,897 で、事務所を増やす根拠が出ていない。計画どおり、調査の結果を5か月目に判断する。今月は案にしない
  - 観光(公約4)と人口(公約1)の目標は、局の手では動きにくい。名所と入口は、ほかの局の案と島の道の結果が要る
  - 案の数を0にした理由: 計画の今月の予定に、新しい税・予算の案がない。道路 120 は続けるだけで、議決を要する変更がない。前の月は案がなかった(3か月目)ため、今月の空白を続けると、大卒の需要の調査が5か月目に間に合わない
  - 答え合わせ(3か月目): 3か月目は案なし。計画の大卒の需要の調査は、出ていなかった(council/m03-survey-finance.md がない)。今月の調査で代える

- 捨てたもの:

  - 商業(低密度)の税 9→8: 道路 120 のまま(計画どおり、今は出さない)。打てば、条件(道路 100 に戻る)に反する
  - 事務所の税 3→2(週 -約8,100): 大卒の失業が動いていない。調査の結果を5か月目に見て決める。今出すと、計画の順が崩れる
  - SmallBusiness を外す(週 +315 の余裕): Tourism は 58 で、4月末の読みを待つ。今外すと、効きが出ていたかどうかを確かめられない
  - RecreationalUse を外す・出し直す(費用0): 効きが切り分けられていない。費用の変化もないので、今月は触らない
  - 予算を上げる(ごみ・医療・警察・公園): すでに上限150のため、上げられない
  - 消防の予算 140 を 150 にする: 火事の印 8 の原因が未確認で、効きが分からない。消防局の調査を待つ
  - 政策 HighTechHousing(週 20,228)、IndustrySpace(週 4,797): 費用が大きく、観光と働き口にどう効くかの根拠がない

## 4. 差し戻しと再調査

- 差し戻しはなかった

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m04-bill.md](m04-bill.md)
- 採った m04-1: 政策 RecreationalUse を外す(元 economy-1、議決は要らない)
- 採った m04-2: 東の交差点2か所に信号(元 roads-2、議決は要らない)
- 採った m04-3: z=-1010 の幹線3区間を4車線に(元 roads-1、議決は要らない)
- 採った m04-4: 空き地3に道と送電線(元 roads-3、議決は要らない)
- 採った m04-5: Fire House を工場周りに足す(試し)(元 fire-1、議決は要らない)
- 採った m04-6: 診療所を放棄商店の跡に置く(元 health-1、議決が要る(取り壊し))
- 採った m04-7: 満杯の埋立地2つを建て直す(元 health-2、議決が要る(取り壊し))

- 見たもの:

  - `m04-urban.md` から `m04-finance.md` の8局の案: 案7件(roads 3、economy 1、health 2、fire 1)、案なし4局(urban、port、education、finance)
  - `mayor-note.md`: 4月の数字(人口178,486、所持金2,110,220、週の収支+9,303、観光客1,742、Tourism 58)と、分からないことの一覧
  - `plan-city.md`、`plan-port.md`: 調整1〜16、港の事業を閉じた変更
  - 各局が書いた道具の結果(`test_place_building`、`test_build_line`、`test_upgrade_road`、`preview_bulldoze`、`junction_info`)を引数ごと確認した。市長は街の道具を自分では呼んでいない

- 判断の根拠:

  7件とも実行可否が確認済みで、本文に未確認の必須条件がなかったので、すべて採った。観光の重点には m04-1(政策を外して測りを切り分ける)と m04-4(名所と公園の置き場所を作る)が当たる。島や入口の案は出なかった(港は全11地点で落ち、駅は空きなし)。費用は建設費 41,520、週の維持費の増え約1,335で、守る線に収まる。

- 捨てたもの:

  - 調査 urban と fire: 上限3件のため。重点(8-1、6-4・7-1、働き口の判断)の3件を優先した
  - 港湾空港局、住宅都市みどり局、教育委員会、財政局の施策: 案なし。局の役割から外れた判断ではなく、実行条件が確かめられなかったという理由なので、市長は代案を作らない
  - 分からないことの一覧の試し: SmallBusiness の試し(m02-4)は案が出なかった。m04-1 で RecreationalUse を外し、5月に切り分けて見る。島の橋は案が出なかった

## 6. 議会: 可決と否決(hooks の記録で 14:03〜14:03)

- 元のファイル: [m04-assembly.md](m04-assembly.md)
- m04-1 財政: 可決。費用0で守る線に影響しない。
- m04-2 財政: 可決。建設費0。維持費は小さく守る線に収まる。
- m04-3 財政: 可決。建設費0、維持費の増えは約0。
- m04-4 財政: 可決。建設費11,520、維持費約55で守る線に収まる。
- m04-5 財政: 可決。建設費12,000、維持費560で守る線に収まる。
- m04-6 取り壊し: 可決。放棄商店1棟のみ、働き口0、家0を確認。代わりの手の比べあり。
- m04-7 取り壊し: 可決。埋立地2棟のみ、働き口0、家0を確認。失うごみと代わりの手が書かれている。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `economy`: 税・予算の現状(今月の議案に税・予算なし)
  - `city_info`: 所持金 2,110,220、週の収入 347,484、支出 338,181
  - `preview_bulldoze`: 46949、25692、157 がそれぞれ1棟のみ、働き口0、家0、電気の喪失0

- 判断の根拠:

  費用の合計は建設費 41,520、維持費の増え 1,335 で、案の数字と一致した。打った後も収支 +3,000 と所持金 1,874,000 の線を大きく上回る。取り壊し2件は失うものを自分でも確かめ、問題がなかった。収支は3か月連続で +4,900 を切ってはいない。

- 捨てたもの:

  - m04-6 と m04-7(戻せない手): 失うものが0または数字で書かれ、代わりの手との比べもあるので可決した。

## 7. 実行する市長: 実行と見回り(hooks の記録で 14:03〜14:16)

- 実行してよい施策: m04-1、m04-2、m04-3、m04-4、m04-5、m04-6、m04-7
- 実行した: m04-1、m04-2、m04-3、m04-4、m04-5、m04-6、m04-7
- 失敗した: なし
- 臨時: なし
- 見回り 2050-04-11: 人口 178222、所持金 2081499、週の収支 9123、幸福度 85
- 見回り 2050-04-21: 人口 178395、所持金 2095889、週の収支 10109、幸福度 85
- 報告:

  7件すべて実行した。建設費は計41,520、所持金は2,110,220から月末2,111,160。月末(2050-05-01)の週の収支は+10,614で、守る線の+3,000を上回った。見回りは境目に当たらず、臨時もなし。hooks に止められた手もなかった。取り壊しは preview で働き口0・家0を確認してから行った(放棄商店46949、満杯の埋立地25692と157)。診療所18600、埋立地40097と2224、Fire House 25877はいずれも置けた。m04-4 は、道が既存の道につながり、送電線も既存の送電線につながった。送電線の始点は未接続のまま、`height_at` は未確認。月末の計測は、信号の東で blocked 254→92、観光客1,811、Tourism週24、満杯の埋立地0、ごみの印14。工場12882の火事は残っている。調査 s04-1〜s04-3 は council/m04-survey-*.md に書いた。市政ノート: 2026/10-27-AI市役所で福岡を観光都市にする-03-観光の街を目指す計画と局を決める/mayor-note.md

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m04、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 13:53〜14:26(hooks の記録の時刻から)、道具の行 308
- 議会が可決した種類: 取り壊し
- 議決が要る道具の呼び出し: 3 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 588 件
- hooks の拒否: 0 回

#### 運営のフォルダで、決まりの外の変更(git status)

- `council/m01-port-zonemap-east.jpg`
- `council/m01-roads-zonemap.jpg`
- `council/m01-zonemap-east.jpg`
- `council/m03-zone-a.jpg`
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

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 11)
