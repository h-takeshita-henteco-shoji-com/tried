# 22か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 20:00〜20:00)

- 元のファイル: [m22-policy.md](m22-policy.md)
- ゲーム内の日付: 2051-10-03、保存: fukuoka-plan-m22
- 重点: 5-1・5-2 観光(旅客の入口、島・空き地の名所)、8-1 物流・人流のゲートウェイ、6-3 公共交通を主軸とした交通体系

- 見たもの: [m22-policy.md の「見たもの」](m22-policy.md#見たもの)(15 行)
- 判断の根拠:

  公約4は今月、観光客も Tourism も前月より増えたが、目標との差が大きく、入口0と島・空き地0が22か月続くため、観光は重点に入れる。8-1 は 632 が目標250の2.5倍で、m21-4 が外れたため別の手が要る。6-3 は目標60にあと5で、局所の手が当たり続けているので続ける。3つとも、局の案を比べて選ぶ。

- 捨てたもの:

  - 4-2 公園: あと4で、安い手が続いている。重点にせず、案が出れば比べる
  - 4-3 汚染: 汚染の印は25→32に増えたが、出どころが分からず、木や焼却場停止は効かなかった。重点にしない。調査の案は歓迎
  - 3-4 火事・犯罪: 合わせて7で目標4以下を超えたが、印の場所は散らばっている。案があれば比べる
  - 6-1 事務所、6-4・7-1: 事務所L3 3,281(目標3,500)は税や教育の手が効かなかった。今月は重点にしない

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

### 住宅都市みどり局(urban)(hooks の記録で 20:02〜20:09)

- 元のファイル: [m22-urban.md](m22-urban.md)
- 案 urban-1: 放棄店 6208 の跡(56,22)に公園 JapaneseGarden を1つ置く
  - 建設費 2500、週の維持費 +40、戻せない
  - 市の計画: 4-2
  - 議決: 要る(取り壊し)
- 案 urban-2: x=2200 の幹線沿いに木を植える(試し、4-1)
  - 建設費 400、週の維持費 +0、戻せる
  - 市の計画: 4-1
  - 議決: 要らない

- 見たもの: [m22-urban.md の「見たもの」](m22-urban.md#見たもの)(14 行)
- 判断の根拠:

  - 4-2 は 96 から 100 まで4棟が要る。23・24月に残りを置くため、22月は確かめた1棟を出す。候補は、取り壊しで家や働き口を失わない (56,22) を採った。予備 (1856,253) は働き口5を失うので、案の順番の後にした
  - 4-1 は、残る原因が x=2200 の幹線の騒音と分かった。手は木(試し)。HeavyTrafficBan は品物の届きを悪くするため採らない。木の効きは未確認のため試しにし、実行条件が未確認なので executionReady は false
  - 案の数は2件。4-2 の1棟と、4-1 の試し1件で、手が別々

- 捨てたもの:

  - 放棄店の跡に公園を置く案の、取り壊しで家・働き口を失う候補(2234,-54、2232,-166、-664,-56 など): 失う家・働き口が多く、放棄の候補に空きがあるうちは出さない。予備候補にも入れない
  - 岩や石(Boulder、Rock Area など、費用100、維持費0): Beautification の数は増えるが、花や緑による潤いの施策に当たらない。数だけを増やす手は使わない
  - HeavyTrafficBan(区間の騒音を下げる政策): トラックを止め、品物がない店(227)を増やす
  - 公園を Regular Park(9×8、電気のみ、1,000)に替える案: 空いた道沿いの区画が確かめられず、置けるかが未確認

### 道路下水道局(roads)(hooks の記録で 20:02〜20:05)

- 元のファイル: [m22-roads.md](m22-roads.md)
- 案 roads-1: x=-1640 の残り Basic 6区間を Small 4 Lane にする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 交差点 (2236,-950) に信号を付ける(試し)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m22-roads.md の「見たもの」](m22-roads.md#見たもの)(23 行)
- 判断の根拠:

  - 21月の2か所のうち、信号 (2668,330) は 53→1 で効いた。x=-1640 は 41 で、目標40にあと1。残りの Basic 6区間は、同じ型で `test_upgrade_road` が通るので、案1にした(費用 0、取り壊しなし)
  - 上位の止まり (2302,-946) 51 の Basic 3334 は、9m の Basic 36011 が差し替えを断る。差し替えの案は出せないため、同じ地点の信号を案2にした(試し。費用は道具の記載なしで、0と見込む)
  - 案は2件。車線の残りと信号は別の手で、同じ道の言い換えではない。調査は、x=-920 の止まりの原因が上流か下流かを決める
  - 28755 の道は詰まっていない(blocked 0)。止まりは敷地の中の空き待ちで、道の手は効かない。8-1 は港湾空港局の振り分けの試しに任せる(計画の調整5)

- 捨てたもの:

  - 上位 (2302,-946) の Basic 3334・19196 を Small 4 Lane にする: 9m の Basic 36011 が TooShort とぶつかりで断る。36011 を消すと、西へ抜ける道が切れるため出さない
  - (3099,-471) の Basic 2871 を Small 4 Lane にする: 14m で TooShort、SlopeTooSteep。実行可否が未確認のため出さない
  - (-920,-857) の4車線を Large Road に太くする: 沿道の住宅 10 棟、店 3 棟、事務所 2 棟、計 15 棟の取り壊しで、家と働き口を失う。調査の結果を待つ
  - 3138 の Basic 2074 を Small 4 Lane にする: villa 1 棟の取り壊しが要る。上の 2871 が断られるため、効かない区間を広げるだけになる
  - 政策 HeavyTrafficBan: 費用 0 だが、トラックを道から締め出し、noGoods 227 と 28755 の運びに響く。6-4・8-1 と逆になるため出さない
  - 28755 の道の混み対策: 道の blocked は 0。敷地の中の空き待ちに道路の手は効かないため出さない

### 港湾空港局(port)(hooks の記録で 20:02〜20:09)

- 元のファイル: [m22-port.md](m22-port.md)
- 案 port-1: 車が来ない貨物センター 40031 を止める
  - 建設費 0、週の維持費 +-1440、戻せる
  - 市の計画: 8-1
  - 議決: 要らない
- 案 port-2: 路線28の予算を 200% に戻す
  - 建設費 0、週の維持費 +220、戻せる
  - 市の計画: 6-3
  - 議決: 要る(予算)

- 見たもの: [m22-port.md の「見たもの」](m22-port.md#見たもの)(22 行)
- 判断の根拠:

  - 6-3 の路線28 は、台数 171 で流れは 53 から 55 に上がり、ここまでは効いた。だが乗客は 110 から 53 に減った。第21月の計画が決めた「乗客が減るなら戻す」に当たるため、予算を 200% に戻す(案2)。
  - 8-1 の 40031 は、再開から車が来ないまま。計画の条件を満たしたので止める(案1)。週の維持費 1,440 が減り、週の収支は守る線 +3,000 の上に残る。案1と案2をあわせても、週の収支は約 +5,000 の見込み(案2の増えは粗い見積もり)。
  - 旅客の入口(5-1、5-2)は、今月も置けない。東の列と空き地5は、置く場所は確かめられたが、道路網まで道を通せない(地上の道が350m以内になく、東の列はオフィスに塞がれる)。島Bは坂。整地の見積もりを局の道具で確かめられないため、案にせず、実行する市長に求める(計画の事業1)。
  - 案は2件。8-1 と 6-3 の2つにした。入口は、確かめた道が実行条件を満たさないため、案に含めない。

- 捨てたもの:

  - 旅客の駅を東の列(3300,1900)に置く: 置く位置は確かめた(test_place_building は ok)が、道路網までの経路がオフィスに塞がれ、test_build_line が2本とも断った。道路を取り壊す案は、失う働き口の数を確かめていない。実行条件が未確認のため出さない
  - 旅客の駅を空き地5(4300,2350)に置く: 置く位置は確かめた。350m以内に地上の道がなく、道の経路を引く候補を確かめていない。実行条件が未確認のため出さない
  - 旅客の駅を島B(-4700,1600)に置く: 整地が要り、level_terrain の見積もりは局の道具にない。未確認のため出さない
  - 政策 FreeTransport を有効にする(乗客を増やす): 運賃収入が0になり、収入の損は週約5,000(前の月の測り 5,086)。m16-4 と m17-4 の測りで、乗客の増えは確かめられなかった。出さない
  - 貨物の受け口を足す(40031 の代わりに、近い店の周りに別の貨物駅): 行き先の距離は 3〜6km と見えるが、置く場所と道を確かめていない。s22-1 の結果を見てから考える
  - 路線28 の予算を 160% に下げる: 乗客が減っているときに下げると、乗客の減りが続く。出さない

### 経済観光文化局(economy)(hooks の記録で 20:02〜20:04)

- 元のファイル: [m22-economy.md](m22-economy.md)
- 案: なし

- 見たもの: [m22-economy.md の「見たもの」](m22-economy.md#見たもの)(17 行)
- 判断の根拠:

  - 21月は案なしで、22月は置き場所を探した。試した5地点は道路と既存の建物に重なり、取り壊しなしでは置けなかった。取り壊しの候補は、住宅と働き口を失う。道路に面した空きは、citywide で CommercialHigh の 68 マスだけで、名所の大きさに足りないと見た(名所の大きさは道具の数字で、マスの大きさは確かめていない)
  - 最安の名所 Transport Tower は週960で、調整8の週320上限を超える。上限を超える案は、実行の前に市長が決める
  - 魅力度は、名所の周りに偏って出る(最大295、平均2)。名所を置く場所は、ここで探す。ただし、点の出どころは未確認なので、調査 s22-1 で確かめる
  - 案の数は0。調査は1件(魅力度の高い点の出どころ)。調査は街を変えず、見る道具だけを使う
  - m21-survey-economy.md は無いので、前の月の調査の答え合わせはなし

- 捨てたもの:

  - Transport Tower を (324,222)、(564,-146)、(96,264)、(2500,-546)、(3513,-96) に置く案: 道路の中心線と重なるか、住宅・働き口を失う。試しで断られた。取り壊しの案にすると、住宅と働き口を失う
  - 名所を空き地3、島B に置く案: 水・下水の管がなく、水・下水の見積もりも道路下水道局が出していない。22月は確かめられなかった
  - Observatory、Grand Mall、Colossal Offices など、ほかの未建設の名所: 維持費が週1,000〜1,600で、週320の上限と市の守る線(+3,000)の余裕に合わない
  - 政策 RecreationalUse、SmallBusiness を戻す案: 効きが m02〜m05 で切り分けられず、確かめる手が残っていない。観光の数字の前提を変えられない

### 保健環境局(health)(hooks の記録で 20:02〜20:04)

- 元のファイル: [m22-health.md](m22-health.md)
- 案: なし

- 見たもの: [m22-health.md の「見たもの」](m22-health.md#見たもの)(20 行)
- 判断の根拠:

  汚染の印 32 と、ごみの印 14 の多くは、2267 の周りではなく、2200〜2500、z 430〜530 の帯の周りにある。
  2267 の周りの 255 は3か月動かず、2267 を止めた試し(m16)も効かなかったため、2267 の移しは見送る。
  帯の周りには、ごみ収集車が 45436 と 3565 の近くに集まり、z=560 の道が混んでいる。出どころが収集車の渋滞か、それ以外かは、今の数字では決められない。
  効きの見込みのある施策は、3565 の空けと、東の新しい埋立地に限られる。どちらも今月は実行条件が確かめられないか、運搬が長くなるため採らない。
  そのため、案は出さず、帯の調査を1件出す。

- 捨てたもの:

  - 2267 を移す(事業2の旧案): 帯は 2267 から約1km 離れ、2267 の周りは3か月動かず、移しても汚染の印の大半は残る見込み。調査の結果で、出どころが 2267 だと分かるまで出さない
  - 満杯の埋立地 3565 を空にする(empty_building): 近くの 45436 は84%、遠い 16551 は20%で、運搬が長くなる。m13 で同じ理由で止めた手。収集車の渋滞を増やす恐れがあり、今月は見送る
  - 埋立地を東(3945,-189 付近)に新しく置く: 候補の4か所は、Expensive Plaza と道路に当たって置けない。実行条件が未確認のため、採らない
  - 政策 Recycling(街全体): 住宅税 -5% で約 -13,000/週(m19 の計算)。週の収支 +5,957 が守る線 +3,000 を割るため採らない。地区だけにかける案は、地区の税の額を道具で確かめられないため、今月は出さない
  - 政策 HeavyTrafficBan: 直接の費用は0だが、効果の実測がなく、品物の運搬(NoGoods 227)を悪くする恐れがある。今月は出さない
  - 政策 SmokeDetectors: 週 58,040 で、守る線を大きく超える
  - 23459 の入口の道: 計画の23月に回す。今月は帯の出どころが決まっておらず、道を引いても汚染の印には効かない

### 教育委員会(education)(hooks の記録で 20:02〜20:03)

- 元のファイル: [m22-education.md](m22-education.md)
- 案: なし

- 見たもの: [m22-education.md の「見たもの」](m22-education.md#見たもの)(13 行)
- 判断の根拠:

  - 子どもと10代の定員は、目標(定員が子ども・10代以上)を満たす。小学校は1.46倍、高校は1.34倍で、計画の余剰の線 1.3倍を小学校だけが超える。
  - 小学校の4校目は、候補 28785 と 15022 が南の共同住宅の覆いを0にするため外す。候補 34817 は、住宅の覆いが 2030 と重なるが、0の有無を止めずに確かめられない。計画の「試しを出すときは覆いの0を住宅に出さない見込みが要る」を満たせず、案を出さない。
  - 高校は余裕 6,209 で、計画の置く線 1,000 を超えて余る。置く案はなし。
  - 政策 EducationBoost(週 7,940)は学校の維持費の上乗せで、財政の判断にかかる。局の案にしない。

- 捨てたもの:

  - 小学校 28785 の停止(4校目): 南の共同住宅(-908〜-512, -768〜-596 付近)の覆いが 17〜31 から 0 に落ちる見込み。覆いの0を住宅に出さない条件を満たせない。
  - 小学校 15022 の停止: 21月に再調査で外れた候補。同じ理由で外す。
  - 小学校 34817 の停止(4校目): 東の住宅(3436,122〜227)の覆いが 2030 と重なるが、止めて確かめないと0の有無が分からない。置いてから確かめる案は採択の対象にしない。候補の住宅の位置は確認済み。
  - 小学校 2030 の停止(4校目): 東の縁(4200,-100 付近)は 10 で、住宅は無い。しかし、(3436,122〜227)の住宅は 2030 の覆いに頼るため、0が出る見込みがある。外す。
  - 高校の定員の増設: 余裕 6,209 で、計画の線 1,000 を大きく超える。今月は要らない。
  - 政策 EducationBoost の解除: 学校の定員を見て効きの変化が分からず、財政の判断にかかる。局の案にしない。

### 消防局(fire)(hooks の記録で 20:02〜20:03)

- 元のファイル: [m22-fire.md](m22-fire.md)
- 案: なし

- 見たもの: [m22-fire.md の「見たもの」](m22-fire.md#見たもの)(18 行)
- 判断の根拠:

  - 合計は 7(火事 4、犯罪 3)で、目標 4 以下を超えた。計画の条件(合計 5 以上なら届きを確かめる)に当たり、確かめた。火事の場所の届きは 60〜297 で、足りている。
  - 48237 は 21月と 22月で同じ場所の火事で、焼け跡ではない(abandoned=false、Fire と FatalProblem)。事業2の条件(同じ場所が2か月続く)に当たる。道と届きは足りるので、原因は消防の出動か、焼け跡になる途中かのどちらかと見て、調査で確かめる。
  - 他の火事 3 棟は場所が別々で、焼け跡もない。施策の効きを、4 棟の数では測れない。
  - 犯罪 3 棟は場所が別々で、警察の届きは 50〜100 程度ある。届きでは説明できず、原因は分からない。
  - 案は 0 件。施策の候補は、確かめた条件が満たせないか、効きを測れないため出さない。原因が分からない問題は調査を1件出した。

- 捨てたもの:

  - 焼け跡の取り壊し(48237 ほか 3 棟): 焼け跡になっていない(abandoned=false)。計画の条件(焼け跡が2か月続く)を満たさない。
  - 消防署の追加(2834,1118 付近): 届きは 168〜297 で足りている。出動が足りないかを、23月に確かめてから考える。
  - 政策 SmokeDetectors(街全体): 週 58,040 で、週の収支 +5,957 が守る線 +3,000 を割る。採らない。
  - 政策 SmokeDetectors(地区だけ): 地区の棟数と費用が未確認で、火事4棟の数では効きを測れない。
  - 警察署の追加(犯罪 3 棟): 届きが 50〜100 あり、足りない原因がない。犯罪の原因を調べてから考える。

### 財政局(finance)(hooks の記録で 20:02〜20:02)

- 元のファイル: [m22-finance.md](m22-finance.md)
- 案: なし

- 見たもの: [m22-finance.md の「見たもの」](m22-finance.md#見たもの)(11 行)
- 判断の根拠:

  - 前の月の答え合わせ: 前の月(第21月)は案なし。調査 s21-1 の結果は、転入 9→9→4、空き家 5,900→5,936→5,975、地価 53 のまま。住宅税と地価の差は、この1か月では見えなかった。判定は半分。税の試しを出すには、まだ根拠が足りない。
  - 空きの見方: 道に面した空きの住宅が 0 で、空き家 5,975 は既存の建物の中にある。住宅の土地が足りないことが、転入の少なさの原因とは言えない。転入が少ないのは、家の場所・税・働き口のどれが効くかが、まだ分からない。
  - 財政の余裕: 週の収支は +5,957 で守る線 +3,000 の上にある。名所 640〜720 と旅客の駅 960 を足しても、+3,000 以上に残る見込み(計画の見積もり)。財政局が今、削る・足すを決める理由はない。
  - 観光: 観光の収入は週 105 で、観光客 2,020 に比べて小さい。ただし、効く手は名所と入口(economy と port の案)で、財政局の税・政策では効きが切り分けられなかった。財政局は案を出さない。
  - 案の数: 0 件。調査を 1 件出す。

- 捨てたもの:

  - 医療の予算を 130 から 110 へ(週約 -10,200 の見積もり): 墓地の使用が 65% で、保留の条件(半分以下)を満たさない。墓地の空きが増えて条件が満たされるまで出さない。
  - 住宅税の1地区の減税(区127、TaxLowerResLow): 区127 は人口 2,693 で、1か月では人口や転入の差が測れない。区126 は全市の大半で、街全体の減税になる。まず、区127 の基準を調査で取る。
  - 観光に効くとされる政策(RecreationalUse、SmallBusiness)の再有効化: 観光客と Tourism の動きを切り分けられず、3回の試しで効きが出なかった。外れた手を続けない。
  - 事務所税の変更(3% から 2% など): 第9〜11月に試して戻した。事務所の数(目標 3,500)は 6-1 の担当で、財政局の案にしない。
  - 融資: 未借入で、週の収支と所持金に余裕がある。借りる理由がない。

## 4. 差し戻しと再調査

- 住宅都市みどり局: urban-2(実行可 False)
- 港湾空港局: port-2(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m22-bill.md](m22-bill.md)
- 採った m22-1: 放棄店6208の跡に公園JapaneseGarden(元 urban-1、議決が要る(取り壊し))
- 採った m22-2: x=-1640の残りBasic6区間をSmall 4 Laneに(元 roads-1、議決は要らない)
- 採った m22-3: 3叉路(2236,-950)に信号(試し)(元 roads-2、議決は要らない)
- 採った m22-4: 貨物センター40031を止める(元 port-1、議決は要らない)
- 採らなかった urban-2: 木を植える空きが道具で確かめられておらず、実行計画が未確認。
- 採らなかった port-2: 路線28の乗客は92→29→110→53と揺れ、1期間の値では戻す根拠にならない。維持費の増え約2,400の見積もりも粗い。

- 見たもの:

  - `list_building_types`: 局の案の費用(JapaneseGarden 2,500、週 40。Cargo Center 週 1,440)を、局の記述から引いた
  - `city_info`: 局の記述から、人口 173,537、所持金 2,643,814、週の収支 +5,957、観光客 2,020(各局の「見たもの」と一致)
  - 8局の案 `council/m22-<局>.md`、編成方針 `council/m22-policy.md`、長期計画 `council/plan-city.md`、市政ノート(直近月)を読んだ
  - 街を作る・変える道具と `tool-reference.md` は、局の実行計画の引数を照らすために参照した(局が引数と試しの結果を書いている)

- 判断の根拠:

  重点の 6-3 と 8-1 は、確認済みの手を採った。公園は損失0の場所が確認済みで、取り壊しの議決が要る。4案の費用は建設費 2,500、週の維持費の増え 約 -1,400 で、週の収支は約 +7,360、所持金は約 2,641,300 の見込み。守る線(週の収支 +3,000 以上、所持金 1,874,000 以上)を破らない。port-2 は揺れる1期間の値が根拠のため、条件付きで戻す。観光は、案がなく、調査 s22-1 で場所の手がかりを取る。

- 捨てたもの:

  - port-2(路線28の予算を戻す): 乗客が揺れて1期間で判断できず、維持費 約+2,400 が収支を押し下げる
  - urban-2(木を植える試し): 植える空きが未確認
  - 調査 health・fire・finance: 上限3件。重点の観光、8-1、6-3 を優先した
  - 編成方針で重点にしなかった 4-3 汚染、3-4 火事・犯罪、6-1 事務所: 局の案が出ず、確認済みの手がない

## 6. 議会: 可決と否決(hooks の記録で 20:10〜20:10)

- 元のファイル: [m22-assembly.md](m22-assembly.md)
- m22-1 取り壊し: 可決。壊すのは放棄店1棟で、失う働き口・家は0。維持費 +40 は小さい。
- m22-2 財政: 可決。建設費0、維持費の増え0。守る線を破らない。
- m22-3 財政: 可決。費用0で戻せる。守る線を破らない。
- m22-4 財政: 可決。維持費を週1,440減らす施策で、守る線の対象外。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `preview_bulldoze`: (56,22) r12 で壊すのは 6208 の1棟、jobs 0、homes 0、電気の喪失0
  - `economy`: 税・予算の現状を確認(今月の税・予算の議案はなし)
  - `city_info`: 所持金 2,643,814、週の収支 +5,957
  - `council/m22-bill.md`: 議案と費用

- 判断の根拠:

  議決が要る議案は m22-1 のみ。失うものは0と自分でも確かめた。ほかは費用0か維持費の減りで、守る線(週の収支 +3,000、所持金 1,874,000)を大きく上回る。前月に外れた 40031 は、理由を添えて止める手に変えており、点3にも当たらない。

- 捨てたもの:

  - m22-3(信号の試し): 効きが見積もれないが、費用0で戻せるため可決

## 7. 実行する市長: 実行と見回り(hooks の記録で 20:11〜20:18)

- 実行してよい施策: m22-1、m22-2、m22-3、m22-4
- 実行した: m22-1、m22-2、m22-3、m22-4
- 失敗した: なし
- 臨時: なし
- 見回り 2051-10-13: 人口 173326、所持金 2651614、週の収支 7074、幸福度 87
- 見回り 2051-10-23: 人口 173011、所持金 2661649、週の収支 6904、幸福度 87
- 報告:

  4施策をすべて打てた。m22-1は放棄店6208を壊し、公園48363(JapaneseGarden)を(56,22)に置いた。もう1棟の放棄店24321は、置いたときに壊れた。失った働き口と家は0で、費用は2,500。m22-2はSmall 4 Lane Roadへの差し替えが4区間と2区間で通った(費用0)。m22-3は(2236,-950)の信号を付けた。m22-4は貨物センター40031を、車0を確かめて止めた。月末(2051-11-02)の数字は次のとおり。人口172,759(14か月連続で減少)、所持金2,672,278、週の収支+7,746(守る線+3,000の上)、観光客2,020(訪問179)。電気・水・下水が来ない市民は0。月末の実測では、m22-2のblockedが(-1640,-880 r100)で22→15、(-1640,-1000 r200)で41→30。m22-3の(2302,-946 r150)は75→0だった。調査3件は3回分を、council/m22-survey-economy.md、m22-survey-port.md、m22-survey-roads.mdに書いた。結果の主な点は3つ。魅力度295の点は公園3棟の周りで、3回とも動かなかった。28755の止まりは遠い店にも近い店にも向かい、行き先の遠さだけが原因ではなかった。x=-920の止まりは、月末にだけblocked 15が出た。境目には当たらず、臨時は行っていない。hooksに止められた手はない。ログは command-log.txt に写した。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m22、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 19:59〜20:28(hooks の記録の時刻から)、道具の行 268
- 議会が可決した種類: 取り壊し
- 議決が要る道具の呼び出し: 1 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 610 件
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
- `council/m11-port-map-north.jpg`
- `council/m12-port-zonemap.jpg`
- `council/m13-port-zonemap-cargo.jpg`
- `council/m13-port-zonemap-west.jpg`
- `council/m14-urban-map-east.jpg`
- `council/m15-economy-map-east.jpg`
- `council/m15-economy-map-southwest.jpg`
- `council/m15-zonemap-urban.jpg`
- `council/m16-fire-zone.jpg`
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
