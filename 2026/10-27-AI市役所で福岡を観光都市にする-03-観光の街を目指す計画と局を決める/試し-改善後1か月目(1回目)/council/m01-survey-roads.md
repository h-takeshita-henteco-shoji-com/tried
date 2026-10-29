# m01 調査 s01-3(roads) 2280付近の狭まりの止まりを見る

問い: 2280付近(4車線が1車線に狭まる区間)の止まった車は、時間がたつと減るか、増えるか

## 見回り1 (2050-01-12)

- `traffic`(x=2300, z=-930, radius=120, limit=5): flow 50、cars 89、blocked 64(すべて道の上)、congestion 37、averageDensity 91。blockedSpots は (2297,-923) 60台、(2409,-946) 4台。busiest は density 100 の区間5本(segment 20293 (2236,-886)、19196 (2194,-950)、29545 (2220,-978)、36011 (2228,-950)、30068 (2313,-950))

## 月末 (2050-02-01)

- `traffic`(x=2300, z=-930, radius=120, limit=5): flow 52、cars 71、blocked 0、congestion 24、averageDensity 81。blockedSpots は空。busiest は density 100 の5区間(30068、19196、29545、13096 (2370,-950)、3334 (2258,-950))

## 見回り2 (2050-01-22)

- `traffic`(x=2300, z=-930, radius=120, limit=5): flow 51、cars 84、blocked 0、congestion 32、averageDensity 90。blockedSpots は空。busiest は見回り1と同じ5区間で、density はすべて 100
