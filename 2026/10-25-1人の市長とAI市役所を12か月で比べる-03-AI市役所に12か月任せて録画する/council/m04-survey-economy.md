# m04 調査の結果(economy)

## s04-2 事務所が建たないのは、道に面した空きがないためか

問い: 働き口の需要が58でも事務所が建たないのは、空きマス1,642がすべて道の奥(emptyBehind)にあり、道に面した空きがないためか。
見立ては書かない。局が翌月に読んで決める。

### 見回り1(2050-04-11)

- `zone_summary(grid=1000)`
  - Office: total 36,805、empty 1,642、emptyShallow 0、emptyNarrow 0、emptyBehind 1,642、emptyFacingRoad 0
  - ResidentialHigh: total 37,645、empty 705、emptyBehind 705、emptyFacingRoad 0
  - CommercialHigh: total 8,973、empty 573、emptyShallow 8、emptyNarrow 9、emptyBehind 441、emptyFacingRoad 132
  - Industrial: empty 66(emptyBehind 66)。CommercialLow: empty 90(emptyBehind 90)。ResidentialLow: empty 381(emptyBehind 381)
  - 事務所の空きの多い区切り: (-500,-500) 197、(-1500,-500) 187、(3500,-500) 123、(-2500,-500) 106、(500,-500) 88、(2500,-500) 86、(500,-1500) 83、(1500,1500) 82
- `demand_breakdown()`
  - jobs 86,907、emptyJobs 3,272、homes 55,558、emptyHomes 5,132、unemployed 6,932、homeless 0
  - byEducation の unemployed: uneducated 111、elementary 41、highSchool 25、university 6,755
- `vehicles_stuck(kind="truck", building=28755, limit=5)`
  - vehicles 597。WaitingSpace+Importing+InGrounds 502、WaitingSpace+Importing+OnRoad 59、Importing+Spawned+OnRoad+Blocked 24
  - byPath ready 593、none 4。bySeenStopped <1day 143、7days+ 454
  - samples 5台はすべて (3441,-1555)、荷物は Goods

### 見回り2(2050-04-21)

- `zone_summary(grid=1000)`
  - Office: total 36,805、empty 1,642、emptyShallow 0、emptyNarrow 0、emptyBehind 1,642、emptyFacingRoad 0(見回り1と同じ)
  - ResidentialHigh: empty 705、emptyBehind 705、emptyFacingRoad 0
  - CommercialHigh: empty 552、emptyBehind 443、emptyFacingRoad 109(見回り1は 573 / 441 / 132)
  - 事務所の区切りごとの空きは見回り1と同じ
- `demand_breakdown()`
  - jobs 86,991、emptyJobs 3,290、homes 55,607、emptyHomes 5,163、unemployed 6,927、homeless 0
  - byEducation の unemployed: uneducated 128、elementary 34、highSchool 37、university 6,728
- `vehicles_stuck(kind="truck", building=28755, limit=5)`
  - vehicles 572。WaitingSpace+Importing+InGrounds 484、WaitingSpace+Importing+OnRoad 63、Importing+Spawned+OnRoad+Blocked 15
  - byPath ready 569、none 3。bySeenStopped <1day 113、7days+ 459
  - samples 5台はすべて (3441,-1555)、荷物は Goods

### 月末(2050-05-01)

- `zone_summary(grid=1000)`
  - Office: total 36,805、empty 1,642、emptyShallow 0、emptyNarrow 0、emptyBehind 1,642、emptyFacingRoad 0(見回り1・2と同じ)
  - ResidentialHigh: empty 705、emptyBehind 705、emptyFacingRoad 0
  - CommercialHigh: empty 520、emptyBehind 443、emptyFacingRoad 77
  - Industrial 66、CommercialLow 90、ResidentialLow 381 の空きは、どれも emptyBehind で emptyFacingRoad 0
  - 事務所の区切りごとの空きは見回り1・2と同じ
- `demand_breakdown()`
  - jobs 87,025、emptyJobs 3,259、homes 55,618、emptyHomes 5,179、unemployed 6,771、homeless 0
  - byEducation の unemployed: uneducated 115、elementary 30、highSchool 28、university 6,598
- `vehicles_stuck(kind="truck", building=28755, limit=5)`
  - vehicles 588。WaitingSpace+Importing+InGrounds 485、WaitingSpace+Importing+OnRoad 64、Importing+Spawned+OnRoad+Blocked 32
  - byPath ready 586、none 2。bySeenStopped <1day 136、7days+ 452
  - samples 5台はすべて (3441,-1555)。荷物は Food、Goods、Lumber、Petrol、Goods
