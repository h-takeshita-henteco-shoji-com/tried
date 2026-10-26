# m12 道路下水道局の案

## 施策

- 施策: 東の3差路 (2110,330) と (2110,240) に、`set_traffic_lights` で信号を付ける試し
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `set_traffic_lights(x=2110, z=330, active=true)`
  2. `set_traffic_lights(x=2110, z=240, active=true)`
  3. 実行直後に `traffic(x=2108, z=313, radius=200)` で blocked を測る。月末にも同じ円で測る
- 設置条件の確認:
  - `junction_info(2110,330)`: node 30603、trafficLights false、canEnableLights true。Small 4 Lane Road の3本(segment 3990 bearing 90、22887 bearing 180、26735 bearing 270)
  - `junction_info(2110,240)`: node 24624、trafficLights false、canEnableLights true。Small 4 Lane Road の3本(segment 5864 bearing 0、4374 bearing 180、9308 bearing 270)
- 接続工事: 不要(信号の設定のみ。建設費0、維持費の増え分0の見込み)
- 予備候補: なし
- 中止する条件: 実行前の `junction_info` で canEnableLights が false、または既に trafficLights が true なら、その交差点は見送る

## 期待する効果

- 改善の見込み: 今月の blockedSpots (2075,234) の15台は (2110,240) の近くで、信号のない3差路で車が譲り合えず止まっていると予想する。信号を付けた (2700,330) では止まる車が 30→6 に減ったので、同じ形の手を使う。
- 数値と期限: `traffic(x=2108, z=313, radius=200)` の blocked は今 39(congestion 100、averageDensity 65)。予想は 25 以下。確認は月末(12か月目の終わり)。
- 確認方法: `traffic(x=2108, z=313, radius=200)` を実行直後と月末の同じ条件で測り、blocked と congestion を比べる。
- 不確かな点: 街全体の flow 54% は動かない見込み(過去の信号3件とも全体には効かなかった)。(2700,330) では交差点の止まる車は減ったが渋滞は減らなかった。バスの予算が同じ月に変わると数が混ざる。
- 試し: 仮説は、信号が3差路の譲り合いの停止を減らし、blocked を減らす。測る数は `traffic(x=2108, z=313, radius=200)` の blocked。場所は (2110,330) と (2110,240)。基準は blocked 39。編成方針の「分からないこと」の外で、6-3 の流れに関わる試し。

## 調査

- 調査: なし

## 費用

- 建設費: 0(信号の設定のみ)
- 週の維持費の増え分: 0(見込み。道具では費用を確かめられない)

## 戻せるか

戻せる。`set_traffic_lights` を active=false にすれば外せる。

## 前の月の答え合わせ

- m11-roads(同じ2か所の信号): 採られなかった。理由は、バス予算の変更と blocked が混ざり分けられないため。今月はバスの予算が130%で安定した後なので、実行直後と月末の2回に分けて測り、再提出する。
- m11 の調査 s11-2: (2700,330) の信号後も blocked は 45→38→41 で下がらず、density 100 の区間が信号の周りに残った。信号は止まる車を減らしたが、道が飽和して渋滞は残ると分かった。今月は、同じ形の手を、まだ信号のない近くの2か所に使う。街全体の flow は54%で、6-3 の目標60%は届かない見込みと認める。

## 市の計画

- 当たる施策: 6-3 公共交通を主軸とした交通体系
- 編成方針の重点に当たるか: 当たる

## 見たもの

- `traffic`: 街全体 flow 54、cars 7,821、blocked 700、congestion 2,351。blockedSpots 上位 (-2113,-1931) 67、(2693,318) 35、(1484,81) 29。円 (2108,313) 半径200 は blocked 39、congestion 100、blockedSpots (2075,234) 15
- `city_info`: 人口177,159、所持金2,390,360、週 +8,291、電気・水・下水が来ない 0/0/0
- `list_policies`: 有効は EducationBoost 7,940、BigBusiness 4,112、IndustrySpace 4,821。道路・信号に関わる政策は HeavyTrafficBan(無効、費用0)だけで、流れへの効きの根拠がなく外した
- `junction_info`: (2110,330) と (2110,240) は信号なし、canEnableLights true
- `net_near`: (-2113,-1931) の周りは Basic Road の格子で、blocked 67 の交差点は junction_info で見つからなかった(40m以内に交差点なし)
- `Read`: tool-reference.md で `set_traffic_lights` の引数を確かめた

## 判断の根拠

担当の電気・水・下水は 0/0/0 で保てている。流れは54%で、60%に1か月で届く手は見つからない。最も費用が低く戻せる手として、実行条件を確認済みの信号2か所を再提出する。(-2113,-1931) の blocked 67 は、近くに交差点がなく、Basic Road の差し替えも手がかりがないので、今月は案にしなかった。

## 捨てたもの

- (-2113,-1931) の blocked 67 への手: 40m以内に交差点がなく、原因が分からない。最終月で調査の結果を次の手に使えないため出さない
- HeavyTrafficBan: 費用0だが、流れへの効きの根拠がなく、貨物の流れを変えるおそれがある
- Large Road への差し替え(2700,330 付近): 10か月目に防火署や高密度住宅の取り壊しで断られた。戻せない
