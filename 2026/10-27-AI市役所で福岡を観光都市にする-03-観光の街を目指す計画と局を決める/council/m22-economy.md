# m22 経済観光文化局の案

## 案なし

案を1件も出さない。理由は次の2つ。

- 名所の候補地が確かめられない: 未建設の名所の最安は Transport Tower(60,000 / 週960)で、週320の上限(調整8)を超える。置き場所は、道路に面した空きが名所の大きさに足りず、試した5地点はすべて道路か住宅・働き口と重なった。取り壊しで住宅や働き口を失う案は、採らない
- 旅客の入口は港湾空港局の担当で、経済観光文化局の手ではない

22月末の「やめる条件」(置ける場所が確かめられないとき、名所の事業を閉じる)を満たしたので、名所の事業は閉じる。上限の見直しは市長に求める。

## 調査

- 調査: あり
- 問い: 魅力度の高い点(1818,332 付近で 295)は、どの建物の周りに出ていて、見回りごとに動くか。
- 見る道具と引数: `buildings_near`(x=1818, z=332, radius=80, brief=true)、`map_layer`(type="attractiveness", x=1818, z=332, radius=150, n=5)
- いつ見るか: 見回り1、見回り2、月末
- 何が分かれば次の手が決まるか: 魅力度の高い点の近くに店(商業)か公園や名所があれば、23月に、その近くの商業の店を伸ばす手を調べる。近くに建物がなく、点が動くなら、魅力度の測り方が揺れると見て、調査を続けない。
- 担当の問題: 5-1、5-2 観光(attractiveness の平均と名所の棟数)

## 見たもの

- `city_info`: 人口173,537、所持金2,643,814、週の収支 +5,957(収入335,699、支出329,742)、幸福度87、観光客2,020(訪問171)、需要 住34/商2/工43、来ない市民 0/0/0
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940)、BigBusiness(4,068)。SmallBusiness は無効(319)、RecreationalUse は無効(0、効きの記述なし)。政策の費用の計は 10,794/週。観光に効く政策は、効きが確かめられていない(m02、m03、m05 の結果が割れた)
- `list_building_types`(service=Monument): 解禁済みは 21 種。建設済みの型(SeaWorld、Friendly Neighborhood、Countdown Clock、StatueOfWealth、ScienceCenter、Winter Market 01、Servicing Services、Fountain of LifeDeath、Plaza of Transference、Official Park)を除くと、最安は Transport Tower(60,000 / 960)。次は Colossal Offices(70,000 / 1,200)、Observatory(85,000 / 1,600)、Grand Mall(85,000 / 1,280)
- `buildings_near`(service=Monument、x=0、z=0、r=6000): 10棟。中心の数は観光の名所の 10 を満たす
- `buildings_near`(abandoned=true、r=5000): 112棟。ほぼすべて店・工場・住宅の放棄(NoGoods、NoResources、Death)
- `zone_summary`(grid=1000): 道路に面した空きは、CommercialHigh の 68 マスだけ(Office、ResidentialHigh は奥だけ)
- `zone_map`(x=500, z=0, r=1500): 道路沿いの空きは少ない。北と東の空きは、道路から離れている
- `zone_map`(x=2150, z=450, r=400)、`zone_map`(x=2450, z=450, r=200): 東の商業とオフィスの帯は、ほぼ埋まっている
- `net_near`(x=2450, z=450, r=150)、`net_near`(x=2136, z=580, r=90): 道路の区間を確かめた。z=330、z=560 の幹線の間は住宅で埋まる
- `buildings_near`(x=2136, z=600, r=80): 26棟、すべて店かオフィス。空きなし
- `test_place_building`(Transport Tower、324,222、assume 7265): 不採用。道路 5 区間(blocks)と、住宅 3棟・店 3棟が重なる
- `test_place_building`(Transport Tower、564,-146、assume 5573): 不採用。道路と歩道、公園 27644 が重なる
- `test_place_building`(Transport Tower、96,264、assume 12561): 不採用。道路 5 区間と、オフィス・店 7棟が重なる
- `test_place_building`(Transport Tower、2500,-546、assume 4125): 不採用。道路 2 区間と、住宅・店 10棟が重なる
- `test_place_building`(Transport Tower、3513,-96、assume 17697): 不採用。道路 2 区間と、住宅 7棟が重なる
- `map_layer`(type=attractiveness、x=2118, z=482, r=300, n=5): 平均 37、最大 295(1818,332)。魅力度は点で偏って、街全体の平均 2 は大半が 0 のため
- `list_transport_lines`(type=bus): 読んだが、観光の判断には使わなかった(路線の台数と乗客は、交通局の担当)

## 判断の根拠

- 21月は案なしで、22月は置き場所を探した。試した5地点は道路と既存の建物に重なり、取り壊しなしでは置けなかった。取り壊しの候補は、住宅と働き口を失う。道路に面した空きは、citywide で CommercialHigh の 68 マスだけで、名所の大きさに足りないと見た(名所の大きさは道具の数字で、マスの大きさは確かめていない)
- 最安の名所 Transport Tower は週960で、調整8の週320上限を超える。上限を超える案は、実行の前に市長が決める
- 魅力度は、名所の周りに偏って出る(最大295、平均2)。名所を置く場所は、ここで探す。ただし、点の出どころは未確認なので、調査 s22-1 で確かめる
- 案の数は0。調査は1件(魅力度の高い点の出どころ)。調査は街を変えず、見る道具だけを使う
- m21-survey-economy.md は無いので、前の月の調査の答え合わせはなし

## 捨てたもの

- Transport Tower を (324,222)、(564,-146)、(96,264)、(2500,-546)、(3513,-96) に置く案: 道路の中心線と重なるか、住宅・働き口を失う。試しで断られた。取り壊しの案にすると、住宅と働き口を失う
- 名所を空き地3、島B に置く案: 水・下水の管がなく、水・下水の見積もりも道路下水道局が出していない。22月は確かめられなかった
- Observatory、Grand Mall、Colossal Offices など、ほかの未建設の名所: 維持費が週1,000〜1,600で、週320の上限と市の守る線(+3,000)の余裕に合わない
- 政策 RecreationalUse、SmallBusiness を戻す案: 効きが m02〜m05 で切り分けられず、確かめる手が残っていない。観光の数字の前提を変えられない
