# m11 調査 s11-2(economy): 名所 (1580,-530) を置いた後の効き

基準(置く前): 周りの attractiveness は 0(議案より)。名所 9棟、観光客 1,763(訪問138)、Tourism 週27。

## 2050-12-07(月末)

- `map_layer`(attractiveness, x=1580, z=-530, radius=300, n=5): 平均 14、最小0、最大118(最大は (1580,-530))
- `buildings_near`(service=Monument, x=1580, z=-530, radius=60, brief=true): 40850 Servicing Services、problems は RoadNotConnected
- `city_info`: 観光客 now 1,725、visits 133。`economy_breakdown` の Tourism 週 42

## 2050-11-17(見回り1)

- `map_layer`(attractiveness, x=1580, z=-530, radius=300, n=5): 平均 13、最小0、最大118(最大は (1580,-530))。格子の中央付近は 118、117、53、19 など
- `buildings_near`(service=Monument, x=1580, z=-530, radius=60, brief=true): 40850 Servicing Services、problems は RoadNotConnected(入口の道は引けなかった)
- `city_info`: 観光客 now 1,724、visits 136(置く前 1,763 / 138)
