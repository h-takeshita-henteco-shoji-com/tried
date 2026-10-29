# m11 経済観光文化局の案

## 案1: 東の空き地に名所 Servicing Services を置き、道・電気・水をつなぐ

### 施策

- 案の id: economy-1
- 施策: 名所 Servicing Services(12x13 m、建設費 20,000、週 320)を (1580,-530) に、西向き(facing west)で置く。入口は西側の道 (1566,-530)→(1534,-530)→(1534,-470) で、既存の道 node 9041 (1530,-470) につなぐ。電気と水は既存の網から引く
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building`(prefab="Servicing Services", x=1580, z=-530, facing="west", pay=true)。`test_place_building` で ok=true、angleUsed=90、費用 20,000 を確認済み
  2. 置いた後、返り値の `entrance`(入口と道)と `ports`(電気・水のつなぎ口)を読む
  3. `test_build_line`(prefab="Basic Road", points=[[1566,-530],[1534,-530],[1534,-470]])で再確認し、`build_line`(同じ引数、pay=true)で引く。道の端 (1534,-470) は既存の node 9041 (1530,-470) に近く、つながる見込み
  4. `test_build_line`(prefab="Power Line", points=[[1683,-514],[1580,-530]])で確認し、`build_line` で引く。端 (1683,-514) は既存の送電線の点 node 19435
  5. `test_build_line`(prefab="Water Pipe", points=[[1694,-536],[1580,-530]])で確認し、`build_line` で引く。端 (1694,-536) は既存の水道管の点 node 31504。手順 2 の `ports` が (1580,-530) と違えば、水の端をその `ports` の座標に替えて試し直す
  6. `water_trace`(x=1580, z=-530)で、建物の電気・水・下水が届くかを見る
- 設置条件の確認:
  - 敷地: `test_place_building` で ok。衝突はなし(建物の判定 ok)。空き地(未指定の区画)の中
  - 道路: `test_place_building`(facing west)の入口は (1528,-530)。置く前は道が null。この入口から 6m の位置に、道 (1566,-530)→(1534,-530)→(1534,-470) の西の辺 (x=1534) が通る。`test_build_line` で ok(overlaps なし、費用 480)。入口の16m以内に道が入る見込み。置いた後の `entrance.road` で確かめる
  - 電気: 送電線の点 node 19435 (1683,-514) から、建物の中心へ引く `test_build_line` が ok(費用 280)
  - 水と下水: 水道管の点 node 31504 (1694,-536) から引く `test_build_line` が ok(費用 280)。下水の管は見当たらず、`net_near`(Sewage)で0。`water_trace` の網では、同じ網に取水口と排水口があり、水の管につなげば下水も届く見込み。置いた後に `water_trace` で確かめる
  - 木・建物の重なり: 道の経路は、事務所 22965 (1554,-452) と店 3389・17073 を避ける形にした。西へ回る案 (1566,-470 経由と 1500 経由) は ObjectCollision で断られた
- 接続工事: 道 480、送電線 280、水道管 280(いずれも `test_build_line` の費用)。道の端 (1566,-530) は建物の外形から数m離す。入口は置いた後の `entrance` で確かめる
- 予備候補: なし。別の空き地 (1600,-580) などは、道・電気・水を確かめていないため使わない
- 中止する条件:
  - `test_place_building` が、置く直前に ok=false になったら、置かずに見送る
  - 置いた後、入口の道が1つもつながらなければ、道を引き直す。それでもつながらなければ、建物を取り壊す(議決が要る)か、そのまま残して名所の数だけ見る
  - 水のつなぎ口が `water_trace` で届かなければ、水の管を (1530,-465) の既存の管の点から引き直す。それもだめなら見送る

### 期待する効果

- 改善の見込み: 名所の棟数を 9 から 10 にして、目標 10 に届く。空き地のため、置けば棟数は確実に増える。周りの attractiveness も上がる見込みだが、その量は見積もれない(今は 0)
- 数値と期限: 名所の棟数 9 → 10(第11月末、buildings_near の Monument)。周りの attractiveness は 0 → 数値は見積もれない(第12月末まで)
- 確認方法: `buildings_near`(service=Monument、x=1580、z=-530、radius=60)で棟数を見る。`map_layer`(type=attractiveness、x=1580、z=-530、radius=300、n=5)で、今の値(中心の点 0、西の山 (1430,-680) 117)と比べる。`city_info` の tourists も、同じ月で比べる
- 不確かな点: 入口の道と水のつなぎ口は、置いた後にしか確かめられない。置いたあとに中止条件に当たれば、名所は置けない。効き目(attractiveness と観光客)は、数値を見積もれない
- 試し: なし(棟数の目標を置く案)。効き目の確認は、調査で見る

### 費用

- 建設費: 約21,040(建物 20,000、道 480、送電線 280、水道管 280。`test_place_building` と `test_build_line` の費用)
- 週の維持費の増え: 約340(名所 320、道 約4(92m×40/km)、送電線と水道管 約14)

### 戻せるか

戻せる。置いた建物と線は取り壊せる。取り壊しは議決が要る。

### 前の月の答え合わせ

- 10月の案1(economy-1、同じ場所 (1580,-530)、台帳 m10-economy-1)は、採られなかった。理由は「電気と水のつなぎ口の位置と、入口の道路が既存道路につながる形が未確認」
- 今月の案での扱い: 道・電気・水の経路を、`test_build_line` と `test_place_building` で通した。手当てとして、道は西の経路にした。残る未確認は、置いた後の入口と水のつなぎ口だけ

### 市の計画

- 当たる施策: 5-1、5-2 観光(名所の棟数、attractiveness、観光客)
- 編成方針の重点に当たるか: 当たる(重点1: 名所を目標10まで)

## 調査

- 調査: あり
- 問い: 名所 (1580,-530) を置いた後、周りの attractiveness と観光客は、置く前より上がったか
- 見る道具と引数: `map_layer`(type=attractiveness、x=1580、z=-530、radius=300、n=5)、`buildings_near`(service=Monument、x=1580、z=-530、radius=60、brief=true)、`city_info`
- いつ見るか: 見回り1、月末
- 何が分かれば次の手が決まるか: 中心の attractiveness が 0 から上がり、観光客が増えるなら、12月に2棟目を別の空き地で試す(時間が足りれば)。上がらないなら、名所の効きは場所では変わらないと判断し、12月は入口の進み具合だけを見る
- 担当の問題: 5-1、5-2 観光

## 見たもの

- `city_info`: 人口 179,848、所持金 2,313,772、週の収入 335,847 / 支出 325,167(収支 +10,680)、幸福度 89、観光客 1,763(訪問 138)、dialog なし、citizensWithoutService 0/0/0
- `list_policies`: 有効は SmokingBan(0)、BigBusiness(4,012/週)。SmallBusiness は無効(317/週)、RecreationalUse は無効(費用0。m04 で効かず外した)、EducationBoost は無効(7,940/週)。政策の週の合計は 10,812。観光に効く政策で、効き目が確かめられたものはない
- `list_building_types`(service=Monument): 解禁済みの名所のうち、未建設は Servicing Services(20,000、12x13、週 320)、Transport Tower(60,000)、Colossal Offices(70,000)など。名所は1種類につき1棟
- `buildings_near`(service=Monument、半径 8000): 名所は9棟。StatueOfWealth 11580(668,1565)は電気が来ない
- `buildings_near`(半径 200、(668,1565)): 11580 と公園 30466 が電気の問題(Electricity, MajorProblem)
- `map_layer`(attractiveness、街全体、n=9): 平均 4、最大 119
- `map_layer`(attractiveness、(-1200,-1000)、半径 500、n=9): 平均 12、最大 211(-1700,-750)
- `map_layer`(attractiveness、(668,1565)、半径 200、n=3): 11580 の場所は 75
- `map_layer`(attractiveness、(1580,-530)、半径 300、n=5): 中心の点は 0。西の (1430,-680) は 117
- `economy_breakdown`: Tourism 週 27、Office 16,472、policyExpenses 10,812、Road の維持費 8,908、Electricity 35,441、Water 19,351
- `zone_map`: (-1250,-780)、(-1200,-1100)、(-1550,-740)、(1540,-510)、(1450,-650) を見た。市の中心は区画が詰まり、空きは少ない。(1540,-510) の東と南は未区画の空き地
- `buildings_near`(半径 250、(-1250,-780)、brief): 住宅・事務所・SeaWorld・ScienceCenter が詰まる
- `buildings_near`(abandoned=true、半径 5000、brief): 放棄された店などが112棟(多くは街の外れ)。(-1176,-1166)〜(-1404,-1214) に5棟
- `buildings_near`(service=PublicTransport、半径 400、(-1250,-780)): 0棟
- `land_value`(-1250,-780、半径 300): 平均 65、街の平均 54
- `test_place_building`: Servicing Services を (1580,-530) で、facing south(ok、entrance road null)、facing west(ok、angleUsed 90、entrance (1528,-530))。Servicing Services を (1389,-711) east(ObjectCollision、CannotBuildOnWater)。Friendly Neighborhood を (-1625,-700) east(ObjectCollision、建物と道路が密)。Official Park を (-1630,-835) east(ObjectCollision、建物が密)
- `test_build_line`: Basic Road [[1566,-530],[1566,-470],[1530,-470]](断られた。事務所 22965 と重なる)、Basic Road [[1566,-530],[1566,-545],[1500,-545],[1500,-470]](断られた。店 3389 と重なる)、Basic Road [[1566,-530],[1534,-530],[1534,-470]](ok、費用 480)、Power Line [[1683,-514],[1580,-530]](ok、費用 280)、Water Pipe [[1694,-536],[1580,-530]](ok、費用 280)、Power Line [[603,1533],[668,1565]](断られた。11580 の敷地と重なる)
- `net_near`: (1580,-560) 半径120(道 (1530,-424)〜(1530,-470)、(1485,-470)〜(1530,-470)、送電線 (1683,-514)、(1687,-586)、水道管 (1694,-536)、(1530,-396)〜(1530,-465))。(1580,-530) 半径150、Sewage は0。(668,1565) 半径250、Electricity は 11580 の近くに線が (603,1533) まで
- `water_trace`(1580,-530): 取水口と排水口が同じ水道管の網につながる。市の水と下水の容量は 2,400,000、使用 1,923,792 / 1,921,872
- `list_net_types`(service=Road、解禁済み): Basic Road は 5,000/km、維持費 40/km/週

## 判断の根拠

- 担当の数字のうち、名所の棟数だけが目標 10 に届いていない(9)。名所は1棟足せば届く。10月に採られなかった案の理由は、道と水の接続の未確認だった。今月は、道・電気・水を試しの道具で通せたので、実行条件はそろった
- 場所は、市の中心に空きがないため、東の空き地 (1580,-530) を選んだ。中心の attractiveness の山は (1430,-680) と (-1700,-750) にあるが、空きがなく、`test_place_building` で置けなかった
- 案は1件にした。2棟目の名所は、1棟目の効きを見てから決める。同じ月に2棟目を足すと、測る数の場所が重なり、効きが分からなくなる
- 費用は、週の収支 +10,680 に対し、週 340 の増え。守る線(+3,000、所持金 1,874,000)を破らない
- 調査は1件。効き目の量は見積もれないため、名所の効きを見る道具(attractiveness と観光客)を決めた

## 捨てたもの

- 中心の空きに名所を置く案: 市の中心 (-1700〜-1300, -625〜-800) は attractiveness が高いが、空きがない。`test_place_building` で 2 か所とも ObjectCollision。取り壊しで住宅を減らす案は、住民への影響が大きく、今月は見送る
- 放棄された店やホテル(-1176,-1166)〜(-1404,-1214)の跡に名所: 中心の山から 400m 以上離れ、attractiveness が低いと見込む。今月は試していない。効き目が分かってから候補にする
- 11580 の電気を引く送電線(603,1533)→(668,1565): 11580 の敷地と重なり断られた。11580 は、電気がなくても attractiveness 75 がある。今月の名所の数は変わらないため出さない。空き地3の接続は道路下水道局の担当
- 政策 RecreationalUse・SmallBusiness・EducationBoost の有効化: RecreationalUse は m04 で効きが見られず外した。SmallBusiness と EducationBoost は m05、m07 で試し済み。観光の効きの根拠が増えないため出さない
- 2棟目の名所(別の空き地): 1棟目の効きが分からないうちは、見送る
- 旅客の入口: 港湾空港局の担当。局は求めることとして長期計画に書く
