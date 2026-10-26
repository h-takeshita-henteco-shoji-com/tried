# m05 調査の結果(health)

## s05-2 汚染の印はごみ施設の近くに集まっているか

問い: 汚染の印は、ごみ施設(焼却場と満杯の埋立地)の近くに集まっているか。

### 見回り1(2050-05-11)

- `buildings_near(x=2070, z=866, radius=250, problem="Pollution", brief=true)`(焼却場10351の周り)
  - total 6: 5971 (1999,806)、23633 (2216,854)、27404 (2168,854)、37309 (2070,764)、45777 (2212,806)、46915 (2066,806)
- `buildings_near(x=3900, z=-575, radius=250, problem="Pollution", brief=true)`(満杯の埋立地25590の周り)
  - total 5: 14175 (3976,-555)、19925 (4024,-531)、31474 (3976,-607)、34720 (4024,-503)、47833 (4024,-636)
- `complaints`
  - Pollution 41、hotspot (3901,-303) 15棟
  - Garbage 8、hotspot (-451,-1385) 3棟
  - Fire と Crime の項目は返らなかった
  - Death 46、Noise 9、NoGoods 182

### 見回り2(2050-05-21)

- `buildings_near(x=2070, z=866, radius=250, problem="Pollution", brief=true)`
  - total 7: 5971 (1999,806)、9893 (2196,854)、23633 (2216,854)、25819 (1975,806)、27404 (2168,854)、46450 (2042,764)、46915 (2066,806)
- `buildings_near(x=3900, z=-575, radius=250, problem="Pollution", brief=true)`
  - total 4: 19925 (4024,-531)、34437 (4024,-579)、34720 (4024,-503)、47833 (4024,-636)
- `complaints`
  - Pollution 41、hotspot (3871,-261) 15棟。examples に 4378 (3532,24)、10822 (3736,-86)、16852 (3564,24)、19925 (4024,-531)、23124 (3604,-68)
  - Garbage 11、hotspot (1246,-1086) 4棟
  - Fire 2(hotspot (3644,-1190) の 9120 H3 2x2 Bigfactory06)、Crime 1(32211 Cargo Harbor (-640,1074))
  - Death 50、Noise 8、NoGoods 185

### 月末(2050-05-31)

- `buildings_near(x=2070, z=866, radius=250, problem="Pollution", brief=true)`
  - total 8: 9893 (2196,854)、25819 (1975,806)、27404 (2168,854)、28167 (1999,854)、28657 (2038,806)、37309 (2070,764)、46450 (2042,764)、46915 (2066,806)
- `buildings_near(x=3900, z=-575, radius=250, problem="Pollution", brief=true)`
  - total 4: 19925 (4024,-531)、34526 (3976,-668)、34720 (4024,-503)、47833 (4024,-636)
- `complaints`
  - Pollution 42、hotspot (3890,-309) 14棟。examples に 4378 (3532,24)、6720 (3681,-94)、10822 (3736,-86)、19925 (4024,-531)、23124 (3604,-68)
  - Garbage 15、hotspot (2266,387) 6棟(高校5088・15042、住宅19260 など)
  - Fire と Crime の項目は返らなかった
  - Death 43、Noise 6、NoGoods 178
