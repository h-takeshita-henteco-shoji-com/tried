# m01 調査 s01-3(roads): 2か所の詰まりの原因が道の幅か交差点か

問い: 止まった車が多い (-726, -736) と (2100, 309) の詰まりの原因は、道の幅の絞りか、交差点か

## 見回り1(2050-01-11)

### `traffic(x=-726, z=-736, radius=200, limit=6)`

- cars 207、blocked 89、congestion 31、roadSegments 8、averageDensity 93
- busiest: 10922 Large Road (-759,-740) 100、16866 Small 4 Lane Road (-920,-712) 100、36115 Large Road (-832,-740) 100、6545 Large Road (-685,-740) 100、3276 Large Road with Median (-895,-740) 100、30435 Large Road (-611,-740) 91
- blockedSpots: (-681,-735) 71、(-556,-740) 17、(-924,-721) 1

### `traffic(x=2100, z=309, radius=200, limit=6)`

- cars 157、blocked 90、congestion 109、roadSegments 24、averageDensity 69
- busiest: 22887 Small 4 Lane Road (2110,303) 100、3990 (2132,330) 100、6523 (2152,443) 100、18 (2153,371) 100、4374 (2110,213) 99、5864 (2110,267) 90。どれも Small 4 Lane Road
- blockedSpots: (2110,292) 41、(2154,445) 26、(2078,154) 14、(2253,321) 7、(1987,148) 2

## 見回り2(2050-01-21)

### `traffic(x=-726, z=-736, radius=200, limit=6)`

- cars 190、blocked 65、congestion 43、roadSegments 8、averageDensity 89
- busiest: 16866 Small 4 Lane Road (-920,-712) 100、36115 Large Road (-832,-740) 100、3276 Large Road with Median (-895,-740) 100、10922 Large Road (-759,-740) 95、6545 Large Road (-685,-740) 89、9066 Small 4 Lane Road (-920,-768) 85
- blockedSpots: (-843,-734) 41、(-777,-735) 24

### `traffic(x=2100, z=309, radius=200, limit=6)`

- cars 169、blocked 14、congestion 99、roadSegments 24、averageDensity 73
- busiest: 22887 Small 4 Lane (2110,303) 100、18 (2153,371) 100、6523 (2152,443) 100、3990 (2132,330) 98、1374 (2175,330) 95、13553 Medium Road (2200,221) 93
- blockedSpots: (2218,227) 10、(2204,188) 4

## 月末(2050-01-31)

### `traffic(x=-726, z=-736, radius=200, limit=6)`

- cars 138、blocked 9、congestion 47、roadSegments 8、averageDensity 88
- busiest: 9066 Small 4 Lane Road (-920,-768) 100、16866 Small 4 Lane Road (-920,-712) 100、3276 Large Road with Median (-895,-740) 100、36115 Large Road (-832,-740) 100、32158 Large Road (-537,-740) 81、10922 Large Road (-759,-740) 79
- blockedSpots: (-909,-741) 9

### `traffic(x=2100, z=309, radius=200, limit=6)`

- cars 164、blocked 127、congestion 109、roadSegments 24、averageDensity 68
- busiest: 6523 Small 4 Lane (2152,443) 100、9308 (2069,240) 100、22887 (2110,303) 100、18 (2153,371) 100、5 (1995,330) 100、26735 (2069,330) 86
- blockedSpots: (2101,302) 55、(2154,446) 28、(1958,305) 16、(2070,160) 14、(2207,286) 11、(1991,148) 3
