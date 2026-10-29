# m16 保健環境局の案

## 案1: 焼却場 2267 を止め、汚染の印を減らす(試し)

### 施策

- 案の id: health-1
- 施策: 焼却場 Combustion Plant(id 2267、(3604,-30))を止める。道具は `set_building_active`(id 2267、active false)。止めた後の汚染とごみを、見回り1・見回り2・月末で測る
- 議決: 要らない(`set_building_active` は議決の種類に入らない)

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `services` で garbage.full が0、`complaints` の Garbage が9以下、東の埋立地 39575(3250,-362)に空きがあることを確かめる。2. `set_building_active(id=2267, active=false)`。3. 見回り1・2と月末に、`complaints` の Pollution と Garbage、`services` の garbage と electricity を測る
- 設置条件の確認: 道具で確かめた事実。
  - `buildings_near`(x 3604、z -30、r 40、service Garbage): 2267 が Combustion Plant、storage 348,750 / 400,000(87%)、処理 60,000 / 週、Power Output 15 MW、trucks 4/34。
  - `buildings_near`(x 3400、z -200、r 400、service Garbage): 埋立地 39575(3250,-362)が storage 564,916 / 8,000,000(7%)、trucks 15/19。東に空きがある。
  - `services`: garbage.full count 0、garbage 使用 100,092,198 / 184,000,000、electricity 容量 2,318,624 / 使用 1,707,040。
  - `complaints`: Garbage 4、Pollution 21(hotspot (3696,-10)、11棟)。
  - 2267 の近く(40m以内)に住宅 23124、31499 があり、31499 は Pollution の印。
- 接続工事: 不要(止めるだけ)
- 予備候補: なし
- 中止する条件: (1) 見回りか月末で Garbage が15を超える → `set_building_active(id=2267, active=true)` で戻す(前の月の決まりと同じ)。(2) `services` の electricity で used が capacity を超える、または `city_info` の citizensWithoutService.electricity が0より増える → 同じく戻す。(3) `services` の garbage.full が1以上になる → 戻す。

### 期待する効果

- 改善の見込み: 2267 の煙が近くの住宅の汚染の印を出している、と見込む。m02-3 では同じ停止で汚染の印が 45→35 に減った(局の予測。同じ施設の前例で、確かな数字ではない)。
- 数値と期限: 汚染の印(`complaints` Pollution)を 21 から 15 以下へ近づける。予想は 11〜15(量は見積もれない。前例の -10 からの見込み)。判定は 2051-04-30(月末)。ごみの印(Garbage)は 4 から増える見込み。m02-3 では 11→22 だったので、今は 4→8〜10 程度と予想する(量は見積もれない)。上限15を超えたら戻す。
- 確認方法: `complaints`(Pollution と Garbage の件数)と、`map_layer`(pollution、中心 (3650,-50)、r 300)の平均。今の値(Pollution 21、ごみ 4)と同じ範囲で比べる。週の収支は `city_info` の weeklyIncome と weeklyExpenses で見る。
- 不確かな点: 2267 の 15 MW が電気の容量から外れたときの余裕は未確認(容量 2,318,624 に対し使用 1,707,040 で余裕はある)。ごみの増えは、東の埋立地 39575 と 2267 の周りの運搬で変わる。
- 試し: あり。仮説: 2267 の煙(汚染)が近くの住宅の汚染の印を出し、止めると減る。測る数: `complaints` の Pollution 件数と、`map_layer` pollution の平均。場所: 2267 の周り (3604,-30) の r 300。基準: 今の値 Pollution 21(4/6)。平均は今月は未測定で、止める前に測る。同じ条件で月末に測る。担当の範囲の数(汚染とごみ)で測る。

### 費用

- 建設費: 0
- 週の維持費の増え分: 約 -1,440(止めると減る。局の見積もり。道具の確認は実行後に `city_info` で見る)

### 戻せるか

戻せる。`set_building_active(id=2267, active=true)` で戻す。

### 前の月の答え合わせ

- 前の月の案 health-1(m15-3、満杯の埋立地 12880 を空にする): 予想はごみの印 8→0 に近づく。結果は 4 で、ほぼ当たり。ただし 12880 は先月と同じ 95%(7,620,000)で、空けが進んでいない。原因は分からない。判定: 半分。次の扱い: 12880 の空けは、今月の案の判定と並べて見る。
- 前の月の調査 s15-2(死体の印 42、霊柩車): 3月から4月の結果を読んだ。霊柩車が 158 台中 約 76 台 Blocked、41 台が7日以上止まっていた。死体の印の hotspot は東(3606,-231)。
  - 今回の確認(4/6): 東の火葬場 39843(3598,-90)は `buildings_near` の stats で「Deceased stored 0 / 105、Deceased processed last week 0、Hearses in use 8/9」。`vehicles_stuck`(building 39843)では、霊柩車 5 台のうち 4 台が Congestion か Blocked で、東の幹線(x 3117〜3258、z -258〜-618)で止まっている。道の密度は 100 で、`traffic`(3297,-248、r150)は blocked 9、congestion 44、flow 53。
  - 判断: 死体の印の主な原因は、東の幹線の混みで霊柩車が火葬場に戻れないこと、と見込む。火葬場を足す手ではなく、混みを減らす道路の手になる。道路の手は道路下水道局の担当なので、求めることとして渡す(下の調査とは別)。

### 市の計画

- 当たる施策: 4-3 脱炭素社会(汚染の印)
- 編成方針の重点に当たるか: 当たらない(重点は観光、貨物、公園。汚染は重点の外だが、担当の目標 4-3 の 21→15 に効く)

## 調査

- 調査: あり
- 問い: 火葬場 39843 の処理が1週間で0のままなのは、霊柩車が東の幹線の混みで止まるためか、ほかの原因か。
- 見る道具と引数: (1) `vehicles_stuck`(kind="hearse"、building=39843、limit=10)。(2) `traffic`(x=3200、z=-260、radius=150)。(3) `buildings_near`(x=3598、z=-90、radius=40)で、火葬場 39843 の stats(Deceased stored、processed last week、Hearses in use)。
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: (a) Congestion と Blocked の台数が、見回りごとに減らず、seenStoppedDays が 7 日以上のまま → 道路の混みとして roads へ渡す(求めること)。(b) 霊柩車の状態が Stopped か path none が多い → 道順の問題として、火葬場の入口の道を確かめる案を次の月に出す。(c) processed が見回りごとに 0 から増える → 直ったとして、死体の印を月末で見る。
- 担当の問題: 1-2 健やかで心豊かに暮らせる社会(健康)。死体の印は担当の数字の一つ(施策の番号はない)

## 見たもの

- `city_info`: 人口176,528、所持金2,473,305、週の収支 +12,150(収入337,563、支出325,413)、幸福度88、観光客1,937(訪問160)、来ない市民 0/0/0
- `services`: garbage 使用 100,092,198 / 184,000,000、garbage.full 0、deathcare 14,623 / 24,000(full 0)、electricity 2,318,624 / 1,707,040、water・sewage に余裕、healthcare 732 / 5,100、police 435 / 1,000
- `complaints`: Pollution 21(hotspot (3696,-10)、11棟)、Garbage 4(hotspot (1972,514)、2棟)、Death 32(hotspot (3606,-231)、12棟)、Fire 4、電気 2(11580、30466)
- `citizens_summary`: 健康88、失業4,713(大卒4,608)、badHealth 895、電気・水・下水が来ない 0
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(3,824)。無効のうち汚染やごみに関係するのは Recycling(costPerWeek 0。説明: 住宅の税収 -5%、ごみ -15%)。SmokeDetectors(57,718、火事の政策)は汚染に効かない。汚染を直接減らす政策は一覧にない。政策の費用は policyExpensesPerWeek 10,591
- `buildings_near`(x 3604、z -30、r 40): 2267 の storage 348,750 / 400,000、処理 60,000 / 週、Power Output 15 MW
- `buildings_near`(x 3400、z -200、r 400、Garbage): 埋立地 39575(3250,-362)が 7%(564,916 / 8,000,000)
- `buildings_near`(x 3598、z -90、r 60): 火葬場 39843 の stats は Deceased stored 0 / 105、processed last week 0、Hearses 8/9
- `buildings_near`(x 3300、z -200、r 1200、HealthCare): 火葬場は東にも 39843(3598,-90)、21324(2685,-138)、23747(2222,-255)、墓地 9364(4090,-210)。東の死体の印の場所には火葬場がある
- `buildings_near`(x 3500、z -200、r 500、problem Death): 東の死体の印 6棟(675、7607、10743、10822、25843、44578)。Death が Major か Fatal
- `vehicles_stuck`(kind hearse、limit 8): 158 台、Congestion か Blocked の状態が多い。7日以上止まり 41 台
- `vehicles_stuck`(kind hearse、building 39843): 5 台のうち 4 台が Congestion か Blocked。東の幹線(x 3117〜3258)で止まる
- `traffic`(x 3297、z -248、r 150): flow 53、cars 106、blocked 9、congestion 44。busiest は Small 4 Lane Road(x 3162〜3281、z -232〜-278)で density 100
- `net_near` と `net_reach`(x 3560、z -120、r 180 / 250): 火葬場の道は z=-120 の Basic Road(西へ)と、x=3580 の枝。道の到達は全部 OK(notEnterable 0、notLeavable 0)
- `list_building_types`(service HealthCare): Crematory 25,000 / 720 週、Cemetery 8,000 / 160 週(deathcare 容量 3,000)
- `zone_map`(x 3500、z -200、r 350): 東の区画は埋まりに近く、空きは少ない。候補の空きは今回は確かめていない

## 判断の根拠

- 汚染の印 21 は目標 15 以下に6足りない。近くの 2267 は止めれば汚染を減らした前例(m02-3: 45→35)がある。ごみは 4 で、停止の条件(9以下、満杯0、東の埋立地の空き)を満たした。埋立地 39575 は 7% なので、運搬先の余裕は十分と見込む。電気の余裕も確かめた(容量 2,318,624 に対し使用 1,707,040)。維持費は約 -1,440 で減る。以上から、試しとして案1を出す。
- 死体の印は、東の火葬場 39843 の処理が 0 / 週で、霊柩車が東の幹線の混みで止まっていた。原因の道路の混みは、局の手の外(道路下水道局の担当)にある。案は出さず、道路の混みとして求めることに渡す。混みが続くかを見るため、調査を1件出す。
- 案は1件。政策の Recycling は、住宅の税収 -5% の額が確かめられず、週の収支の守る線(+3,000)との余裕を見られないので出さない。

## 捨てたもの

- 政策 Recycling を有効にする(ごみ -15%、週の費用 0): ごみの印 4 を 0 に近づける手として比べた。ただし住宅税収 -5% の額を道具で確かめられていない。政策の変更は月1件で、2267 の試しと同じ月に行うと効きが混ざる。来月以降、税収の額を確かめてから出す。
- 東の火葬場を増やす(Crematory 25,000、週 720、または墓地 8,000、週 160): 東にはすでに火葬場 39843 と墓地 9364 があり、死体の印は、場所が遠いのではなく霊柩車の道の混みで起きている。足しても混みは減らない。取り下げ。
- 霊柩車の混みを減らす道路の拡張: 道路下水道局の担当で、局の案にできない。求めることとして市長に渡す(今月の案には入れない)。
