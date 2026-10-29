# m05 経済観光文化局の案

## 案1: 空き地3に名所 StatueOfWealth を置く(支線つき)

### 施策

- 案の id: economy-1
- 施策: 名所(Monument)の StatueOfWealth を空き地3の (668, 1565) に、向き east で置く。送電線の支線 (647,1587)→(668,1565) で電気を通す。名所の棟数 8 → 9 を狙う。空き地3は道路(セグメント 13359)に面している。市の計画 5-1、5-2 観光
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み(再調査で、条件の道具の確認が通った。通電は置いた後の grid で確かめる)
- 対象と操作順(建物を先、線を後):
  1. `test_place_building` prefab=StatueOfWealth、x=668、z=1565、facing=east(実行の直前に、もう一度試す。ok なら次へ)
  2. `place_building` prefab=StatueOfWealth、x=668、z=1565、facing=east、pay=true(建設費 25,000)
  3. `test_build_line` prefab=Power Line、points=[[647,1587],[668,1565]](置いた後に試す。ok なら次へ)
  4. `build_line` prefab=Power Line、points=[[647,1587],[668,1565]]、pay=true(建設費 80。始点は既存の送電線の node 32160、終点は名所の敷地の中)
  5. `buildings_near` x=668、z=1565、radius=40 で、名所の grid.electricity が true、ports を確かめる。建物は道路に面しているので、道路は引かない
- 設置条件の確認:
  - 敷地と道路: `test_place_building`(2050-05-01 と今回の再確認)で ok、cost 25,000、enoughMoney true、needsRoad true、入口 (700,1565) が道路 13359 から距離 4、wouldDemolish 0、取り壊しの働き口と家 0。大きさは 8×8 マス(`list_building_types`)
  - 公園 P3(762,1600)との重なり: P3 は未建設。`test_place_building`(Regular Park、762,1600、facing west)で ok、入口 (730,1600) が道路 968 から距離 10。名所の東の端は x=700 付近(8マス=約64m、中心から±32m)で、P3 の西の端は x≈726(公園の大きさの見積もり)。約26m空くので重ならない
  - 電気の網: `net_near`(690,1640、r150、Electricity)で、送電線 36842(node 4380→32160)、5220(32160→17930)、13409(17930→24073)、22108、13350(21832→12272)が node を共有してつながる。`net_near`(560,1480、r120)で、網は (467,1373) まで続く。`map_layer` electricity_service(440,1340、r40)は全部 1。網は電気のある所とつながると読む。名所の敷地(668,1565、r60)の electricity は今 0(建物も線もないため)
  - 支線: `test_build_line`(Power Line、[[647,1587],[668,1565]])で ok、segments 1、cost 80、overlaps []
  - 水と下水: 要らない(`list_building_types`(service=Monument)の needs)
- 接続工事: 支線 1 本(建設費 80、週 約 2。`list_net_types` の Power Line は 1km あたり週 60、長さ約 30m)。道路は不要。道路下水道局への接続の依頼は不要(4380 の網は確かめた)
- 予備候補: なし(空き地3の中で、道路 13359 に面して名所が置けるのは (668,1565) のみ確認済み)
- 中止する条件: (a) 実行直前の `test_place_building` が断られる。(b) 置いた後の `test_build_line` が断られる。(c) 支線を引いた後、名所の grid.electricity が 1 にならない。その場合は支線を消さず(remove_line は議決が要る)、名所は残して、次の月に通電の原因を確かめる。(d) 建設費の合計が 25,080 を超える
- 再調査の結果: 条件(`test_build_line` で既存の網から名所の敷地に端が入る支線が通ること、費用つき。P3(762,1600)と重ならない位置で `test_place_building` が ok)を満たした。支線 (647,1587)→(668,1565)、費用 80。P3 と重ならない(上の確認)。前の調査の「4380 は網につながっていない」は、4380 の端の点だけを見た読み違いだった。4380 は 36842 で 32160 につながり、網の一部になっている

### 期待する効果

- 改善の見込み: 観光の名所を1棟増やすと、名所の棟数が 8 から 9 になる(目標 10)。名所は観光の魅力を上げる施設なので、attractiveness が上がれば観光客が増えると予想する。ただし、空き地3は街の中心から約2.6km 離れ、今の attractiveness は 0 なので、観光客が来るかは確かめるまで分からない
- 数値と期限: 名所の棟数は、置いたときに 8 → 9(確実)。attractiveness(空き地3の周り)は今 0 で、第7月末に 0 より大きくなるかを見る。観光客は今 1,811、Tourism は週 24。これらは数値を見積もれない
- 確認方法: `buildings_near`(service=Monument、x=668、z=1565、半径 500)で棟数。`map_layer` attractiveness(x=668、z=1565、半径 400、n=5)で、今の基準は平均 0。`city_info` の tourists.now と `economy_breakdown` の Tourism を、今の値(1,811 と 24)と比べる
- 不確かな点: (a) 名所の敷地に通電するかは、置いた後の grid で確かめる(網のつながりは確認済み)。(b) 名所が観光客を呼ぶかどうか。(c) 空き地3の場所は都心から離れ、観光客が寄るかは未確認
- 試し: 試し。仮説: 空き地3の名所が attractiveness を上げ、近くを通る観光客が増え、Tourism が上がる。測る数: `map_layer` attractiveness(x=668、z=1565、半径 400)と、`buildings_near` の名所の棟数。基準: attractiveness 平均 0、名所 8 棟。編成方針の分からないこと「名所と入口で Tourism が増えるか」の項目

### 費用

- 建設費: 25,080(名所 25,000 は `test_place_building` の cost、支線 80 は `test_build_line` の cost)
- 週の維持費の増え分: 402 ほど(名所 400 は `list_building_types` の upkeepPerWeek、支線 約 2 は `list_net_types` の upkeepPerWeekPerKm から計算)。週の収支は +10,614 で、足りる

### 戻せるか

戻せる。名所の取り壊しは議決が要るが、建てる段階では取り消せる(取り壊しを使う場合は議決)。

### 前の月の答え合わせ

なし(前の月の案は、4か月目の RecreationalUse 外しのみで、判定済み)。前の月(4か月目)の計画の予定「空き地3の道の進み具合」は、道路 13359 が既にあると分かった。

### 市の計画

- 当たる施策: 5-1、5-2 観光(名所)
- 編成方針の重点に当たるか: 当たる(重点1 観光。空き地を含む)

## 調査

- 調査: あり
- 問い: 空き地3の送電線が、既存の電気の網につながり、名所の候補地 (668, 1565) に電気が届くか
- 見る道具と引数: (1) `map_layer` type=electricity_service、x=668、z=1565、radius=150、n=5。(2) `net_near` x=690、z=1640、radius=150、service=Electricity、limit=20
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: (a) 電気の点が1のまま(送電線の端 690,1640 が網につながっている)なら、案1を第6月に実行可にする。(b) 0のまま、かつ端が網につながっていないなら、道路下水道局に接続を求め、案1を未確認のまま保留する。(c) 届き方が変わらないなら、名所の場所を電気の届く所へ替えるか、案1を取り下げる
- 担当の問題: 5-1、5-2 観光(名所)

## 見たもの

- `city_info`: 人口約178,380、所持金2,111,160、週の収入 345,801 / 支出 335,187、観光客 1,811(訪問 138)
- `economy_breakdown`: Tourism 週 24、Office 週 24,525、Monument 維持費 週 2,728、PublicTransport 維持費 週 38,238
- `list_policies`: RecreationalUse は有効でない(週 0)。SmallBusiness は有効(週 311)、BigBusiness は有効(週 3,908)、EducationBoost は有効(週 7,940)。有効な政策の合計 週 10,960。観光の効きが確認できた政策はない
- `list_building_types`(service=Monument): StatueOfWealth 建設費 25,000、維持費 週 400、電気だけ要る(水と下水は要らない)。Servicing Services 20,000(12×13)、Transport Tower 60,000(8×12)、Colossal Offices 70,000、Observatory 85,000、Grand Mall 85,000、Library 90,000、ExpoCenter 100,000、High Interest Tower 125,000、Modern Art Museum 130,000、Theater of Wonders 175,000、Stadium 200,000(維持費 週 4,000)、ChirpX 200,000
- `buildings_near`(service=Monument、半径 5000): 名所 8 棟(SeaWorld、Friendly Neighborhood、Countdown Clock、ScienceCenter、Winter Market、Fountain、Plaza of Transference、Official Park)
- `buildings_near`(abandoned=true、半径 4000): 放棄された建物 135 棟。(2136, 629) の 7201 ほか
- `zone_map`(712, 1644、半径 400): 道路が (712,1644) から南へ延びる。道路沿いの空きは灰色の帯
- `net_near`(712, 1644、半径 300、道路): Basic Road の区間 968、13359、29045、15421、24564。送電線の鎖 5220、13350、13409、22108、36842 は端 4380 (690,1640) が connectedTo none
- `height_at`(712, 1644): 地面 45.3、水面 45.3
- `map_layer` electricity_service: (712,1580) 半径150 は 0(5×5点)。(668,1565) 半径150 は 0 で、南西隅 (518,1415) だけ 1。(560,1480) 半径60 は 1 が1点だけ。(440,1340) 半径40 は全部 1
- `map_layer` attractiveness: 全体(x=0、z=0、半径4000、n=9)の平均 2、最大 25。(668,1565) 半径400(n=5)は平均 0、最大は (268,1765) の 5
- `water_trace`(700, 1600): 水 false、下水 false、水の網 []。空き地3に水の網がない
- `services`: 電気の容量 2,507,120 に対し使用 1,709,488。水の容量 2.4M に対し使用 1.92M。ごみと墓地は満杯なし
- `zone_summary`(グリッド 1000): 商業(高密度)の道に面した空き 172、住宅(高密度)の道に面した空き 6、事務所の道に面した空き 0
- `zones_at`: 都心の空きは、道に面した区画が少ない
- `preview_bulldoze`(2150, 630、半径45): 壊す建物 10、失う働き口 55、家 0、道路の区間 8 を含む(道路は壊せないので、案にしない)
- `preview_bulldoze`(2120, 448、半径40): 建物 3(Official Park を含む)、失う働き口 30
- `test_place_building`(名所、都心の候補、空き地3の候補): 都心の候補はすべて ObjectCollision(道路 z=560、z=650、x=2152 や、事務所の高層)。Countdown Clock、Fountain、Official Park は AlreadyExists(市に1棟のみ)。StatueOfWealth (2620,530)、(2512,-432) は ObjectCollision。Transport Tower (2512,-434) は ObjectCollision。StatueOfWealth (686,1600) は道路 968 と 13359 に当たる。StatueOfWealth (668,1565) east は ok=true、cost 25,000、入口 (700,1565) が道路 13359 から距離 4、取り壊し 0
- (再調査で追加)`test_build_line`(Power Line、[[647,1587],[668,1565]]): 2回とも ok、segments 1、cost 80、overlaps []。始点は node 32160
- (再調査で追加)`test_place_building`(StatueOfWealth、668,1565、east): ok、cost 25,000、入口 (700,1565) が道路 13359 から距離 4、取り壊し 0
- (再調査で追加)`test_place_building`(Regular Park、762,1600、west): ok、cost 1,000、入口 (730,1600) が道路 968 から距離 10、取り壊し 0。P3 は未建設
- (再調査で追加)`net_near`(690,1640、r150、Electricity): 送電線 36842(4380→32160)、5220(32160→17930)、13409(17930→24073) を確認。端 4380 は 36842 を通って 32160 につながる
- (再調査で追加)`net_near`(560,1480、r120、Electricity): 5220、13350(21832→12272)、13409、22108(24073→21832) を確認。網は (467,1373) まで続く
- (再調査で追加)`map_layer` electricity_service(668,1565、r60、n=5): 25点とも 0(建物も線もないため)
- (再調査で追加)`buildings_near`(x=668、z=1565、r120、brief): 0 棟。(x=762、z=1600、r80、brief): 0 棟。(x=590、z=1520、r90): 0 棟
- (再調査で追加)`list_building_types`(service=Monument): StatueOfWealth の大きさが 8×8 マス(再確認)
- (再調査で追加)`list_net_types`(service=Electricity、locked=false): Power Line 1km あたり建設費 2,500、維持費 週 60
- (再調査で追加)`citizens_without_service`(type=electricity、limit=5): 住民 0、建物 0。電気が来ない住まいはない
- (再調査で追加)`water_trace`(668, 1565): 水 false、下水 false(名所は水と下水が要らない)

## 判断の根拠

観光は市長の方針で、今月の重点の1つ。Tourism は週 24(目標 1,000)、名所は 8 棟(目標 10)、attractiveness 平均 2 と、どれも目標から遠い。都心の候補は道路と建物に当たり、実行できる場所が確認できたのは空き地3の1か所だけ。その場所は道路があり、建物を置く条件のうち道路と敷地は確認済み。電気は届かず、送電線の端が網につながっていないので、実行は電気の確認後にする。よって案1は、実行可否「未確認」で出し、電気の調査を1件出す。Official Park 系の2棟目は市に1棟だけなので、案にしない。案は1件にとどめ、ほかの候補は捨てたものに書く。

## 捨てたもの

- Official Park 系の名所を2棟目と3棟目に置く(計画の旧案): 市に1棟だけ置ける(AlreadyExists)ので、置けない。計画から外した
- 都心の名所(StatueOfWealth、Transport Tower など): 道路 z=560、z=650、x=2152 と事務所に当たり、ObjectCollision。壊して置く案は、失う働き口が 30〜55 出るので、今月は出さない
- 島Bの StatueOfWealth: 橋と電気が未確認。空き地3の名所と同じ種類なので、空き地3が通れば島Bは別の種類になる。今月は出さない(第8月の予定に残す)
- 品物の手(入口や店の周りの道): 貨物駅28755の敷地内の止まりが主な原因で、道と港の問題。経済の手ではない。入口は港湾空港局の担当で、第6月に他局へ求める
- 政策 RecreationalUse の再有効化: 4か月目に効かなかったので外した。SmallBusiness の効きは分からないが、今月は出さない
