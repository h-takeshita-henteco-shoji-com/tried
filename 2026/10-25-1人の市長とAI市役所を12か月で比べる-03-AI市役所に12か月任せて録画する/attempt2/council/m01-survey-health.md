# s01-3 ごみの印の原因(health)

問い: ごみの印15棟は、収集車の不足と処理場の満杯のどちらから来ているか

## 見回り1(2050-01-11)

### `buildings_near(x=-458, z=-1468, radius=400, problem="Garbage", limit=30)`

- total 10。全部が住宅(Tenement)で、電気・水・下水は来ている
- id と位置: 672 (-652, -1384)、2717 (-370.5, -1236)、5049 (-480, -1336)、16326 (-523, -1384)、22784 (-724, -1497)、29776 (-676, -1384)、33255 (-724, -1422)、33792 (-680, -1284)、45106 (-724, -1521)、48570 (-688, -1236)

### `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`

- total 1。33797 Combustion Plant (-570, -1840)、problems None
- storage 385,000 / 400,000(96%)
- stats: Processing rate 60,000 / week、Garbage trucks in use 10 / 34
- workers 29

### 参考(m01-2 の確かめで見た値)

- `buildings_near(x=-650, z=-490, radius=50, service="Garbage")`: 16914 は Emptying、7,620,000 / 8,000,000(95%)、車 19 / 19

## 見回り2(2050-01-21)

### `buildings_near(x=-458, z=-1468, radius=400, problem="Garbage", limit=30)`

- total 6。全部が住宅(Tenement)
- id と位置: 672 (-652, -1384)、14981 (-724, -1347)、22784 (-724, -1497)、29776 (-676, -1384)、33255 (-724, -1422)、45106 (-724, -1521)
- 見回り1から消えた: 2717、5049、16326、33792、48570。新しく出た: 14981

### `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`

- 33797 Combustion Plant、problems None
- storage 396,250 / 400,000(99%)
- stats: Processing rate 60,000 / week、Garbage trucks in use 3 / 34

### 参考(m01-2 の確かめで見た値)

- `buildings_near(x=-650, z=-490, radius=50, service="Garbage")`: 16914 は Emptying、7,620,000 / 8,000,000(95%)、車 19 / 19。見回り1から量は変わっていない

## 月末(2050-01-31)

### `buildings_near(x=-458, z=-1468, radius=400, problem="Garbage", limit=30)`

- total 5。全部が住宅(Tenement)
- id と位置: 672 (-652, -1384)、5118 (-724, -1396)、21897 (-354.5, -1384)、29776 (-676, -1384)、33255 (-724, -1422)
- 見回り2から消えた: 14981、22784、45106。新しく出た: 5118、21897

### `buildings_near(x=-570, z=-1840, radius=300, service="Garbage")`

- 33797 Combustion Plant、problems None
- storage 330,000 / 400,000(82%)
- stats: Processing rate 60,000 / week、Garbage trucks in use 13 / 34

### 参考(m01-2 の確かめで見た値)

- `buildings_near(x=-650, z=-490, radius=50, service="Garbage")`: 16914 は Emptying、7,620,000 / 8,000,000(95%)、車 19 / 19。見回り1から量は変わっていない
- `services`: garbage.full.count 6(19182、23032、25590、25826、29270、45892。16914 が外れた)、used 126,950,203 / 160,000,000
