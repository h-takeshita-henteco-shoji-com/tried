# m17 道路下水道局の案

## 案1: 交差点 (2155,330) に信号を置き、東の止まりを減らす

### 施策

- 案の id: roads-1
- 施策: 交差点 node 4709(2155,330)に `set_traffic_lights`(x 2155、z 330、active true)で信号を付ける。信号のない3叉で、止まりの集まり (2256,296) blocked 37 の西側にある。市の計画 6-3
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `set_traffic_lights` x=2155, z=330, active=true。2. `junction_info`(x 2155, z 330)で trafficLights が true になったことを確かめる
- 設置条件の確認: `junction_info`(2155,330): trafficLights false、customLights false、canEnableLights true、3本の Small 4 Lane Road(segment 1374、3990、18)。`traffic`(x 2256, z 296, r 150): blocked 55、flow 52(基準)
- 接続工事: 不要
- 予備候補: なし(交差点が1つに決まっている)
- 中止する条件: 実行前の `junction_info` で canEnableLights が false、または trafficLights が既に true なら見送る

### 期待する効果

- 改善の見込み: (2256,296) の止まり 37 と、(2135,302) の 10 は、この交差点の東と西にある。信号で待ちを時間で分ける見込み。16月の信号 (1692,100) と同じ型で、blocked が下がると予想する
- 数値と期限: `traffic`(x 2256, z 296, r 150)の blocked。今の値 55(5/6)。予想は下がること(量は見積もれない)。判定は18月末
- 確認方法: `traffic`(x 2256, z 296, r 150)を見回り1と月末に測る。同じ範囲・同じ半径で比べる
- 不確かな点: 14月の信号 (-1640,-1100) は 1→8→33 と揺れた前例がある。量は見積もれない。信号の週の維持費は道具で見えない
- 試し: なし(同型の信号で効きが出ている)

### 費用

- 建設費: 0(実行時に所持金の差0を確かめる)
- 週の維持費の増え分: 未確認(道具で見えない)

### 戻せるか

戻せる。`set_traffic_lights` で active を false にすれば外せる。

### 前の月の答え合わせ

前の月の案 roads-1(m16-2、交差点 (1692,100) の信号)は採られ、実行できた。期待は blocked 64→25〜45(r100)。結果は 6〜17(5/6 は 17)で、r200 は 36(基準 102)。当たり。同じ型の信号を次の交差点に足す。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(港湾空港局と分け持ち)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1・5-2、8-1・6-4、4-4)。ただし 6-3 の目標に直接効く

## 案2: 送電線の網を、名所 11580 と公園 30466 につなぐ

### 施策

- 案の id: roads-2
- 施策: 孤立した送電線の端 node 4380(690,1640)を、網の端 node 17930(603,1533)へ、名所の北を通して引く。名所の西の縁に枝を1本引く。`build_line`(prefab "Power Line")を使う。市の計画 5-1、5-2 と 4-2
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み(線の試しが通った。電気が建物に届くかは、18月末の測りで確かめる。効きは「期待する効果」に書く)
- 対象と操作順:
  1. `build_line`(prefab "Power Line", points [[603,1533],[612,1600],[690,1640]])。`test_build_line` は ok、segments 3、crossings 0、cost 420、overlaps なし
  2. `build_line`(prefab "Power Line", points [[612,1575],[633,1575]])。`test_build_line` は ok、segments 1、cost 60、overlaps なし
  3. 18月末に `buildings_near`(x 712, z 1600, r 120)で、30466 と 11580 の grid.electricity を見る
- 設置条件の確認:
  - `net_near`(x 560, z 1480, r 250, Electricity): node 17930 は segment 13409 で、既存の網の node 24073 につながっている
  - `net_near`(x 712, z 1644, r 200, Electricity): segment 25434 は node 4380(690,1640)と node 17161(727,1626)をつなぐ。node 4380 は網につながっていない(connectedTo none の元の状態)。segment 25433 は長さ0
  - `buildings_near`(x 712, z 1644, r 200): 11580 StatueOfWealth(668,1565)と 30466 Regular Park(762,1600)とも electricity false、problems は Electricity
  - `zone_map`(x 700, z 1600, r 200): 名所の敷地は x 約637〜699、z 約1533〜1597(図から目測)。公園の敷地は x 約730〜793、z 約1564〜1635。新しい線は、どちらの敷地の中にも入らない
  - `test_build_line` で敷地の中に端を置く線は、ObjectCollision で断られた: (727,1626)→(748,1612)(公園)、(612,1585)→(652,1580)(名所)。敷地の縁の外で止める形にした
- 接続工事: 本線の費用 420、枝 60。週の維持費は 60/km/週(`list_net_types`)× 約0.19km で、約 +12
- 予備候補: 枝の端を名所の縁から2m外、(635,1575) に縮めて試す(`test_build_line` で確かめてから使う)。公園は、既存の端 node 17161(727,1626)が縁から3m。網につなげば届くかを見る。届かなければ予備はなし
- 中止する条件: 実行前の `test_build_line` が ok でなくなったら見送る。node 17930 が `net_near` で網から外れていたら見送る

### 期待する効果

- 改善の見込み: 網につながらない送電線(node 4380、17161)を、既存の網につなぐ。これで公園 30466 が電気を受ける見込み。名所 11580 は枝の先が届くかどうか未確認
- 数値と期限: `buildings_near` の grid.electricity。今は 30466 も 11580 も false(5/6)。予想は 30466 が true(見込み)、11580 は不確か。判定は18月末
- 確認方法: `buildings_near`(x 712, z 1600, r 120)で grid.electricity と problems(Electricity)を見る。月末に比べる
- 不確かな点: 電気が建物に届く距離と条件は道具で見えない。16月に、送電線の端 (727,1626) から敷地を避けて引いた経路は、建物に当たって断られた。数値は見積もれない
- 試し: 仮説は、網の端を公園の縁から3m以内に置くと、公園に電気が届く。名所は枝の端が縁から4m外で届く。測る数は `buildings_near` の grid.electricity(30466、11580)、場所 (712,1600)、基準は両方 false。編成方針の「分からないこと」の名所と公園の電気の項目

### 費用

- 建設費: 480(本線 420 + 枝 60。`test_build_line` の cost)
- 週の維持費の増え分: 約 +12(`list_net_types` の upkeepPerWeekPerKm 60 から計算)

### 戻せるか

戻せる。線は `remove_line` で外せるが、取り壊しの議決が要る。

### 前の月の答え合わせ

前の月(16月)の送電線の経路は、起点を送電線の端 (727,1626) にして、敷地を避ける経路を試し、どれも建物に当たって断られた(計画の 16月の記録)。今月は起点を網の端 (603,1533) に変え、名所の北を通す経路で、試しが通った。前の月の案は採られていないため、答え合わせは「なし(採られなかった)」。

### 市の計画

- 当たる施策: 5-1、5-2 観光(名所 11580 の電気)、4-2 花や緑による潤い(公園 30466 の電気)
- 編成方針の重点に当たるか: 当たる(重点1: 5-1、5-2 観光)

## 案3: 政策 FreeTransport を外し、運賃収入を戻す

### 施策

- 案の id: roads-3
- 施策: `set_policy`(name "FreeTransport", active false)。16月の試しを、乗客と流れが動かなかったため戻す。市の計画 6-3(流れの試し)
- 議決: 要らない(`set_policy` は議決の種類に入らない)

### 実行計画

- 実行可否: 確認済み(`list_policies` で FreeTransport は active true、costPerWeek 0)
- 対象と操作順: 1. `set_policy`(name "FreeTransport", active false)。2. 翌月に `economy_breakdown` の PublicTransport 収入が 0 から約 4,800 に戻ったかを見る
- 設置条件の確認: 該当なし(政策の変更のみ)
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: 実行前に `list_transport_lines`(bus)の passengersLastPeriod の合計が、今の約4,850 より増えていたら、効きが出た見込みとして見送る

### 期待する効果

- 改善の見込み: 戻しても、流れと乗客は大きく変わらないと予想する。16月の試しで、乗客は約5,040→約4,850、流れは 53→52 で、無料の効きは見えなかった。戻すと、運賃収入が約4,800 戻る(財政の数字であり、局の目標ではない)
- 数値と期限: `economy_breakdown` の PublicTransport 収入 0 → 約 4,800(18月末)。`traffic` の flow 52(変化なしを予想)
- 確認方法: `economy_breakdown`(PublicTransport)、`list_transport_lines`(bus)の passengersLastPeriod 合計、`traffic` の flow。今の値と同じ道具で比べる
- 不確かな点: 運賃を戻すと、乗客が減るかどうか。量は見積もれない。乗客の合計は目で足した概算(約4,850)
- 試し: なし(戻しの判断は、16月の試しの結果を受けたもの)

### 費用

- 建設費: 0
- 週の維持費の増え分: 0(運賃収入は約 +4,800 戻る見込み)

### 戻せるか

戻せる。`set_policy`(name "FreeTransport", active true)で再びかけられる。

### 前の月の答え合わせ

前の月(16月)の FreeTransport(m16-4、財政局の試し)は外れ。予想は乗客が増え流れが上がること。結果は乗客約5,040→約4,850、流れ 53→52、運賃収入 4,796→0、週の収支 +12,150→+7,468。今月は、その結果を受けた戻しの案。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系
- 編成方針の重点に当たるか: 当たらない(流れの効きは見えず、担当の数字に効く見込みは小さい)

## 調査

- 調査: あり
- 問い: 交差点 (2155,330) の信号のあと、(2256,296) 付近の止まりは、Medium Road(x 2200、z 182〜298)の密度100の区間から来ているか。信号の後も残るか
- 見る道具と引数: `traffic`(x 2200、z 260、radius 120)、`traffic`(x 2256、z 296、radius 150)
- いつ見るか: 見回り1・月末
- 何が分かれば次の手が決まるか: 信号の後も、x 2200 の範囲の blocked が 30 以上なら、Medium Road を Large Road に太くする案を出す(`test_upgrade_road` で確かめる)。10 未満なら、信号の効きとして事業1を続け、太くしない
- 担当の問題: 6-3 公共交通を主軸とした交通体系

## 見たもの

- `city_info`: 人口 175,864、所持金 2,502,262、週の収支 +7,468、観光客 1,875(訪問158)、来ない市民 0/0/0、dialog なし、需要 住26/商2/工45
- `list_policies`: 有効は SmokingBan、EducationBoost(週 7,940)、FreeTransport(週 0、運賃収入 0)、BigBusiness(週 3,888)。SmallBusiness、RecreationalUse、HeavyTrafficBan は無効。政策の費用合計 10,766/週
- `traffic`(全体): flow 52、cars 7,332、blocked 845、congestion 2,263。busiest は Basic Road の density 100 が並ぶ。blockedSpots 上位は (2256,296) 37、(694,-703) 36、(-1093,-686) 34、(2704,-502) 30
- `traffic`(x 2256, z 296, r 150): flow 52、blocked 55、congestion 44。blockedSpots は (2256,296) 37、(2135,302) 10、(2204,173) 8。busiest は Medium Road(x 2200、z 182〜298)が density 100
- `traffic`(x 694, z -703, r 150): blocked 40、blockedSpots (694,-703) 36
- `junction_info`(2648,691): 40m以内に交差点なし(計画の候補は使えない)
- `junction_info`(2200,298): 40m以内に交差点なし
- `junction_info`(2200,330): trafficLights true、customLights false(自動の信号。ほかの手を足す余地なし)
- `junction_info`(2175,330): 40m以内に交差点なし。`junction_info`(2155,330) は node 4709、trafficLights false、canEnableLights true、canSetYield true
- `junction_info`(2699,303): 交差点なし。`junction_info`(2700,330): trafficLights true(既存の信号)
- `junction_info`(694,-703): node 19677、trafficLights true(自動)、customLights false
- `junction_info`(-1093,-686): 40m以内に交差点なし
- `buildings_near`(x 712, z 1644, r 200): 11580 StatueOfWealth(668,1565)、30466 Regular Park(762,1600)。どちらも electricity false、water false、sewage false
- `buildings_near`(x 2256, z 296, r 120, brief): 近くの店と住宅。problems は None が多い(4214 は NoGoods)
- `net_near`(x 712, z 1644, r 200, Electricity): segment 25434(node 4380 (690,1640) — 17161 (727,1626))、25433(長さ0)、13409(603,1533)-(560,1480)
- `net_near`(x 560, z 1480, r 250, Electricity): 既存の網。node 17930 は segment 13409 で 24073 につながる
- `zone_map`(x 700, z 1600, r 200, size 600): 名所と公園の敷地、道(x 約709〜717)、送電線(橙)の位置
- `list_net_types`(Electricity): Power Line costPerKm 2,500、upkeepPerWeekPerKm 60
- `test_build_line`: Power Line 3本(本線 ok、枝 ok、名所の縁の中に端を置く線は ObjectCollision、公園の縁の中に端を置く線は ObjectCollision)
- `test_build_line`(Power Line、(727,1626)→(728,1600)→(726,1585)): ObjectCollision(30466)
- 呼んでいない道具: `economy_breakdown`、`list_transport_lines`(数字は 17月の mayor-note の値を使った。道具では今回確かめていない)

## 判断の根拠

事業1の規則に沿い、次の交差点を (2155,330) に決めた。計画の候補 (2648,691) は交差点がなく、blocked の上位は自動の信号か交差点なしで、案にできなかった。事業2は、18月末までの期限の前に、網の端からの経路が試しで通ったので案にした。FreeTransport は 16月の試しで外れが出たので、戻す案として出した。3案は別の手で、件数は効きが見込める3つに絞った。4件目の候補は、道を太くする案(Medium Road)で、今月は測っていないため調査に回した。

## 捨てたもの

- 交差点 (2648,691): 40m以内に交差点がない。計画の候補が存在せず、取り下げた
- 交差点 (694,-703) と (2200,330): 自動の信号が既に付いている。`set_traffic_lights` で足す手がない。流れ(blocked 36)の原因は調査の対象外
- 交差点 (-1093,-686): 40m以内に交差点がない
- 名所の枝を敷地の中へ入れる案: `test_build_line` で ObjectCollision。敷地の縁で止める形に変えた
- 政策 HeavyTrafficBan(無効、費用0): 交通の流れに効く見込みがあるが、トラックを締め出すと、品物がない店と原料がない工場(6-4、8-1)が悪化する懸念がある。効きも未測定のため、今月は出さない
- Medium Road(x 2200)の Large Road への差し替え: 今は測定が足りないため、調査で見てから決める
- 事業3(旅客の入口の道と電線): 駅が置かれていない(旅客の入口0、港湾空港局の案待ち)
