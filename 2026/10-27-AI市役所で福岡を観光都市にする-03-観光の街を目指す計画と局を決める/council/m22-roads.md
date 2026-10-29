# m22 道路下水道局の案

## 案1: x=-1640 の残り Basic 6区間を Small 4 Lane にする

### 施策

- 案の id: roads-1
- 施策: x=-1640 の南北道のうち、まだ Basic Road の6区間(z -1190〜-785)を Small 4 Lane Road に差し替える。21月の3区間の続き。止まりの中心は (-1637,-901) 20 台
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `upgrade_road`(prefab="Small 4 Lane Road", points=[[-1640,-965],[-1640,-785]], tolerance=20, pay=true, demolish=false)。対象は4区間(segment 35196、3136、5629、30638)
  2. `upgrade_road`(prefab="Small 4 Lane Road", points=[[-1640,-1180],[-1640,-1100]], tolerance=20, pay=true, demolish=false)。対象は2区間(segment 34727、33705)
- 設置条件の確認: `test_upgrade_road` の両方で、matched と upgraded が同数、skipped なし、demolishedBuildings なし、cost 0、zonesKept true。1回目は matched 4 / upgraded 4、2回目は matched 2 / upgraded 2
- 接続工事: 不要(同じ道の差し替えで、交差点と接続は変わらない)
- 予備候補: なし(差し替えの引数は試しの道具で通った)
- 中止する条件: 実行時の `upgrade_road` が skipped を返したら、その区間だけ外して残りを差し替える。全部断られたら見送る

### 期待する効果

- 改善の見込み: x=-1640 の南北道の Basic 区間が、止まりの中心になっている。21月に3区間を Small 4 Lane にしたとき、同じ道の止まりは下がった(確認した事実)。残りの Basic 区間も同じ型で止まりを減らすと、局は予想する。
- 数値と期限: 確認した今の値は、`traffic` の (x=-1640, z=-880) r100 で blocked 22、(x=-1640, z=-1000) r200 で blocked 41。予想は、r100 の blocked を 10 以下、r200 の blocked を 40 以下。期限は第22月末(見回り2回と月末で確認)。局の見積もりで、効きの量は確かめていない
- 確認方法: `traffic` の x=-1640、z=-880、radius=100 と、x=-1640、z=-1000、radius=200 の blocked。今日の値と同じ範囲で比べる
- 不確かな点: 止まりが上流(南の -1190 より先)へ移る可能性がある。移ったら、次の月の上位に入れる
- 試し: なし(21月の同じ型の差し替えで効きを確かめている)

### 費用

- 建設費: 0(`test_upgrade_road` の cost 0。Basic Road と Small 4 Lane Road は、どちらも km 当たり 5,000)
- 週の維持費の増え分: 0(どちらも km 当たり 40)

### 戻せるか

戻せる。`upgrade_road` で Basic Road に差し替え直せる。

### 前の月の答え合わせ

- 21月の案 roads-2(x=-1640 の南北道3区間を Small 4 Lane、m21-3)は採られ、実行 ok。予想は blocked 74→40以下(22月末)
- 今日の測り `traffic`(x=-1640, z=-1000, r200)は 41。予想の40以下に届かず、半分。残りの Basic 区間が止まりの中心と見える
- 今月の案での扱い: 残りの6区間を、案1として出す

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たる(重点3)

## 案2: 交差点 (2236,-950) に信号を付ける(試し)

### 施策

- 案の id: roads-2
- 施策: 3叉路 (2236,-950) に信号を付ける。(2280,-950) の信号を抜けた先で、Basic 3334・36011(9m)が合流する交差点。上位の止まり (2302,-946) 51 台は、この交差点より上流に並ぶ。試し
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `set_traffic_lights`(x=2236, z=-950, active=true)
- 設置条件の確認: `junction_info`(2236,-950) で、node 5405、3区間(segment 3334 Basic 東、36011 Basic 西、10391 Basic 北)。trafficLights false、customLights false、canEnableLights true。信号の付けられる交差点
- 接続工事: 不要
- 予備候補: なし。(2280,-950) は既に人の信号があるため使わない
- 中止する条件: 実行時に `junction_info` の canEnableLights が false なら見送る

### 期待する効果

- 改善の見込み: 上位の止まり (2302,-946) は、(2280,-950) の信号の先で、Basic 3334 から (2236,-950) に入る車が詰まっていると見る。この3叉路は譲れの標識も信号もなく、出入りが順番にならない。信号で順番を決めると、3334 からの流れが改善すると局は予想する。効きは不確か
- 数値と期限: `traffic` の (x=2302, z=-946) r150 の blocked は今 75(その地点の上位は 51)。予想は 50 以下。期限は第22月末(見回り2と月末)。基準より増えたら、外す
- 確認方法: `traffic` の x=2302、z=-946、radius=150 の blocked と blockedSpots。同じ範囲で比べる
- 不確かな点: 1車線の Basic 3334 の容量が上限なら、信号では効かない。その場合は 36011(9m)を含む区間の作り直しが要り、取り壊しの議決になる。効きの量は見積もれない
- 試し: 仮説は「無信号の3叉路が、Basic 3334 からの合流を止め、(2280,-950) の信号の出口を詰まらせる」。測る数は `traffic` の blocked。場所は (2302,-946) r150。基準は 75(地点の上位 51)

### 費用

- 建設費: 0(道具の説明に費用の記載なし。実行後の予算の変化で確かめる)
- 週の維持費の増え分: 0(同上)

### 戻せるか

戻せる。`set_traffic_lights`(active=false)で外せる。

### 前の月の答え合わせ

- 21月の案 roads-1(信号 (2668,330)、m21-2)は採られ、実行 ok。予想は blocked 53→30以下(22月末)
- 今日の測り `traffic`(x=2668, z=330, r200)は blocked 1。53 から 1 に下がり、当たり
- 今月の案での扱い: 信号の手は効いた地点があるので、別の3叉路で試す(案2)

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たる(重点3)

## 調査

- 調査: あり
- 問い: x=-920 の4車線区間(z -857)の止まり(`traffic` の r150 で 58)は、上流の4車線の容量が原因か、下流の Basic 区間(segment 4744、32601)の詰まりが原因か。
- 見る道具と引数: `traffic`(x=-920, z=-980, radius=80)と `traffic`(x=-920, z=-857, radius=60)。今日の基準は、下流が blocked 7、上流の r150 が 58
- いつ見るか: 見回り1、見回り2、月末
- 何が分かれば次の手が決まるか: 下流の blocked が上流と同じく増えるなら、下流 Basic 4744 と 32601 を Small 4 Lane に差し替える案を次に出す(4744 は `test_upgrade_road` で matched 1、cost 0 を確認済み)。上流だけが増えるなら、4車線を Large Road に太くする案を考える。ただし沿道の建物 15 棟(住宅 10、店 3、事務所 2)の取り壊しが要るため、取り壊しの議決と働き口・家の損失を数えてから
- 担当の問題: 6-3 公共交通を主軸とした交通体系(交通の流れ)

## 見たもの

- `traffic`: 街全体 flow 55、cars 7,532、blocked 642。busiest は Basic の区間が多い。blockedSpots 上位は (2302,-946) 51、(-920,-857) 48、(3099,-471) 47、(3137,-284) 41
- `city_info`: 人口 173,537、所持金 2,643,814、週の収支 +5,957(収入 335,699、支出 329,742)、幸福度 87、観光客 2,020(訪問 171)、来ない市民 0/0/0
- `list_policies`: 政策の費用計 10,794/週。有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,068)。関係する交通の政策 FreeTransport と HeavyTrafficBan は無効(費用 0)。SmallBusiness と RecreationalUse は無効
- `traffic`(x=2668, z=330, r200): flow 55、blocked 1(基準 21月は 53)。(2663,529) 1
- `traffic`(x=-1640, z=-1000, r200): blocked 41。blockedSpots (-1637,-912) 23、(-1632,-1106) 18
- `traffic`(x=-1640, z=-880, r100): blocked 22。blockedSpots (-1637,-901) 20
- `traffic`(x=2302, z=-946, r150): blocked 75。blockedSpots (2302,-946) 51、(2172,-917) 12、(2225,-1042) 9
- `traffic`(x=-920, z=-857, r150): blocked 58。blockedSpots (-920,-857) 48、(-917,-784) 10
- `traffic`(x=3099, z=-471, r150): blocked 63。blockedSpots (3099,-471) 47、(3158,-369) 10
- `traffic`(x=-920, z=-980, r80): blocked 7。下流の Basic 4744(-920,-988) density 100、32601(-920,-1036) density 100
- `traffic`(x=3449, z=-1555, r150): blocked 0。道の密度の平均 9
- `junction_info`(2236,-950): trafficLights false、canEnableLights true、canSetYield true
- `junction_info`(2280,-950): trafficLights true、customLights true(人が決めた信号)
- `junction_info`(3130,-490): trafficLights false、canEnableLights true。ただし隣の Basic 2871 は TooShort・SlopeTooSteep
- `junction_info`(-920,-857): 40m 以内に交差点なし(区間の途中)
- `net_near`(2302,-946 r120、-920,-857 r120、3130,-430 r90、-1640,-900 r110、-1640,-1140 r60、3449,-1555 r80): 区間の番号、種類、両端、長さ、車線
- `test_upgrade_road`(Small 4 Lane Road): [[2160,-950],[2280,-950]] は ObjectCollision(36011 9m、TooShort)で断られた。[[2236,-950],[2280,-950]]、[[2160,-950],[2220,-950]] も同じ。[[2220,-1050],[2220,-950]] は 29545 が断られる。[[3138,-490],[3138,-370]] は 2871(TooShort、SlopeTooSteep)と 2074(villa 1棟の取り壊し)。[[-1640,-965],[-1640,-785]] は matched 4、upgraded 4、cost 0。[[-1640,-1180],[-1640,-1100]] は matched 2、upgraded 2、cost 0。[[-920,-1010],[-920,-965]] は matched 1、upgraded 1、cost 0
- `test_upgrade_road`(Large Road): [[-920,-785],[-920,-920]] は、沿道の建物 15 棟(住宅 10、店 3、事務所 2)の取り壊しが要る(demolish=false で skipped)
- `list_net_types`(Road): Basic Road と Small 4 Lane Road は、どちらも 5,000/km、維持費 40/km。Large Road は 10,000/km、維持費 120/km
- `cargo`: stoppedInBuildings 632(28755 が 631)、noGoods 227、stoppedOnRoads 345。28755 は (3449,-1555) の Cargo Center
- `vehicles_stuck`(truck, building=28755): 777 台。WaitingSpace+Importing+InGrounds 630 台が敷地の中で空きを待つ。道の上で止まったのは 85+12+47
- `zone_map`(x=2250, z=-950, r150): 2302 の周りは、道沿いに事務所と店が並ぶ
- `zone_map`(x=-920, z=-850, r120): 4車線の両側に住宅とオフィス、店が並ぶ

## 判断の根拠

- 21月の2か所のうち、信号 (2668,330) は 53→1 で効いた。x=-1640 は 41 で、目標40にあと1。残りの Basic 6区間は、同じ型で `test_upgrade_road` が通るので、案1にした(費用 0、取り壊しなし)
- 上位の止まり (2302,-946) 51 の Basic 3334 は、9m の Basic 36011 が差し替えを断る。差し替えの案は出せないため、同じ地点の信号を案2にした(試し。費用は道具の記載なしで、0と見込む)
- 案は2件。車線の残りと信号は別の手で、同じ道の言い換えではない。調査は、x=-920 の止まりの原因が上流か下流かを決める
- 28755 の道は詰まっていない(blocked 0)。止まりは敷地の中の空き待ちで、道の手は効かない。8-1 は港湾空港局の振り分けの試しに任せる(計画の調整5)

## 捨てたもの

- 上位 (2302,-946) の Basic 3334・19196 を Small 4 Lane にする: 9m の Basic 36011 が TooShort とぶつかりで断る。36011 を消すと、西へ抜ける道が切れるため出さない
- (3099,-471) の Basic 2871 を Small 4 Lane にする: 14m で TooShort、SlopeTooSteep。実行可否が未確認のため出さない
- (-920,-857) の4車線を Large Road に太くする: 沿道の住宅 10 棟、店 3 棟、事務所 2 棟、計 15 棟の取り壊しで、家と働き口を失う。調査の結果を待つ
- 3138 の Basic 2074 を Small 4 Lane にする: villa 1 棟の取り壊しが要る。上の 2871 が断られるため、効かない区間を広げるだけになる
- 政策 HeavyTrafficBan: 費用 0 だが、トラックを道から締め出し、noGoods 227 と 28755 の運びに響く。6-4・8-1 と逆になるため出さない
- 28755 の道の混み対策: 道の blocked は 0。敷地の中の空き待ちに道路の手は効かないため出さない
