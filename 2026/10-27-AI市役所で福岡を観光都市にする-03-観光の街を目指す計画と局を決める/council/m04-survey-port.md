# m04 調査 s04-1 貨物センター28755の待ちの行き先(port)

見立ては書かない。局が翌月に読んで決める。

## 2050-04-11(見回り1)

- `vehicles_stuck`(kind="truck", building=28755, limit=10): vehicles 620。byState は WaitingSpace+Importing+InGrounds 522、WaitingSpace+Importing+OnRoad 55、Importing+Spawned+OnRoad+Blocked 22、GoingBack+Importing+Spawned+OnRoad+Blocked 15 ほか。byPath は ready 616、none 4。bySeenStopped は 7days+ が 484、<1day が 136。サンプル10台のうち9台は x3441 z-1555 の敷地内で WaitingSpace、seenStoppedDays 20〜100、path ready、行き先は店・工場(distance 2,559〜6,296)。1台は x252 z-259 で OnRoad+Blocked(blockCounter 54)
- `net_near`(x=3529, z=-1555, radius=80, service="Road"): 4区間。segment 15733(Small 4 Lane Road、(3495,-1490)〜(3495,-1565)、長さ65)、19541(Basic Road、(3495,-1415)〜(3495,-1490)、長さ59)、22686(Small 4 Lane Road、(3495,-1565)〜(3496,-1610)、長さ47)、25261(Small 4 Lane Road、(3496,-1610)〜(3496,-1626)、長さ16)。13893(x3529 z-1555)の入口の道は、この x=3495 の南北の道に通じている
- 参考 `cargo`: stations の 28755 は vehiclesLeaving 807、vehiclesArriving 12。13893 は 0 / 0。stoppedInBuildings 522(すべて 28755)

## 2050-05-01(月末)

- `vehicles_stuck`(kind="truck", building=28755, limit=10): vehicles 627。byState は WaitingSpace+Importing+InGrounds 539、WaitingSpace+Importing+OnRoad 44、Importing+Spawned+OnRoad+Blocked 34、GoingBack+Importing+Spawned+OnRoad+Blocked 9 ほか。byPath は ready 626、none 1。bySeenStopped は 7days+ が 485、<1day が 142。サンプル10台のうち9台は x3441 z-1555 の敷地内で WaitingSpace(seenStoppedDays 0〜120)、path ready。Goods の車(vehicle 8、36、156、183、229)は 100〜120日止まったまま。新しく見えた車: vehicle 152(行き先 distance 555)、143(distance 925)
- `net_near`(x=3529, z=-1555, radius=80, service="Road"): 4/11 と同じ4区間(15733、19541、22686、25261)。変化なし
- 参考 `cargo`: stoppedInBuildings 563(28755 が 539、貨物港1366 が 24)。28755 の vehiclesLeaving 784、vehiclesArriving 11。13893 は 0 / 0
