# 24か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 20:41〜20:42)

- 元のファイル: [m24-policy.md](m24-policy.md)
- ゲーム内の日付: 2051-12-02、保存: fukuoka-plan-m24
- 重点: 5-1・5-2 観光、6-3 公共交通を主軸とした交通体系、4-3 脱炭素社会(汚染の印)

- 見たもの: [m24-policy.md の「見たもの」](m24-policy.md#見たもの)(16 行)
- 判断の根拠:

  公約4は、観光客とTourismがともに前月より減り、入口0と島・空き地0が24か月続くため、観光を重点に入れる。6-3 は止まった車が625→994に増え、局所の手が外れたので重点に置く。汚染は20→43で目標から遠のいたため、残りの重点にする。人口は15か月連続で減るが、計画の施策に担当がないため、試しの案で扱う。

- 捨てたもの:

  - 4-2 公園: Beautification 99でほぼ達成(あと1)。重点にせず、案が出れば比べる
  - 8-1 物流: 28755 の止まり613は目標250の倍以上だが、40031 の再開も停止も効かなかった。別の手の案は歓迎するが、今月の重点にはしない
  - 3-4 火事・犯罪: 合わせて6で目標4以下を超えたが、印は散らばる。案があれば比べる
  - 6-1 事務所、6-4・7-1: 事務所L3 3,286(目標3,500)は税や教育の手が効かず、品物がない店は8-1と合わせて見る

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

### 住宅都市みどり局(urban)(hooks の記録で 20:44〜20:46)

- 元のファイル: [m24-urban.md](m24-urban.md)
- 案 urban-1: 放棄建物 30881 の跡に公園 JapaneseGarden を置き、4-2 を100にする
  - 建設費 2620、週の維持費 +41、戻せない
  - 市の計画: 4-2
  - 議決: 要る(取り壊し)

- 見たもの: [m24-urban.md の「見たもの」](m24-urban.md#見たもの)(14 行)
- 判断の根拠:

  - 4-2 の Beautification は、市政ノートの24月の値で 99 で、100 まであと1。案1は、放棄建物 30881 の跡に JapaneseGarden を1棟置き、100 にする。道は入口から既存の交差点へ1本(24m)で、確認した。Regular Park や Playground は、道と重なって置けなかった
  - 4-1 の住宅(高)地価 59 は、目標 62 まで3足りない。23月の木の試しは地価を動かさず、24月で最終月のため、今月の案で 62 に届く手は見つからなかった。事業2は閉じる
  - 案は1件に絞った。4-2 はあと1で、ほかの手(政策、木)は効きが小さいか、守る線を割るため
  - 観光(5-1・5-2)は重点だが、公園は Visitors 11 程度で街全体の観光客を動かさなかった(23月の測り)。今月の観光の案は、economy と port の担当に任せる

- 捨てたもの:

  - 1856,-132 の JapaneseGarden(facing east): 4-2 の効きは案1と同じだが、取り壊す 1110 が働き口 6 を失う。放棄の 30881 で置けるため、予備にとどめた
  - 2168,-166 の JapaneseGarden(facing west): 取り壊す 45283 が働き口 8 を失い、入口に道がない。案1より悪い
  - Regular Park(1,000 / 8)・Regular Playground(1,250 / 24): 安いが、(1856,-132) と (2128,423) で道に重なり、置けない
  - 木を増やす(4-1): 23月の試しで地価は動かず、騒音の効きも3だけ。24月で閉じた
  - HighTechHousing(政策、週 20,244): 4-1 に効く見込みはあるが、週の収支 +6,823 を割るため不採用(守る線 +3,000 を割る)
  - RecreationalUse(政策、0): 観光の効きが見えず、4-1 にも関係しないため見送り

### 道路下水道局(roads)(hooks の記録で 20:44〜20:46)

- 元のファイル: [m24-roads.md](m24-roads.md)
- 案 roads-1: 止まりの2番目 (2082,-840) の4車線を Basic に戻す
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m24-roads.md の「見たもの」](m24-roads.md#見たもの)(20 行)
- 判断の根拠:

  - 6-3 の止まりは、(2082,-840) の4車線化が、24月の測りで 35 から 81 に増えた。計画の「2回の測りで基準より増えたら戻す」に当たるため、案1 は戻すことにした。戻しは test で断られず、費用0で、戻せる。
  - 上位の止まりは、(1670,93) と (1882,-903)。(1670,93) の 109 は、4車線化が高校と車庫に断られるため、今月の候補にならない。(1882,-903) は、26706 など1車線の区間が詰まりの中心に見えるが、上流の溢れかどうかを、戻した後に見る。このため今月は調査にし、25月の判断に回した。
  - 案は1件にした。戻す案と、上位の4車線化は、同じ区間の交通を取り合うため、同じ月に両方打つと結果が読めなくなる。
  - 信号は、(3130,-490) で外れた。信号の追加は今月の手にしない。

- 捨てたもの:

  - (1670,93) の 109 Medium を Large Road にする: ObjectCollision で、高校 1226 と車庫 30483 を壊す必要がある。教育と交通の損失が大きいため採らない。
  - 31882(1880→1957、z -840)を Small 4 Lane にする: test は通る(cost 0)。ただし、7413 が1車線のまま残るため、戻しと組むと詰まりが移る。戻しの結果を見た25月に回す。
  - 政策 HeavyTrafficBan(費用0、無効): 大型車を締め出すと、noGoods 201 の店への配達(6-4)が遅れ、6-4 の目標(120以下)から遠ざかる。採らない。
  - 信号を (3130,-490) の近くに追加: 既に信号があり、24月の測りで効かなかった。採らない。
  - (3092,-477) の上流 Basic 2871 の4車線化: 14m で TooShort、坂が急で SlopeTooSteep(23月の test)。採らない。

### 港湾空港局(port)(hooks の記録で 20:43〜20:46)

- 元のファイル: [m24-port.md](m24-port.md)
- 案: なし

- 見たもの: [m24-port.md の「見たもの」](m24-port.md#見たもの)(16 行)
- 判断の根拠:

  確認した事実は、道と水の経路は試しで通ること、電気の経路は川と既存の線に当たって未確認なこと、8-1 は調査で手を止める条件を満たしたこと。
  電気の経路が未確認なので、入口の駅は実行条件を満たさない。案は出さず、次の月に電気の経路を試す。
  8-1 の手は、止める条件を満たした。目標の扱いは市長が決める。
  6-3 は乗客が目標を超えており、今月は手を足す根拠がない。案の数は0件。

- 捨てたもの:

  - 空き地1 の駅(道と水は通るが、電気の経路が未確認): 配置の条件が残る。電気の経路が通るまで案にしない
  - 旅客の港(Harbor)を岸に置く案: 候補の岸が高すぎ(HeightTooHigh)、置ける場所が確認できない
  - 8-1 の別の手(近い店への道): 調査で 13893 に車が来ないと確かめた。手を止める条件を満たした
  - 路線28 の予算 180%(今月の乗客 101 で、下げる根拠なし)

### 経済観光文化局(economy)(hooks の記録で 20:44〜20:46)

- 元のファイル: [m24-economy.md](m24-economy.md)
- 案: なし

- 見たもの: [m24-economy.md の「見たもの」](m24-economy.md#見たもの)(12 行)
- 判断の根拠:

  - 前の月の答え合わせ(m23-economy-1、峰の公園1棟、試し): 半分。公園 29231 の Visitors は 11 で、予想の 10〜15 に入った。一方、街全体の訪問は 179 のまま、Tourism は 130 から 89 に下がった。公園の効きは1棟の周りに限られ、街全体の観光客は動かなかった。前月の調査ファイル(m23-survey-economy.md)はない。
  - 入口は24月末まで0。計画の期限のため、入口の事業を閉じ、入口なしの計画に切り替えた(調整6)。
  - 名所は、未建設の名所がすべて計画の週320を超えるため、上限を見直した(plan-economy.md の計画の変更)。ただし場所が確かめられていないので、実行はしない。
  - 2棟目の公園は、1棟目の効きが街全体に出ず、候補2か所も置けないため、閉じた。
  - 案の数は0。確かめた候補は、置ける場所も実行条件も残らなかった。

- 捨てたもの:

  - 名所 Transport Tower(60,000 / 週 960)と Grand Mall(85,000 / 週 1,280): 取り壊しなしの空きが道沿いになく、放棄店を壊す前提でも道と建物に重なる。週320の上限も超える。
  - 峰の2棟目の公園: 候補 (1880,305)、(1770,315) が道と重なり置けない。1棟目の効きも街全体には出ていない。
  - SmallBusiness の再試し: m02-4 の結果が分からないまま。今月の Tourism 89 で効きを示す新しい数字がない。

### 保健環境局(health)(hooks の記録で 20:44〜20:48)

- 元のファイル: [m24-health.md](m24-health.md)
- 案: なし

- 見たもの: [m24-health.md の「見たもの」](m24-health.md#見たもの)(11 行)
- 判断の根拠:

  - 死体の印 64 の原因は、東側の火葬場 21324(9/9 使用中)、23747、31990 が霊柩車不足で、死体が待つことにある。増設が効く見込みは高いが、道に面した置き場所が、取り壊しなしで見つからない。取り壊しは議決が要り、住宅の失う量(45世帯)が大きいので、今月は採らない。
  - 汚染の印 43 は、道の混みと関係しないと分かった(23月の調査)。出どころは火力発電所 10351 の近くとみられるが、確かめていない。止める試しは、ごみの印を増やすので、ごみの目標と衝突する。そこで今月は、10351 の近くの帯を測る調査を出し、25月に手を決める。
  - ごみの印 12 は、満杯の埋立地 3565 の位置が分からず、空いた埋立地の置き場所も見つからなかった。今月は手がない。
  - 守る線は、週の収支 +6,823(下限 +3,000)、所持金 2,697,883(下限 1,874,000)で、新しい費用の案は出さなくても守れる。
  - 案の数は0件。実行できる形の案が、確かめた条件を満たさなかったため。

- 捨てたもの:

  - 火葬場を東側に増設(2667,-97): 入口の道が住宅 32274 と 44474 にぶつかる。取り壊しが要り、住宅の失う量を確かめる前に、議決を求めない。
  - 火葬場を (2600,-100) に置く: 住宅2棟(45世帯)の取り壊しが要る。今月は取り壊しの議決を求めない。
  - 汚染の試し(10351 を止める): ごみの処理を止めるため、ごみの印 12 が増え、ごみの目標0と衝突する。
  - 汚染の移設(10351 を relocate): 置き場所が見つかっていない。調査の結果を待つ。
  - Recycling 政策: 税の収入が約13,000/週減り、守る線 +3,000 を割る。前の月の理由のまま。
  - 工場地帯の埋立地(2017,-1136): 道に面した空きを、今月は確かめられなかった。事業2の予定どおり、25月に試す。

### 教育委員会(education)(hooks の記録で 20:44〜20:45)

- 元のファイル: [m24-education.md](m24-education.md)
- 案 education-1: 小学校 24888 を1校止める(4校目、試し)
  - 建設費 0、週の維持費 +-160、戻せる
  - 市の計画: 2-3
  - 議決: 要らない

- 見たもの: [m24-education.md の「見たもの」](m24-education.md#見たもの)(12 行)
- 判断の根拠:

  - 担当の数字: 小学校の定員 13,224 は子ども 9,436 の1.40倍で、1.3倍の線を超えたままです。計画の事業(余剰の小学校を止める)の条件を満たします。高校は 24,360 が 10代 18,277 の1.33倍で、余裕 1,000 を大きく超えるため、高校の案は出しません。
  - 候補地: 計画の 34817 は、西の住宅の覆いが 2〜51 と低く、止めると0が出る見込みが残るため、案にしません。24888 は、住宅の密集する地区の中心で、近くに2325、39350、42823 があり、覆いが重なると見ます。住宅のそばに覆いの0が出ないという見込みが残るため、試しとして出します。
  - 費用: 週 -160(EducationBoost を含めて約 -200)。週の収支 +6,823 と守る線 +3,000 に影響しません。
  - 案の数を1件にした理由: 担当の数字で動かせる手は、小学校を止めることだけです。高校、大学、EducationBoost は、担当の目標か数字に効かないため、案にしません。

- 捨てたもの:

  - 小学校 34817(3605,-342): 西の住宅の覆いが、止めた後に0になる見込みが残る。止めて確かめる以外に分からないため、今月は出しません。
  - 小学校 15022、28785: 22月に、住宅の覆いが0になる見込みで外した(計画どおり)。
  - 小学校をもう1校(25月以降の5校目の候補): 今月は1校ずつ試す計画のため、24888 の結果を見てから考えます。
  - 高校を1校置く: 余裕 6,083(133%)で、余裕 1,000 を切っていません。計画の条件に合わないため出しません。
  - 大学を置く: 担当の目標(小学校と高校の定員)に入らず、75,000 の建設費と週 1,920 の維持費が必要です。市の計画の目標にも当たらないため出しません。大卒の失業は 6-4 や 7-1 の範囲です。
  - 政策 EducationBoost を外す(週 7,940): 担当の数字(定員と子どもの数)に効かず、維持費の判断は財政の範囲です。担当の案にしません。

### 消防局(fire)(hooks の記録で 20:44〜20:47)

- 元のファイル: [m24-fire.md](m24-fire.md)
- 案: なし

- 見たもの: [m24-fire.md の「見たもの」](m24-fire.md#見たもの)(27 行)
- 判断の根拠:

  - 火事の印(2)は、48237 の出動が 0/8 のままで、道も届きも問題がない。前月の調査(s23-3)と同じく、出動の判定が原因かどうかは分からない。よって、消防署の追加も、焼け跡の取り壊しも、今月は案にしない。48237 が焼け跡の絞り込みに入ったのは今月が初めてなので、取り壊しは25月に2か月目を見て決める。
  - 犯罪の印(4)は、埋立地の付近で警察の届きが 0〜25 と低い。しかし、9か所の候補地は発電所と送電線で塞がれ、道具で置ける場所を確かめられなかった。実行条件が残るため、案にできない。
  - 調査 s24-2 は、道の原因を外したうえで、26833 が別の火事に出るかを見る。前月と違う問いなので、結果を読んでから次を決められる。
  - 24月は任期の最後の月のため、次の月の結果を読めるかは未確認。調査の結果は、市長が残すかを決める。
  - 市の地形(`city-map.md`)は読んだ。図(`city-map.png`)は読まなかった。この局の問題に必要な範囲は `map_layer` と `zone_map` で確かめたため。
  - 政策は、一覧で火事と犯罪に効く政策を確かめた。SmokeDetectors は週58,015で、守る線を大きく割るため、見送る。
  - 前の月の答え合わせ: 23月は案なし。23月の調査 s23-3 の結果は、26833 が 0/8 のまま3回の見回りで動かず、48237 は燃え続けた。今月の調査は、その結果の続きとして、判定か道かを分ける。

- 捨てたもの:

  - 消防署の追加(Fire House を 48237 の近くに置く): 出動が 0/8 で、消防署の数が足りない前提が外れている。道具の効きも見えない。
  - 48237 の取り壊し(`preview_bulldoze` 済み、失う働き口7、家0): 焼け跡の絞り込みに入ったのは今月が初めてで、2か月の条件に届かない。取り壊しは戻せないため、今月は出さない。
  - 警察署を埋立地の付近に置く案(3-4 の犯罪): 9か所の候補地が、発電所と送電線で塞がれ、置けない。確かめられない場所は案にしない。別の地区を次の月に試す。
  - SmokeDetectors の政策: 週58,015の維持費で、守る線 +3,000 を大きく割る。

### 財政局(finance)(hooks の記録で 20:44〜20:46)

- 元のファイル: [m24-finance.md](m24-finance.md)
- 案 finance-1: 政策 HeavyTrafficBan を試す(汚染の印、4-3)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 4-3
  - 議決: 要らない

- 見たもの: [m24-finance.md の「見たもの」](m24-finance.md#見たもの)(15 行)
- 判断の根拠:

  - 重点3(4-3 汚染の印 43)に、財政の手の中で効きうるものは政策だけ。HeavyTrafficBan は維持費0で、守る線(週の収支 +3,000)を脅かさない。効きは分からないので試しにした
  - 重点1(観光)は、財政の手で効く候補がない。商業税は商業の需要が 2 のため効かない。観光の政策(SmallBusiness、RecreationalUse)は 02 と 03 の月に入れ、05 と 04 の月に外している。同じ手は外れた手として出さない
  - 重点2(6-3 交通)は、道路の予算 120→150 が候補だが、週 約 -2,200(見積もり。道路の維持費 8,920 の比)。守る線を、計画の駅と名所の費用と合わせると割る。効きも未確認なので出さない
  - 税の試し(区127 の住宅税)は出さない。23月の調査の結果ファイルが見つからず、基準を読めない。区127 は人口 2,734 で、1か月の測りで変化が出るか分からない。街全体の住宅税の減税は週 約 2万(見積もり)で、守る線を割る
  - 案の数は1件。費用0の試し1つに絞る。政策の変更は月1件の上限があるため

- 捨てたもの:

  - 区127 の住宅税の試し: 23月の調査の結果が見つからず、税の試しの根拠がない。1か月で効果を測れる人口の動きが小さい
  - 街全体の住宅税の減税: 週 約 -2万(見積もり)で、週の収支が +6,823 から負になる
  - 商業税の引き下げ(観光の収入): 商業の需要 2 で、税を下げても商業は増えにくい。Tourism の週の収入は 89 で、効きの見込みが小さい
  - 政策 RecreationalUse / SmallBusiness の再採用: 02 と 03 の月に入れ、04 と 05 の月に外した。外した理由の数字が台帳にないため、同じ手は出さない
  - 道路の予算 120→150(6-3): 週 約 -2,200(見積もり)。効きが未確認で、守る線の余裕を割る
  - 医療の予算 130→110: 墓地の使用が 65.6%(15,744 / 24,000)で、計画の条件(半分以下)に届かない
  - 融資: 所持金 2,697,883 のため、借りる理由がない

## 4. 差し戻しと再調査

- 差し戻しはなかった

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m24-bill.md](m24-bill.md)
- 採った m24-1: 放棄店30881の跡にJapaneseGarden(元 urban-1、議決が要る(取り壊し))
- 採った m24-2: (2082,-840)の4車線をBasicに戻す(元 roads-1、議決は要らない)
- 採った m24-3: 小学校24888を止める(試し)(元 education-1、議決は要らない)
- 採らなかった finance-1: 23月の調査で汚染は道の混みと無関係と分かっており、物流の目標(6-4、8-1)を悪くし、m24-2の測りとも重なる

- 見たもの:

  - `city_info`(局の案の引用): 人口172,273、所持金2,697,883、週の収支+6,823、観光客2,011
  - `list_policies`(局の案の引用): HeavyTrafficBan は費用 0、無効
  - `traffic`(局の案の引用): (2082,-840) r200 blocked 81、街全体 flow 52
  - `services`(局の案の引用): 小学校の定員 13,224
  - `citizens_summary`(局の案の引用): 子ども 9,436
  - `buildings_near`(局の案の引用): 30881 の取り壊しと入口の確認、24888 は困りごと None

- 判断の根拠:

  確認済みの実行計画がある案は urban-1、roads-1、education-1。この3件は、費用が小さく、測る場所が重ならない。週の収支は +6,823 から約 +7,000 になる見込みで、所持金も守る線の上に残る。finance-1 は、23月の調査と食い違い、物流の目標を悪くする恐れと、roads-1 の測りに重なる点で採らない。観光(5-1・5-2)は、port が電気の経路が通らず案なし、economy が名所の置き場所なしで案なしだった。どちらも実行条件が確認できないためで、市長は代案を作らない。分からないことの観光の項目に、試しの案は出なかった。

- 捨てたもの:

  - finance-1(HeavyTrafficBan): 上のとおり。不可
  - 観光の入口と名所の案: port と economy が案を出さなかった。実行条件が確認できていない
  - 編成方針で重点にしなかった 8-1、3-4: 該当する確認済みの案が出ていない

## 6. 議会: 可決と否決(hooks の記録で 20:50〜20:50)

- 元のファイル: [m24-assembly.md](m24-assembly.md)
- m24-1 取り壊し: 可決。失うのは放棄店1棟で働き口0・家0。preview_bulldozeで確認。代わりの手より損失が小さい。
- m24-2 財政: 可決。建設費0、維持費の増え0。守る線に影響しない。
- m24-3 財政: 可決。維持費が約-160で減る。守る線は守れる。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `city_info`: 週の収支 +6,823、所持金 2,697,883
  - `preview_bulldoze`: 30881 のみ、jobs 0、homes 0、電気の影響 0
  - `council/m24-bill.md`: 議案の費用と操作

- 判断の根拠:

  3件とも費用が小さく、所持金も収支も守る線から遠い。取り壊しは失うものが数字で書かれ、自分でも 0 と確かめた。前の月に外れた施策の継続や、市の計画に逆らう点は見当たらない。

- 捨てたもの:

  - m24-1(戻せない取り壊し): 失うものが 0 で、代わりの手より損失が小さいため可決。

## 7. 実行する市長: 実行と見回り(hooks の記録で 20:50〜20:57)

- 実行してよい施策: m24-1、m24-2、m24-3
- 実行した: m24-2、m24-3
- 失敗した: m24-1
- 臨時: なし
- 見回り 2051-12-12: 人口 172098、所持金 2704477、週の収支 5809、幸福度 86
- 見回り 2051-12-22: 人口 171969、所持金 2711802、週の収支 5160、幸福度 86
- 報告:

  m24-2 は成功。(2082,-840) の4車線を Basic に戻し、費用は0。m24-3 は成功。小学校24888を停止し、月末の定員は12,876。覆いが0になった点はなかった。m24-1 は公園だけ設置し、接続の道路は重なりで引けず部分実行。Beautification は100で、目標に届いた。2052-01-01 の月末は人口171,949、所持金2,717,838、週の収支+4,298。収支は黒字だが、+4,900を下回った。観光客は2,048、Tourism は週93。(2082,-840)r200の blocked は戻す前81、月末85で、止まりが (2134,-908) に移った。臨時はなし、境目なし、ダイアログなし。調査 s24-1〜3 は council/m24-survey-*.md に3回分を記録した。市政ノートとコマンドログは更新済み。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m24、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 20:40〜21:07(hooks の記録の時刻から)、道具の行 323
- 議会が可決した種類: 取り壊し
- 議決が要る道具の呼び出し: 1 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 612 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m24-fire-map-police.jpg`

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
- `council/m23-zone-east.jpg`
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
