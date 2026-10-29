# m14 道路下水道局の案

## 案1: 名所 40850 の入口へ南回りの道をつなぐ

### 施策

- 案の id: roads-1
- 施策: 名所 40850(Servicing Services、(1580,-530))の RoadNotConnected を解く。東の道の端 (1640,-530) から南回りを引き、入口へつなぐ
- 議決: 要らない

### 実行計画

- 実行可否: 未確認
- 対象と操作順: (1) `build_line`、prefab "Basic Road"、points [[1640,-530],[1640,-590],[1600,-595]]。端 (1640,-530) は既存の node 25279(東の道、segment 30876)につながる。(2) 入口への支線: 位置と向きが未確認のため、まだ決めない。(1) は (2) の位置が確かめられてから実行する
- 設置条件の確認: `test_build_line`(同じ points、prefab "Basic Road")は ok、segments 2、cost 520、overlaps []。`net_near`(1600,-530、r200)で東の道 segment 30876 の端が (1640,-530) と確認。40850 の外形は、`test_build_line` の overlaps で width 96、length 104、angle 90(推定の範囲は x 1532〜1628、z -582〜-478)。`test_place_building`(Servicing Services、(1580,-530)、assume_removed_buildings [40850])は AlreadyExists で、入口の位置と向きは返らない。入口の向きは未確認
- 再調査の結果: 満たせず。条件の入口の位置と向きは、道具で確かめられなかった。`test_place_building`(Servicing Services、(1580,-530)、facing south / west / north、assume_removed_buildings [40850])は、どの向きも AlreadyExists で、入口は返らない。`buildings_near`(1580,-530、r30)の ports も空。`zone_map`(1580,-530、r150)で見ると、40850 の西と南に道はなく、支線の取り付け先も確かめられない。`net_reach`(1580,-530、r200)の badBuildings は 40850 の1件のまま。支線の経路を引けないため、全経路の `test_build_line` も確かめられない。実行可否は未確認のまま、採らない
- 接続工事: 支線(入口から南回りの末端 (1600,-595)、または東の道の端への短い支線)。入口の位置が決まるまで、長さと費用は未確認
- 予備候補: なし
- 中止する条件: 入口の位置と向きが確かめられないなら、(1) を引かない。支線の `test_build_line` が断られたら、案をやめる。第15月末まで印が残るなら、名所の道をやめる(事業2)

### 期待する効果

- 改善の見込み: 40850 は RoadNotConnected のため、Visitors が週5、観光客が週2しか入らない。道がつながると観光客が名所に入り、5-1・5-2 の Tourism が増えると予想する。量は見積もれない
- 数値と期限: 今の値は、`buildings_near`(1580,-530、r30)で problems が RoadNotConnected、Visitors last week 5、Tourists last week 2。期限は道が通った月の月末(第15月末)。RoadNotConnected が消えることを判定の条件にする
- 確認方法: `buildings_near`(x 1580、z -530、radius 30)の problems と stats(Visitors、Tourists)。`net_reach`(x 1580、z -530、radius 300)の badBuildings(40850 の reachable)
- 不確かな点: 入口の位置と向きが未確認。入口の道が未確認のまま、南回りだけでは道がつながらないおそれがある。効きの量は見積もれない
- 試し: なし(観光の名所は 11月の economy-1 で、周りの attractiveness が上がることを確認済み。道がないことが観光客を止めている)

### 費用

- 建設費: 520(南回り 104m、`test_build_line` で確かめた)。支線の費用は未確認
- 週の維持費の増え分: 4.2(104m × 40/km/週。`list_net_types` の Basic Road)

### 戻せるか

戻せる。道は `remove_line` で消せるが、取り壊しの議決が要る。

### 前の月の答え合わせ

- 13月の案 roads-2(東の道 (1703,-536)→(1640,-530)、320)は採られ、実行できた。判定: 外れ。RoadNotConnected は残り、道の端が名所の外形から約12m離れていた。理由: 道の端を建物の外形に届かせる一方、入口の向きを確かめていなかった。今月の案で、入口の向きを先に確かめる条件にした
- 13月の案 roads-1(信号 (1536,-114))は採られ、実行できた。判定: 当たり。`traffic`(x 1536、z -114、r 150)の blocked が 51 から 30 へ下がった(2051-02-05 の月末)

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる(重点1)

## 案2: 交差点 (-1640,-1100) に信号を置く

### 施策

- 案の id: roads-2
- 施策: 交差点 (-1640,-1100)(node 31583)に信号を付ける。止まりの集まり (-1684,-1060) の blocked 56 に近い
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `set_traffic_lights`(x -1640、z -1100、active true)。1回だけ
- 設置条件の確認: `junction_info`(x -1640、z -1100)で node 31583、trafficLights false、customLights false、canEnableLights true。4方向の区間(36327、27480、33705、35101)は cars true
- 接続工事: 不要
- 予備候補: 交差点 (-1640,-1010)(node 21887、`junction_info` で trafficLights false、canEnableLights true)。(-1640,-1100) が断られたときだけ、`set_traffic_lights`(x -1640、z -1010、active true)
- 中止する条件: `junction_info` で canEnableLights が false になっていたら、予備へ移る。両方とも false なら、案をやめる

### 期待する効果

- 改善の見込み: 13月の信号 (1536,-114) で blocked が 51 から 30 へ下がった。同じ手で、止まりの集まり (-1684,-1060) の blocked が下がると予想する。量は見積もれない
- 数値と期限: 今の値は `traffic`(x -1684、z -1060、r 150)の blocked 62(cars 116、congestion 56)。判定は第15月の月末
- 確認方法: `traffic`(x -1684、z -1060、radius 150)の blocked と congestion。同じ範囲で見回り1・見回り2・月末に測る(調査と同じ)
- 不確かな点: 信号の効きは測るたびに揺れた(2257・3297 の調査では下がらなかった)。(-1640,-1010) と (-1640,-1100) の両方の影響が混ざる。週の維持費は未確認
- 試し: なし(13月の信号が効いた同じ手)

### 費用

- 建設費: 0(13月の案 roads-1 の信号は、実行時の費用が 0 だった)
- 週の維持費の増え分: 未確認(信号の週の維持費は、city_info の週の収支の差で確かめる)

### 戻せるか

戻せる。`set_traffic_lights` で active false にすれば外せる。

### 前の月の答え合わせ

13月の2件(東の道、信号 (1536,-114))の判定は、案1の「前の月の答え合わせ」に書いた。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たらない(重点の外。長期計画の事業1の次の一手)

## 調査

- 調査: あり
- 問い: 信号 (-1640,-1100) を置いたあと、止まりの集まり (-1684,-1060) の blocked は下がるか
- 見る道具と引数: `traffic`(x -1684、z -1060、radius 150)
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 月末で基準 62 より下がれば、15月に次の交差点 (-1640,-1010) を案にする(canEnableLights 確認済み)。上がれば、信号を外す(`set_traffic_lights` で active false)。見回りの揺れが大きければ、月末の値で判定する
- 担当の問題: 6-3 公共交通を主軸とした交通体系

## 見たもの

- `city_info`: 人口178,202、所持金2,419,253、週の収支+3,922(収入338,692、支出334,770)、観光客1,847(訪問143)、来ない市民 0/0/0、dialog なし。週の収支は1月(12,404)、2月(3,922)と2か月続けて下がった
- `list_policies`: policyExpensesPerWeek 10,594。観光と交通に関係する政策は、RecreationalUse(無効、0)、SmallBusiness(無効、315)、HeavyTrafficBan(無効、0)、BigBusiness(有効、3,948)、EducationBoost(有効、7,940)。RecreationalUse は4月に外した後も attractiveness が動かず、SmallBusiness は Tourism の効きを切り分けられていない。HeavyTrafficBan は13月に採らなかった(品物がない店を悪化させるおそれ)。今月は、道と信号の手が政策より担当の数字に直接効くと判断した
- `buildings_near`(1580,-530、r150):名所 40850(Servicing Services)は problems RoadNotConnected、grid の電気・水・下水は true、Visitors last week 5、Tourists last week 2。周りは事務所・店
- `buildings_near`(1580,-530、r400、problem RoadNotConnected):40850 の1件だけ
- `net_reach`(1580,-530、r300):badBuildings は 40850 の1件(reachable false、canLeave false)。道の37区間は notEnterable 0
- `traffic`(街全体):flow 52、cars 7,446、blocked 873、congestion 2,357。blockedSpots は (-1684,-1060) 56、(1710,97) 46、(3122,-306) 44、(2068,279) 38、(2255,284) 37
- `traffic`(x -1684、z -1060、r150):blocked 62、cars 116、congestion 56。blockedSpots (-1684,-1060) 56
- `traffic`(x 1710、z 97、r150):blocked 50。blockedSpots (1710,97) 46
- `junction_info`(1536,-114):trafficLights true(13月の信号)、customLights true
- `junction_info`(-1640,-1100):node 31583、trafficLights false、canEnableLights true
- `junction_info`(-1640,-1010):node 21887、trafficLights false、canEnableLights true
- `junction_info`(1710,100):node 17442(1692,100)、trafficLights false、canEnableLights true
- `net_near`(1600,-530、r200、Road):東の道 segment 30876(1703,-536)→(1640,-530)、長さ45。Medium Road の南北幹線(x 1699〜1711)
- `net_near`(-1660,-1040、r80、Road):x -1640 の南北道(z -920〜-1164)と東西道(z -1010、-1100)
- `zone_map`(1600,-530、r250):名所の外形の東の端(約1628)と、道の端(1640)の間に約12m の空きがある
- `test_place_building`(Servicing Services、(1580,-530)、assume_removed [40850]):AlreadyExists(入口の情報は返らない)。facing east、(1580,-528) でも同じ
- `test_build_line`(Basic Road、[[1640,-530],[1624,-530]]):overlaps 40850(width 96、length 104、angle 90)
- `test_build_line`(Basic Road、[[1640,-530],[1640,-590],[1600,-595]]):ok、segments 2、cost 520、overlaps []
- `test_build_line`(Power Line、[[3250,-1420],[3237,-1293]]):ok、segments 2、cost 320、overlaps []。港湾空港局に渡す
- `list_net_types`(Road、Power Line):Basic Road 5,000/km、40/km/週。Power Line 2,500/km、60/km/週

## 判断の根拠

- 案1 は、重点1(5-1、5-2 観光)の名所 40850 が、道がないため Visitors 週5のまま動かないことを根拠にした。南回りの test は ok(520)で、週 4.2 は道の枠 12 に収まる。入口の位置と向きは道具で確かめられないため、実行可否は未確認にした。確かめられるまで、道は引かない
- 案2 は、13月の信号が効いた(51→30)のと、(-1640,-1100) の canEnableLights が true で置けることを根拠にした。6-3 は編成方針の重点の外だが、長期計画の事業1の次の一手で、交通の流れ 52% を 60% に近づける手
- 案の数を2件にした理由: 観光の道(案1)と、交通の信号(案2)は別の手。ほかの候補は、確かめられていないか、次の月に回す事業のため、件数を埋めない
- 電線の直線 (3250,-1420)→(3237,-1293) は test ok(320)。道路下水道局の案には入れず、結果を港湾空港局に渡す(調整4)
- 週の収支は +3,922 で守る線 +3,000 の上に残る。案1 の 4.2 を入れても +3,918 程度。ただし、2か月続けて下がっているため、15月にもう一度下がると下降規則の対象になる

## 捨てたもの

- 名所 40850 の東の道の延長(1640→1624 の区間): test_build_line で、建物の外形に重なると断られた。外形の手前まで道を伸ばす案は作れない
- 南回り 1,320(経済観光文化局の経路の概算): test で 104m(520)の経路が確かめられたため、長い経路は出さない
- 信号 (1710,97)(blocked 46): 交差点 (1692,100) は canEnableLights true。ただし、15月の判定で次に出す予備とし、今月は1つだけにした(案2)
- 信号 (-1640,-1010): 案2 の予備。両方を同時に置くと、同じ手の2件になり、効きが混ざるため出さない
- 2257・3297 周りの手: 長期計画の17月に回す。13月の調査の結果が、まだ1回の測りだけのため
- 太くする手(Large Road): 13月に、医療所 10289 と電柱にぶつかるため採らない
- HeavyTrafficBan: 13月に採らない(品物がない店を悪化させるおそれ)。今月も、6-4・7-1 と合わせて採らない
