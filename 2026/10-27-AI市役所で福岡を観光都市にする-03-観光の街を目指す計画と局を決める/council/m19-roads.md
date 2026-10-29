# m19 道路下水道局の案

## 案1: 止まりの多い z=-490 の幹線7区間を4車線にする(試し)

### 施策

- 案の id: roads-1
- 施策: 幹線 z=-490(x 2645〜3135)の Basic Road 7区間を Small 4 Lane Road に差し替える。道具は `upgrade_road`
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `upgrade_road(prefab="Small 4 Lane Road", points=[[2645,-490],[3135,-490]], tolerance=20, pay=true, demolish=false)`。対象は segment 13834、28637、5524、35451、26681、9242、21069(7区間)。2. 実行後、`traffic(x=2790, z=-490, radius=150)` で blocked を測る
- 設置条件の確認: `test_upgrade_road` で同じ引数を試した。matched 7、upgraded 7、skipped なし、demolishedBuildings なし、cost 0、zonesKept true。`net_near`(x 2776, z -490, r130)で、対象の4区間が Basic Road の1車線ずつ。`net_near`(x 3010, z -490, r60)で、東の3区間(26681、9242、21069)が Basic Road。3130 から先の曲がり(segment 2871、2074)は対象外で、Basic Road のまま残す
- 接続工事: 不要(差し替えだけで、交差点と接続は変わらない)
- 予備候補: 確認済み。`upgrade_road(prefab="Small 4 Lane Road", points=[[2645,-490],[2980,-490]])` は test で matched 5、upgraded 5、skipped なし、demolishedBuildings なし、cost 0。東の2区間(9242、21069)を外す
- 中止する条件: 実行時に matched が 7 にならない、demolishedBuildings が1件以上、または cost が 0 より大きい場合は、予備候補の5区間に直す。それでも断られたら見送る

### 期待する効果

- 改善の見込み: z=-490 の東西の幹線は、4区間が density 100 で詰まり、止まりの上位に入っている(blockedSpots (2734,-491) 29、(2851,-491) 18)。1車線を2車線にすると、車の通過が速くなり、止まりが減ると見込む。東側の Basic の区間も density 100 のため、一緒に太くして、詰まりを後ろに移さないようにする
- 数値と期限: 基準は 2051-07-05 の `traffic(x=2790, z=-490, radius=150)` で blocked 47、cars 59、congestion 57。予想は 20月末に blocked 20 以下。量は見積もれない範囲で、前の4車線の結果は揺れた(m07-2 は 60→17、m09-2 は 76→154)。判定は20月末
- 確認方法: `traffic(x=2790, z=-490, radius=150)` の blocked と cars を、今の値(47、59)と同じ条件で測る。20月は見回り1と月末で2回測る
- 不確かな点: 詰まりが、東の端(3130 の先の曲がり、segment 2871・2074)へ移る見込みがある。街全体の流れ(52%)は、この1路線だけでは大きく動かない見込み
- 試し: 試し。仮説: 1車線の Basic が続く幹線は、通過の遅れが止まりになり、2車線にすると止まりが減る。測る数: `traffic` の blocked(x 2790、z -490、r150)。場所: z=-490、x 2645〜3135。基準: 47(2051-07-05)。編成方針の「分からないこと」のうち「信号と4車線化の効きの揺れ」に当たる

### 費用

- 建設費: 0(`test_upgrade_road` の cost 0。Basic 5,000/km と Small 4 Lane 5,000/km で差がない)
- 週の維持費の増え分: 0(Basic 40/km と Small 4 Lane 40/km。`list_net_types`)

### 戻せるか

戻せる。Small 4 Lane Road から Basic Road へ差し替えれば、費用 0 で戻る。

### 前の月の答え合わせ

- 18月の案 m18-roads-1(z=10 の幹線を4車線にする、試し)は採られ、実行 ok。判定前。今月の `traffic(x=1497, z=62, radius=200)` は blocked 37、flow 52。台帳に18月の基準の値がないため、判定できない。20月に同じ範囲で測る

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たらない

## 調査

- 調査: あり
- 問い: 交差点 (2700,330) の北脚で止まる車(blocked 72、(2710,309) 付近)は、信号の待ちが続く形か、北側の出口の詰まりか。
- 見る道具と引数: `traffic(x=2710, z=309, radius=60)`、`junction_info(x=2700, z=330)`
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: 3回とも blocked が50以上で、busiest が北脚(segment 19421、2700 の 285〜330)なら、この交差点の信号の見直しを次の案にする。30以下が続けば一時的とみて、案なし。北脚の先(segment 9781、2700 の 240〜285)が busiest なら、その区間の太さを確かめる案にする
- 担当の問題: 6-3 公共交通を主軸とした交通体系

## 見たもの

- `city_info`: 人口174,778、所持金2,555,946、週の収支 +7,740(収入336,364、支出328,624)、観光客1,795(訪問150)、来ない市民 0/0/0、dialog なし
- `traffic`(街全体): 流れ52%、cars 7,393、blocked 772(道の上 771)。blockedSpots の上位は (2710,309) 72、(3910,-253) 37、(-1486,-695) 34、(2734,-491) 29、(2656,494) 28、(2517,557) 28
- `traffic`(x 2710、z 309、r150): blocked 95。(2710,309) の 72 は北脚。density 100 は、東西の Small 4 Lane(2684,330 など)と北の Basic(2668,370〜445)
- `traffic`(x 3910、z -253、r150): blocked 58。(3910,-253) 37 は Small 4 Lane 1826(3808,-250)付近
- `traffic`(x 2734、z -491、r150): blocked 45。Basic Road の z=-490 の4区間が density 100
- `traffic`(x 2790、z -490、r150): blocked 47、cars 59、congestion 57(案の基準)。3区間の density 100 は 26681、28637、35451
- `traffic`(x 2517、z 557、r150): blocked 40。(2517,557) 28 は Basic Road 18127(2557,560)付近
- `traffic`(x 1497、z 62、r200): blocked 37、flow 52(18月の案の結果)
- `junction_info`(x 2700、z 330): 信号あり(customLights true、canEnableLights true)。3脚(東西と北)。北脚は segment 19421
- `net_near`(x 2710、z 309、r120): 北脚 19421、南北の 9781、2176、東西の 4818、2093、25781 の Small 4 Lane。Basic Road は 6704、7468(x 2668)
- `net_near`(x 2776、z -490、r130): z=-490 の Basic 10区間のうち、対象の4区間(13834、28637、5524、35451)は 1車線ずつ
- `net_near`(x 3010、z -490、r60)、`net_near`(x 3150、z -490、r50): 東の 26681、9242、21069 は Basic、3130 から先は 2871、2074
- `test_upgrade_road`: [[2683,-490],[2869,-490]] は matched 2(端が足りない)。[[2668,330],[2668,483]] は matched 2、cost 0。[[2645,-490],[2905,-490]] は matched 4、cost 0。[[2645,-490],[2980,-490]] は matched 5、cost 0。[[2645,-490],[3135,-490]] は matched 7、cost 0、demolishedBuildings なし
- `list_net_types`(Road、解禁済み): Basic Road 5,000/km、40/km。Small 4 Lane Road 5,000/km、40/km。Large Road 10,000/km、120/km
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,044)。無効は SmallBusiness(313)、RecreationalUse(0)、HeavyTrafficBan(0。貨物のトラックを止める政策)、FreeTransport(0。運賃収入が0になる)。policyExpensesPerWeek 10,898
- `citizens_without_service`(sewage): residents 0
- `buildings_near`(x 712、z 1644、r150、brief): 11580 StatueOfWealth(668,1565)と 30466 Regular Park(762,1600) の problems は None

## 判断の根拠

- 交通の流れは52%で、計画の前提(6/5 の55%)と違うため、計画の出発点を直した。目標の60%までは、止まりを1か所ずつ減らすしかない。
- 止まりの最大(2710,309)は、交差点の信号と4車線がすでにあり、手が決まらない。原因を調査で確かめる。
- z=-490 の7区間は、1車線の Basic で止まりの上位に入り、差し替えの費用と維持費が 0 と確かめた。今月の手として選んだ。
- 案は1件、調査は1件。案を増やすと、同じ4車線化の効きが混ざるため、1か月に1路線だけにした(計画の「1つずつ」)。

## 捨てたもの

- 幹線 z=560 の Basic 2区間(2557,560、2630,560 の付近)の4車線化: 止まり 28(2517,557)に効く見込みがある。ただし、同じ4車線化を同月に入れると効きが混ざり、台帳の m07-3 では効きが出なかった。今月は1路線だけにする
- 政策 HeavyTrafficBan を有効にする: 費用は0だが、貨物のトラックを止める政策で、6-4 の品物がない店(194、目標120以下)を悪くする見込み。政策の変更は月1件の上限もあるため、今月は出さない
- 交差点 (2700,330) の信号の見直し: 原因が分からないため、調査の結果を待つ
- 埋立地や名所の道(担当外、または前に採られた名所の道): 今月は出さない
