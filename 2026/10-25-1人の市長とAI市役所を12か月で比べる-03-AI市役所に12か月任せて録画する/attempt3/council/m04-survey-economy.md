# s04-3 放棄された店と工場が増える時期と種類(economy)

問い: 放棄された店と工場は、月のうち何日目ごろに、どの種類が増えるか

基準(月例 2050-04-01、市政ノート): 放棄 66棟(`building_stats` で高密度商業45、工業12)、noGoods 166、noResources 29

## 見回り1(2050-04-11)

- `buildings_near(x=0, z=0, radius=10000, abandoned=true, brief=true, limit=100)`: total 76
  - 種類(prefab の名前で数えた): 店・ホテル(Shop、Future Store、Hotel)56(H3 が大半、H2 3棟、L3 2棟)、工場(Factory、Facility)12、住宅(Tenement)4、電柱4
  - 印: NoGoods 52、NoResources 12、Death 2(L3 の店 24747、41535)、Garbage 2、Pollution 2、StructureDamaged 4(電柱)
  - z 約986 の通りの放棄: 17281(2162,986)、35733(2118,986)、42379(2368,986)
- `cargo()`: noGoods 181(多い場所 2250,759 に49、-1122,-1051 に39、822,231 に29)、noResources 33(2895,-852 に15、2204,1193 に13)。stoppedTrucks 840、stoppedInBuildings 598(28755 が579、Cargo Harbor 1366 が19)。Goods の止まった車515。28755 の vehiclesLeaving 851

## 見回り2(2050-04-21)

- `buildings_near(x=0, z=0, radius=10000, abandoned=true, brief=true, limit=100)`: total 85
  - 種類(prefab の名前で数えた): 店・ホテル 66、工場 12(H2 sweatshop 1棟を含む)、住宅 3、電柱4
  - 見回り1 にあって今回ない id 13: 4254、4871、7016、12748、14618、17256、18765、19744、24142、32019、43327、43865、45069
  - 今回新しく出た id 22: 3222(工場)、4341、5681、6504、10693、15267、17036、20779、21039、22735、23472、25933、29929(工場)、32954、36040、36174、37891、40863、41168、44294(工場)、44663、46268。工場3棟のほかは店
  - 印: 店はすべて NoGoods(L3 の 24747、41535 は Death)、工場はすべて NoResources
- `cargo()`: noGoods 185(2246,743 に51、-1104,-1038 に42、780,222 に29)、noResources 32(2810,-893 に16、2210,1169 に12)。stoppedTrucks 867、stoppedOnRoads 290、stoppedInBuildings 577(28755 が576)。Goods の止まった車523。28755 の vehiclesLeaving 858

## 月末(2050-05-01)

- `buildings_near(x=0, z=0, radius=10000, abandoned=true, brief=true, limit=100)`: total 94
  - 種類(prefab の名前で数えた): 店・ホテル 76(H1 1棟、H2 1棟、L3 2棟のほかは H3)、工場 10、住宅 4(L1 1987・L3 34437 の低密度2棟は Pollution)、電柱4
  - 印: 店は NoGoods(L3 の 24747、42869 は Death)、工場は NoResources(7607 だけ Garbage)
  - 見回り2 の工場のうち、今回ない id: 10713、18720、20563、24256、24622、38551。新しく出た工場: 7607、13987、30123、47004
- `cargo()`: noGoods 199(2247,729 に52、-1103,-995 に50、777,225 に31)、noResources 32(2829,-874 に19、2269,1200 に9)。stoppedTrucks 854、stoppedOnRoads 300、stoppedInBuildings 554(28755 が553)。Goods の止まった車550。28755 の vehiclesLeaving 825
