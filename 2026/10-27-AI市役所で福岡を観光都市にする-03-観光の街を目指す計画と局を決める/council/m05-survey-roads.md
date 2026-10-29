# m05 調査 s05-2(roads): (1694,93) 付近の止まり

問い: (1694,93) 付近の止まり(blocked 86)は、両端の信号の待ちが伸びた列か、道幅の詰まりか。

## 2050-05-11(見回り1)

- `traffic`(x 1694, z 93, r200, limit 5): flow 56、cars 207、blocked 104、congestion 92、roadSegments 17、averageDensity 85。blockedSpots は (1692,91) 66、(1841,100) 18、(1555,30) 9。busiest は density 100 の Basic/Medium Road 5区間(x 1523〜1572、z -20〜100)
- `traffic`(x 1560, z 100, r150, limit 5): flow 56、cars 140、blocked 61、congestion 65、averageDensity 85。blockedSpots は (1669,90) 41、(1532,22) 14

## 2050-05-21(見回り2)

- `traffic`(x 1694, z 93, r200): flow 53、cars 186、blocked 38、congestion 72、averageDensity 81。blockedSpots は (1826,98) 20、(1539,35) 8。busiest に Large Road (1850,107) density 100
- `traffic`(x 1560, z 100, r150): flow 53、cars 115、blocked 19、congestion 52。blockedSpots は (1514,24) 13

## 2050-05-31(月末)

- `traffic`(x 1694, z 93, r200): flow 51、cars 190、blocked 76、congestion 76、averageDensity 84。blockedSpots は (1681,91) 59、(1539,91) 8、(1881,57) 7。busiest は Large Road (1850,107)、Basic Road (1560,70) など density 100
- `traffic`(x 1560, z 100, r150): flow 51、cars 130、blocked 64、congestion 47、averageDensity 86。blockedSpots は (1660,90) 44、(1496,66) 19
