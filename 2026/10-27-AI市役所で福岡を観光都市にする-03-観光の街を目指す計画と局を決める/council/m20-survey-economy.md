# m20 調査 s20-1 名所の訪問と外とのつなぎ口の近さ

## 2051-08-14 見回り1

- `buildings_near`(x 0, z 0, service Monument, radius 9000, limit 10): total 10。訪問(Visitors last week / Tourists last week)
  - SeaWorld 2374 (-1350,-796): 51 / 16
  - Friendly Neighborhood 7856 (2290,972): 10 / 8
  - Countdown Clock 9113 (1765,622): 19 / 14
  - StatueOfWealth 11580 (668,1565): 3 / 2(水・下水なし)
  - ScienceCenter 29187 (-1130,-804): 12 / 4
  - Winter Market 01 30532 (-1550,-205): 13 / 8
  - Servicing Services 40850 (1580,-530): 8 / 4(Crime, MajorProblem)
  - Fountain of LifeDeath 41780 (1804,170): 12 / 11
  - Plaza of Transference 45587 (-1560,-855): Passengers serviced 0
  - Official Park 46934 (2118,482): 6 / 2
- `trade`: import 16,008(goods 7,491)、export 1。つなぎ口の入る車の今: road 8840 (5788,-8649) 190、road 19832 (5818,-8649) 入50・出10、road 27833 (5294,8649) 140、road 43980 (5264,8649) 入12・出6、ship 17593 入9、train 32589 入6、train 34128 入5、plane 10494 / 38612 / train 19489 は0
- `city_info`: tourists now 1,784、visits 151

## 2051-08-24 見回り2

- `buildings_near`(Monument, total 10)。訪問 / 観光客(先週): SeaWorld 50/16、Friendly Neighborhood 9/6、Countdown Clock 18/13、StatueOfWealth 6/5、ScienceCenter 12/4、Winter Market 13/9、Servicing Services 5/2、Fountain of LifeDeath 12/11、Plaza of Transference 0(Passengers)、Official Park 13/9
- `trade`: import 15,862(goods 7,481)、export 1。road 8840 入204、road 19832 入52・出11、road 27833 入155、road 43980 入12・出6、ship 17593 入9、train 32589 入5、train 34128 入7、plane・train 19489 は0
- `city_info`: tourists now 1,810、visits 148

## 2051-09-03 月末

- `buildings_near`(Monument, brief, total 10)。10棟とも前回と同じ。Servicing Services 40850 は Crime, MajorProblem のまま。訪問数は brief では出ない
- `trade`: import 15,714(goods 7,508)、export 1。road 8840 入202、road 19832 入44・出15、road 27833 入156、road 43980 入15・出8、ship 17593 入9、train 32589 入6、train 34128 入6、plane・train 19489 は0
- `city_info`: tourists now 1,837、visits 164
