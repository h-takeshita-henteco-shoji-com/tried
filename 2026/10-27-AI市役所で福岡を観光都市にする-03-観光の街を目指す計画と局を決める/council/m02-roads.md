# m02 道路下水道局の案

## 案1: 島Bに道と名所の入口への支線を引き、電線を試す

### 施策

- 案の id: roads-3
- 施策: 島Bの中に Basic Road で道(1,600)を引き、名所の入口 (-4640,1552) から道への支線(320)を引く。風力から名所への電線は試しのみ(引かない)。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み(順番どおりに実行する。手順2の後に支線の接続を試し直す)
- 対象と操作順:
  1. `build_line` prefab "Basic Road"、points [[-4500,1700],[-4550,1600],[-4600,1500],[-4600,1400]]、pay=true(試し: cost 1,600、segments 6、enoughMoney true、overlaps なし)
  2. 手順1のあとに `test_build_line` prefab "Basic Road"、points [[-4640,1552],[-4580,1540]] を試す。支線が道につながる(snapped か split が1以上)ことを確かめてから、同じ引数で `build_line`(pay=true、試し: cost 320、segments 1)。つながらなければ止める
  3. 手順1のあとに `test_build_line` prefab "Power Line"、points [[-4560,1450],[-4640,1520]] を試し直す(試し: cost 280、segments 2、overlaps なし)。電線は引かない。5月に風力と一緒に引く
- 設置条件の確認:
  - 島の道: `test_build_line`(Basic Road、上の4点)で、断られず、overlaps なし。道路と建物の重なりなし。SlopeTooSteep は出ていない(第1月の是正で試し済み)
  - 名所の入口: `test_place_building` StatueOfWealth、x -4640、z 1520、facing north で ok。entrance は (-4640,1552)、road は null(手順2の道を引けばつながる)。電気が要る(needs.electricity true)、水と下水は不要。費用 25,000 は経済観光文化局の案で、今月は置かない
  - 風力: `test_place_building` Wind Turbine、x -4560、z 1450 で ok(cost 6,000、needsRoad false)。今月は置かない
  - 支線: `test_build_line` Basic Road、points [[-4640,1552],[-4580,1540]] は ok(cost 320)。ただし道が引かれる前の判定なので、接続は手順2で確かめる
  - 電線: `test_build_line` Power Line は ok(cost 280)。風力と名所は、まだ建っていないので、端点は建物の中心で試した
- 接続工事: 島の道は本土とつながらない(橋は5月)。電線は今月は引かない。本土との接続は5月に確かめる
- 予備候補: なし(支線の終点を変える案は、試しの道具で確かめるまで使わない)
- 中止する条件: 手順1が断られる、または手順2の支線がつながらない場合は、支線を引かず、橋を5月に引かない(計画の事業2のやめる条件)

### 期待する効果

- 改善の見込み: 島Bの名所の入口に道がつながれば、経済観光文化局が7月以降に島へ名所を置けるようになる。観光の入口(5-1、5-2)の材料を作る。
- 数値と期限: 今の値は、島の道0本、島の入口の道0、電線0本。期限は2月末(手順2の試し直し)。数値は見積もれない(観光の収入に効くのは名所ができた後の話)。
- 確認方法: `test_build_line`(支線と電線)の戻り値の snapped / split、`net_near`(x -4600、z 1520、radius 200、service Road)で島の道と支線の区間数を見る。今の値は0。
- 不確かな点: 島の道と支線がゲームで道として通るか(坂の勾配)。試しの道具は坂の判定を gameCheck で返すので、そこを見る。数値は見積もれない。
- 試し: 「島の中を道でつなぐと、名所の入口が道につながる」を試す。測る数は、`net_near` の島の道の区間数(今0)と、支線の接続(snapped か split、今0)。場所は島B、(-4640,1552)。基準は0。編成方針の「分からないこと」(2)(島に橋を架けて名所を置けるか)のうち、島の中の部分。

### 費用

- 建設費: 1,920(島の道 1,600、支線 320。道具の見積もり)
- 週の維持費の増え分: 約15(Basic Road の 40/km/週で、島の道と支線の長さから見積もる。道具の表示は未確認)。電線と風力は今月は引かない

### 戻せるか

戻せない。道を消すには取り壊しの議決が要る(道の撤去は `remove_line`)。

### 前の月の答え合わせ

なし(前の月に同じ対象の案はない。前の月の道の案は、案2の答え合わせに書く)。

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる(重点1の入口の材料)

## 案2: 幹線の交差点2か所に信号を付け、止まった車を測る

### 施策

- 案の id: roads-4
- 施策: 交差点 (-1820,-1010) と (-1820,-1100) に信号を付ける(`set_traffic_lights` active=true、2か所)
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `set_traffic_lights` x -1820、z -1010、active true(交差点 node 1347)
  2. `set_traffic_lights` x -1820、z -1100、active true(交差点 node 27263)
  3. 2か所とも、`junction_info` で trafficLights=true を確かめる
- 設置条件の確認:
  - `junction_info` (-1820,-1010): trafficLights false、customLights false、canEnableLights true、4本の区間(13510 Basic、27473 Basic、19141 Small 4 Lane、23813 Small 4 Lane)
  - `junction_info` (-1820,-1100): trafficLights false、customLights false、canEnableLights true、4本の区間(21849 Basic、13572 Basic、1834 Small 4 Lane、12741 Small 4 Lane)
  - 2か所とも、道と線路が交わる交差点ではない。信号は付けられる
- 接続工事: 不要
- 予備候補: なし(信号が付かなければ、その交差点は付けない)
- 中止する条件: `junction_info` で canEnableLights が false になっていたら、その交差点は付けない

### 期待する効果

- 改善の見込み: 1月に北の幹線の2か所に信号を付けたとき、blocked が 91→64 に減った(m01-7)。同じ仕組みで、止まった車の多いこの2交差点の blocked を減らす。効き目の大きさは数値に見積もれない。
- 数値と期限: 今の値は、`traffic`(x -1800、z -1000、radius 400)の blocked 159、cars 347、congestion 150、flow 50(2050-01-31 の見た値)。予想は blocked が減ること。期限は2月末(月末の見回り)。数値は見積もれない。
- 確認方法: `traffic`(x -1800、z -1000、radius 400)の blocked と congestion。今の値と同じ条件で比べる。見回り1、見回り2、月末に見る。
- 不確かな点: 流れの全体(flow 50%)はほとんど動かなかった(1月も51→50)。効きは、局所の blocked で見る。信号の週の維持費は表示がなく未確認。
- 試し: 「交差点に信号を付けると、この2交差点の止まった車が減る」を試す。測る数は、`traffic`(x -1800、z -1000、radius 400)の blocked(基準159)。場所は (-1820,-1010) と (-1820,-1100) の周り。編成方針の「分からないこと」(5)(道の差し替えと信号で流れ50%が動くか)。案1と測る範囲は重ならない。

### 費用

- 建設費: 0(1月の信号と同じく、所持金の差で確かめる見込み)
- 週の維持費の増え分: 未確認(道具の表示がない)。実行の後に、`city_info` の週の収支を確かめる

### 戻せるか

戻せる。`set_traffic_lights` active=false で外せる(取り壊しではない)。

### 前の月の答え合わせ

- roads-1(m01-3、東と南西の4車線化、採られた): 予想は両地点の blocked が減る。結果は、東が104→30、南西が55→26。測る範囲と測り方が違うため、基準との比は参考にとどまる。流れは51→50。判定: 半分。18205 は衝突で残った。次の扱い: 4月の4車線化は、衝突する区間を外して候補にする(計画の4月)。
- roads-2(m01-7、信号2か所、採られた): 予想は blocked が減る。結果は 91→64。判定: 当たり。今月の案2は同じ仕組みを、ほかの2交差点に足す。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系
- 編成方針の重点に当たるか: 当たる(重点2)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `city_info`: 2050-01-31、人口178,859、所持金2,015,489、週の収支 +8,421(収入341,792、支出333,371)、来ない市民 0/0/0、観光客1,747(訪問139)、dialog なし
- `traffic`: flow 50、cars 7,580、blocked 990、congestion 2,535。busiest は (2152,522) Basic、(2608,-1240) Basic など。blockedSpots は (2091,302) 41台、(-1681,-1128) 38台、(1541,-763) 36台
- `traffic`(x -1800、z -1000、radius 400): flow 50、cars 347、blocked 159、congestion 150。blockedSpots は (-1681,-1128) 38台、(-1822,-919) 29台、(-1866,-1060) 29台
- `traffic`(x 2091、z 302、radius 250): flow 50、cars 199、blocked 116。(2091,302) 41台は Small 4 Lane の直線上で、交差点はない(`junction_info` で確認、40m以内に交差点なし)
- `list_policies`: 有効は EducationBoost(週7,940、学校の維持費への+25%)、BigBusiness(週3,872)。費用0の政策は Recycling、FreeTransport、HeavyTrafficBan、RecreationalUse、SmokingBan、PetBan、各税の上げ下げ。交通に効く政策のうち、HeavyTrafficBan は費用0だが、トラックを道から締め出す。貨物の流れと 6-4、7-1(品物がない店222)を悪くするおそれがあるため、今月は採らない。FreeTransport は運賃収入が0になる。
- `list_building_types`(Electricity): 風力 Wind Turbine 6,000(週80、needsRoad false)、高度風力 Advanced Wind Turbine 12,000(週200)、石炭 19,000(週560)
- `list_building_types`(Monument): StatueOfWealth 25,000(週400、needsRoad true、電気が要る、水と下水は不要)、Official Park 45,000(週128)、Friendly Neighborhood 20,000(週320)
- `list_net_types`(Electricity): Power Line 2,500/km、週60/km
- `list_net_types`(Road): Basic Road 5,000/km、週40/km。Small 4 Lane Road 5,000/km、週40/km(同じ維持費)
- `net_near`(x -4600、z 1520、radius 200、Road): 島に道はなし(segments 0)
- `net_near`(x -1800、z -1010、radius 120、Road): 13510 は Basic Road で10mの短い区間。27473 と 35109 と 31370 と 19964 は Basic Road で、z=-1010 の幹線をなす
- `net_near`(x 2091、z 302、radius 60、Road): 交差点の候補は、既存の信号 node 30603 (2110,330) だけ
- `test_upgrade_road`(Small 4 Lane Road、(-1960,-1010)→(-1640,-1010)): matched 5、upgraded 4、skipped 31370(ObjectCollision、13510 と衝突、blocks)。cost 0。assume_upgraded で 13510 を入れても 31370 は衝突が残る
- `test_upgrade_road`(Small 4 Lane Road、(-1880,-1100)→(-1720,-1100)): matched 3、upgraded 2、skipped 31362(ObjectCollision、21849 と衝突)。cost 0。assume_upgraded で 21849 を入れても 31362 は衝突が残る
- `test_build_line`(Basic Road、[[-4500,1700],[-4550,1600],[-4600,1500],[-4600,1400]]): ok、segments 6、cost 1,600、enoughMoney true、overlaps なし
- `test_build_line`(Basic Road、[[-4640,1552],[-4580,1540]]): ok、segments 1、cost 320、overlaps なし(道が引かれる前の判定。接続は未確認)
- `test_build_line`(Power Line、[[-4560,1450],[-4640,1520]]): ok、segments 2、cost 280、overlaps なし
- `test_place_building`(Wind Turbine、-4560、1450): ok、placed false、cost 6,000、entrance (-4560,1478)、wouldDemolish 0
- `test_place_building`(StatueOfWealth、-4640、1520、facing north): ok、placed false、cost 25,000、entrance (-4640,1552)、road null、wouldDemolish 0
- `junction_info`(-1820,-1010): canEnableLights true、trafficLights false、4本の区間
- `junction_info`(-1820,-1100): canEnableLights true、trafficLights false、4本の区間
- `junction_info`(2110,285): 40m以内に交差点なし

## 判断の根拠

- 担当の数字: 交通の流れは50%で、目標60%に届いていない(6-3)。止まった車は990。1月の幹線の差し替えと信号は、局所の blocked を減らした(信号 91→64)が、流れ全体は動かなかった。したがって、局所の止まった車を減らす手を続ける。
- 観光(重点1): 島Bへの道は、橋より先に引ける。島の中の道と支線は、道具で断られず、接続を試し直せる。橋と風力は5月の計画どおり。今月は観光の入口の材料を作る案1を出す。
- 案1は、島の中で道が通ることを確かめる「試し」。効きは数字に見積もれず、確かめる数は支線の接続(今は0)。
- 案2(信号): 1月の信号が効いたため、同じ手を、止まった車の多い2交差点に足す。費用0。測る範囲は案1と重ならない。
- 案の数は2件。4車線化は、今月は測る範囲が案2の信号と重なるため、4月に回す(判定の範囲を分ける)。

## 捨てたもの

- z=-1010 の幹線の4車線化(35109、27473、19964、13510): 効きが大きい手だが、今月は案2の信号と測る範囲が重なる。31370(80m)は衝突が残る。4月に、信号の結果を見てから出す(計画の4月)。
- 13510 単独の4車線化: 10mの短い区間で、単独では効きが小さい。隣の31370が残るため、効きが見込めない。
- z=-1100 の幹線の4車線化(21849、31362): 31362 は衝突で残る。4月の候補にする。
- 駅への道・水道管・送電線(事業3): 港湾空港局が決める場所と経路を、局の読むファイル(plan-city.md)からは確かめられない。港湾空港局の場所を受けてから試す。
- HeavyTrafficBan(政策、費用0): トラックを締め出すと、貨物と品物の流れを悪くするおそれがある。効きは見込めない。
- 空き地3(712,1644)の道と送電線: 4月の計画。今月は、島の試しと交通の試しで手いっぱいにする。
- (2091,302)付近の交差点への信号: 40m以内に交差点がない(`junction_info`)。信号を付けられる場所は確かめられない。
