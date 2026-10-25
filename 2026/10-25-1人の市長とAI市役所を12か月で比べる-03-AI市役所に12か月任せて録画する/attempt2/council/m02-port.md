# m02 港湾空港局の案

## 施策

- 施策: 貨物駅28755(3449, -1555)を `set_building_active` で一度止めて、すぐ動かし直す(試し)。止まった車の溜まりが解けるかを見る
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `cargo()` と `vehicles_stuck(kind="truck", building=28755, limit=30)` で、敷地の中で止まった車が520前後であることを実行の直前に確かめる
  2. `set_building_active(id=28755, active=False)`
  3. 時間を進めて(実行する市長の手順で半日〜1日)、`vehicles_stuck(kind="truck", building=28755, limit=30)` の車数を見る
  4. `set_building_active(id=28755, active=True)`
  5. 見回り1・見回り2・月末に `cargo()` の stoppedInBuildings と shortages.noGoods を測る
- 設置条件の確認:
  - `buildings_near(x=3449, z=-1555, radius=120)`: 28755 は Cargo Center、放棄なし、電気・水・下水あり、働き手58、使用中の車792。id が一致する
  - `transport_reach`: 28755 は train、outsideConnected true
  - `net_near(x=3449, z=-1555, radius=150, service="Road")`: 周りは Large Road(各向き3車線)と Small 4 Lane Road。出口は詰まっていない(先月の `traffic` で blocked 0)
  - 建設ではないので敷地・地形の確認は該当なし
- 接続工事: 不要
- 予備候補: なし。同じ型の Cargo Center 13893(3529, -1555)は車0台で効き目の対象外
- 中止する条件:
  - 実行直前に28755の敷地の中の止まった車が300未満なら、すでに解けているので打たない
  - 手順3で車数が減らず、noGoods が基準233から20以上増えたら、手順4を直ちに行って見送る
  - `set_building_active` が断られたら、打たずに終える

## 期待する効果

- 改善の見込み: 28755の敷地の中の520台は、WaitingSpace+Importing で道順 ready のまま30日動いていない。止めて動かし直すと車の割り当てが組み直され、溜まりが解ける可能性がある。確証はなく、解けない可能性もある
- 数値と期限: `cargo` の stoppedInBuildings は今521(28755が520)。予想は、解ければ250以下に、解けなければ変わらない。量は見積もれない。期限は月末(30日目)
- 確認方法: `cargo()` の stoppedInBuildingsTop(28755)と shortages.noGoods(今233)を、見回り1・2と月末に同じ条件で測る。`vehicles_stuck(kind="truck", building=28755)` の byState と bySeenStopped も見る
- 不確かな点: 止めると積んだ荷が捨てられるか、止まった車が消えずに残るかは分からない。止めた間に品物の入荷が途切れ、noGoods が一時的に増える恐れがある。止まる原因(空きが出ない理由)そのものは分からないので、解けても再び溜まるかもしれない
- 試し: 仮説は、駅の状態を一度リセットすると、空き待ちで固まった車が解放され、敷地の中の止まった車が減る。測る数は `cargo` の stoppedInBuildings(基準521)と 28755 の stoppedTrucks(基準520)、noGoods(基準233)。場所は貨物駅28755(3449, -1555)。編成方針の「分からないこと」の1つ目(貨物駅28755の敷地の中でトラックが止まる原因)に当たる

## 調査

- 調査: なし

## 費用

- 建設費: 0
- 週の維持費の増え分: 0(止めた間は下がり、戻せば元どおり)

## 戻せるか

戻せる。`set_building_active(id=28755, active=True)` で動かし直せる。

## 前の月の答え合わせ

先月は案なしで、調査 s01-1 だけ採られた。結果は次のとおり。
- 分かったこと: 28755の敷地の中の車は、月の間ずっと508〜520台が WaitingSpace+Importing で、道順 ready、blockCounter 0。同じ車が30日動かない。出口の道は詰まっていない(半径300の blocked 0〜1、密度25〜36)。同じ型の Cargo Center 7つは出入り0
- 次の手: 原因は道の外にあると見て、今月は駅を止めて動かし直す試しを出す

## 市の計画

- 当たる施策: 8-1 物流・人流のゲートウェイ(6-4・7-1 の品物がない店にも関わる)
- 編成方針の重点に当たるか: 当たる(重点2)

## 見たもの

- `cargo`: trucks 2,066、stoppedInBuildings 521(28755が520)、stoppedOnRoads 301、noGoods 233、noResources 28。28755 は vehiclesLeaving 792 / Arriving 12。ほかの Cargo Center は出入り0
- `trade`: 輸入 15,474(goods 6,970)、輸出 1。道路の入口 8840 に輸入車200台、27833 に140台
- `list_transport_lines`: バス路線は多数。地下鉄 Metro Line 1 は乗客0。pathFailed は Bus Line 81 に1。8-1 には直接つながらない
- `list_policies`: HeavyTrafficBan 無効・週0、FreeTransport 無効・週0、EducationBoost 有効・週7,940、BigBusiness 有効・週3,896、IndustrySpace 無効・週4,846、Recycling 無効・週0。港の止まりに直接効く政策は見当たらない
- `buildings_near`(x=3449, z=-1555, 半径120): 28755 と 13893 の2棟。28755 は問題なし、車792
- `net_near`(x=3449, z=-1555, 半径150, Road): 13区間。Large Road と Small 4 Lane Road が中心
- `transport_reach`: 28755 は outsideConnected true

## 判断の根拠

駅28755の敷地の中の520台は、目標250の倍で、30日動かない。出口の道は詰まっておらず、道の工事で解ける形ではない。政策にも効くものが見当たらないので、駅の状態を戻して組み直す、費用0で戻せる手を試しとして出す。効くかは分からないので、noGoods が増えたらすぐ戻す条件を付けた。

## 捨てたもの

- 貨物駅を新しく建てる: 28755と同じ型の7つが出入り0で使われておらず、増やしても荷が流れない見込み。建設費も要る
- 輸入の荷を港(船)へ回す: 船着きの予算は動かせるが、港に荷を寄せる道具がなく、効く見込みを確かめられない
- バス・地下鉄の路線の変更: 8-1 に効かず、6-3 は道路の幅の問題が先と見て、港湾の担当の数字に結びつかない
- 調査の追加: 先月の調査で、道の詰まりでないことは分かった。今月は試しで確かめる
