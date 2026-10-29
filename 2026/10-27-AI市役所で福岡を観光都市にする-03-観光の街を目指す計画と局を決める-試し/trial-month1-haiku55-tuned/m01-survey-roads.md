# m01 調査 s01-1(roads)幹線 (-726,-740) の止まった車の並び方

## 2050-01-31(月末)

- `traffic`(x=-800, z=-740, radius=120): flow 52、cars 101、blocked 1、congestion 33、averageDensity 96。blockedSpot (-915,-764) に 1 台。busiest は segment 10922、36115、3276 が density 100、6545 が 84
- `traffic`(x=-920, z=-740, radius=60): flow 52、cars 59、blocked 4、congestion 20、averageDensity 93。blockedSpot (-921,-718) に 4 台。busiest は segment 16866(-920,-712)100、9066(-920,-768)100、3276(-895,-740)100、10370 73

## 2050-01-21(見回り2)

- `traffic`(x=-800, z=-740, radius=120): flow 51、cars 98、blocked 0、congestion 25、averageDensity 100。blockedSpots なし。busiest は segment 10922、36115、3276、6545 で density 100(見回り1と同じ)
- `traffic`(x=-920, z=-740, radius=60): flow 51、cars 60、blocked 13、congestion 9、averageDensity 92。blockedSpot (-919,-754) に 13 台。busiest は segment 9066(-920,-768)100、3276(-895,-740)100、16866(-920,-712)95、10370(-960,-740)73

## 2050-01-11(見回り1)

- `traffic`(x=-800, z=-740, radius=120): flow 49、cars 102、blocked 10、congestion 13、averageDensity 100。blockedSpot (-888,-740) に 10 台。busiest は segment 10922(-759,-740)、36115(-832,-740)、3276(-895,-740)、6545(-685,-740)で、すべて density 100
- `traffic`(x=-920, z=-740, radius=60): flow 49、cars 53、blocked 20、congestion 13、averageDensity 96。blockedSpot (-907,-736) に 20 台。busiest は segment 3276(-895,-740)density 100、16866(-920,-712)99、9066(-920,-768)99、10370(-960,-740)89
