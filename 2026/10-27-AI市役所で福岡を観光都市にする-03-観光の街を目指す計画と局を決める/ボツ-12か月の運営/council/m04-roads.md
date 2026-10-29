# m04 道路下水道局の案

## 案1: 北からの基本道路(x=2668)を4車線に差し替える(試し)

### 施策

- 案の id: roads-1
- 施策: 交差点(2668,330)の北へ出る基本道路2区間(z=330〜483、x=2668)を Small 4 Lane Road に差し替える。交差点(2719,326)の詰まりへ流れる車の入口を広げる。
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `test_upgrade_road`(prefab `Small 4 Lane Road`、points `[[2668, 330], [2668, 407], [2668, 483]]`、tolerance 20)で試す。結果: matched 2、upgraded 2、skipped 0、cost 0、demolishedBuildings 0。
  2. `upgrade_road`(prefab `Small 4 Lane Road`、points `[[2668, 330], [2668, 407], [2668, 483]]`、tolerance 20、pay true、demolish false)を本番で実行する。区間は segment 7468(2668,330→407)と segment 6704(2668,407→483)。
  3. 実行後に `traffic`(x 2719、z 326、radius 60)で blocked の数を見る。
- 設置条件の確認:
  - segment 7468: Basic Road、carLanes 1/1、交差点 node 4025(2668,330)の北の脚。`net_near`(x 2668、z 330、r 120)で確認。
  - segment 6704: Basic Road、carLanes 1/1、end node 5946(2668,483)。同じ `net_near` で確認。
  - 両区間とも `test_upgrade_road` で断られず、建物との重なりはなし(demolishedBuildings 0)。区画は保たれる(zonesKept true)。
  - 道路の差し替えは区画の指定と沿道の建物を保つ(tool-reference の upgrade_road の説明どおり)。
- 接続工事: 不要(差し替えのみ。新しい線は引かない)
- 予備候補: なし(この2区間だけを対象にする。別の区間は、この案の結果を見てから出し直す)
- 中止する条件: 実行の直前に `test_upgrade_road` を取り直し、skipped が1件でも出たら実行しない。demolishedBuildings が1件でも出たら実行しない(取り壊しの議決が要るため)。

### 期待する効果

- 改善の見込み: 交通の流れ53は目標60に届いていない。北からの基本道路 7468 と 6704 は、どちらも density 100(満杯)で、交差点 4025 の入口を狭めている。入口を広げると、交差点 9244(2700,330)へ流れる車が増える。その分、詰まりの位置が動く可能性がある。流れがどこまで上がるかは見積もれない。
- 数値と期限: 基準は `traffic` の blockedSpots (2719,326) の 52(半径200mの集計)、街全体の流れ 53、blocked 716。次の月例(4か月目から約30日後、5か月目の月例)で比べる。予想は、(2719,326) の blocked が下がるか、変わらないか、上がるかの3通り。下がれば効いた、上がれば詰まりが動いた。量は見積もれない。
- 確認方法: `traffic`(x 2719、z 326、radius 60)の blocked と、`traffic`(全体)の flow。見回り1・見回り2・月末の3回。実行前の値を同じ半径で取り直してから比べる。
- 不確かな点: 交差点 9244 は信号がなく、ここが本当の詰まりの場所なら、入口を広げても効きは小さい。その場合の戻し方は、同じ道具で Basic Road に戻す(`upgrade_road` の prefab を Basic Road に変え、同じ points)。費用は0の見込みだが、戻す操作は試していないため未確認。
- 試し: 仮説: 北の基本道路の狭さが、交差点 4025 の入口の詰まりを通じて、交差点 9244 の止まりを増やしている。測る数: `traffic` の blocked(x 2719、z 326、radius 60)と、街全体の flow。基準: blocked 52(半径200m の集計で見た値)、flow 53。編成方針の「分からないこと」の項目には当たらない。交通の流れの原因を確かめるための試し。

### 費用

- 建設費: 0(`test_upgrade_road` の cost 0、paid true。Basic Road と Small 4 Lane Road は同じ costPerKm 5,000、`list_net_types`)
- 週の維持費の増え分: 0(`list_net_types` で Basic Road と Small 4 Lane Road とも upkeepPerWeekPerKm 40。差は0)

### 戻せるか

戻せる。同じ区間を Basic Road に差し替え直すと、元に戻る(費用0の見込み。戻す操作は未確認)。

### 前の月の答え合わせ

- m03-roads-1(東西の基本道路7区間を Small 4 Lane Road に差し替え、採択・実行済み): 半分。東の (3230,-270) r250 の blocked は 116→18 に下がり、効いた。一方で、街全体の流れは 54→53 で、目標60に届かなかった。飛ばした 12091・16182 の扱いは、今月の案では扱わない。
- 前の月の調査 m03 の survey(`council/m03-survey-roads.md`): ファイルはない。今月は、この調査の結果を使えなかった。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(港湾空港局と分け持つ。流れの数)
- 編成方針の重点に当たるか: 当たらない(重点は観光、8-1、4-4。6-3 は重点外の案として道路下水道局が出す。編成方針の「局への伝え」どおり)

## 調査

- 調査: あり
- 問い: 交差点 9244(2700,330)と 30603(2110,330)の止まりは、信号のない交差点で続くか。続くなら、交差点の詰まりが流れの本当の制約か。
- 見る道具と引数: (1) `traffic`(x 2700、z 330、radius 60)、(2) `traffic`(x 2110、z 330、radius 60)、(3) `junction_info`(x 2700、z 330)
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: (1) (2700,330) r60 の blocked が、3回とも 40 以上なら、交差点が本当の制約。次の月に、交差点の制御(信号か譲れの標識)を出す。ただし、その費用は道具では確かめられない(tool-reference に費用の数字がない)ので、費用が確かめられるまでは案にしない。(2) blocked が 10 以下に減ったら、詰まりは一時的。案1の結果と合わせて見る。(3) canEnableLights が false に変わったら、信号の案は取り下げる。
- 担当の問題: 6-3 公共交通を主軸とした交通体系(交通の流れ)

## 見たもの

- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940/週、学校の維持費の25%増し)、RecreationalUse(0)、BigBusiness(3,952/週)。無効の HeavyTrafficBan(0)、FreeTransport(0、運賃の収入が0になる)は、交通の流れに関係する。政策の費用の合計 10,727/週(`economy_breakdown` の policyExpenses と同じ)。
- `city_info`: 人口 180,759、観光客 1,625/161、所持金 2,145,261、週の収入 346,977・支出 336,944、電気・水・下水が来ない市民 0/0/0。
- `citizens_without_service`(electricity): residents 0、buildings 0。
- `traffic`(全体): flow 53、cars 7,177、blocked 716(道の上 714)、congestion 2,487。blockedSpots は (2719,326) 52、(2102,305) 40、(2255,293) 37、(237,-293) 31、(2094,-884) 29。busiest は density 100 の基本道路が多い(例: segment 21069 (3093,-490)、segment 7468 (2668,370))。
- `net_near`(x 2719、z 326、r 120、Road): 交差点 9244(2700,330)の周りは Small 4 Lane Road。北からの基本道路 7468(2668,330→407)と 6704(2668,407→483)は Basic Road、carLanes 1/1。
- `traffic`(x 2719、z 326、r 200): blocked 75、busiest は 7468 (2668,370) と 6704 (2668,445) の density 100、Small 4 Lane の z=330 の区間は density 100。blockedSpots は (2719,326) 52、(2553,334) 10、(2666,441) 9。
- `junction_info`(x 2700、z 330): node 9244。trafficLights false、canEnableLights true、canSetYield true。脚は 3本(19421 の南、4818 の東、2093 の西)。
- `junction_info`(x 2668、z 330): node 4025。trafficLights false、canEnableLights true、canSetYield true。脚は 25781(西)、2093(東)、7468(北、Basic Road)。
- `test_upgrade_road`(Small 4 Lane Road、[[2668,330],[2668,407],[2668,483]]): matched 2、upgraded 2、skipped 0、cost 0、demolishedBuildings 0。
- `test_upgrade_road`(Small 4 Lane Road、[[2775,-490],[3130,-490]]): matched 5、upgraded 5、skipped 0、cost 0。ただし、この区間の blocked は 0(`traffic` r250 の blockedSpots は空)。案にしない。
- `test_upgrade_road`(Small 4 Lane Road、[[2236,-950],[2236,-860]]): upgraded 0。ObjectCollision で Fire House 32853(2253,-880)と Medical Clinic 32923(2213,-884)に当たる(blocks true)。demolish なしでは断られ、取り壊すとサービス施設が失われる。案にしない。
- `test_upgrade_road`(Small 4 Lane Road、[[2160,-950],[2280,-950]]): upgraded 0。ObjectCollision で segment 36011(9m、TooShort)。案にしない。
- `test_upgrade_road`(Small 4 Lane Road、[[3050,-390],[3080,-390],[3150,-390],[3154,-381]]): upgraded 1、skipped 16182(TooShort、SlopeTooSteep)。案にしない(点列の選び方が粗いので、同じ区間を試し直すには別の点列が要る)。
- `test_upgrade_road`(Basic Road、[[2668,330],[2668,407],[2668,483]]): 7468 と 6704 は既に Basic Road のため、戻す試しにはならなかった(戻す操作は未確認のまま)。
- `list_net_types`(Road、locked false): Basic Road と Small 4 Lane Road は costPerKm 5,000、upkeepPerWeekPerKm 40(同じ)。Large Road は 10,000 / 120。Medium Road は 7,500 / 100。
- `traffic`(x 2180、z 300、r 180): blocked 90、blockedSpots は (2102,305) 40、(2244,289) 34。busiest は Small 4 Lane の z=330 の区間(density 100)と Medium Road(density 92)。詰まりは交差点 30603(2110,330)付近で、道路の幅ではなく交差点が原因と見える。
- `traffic`(x 2094、z -884、r 150): blocked 35、blockedSpots は (2094,-884) 29。busiest は Basic Road(density 100)の 11482、10391、19196、20293、36011。道路の幅は狭いが、上の差し替えは断られる(前の項目)。
- `net_near`(x 2950、z -490、r 160、Road): 基本道路の格子(z=-390、-490、-620)。z=-490 の区間は 5524、9242、26681、21069、35451 の5本が1車線ずつ。
- `net_near`(x 2180、z 300、r 150、Road): 交差点 30603(2110,330)の脚は 26735、3990、22887。いずれも Small 4 Lane Road。
- `net_near`(x 2200、z -900、r 110、Road): 基本道路 10391、20293、19196、36011、3334、6223、29545 など。
- `net_near`(x 3140、z -410、r 90、Road): 基本道路 16182、2074、26243、27257 など。
- `zones_at`(x 2950、z -490、r 100): ResidentialLow 250(空き 2)。z=-490 の差し替えの確認に使った。
- `zone_map`(x 2200、z -880、r 150、size 500): 交差点 (2200,-880) の周りの区画。Fire House と Medical Clinic が差し替え区間に接している。
- `economy_breakdown`: 収入 346,977、支出 336,944、policyExpenses 10,727、loanExpenses 0。Road の支出は 8,526/週。Tourism 86。

## 判断の根拠

- 交通の流れは 53 で、目標60まで 7 足りない。blocked 716 のうち、(2719,326) の 52 がいちばん大きい単独の集まりで、ここは交差点 9244 と 4025 の近くにある。
- 北の基本道路 7468 と 6704 は、density 100 の満杯で、ここの入口を広げる手は、確認した条件(差し替えは断られず、費用0、維持費の増えも0)を満たす。唯一、実行できる手として確認済みの案。効きは見積もれず、試しとして出す。
- 交差点の制御(信号・譲れの標識)は、canEnableLights と canSetYield が true で、場所は確かめられた。しかし、費用を道具で確かめられない(前の月の m01 roads-2 と同じ理由)ため、案にしない。調査で、交差点の詰まりが続くかを先に確かめる。
- 案は1件だけにした。ほかの候補は、サービス施設との重なり、TooShort、blocked が0で効きの見込みがないため、採らない。件数を埋めるための案は出さない。

## 捨てたもの

- 信号を交差点 9244(2700,330)に付ける: blocked 52 の原因は交差点の可能性が高いが、建設費・維持費を道具で確かめられない(`list_net_types` と tool-reference に費用の数字がない)。上限に当てられないため、今月は案にしない。調査で、交差点の詰まりが続くかを確かめる。
- 譲れの標識を交差点 9244 に付ける: 信号と同じく費用を確かめられない。調査の結果を待つ。
- 信号を交差点 30603(2110,330)に付ける: 同じ理由(費用未確認)。blocked 40 の交差点で、次の月の候補。
- 2236,-950〜-860 の基本道路 10391・20293 を差し替える: Fire House 32853 と Medical Clinic 32923 に当たり、取り壊しにはサービス施設が要る。取り壊しの議決が要るうえ、サービスを失うため採らない。
- 2160〜2280, -950 の基本道路の行(3334、19196、36011): 36011 が TooShort で断られる。点列の引き直しが要る。今月は採らない。
- z=-490 の基本道路 5 本を 4車線化: 試しは断られず費用0。ただし blocked は 0 で、流れの目標へ効く根拠がない。次の月の候補として残す。
- 基本道路 16182 の差し替え: TooShort と SlopeTooSteep で断られる。点列の引き直しが要る。
- 政策 HeavyTrafficBan(トラックを道路から締め出す、費用0、無効): 交通の流れには効くと見込めるが、トラックは 8-1 の物流(貨物駅28755)の足で、port の目標と争う。効きを測れる根拠もない。今月は採らない。
- 道路の予算の変更(set_budget roads): 議決が要り、流れへの効きを道具で確かめられない。今月は出さない。
