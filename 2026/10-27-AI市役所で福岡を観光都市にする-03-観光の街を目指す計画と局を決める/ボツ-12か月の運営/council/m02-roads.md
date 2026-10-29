# m02 道路下水道局の案

## 案1: 渋滞する基本道路を4車線に差し替える(西と東の2か所)

### 施策

- 案の id: roads-1
- 施策: 基本道路(Basic Road)の渋滞区間を、同じ維持費の Small 4 Lane Road に差し替える。西は x=2110 の南北区間と、(2110,-840) から (2160,-880) までの連絡。東は (3154,-381) から (3185,-161) までの区間。道具は `upgrade_road`。6-3 の流れを上げるのが狙い
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `upgrade_road(prefab="Small 4 Lane Road", points=[[2110,-570],[2110,-840]], tolerance=20, pay=true, demolish=false)`(西の南北区間。6本)
  2. `upgrade_road(prefab="Small 4 Lane Road", points=[[2033,-840],[2110,-840],[2160,-880]], tolerance=20, pay=true, demolish=false)`(西の連絡。2本)
  3. `upgrade_road(prefab="Small 4 Lane Road", points=[[3154,-381],[3162,-339],[3162,-278],[3174,-205],[3185,-161]], tolerance=20, pay=true, demolish=false)`(東。3本が差し替わり、2本は飛ばされる)
  4. 実行後に `traffic` で、下の確認方法の3地点を見る
- 設置条件の確認:
  - 1 は `test_upgrade_road` で matched 6、upgraded 6、skipped 0、cost 0、demolishedBuildings 0、zonesKept true
  - 2 は `test_upgrade_road` で matched 2、upgraded 2、skipped 0、cost 0、demolishedBuildings 0
  - 3 は `test_upgrade_road` で matched 5、upgraded 3、skipped 2(segment 12091 は TooShort、segment 16182 は TooShort と SlopeTooSteep)、cost 0、demolishedBuildings 0
  - 3 の飛ばされる2本は、差し替えられず、(3145,-274) 付近の詰まりが残る
  - `list_net_types` で、Basic Road と Small 4 Lane Road は同じ 5,000/km、40/週/km と確認
  - `traffic` と `net_near` で、対象の区間が Basic Road で density 100 と確認
- 接続工事: 不要。同じ幅の差し替えで、つながりと沿道の区画は保たれる(zonesKept true)
- 予備候補: なし。3 で飛ばされた2本は、今月は差し替えない
- 中止する条件: 実行前に `test_upgrade_road` を同じ引数で取り直し、upgraded の数が上の値より減った、demolishedBuildings が1以上、cost が0でなくなった、のいずれかなら見送る

### 期待する効果

- 改善の見込み: 6-3 の流れを上げる。m01 の roads-1(m01-2)は、1車線を4車線に替えたあと、blocked が 50→13、36→0 に減った。今も同じ型の詰まりがある。西 (2162,-721) r150 は blocked 71、東 (3160,-250) r200 は blocked 95 で、どちらも density 100 の基本道路が続いている。
- 数値と期限: 街の流れは今 52(目標60)。流れの予想値は見積もれない。見る数は、下の3地点の blocked で、見回り1、見回り2、月末に確認する。基準は (2162,-721) r150 が 71、(3160,-250) r200 が 95、(2138,-838) r80 が 26(西の連絡)
- 確認方法: `traffic` を、x=2162 z=-721 radius=150、x=3160 z=-250 radius=200、x=2138 z=-838 radius=80 で呼ぶ。blocked と busiest の density を、上の基準と比べる。街全体の flow は参考にする
- 不確かな点: 差し替えの効き目の量は見積もれない。流れが60に届くかも見積もれない。東の2本は差し替えられず、その近くの詰まりは残るかもしれない。8-1 の貨物駅の停滞には効かない(案の範囲外)
- 試し: なし

### 費用

- 建設費: 0(`test_upgrade_road` の cost 0。差し替えは計11本)
- 週の維持費の増え分: 0(Basic Road と Small 4 Lane Road は、どちらも 40/週/km)

### 戻せるか

戻せる。同じ幅の差し替えで、区画も沿道の建物も壊さない。必要なら Basic Road に戻せる。

### 前の月の答え合わせ

前の月の roads-1(m01-2)は採られ、成功した。西の (703,-600) r250 の blocked は 50→13、(2157,474) r120 は 36→0 に減った。今月の案は同じ型の手を、別の詰まりに当てたもの。前の月の roads-2(信号)は採られず、費用の確認が理由だった。今月は信号を出さない。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(港湾空港局と分け持つ)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2、4-4、8-1。6-3 は重点の外。重点の外の案として出す)

## 調査

- 調査: あり
- 問い: 貨物駅 28755 の敷地の中で空き待ちになっているトラック(509台)は、周りの道の混みで減らないのか、それとも敷地の出口そのもので詰まっているのか。
- 見る道具と引数: `vehicles_stuck`(kind="truck", building=28755, limit=3)、`traffic`(x=3449, z=-1555, radius=150)
- いつ見るか: 見回り1、見回り2、月末
- 何が分かれば次の手が決まるか: 空き待ちの数が減らず、traffic の blocked が周りで0のままなら、道の差し替えは効かないと判断し、敷地の出口の問題として港湾空港局に渡す。周りの道の blocked が増えて空き待ちが増えるなら、x=3495 の Small 4 Lane(segment 15733、22686)を Large Road に上げる案を、費用(維持費の増え分は +80/km/週)と合わせて出し直す。
- 担当の問題: 8-1 物流・人流のゲートウェイ(担当は港湾空港局。道路の面から見る)

## 見たもの

- `city_info`: 人口178,861、観光客1,633/144、所持金2,077,453、週の収支 +6,910、citizensWithoutService 0/0/0
- `traffic`(街全体): flow 52、cars 7,384、blocked 831(道の上 830)、blockedSpots 上位 (2162,-721) 41、(1678,90) 36、(3145,-274) 36、(2129,-843) 34
- `traffic`(x=2162 z=-721 r150): blocked 71、density 100 の基本道路が4本以上
- `traffic`(x=2130 z=-856 r80): blocked 30、density 100 の基本道路が3本
- `traffic`(x=3160 z=-250 r200): blocked 95、congestion 78、density 100 の基本道路と小型4車線
- `traffic`(x=3449 z=-1555 r150): blocked 0、cars 40(貨物駅の周りの道は詰まっていない)
- `traffic`(流れの比較に使う、街の空き): blockedSpots の上位と同じ地点
- `citizens_without_service`(type=sewage): residents 0
- `list_policies`: 取得できた。有効は EducationBoost(週 7,940、学校の維持費の25%)、RecreationalUse(0)、BigBusiness(週 3,920)。無効は HeavyTrafficBan(0)、FreeTransport(0。運賃収入が0になる)、SmallBusiness(309)ほか。交通に関係するのは HeavyTrafficBan と FreeTransport で、今月は案にしない
- `cargo`: trucks 2,056、stoppedTrucks 803(道の上 292、敷地の中 511)。Cargo Center 28755 が 509 台。stoppedSpots (3440,-1552) 58 台。28755 の vehiclesLeaving 764。shortages の noGoods 229
- `vehicles_stuck`(kind=truck, building=28755): vehicles 600、WaitingSpace+Importing+InGrounds 509、seenStopped 7日以上 483、path ready 599
- `net_near`(x=3449 z=-1555 r250、Road): 19本。貨物駅の西に Large Road(x=3400、3車線)、東に Small 4 Lane(x=3495)
- `net_near`(x=2162 z=-721 r120、Road): 15本。x=2110 の Basic Road(1車線ずつ)が南北に続く
- `net_near`(x=2125 z=-850 r70、Road): 6本。segment 9298(2110,-840)〜(2160,-880)と 28251(2033,-840)〜(2110,-840)が Basic Road
- `buildings_near`(x=3449 z=-1555 r60): Cargo Center 28755 だけ。ports は空、jobs workers 57
- `junction_info`(3495,-1565)、(3400,-1567): 40m 以内に交差点なし(道路の途中の点)
- `net_reach`(x=3449 z=-1555 r120): 通れない区間 0、通れない建物 0
- `transport_reach`: 28755 は outsideConnected true(viaLaneConnection)
- `zone_map`(x=3449 z=-1555 r150 size=500): 貨物駅の敷地は、おおよそ x 3417〜3481、z -1491〜-1618。両側に道
- `list_net_types`(service=Road、locked=false): Basic Road 5,000/km・40/週/km、Small 4 Lane Road 5,000/km・40/週/km、Large Road 10,000/km・120/週/km
- `test_upgrade_road`: 西 x=2110(6本、upgraded 6、cost 0)、西の連絡(2本、upgraded 2、cost 0)、東(5本、upgraded 3、skipped 2、cost 0)
- `test_build_line`: 貨物駅の西に stub (3416,-1540)→(3400,-1540) を試したが、敷地と重なるため断られた(overlaps 28755)

## 判断の根拠

確認した事実として、6-3 の流れは 52(目標60)で、基本道路の density 100 の区間に blocked が集まっている。西 (2162,-721) は71台、東 (3160,-250) は95台。どちらも同じ幅の差し替えで、建設費0、維持費の増え分0で直せると道具で確かめた。m01 の同じ型の差し替えが効いた前例もある。このため、案1に西と東の2か所をまとめた。同じ手(同じ幅の差し替え)を2か所に当てるので、件数は1件に抑えた。8-1 の貨物駅の停滞は、周りの道が空いている(blocked 0)ので道の太さが原因だと示せない。このため、案には入れず、調査で見る。案の数を1件にしたのは、ほかに費用と実行条件が確認できた手がないため。

## 捨てたもの

- 貨物駅 28755 の出口に道を足す(stub): 貨物駅の両側の道の間に余地がなく、`test_build_line` が敷地との重なりで断った。
- x=3495 の Small 4 Lane を Large Road に上げる: 維持費が 40→120/週/km と増える(+80/km/週)。空き待ちのトラックは道の上で止まっていないので、効く根拠がない。調査で確かめてから出す。
- HeavyTrafficBan(政策、無効、費用0): 大型トラックの市内通行を止める。商品を運ぶトラックが減り、届かない店 229 軒(目標120)をさらに悪くする。6-4、7-1 に反する。
- 信号を付ける(前月の roads-2 の再提出): 今月は費用を道具で確かめていない。来月に候補を調べ直す。
- (1678,90) の blocked 36 の地点: 西と東と同じ手で当てられるか、まだ確かめていない。来月の候補にする。
