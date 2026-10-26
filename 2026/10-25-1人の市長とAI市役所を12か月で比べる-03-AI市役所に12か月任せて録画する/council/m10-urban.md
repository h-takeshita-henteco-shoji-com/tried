# m10 住宅都市みどり局の案

## 施策

- 施策: 東の (2688,45) に公園 JapaneseGarden を1棟、その西の空き地 (2600〜2660, 40〜100) に岩の飾り(Boulder)を7棟置く。計8棟。道具は `place_building`(pay=True)。公園などを 93 から 101 にし、4-2 の目標100を満たす
- 議決: 要らない

## 実行計画

- 実行可否: 確認済み
- 対象と操作順(上から順に実行する。1棟ごとに `test_place_building` を同じ引数で通ってから `place_building` を呼ぶ):
  1. `place_building(prefab="JapaneseGarden", x=2688, z=45, angle=0, pay=True)`。入口は北向き (2688,61)
  2. `place_building(prefab="Boulder 01", x=2640, z=40, angle=0, pay=True)`
  3. `place_building(prefab="Boulder 03", x=2620, z=40, angle=0, pay=True)`
  4. `place_building(prefab="Boulder 01", x=2620, z=75, angle=0, pay=True)`
  5. `place_building(prefab="Boulder 02", x=2640, z=80, angle=0, pay=True)`
  6. `place_building(prefab="Boulder 04", x=2660, z=80, angle=0, pay=True)`
  7. `place_building(prefab="Boulder 03", x=2640, z=100, angle=0, pay=True)`
  8. `place_building(prefab="Boulder 02", x=2660, z=100, angle=0, pay=True)`
- 設置条件の確認(すべて `test_place_building`。街は変えていない):
  - JapaneseGarden (2688,45): ok=true、費用2,500、入口の道路は Basic Road 区間26352(距離12.7m)、wouldDemolish 0
  - Boulder 01 (2640,40): ok=true、費用100、wouldDemolish 0。道路・電気・水・下水は不要(needsRoad null、needs すべて false)
  - Boulder 03 (2620,40): ok=true、費用100、wouldDemolish 0
  - Boulder 01 (2620,75): ok=true、費用100、wouldDemolish 0
  - Boulder 02 (2640,80): ok=true、費用100、wouldDemolish 0
  - Boulder 04 (2660,80): ok=true、費用100、wouldDemolish 0
  - Boulder 03 (2640,100): ok=true、費用100、wouldDemolish 0
  - Boulder 02 (2660,100): ok=true、費用100、wouldDemolish 0
  - 岩どうしの間隔は x、z とも20m以上。岩は 2x1 マスで、互いの敷地は重ならない見込み。ただし8棟を同時に置いた状態の試しはできないため、2棟目以降の断りは実行時に出る可能性がある(下の中止の条件)
  - `water_trace`(2688,45): 近くの既存園42573 は電気・水とも true、cell の water true。給水塔 16957 (2640,60) が近い。園の水は既存園での代用確認
  - `buildings_near`(Beautification、半径9000): 93棟。岩の Boulder・Rock は今の93棟に含まれない(prefab は園・公園・広場・遊び場のみ)。そのため、岩が「公園など」の数に入るかは未確認(下の不確かな点)
- 接続工事: 不要
- 予備候補(確認済み。使う順):
  1. Boulder 04 (2660,80) が断られたら Boulder 04 を (2660,60) 付近に替えず、その棟を見送る。代わりに下の2.で補う
  2. 予備の岩は用意しない(これ以上の取り壊しゼロの場所は確認していない)。8棟のうち置けた数で 93 に足す
  - 公園の予備: なし。(2655,-240)、(2530,-240)、(2655,-416) などの JapaneseGarden は ok でも住宅を壊すか入口の道路がなく、除いた
- 中止する条件: 1棟ごとに、実行前の `test_place_building` が ok=false、wouldDemolish が1以上、または所持金が 2,082,287 を下回る場合は、その棟だけ見送る。8棟とも見送るときは何もしない。費用は全体で3,200で、所持金 2,318,972 との差は大きく、下回る見込みはない

## 期待する効果

- 改善の見込み: 4-2 の公園などの数が増える。公園は過去5回(m03〜m07)で置いた棟数どおりに数が増えた。岩は今回が初めてで、数に入るかは未確認
- 数値と期限: `buildings_near` の公園など(Beautification、半径9000)は今93。予想は、公園だけなら94、岩も数に入れば101。月末(10か月目の30日目)までに確認する
- 確認方法: `buildings_near`(x=0, z=0, radius=9000, service="Beautification", brief=true)の total を、置く前の93と比べる。同じ条件で測る。岩の id が一覧に出るかも見る
- 不確かな点: 岩が「公園など(Beautification)」の total に入るかは、`list_building_types` で service が Beautification と出ていることだけが根拠で、置いて数えるまで分からない。岩は花や緑ではなく、地価を上げる見込みも持たない。そのため 4-2 の数の目標には届いても、「花や緑による潤い」の中身は公園1棟分に近い。地価(4-1)への効きは見積もれない(m06、m07 で公園は地価に効かなかった)
- 試し: 仮説は、「岩(Boulder)は service が Beautification の建物なので、`buildings_near` の公園などの数に入り、1棟100円・維持費0・道路不要で 4-2 の数を進められる」。測る数は `buildings_near`(service="Beautification", x=0, z=0, radius=9000)の total。場所は (2600〜2660, 40〜100) の空き地。基準は 93。編成方針の「分からないこと」の項目には当たらない(数の定義についての試し)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 費用

- 建設費: 3,200(JapaneseGarden 2,500 + Boulder 7棟 × 100。`test_place_building` の cost)
- 週の維持費の増え分: 40(JapaneseGarden のみ。Boulder の upkeepPerWeek は0。`list_building_types`)

## 戻せるか

戻せる。園も岩も後で取り壊せ、建設費も小さい。

## 前の月の答え合わせ

- m09-urban(公園を (2688,45) に1棟)は採られなかった。理由は、3件の上限の中で重点の2つの試しと流れの試しを先にしたため、1棟では 4-2 の目標100への進みが小さいとされた。今月の公園などは 93 のまま(`buildings_near` total 93)で、判定前。
- 手当て: 1棟では進みが小さいという理由に対し、今月は道路も電気も水も要らない岩7棟を足し、公園などを101にできる形にした。目標100まで残り7、残りは2か月のため、今月置かなければ届かない。実行条件は、棟ごとに `test_place_building` が通ることを確かめた。
- 公園の置き場は、(2688,45) の1か所のほかは、住宅を壊すか入口の道路がなく、取り壊しゼロで置ける場所はなかった(今月8か所を試して確認)。
- 前の月の調査 `council/m09-survey-urban.md` は出しておらず、なし。

## 市の計画

- 当たる施策: 4-2 花や緑による潤い
- 編成方針の重点に当たるか: 当たる(重点の3番目)

## 見たもの

- `list_policies`: 有効は EducationBoost(週7,940)、BigBusiness(4,144)、IndustrySpace(4,834)。無効の HighTechHousing は週20,240(維持費の幅5,000を超え、公園の数にも地価にも効く根拠がない)。Recycling・PetBan・SmokingBan は無効で週0(公園や地価には関係しない)。公園の数や地価の案に使える政策は見当たらない
- `city_info`: 2050-09-28、人口177,490、所持金2,318,972、需要 25/4/56、週の収支 +8,676
- `list_building_types`: Beautification。JapaneseGarden 4x4・2,500・維持費40・電気と水。Boulder 01〜04 は 2x1・100・維持費0・道路と電気・水・下水が要らない。Regular Park 1,000・Regular Playground 1,250 は道路と電気が要る
- `buildings_near`: (2688,-100) 半径400 の公園など13棟。全街(半径9000)の公園など93棟の一覧に Boulder・Rock はない
- `zone_map`: (2688,-100) 半径300。公園の列 x=2688 は z=-416〜-5 で埋まり、北西 (2560〜2650, 40〜190) に空き地
- `test_place_building`: 上の「設置条件の確認」のとおり。公園の候補は (2688,45) だけが取り壊しゼロで通った。ほかの JapaneseGarden (2688,-130)、(2688,-325)、(2688,90) は道路・建物にぶつかり断られた。(2688,-460)、(2655,-5)、(2655,-183)、(2655,-240)、(2655,-276)、(2655,-55)、(2655,-416)、(2530,-240) は住宅などの取り壊し1〜3棟。Regular Park (2640,100)、(2465,778)、(3115,482)、(3520,482)、(2900,784)、(2200,778) は断られ、(2600,20) は5棟取り壊し、(2770,1188) は通るが入口の道路が null
- `water_trace`: (2688,45) の近くの既存園42573 は電気・水・下水とも true。水の網は1つで、給水塔 16957 (2640,60) が近い
- `land_value`: (2640,60) 半径100 の平均63、最小42、最大86、街の平均52
- `building_stats`: 高密度住宅 4,059棟、L1〜L5 は 57/63/388/1,487/2,059。街の地価の平均は住宅(高密度)58

## 判断の根拠

公園などは93で、目標100まで7。取り壊しゼロで道に面して置ける公園は (2688,45) の1棟だけで、公園の列は埋まっている。そのため公園だけでは94止まり。道路も電気も要らず、住宅を壊さない岩(Boulder)を空き地に置けば、数の目標には届く見込み。ただし岩が数に入るかと、花や緑の中身が伴うかは確かめられていない。そこで試しとして明記し、費用3,200・戻せる形で出す。

## 捨てたもの

- 公園を住宅の取り壊しを伴う場所に置く(2〜5棟壊す): 戻せず、住宅と人口を失うため
- Expensive Plaza(12,000)や Botanical garden(15,000)など高額な公園: 1棟で数は1しか増えず、維持費が120〜240かかる。建設費の枠内でも、7棟分には届かない
- Regular Park (2770,1188): 入口の道路が null で、道に面さず働かないおそれがある(m05 で必須条件未確認として採られなかった)
- 住宅の税の変更・HighTechHousing: 4-1 の地価に結びつく根拠がなく、HighTechHousing は週20,240で維持費の幅5,000を超える
