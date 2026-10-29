# m01 調査 s01-3(urban): 公園を置ける場所

見立ては書かない。局が翌月に読んで決める。

日付: 2050-01-31(月末)

- `zone_summary(grid=500)`: 空き区画は Office 1,642、CommercialHigh 575、ResidentialHigh 709、ResidentialLow 381、CommercialLow 90、Industrial 66。全部 emptyBehind(道の側から続かない空き)が主で、emptyFacingRoad は CommercialHigh の 133 のみ
- 空きが多い区切り(中心): (2250, 250) CommercialHigh 95 / ResidentialHigh 66、(2250, -750) ResidentialHigh 132 / Office 43、(2250, -250) ResidentialHigh 83 / CommercialHigh 69、(250, -250) ResidentialHigh 91 / Office 62、(-250, -250) Office 90
- `buildings_near(x=250, z=-250, radius=500, service="Beautification", limit=50, brief)`: total 10。Regular Park 6(410,-210 / 610,-389 / 410,-389 / 190,-210 / 610,-210 / 190,-389)、JapaneseGarden 3(370,-328 / 446,82 / 366,82)、Expensive Park 1(245,-591)
- `test_place_building`: 議案に候補地(座標と prefab)がなく、引数を決められないため呼ばなかった。調査にない座標を市長が作らない決まりによる
