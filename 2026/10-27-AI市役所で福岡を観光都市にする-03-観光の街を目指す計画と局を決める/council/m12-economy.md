# m12 経済観光文化局の案

## 案1: 名所 40850 の西側の入口へ南回りの道をつなぐ

### 施策

- 案の id: economy-1
- 施策: 名所 Servicing Services(id 40850、(1580,-530)、入口は西向き)に、道を1本つなぐ。道は既存の Medium Road(11011 の区間、(1703,-600) で分ける)から、南回りに西へ回り、名所の西側に入る
- 議決: 要らない

### 実行計画

- 実行可否: 未確認
- 対象と操作順:
  1. `build_line`(prefab "Basic Road"、points [[1703,-600],[1517,-600],[1517,-530]]、pay=true、demolish=false)
  2. 操作はこの1回だけ。引いたあと、40850 の problems が RoadNotConnected から消えたかを `buildings_near`(x=1580、z=-530、radius=5)で見る(結果の確認であり、事前確認の代わりにはしない)
- 設置条件の確認:
  - `test_build_line`(同じ引数): ok=true、segments 4、crossings 0、cost 1,320、enoughMoney true、overlaps なし
  - `buildings_near`(x=1580、z=-530、radius=5): 40850 は problems RoadNotConnected、grid の electricity・water・sewage は true(電気・水・下水は届いている)
  - `net_near`(x=1600、z=-600、radius=120、Road): 北端の接続先は Medium Road の node 24831 と 21207(区間 11011 と 32460)。道は、この区間の途中に点 (1703,-600) で割って交差点を作る
  - 未確認: 40850 の入口の向き。`test_place_building` は、同じ種類の名所が既にあるため AlreadyExists で断られ、入口の位置を返さない。11月の記録(西向きで置いた)を前提にしている。入口が西でなければ、道は入口に届かない
  - 再調査(m12 の段: 再調査): `buildings_near`(x=1580、z=-530、radius=5、limit=3)は、40850 の ports が空で、入口の向きを返さない。`test_place_building`(Servicing Services、(1580,-530)、facing west、assume_removed_buildings [40850])は AlreadyExists で、入口の位置を返さない。40850 は assumedRemoved のまま衝突の相手に残る。`net_near`(x=1560、z=-530、radius=60)は水道管 29679 の1本だけで、道の接続先はない。`zone_map`(x=1580、z=-530、radius=80)は、名所の敷地の四角を描くが、入口の向きは描かれない。`test_build_line`(同じ引数)は、再確認しても ok のまま、cost 1,320
- 再調査の結果: 条件を満たせず。40850 の入口の向きは、道具(`buildings_near` の ports、`test_place_building` の entrance、`zone_map`)のどれでも確かめられなかった。道が入口に届くかも確かめられない。実行可否は未確認のまま、採れない
- 接続工事: 不要(道の両端は、既存の Medium Road の途中と、名所の西側の空き地で終わる。電気・水は既につながっている)
- 予備候補: なし。確認済みの予備は、同じ入口に届く経路だけになる。`test_build_line` で (1517,-470) から南へ引く案は、道路 12043・34893 の交差点にぶつかり断られた(店 17073 の取り壊しも要る)。使わない
- 中止する条件: 実行前に、40850 の入口が西向きでないと確かめられたら見送る(名所は10棟で終える)。`test_build_line` の結果が変わり、overlaps か colliding が出たら見送る

### 期待する効果

- 改善の見込み: 名所 40850 は、道がつながらないと入口から観光客が来ない。道がつながれば、名所に来る観光客と訪問が増え、Tourism の収入も増えると予想する。11月の確認で、名所の周りの attractiveness は 0 から 14(平均、半径300m)に上がったが、観光客は 1,763 から 1,725 に減り、Tourism は 27 から 42 に増えた。道がなくても効くのは周りの attractiveness だけで、観光客は増えていない
- 数値と期限: 観光客(city_info の now)は今 1,725、訪問(visits)は今 133、Tourism(economy_breakdown)は今 42。予想値は数値で見積もれない。期限は12月の月末(12月28日ごろ)
- 確認方法: `buildings_near`(x=1580、z=-530、radius=5)で 40850 の problems が消えたか。`city_info` の tourists(now、visits)と `economy_breakdown` の Tourism を、今の値と比べる。周りの attractiveness は `map_layer`(attractiveness、x=1580、z=-530、radius=300、n=5)で、12月7日の平均 14 と比べる
- 不確かな点: 入口の向きが未確認。月末までに道が完成するか(建設に数日かかる)。観光客が増えるかは、道の効きの量として見積もれない。増えなければ、12月末の判定は外れ
- 試し: 効き目が分からない案として出す。仮説: 名所の入口に道がつながると、名所に来る観光客が増え、訪問と Tourism が上がる。測る数は、`city_info` の tourists と visits、`economy_breakdown` の Tourism。場所は名所 40850 の周り(半径300m)。基準は、観光客 1,725、訪問 133、Tourism 42(12月7日)

### 費用

- 建設費: 1,320(`test_build_line` の cost)
- 週の維持費の増え分: 約12(Basic Road の週の維持費 1kmあたり約46.6。`economy_breakdown` の 6,101 を 131km で割った値から、道の長さ約0.26kmを掛けた概算)

### 戻せるか

戻せる。`remove_line` で消せるが、取り壊しの議決が要る。

### 前の月の答え合わせ

- 11月の案 economy-1(名所 40850 を (1580,-530) に置き、道・電気・水をつなぐ)は採られ、部分実行。名所は置け、電気と水はつながったが、入口の道は引けず、RoadNotConnected のまま。
- 調査 s11-2(12月7日の結果): 周りの attractiveness は、置く前の 0 から、平均 14(最大 118、(1580,-530))。観光客は 1,763 から 1,725、訪問は 138 から 133。Tourism は 27 から 42。
- 判定: 半分。周りの attractiveness は上がったが、道がないため観光客は増えず、道の未接続が原因と見る。道の件は今月の案1で扱う。

### 市の計画

- 当たる施策: 5-1、5-2 観光(名所の棟数、今いる観光客、訪問の平均、Tourism の収入、attractiveness)
- 編成方針の重点に当たるか: 当たる(重点1)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `list_policies`: 取得した。有効なのは SmokingBan(費用0)、BigBusiness(週 4,004)。関係する政策は見当たらない。RecreationalUse は無効で、費用 0。3月に試し、4月に外した。SmallBusiness は無効、週 313。EducationBoost は無効、週 7,940(教育の支出に入る)。政策の費用の合計は週 10,786。今月は政策を変えない
- `city_info`: 人口 179,547、所持金 2,358,955、週の収支 +13,509、観光客 1,725(訪問 133)、dialog なし
- `economy_breakdown`: Tourism 週 42、Office 23,833、Monument 週の支出 3,448、Basic Road の 2,491 区間 131.02km の週の維持費 6,101
- `buildings_near`(x=1580、z=-530、radius=150、brief、limit 30): 名所 40850 は RoadNotConnected。周りに店と事務所。店 17073 は NoGoods、FatalProblem
- `buildings_near`(x=1580、z=-530、radius=5、limit 3): 40850 の grid は electricity・water・sewage が true。ports は空
- `net_near`(x=1580、z=-530、radius=150): 水道管 29679・30108 が名所の東に通り、電線 11460 は (1640,-526) で終わる。道は、北の Medium Road(11011、32460、17128)と、西の Basic Road(12043、34893。z=-470 と x=1530)
- `net_near`(x=1600、z=-600、radius=120、Road): Medium Road 11011(node 24831〜21207)と 32460(21207〜4119)
- `zone_map`(x=1600、z=-500、radius=200、size 600): 名所の敷地は約 x 1528〜1632、z -481〜-577。西側は店 17073、3389 の列。南側の空き地に道を通せる
- `test_place_building`(Servicing Services、(1580,-530)、facing west、assume_removed [40850]): AlreadyExists。入口の位置は得られない
- `test_place_building`(Servicing Services、(1580,-700)、facing west): ObjectCollision(タワー住宅)、AlreadyExists。使えない
- `test_place_building`(Servicing Services、(1580,-640)、facing west): AlreadyExists。使えない
- `preview_bulldoze`(x=1517、z=-494、radius=12、what=building): 店 17073 の1棟。失う働き口 0、家 0。取り壊しは議決が要るため、今月は使わない
- `test_build_line`(Basic Road、[[1530,-470],[1516,-470],[1516,-530]]、assume 17073): ObjectCollision、TooShort。道路 12043・34893 の交差点にぶつかる
- `test_build_line`(Basic Road、[[1530,-470],[1516,-470],[1516,-530]]): ObjectCollision。店 17073、3389 に重なる
- `test_build_line`(Basic Road、[[1517,-470],[1517,-530]]、assume 17073): ObjectCollision。始点が交差点の近くで、道路 12043・34893 にぶつかる
- `test_build_line`(Basic Road、[[1703,-600],[1517,-600],[1517,-530]]): ok。segments 4、cost 1,320、overlaps なし

## 判断の根拠

確認した事実は、名所 40850 が RoadNotConnected で、電気・水・下水は届いていること。西側の道は、店 17073、3389 と交差点にぶつかって通らない。取り壊しを含む西回りは、議決が要り、失う店の数も大きくないが、取り壊しの案は今月の判定までに終わらない見込み。よって取り壊さず、南回りの道を試した。test_build_line は通り、費用 1,320 で所持金も足りる。残る不確かさは、入口の向きだけで、道具では確かめられない。そのため実行可否は未確認にした。案は1件とした。最終月で、観光の有効な手は名所の道だけだからである。入口と2棟目の名所は、12月の時間では間に合わない。

## 捨てたもの

- 名所 40850 の西側への道(店 17073 の取り壊しを含む): 取り壊しの議決が要り、今月の判定までの時間が足りない。`preview_bulldoze` で失うものは働き口 0、家 0 だが、議決の手間に見合わない
- 名所の2棟目(空き地): 電気と道が要り、12月末までに道と電気を引けない。計画の変更で見送った
- 旅客の入口(駅・港・空港): 港湾空港局の担当。経済観光文化局の案にせず、市長の判断に任せる
- 品物がない店の改善(214、目標120以下): 原因の貨物センター 28755 の止まりは港湾空港局の担当。12月の時間で効く手がない
- 政策 RecreationalUse の再試し: 無効で費用 0 だが、3月の試しで attractiveness が上がらず、4月に外した。同じ試しは繰り返さない
- 事務所税の変更: 6-1 の効きは出ていない。最終月で判定までに数字が出ない
