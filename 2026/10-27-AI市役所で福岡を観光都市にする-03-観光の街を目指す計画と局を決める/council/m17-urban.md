# m17 住宅都市みどり局の案

## 案1: 道に面した空き地(1820,300)に公園 JapaneseGarden を1つ置く

### 施策

- 案の id: urban-1
- 施策: 4-2 の公園(Beautification)を1つ増やし、計画の第17月の予定(1つ)に沿って、公園の数を 91 から 92 にする。場所は (1820,300)、道 29165(Basic Road、z=330)の南側。向きは north(入口を道に向ける)。道具は place_building
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. `place_building`(prefab=JapaneseGarden、x=1820、z=300、facing=north、pay は既定の true)。建設費 2,500、週の維持費 40
  2. 置いた後、`buildings_near`(x=1820、z=300、radius=20)で、新しい棟の id と problems(電気・水が来ているか)を確かめる
  - 道は引かない。入口は既存の道路 29165 に、置いた時点で距離 6 で面する
- 設置条件の確認:
  - `test_place_building`(JapaneseGarden、1820、300、facing=north): ok=true、placed=false、angleUsed=0、cost 2,500、enoughMoney=true。入口 (1820,316) north、道 29165(距離 6)。wouldDemolish 0、lostByDemolish 働き口 0・家 0。
  - `net_near`(1820、300、r60、Road): 道 29165(1825,330)〜(1770,330)、23279(1880,330)〜(1825,330)、4414(1770,330)〜(1770,253)。
  - `zones_at`(1820、300、r40): Unzoned 48(空き 32)、CommercialHigh 3(空き 0)。
  - `buildings_near`(1820、300、r40、brief): 近くの建物は 39519 JapaneseGarden(1856,306)のみ。test が ok のため、敷地の重なりは無し。
  - 電気・水: 近くの 39519(1856,306)と 46572 JapaneseGarden(1820,355)の problems が None。`water_trace`(1856,306)の grid は電気・水・下水が届き、水の網は1つにつながる。
- 接続工事: 不要(道 29165 が既にある)
- 予備候補(いずれも `test_place_building` で ok=true を確認。使う順):
  1. (1856,356) JapaneseGarden、facing=south。入口 (1856,340)、道 23279(距離 2)。働き口・家を失わない
  2. (1745,316) JapaneseGarden、facing=east。入口 (1761,316)、道 4414(距離 1)。働き口・家を失わない
- 中止する条件:
  - 実行時の `test_place_building` が ok=false になったら、予備候補 1 → 2 の順に置く。全部だめなら見送る
  - 置いた後の `buildings_near` で、電気か水が来ない(problems に出る)なら、その旨を報告し、次の月に電気・水の確認を先にする(公園は置いたままにする)
  - 置く前に公園の数が 91 から変わっていたら、第17月末の見込み(92)を合わせ直す

### 期待する効果

- 改善の見込み: 4-2 の公園などの数を、計画どおり1つ増やす。建設の時点で Beautification の数は 1 増える。公園は 4-2 の目標(100)に向けた月1件の手で、計画の第17月の予定にあたる。
- 数値と期限: 公園の数 91(前の月の方針の値)→ 92(第17月末)。目標は第24月末に 100 以上。
- 確認方法: `buildings_near`(brief=true、公園の数を街全体で数える)と、置いた棟の problems。今の値 91 と同じ数え方で比べる。
- 不確かな点: 公園の効きで地価が上がるかは、局の事業2(第20月の `land_value` 測定。基準は 2168,194 r200 の平均 66)で見る。今月の効果は数の増えだけで、地価の変化は見積もらない(数値は見積もれない)。
- 試し: なし

### 費用

- 建設費: 2,500(`list_building_types` の JapaneseGarden。`test_place_building` の cost と一致)
- 週の維持費の増え分: 40(`upkeepPerWeek`)。週の収支 +7,468(今月)から 40 を引いても、守る線 +3,000 の上

### 戻せるか

戻せる。ただし建設費は戻らず、取り壊しには議決が要る。取り壊しが必要になったら、議会に別の案として出す。

### 前の月の答え合わせ

- 前の月の案 urban-1(m16-1、道に面した空き地 (1820,355) に JapaneseGarden)は採られ、実行 ok(建設費 2,500)。期限は第16月末。期待は公園の数の1増加。
- 判定: 当たり。`buildings_near`(1820、330、r250、brief)で、46572 JapaneseGarden(1820,355)が建っていることを確認。公園の数は、前の月の方針の値で 90 から 91 へ増えた。事業2の基準の地価(`land_value`、2168,194、r200)は、今月の測りでも平均 66 で、基準から動いていない。

### 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たらない(重点は 5-1、5-2、8-1、6-4、4-4。4-2 は計画の事業1として、今月も予定どおり1つ進める)

## 調査

- 調査: なし

## 見たもの

- `city_info`: 人口 175,864、所持金 2,502,262、週の収支 +7,468(収入 333,111、支出 325,643)、観光客 1,875(訪問 158)、需要 住 26/商 2/工 45、来ない市民 0/0/0、dialog なし
- `list_policies`: 有効は SmokingBan(0)、EducationBoost(週 7,940、学校の維持費の25%)、FreeTransport(0、運賃収入 0)、BigBusiness(3,888)。無効は PowerSaving、WaterSaving、SmokeDetectors、Recycling(0)、RecreationalUse(0)、HighTechHousing(20,272)、IndustrySpace(4,761)、SmallBusiness(311)ほか税の政策(0)。公園・緑に直接効く政策は一覧にない。政策の変更は案に含めない
- `demand_breakdown`: 働き口 86,773(空き 3,190)、住宅 56,132(空き 5,640)、失業 4,989(大卒 4,815)、homeless 0
- `buildings_near`(1820、330、r250、brief): 総数 60(先頭30件)。公園 JapaneseGarden 1940,126、1856,183 ほか
- `zone_map`(1820、250、r300、size600): 道 29165、23279 の南北に空きの区画がある。(1820,300) の敷地は空き
- `land_value`(2168、194、r200): 平均 66、min 37、max 79、cityAverage 53(事業2の基準の確認)
- `net_near`(1820、300、r60、Road): 道 29165、23279、4414(上記)
- `zones_at`(1820、300、r40): Unzoned 48(空き 32)、CommercialHigh 3(空き 0)
- `test_place_building`(JapaneseGarden、1820、300、facing=north): ok=true、cost 2,500、入口は道 29165(距離 6)、壊す建物 0
- `buildings_near`(1820、300、r40、brief): 39519 JapaneseGarden(1856,306)のみ
- `water_trace`(1820、300): 近くの 39519 の grid は電気・水・下水が届く。水の網は1つ。city の水 容量 2,400,000 / 使用 1,904,208
- `zone_summary`(grid 1000): 道路に面した空きは CommercialHigh 36 のみ(多くは奥の空き)。候補は zone_map と test_place_building で道路沿いを確かめた
- `list_districts`: HighTech(126)、Hakata(127)。地区ごとに政策がかかっている(公園の候補地には影響しない)
- `list_building_types`(Beautification): JapaneseGarden 4×4、建設費 2,500、維持費 40、電気・水が要る。ほかに Regular Park 9×8(1,000 / 8)、Regular Plaza 5×5(2,500 / 32)など
- `test_place_building`(JapaneseGarden、1856、356、facing=south): ok=true、cost 2,500、入口 (1856,340)、道 23279(距離 2)、壊す建物 0
- `net_near`(2080、250、r80、Road): 道 2110 の線(Small 4 Lane)など。候補 (2160,232) は道が見つからず、高密度の家 2 棟(失う家 6)を壊すため捨てた
- `test_place_building`(JapaneseGarden、1745、316、facing=east): ok=true、cost 2,500、入口 (1761,316)、道 4414(距離 1)、壊す建物 0
- `test_place_building`(JapaneseGarden、1745、290、facing=east): ok=false(ObjectCollision、Cemetery 44681 が重なる)
- `buildings_near`(1745、290、r60、brief): Cemetery 44681 (1732,250) のみ

## 判断の根拠

- 4-2 は、計画の事業1(第17月は公園を1つ置く)の予定どおり。前の月(第16月)の公園が建って公園の数が 90 から 91 へ増えたので、計画の前提は今月も合う。計画は直さない。
- 公園は JapaneseGarden(2,500、維持費 40)を、計画どおり使う。候補の (1820,300) は `test_place_building` が ok で、入口の道 29165 に距離 6 で面し、働き口・家を失わない。電気・水は近くの 39519 と 46572 の grid が満たしている。
- 予備の (1856,356) と (1745,316) も `test_place_building` で ok。別の道(23279、4414)に面し、場所は (1820,300) から 60m 以上離れている。
- 案は1件だけ。4-2 の手は公園を置くことで、1件の案に別の手を足すと件数を埋めることになるため、2件目は出さない。
- 政策は、担当の数字(公園の数、地価)に効く政策が一覧にない。RecreationalUse は効果の記述がなく、担当の数字への効きを確かめられないので、今月は見送る。

## 捨てたもの

- 2件目の公園(同じ手の増やし): 計画は月1件。件数を埋めるための案にしない。
- Regular Park(9×8、1,000 / 維持費 8): 維持費は安いが、道に面した空きで 72×64m を確保できるかを未確認。今月の (1820,300) の候補では、隣の 39519 と重なる見込み。次の月に空きを探すときの候補として残す。
- Parking Lot 系、Decoration 系の Beautification: 4-2 の「花や緑による潤い」に当たらない。数を増やすためだけの置き方になるため、捨てる。
- RecreationalUse(政策、0 円): 効果の記述が「費用なし」だけで、担当の数字への効きを確かめられない。今月は試しにもしない。
- 地区の政策(set_district_policy): 地価を上げる効きを確かめる手段がなく、今月の担当の数字に当たらない。
- (2160,232) の公園: 道路に面していない。高密度の家 2 棟(失う家 6)を壊す必要があるため、捨てる。
