# m24 調査 s24-1 (1882,-903) の止まり

## 2051-12-12 見回り1(戻しの10日後)

- `traffic`(x=1882, z=-903, radius=120): blocked 2、blockedSpots は (1848,-949) 2 のみ、flow 54、cars 79、congestion 11
- `traffic`(x=2110, z=-840, radius=80): blocked 2、blockedSpots は (2080,-841) 2、flow 54、cars 49、busiest は 26558 Small 4 Lane (2110,-813) density 100
## 2051-12-22 見回り2

- `traffic`(x=1882, z=-903, radius=120): blocked 17、blockedSpots は (1778,-905) 9、(1848,-936) 8、flow 54、cars 80、congestion 15
- `traffic`(x=2110, z=-840, radius=80): blocked 13、blockedSpots は (2116,-837) 10、(2105,-788) 3、flow 54、cars 35、busiest は 7043 Medium (2181,-848) density 100

## 2052-01-01 月末

- `traffic`(x=1882, z=-903, radius=120): blocked 6、blockedSpots は (1967,-954) 5、(1765,-889) 1、flow 52、cars 69、congestion 29、busiest は 26706 Basic (1844,-903) density 100
- `traffic`(x=2110, z=-840, radius=80): blocked 14、blockedSpots は (2170,-859) 14、flow 52、cars 37、busiest は 7043 Medium (2181,-848) density 96
- 参考 `traffic`(x=2082, z=-840, radius=200): blocked 85、blockedSpots は (2134,-908) 53、(2195,-736) 18、(2225,-948) 8、flow 52

## 参考

- 参考(m24-2 の基準 `traffic` x=2082, z=-840, r=200、戻す直前): blocked 81、blockedSpots (2058,-871) 30、(1955,-874) 17
