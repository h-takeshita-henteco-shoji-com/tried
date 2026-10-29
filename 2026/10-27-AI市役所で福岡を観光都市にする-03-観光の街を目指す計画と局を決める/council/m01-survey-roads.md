# m01 調査 s01-2(roads): 幹線(-726,-736)で止まる車の原因

見立ては書かない。局が翌月に読んで決める。

## 2050-01-31(月末)

- `traffic`(x=-726, z=-736, radius=150): flow 50、cars 101、blocked 7、congestion 37、averageDensity 79、roadSegments 4。density は 36115 が100、10922 が93、30435 が67、6545 が59。blockedSpots は (-704,-738) 7台
- `traffic`(x=-920, z=-740, radius=200): flow 50、cars 197、blocked 28、congestion 72、averageDensity 75、roadSegments 21。density 100 は 36115、16866、10176、3276、7655。blockedSpots は (-927,-897) 15台、(-1034,-656) 7台、(-980,-654) 5台、(-724,-738) 1台
- `net_reach`(x=-726, z=-736, radius=300): roads 26区間、notEnterable 0、notLeavable 0。buildings 126、noRoad 0、notReachable 0、cannotLeave 0。bad 系は空

## 2050-01-21(見回り2)

- `traffic`(x=-726, z=-736, radius=150): flow 50、cars 107、blocked 63、congestion 22、averageDensity 92、roadSegments 4。density 100 は 36115、10922。blockedSpots は (-713,-737) 42台、(-841,-735) 18台、(-593,-738) 3台
- `traffic`(x=-920, z=-740, radius=200): flow 50、cars 224、blocked 62、congestion 51、averageDensity 78、roadSegments 21。density 100 は 10922、9066、12614、36115、16866、8020、7655、3276。blockedSpots は (-853,-734) 24台、(-764,-736) 21台、(-926,-878) 17台
- `net_reach`(x=-726, z=-736, radius=300): roads 26区間、notEnterable 0、notLeavable 0。buildings 125(建設中1)、noRoad 0、notReachable 0、cannotLeave 0。bad 系は空

## 2050-01-11(見回り1)

- `traffic`(x=-726, z=-736, radius=150): flow 51、cars 147、blocked 2、congestion 28、averageDensity 100、roadSegments 4(すべて Large Road、density 100: 30435、36115、6545、10922)。blockedSpots は (-872,-734) に2台
- `traffic`(x=-920, z=-740, radius=200): flow 51、cars 185、blocked 29、congestion 51、averageDensity 64、roadSegments 21。density 100 は 36115、10922、16866(-920,-712)、3276(-895,-740 Large Road with Median)。blockedSpots は (-929,-714) に20台、(-1049,-664) に8台、(-932,-914) に1台
- `net_reach`(x=-726, z=-736, radius=300): roads 26区間、notEnterable 0、notLeavable 0。buildings 126、noRoad 0、notReachable 0、cannotLeave 0。badBuildings、badSegments は空
