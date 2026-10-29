# 3か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 13:40〜13:40)

- 元のファイル: [m03-policy.md](m03-policy.md)
- ゲーム内の日付: 2050-03-02、保存: fukuoka-plan-m03
- 重点: 5-1、5-2 観光、8-1 物流・人流のゲートウェイ、4-3 脱炭素社会、4-4 資源循環

- 見たもの: [m03-policy.md の「見たもの」](m03-policy.md#見たもの)(16 行)
- 判断の根拠:

  観光の3指標(人数、Tourism、入口)のうち、入口が0のままで Tourism が目標の7%にとどまる。市長の方針で5-1、5-2を重点にする。8-1は止まったトラック504が目標の2倍で、交通の流れ50%にも響くため、港湾空港局の入口の案と合わせて重点にした。4-3、4-4は焼却場停止の試しで、汚染とごみがトレードオフと分かったので、別の手を求める。

- 捨てたもの:

  - 2-3 教育、1-2 健康(78→目標80): 定員に余裕があり、目標まであと2。今月は重点にしない
  - 6-1 事務所L3(3,240棟→3,500): 前月から13棟増え、動いている。重点にしない
  - 4-1 地価、4-2 公園: 数字は動かず、観光の名所の案と重なるため、重点の外で案を待つ
  - 3-4 火事と犯罪: 合わせて5で目標4以下まであと1。重点の外の案で足りる
  - 6-3 交通(50%): 8-1 の止まったトラックの手と合わせて見る。単独の重点にしない

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

### 住宅都市みどり局(urban)(hooks の記録で 13:41〜13:43)

- 元のファイル: [m03-urban.md](m03-urban.md)
- 案: なし

- 見たもの: [m03-urban.md の「見たもの」](m03-urban.md#見たもの)(17 行)
- 判断の根拠:

  - 今月の数字: 住宅(高密度)の地価 58(目標 62)、公園 81(目標 100)。どちらも今月は動いていません。公園を増やす手は空き地3の道路待ちで、今月は置く場所がありません。
  - 取り壊しなしの場所を、東の街区、A の周り、(2350, 700) の周りで試しました。どれも既存の建物、水塔、道路と重なりました。取り壊しの案は、計画の「取り壊しなし」と、働き口や家の損失の上限に反するので、出しません。
  - 地価が動かない原因は、確かめていません。A の周りの地価は76と高く、街全体の58との差は、汚染・騒音・公園の不足のどれかの影響かもしれません。原因が分からないので、地価の3つの地図を見る調査を1件出します。
  - 案の数は0件です。試しに出せる手が、確かめた場所では1つもありません。

- 捨てたもの:

  - 東の街区の公園(2510, 375)、(2420, 375)、(2510, 605)、(2300, 600)、(2484, 695): 水塔、既存の店・住宅・事務所と重なる。取り壊しを伴うため、計画の「取り壊しなし」に反する
  - 東の街区の公園(2180, 658)、(2150, 940)、(2150, 985): 道路と小学校、店4軒(働き口44)に重なる。取り壊しを伴うため、今月は出さない
  - 名所の追加: 名所の2棟目以降は経済観光文化局の担当(計画の調整1と14)。局は出さない
  - 政策 HighTechHousing(週20,244): 効き目の記述が確かめられず、週の維持費の枠 6,965 を大きく超える
  - 政策 RecreationalUse、Recycling: 地価と公園への効きを、道具で確かめられない

### 道路下水道局(roads)(hooks の記録で 13:42〜13:43)

- 元のファイル: [m03-roads.md](m03-roads.md)
- 案: なし

- 見たもの: [m03-roads.md の「見たもの」](m03-roads.md#見たもの)(21 行)
- 判断の根拠:

  - 担当の問題は、交通の流れ50%(目標60%)と、電気・水・下水が来ない市民0(目標0を保つ)です。後者は0のまま保たれています。
  - 観光に効く道の手は、今月は実行条件が揃っていません。旅客の駅の場所が未着で、島の橋は第5月の予定です。
  - 6-3 の信号は、交差点のあるところにしか付けられません。(-687,-736) の詰まりは区間の途中なので、信号は効きません。
  - 貨物センター28755の止まったトラックは、敷地の中で空きを待っています。道路の差し替えで直るかは、まだ確かめていません。調査で見ます。
  - 案の数は0です。実行条件が揃う手がないためです。前月の非採択は今月の理由にしていません。

- 捨てたもの:

  - 旅客の駅への道(事業3): 場所が届いていないため、実行条件が未確認。届き次第、第3月の予定として出し直す。
  - 島Bの橋・水道管・風力(事業2、第5月): 第5月の予定どおり。今月は引かない。
  - 島Bの電線を本土から引く案: 2経路とも、水道タンクと海で断られた。島の電気は風力で出す(調整5)ので、試さない。
  - z=-740 に信号を足す案: 交差点がない区間なので、効かないと判断した。
  - 4車線化 z=-1010 の4区間(事業1): 次の確認は第4月(blocked と流れを見てから)。今月は前倒ししない。
  - `HeavyTrafficBan`(トラックの通行禁止、費用0): 交通の流れには効く見込みがあるが、トラックを止めると品物がない店230と工場34が悪くなる(8-1、6-4)。どれだけ悪くなるかは測っていない。今月は出さない。
  - `RecreationalUse`(観光の政策、費用0): 観光に効く記述は一覧にない。観光の効きは、経済観光文化局と財政局の担当。今月は道路の案にしない。

### 港湾空港局(port)(hooks の記録で 13:42〜13:45)

- 元のファイル: [m03-port.md](m03-port.md)
- 案: なし

- 見たもの: [m03-port.md の「見たもの」](m03-port.md#見たもの)(11 行)
- 判断の根拠:

  - 旅客の入口(5-1、5-2)は、目標が 0 から 1 以上。しかし 3 か月の候補(駅 3 か所、港 5 か所)は、どれも設置条件を満たさなかった。勾配、ぶつかり、道の接続のどれかで落ちている。条件が確かめられない案は出さない(局の決まり)。
  - 地形は、線路の側が低く(60〜66m)、道の側が高い(108m以上)。どちらに駅を置いても、もう一方へ勾配で届かない。この地形の制約は、今月の道具で確かめた事実として計画に残す。
  - 貨物の止まり(8-1)は、道の渋滞ではないと分かった。原因は敷地の中の積み残しか、出口の容量と見られるが、確かめていない。施策の案にする前に、調査で台数の動きを見る。
  - 案の数は 0。確認済みの候補がないため、案なしにする。島と空き地は、橋と電気の試しを先に行う必要があり、今月の案の根拠にならない。
  - 調査は 1 件。問いは 1 つに絞り、見回りごとに台数が動くかを見る。

- 捨てたもの:

  - 駅 (3290,-1790) 北向き: 入口は道なしで置けるが、道の接続先が勾配で通らない。道を引けないため出さない。
  - 駅 (3360,-1560) 東向き: 道は要らないが、旅客線が勾配で通らない。線路が引けないため出さない。費用 45,000 の駅を、線が通らないまま置かない。
  - 駅 (3380,-1720) 北向き: 線路 18304 とぶつかる。線路を取り壊す案は、旅客の鉄道を壊すため、取り壊しの議決が要る。今月は出さない。
  - 港 (-700,1080) 東向き、(-560,985) 南向き、(-500,1010) 南向き、(-260,1060) 北向き、(-370,1050) 北向き: ぶつかり、勾配、地面の高さ、道の接続のどれかで落ちている。
  - 島B(能古島の候補)の旅客の入口: 橋と電気の試しが未確認。今月は試しの段階にも入れない。
  - 貨物の道の差し替え(28755 の出入口): 原因が道と決まっていない。道路下水道局の案として扱うため、この局では出さない。

### 経済観光文化局(economy)(hooks の記録で 13:42〜13:43)

- 元のファイル: [m03-economy.md](m03-economy.md)
- 案 economy-1: 政策 RecreationalUse を有効にする(観光の魅力の試し)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 5-1、5-2 観光
  - 議決: 要らない

- 見たもの: [m03-economy.md の「見たもの」](m03-economy.md#見たもの)(10 行)
- 判断の根拠:

  - 観光の3つの数字(観光客1,772、Tourism 週66、名所8棟)は、目標の半分にも届いていない。名所 B 周りの attractiveness は、2月の調査で3回とも8で、基準14に届かなかった。名所の増設を急ぐ根拠が弱い。
  - 建設なしで試せる手として、RecreationalUse を選んだ。費用0、いつでも外せる。効き目は list_policies に書かれていないので、試しにした。
  - 案の数は1件にした。2棟目の名所(A 周りや別の地区)は、測る範囲が政策と重なるため、今月は出さない(調整15)。品物がない店の原因は未確認なので、調査で確かめる。
  - 入口(港湾空港局)の求めは、長期計画の第3月の予定どおり、すでに計画に入っている。今月の案には入れない。
  - 長期計画は、第3月の予定に「政策の試し」を足した。理由は、名所の増設の前提(B 周りの効き)が崩れたこと。計画の変更の欄に書いた。

- 捨てたもの:

  - 名所の2棟目(A 周り、または別の地区): 測る範囲が RecreationalUse と重なる(調整15)。B 周りは3回とも8で、基準14に届かない。空き地3は道がまだなく、第5月の予定どおり。
  - 名所の2棟目を島Bに置く案: 島Bの橋と電気が未確認(第7月の予定)。今月は試せない。
  - 品物がない店への対策(店の周りの道、貨物センター): 原因が未確認なので、今月は案にしない。調査 s03-1 で確かめ、第4月に他局へ求める。
  - 入口の求め: 港湾空港局の担当で、長期計画の第3月に済み。今月の案には入れない。
  - 6-1 事務所レベル3、働き口: 長期計画の見送り。税は既に低く、道に面した空きが少ない。

### 保健環境局(health)(hooks の記録で 13:42〜13:44)

- 元のファイル: [m03-health.md](m03-health.md)
- 案: なし

- 見たもの: [m03-health.md の「見たもの」](m03-health.md#見たもの)(16 行)
- 判断の根拠:

  2267の処理が0のまま満杯なのは、止めたあとの戻しが効いていないのか、再開の途中なのかを、道具の数字だけでは決められない。ごみの印は、2267を運転に戻した後も22のまま。埋立地の追加は、ごみの中心の密な住宅で置けなかった。汚染を減らす手は、工場群の側が最も高く、住宅の汚染は2267の近くにある。2267の状態を見てからでないと、汚染の手を決められない。Recycling は税の損失が守る線を破るため、出さない。診療所は、健康の79未満の判定が4月のため、今月は置かない。案の数は0件。実行条件を確かめた案がないため。

- 捨てたもの:

  - 埋立地を2271,-421の近くに置く案: 試した2か所(2380,-300)、(2200,-560)とも道路と建物にぶつかった。空きが取れるまで出さない
  - 2267を空き地へ移す案: (3420,-420)、(3300,-400)とも風力発電とぶつかった。空きを選び直す必要があり、今月は未確認
  - 政策 Recycling: 税-5%(約13,200/週)で守る線を破る
  - 政策 HeavyTrafficBan: 貨物の車を止め、品物がない店(230)を悪くする
  - 火葬場31990の増設: 火葬場31990は0/週のまま。増やす前に、なぜ0なのか(霊柩車の出方)を確かめる必要がある。死体の印は担当だが、今月の調査は1件のため、次の月に回す

### 教育委員会(education)(hooks の記録で 13:42〜13:43)

- 元のファイル: [m03-education.md](m03-education.md)
- 案: なし

- 見たもの: [m03-education.md の「見たもの」](m03-education.md#見たもの)(26 行)
- 判断の根拠:

  - 担当の数字は、両方とも目標を満たし、余裕は減っていない。条件(余裕が1,000を切る)に達していないので、高校の建設は見送る
  - 前の月の答え合わせ: 2か月目の案はなし。2か月目の予定「前月比で10代と子どもの増え方を記録する」は、上の推移のとおり記録した
  - 計画との関係: 長期計画の第3月の予定(置き場所を試しで探す)どおり。計画は変えない
  - 候補地は、東・中央・西の3地区で試した。取り壊しなしで置けたのは東の (2600, 450) だけで、入口の道路がない。ほかは取り壊しで家か働き口を失うか、道路と重なる
  - 高校を置くのは、余裕が1,000を切ったあと(計画の第7か月以降)。そのときは、置く前に、東の (2600, 450) の道路を試し直し、取り壊しの少ない候補を比べる

- 捨てたもの:

  - 高校を今置く(建設費 24,000、週 560): 余裕が 2,010 あり、条件の 1,000 を切っていない。今置くと、維持費の増えに見合う効果がない
  - 小学校を足す(建設費 10,000、週 160): 余裕が 3,305 あり、目標を満たしている。子どもは減っている
  - 大学を足す(建設費 75,000、週 1,920): 大卒の失業は、働き口が足りないことが原因。定員を足しても失業は減らない。費用が大きい
  - 東の候補(2600, 300)や(2640, 445)に高校を置く案: 取り壊しで家か働き口を失う。今月は置かず、試しの結果だけを残した
  - 政策 EducationBoost の変更: 教育の数字は目標を満たしている。効き目を見積もれない。今月は触らない

### 消防局(fire)(hooks の記録で 13:42〜13:43)

- 元のファイル: [m03-fire.md](m03-fire.md)
- 案: なし

- 見たもの: [m03-fire.md の「見たもの」](m03-fire.md#見たもの)(17 行)
- 判断の根拠:

  - 火事の印は5で、目標の合計4以下より1多い。犯罪の印は0。3-4 の残りは火事だけ。
  - 火事は、覆いが高い (3255,-805) に3棟、工場 (2184,-918) に1棟、西の端に1棟と散っている。(3255,-805) は、1月の4、1月末の7、3月の5と、月をまたいで同じ場所に出ている。
  - 消防署の数が足りないとは言えない。(3255,-805) の近くの消防署は消防車を1/8しか使っていない。覆いが低い所は工場の周りだけで、燃えは1棟。
  - 原因(燃えが続くのか、消防車が着くのに時間がかかるのか、新しい火が出るのか)が、数字だけでは分からない。計画のとおり、月末までの見回りで調べる。
  - 前の月の答え合わせ: 2月の消防局は案なしで、調査も出ていない。1月の警察署(m01-6)の犯罪の印は、1月末に3から2へ、3月に0へ減った(当たり)。

- 捨てたもの:

  - Fire House を (2262,-1190) に置く(計画の候補A): 試しの道具では通るが、火事の多い (3255,-805) には届かず(約1,065m)、工場の周りの燃え1棟に効くだけ。原因が決まるまで置かない。4月に調査の結果で出し直す。
  - (3255,-805) 付近に消防署を足す(候補B): 覆いは231で、足す根拠が弱い。消防車も空いている。調査で、燃えが続き消防車が出払うと分かったら、4月に場所を試す。
  - SmokeDetectors の政策: 有効にすると週の費用が約57,759増え、今の週の収支 +12,912 が赤字になる。守る線を破るため、採らない。
  - 警察署を足す・移す: 犯罪の印が0で、警察の定員(980 に対し使用389)に余裕がある。今は不要。
  - 消防の予算を上げる: 覆いは (3255,-805) で既に高い。議決を使うほどの効き目の根拠がない。

### 財政局(finance)(hooks の記録で 13:42〜13:42)

- 元のファイル: [m03-finance.md](m03-finance.md)
- 案: なし

- 見たもの:

  - `city_info`: 人口 178,639、所持金 2,074,074、週の収支 +12,912(収入 344,486、支出 331,574)、観光客 1,772(訪問 146)、来ない市民 0/0/0、dialog なし
  - `economy`: 税 住低9・住高7・商低9・商高3・工3・事務所3。道路予算 120、ごみ・保健・警察・公園 150、消防 140、教育 120
  - `economy_breakdown`: Tourism 週66(収入)、事務所の収入 24,439、住宅の収入 264,145、政策の費用 11,011、道路の維持費 8,541、融資の週の支出 0
  - `list_policies`: 有効は EducationBoost(週 7,940、教育の支出に入る)、BigBusiness(週 3,908)、SmallBusiness(週 317)。無効で費用が0のものは RecreationalUse、Recycling、HeavyTrafficBan、FreeTransport、PetBan、SmokingBan、税の政策。無効で費用が大きいものは PowerSaving・WaterSaving(各 58,322)、SmokeDetectors(57,759)、HighTechHousing(20,244)、IndustrySpace(4,803)
  - `list_loans`: 融資の枠は3つとも未借入(BankA 20,000 / 5%、BankB 60,000 / 10%、BankC 200,000 / 15%)。融資の支出 0
  - `demand_breakdown`: 働き口 86,566、空き働き口 3,499、空き家 5,041、失業 7,262。大卒の失業 7,082(大卒の働ける人 82,632)、高卒の失業 34、小卒 39、無学歴 107

- 判断の根拠:

  - 前の月の答え合わせ(m02-4、政策 SmallBusiness): 予想は Tourism が42から増える。結果は 42→57→70→66 で増えた。判定は半分。増えたが、観光客(1,747→1,772)も同じ期間に増え、効きの量は分けられない。次の扱い: 続ける。量は見積もれない
  - 週の収支は +12,912 で、守る線(+3,000 以上)に余裕がある。所持金も守る線(1,874,000 以上)を大きく超える
  - 税の動かし方: 商業の税は道路 120 と同じ月に出せない。事務所の税は計画で5月以降と決めた。今月の数字(大卒の失業 7,082、事務所の需要)だけでは、事務所の税が効く根拠が足りない
  - 政策の動かし方: 週の費用0の政策は、Recycling のように住宅の税を減らすものがあり、守る線を割る。費用の大きいものは守る線の余裕 6,965 を超える。残る RecreationalUse は、SmallBusiness の判定と観光の測りが重なるため、今月は出さない
  - 案の数を0にした理由: 計画の3月の予定に新しい手がなく、件数を埋めるための案は作らない。大卒の失業の原因を、調査で確かめてから5月に決める

- 捨てたもの:

  - 事務所の税 3→2: 大卒の働き口への効きは見込みだけ。計画は5月以降。今月は根拠が足りない
  - 商業の税 9→8: 道路の予算 120 と同じ月には出せない(規則)
  - RecreationalUse: 効きは未確認。SmallBusiness の判定と観光の測りが重なる
  - Recycling: 住宅の税の収入が約5%減り(週 約13,000)、守る線を割る
  - HighTechHousing、PowerSaving、WaterSaving、SmokeDetectors: 週の費用が大きく、守る線の余裕を超える
  - HeavyTrafficBan: 物流を悪くするおそれ。8-1 と 6-3 は他局の担当
  - 融資(take_loan): 所持金に余裕があり、借りる理由がない

## 4. 差し戻しと再調査

- 差し戻しはなかった

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m03-bill.md](m03-bill.md)
- 採った m03-1: 政策 RecreationalUse を有効にする(観光の魅力の試し)(元 economy-1、議決は要らない)

- 見たもの:

  - `city_info`(局の案の引用): 人口178,639、所持金2,074,074、週の収支+12,912、観光客1,772(訪問146)
  - 8つの局の案(m03-urban、roads、port、economy、health、education、fire、finance)と編成方針(m03-policy)
  - `list_policies`(economy-1 の引用): RecreationalUse は active=false、costPerWeek=0。政策の費用は週11,011
  - `map_layer`(economy の引用): attractiveness(x=0、z=0、radius=4000、n=9)の平均2
  - 市政ノートの分からないことの一覧(10項目)と、長期計画 plan-city.md の調整1〜16

- 判断の根拠:

  案が1件しかなく、確認済みで費用0の RecreationalUse を採りました。観光客1,772、Tourism 週66、attractiveness 平均2は目標から遠く、市長の方針の観光に当たります。分からないことの一覧の「名所や入口を足すと観光が増えるか」に当たる試しにもなります。守る線への響きはありません。調査は、貨物の止まり(port、economy)と焼却場(health)の3件を採りました。どれも次の月に打つ手の分かれ目を決めます。

- 捨てたもの:

  - 調査 roads(幹線 (-687,-736) の止まった車): 上限3件のため。信号は区間の途中に付けられないと分かっており、急ぎでない
  - 調査 urban(住宅の地価の原因): 上限3件のため。地価は動いておらず、公園の置き場所が空き地3の道待ち
  - 調査 fire(火事の繰り返し): 上限3件のため。火事は5で目標にあと1。4月に再検討
  - 調査 finance(大卒の失業): 上限3件のため。事務所の税の検討は5月以降
  - 港湾空港局の駅・港の候補、住宅都市みどり局の公園、保健環境局の埋立地・焼却場移設: 案として出ていない。実行条件が未確認のため、市長は代案を作らない

## 6. 議会: 可決と否決(hooks の記録で 13:48〜13:48)

- 元のファイル: [m03-assembly.md](m03-assembly.md)
- m03-1 財政: 可決。建設費0、週の維持費の増え0で守る線に響かない。政策の変更は月1件の上限内。
- 可決した種類(hooks が見る): なし

- 見たもの:

  - `city_info`: 2050-03-02、所持金2,074,074、週の収支+12,912、観光客1,772
  - `council/m03-bill.md`: 施策1件、費用0

- 判断の根拠:

  施策は m03-1 の1件で、議決は要らないので点5だけで確かめた。費用が0なので、週の収支も所持金も守る線を割らない。政策の変更は月1件の上限内である。調査3件は施策ではなく、判断の対象にしない。

- 捨てたもの:

  - m03-1: 効き目が量で見積もれないが、費用0で戻せるため、否決の4点のどれにも当たらない。

## 7. 実行する市長: 実行と見回り(hooks の記録で 13:48〜13:54)

- 実行してよい施策: m03-1
- 実行した: m03-1
- 失敗した: なし
- 臨時: なし
- 見回り 2050-03-12: 人口 178450、所持金 2086309、週の収支 8581、幸福度 85
- 見回り 2050-03-22: 人口 178525、所持金 2097125、週の収支 7396、幸福度 85
- 報告:

  m03-1(RecreationalUse 有効化、費用0)を実行しました。実行前に active=false、costPerWeek=0 を確認し、実行後も policyExpenses は 11,012 で変わりません。月末(2050-04-01)は人口178,486、所持金2,110,220、週の収支+9,303、観光客1,742(訪問139)、Tourism 週58、attractiveness 平均2です。attractiveness は4回とも2で動かず、効いた形跡はまだありません。SmallBusiness と重なるため判定は保留で、4月に決めます。見回りは2回とも境目に当たらず、臨時は行っていません。調査3件はまとめて council/m03-survey-port.md、m03-survey-health.md、m03-survey-economy.md に書きました。主な事実は3つです。貨物センター28755の敷地内で止まったトラックは500台前後で、同じ車が70〜90日動いていません。周辺の道は blocked 0 で、渋滞は見えません。焼却場2267の貯蔵は333,750から251,468へ減り、処理は動いています。品物がない店は226から235へ増え、止まったトラックの数とは連動して減っていません。set_time ツールがこの環境になく、一時停止の確認はできませんでした。ただし advance は進めた後に自分で止まり、city_info は paused=true を返しました。command-log.txt は保存済みです。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m03、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 13:39〜14:04(hooks の記録の時刻から)、道具の行 265
- 議会が可決した種類: なし
- 議決が要る道具の呼び出し: 0 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 588 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m03-zone-a.jpg`

#### 運営のフォルダで、決まりの外の変更(git status)

- `council/m01-port-zonemap-east.jpg`
- `council/m01-roads-zonemap.jpg`
- `council/m01-zonemap-east.jpg`
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

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 8)
