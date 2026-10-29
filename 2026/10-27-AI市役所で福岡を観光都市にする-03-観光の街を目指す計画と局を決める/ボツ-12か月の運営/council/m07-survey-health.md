# m07 調査 s07-2(health)ごみの印の hotspot と満杯の埋立地

## 2050-07-11(見回り1)

- `complaints` Garbage: 248棟、hotspot (-2289.7,-1617.6) 85棟(月例時は 231、(-2293,-1584) 72棟)
- `buildings_near` x -2293, z -1584, radius 300, problem Garbage, brief true, limit 30: total 0(この円の中に印のある建物なし)
- `services` garbage: 満杯9(157、16914、19182、23032、25692、25826、29270、45892、48698)、capacity 168,000,000、used 135,157,609(置く前は 160,000,000 / 134,837,609)
- 新しい埋立地 6816: 0% full、収集車 0/19(置いた直後)

## 2050-07-31(月末)

- `complaints` Garbage: 262棟、hotspot (-2119.4,-1581.1) 73棟(見回り1は 248棟、(-2289.7,-1617.6) 85棟。見回り2は 257棟、(-2273.2,-1560.5) 85棟)
- `buildings_near` x -2293, z -1584, radius 300, problem Garbage, brief true, limit 30: total 1(H3 3x4 Office14 id 27938)
- `services` garbage: 満杯10(157、16914、19182、23032、24569、25692、25826、29270、45892、48698。24569 が加わった)、capacity 168,000,000、used 136,025,884
- 新しい埋立地 6816: 2% full(222,767 / 8,000,000)、収集車 18/19、electricity true
