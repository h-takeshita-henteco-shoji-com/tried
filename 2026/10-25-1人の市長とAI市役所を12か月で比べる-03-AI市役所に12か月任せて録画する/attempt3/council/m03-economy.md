# m03 経済観光文化局の案

## 施策

- 施策: 街全体の放棄された区画の建物121棟(店と工場が中心)を、`bulldoze(x=0, z=0, radius=10000, what="abandoned")` で取り壊す。品物がない店と原料がない工場の印を、死んだ建物から消す。
- 議決: 取り壊し

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 実行前に `buildings_near(x=0, z=0, radius=10000, abandoned=True, brief=True, limit=150)` を測る(今日の total は125。うち電柱4本は区画の建物でなく対象外)
  2. `preview_bulldoze(x=0, z=0, radius=10000, what="abandoned")` で targets.buildings 121、lost.jobs 0、lost.homes 0、power.buildingsLosingPower 0 を確かめる
  3. `bulldoze(x=0, z=0, radius=10000, what="abandoned")`
  4. 実行後に `cargo`(shortages の noGoods と noResources)、`complaints`(火事・死体の印)、`buildings_near(abandoned=True)` を測る
- 設置条件の確認: 該当なし(建設ではない)。確認は次のとおり。`buildings_near(abandoned=True)` で放棄された建物125(商業中心の店・ホテル、工場、電柱4本)を確認。`preview_bulldoze(what="abandoned")` で壊す121棟は全部 jobs 0・homes 0、道路の区間0、送電線の区間0、電気が切れる建物0、水の施設0、駅・港0、modelAgreement 1.0
- 接続工事: 不要
- 予備候補: なし。radius 10000 の呼び出しが断られたら、実行を見送り、市長が引数を直して議会に出し直す
- 中止する条件: 実行前の `preview_bulldoze` で、lost.jobs か lost.homes が0でない、waterFacilities か transportStations が空でない、power.buildingsLosingPower が0でない、のどれかなら見送る。targets.buildings が121から大きく外れる(100未満か140超)ときも見送る

## 期待する効果

- 改善の見込み: 品物がない店229のうち約106棟と、原料がない工場34のうち約10棟は、放棄された建物(NoGoods か NoResources と FatalProblem)の印です。働き口0の死んだ建物なので、壊せば印が数から消えます。区画が空き、建て替えの需要が出れば新しい店や工場が建ちます。ただし、店に品物が届かない原因(輸入品物のトラックが貨物駅28755 で止まる)は残るので、建て替えた店が再び放棄される可能性があります。
- 数値と期限: `cargo` の品物がない店 229 → 約123(目標120以下に近づく)、原料がない工場 34 → 約24(目標15以下に近づく)。`complaints` の火事 1 → 0(12882 の焼け跡を含む)。壊した直後の `cargo` で確かめる。翌月の月例まで、同じ数が再び増えるかも見る。数は火災の印と放棄の内訳からの局の計算で、効果の実測ではない
- 確認方法: `cargo` の shortages.noGoods.buildings と noResources.buildings、`buildings_near(x=0, z=0, radius=10000, abandoned=True)` の total(125 → 4 になる見込み。電柱は残る)、`new_buildings` の CommercialHigh と IndustrialGeneric の増えた数(建て替えの確認)。今の値と同じ道具・同じ範囲で比べる
- 不確かな点: 建て替えの数は見積もれない(商業の需要は2、工業は59)。放棄が再び起きる率も未確認。品物がない店のうち生きている店(約123棟)には効かない。働き口は増えない(壊す建物の働き口は0)ため、6-4・7-1 の働き口(86,452)の目標には直接効かない
- 試し: なし

## 調査

- 調査: なし

## 費用

- 建設費: 0(取り壊しの払い戻しも費用もない。`preview_bulldoze` で確認)
- 週の維持費の増え分: 0(減る側。放棄された建物は維持費の増減なし)

## 戻せるか

戻せない。取り壊した建物は元に戻せないが、区画の指定は残るので、需要があれば新しい建物が建つ。

## 前の月の答え合わせ

- m02-1(道沿いの未指定マス70を工業区画にする、試し): 半分当たり。市政ノートのとおり、工業は4→13棟、働き口は54→120(+66)で、予想の数百に届かなかった。今月の `building_stats` では、街全体の IndustrialGeneric は815棟・jobs 10,771、`zones_at`(3470,-1040、r200)の Industrial 319 のうち空き18。働き口は街全体で86,175→86,452(+277)。
- 前の月の自分の調査: m02 は調査を出さなかったので、結果ファイルなし。
- 今月の扱い: 工業の空きは18まで減り、需要の側の失業は大学卒7,126で、工業の働き口(低学歴向け)では吸えない。工業をさらに増やす案は出さない。

## 市の計画

- 当たる施策: 6-4、7-1 企業の立地、地場企業(品物がない店と原料がない工場)
- 編成方針の重点に当たるか: 当たる

## 見たもの

- `list_policies`: 取得できた。BigBusiness 有効(週3,900)、EducationBoost 有効(週7,940。教育の支出に計上)。SmallBusiness 無効(週315)、IndustrySpace 無効(週4,864)、TaxLowerOffice 無効(週0)、TaxRaiseOffice 無効(週0)、Recycling 無効(週0)。工業・事務所に効きそうな IndustrySpace は週4,864で枠4,000を超える。効果の数字は読めない
- `demand_breakdown`: jobs 86,452、emptyJobs 3,323、失業7,318(大学卒7,126、学歴なし118)、homes 55,485、空き家5,085
- `cargo`: 品物がない店229、原料がない工場34、stoppedInBuildings 555(28755 が534)、Goods の輸入トラックの停止562
- `building_stats`: 街全体 事務所3,979棟(L1 67、L2 680、L3 3,232)・jobs 53,210、商業(高密度)1,104棟のうち放棄109、工業815棟のうち放棄10、商業(低密度)165棟のうち放棄1
- `zone_summary`: 事務所の空き1,642はすべて道に面さない(emptyBehind)。工業の空き79も同じ。道に面した空きは商業(高密度)140
- `zone_map`: (1500,-500、r2000)と (3470,-1040、r250)。未指定の灰色マスが 3445〜3530,-1085〜-1005 に残る
- `zones_at`: (3470,-1040、r200)Unzoned 164、Industrial 319(空き18)。(3490,-1055、r45)Unzoned 29
- `map_layer`: electricity_service(3480,-1055、r60、n13)は全点1
- `net_near`: (3480,-1055)Electricity 送電線2区間、Road は Small 4 Lane Road 4区間
- `water_trace`: (3450,-1055)と (3525,-1040)の近くの建物は電気・水・下水が来ている
- `buildings_near`: abandoned=True で total 125(NoGoods 106棟ほど、NoResources 10、Fire 1、Death 3、Water 1、電柱 StructureDamaged 4)。problem=NoGoods の total 229、problem=NoResources の total 34。(3490,-1055、r60)に建物4
- `new_buildings`: since 0 で OfficeGeneric 3,979、CommercialHigh 1,104、IndustrialGeneric 815 など(累計)
- `preview_bulldoze`: (0,0、r10000、what=abandoned)targets.buildings 121、segments 0、powerLineSegments 0、lost.jobs 0、lost.homes 0、waterFacilities 0、transportStations 0、buildingsLosingPower 0、modelAgreement 1.0

## 判断の根拠

放棄された建物は店と工場を中心に121棟あり、働き口は0です。品物がない店229のうち約106棟、原料がない工場34のうち約10棟は、この放棄の建物の印です。壊しても失うものは0と `preview_bulldoze` で確かめました。印を数から外せることと、区画が空いて建て替えが起きる余地ができることから、目標(120以下 / 15以下)に近づく手と考えます。失業の大半が大学卒で、事務所の道沿いの空き区画は0のため、今月は工業・事務所の新規指定に代わる手は確認できませんでした。

## 捨てたもの

- 工業区画のさらなる指定(3445〜3530,-1085〜-1005 の未指定マス): 工業の空きが18まで減り、失業の大半は大学卒で工業の働き口では吸えない。原料がない工場も増やしかねない
- 事務所の区画指定: 事務所の空き1,642はすべて道に面さず、道沿いの未指定マスを事務所にできる場所の電気・水の確認が、地図から読めた範囲(3445〜3530,-1085〜-1005)に限られる。事務所のレベル(L2 680棟)が上がらない原因(levelUp の条件)は道具で読めず、効く手は確認できなかった
- 政策 IndustrySpace(週4,864): 維持費の枠4,000を超える。効果の量が読めない
- 政策 SmallBusiness(週315)・TaxLowerOffice(週0): 効きの見込みと確認方法が示せず、議決(税)の枠を取り壊しと分けられない
- 観光(5-1、5-2): 観光客1,696で目標に+304。放棄ホテル5棟は今回の取り壊しに含まれ、新しい施設の案は今月の確認が足りない
