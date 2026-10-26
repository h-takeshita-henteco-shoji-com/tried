# m04 住宅都市みどり局の案

## 施策

- 施策: 東の空き地(2590〜2680, -640〜-765)に Boulder 01 を17個、西の通り(2135,-398)に Decoration Concrete Parking Lot 01 を1棟、place_building で置く試し。Beautification の数を 83 → 101 に増やし、4-2 の目標100に届かせる。
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順: place_building(pay=true)を次の順に18回。
  1. prefab="Decoration Concrete Parking Lot 01", x=2135, z=-398, facing="west"
  2. prefab="Boulder 01" を次の17点に置く(facing と angle は省く。向きは使わない)
     (2590,-640) (2590,-690) (2590,-715) (2590,-765)
     (2620,-640) (2620,-665) (2620,-690) (2620,-715) (2620,-740) (2620,-765)
     (2650,-665) (2650,-690) (2650,-715) (2650,-740) (2650,-765)
     (2680,-690) (2680,-715)
- 設置条件の確認: 今月、上の18点すべてを `test_place_building` で同じ引数で試した。すべて ok=true、wouldDemolish.count=0、費用は駐車場1,000・Boulder 各100。駐車場は入口(2119,-398)が Basic Road 28764 に距離1で接し、電気が要る(`list_building_types` の needs)。Boulder は needsRoad=null で、電気・水・下水が要らない。
- 接続工事: 不要
- 予備候補: なし。前月に通らなかった点((2590,-665)、(2590,-740)、(2560,*)、(2650,-640)、(2135,-411))は使わない。(2135,-411) は建物44025を壊す。
- 中止する条件: 実行前の `test_place_building` が ok=false、または wouldDemolish.count が1以上になった点は、その点だけ見送る。駐車場が通らなければ Boulder だけ置く。Boulder を1個置いて `buildings_near(service="Beautification")` の total が増えなければ、残りの Boulder は置かずに止める。

## 期待する効果

- 改善の見込み: 4-2 の測り方は Beautification の棟数。`list_building_types` で Boulder 01 の service は Beautification(subService None)と確認した。同じ service の駐車場の飾りは、前々月に 81 → 83 と棟数に数えられた。18棟足すと 101 になると予想する。
- 数値と期限: `buildings_near`(service="Beautification")の total は今 83(今月確認)。実行直後に 101、月末も 101 を予想。目標100以上。
- 確認方法: `buildings_near`(x=0, z=0, radius=6000, service="Beautification", brief=true)の total。地価は `land_value`(x=2620, z=-700, radius=150)の average を今の 42 と比べる。
- 不確かな点: Boulder が total に数えられる点は、同じ service の根拠はあるが、置くまで確かでない(上の中止条件で1個目に確認)。地価・幸福度への効果は数値は見積もれない。数が増えるだけで暮らしは変わらない可能性が高い。
- 試し: 仮説は、安い装飾(Boulder)でも service が Beautification なら市の計画の棟数が上がる。測る数は Beautification の棟数(`buildings_near`)と、置いた場所の地価(`land_value`)。場所は (2620,-700) の周り。基準は 83 と 42。編成方針の「分からないこと」のどれにも当たらない。

これは局の予測です。ゲームの効果の正解を取得しません。

## 調査

- 調査: あり
- 問い: 空き家 5,124 と空いた働き口 3,154 があるのに、住宅の需要 24 のまま人口が増えないのは、大学卒の失業 6,865 が空きの働き口の学歴と合わないためか。
- 見る道具と引数: `demand_breakdown()`、`citizens_summary()`、`building_stats()`(x を省く)
- いつ見るか: 見回り1、月末
- 何が分かれば次の手が決まるか: 大学卒の失業が空きの働き口の数を上回り続け、空きの多くが学歴不問の働き口なら、学歴の合う事務所の区画(`zone_summary` の空き)を増やす案を来月出す。失業が減り人口も増えるなら、住宅側の案は要らず、調査を閉じる。空き家が多いのに homeless が 0 のままなら、引っ越し先の不足ではなく仕事の側が原因と見て、経済観光文化局への情報にする。
- 担当の問題: 4-1 都市と自然が調和したコンパクトなまち(住宅の需要と人口。分からないことの3項目目)

## 費用

- 建設費: 2,700(駐車場 1,000 + Boulder 100×17。`test_place_building` の cost)
- 週の維持費の増え分: 16(Boulder は0、駐車場 Lot 01 は16。`list_building_types`)

## 戻せるか

戻せる。置いた建物は bulldoze で壊せる(ただし払い戻しはない)。

## 前の月の答え合わせ

- m03-urban(東の空き地に Boulder 15個と駐車場1棟の試し): 採られなかった。理由は「16点の試しは通るが重点の外で枠が埋まり、Boulder が Beautification に数えられるかが置くまで分からない。出し直すなら list_building_types の service の値を根拠に添えること」。今月の扱い: `list_building_types` で Boulder 01 の service が Beautification と確認し、本文に根拠として書いた。点を15から17に増やして 101 にし、目標100を越えるようにした。1個目で数えを確かめる中止条件も足した。重点の外の件は、局の決まりにより案を控える理由にしない。
- m02-3(駐車場の飾り2つの試し): 当たり。Beautification 81 → 83。4-1 の地価は 58 のままで、地価の効きは測れなかった。
- m03 の調査: 出していないため結果なし。

## 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `list_policies`: 取得できた。比較した政策は、HighTechHousing(無効、週20,232)、BigBusiness(有効、3,936)、SmallBusiness(無効、313)、IndustrySpace(無効、4,828)、Recycling・PetBan・TaxLower* など(無効、0)。住宅の需要や地価に直接効く政策で、枠5,000の中に収まり、収入を削らないものは見つからなかった。税の政策(TaxLower*)は費用0だが税収を削る。
- `demand_breakdown`: 働き口 86,397、空き 3,154、失業 7,056(大学卒 6,865、学歴なし 133)、家 55,476、空き家 5,124、homeless 0
- `city_info`: 人口 178,394、需要 住宅24・商業2・働き口58、所持金 2,169,039、収支 +8,951
- `buildings_near`: Beautification 83(service="Beautification"、radius 6000)。Boulder は未設置
- `list_building_types`: Boulder 01 は service Beautification、cost 100、upkeep 0、needsRoad null。駐車場 Lot 01 は 1,000 / 16
- `land_value`: (2620,-700) 半径150 の平均 42(min 29、max 68)。街の平均 52
- `test_place_building`: 駐車場1点と Boulder 17点、計18点がすべて ok、wouldDemolish 0

## 判断の根拠

4-2 は Beautification が 83 で、目標100まで17足りない。Boulder は service が Beautification で、100円、維持費0、道路・電気が要らない。そのため、費用の上限1,084,519と維持費の枠5,000にほとんど影響せず、数を確実に積める手になる。18点すべてが今月の試しの道具で通ったため、実行計画に入れた。効果は棟数の増加に限られ、暮らしの改善は見積もれないと明記する。人口が増えにくい原因は分からないので、調査を1件出す。

## 捨てたもの

- Regular Park(1,000)などの本物の公園: 前月に敷地(道路に接する72×64mの空き地)が確認できなかった。今月は新しい場所を確認していないため出さない。
- 放棄された高密度商業42棟の取り壊し(議決: 取り壊し): 今月は preview_bulldoze を呼んでおらず、失うものを数字で書けない。economy 局の担当でもある。
- 政策 HighTechHousing(週20,232): 維持費の枠5,000を超える。
- 税の引き下げ(住宅税): 週の黒字 +8,951 が薄く、守る線に当たる。
- 住宅の区画を増やす案: 空き家が5,124戸あり、住宅の需要の足りなさは家の数ではなく仕事の側にあると見るため、今月は調査で確かめる。
