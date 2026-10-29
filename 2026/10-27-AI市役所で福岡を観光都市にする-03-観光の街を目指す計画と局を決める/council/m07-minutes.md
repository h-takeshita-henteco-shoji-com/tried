# 7か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 15:01〜15:02)

- 元のファイル: [m07-policy.md](m07-policy.md)
- ゲーム内の日付: 2050-06-30、保存: fukuoka-plan-m07
- 重点: 5-1・5-2 観光、8-1 物流・人流のゲートウェイ、6-4・7-1 企業の立地、地場企業

- 見たもの: [m07-policy.md の「見たもの」](m07-policy.md#見たもの)(18 行)
- 判断の根拠:

  公約は、人口が7か月で初めて増え、健康と火事・犯罪が目標に届いた。観光は人数と収入とも目標から遠く、入口が0のままなので、毎月の重点に置く。残りの2つは、目標の2倍超で動かない 8-1 と、255まで増えた品物がない店(6-4)を選んだ。島Bと空き地3は準備が進んだので、名所と電気の案を局に求める。

- 捨てたもの:

  - 6-3 交通(流れ54%): 東の幹線の4車線化で blocked が増えた(m06-2)。重点にせず、局が出した案の中から選ぶ
  - 4-2 公園(82棟)、4-3 汚染(23)、4-4 ごみ(8): 数字は前月より良い方向。重点の外で案が出れば採る
  - 1-2 健康(89)、3-4 火事と犯罪(合わせて4): 目標を達成。保つ
  - 6-1 事務所のレベル3(3,260): 目標3,500に遠いが、6-4 の働き口と同じ方向なので、そちらで見る

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

### 住宅都市みどり局(urban)(hooks の記録で 15:04〜15:06)

- 元のファイル: [m07-urban.md](m07-urban.md)
- 案 urban-1: 風力の網の空きに公園を1か所置く(588,1232)
  - 建設費 1000、週の維持費 +8、戻せる
  - 市の計画: 4-2
  - 議決: 要らない

- 見たもの: [m07-urban.md の「見たもの」](m07-urban.md#見たもの)(19 行)
- 判断の根拠:

  - 4-2 は、82 から 100 まで 18 棟足りない。電気の届く網の空きに1棟ずつ置くのが、確かめられた手で、計画の第7月の予定(同じ網に1か所)と一致する。公園 100 は 6/30 も電気 1 だった
  - (588,1232) は、6か所を試して、道と風力を避けて通った唯一の候補。入口から道までは 15.2m で、道具の基準の内に入る
  - 4-1 は、この月に効きを確かめる手がない。公園の地価への効きは、いまの数字では測れない。そこで、調査で基準(平均 2)を取り、置いた後に同じ道具で測る。HighTechHousing は週の収支が割れるため選ばない
  - 案は1件。同じ網の公園を増やすだけで、件数を埋めない

- 捨てたもの:

  - 4-1 の地価を上げる手(公園の地価効果を前提にした高密度住宅の近くの公園): 効きを確かめる道具がなく、場所も電気の網の中に見当たらない。第8月に調査の結果で出し直す
  - HighTechHousing(4-1 の候補): 週 20,232 の維持費で、週の収支が守る線(+3,000)を大きく割る
  - (625,1258)、(680,1280)、(560,1250)、(600,1232)、(540,1222)、(588,1240)、(652,1382): 上の試しで、道・風力・公園の歩道と衝突し置けない
  - 入口から道へ短く伸ばす案(588,1264→1289): 道の交差点に衝突し、引けない
  - 公園を2か所以上(同じ月): 電気の網の空きが確かめられていない。事業2の「月1か所」に従う

### 道路下水道局(roads)(hooks の記録で 15:03〜15:06)

- 元のファイル: [m07-roads.md](m07-roads.md)
- 案 roads-1: 東の出口側 z=-318 の Basic Road 3区間を4車線にする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 北東 z=560 の Basic Road 2区間を4車線にする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m07-roads.md の「見たもの」](m07-roads.md#見たもの)(26 行)
- 判断の根拠:

  - 6-3 の交通の流れは 54%(目標 60%)。残った blocked は東の出口(60)と北東(41)に多い。どちらも道の差し替えだけで、建設費と維持費の差は 0。試しの道具が両方とも通ったので、2案を出す。
  - 6月の東の4車線化は、判定の条件(2か月続けて増える)に当たらない。戻さず、今回の案1は測る範囲を分けて読む。
  - 案の数は2件。交差点の信号は、この周りに候補がない。埋立地が道を挟む区間は、取り壊しを伴うので、今月の案に入れない。
  - 名所 11580 の電気は、今回の試しでも、建物の敷地に届く線の端が決まらなかった。案にできないので、捨てたものに書く。
  - 政策は HeavyTrafficBan(トラックの通行を止める政策、費用0)を比べた。担当の問題に効きうるが、トラックが品物を運ぶため、品物がない店 255(6-4 の目標 120 以下)を悪くする見込みで、今月は出さない。

- 捨てたもの:

  - 政策 HeavyTrafficBan(費用0): 交通の流れに効きうるが、トラックが止まる(品物がない店 255、6-4 の目標 120 以下)。品物の流れを悪くするおそれがあるので、出さない。
  - 北東の幹線 z=560 の全区間の4車線化(x 2152〜2594): 埋立地 45436 と 3565 がぶつかり、差し替えられない。埋立地の取り壊しは、議決の案と、ごみの数(4-4)への影響を見てから。
  - 交差点の信号(東の出口、北東): 近くに交差点がなく、信号の候補地がない。
  - 名所 11580 の電気の支線: 試しの端点が、建物と重なって断られた(ObjectCollision)。敷地に入る端の位置が決まらない。9月までに、敷地の縁を探して試し直す(計画の事業2)。

### 港湾空港局(port)(hooks の記録で 15:03〜15:08)

- 元のファイル: [m07-port.md](m07-port.md)
- 案: なし

- 見たもの: [m07-port.md の「見たもの」](m07-port.md#見たもの)(19 行)
- 判断の根拠:

  - 旅客の入口(5-1、5-2)は0のまま。今月の入口の案は、島Bの岸がすべて落ち、貨物センター周りの駅は道が工場にぶつかるため、実行条件を満たせない。確認できた事実は、島Bの Harbor の位置、駅の候補 1点だけで、どちらも接続が未確認。
  - 8-1 の 28755 の止まりは、550台が敷地の中で空き待ちのまま。7日以上止まった車が369台あり、対象の行き先(距離 925〜5,658)への戻りも止まっている。原因が敷地の道か積み降ろし場所かを、まだ確かめられていない。したがって、道の差し替えの案は、原因が分かるまで出せない。
  - 案なしにする。島Bの Harbor は11点で試し、すべて落ちた。旅客の駅は、置ける点がある一方で、入口の道と旅客線の接続が未確認のまま。確認できない手を案にすると、実行の市長が必須条件を満たせない。
  - 調査は1件出す。28755 の止まりは、時間の経過で変わるかどうかで次の手が変わるため、見回り2回と月末で見る。

- 捨てたもの:

  - 島Bの Harbor(旅客の港、建設費 80,000、週 1,600): 11点すべて落ちた(HeightTooHigh、ObjectCollision、CannotConnect、SlopeTooSteep)。岸の高さが海面と合わず、橋と道路のそばに置く場所がない。8月に試し直す案を残すが、今月は出さない。
  - 旅客の駅(2600,-1400)の案: 試しは ok だが、入口の道が工場2棟にぶつかり、旅客線の外向きの接続も未確認。実行可能にできない。8月に、道の経路を工場を避けて組み直す。
  - Airport(建設費 150,000、週 4,800): 守る線の余裕を割るため、試さない。
  - 28755 の道の差し替え(8-1): 原因が未確認で、道の差し替えは道路下水道局の仕事。調査の結果が出てから検討する。
  - 政策の変更(SmallBusiness、RecreationalUse など): 港湾空港局の数字(入口、28755)に効く根拠がない。前月に観光の政策の効きは切り分けられなかった。今月は手を出さない。

### 経済観光文化局(economy)(hooks の記録で 15:04〜15:13)

- 元のファイル: [m07-economy.md](m07-economy.md)
- 案 economy-1: 電気の来ない名所 11580(空き地3)を取り壊す
  - 建設費 0、週の維持費 +-400、戻せない
  - 市の計画: 5-1、5-2
  - 議決: 要る(取り壊し)

- 見たもの: [m07-economy.md の「見たもの」](m07-economy.md#見たもの)(33 行)
- 判断の根拠:

  - 再調査の条件1 は、島Bで 11580 を壊さずに名所を置けるかだった。(-4640,1520) は道路と重なり、どの種類も置けない。島Bの別の場所の Observatory は ok だが、水と下水の網が島にないため、実行できない。Servicing Services と Transport Tower は入口の道がなく、道を引く案は今月の範囲外。条件1 は満たせなかった。
  - 再調査の条件2 は、残す場合の支線と維持費の比べ。支線は敷地の外までは通るが、敷地の中へは断られた。電気が届く線は確かめられていない。維持費の差は週 400 で、収支の +10,489 に対して小さい。
  - 取り壊しの効きは、週 400 の減りと、名所 1 棟の減り(9 → 8)だけで、観光客の増えは確かめられていない。島Bの置き直しが道具で確かめられない以上、取り壊しは採る根拠がなく、実行可否は「未確認」にする。市長が採っても、島Bの確かめを先にする条件を守る。
  - 案は1件だけにする。島Bの Observatory は水の網がなく、今回の条件の外で、今月の案にしない。

- 捨てたもの:

  - economy-1 の「島B で (-4640,1520) に別の名所を置く」: 道路と重なり、どの種類も断られる。ほかの位置を探すことは、条件の外のため今月はしない
  - 島Bの Observatory(-4640,1585、南向き): ok だが、水と下水の網が島にない。水の管を海の向こうへ引く案は、道具で確かめられていない。次の月に出すなら、水の網の接続を先に確かめる
  - 島Bの Servicing Services(-4700,1650)、Transport Tower(-4680,1565): ok だが、入口の道がなく、道を引く案は条件の外
  - 残す案(11580 に電気を通す支線): 敷地の中へ端を入れる線が断られ、電気が届くかは確かめられていない
  - 名所の種類の同一の重なり(StatueOfWealth の島B 置き直し): AlreadyExists が取り壊しを仮定しても出るため、道具では確かめられない

### 保健環境局(health)(hooks の記録で 15:03〜15:07)

- 元のファイル: [m07-health.md](m07-health.md)
- 案: なし

- 見たもの: [m07-health.md の「見たもの」](m07-health.md#見たもの)(14 行)
- 判断の根拠:

  - 健康は目標の80を超え、体調の悪い市民は 1,644。SmokingBan は 6月から有効で、今月は見るだけにする。
  - 汚染の印は 23(目標15以下)、ごみの印は 8(目標0)。ごみは満杯の埋立地がなく、焼却場の貯蔵は 40〜58%。
  - 汚染の印の位置は、2267 の周りより 10351 の周りに多い(11棟対2棟)。計画の「2267を止める」は、事実と合わない。停止先は9月に決める。
  - 3基目の焼却場は、道が通る候補がない。取り壊しの議決が要るので、今月は案にできない。8月に取り壊しの案を出せるよう、候補地の壊す対象を調べた。
  - 案を出さないので、件数は0。

- 捨てたもの:

  - 政策 Recycling(住宅税 -5%、週 約 -13,470): 週の収支が +10,489 から約 -3,000 になり、守る線(+3,000)を割る。出さない。
  - 3基目の焼却場を (3900,-1100) に置く案: 住宅2棟の取り壊しが要るため、今月は出さない。8月に取り壊しの案として出す。
  - 2267 を今月止める案: 3基目がないと、ごみの印が 2月の 11 → 22 と同じく増えるおそれがある。3基目の後に行う。
  - 埋立地の増設: 満杯の埋立地がなく、貯蔵も 40〜58% なので、今は要らない。

### 教育委員会(education)(hooks の記録で 15:04〜15:04)

- 元のファイル: [m07-education.md](m07-education.md)
- 案: なし

- 見たもの:

  - `services`: 小学校の定員 14,268、高校の定員 24,360、大学の定員 36,540。電気・水・下水・ごみ・墓地は満杯なし、警察の犯罪率 5
  - `citizens_summary`: 子ども 10,319、10代 21,927、若者 32,513。大人の失業 5,596(大卒 5,508)。健康の平均 89。来ない市民 0/0/0
  - `city_info`: 人口 179,174、所持金 2,101,000、週の収支 +10,489(収入 346,067、支出 335,578)、観光客 1,665、dialog なし
  - `list_policies`: policyExpensesPerWeek 10,600。SmokingBan は active で 0。EducationBoost は active で 7,940(学校の維持費の25%。政策の欄ではなく教育の支出に出る)。RecreationalUse は inactive で 0。SmallBusiness は inactive で 313。BigBusiness は active で 3,812

- 判断の根拠:

  - 長期計画の前提は当たった。余裕は 1,000 を大きく超え、計画の「今月の予定」(余裕の推移を見る、1,000 を切るまで置かない)のとおり、置かない。計画は直さない
  - 2-3 の目標(小学校と高校の定員が、子ども・10代以上を保つ)は満たしている。担当の問題が、まだ無い
  - 大学の定員 36,540 は、若者 32,513 を上回る。大卒の失業 5,508 は、市政ノートで働き口の不足と見られている。大学を足しても、失業は減らない。働き口は経済観光文化局の担当
  - 前の月(m06)の教育委員会は案なし。答え合わせの対象はない
  - 案の数は0。件数を埋めるための案は作らない
  ### 前の月の答え合わせ
  なし(前の月に案なし)

- 捨てたもの:

  - 高校1校を置く(建設費 24,000、週の維持費 +560): 余裕 2,433 は基準 1,000 より大きい。置くと、10代が減る中で定員だけが増え、維持費が増える。計画の休止の条件(余裕 2,000 以上で休止)にも合う状態のため、再開しない
  - 小学校1校を置く(建設費 10,000、週の維持費 +160): 余裕 3,949 で、置く理由がない
  - 大学の追加: 大学の定員が若者を上回り、2-3 の数にも入らない。大卒の失業は働き口の不足が原因と見込む(教育では直らない)
  - 政策 EducationBoost を外す(週 7,940 の節約): 2-3 の数(定員と年齢層)に効かないと見込むが、確かめていない。学歴の効きを担当の外で動かすことになり、財政の守る線は今も十分(週の収支 +10,489)のため、節約の必要はない。財政局が判断する事項

### 消防局(fire)(hooks の記録で 15:03〜15:04)

- 元のファイル: [m07-fire.md](m07-fire.md)
- 案: なし

- 見たもの: [m07-fire.md の「見たもの」](m07-fire.md#見たもの)(10 行)
- 判断の根拠:

  - 前の月の答え合わせ(6月末の取り壊し m06-6): 予想は火事の印 6→0。結果は 3 で、部分的に当たり。残る3は焼け跡ではなく、稼働中の事務所2棟だった。火事と犯罪の合計は 8→4 で目標に届いた。次の扱い: 焼け跡の取り壊しは、焼け跡が出たときの手として残す
  - 今月の判断: 合計4で目標に届いた。残る火事の原因は、焼け跡ではなく火元の側かもしれないが、1か月目の印では確かめられない。2か月続けば火元の側の手に切り替える、という事業2の条件を、そのまま使う
  - 手を出さない理由: 煙探知機は週の費用が守る線を超える。消防署を足す案は、届き 118 と消防車 2/8 台から、効きが小さい
  - 案の数: 0件。調査を1件出す

- 捨てたもの:

  - 煙探知機(SmokeDetectors、街全体): 週 57,636 で、守る線(週の収支 +3,000)を超える。政策の変更も月1件まで。不採用
  - 地区の煙探知機(事務所の周りに地区をかけて試す): 地区の政策の費用を道具で確かめられない(list_policies は街全体の費用だけを返す)。今月は確かめる手がなく、8月に火事が続いたときに、費用を道具で確かめてから出す
  - 消防署を足す(事務所の周り、Fire House 12,000 / 週 560): 届き 118 と消防車 2/8 台から、効きは小さいと見る。火事が続いても、まず火元の手を先に調べる
  - 小学校 47076 の犯罪の印 1: 目標の内(犯罪2以下)で、警察署 45584 の事業1で見る。今月は動かさない

### 財政局(finance)(hooks の記録で 15:03〜15:04)

- 元のファイル: [m07-finance.md](m07-finance.md)
- 案 finance-1: 政策 EducationBoost を外す(試し)
  - 建設費 0、週の維持費 +-7940、戻せる
  - 市の計画: 6-1、6-4・7-1、5-1・5-2
  - 議決: 要らない

- 見たもの: [m07-finance.md の「見たもの」](m07-finance.md#見たもの)(10 行)
- 判断の根拠:

  - 守る線: 週の収支 +10,489 は守る線 +3,000 を 7,489 上回る。所持金 2,101,000 は守る線 1,874,000 を 227,000 上回る。今月は、守る線を割る手を出さない
  - 観光: 局の手は、名所と入口を置く手ではない。局の手は、観光の事業が入る維持費の余地を残すこと。EducationBoost の 7,940 は、その余地として最も大きく、政策の変更1件で足りる。案1 を出す
  - 6-1 と 6-4・7-1: 大卒の失業 5,508 と事務所レベル3 3,260 が目標に届かない。上げる手は、事務所の税(下の捨てたもの)か、教育の上乗せの見直し。教育の上乗せを試す案1 を選ぶ(税より損が小さく、戻せる)
  - 道路の予算は保留。流れ 54 は目標 60 より低く、予算を下げると 6-3 と 8-1 の止まりに効きうる
  - 案は1件。件数を埋めるための案は作らない

- 捨てたもの:

  - 道路の予算を 120 から 100 に戻す: 市の交通の流れが 54 で、6-3 の目標 60 に逆行する。維持費の減りは 1,483 で小さい。保留にした(`plan-finance.md`)
  - 事務所の税 3 を 2 に下げる: 1点で約 -8,250 の見積もり(事務所の収入 24,741 を3点で割った値)。守る線の余裕 7,489 を超え、守る線を割る
  - 教育の予算を 120 から 100 に下げる: 週 約 -8,000 の見積もり。ただし EducationBoost の試しと、教育の効きが重なり、切り分けられない。試しの案1 を先にする
  - 融資: 所持金 2,101,000 で要らない。利息が増えるだけ
  - 商業(低)の税 9 を 8 に下げる: 観光の収入は週 53 で、税の効きは小さい見込み。1月に不採用とした手で、理由が増えていない

## 4. 差し戻しと再調査

- 経済観光文化局: economy-1(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m07-bill.md](m07-bill.md)
- 採った m07-1: 風力の網の空きに公園を1か所(588,1232)(元 urban-1、議決は要らない)
- 採った m07-2: 東の出口 z=-318 の3区間を4車線に(元 roads-1、議決は要らない)
- 採った m07-3: 北東 z=560 の2区間を4車線に(元 roads-2、議決は要らない)
- 採った m07-4: 政策 EducationBoost を外す(試し)(元 finance-1、議決は要らない)
- 採らなかった economy-1: 名所が9から8に下がり、取り壊し後に島Bへ置けるかが未確認(取り壊しを仮定した試しも AlreadyExists)で、戻せない。

- 見たもの:

  - `council/m07-urban.md`、`m07-roads.md`、`m07-economy.md`、`m07-finance.md`、`m07-port.md`、`m07-health.md`、`m07-fire.md`、`m07-policy.md`: 各局の案と編成方針。ゲームの道具は呼んでいない(月例の前半が止めた状態の数字を使う)
  - `council/plan-economy.md`、`plan-city.md`、`ledger-recent.jsonl`: 長期計画と、前の月までの案の行方
  - `mayor-note.md`: 7か月目の数字(人口 179,174、所持金 2,101,000、週の収支 +10,489、観光客 1,665)

- 判断の根拠:

  守る線は、週の収支 +10,489 に対して +3,000 まで余裕 7,489、所持金は 227,000 の余裕がある。今月の4件は建設費の合計が 1,000、週の維持費の増えは約 -7,930 で、守る線を破らない。観光の重点では、名所を壊す案を採らず(実行後の置き直しが未確認)、観光の入口は港湾空港局が案なしのまま。これは最大の穴として記録し、8月に局の再調査を求める。交通は、測る場所を約 3.5km 離した2つの試しにして結果を分ける。

- 捨てたもの:

  - economy-1(11580 の取り壊し): 名所を減らす手で、得るものが週 400 と未確認の置き直しだけ。条件付きで再調査を求める
  - 調査 fire: 上限3件。目標に届いているため
  - 6-4・7-1 の重点: 局の案が出なかった(economy は6-1 と働き口を見送り中)。finance-1 の間接の効きに任せる
  - 8-1 の道の差し替え: 原因が未確認。調査 s07-1 の結果が出てから

## 6. 議会: 可決と否決(hooks の記録で 15:14〜15:14)

- 元のファイル: [m07-assembly.md](m07-assembly.md)
- m07-1 財政: 可決。建設費1,000、維持費+8で守る線に収まる。
- m07-2 財政: 可決。費用0で守る線に影響しない。
- m07-3 財政: 可決。費用0で守る線に影響しない。
- m07-4 財政: 可決。維持費が約7,940減り、政策の変更は月1件の上限内。
- 可決した種類(hooks が見る): なし

- 見たもの:

  - `city_info`: 所持金 2,101,000、週の収入 346,067、支出 335,578
  - `economy`: 税率と予算の現状(今月は税・予算の議案なし)
  - `council/m07-bill.md`: 4件の施策と費用

- 判断の根拠:

  今月は議決の要る議案がなく、点5だけで確かめた。建設費の合計は 1,000、維持費は減るので、守る線(週の収支 +3,000、所持金 1,874,000)を大きく上回る。政策の変更は1件で、上限内である。

- 捨てたもの:

  - m07-4: 教育の質が下がるおそれがあるが、点5の対象外であり、定員に余裕があり戻せる。可決とした。

## 7. 実行する市長: 実行と見回り(hooks の記録で 15:14〜15:20)

- 実行してよい施策: m07-1、m07-2、m07-3、m07-4
- 実行した: m07-1、m07-2、m07-3、m07-4
- 失敗した: なし
- 臨時: なし
- 見回り 2050-07-10: 人口 179508、所持金 2127433、週の収支 19012、幸福度 88
- 見回り 2050-07-20: 人口 179856、所持金 2151284、週の収支 16406、幸福度 88
- 報告:

  議案の4件は全部打てた。m07-1 は Regular Park 32260 を(588,1232)に置き、電気・水・下水が来た(費用1,000)。m07-2 は z=-318 の3区間、m07-3 は z=560 の2区間を4車線にした(どちらも費用0)。m07-4 は EducationBoost を外した。月末(7/30)は人口180,138、所持金2,174,932、週の収支+16,355、観光客1,744(Tourism 週32)。見回りは境目に当たらず、臨時なし。hooks に止められた手もなし。月末の計測は、m07-2 の blocked が60→17に減り、m07-3 は41→47に増えた。m07-4 は Education 支出が48,120→38,592に下がったが、大卒の失業は5,508→5,954に増えた。事務所レベル3は3,260→3,262で、判定は8月。貨物センター28755の止まった車は645台で、周辺の道路の blocked は0。調査 s07-1〜s07-3 は council/m07-survey-port.md、m07-survey-health.md、m07-survey-urban.md に記録した。月末の s07-1 では cargo を呼んでいない(見回り2の値が最新)。市政ノートは mayor-note.md に追記済み。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m07、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 15:00〜15:30(hooks の記録の時刻から)、道具の行 369
- 議会が可決した種類: なし
- 議決が要る道具の呼び出し: 0 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 596 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m07-port-islandB-map.jpg`

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
