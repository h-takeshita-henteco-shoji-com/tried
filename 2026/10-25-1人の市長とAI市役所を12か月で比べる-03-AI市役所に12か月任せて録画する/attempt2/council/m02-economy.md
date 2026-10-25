# m02 経済観光文化局の案

## 施策

- 施策: 放棄された区画の建物128棟(店約110、工場5、住宅ほか)を取り壊す。街全体(中心 x=0, z=0、半径6000)に `bulldoze(what="abandoned")` を1回打つ。サービスの建物と道路は残る
- 議決: 取り壊し

## 実行計画

- 実行可否: 確認済み
- 対象と操作順:
  1. 実行直前に `preview_bulldoze(x=0, z=0, radius=6000, what="abandoned")` をもう一度呼び、targets が128前後、lost の jobs と homes が 0、power の buildingsLosingPower が 0 であることを見る
  2. `bulldoze(x=0, z=0, radius=6000, what="abandoned")`
  3. 直後に `cargo` と `buildings_near(x=0, z=0, radius=6000, abandoned=true, brief=true)` で、品物がない店とのこりの放棄数を見る
- 設置条件の確認: 新設なし。`buildings_near(x=0, z=0, radius=6000, abandoned=true, brief=true, limit=200)` で放棄の建物133件(うち5件は電柱4と小学校5804で、what="abandoned" の対象外)。`preview_bulldoze(what="abandoned")` で targets 128、segments 0、powerLineSegments 0、waterFacilities 空、transportStations 空、lost は jobs 0 / homes 0、停電する建物 0(modelAgreement 1.0)
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: 実行前の preview で lost の jobs か homes が0でない。buildingsLosingPower が0でない。waterFacilities か transportStations が空でない。targets が150を超える

## 期待する効果

- 改善の見込み: 放棄された店の多くは NoGoods の印を持ち、`cargo` の品物がない店233に数えられている。放棄の店を壊すと数えから外れ、空いた区画に新しい店が建つ余地もできる。壊す建物の働き口と家は0なので、働き口と人口は減らない
- 数値と期限: 品物がない店 233 → 130前後(放棄で NoGoods の店は約110)。原料がない工場 28 → 23前後(放棄の工場5)。建物の `building_stats` の放棄数(商業高密度114など) → 0に近づく。壊した直後と月末に確かめる
- 確認方法: `cargo` の shortages.noGoods.buildings と shortages.noResources.buildings を、壊す前(233 / 28)と同じ範囲(街全体)で比べる。`building_stats`(radius=8000)の abandoned
- 不確かな点: 数えから外れるだけで、生きている店への品物の流れ(貨物駅28755の止まり)は直らない。目標120以下には届かない見込み。空いた区画に建て直す需要は商業2で低い。壊した後に、同じ区画へ再び放棄が出るかは分からない
- 試し: なし

これは局の予測です。

## 調査

- 調査: なし

## 費用

- 建設費: 0(`bulldoze` に費用はなく、払い戻しもない)
- 週の維持費の増え分: 0

## 戻せるか

戻せない。取り壊しは元に戻せないが、壊す建物の働き口と家は0。

## 前の月の答え合わせ

m01-economy(放棄された建物131棟の取り壊し)は採られなかった。理由は、試しの場所(x=2240, z=-950)に焼けた工場12882を含み、s01-1 の基準が動くため来月に比べ直す、というもの。今月は m01-1(道路)が打てず、その場所は変わっていない。基準を保つ事情は消え、品物がない店は228 → 233と悪化した。今月の数字(放棄128棟、失う働き口・家0)で出し直す。調査の結果ファイル m01-survey-economy.md はない(調査を出していない)。

## 市の計画

- 当たる施策: 6-4、7-1 企業の立地、地場企業(品物がない店と原料がない工場)
- 編成方針の重点に当たるか: 当たる

## 見たもの

- `list_policies`: 比較した政策は、BigBusiness(有効、週3,896)、EducationBoost(有効、週7,940)、SmallBusiness(無効、週313)、IndustrySpace(無効、週4,846)、HighTechHousing(無効、週20,252)、Recycling(無効、週0)。税の政策(TaxLower*)は無効、週0。放棄の取り壊しのほうが、品物がない店に直接効くと判断した
- `demand_breakdown`: 働き口86,342、空き3,201、失業7,409(大卒7,205)、空き家4,939
- `cargo`: 品物がない店233、原料がない工場28、敷地の中で止まった521(28755が520)
- `building_stats`(radius=8000): 商業高密度1,110棟のうち放棄114、商業低密度166のうち2、工業806のうち5、住宅高密度の放棄3、住宅低密度の放棄2。事務所のレベル3 3,229
- `zone_summary`(grid=1000): 事務所の空き1,642はすべて emptyBehind。商業高密度の空き549(道に面して建つ112)
- `buildings_near`: 放棄133件(店ほか。NoGoods が大半、工場は NoResources)
- `preview_bulldoze`: 128棟、lost 0 / 0、停電 0

## 判断の根拠

放棄の建物は働き口も家も0で、壊しても失うものがない。品物がない店233のうち約110は放棄で、取り壊すと目標120以下に近づく。事務所の新築や貨物駅の止まりには効かないが、費用0で担当の数字を直接動かせる。

## 捨てたもの

- 道に面した事務所の区画を足す案: 道路の敷設場所と接続を未確認で、実行条件が確認できないため
- SmallBusiness・IndustrySpace・HighTechHousing の政策: 週の費用が増え(313 / 4,846 / 20,252)、品物がない店への効きの見込みが薄い。商業の需要が2で、新しい店が増えても止まらない
- 税の変更: 商業高密度3%・事務所3%・工業3%はすでに低い。働き口の需要への効きは見込めない
- 観光(1,636 → 2,000以上): 有効な建設の場所と接続を今月の道具で確認できなかった
