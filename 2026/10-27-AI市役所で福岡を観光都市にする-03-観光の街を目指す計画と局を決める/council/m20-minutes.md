# 20か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 19:21〜19:21)

- 元のファイル: [m20-policy.md](m20-policy.md)
- ゲーム内の日付: 2051-08-04、保存: fukuoka-plan-m20
- 重点: 5-1、5-2 観光(旅客の入口、島・空き地の名所)、8-1、6-4 貨物センターの止まったトラックと品物がない店、4-4 資源循環(道のない埋立地、満杯の埋立地)

- 見たもの: [m20-policy.md の「見たもの」](m20-policy.md#見たもの)(15 行)
- 判断の根拠:

  観光は2つの数字(観光客、Tourism)とも前月より増えたが、目標との差が大きく、入口が0のため重点に置く。貨物センター28755の617台は目標の2.5倍で、品物がない店202にもつながるため、2番目の重点にする。3つ目は、確かめられた手が残るごみ(4-4)を選んだ。人口の減少は原因が分からないので、局の試しの案を待つ。

- 捨てたもの:

  - 4-2 公園(94→100): 6棟足りないが、費用が小さく、局が重点外の案として出せる
  - 6-3 交通の流れ(53%、目標60): 4車線化の局所の効きは出たが、街全体は動かない。重点外の案を待つ
  - 4-3 汚染(22→15以下): 焼却場の停止が2回効かず、出どころが不明。試しの案を待つ
  - 6-1 事務所L3(3,283→3,500): 事務所税の試しで動かなかったため、新しい手がない

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

### 住宅都市みどり局(urban)(hooks の記録で 19:23〜19:24)

- 元のファイル: [m20-urban.md](m20-urban.md)
- 案 urban-1: 道に面した放棄店の跡(2176,443)に公園 JapaneseGarden を1つ置く
  - 建設費 2500、週の維持費 +40、戻せない
  - 市の計画: 4-2
  - 議決: 要る(取り壊し)

- 見たもの: [m20-urban.md の「見たもの」](m20-urban.md#見たもの)(24 行)
- 判断の根拠:

  - 4-2 の Beautification は 94 で、目標 100 まで 6 つ。事業1の第20月の一歩で、道に面した放棄店の跡(2176,443)が、道と電気・水の条件を満たし、`test_place_building` で ok。入口の道(segment 6523、距離0)も確かめた。
  - 取り壊しで失う働き口は 30(全体の 0.03%)。前の月の案と同じく、失う数を議会に出して判断してもらう。
  - 事業2の判定(+1)は、計画の条件(+2)に届かなかった。4-1 は、公園以外の手を探すと計画に書いた。その原因を、調査で見る。手は調査の結果が出てから決める。
  - 案を1件にした理由: 道に面した空きと放棄店の跡の候補は、今月の試しで 1 件だけ確かめられた。ほかの候補は、道がないか、道と重なっていた。確かめられない案を出さないため、1件にとどめた。
  - 重点は 5-1・5-2 観光などで、局の担当の外。局の計画に沿って出した。

- 捨てたもの:

  - 放棄店の跡 (1856,-238) と (1856,-488): 入口に道がないため、未確認。道を引く案は、この月の実行条件を満たせないため出さない。21月に道の案を立てる。
  - 放棄店の跡 (1600,440): 入口に道がない(road null)。道を引く案は未確認。
  - 放棄店 (2172,102)、(2176,-190)、(2176,306)、(2224,38)、(2128,447): 道や公園と重なり、置けない(`test_place_building` で ObjectCollision)。
  - 政策 HighTechHousing(20,244/週): 守る線(週の収支 +3,000)を割るため不採用。
  - 政策 RecreationalUse(0/週): 地価に効くかは見ていない。効きは m03・m04 で観光の数字と切り分け不能だったため、今月は試しとして出さない。調査の結果を見て考える。
  - 樹木の植え付け(`plant_trees`): 地価に効くかは未確認。費用は本数で変わる。調査の結果を見てから、試しの案を考える。

### 道路下水道局(roads)(hooks の記録で 19:23〜19:25)

- 元のファイル: [m20-roads.md](m20-roads.md)
- 案 roads-1: 支線 x=2668 と z=560 の東端を Small 4 Lane にする(止まりの上位、2655,502 付近)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 幹線 z=100 の交差点 (1300,100) の両側を Large Road にする(止まりの上位、1302,120 付近)
  - 建設費 400、週の維持費 +2、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m20-roads.md の「見たもの」](m20-roads.md#見たもの)(15 行)
- 判断の根拠:

  - 19月の z=-490 の4車線化は、blocked 47→0 で効いた(20月の測り)。同じ型の手を、次の止まりの上位に使う。上位の (1302,120) 39 と (2655,502) 29 は、どちらも道具の試しで通る形がある。
  - 2つの案は、どちらも建設費が小さく、取り壊しがなく、維持費の増えも小さい(案1は0、案2は約2/週)。議決は要らない。
  - 街全体の流れ 53% は、局所の4車線化では動かない(19月と同じ)。案は街全体の目標ではなく、場所ごとの blocked を指標にする。6-3 の 60% には、局所の手だけでは届かない見込み。
  - 案を2件に絞った理由: 3件目の候補 (1663,-764) は Large Road の直線上で、交差点がなく、幅を広げる手が試せなかった。政策 HeavyTrafficBan は、トラックの通行を止めるため 8-1 と 6-4 の品物の流れに効き、重点2 と衝突する。案にしない。
  - 調査を1件出した理由: 北脚 (2700,330) は、19月に調査を出す予定だったが出ていなかった。止まりの原因が、交差点の待ちか支線の流入かで、次の手が変わる。

- 捨てたもの:

  - 埋立地 3565 の取り壊しと、z=560 西側の4車線化: 埋立地は満杯の1つで、4-4 の対象。取り壊しの議決が要り、この局の案にしない。案1は埋立地を避けた形で出す
  - 区間 1236 と公園 12209 の差し替え: 公園とぶつかり、壊す案になるため、今月は見送る
  - 政策 HeavyTrafficBan(無料): トラックの通行を止めると、品物がない店(202)と 8-1 の止まったトラック(617)を悪くする。6-3 の目標より重点2 を優先する。市の計画の 6-4 とずれるため案にしない
  - (1663,-764) の Large Road の4車線化(Highway への差し替え): 高架や道の形の試しが要り、今月は道具で確かめていない。次の月に、ほかの候補と比べる
  - 交差点 (1300,100) の信号の変更: `set_traffic_lights` は付けるか外すかだけで、青の時間は変えられない。効き目を見積もれないため、今月は見送る

### 港湾空港局(port)(hooks の記録で 19:23〜19:27)

- 元のファイル: [m20-port.md](m20-port.md)
- 案 port-1: 路線28の予算を下げて、バスの台数を減らす
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要る(予算)

- 見たもの: [m20-port.md の「見たもの」](m20-port.md#見たもの)(7 行)
- 判断の根拠:

  - 旅客の入口は、島Bの駅が斜面と整地の結果で止まっている。本土の港と駅の候補は、すべて道か地形で断られた。入口の案は、局の道具で確かめられる形がない。第19月末の閉じる条件に当たるため、案を出さず、市長に入口の扱いを決めてもらう
  - 8-1 は、目標 250 に対して 617 台が敷地内で動かない。道の混みは小さく、13893 も列車が来ない。局の道具で効く手段がないため、案を出さない。目標を下げるかを市長に求める
  - 6-3 は、街の流れが 53%。路線28 は乗客 92 に対して台数 186 と多い。予算を 180% に下げるのは、局の道具で確かめられる、費用が最も小さい手。効き目の大きさは見積もれないので試しとして出す。予算の±20の上限内に収まる
  - 案は1件にした。6-3 の手段が、ほかに実行できる形で見つからなかったため。件数を埋めるために案を作らない

- 捨てたもの:

  - 島Bの旅客の駅(再提出): 整地の結果が届いておらず、道の斜面(SlopeTooSteep)は残る。第19月末の閉じる条件に当たる。未確認の再提出は、市長が前月に採らなかった理由と同じになるため出さない。入口の扱いは市長に決めてもらう
  - 港の候補(本土の北、南、西、東): test_place_building で ObjectCollision、HeightTooHigh、CannotBuildOnWater、道なしで断られた。空いた場所が確かめられなかった
  - 8-1 の手段(貨物センター13893 の列車を増やす、道を広げる): 13893 は列車の行き先になっていない。接続の手段を局の道具で確かめられない。幹線の Large Road への差し替えは 13893 と 28755 にぶつかって断られ、道の混みも小さいので効きが見込めない。目標を下げるかを市長に求める
  - FreeTransport(政策): 直接の費用は 0 だが、運賃収入 5,073/週が消え、収支の見込みが +3,000 の守る線を割る
  - 路線81(pathFailed 1、乗客 0): 道順が見つからない区間があるが、路線を直す手は局の道具で確かめていない。乗客がなく、6-3 への効きが見込めない

### 経済観光文化局(economy)(hooks の記録で 19:23〜19:25)

- 元のファイル: [m20-economy.md](m20-economy.md)
- 案: なし

- 見たもの: [m20-economy.md の「見たもの」](m20-economy.md#見たもの)(18 行)
- 判断の根拠:

  - 観光の数字(観光客1,852、訪問154、Tourism 87)は、目標の3,000、250、1,000に届いていない。名所の棟数は10で目標どおり。名所の訪問は、SeaWorld の55が最大で、ほかは3〜20。
  - 名所を増やす手は、置ける場所が確かめられなかった。中心と南西は、解禁済みの名所の型に対して空きの大きさが足りない。島Bと空き地3は、水と下水の管がなく、必須条件が残る。
  - 道路の取り壊しや住宅の取り壊しは、名所の場所を作れるが、住宅と事務所を失う。今の数字では、失う働き口と家の見積もりを出す前に、予備候補が確かめられなかった。取り壊しの案は出さない。
  - 政策の一覧に、観光に直接効く政策はない。SmallBusiness と RecreationalUse は、前の試しで効きが切り分けられなかった。今月は新しい政策の試しを出さない。
  - 案を出さない代わりに、調査 s20-1 で、訪問が道のつなぎ口に近いかを確かめる。21月に名所の場所を決める材料にする。

- 捨てたもの:

  - 中心(0,-1500)の名所: 空きの8x12がなく、置けない(ObjectCollision)。道路と住宅の取り壊しは、失う家と働き口が大きく、局の案にしない
  - 南西(-1133,-800)の名所: 空きがなく、Expensive Park と道に重なる。Expensive Park を壊すと 4-2 の公園の数が減るので、案にしない
  - 島Bの Transport Tower(60,000、960/週): 置く場所は確かめられた(ok)が、水・下水の管と入口の道が未確認。見積もりの管の費用(本土から数千)は、道路下水道局の見積もりを待つ
  - 空き地3の名所: 水・下水がなく、道が重なる。19月の天文台と同じ理由で採らない
  - 名所 Observatory(85,000、1,600/週): 19月に採られず、維持費が枠を超えるため
  - 名所 Grand Mall、Modern Art Museum: 維持費が大きく(1,280、1,040/週)、置く場所がない
  - 商業の税を下げる案: 商業の需要が2と低く、税の効きは大きな変化を見込めない。税の議決も要るため、今月は見送る
  - 旅客の入口: 港湾空港局の担当。経済観光文化局は、入口を港湾空港局に求める(長期計画の事業)

### 保健環境局(health)(hooks の記録で 19:23〜19:24)

- 元のファイル: [m20-health.md](m20-health.md)
- 案: なし

- 見たもの: [m20-health.md の「見たもの」](m20-health.md#見たもの)(13 行)
- 判断の根拠:

  第20月の計画は、ごみの印と埋立地の受け入れを見る月で、案を入れていない。満杯の空けは2か所がまだ進行中のため、3つ目を足すと効きが測れない。汚染の出どころは、2267 の周りに 255 の一帯があるものの、停止の試し(m16)が効かなかったため、調査で確かめてから決める。案は出さず、2267 の周りの汚染を3回測る調査を1件出す。

- 捨てたもの:

  - 満杯の埋立地 3565 を空にする(empty_building): 過去の空けは効いたが、12880 と 45892 がまだ進行中で、収集車が足りない。20月は見送り、21月の受け入れを見て判断する。
  - 政策 Recycling(街全体): 住宅税 -5%、約 -13,000/週(計算値)で、週の収支 +7,697 が守る線 +3,000 を割る。採らない。地区だけにかける案は、街の汚染の出どころが分かってから考える。
  - 2267 を移す案: 22月の計画どおり。候補探しに入る前に、調査の結果が要る。

### 教育委員会(education)(hooks の記録で 19:23〜19:23)

- 元のファイル: [m20-education.md](m20-education.md)
- 案: なし

- 見たもの:

  - `services`: 小学校 13,224、高校 24,360、大学 36,540。ごみの満杯 1(3565)、電気・水・下水は余裕あり、犯罪率 5
  - `citizens_summary`: 子ども 9,017、10代 17,997、来ない市民は電気・水・下水すべて 0。健康 88、失業 1,194
  - `map_layer`(education_elementary、x -1370、z -1350、r 400、n 9): 平均 47、最小 3、最大 110。0 は出ていない
  - `buildings_near`(service Education、x -1370、z -1350、r 700): 小学校 15301、43936、25802 は TurnedOff。有効なのは 15022(-1350,-986)と 43393(-1170,-1828)。高校 11542、21446、46203 は問題なし
  - `city_info`: 人口 174,330、所持金 2,581,541、週の収支 +7,697(収入 336,073、支出 328,376)、観光客 1,852(訪問 154)
  - `list_policies`: 有効は SmokingBan(0)、EducationBoost(週 7,940。教育の支出に入る)、BigBusiness(週 4,104)。教育の目標に効く政策の変更はない。EducationBoost は財政の判断に任せ、今月は変えない

- 判断の根拠:

  - 前の月の答え合わせ(m19-5、25802 の停止): 採られて実行できた。期待は、窓の最小が0を出さないことと、維持費が約 -200 減ること。結果は、窓の最小3で0は出ず、教育の支出は 47,640 から 47,400 に下がった(約 -240)。当たり。判定は20月末で済んだので、止めたまま続ける。
  - 定員と子どもの比は 1.47(19月の 1.52 から下がった)。1.3倍を超える状態はまだ続くが、4校目を止めると覆いが0になるかは未確認。
  - 高校の余裕は 6,363(135%)で、10代が減っている。置く条件に届いていない。
  - 案の数: 0。目標を満たしていて、有効な手は覆いの確認が先に要るため。

- 捨てたもの:

  - 4校目の小学校を止める案(候補 15022 か 43393): 効果は週 -160 と小さい。覆いの最小が3なので、止めると0になる恐れがある。候補ごとの覆いを確かめてから、21月に試しで出す。
  - 高校を1校置く案: 余裕が6,363あり、置く条件(余裕1,000を切る)に届いていない。

### 消防局(fire)(hooks の記録で 19:23〜19:23)

- 元のファイル: [m20-fire.md](m20-fire.md)
- 案: なし

- 見たもの:

  - `city_info`: 2051-08-04、人口174,330、所持金2,581,541、週の収支 +7,697、幸福度88、観光客1,852(訪問154)、dialog なし
  - `complaints`: Fire 1(23175、(-1256,-1420))、Crime 1(40850、(1580,-530))、Death 54、NoGoods 202
  - `buildings_near`(x -1256, z -1420, r 60): 23175 が Fire、abandoned false、homes 19(住んでいる16)。grid は電気・水・下水とも true
  - `buildings_near`(problem=Fire、r 5000): 1件(23175)
  - `buildings_near`(abandoned=true、r 5000、上位20件): 焼け跡の建物は見つからず、出たのは店などの FatalProblem の放棄(NoGoods、Death など、火事ではない)
  - `buildings_near`(service=FireDepartment、x -1256, z -1420, r 400): Fire House 46366(-1150,-1624)の1件
  - `map_layer`(type=fire、x -1256, z -1420, r 200, n 5): 平均144、最小98、最大183
  - `list_policies`: 取得できた。火事に関係する政策は SmokeDetectors のみで、非有効、週の費用 58,097(11,347 の火事の建物 × 5.12)。費用が大きく、守る線(週の収支 +3,000)を超えるため、取らない。SmokingBan は有効(0)、EducationBoost は有効(7,940)、BigBusiness は有効(4,104)。政策一覧の政策合計は週 10,856

- 判断の根拠:

  3-4 の合計は2で、目標の4以下を満たします。長期計画の 20月の予定は「案なし」です。焼け跡の取り壊しは、18月と19月の2回とも、合計を下げませんでした。18月は焼け跡 1573 を消したが、948 が新しく焼け跡になり、合計は2のまま(半分)。19月は 948 を消したが、別の建物 23175 に火事が出て、件数は1のまま(外れ)。そのため、長期計画の事業1を見直し、焼け跡が出ても取り壊しは案にしないことにしました(計画の変更、2051-08-04)。今月の火事は、焼け跡でない建物に出たので、取り壊しの対象になりません。
  前の月の答え合わせ(19月の案 fire-1、m19-4): 期待は火事の印 1→0 でした。結果は、948 の印は消えたが、23175 に火事が出て件数は1のままで、外れです。
  消防局は、編成方針の重点(観光、貨物、資源循環)には当たりません。今月は重点外の案を出す理由がありません。ほかに案の候補を探す理由もありません。

- 捨てたもの:

  - 政策 SmokeDetectors の有効化: 週の費用 58,097 で、守る線(週の収支 +3,000)を大きく超えます。今の合計2の目標に対して、効きの量も確かめられていません。
  - 高層住宅 23175 の取り壊し: 焼け跡になっていない建物を壊すのは、焼け跡の取り壊しの効きが見えない今は、根拠がありません。失う家は19(住んでいる16)で、取り壊しは戻せません。
  - 火事の場所 (-1256,-1420) への消防署の追加: 届きは平均144で足りています。維持費を足す理由がありません。
  - 警察署の追加(犯罪の印は1件): 犯罪の印は1で、目標の範囲内です。14月の不採用の理由(3-4 は目標を満たし、週480で守る線の余裕が減る)と同じです。

### 財政局(finance)(hooks の記録で 19:23〜19:24)

- 元のファイル: [m20-finance.md](m20-finance.md)
- 案: なし

- 見たもの: [m20-finance.md の「見たもの」](m20-finance.md#見たもの)(11 行)
- 判断の根拠:

  - 前の月の答え合わせ: m19 の調査 s19-1 は、人口の減りを「死亡」と「転出」で切り分ける問いだった。結果は、高齢は 51,624 → 51,771 と増え、死亡が主ではないと分かる。若い世代と働き盛り(teen 18,147 → 17,997、young 30,888 → 30,766、adult 65,130 → 64,791)が減る。判定は半分。転入と転出の切り分けはまだ。
  - 大卒の働き口の仮説: 大卒の失業は 3,346(7/5)から 2,661(8/4)に減った。それでも人口は 174,778 から 174,330 に減った。大卒の働き口の不足は、減りの主因と言えない。
  - 守る線は、週の収支 +7,697(線 +3,000)と所持金 2,581,541(線 1,874,000)の両方を満たす。義務の範囲では、今月は動かさなくても守れる。
  - 税と政策は、効きが未測で、減りの原因も確定しない。第19月の計画の「原因が分かり、効くと確かめてから動かす」に従い、据え置く。
  - 調査 s20-1 を1件だけ出す。問いは、人口の減りが転入の不足か転出の多さかで、次の手が決まる。
  - 案の数は0件。担当の数字(週の収支、所持金)は守る線の上にあり、今月に打つべき手がないため。

- 捨てたもの:

  - 警察の予算 150 → 120(週 約 -7,250 の見積もり。線形で割った概算): 犯罪の印 1 と警察の使用 41% から、余裕はあるように見える。ただし map_layer(crime)で 3 超の所(11、7、5)が東にあり、下げると住民の犯罪が増えるおそれがある。3-4 の合計(火事 1 + 犯罪 1 = 2)の余裕も、今は要らない。出さない。
  - 医療の予算 130 → 110(週 約 -10,200 の見積もり): 墓地の使用が 63%(15,216 / 24,000)で、計画の条件「半分以下」を満たさない。再調査で条件を満たせなかった前例もある。出さない。
  - 住宅税の減税(低 9 → 8、高 7 → 6): 週の収入の減りが数万円の規模で、余裕 4,697 を超える。転入の効きも未測。出さない。
  - 政策 Recycling(住宅税 -5%、ごみ -15%): 住宅税の減りが週 1 万円台で、余裕を超える。ごみの印 13 の手は、保健環境局の埋立地の案が先。出さない。
  - 政策 HighTechHousing(週 20,244): 余裕 4,697 を超える。出さない。
  - 政策 SmokeDetectors・PowerSaving・WaterSaving(各 58,000 台): 余裕を超える。出さない。
  - 政策 RecreationalUse・SmallBusiness: 観光への効きは、2回の試しで切り分けられなかった。今月の観光の数字(観光客 1,852、Tourism 87)の手は、名所と入口の案に任せる。出さない。
  - 事務所税の変更: 2% と 3% の試し(m09、m11)で、事務所 L3 と大卒の失業は動かなかった。出さない。

## 4. 差し戻しと再調査

- 差し戻しはなかった

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m20-bill.md](m20-bill.md)
- 採った m20-1: 放棄店の跡(2176,443)に公園 JapaneseGarden(元 urban-1、議決が要る(取り壊し))
- 採った m20-2: 支線 x=2668 と z=560 東端を Small 4 Lane に(元 roads-1、議決は要らない)
- 採った m20-3: 交差点(1300,100)両側を Large Road に(試し)(元 roads-2、議決は要らない)
- 採った m20-4: 路線28の予算を200%から180%に(試し)(元 port-1、議決が要る(予算))

- 見たもの:

  - `council/m20-policy.md`: 重点は 5-1・5-2 観光 / 8-1・6-4 貨物 / 4-4 資源循環
  - `council/m20-urban.md`、`m20-roads.md`、`m20-port.md`、`m20-economy.md`、`m20-health.md`、`m20-education.md`、`m20-fire.md`、`m20-finance.md`: 案4件(urban-1、roads-1、roads-2、port-1)と調査5件。economy、health、education、fire、finance は案なし
  - `council/plan-city.md`: 長期計画(第13〜24月)。urban の事業2(公園の周りの地価)を「公園以外の手を探す」に切り替え、fire の事業1(焼け跡の取り壊し)を「焼け跡が出ても案にしない」に切り替えたと各局が書いた。反映する
  - `council/m19-bill.md`: 前月の施策と、採らなかった案の行方
  - 費用の合計: 建設費 2,500 + 0 + 400 + 0 = 2,900。週の維持費の増え 40 + 0 + 2 + (バスの減り) = 約 +42 未満。週の収支は +7,697 から約 +7,650 以上の見込みで、守る線 +3,000 の上。所持金 2,581,541 は、守る線 1,874,000 の上

- 判断の根拠:

  重点1(観光)と重点2(8-1、6-4)は、局の案が出なかった。経済観光文化局は名所の置き場所を確かめられず、港湾空港局は旅客の入口と貨物センターの手を確かめられなかったと書いた。旅客の入口が0のままである点は、公約4の最大の穴として残る。確認済みの案は urban-1、roads-1、roads-2、port-1 の4件で、どれも実行条件が道具で確かめられている。費用は建設費 2,900 と小さく、守る線を破らない。議決は取り壊し(m20-1)と予算(m20-4)で、1件に1種類にしている。調査は、観光(economy)、人口(finance)、汚染(health)の3件を採った。

- 捨てたもの:

  - urban の調査(地価): 3件の上限のため。公園の地価の効きは、4-2 の数の案で追う
  - roads の調査(北脚 (2700,330)): 3件の上限のため。m20-2 が近くの支線を差し替えるので、基準が変わる
  - 重点にしなかった施策の手(RecreationalUse、SmallBusiness、HeavyTrafficBan など): 局が根拠なしか、重点2・6-4 と衝突する理由で出していない
  - 市長による代案(旅客の入口、貨物の手): 市長は自分で施策を考えない。担当局が確かめられる形で出すのを待つ

## 6. 議会: 可決と否決(hooks の記録で 19:30〜19:30)

- 元のファイル: [m20-assembly.md](m20-assembly.md)
- m20-1 取り壊し: 可決。preview_bulldozeで3棟、働き口30、家0と一致。代わりの手の検討も書かれている。
- m20-2 財政: 可決。建設費0、維持費の増え0で守る線に響かない。
- m20-3 財政: 可決。建設費400、維持費の増え約2で守る線に響かない。
- m20-4 予算: 可決。変更幅20で上限内。維持費が減る方向で、試しの仮説と測る数がある。
- 可決した種類(hooks が見る): 予算、取り壊し

- 見たもの:

  - `city_info`: 所持金 2,581,541、週の収入 336,073、支出 328,376
  - `economy`: 税と予算は今の値。路線28 の変更は別の路線予算
  - `preview_bulldoze`: radius 32 で3棟(ホテル2、店1)、働き口30、家0

- 判断の根拠:

  費用の合計は建設費2,900、維持費の増え42で、収支も所持金も守る線から大きく離れている。取り壊しは失うものが数字で示され、予算の変更は幅が上限内である。ホテルが含まれる点は、観光の方針とは緊張するが、働き口の少ない放棄された跡であり、記載の数字は確認できたので否決の点には当たらない。

- 捨てたもの:

  - m20-1: 壊す3棟に観光向けのホテルが含まれるが、点1から5のどれにも当たらず、数字も書かれているので可決にした。

## 7. 実行する市長: 実行と見回り(hooks の記録で 19:30〜19:37)

- 実行してよい施策: m20-1、m20-2、m20-3、m20-4
- 実行した: m20-1、m20-2、m20-3、m20-4
- 失敗した: なし
- 臨時: なし
- 見回り 2051-08-14: 人口 174242、所持金 2592021、週の収支 9620、幸福度 88
- 見回り 2051-08-24: 人口 174078、所持金 2603668、週の収支 8503、幸福度 88
- 報告:

  4件の施策を、議案のとおりすべて打ちました。m20-1 は preview で3棟(29473、34163、42442)を確認して壊し、JapaneseGarden(id 13376、2,500)を置きました。入口は segment 6523 です。月末の Beautification は95で、予想どおりです。m20-2 は x=2668 の3区間と z=560 東端の1区間を Small 4 Lane にしました(費用0)。blocked は53から26に減りましたが、見回り2では65に揺れました。止まりは北の交差(2678,338)に移っています。m20-3 は区間 17667 と 33219 を Large Road にしました(400)。blocked は71から8に減りました。区間 1236 は density 100 のままです。m20-4 は路線28(line 136)を予算180%にし、台数は186から171になりました。乗客は92、29、110と揺れ、街全体の流れは53から55になりました。月末の人口は174,078(月初174,330)で、減少が続いています。所持金は2,616,061、週の収支は+8,868、幸福度は88です。見回りは2回とも境目に当たらず、臨時は行っていません。議決が要る道具は advance の前に済ませました。調査は s20-1(economy)、s20-2(finance)、s20-3(health)を3回ずつ council/m20-survey-*.md に書きました。市政ノートと command-log.txt も更新済みです。旅客の入口は0のままで、今月も案はありませんでした。月末の保存は頼まれていないので、していません。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m20、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 19:20〜19:47(hooks の記録の時刻から)、道具の行 233
- 議会が可決した種類: 予算、取り壊し
- 議決が要る道具の呼び出し: 2 回
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
