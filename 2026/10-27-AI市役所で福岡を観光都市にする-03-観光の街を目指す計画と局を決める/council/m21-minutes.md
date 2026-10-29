# 21か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 19:38〜19:39)

- 元のファイル: [m21-policy.md](m21-policy.md)
- ゲーム内の日付: 2051-09-03、保存: fukuoka-plan-m21
- 重点: 5-1・5-2 観光(入口、島・空き地の名所)、8-1 物流・人流のゲートウェイ(6-4 と合わせる)、4-2 花や緑による潤い

- 見たもの: [m21-policy.md の「見たもの」](m21-policy.md#見たもの)(16 行)
- 判断の根拠:

  公約4の観光が前月より減り、入口は21か月0のため、観光を第1の重点にする。計画の目標から最も遠いのは 8-1(止まったトラック605、目標250以下)で、6-4 の品物がない店205とつながるため第2にする。第3は、あと5で目標に届く 4-2 公園とする。公約1(人口)は12か月連続で減っており原因が分からないため、局の調査と試しで確かめる。守る線は、週の収支+8,868、所持金2,616,061で、どちらも上にある。

- 捨てたもの:

  - 6-3 交通: m20 で3件とも当たり、街全体の流れは55%。重点から外すが、局が同じ型の案を出すのは歓迎する
  - 4-3 汚染(印25): 焼却場の停止や木で3度効かず、出どころが分からない。案が出れば試しとして扱う
  - 4-4 ごみ(印9): 満杯は3565の1つに減った。道のない埋立地の案は局に任せる
  - 6-1 事務所L3、4-1 地価、1-2 健康: 目標に近いか達成済みで、今月は動かさない

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

### 住宅都市みどり局(urban)(hooks の記録で 19:40〜19:43)

- 元のファイル: [m21-urban.md](m21-urban.md)
- 案 urban-1: 放棄店24928の跡に公園を1つ置く(4-2)
  - 建設費 2500、週の維持費 +40、戻せない
  - 市の計画: 4-2
  - 議決: 要る(取り壊し)

- 見たもの: [m21-urban.md の「見たもの」](m21-urban.md#見たもの)(23 行)
- 判断の根拠:

  - 担当の数字は、4-2 Beautification が 95(目標100)、4-1 住宅(高密度)の地価が 59(目標62)。4-2 は残り5で、公園の型が確かめられている。4-1 は公園で +1 しか出なかったため、原因を調べる
  - 案1 は、(2160,-318) で道、電気、水、下水が確認でき、取り壊しで働き口や家を失わないので、採る。今月の予定は、22月の1か所を前倒しした形になる
  - 4-1 の原因は、調査 s21-1 で汚染・騒音・葬祭を見る。20月の調査は結果がないため、同じ問いを21月に出し直す
  - 案の数は1件。ほかの候補は、取り壊しで働き口か家を失うか、活動中の建物と重なるため、実行条件を満たさない

- 捨てたもの:

  - (1928,854) facing west、放棄の 10797 と 18349 を取り壊す案: 活動中の 43328(働き口5)も重なる。放棄された建物だけでは置けないため、今月は出さない
  - (1856,262) facing east、放棄の 34259 を取り壊す案: 活動中の 15951(働き口10)が重なる。放棄された建物だけでは置けないため、出さない
  - (2160,-612) facing east、放棄の 31154 を取り壊す案: 家26を失う建物(10866、23504)が重なり、働き口も16を失う。出さない
  - (2172,-78) facing east、放棄の 7475 を取り壊す案: 活動中の 1787(働き口8)が重なる。出さない
  - (2160,306) facing east、放棄の 21845 を取り壊す案: 活動中の 3442(働き口11)と 17474(家2)が重なる。出さない
  - 政策 Recycling(住宅税 -5%、ごみ -15%): 地価を直接動かさず、週の収支を約 -13,000 下げる見込み(計算値)で、守る線に近づく。採らない
  - 公園の型を Regular Park(1,000、週8)に替える案: 4-2 の数は同じく1つ増えるが、型による地価の差は未確認。今月は、確かめた JapaneseGarden のまま進める

### 道路下水道局(roads)(hooks の記録で 19:40〜19:41)

- 元のファイル: [m21-roads.md](m21-roads.md)
- 案 roads-1: 交差点 (2668,330) に信号を付ける
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 止まりの多い x=-1640 の南北道 3区間を Small 4 Lane にする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m21-roads.md の「見たもの」](m21-roads.md#見たもの)(22 行)
- 判断の根拠:

  - 20月の2か所の測りは当たり(26、8)で、長期計画の事業1の型(信号と車線)は効いている。21月は、止まりの上位が 37〜38 台の3か所に移った。そこで、計画の「1つずつ」を21月だけ2つに直した(計画の変更に理由を書いた)
  - 案1は、止まりの上位 (2689,302) の交差点に信号を付ける。費用 0、道具で canEnableLights を確かめた。信号の効きは交差点ごとに違うため、効き目は試しとして扱い、2回の測りで戻す条件を付けた
  - 案2は、(-1725,-1042) の東側の南北道を4車線にする。test_upgrade_road で matched 3、cost 0 を確かめた。z=-1010 の東西道は ObjectCollision で断られたため、予備にしない
  - (4100,-244) は交差点ではなく、Small 4 Lane の途中で止まる。原因が分からないため、案にせず、調査 1件で原因を見る
  - 案は2件にした。3件目は、信号か車線を同じ型で増やすことになり、件数を埋めるための案になるため出さない。(-916,-891)、(2341,-946) は、22〜24月の上位から1か所ずつ取る

- 捨てたもの:

  - 政策 HeavyTrafficBan(大型車を止める。0円): 街の流れを上げうるが、貨物の大型トラックも止まる。品物がない店205(6-4)と駅・港の止まり(8-1)に逆らうため採らない。政策の変更は港湾空港局と一緒に決める
  - 政策 FreeTransport: m16〜m17 で試し、効かなかったため外した。再提出しない
  - (4100,-244) への信号・車線の案: 交差点ではなく、途中の詰まりのため、原因が分かるまで案にしない(調査で見る)
  - z=-1010 の Basic 31370 の4車線化: test で 5219 にぶつかり断られた。31370 と 35109 だけを太くすると片側だけになるため、やめる
  - (-916,-891) 29台、(2341,-946) 28台、(-1637,-1473) 28台: 上位の候補として残す。22〜24月に、1か所ずつ取る
  - 駅・港の敷地の中の止まり(貨物センター 28755 の 604台): 8-1 は港湾空港局の担当。道の幅で止まりが減るかは未確認のため、局の案にしない
  - 旅客の入口の道と電線(事業3): 旅客の駅がまだ置かれていないため、今月は引かない(第24月末までに駅が置かれなければ、引かない)

### 港湾空港局(port)(hooks の記録で 19:40〜19:43)

- 元のファイル: [m21-port.md](m21-port.md)
- 案 port-1: 8-1: 休止中の貨物センター 40031 を動かし、28755 の止まりを減らす(試し)
  - 建設費 0、週の維持費 +1440、戻せる
  - 市の計画: 8-1
  - 議決: 要らない

- 見たもの: [m21-port.md の「見たもの」](m21-port.md#見たもの)(20 行)
- 判断の根拠:

  - 8-1 の数字は 605(目標 250 以下)で、ほかの局の担当に比べて目標から一番遠い。28755 の 604 台は、空き待ちでその場に止まっており、出先が 2,800〜6,000 m 先の店である。近くに供給先を増やすか、近くから出す手が効くとみる
  - 40031 は TurnedOff で、道と電気・水・下水がつながっていた。`set_building_active` の1操作で動かせ、費用は週 1,440 だけで、建設費はない。試しとして、確かめた形で出せる
  - 入口(5-1、5-2)は、今月も 0 のまま。候補を試したが、島B の駅は道の坂が残り、空き地側の駅は道がつながらず(坂 17〜29%)、海岸の港は高さと既存の港で断られた。道具で実行条件が確かめられなかったため、入口の案は出さない。整地の試し(`level_terrain`)は、この局の道具にないため、市長の決定を求める
  - 路線28(m20 の案)は、台数 171、乗客 110、流れ 55% で効いている。予算は 180% のまま、次の判断は第22月とする
  - 案は1件とした。ほかに実行できる確認済みの手がないため、件数を埋めない
  - 守る線は、週の収支 +8,868(+3,000 以上)と所持金 2,616,061(1,874,000 以上)。案1 の週 1,440 で、どちらも守れる

- 捨てたもの:

  - 旅客の駅(空き地側、3330,-1720 と 3322,-1640): 置けるが、道の坂が 12〜29%で、道路が引けない。整地なしでは実行できない。整地の試しは、この局の道具にないため未確認。市長の決定を求める
  - 島Bの旅客の駅(-4700,1600): 置けて入口(-4700,1576)も取れるが、道の坂が残り、道路が引けない。案を出すなら整地が要る。未確認のため見送る
  - 旅客の港(海岸、(-560,1200)、(-820,1080)、(-400,1400)、(-640,1020)): 高さか、既存の港や道と重なるため置けない。見送る
  - 旅客の駅 (3600,-1790): 線路と重なり、置けない
  - 大道路の拡張(x=3495): 貨物センターとぶつかり、道具が断る。見送る
  - 路線28 の予算をさらに下げる: 第21月は効きを測る月。第22月に判断する
  - 40031 以外の貨物センターの追加: 建設費と空き地の確認が要り、今月の確認範囲では実行条件が揃わない
  - 3つ目の案(交通、道の止まりの手): 重点の外で、確かめた実行条件が揃わない。ただし `traffic` の blockedSpots は、局が次の月に見る候補として残す

### 経済観光文化局(economy)(hooks の記録で 19:40〜19:43)

- 元のファイル: [m21-economy.md](m21-economy.md)
- 案: なし

- 見たもの: [m21-economy.md の「見たもの」](m21-economy.md#見たもの)(18 行)
- 判断の根拠:

  - 観光の数字は、前の月から大きく動いていない(観光客 1,784→1,810→1,837、訪問 151→148→164)。名所が増えれば、訪問と Tourism が増えると予想するが、今の街で効く量は見積もれない。
  - 名所を置くには、道路の入口、電気、水、下水が要る。候補を、中心、南西、島B、空き地3、東の住宅地で確かめたが、どれも今月の条件を満たす場所を確認できなかった。
  - 東の住宅地の空きは、道を引くと建物の取り壊しが要る。取り壊しの案は、失うものを見積もってから出す必要があるため、今月は出せない。
  - 2棟目以降は、2267 の停止(市の調整8)が済んでいることが条件。今月は1棟の案も出せないため、2棟目は考えない。
  - 案なしの判断は、前月の非採択による理由ではない。前の月(20月)は案なしで、今月は場所の確認が前提として足りなかった。

- 捨てたもの:

  - 東の住宅地の Transport Tower(1950,470 など): 置けるが道路に面しない。道を引くには事務所と住宅の取り壊しが要るため、今月は案にしない。22月に、取り壊しなしの場所を探した上で、取り壊しの案として出し直すかを決める。
  - 中心と南西の名所: 空きがない。
  - 島Bと空き地3の名所: 水・下水の管がなく、管の経路の見積もりも未確認。道路下水道局の見積もりを待つ。
  - 大型の名所(Stadium 200,000 / 4,000、ChirpX 200,000 / 2,400 など): 週の維持費が余裕を超えるため、今は対象にしない。

### 保健環境局(health)(hooks の記録で 19:40〜19:48)

- 元のファイル: [m21-health.md](m21-health.md)
- 案 health-1: 道のない埋立地 33216 に北から道をつなぐ
  - 建設費 240、週の維持費 +2、戻せる
  - 市の計画: 4-4
  - 議決: 要らない

- 見たもの: [m21-health.md の「見たもの」](m21-health.md#見たもの)(26 行)
- 判断の根拠:

  - 第21月の予定は、33216 の入口の道を試しで探すこと。北(240)が試しを通ったので、案1にする。南(120)は入口の向きが南だった場合の予備。入口の向きは道具で確かめられず、建てた後の `net_reach` で確かめる
  - 再調査で、入口の向きを道具で確かめた。entrance は (3499,682) の北向きで、北の道の始点は 10m。16m 以内なので、北案で道が入口に届く条件を満たした
  - 23459 の道は、予定どおり23月に回す。今月は出さない
  - 満杯の 3565 の空けは出さない。12880 と 45892 がまだ Emptying のため、計画どおり終わるまで待つ
  - 汚染(印 25): 20月の調査で、2267 の周りの最大 255 は3回とも横ばい。2267 が出どころと決められないため、22月の候補探しは東側の調査を見てから決める。調査を1件出す
  - 政策 Recycling(ごみ -15%、住宅税 -5%)は採らない。住宅税 -5% は、今の住宅税の収入(約 261,000/週、m19 の計算)で約 -13,000/週。週の収支 +8,868 では守る線 +3,000 を割るため
  - 案は1件。担当の問題のうち、確かめられる手は道の1本だけで、ほかは前提が未確認のため出さない

- 捨てたもの:

  - 満杯の 3565 を空にする(`empty_building`): 12880 と 45892 がまだ Emptying。終わるまで待つ(計画どおり)
  - 2267 の移す先の候補探し(22月の予定): 20月の調査で、2267 が出どころと決められない。東側の調査の結果を見てから決める
  - 政策 Recycling: 上記の守る線の理由。週の収支に大きく響く
  - 南の道(120): 予備にした。入口が北と確かめられた後は使わない
  - 23459 の道: 23月の予定。今月は道具の試しをしない

### 教育委員会(education)(hooks の記録で 19:40〜19:48)

- 元のファイル: [m21-education.md](m21-education.md)
- 案 education-1: 小学校 15022 を1校止める(4校目、試し)
  - 建設費 0、週の維持費 +-160、戻せる
  - 市の計画: 2-3
  - 議決: 要らない

- 見たもの:

  - `map_layer`(education_elementary、x=-1350、z=-986、r=300、n=7): 平均 59、min 23(-1050,-1286)、max 116(-1350,-986)。前回と同じ
  - `map_layer`(education_elementary、x=-1350、z=-986、r=600、n=9): 平均 56、min 0(-750,-836)、max 181(-1050,-386)。東の縁 (-900,-986) は 17、(-900,-836) は 10、(-900,-1136) は 11
  - `buildings_near`(x=-1350、z=-986、r=600、service=Education、brief=true): 8 棟。有効な小学校は 15022 だけ。15301、25802、43936 は TurnedOff
  - `buildings_near`(x=-1350、z=-986、r=1200、service=Education、brief=true): 有効な小学校 12 校。15022 以外は 800m 以上離れる(36465、42823、43393 など)
  - `map_layer`(education_elementary、x=-1170、z=-1828、r=300、n=5): 平均 53、min 19(-1470,-1528)、max 116(-1170,-1828)。縁は 19〜21
  - `services`: 小学校 13,224、高校 24,360、大学 36,540。電気・水・下水は余裕あり

- 判断の根拠:

  - 条件は、15022 の覆いで測り、止めても 0 が出ない根拠を出すこと。根拠は出せなかった。15022 の東の縁 (-900,-986) の 17、(-900,-836) の 10、(-900,-1136) の 11 は、近くの有効な学校が 800m 以上離れるため、15022 の分しか届いていない。止めれば 0 が出る見込み
  - 4 校目の候補は、ほかに有効な小学校がない。43393 は縁が 19〜21 で、止めれば 0 が出る見込み。今月は候補がない
  - 案1 は、条件を満たせないため、実行可否を未確認のまま残す。採る理由はない。局は、この案を実行しないことを勧める
  - 2-3 の目標は保っている。小学校の定員 13,224 は子ども 9,049 の 1.46 倍。高校の定員 24,360 は 10代 18,024 の 1.35 倍
  - 費用は週 -160 で、守る線を脅かさない
  - 引数は `tool-reference.md` で確かめた。`set_building_active(id, active)` の形は、この案の操作と合う

- 捨てたもの:

  - 43393(-1170,-1828)を止める: 縁が 0 に落ちる見込み。覆いの重なりがない
  - 15022 を止める(案1): 東の縁が 0 に落ちる見込みで、条件を満たせない。未確認のまま残す
  - 高校を1校置く: 余裕が 6,336 あり、計画の条件(余裕1,000を切ったら置く)に当たらない。休止を続ける
  - 政策 EducationBoost を外す: 週 7,940 の節約になるが、政策は finance の担当。大卒の失業への効きは分からないまま。教育の担当の数字(定員)には当たらない

### 消防局(fire)(hooks の記録で 19:40〜19:40)

- 元のファイル: [m21-fire.md](m21-fire.md)
- 案: なし

- 見たもの: [m21-fire.md の「見たもの」](m21-fire.md#見たもの)(9 行)
- 判断の根拠:

  21月の担当の数字は、火事1、犯罪2、合計3で、目標の4以下を満たしています。計画の事業1の条件(焼け跡が2か月続く)は、今月の数字に当たりません。燃えている火事(48237)は1件で、場所は前の月と別々なので、事業2の「同じ場所で2か月続く」にも当たりません。計画の「合計が5以上なら届きを確かめる」は、合計3のため動きません。よって、計画どおり案を出しません。政策 SmokeDetectors は、街の週の収支 +8,868 に対して週 58,138 かかり、守る線を破るため採りません。
  来月の確かめ: 48237 が焼け跡になったら、事業1の1か月目として記録します(取り壊しは、2か月続くまで案にしません)。

- 捨てたもの:

  - 政策 SmokeDetectors の有効化: 週の費用 58,138 で、週の収支 +8,868 から大きく下がり、守る線(+3,000)を破る。火事の印の数に見合わない。
  - 焼け跡の建物の取り壊し: 焼け跡はまだ出ていない。出ても、2か月続くまで案にしない(計画の事業1)。
  - 火事の届きの追加(消防署): 合計が5未満で、計画の条件に当たらない。届きの確認は、合計が5以上になった月に行う。

### 財政局(finance)(hooks の記録で 19:40〜19:41)

- 元のファイル: [m21-finance.md](m21-finance.md)
- 案: なし

- 見たもの: [m21-finance.md の「見たもの」](m21-finance.md#見たもの)(11 行)
- 判断の根拠:

  - 守る線は、週の収支 +8,868 と所持金 2,616,061 の両方が上にある。財政の手で直す問題はない。
  - 人口は 174,330 → 174,078 と減り、12か月連続。s20-2 の結果では、movingIn が 6〜16 と少なく、転入は止まっているとみえる。ただし、転出の数は道具で測れず、切り分けは半分。
  - 税を動かす案は出さない。住宅税の減税は、1点で週およそ2万の減収(見積もり)で、今の余裕は約 5,800 しかない。効きも未測のため、先に原因を切り分ける。
  - 医療の予算 110 の案は、墓地の使用が 64%(半分以下の条件は未達)のため出さない(計画の条件どおり)。
  - 政策は、税の政策と SmallBusiness を含め、今月は効きが切り分けられないため動かさない。HighTechHousing と Recycling は、週の費用が余裕を超えるため採らない。
  - 案の数は0。代わりに、調査 s21-1 を1件出す。

- 捨てたもの:

  - 住宅税を街全体で1点下げる: 週およそ2万の減収(見積もり)。余裕約 5,800 を超え、効きも未測のため。
  - 住宅税を1地区だけ下げる試し(TaxLowerResHigh を地区に): 原因が税かどうか未確認のため、s21-1 の結果を待つ。議決が要るため、22月に案を出せるか判断する。
  - 政策 Recycling(住宅税 -5%): 週およそ -13,000 の見積もりで、守る線 +3,000 を割る。採らない。
  - 政策 HighTechHousing(週 20,268): 余裕を超え、人口の効きも未確認。採らない。
  - 医療の予算 110(週約 -10,200): 墓地 64% で、条件未達。22月に墓地を確かめる。
  - 融資(BankA、B、C): 所持金が 2,616,061 あり、借りる理由がない。

## 4. 差し戻しと再調査

- 保健環境局: health-1(実行可 True)
- 教育委員会: education-1(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m21-bill.md](m21-bill.md)
- 採った m21-1: 放棄店跡に公園 JapaneseGarden(元 urban-1、議決が要る(取り壊し))
- 採った m21-2: 交差点 (2668,330) に信号(試し)(元 roads-1、議決は要らない)
- 採った m21-3: x=-1640 の南北道を Small 4 Lane に(元 roads-2、議決は要らない)
- 採った m21-4: 休止中の貨物センター 40031 を再開(試し)(元 port-1、議決は要らない)
- 採った m21-5: 埋立地 33216 に北から道をつなぐ(元 health-1、議決は要らない)
- 採らなかった education-1: 再調査でも、小学校 15022 を止めると覆いの東の縁が 0 に落ちる見込みで、止めても 0 が出ない根拠を出せなかった。

- 見たもの:

  - `explain`、`city_info` などの月例の数字: 見る段の市政ノート(2051-09-03)から。人口 174,078、所持金 2,616,061、週の収支 +8,868
  - 局の案: `council/m21-urban.md`、`m21-roads.md`、`m21-port.md`、`m21-health.md`、`m21-education.md`(案あり)。`m21-economy.md`、`m21-fire.md`、`m21-finance.md`(案なし)
  - 編成方針: `council/m21-policy.md`(重点は 5-1・5-2 観光、8-1、4-2)
  - 長期計画: `council/plan-city.md`(第13〜24月、調整 1〜20)
  - 市政ノート: 数字の表、施策の一覧、分からないことの一覧、20月の記録

- 判断の根拠:

  重点 2 の 8-1(m21-4)と重点 3 の 4-2(m21-1)に、局の確認済みの案を採った。重点 1 の観光は、economy が場所を確かめられず案なし、port が旅客の入口を整地なしに置けず案なしで、今月は施策にできない。6-3 の信号と 4 車線化(m21-2、m21-3)は、20月に 3 件とも当たった型で、費用 0 のため採った。
  費用は、建設費が 2,500、週の維持費の増えが 40+1,440+信号(未確認、0 と置く)で約 1,480。週の収支は +8,868 から約 +7,390 に下がり、守る線 +3,000 と下降規則の +4,900 の上にある。所持金は約 2,613,500 の見込みで、守る線 1,874,000 の上。
  観光の公約 4 は、3 か月続けて動かせていない。economy の案なしの理由は、場所の実行条件が確認できないことで、他局の優先順位ではない。役割から外れた判断ではない。port の「整地は局の道具にない」は事実なので、市長は計画の調整に書く。

- 捨てたもの:

  - health-1: 入口の向きが未確認。北が外れると 240 の道が無駄になるだけだが、18月に同じ形で失敗しており、確認が先。
  - education-1: 測りの窓が 15022 の覆いを見ない。節約が小さく、戻す手が前提のため。
  - roads の調査 (4094,-245)、port の調査: 調査の上限 3 件のため。
  - 政策 SmokeDetectors(週 58,138)、Recycling(週およそ -13,000): 守る線を破るため、局も出していない。
  - 市長が観光の代案(名所や整地の試し)を作ること: 局の案から選ぶ決まりのため、作らない。

## 6. 議会: 可決と否決(hooks の記録で 19:51〜19:51)

- 元のファイル: [m21-assembly.md](m21-assembly.md)
- m21-1 取り壊し: 可決。壊すのは働き口0・家0の放棄店1棟。preview_bulldozeで確認済み。
- m21-2 財政: 可決。費用0で守る線に響かない。
- m21-3 財政: 可決。建設費0、維持費の増え0で守る線に響かない。
- m21-4 財政: 可決。維持費+1,440でも週の収支は約+7,400で、守る線と下降規則の上。
- m21-5 財政: 可決。建設費240、維持費約2で守る線に響かない。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `city_info`: 週の収支 +8,868、所持金 2,616,061
  - `preview_bulldoze`(x=2176, z=-318, radius=12, what=abandoned): 24928 の1棟、jobs 0、homes 0、電気の喪失 0
  - `council/m21-bill.md`: 案の費用と予想

- 判断の根拠:

  取り壊しの議案 m21-1 は、失うものが働き口 0、家 0 で、自分でも確かめた。財政は、建設費の合計 2,740 と維持費の増え 1,482 を引いても、週の収支と所持金が守る線を上回る。信号の維持費は未確認だが、0 として扱っても余裕が大きい。

- 捨てたもの:

  - m21-4: 維持費 +1,440 が最大だが、見込みは線の上にあり、重点に当たるため可決にした。

## 7. 実行する市長: 実行と見回り(hooks の記録で 19:51〜19:59)

- 実行してよい施策: m21-1、m21-2、m21-3、m21-4、m21-5
- 実行した: m21-1、m21-2、m21-3、m21-4、m21-5
- 失敗した: なし
- 臨時: なし
- 見回り 2051-09-13: 人口 173978、所持金 2624775、週の収支 7909、幸福度 88
- 見回り 2051-09-23: 人口 173755、所持金 2635070、週の収支 7188、幸福度 88
- 報告:

  5施策すべて成功。月末は2051-10-03。人口173,537(12か月連続の減少が続く)、所持金2,643,814、週の収支+5,957、幸福度87。来ない市民は0/0/0。観光客は2,020人(訪問171)で、前月例の1,837から増えた。Tourism は週105。
  - m21-1: JapaneseGarden(id 12168)を設置。Beautification は96棟で、予想どおり。
  - m21-2: 信号を付けた。blocked は53から、見回りで13、46、月末0に変わった。
  - m21-3: 3区間を Small 4 Lane に差し替えた。blocked は74から、28、17、37に変わった。止まりは (-1632,-1106) 18 に移った。
  - m21-4: 貨物センター40031を再開した。しかし40031には車が0台のまま。28755の止まったトラックは605から632に増えた。WaitingSpace は716のまま。中止条件は両方そろわないので止めていない。週の収支が+5,000に近づいており、22月に再確認が要る。
  - m21-5: 道を引いた。33216 の RoadNotConnected は消え、残りは2。
  - 臨時なし。議決が要る道具で止められた手もなし。
  - 市政ノートは /Users/takeshita/orca/workspaces/tried/issue-124/2026/10-27-AI市役所で福岡を観光都市にする-03-観光の街を目指す計画と局を決める/mayor-note.md に記録した。
  - 調査3件は council/m21-survey-finance.md、m21-survey-health.md、m21-survey-urban.md に書いた。見立ては書いていない。command-log.txt も保存した。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m21、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 19:37〜20:09(hooks の記録の時刻から)、道具の行 287
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

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 9)
