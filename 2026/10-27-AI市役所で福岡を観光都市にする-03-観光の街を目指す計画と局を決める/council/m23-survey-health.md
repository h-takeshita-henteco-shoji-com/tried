# m23 調査 s23-2(health): 汚染の強い一帯と混んだ幹線 z=-250 の関係

問い: 汚染の強い一帯(x 3500〜3650、z -50〜-550)の値は、混んだ幹線 z=-250 の車の混みと一緒に動くか。

## 2051-11-12(見回り1)

- `map_layer`(pollution, x=3500, z=-250, r=200, n=5): average 67、min 0、max 255(maxAt (3500,-50))。北の行 [0,0,255,255,255]、2行目 [0,0,0,145,4]、3行目 [3,0,0,0,255]、4行目 [86,0,0,0,0]、5行目 [0,0,0,249,183]
- `traffic`(x=3500, z=-250, r=200): flow 53、cars 59、blocked 2、congestion 29、averageDensity 30。busiest は z=-252 の Small 4 Lane Road (3361)100、(3441)100、(3520)88、(3595)68、(3666)65
- `complaints`: Pollution 28棟、hotspot (3724,-165.3) 17棟

## 2051-11-22(見回り2)

- `map_layer`(pollution, 同じ引数): average 68、min 0、max 255(maxAt (3500,-50))。北の行 [0,0,255,255,255]、2行目 [0,0,0,159,5]、3行目 [0,0,0,0,255]、4行目 [91,0,0,0,0]、5行目 [1,0,0,247,183]
- `traffic`(同じ引数): flow 53、cars 103、blocked 12、congestion 32、averageDensity 37。busiest は z=-250 の Small 4 Lane Road (3595)100、(3666)100、(3361)100、(3441)100、(3520)81
- `complaints`: Pollution 37棟、hotspot (3747.8,-187.1) 19棟

## 2051-12-02(月末)

- `map_layer`(pollution, 同じ引数): average 67、min 0、max 255(maxAt (3600,-50))。北の行 [0,0,252,255,254]、2行目 [0,0,0,157,7]、3行目 [0,0,0,0,251]、4行目 [105,0,0,0,0]、5行目 [2,0,0,235,165]
- `traffic`(同じ引数): flow 52、cars 110、blocked 22、congestion 34、averageDensity 40。busiest は z=-250 の (3520)100、(3361)100、(3441)100、(3595)98、(3666)79
- `complaints`: Pollution 43棟、hotspot (2080.7,505.4) 16棟(hotspot が東の一帯から移った)
