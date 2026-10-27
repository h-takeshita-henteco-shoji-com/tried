# 街を作る・変える道具の説明と引数

<!-- code/ai-mayor/tools/make_tool_reference.py が mcp/server.py から作る。手で編集しない -->

局と見てまとめる市長は、これらの道具を持っていません。案の実行計画に、使う道具の名前と引数の値を書くために読みます。
道具を呼べるのは、実行する市長だけです。

## 道路・線・路線

### `build_line(prefab: str, points: list[list[float]], frames: int = 0, gif_name: str | None = None, pay: bool = True, follow: bool = False, size: float = 2500, demolish: bool = False, y: float | None = None)`

座標の並び [[x, z], ...] に沿って、線(道路・線路など)を引く。
道路と水道管は、線の途中で交わる既存の地上の道路・管にも交差点を作る(戻り値の crossings。一般道は高速道路の本線とは交差点を作らない)。
端点の12m以内に同じサービスの点があれば、そこにつなぐ。点がなく16m以内に区間があれば、その区間を途中で分けて
交差点を作り、つなぐ(既存の道路の途中に突き当てられる)。
prefab: 種類の名前(例: "Train Track", "Highway", "Basic Road")。list_net_types で調べる。
frames: 1以上なら、線をその数の区間に分けて順に引き、区間ごとに今の視点で画面写真を撮って GIF にまとめる。
一方通行の道(高速道路など)は、並びの順が進む向きになる。
川や海を渡る区間は、自動で橋の種類(例: "Basic Road Bridge")になり、水面より3m以上高く架ける。戻り値の bridgeSegments が橋の区間の数。
点を [x, z, 地面からの高さ(m)] にすると、高さ0.5mを超える点は高架の種類(例: "Highway Elevated")で、その高さに引く。
高架の区間では、水の上の点を外して川を1区間でまたぐ(水の中に橋脚を立てないため)。
pay: True(既定)なら、ゲームの道具と同じく建設費を予算から差し引く。足りなければ建てずに断る。
人が置く骨格(#69)だけ False にする。
follow: True なら、区間を引くたびにカメラをその区間の先端へ動かしてから撮る(長い線を追いかけて撮る)。
size: follow のときのカメラの引き。
戻り値の snapped(既存の点につないだ数)と split(既存の区間を分けてつないだ数)が両方0なら、新しい線はどこにもつながっていない。
高速道路は上り・下りが別の線なので、間の中央分離帯に端を置くとつながらない。net_near で車線の位置を確かめてから引く。
ends: 始点と終点が何につながったか。connectedTo は "node"(既存の点)/ "split"(既存の区間を分けた)/ "none"。
building は、端が建物の管のつなぎ口につながったときの建物の id(なければ 0)。
insideBuilding は、端が敷地の中にある建物の id。送電線は端が建物の敷地に入れば電気が通る。
net は、端がつながった線の種類。一般道の端が高速道路の本線につながると warning が付く(つなぐのは止めない)。
道路・線路が建物の敷地に重なるときは、建てずに断り、overlaps に重なる建物(id、種類、位置)を返す。
重なった建物はゲームが取り壊す。壊してよければ demolish=True で引く。成功したときも overlaps を返す。
ゲームの線を引く道具と同じく、取り除けない相手(交差点の近くの別の道路、サービスの建物など)にぶつかる線と、
短すぎる区間(TooShort)がある線は、引かずに断る。
そのとき atSegment(ぶつかった区間の両端)と colliding(ぶつかった区間と建物。blocks=true が断る相手)を返す。
gameCheck: ゲームの道具なら出るそのほかの注意(坂が急すぎるなど)。引くことは引く。
点を [x, z, −深さ] にすると、地下にその深さ(8mより浅いと9m)で引く。両端が地下の区間はトンネル、片方だけの区間は坂
(地上への出入り口)になる。トンネルの種類がない線(管・送電線など)は断る。地下の端は地下の点(地下鉄の駅の乗り場の線路の端を含む)
にだけつなぐ。地下の区間は地面の建物と重ならない。戻り値の undergroundSegments が地下と坂の区間の数。
y: 点の高さを固定するとき(m)。地面の高さの代わりにこの高さで引き、橋・高架・トンネルにはしない。
船の航路(Ship Path)を水面(約40m)に引くときに使う(#100)。省くと地面の高さ。
解禁前の線は断る。

### `remove_line(points: list[list[float]], prefab: str | None = None, tolerance: float = 20)`

座標の並び [[x, z], ...](線)に沿った区間を消す。区間の両端が線から tolerance(m)以内のものが対象。
prefab を指定すると、その種類だけを消す(例: "Train Track")。省くと種類を問わない。

### `upgrade_road(prefab: str, points: list[list[float]], tolerance: float = 20, pay: bool = True, demolish: bool = False)`

道路を別の種類に差し替える(例: "Basic Road" → "Medium Road"、"Large Road")。ゲームの道路の道具の「アップグレード」と同じ。
points: [[x, z], ...] の線。両端の点が両方とも線から tolerance(m)以内にある道路の区間を差し替える。
区画の指定と沿道の建物は保たれる。太くした道路の下になったマスは消える。
太くした道路の下になる区画の建物は、ゲームが壊す。
既定(demolish=False)では、そうなる区間は差し替えずに飛ばし、skipped に壊れる建物の番号と名前を返す。
demolish=True なら差し替え、壊れた建物を demolishedBuildings に返す。
サービスの建物(病院、学校など)や別の道にぶつかる区間は、ゲームが断るので飛ばす(ぶつかった区画の建物があれば、demolish=True で壊してやり直す)。
同じ幅の種類(Basic Road → Small 4 Lane Road など)への差し替えでは、沿道の建物は壊れない。
壊す前に preview_bulldoze で、失う家と席を見積もる。
橋・高架・トンネルの区間は、ゲームが高さに合う種類を選ぶ。費用は新旧の建設費の差。足りなければその区間を飛ばす。
戻り値: matched(選んだ区間の数)、upgraded(差し替えた数)、skipped(飛ばした区間と理由)、cost。
ぶつかって断られた区間(reason に ObjectCollision)には colliding を付ける。ゲームの道具の画面で赤く塗られる相手と同じ。
colliding.segments(区間の番号、種類、中ほどの位置)と colliding.buildings(建物の番号、種類、位置)。
blocks=true の相手があると断られる。blocks=false の相手は、作るときにゲームが取り除く。
一方通行の道路に差し替えると向きは元の区間のまま。逆にするときは reverse_road を使う。

### `reverse_road(points: list[list[float]], tolerance: float = 20)`

一方通行の道路の向きを逆にする(種類は変えない)。ゲームの道路の道具の右クリックと同じ。両方向の道路は飛ばす(skipped)。
points と tolerance は upgrade_road と同じ。

### `create_transport_line(type: str, stops: list[list[float]])`

公共交通の路線を作る。type は bus / metro / train / ship / plane。
stops は停留所・駅の位置 [[x, z], ...] の並び(2つ以上)で、最後のあと最初の停留所に戻って環状になる。
バスは各点から64m以内で最も近い道路の区間に停留所を置く。地下鉄・鉄道・船・飛行機は、各点から300m以内で
最も近いその種類の駅の乗り場を使う(駅は先に place_building で置く)。
バスの路線は、先にバスの車庫(Bus Depot)を建てないと作れない(ゲームの決まり。地下鉄・鉄道も駅が要る)。
どれか1つでも置けなければ、路線を作らずに断る(index に置けなかった停留所)。建設費はかからない。
台数はゲームが決める。道順は数日かけて計算されるので、
後で list_transport_lines の pathFailed を確かめる。
バスの停留所は、点に最も近い車線に置かれ、進む向きは見ない。この街は右側通行なので、東へ進む区間は道の南側、
西へ進む区間は北側に点を置く(北へ進む区間は東側、南へ進む区間は西側)。
逆の側に置くと、隣の停留所まで遠回りする。

### `remove_transport_line(line: int)`

路線を消す。line は list_transport_lines の line(画面の番号 number ではない)。

### `set_transport_line_budget(line: int, percent: int)`

路線ごとの台数の割合を変える(10〜300%)。

### `set_traffic_lights(x: float, z: float, active: bool)`

交差点の信号を付ける(active=True)・外す(False)。ゲームの交通の情報画面の「交差点」のボタンと同じ。
道路と線路が交わる交差点などは付けられない(junction_info の canEnableLights)。

### `set_yield_sign(x: float, z: float, segment: int, active: bool = True)`

交差点に入る区間(segment は junction_info の roads の segment)に「譲れ」の標識を付ける・外す。
標識のある側の車は、ほかの道の車に譲ってから入る。信号のある交差点には付けられない(先に set_traffic_lights で外す)。

## 建物

### `place_building(prefab: str, x: float, z: float, angle: float = 0, pay: bool = True, facing: str | None = None)`

建物を (x, z) に置く。正面(入口)を道路に向けること。建物は道路に面していないと働かない(needsRoad が true のとき)。
facing: 入口の向き(north / northeast / east / southeast / south / southwest / west / northwest、
または北0・東90の時計回りの度)。angle より優先する。向きを決めるときは facing を使う。
angle は反時計回りの度で、入口の方位 = (360 − angle) % 360(0で北、90で西、270で東)。angleUsed は実際に使った angle。
needsRoad が false の建物(風車など)は、entrance.road が null でも働く。needs は電気・水・下水が要るか。
道路が要る建物の入口のそばに道路がないときは、置いた上で warning を返す。向き(facing)を変えるか、入口の前に道路を引く。
demolished: 敷地が重なって取り壊される区画の建物の数(count)と id(ids、最大20)。removedNow は置いた直後にもう消えていた数。
pay: True(既定)なら建設費を予算から払う。足りなければ置かずに断る。人が置く骨格だけ False。
まだ解禁されていない建物は置かずに断る(unlock に条件を返す)。
ゲームの建物の道具と同じ判定で、置けない場所(道路やサービスの建物に重なる、買っていない土地、岸がないなど)なら置かずに断る。
そのとき reasons(理由)と colliding(ぶつかった区間と建物。blocks=true が断る相手)を返す。区画の建物は断る理由にならず、取り壊される。
岸に置く建物などは、ゲームが位置と向きを直すことがある(angleUsed と entrance で確かめる)。
"simulation thread timeout" が返ったら、建物は置かれていない(executed=false)。sim_health で確かめてから置き直す。
entrance: 置いた建物の入口の x, z、正面の向き(facing: north など / bearing: 北0・東90の度)、
入口から16m以内の道路(road。なければ null)。road が null なら、道路を引くか、向きを変えて置き直す。
ports: 管・送電線のつなぎ口の x, z と、外の線につながっているか(connected)。管はこの点に端を合わせて引く。

### `relocate_building(id: int, x: float, z: float, angle: float = 0, facing: str | None = None, pay: bool = True)`

サービスの建物を別の場所へ移す(ゲームの「移す」と同じ)。費用は建設費の1/5。facing / angle は place_building と同じ。
置けない場所なら reasons に理由を返して断る。ぶつかる区画の建物は取り壊される。
移した後は、道路・管・送電線のつながりを確かめ直す。
置けないときは、ぶつかった建物(collidingBuildings)と区間(collidingSegments)の番号を返す。理由は、建物の型の判定(positionReasons)と
場所の判定(spaceReasons)に分けても返す(#107。相手が空のまま断られたときの手がかり)。移す建物そのものとの重なりは、
ゲームと同じく数えない。向きを変えると幅と奥行きが入れ替わり、隣の道路にぶつかることがある。

### `bulldoze(x: float, z: float, radius: float = 50, what: str = 'all')`

中心 (x, z) から半径 radius(m)の円の中を取り壊す。
what: "all"(道路・線路と建物) / "net"(道路・線路だけ) / "building"(建物だけ)。取り壊しの払い戻しはない。
buildings: 壊した建物の id と種類(最大50件)。
what="abandoned" で、円の中の放棄された建物と、壊れた・焼けた建物(区画の建物だけ)を取り壊す。サービスの建物と道路は残す。
放棄された建物をまとめて片づけるのに使う。

### `set_building_active(id: int, active: bool)`

サービスの建物を止める・動かす。止めると維持費と働き手が0になり、サービスもしない。

### `empty_building(id: int, active: bool = True)`

満ちた埋立地や墓地を空にする。中身はほかの同じ種類の施設へ運ばれる。空にしている間は受け入れない。
終わったら active=False で戻す。

### `set_historical(id: int, active: bool = True)`

区画の建物を歴史的建造物にする。レベルが上がらず建て替わらない。

## 区画と地区

### `zone_area(x: float, z: float, radius: float, type: str)`

中心 (x, z)、半径 radius(m)の円の中の、道路沿いの区画マスを指定する。区画マスは道路を引くと両側にできる。
type: residential_low / residential_high / commercial_low / commercial_high / industrial / office / none(解除)。
建物が建っているマスは変えない。解禁前の区画の種類は断る。

### `zone_rect(x1: float, z1: float, x2: float, z2: float, type: str)`

東西・南北の向きの四角 (x1, z1)〜(x2, z2) の中の、道路沿いの区画マスを指定する。type は zone_area と同じ。

### `zone_polygon(points: list[list[float]], type: str)`

多角形 [[x, z], ...](頂点3つ以上)の中の、道路沿いの区画マスを指定する。type は zone_area と同じ。
建物が建っているマスは変えない。通りに沿った細長い区画や、街区をまとめて塗るのに使う。

### `paint_district(x: float, z: float, radius: float = 150, name: str | None = None, erase: bool = False)`

円の中を地区に塗る。name の地区がなければ作る。erase=True で塗りを消す。
地区には政策や産業の特化をかけられる(set_district_policy)。cells は地区のマスの数(1マス19.2m四方)。

### `set_district_policy(district: str, name: str, active: bool = True)`

地区だけに政策をかける。district は番号か名前。name は list_policies の名前、または産業の特化
(Forest / Farming / Oil / Ore。工業の区画が資源の産業になる。地面の資源が要る)。税の政策(TaxRaise / TaxLower)も地区にかけられる。
特化は同じ組で1つだけ。解禁前やDLCのない政策は断る。

### `rename_district(district: str, name: str)`

地区の名前を付け替える。district は番号か名前。

## 税・予算・政策・融資

### `set_tax(target: str, rate: int)`

税率を変える。target: residential_low / residential_high / commercial_low / commercial_high / industrial / office。
rate: 1〜29(%)。

### `set_budget(target: str, percent: int | None = None, day: int | None = None, night: int | None = None)`

サービスの予算を変える。percent: 50〜150 で、昼と夜の両方を同じ値にする。
day と night で昼と夜を分けて設定できる(50〜150。どちらかだけでもよい)。
target: electricity / water / garbage / healthcare / fire / police / education / parks / roads /
bus / metro / train / ship / plane / taxi。

### `set_policy(name: str, active: bool = True)`

街全体の政策をかける(active=True)・外す(False)。name は list_policies の名前(例: "Recycling")。
かける前に list_policies の costPerWeek で週の費用を確かめる。戻り値にも同じ見積もりを返す。

### `take_loan(index: int)`

銀行の申し出どおりに借りる。返済は毎週、自動で支出に入る。

### `repay_loan(index: int)`

融資の残りを今すぐ返す。お金が足りなければ断る。

## 木と地形

### `plant_trees(polygon: list[list[float]], prefab: str | None = None, spacing: float = 12, pay: bool = True)`

多角形 [[x, z], ...] の中に、spacing(m)おきに少しずらして木を植える。1本ごとに建設費を払う。
建物・道路・水の上には植えない(blocked)。お金が尽きたら止まる。

### `remove_trees(polygon: list[list[float]])`

多角形の中の木を取り除く。払い戻しはない。

### `level_terrain(polygon: list[list[float]], height: float, pay: bool = True, test: bool = False)`

多角形の中の地形を、その高さ(m)にならす。ゲームの景観の道具と同じく、元の地形との差が広がる分に土の値段を払い、
縮めば払い戻す。盛るには土の蓄えが要り、削ると蓄えに入る。足りなければ何も変えずに断る。
建物・道路・線路の下と、持っていない区画は変えない(skipped*)。低い土地を盛って浸水を防ぐのに使う。
test=True なら、変えずに、土と費用の見積もり(raisedM3、loweredM3、cost、enoughMoney、dirtBufferM3)だけ返す。

### `raise_terrain(polygon: list[list[float]], amount: float, pay: bool = True, test: bool = False)`

多角形の中の地形を amount(m)上げる。費用と制限は level_terrain と同じ。

### `lower_terrain(polygon: list[list[float]], amount: float, pay: bool = True, test: bool = False)`

多角形の中の地形を amount(m)下げる。費用と制限は level_terrain と同じ。

### `terrain_dirt()`

地形を変えるための土の蓄え(m³)と1m³の値段。
