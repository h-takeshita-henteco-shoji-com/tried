# m06 道路下水道局の案

## 案1: 渋滞する Basic Road を Small 4 Lane Road に差し替える(3群、取り壊しなし)

### 施策

- 案の id: roads-1
- 施策: density 100 で混んでいる Basic Road(1車線ずつ)の3群を、同じ幅の Small 4 Lane Road(2車線ずつ)に差し替える。(1) z=-860 の東西の幹線(x 2304〜2640)、(2) z=-1240 の東西の道(x 2306〜2520)、(3) z=-490 の東西の道(x 2800〜3100)。(1) は、blocked が集まる z=-950 の4車線の並行路。道具は `upgrade_road`。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順(`upgrade_road`、prefab "Small 4 Lane Road"、demolish は false のまま。順番は自由):
  1. `upgrade_road` prefab "Small 4 Lane Road"、points [[2304, -860], [2640, -860]]、tolerance は既定の 20、pay は true。試し(`test_upgrade_road`)で matched 5、upgraded 5、skipped 0、cost 0、取り壊し 0。
  2. `upgrade_road` prefab "Small 4 Lane Road"、points [[2306, -1240], [2520, -1240]]、pay true。試しで matched 3、upgraded 3、skipped 0、cost 0、取り壊し 0。
  3. `upgrade_road` prefab "Small 4 Lane Road"、points [[2800, -490], [3100, -490]]、pay true。試しで matched 3、upgraded 3、skipped 0、cost 0、取り壊し 0。
- 設置条件の確認:
  - 1 の区間: `test_upgrade_road` で matched 5、upgraded 5。対象は segment 5784、17509、26067、36689、22905(すべて Basic Road)。ObjectCollision、取り壊し、TooShort なし。
  - 2 の区間: `test_upgrade_road` で matched 3、upgraded 3。対象は segment 9229、13690、27206(すべて Basic Road)。skipped なし。
  - 3 の区間: `test_upgrade_road` で matched 3、upgraded 3。`traffic`(x 2950、z -490、r200)で、density 100 の Basic Road 21069、9242、35451、2871、5524 が並ぶ。blocked は 0 だった。
  - 除外した区間: segment 14040(Basic、(2272,-860))は、`test_upgrade_road` で Fire House 32853 にぶつかって断られた。取り壊しは使わないので外す。
  - 除外した区間: z=-950 西の 3334、19196 は、TooShort の 36011 にぶつかる。同じく外す。
- 接続工事: 不要。差し替えは同じ幅・同じ維持費(Basic Road と Small 4 Lane Road は 5,000/km、40/km/週)で、接続は変わらない。
- 予備候補: なし。3群のどれかが実行時に断られたら、その群だけを外す(ほかの群は続ける)。
- 中止する条件: 実行直前の `test_upgrade_road` で、いずれかの群の skipped に ObjectCollision か取り壊し(demolishedBuildings が 0 でない)が出たら、その群を外す。建設費が 0 でなければ見送る。

### 期待する効果

- 改善の見込み: z=-950 の4車線(density 100、blocked 52 と 42 の場所)は、並行の Basic Road が1車線のままで、東西の交通が z=-950 に集まっている。並行の z=-860 を4車線にすると、交通の一部がそちらへ回り、z=-950 の blocked が減ると予想する。z=-1240 と z=-490 は density 100 の道で、流れの分散に効くと予想する。
- 数値と期限: 確認した今の値(2050-06-01 月末)は、`traffic` の flow 54(目標60)、x 2450 z -900 r300 の blocked 108(z=-950 の (2504,-946) が 52、(2323,-946) が 42)。予想は、z=-950 の blocked が 2 か月以内に半分程度へ減ること。街全体の flow は、数値で見積もれない。期限は 2 か月後(2050-08-01)の月末。
- 確認方法: `traffic`(x 2450、z -900、radius 300)の blocked と blockedSpots、`traffic`(街全体)の flow。見回り1、見回り2、月末の3回を、今の値と同じ範囲で比べる。
- 不確かな点: 差し替えた道の車が増えて、別の交差点(x 2236 の交差点など)が詰まるおそれがある。過去の同じ手(m01-2、m02-2、m03-1、m05-3)は、局所の blocked を大きく減らした(例: 116→18、139→46)が、街全体の flow は 51→52→54→53→54 と動かなかった。街全体の flow が 60 に届くかは見積もれない。
- 試し: なし(局所の効きは過去の同じ手で確かめている。街全体への効きは見積もれない)。

### 費用

- 建設費: 0(`test_upgrade_road` の cost 0、3群の合計 0)
- 週の維持費の増え分: 0(Basic Road と Small 4 Lane Road は 40/km/週で同じ。`list_net_types` で確認)

### 戻せるか

戻せる。Small 4 Lane Road から Basic Road へ同じ方法で差し替えられ、費用は 0 のまま。

### 前の月の答え合わせ

- m05-roads-1(西の基本道路15区間を Small 4 Lane Road に差し替え、採択・実行済み): 半分。西 r250 の blocked は 139→46(月末)に減った。街全体の flow は 54 のままで、目標 60 に届いていない。(`mayor-note.md` の施策の一覧、5か月目の記録)
- m05 の調査 s05-3(東西の幹線 z=330 の詰まりの原因): 見回り1 から月末まで、交差点 9244(2700,330)は信号なし・譲れなしの3差路。流入の3本とも車が通る。blockedSpots は (2716,334) で、見回り1 の 6 から月末 3 へ減った。交差点が詰まりの原因かは、まだ確かめられていない(次の節で扱う)。
- 判定前ではなく、今月の案 roads-1 の効果は、2 か月後の月末で判定する。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(流れ 54、目標 60%以上)
- 編成方針の重点に当たるか: 当たらない(重点は観光、4-4、8-1)。6-3 は編成方針の「案は出してよい」の枠に当たる。

## 案なし

(案がある月は書かない。)

## 調査

- 調査: あり
- 問い: 並行の z=-860 を4車線にした後、z=-950 西の blocked(x 2450 付近)は減るか。
- 見る道具と引数: `traffic` の x 2450、z -900、radius 300(blocked と blockedSpots を記録)。ほかに同じ引数で街全体の `traffic`(flow)。2 つまで。
- いつ見るか: 見回り1 / 見回り2 / 月末(3回)
- 何が分かれば次の手が決まるか: z=-950 の blocked の(2504,-946) 付近が、月末に 52 から 25 以下に減れば、同じ手(Basic → 4車線)を別の幹線に広げる案を次月に出す。減らなければ、z=-950 の詰まりは交差点(x 2236 と x 2160 の交差点など)が原因と見て、譲れの標識や信号の案を次月に検討する(費用の確認が先)。
- 担当の問題: 6-3 公共交通を主軸とした交通体系

## 見たもの

- `city_info`: 人口180,778、幸福度87、所持金2,197,627、週の収支 +8,944(収入348,533、支出339,589)、観光客1,631/155、需要 住27・商2・工56。電気・水・下水が来ない市民は 0/0/0
- `traffic`(街全体): flow 54、cars 7,261、blocked 802(道の上 801)。busiest は density 100 の Basic Road(9229 ほか)と Medium Road(3239 ほか)
- `traffic`(x 2700、z 320、r150): flow 54、blocked 18、busiest は 19421、25781、2093、4818、22938(すべて Small 4 Lane、density 100)。blockedSpots (2715,334) 13
- `traffic`(x 2450、z -946、r200): flow 54、blocked 108。blockedSpots (2504,-946) 52、(2325,-946) 42、(2620,-946) 14。Small 4 Lane の z=-950 の区間は density 100
- `traffic`(x 2300、z -900、r400): blocked 153。busiest に z=-950 の Small 4 Lane(15481、14041、17546)と、Basic Road(9229、19196)
- `traffic`(x 2950、z -490、r200): blocked 0、density 100 の Basic Road が5区間(21069、9242、35451、2871、5524)
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940/週、学校の維持費の25%増し。教育費に入る)、RecreationalUse(0)、BigBusiness(3,872/週)。無効で交通に関係するのは HeavyTrafficBan(0)、FreeTransport(0。運賃収入が 0 になる)。政策費用の合計 10,633/週。交通の流れに効く政策は、今月の案には使わない(下の捨てたもの)
- `list_net_types`(Road): Basic Road 5,000/km・40/km/週、Small 4 Lane Road 5,000/km・40/km/週、Medium Road 7,500/km・100/km/週、Large Road 10,000/km・120/km/週
- `citizens_without_service`(sewage): residents 0、homes なし
- `net_near`(2700,330、r130、Road): 交差点 9244 に入る区間は 19421、4818、2093(すべて Small 4 Lane Road、2 車線ずつ)
- `junction_info`(2700,330): 信号なし、customLights false、canEnableLights true、canSetYield true。流入 3本とも cars true、yield false
- `net_near`(2450,-946、r160、Road): z=-950 は Small 4 Lane(5848、13096、14041、15481、30068、34194)。z=-860 は Basic Road(5784、17509、22905、26067、36689)
- `net_near`(2250,-950、r90、Road): z=-950 西の 3334、19196、36011(TooShort)、z=-860 の 10391、20293 など。Basic Road と Medium Road(20169)
- `net_near`(2413,-1240、r80、Road): z=-1240 の Basic Road 27206、9229、13690(すべて1車線ずつ)
- `net_near`(2087,282、r90、Road): 周りはすべて Small 4 Lane Road。Basic Road はない
- `test_upgrade_road`(Large Road、(2575,330)→(2778,330)): 差し替えには取り壊しが要る(断られた区間は 2093、4818、19619、25781。Fire House 17000 と高層の住宅・店を含む)。demolish=true は、Fire House の取り壊しを含むため採らない
- `test_upgrade_road`(Medium Road、同じ区間): 同じく断られた(ObjectCollision、取り壊しが要る)。採らない
- `test_upgrade_road`(Small 4 Lane Road、(2304,-860)→(2640,-860)): matched 5、upgraded 5、skipped 0、cost 0、取り壊し 0
- `test_upgrade_road`(Small 4 Lane Road、(2236,-860)→(2304,-860)): segment 14040 が Fire House 32853 にぶつかって断られた
- `test_upgrade_road`(Small 4 Lane Road、(2306,-1240)→(2520,-1240)): matched 3、upgraded 3、skipped 0、cost 0
- `test_upgrade_road`(Small 4 Lane Road、(2280,-950)→(2160,-950)): 3334、19196 が TooShort の 36011 にぶつかって断られた
- `test_upgrade_road`(Small 4 Lane Road、(2800,-490)→(3100,-490)): matched 3、upgraded 3、skipped 0、cost 0

## 判断の根拠

- 6-3 の流れは 54 で、目標 60 に届いていない。局所の blocked は、z=-950 の (2504,-946) 52 と (2325,-946) 42 に集まる。並行の z=-860 も density 85〜100 の Basic で、1車線ずつのまま。
- 同じ手(Basic → Small 4 Lane、取り壊しなし、費用 0)は、過去4回の月で局所の blocked を大きく減らした(m01-2、m02-2、m03-1、m05-3)。今月は、その手を、まだ残る density 100 の Basic の3群に当てる。
- 費用は、3群の試しの cost がすべて 0 で、維持費も Basic と同じ 40/km/週。上限(建設費 100,000、維持費の幅 4,000)に収まる。
- 案は1件にした。別の手は、確認できなかったり、取り壊しを伴ったりした(下の捨てたもの)。件数を埋めるための案は出していない。
- 調査は1件、z=-950 の blocked の追跡に使う。この案の効きを、見回り3回と月末で、同じ範囲で測るため。

## 捨てたもの

- 幹線 z=330 を Large Road や Medium Road に広げる案: `test_upgrade_road` で、沿道の高層住宅・店・Fire House の取り壊しが要る(Large は Fire House 17000 を含む。demolish=true では家と働き口を大きく失う)。取り壊しは戻せず、6-3 の効きも局所に留まるため採らない。
- 交差点 9244(2700,330)の信号、または譲れの標識: 交差点は信号なしで、canEnableLights と canSetYield は true。ただし、信号と譲れの費用・維持費は、道具の数字で確かめられない(list_net_types にも list_building_types にもない)。費用の上限に当てられないため、今月は実行対象に含めない。次月に、費用の確認が取れたら出し直す。
- 交差点 (2087,282) 周りの blocked 44: 周りは Small 4 Lane だけで、Basic → 4車線の手が当たらない。信号の費用が未確認のため、案に含めない。
- z=-950 西の 3334、19196 の差し替え: 36011(9m、TooShort)にぶつかる。TooShort の区間を外せば差し替えられるが、削る道具は持っていない(remove_line は取り壊しの議決が要る)ため採らない。
- 名所(Monument)の支線の道路: 名所の置き場は経済観光文化局の担当。道路側の案は出さない(前月の支線 [[2822,1000],[2728,1000]] は、economy-1 の担当で、道路の差し替えの手段ではない)。
- 政策 HeavyTrafficBan(トラックを道路から締め出す、costPerWeek 0): 交通の流れに効く見込みはあるが、トラックは品物を運ぶ車で、品物がない店 258(目標 120)と原料がない工場 37(目標 15)を悪化させるおそれが大きい。6-4、7-1 の数字を悪くするため採らない。
- 政策 FreeTransport(運賃を 0 にする): 交通の流れを変える政策ではなく、運賃収入が 0 になる(週の収入が減る)ため採らない。
- 6-3 の残りの手(バス台数の減少など): 港湾空港局の担当(port)。道路下水道局の案には含めない。
