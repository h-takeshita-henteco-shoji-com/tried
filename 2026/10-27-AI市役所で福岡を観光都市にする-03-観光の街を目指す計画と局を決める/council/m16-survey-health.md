# m16 調査 s16-2(health): 霊柩車が東の幹線の混みで止まるか

## 2051-04-16(見回り1)

- `vehicles_stuck`(kind hearse、building 39843、limit 10): vehicles 6。状態は全部 Congestion+...+Blocked(うち GoingBack 3)。道順は6台とも ready。止まって見えた日数は 7days+ が4台、<1day が2台(最大40日)。位置は (3166,-320)、(3146,-456)、(2684,-492)、(2877,-491)、(3442,-256)、(2562,326)
- `traffic`(x3200 z-260 r150): flow 55、cars 96、blocked 0、congestion 39、averageDensity 68。density 100 の区間は (3174,-205)、(3154,-381)、(3204,-254)、(3189,-310)
- `buildings_near`(x3598 z-90 r40): 火葬場 39843 は problems None、電気・水・下水 true、workers 30。Deceased stored 0 / 105、Deceased processed last week 0、Hearses in use 8 / 9

## 2051-05-06(月末)

- `vehicles_stuck`(kind hearse、building 39843、limit 10): vehicles 8。Blocked 付き3台(GoingBack 2)、Blocked なし5台。道順は8台とも ready。7days+ が5台、<1day が3台。最長60日(vehicle 5029、(3407,-122) GoingBack)。Blocked の位置は (2820,-492) blockCounter 86、(3027,-492) blockCounter 106、(3733,-254) blockCounter 50
- `traffic`(x3200 z-260 r150): flow 52、cars 88、blocked 19(blockedSpots (3164,-297) 18)、congestion 39、averageDensity 63。density 100 は 7区間
- `buildings_near`(x3598 z-90 r40): 火葬場 39843 は Deceased stored 0 / 105、Deceased processed last week 0、Hearses in use 8 / 9。problems None。`services` deathcare used 14,723 / 24,000

## 2051-04-26(見回り2)

- `vehicles_stuck`(kind hearse、building 39843、limit 10): vehicles 7。Blocked 付き4台(GoingBack 3)、Blocked なし3台。道順は7台とも ready。7days+ が5台、<1day が2台。最長50日(vehicle 5029、(3166,-362) で GoingBack、blockCounter 68)。ほかの Blocked 位置は (2764,-492)、(2964,-491)、(3574,-254)
- `traffic`(x3200 z-260 r150): flow 55、cars 96、blocked 28(blockedSpots (3153,-301) 19、(3220,-314) 9)、congestion 42、averageDensity 65。density 100 は (3154,-381)、(3281,-254)、(3204,-254)、(3174,-205)、(3189,-310)
- `buildings_near`(x3598 z-90 r40): 火葬場 39843 は Deceased stored 0 / 105、Deceased processed last week 0、Hearses in use 8 / 9。problems None
