# m02 調査 health(s02-1 焼却場を止めたあとの埋立地)

## 2050-02-10(見回り1)

- `buildings_near`(x=3300, z=200, radius=900, service=Garbage, limit=15, brief): 4棟。2267 Combustion Plant は problems=TurnedOff。埋立地 3565、28130、29266 は problems=None
- `services` garbage: capacity 160,000,000、used 80,014,021(2050-01-31 は 79,061,516)、full count 0

## 2050-02-20(見回り2)

- `buildings_near`(同じ引数): 2267 は TurnedOff。3565 Landfill Site は problems=Death(前回は None)。28130、29266 は None
- `services` garbage: used 80,634,021、full count 0

## 2050-03-02(月末)

- `buildings_near`(同じ引数): 2267 は TurnedOff。3565 は problems=Death。28130、29266 は None
- `services` garbage: used 81,414,021、full count 0
- 参考 `complaints`: Garbage 22(月初 11)、Pollution 35(月初 45)、Death 60。`map_layer` pollution(3600,-40,r150,n=5): 平均67、最大188(焼却場停止前 平均93、最大255)
- 月末に 2267 を active=true に戻した(議案の中止条件: Garbage が15を超えた)
