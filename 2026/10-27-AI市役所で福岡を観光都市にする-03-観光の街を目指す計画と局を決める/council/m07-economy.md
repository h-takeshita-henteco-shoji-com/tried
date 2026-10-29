# m07 経済観光文化局の案

## 案1: 電気の来ない名所 11580(空き地3)を取り壊す

### 施策

- 案の id: economy-1
- 施策: 空き地3(668,1565)の StatueOfWealth 11580 を取り壊す。電気が来ないまま、2か月たった(取り下げ条件を満たした)
- 議決: 取り壊し

### 実行計画

- 実行可否: 未確認
- 対象と操作順: `bulldoze`(対象は建物 11580 の1棟だけ。区間と送電線は含まない。円の中心 (668,1565)、半径 30)。ただし、取り壊しの目的(島Bでの置き直し)が確かめられていないため、実行は保留する
- 設置条件の確認: `preview_bulldoze`(x 668, z 1565, radius 30)。対象は11580の1棟、失う働き口0・家0、電気が切れる建物0、水の施設0、港・駅0。`buildings_near`(x 668, z 1565, radius 40)で対象が11580だけと確認。取り壊し自体の条件は確認済み。置き直し先の条件は未確認(下の再調査の結果)
- 接続工事: 不要
- 予備候補: なし(取り壊しだけの案)
- 中止する条件: 取り壊し前に、11580 が電気を得ている(grid.electricity が 1)か、円の中に別の建物が増えていたら見送る。島Bに同じ種類を置けないと確かめられたら、取り壊さない
- 再調査の結果:
  - 条件1(島Bの (-4640,1520) で、11580 を壊さずに置ける別の種類の名所を ok で示す): 満たせなかった。
    - (-4640,1520) は、`test_place_building` で SeaWorld、Countdown Clock、Friendly Neighborhood、StatueOfWealth、Servicing Services を、東・西・南・北の向きで試した。どれも ObjectCollision で断られ、道路 13902、14667、34550 と重なる。
    - 別の場所 (-4640,1585)(南向き)の Observatory は ok(入口の道 13902 まで 1m)。ただし Observatory は電気・水・下水が要る。島Bには水の網がなく、`water_trace` の networkCount は 0、`net_near`(Water、半径 400m)は 0 件。水を引けるかは未確認。
    - 名所は、街に1種類につき1棟しか置けないと見られる(9棟が9種類)。島Bの StatueOfWealth は、取り壊しを仮定しても `test_place_building` が AlreadyExists を返す。取り壊し後に置けるかは、道具では確かめられない。
    - 電気だけを要る名所は StatueOfWealth だけで、ほかの名所は水と下水も要る。
  - 条件2(壊す案を残すなら、壊さずに 11580 へ届く支線を `test_build_line` で試した結果と、維持費の差を比べる): 支線の端を敷地の外に置く線は ok(`test_build_line`、Power Line、(690,1640)→(700,1610)、費用 80)。ただし、端を 11580 の敷地の中に入れる線(例: (690,1640)→(690,1590)、(727,1626)→(668,1572))は、ObjectCollision で断られる(blocks=true の 11580)。電気が 11580 に届く線は、確かめられていない。
    - 維持費の差: 取り壊すと週 400 減る(StatueOfWealth の upkeepPerWeek 400)。残すと、週 400 払い続ける。
    - 得るものと失うもの: 取り壊すと週 400 が減るが、名所が 9 → 8 になる。残すと名所は 9 のままだが、11580 は電気なしで観光客を呼ばない。どちらも、島Bで置き直せるかが確かめられていない。
  - 判定: 条件1と条件2は満たせなかった。実行可否は「未確認」にする。取り壊しは、島Bへの置き直しが道具で確かめられるまで実行しない。

### 期待する効果

- 改善の見込み: 電気が来ない名所は観光客を呼べず、維持費だけを払っている。取り壊すと、その分の維持費が減り、同じ種類(StatueOfWealth)を島Bで試せるようになる見込み。ただし、置き直しは道具で確かめられておらず、この見込みは未確認
- 数値と期限: 週の維持費 -400(前月の list_building_types の値。今月 `list_building_types`(service=Monument)で 400 を再確認した)。名所の棟数 9 → 8(置き直しが通れば 9 に戻す見込み。未確認のため、戻る保証はない)。期限は8月末
- 確認方法: `buildings_near`(service=Monument)の棟数、`economy_breakdown` の Monument の週の支出、`buildings_near`(x 668, z 1565, radius 40)で11580が消えたこと
- 不確かな点: 名所の数は一時的に 8 に下がる。島Bの置き直しは `test_place_building` で確かめられていない(AlreadyExists)。島Bの水の網も、取り壊しの前に確かめる必要がある。維持費の減りは、建物の維持費の表の値を取り直して確かめる
- 試し: なし

### 費用

- 建設費: 0(取り壊しの費用は道具の表示なし。未確認)
- 週の維持費の増え分: -400(減る)

### 戻せるか

戻せない。取り壊した建物は、同じ場所に同じ種類を建て直すしかない。建て直すには、島Bと同じく名所の種類の空きが要る。

### 前の月の答え合わせ

前の月(6月)の案は、空き地3に StatueOfWealth を置いて電気を通すものだった。採られて置けたが、6月10日と6月30日の調査で、11580 の grid.electricity は 0 のままだった(`buildings_near` の problems: Electricity, MajorProblem)。送電線の支線は test_build_line で通ったが、名所の電気には届いていない。外れ。原因は確かめられていない(m06-survey-economy の s06-2)。今月の再調査で、敷地の中へ端を入れる線が断られたことが分かった。電気が届かない原因の一部は、この敷地の接続の仕方にある可能性がある(確かめていない)。

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる(重点1 の名所)

## 調査

- 調査: なし
- 問い: —
- 見る道具と引数: —
- いつ見るか: —
- 何が分かれば次の手が決まるか: —
- 担当の問題: —

## 見たもの

- `city_info`: 観光客 1,665、訪問 141。所持金 2,101,000、週の収入 346,067、週の支出 335,578(収支 +10,489)。date 2050-06-30
- `list_building_types`(service=Monument): 名所 21 種類の解禁状況と費用。StatueOfWealth は 25,000、維持費 400、電気だけが要る(水と下水は不要)。ほかの名所は電気・水・下水が要る
- `buildings_near`(service=Monument, x 0, z 0, radius 9000, brief): 名所 9 棟。SeaWorld、Friendly Neighborhood、Countdown Clock、StatueOfWealth 11580(電気なし)、ScienceCenter、Winter Market 01、Fountain of LifeDeath、Plaza of Transference、Official Park
- `buildings_near`(x -4640, z 1520, radius 120, brief): 島Bの風力発電 44460 の1棟だけ
- `buildings_near`(x 668, z 1565, radius 150): 11580(electricity 0、ports なし)と、公園 30466(電気なし)
- `net_near`(x -4700, z 1600, radius 200, service=Road): 島Bの道路 7 区間。(-4640,1552) の 13902 が島の中の道。島の道は、(-4500,1700) から (-4600,1450) までつながる
- `net_near`(x -4600, z 1550, radius 400, service=Water): 0 件(島Bに水の網がない)
- `net_near`(x -4600, z 1550, radius 400, service=Electricity): 送電線 22680 の1区間だけ((-4655,1466)〜(-4650,1500))
- `net_near`(x 668, z 1565, radius 250, service=Electricity): 送電線 5 区間。最も近い節点は 4380(690,1640)と 17161(727,1626)
- `zone_map`(x -4700, z 1650, radius 300, size 500): 島Bの道沿いの空きは、(-4640,1550) 付近の東側に限られる
- `test_place_building`(SeaWorld、(-4640,1520)、south): ObjectCollision、AlreadyExists。道路 13902、14667、34550、送電線 22680
- `test_place_building`(Countdown Clock、(-4640,1520)、south): ObjectCollision、AlreadyExists
- `test_place_building`(Friendly Neighborhood、(-4640,1520)、south): ObjectCollision、AlreadyExists
- `test_place_building`(StatueOfWealth、(-4640,1520)、south): ObjectCollision、AlreadyExists
- `test_place_building`(Servicing Services、(-4640,1520)、west / north / south): ObjectCollision(いずれも道路 13902、14667 または 34550 と重なる)
- `test_place_building`(SeaWorld、(-4700,1700)、east): AlreadyExists(空き地でも、同じ種類は置けない)
- `test_place_building`(StatueOfWealth、(-4700,1700)、east): AlreadyExists
- `test_place_building`(StatueOfWealth、(-4640,1520)、west、assume_removed_buildings=[11580]): AlreadyExists(取り壊しを仮定しても同じ)
- `test_place_building`(Servicing Services、(-4700,1650)、east): ok(位置は通る)。入口の道なし(road null)、電気・水・下水が要る。20,000
- `test_place_building`(Servicing Services、(-4680,1565)、south): ObjectCollision(道路 13902)
- `test_place_building`(Transport Tower、(-4680,1565)、south): ok(位置は通る)。入口の道なし、電気・水・下水が要る。60,000
- `test_place_building`(Observatory、(-4700,1600)、south): ok(位置は通る)。入口の道なし、電気・水・下水が要る。85,000
- `test_place_building`(Observatory、(-4640,1585)、south): ok。入口の道 13902 まで 1m。電気・水・下水が要る。85,000
- `test_place_building`(Transport Tower、(-4640,1580)、south): ObjectCollision(道路 13902)
- `test_place_building`(Servicing Services、(-4640,1585)、south): ObjectCollision(道路 13902)
- `water_trace`(x -4640, z 1585): 水・下水の網なし(networks 0)。市全体の水は容量 2,520,000 / 使用 1,923,808、下水は 2,400,000 / 1,921,888
- `net_reach`(x -4640, z 1585, radius 300): 道路 10 区間、来られない・出られない区間 0。島の道は街とつながっている
- `test_build_line`(Power Line、[[690,1640],[668,1572]]): ObjectCollision(11580 の敷地)
- `test_build_line`(Power Line、[[727,1626],[668,1572]]): ObjectCollision(11580、公園 30466)
- `test_build_line`(Power Line、[[690,1640],[690,1590]]): ObjectCollision(11580。敷地の中へ端を入れられない)
- `test_build_line`(Power Line、[[690,1640],[700,1610]]): ok。費用 80、交差なし
- `preview_bulldoze`(前の月の確認): 建物1(11580)、失う働き口0・家0、電気が切れる建物0
- `list_policies`(前の調べ): SmokingBan 有効、policyExpenses 10,600/週(m07 の見たもの)。今月は見直していない

## 判断の根拠

- 再調査の条件1 は、島Bで 11580 を壊さずに名所を置けるかだった。(-4640,1520) は道路と重なり、どの種類も置けない。島Bの別の場所の Observatory は ok だが、水と下水の網が島にないため、実行できない。Servicing Services と Transport Tower は入口の道がなく、道を引く案は今月の範囲外。条件1 は満たせなかった。
- 再調査の条件2 は、残す場合の支線と維持費の比べ。支線は敷地の外までは通るが、敷地の中へは断られた。電気が届く線は確かめられていない。維持費の差は週 400 で、収支の +10,489 に対して小さい。
- 取り壊しの効きは、週 400 の減りと、名所 1 棟の減り(9 → 8)だけで、観光客の増えは確かめられていない。島Bの置き直しが道具で確かめられない以上、取り壊しは採る根拠がなく、実行可否は「未確認」にする。市長が採っても、島Bの確かめを先にする条件を守る。
- 案は1件だけにする。島Bの Observatory は水の網がなく、今回の条件の外で、今月の案にしない。

## 捨てたもの

- economy-1 の「島B で (-4640,1520) に別の名所を置く」: 道路と重なり、どの種類も断られる。ほかの位置を探すことは、条件の外のため今月はしない
- 島Bの Observatory(-4640,1585、南向き): ok だが、水と下水の網が島にない。水の管を海の向こうへ引く案は、道具で確かめられていない。次の月に出すなら、水の網の接続を先に確かめる
- 島Bの Servicing Services(-4700,1650)、Transport Tower(-4680,1565): ok だが、入口の道がなく、道を引く案は条件の外
- 残す案(11580 に電気を通す支線): 敷地の中へ端を入れる線が断られ、電気が届くかは確かめられていない
- 名所の種類の同一の重なり(StatueOfWealth の島B 置き直し): AlreadyExists が取り壊しを仮定しても出るため、道具では確かめられない
