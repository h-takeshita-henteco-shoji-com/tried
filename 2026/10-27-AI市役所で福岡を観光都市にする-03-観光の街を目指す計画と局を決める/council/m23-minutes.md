# 23か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 20:19〜20:20)

- 元のファイル: [m23-policy.md](m23-policy.md)
- ゲーム内の日付: 2051-11-02、保存: fukuoka-plan-m23
- 重点: 5-1・5-2 観光、8-1 物流・人流のゲートウェイ、6-3 公共交通を主軸とした交通体系

- 見たもの: [m23-policy.md の「見たもの」](m23-policy.md#見たもの)(16 行)
- 判断の根拠:

  公約4は、観光客が前月と同数で、入口0と島・空き地0が23か月続くため、観光は重点に入れる。8-1 は 635 が目標250の2.5倍で、40031 の再開も停止も効かなかったため、別の手を求める。6-3 は流れが55→52%に下がり、局所の手が当たっているので続ける。人口は14か月連続で減るが、計画の施策に直接の担当がないため、試しの案(財政局など)で扱う。

- 捨てたもの:

  - 4-2 公園: あと3で、安い手が続いている。重点にせず、案が出れば比べる
  - 4-3 汚染: 32→20に減ったが原因は分からず、木や焼却場停止は効かなかった。重点にしない。調査の案は歓迎
  - 3-4 火事・犯罪: 合わせて6で目標4以下を超えたが、印の場所は散らばっている。案があれば比べる
  - 6-1 事務所、6-4・7-1: 事務所L3 3,281(目標3,500)は税や教育の手が効かず、変わらない。品物がない店は8-1と合わせて見る

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

### 住宅都市みどり局(urban)(hooks の記録で 20:21〜20:31)

- 元のファイル: [m23-urban.md](m23-urban.md)
- 案 urban-1: 放棄店 10258 の跡(1856,-46)に公園 JapaneseGarden を1つ置く
  - 建設費 2500、週の維持費 +40、戻せない
  - 市の計画: 4-2
  - 議決: 要る(取り壊し)
- 案 urban-2: 空き2か所に木を植える(試し、4-1)
  - 建設費 50、週の維持費 +0、戻せない
  - 市の計画: 4-1
  - 議決: 要らない

- 見たもの: [m23-urban.md の「見たもの」](m23-urban.md#見たもの)(23 行)
- 判断の根拠:

  4-2 は、22月の公園で 96 → 97 になった。目標 100 まで3つ残る。23月に1つ置くのが、24月末の目標に届く計画(事業1)と合う。配置候補は、道具で確かめた中で、10258 の跡(1856,-46)だけが働き口・家を失わず、入口の道に面して置けた。案1 はこの候補で、取り壊しの議決を要する。
  4-1 は、住宅(高密度)の地価が 59 のまま(目標 62)。原因は、x=2200 の幹線の騒音(86〜92)と、22月の調査で分かっていた。木の試し(案2)は、22月に不採用になったのと同じ理由(場所が未確認)のままで、今月も実行可にできない。ただ事業2の手として計画に残し、場所を道具で確かめられるまで「未確認」と書いて出す。市長が採らなければ、場所を探し直す。
  案の数は2件。4-2 と 4-1 は同じ手ではないため別の案にした。ほかの手(政策、税)は、担当の数字に直接効く政策が一覧にないため出さない。

- 捨てたもの:

  - 1856,-132 の跡(案1の予備): 取り壊しで働き口を6失う。取り壊しを1回増やすことになるので、今月の案の中では使わない。24月の候補に回す
  - 2224,-54・2228,102・2176,126・2224,-190・2432,256・2172,584(公園の候補): 道路か建物に重なり、置けなかった。空きの道を先に引く案は、今月は出さない
  - 2168,-692・2168,-612・1856,-508・2692,435・1856,273(公園の候補): 取り壊しで働き口を6〜30失う。今月は、無損失の 10258 の跡を優先する
  - Boulder などの装飾(100、維持費0): 公園ではなく、4-2 の数を埋めるための手になる。市の計画の「花や緑による潤い」に当たらないため出さない
  - Regular Park(1,000、維持費8、9x8): 安くて維持費も小さいが、10258 の跡(4x4)に入らない。空きの広い場所が確かめられるまで保留
  - 政策による地価の手: list_policies に、地価に直接かける政策が見当たらなかった。出さない

### 道路下水道局(roads)(hooks の記録で 20:21〜20:23)

- 元のファイル: [m23-roads.md](m23-roads.md)
- 案 roads-1: 止まりの2番目 (2082,-840) の Basic 3組を Small 4 Lane にする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 止まりの1番目 (3092,-477) の上流、交差点 (3130,-490) に信号を付ける(試し)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m23-roads.md の「見たもの」](m23-roads.md#見たもの)(28 行)
- 判断の根拠:

  - 6-3 の交通の流れは 52% で、目標 60% から遠い。22月の2件は当たり。x=-1640 は 41 から 30 になり、(2302,-946) の信号は 51 から 0 になった。局所の手は当たり続けているので、続ける。
  - 止まりの上位 (3092,-477) 44 は、差し替えの道具が断る。14m の stub(2871、16182)は TooShort と急な坂で、2074 は villa 1182 の取り壊しが要る。取り壊しは議決が要るうえ、残る14m の区間が詰まりを残す。そこで今月は、差し替えが通る2番目 (2082,-840) を案1にする。
  - 案2は、(3092,-477) の上流の交差点に信号を付ける試しにした。効き目は分からないので、試しとして 56 と 44 を基準に測る。
  - 2件にしたのは、1か所の予定を2件に直したため。理由は、(3092,-477) の差し替えが断られ、次の手を今月の試しで測るため。24月末で、どちらかが外れたら戻す。
  - 案の数は2件。観光(5-1・5-2)の入口は駅が無いので、事業3は進められない。案は出さない。

- 捨てたもの:

  - 3092,-477 の差し替えと、2871・2074 を壊す案: 2871 と 16182 は 14m で、差し替えが TooShort と SlopeTooSteep で断られる。2074 の差し替えは villa 1182 の取り壊しが要り、2871 が残るので流れは変わらない。新しい道を (3130,-490) から (3145,-390) へ通す案は、`test_build_line` で建物3棟(30792、12592、17931。17931 は3戸)と villa 1182 にぶつかり、取り壊しの議決と住宅の損失が要る。今月は採らない。
  - HeavyTrafficBan(政策、0): トラックの通行を止める。費用は0だが、8-1 の止まり(635)と 6-4 の品物がない店(215)を悪くするおそれがある。市の計画の7-1・6-4 と合わせて見直す。
  - (1083,95) の差し替え(止まり28、Medium と Basic の区間): 同じ月に3か所目になり、1か所の予定を超える。24月に、案1の測りを見てから決める。
  - 事業3(旅客の入口の道と電線): 駅が無いので、引けない。第24月末の駅の判定まで待つ。

### 港湾空港局(port)(hooks の記録で 20:21〜20:25)

- 元のファイル: [m23-port.md](m23-port.md)
- 案 port-1: 路線28の予算を 200% に戻す(試し)
  - 建設費 0、週の維持費 +250、戻せる
  - 市の計画: 6-3
  - 議決: 要る(予算)

- 見たもの: [m23-port.md の「見たもの」](m23-port.md#見たもの)(28 行)
- 判断の根拠:

  - 6-3 の路線28: 2期続けて乗客が92未満(前期 73、今期 85)で、22月の条件を満たした。乗客が台数に効くかは期の振れで切り分けられていないが、計画の条件どおりに案1を出す。費用は約 +220〜270 で、週の収支 +7,746 と守る線 +3,000 の内に収まる
  - 5-1、5-2 の入口: 島B は道の坂が急で断られ(SlopeTooSteep、3 区間)、空き地5 は駅を置けるが一般道がない。中心部は空きがなく、取り壊しの案は失うものを未確認。計画の条件(第23月末までに置ける候補と道の経路)を満たせないので、事業1 を閉じる。案は出さない
  - 8-1 の 28755: 止まった車の行き先は 436〜6,014m で散らばり、距離も店への集中も原因ではない。止まりは庫内の空き待ち(629)。隣の 13893 は職員 43 で道にもつながるが車が来ない理由は分からない。原因が切り分けられないので、調査 1 件で見る。施策は出さない
  - 案の数: 1件。入口は道の経路が見つからず、8-1 は調査で切り分け中。ほかの手(FreeTransport、HeavyTrafficBan、低乗客路線の削減)は、根拠が弱いか逆効果になるため出さない

- 捨てたもの:

  - 旅客の駅(島B、(-4780,1560) と (-4740,1680)): 置けるが、道の経路が SlopeTooSteep。道の高さを平らにする道具がない。入口を1つにする条件を満たせないため、今月は案にしない
  - 旅客の駅(空き地5、(4300,2350)): 置けるが、一般道が 900m 以内に見えない。高架の高速道路へ出る接続は未確認。道の経路を見つけるまで、案にしない
  - 旅客の駅(中心部の空き): 道路 2〜8 本と店・事務所の取り壊しが要る。失う働き口と家を `preview_bulldoze` で確かめていないため、案にしない
  - FreeTransport(政策): 運賃収入 5,053/週 を失う。17月に効かず外した経緯があるため、再提出しない
  - HeavyTrafficBan(政策): 貨物トラックを締め出すおそれがあり、8-1 に逆効果。案にしない
  - 低乗客路線の台数の削減(Bus Line 74、9、81): 台数 -12 程度、週 -170 程度。流れ 52% に効く根拠が見つからず、6-3 への効きが見積もれない。今月は出さない
  - 40031 の再開: 22月に止めた後も 28755 の止まりは動かず、再開の根拠がない。出さない

### 経済観光文化局(economy)(hooks の記録で 20:21〜20:24)

- 元のファイル: [m23-economy.md](m23-economy.md)
- 案 economy-1: 峰の近くに公園を1棟置く(試し、(1862,360))
  - 建設費 2500、週の維持費 +40、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m23-economy.md の「見たもの」](m23-economy.md#見たもの)(10 行)
- 判断の根拠:

  - 担当の問題は、観光(5-1・5-2)の訪問の平均 179 と Tourism 週 130 が、目標 250 と 1,000 から遠いこと。名所は週320の上限と空きで置けず、入口は0のまま。
  - 調査 s22-1 の結果で、魅力度の峰は店の周りではなく、公園の周りにある。そのため、公園を峰の近くに1棟置く試しを選んだ。費用は建設 2,500、週 40 で、週の収支 +7,746 と守る線の中に収まる。
  - 場所は、`test_place_building` と `map_layer` の電気・水で確かめた (1862,360) を選んだ。既存の道路に入口がつき、道路や管の新設が要らない。
  - 案の数は1件。ほかの候補(商業の税、店の品物、政策)は、当月の確かめた事実で効く見込みが薄い(下の捨てたもの)。件数を埋めるための案は作らなかった。

- 捨てたもの:

  - 名所(Monument)の再開: 未建設の最安は Transport Tower(建設費 60,000、週 960)で、週320の上限を超える。置ける空きも22月の5地点で見つからなかった。閉じたまま
  - 放棄された店 34259 の取り壊しと跡の再利用: 取り壊しは議決が要り、跡は商業の需要 2 では店が建つ見込みが薄い。放棄地の公園は urban の 4-2 の手と重なる
  - 商業(低)の税を下げて店を増やす: 商業の需要は 2 で、店が増えても品物がない店 215 が残るため、観光の収入に効く見込みが薄い。税は finance の担当で、過去にも不採用(m01-finance-3)
  - 政策 SmallBusiness(週 319): 試しの結果で Tourism が揺れ、因果が切り分けられない(市政ノート)。同じ試しを繰り返さない
  - 政策 RecreationalUse(0): 4回の試しで attractiveness の平均が 2 から動かなかった。効かない見立て
  - 旅客の入口: 港湾空港局の担当。経済観光文化局は「求めること」として計画に書いた
  - 峰の西側 (1790,300) の公園: 道路と既存の公園に重なり、置けない

### 保健環境局(health)(hooks の記録で 20:22〜20:24)

- 元のファイル: [m23-health.md](m23-health.md)
- 案: なし

- 見たもの: [m23-health.md の「見たもの」](m23-health.md#見たもの)(25 行)
- 判断の根拠:

  - 汚染の印 20 は、目標15以下に5減らす必要があります。原因は分かっていません。前の月の22月の調査は出ていないため、帯の出どころは、今月の調査で確かめます。
  - ごみの印 14 は、工場地帯の4棟が中心です。道と埋立地の置き場所を試しましたが、23459 は入口が取れず、ほかの空きも道具で確かめられません。案にできる手がありません。
  - 政策 Recycling は、ごみを15%減らす効きがあります。費用は0ですが、住宅税の収入(259,980 /週)の5%減で、約13,000 /週の減りです。週の収支 +7,746 から、守る線 +3,000 を割るため、使えません。
  - 政策 HeavyTrafficBan は、トラックを締め出す手です。貨物(8-1)とごみの車にも効くため、ほかの局の数字と衝突します。試しとしても出しません。
  - 案の数は0件です。調査は1件、汚染の出どころを見るためです。

- 捨てたもの:

  - 埋立地 23459 の入口の道(長期計画の23月): 道具で断られ、入口の北側は道が引けません。移す案は、道に面した空きが見つからないため、出しません。
  - 埋立地を (2290,-1275) に置く: 道路と貨物センター 3940 にぶつかります(`test_place_building` で断られた)。
  - 政策 Recycling: 住宅税の減り約13,000 /週で守る線を割ります。
  - 政策 HeavyTrafficBan: 貨物とごみの車を止める手で、8-1 とごみの回収に逆に働くおそれがあります。効きは未確認です。
  - 名所の周りの木(m22-urban-2 系): 汚染への効きは01月の試しで見えませんでした(m01-5)。木の案は、木を植える空きも未確認のため出しません。
  - 焼却場 2267・10351 の停止: 2回の試しで効きませんでした(m16-3、m10-2)。
  - 3565 の空け: 近くの埋立地 45436 は84%で、受け入れの余裕が小さい。空けると、ほかの埋立地へ運ぶ距離が延びます。今月は見送ります。

### 教育委員会(education)(hooks の記録で 20:21〜20:23)

- 元のファイル: [m23-education.md](m23-education.md)
- 案: なし

- 見たもの: [m23-education.md の「見たもの」](m23-education.md#見たもの)(13 行)
- 判断の根拠:

  前の月の答え合わせ: 22月は案なし。21月の education-1(4校目 15022)は、再調査でも採られず、覆いの0を止めずに確かめられなかった。20月は案なし(判定は当たり)。19月の 25802 の停止は、窓の最小3で0が出ず当たり。
  今月の判断: 子どもの数は 9,077 から 9,169 に増えたが、定員は変わらず、比率は 1.46 から 1.44 にわずかに下がった。計画の前提(余りが1.3倍を超える)は変わっていない。計画の変更はない。
  案なしの理由: 候補の 34817 を止めると、東の住宅の覆いが 4〜16 の場所は 0 に落ちる見込みがある。0 が出るかは止めるまで分からない。0 の出ない根拠がないまま試しは出さない。15841 は周りの覆いが広く、止めると影響が大きい。高校は余裕が十分ある。
  節約は 1校あたり週 -160 で、週の収支(+7,746)に対して小さい。0 の出る危険のほうが大きいと判断した。

- 捨てたもの:

  - 34817(小学校)を止める: 1校で週 -160。東の住宅の覆いが 4〜16 の場所があるため、止めると0が出る見込みがある。0 が出ない根拠を出せないので、今月は出さない。覆いの変化が見えるまで、見直す
  - 15841(小学校)を止める: 周りの住宅の覆いが 33〜141 で、ほぼ全部がこの学校に頼るため、広く0が出る見込み。取り下げ
  - 高校を1校置く: 余裕 6,175(1.34倍)で、計画の置く条件(余裕 1,000 を切る)に届かない
  - EducationBoost を外す(週 7,940 の節約): 学校の維持費に乗る政策だが、大卒の働き口と失業に効く政策で、finance 局の判断の範囲。教育の担当の数字(定員)には効かないため、案にしない

### 消防局(fire)(hooks の記録で 20:21〜20:22)

- 元のファイル: [m23-fire.md](m23-fire.md)
- 案: なし

- 見たもの: [m23-fire.md の「見たもの」](m23-fire.md#見たもの)(16 行)
- 判断の根拠:

  - 3-4 の合計は 6(火事 2、犯罪 4)で、目標 4 以下を超えている。23月は、計画の分岐「出動が足りない」を確かめた。出動は 0/8 で、足りないとはいえない。前提が外れたため、長期計画を直し(計画の変更の 2051-11-02)、消防署の追加を見送った。
  - 48237 の火事は、届き・道路・予算のどれでも説明できない。原因は出動の記録が見えないことにあるとみて、調査で確かめる。
  - 22月の答え合わせ: 22月の調査の結果ファイル `council/m22-survey-fire.md` は見つからなかった。ただ、22月の問い「48237 は燃え続けるか」は、23月の確かめで「燃え続けた」と分かった。判定は、その範囲で「当たり(燃え続ける側)」。ほかの見回りの値は確かめられない。
  - 犯罪の印 4 棟は場所が別々で、警察の届きは 54〜198 ある。届きでは説明できず、警察署の追加は効きを測れない。
  - SmokeDetectors(街全体)は週 58,107 で、週の収支 +7,746 から +3,000 の線を割る。採らない。
  - 案は0件。有効に見込める手が確かめられず、原因を調べる調査を1件出した。

- 捨てたもの:

  - 消防署の追加(2834,1118 付近): 届きは 168〜297 で足りている。出動は 0/8 で、車が余っている。増やしても効く根拠がない。
  - 焼け跡の取り壊し(48237): abandoned=false で、焼け跡になっていない。計画の条件(焼け跡が2か月続く)を満たさない。
  - 政策 SmokeDetectors(街全体): 週 58,107 で、守る線を割る。採らない。
  - 政策 SmokeDetectors(地区だけ): 地区の棟数と費用が未確認。火事の印は 2 棟で、効きを測れない。
  - 警察署の追加(2185,157 付近、12,000、維持 480/週): 届きは約 85 あり、犯罪の印は場所が散らばっている。効きを測れないため、今月は見送る。

### 財政局(finance)(hooks の記録で 20:21〜20:22)

- 元のファイル: [m23-finance.md](m23-finance.md)
- 案: なし

- 見たもの: [m23-finance.md の「見たもの」](m23-finance.md#見たもの)(8 行)
- 判断の根拠:

  - 数字: 週の収支 +7,746 は守る線 +3,000 の上で、所持金 2,672,278 は 1,874,000 の上にある。22月末から収支は上がっている。3か月続けての下降もない。守る線を破る理由はない。
  - 計画の予定: 第23月は区127 の基準の調査のみ。計画の前提(区が2つしかなく、税の効果を区の人口で測る)は、今月の `list_districts` でも変わらない。区127 は 2,735 人で、22月の 2,693 から増えているが、1か月の差では判断しない。
  - 計画の数字の更新: 目標の「今」の値を第23月例に合わせた(計画の変更に1行)。予定は変えていない。
  - 医療 110: 墓地が 65% のままで、計画の条件(半分以下)に届かない。保留。
  - 維持費の枠: 駅と名所がまだ置かれていないため、計画が言う「駅と名所の後の数字」は今月の時点では確かめられない。枠は、置かれた後に見る。
  - 前の月の答え合わせ: 22月の財政局は案なし(計画どおり)。判定の対象はない。
  - 観光(重点): 財政局の手は税・予算・政策だけ。観光の政策(RecreationalUse、SmallBusiness)は、m02-4・m03-1・m04-1・m05-4 で効きを切り分けられなかった。今月は動かさない。観光の手は economy と port の案で扱う。
  - 案の数: 0件。案を出さない理由は、守る線に余裕があり、計画が今月を調査と決めているため。

- 捨てたもの:

  - 政策 RecreationalUse を有効にする: 観光への効きは切り分けできていない(m03-1、m04-1)。政策の変更は月1件で、観光の効きは economy の数(attractiveness、名所)で測るほうが確か。財政の手にはしない。
  - 政策 SmallBusiness を有効にする: 週319の費用に対して、Tourism の増えが他の要因と分けられない(m02-4、m05-4)。今月は費用を増やさない。
  - 区127 の住宅税の減税(今月実行): 計画は基準の調査を先にしている。基準がないまま試すと、効果を区の人口で測れない。24月の判断に回す。
  - 医療の予算 110: 墓地が 65% で、計画の条件(半分以下)を満たさない。
  - 全体の税率の変更(住宅・商業・事務所): 人口の減りの原因が、税か需要かまだ決まらない。全体の減税は週の減収が大きい見積もり。
  - 維持費の枠の組み替え(名所・駅): 名所と駅がまだ置かれていないため、組み替える数字がない。

## 4. 差し戻しと再調査

- 住宅都市みどり局: urban-2(実行可 True)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m23-bill.md](m23-bill.md)
- 採った m23-1: 放棄店 10258 の跡に公園 JapaneseGarden(元 urban-1、議決が要る(取り壊し))
- 採った m23-2: 交差点 (2110,-840) の3本を Small 4 Lane にする(元 roads-1、議決は要らない)
- 採った m23-3: 交差点 (3130,-490) に信号を付ける(試し)(元 roads-2、議決は要らない)
- 採った m23-4: 路線28の予算を 180%→200% にする(試し)(元 port-1、議決が要る(予算))
- 採った m23-5: 峰の近くに公園 JapaneseGarden を1棟(試し)(元 economy-1、議決は要らない)
- 採った m23-6: 空き2か所に木を植える(試し)(元 urban-2、議決は要らない)

- 見たもの:

  - `city_info`、`economy`、`services`、`citizens_summary`、`complaints`、`citizen_voices`、`events`、`screenshot`: 見る段で確認(市政ノートの23か月目に記録)
  - 局の案 `council/m23-urban.md`、`m23-roads.md`、`m23-port.md`、`m23-economy.md`、`m23-health.md`、`m23-education.md`、`m23-fire.md`、`m23-finance.md`: 5件の案と4件の調査、案なし4局
  - `council/plan-city.md`: 長期計画と調整1〜25
  - 週の収支 +7,746、所持金 2,672,278(各局の `city_info`)

- 判断の根拠:

  採った5件は、どれも実行計画が確認済みで、道具の引数が書かれている。建設費は合計 5,000、週の維持費の増えは約 +300〜350(公園 +80、バス +220〜270)。週の収支は約 +7,400 に残り、守る線 +3,000 と、下降規則の +4,900 の上にある。所持金は 2,667,000 前後で、守る線 1,874,000 の上にある。取り壊しは m23-1 の1件で、放棄店のため失うものは0。観光(重点1)は m23-5、交通(重点3)は m23-2 から m23-4。8-1(重点2)は施策がなく、調査 s23-1 で原因を切り分ける。試しの案は m23-3、m23-4、m23-5 の3件で、場所は重ならない。

- 捨てたもの:

  - urban-2(木の試し): 再調査で位置が確認でき、m23-6 として採った
  - 財政局の調査(区127): 3件の上限と、他の2件の優先。24月に回す
  - 保健環境局、教育委員会、消防局、財政局の施策: 案なし。市長は代案を作らない
  - 重点 8-1 の施策: 局に確かめ済みの手がなく、調査で原因を見る
  - 政策 SmokeDetectors、Recycling、HeavyTrafficBan、FreeTransport: 局が費用か副作用で見送った

## 6. 議会: 可決と否決(hooks の記録で 20:32〜20:32)

- 元のファイル: [m23-assembly.md](m23-assembly.md)
- m23-1 取り壊し: 可決。preview_bulldozeで働き口0・家0・施設なしを確認。
- m23-2 財政: 可決。費用0で守る線に響かない。
- m23-3 財政: 可決。費用0で守る線に響かない。
- m23-4 予算: 可決。+20は上限内。響きも書かれ、維持費+250は守る線の内。
- m23-5 財政: 可決。建設費2,500、維持費+40で守る線の内。
- m23-6 財政: 可決。建設費約50で小さく、守る線を破らない。
- 可決した種類(hooks が見る): 取り壊し、予算

- 見たもの:

  - `city_info`: 所持金 2,672,278、週の収入 336,105、支出 328,359
  - `preview_bulldoze`: 10258 のみ、失う働き口0・家0、電気の影響0
  - `council/m23-bill.md`: 6件の施策

- 判断の根拠:

  6件とも、費用は合計で建設費 5,050、維持費 +330 と小さく、守る線に十分な余裕がある。取り壊しの m23-1 は損失0を自分で確かめた。型の上限(税、予算±20、政策)を超える施策はない。

- 捨てたもの:

  - m23-6: 維持費が未確認なので否決を考えたが、額が小さく守る線を破らないため可決した

## 7. 実行する市長: 実行と見回り(hooks の記録で 20:33〜20:41)

- 実行してよい施策: m23-1、m23-2、m23-3、m23-4、m23-5、m23-6
- 実行した: m23-1、m23-2、m23-3、m23-4、m23-5、m23-6
- 失敗した: なし
- 臨時: なし
- 見回り 2051-11-12: 人口 172662、所持金 2677720、週の収支 6999、幸福度 87
- 見回り 2051-11-22: 人口 172401、所持金 2688287、週の収支 7496、幸福度 87
- 報告: 長いので [市政ノート](../mayor-note.md) を見る(923 字)

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m23、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 20:18〜20:51(hooks の記録の時刻から)、道具の行 282
- 議会が可決した種類: 予算、取り壊し
- 議決が要る道具の呼び出し: 2 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 611 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m23-zone-east.jpg`

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

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 10)
