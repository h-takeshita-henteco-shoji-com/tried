# 15か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 17:42〜17:42)

- 元のファイル: [m15-policy.md](m15-policy.md)
- ゲーム内の日付: 2051-03-07、保存: fukuoka-plan-m15
- 重点: 5-1・5-2 観光(入口、名所、島と空き地)、8-1・6-4 物流・人流のゲートウェイと企業の立地、4-2 花や緑による潤い

- 見たもの: [m15-policy.md の「見たもの」](m15-policy.md#見たもの)(16 行)
- 判断の根拠:

  観光の4つの数字(Tourism、attractiveness、入口、観光客)は、14か月続けて目標から遠く、市長の方針として毎月の重点に入れる。残りの2つは、目標から遠い度合いで選んだ。8-1 は止まったトラックが653で目標の2.5倍、6-4 は品物がない店と原料がない工場が目標を超えている。4-2 は残り11棟で、費用が小さく確かめ済みの手がある。週の収支の余裕が小さいので、維持費の大きい案は重点に置かない。

- 捨てたもの:

  - 6-3 交通(流れ55%、目標60): 前月より上がり、止まった車も減った。信号の効きは揺れて切り分けられず、重点から外す。案が出れば評価する
  - 4-3 汚染(印27、目標15以下): 出どころが特定できず、手が出せない。調査があれば歓迎する
  - 1-2 健康、3-3 来ない市民、3-4 安全、2-3 教育: 目標を満たしている。保つだけ
  - 6-1 事務所L3(3,280、目標3,500): 税の試しで動かなかった。重点にしない

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

### 住宅都市みどり局(urban)(hooks の記録で 17:43〜17:45)

- 元のファイル: [m15-urban.md](m15-urban.md)
- 案 urban-1: 放棄された店の跡(1856,183)に JapaneseGarden を置き、公園を1つ増やす
  - 建設費 2500、週の維持費 +40、戻せない
  - 市の計画: 4-2
  - 議決: 要る(取り壊し)

- 見たもの: [m15-urban.md の「見たもの」](m15-urban.md#見たもの)(13 行)
- 判断の根拠:

  - 4-2 は Beautification 89 で、目標100まで11。12か月で1か月1つ(22月は2つ)の計画を続ける。今月は、放棄店の候補を8か所試し、条件を満たしたのは (1856,183) の1か所だけだった。ほかの7か所は、道路やサービスの建物に当たる、または働き口8〜15や家2〜19を失うため、取り壊しでは採れない。
  - 案 urban-1 は、取り壊す2棟の働き口と家が0、入口の道路と電気・水が確認でき、費用も守る線の範囲内なので採った。
  - 案は1件にした。候補が少ないため、2件目を作っても、同じ放棄店の候補を奪い合う。件数を埋めるための案は作らない。
  - 週の収支は +4,216 の見込みで、守る線 +3,000 の上。4-2 以外の手(HighTechHousing など)は、週の費用が余裕を超えるか、4-1 の効きが見積もれないので、今月は採らない。

- 捨てたもの:

  - Regular Park(9×8、建設費 1,000、維持費 8): 計画では2100〜2250 の場所で道や電線に当たった。今月は試していない。候補が取れれば、次の月に試す価値がある。
  - HighTechHousing(政策、週 20,260): 守る線の余裕 1,256 を超える。4-1 の地価への効きも確認できていない。
  - 事業2の地価の測り(第16月に予定): 今月は予定にない。計画どおり第16月に測る。
  - 放棄店の取り壊し(候補8か所のうち、取り壊しで働き口や家を失うもの): 働き口8〜15または家2〜19を失うので採らない。

### 道路下水道局(roads)(hooks の記録で 17:43〜17:44)

- 元のファイル: [m15-roads.md](m15-roads.md)
- 案 roads-1: 交差点 (-1640,-1010) に信号を置く
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m15-roads.md の「見たもの」](m15-roads.md#見たもの)(14 行)
- 判断の根拠:

  - 6-3(交通の流れ 55%、目標60%)が担当の数字。14月の信号 (-1640,-1100) は基準 62 に対し 1→8→33 と、基準を超えず残せる状態。計画の規則により次の交差点へ進む。(-1640,-1010) は止まりの集まり (-1666,-1029) の近くで、canEnableLights が確認済み。案1として出す
  - 事業2(名所 40850 の道)は、計画の「入口の確認手段がなければ中止」に当たる。確認手段は3つの向きで試しても見つからず、印も残る。中止し、5-1・5-2 の道の手は今月ない。5-1・5-2 の入口は事業3で、駅が置かれるまで待つ
  - 案は1件にする。ほかの交差点や道の太さの手は、同じ範囲の測りと重なるため、今月は出さない。東の出口は調査で測り、17月に手を決める
  - 5-1・5-2 の観光の数字に対して、道路が今月できることは少ない。その事実は判断の根拠として残す

- 捨てたもの:

  - 交差点 (1692,100) に信号: 道が2本しかなく、止まりの集まりからも遠い(約190m)。交差点として効く見込みが小さい
  - 道 (-1640,-984)・(-1640,-808) の Basic Road を Small 4 Lane に太くする: 密度100の区間だが、測り分けの範囲が信号と重なり、太くすると止まりが移った前例がある(西の幹線 m09-2)。今月は見送る
  - 政策 HeavyTrafficBan: 費用は0だが、トラックを止めるため、品物がない店267、原料がない工場49を悪くするおそれ。8-1・6-4 と逆に効く
  - 政策 FreeTransport: 運賃収入が週 5,229 消え、週の収支 +4,256 が負になる。守る線 +3,000 を割るので取らない
  - 事業2の南回り (1640,-530)→(1640,-590)→(1600,-595): 入口の位置と向きが未確認のため。中止した

### 港湾空港局(port)(hooks の記録で 17:43〜17:47)

- 元のファイル: [m15-port.md](m15-port.md)
- 案: なし

- 見たもの:

  - `list_policies`: 有効は SmokingBan(0)、EducationBoost(週7,940)、BigBusiness(3,832)。政策の費用は週10,598。RecreationalUse(0)、SmallBusiness(313)、Recycling(0)は無効。観光や入口に効く新しい政策は、今月は選ばない。
  - `cargo`: 止まったトラック964、敷地の中653、28755が632。品物が届かない店267、原料が届かない工場49。
  - `vehicles_stuck`(building=28755): 766台。632台が WaitingSpace と InGrounds(敷地の中で空き待ち)、88台が道の上で空き待ち、453台が7日以上止まっている。行き先は1〜6kmに分かれる。
  - `test_place_building`(Train Station, (-4700,1600), south): 置けるのは assume_terrain(72m)を付けたときだけ。入口は (-4700,1576)、道は未接続(road null)。費用45,000、維持費960/週。
  - `test_build_line`(Power Line, [[-4650,1500],[-4675,1540],[-4690,1592]]): ok。2区間、費用260、交差と重なりなし。
  - `test_build_line`(Water Pipe, 本土から島へ、35区間、費用6,240): ok(前月までの試し)。海の上の通水は未確認。
  - `test_upgrade_road` と `test_build_line`(Basic Road, [[-4640,1552],[-4700,1552],[-4700,1568]]): 仮定なしでは SlopeTooSteep。66mに整地した仮定で通る。

- 判断の根拠:

  - 第15月の予定は「島Bの水源・電線・水管を試し、候補を1つに決める」でした。候補は (-4700,1600) 南向きに決めました。電線と水管は仮定なしで通ります。
  - ただし駅と道は、整地を仮定しないと置けません。必須の実行条件が未確認のため、この月は案を出しません。整地の試しは、実行する市長が `level_terrain` を test=true で行い、その結果を持って次の月に案を出します。
  - 8-1 の振り分けは、計画の前提が崩れています。`vehicles_stuck` で 3940 と 4740 を見ると、28755 から出る車はありません(前月までの確認)。振り分けを試す道の根拠がないため、道は引きません。代わりに 28755 の空き待ちを調査で追います。
  - 守る線: 現在の週の収支は +4,256。駅の960と水管・電線・道の維持費(約40)を足すと約3,256で、+3,000 は守れます。ただし余裕は約256です。3か月続けて下がる規則に入るため、次の月に案を出すときは、収支の見込みを確かめます。

- 捨てたもの:

  - 島Bの旅客の駅(-4700,1600)の案: 整地と道の傾きが未確認。実行条件が揃うまで出せません。次の月に、整地の試しを済ませてから出します。
  - 8-1 の振り分けの道(28755 から 3940 へ): 3940 と 4740 に出入りする車が0のため、目的地が成り立ちません。調査で空き待ちを追ってから判断します。
  - 4-2 の公園を11棟足す案: 今月は島Bの入口に手を集めるため、出しません。次の月に、取り壊しなしで置ける候補を確かめて出します。

### 経済観光文化局(economy)(hooks の記録で 17:43〜17:47)

- 元のファイル: [m15-economy.md](m15-economy.md)
- 案: なし

- 見たもの:

  - `list_policies`: 政策一覧。有効は SmokingBan、EducationBoost(7,940)、BigBusiness(3,832)。RecreationalUse、SmallBusiness(313)は無効。政策費用の合計 10,598
  - `zones_at`: (2500,500) r150。事務所 258(空き3)、住宅(高) 26(空き0)、未指定 60、商業(高) 17(空き4)
  - `list_net_types`: Water Pipe、建設 2,500/km、維持 10/週/km
  - `net_near`: (-4300,1600) r700、Water の管 0 本
  - `water_trace`: (-4620,1608) の島B。水と下水は届かず、管網なし。本土の網(2445 区間、取水塔多数、排水の処理場あり)
  - `water_trace`: (2692,463) 本土の商店。水と下水は届く
  - `test_place_building`: Transport Tower (2715,470) 西向き、ObjectCollision(道路 6704、33471、商店3棟)
  - `test_place_building`: Transport Tower (-4620,1608) 南向き、ok、費用 60,000、needs 電気・水・下水、入口 segment 13902(0.6m)
  - `test_build_line`: Basic Road (-1500,-500)〜(-500,-500)、建物の重なりで断り(水塔 26691、30116、高層住宅 8353、21746、13598、16024、事務所 31488、埋立地 46633)

- 判断の根拠:

  - 名所の型は、未建設のもので試す必要がある。3型の AlreadyExists は、計画の前提(3型を建てる)を外した。計画は直した。
  - 島Bの候補は、水と下水の接続が確かめられない。必須条件が残るので、実行対象にしない。
  - 本土の候補と事務所の道は、今回の確認で通らなかった。16月に、重ならない場所を探し直す。
  - 週の収支の余裕 1,256 は、名所1棟で使い切りに近い。島の管を足すと守る線を割るため、案は見送る。

- 捨てたもの:

  - Transport Tower 島B(-4620,1608): 入口と置く場所は確かめた。水と下水の管が未確認(最寄りの網まで数km)。試しは作れるが、接続の手がないため実行可否は未確認。今月は出さない。
  - 事務所の道 (-1500,-500)〜(-500,-500): 建物と重なり、通らない。
  - Colossal Offices、Library: 費用 70,000〜90,000、週 1,200〜1,360。Library は守る線を割る。Colossal Offices は余裕を約 56 にする。敷地が未確認のため、今月は出さない。
  - 政策 RecreationalUse、SmallBusiness: 観光への効きが確かめられていない。今月は採らない。

### 保健環境局(health)(hooks の記録で 17:43〜17:52)

- 元のファイル: [m15-health.md](m15-health.md)
- 案 health-1: 満杯の埋立地 12880 を空にして、受け入れを戻す
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 4-4
  - 議決: 要らない

- 見たもの: [m15-health.md の「見たもの」](m15-health.md#見たもの)(15 行)
- 判断の根拠:

  健康の平均 89 は目標 80 以上を満たしている。汚染の印 27(目標 15 以下)とごみの印 8(目標 0)は未達。2267 の停止は汚染に効くが、満杯 0 の条件を満たさない。その条件の妨げは、満杯の 12880 で、空けるのは取り壊しも費用もない手である。案は1件にした。焼却場の移設、火葬場の追加、政策は、確かめた事実が足りないか、守る線に関わるので、案にしない。死体の印は原因が分からないので、調査で分ける。

- 捨てたもの:

  - 焼却場 2267 の停止(事業2): 満杯 0 を満たさない(12880 が 100%、収集車 0/19)。4月に再判定する。
  - 2267 を (3400,-520) へ移す: 入口の道路がない(entrance.road が null)。道路が約190m要る。下水の網が200m以内に見当たらず、未確認。
  - 東の死体の hotspot に火葬場を足す: `list_building_types`(service DeathCare / Deathcare)では火葬場の prefab 名が返らず、名前と費用が未確認。調査の結果を待つ。
  - 45892 の空けを止める(前の計画の案): 45892 は 46% で空け中。止める理由が数字にない。
  - 政策 Recycling(ごみ -15%、住宅税 -5%、週 0): ごみに効くが、住宅税の収入の減りを数字で確かめていない。守る線(+3,000)の余裕は 1,256 しかない。財政の判断に任せる。

### 教育委員会(education)(hooks の記録で 17:43〜17:48)

- 元のファイル: [m15-education.md](m15-education.md)
- 案 education-1: 小学校 15301 を1校止め、維持費を減らす
  - 建設費 0、週の維持費 +-160、戻せる
  - 市の計画: 2-3
  - 議決: 要らない

- 見たもの: [m15-education.md の「見たもの」](m15-education.md#見たもの)(10 行)
- 判断の根拠:

  - 小学校の定員は 14,268、子どもは 8,842 で、定員は子どもの1.61倍。13月・14月と同じく1.3倍を超えており、長期計画の「超えが続けば1校止める」条件に当たる。止めた後の定員は 13,920(子どもの1.57倍)で、1.3倍を保つ。案1を出す
  - 高校の定員は 24,360、10代は 19,442 で、余裕は 4,918。休止の条件(余裕1,000を切る)に当たらないので、高校は置かない
  - 止める学校は、近くに余裕のある小学校がある 15301 を選んだ。生徒 178 人は 15022、43936、25802 の余裕(合計 約 470)で吸収できる見込み。覆いの最小 63 の地点は確かめ直す
  - 案は1件にした。小学校は1校ずつ止める方針で、2校目は1か月置いて判断する

- 捨てたもの:

  - 小学校を2校同時に止める案: 長期計画の「1校ずつ」に反する。2校目は、1校目の結果を見てから判断する
  - 教育の予算を下げる案(`set_budget` で education): 議決が要り、すべての学校の運営に効く。定員の余りを狙うには粗すぎるため、出さない
  - 高校を1校増やす案: 余裕が 4,918 あり、休止の条件に当たらない
  - 政策 EducationBoost を外す案: 大卒の失業への効きを試している最中(finance の試し)で、教育の政策を外すと、その試しの判定が崩れる。出さない

### 消防局(fire)(hooks の記録で 17:43〜17:47)

- 元のファイル: [m15-fire.md](m15-fire.md)
- 案 fire-1: 貨物港 32211 の横に警察署を置く(再提出)
  - 建設費 12000、週の維持費 +480、戻せない
  - 市の計画: 3-4
  - 議決: 要らない

- 見たもの: [m15-fire.md の「見たもの」](m15-fire.md#見たもの)(20 行)
- 判断の根拠:

  - 3-4 の合計は今 4 で、目標ちょうどにある。火事は 1、犯罪は 3。犯罪のうち 32211 は警察の届きが 0 で、印が残る。ほかの 2 つの犯罪は、警察署 1 棟では届かない場所にあるため、この案の対象外とした
  - 案1 は、14月に採られなかった案の再提出。前提(守る線の余裕)は、今月の数字で直した。週の収支 +4,256 から 480 を引いても +3,776 で、守る線 +3,000 の上に残る。所持金も守る線 1,874,000 の上に残る
  - 候補地は (-575, 1095) の1つで、試しの道具が通り、電気・水・下水の確認も通った。ほかの2つの候補は試して不可だったので、使わない
  - 案を1件に絞った。火事は今月の印 1 で、焼け跡もなく、手を打つ理由がない。事業1と事業2は、条件が出た月に出す
  - 維持費の増えは 480 で、下降の規則に触れる恐れがあるため、費用と守る線の見込みを書いた

- 捨てたもの:

  - 犯罪の印 29104(240, -1248)の近くに警察署を置く案: 試しの道具で置けたが、取り壊し(Office 916、働き口27)が要り、入口の道もない。今月は、取り壊しの議決を求める理由がない
  - SmokeDetectors(政策): 週 57,702。守る線を大きく割るため、対象外
  - 政策による犯罪の抑え: 犯罪・警察に効く政策が一覧にない。対象外
  - 火事の追跡の調査(事業2): 同じ場所の火事が続いていない(火事の印は 1 で、場所も 1 棟)。今月は調査なし

### 財政局(finance)(hooks の記録で 17:43〜17:44)

- 元のファイル: [m15-finance.md](m15-finance.md)
- 案 finance-1: 医療の予算を 150 から 130 に下げる
  - 建設費 0、週の維持費 +-10200、戻せる
  - 市の計画: 財政の守る線(週の収支 +3,000)
  - 議決: 要る(予算)

- 見たもの: [m15-finance.md の「見たもの」](m15-finance.md#見たもの)(6 行)
- 判断の根拠:

  週の収支は +4,256 で守る線 +3,000 の上だが、余裕は 1,256 しかない。EducationBoost の判定値は、今の数字のままだと 2,428〜2,508 で満たさない。医療の予算は、支出 76,440 が最も大きく、容量に対する使用が 785 と小さい。予算を 20 点だけ下げると、約 10,200 の余裕が出る。これで判定値が満たされ、駅と名所の再開も、2267 の停止を待たずに進められる。1件に絞った理由は、予算の上限が1か月20点で、ほかの予算(警察、教育、ごみ)は目標に近く、減らすと 3-4、2-3、4-4 が崩れる恐れがあるため。

- 捨てたもの:

  - 医療の予算を 110 にする: 1か月20点の上限を超える。見回りの結果を見て、第17月に判断する
  - 警察の予算を 150 から 130: 支出が約 4,700 減るが、3-4 は火事1+犯罪3=4 で目標の上限ぎりぎり。減らすと犯罪が増えて未達になる恐れ
  - 教育の予算を 120 から 100: 支出が約 8,000 減るが、高校の定員が約 20,300 になり、10代 19,442 との差が約 850 まで縮む。2-3 が崩れる恐れ
  - ごみの予算を 150 から 130: 支出が約 2,500 減るが、ごみの印が 8(目標 0)で、4-4 を悪くする恐れ
  - 融資(BankA、BankB、BankC): 週の支払いが増えるため、守る線に逆らう。所持金は 2,433,116 で足りているため不要
  - 税を上げる: 住宅の需要が 21 あり、人口が6か月減っている。住宅税を上げると、需要が下がり人口の減りを強める恐れ。見直しは第18月に回す
  - 政策 Recycling: 住宅の税収が約 5% 減り(住宅の収入 264,785 の5%は約 13,200/週の見積もり)、週の収支を大きく下げる
  - 政策 FreeTransport: 運賃収入 5,227/週を失う。交通の効きは未確認で、バスは港湾空港局の担当
  - 政策 HeavyTrafficBan(費用0): 貨物の運搬が減り、品物がない店 267 を悪くする見立て(未確認)。8-1 の止まりは施設内の待ちで、道の混みではない
  - 2267 の停止(保健環境局の手): 財政の余裕は医療の予算で足りるため、財政の条件から外す。停止の判断は保健環境局

## 4. 差し戻しと再調査

- 差し戻しはなかった

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m15-bill.md](m15-bill.md)
- 採った m15-1: 放棄店跡に JapaneseGarden(元 urban-1、議決が要る(取り壊し))
- 採った m15-2: 交差点 (-1640,-1010) に信号(元 roads-1、議決は要らない)
- 採った m15-3: 満杯の埋立地 12880 を空にする(元 health-1、議決は要らない)
- 採った m15-4: 小学校 15301 を止める(元 education-1、議決は要らない)
- 採った m15-5: 貨物港横に警察署(元 fire-1、議決は要らない)
- 採った m15-6: 医療の予算を130に(元 finance-1、議決が要る(予算))

- 見たもの:

  - `city_info`、`economy`、`services`、`citizens_summary`、`complaints`: 各局の案が書いた値を読んだ(人口177,176、所持金2,433,116、週の収支 +4,256)
  - 8局の案 `council/m15-<局>.md` と、編成方針 `council/m15-policy.md`、長期計画 `council/plan-city.md`、市政ノート
  - `tool-reference.md`: bulldoze、place_building、set_traffic_lights、empty_building、set_building_active、set_budget の引数が局の実行計画と合うことを確かめた
  - 市長が街の道具を呼んだものはない(局が `test_place_building`、`preview_bulldoze`、`junction_info`、`buildings_near` で確かめた結果を使った)

- 判断の根拠:

  6件はすべて、実行計画に道具の名前と引数があり、必須条件の未確認が本文に残っていない。重点3(観光、物流、公園)のうち、公園(m15-1)だけが案になった。観光と物流は、economy と port が案なしで、市長は代案を作らない。そのため、観光の入口と名所は今月も進まない。この事実を市政ノートに残す。週の収支の余裕が 1,256 と小さい中で、医療の予算(m15-6)と小学校の休止(m15-4)で維持費を減らし、警察署(m15-5)と公園(m15-1)の増えを吸収する形にした。3回目の下降の数えが始まる前に、収支を上げる狙い。

- 捨てたもの:

  - 観光の名所と旅客の駅: economy と port が案なし。島Bの駅は整地(`level_terrain` の test)が未確認。名所 Transport Tower(島B)は水・下水の接続が未確認。局の役割として、17月に実行条件をそろえた案を求める
  - 分からないことの試し: 試しの案は m15-2(信号)の1件が出た。ほかの項目(観光の名所、島の橋、人口の減り)の試しの案は出なかった
  - 編成方針の重点の外のうち、焼却場 2267 の停止: 満杯0が条件。m15-3 の結果を待つ

## 6. 議会: 可決と否決(hooks の記録で 17:55〜17:55)

- 元のファイル: [m15-assembly.md](m15-assembly.md)
- m15-1 取り壊し: 可決。壊す2棟は働き口0・家0の放棄店で、失うものが0。他7か所と比べて選んでいる。
- m15-2 財政: 可決。建設費0で戻せる。守る線に響かない。
- m15-3 財政: 可決。費用0・維持費0。守る線に響かない。
- m15-4 財政: 可決。維持費を減らす施策。定員は子ども以上を保つ。
- m15-5 財政: 可決。建設費12,000、維持費+480。見込みの収支は+3,700台以上で守る線の上。
- m15-6 予算: 可決。変更20点で上限内。容量に余裕があり健康は目標の上。戻せる。
- 可決した種類(hooks が見る): 取り壊し、予算

- 見たもの:

  - `city_info`: 所持金 2,433,116、週の収入 339,306、支出 335,050
  - `economy`: healthcare 昼150・夜150
  - `council/m15-bill.md`、`council/m15-finance.md`: 費用と実行計画

- 判断の根拠:

  費用は案とスクリプトの値が一致した。医療の削減が効かなくても、収支は +3,736 で線 +3,000 の上、所持金も線の上にある。取り壊しは失うものが0で、代わりの手との比べがある。

- 捨てたもの:

  - m15-5(警察署): 維持費が増えるが、同じ月の減らす施策で相殺され、線を破らないため可決

## 7. 実行する市長: 実行と見回り(hooks の記録で 17:56〜18:04)

- 実行してよい施策: m15-1、m15-2、m15-3、m15-4、m15-5、m15-6
- 実行した: m15-1、m15-2、m15-3、m15-4、m15-5、m15-6
- 失敗した: なし
- 臨時: なし
- 見回り 2051-03-17: 人口 177145、所持金 2437243、週の収支 12784、幸福度 88
- 見回り 2051-03-27: 人口 176872、所持金 2455370、週の収支 12913、幸福度 88
- 報告:

  6件すべて議案どおりに実行した。取り壊し(m15-1)と予算(m15-6)は advance の前に打ち、hooks に止められた手はない。m15-1 は放棄店2棟(働き口0・家0)を壊し、JapaneseGarden(id 3801)を置いた。Beautification は月末に 90 棟になった。m15-2 は (-1640,-1010) に信号を付けた。blocked は基準26から月末9に下がったが、判定は16月末。m15-3 は埋立地12880を空け始め、月末は95%でまだ途中。戻す操作は次月以降。m15-4 は小学校15301を止め、定員は 13,920 になった。m15-5 は警察署(id 34351)を置いた。m15-6 は医療の予算を 130 にし、HealthCare の支出は 76,440 から 66,248 に減った。月末の週の収支は +12,150(月初 +4,256)。人口は 176,528 で、7か月連続の減少。観光客は 1,937、Tourism は週59。見回りでは境目に当たらず、臨時は行っていない。調査3件は council/m15-survey-*.md に3回分を記録した。観光の入口と名所は、案がなく今月も進まなかった。市政ノート: /Users/takeshita/orca/workspaces/tried/issue-124/2026/10-27-AI市役所で福岡を観光都市にする-03-観光の街を目指す計画と局を決める/mayor-note.md

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m15、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 17:41〜18:14(hooks の記録の時刻から)、道具の行 277
- 議会が可決した種類: 予算、取り壊し
- 議決が要る道具の呼び出し: 2 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 609 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m15-economy-map-east.jpg`
- `m15-economy-map-southwest.jpg`
- `m15-zonemap-urban.jpg`

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
