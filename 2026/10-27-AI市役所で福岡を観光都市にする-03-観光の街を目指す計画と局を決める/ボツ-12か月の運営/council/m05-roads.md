# m05 道路下水道局の案

## 案1: 西の基本道路15区間を Small 4 Lane Road に差し替える

### 施策

- 案の id: roads-1
- 施策: 西の詰まり(中心 (-1256,-488)、(-1098,-481)、(-1296,-649))の基本道路15区間を、同じ道の幅の Small 4 Lane Road に差し替える。取り壊しはない
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: `upgrade_road`(prefab "Small 4 Lane Road"、tolerance 20、pay true、demolish false)を、次の5つの点列で順に呼ぶ。道路は1区間ずつ差し替える
  1. points [[-1245,-440],[-1245,-500],[-1245,-560]](2区間。Basic Road 3384・11218 付近)
  2. points [[-1070,-440],[-1070,-500],[-1070,-560]](2区間。Basic Road 3941・23469 付近)
  3. points [[-1340,-440],[-1280,-440],[-1245,-440],[-1160,-440],[-1100,-440],[-1070,-440]](6区間。Basic Road 14509・17903・14511・32461 付近)
  4. points [[-1388,-650],[-1317,-650],[-1245,-650],[-1187,-650]](3区間。Basic Road 20804・2820・22372 付近)
  5. points [[-1245,-560],[-1245,-605],[-1245,-650]](2区間。Basic Road 8821 付近)
- 設置条件の確認: 各点列を `test_upgrade_road`(同じ引数、demolish=false)で試した。
  - 1: matched 2、upgraded 2、skipped 0、cost 0、demolishedBuildings 0
  - 2: matched 2、upgraded 2、skipped 0、cost 0、demolishedBuildings 0
  - 3: matched 6、upgraded 6、skipped 0、cost 0、demolishedBuildings 0
  - 4: matched 3、upgraded 3、skipped 0、cost 0、demolishedBuildings 0
  - 5: matched 2、upgraded 2、skipped 0、cost 0、demolishedBuildings 0
  - 差し替えるのは同じ道路の仲間の道(`net_near` で、Basic Road、carLanes 1/1 を確認)。`list_net_types` で、Basic Road と Small 4 Lane Road の維持費は、どちらも 40/km/週で同じ。建設費は 5,000/km で、差し替えの試しの cost は 0
- 接続工事: 不要(既存の道の差し替えだけ。新しい線は引かない)
- 予備候補: なし(西の詰まりに使える未試しの区間はない。東の (2072,288) 付近は既に Small 4 Lane Road で、太くするには取り壊しが要るため外した)
- 中止する条件: 実行の直前に同じ点列で `test_upgrade_road` を取り直し、次のどれかに当たる点列は差し替えない。
  - cost が 0 でない、または demolishedBuildings が1件以上ある
  - skipped が1件以上ある(その区間は飛ばし、結果に記録する)
  - 取り直しで、街の財政が赤字(週の収支が 0 以下)になっている

### 期待する効果

- 改善の見込み: 西の詰まりの基本道路は、片側1車線(carLanes 1/1)で、交通量の密度が 100 に張りついている(`traffic` の busiest: 17903、23469、25388、14879 ほか)。同じ道幅の差し替えは、東と西ですでに詰まりを減らした(m02-2 西 blocked 71→11、m03-1 東 blocked 116→18)。今回も同じ手で、西の詰まりを減らすと予想する(局の予測)。
- 数値と期限: 対象は `traffic` の (x -1200, z -520, r 250) の円。今の値は blocked 139、cars 279、blockedSpots は (-1256,-488) 51、(-1098,-481) 41、(-1296,-649) 24。街全体の流れは 54(目標 60)。見回り1(10日後)と月末(30日後)で比べる。量の予想は、数値では見積もれない。
- 確認方法: `traffic`(x -1200、z -520、radius 250)の blocked と blockedSpots。街全体は `traffic`(引数なし)の flow。今と同じ引数で比べる。
- 不確かな点: 詰まりは別の場所(交差点や、差し替えていない区間)へ移るおそれがある(前例: m01-2 で詰まりが (2162,-721) へ移った)。数値は見積もれない。見るのは、西の円の blocked が 139 より減るかと、3つの blockedSpots が減るかの2点。
- 試し: なし(前例の同じ手で、効きの向きは確かめられている)

### 費用

- 建設費: 0(`test_upgrade_road` の cost 0。15区間の試し、どちらも cost 0)
- 週の維持費の増え分: 0(Basic Road と Small 4 Lane Road の維持費は、どちらも 40/km/週。`list_net_types`)

### 戻せるか

戻せる。`upgrade_road` で Basic Road に戻せる。取り壊しを伴わない。

### 前の月の答え合わせ

- m04-roads-1(北の基本道路 x=2668 を Small 4 Lane Road に差し替え、試し・採択・実行済み): 外れ。`traffic` の (2719,326) r60 の blocked は 27 → 26 で横ばい、flow は 53 → 54。見立ての「交差点が制約」は、この月の確認で半分だけ当たりと分かった。東の幹線の詰まりは、3差路 9244(2700,330)の南の枝(19421)の合流付近(2714,313)と、幹線の途中(2510,328)にある。`junction_info`(2700,330)は、信号なし、譲れの標識なしの3差路。
- m03-roads-1(東西7区間の差し替え、採択・実行済み): 半分。東の (3230,-270) r250 の blocked は 116 → 18 に下がった。街全体の流れは 54 → 53 で、目標 60 に届かない。
- 前の月の調査: `council/m04-survey-roads.md` はない(見つからなかった)。

### 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系(道路下水道局、港湾空港局と分け持ち)
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2 観光、4-4 資源循環、8-1 物流・人流のゲートウェイ)。6-3 は重点の外の案として出す

## 調査

- 調査: あり
- 問い: 東西の幹線 z=330 の詰まり(2510,328)と(2714,313)は、3差路 9244 の合流が原因か、区間の容量が原因か。
- 見る道具と引数: (1) `traffic` x 2700、z 320、radius 60(blocked、blockedSpots、busiest)。(2) `junction_info` x 2700、z 330(3差路 9244 の信号・標識の有無と、各枝の cars)
- いつ見るか: 見回り1・月末
- 何が分かれば次の手が決まるか: (a) 2714,313 の blocked が 2回とも 30 以上、かつ南の枝 19421 の density が 100 なら、9244 の合流が原因と見て、信号の案を次の月に出す。ただし信号の費用を道具で確かめる手がないため、費用を確かめる手を先に探す。(b) 詰まりが 2510,328 の区間に多いなら、区間の容量が原因。太くする案は取り壊しを伴うので、`preview_bulldoze` で失う家と働き口を数えてから検討する。
- 担当の問題: 6-3 公共交通を主軸とした交通体系(`traffic` の流れ)

## 見たもの

- `city_info`: 人口 180,993、所持金 2,161,625、週の収支 +8,218(収入 348,060、支出 339,842)、観光客 1,533/152、需要 26/2/56、幸福度 87、電気・水・下水が来ない市民 0/0/0、dialog なし
- `traffic`(街全体): flow 54、cars 7,253、blocked 790(道の上 790)、busiest は density 100 の基本道路が多い。blockedSpots は (-1256,-488) 51、(2072,288) 45、(-1098,-481) 41、(2510,328) 38、(2714,313) 38
- `traffic`(x 2600、z 310、r 400): flow 54、cars 339、blocked 127、blockedSpots は (2510,328) 38、(2714,313) 38、(2293,287) 23
- `traffic`(x -1200、z -520、r 250): flow 54、cars 279、blocked 139、busiest は density 100 の基本道路 8 本、blockedSpots は (-1256,-488) 51、(-1098,-481) 41、(-1296,-649) 24
- `traffic`(x 2050、z 290、r 150): cars 89、blocked 77、blockedSpots は (2072,288) 45、(1960,280) 17、(2075,160) 15(既に Small 4 Lane Road)
- `junction_info`(2700,330): node 9244、信号なし、customLights false、canEnableLights true、canSetYield true。枝は Small 4 Lane Road 3本(東 4818、西 2093、南 19421)
- `junction_info`(2719,326)・(2072,288)・(1908,291)・(2510,328)・(-1256,-488)・(-1098,-481): 40m 以内に交差点なし(詰まりは区間の途中)
- `list_policies`: 政策の週の費用の合計 10,627。有効なのは SmokingBan(0)、EducationBoost(7,940/週、学校の維持費の25%増し)、RecreationalUse(0)、BigBusiness(3,920/週)。HeavyTrafficBan は無効で費用 0。FreeTransport は無効で費用 0(運賃の収入が 0 になる)。道路に関係する政策は HeavyTrafficBan のみ
- `list_net_types`(Road、解禁済み): Basic Road 5,000/km・40/km/週、Small 4 Lane Road 5,000/km・40/km/週、Medium Road 7,500/km・100/km/週、Large Road 10,000/km・120/km/週
- `net_near`(x 2650、z 330、r 340): 東西の幹線 z=330 は Small 4 Lane Road(2 車線ずつ)。西端の x=2450〜2935 の区間は、利用の多い区間が含まれる
- `net_near`(x -1200、z -520、r 200): 西の詰まりの区間は Basic Road(1 車線ずつ)。Small 4 Lane Road は z=-650 の 2 区間 ほか
- `net_near`(x 2050、z 290、r 130): 東の (2072,288) 付近は Small 4 Lane Road
- `test_upgrade_road`(Large Road、z=330 幹線 x 2450→2935、demolish=false): matched 8、upgraded 0、skipped 7。壊す建物 の数が多い(住宅・事務所・店)。Fire House 17000(2680,300)が 2093 の区間をふさぐ
- `test_upgrade_road`(Large Road、同じ点列、demolish=true): upgraded 7、cost 2,320、demolishedBuildings 約 35 棟(住宅・事務所・店・Fire House 17000 を含む)。2093 は Fire House にぶつかって飛ぶ
- `test_upgrade_road`(Small 4 Lane Road、西の5点列): 上の「設置条件の確認」の表のとおり。どれも cost 0、skipped 0、demolishedBuildings 0
- `citizens_without_service`(electricity): 0 件
- `read`: `tool-reference.md`(道具の名前と引数)

## 判断の根拠

- 担当の数字は、流れ 54(目標 60)と、止まった車 790。重点の外だが、道路は担当の問題で、案は出せる。
- 西の詰まりは、片側1車線の基本道路で、密度が 100 に張りついている。同じ道幅の差し替えは、費用 0、取り壊し 0 で確認できた。前例(m02-2、m03-1)で効いた手と同じなので、1件出す。
- 東の z=330 幹線は、Large Road に太くすると 30 棟以上を取り壊す(Fire House を含む)。取り壊しは戻せず、失う家と働き口も大きいため、案にしない。
- 3差路 9244 の信号は、canEnableLights が true で、置ける。ただし信号の建設費と維持費の数字が道具にない。前月の信号案(m01-roads-2)も費用が確かめられず不採択だった。費用を確かめる手段が見つからないので、案にせず調査にする。
- 案の数は1件。ほかの候補は、取り壊しを伴うか、費用が確かめられないか、既に 4 車線で効きが見込めないため。件数を埋めるための案は出さない。

## 捨てたもの

- 東の z=330 幹線(x 2450〜2935)を Large Road に太くする: test で 30 棟以上の取り壊しが出る(住宅・事務所・店。Fire House 17000 を含む)。取り壊しは戻せず、失う家と働き口も数えきれていない。案にしない。取り壊しの議案として出すなら、`preview_bulldoze` で家と働き口を数えてから出し直す。
- 3差路 9244(2700,330)に信号(`set_traffic_lights`、x 2700、z 330、active true): canEnableLights は true だが、信号の建設費と維持費が道具に出ない。前月の信号案と同じく、費用が確かめられない。調査で、詰まりが合流によるかを先に確かめる。
- 東の (2072,288) 付近の幹線: 既に Small 4 Lane Road。太くするには取り壊しが要る見込み(未試し)。
- HeavyTrafficBan(政策、費用 0、無効): 大型のトラックを道から締め出すと、品物がない店 258 と原料がない工場 32 が増えるおそれがある。6-4、7-1 の目標に反するため、採らない。
- FreeTransport(政策、費用 0): 運賃の収入が 0 になる(週の収入が減る)。黒字を守る財政の線に反するため、採らない。
- バスの台数と路線の予算: 港湾空港局の担当(port 側)。道路局の案にしない。
