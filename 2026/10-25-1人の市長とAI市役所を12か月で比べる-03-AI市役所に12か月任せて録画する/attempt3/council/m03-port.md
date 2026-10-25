# m03 港湾空港局の案

## 施策

- 施策: 鉄道の予算を昼夜とも120%から100%へ戻す。`set_budget` で train を対象にする(試し m02-2 の撤回)
- 議決: 予算

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `economy` で train が昼120・夜120であることを確かめる
  2. `economy_breakdown` で PublicTransportTrain の支出が12,701前後(12,000〜13,500)であることを確かめる
  3. `set_budget(target="train", percent=100)`
  4. `economy` で train が昼100・夜100になったことを確かめる
- 設置条件の確認: 該当なし。`economy` で train 昼120・夜120、`economy_breakdown` で PublicTransportTrain の支出12,701を今月確認した。引数は `tool-reference.md` の set_budget(percent は 50〜150)で確かめた
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: train が昼夜とも120でない、または PublicTransportTrain の支出が12,000未満か13,500超なら見送り、理由を書く

## 期待する効果

- 改善の見込み: 8-1 の止まったトラックは予算では動かないと m02-2 で分かった(blockCounter 0・waitCounter 0)。100%へ戻すと、効かない支出だけが減る。確認した事実は、予算を上げた後に stoppedInBuildings が496→555へ増えたことである
- 数値と期限: PublicTransportTrain の支出は12,701、予想は約11,000〜11,500(m02-2 の増分1,728を戻す見込み。見積もれない部分あり)。週の収支は+8,035、予想は+9,500前後。期限は翌月の月例(2050-04-01)。`cargo` の stoppedInBuildings は555、予算を戻しても大きくは変わらない見込み(現状維持の確認)
- 確認方法: `economy_breakdown` の PublicTransportTrain の支出、`city_info` の週の収支、`cargo` の stoppedInBuildings(28755 が534)、`vehicles_stuck(kind="truck", building=28755, limit=10)` の 7days+(基準485)
- 不確かな点: 支出が1,728分ぴったり戻るかは未確認。stoppedInBuildings が増減するかも見積もれない。戻して増えたら、予算は駅の台数に関与するという別の仮説が立つ
- 試し: 仮説「鉄道の予算は貨物駅28755 の止まったトラックの数に効かない」。測る数は `cargo` の stoppedInBuildings(555、28755 は534)と `vehicles_stuck` の 7days+(485)。場所は 28755(3449,-1555)。基準は今月の値。編成方針の「貨物駅28755 の敷地の中で止まるトラックの原因」に当たる

## 調査

- 調査: あり
- 問い: 28755 の敷地の中で60日動かない車は、出口の点(3441,-1555)の先頭の車が動かないことで列が止まっているのか
- 見る道具と引数: `vehicles_stuck(kind="truck", building=28755, limit=30)`、`cargo()`、`traffic(x=3441, z=-1555, radius=150)`
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: 先頭の車(vehicle 8、183 など seenStoppedDays 60超)が同じ位置と状態のまま、列の後ろの車が動いているなら、出口の点に詰まる車が原因。次月は `set_building_active(id=28755, active=false)` を止めて動かす試しを出す。全体の台数が揃って増えるなら、駅の到着が処理を超えているため、別の貨物駅へ荷を分ける案を調べる
- 担当の問題: 8-1 物流・人流のゲートウェイ

## 費用

- 建設費: 0
- 週の維持費の増え分: 約-1,700(減る側。m02-2 で測った PublicTransportTrain の増分 +1,728 を戻す見込み)

## 戻せるか

戻せる。`set_budget` で120%に戻せる。

## 前の月の答え合わせ

m02-2(鉄道の予算120%、試し、可決、実行済み)は外れ。期限は見回り2の400以下だったが、`cargo` の stoppedInBuildings は 496→527→527→555 と増え、28755 の7日以上止まった車は455→485 だった。鉄道の支出は10,973→12,701(+1,728)。理由は、敷地の中の車の blockCounter 0・waitCounter 0 が60日変わらず、処理の速さが原因でないため。今月は戻す案を出す。調査 s02-1 の結果は、28755 の vehiclesLeaving が746→807 と増え続け、stoppedSpots 先頭は3441,-1555 の51台で変わらなかった。出口の先の渋滞は支持されず、出口の点に残る仮説を今月の調査で絞る。m01-3(バスの大型3路線)は小さく効いた(支出-343)が、交通の流れの効きは分からない。

## 市の計画

- 当たる施策: 8-1 物流・人流のゲートウェイ
- 編成方針の重点に当たるか: 当たらない

## 見たもの

- `cargo`: stoppedInBuildings 555(28755 が534、港1366 が20)、stoppedTrucks 874、stoppedOnRoads 319、stoppedSpots 先頭 3441,-1555 が51、noGoods 229、noResources 34、28755 の vehiclesLeaving 807
- `list_policies`: 比較した政策は PowerSaving(無効、58,373)、WaterSaving(無効、58,373)、HeavyTrafficBan(無効、0)、FreeTransport(無効、0。運賃収入が0になる)、IndustrySpace(無効、4,864)、BigBusiness(有効、3,900)、EducationBoost(有効、7,940)。貨物駅の止まったトラックに直接効く政策は見当たらない。HeavyTrafficBan は重い車の通行を止めるので、荷の車を減らすが店の品物がさらに届かなくなるため見送り
- `economy`: train 昼120・夜120、bus 150、ship 120、plane 100、metro 100。税 住低9・住高7・商低9・商高3・工3・事3
- `economy_breakdown`: PublicTransportTrain の支出12,701、バス21,746(収入4,801)、船4,608、地下鉄539。週の収入341,780・支出333,745
- `vehicles_stuck`: 28755 の vehicles 634、WaitingSpace+Importing+InGrounds 534、7days+ 485、標本の vehicle 8 と 183 が60日、全部 3441,-1555
- `net_near`: (3441,-1555、r150、Road)12区間。出口側に Large Road(3400,-1493〜-1640)と Small 4 Lane Road(3495,-1490〜-1626)があり、点そのものは道路の区間の上にない
- `traffic`: 流れ53%、blocked 688、blockedSpots の上位に 3441,-1555 付近はない
- `junction_info`: (3441,-1555)から40m以内に交差点なし(エラー)
- `buildings_near`: (3449,-1555、r60)28755 のみ。workers 53、vehicles.inUse 807、problems Garbage、電気・水・下水あり
- `transport_reach`: 28755、13893、3940、4740、40031 は outsideConnected true。14580、16572、48243 は false

## 判断の根拠

m02-2 は効かず、鉄道の支出が+1,728 増えたまま残っている。月例の方針も、100%へ戻す案を求めている。戻すと週の維持費が約1,700減り、黒字(+8,035)が厚くなる。止まったトラックの数は、予算では動かないと実測で分かった。このため、新しい建設より先に、動かない原因を絞る調査をあわせて出す。

## 捨てたもの

- 貨物駅28755 を `set_building_active` で止めて動かす案: 議決はいらないが、止めると働き手53と荷の流れが止まる。効きが分からず、原因を絞る前なので、調査の結果を見て来月に出す
- 別の貨物駅(13893 など)を新設して荷を分ける案: 13893 は vehicles.inUse 0 で既にあるが、荷の行き先をこちらで選ぶ道具がなく、効きの見込みが立たない。建設費も枠(400,000)の使い道として弱い
- FreeTransport や HeavyTrafficBan の政策: 貨物駅の台数に直接効かず、運賃収入や品物の流れを減らす
- バスの予算の変更: m01-3 で小さく効いたのみで、今月の8-1 の課題とは別
