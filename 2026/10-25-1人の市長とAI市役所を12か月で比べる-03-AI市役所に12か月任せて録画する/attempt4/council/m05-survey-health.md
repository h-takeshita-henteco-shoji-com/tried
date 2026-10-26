# m05 調査 health(s05-2)

問い: 埋立地26899 の収集車19台は、なぜ出ているのに0%のままか

## 見回り1(2050-05-11)

- `vehicles_stuck(kind="garbage", building=26899, limit=20)`
  - vehicles 10(止まっているか敷地の中の車だけ)
  - byState: Congestion+GoingBack+Spawned+OnRoad 3、Congestion+GoingBack+Spawned+OnRoad+Blocked 1、Congestion+Spawned+OnRoad 1、Congestion+Spawned+OnRoad+Blocked 2、GoingBack+Spawned+OnRoad+Blocked 2、Spawned+OnRoad+Blocked 1
  - byPath: ready 10。bySeenStopped: <1day 10
  - GoingBack の6台は積み荷 20,000(満載)で戻る途中。位置は (560,-709)、(57,-723)、(1528,93)、(1881,13)、(1686,-363)、(396,-1662)
  - 集めている4台の行き先と距離: 46244 (394,-1036) 788m、3844 Medical Clinic (-180,-1980) 1,686m、17745 (984,-398) 743m、13449 (1905,-316) 1,105m
- `buildings_near(x=1655, z=-600, radius=100, service="Garbage")`
  - 26899: 1% full(40,000 / 8,000,000)、収集車 18 / 19、働き手20、困りごとなし
- `traffic(x=1655, z=-600, radius=300, limit=5)`
  - flow 56、cars 212、blocked 54、congestion 70、averageDensity 33
  - busiest: 29888 Medium Road (1718,-815) 100、26250 Medium Road (1741,-873) 100、36747 Large Road (1673,-768) 100、2690 Large Road (1458,-750) 91、10331 Large Road (1605,-762) 84
  - blockedSpots: (1476,-757) 42、(1726,-827) 6、(1639,-774) 4

## 見回り2(2050-05-21)

- `vehicles_stuck(kind="garbage", building=26899, limit=20)`
  - vehicles 12
  - byState: GoingBack+Spawned+OnRoad+Blocked 4、Congestion+GoingBack+Spawned+OnRoad+Blocked 3、Congestion+GoingBack+Spawned+OnRoad 2、Congestion+Spawned+OnRoad 1、Congestion+Spawned+OnRoad+Blocked 1、Spawned+OnRoad+Blocked 1
  - byPath: ready 12。bySeenStopped: <1day 7、7days+ 5
  - GoingBack の9台は積み荷 20,000(満載)。位置は (1671,-377)、(677,-702)、(1450,8)、(1529,8)、(452,-891)、(-1673,-1282)、(451,-846)、(692,-78)、(1690,-771)
  - 見回り1と同じ車で seenStoppedDays 10: 3014、3357、14015、14169、14676
  - 集めている3台の行き先と距離: 45339 Crematory (-2625,-56) 2,745m、3844 Medical Clinic (-180,-1980) 1,443m、13449 (1905,-316) 868m
- `buildings_near(x=1655, z=-600, radius=100, service="Garbage")`
  - 26899: 1% full(60,000 / 8,000,000)、収集車 19 / 19、働き手20、困りごとなし
- `traffic(x=1655, z=-600, radius=300, limit=5)`
  - flow 56、cars 208、blocked 50、congestion 87、averageDensity 38
  - busiest: 17128 Medium Road (1696,-419) 100、36747 Large Road (1673,-768) 99、34666 Medium Road (1692,-336) 97、11011 Medium Road (1705,-575) 95、29888 Medium Road (1718,-815) 95
  - blockedSpots: (1485,-756) 25、(1650,-771) 23、(1672,-380) 1、(1395,-750) 1

## 月末(2050-05-31)

- `vehicles_stuck(kind="garbage", building=26899, limit=20)`
  - vehicles 15
  - byState: Congestion+GoingBack+Spawned+OnRoad+Blocked 5、Spawned+OnRoad+Blocked 4、Congestion+Spawned+OnRoad+Blocked 2、Congestion+GoingBack+Spawned+InGrounds 1、Congestion+GoingBack+Spawned+OnRoad 1、Congestion+Spawned+OnRoad 1、GoingBack+Spawned+OnRoad+Blocked 1
  - byPath: ready 14、none 1。bySeenStopped: <1day 7、7days+ 8
  - GoingBack の8台は積み荷 20,000。位置は (1698,-597)(敷地の中、path none、seenStoppedDays 19.9)、(1513,8)、(452,-734)、(1276,-741)、(-916,-951)、(412,-711)、(1312,-743)、(1362,8)。blockCounter 最大 91
  - seenStoppedDays 19.9 の車: 3357、14015、14169、14676
  - 集めている7台の行き先と距離: 31029 (-1143,-674) 394m、34101 (-1868,-1124) 3,009m、44909 (284,-936) 844m、35063 (1975,764) 1,712m、3844 (-180,-1980) 87m、13449 (1905,-316) 822m、3236 (2286,1484) 2,471m
- `buildings_near(x=1655, z=-600, radius=100, service="Garbage")`
  - 26899: 2% full(200,000 / 8,000,000)、収集車 19 / 19、働き手20、困りごとなし
- `traffic(x=1655, z=-600, radius=300, limit=5)`
  - flow 56、cars 200、blocked 59、congestion 71、averageDensity 33
  - busiest: 17128 Medium Road (1696,-419) 100、10331 Large Road (1605,-762) 100、2690 Large Road (1458,-750) 100、29888 Medium Road (1718,-815) 100、34666 Medium Road (1692,-336) 93
  - blockedSpots: (1491,-759) 45、(1647,-772) 12、(1398,-751) 2
