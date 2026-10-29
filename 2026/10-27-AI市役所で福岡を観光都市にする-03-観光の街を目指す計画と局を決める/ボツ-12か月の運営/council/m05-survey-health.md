# m05 調査 s05-2(health)焼却場33797の周りで収集車が止まる場所

## 2050-05-12(見回り1)

- `vehicles_stuck` kind=garbage、building=33797、limit=10: 20台。Congestion 系+OnRoad のみ(InGrounds 0)。Blocked 12、7日以上止まり 12。GoingBack 15台は荷20000のまま target なし。止まっている位置の例: (-476,-738)、(-588,-748)、(-519,-748)、(-304,-741)、(-2195,-1841)、(-426,-1694)、(-916,-895)。ほかに行き先が住宅や警察署の車が5台(distance 53〜2228)
- `traffic` x -425、z -1300、radius 200: flow 53、cars 28、blocked 0、congestion 6、averageDensity 15。busiest は (-425,-1372) density 72、(-425,-1448) 64。blockedSpots なし
- `complaints`: Garbage 81 棟(hotspot (-511,-1347) 27棟)、Pollution 37(hotspot (3728,-215))、Death 51、NoGoods 258、Fire 7、Noise 1、Flood 1、Water 1(19148 Shop04 (2658,925))、RoadNotConnected 1(Regular Park 44507)

## 2050-06-01(月末)

- `vehicles_stuck` kind=garbage、building=33797、limit=10: 13台。Congestion 系+OnRoad のみ。Blocked 3、7日以上止まり 7。GoingBack 10台は荷20000のまま target なし。位置の例: (-566,-748)、(-359,-743)、(-740,-748)、(-276,-953)、(-916,-798)、(-1353,-1098)、(-919,-1237)。行き先のある3台は住宅(distance 2022〜2102)
- `traffic` x -425、z -1300、radius 200: flow 54、cars 27、blocked 0、congestion 7、averageDensity 14。busiest は (-425,-1372) 73、(-425,-1242) 62、(-425,-1197) 50。blockedSpots なし
- `complaints`: Garbage 134 棟(hotspot (-178,-1586) 45棟。基準の見回り1は81棟、hotspot (-511,-1347))、Pollution 33(hotspot (3800,-203))、Death 37、NoGoods 258、Fire 4、Noise 2、Water 1、NoEducatedWorkers 1、RoadNotConnected 1
