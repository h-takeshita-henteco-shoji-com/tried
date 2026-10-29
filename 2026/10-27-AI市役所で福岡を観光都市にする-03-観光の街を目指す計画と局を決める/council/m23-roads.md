# m23 道路下水道局の案

## 案1: 止まりの2番目 (2082,-840) の Basic 3組を Small 4 Lane にする

### 施策

- 案の id: roads-1
- 施策: 交差点 (2110,-840) の西と南の Basic 道を、Small 4 Lane に差し替える(止まりの中心は (2082,-840)、6-3 の交通の流れ)。道路下水道局の案1
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `upgrade_road` prefab="Small 4 Lane Road", points=[[1957,-840],[2033,-840],[2110,-840]](区間 11482、28251 を差し替え)
  2. `upgrade_road` prefab="Small 4 Lane Road", points=[[2110,-705],[2110,-750],[2110,-795],[2110,-840]](区間 21607、20648、17090 を差し替え)
  3. `upgrade_road` prefab="Small 4 Lane Road", points=[[2110,-840],[2160,-880]](区間 9298 を差し替え)
  - 3つとも demolish は付けない(沿道の建物は壊れない)。pay は既定(費用は 0)
- 設置条件の確認:
  - 1: `test_upgrade_road` で matched 2、upgraded 2、skipped 0、demolishedBuildings なし、cost 0
  - 2: `test_upgrade_road` で matched 3、upgraded 3、skipped 0、demolishedBuildings なし、cost 0
  - 3: `test_upgrade_road` で matched 1、upgraded 1、skipped 0、demolishedBuildings なし、cost 0
  - 交差点 (2110,-840) は `junction_info` で、信号なし、canEnableLights true
- 接続工事: 不要(同じ幅の差し替えで、つながりは変わらない)
- 予備候補: 区間 34428 (2033,-750)→(2110,-750) を Small 4 Lane に。`test_upgrade_road` で matched 1、upgraded 1、skipped 0、cost 0 を確認済み。1〜3 のどれかが実行で断られたときに使う。使うなら `upgrade_road` prefab="Small 4 Lane Road", points=[[2033,-750],[2110,-750]]
- 中止する条件: 実行前に、いずれかの点で `test_upgrade_road` が skipped や demolishedBuildings を返したら、その区間だけを外す。3区間のどれも通らなければ案1を止める。23月末の基準 (2082,-840) r200 の blocked が 35 より増えていたら、差し替えの前に止めて測り直す

### 期待する効果

- 改善の見込み: (2082,-840) の止まりは、東へ流れる Basic 道の1車線が詰まるために起きている。2車線の Small 4 Lane にすれば、この流れが速くなり、止まりが減ると予想する。確認した事実は、今月の (2082,-840) r200 の blocked 35(spot 22)と、この交差点の3本が Basic で密度 100 であること。
- 数値と期限: 基準は `traffic`(x=2082, z=-840, radius=200)の blocked 35(23月末)。予想は 20 以下。期限は第24月末(2回目の測り)。流れの % は、今の 52 から動くかを見る(数値は見積もれない)
- 確認方法: `traffic`(x=2082, z=-840, radius=200)の blocked と busiest。同じ範囲で、23月末の 35 と比べる。街全体の flow も併せて見る(52%)
- 不確かな点: 止まりが西の Basic 区間(x=1957〜2033)から来ているか、交差点の先の Medium 道(7043、20169)の詰まりに移るかは、測って確かめる。(2108,-840) の止まりが15あるため、移ったときは次の月に続きを見る
- 試し: なし

#### 前の月の答え合わせ

- 22月の案 roads-1(x=-1640 の残り Basic 6区間を Small 4 Lane、m22-2): 採られ、実行 ok。予想は (-1640,-1000) r200 の blocked を 41 から 40 以下。23月末の測りは 30。当たり。
- 22月の案 roads-2(交差点 (2236,-950) に信号、試し、m22-3): 採られ、実行 ok。予想は (2302,-946) r150 の blocked 51 が減る。23月末の測りは 0(その範囲の blocked の上位は (2108,-840) に移り、r200 で 15)。当たり。ただし止まりは次の場所へ移ったので、案1で続きを見る。

### 費用

- 建設費: 0(3区間と予備1区間とも、`test_upgrade_road` の cost 0。Basic と Small 4 Lane は 5,000 / km)
- 週の維持費の増え分: 0(Basic と Small 4 Lane は 40 / km / 週。延長は変わらない)

### 戻せるか

戻せる。`upgrade_road` で Basic Road に戻せる。取り壊しは含まない。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ 52%、目標 60%以上)
- 編成方針の重点に当たるか: 当たる(重点3。6-3 の止まりの上位)

## 案2: 止まりの1番目 (3092,-477) の交差点 (3130,-490) に信号を付ける(試し)

### 施策

- 案の id: roads-2
- 施策: 交差点 (3130,-490) に信号を付ける。Small 4 Lane(7711、東から)と Basic(2871、北東へ)の交差点で、(3092,-477) の止まり(44)の上流
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `set_traffic_lights` x=3130, z=-490, active=true
  2. `junction_info` x=3130, z=-490 で、trafficLights が true になったかを確かめる
- 設置条件の確認:
  - `junction_info`(3130,-490): node 9088、trafficLights false、customLights false、canEnableLights true。入る区間は 7711(Small 4 Lane、bearing 270)と 2871(Basic、bearing 37)の2本
  - 差し替え(差し替えの試し)は、この2本で断られた。2871 は TooShort、SlopeTooSteep。よって信号を先に試す
- 接続工事: 不要
- 予備候補: 交差点 (3145,-390) の node 4963(3本の交差点。区間 2074、26243、16182)。`junction_info` で trafficLights false、customLights false、canEnableLights true を確認済み。使うなら `set_traffic_lights` x=3145, z=-390, active=true
- 中止する条件: 実行前に `junction_info`(3130,-490)の canEnableLights が false、または入る区間が2本から変わっていたら、予備候補に替える。実行後に trafficLights が true にならなければ止める

### 期待する効果

- 改善の見込み: 止まりの上位 (3092,-477) は、7711 から交差点へ入る車が、2871 の1車線で詰まっている。信号で入る順番を分ければ、この交差点の流れが整うと予想する。確認した事実は、(3092,-477) r200 の blocked 56(spot 44)と、(3015〜3089,-490) の4車線の密度 100。ただし、差し替えを断る2871 の長さの制約は残るので、効きは限られる見込み。
- 数値と期限: 基準は `traffic`(x=3092, z=-477, radius=200)の blocked 56(spot 44)(23月末)。数値は見積もれない。期限は第24月末。判定は、同じ範囲で 56 より減るか
- 確認方法: `traffic`(x=3092, z=-477, radius=200)の blocked と blockedSpots。`junction_info`(3130,-490)の trafficLights
- 不確かな点: 2本だけの曲がった交差点に信号を付けても、流れが整うかは確かめられていない。効かなければ、信号は外す(`set_traffic_lights` active=false)。根本の2871 の14m は差し替えられず、取り壊し(villa 1182、住宅3戸以上)を伴う案は今月出さない
- 試し: 効き目が分からないので試しにする。
  - 仮説: 信号で 7711 と 2871 の入る順番を分ければ、(3092,-477) の止まりが減る
  - 測る数: `traffic`(x=3092, z=-477, radius=200)の blocked と、spot 44 の値
  - 場所: (3092,-477) 周辺。範囲は 200m
  - 基準: 23月末の blocked 56、spot 44
  - 編成方針の「分からないこと」のうち、6-3 の止まりの上位の原因に当たる

#### 前の月の答え合わせ

- 案2は、前の月の案の続きではない。22月の信号の答え合わせは案1の欄に書いた。

### 費用

- 建設費: 0(`set_traffic_lights` は建設費がかからない)
- 週の維持費の増え分: 0

### 戻せるか

戻せる。`set_traffic_lights` active=false で外せる。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ 52%)
- 編成方針の重点に当たるか: 当たる(重点3。6-3 の止まりの上位)

## 案なし

(案1と案2があるため、この見出しは書かない)

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口172,759、所持金2,672,278、週の収支+7,746、観光客2,020(訪問179)、来ない市民 0/0/0、幸福度87(23月の数字と同じ)
- `list_policies`: 有効 SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,052)。不活性で関係しそうなもの HeavyTrafficBan(0。トラックを止める政策。8-1 の止まりと 6-4 の品物がない店を悪くするおそれがあるので、今月は採らない)、FreeTransport(0。運賃が0になる)。政策の合計 policyExpensesPerWeek は 10,794
- `traffic`(街全体, limit 10): flow 52、cars 7,630、blocked 625、congestion 2,101。blockedSpots 上位は (3092,-477) 44、(1083,95) 28、(2082,-840) 22
- `traffic`(x=-1640, z=-1000, radius=200): flow 52、blocked 30、blockedSpots (-1635,-839) 11、(-1528,-1101) 9
- `traffic`(x=2302, z=-946, radius=150): blocked 0(前の月は 51)
- `traffic`(x=3092, z=-477, radius=200): blocked 56、spot (3092,-477) 44、(2958,-492) 12。busiest 6051、7711、16182、2871、1297、2074 がすべて density 100
- `traffic`(x=1083, z=95, radius=200): blocked 48、spot (1083,95) 28
- `traffic`(x=2082, z=-840, radius=200): blocked 35、spot (2082,-840) 22、(1968,-841) 7、(2107,-778) 6
- `traffic`(x=2236, z=-950, radius=200): blocked 16、spot (2108,-840) 15
- `net_near`(x=3120, z=-400, radius=130, Road): 区間 2871 と 16182 は Basic で長さ 14m、2074 は Basic で長さ 68m、7711 と 6051 は Small 4 Lane
- `net_near`(x=2110, z=-840, radius=90, Road): 区間 11482(77m)、28251(67m)、17090(37m)、21607(35m)、20648(35m)、9298(41m)、34428(67m) は Basic
- `list_net_types`(service=Road, locked=false): Basic 5,000/km・40/週、Small 4 Lane 5,000/km・40/週
- `junction_info`(2236,-950): 信号あり、customLights true
- `junction_info`(3130,-490): node 9088、信号なし、canEnableLights true、入る区間 7711 と 2871
- `junction_info`(3145,-390): node 4963、信号なし、canEnableLights true、入る区間 2074、26243、16182
- `junction_info`(2110,-840): node 28064、信号なし、canEnableLights true、入る区間 17090、28251、9298
- `test_upgrade_road`(Small 4 Lane, [[3130,-490],[3145,-470],[3145,-390],[3162,-372]]): matched 3、upgraded 0。2074 は villa 1182 の取り壊しが要る、2871 と 16182 は TooShort、SlopeTooSteep
- `test_upgrade_road`(Small 4 Lane, [[3145,-390],[3080,-390],[3015,-390]]): matched 2、upgraded 2、cost 0
- `test_upgrade_road`(Small 4 Lane, [[3145,-470],[3145,-390]], demolish=true): matched 1、upgraded 1、demolishedBuildings 1182(L4 1x1 Villa04)
- `test_upgrade_road`(Small 4 Lane, [[2070,-750],[2110,-816],[2130,-856],[2194,-950]]): matched 2、upgraded 2、cost 0
- `test_upgrade_road`(Small 4 Lane, [[1957,-840],[2033,-840],[2110,-840]]): matched 2、upgraded 2、cost 0
- `test_upgrade_road`(Small 4 Lane, [[2110,-840],[2160,-880]]): matched 1、upgraded 1、cost 0
- `test_upgrade_road`(Small 4 Lane, [[2110,-705],[2110,-750],[2110,-795],[2110,-840]]): matched 3、upgraded 3、cost 0
- `test_upgrade_road`(Small 4 Lane, [[2033,-750],[2110,-750]]): matched 1、upgraded 1、cost 0
- `test_build_line`(Small 4 Lane, [[3130,-490],[3140,-440],[3145,-390]], 区間 2871、2074 と villa 1182 を除いて): ok false、overlaps 30792(L3 2x2)、12592(L3 1x1)、17931(L3 3x4)。取り壊しが要るので、今月は採らない
- `preview_bulldoze`(x=3145, z=-430, radius=25): buildings 1(17931、homes 3)、jobs 0、homes 3、power 影響なし
- `buildings_near`(x=3145, z=-430, radius=40, brief): 1182(Villa04)、7503、9536(Office04)、12592、17931
- `buildings_near`(x=2000, z=0, radius=5000, service=PublicTransport, brief): 15棟。Cargo Center、Cargo Harbor、Metro Entrance、Bus Depot、Cargo Harbor。旅客の駅・港・空港は0(入口0のまま。事業3は未着手)

## 判断の根拠

- 6-3 の交通の流れは 52% で、目標 60% から遠い。22月の2件は当たり。x=-1640 は 41 から 30 になり、(2302,-946) の信号は 51 から 0 になった。局所の手は当たり続けているので、続ける。
- 止まりの上位 (3092,-477) 44 は、差し替えの道具が断る。14m の stub(2871、16182)は TooShort と急な坂で、2074 は villa 1182 の取り壊しが要る。取り壊しは議決が要るうえ、残る14m の区間が詰まりを残す。そこで今月は、差し替えが通る2番目 (2082,-840) を案1にする。
- 案2は、(3092,-477) の上流の交差点に信号を付ける試しにした。効き目は分からないので、試しとして 56 と 44 を基準に測る。
- 2件にしたのは、1か所の予定を2件に直したため。理由は、(3092,-477) の差し替えが断られ、次の手を今月の試しで測るため。24月末で、どちらかが外れたら戻す。
- 案の数は2件。観光(5-1・5-2)の入口は駅が無いので、事業3は進められない。案は出さない。

## 捨てたもの

- 3092,-477 の差し替えと、2871・2074 を壊す案: 2871 と 16182 は 14m で、差し替えが TooShort と SlopeTooSteep で断られる。2074 の差し替えは villa 1182 の取り壊しが要り、2871 が残るので流れは変わらない。新しい道を (3130,-490) から (3145,-390) へ通す案は、`test_build_line` で建物3棟(30792、12592、17931。17931 は3戸)と villa 1182 にぶつかり、取り壊しの議決と住宅の損失が要る。今月は採らない。
- HeavyTrafficBan(政策、0): トラックの通行を止める。費用は0だが、8-1 の止まり(635)と 6-4 の品物がない店(215)を悪くするおそれがある。市の計画の7-1・6-4 と合わせて見直す。
- (1083,95) の差し替え(止まり28、Medium と Basic の区間): 同じ月に3か所目になり、1か所の予定を超える。24月に、案1の測りを見てから決める。
- 事業3(旅客の入口の道と電線): 駅が無いので、引けない。第24月末の駅の判定まで待つ。
