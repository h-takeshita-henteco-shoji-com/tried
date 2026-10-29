# m17 調査 s17-3(health) 汚染の印 21 の発生源

引数: `buildings_near`(x=3804、z=-170、radius=200、problem="Pollution"、brief=true、limit=20)、`map_layer`(pollution、x=3804、z=-170、radius=300、n=9)、`complaints`。基準は焼却場 10351 を動かした直後(2051-05-06 の操作後)。

## 2051-05-16(見回り1)

- `buildings_near`: total 1。47039 L2 4x4 Detached08 (3709,-86)、問題 Garbage, Pollution
- `map_layer`: 平均 70、最大 255(3579,-20)。255 に近い格子は x=3504〜3729 の z=-20〜-170 付近と、最南の行 z=130 の x=3579〜3804。x=3804 より東は 0 が多い
- `complaints`: Pollution 26(hotspot (3818,-169)、16棟)、Garbage 18

## 2051-05-26(見回り2)

- `buildings_near`: total 1。47039 (3709,-86)、問題 Pollution, Death
- `map_layer`: 平均 70、最大 255(3579,55)。分布は見回り1と同じ形
- `complaints`: Pollution 22(hotspot (3798,-159)、20棟)、Garbage 12

## 2051-06-05(月末)

- `buildings_near`: total 1。47039 (3709,-86)、問題 Pollution, MajorProblem
- `map_layer`: 平均 69、最大 255(3579,-20)。分布は同じ形
- `complaints`: Pollution 23(hotspot (3721,-96)、18棟)、Garbage 12
- 参考: 10351 は動いている(Processing 60,000/週、貯め 286,354/400,000=71%、Power Output 15 MW、ごみ収集車 11/34)。`services` の満杯の埋立地は 4(24569、29266、29981、48698)

(見立ては書かない。局が翌月に読む)
