# 11か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 16:15〜16:15)

- 元のファイル: [m11-policy.md](m11-policy.md)
- ゲーム内の日付: 2050-11-07、保存: fukuoka-plan-m11
- 重点: 5-1・5-2 観光(名所・attractiveness・Tourism)、5-1・5-2(入口) 旅客の駅・港・空港、8-1 物流・人流のゲートウェイ

- 見たもの: [m11-policy.md の「見たもの」](m11-policy.md#見たもの)(15 行)
- 判断の根拠:

  観光は市長の方針で重点に入れ、入口は一度も案が実を結んでいないため2番目に置いた。3つ目は、計画の目標から最も遠い数字(止まったトラック580、目標250以下)の8-1を選んだ。4-3 汚染は焼却場の停止が効かず、出どころが分からないので、重点にせず調査の案に回す。

- 捨てたもの:

  - 4-3 汚染: 10351 の停止で汚染の印が27→30と動かず、出どころが不明。重点ではなく、局の調査や試しの案で扱う
  - 6-3 交通: 流れ54%で、4車線化の効きは小さい。8-1 の貨物の止まりと一緒に、局が案を出してよい
  - 6-1 事務所L3・大卒の失業: 事務所税2%は2回続けて「まだ分からない」。財政局が案を出してよいが、重点にはしない
  - 4-2 公園: 86棟で目標100に遠いが、今月の公約への効きが小さい

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

### 住宅都市みどり局(urban)(hooks の記録で 16:17〜16:18)

- 元のファイル: [m11-urban.md](m11-urban.md)
- 案 urban-1: 電気の届く道沿いに公園を1か所足す(658,1400)
  - 建設費 1000、週の維持費 +8、戻せる
  - 市の計画: 4-2
  - 議決: 要らない

- 見たもの: [m11-urban.md の「見たもの」](m11-urban.md#見たもの)(16 行)
- 判断の根拠:

  - 4-2 は、今の 86 棟から目標 100 に届かない。電気が届き、道に面する空きが、確かめた範囲で (658,1400) の1か所だけだった。他の候補は、電気が z=1460 の行で届かないか、既存の公園や歩道にぶつかった
  - 4-1 の高密度住宅(地価 59、目標 62)は、高密度住宅の近くの空きが取れなかった。残り1か月で地価に効く見込みが薄いため、事業3を見送った
  - 政策の比べ: HighTechHousing は 20,252/週で、週の収支が +10,680 から −9,572 になる。守る線(+3,000)を大きく割るので採らない。SmokingBan は有効のまま。政策の変更は、urban の数字には効かない
  - 案は1件。電気と道の条件を確かめた場所は1か所だけなので、予備を置かず、案を1件にする

- 捨てたもの:

  - 公園 (668,1460) east、(752,1460) west: 置ける(`test_place_building` が ok)が、`map_layer` の z=1460 の行は電気 0。電気が届かないため、実行の条件を満たせない
  - 公園 (766,1408) west、(754,1432) west: 既存の公園 19278 と歩道にぶつかる(ObjectCollision)
  - 公園 (668,1530) east: 取り壊し対象の StatueOfWealth 11580 にぶつかる(電気の印の名所。取り壊しは議決が要る)
  - ParadoxPlaza (690,1372)、Regular Plaza (735,1320): 道と歩道にぶつかる
  - 事業3(高密度住宅の近くの公園、地価の手): 高密度の空きが取れず、残り1か月で効く見込みが薄い(予想)
  - HighTechHousing: 20,252/週で守る線を割る

### 道路下水道局(roads)(hooks の記録で 16:17〜16:19)

- 元のファイル: [m11-roads.md](m11-roads.md)
- 案 roads-1: 交差点 (2280,-950) に信号を試す
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m11-roads.md の「見たもの」](m11-roads.md#見たもの)(15 行)
- 判断の根拠:

  - 6-3 の流れ(54%)を動かす候補は、blocked が集まる場所の4車線化か信号だった。しかし、(2310,-944) の4車線化は、36011 の9mの stub に止められた。z=100 の Large 化は、火葬場・高校・バスデポに当たる。取り壊しの案は、死体処理の施設と学校を失うので採らない。
  - 実行できる手は、交差点 (2280,-950) の信号だけだった。建設費 0、場所と接続を道具で確かめた。効きは量を見積もれないので、試しとして出す。
  - 案の数は1件。案を埋めるための案は出さない。(-1678,-1323) の止まりは原因が分からないので、調査を1件出す。

- 捨てたもの:

  - Basic Road 3334 の4車線化(2310 付近の詰まりの元): 36011 とぶつかり、36011 は 9m で広げられない。36011 を取り壊すと西の接続が切れるため、不採用。
  - Basic Road 11179(z 100、x 1457〜1535、blocked 33 の場所)の Large 化: 火葬場 29774 に当たる。壊すと死体処理の施設を失い、4-3 の死体の印の対策と逆になる。不採用。
  - 109 と 3239(z 100)の Large 化: 高校 1226 とバスデポ 30483 に当たる。取り壊しを伴い、失う働き口と学校が大きい。不採用。
  - 政策 HeavyTrafficBan(0円): 貨物トラックを締め出し、品物がない店(209)を増やすおそれがある。6-4 と 8-1 に反する。不採用。
  - 政策 FreeTransport(0円): 運賃収入が0になる。交通の流れへの効きは量を見積もれない。財政の判断として、不採用。
  - 本土の名所の送電線(前月 roads-2 の再提出): 名所の建物が (1580,-530) にまだない。名所が置かれてから引く(事業2)。今月は出さない。
  - 旅客の駅への道・水・電気: 駅がない。港湾空港局が駅を決めてから(事業2)。
  - 貨物センター 28755 の道の差し替え: 止まったトラックは敷地内の WaitingSpace(前の月の調査 s03-1)で、道の blocked は 0。道の詰まりでないため、道路の手は効かない。8-1 は港湾空港局。
  - 西 z=-560 の4車線化の撤去: 11/7 の blocked は 14(基準 66)。戻す条件を満たさない。

### 港湾空港局(port)(hooks の記録で 16:17〜16:20)

- 元のファイル: [m11-port.md](m11-port.md)
- 案: なし

- 見たもの: [m11-port.md の「見たもの」](m11-port.md#見たもの)(14 行)
- 判断の根拠:

  旅客の入口は、解禁済みの旅客の駅・港・空港がすべて下水を要る。下水の網は、空き地3(700,1700)にも港の候補にも届いていない。網のある貨物センター48243 は、線路の2,933m が事務所の密集地を通るため、試しで断られた。この2つを両方満たす手は、今月の確かめた範囲にない。事業1は、11月の判定(電気・下水・外への線路のどれかが通る)を満たさないので閉じる。
  8-1 は、580台が敷地の中で空き待ちのまま止まっている。道の上の止まり(382台)とは別の原因の可能性があるが、原因はまだ確かめていない。道の差し替えや貨物駅の増設は、原因を確かめてから出す。今月は、調査で止まり方の動きを見る。
  今月は、確かめた実行条件を満たす案がないので、案は0件とする。

- 捨てたもの:

  - 旅客の駅を空き地3(700,1700)に置く案: 半径1,500m 内に下水の網がなく、下水を引く管も解禁済みの一覧にないため、実行条件を満たせない。事業1 は閉じる
  - 貨物センター48243 の近くに旅客の駅を置き、線路を外へ引く案: 線路の2,933m が事務所の密集地を通り、試しで断られた(overlaps 約60棟)。取り壊しを含むので、今月は見送る
  - 貨物港 (-640,1074) の近くに旅客の港を置く案: 半径400m 内に下水の網がなく、実行条件を満たせない
  - 空港(150,000、週4,800): 旅客の入口の条件は同じく下水が要り、費用も大きく、今月の上限に入らない
  - 8-1 の道の差し替え案: 原因が分かっていないため、今月は出さない。調査の結果を見て出す
  - 政策による対策: 8-1 の止まりと旅客の入口に効く解禁済みの政策が見当たらない

### 経済観光文化局(economy)(hooks の記録で 16:17〜16:21)

- 元のファイル: [m11-economy.md](m11-economy.md)
- 案 economy-1: 観光の名所 Servicing Services を東の空き地に置き、道・電気・水をつなぐ
  - 建設費 21040、週の維持費 +340、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m11-economy.md の「見たもの」](m11-economy.md#見たもの)(20 行)
- 判断の根拠:

  - 担当の数字のうち、名所の棟数だけが目標 10 に届いていない(9)。名所は1棟足せば届く。10月に採られなかった案の理由は、道と水の接続の未確認だった。今月は、道・電気・水を試しの道具で通せたので、実行条件はそろった
  - 場所は、市の中心に空きがないため、東の空き地 (1580,-530) を選んだ。中心の attractiveness の山は (1430,-680) と (-1700,-750) にあるが、空きがなく、`test_place_building` で置けなかった
  - 案は1件にした。2棟目の名所は、1棟目の効きを見てから決める。同じ月に2棟目を足すと、測る数の場所が重なり、効きが分からなくなる
  - 費用は、週の収支 +10,680 に対し、週 340 の増え。守る線(+3,000、所持金 1,874,000)を破らない
  - 調査は1件。効き目の量は見積もれないため、名所の効きを見る道具(attractiveness と観光客)を決めた

- 捨てたもの:

  - 中心の空きに名所を置く案: 市の中心 (-1700〜-1300, -625〜-800) は attractiveness が高いが、空きがない。`test_place_building` で 2 か所とも ObjectCollision。取り壊しで住宅を減らす案は、住民への影響が大きく、今月は見送る
  - 放棄された店やホテル(-1176,-1166)〜(-1404,-1214)の跡に名所: 中心の山から 400m 以上離れ、attractiveness が低いと見込む。今月は試していない。効き目が分かってから候補にする
  - 11580 の電気を引く送電線(603,1533)→(668,1565): 11580 の敷地と重なり断られた。11580 は、電気がなくても attractiveness 75 がある。今月の名所の数は変わらないため出さない。空き地3の接続は道路下水道局の担当
  - 政策 RecreationalUse・SmallBusiness・EducationBoost の有効化: RecreationalUse は m04 で効きが見られず外した。SmallBusiness と EducationBoost は m05、m07 で試し済み。観光の効きの根拠が増えないため出さない
  - 2棟目の名所(別の空き地): 1棟目の効きが分からないうちは、見送る
  - 旅客の入口: 港湾空港局の担当。局は求めることとして長期計画に書く

### 保健環境局(health)(hooks の記録で 16:17〜16:24)

- 元のファイル: [m11-health.md](m11-health.md)
- 案 health-1: 焼却場 2267 の運び先に埋立地を空き地へ置き、2267 を止める
  - 建設費 4000、週の維持費 +160、戻せる
  - 市の計画: 4-3、4-4
  - 議決: 要らない

- 見たもの: [m11-health.md の「見たもの」](m11-health.md#見たもの)(29 行)
- 判断の根拠:

  - 汚染の出どころは 2267 と確かめた(pollution の最大が 2267 の周り)。10351 は外れだった。よって 11月の計画の条件(10351 で汚染が減る)は崩れ、計画を直した。
  - 2267 の停止は、ごみを増やす恐れがある(m02 で ごみ11→22)。その対策として、近くの埋立地を先に置く案にした。
  - 埋立地の場所は、(3640,-200) の1か所しか確認できなかった。放棄の建物の跡は、10x8 の敷地に入らなかった。取り壊しは、失う働き口が75(家0)で、wouldDemolish の件数と preview_bulldoze が一致した。
  - 案は1件。2件目(死体の印の手)は、原因が確かめられていないので、調査にした。
  - 重点(観光、入口、8-1)には当たらない。4-3・4-4 の目標は今の数字から遠いが、12か月のうち残る1か月で、確かめられた手に限った。

- 捨てたもの:

  - 10351 を戻す案: 汚染は減っておらず、戻しても効く見込みが低いので、今月は出さない。12月に判定する。
  - 別の場所の埋立地(放棄の建物の跡): 10x8 の敷地に入らないと、test_place_building で確かめた(37356、39789)。
  - 政策 Recycling: ごみの印は8で、今は足りている。住宅税を5%下げる費用が増えるため、今月は見送る。
  - 死体の印への火葬場・墓地の追加: 施設は満杯0(used 14,019 / 24,000)で、印の場所も散らばっている。火葬場の型も確かめられなかったので、原因が分かるまで出さない(調査を出した)。

### 教育委員会(education)(hooks の記録で 16:17〜16:17)

- 元のファイル: [m11-education.md](m11-education.md)
- 案: なし

- 見たもの:

  - `services`: 小学校の定員 14,268、高校の定員 24,360、大学の定員 36,540。電気・水・下水は容量に余裕がある。
  - `citizens_summary`: 子ども 9,363、10代 20,993、住民 179,903、来ない市民 0 / 0 / 0。大卒の失業 8,341(教育の担当の数字ではない)。
  - `city_info`: 人口 179,848、所持金 2,313,772、週の収支 +10,680(収入 335,847、支出 325,167)、dialog なし。
  - `list_policies`: EducationBoost は active=false、costPerWeek 7,940。ほかに教育の数字に関係する政策はない。SmokingBan(active)、BigBusiness(active)は教育と関係がない。政策一覧の取得は成功した。

- 判断の根拠:

  - 担当の数字は、小学校と高校の両方で目標を満たしている。定員から子ども・10代を引いた余裕は、小学校 4,905、高校 3,367。どちらも、長期計画で事業を置く条件(余裕 1,000 を切る)より十分に大きい。
  - 計画の第11月の予定は「余裕の推移を見る」で、今月の数字は計画の前提どおり。計画は直さない。
  - 前の月(10月)は案なしで、答え合わせの対象はない。
  - 有効な手は今月なく、案なしにする。前月の非採択は理由にしていない。

- 捨てたもの:

  - 高校の新設(建設費 24,000、週 +560): 余裕が 3,367 あり、置く条件に当たらない。置くと、今の定員が10代の数を上回る状態が続き、週の維持費だけが増える。
  - 小学校の新設(建設費 10,000、週 +160): 余裕が 4,905 あり、条件に当たらない。子どもも減っている。
  - EducationBoost の有効化(週 7,940): 学校の定員を増やさない。守る線を割るため、出さない。

### 消防局(fire)(hooks の記録で 16:16〜16:19)

- 元のファイル: [m11-fire.md](m11-fire.md)
- 案 fire-1: 焼け跡の事務所 37356(3508.3,-274.7)を取り壊す
  - 建設費 0、週の維持費 +0、戻せない
  - 市の計画: 3-4
  - 議決: 要る(取り壊し)

- 見たもの: [m11-fire.md の「見たもの」](m11-fire.md#見たもの)(18 行)
- 判断の根拠:

  - 事業3の条件(焼け跡が出た月に取り壊しの案を出す)を満たした。37356 は放棄され、火事の印を持つ。事業1の条件は未達(犯罪の印が3以上の月が続いていない)。
  - 取り壊す1棟は、働き口0、家0。preview_bulldoze(what="abandoned")で確かめた。occupied の事務所を巻き込まない形を、試しの道具で確かめた。
  - 火事の印が1つ減ると、3-4 の合計が5から4になり、目標に届く。ほかに同じ効きを持つ手は見当たらない(消防署の新設は火事の効きが届いており根拠がない。SmokeDetectors は週 57,948 で守る線を破る)。
  - 案は1件。ほかの候補に実行条件を満たすものがない。調査は1件。犯罪率の原因を確かめる。

- 捨てたもの:

  - 同じ円の全部の取り壊し(what="building"): 働き口20を失う(事務所 7356、9339 を含む)。放棄された1棟だけを壊す形に絞った。
  - 工場 10741(3622,-506)の取り壊し: 放棄されているが、火事の印がなく、3-4 の数に効かない。対象外。
  - 警察署を (3604,-373) 付近に新設する案: 警察の効きが平均121あり、効き目を見積もれない。建設費 12,000、週 480 を払う根拠が足りない。調査の結果で12月に出し直す。
  - 警察署 45584 を移す案(建設費 2,400): 移す先の効きの見積もりがない。事業1の条件も未達。
  - 消防署の新設、Fire House の再置き: 火事の効きは届いている(平均192)。火事の場所が毎月違う。根拠なし。
  - 政策 SmokeDetectors: 週 57,948 で、守る線を破る。

### 財政局(finance)(hooks の記録で 16:17〜16:17)

- 元のファイル: [m11-finance.md](m11-finance.md)
- 案 finance-1: 事務所税を 2% から 3% に戻す
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-1
  - 議決: 要る(税)

- 見たもの:

  - `city_info`: 人口 179,848、所持金 2,313,772、週の収入 335,847、週の支出 325,167(週の収支 +10,680)、観光客 1,763(訪問 138)、dialog なし
  - `economy`: tax.office 2(案1の前の値)。税は住宅低9/高7、商業低9/高3、工業3。予算は roads 120、garbage・healthcare・police 150、fire 140
  - `list_policies`: policyExpensesPerWeek 10,812。有効は SmokingBan(費用0)と BigBusiness(4,012)。EducationBoost は無効(費用7,940 の見積もり)。SmallBusiness と RecreationalUse は無効(RecreationalUse は費用0)。税の政策(TaxRaise / TaxLower 系)は、いずれも費用0で無効。政策の一覧は、観光と事務所に直接の効きを示していない
  - `demand_breakdown`: 働き口 87,275(空き 2,602)、空き家 5,080、失業 9,736(大卒 9,227)、需要 住14・商2・工66
  - `economy_breakdown`: Office 収入 16,472、Tourism 27、policyExpenses 10,812、loanExpenses 0

- 判断の根拠:

  事務所税の試し(9月から)は、10月から11月の事務所の建設が0で、大卒の失業にも効かなかった。計画の11月の予定は「外れなら 3% に戻す」で、戻す条件(事務所の建設が2か月続けて0)も満たした。よって案1は、税を 3% に戻す1件に絞った。週の収支は +10,680 で守る線 +3,000 の上にあり、戻すと余地が広がる。案は1件。
  EducationBoost の再投入は、週 7,940 の費用が枠の中に入るが、大卒の失業への効きの向きが分からない(教育を増やすと大卒の働き手も増える)。1か月では判定できないため、今月は出さない。

- 捨てたもの:

  - 政策 EducationBoost の再投入(週 7,940): 大卒の失業に効く見込みはあるが、効きの向きが分からず、1か月で判定できない。税を戻したあとの枠で、12月の月例に改めて見る
  - 道路の予算 120 から 100 への変更: 計画の保留どおり。交通の流れは 54% で、60% に届く前に維持費を減らす理由がない
  - 税の追加の変更(住宅・商業など): 週の収支は守る線の上にあり、担当の数字の改善に当たらない。今月は、税の変更を1件に絞る

## 4. 差し戻しと再調査

- 保健環境局: health-1(実行可 True)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m11-bill.md](m11-bill.md)
- 採った m11-1: 名所 Servicing Services を (1580,-530) に置く(元 economy-1、議決は要らない)
- 採った m11-2: 公園 Regular Park を (658,1400) に置く(元 urban-1、議決は要らない)
- 採った m11-3: 焼け跡の事務所 37356 を取り壊す(元 fire-1、議決が要る(取り壊し))
- 採った m11-4: 事務所税を 3% に戻す(元 finance-1、議決が要る(税))
- 採った m11-5: 交差点 (2280,-950) に信号を付ける(試し)(元 roads-1、議決は要らない)
- 採った m11-6: 埋立地を (3250,-362) に置き、条件付きで焼却場 2267 を止める(元 health-1、議決は要らない)

- 見たもの:

  - `m11-urban.md`、`m11-roads.md`、`m11-port.md`、`m11-economy.md`、`m11-health.md`、`m11-education.md`、`m11-fire.md`、`m11-finance.md`: 8つの局の案を読んだ(局が道具で確かめた結果として)
  - `mayor-note.md`: 数字の表、分からないことの一覧、10月・11月の月例
  - `m11-policy.md`: 重点は 5-1・5-2 観光、5-1・5-2(入口)、8-1
  - 費用の合計(自分で足した): 建設費 1,000 + 21,040 + 0 + 0 + 0 = 22,040。週の維持費の増え 8 + 340 = 348。税収 約 +8,000 は見込み。週の収支は +10,680 から約 +10,330(税を含めて約 +18,300)。所持金は約 2,291,700。守る線(+3,000、1,874,000)の上

- 判断の根拠:

  重点1の名所は、道・電気・水を局が道具で通したので採った。重点2の旅客の入口は、解禁済みの駅・港・空港がすべて下水を要り、確かめた候補に下水の網が届かないため、港湾空港局は案なしにした。根拠は道具の結果で、局の役割から外れた判断ではない。重点3の8-1は原因が不明なので調査にした。
  取り壊しを伴う案は、失うものが0の m11-3 だけを採った。health-1 は75の働き口を失い、受け皿不足の根拠が弱いので採らない。税は、2%の試しが2回「まだ分からない」で効かなかった結果から、戻す。信号は費用0で戻せる試しとして採った。

- 捨てたもの:

  - health-1: 上の「採らなかった案」のとおり。取り壊しの損失に対し、効きの根拠が弱い
  - 教育委員会、港湾空港局の案なし: 教育は定員に余裕があり、港湾空港局は実行条件を満たす手がない。市長は代案を作らない
  - 編成方針で重点にしなかった 4-3 汚染、6-1 事務所: 汚染は health-1 の見送りで今月は動かさない。事務所は m11-4 の税の戻しで扱う

## 6. 議会: 可決と否決(hooks の記録で 16:26〜16:26)

- 元のファイル: [m11-assembly.md](m11-assembly.md)
- m11-1 財政: 可決。建設費21,040、維持費+340で守る線に収まる。
- m11-2 財政: 可決。建設費1,000、維持費+8で守る線に影響しない。
- m11-3 取り壊し: 可決。preview_bulldozeで失う働き口0、家0、電気影響0を確認。代わりの手も書かれている。
- m11-4 税: 可決。変更幅+1で上限内。2%の試しの結果を踏まえた理由があり、収支は上向く。
- m11-5 財政: 可決。建設費0で戻せる。守る線に影響しない。
- m11-6 財政: 可決。建設費4,000、維持費+160で守る線に収まる。2267停止で維持費は減る。
- 可決した種類(hooks が見る): 取り壊し、税

- 見たもの:

  - `economy`: office 税 2%、ほかの税率と予算を確認。m11-4 の前提と一致
  - `city_info`: 所持金 2,313,772、週の収入 335,847、支出 325,167
  - `preview_bulldoze`: 37356 の1棟、働き口0、家0、電気の影響0
  - `council/m11-bill.md`: 議案を読んだ

- 判断の根拠:

  費用の合計は、案の自己計算に 4,000 の抜けがあり、スクリプトの 26,040 を正とした。それでも所持金は約 2,287,700 で 1,874,000 を大きく上回り、週の収支も +3,000 を上回る。取り壊しは失うものが0と確かめた。税の変更は幅が上限内で、前月までの結果に基づく理由がある。

- 捨てたもの:

  - m11-5: 効きが不確かで外れる恐れがあるが、費用0で戻せ、中止条件もあるため可決
  - m11-4: 事務所の建設が戻らない恐れがあるが、否決の4点に当たらないため可決

## 7. 実行する市長: 実行と見回り(hooks の記録で 16:27〜16:34)

- 実行してよい施策: m11-1、m11-2、m11-3、m11-4、m11-5、m11-6
- 実行した: m11-3、m11-4、m11-5
- 失敗した: m11-1、m11-2、m11-6
- 臨時: なし
- 見回り 2050-11-17: 人口 179825、所持金 2315777、週の収支 18525、幸福度 88
- 見回り 2050-11-27: 人口 179798、所持金 2338772、週の収支 15802、幸福度 88
- 報告:

  議決が要る m11-3(焼け跡の事務所 37356 の取り壊し)と m11-4(事務所税 2%→3%)を、advance の前に打った。m11-5 の信号は付けた。m11-1 は名所を置けたが、入口の道は建物の外形に重なって引けなかった(RoadNotConnected)。電気と水は届いた。m11-2 の公園は電気の中止条件に当たり見送った。m11-6 は埋立地を置いたが、garbage.full が2で、2267 は止めなかった。月末は 2050-12-07。人口 179,547(11/7 の 179,848 から減少)、所持金 2,358,955、週の収支 +13,509。観光客 1,725、Tourism 週42、名所10棟。信号の blocked は見回りでは2と0で、月末は82(基準72)だった。月末は見回りではないので外していない。境目に当たらず、臨時は行っていない。hooks に止められた手はなかった。市政ノート: /Users/takeshita/orca/workspaces/tried/issue-124/2026/10-27-AI市役所で福岡を観光都市にする-03-観光の街を目指す計画と局を決める/mayor-note.md

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m11、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 16:14〜16:44(hooks の記録の時刻から)、道具の行 299
- 議会が可決した種類: 取り壊し、税
- 議決が要る道具の呼び出し: 2 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 602 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m11-port-map-north.jpg`

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

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 8)
