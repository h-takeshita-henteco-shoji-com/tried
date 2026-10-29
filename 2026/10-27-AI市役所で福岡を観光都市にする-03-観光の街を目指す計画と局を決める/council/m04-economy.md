# m04 経済観光文化局の案

## 案1: 政策 RecreationalUse を外す(第4月の判定)

### 施策

- 案の id: economy-1
- 施策: 政策 RecreationalUse を外す(街全体。地区の指定はしない)。道具は set_policy
- 議決: 要らない

### 実行計画

- 実行可否: 確認済み
- 対象と操作順: (1) list_policies で RecreationalUse の active が true、costPerWeek が 0 であることを確かめる。(2) set_policy(name="RecreationalUse", active=False)。(3) list_policies で active が false、policyExpensesPerWeek が 10,980 のまま変わらないことを確かめる
- 設置条件の確認: 該当なし(建設なし)
- 接続工事: 不要
- 予備候補: なし
- 中止する条件: (1) 実行前に RecreationalUse が既に active=false なら、操作はしない。(2) 同じ月に財政局が別の政策を変えるなら、月1件の枠を財政局と合わせ、順番を市長が決める

### 期待する効果

- 改善の見込み: 観光の数字(観光客、attractiveness、Tourism)は、この政策を外しても動かないと予想する。第3月の試しで、attractiveness は4回とも平均2のまま、観光客と Tourism も基準から動かなかった。効きのない政策を外し、残る SmallBusiness の判定を、ほかの政策と重ねずに見られるようにする
- 数値と期限: 基準は4月1日の値。観光客1,742、訪問139、Tourism 週58、attractiveness 平均2(x=0 z=0 r=4000 n=9)。外した後、5月末に同じ引数で測る。予想は、いずれも基準から大きく動かないこと。量は見積もれない
- 確認方法: city_info の tourists.now と tourists.visits、economy_breakdown の Tourism、map_layer の attractiveness(x=0、z=0、radius=4000、n=9)。今の値と同じ引数で比べる
- 不確かな点: 政策の効きは、今回の試しでは見えなかった。外すことで観光が落ちるかどうかは、5月末の測りで確かめる。週の維持費は0なので、収支は変わらない
- 試し: なし(判定で外す。効き目の試しではない)

### 費用

- 建設費: 0
- 週の維持費の増え分: 0(list_policies の costPerWeek が RecreationalUse は 0)

### 戻せるか

戻せる。政策は set_policy で、いつでもかけ直せる。

### 前の月の答え合わせ

- m03-economy-1(政策 RecreationalUse、試し、採られた): 予想は、attractiveness 平均2、観光客1,772、Tourism 週66が4月末までに増える。結果は、attractiveness 平均2のまま、観光客1,742、Tourism 58。外れ。理由の見立て: 名所を足さない政策では attractiveness は動かない。次の扱い: 外す(この案1)。

### 市の計画

- 当たる施策: 5-1、5-2 観光
- 編成方針の重点に当たるか: 当たる

## 調査

- 調査: あり
- 問い: 品物がない店(noGoods)235軒は、品物のトラックが届かないためか、届いても足りないためか。
- 見る道具と引数: `cargo`(引数なし。shortages.noGoods の数と spots を見る)、`traffic`(x=-1132、z=-1065、radius=400。noGoods が最も多い場所の周りの blocked と cars)、`vehicles_stuck`(kind="truck"、building=null、limit=10。品物を運ぶ止まった車の場所と行き先)
- いつ見るか: 見回り1・見回り2・月末
- 何が分かれば次の手が決まるか: (a) noGoods の数が減らず、traffic の blocked が多く、止まった車が近くにいる → 道の手(道路下水道局に、その区間の道を求める)。(b) blocked が少なく、品物のトラックが届いている → 店の数ではなく品物の量が足りない。原料がない工場(noResources 32)の原料の手(港湾空港局の貨物、または工業の特化)を検討する。(c) noGoods が見回りのたびに変わり、道も量も説明できない → 店の位置が原因として、店の周りの空き地に名所を置く案を検討する
- 担当の問題: 6-4、7-1 企業の立地、地場企業(品物がない店と原料がない工場)

## 見たもの

- `city_info`: 人口178,486、所持金2,110,220、週の収支+9,303、観光客1,742(訪問139)、来ない市民0/0/0、dialog なし
- `list_policies`: RecreationalUse は active=true、costPerWeek=0。SmallBusiness は active=true、costPerWeek=315。BigBusiness、EducationBoost も有効。policyExpensesPerWeek は 10,980
- `economy_breakdown`: Tourism 週58、総収入347,484、総支出338,181
- `map_layer`: attractiveness 平均2(x=0、z=0、r=4000、n=9)、最大25(x=-3000、z=0)
- `list_building_types`(service=Monument): 解禁済みの名所は 20 種類。費用は 20,000(SeaWorld、ScienceCenter、Servicing Services、Friendly Neighborhood)から 200,000(Stadium)まで。大きさは 6×6 から 16×8 の区画単位
- `buildings_near`(service=Monument、x=0、z=0、r=6000): 名所8棟(SeaWorld 2374、Friendly Neighborhood 7856、Countdown Clock 9113、ScienceCenter 29187、Winter Market 30532、Fountain 41780、Plaza 45587、Official Park 46934)。いずれも問題なし
- `buildings_near`(service=PublicTransport、x=0、z=0、r=6000): 旅客の入口 0。バス車庫、貨物センター、貨物港、地下鉄の入口
- `buildings_near`(abandoned=true、x=0、z=0、r=6000): 放棄された建物 134棟。多くは NoGoods の店。候補は 7016(1507,476)、9072(120,68)、9170(1473,306)、4226(-572,132)、11199(2212,1084)、17223(507,206)
- `demand_breakdown`: 働き口86,569、空き働き口3,329、空き家5,062、失業7,090(大卒6,897)
- `cargo`: 品物がない店235、原料がない工場32。止まったトラック804(貨物センター28755 に517)。noGoods の多い場所は (-1132,-1065) 63棟、(2197,823) 47棟、(881,247) 38棟
- `zone_summary`(grid=1000): 道に面した空きの区画は、商業(高密度)141マスのみ。事務所の空き1,641マスは、すべて道に面していない
- `zone_map`(x=2300、z=1200、r=1200): 街の中心の東側は密集した事務所と住宅で、名所を置ける空きは見当たらない
- `zone_map`(x=2600、z=300、r=600): 道に挟まれた街区は、ほぼ既存の建物で埋まっていた
- `zones_at`(x=2500、z=2250、r=300)、`net_near`(x=2500、z=2250、r=400、Road): 道がない。空き地の上に道は0区間
- `map_layer`(x=-3000、z=-2000、r=800、n=5): 空き地2の周りは attractiveness 最大24 だが、道がない
- `map_layer`(x=2500、z=1800、r=1000、n=5): 最大16は (2500,2300) の空き地。道がなく、置けない
- `net_near`(x=2040、z=-280、r=150、Road): 道は区間の格子のみ。周りは高層の住宅と店で、空きは見当たらない
- `test_place_building`(名所の候補を、放棄された店の跡に置く形で6か所以上): Countdown Clock(120,68)、StatueOfWealth(1507,476)、ScienceCenter(2136,629)、Official Park(1507,476、120,68、1473,306、-572,132、2212,1084、507,206)、Official Park(1500,478、angle 90、店2棟を外す)。いずれも道路(Medium Road、Basic Road)か既存の建物と重なった。名所は 6〜16 マス(約48〜128m)で、道路から離れた空きが必要

## 判断の根拠

第3月に試した政策 RecreationalUse は、4月末の判定で、観光の数字がどれも動かなかった(attractiveness 平均2、観光客1,742、Tourism 58)。政策の効きは見えないので、外すのが計画の判定どおりである(案1)。この案は費用0で戻せるが、観光の数字を上げる見込みはない。名所の2棟目は、市街の道に面した空きが名所の大きさに足りず、試しの道具でどの候補も道路か既存の建物と重なった。空き地3の道を待つのが計画どおりで、今月の案にはできない。品物がない店235軒の原因は、道、量、店の位置のどれか分からないので、調査で見る(政策の案は1件まで)。

## 捨てたもの

- 名所の2棟目(放棄された店の跡、7016・9072・9170・4226・11199・17223): 試しの道具で、どれも道路か既存の建物と重なった。名所の大きさ(6〜16マス)に、店を外しても空きが足りない。空き地3の道が引かれる第5月まで待つ
- 名所を空き地2・4・5 に置く案: 道路から400m以内に道がなく、道を引く工事は道路下水道局の担当。今の案にはできない
- 島Bの名所(StatueOfWealth): 橋と電線が未確認。第7〜8月の計画どおり
- 政策 SmallBusiness を外す案: Tourism は42→66→74→68→58と動き、重なりが切れないため、外すと判定できない。月1件の政策の変更を RecreationalUse に使うため、次の月に回す
- 働き口(6-4): 道に面した空きが少なく、税も既に低い。計画の見送りのまま
- 品物の対策の案: 原因が決まっていないので、調査の結果を待つ。港湾空港局の貨物と道路下水道局の道は、他局の担当なので、案を書かず、調査の結果を基に求める
