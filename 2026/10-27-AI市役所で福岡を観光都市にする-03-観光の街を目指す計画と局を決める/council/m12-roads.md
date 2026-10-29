# m12 道路下水道局の案

## 案1: 名所 40850 の道を東と南から引く

### 施策

- 案の id: roads-1
- 施策: 名所 Servicing Services(id 40850、(1580,-530))の入口の道を、東側の Medium Road 8836 と南側の Medium Road 11011 から引く。道は Basic Road。対象は 5-1・5-2 の名所(重点1)
- 議決: 要らない

### 実行計画

- 実行可否: 未確認
- 対象と操作順:
  1. `build_line` prefab "Basic Road"、points [[1703,-520],[1640,-520]]、pay=true、demolish=false。試し(`test_build_line`)は ok、cost 320、overlaps なし。始点は 8836 の上に載り、交差点でつながる
  2. `build_line` prefab "Basic Road"、points [[1703,-590],[1560,-590]]、pay=true、demolish=false。試し(`test_build_line`)は ok、segments 2、cost 720、overlaps なし。始点は 11011 の上に載る
  3. 実行後の報告(判定の前提にはしない): `buildings_near` の x 1580、z -530、r 80 で、40850 の problems が RoadNotConnected のままかを見る
- 設置条件の確認:
  - 40850 の入口の向きは未確認。`test_place_building` で同じ種類を試すと AlreadyExists になり、読めない(唯一の記念物のため、同じ種類は2つ置けない)
  - 再調査(m12): 入口の向きを読む道具を、もう一度確かめた。`buildings_near`(x 1580、z -530、r 80)は ports が空で、向きを返さない。`test_place_building`(Servicing Services、(1580,-530)、facing south、assume_removed 40850)は AlreadyExists で、向きを読めない。`zone_map`(x 1580、z -530、r 120)の図にも入口の印はない。向きは、道具では確かめられなかった
  - 東側(x 1632 の外、道の端 x 1640)と南側(z -582 の外、道 z -590)は、道具の試しで重なりなし
  - 北側は `test_build_line` の (1530,-470)→(1580,-468)が、office 22965(1554,-452)に重なって断られた。採らない
  - 西側は、店 3389(1497,-494)と放棄された店 17073(1517,-494)のそば。道の経路は未確認。道を通すには 17073 の取り壊しが要る(議決が要る)
  - 周りを一周する道(四方から入口に届かせる案)は、北が office 22965 に当たり、西は 17073 の取り壊しが要るため、取り壊しなしには組めない
- 接続工事: 上の2本で、東と南の両方から入口に近づける。電線 11460 の上は試しで重なりなし。費用は計 1,040(建設費)、週の維持費 +約10
- 再調査の結果: 条件(入口の向きを道具で確かめ、東か南の道が入口に届く経路を書く)を満たせなかった。入口の向きは、道具(`buildings_near`、`test_place_building`、`zone_map`)では読めない。東か南の道が入口に届くかは確かめられず、実行可否は未確認のまま。この回では採らない
- 予備候補: 確認済みの予備はない。北は office に当たる。西は取り壊しが要る(未確認)
- 中止する条件: 実行時の `test_build_line` が overlaps か断りを返したら、その1本を外す。2本とも断られたら、案1を見送る

### 期待する効果

- 改善の見込み: 名所 40850 は RoadNotConnected のままで、今週の訪問は 1 だけ(`buildings_near` の stats)。道がつながると、観光客が名所に来る見込み(局の予測。ゲームの仕組みからの推定で、量は見積もれない)。観光の 5-1・5-2 の3つ(今いる観光客、訪問、Tourism の収入)に効く
- 数値と期限: 40850 の Visitors last week は今 1。都市の今いる観光客は 1,725(目標 3,000)、Tourism 週 42(目標 1,000)。数値は見積もれない。期限は12月末
- 確認方法: `buildings_near`(x 1580、z -530、r 80)の problems(RoadNotConnected の有無)と stats(Visitors last week)、`city_info` の tourists、`economy_breakdown` の Tourism。今の値(1 / 1,725 / 42)と比べる
- 不確かな点: 入口の向きが未確認。東か南の道が入口に届くかは、実行して初めて分かる。道が届いても、観光客が増える量は見積もれない。実行前に確かめられるのは、道と建物の重なりだけ
- 試し: なし(効き目の仕組みは確かめられているが、接続が未確認のため、実行可否は未確認)

### 費用

- 建設費: 1,040(`test_build_line` の cost 320 と 720 の合計)
- 週の維持費の増え分: 約 +10(Basic Road 40 / km / 週、約 0.24km)

### 戻せるか

戻せる。道は取り壊しの議決なしで、必要なら後で消せる。

### 前の月の答え合わせ

前の月の案 roads-1(11月、交差点 (2280,-950) の信号)は採られ、実行できた(費用 0)。期限は12月末。
- 見回り(前の月の記録): blocked は 0〜2 で、基準 72 より下。
- 月末(今月の `traffic`、x 2290、z -950、r 150): blocked 82。基準 72 より多い。
- 判定: 半分(見回りは当たり、月末は外れ)。外す条件(見回りで 72 超)は満たさないため、信号は残す。
- 11月の調査 s11-3(`traffic`、x -1678、z -1323、r 150): 今月の blocked は 15(11/17 は 22、11/27 は 13)。減っており、今月は手を打たない。

## 案2: 10647 を Large Road に太くする(z=100 の東西の幹線)

### 施策

- 案の id: roads-2
- 施策: 区間 10647(Medium Road、x 1692〜1770、z 100)を Large Road に太くする。交通の流れを上げる(6-3)。blocked 89(r 150、(1689,94) に 68)の場所の、東から西への車線を増やす
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `upgrade_road` prefab "Large Road"、points [[1770,100],[1692,100]]、tolerance 20、pay=true、demolish=false。試し(`test_upgrade_road`)は ok、matched 1、upgraded 1、skipped なし、cost 200、demolishedBuildings なし
- 設置条件の確認: `test_upgrade_road` で、同じ道の区間 109(x 1613〜1692)は High School 1226(1640,134)と Bus Depot 30483(1652,66)にぶつかって断られた。109 は入れない。10647 だけなら通る。`list_net_types` で Large Road の解禁は確認(unlocked true、costPerKm 10,000)
- 接続工事: 不要
- 予備候補: 区間 109 は、学校と車庫を取り壊す議案になるため採らない。なし
- 中止する条件: 実行時の `test_upgrade_road` が skipped を返したら、中止する。cost が 200 を大きく超えたら見直す

### 期待する効果

- 改善の見込み: 10647 は z=100 の幹線で、東から西へ向かう車が詰まる場所(1689,94 の blocked 68)のすぐ東。車線が増えると、この場所の待ちが減る見込み(局の予測)
- 数値と期限: `traffic`(x 1689、z 94、r 150)の blocked は今 89、blockedSpots の (1689,94) は 68。数値は見積もれない。期限は12月末
- 確認方法: `traffic`(x 1689、z 94、r 150)の blocked と blockedSpots、同じ範囲で比べる
- 不確かな点: 太くしても、西側の区間 109 が細いままなので、詰まりが西へ移るだけかもしれない。都市全体の流れ(今 53%、目標 60%)は、この1区間では届かない
- 試し: あり。仮説: 10647 を太くすると、東から西への車線が増え、(1689,94) の待ちが減る。測る数: `traffic`(x 1689、z 94、r 150)の blocked(基準 89)と、blockedSpots の (1689,94) の台数(基準 68)。場所: この区間の周り。基準: 今の値。6-3 の交通の効きとして測る

### 費用

- 建設費: 200(`test_upgrade_road` の cost)
- 週の維持費の増え分: 約 +2(Large Road 120 と Medium Road 100 の差 20 / km、約 0.08km)

### 戻せるか

戻せる。太くした道は、元の道に戻せる(取り壊しを使わない)。

### 前の月の答え合わせ

なし(前の月に、この区間を太くする案はない)。信号の判定は案1の欄を見る。

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口179,547、所持金2,358,955、週の収支 +13,509、観光客 1,725(訪問 133)、需要 住16/商2/工66、citizensWithoutService 0/0/0、dialog なし
- `traffic`(x 2290、z -950、r 150): flow 53、cars 104、blocked 82、blockedSpots (2293,-922) 67。基準 72 より多い
- `traffic`(x -1678、z -1323、r 150): flow 53、cars 62、blocked 15、blockedSpots (-1817,-1308) 11
- `traffic`(全体): flow 53、cars 7,334、blocked 957、blockedSpots (1689,94) 68、(2293,-922) 67、(2498,-946) 51。60% の目標とは差が大きい
- `traffic`(x 1689、z 94、r 150): flow 53、cars 149、blocked 89、blockedSpots (1689,94) 68
- `junction_info`(2280,-950): trafficLights true、customLights true、canEnableLights true(信号は残っている)
- `list_policies`: 有効は SmokingBan(0)と BigBusiness(4,004 /週)。SmallBusiness 無効(313 /週)、RecreationalUse 無効(0)、EducationBoost 無効(7,940 /週)。交通に効く政策はなし。観光に関わる政策の変更は、案にしない
- `buildings_near`(x 1580、z -530、r 150): 名所 40850 は problems RoadNotConnected、Visitors last week 1、Tourists last week 0。店 17073(放棄)、3389、office 22965 が道の経路のそば
- `net_near`(x 1580、z -530、r 150): 8836(Medium Road、1699,-457 → 1703,-536)、11011(Medium Road、1703,-536 → 1707,-614)、電線 11460(1683,-514 → 1640,-526)、水道管 29679 と 30108(z -533〜-536)、Basic Road 34893 と 24553(z -470、x 1440〜1530)
- `net_near`(x 1689、z 94、r 100、Road): 109(Medium、1613〜1692)、10647(Medium、1692〜1770)、3239(Medium、1560〜1613)、6010(Large、1770〜1824)
- `citizens_summary`: 失業 8,524(大卒 8,402)、健康 89、来ない市民 0/0/0、幸福度 94(住民平均)
- `test_build_line`(Basic Road、[[1530,-470],[1580,-468]]): ng、overlaps 22965(断られた)
- `test_build_line`(Basic Road、[[1703,-520],[1640,-520]]): ok、cost 320、overlaps なし
- `test_build_line`(Basic Road、[[1703,-590],[1560,-590]]): ok、segments 2、cost 720、overlaps なし
- `test_place_building`(Servicing Services、(1580,-530)、facing 4方向、assume_removed 40850): ng、AlreadyExists(唯一の建物のため、入口の向きは読めない)
- `test_place_building`(Servicing Services、(1580,-700)、(1580,-660)、(1580,-640)): ng、AlreadyExists または ObjectCollision(空き地での入口の読みは不可)
- `zone_map`(x 1580、z -500、r 150、size 600): 40850 の外形(x 1532〜1628、z -478〜-582)、南と東は空き、北は店とオフィス
- `zone_map`(x 1580、z -600、r 120、size 480): 40850 の南は空き地(未区画)
- `test_upgrade_road`(Large Road、[[1770,100],[1692,100],[1613,100]]): ok、matched 2、upgraded 1、109 は High School 1226 と Bus Depot 30483 にぶつかって skipped
- `test_upgrade_road`(Large Road、[[1770,100],[1692,100]]): ok、matched 1、upgraded 1、skipped なし、cost 200
- `list_net_types`(Road、locked false): Large Road は解禁済み(costPerKm 10,000、upkeep 120 /km 週)。Medium Road は 7,500 / 100。Basic Road は 5,000 / 40
- 再調査(m12)`buildings_near`(x 1580、z -530、r 80): 40850 の ports は空、problems RoadNotConnected。入口の向きは返らない
- 再調査(m12)`test_place_building`(Servicing Services、(1580,-530)、facing south、assume_removed 40850): ng、AlreadyExists(向きを変えても同じ。入口は読めない)
- 再調査(m12)`zone_map`(x 1580、z -530、r 120、size 480): 40850 の外形は見えるが、入口の印はない
- 再調査(m12)`net_near`(x 1580、z -530、r 120): 北の office と西の店の経路は、前の見たものと同じ。新しい道の候補は増えず

## 判断の根拠

- 観光は今月の重点1。名所 40850 は RoadNotConnected のままで、訪問は週 1。道を東と南から引く案1を、観光の1手とした。入口の向きは読めないが、2本の試しは重なりなしで通る。実行可否は「未確認」にする(入口の側が確かめられない)
- 再調査(m12): 条件は入口の向きを道具で確かめることだった。`buildings_near`、`test_place_building`、`zone_map` のどれも向きを返さず、条件を満たせなかった。案1は採らず、実行可否は未確認のまま残す
- 駅は未建設(入口 0)。港湾空港局の担当のため、局は動かさない
- 信号 (2280,-950) は残す。月末の blocked 82 は基準 72 より多いが、見回りは 0〜2 で外す条件に当たらない
- 6-3 は流れ 53%。目標 60% には届かない見込みが強い。1区間を太くする案2は、試しで通り、費用 200 と小さいため採った。効きは測る
- 案の数を2件にした理由: 観光の道(案1)と、交通の太くする手(案2)の2つだけが、道具の試しで通ったため。ほかの候補(区間 109、北側の道、取り壊しを含む西側の道)は、断られたか、議決が要るか、期限に間に合わない

## 捨てたもの

- 信号 (2280,-950) を外す: 見回りは 0〜2 で、外す条件(見回りで 72 超)に当たらない。月末の 82 だけでは外さない
- 区間 109(Medium から Large): High School 1226 と Bus Depot 30483 にぶつかる。取り壊しは議決が要り、期限の12月末に間に合わない
- 名所 40850 の北側の道(1530,-470 → 1580,-468): office 22965 にぶつかり、`test_build_line` が断った
- 名所 40850 の西側の道(店 17073 の取り壊しを含む): 取り壊しは議決が要る。道の経路も未確認
- 名所 40850 を四方から囲む道: 北が office に当たり、西は取り壊しが要る。取り壊しなしには組めないため捨てた(再調査で検討)
- 観光の政策(RecreationalUse、SmallBusiness): 効きが台帳で確かめられず外した経緯がある(m04-economy-1)。今月は政策の変更を、局の案にしない
- 交通の流れ 60%: 今月の到達は見込めない(53%)。目標の差は、この月の手では埋まらない
