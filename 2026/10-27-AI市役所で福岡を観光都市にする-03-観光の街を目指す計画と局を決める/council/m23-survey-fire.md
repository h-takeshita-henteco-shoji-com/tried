# m23 調査 s23-3(fire): 48237 の火事と消防署の出動

問い: 48237 の火事は燃え続けているのに、近くの消防署の車が出ていないのはなぜか。出動が見えるか。

## 2051-11-12(見回り1)

- `buildings_near`(x=2643, z=1437, r=5, service=FireDepartment): Fire House 26833、problems None、workers 31、vehicles inUse 0、Fire engines in use: 0 / 8
- `buildings_near`(x=2834, z=1118, r=30): 3棟。48237(H3 3x2 Office01)problems "Fire, FatalProblem"、電気・水・下水 true。3556 と 28124 は problems None
- `complaints`: Fire 1棟(48237、hotspot (2834,1118))。Crime 6、Pollution 28、Garbage 7

## 2051-11-22(見回り2)

- `buildings_near`(x=2643, z=1437, r=5, service=FireDepartment): Fire House 26833、problems None、workers 30、Fire engines in use: 0 / 8
- `buildings_near`(x=2834, z=1118, r=30): 48237 は problems "Fire, FatalProblem" のまま。3556 と 28124 は None
- `complaints`: Fire 1棟(48237)。Crime 3、Pollution 37、Garbage 8

## 2051-12-02(月末)

- `buildings_near`(x=2643, z=1437, r=5, service=FireDepartment): Fire House 26833、problems None、workers 30、Fire engines in use: 0 / 8
- `buildings_near`(x=2834, z=1118, r=30): 48237 は problems "Fire, FatalProblem" のまま(3回の測りで不変)。3556 と 28124 は None
- `complaints`: Fire 2棟(hotspot (2134,-218)、examples は 47239 の1件のみ)。Crime 4(例: 埋立地 23459)、Pollution 43、Garbage 12
