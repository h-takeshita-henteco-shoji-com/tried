# m09 調査 s09-3 ごみ収集車の停止場所(health)

問い: ごみ収集車は、x=-1820 の道(z=-1224 から -1800)で Congestion に止まっているか。見立ては書かない。

## 2050-08-30(月例の実行直後、m09-3 の差し替え前。基準)

- `vehicles_stuck`(garbage, limit=10): 328台。Congestion を含む 295(Blocked つき 155)、Blocked のみ 31、WaitingSpace 2。7日以上止まっている 110。x=-1820 付近の sample は 3台(vehicle 222 は 6816 発で (-1818,-1825) Blocked、vehicle 444 は 6816 発で (-1822,-1546) Congestion+GoingBack、amount 20000)。ほかの sample は Combustion Plant 31232 や Landfill 29266・29981・25590 発で、位置は x=-1820 の外
- `traffic`(-1820,-1500 r300): blocked 17、congestion 94、cars 172、density 平均 51。blockedSpots (-1825,-1255) 17。density 100 は x=-1820 の Basic Road(z=-1419〜-1725)ほか

## 2050-09-09(見回り1。m09-3 の差し替え後10日)

- `vehicles_stuck`(garbage, limit=3): 318台。Congestion を含む 280(Blocked つき 161)、Blocked のみ 35、WaitingSpace 2。7日以上止まっている 240
- `traffic`(-1820,-1500 r300): blocked 60、congestion 70、cars 148、density 平均 45。blockedSpots (-1818,-1505) 27、(-1818,-1701) 26、(-1830,-1337) 4。density 100 は 23103(Small 4 Lane Road、z=-1291)、26868・22822(Basic Road)

## 2050-09-29(月末。差し替え後30日)

- `vehicles_stuck`(garbage, limit=10): 297台。Congestion を含む 255(Blocked つき 120)、Blocked のみ 40、WaitingSpace 2。7日以上止まっている 154。x=-1820 付近の sample は vehicle 350(6816 発、(-1819,-1498)、Congestion+Blocked、blockCounter 27)の1台。ほかの sample は Combustion Plant 31232・10351 や Landfill 29981・45436・12880・28130 発で、位置は x=-1820 の外
- `traffic`(-1820,-1500 r300): blocked 12、congestion 88、cars 167、density 平均 44。blockedSpots (-1818,-1363) 6、(-1703,-1281) 4、(-1818,-1406) 2。density 100 は 20310(Small 4 Lane Road、z=-1502)、21083(Small 4 Lane Road、z=-1248)、9059(Basic Road、x=-1640)
- `complaints`: Garbage 377棟(hotspot (-2203,-1726) 68棟)
