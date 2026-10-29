# m12 調査 economy(s12-2)

## 2050-11-28(実行直後、見回り1の前の基準)

- `vehicles_stuck` kind=truck building=13893 limit=3: vehicles 0(byState 空)
- `net_near` x=3529 z=-1555 radius=40 service=Road: 2区間のみ。15733 Small 4 Lane Road (3495,-1490)-(3495,-1565) と 22686 (3495,-1565)-(3496,-1610)。どちらも carLanes 2/2。13893 の位置 (3529,-1555) から約 34m 西
- `cargo`: stations の 13893 は vehiclesLeaving 0、vehiclesArriving 0

## 2050-12-28(月末)

- `vehicles_stuck` kind=truck building=13893 limit=3: vehicles 0(byState 空)
- `net_near` x=3529 z=-1555 radius=40 service=Road: 基準と同じ2区間(15733、22686)。carLanes 2/2。13893 に面する道路は radius 40 に増えていない
- `cargo`(月末は調査の予定外だが、port の呼びで取れた): stations の 13893 は vehiclesLeaving 0、vehiclesArriving 0

## 2050-12-08(見回り1)

- `vehicles_stuck` kind=truck building=13893 limit=3: vehicles 0(byState 空)
- `net_near` x=3529 z=-1555 radius=40 service=Road: 基準と同じ2区間(15733、22686)。carLanes 2/2
- `cargo`: stations の 13893 は vehiclesLeaving 0、vehiclesArriving 0
