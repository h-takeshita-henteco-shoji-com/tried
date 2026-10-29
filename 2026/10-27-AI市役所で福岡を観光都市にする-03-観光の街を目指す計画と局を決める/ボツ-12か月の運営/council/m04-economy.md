# m04 経済観光文化局の案

## 案1: 北の道路沿いに名所 StatueOfWealth を1棟置く(試し)

### 施策

- 案の id: economy-1
- 施策: 名所(Monument)の StatueOfWealth を (-288, 1350) に、入口を西(道路 Small 4 Lane Road に面す)に向けて1棟置く。電気は送電線 Power Line を (-232, 1515)→(-255, 1420)→(-288, 1352) に引いて通す。5-1、5-2 観光の名所を6棟から7棟に増やす
- 議決: 要らない

### 実行計画

- 実行可否: 未確認(電気の網が発電所につながるかが未確認。下の設置条件の確認を参照)
- 対象と操作順:
  1. `place_building`(prefab "StatueOfWealth", x -288, z 1350, facing "west", pay true)。建設費 25,000、維持費 400/週。`test_place_building` は ok、入口の道路 Small 4 Lane Road まで 10.5m、取り壊し 0
  2. `build_line`(prefab "Power Line", points [[-232, 1515], [-255, 1420], [-288, 1352]], pay true)。建設費 440、維持費は約 11/週。`test_build_line` は ok、区間 3、重なり 0、gameCheck は水の指摘なし。端 (-288, 1352) は建物の敷地の中(中心から 2m)で、送電線の端が敷地に入れば電気が通る
- 設置条件の確認:
  - 敷地と道路: `test_place_building` で ok。取り壊し 0。入口の道路あり
  - 水・下水: StatueOfWealth は needs の water、sewage が false。接続工事は不要
  - 電気: 近くの送電線の節点 (-232, 1515) は、`net_near` で既存の送電線の網(区間 25609、27677)につながる。ただし `map_layer` electricity_service の (-225, 1525) は 0 で、この網が発電所から電気を受けているかは確認できなかった。発電所との経路は未確認
  - 置く前の確認で、電気が届く網かを判定する道具はない。置いた後に `buildings_near`(x -288, z 1350)の grid.electricity を見るしかない
- 接続工事: 送電線 1 本(上の build_line)。費用 440、維持費約 11/週。水道管・下水管は不要
- 予備候補: なし(北の道路沿いで、電気の経路を確かめた場所はこの 1 か所だけ)。ほかの候補は「捨てたもの」を見る
- 中止する条件:
  - `test_place_building` が ok を返さない(ぶつかる相手が増えた、入口の道路が消えた)なら見送る
  - `place_building` 後、`buildings_near`(x -288, z 1350, radius 30)の grid.electricity が false のままなら、送電線の経路を外れた原因を調べるまで追加の送電線を引かない。送電線の経路を引き直す案は出し直す
  - 予算が建設費 25,440 に足りないなら見送る

### 期待する効果

- 改善の見込み: 名所の棟数が6から7に増える。名所は目標10に届かせる手の一つ。さらに、名所の周りの魅力度が上がれば、観光客が増える見込み。ただし、この場所の魅力度は低い(下の数値を参照)。効く量は見積もれない
- 数値と期限:
  - 名所の棟数(`buildings_near` service=Monument): 6 → 7。置いて電気が通れば、期限は次の月例(1か月後)。目標 10
  - 置く場所の魅力度(`map_layer` attractiveness、x -288 z 1350、radius 150、n 5)の平均: 基準 3(最大 25、最小 0)。月末で測り直す
  - 観光客(`city_info` tourists): 基準 1,625 / 訪問 161。目標 3,000 / 250 は遠い。月末と次の月例で測る
- 確認方法: 上の道具を、同じ引数で、基準の値と比べる。観光客は街全体の数なので、置いた場所の魅力度の変化と一緒に読む
- 不確かな点: 送電線が発電所の網につながるかが未確認。場所は北の端で、中心の魅力度が高い場所から遠い。名所の周りの魅力度が上がっても、観光客は増えないかもしれない(前の月の広場 1 棟は、周りの魅力度 36→40 で、観光客は増えなかった)
- 試し: 効き目が分からないため試しとして出す。仮説: 名所を置くと、その周りの魅力度が上がり、観光客が増える。測る数: `map_layer` attractiveness(x -288, z 1350、radius 150、n 5)の平均。基準は 3。判定は月末と次の月例。もう一つの数は名所の棟数(6→7)。前の月の答えの扱い: 広場 1 棟で観光客が増えなかったため、観光客の増えを見るのは、魅力度の平均が上がった後にする

### 費用

- 建設費: 25,440(StatueOfWealth 25,000 + Power Line 440)。上限 200,000 の内
- 週の維持費の増え分: 約 411(StatueOfWealth 400 + Power Line 約 11)。上限 5,000 の内

### 戻せるか

戻せる。建物と送電線は、取り壊し(bulldoze、remove_line)で消せる。ただし、取り壊しは議決が要る。建設費は払い戻されない。

### 前の月の答え合わせ

なし(3か月目の経済観光文化局は案なし)。前の月の調査 s03-2(品物がない店)は、観光ではなく 6-4、7-1 の数字なので、今月の案とは別に扱う。品物がない店は 222 → 224 → 228 と動かなかった。

### 市の計画

- 当たる施策: 5-1、5-2 観光(名所の棟数、観光客、魅力度)
- 編成方針の重点に当たるか: 当たる(重点 1: 5-1、5-2 観光)

## 調査

- 調査: あり
- 問い: 観光客の人数は、見回りごとにどれだけ動くか。政策も建設もしていない今の幅を、基準にする。
- 見る道具と引数: `city_info`(引数なし)の tourists.now と visits。`economy_breakdown`(引数なし)の Tourism の週の収入
- いつ見るか: 見回り1 / 見回り2 / 月末
- 何が分かれば次の手が決まるか: 見回りごとの動きが ±100 以内なら、観光客の数はノイズが大きいと見て、次の月は魅力度の平均(map_layer)を主に測る。±100 を超えて動くなら、動いた時期に起きたことを調べる(名所の周りの魅力度・政策・人口)
- 担当の問題: 5-1、5-2 観光

## 見たもの

- `list_policies`: 有効は SmokingBan(0)、EducationBoost(7,940/週、学校の維持費の 25% 増し。教育費に入る)、RecreationalUse(0)、BigBusiness(3,952/週)。ほかは無効。担当の観光に関係する政策は RecreationalUse(有効、費用 0)のみ。前の月に外れたので、政策の変更は今月しない。政策の週の費用の合計は 10,727
- `list_building_types`(service=Monument、解禁済み): SeaWorld 20,000(320/週)、ScienceCenter 20,000(320/週)、Servicing Services 20,000(320/週)、Friendly Neighborhood 20,000(320/週、8×7)、Fountain of LifeDeath 30,000(240/週、7×7)、Countdown Clock 37,500(80/週、12×12)、Official Park 45,000(128/週、6×6)、StatueOfWealth 25,000(400/週、8×8、電気だけ要る)、ほかは 40,000 以上
- `city_info`: 人口 180,759、所持金 2,145,261、観光客 1,625 / 161、週の収入 346,977・支出 336,944、需要 25 / 2 / 57、電気・水・下水が来ない市民 0 / 0 / 0
- `buildings_near`(x 0、z 0、radius 5000、service=Monument): 名所 6 棟(SeaWorld -1350,-796、Countdown Clock 1765,622、ScienceCenter -1130,-804、Winter Market 01 -1550,-205、Fountain of LifeDeath 1804,170、Plaza of Transference -1560,-855)
- `buildings_near`(x 2600、z 800、radius 300、service=Monument): 0 棟
- `map_layer`(attractiveness、x 0、z 0、radius 2000、n 9): 平均 2、最大 117(0, -1500 付近)、最小 0。街の平均は 5(前の月の値)
- `map_layer`(attractiveness、x -288、z 1350、radius 150、n 5): 平均 3、最大 25(-213, 1200)、最小 0。案の場所の基準
- `map_layer`(electricity_service、x -200、z 1450、radius 150、n 5): 1 は北の端(z 1600)だけ。(-225, 1525)は 0
- `zone_map`(x 0、z 0、radius 2000、size 700)、(x -200、z 1100、radius 500)、(x 1000、z 300)、(x 0、z -1300)、(x 650、z -250)、(x -1100、z -450)、(x 300、z 50)、(x 500、z -350): 空きのある場所と道路の位置を見た
- `list_districts`: 地区は HighTech(481, -323)と Hakata(299, 49)の 2 つ。北の道路沿いは地区に入っていない
- `test_place_building`: StatueOfWealth (-288,1350) west は ok(採用)。StatueOfWealth (-300,1350) west は道路 Small 4 Lane Road とぶつかった。Friendly Neighborhood (-300,1350) west は ok だが水の網が遠く(最も近い水道管 155m)採らない。Official Park (-262,930) west は ok(入口の道路 12.6m)だが、水の網が 200m 以内にない。Official Park (-230,930) east は入口の道路なし。Friendly Neighborhood (-1187,-281) north は High School とぶつかった。Fountain of LifeDeath (-1370,-105) east は Elementary School とぶつかった。SeaWorld (785,-120) west と Countdown Clock (785,-310) west は Expensive Park とぶつかった。Countdown Clock (700,-620) west は道路と Crematory、Landfill とぶつかった。Friendly Neighborhood (192,-104) north は Fire Station とぶつかった。Official Park (400,235) south は Hospital と水域。Friendly Neighborhood (390,-232) south と (590,-232) south は Regular Park とぶつかった。Friendly Neighborhood (-250,1200) west は斜面が急すぎる
- `test_build_line`(Power Line): [[-295,1500],[-288,1350]] は gameCheck に CannotBuildOnWater。[[-358,1485],[-320,1420],[-288,1350]] は道路 Small 4 Lane Road とぶつかって断られた。[[-232,1515],[-255,1420],[-288,1352]] は ok(採用、cost 440、重なり 0)
- `list_net_types`(Electricity、locked=false): Power Line 2,500/km、維持費 60/km/週
- `net_near`(Electricity、(-250,1330)、r260): 送電線の節点 (-232,1515)、(-295,1500)、(-170,1530)、(-170,1605) など。(-232,1515) は既存の網の一部
- `net_near`(Water、(-300,1350)、r160): 水道管は (-358,1495)、(-420,1480)、(-445,1415)、(-470,1350) の付近。最も近い水道管 155m
- `net_near`(Water、(-262,930)、r200): 水道管なし
- `water_trace`(-300,1350): 水・下水が届かない。近くの網に取水口(給水塔)はあるが、この網と案の場所は離れている
- `water_trace`(-262,930): 水・下水の網なし
- `buildings_near`(Monument)の街全体の確認: 名所 6 棟(上)
- 写真や画面の道具(`events`、`citizen_voices`、`citizens_summary`)は呼んでいない

## 判断の根拠

- 観光の数字は、名所 6 棟(目標 10)、観光客 1,625(前の月 1,722、目標 3,000)、Tourism 86(目標 1,000)。名所の棟数を増やす手は、前の月の広場 1 棟より効きが大きいと見込まれる。ただし効く量は見積もれない
- 名所を増やせる場所は、5 つの地区・候補地(西の住宅地、東の商業、Hakata、HighTech、北の道路沿い)で試した。多くは既存の建物や公園とぶつかった。建設費 20,000 台の名所は、水と下水の網が要るものが多く、網が近い場所は北の 1 か所しかなかった
- 北の道路沿いの (-288, 1350) は、道路・建設条件は確認できた。電気は送電線 1 本で網に入れられると見込むが、その網が発電所から電気を受けているかは未確認
- 案は 1 件だけにした。ほかの候補(Official Park、Friendly Neighborhood)は水の網が確認できず、必須条件を満たさない。件数を埋めるための案は出さない
- 政策は RecreationalUse が前の月に効かなかったため、変えない。調査は観光客の動きの幅を決めるため 1 件出す
- 観光客の増えが名所の効きかどうかを切り分ける手は、今の数では確かめられない。試しとして魅力度の平均を測る

## 捨てたもの

- Official Park (-262, 930) facing west: `test_place_building` は ok(入口の道路 12.6m、取り壊し 0)だが、`water_trace` と `net_near` で水の網が 200m 以内にない。水道管を数百 m 引く工事になり、上限の判断に収まらない。見送る
- Friendly Neighborhood (-300, 1350) facing west: 試しは ok だが、水道管まで 155m。水の接続工事の口(つなぎ口)の位置は、置いた後にしか分からない。置いてから確かめる案は採らない
- Official Park (-230, 930) facing east: 入口の道路がない(road null)。道路を引く工事が要る
- Friendly Neighborhood (-1187, -281)、Fountain of LifeDeath (-1370, -105): 既存の高校・小学校とぶつかる
- SeaWorld (785, -120)、Countdown Clock (785, -310): 公園(Expensive Park)とぶつかる
- Countdown Clock (700, -620): 道路・墓地・埋立地とぶつかる
- Friendly Neighborhood (192, -104)、Official Park (400, 235): 消防署・病院とぶつかる、または水域
- Friendly Neighborhood (390, -232)、(590, -232): 公園とぶつかる
- StatueOfWealth (-300, 1350): 道路とぶつかる。(-288, 1350) に寄せて採用
- 放棄された建物を壊して名所を置く案: 取り壊しは議決が要る。今月は確認できた空きの候補がなく、放棄建物の候補まで調べる時間がなかった。来月の候補にする
- RecreationalUse の入れ替え、ほかの観光の政策: 有効な観光の政策は RecreationalUse のみで、前の月に効かなかった。新しい政策の候補は一覧にない
- 観光の商業への投資(観光客が使う店の近く): 商業の空きの候補を確かめる時間がなく、確認済みの候補がない
