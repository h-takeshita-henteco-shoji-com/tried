# m13 経済観光文化局の案

## 案なし

第13月は、案を出しません。理由は次の3つです。

- 40850 の道は、調整(計画の調整2)で道路下水道局の roads-2 に任せた。経済観光文化局の案1(南回りの道)は、第13月は採らない
- 旅客の入口と、28755 の出口の振り分けは、港湾空港局の担当に移った。経済観光文化局は、測って渡す
- 働き口、Tourism、attractiveness の事業は、道に面した空きの候補地が、今月の道具では確定できなかった。第14月以降に試す

## 調査

- 調査: あり
- 問い: 40850(名所)の訪問と観光客は、道路が通ったあとで増えるか。
- 見る道具と引数: `buildings_near`(x 1580, z -530, radius 20、brief なし)、`city_info`
- いつ見るか: 見回り2、月末
- 何が分かれば次の手が決まるか:
  - RoadNotConnected が消え、Visitors が 5 より増えれば、道の効きを確かめた。道路下水道局に結果を渡し、14月の南回りは不要と伝える
  - RoadNotConnected が残れば、道路下水道局に南回りの案を求める材料にする(調整2)
  - 道が通っても Visitors が 5 のままなら、名所の効きは道ではなく別の手で見る(計画の変更で直す)
- 担当の問題: 5-1、5-2 観光(名所の棟数、訪問の平均、今いる観光客)

## 見たもの

- `city_info`: 人口 179,020、所持金 2,411,252、週の収入 338,057、週の支出 325,653、観光客 1,765(訪問 132)、需要 住16/商4/工66、来ない市民 0/0/0、dialog なし
- `economy_breakdown`: Tourism の週の収入 28、Monument の週の支出 3,448、政策の費用 10,709、Road の週の支出 8,910
- `demand_breakdown`: 働き口 87,170、空き 2,449、働ける人 79,008、大卒の失業 9,329
- `building_stats`: 事務所(OfficeGeneric)3,979棟のうちレベル3 が 3,279(目標 3,500 まで 221)、商業(高)918 が最大レベル、住宅(高)2,143 が最大レベル
- `buildings_near`(service=Monument、radius 8000): 名所 10棟。どれも働き口は 0。40850 は RoadNotConnected、ほかは問題なし。StatueOfWealth 11580 は電気の印(MajorProblem)
- `list_building_types`(service=Monument): 解禁済みの名所 20種の大きさ、建設費、週の維持費。電気・水・下水が要らないのは StatueOfWealth(電気だけ)
- `list_policies`: 有効は SmokingBan(0)、BigBusiness(週 3,996)。観光の数字を直接動かす政策は見当たらない。政策の費用合計 10,709
- `buildings_near`(abandoned=true、x -1500, z -500, radius 1500、brief): 41棟。多くは店(NoGoods の印)
- `map_layer`(attractiveness、街全体、n=5): 平均 2、最大 30
- `trade`: 輸入 15,896(週)、輸出 1。道と船、鉄道、飛行機のつなぎ口は、いずれも入ってくる車が動いている
- `test_place_building`(Colossal Offices、(-868,-56)、assume_removed 9713): ObjectCollision(道路、歩道、建物が重なる)
- `test_place_building`(Colossal Offices、(-2744,27)、assume_removed 17963): ObjectCollision(道路、店が重なる)
- `test_place_building`(Colossal Offices、(-1344,-1214)、assume_removed 12976): ObjectCollision(道路、建物が重なる)
- `test_place_building`(Friendly Neighborhood、(1650,-45)、west): ObjectCollision、AlreadyExists。Expensive Park 8420 が敷地にある(空きではない)
- `test_place_building`(Official Park、(1650,-45)、west): ObjectCollision、AlreadyExists。同上
- `zone_map`(中心 (0,-400)、radius 1200、size 700): 中心部は密集しており、12x12 の空きは見当たらない
- `zone_map`(中心 (-500,-500)、radius 400、size 600): 事務所(水色)の区画は道に沿って並ぶ。空きの位置は、この図からは確定できない
- `zone_map`(中心 (2000,-300)、radius 500、size 600): 大きな空きは見当たらない。枠線の大きい建物は Expensive Park など
- `buildings_near`(x -1000, z 450, radius 250、brief): 浄水場 5棟(水の施設)。空きの候補地ではない
- `zone_summary`(grid 1000): 事務所 36,777(空き 1,642、道に面した空き 0)、商業(高)8,906(空き 486、道に面した空き 52)、住宅(高)37,676(空き 748、道に面した空き 0)、工業 6,104(空き 66、道に面した空き 0)、商業(低)1,749(空き 90、道に面した空き 0)、住宅(低)10,586(空き 381、道に面した空き 0)
- `test_place_building` の結果(Colossal Offices の3か所、Friendly Neighborhood と Official Park の1か所)から、密集地では名所を置く空きが少ない

## 判断の根拠

- 第13月は案なしにした。案1(南回りの道)は、調整2のとおり道路下水道局の roads-2 に任せ、経済観光文化局は測って渡す。残りの候補(名所の試し、事務所の空きの道)は、道に面した空きの場所が未確定で、道具で確かめた引数がそろっていない。実行条件を満たさない案は出さない
- 調査は1件にした。40850 の訪問が道の前後で動くかを、見回り2と月末に測る。結果で、14月末の測りと、道路下水道局への南回りの材料が決まる
- 前の月(12月)の案1(40850 の西側の道)は、非採択だった。今月の計画では、40850 の道を道路下水道局が引くため、経済観光文化局の案は出さない
- 計画の是正(第1回)で、6-1 を目標に足した。事務所レベル3の 3,279 は、道に面した空きが増えて地価が上がれば増えると見込む(直接は動かさない)。数値は見積もれない
- 名所の棟数の見込み: 名所の棟は働き口 0。働き口 +2,830 は、事務所と商業の建物が道に面して建つことで得る。名所では増やせない
- 働き口と Tourism の数値は、名所1棟の効果で見積もれない。試しの名所を16〜17月に置いて、Visitors と Tourism を測る

## 捨てたもの

- 案1 の南回りの道(1,320、維持費 約10): 調整2で道路下水道局が引く。経済観光文化局の案からは外す
- Colossal Offices(70,000、維持費 1,200)の密集地への置き直し: 3か所の試しで ObjectCollision。12x12 の空きが見当たらない。島Bは水と下水が来ない(前の月の判断)
- Friendly Neighborhood、Official Park の既存の名所の敷地: Expensive Park 8420 がある。空きではない
- 働き口の空きに面する道の案: 道路下水道局の担当。今月は経済の案にせず、計画の事業3で求める
- 品物がない店の出口の改善: 調整5で港湾空港局の振り分けに一本化。経済観光文化局は測るだけ
- 政策の有効化(RecreationalUse 等): 効きが確かめられず、今月は見送り
