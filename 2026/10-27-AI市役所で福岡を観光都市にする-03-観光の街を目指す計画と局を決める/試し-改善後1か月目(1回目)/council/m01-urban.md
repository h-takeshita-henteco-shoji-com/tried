# m01 住宅都市みどり局の案

## 案1: 空き地3に公園1棟と幹線・送電線を引く

### 施策

- 案の id: urban-1
- 施策: 空き地3(712,1644)に Regular Park を1棟置き、入口(680,1644)から西へ幹線 Basic Road を (668,1644) → (-346,1441) で引く。公園へ送電線 (712,1644) → (421,1320) をつなぐ。4-2 の公園の数を 81 → 82 にする。周りの attractiveness と地価を測る
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順(建物が先、道路が後):
  1. `place_building`: prefab=Regular Park、x=712、z=1644、facing=west、pay=true(建設費 1,000)。入口は (680,1644)
  2. `build_line`: prefab=Basic Road、points=[[668,1644],[-346,1441]]、pay=true(建設費 7,700)。始点を入口から12m西にずらす。入口(680)から始めると、公園の西の縁に重なるおそれがあるため
  3. `build_line`: prefab=Power Line、points=[[712,1644],[421,1320]]、pay=true(建設費 1,080)。端の (712,1644) は公園の敷地の中
- 設置条件の確認:
  - 公園: `test_place_building`(Regular Park、712、1644、facing west)は ok。cost 1,000、enoughMoney true、wouldDemolish 0 件、lostByDemolish は 0。needs.electricity=true。道路はまだないため entrance.road は null
  - 幹線: `test_build_line`(Basic Road、[[668,1644],[-346,1441]])は ok。segments 13、bridgeSegments 3、cost 7,700、overlaps 空。終点 (-346,1441) は `net_near` の segment 1919 と 1702 の共通の点(node 1812)
  - 送電線: `test_build_line`(Power Line、[[712,1644],[421,1320]])は ok。segments 6、cost 1,080、overlaps 空。終点 (421,1320) は segment 1937 の端(node 16294)
  - 幹線の別案: 始点を (680,1644) にすると cost 7,300 で ok だが、公園と重なるおそれがあるため採らない
- 接続工事: 幹線(Basic Road、7,700)と送電線(Power Line、1,080)。水と下水は要らない(公園の needs は電気のみ)
- 予備候補: なし。幹線と送電線の経路は1本ずつしか確かめていない
- 中止する条件: 公園の `test_place_building` が断ったら、案全体を見送る。幹線の `build_line` が overlaps を返したら、公園のほかの建物には触らず、始点を西へ8m動かして `test_build_line` を通し直す。通らなければ見送る。送電線を引いたあと、公園の grid.electricity が来ていなければ、送電線の端を見直す(この案の幹線は残す)

### 期待する効果

- 改善の見込み: 4-2 の公園の数を1棟増やす(81 → 82)。公園が近くの attractiveness と地価を上げるかを試す。今の周りの attractiveness は 0 で、基準として使う
- 数値と期限: 4-2 の数は建った直後に 82。attractiveness は3月の見回りで測る(基準は 0)。地価は、建てる前に `land_value` で基準を取ってから、3月に比べる
- 確認方法: `buildings_near`(service=Beautification、x=712、z=1644、radius=100、brief=true)で棟数。`map_layer`(type=attractiveness、x=712、z=1644、radius=150、n=5)で平均。`land_value`(x=712、z=1644、radius=150)で地価。今の値と同じ範囲で比べる
- 不確かな点: 公園が attractiveness に効くかは分からない。効果の量は見積もれない。幹線の端(node 1812)へのつながりは、試しの返りに snapped が出ないため、実行後に `net_near` で確かめる。公園の電気は、送電線の端が敷地に入るため通る見込みだが、実行後に grid で確かめる
- 試し: あり。仮説: 公園が近くの attractiveness を上げ、その周りの地価も上がる。測る数: `map_layer` の attractiveness の平均(基準 0)と、`land_value` の地価(基準は建てる前に測る)。場所: (712,1644) の半径150m。基準: attractiveness 0

### 費用

- 建設費: 9,780(公園 1,000 + 幹線 7,700 + 送電線 1,080。道具の `test_place_building` と `test_build_line` の cost)
- 週の維持費の増え分: 約79(公園 8 + 幹線 約44 + 送電線 約26)。幹線は `list_net_types` の 1km あたり 40 からの見積もり。橋の分は含まない

### 戻せるか

戻せる。取り壊しの議決を経れば戻せるが、建設費の払い戻しはない。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たる

## 案なし

案1 を出すため、この見出しは書かない。

## 調査

- 調査: あり
- 問い: 公園(Beautification)の周りで、attractiveness が上がっているか。今の公園の周りの値を基準にして、動きを見る
- 見る道具と引数: `map_layer` の type=attractiveness、x=2582、z=1222、radius=150、n=9 / `buildings_near` の service=Beautification、x=2575、z=1224、radius=400、brief=true
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 基準の最大は 157(2575, 1224)付近。公園の周りの値が変わらなければ、公園は attractiveness に効かないとみて、4-2 だけの案として出す。上がれば、同じ街区に公園を増やす案を出す。公園の数(基準 81 のうち近くの棟数)が変わったときは、建った公園を記録する
- 担当の問題: 4-2 花や緑による潤い(公園の数)と、5-1、5-2 観光(attractiveness は局の担当の外。結果を市長に伝える)

## 見たもの

- `net_near`: (712,1644) 半径700 の道路は0件。(712,1644) 半径1100 の最寄りの道路は、segment 1702 と 1919(-352,1515 → -340,1368)と、segment 6753 と 7170(1780, 1316〜1460)。(712,1200) 半径1000 の道路は、z 175〜640 の区間だけ。送電線は (712,1644) 半径800 で、segment 1937(421,1320 → 357,1360)など
- `list_net_types`: Basic Road 建設費 5,000/km、週 40/km。Power Line(Electricity)建設費 2,500/km、週 60/km
- `test_build_line`: Basic Road (712,1644) → (-346,1441) ok、cost 8,100。Basic Road (680,1644) → (-346,1441) ok、cost 7,300。Basic Road (668,1644) → (-346,1441) ok、cost 7,700、overlaps 空。Basic Road (712,1644) → (1780,1388) 断り(風車 25669 と警察 33595 に重なる)。Power Line (712,1644) → (421,1320) ok、cost 1,080。Basic Road (500,1613) → (500,1500) ok、cost 560
- `test_place_building`: Regular Park (712,1644) facing west ok、cost 1,000、needs.electricity true、entrance (680,1644)。Regular Park (500,1645) facing south ok、entrance (500,1613)。Regular Park (-696,132) facing south、assume_removed 3952 は断り(ObjectCollision: Medium Road 1435 と 23177、店 24961 と 45772)。Regular Park (2152,900) facing west、assume_removed 22930, 36901, 27586, 38418 は通るが、取り壊しで家 36(27404、46477)を失う。Regular Plaza (2150,820) facing south、assume_removed 22930, 36901, 38418 は断り(ObjectCollision: Basic Road 7205、12913、26756。家 27404、46477 が残る)。Regular Park (2300,1000) facing south、assume_removed 5266, 12373, 47695, 23391 は断り(ObjectCollision: Basic Road 19287、20165。現役の店が残る)。Regular Plaza (-648,40) facing north、assume_removed 22529, 19439, 17702 は置けるが、取り壊しに現役の建物 548、2109、2367、2372 が入り、働き口 32 を失う
- `buildings_near`(abandoned=true、(-696,132)、半径200、brief): 5棟(3952、11452、17702、19439、22529)。すべて店で、NoGoods と FatalProblem
- `buildings_near`(abandoned=true、(2400,1000)、半径400、brief): 12棟。店、ホテル 5266、12373、工場 13612 を含む
- `map_layer`(attractiveness、(712,1644)、半径150、n=5 と n=3): 平均 0、最大 0。基準

## 判断の根拠

指摘1: 空き地3(712,1644)から、道路網の node 1812(-346,1441)まで、Basic Road を試しで引けた(断りなし、費用 7,700、橋 3区間)。始点は公園の入口から12m西にずらし、公園との重なりを避けた。送電線も試しで引けた(費用 1,080)。道路が引けたので、案1 の実行条件が確認できた。

指摘2: 取り壊しを使う5か所を、assume_removed_buildings 付きで試した。道路・現役の建物にぶつかるか、家 36 または働き口 32 を失うため、取り壊しの案は今は出さない。取り壊しの議決は、置ける候補が見つかった月に出す。

指摘3: 公園20棟の費用に、幹線と送電線の費用を足した(plan-urban.md の事業の費用)。建設費 約31,500、週の維持費 約295。

案の数は1件とした。2棟目以降は、幹線が建ってから、入口の位置を試す必要がある。今の時点で案にすると、実行できない案になる。

## 捨てたもの

- 空き地3(712,1644)に公園を置く案を、道路なしで出す案: 幹線の経路が確かめられたため、道路つきの案1 にした
- 放棄された店の跡(-696,132)、(2150,820)、(2152,900)、(2300,1000)に公園を置く案: 道路・現役の建物にぶつかるか、家 36 を失う。取り壊しの案にはしない
- (-648,40)に広場を置く案: 現役の建物を4棟取り壊し、働き口 32 を失う
- (1780,1388)へ幹線を引く案: 風車 25669 と警察 33595 にぶつかる。案1 の幹線で足りる
- 灰色の空き(2240,522)、(2525,522)、(1200,-1200)、(2575,1224)、(-1000,1350): 前の月と同じ。埋立地、取り壊しで家を失う、海の上、建物と道路に重なる、のいずれか
- 2棟目以降の公園の案: 幹線が建ってから、入口の位置を試す。今月は出さない
- 政策の変更: 今月は政策一覧を取り直していない。4-2、4-1 に効く政策は、前の月に見た一覧にない
