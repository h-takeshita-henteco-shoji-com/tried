# m08 消防局の案

## 案1: 火元の事務所2棟を取り壊し、同じ場所に消防署(Fire House)を置く

### 施策

- 案の id: fire-1
- 施策: 火事の印が続いている事務所2棟(957、27740。中心 (2926, 1470))を取り壊し、同じ場所に Fire House を1棟置く。道具は `bulldoze` と `place_building`
- 議決: 取り壊し

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `test_place_building`(prefab="Fire House", x=2926, z=1470, facing="south", assume_removed_buildings=[957, 27740])。ok と、入口の道路 segment 10025(距離0)を確かめる
  2. `bulldoze`(x=2926, z=1470, radius=30, what="building")。壊す相手は建物 957(H2 4x3 Office09、(2941.5, 1470))と 27740(H2 3x2 Office13、(2910, 1470))の2棟だけ
  3. `test_place_building`(prefab="Fire House", x=2926, z=1470, facing="south")。取り壊し後に wouldDemolish が 0 か確かめる
  4. `place_building`(prefab="Fire House", x=2926, z=1470, facing="south")。建設費 12,000
- 設置条件の確認:
  - 取り壊し: `preview_bulldoze`(x=2926, z=1470, radius=30, what="building")で2棟、働き口0、家0
  - 置く位置: `test_place_building`(assume_removed_buildings=[957, 27740])で ok、wouldDemolish 0、入口 (2926, 1458) の道路は segment 10025(Basic Road、距離0)
  - 電気・水・下水: `buildings_near`(x=2926, z=1470, radius=30)で、2棟とも grid の electricity・water・sewage が true。同じ網に入る
  - 敷地: 半径30mの建物は2棟だけ
  - 道路: `net_near`(Road、x=2926, z=1400, radius=200)で、segment 10025(2926,1450)〜(3001,1450)の Basic Road を確認。新しく道を引く操作はない
- 接続工事: 不要
- 予備候補: なし。放棄された建物は、半径500mでこの2棟だけ(`buildings_near` abandoned=true)。ほかの候補(2822,1425 / 2822,1340 / 3100,1310)は、取り壊しで働き口11〜26を失うため使わない
- 中止する条件: 取り壊しの前の `test_place_building` が通らない、または入口の道路が null。`preview_bulldoze` の対象が957、27740の2棟と違う、または働き口・家の失うものが0を超える。`bulldoze` が timeout を返したら `sim_health` で確かめてから。取り壊し後に置けなければ、空いた場所に置き直す前に、局がもう一度 `test_place_building` で確かめる

### 期待する効果

- 改善の見込み: 火事の印は、事務所2棟が6月末から7月末まで同じ場所で続いている(確認した事実)。その2棟を取り壊すと、この場所の火事の印は消える見込み。置いた消防署は、火元の上に消防車を置き、ここでの火事に早く出られるようにする見込み
- 数値と期限: 火事の印 2(`complaints` の Fire、hotspot (2926, 1470)、2棟)→ 0。期限は8月末の月末。火事と犯罪の合計は 2 → 0〜2。目標の4以下は今も達成
- 確認方法: `complaints`(Fire の件数と hotspot)、`buildings_near`(x=2926, z=1470, radius=100, problem="Fire")の件数、`buildings_near`(x=2926, z=1470, radius=100, service="FireDepartment")の stats(消防車の使用数)。見回り1・見回り2・月末に同じ引数で測る
- 不確かな点: 2棟が2か月燃え続けた原因は道具では分からない(道は空いていて、消防の届きは平均以上)。消防署を置いた後に火事がどれだけ減るかは見積もれない。確かめるのは、火事の印が同じ場所に出続けないこと
- 試し: なし(火元そのものを取り除く直接の手)

### 費用

- 建設費: 12,000(`list_building_types` の Fire House)
- 週の維持費の増え: 560(同じく upkeepPerWeek)。取り壊しで消える2棟の維持費の減りは未確認のため、0として数えない

### 戻せるか

戻せない。取り壊しは元に戻せない。

### 前の月の答え合わせ

前の月(7月)の案はなし(台帳の m07-fire は案なし)。7月の調査ファイル(`council/m07-survey-fire.md`)はない。火事の印は、6月末に3、7月末に2で、同じ 957、27740 が続いた。この続きが、今月の案の根拠。

### 市の計画

- 当たる施策: 3-4 日常生活の安全・安心
- 編成方針の重点に当たるか: 当たらない(重点は 5-1・5-2、8-1、4-4)。3-4 の目標(合計4以下)は今も達成しているが、火元が続いているため、重点の外の案として出す

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口 180,138、所持金 2,174,932、週の収入 342,510、支出 326,155(週の収支 +16,355)、来ない市民 0/0/0、幸福度 88
- `complaints`: 火事2(hotspot (2926, 1470)、2棟 957、27740)、犯罪の印なし、汚染21、ごみ23、品物がない店227
- `events`: 0件
- `list_policies`: SmokeDetectors は inactive、週 57,723(11,274 の fire buildings × 5.12)。SmokingBan は active(週0)、EducationBoost は inactive(週 7,940)。火事に効く安い政策は見当たらない
- `buildings_near`(problem="Fire"、x=2184, z=-918、半径3000): 957、27740 とも Fire, FatalProblem
- `buildings_near`(x=2926, z=1470、半径200): 事務所の棟。火事は957、27740 の2棟だけ
- `buildings_near`(service="FireDepartment"、x=2926, z=1470、半径300): Fire House 26833(2643, 1437)、使用中の消防車 2/8
- `buildings_near`(x=2926, z=1470、半径30): 957、27740 の2棟
- `buildings_near`(abandoned=true、x=2926, z=1400、半径500): 957、27740 の2棟だけ
- `map_layer`(type="fire"、x=2926, z=1470、半径400、n=5): 街の平均 115。hotspot 付近 128。半径120(n=5)では平均 130
- `list_building_types`(service="FireDepartment"): Fire House 12,000 / 週 560、Fire Station 60,000 / 週 1,440
- `services`: 埋立地の満杯0、火葬場の満杯0、警察 980/397
- `net_reach`(x=2926, z=1470、半径300): 道22区間、入れない0、出られない0、建物に道のないものは0
- `traffic`(x=2926, z=1470、半径300): flow 56、cars 5、blocked 0。道は空いている
- `zone_map`(x=2926, z=1400、半径250、size 500): 2棟の周りは事務所の街区。道路(z=1450)の南北に空きはない
- `net_near`(service="Road"、x=2926, z=1400、半径200): segment 10025(2926,1450)〜(3001,1450)の Basic Road など
- `preview_bulldoze`(x=2926, z=1470、半径30、what="building"): 2棟、働き口0、家0、電気を失う建物0
- `test_place_building`(Fire House、2926,1470、south、assume_removed_buildings=[957, 27740]): ok。入口 (2926, 1458) の道路 segment 10025(距離0)。wouldDemolish 0。費用 12,000、足りる
- `test_place_building`(Fire House、2926,1470、north、assume_removed_buildings=[957, 27740]): 入口の道路が null のため不可
- `test_place_building`(Fire House、2822,1425、east): 取り壊し2棟(働き口11)。予備にしない
- `test_place_building`(Fire House、2822,1340、east): 取り壊し2棟(働き口11)。予備にしない
- `test_place_building`(Fire House、3100,1310、south): 取り壊し2棟(働き口26)、入口の道路 null。予備にしない

## 判断の根拠

- 火事の印は、6月末(3)から7月末(2)まで同じ2棟(957、27740)で続いた。計画の条件(2か月続く)に当たったので、火元の側の手を案にした
- 2棟は今も Fire, FatalProblem のまま。取り壊しで失う働き口・家は0で、放棄された建物として、半径500mにこの2棟だけ
- 原因(消防車が届かないのか、燃え続けるのか)は道具では確かめられない。ただ、取り壊しは原因によらず火元を消す。直接の手として取り壊しを選んだ
- 置き場所は同じ場所にした。火元の上に消防署を置くと、同じ手で届きも足せる。別の場所は、働き口11〜26を失うため使わない
- 案は1件にした。件数を埋めるための案は作らない。調査も出さない。火元は見えていて、取り壊しで止められる
- 地形の資料は、火元の判断に使わないため読まない

## 捨てたもの

- 別の場所に消防署を置く案(2822,1425 / 2822,1340 / 3100,1310): 取り壊しで働き口11〜26を失う。火元の取り壊しで足りるため、出さない
- 政策 SmokeDetectors: 週 57,723。守る線(週の収支 +3,000)の余裕を大きく超えるため、出さない
- Fire Station(建設費 60,000、週 1,440): 火元の上の Fire House より高く、火事を止める根拠がないため出さない
- 消防の予算を上げる: 消防の予算はすでに140で、火元が燃え続ける原因が予算とは確かめられていない。出さない
