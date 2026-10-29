# m01 住宅都市みどり局の案

## 案1: 街全体の娯楽の政策 RecreationalUse を試しでかける

### 施策

- 案の id: urban-1
- 施策: 街全体に政策 RecreationalUse をかける(街の全体。地区や座標は指定しない)。道具は `set_policy`
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: 1) `list_policies` で RecreationalUse が active=false、costPerWeek=0 であることを確認済み(今月の確認)。2) `set_policy(name="RecreationalUse", active=True)` を呼ぶ。3) 戻り値の costPerWeek が 0 であることを確かめる。4) 1か月後と2か月後に、下の「確認方法」の数字を測る
- 設置条件の確認: 該当なし(政策の操作。建物や線の設置はない)。政策名は `list_policies` の一覧にあり、解禁の条件は一覧に出ていない
- 接続工事: 不要
- 予備候補: なし(政策の操作で、場所の候補はない)
- 中止する条件: `set_policy` の戻り値の costPerWeek が 0 でないとき、または政策一覧の policyExpensesPerWeek が 10,665 から 1,000 以上増えたとき。その場合は `set_policy(name="RecreationalUse", active=False)` で外し、理由を書く

### 期待する効果

- 改善の見込み: 4-1 の住宅(高密度)の地価と、5-1、5-2 の観光の魅力度を上げる可能性があると、局は予想する。根拠は、政策の週の費用が 0 と確認できたこと(確認した事実)と、今の住宅(高密度)の地価が 58、魅力度の全市の平均が 6 と低いこと。政策の中身の効果は、道具の説明に書かれていないため確かめていない
- 数値と期限: `building_stats` の ResidentialHigh の averageLandValue 58(目標 62 以上)。`map_layer`(attractiveness、全市)の average 6。期限は 2か月目の月例(かけてから約1か月)。効きが見えなければ、2か月目で外す
- 確認方法: `building_stats`(x を省く、全市)の ResidentialHigh の averageLandValue。`map_layer`(type=attractiveness、x・z を省く、n=9)の average。同じ道具・同じ範囲で、今の値と比べる。加えて `land_value`(x=2575、z=1224、radius=200)の average(今の値 61)を見る
- 不確かな点: 効き目の大きさは数値では見積もれない。政策の効果の内容は道具の説明にないため、ゲームの中で測るしかない。地価が動いても、政策か、建設や人口の変化かは分けにくい。その場合は、同じ月の建設と人口の変化を並べて書く
- 試し: 仮説は「RecreationalUse が娯楽や公園の周りの価値を上げ、住宅の地価と観光の魅力度を上げる」。測る数は、`building_stats` の ResidentialHigh の averageLandValue(基準 58)と、`map_layer` の attractiveness の全市の average(基準 6)。場所は全市。基準は今月の値。編成方針の分からないことの「何が観光客を呼び、落とすお金を増やすのか」の一部を測る

### 費用

- 建設費: 0(政策の操作。建設はない)
- 週の維持費の増え分: 0(`list_policies` の RecreationalUse の costPerWeek が 0、costBasis は「no direct cost」)

### 戻せるか

戻せる。`set_policy(name="RecreationalUse", active=False)` で外せる。費用は、かけている間の週の費用(0)だけ。

### 前の月の答え合わせ

なし(1か月目)

### 市の計画

- 当たる施策: 4-1 都市と自然が調和したコンパクトなまち、5-1、5-2 観光(魅力度の測り方)
- 編成方針の重点に当たるか: 当たる(重点1の 5-1、5-2 観光の魅力度を測る)

## 調査

- 調査: なし
- 問い: なし
- 見る道具と引数: なし
- いつ見るか: なし
- 何が分かれば次の手が決まるか: なし
- 担当の問題: なし

## 見たもの

- `city_info`: 人口 178,872、幸福度 85、所持金 2,082,287、観光客 now 1,646 / visits 139、需要(住宅 23、商業 2、工業 60)、dialog なし
- `demand_breakdown`: 働き口 86,175(空き 3,215)、家 55,253(空き 4,935)、失業 7,911、家のない人 0。住宅の需要は低く、住宅が余っている
- `land_value`: 街の平均 52
- `building_stats`: ResidentialHigh 4,057棟、averageLandValue 58、レベル5が 2,042棟。CommercialHigh の abandoned 114、OfficeGeneric の averageLandValue 58
- `zone_map`(中心 0,0、半径 1000): 高密度住宅の帯が中心部に広く、空きの区画は少ない
- `zone_map`(中心 2500,500、半径 400)、`zone_map`(中心 2300,-400、半径 400)、`zone_map`(中心 3600,0、半径 500)、`zone_map`(中心 4000,-100、半径 350): 公園を置ける空きが少なく、灰色の多くは埋立地や大学などの施設
- `zone_summary`(grid 1000): ResidentialHigh の空き 709(道に面する空きは 0)、CommercialHigh の空き 597(道に面する 156)。道に面した住宅の空きはない
- `list_policies`: 政策一覧を取得。有効なもの: EducationBoost(週 7,940、学校の維持費の25%。支出の別枠)、BigBusiness(週 3,876)。RecreationalUse は active=false、costPerWeek=0(no direct cost)。ほかの無料の政策は HeavyTrafficBan(0)、SmokingBan(0)、PetBan(0)、Recycling(0、住宅の税収 -5%、ごみ -15%)、FreeTransport(0、運賃の収入が 0)。有料の政策は PowerSaving(58,281)、WaterSaving(58,281)、SmokeDetectors(57,718)、HighTechHousing(20,248)、IndustrySpace(4,821)、SmallBusiness(315、有効でない)。政策の週の費用の合計は 10,665
- `list_building_types`(service=Beautification): Regular Park 1,000(維持費 8/週)、Regular Plaza 2,500(32/週)、Regular Playground 1,250(24/週)、Expensive Park 4,500(40/週)。いずれも道路が要り、電気が要る
- `map_layer`(attractiveness、全市): 平均 6、最大 157(2575, 1224 付近)、最小 0
- `map_layer`(landvalue、全市): 平均 30、最大 85(2575, 729 付近)
- `buildings_near`(Beautification、半径 3000、brief): 街の Beautification は 68 件(上限 10 件のみ表示)。市政ノートの 81 とは数え方が違うため、目標との比べは市政ノートの値で行う
- `buildings_near`(abandoned=true、半径 4000、brief): 放棄された建物は135件。大半は NoGoods(品物がない店)の店。Hotel が 3 棟、School が 1 棟(service)
- `net_near`: 道路の配置を確認(2350,560 付近、2290,1010 付近、2168,-166 付近、564,-146 付近、-1211,68 付近)
- `test_place_building`(Regular Park、12 回): 置けた候補はなし(下の「捨てたもの」を参照)。564,-125 は通ったが、取り壊す建物が 8 棟(働き口 75)
- `buildings_near`(x=2400, z=600、半径150): 事務所が密集。公園を置く空きは見当たらない
- `zones_at`(2450,-450、半径90)、`zones_at`(500,-500、半径90)、`zones_at`(3600,-450、半径120): 住宅(高密度)の空きは 5、1、0。無区画の空きは 0、10、7。植樹や公園に使える空きは少ない
- `list_trees`: 木の種類は 40 件、1本 10(建設費)
- `city_info` 以外の数(人口の変化など)は今月の基準なので見ていない

## 判断の根拠

- 担当の数字は、住宅(高密度)の地価 58(目標 62 以上)と、公園などの Beautification 81(目標 100 以上、市政ノートの値)。どちらも目標に届いていない
- Beautification を増やす手は、建設費 1,000(Regular Park)で効きは大きいと見込める。しかし、空きがある場所を 12 回の試しで確かめたが、どれも別の建物か道路に当たった。取り壊しで働き口を失う案になるため、今月は採らない。次の月に、放棄された建物の跡を確かめる案を出す
- 政策の RecreationalUse は、費用 0 で、取り壊しも建設もない。確認した事実は「費用 0、政策の一覧にある」の 2 つ。効きの方向と大きさは分からないため、試しとして 1 件出す。測る数は、担当の範囲の地価と、重点 5-1、5-2 の魅力度
- 案の数は 1 件。ほかの候補は場所がなく、実行条件が確認できなかったため、件数を埋める案は出さない

## 捨てたもの

- Regular Park を 2240,528 と 2527,526(北向き): 置けない。埋立地(id 45436、id 3565)に当たる
- Regular Park を 2520,-425(北向き): 置けない。大学(id 17574)に当たる
- Regular Park を 2335,-322(北向き): 置けない。小学校(id 37622)と高層の住宅に当たる
- Regular Park を 3328,-365 / 3487,-365 / 3633,-365(北向き): 置けない。風力発電、高校、警察、小学校、Expensive Plaza に当たる
- Regular Park を 3760,-158 / 3930,-158(南向き): 置けない。道路、小学校、Expensive Plaza に当たる
- Regular Park を 2286,990(北向き、放棄された Hotel 5266 を取り壊す前提): 置けない。道路に当たり、残りの店 8 棟も取り壊しになる(働き口を失う)
- Regular Park を 2168,-180(南向き、放棄された Shop 4109 を取り壊す前提): 置けない。道路と住宅に当たる
- Regular Park を 564,-125(北向き、放棄された Shop 6384 を取り壊す前提): 置けるが、取り壊す建物が 8 棟(働き口 75、家 2)。放棄された建物の跡だけではないため、今月は採らない
- 木の植樹(Green Tree 01 など、1本 10): 空きが少なく、植える polygon を確かめられなかった。次の月に、空きの場所を調べ直す
- HeavyTrafficBan(トラックの通行を禁じる、費用 0): 騒音を減らして地価を上げる見込みはあるが、トラックの配送を止める。8-1 の物流を悪くするため、今月は捨てる
- Recycling(費用 0、ごみ -15%): 4-4 資源循環は保健環境局の施策。住宅の税収が 5% 減るため、今月の urban の案にはしない
- 高密度住宅の空き地の建て替え、住宅の区画の変更: 住宅の需要は 23 と低く、空きの家が 4,935 あるため、住宅を増やす案は効かない
