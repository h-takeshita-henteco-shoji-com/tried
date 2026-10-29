# m08 道路下水道局の案

## 案1: 交差点(-1100,-440)に信号を付ける

### 施策

- 案の id: roads-1
- 施策: 交差点(-1100,-440、node 32647)に信号を付ける。`set_traffic_lights(x=-1100, z=-440, active=true)`
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `set_traffic_lights(x=-1100, z=-440, active=true)` の1回だけ。道は動かさない
- 設置条件の確認: `junction_info(-1100,-440)` で、信号なし(trafficLights false)、人が決めた信号でない(customLights false)、信号を付けられる(canEnableLights true)、譲れの標識を付けられる(canSetYield true)を確認。交差点に入る道は 25388、32461、14511 の3本
- 接続工事: 不要
- 予備候補: なし(信号が付けられないときは、案を見送る)
- 中止する条件: 実行の直前に `junction_info` で canEnableLights が false になっていたら、見送る

### 期待する効果

- 改善の見込み: `traffic(x=-1098, z=-459, radius=150)` で blocked 45 のうち、交差点の真上(-1098,-459)に 42 台が止まっている。信号を付けると、この交差点の止まりが減ると予想する。
- 数値と期限: 今の値は blocked 45(半径150m)、交差点の止まり 42。8月末の見回りで、同じ円の blocked が減るかを見る。量は見積もれない。
- 確認方法: `traffic(x=-1098, z=-459, radius=150)` の blocked と blockedSpots。街全体の flow(今 56%)も見る。
- 不確かな点: 信号の周期で、流れが悪くなる向きがあるかは未確認。数値は見積もれない。
- 試し: なし

### 費用

- 建設費: 0(信号は費用0。前月までの信号の追加で同じ額だった)
- 週の維持費の増え分: 0(道具で確かめた額はなし。前月までの信号の追加で増えなかった)

### 戻せるか

戻せる。信号は `set_traffic_lights(active=false)` で外せる。

### 前の月の答え合わせ

前の月(7月)の交通の案のうち、この案と関係する答え合わせは、案2の欄に書く。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1・5-2、8-1、4-4。6-3 は重点の外の案)

## 案2: 幹線 x=-1845(z -620〜-830)を Small 4 Lane Road にする

### 施策

- 案の id: roads-2
- 施策: Basic Road の4区間を Small 4 Lane Road に差し替える(x=-1845、z -620〜-830)。`upgrade_road(prefab="Small 4 Lane Road", points=[[-1845,-620],[-1845,-830]])`
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1. `upgrade_road(prefab="Small 4 Lane Road", points=[[-1845,-620],[-1845,-830]])` の1回。道路の差し替えだけで、建物は動かさない
- 設置条件の確認: `test_upgrade_road(prefab="Small 4 Lane Road", points=[[-1845,-620],[-1845,-830]])` で ok、matched 4、upgraded 4、skipped なし、cost 0。`net_near(-1845,-757,r120,Road)` で、対象の4区間は Basic Road(24257、26277、18577、5020)と確認
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: 実行の直前に `test_upgrade_road` が skipped を出したら、skipped の区間を外して出し直すか、見送る

### 期待する効果

- 改善の見込み: この区間の density は 100 で、blockedSpots は(-1836,-829)14台、(-1846,-775)7台。車線を増やすと、この区間の詰まりが減ると予想する。
- 数値と期限: 今の値は `traffic(x=-1845, z=-760, radius=160)` の blocked 21、density 100 の区間が複数。8月末の見回りで、同じ円の blocked と density を見る。量は見積もれない。
- 確認方法: `traffic(x=-1845, z=-760, radius=160)` の blocked、busiest、blockedSpots。街全体の flow(今 56%)も見る。
- 不確かな点: 円の中の blocked は 21 で小さい。流れへの効きは小さいかもしれない。数値は見積もれない。7月の z=560 の4車線化では blocked が1か月だけ増えた例があり、2か月続けて増えたら戻す(事業1の条件)。
- 試し: なし

### 費用

- 建設費: 0(`test_upgrade_road` で cost 0、matched 4)
- 週の維持費の増え分: 0(Basic Road と Small 4 Lane Road は、どちらも 40/週/km。`list_net_types` で確認)

### 戻せるか

戻せる。Small 4 Lane Road を Basic Road に戻すのも、同じ道具で費用0。

### 前の月の答え合わせ

7月の4車線化(z=-318 と z=560)の答え合わせ。`traffic` の flow は 54%(7月)→ 56%(8月)で上がった。北東 z=560 の blocked は 41→47 で、1か月だけ増えた。2か月続けて増えていないので、戻さない(事業1の条件どおり)。判定は半分(流れは上がったが、どの区間の効きかは分けていない)。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(交通の流れ)
- 編成方針の重点に当たるか: 当たらない

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `city_info`: 人口 180,138、所持金 2,174,932、週の収入 342,510、支出 326,155、来ない市民 0/0/0、観光客 1,744(訪問 150)、需要 住22・商2・工56
- `list_policies`: 政策の費用合計 10,695/週。SmokingBan 有効(0)、BigBusiness 有効(3,856)、SmallBusiness 無効(309)、EducationBoost 無効(7,940)、RecreationalUse 無効(0)、Recycling 無効(0)、SmokeDetectors 無効(57,723)、HighTechHousing 無効(20,260)。交通に効く政策はなし
- `traffic`: 街全体 flow 56%、cars 7,528、blocked 944、congestion 2,323
- `traffic(x=-1098, z=-459, r150)`: blocked 45、congestion 28、blockedSpot(-1098,-459) 42台
- `junction_info(-1100,-440)`: 信号なし、customLights false、canEnableLights true、canSetYield true。道 25388、32461、14511
- `net_near(-1098,-459,r130,Road)`: Basic Road が中心。Small 4 Lane は近くにない
- `traffic(x=-1845, z=-760, r160)`: flow 56、cars 85、blocked 21、congestion 22。density 100 の区間 18577、15059、24257、36107、26277。blockedSpots(-1836,-829) 14台、(-1846,-775) 7台
- `net_near(-1845,-757,r120,Road)`: 対象の4区間は Basic Road、x=-1820 の区間 13527 は Small 4 Lane
- `test_upgrade_road(Small 4 Lane Road, [[-1845,-620],[-1845,-830]])`: ok、matched 4、upgraded 4、skipped なし、cost 0
- `test_upgrade_road(Small 4 Lane Road, [[-1100,-363],[-1070,-440],[-1040,-440]])`: matched 2、upgraded 1、skipped 8373(TooShort)。使わない
- `test_upgrade_road(Large Road, [[2200,180],[2200,300]])`: ok、matched 2、upgraded 1、skipped 4412(Crematory 36841 を壊す)、cost 80。壊す案のため、使わない
- `traffic(x=2078, z=292, r150)`: blocked 50、congestion 50、blockedSpot(2078,292) 32
- `junction_info(2078,292)`、`junction_info(2722,279)`: 40m以内に交差点なし
- `junction_info(-920,-740)`、`junction_info(900,-712)`: 既に信号あり
- `list_net_types(Road)`: Basic Road 5,000/km・40/週/km、Small 4 Lane 5,000/km・40/週/km、Large Road 10,000/km・120/週/km、Medium Road 7,500/km・100/週/km
- `list_building_types(Monument)`: 未建設の名所は、StatueOfWealth 以外すべて電気・水・下水が要る。StatueOfWealth は 11580 が既にある
- `buildings_near(service=Monument, 0,0,r6000)`: 名所9棟(11580 を含む)
- `buildings_near(-4600,1500,r250)`: 風車 44460(-4660,1440)、出力 6MW、電気あり
- `test_place_building(SeaWorld/ScienceCenter, -4640,1520, 北向き)`: ObjectCollision(道 13902、14667、34550)と AlreadyExists。島の名所は不可
- `test_build_line(Power Line, [[-4650,1500],[-4645,1512]])`: ok、cost 40
- `net_near(-4600,1500,r200,Road)`: 島の道 13902(z 1550)、支線 22680 など
- `zone_map(-4600,1500,r200)`: 島の名所の候補の周り。送電線 x≈-4650 の z 1467〜1500 を確認
- `list_net_types(Water)`: Water Pipe 2,500/km、維持費 10/週/km
- `water_trace` 相当の確認(net_near の Water、本土の橋の付け根): 本土の水道管 15448(-2715,95→142)。島に水の網はない。橋の水道管の試し(test_build_line)は ObjectCollision で断られた
- `test_build_line(Power Line, 名所 11580 の (668,1565) 付近への4経路)`: すべて ObjectCollision(名所 11580 の敷地)
- `net_near(668,1565,r150,Electricity)`: 送電線 13409 などの近く

## 判断の根拠

- 6-3 の交通の流れは 56%。目標 60% まで4ポイント。道路下水道局の担当の数字なので、今月の案は交通にする。
- 案1: 交差点(-1098,-459)の止まり 42台が、信号なしの交差点で集まっている。信号は費用0で、道具の確認も通った。確認済みなので採る。
- 案2: x=-1845 の Basic Road 4区間は density 100 で、4車線化は費用0、維持費も同じ。確認済みなので採る。効きは小さいかもしれないが、戻せる。
- 島Bの名所と、名所 11580 の電気は、道具で確かめたとおり今月は実行できない。案には出さず、計画の変更に書いた。
- 案の数は2件。確認済みの交通の手が2つだけだった。(2078,292) の周りには近くに交差点がなく、手が見つからなかった。

## 捨てたもの

- 島Bの名所(StatueOfWealth 以外): 未建設の名所は水と下水が要る。島に水の網がなく、本土の水道管 15448 と衝突する。試せないため、案にしない。
- 名所 11580 の電気(送電線の端を敷地の縁に置く案): 4経路がすべて ObjectCollision で断られた。`relocate_building` は試せない(test は AlreadyExists で返す)。案にしない。
- (2200,180〜300) の Large Road 差し替え: 火葬場 36841 を壊す。取り壊しの議決が要り、6-3 の効きも見積もれない。案にしない。
- (-1100,-363) の4車線化の経路: 8373 が TooShort で断られた。案にしない。
- (2078,292) 周りの Medium Road 13553 の差し替え: 近くに交差点がなく、道具の試しを通していない。案にしない。
