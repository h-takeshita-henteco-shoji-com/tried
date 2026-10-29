# m04 調査 s04-3 汚染の印の場所(焼却場10351の周り、health)

## 2050-04-12(見回り1)

- `buildings_near`(x=2086, z=760, radius=250, problem=Pollution, brief=true): total 9。すべて住宅(Tenement、Highrise)で x 1975〜2196、z 764〜854。うち 36594 は FatalProblem、28138 は MajorProblem、9893 は Death を併発
- `map_layer`(pollution, x=2086, z=800, radius=200, n=5): 平均 97、min 0、max 255(maxAt 2086,1000)。北寄りの3行で 255 が集中、南2行はほぼ 0 (東南の2点が 251)
- 参考 `complaints`: Pollution 34(月初26)、hotspot (2065.8,404.7) 12棟

## 2050-04-22(見回り2)

- `buildings_near`(x=2086, z=760, radius=250, problem=Pollution, brief=true): total 8。すべて住宅で x 1999〜2196、z 756〜854。顔ぶれは一部入れ替わり(36594、28138、32913 が外れ、5971、16718 が入る)
- `map_layer`(pollution, x=2086, z=800, radius=200, n=5): 平均 97、min 0、max 255(maxAt 2086,900)。北寄りの3行に 252〜255 が集中。南2行はほぼ 0(東南の2点が 246、255)
- 参考 `complaints`: Pollution 35、hotspot (3845.2,-301.1) 12棟に移った

## 2050-05-02(月末)

- `buildings_near`(x=2086, z=760, radius=250, problem=Pollution, brief=true): total 11。すべて住宅(x 1975〜2216、z 716〜854)。MajorProblem 併発 4棟(27404、28167、45069、46477)、Garbage 併発 1棟(70)
- `map_layer`(pollution, x=2086, z=800, radius=200, n=5): 平均 96、min 0、max 255(maxAt 2086,900)。北寄りの3行に 251〜255 が集中。南2行はほぼ 0(東南の2点が 249、252)
- 推移(事実): 印の棟数 9→8→11。pollution 平均 97→97→96
- 参考 `complaints`: Pollution 40、hotspot (3827.4,-272.4) 15棟
