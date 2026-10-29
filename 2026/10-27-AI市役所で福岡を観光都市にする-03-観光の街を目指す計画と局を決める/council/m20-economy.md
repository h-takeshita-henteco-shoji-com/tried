# m20 経済観光文化局の案

## 案なし

案を1件も出しません。名所と商業の候補を試したが、置ける場所が確かめられなかった。

- 中心の集まり(0,-1500)は、attractiveness の最大 117 の場所だが、道と建物で埋まっている。`test_place_building`(Transport Tower、8x12)は3か所とも ObjectCollision で断られた。`zones_at` で半径200mの空きは、事務所7、住宅0。8x12 の空きがない
- 南西の集まり(-1133,-800)は、attractiveness の最大 225 で、名所 ScienceCenter の隣。`test_place_building` の2か所(-1725,-690、-1400,-720)も ObjectCollision。2か所とも Expensive Park、道、高層住宅に重なる。`zones_at`(-1725,-690、r150)の空きは、事務所37、住宅0、無区画0
- 島B(-4850,1800)は、`test_place_building` で Transport Tower の位置が ok(費用 60,000)。ただし水・下水がなく(`water_trace` の networkCount 0)、入口の道も近くにない(entrance.road null)。水管と下水管、道の経路は未確認で、必須条件が残る
- 空き地3(745,1500)は、`test_place_building` が道(x 712)に重なって断られた。水・下水の管もない(19月の試しで確認済み)
- 観光の入口(旅客の駅・港・空港)は、港湾空港局の担当。経済観光文化局の案にしない

前月の天文台(19月)が採られなかった理由は、水と下水の管がないこと。今月も、名所の候補は解禁済みの型のほとんどが水と下水を要る(StatueOfWealth だけが電気のみ。ほかは電気・水・下水)。管の経路が決まるまで、実行可能な場所はない。

## 調査

- 調査: あり
- 問い: 名所の訪問は、外とのつなぎ口から来る道の車の流れに近いところほど多いか。名所が増えると、観光客の訪問が増えるかを決める前に確かめる。
- 見る道具と引数: `buildings_near`(x 0、z 0、service Monument、radius 9000、brief false、limit 10)で、名所ごとの訪問。`trade`(引数なし)で、外とのつなぎ口と、今出入りする車。`city_info`(引数なし)で、観光客の今いる数と訪問の平均
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: 訪問の多い名所(SeaWorld 55、Countdown Clock 20 など)の位置が、つなぎ口から来る道の近くに並ぶなら、道沿いで水と下水が届く場所に名所を置く案を21月に出す。並ばず、観光客の数と訪問が動かないなら、名所を伸ばす手を止め、入口(港湾空港局)の案を待つ
- 担当の問題: 5-1、5-2 観光(今いる観光客、訪問の平均、名所の棟数)

## 見たもの

- `city_info`: 人口174,330、所持金2,581,541、週の収支+7,697、幸福度88、観光客1,852(訪問154)、需要 住32/商2/工46
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,104)。無効は SmallBusiness(311)、RecreationalUse(0)、FreeTransport(0)ほか。税の政策は無効。政策の合計 10,856/週。観光に直接効く政策は一覧にない。RecreationalUse と SmallBusiness は m03 と m04 の試しで切り分けられなかった
- `list_building_types`(service Monument): 解禁済みの名所は22型。建っている型は10棟(SeaWorld、Friendly Neighborhood、Countdown Clock、StatueOfWealth、ScienceCenter、Winter Market 01、Servicing Services、Fountain of LifeDeath、Plaza of Transference、Official Park)。未建設の型は Transport Tower(60,000、960/週)、Grand Mall(85,000、1,280/週)、Modern Art Museum(130,000、1,040/週)ほか。水・下水は StatueOfWealth 以外すべて要る
- `demand_breakdown`: 働き口87,498、空き4,011、空き家5,838、大卒の失業2,661、大卒の働ける人72,782
- `buildings_near`(x 0、z 0、Monument、radius 9000、brief false): 訪問は SeaWorld(-1350,-796)55、Countdown Clock(1765,622)20、Fountain(1804,170)17、Winter Market(-1550,-205)17、ScienceCenter(-1130,-804)15、Servicing(1580,-530)9、Friendly(2290,972)10、Official Park(2118,482)9、StatueOfWealth(668,1565)3(電気のみ、水なし)。Plaza of Transference は旅客0
- `map_layer`(attractiveness、x 0、z 0、radius 3000、n 9): 平均3、最大117(0,-1500)、最小0。(-3000,3000)は0
- `map_layer`(attractiveness、x 0、z -1500、radius 600、n 7): 平均6、最大147(-400,-900)、中心の集まりは密
- `map_layer`(attractiveness、x -1300、z -800、radius 500、n 7): 平均16、最大225(-1133,-800)、最小0
- `net_near`(x 0、z -1500、radius 500): 道と水管の区間。中心の道は密で、空きの区画がない
- `zone_map`(x 0、z -1500、radius 700): 住宅と事務所が埋まっている。空きは見えない
- `zone_map`(x -1300、z -800、radius 500): 南西も埋まっている。大きな白い区画は Expensive Park
- `zones_at`(x 0、z -1500、radius 200): 事務所551(空き7)、住宅120(空き0)、無区画117(空き8)
- `zones_at`(x -1725、z -690、radius 150): 無区画193(空き0)、事務所100(空き37)、住宅179(空き0)
- `buildings_near`(x 0、z -1500、radius 900、abandoned true): 0件。放棄された建物はない。壊す案の土台がない
- `buildings_near`(x 0、z -1500、radius 900、problems_only): 汚染、洪水、ごみ、死亡の印が中心の周りに点在
- `test_place_building`(Transport Tower): (0,-1500) は ObjectCollision(道、歩道、事務所、Expensive Park、Crematory 46144)、(-200,-1420) は ObjectCollision(道、Fire House 38642)、(-40,-1080) は ObjectCollision(道、住宅)、(-1725,-690) は ObjectCollision(Expensive Park 19823、31166、道)、(-1400,-720) は ObjectCollision(SeaWorld、道、高層住宅)、(-4850,1800) は ok(費用 60,000、entrance.road null)、(745,1500) は ObjectCollision(道 13359、29045)
- `water_trace`(x -4850、z 1800): 島Bの点に水・下水の網がない(networkCount 0)。city の水 used 1,891,360 / capacity 2,400,000、下水 used 1,888,096 / capacity 2,400,000
- `trade`: 輸入16,286(Goods 7,568、Agricultural 3,762、Forestry 1,635、Oil 1,763、Ore 1,558)、輸出1。つなぎ口は道4(5788,-8649、5818,-8649、5294,8649、5264,8649)、船1、鉄道4、飛行機2。旅客の入口の線はない(鉄道は貨物と見られる)

## 判断の根拠

- 観光の数字(観光客1,852、訪問154、Tourism 87)は、目標の3,000、250、1,000に届いていない。名所の棟数は10で目標どおり。名所の訪問は、SeaWorld の55が最大で、ほかは3〜20。
- 名所を増やす手は、置ける場所が確かめられなかった。中心と南西は、解禁済みの名所の型に対して空きの大きさが足りない。島Bと空き地3は、水と下水の管がなく、必須条件が残る。
- 道路の取り壊しや住宅の取り壊しは、名所の場所を作れるが、住宅と事務所を失う。今の数字では、失う働き口と家の見積もりを出す前に、予備候補が確かめられなかった。取り壊しの案は出さない。
- 政策の一覧に、観光に直接効く政策はない。SmallBusiness と RecreationalUse は、前の試しで効きが切り分けられなかった。今月は新しい政策の試しを出さない。
- 案を出さない代わりに、調査 s20-1 で、訪問が道のつなぎ口に近いかを確かめる。21月に名所の場所を決める材料にする。

## 捨てたもの

- 中心(0,-1500)の名所: 空きの8x12がなく、置けない(ObjectCollision)。道路と住宅の取り壊しは、失う家と働き口が大きく、局の案にしない
- 南西(-1133,-800)の名所: 空きがなく、Expensive Park と道に重なる。Expensive Park を壊すと 4-2 の公園の数が減るので、案にしない
- 島Bの Transport Tower(60,000、960/週): 置く場所は確かめられた(ok)が、水・下水の管と入口の道が未確認。見積もりの管の費用(本土から数千)は、道路下水道局の見積もりを待つ
- 空き地3の名所: 水・下水がなく、道が重なる。19月の天文台と同じ理由で採らない
- 名所 Observatory(85,000、1,600/週): 19月に採られず、維持費が枠を超えるため
- 名所 Grand Mall、Modern Art Museum: 維持費が大きく(1,280、1,040/週)、置く場所がない
- 商業の税を下げる案: 商業の需要が2と低く、税の効きは大きな変化を見込めない。税の議決も要るため、今月は見送る
- 旅客の入口: 港湾空港局の担当。経済観光文化局は、入口を港湾空港局に求める(長期計画の事業)
