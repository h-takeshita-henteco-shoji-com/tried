# m06 港湾空港局の案

## 施策

- 施策: 貨物駅28755(3449,-1555)の出口2本(Cargo Connection の端 (3417,-1555) と (3417,-1560))を、Large Road(x=3400)まで Cargo Connection で延ばす試し。`build_line` を2回呼ぶ。止まったトラック514が減るかを見る
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み(置ける条件は試しの道具で確認。線が道路の網につながったかは、実行時の戻り値と翌日の測定で確かめる)
- 対象と操作順:
  1. `build_line(prefab="Cargo Connection", points=[[3417,-1555],[3400,-1555]], pay=True)`(出口。既存 Cargo Connection 25546 の端 node 5129 から Large Road 20316 の中ほどへ)
  2. `build_line(prefab="Cargo Connection", points=[[3400,-1567],[3417,-1560]], pay=True)`(入口。Large Road の node 27757 から既存 Cargo Connection 30062 の端 node 20745 へ。並びの順が進む向き)
  3. 戻り値の `ends`(connectedTo)と `snapped`/`split` を記録する
  4. 2本の後、`net_near(x=3410, z=-1557, radius=30)` で新しい区間の端の node が Large Road と同じ番号か確かめる
- 設置条件の確認:
  - `test_build_line`(Cargo Connection、[[3417,-1555],[3400,-1555]]): ok、segments 1、crossings 0、cost 0、overlaps なし(5か月目に確認)
  - `test_build_line`(Cargo Connection、[[3400,-1567],[3417,-1560]]): ok、segments 1、crossings 0、cost 0、overlaps なし(今月)
  - `test_build_line`(Cargo Connection、[[3417,-1555],[3400,-1543]]、[[3417,-1560],[3400,-1567]]): ok、cost 0(今月。予備の形)
  - `test_build_line`(Basic Road、[[3400,-1567],[3409,-1558]]): ObjectCollision・TooShort・SlopeTooSteep で断られた。道路を引く案は使わない
  - `net_near`(3430,-1557、半径60): 出口 25546 は node 5129 (3417,-1555) で終わり、入口 30062 は node 20745 (3417,-1560) から始まる。Large Road 20316・30945 の端は (3400,-1567) で別の node
  - `net_near`(3540,-1557、半径60)と `net_near`(2380,-1282、半径80): 同じ形の貨物駅13893は、Cargo Connection の端 (3497,-1555) が Small 4 Lane Road(x=3495)に2mまで近く、道路に重なる。28755は端が道路の縁から約5m離れている(Large Road の幅の推定による)。この差が原因かは未確認
  - `traffic`(3400,-1500、半径250): cars 49、blocked 0、congestion 4。Large Road 側は詰まっていない
  - `list_net_types`(Beautification): Cargo Connection は引ける線の一覧にない。`test_build_line` は通る。実行時に断られることがある
- 接続工事: 上の2本が接続工事そのもの。建設費は試しの道具で 0
- 予備候補: 1本目の代わりに [[3417,-1555],[3400,-1543]]、2本目の代わりに [[3417,-1560],[3400,-1567]](向きが逆になるため、1本目が通らなかったときだけ。どちらも `test_build_line` で ok)
- 中止する条件: 実行前に `net_near`(3410,-1557、半径30)が今月と同じ4区間でなければ見送る。`build_line` が断ったら、その線だけ飛ばし、予備の形を1回だけ試す。2本とも断られたら見送る。引いた後、戻り値の ends が両端とも connectedTo "none" なら、網につながっていないので、線は残して測定の結果を待つ(消すには取り壊しの議決が要る)

## 期待する効果

- 改善の見込み: 28755 の止まったトラック514は、全部が (3441,-1555) の出口の線の上で WaitingSpace のまま動かず、120〜150日止まった車もある。出口の端が道路から約5m離れていることが、動かない原因の1つかもしれず、端を道路まで延ばせば出口の列が流れ出すと予想する(予想。同じ形の13893は端が道路に重なっているが、荷が来ず動きは比べられない)
- 数値と期限: `cargo` の stoppedInBuildings 514(全部 28755)→予想は 300 以下(目標250以下)。期限は7か月目の月初。効かなければ514のまま。数値は見積もれない(効くかどうかが二択に近い)
- 確認方法: `cargo` の stoppedInBuildings と stoppedInBuildingsTop、`vehicles_stuck(kind="truck", building=28755, limit=100)` の byState の WaitingSpace+Importing+InGrounds(今 514)と bySeenStopped の 7days+(今 478)。実行の翌日と見回りで、今月と同じ条件で比べる
- 不確かな点: 新しい線が Large Road の網につながるかは、試しの道具では確かめられない(`build_line` の戻り値で分かる)。つながっても、Cargo Connection の車線の向きと、Large Road への出入りの曲がり方で、車が出られない可能性がある。原因が出口の隙間でなく、駅の中の車の数の上限や、原料・品物の行き先の問題なら効かない。1本目と2本目が5m離れて並ぶため、片方だけつながることもある
- 試し: あり。仮説は、出口の端が道路につながっていないことが、貨物駅28755で止まる車の原因になっており、端を道路へ延ばせば、止まった車が減る。測る数は `cargo` の stoppedInBuildings(基準514)と `vehicles_stuck` の WaitingSpace+Importing+InGrounds(基準514)。場所は貨物駅28755 (3449,-1555)。編成方針の「分からないこと」の1つ目(貨物駅28755の敷地の中で止まっている原因)に当たる

これは局の予測です。ゲームの効果の正解を取得しません。

## 調査

- 調査: あり
- 問い: 出口2本の延長の後、28755 の止まったトラックは減り始めたか、先頭の車は動いたか
- 見る道具と引数: `vehicles_stuck(kind="truck", building=28755, limit=100)`、`cargo()`、`net_near(x=3410, z=-1557, radius=30)`
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: stoppedInBuildings が減る、または seenStoppedDays が0に戻るなら、同じ形を残し、来月は貨物駅の入口と出口の組を増やす案を出す。数が変わらず、新しい区間の端が Large Road と別の node のままなら、つながっていないので、別の原因(駅の中の車の数の上限、荷の行き先)を調べる。新しい区間の端が同じ node で、数が変わらないなら、Large Road への曲がりを `junction_info` で調べる
- 担当の問題: 8-1 物流・人流のゲートウェイ

## 費用

- 建設費: 0(`test_build_line` で2本とも cost 0)
- 週の維持費の増え分: 0に近い見込み。Cargo Connection は `list_net_types` に維持費がない。数値は未確認

## 戻せるか

戻せる。`remove_line` で消せるが、取り壊しの議決が要る。

## 前の月の答え合わせ

- 前の月(5か月目)の案「乗客の少ないバス15路線の台数の割合を20ポイント下げる試し」は採られなかった。理由は、同じ6-3の m05-3 と効き目を分けられず、減る約70台が街の車の約1%と小さいため。今月はバスの案を出さない(今月の流れ53%は m05-3 の差し替えが効いて上がり、バスの台数を下げる案の効き目は小さいまま)
- 調査 s05-1(貨物駅28755の出口の隙間が原因か)の結果: 見回り1・2・月末とも、止まった車は611台前後、そのうち約490〜514台が (3441,-1555) の敷地内で WaitingSpace、blockCounter 0、waitCounter 0。120〜150日止まった車が15〜19台。Cargo Connection の端の node(5129、20745)は Large Road の node 27757 と別のまま。出口の外の道は詰まっていない(今月 `traffic` blocked 0)。先頭は動かないので、前月に決めた次の手(出口をつなぐ工事)を今月の案にした
- 前月との違い: 前月は Basic Road や駅の移設を試して駅28755に重なり断られた。今月は、通ると分かっている Cargo Connection の2本に絞り、費用0で、取り壊しも要らない形にした。接続が確かめられない点は、実行時の戻り値と調査で追う

## 市の計画

- 当たる施策: 8-1 物流・人流のゲートウェイ
- 編成方針の重点に当たるか: 当たる(重点の2番目)

## 見たもの

- `cargo`: stoppedInBuildings 514(全部 28755 Cargo Center)、stoppedOnRoads 348。止まった場所の上位 (3439,-1551) 66台。Goods 560、Lumber 98、Petrol 91、Coal 71、Food 41。noGoods 178、noResources 43。28755 の vehiclesLeaving 743
- `list_policies`: 比較した政策。HeavyTrafficBan(無効、週0、重い車の通行禁止。貨物の遅れを悪化させるため不採用)、FreeTransport(無効、週0、バスの切符収入が失われるため不採用)、IndustrySpace(有効、週4,797)、BigBusiness(有効、週4,116)、EducationBoost(有効、週7,940)。貨物駅の出口に効く政策は見当たらない。政策費用は週15,746
- `list_transport_lines`: バス路線は多くが乗客100未満(Line 28 は190台で乗客53)。メトロ Line 1 は乗客0。pathFailed は line 203 の1のみ。今月はバスの予算を変えない
- `transport_reach`: 28755、13893、3940、4740、40031 は outsideConnected true。14580、16572、48243 は false(gap 271・725・2933m)で車は出ない
- `trade`: import 合計15,948(goods 6,911)、export 1。道路のつなぎ口 8840 に185台、27833 に138台
- `net_near`: (3430,-1557) 半径60。Cargo Connection 25546・30062 の端は (3417,-1555)・(3417,-1560)。Large Road 20316・30945 は node 27757 (3400,-1567) で別。(3540,-1557) 半径60 と (2380,-1282) 半径80 は、同じ形の駅13893・3940の端と道路の位置を確認
- `net_near`(service=Road): (3440,-1555) 半径120。Large Road、Small 4 Lane Road x=3495 など9区間
- `zone_map`: (3430,-1557) 半径100。貨物駅28755の敷地は x 約3416〜3481。Large Road(x=3400)の東は未指定の空き
- `junction_info`: (3400,-1567) と (3400,-1493) の40m以内に交差点なし(Large Road は直線)
- `test_build_line`: 上の「設置条件の確認」のとおり
- `list_net_types`: Beautification に Cargo Connection がない(引ける線の一覧の外)
- `vehicles_stuck`: 28755 の車611台、WaitingSpace+Importing+InGrounds 514、WaitingSpace+Importing+OnRoad 64、7days+ 478。samples 12台は全部 (3441,-1555)、blockCounter 0、seenStoppedDays 0〜130
- `traffic`: (3400,-1500) 半径250。flow 53、cars 49、blocked 0、congestion 4

## 判断の根拠

8-1 の stoppedInBuildings は514で、目標250の2倍。止まった車は全部が貨物駅28755の出口の線の上にあり、外の道は詰まっていないので、原因は駅の側にある。出口の端が道路の網につながっていない可能性を、費用0の線2本で試す。つながるかは試しの道具で確かめられないため、効くかどうかが分からない「試し」として出し、効かなくても失うものは0で、結果が来月の調査になる。

## 捨てたもの

- バス路線の台数を下げる案(5か月目の再提出): 6-3 の流れは53%まで上がり、減る台数は街の車の約1%と小さい。当月の担当課題として貨物駅28755のほうが目標から遠い(514対250)ため
- 駅28755を取り壊して別の場所に移す・Cargo Center の新設: 移設先が道路や貨物線路にぶつかって断られた(5か月目)。新設は建設費60,000で、今月の枠95,000には入るが、荷の入口を壊す危険と、効く根拠がないため
- Basic Road で出口の隙間を埋める: `test_build_line` で ObjectCollision・TooShort・SlopeTooSteep、駅28755に重なって断られる
- 港や空港を増やす案: 船・飛行機は貨物の輸入が少なく(ship 10台、plane 0台)、止まった車は貨物駅28755のものだけなので、効きが小さい
- 政策 HeavyTrafficBan: 週0で試せるが、貨物トラックの通行を減らすため、品物がない店178を悪化させる
