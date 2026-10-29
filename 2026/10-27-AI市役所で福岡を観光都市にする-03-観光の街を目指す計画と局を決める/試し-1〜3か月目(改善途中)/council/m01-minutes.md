# 1か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 09:40〜09:40)

- 元のファイル: [m01-policy.md](m01-policy.md)
- ゲーム内の日付: 2050-01-01、保存: fukuoka-plan-m01
- 重点: 5-1、5-2 観光、8-1 物流・人流のゲートウェイ、6-3 公共交通を主軸とした交通体系

- 見たもの: [m01-policy.md の「見たもの」](m01-policy.md#見たもの)(16 行)
- 判断の根拠:

  観光の5つの数字(観光客、訪問、収入、attractiveness、名所)と入口が、どれも目標から遠く、公約4に直結するため、5-1、5-2を重点にした。8-1は貨物駅の停滞が目標の約2倍で、旅客の入口も担当に含まれる。6-3は流れ51%で目標との差が9ポイントある。ほかの施策は出発点が目標に届く、または近い。

- 捨てたもの:

  - 4-2 公園など: 81棟で目標100に18棟足りないが、観光の名所と重なる案は5-1、5-2で出せる。専用の重点にはしない
  - 4-3 脱炭素(汚染32): 目標15以下まで遠いが、公約と直結しない。局の案があれば見る
  - 4-4 資源循環(ごみ15): 満杯の埋立地7を含め課題はあるが、今月は重点にしない
  - 6-4、7-1 企業の立地(品物がない店228): 8-1の貨物改善と合わせて効くため、別の重点にはしない
  - 1-2、2-3、3-3、3-4: 出発点が目標を満たすか近く、今月は維持で足りる

## 2. 長期計画

- 市長がまとめた計画: [plan-city.md](plan-city.md)
- 住宅都市みどり局の計画: [plan-urban.md](plan-urban.md)
- 道路下水道局の計画: [plan-roads.md](plan-roads.md)
- 港湾空港局の計画: [plan-port.md](plan-port.md)
- 経済観光文化局の計画: [plan-economy.md](plan-economy.md)
- 保健環境局の計画: [plan-health.md](plan-health.md)
- 教育委員会の計画: [plan-education.md](plan-education.md)
- 消防局の計画: [plan-fire.md](plan-fire.md)
- 財政局の計画: [plan-finance.md](plan-finance.md)

## 3. 8つの局の案

### 住宅都市みどり局(urban)(hooks の記録で 09:41〜09:52)

- 元のファイル: [m01-urban.md](m01-urban.md)
- 案 urban-1: 放棄された店の跡に広場を置く(1850,-150)
  - 建設費 2500、週の維持費 +32、戻せない
  - 市の計画: 4-2、4-1
  - 議決: 要る(取り壊し)
- 案 urban-2: 街全体の政策 RecreationalUse を試す(観光の名所の仮説)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m01-urban.md の「見たもの」](m01-urban.md#見たもの)(13 行)
- 判断の根拠:

  - 4-2 の Beautification は 81 で、目標 100 まで 19 足りない。街の中は詰まっており、道路に面した空きはほとんどない。放棄された建物を壊して置く手が、実行できる数少ない形だった
  - 案1は、取り壊しが2棟(放棄1棟、住宅1棟)で、失う働き口は 0、家は 1。`test_place_building` が、入口の道路を確かめ、置けると返した
  - 案を1件だけにした。政策の変更(RecreationalUse)は、局をまたぐ調整Aのとおり経済観光文化局が持つ。局は attractiveness と地価を同じ範囲で測るだけにする
  - 広場の候補は、今月の確認で1件(1850,-150)だけが、取り壊しの損失なしで通った。残りの候補は、道路との衝突か働き口・家の損失で断られた。毎月の確認数は計画に書く

- 捨てたもの:

  - 名所型 Expensive Plaza(2575,1224 付近): 最大の名所の地点に置く場所がない。Regular Plaza(2574,1262)は、事務所 12349 と道路 segment 7056 にぶつかり断られた。取り壊しの対象を増やすと、働き口を失う
  - 放棄された店の候補の残り(4109、4171、6384、5985): 道路の中心線と当たるため、今月は断られた。位置と向きを変えて試し直すのは、次の月に計画の中で行う
  - 19566、14298、8020: 壊れる建物に、働き口 35 を失う店(19566、14298)や、家 2 を失う住宅(8020)が含まれる。失うものを増やすため、今月は見送る
  - 南の空き地(-520,-520)の広場: `test_place_building` は、入口の道路が null。道路 z=-440 から引く道は、オフィス2棟(id 9325、33018)を壊す必要がある。失う働き口を増やすので、今月は見送る
  - 木の植栽による地価の手: 効き目の量は見積もれない。事業3として3月以降に試す。今月は案にしない
  - 公園の数を、装飾の駐車場(Decoration Concrete Parking Lot、1,000)で増やす手: 4-2 の数は増えるが、緑による潤いの施策の中身に合わない。出さない
  - 4-1 の高密度住宅の地価を上げる政策(HighTechHousing 週 20,248): 週の収支の守る線を割るおそれがある。今月は出さない

### 道路下水道局(roads)(hooks の記録で 09:41〜09:51)

- 元のファイル: [m01-roads.md](m01-roads.md)
- 案 roads-1: 東の幹線の交差点手前を広げる(segment 5784、Basic から Small 4 Lane へ)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m01-roads.md の「見たもの」](m01-roads.md#見たもの)(29 行)
- 判断の根拠:

  - 担当の数字は、交通の流れ 51%(目標 60%)と、電気・水・下水が来ない市民 0。電気・水・下水は 0 で、保つだけでよい。交通が局の主な担当
  - 案1は、交通の流れを局の範囲で動かす最も小さい手。止まり車が 102 集まる (2309,-925) の北の区間を、Basic から Small 4 Lane に上げる。試し `test_upgrade_road` が通り、費用は 0、維持費の増えも 0。効き目は量を見積もれず、試しとして出す
  - 観光の入口(旅客の港)と名所の置き場は、このたびは案にしない。理由は、旅客の港の候補の岸を試しで全部断られたため。名所の候補は、都心の attractiveness が高い所が事務所で埋まり、空いた所も道路と建物にぶつかったため。港湾空港局の担当でもある。局は、場所が決まったら道路を引く役に回る
  - 政策は、list_policies の一覧で、交通や観光に効く有効な政策が見つからなかった。FreeTransport は運賃収入を0にするので使わない
  - 調査は、西の短い区間 36011(2228,-950)の影響を見るために出す。取り壊しの案は、区画の建物(オフィス 30、空き 6)への影響が見えるまで出さない
  - 案の数は1件。試しの確認済みの手が1つだけ、ほかは実行条件が未確認

- 捨てたもの:

  - 旅客の港(Harbor、80,000)を岸に置く案: 候補の (-1000,1100)、(-800,1180)、(-960,1080)、(-800,1290)、(-1100,1290)、(-900,1150)、(-720,1130)、(-520,1160) を試したが、断られた(HeightTooHigh、既存の港とぶつかる、道路とぶつかる)。接続と置く場所が未確認のため、実行可能の案にしない。港湾空港局の担当でもあるので、次月に場所を探す
  - 名所(SeaWorld 20,000 など)を都心に置く案: attractiveness 最大 188 の (2375,1624) 周辺は事務所で埋まり、空いた所は道路とぶつかる。取り壊しの案は、失う働き口を確かめてから出すべきだが、まだ確かめていない
  - 名所を (-1560,-730)、(-1350,-705) に置く案: 道路と建物にぶつかり、試しが通らない
  - 西の短い区間 36011 を取り壊して、西の Basic Road を上げる案: 取り壊しの議決が要る。preview_bulldoze は区間 2 本で、失う働き口 0。区画の建物が道に面しなくなる恐れ(zones_at で、オフィス 30 のうち空き 6)。効き目は調査の結果を見てから決める。今月は出さない
  - Fire House(32853)が邪魔する区間 14040 を取り壊す案: 消防局の建物を壊すことになり、担当の外。今月は出さない
  - 信号や譲れの標識を (2280,-950) に付ける案: 交差点は譲れが無く、道の幅の差が大きいので、先に幅を直す。効き目を見てから考える

### 港湾空港局(port)(hooks の記録で 09:41〜09:55)

- 元のファイル: [m01-port.md](m01-port.md)
- 案 port-1: バス路線5本の台数を半分にする
  - 建設費 0、週の維持費 +-2400、戻せる
  - 市の計画: 6-3
  - 議決: 要る(予算)

- 見たもの: [m01-port.md の「見たもの」](m01-port.md#見たもの)(23 行)
- 判断の根拠:

  - 案1は、6-3(流れ51%)に効く手として確かめた。路線28、38、39、37、11は、乗客に比べて車両が多い(台数が100台前後なのに乗客が20〜60)。台数を減らすのは、予算(議決)だけで済み、建設も取り壊しもない。道具の line と percent は tool-reference の通り。実行可否は、5路線の id を list_transport_lines で確かめたので確認済み。効きは分からないので試しとし、月末の流れで判定する。維持費の減りは守る線(週の収支+3,000)を破らない
  - 旅客の入口(5-1、5-2)は、今月の重点だが、場所が確かめられなかった。港は、貨物港32211と1366、46112の周りで試したが、どれも建物・桟橋・道路と重なるか、岸の高さで断られた。線路の周りの旅客の駅も、空きが狭く断られた。確認できた場所がないので、案にしない(実行条件が未確認の案は出さない)。次の月は、岸の地形を下げる仮定を続けて試す
  - 8-1(貨物駅28755の空き待ち492台)は、原因が確定していない。道を太くする案は、隣の貨物駅にぶつかって断られた。隣の貨物駅13893は道につながり、出られるのに、トラックが来ていない。原因が分からないので、施策にせず調査にする。是正(第2回)の確認でも、13893 の道は通ったので、道が原因ではないと見る。3月に行き先の決まりとして止めるか、道路下水道局へ伝えるかを、2月末の結果で分ける
  - 案の数: 確認できた案は1件。旅客の港と旅客の駅は場所が未確認、8-1 は原因が未確定なので、件数を埋めるための案は出さない

- 捨てたもの:

  - 旅客の港(Harbor)の置き場所: 貨物港32211・1366・46112 の周り9か所で試して、どこも断られた(ObjectCollision、HeightTooHigh、CannotConnect、SlopeTooSteep)。場所が確認できるまで、案にしない。次の月に、岸を下げる仮定を続けて試す
  - 旅客の駅(Train Station)の置き場所: 線路と道路の密集で、試した2か所とも断られた。場所を探す手は、次の月の候補として残す
  - 空港(Airport、150,000、4,800/週): 維持費が重く、週の収支が約+5,100 まで落ちる。外とつながる飛行機の道と、道路・電気・水・下水も要る。1か月では確かめられないので、採らない
  - 貨物駅28755の出口の道を太くする(Large Road): 隣の貨物駅に当たって断られた。取り壊しが要るが、取り壊しの案は、壊す前に効きを確かめる必要がある。今月は出さない
  - 隣の貨物駅13893を使う案(トラックの振り分け): トラックが来ない理由が分からない。調査の結果で決める
  - HeavyTrafficBan(政策): トラックの通行を止めるため、貨物の流れ(8-1)と店の品物(品物がない店228)を悪くする。採らない
  - FreeTransport(政策): 運賃収入5,179/週を失う。路線の乗客は少なく、車の流れを変える量は小さいと見込む。採らない
  - 名所(Monument)の追加: 解禁済みの名所はあるが、観光の名所は経済観光文化局の担当の数字なので、この局の案にしない

### 経済観光文化局(economy)(hooks の記録で 09:41〜09:54)

- 元のファイル: [m01-economy.md](m01-economy.md)
- 案 economy-1: 観光の政策 Recreational Use を有効にする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m01-economy.md の「見たもの」](m01-economy.md#見たもの)(24 行)
- 判断の根拠:

  - 観光の5つの数字は、どれも目標から遠い(観光客 1,646 → 3,000、Tourism 45 → 1,000、attractiveness 6 → 12、名所 6 → 10)。担当の重点はこれに当たる
  - 名所の追加が本命だが、街の中心は道路と住宅が詰まり、12マスの名所を置ける空きがない。中心の放棄された店を取り壊す案も、道路と建物が重なり置けなかった。北西の空き地の公園2棟は、置く場所は確かめられたが、水道管・下水管・送電線の接続(約 250m 級)が未確認のため、今月の案にはできない。接続を確かめる手は2月の試しに回す(調整C)
  - 観光の政策は、費用0で戻せ、今月の政策の変更の1件に当たる。一覧には観光に直接効く名前の政策がなかったが、Recreational Use の効き方は未確認。試しとして、測る数を決めて出す
  - 品物がない店 228 は観光の収入を止めている。貨物駅 28755 の出口の詰まり(492 台が建物の中で止まる)は港湾空港局の調査(調整B)。経済観光文化局は、hotspot の店が貨物駅以外の道から荷を受けるかだけを見る
  - 案の数は1件にした。ほかの候補は、接続や場所の未確認、または政策の上限(月1件)で出せなかった

- 捨てたもの:

  - 北西の空き地に名所を2棟(Official Park、(-270、880) と (-270、960))置く案: 場所と道路は確認できたが、水道・下水・送電線の接続が未確認(水道管 245m、送電線 260m)。実行対象にできないため、2月の接続の試しに回す。費用は建設 90,000、週の維持 +256
  - 中心部の放棄された店を取り壊して名所を置く案: 取り壊しの議決が要る。道路と建物が重なり、3か所とも置けなかった
  - 住宅を取り壊して名所を置く案(-1700、-30、-110、505): 家 96〜108 を失い、公約1(人口)に反する
  - 事務所を増やして働き口を増やす案: 道に面した空きの事務所区画が 0 で、新しい道路と区画が要る。道路の計画は別に確かめる。今月は見送り、次の月に候補地を調べる(事業3で6月に政策を試す)
  - 政策 SmallBusiness(週 315): 観光と店への効き方が未確認。今月の政策の変更は1件のため、Recreational Use を優先した。経済観光文化局の週の維持費の上限(520)も、名所2棟と合わせると超えるため、今は外す
  - 旅客の入口(Train Station、Harbor、Airport)を置く案: 旅客の入口は港湾空港局の担当。経済観光文化局は案にしない(調整D)
  - 観光客の収入を上げる商業の増設: 商業(高)の需要は 2 と低く、店の数より品物の不足が問題のため、今月は見送る

### 保健環境局(health)(hooks の記録で 09:41〜10:00)

- 元のファイル: [m01-health.md](m01-health.md)
- 案 health-1: 汚染を出す工場4棟の取り壊し(跡は工業から外す)
  - 建設費 0、週の維持費 +0、戻せない
  - 市の計画: 4-3、1-2
  - 議決: 要る(取り壊し)

- 見たもの: [m01-health.md の「見たもの」](m01-health.md#見たもの)(54 行)
- 判断の根拠:

  - 汚染の印(32)は、工場が住宅の隣にある東の地区に集まる。工場の取り壊しは汚染の源を直接減らす手で、局の担当の数字(4-3)に当たる。失う働き口は4棟で60。全体の86,175に比べて小さい。案1を採る
  - 再調査で、300m内の汚染の印は4棟と分かった。印の多くは北の焼却場 2267 の周りにあり、この案の効きは主に工場に近い数棟と見る。その分、判定は2月に印の内訳で行う
  - 死体の印(52)とごみの印(15)は、火葬場と埋立地が十分にあるのに、霊柩車とごみ車が道の渋滞で止まっている(`vehicles_stuck`、`traffic`)。局の手(施設の増設)は渋滞を増やすため、道の改善を求める。局は見る道具で調べる(調査)
  - 埋立地の新設は、近くで試した2か所が道路と線路に重なり、置けなかった。空き地の埋立地は、ごみ車の渋滞を増やすため、今は採らない
  - 健康の平均(78)は、汚染と死体の運びに影響されると見る。医療施設の増設は、住宅のない南東の空白に置くと効かない。人の住む地区の候補は、次の月に探す
  - 案の数: 1件(汚染の取り壊し)。調査を1件。案を増やすと、取り壊しの議決が増えるため、効きの確かめを優先する

- 捨てたもの:

  - 火葬場の新設(死体の印の対策): 近くに火葬場 36841 があるが、処理が0で、霊柩車が渋滞で動けない。火葬場を増やしても、道が詰まったままでは効かない
  - 埋立地の空け(empty_building、満杯の7か所のうち16914 など): 中身 800万を別の埋立地へ運ぶため、ごみ車が大量に増え、渋滞を悪くする。調査の結果を見てから決める
  - 埋立地の新設(ごみの印): 近くで試した2か所は道路と線路に重なり、置けなかった(test_place_building)。空きの場所を探すのは次の月
  - 政策 Recycling(ごみ -15%): 費用は0だが、住宅の税が約5%減り、週約13,000の減収。週の収支 +3,000 の守る線を割るため、採らない
  - 政策 HeavyTrafficBan(大型車の規制): 費用は0だが、商品の運搬を止め、品物がない店(228)を悪くする。採らない
  - 病院の増設(健康の平均): 南東の医療の空白には住宅がない。住宅の多い地区の候補は、まだ確かめていない。次の月に探す
  - 焼却場 2267 の置き直し(汚染): 置ける空きが、住宅から離れた場所にない。工業の空きも、住宅の隣

### 教育委員会(education)(hooks の記録で 09:41〜09:50)

- 元のファイル: [m01-education.md](m01-education.md)
- 案: なし

- 見たもの:

  - `services`: 小学校の定員 14,268、高校 24,360、大学 36,540。働き手 82,895・働き口 86,175。犯罪率 5
  - `citizens_summary`: 子ども 11,344、10代 22,372、若者 32,246、成人 68,040。学生 43,231。失業 6,584(うち大学卒 6,483)。来ない市民 0
  - `buildings_near`(service=Education、半径6,000m、brief、limit 30): 学校と大学の一覧の一部(total 71)。印の付いた建物は、小学校1棟(5804)に火事と致命的な問題、大学1棟(14511)に死亡と重大な問題。定員の数には関係しない
  - `building_stats`(半径6,000m): 住宅(高密度)の地価の平均 58。事務所レベル3 3,227棟
  - `economy`: 教育の予算 120%(昼・夜)、公園 150%、医療 150%、警察 150%、ごみ 150%
  - `list_building_types`(service=Education): 小学校 建設費 10,000・維持 160/週・定員 +300、高校 建設費 24,000・維持 560/週・定員 +1,000、大学 建設費 75,000・維持 1,920/週・定員 +4,500。いずれも解禁済み
  - `list_policies`: 政策の一覧(24件)。比較したのは `EducationBoost`(有効、週 7,940、学校の維持費の +25%)。ほかの政策は担当の数字に関係しないと判断した。`EducationBoost` の働きは名前からの推測で、確かめていない。外す案は出さない

- 判断の根拠:

  - 2-3 の担当の数字(小学校と高校の定員が、子どもと10代を上回る)は目標を満たしている。案で直す問題がない。
  - 高校と小学校を増やす手は、不足が出たときに効く見込みがある。今は不足がないため、今月は出さない。
  - 10代と子どもが定員に近づく速さが分からない。そのため調査を1件出し、見回りと月末に定員と人数を測る。
  - 判定の線は、建って定員になるまでの遅れを入れて2月に決める(計画の是正、第1回)。
  - 印の付いた建物(小学校5804の火事、大学14511の死亡)は、担当の定員の数には入らない。担当外の問題なので、ここでは扱わない。
  - 前の月の答え合わせ: なし(1か月目)。

- 捨てたもの:

  - 高校の増設(1棟): 担当の不足がなく、今の余裕 1,988 で足りる。維持費 560/週を先に払う理由がない。判定の線を超えた月に出す。
  - 小学校の増設(1棟): 子どもの比は 79.5% で、余裕 2,924。今は不要。
  - 大学の増設: 市の計画の目標外で、建設費 75,000、維持 1,920/週と大きい。6-1 の都心機能の効き目も確かめていないため出さない。
  - `EducationBoost` を外す: 週 7,940 の節約になるが、学校の働きが下がるおそれがある。担当の定員の数を悪くするため出さない。
  - 大学卒の失業(6,483)への対策: 働き口の不足の問題で、経済観光文化局の担当(6-4、7-1)。教育の定員では直らない。

### 消防局(fire)(hooks の記録で 09:41〜09:59)

- 元のファイル: [m01-fire.md](m01-fire.md)
- 案 fire-1: 消防の予算を 140 から 150 にして、火事の印を減らす試し
  - 建設費 0、週の維持費 +2280、戻せる
  - 市の計画: 3-4
  - 議決: 要る(予算)

- 見たもの: [m01-fire.md の「見たもの」](m01-fire.md#見たもの)(30 行)
- 判断の根拠:

  - 火事の印 4 棟と犯罪の印 3 棟の合計 7 が、目標の 4 以下を超えている。火事の印 4 棟は、消防署の届きが最大の所にあり、届かないことは原因ではないと見た。原因は確かめられていないので、予算を上げる試しを案1にし、同時に火事の建物が残るかを見る調査を出した。
  - 再調査で、火事の印の 2002 と 5804 は稼働中と確かめた。焼け落ちた建物ではないので、取り壊しの案は要らない。予算の試しは残す。ただし、近くの消防署のエンジンは今ほとんど出ていないため、効き目は見積もれない。3月に出動の数も見る。
  - 犯罪の印 3 棟の近くで、道路に面した空きは確認できなかった。候補はすべて、公園との重なり、道路との重なり、住宅の取り壊し、入口の道路なしのどれかで、実行条件が未確認。このため警察署の案は出さない。
  - 案は1件とした。ほかの手は、実行条件が確認できないか、費用が守る線を割るため。件数を埋めるために案は作らない。

- 捨てたもの:

  - SmokeDetectors(政策): 週の費用の見積もり 57,718。週の収支 +9,965 を約 -47,753 にし、守る線(+3,000)を割るため、今月は見送る。
  - 警察署を犯罪の印の近くに置く案: 候補 (2330,780) は公園と重なる。(2600,1200) は道路と広場と重なる。(2500,1080) は道路と重なる。(2450,860) は住宅 45 世帯の取り壊しが要る(議決が要る)。(2200,700)、(2380,700) は入口の道路がなく、住宅の取り壊しが要る。実行可能な候補がないので案なし。
  - 消防署(Fire House)を火事の印の近くに置く案: (3300,-820) は入口の道路がなく、住宅 17 世帯の取り壊しが要る。消防の届きは最大の所なので、効き目も小さいと見た。
  - 消防の予算を 150 より上げる案: 予算は上限 150 で、今の 140 から +10 が型の上限内。
  - 警察の予算: 既に上限 150 のため、動かさない。
  - 2002 と 5804 を取り壊す案(焼け落ち前提): 再調査で稼働中と確かめたため、取り壊しの案は出さない。

### 財政局(finance)(hooks の記録で 09:41〜09:51)

- 元のファイル: [m01-finance.md](m01-finance.md)
- 案 finance-1: 観光の政策の試し(RecreationalUse を有効化)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m01-finance.md の「見たもの」](m01-finance.md#見たもの)(11 行)
- 判断の根拠:

  - 守る線の余裕: 週の収支 +9,965(守る線 +3,000 に対して余裕 6,965)、所持金 2,082,287(守る線 1,874,000 に対して余裕 208,287)。今月は費用を動かさないので、守れている。
  - 観光の5つの数字は、どれも目標から遠い。観光の支出 45 は、観光客 1,646 に対して小さい。品物のない店(228)と、貨物の止まり(貨物駅 492)が疑わしいが、その手は港湾空港局と道路下水道局の担当で、財政局の手ではない。
  - 財政局の手は、税、予算、融資、政策の4つ。政策は、経済観光文化局の持ち物になった(調整A)。税と予算は、効きを測れる根拠がない。融資は要らない。
  - 案の数を0件にした理由: 有効な手が今月は財政局に残っていない。件数を埋めるための案は作らない。3月の BigBusiness の試しに向けて、守る線を毎月確かめる。

- 捨てたもの:

  - RecreationalUse の有効化(前回の案1): 局をまたぐ調整A で、経済観光文化局が持つ。財政局は案を出さず、attractiveness と Tourism を測るだけにする
  - 観光の支出の原因の調査(前回の調査): 貨物の調査は、局をまたぐ調整B で港湾空港局が持つ。財政局は調査を出さない
  - 商業の税を下げる(商業(低) 9→7、商業(高) 3→1 など): 観光の支出を増やす仕組みは、品物がない店があると働かない。商業の税収(週 41,675)を下げる幅は道具で確かめられず、守る線を割るおそれがある
  - SmallBusiness(週 315): 観光の支出に効く根拠がない。政策の変更枠は、3月の BigBusiness の試しに回す
  - FreeTransport(運賃の収入 週 5,179 を失う): 交通の流れの改善は、混んでいる道路の区間の対策(道路下水道局)が要る。政策だけでは、流れ 51% を 60% にする見込みがない
  - 道路の予算を +20(週 約 1,700 の増え): 道路の傷みの状態を確かめる道具がなく、交通の流れに効くかは未確認
  - 融資(BankA、BankB、BankC): 所持金が十分にあり、借りる理由がない

## 4. 差し戻しと再調査

- 保健環境局: health-1(実行可 True)
- 消防局: fire-1(実行可 True)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m01-bill.md](m01-bill.md)
- 採った m01-1: 放棄された店の跡に広場を置く(元 urban-1、議決が要る(取り壊し))
- 採った m01-2: 東の幹線の細い区間を4車線に広げる(元 roads-1、議決は要らない)
- 採った m01-3: バス路線5本の台数を半分にする(試し)(元 port-1、議決が要る(予算))
- 採った m01-4: 観光の政策 Recreational Use を有効にする(試し)(元 economy-1、議決は要らない)
- 採らなかった health-1: 工業の需要が高く、壊した跡が工業のまま建て替わるおそれがある。汚染の源が4棟かも未確認で、働き口60と品物不足への響きもある。
- 採らなかった fire-1: 火事の印の2002と5804にFatalProblemが付き、焼け落ちた建物なら予算を上げても印は消えない。

- 見たもの:

  - `Read`: 8局の案 `council/m01-<局>.md`、8局の長期計画 `council/plan-<局>.md`、`council/plan-review.md`、`council/m01-policy.md`、`mayor-note.md`、`tool-reference.md`。今月の数字は、見る段で測った値(人口 178,872、所持金 2,082,287、週の収支 +9,965、流れ 51%、観光客 1,646)を局の案から写した

- 判断の根拠:

  確認済みで、費用が守る線の内にあり、重点(観光、8-1、6-3)に当たる手を採った。建設費は 2,500、週の維持費は約 -2,368 で、週の収支 +9,965 と所持金 2,082,287 は守る線(+3,000 / 1,874,000)の内に収まる。観光の入口は、局が置き場所を確かめられなかったため、案がない。調査は、重点の2つ(8-1 と 6-3)と、Tourism の原因の1つを採った。試しの案が複数あるが、測る場所は分かれている。重なる m01-3 と m01-2 は、判定に別の円を足して分けた。

- 捨てたもの:

  - health-1 と fire-1: 上の「条件付き」。局が同じ月に1回調べ直す
  - 保健環境局の霊柩車とごみ車の調査: 枠が3件で、重点の外のため
  - 教育委員会の調査: 市長が毎月同じ数字を読める。2月の判定の線に使う
  - 旅客の入口、名所の新設、島と空き地の案: 局が置き場所を確かめられず、案が出ていない。2月の確認を `plan-city.md` の調整Kに入れた

## 6. 議会: 可決と否決(hooks の記録で 10:01〜10:01)

- 元のファイル: [m01-assembly.md](m01-assembly.md)
- m01-1 取り壊し: 可決。preview_bulldoze で失うものは家1と働き口0の店1棟。案の数字と一致し、代わりの手との比較もある。
- m01-2 財政: 可決。費用0、維持費0で戻せる。守る線に響かない。
- m01-3 予算: 可決。路線の予算の変更で、サービスの予算(バス150)は動かない。維持費は減り、戻せる。観光客への響きも書かれている。
- m01-4 財政: 可決。費用0で戻せる。政策の変更は月1件の内。
- 可決した種類(hooks が見る): 取り壊し、予算

- 見たもの:

  - `Read`: 案 `council/m01-bill.md`、`council/plan-city.md`、`council/plan-finance.md`、`protocol.md`、`guard.py`
  - `city_info`: 所持金 2,082,287、週の収入 342,140、支出 332,175
  - `economy`: バスの予算 150(サービス全体)
  - `preview_bulldoze`(1862,-152, r=22): 壊す建物 2棟(住宅 5113、店 14155)、失う家 1、働き口 0、電気を失う建物 0
  - `list_transport_lines`: 路線 28、38、39、37 の予算 200、路線 11 は 100。vehicles は案の数字と一致

- 判断の根拠:

  4つの点のどれにも当たらない。取り壊しの失うものは自分でも確かめて一致した。財政は建設費 2,500 と維持費の減りで、守る線の内に収まる。

- 捨てたもの:

  - m01-3: 路線の予算の変更幅が大きいので否決を考えた。±20 は路線ではなくサービスごとの決まりで、hooks も同じ読み方のため可決にした。幅の読み方は、人が決め直してよい。

## 7. 実行する市長: 実行と見回り(hooks の記録で 10:02〜10:08)

- 実行してよい施策: m01-1、m01-2、m01-3、m01-4
- 実行した: m01-1、m01-2、m01-3、m01-4
- 失敗した: なし
- 臨時: なし
- 見回り 2050-01-11: 人口 178869、所持金 2089876、週の収支 7259、幸福度 85
- 見回り 2050-01-21: 人口 178667、所持金 2103120、週の収支 9503、幸福度 85
- 報告:

  4件とも議案どおり実行した。m01-1 は広場(id 14807)を設置し、家1と放棄店1を壊した。費用は2,500。m01-2 は4車線化で費用0。(2309,-925) r300 の blocked は102から54になった。m01-3 はバス5路線の台数を半分にした。月末の流れは51%から55%、バス支出は週約-2,140。m01-4 は RecreationalUse を有効にした。観光客は1,646から1,732、Tourism の収入は45から46、attractiveness の平均は6のままだった。月末の人口は178,797(基準比-75)、所持金は2,117,372、週の収支は+9,877。見回り2回は、境目に当たらなかった。電気・水・下水が来ない市民は0。臨時なし。調査3件は council/m01-survey-*.md に書いた。貨物駅28755の敷地内の停止は505、531、520台で動かず、13893は0台。set_time の道具が使えなかった。city_info で paused=true を確かめ、そのまま進めた。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m01、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 09:39〜10:18(hooks の記録の時刻から)、道具の行 502
- 議会が可決した種類: 予算、取り壊し
- 議決が要る道具の呼び出し: 6 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 463 件
- hooks の拒否: 0 回

#### 運営のフォルダで、決まりの外の変更(git status)

- `ボツ-12か月の運営/command-log.txt`
- `ボツ-12か月の運営/council/_tmp_health_m02_west.jpg`
- `ボツ-12か月の運営/council/ledger.jsonl`
- `ボツ-12か月の運営/council/m01-assembly.json`
- `ボツ-12か月の運営/council/m01-assembly.md`
- `ボツ-12か月の運営/council/m01-bill.md`
- `ボツ-12か月の運営/council/m01-economy.md`
- `ボツ-12か月の運営/council/m01-education.md`
- `ボツ-12か月の運営/council/m01-finance.md`
- `ボツ-12か月の運営/council/m01-fire.md`
- `ボツ-12か月の運営/council/m01-guide.md`
- `ボツ-12か月の運営/council/m01-health.md`
- `ボツ-12か月の運営/council/m01-hooks.log`
- `ボツ-12か月の運営/council/m01-minutes.md`
- `ボツ-12か月の運営/council/m01-policy.md`
- `ボツ-12か月の運営/council/m01-port.md`
- `ボツ-12か月の運営/council/m01-roads.md`
- `ボツ-12か月の運営/council/m01-run.json`
- `ボツ-12か月の運営/council/m01-survey-health.md`
- `ボツ-12か月の運営/council/m01-survey-port.md`
- `ボツ-12か月の運営/council/m01-survey-roads.md`
- `ボツ-12か月の運営/council/m01-urban.md`
- `ボツ-12か月の運営/council/m02-assembly.json`
- `ボツ-12か月の運営/council/m02-assembly.md`
- `ボツ-12か月の運営/council/m02-bill.md`
- `ボツ-12か月の運営/council/m02-economy.md`
- `ボツ-12か月の運営/council/m02-education.md`
- `ボツ-12か月の運営/council/m02-finance.md`
- `ボツ-12か月の運営/council/m02-fire.md`
- `ボツ-12か月の運営/council/m02-guide.md`
- `ボツ-12か月の運営/council/m02-health.md`
- `ボツ-12か月の運営/council/m02-hooks.log`
- `ボツ-12か月の運営/council/m02-minutes.md`
- `ボツ-12か月の運営/council/m02-policy.md`
- `ボツ-12か月の運営/council/m02-port-map-cargo.jpg`
- `ボツ-12か月の運営/council/m02-port.md`
- `ボツ-12か月の運営/council/m02-roads.md`
- `ボツ-12か月の運営/council/m02-run.json`
- `ボツ-12か月の運営/council/m02-survey-fire.md`
- `ボツ-12か月の運営/council/m02-survey-health.md`
- `ボツ-12か月の運営/council/m02-survey-port.md`
- `ボツ-12か月の運営/council/m02-urban.md`
- `ボツ-12か月の運営/council/m03-bill.md`
- `ボツ-12か月の運営/council/m03-economy.md`
- `ボツ-12か月の運営/council/m03-education.md`
- `ボツ-12か月の運営/council/m03-finance.md`
- `ボツ-12か月の運営/council/m03-fire.md`
- `ボツ-12か月の運営/council/m03-guide.md`
- `ボツ-12か月の運営/council/m03-health.md`
- `ボツ-12か月の運営/council/m03-hooks.log`
- `ボツ-12か月の運営/council/m03-minutes.md`
- `ボツ-12か月の運営/council/m03-policy.md`
- `ボツ-12か月の運営/council/m03-port-cargo-map.jpg`
- `ボツ-12か月の運営/council/m03-port.md`
- `ボツ-12か月の運営/council/m03-roads.md`
- `ボツ-12か月の運営/council/m03-run.json`
- `ボツ-12か月の運営/council/m03-survey-economy.md`
- `ボツ-12か月の運営/council/m03-survey-fire.md`
- `ボツ-12か月の運営/council/m03-survey-port.md`
- `ボツ-12か月の運営/council/m03-urban.md`
- `ボツ-12か月の運営/council/m04-bill.md`
- `ボツ-12か月の運営/council/m04-economy.md`
- `ボツ-12か月の運営/council/m04-education.md`
- `ボツ-12か月の運営/council/m04-finance.md`
- `ボツ-12か月の運営/council/m04-fire.md`
- `ボツ-12か月の運営/council/m04-guide.md`
- `ボツ-12か月の運営/council/m04-health.md`
- `ボツ-12か月の運営/council/m04-hooks.log`
- `ボツ-12か月の運営/council/m04-minutes.md`
- `ボツ-12か月の運営/council/m04-policy.md`
- `ボツ-12か月の運営/council/m04-port.md`
- `ボツ-12か月の運営/council/m04-roads.md`
- `ボツ-12か月の運営/council/m04-run.json`
- `ボツ-12か月の運営/council/m04-survey-economy.md`
- `ボツ-12か月の運営/council/m04-survey-health.md`
- `ボツ-12か月の運営/council/m04-survey-port.md`
- `ボツ-12か月の運営/council/m04-urban.md`
- `ボツ-12か月の運営/council/m05-assembly.json`
- `ボツ-12か月の運営/council/m05-assembly.md`
- `ボツ-12か月の運営/council/m05-bill.md`
- `ボツ-12か月の運営/council/m05-economy.md`
- `ボツ-12か月の運営/council/m05-education.md`
- `ボツ-12か月の運営/council/m05-finance.md`
- `ボツ-12か月の運営/council/m05-fire.md`
- `ボツ-12か月の運営/council/m05-guide.md`
- `ボツ-12か月の運営/council/m05-health.md`
- `ボツ-12か月の運営/council/m05-hooks.log`
- `ボツ-12か月の運営/council/m05-minutes.md`
- `ボツ-12か月の運営/council/m05-policy.md`
- `ボツ-12か月の運営/council/m05-port.md`
- `ボツ-12か月の運営/council/m05-roads.md`
- `ボツ-12か月の運営/council/m05-run.json`
- `ボツ-12か月の運営/council/m05-survey-health.md`
- `ボツ-12か月の運営/council/m05-survey-port.md`
- `ボツ-12か月の運営/council/m05-survey-roads.md`
- `ボツ-12か月の運営/council/m05-urban.md`
- `ボツ-12か月の運営/council/m06-assembly.json`
- `ボツ-12か月の運営/council/m06-assembly.md`
- `ボツ-12か月の運営/council/m06-bill.md`
- `ボツ-12か月の運営/council/m06-economy.md`
- `ボツ-12か月の運営/council/m06-education.md`
- `ボツ-12か月の運営/council/m06-finance.md`
- `ボツ-12か月の運営/council/m06-fire.md`
- `ボツ-12か月の運営/council/m06-guide.md`
- `ボツ-12か月の運営/council/m06-health.md`
- `ボツ-12か月の運営/council/m06-hooks.log`
- `ボツ-12か月の運営/council/m06-minutes.md`
- `ボツ-12か月の運営/council/m06-policy.md`
- `ボツ-12か月の運営/council/m06-port.md`
- `ボツ-12か月の運営/council/m06-roads.md`
- `ボツ-12か月の運営/council/m06-run.json`
- `ボツ-12か月の運営/council/m06-survey-economy.md`
- `ボツ-12か月の運営/council/m06-survey-health.md`
- `ボツ-12か月の運営/council/m06-survey-port.md`
- `ボツ-12か月の運営/council/m06-urban.md`
- `ボツ-12か月の運営/council/m07-assembly.json`
- `ボツ-12か月の運営/council/m07-assembly.md`
- `ボツ-12か月の運営/council/m07-bill.md`
- `ボツ-12か月の運営/council/m07-economy.md`
- `ボツ-12か月の運営/council/m07-education.md`
- `ボツ-12か月の運営/council/m07-finance.md`
- `ボツ-12か月の運営/council/m07-fire.md`
- `ボツ-12か月の運営/council/m07-guide.md`
- `ボツ-12か月の運営/council/m07-health-zonemap-west.jpg`
- `ボツ-12か月の運営/council/m07-health.md`
- `ボツ-12か月の運営/council/m07-hooks.log`
- `ボツ-12か月の運営/council/m07-minutes.md`
- `ボツ-12か月の運営/council/m07-policy.md`
- `ボツ-12か月の運営/council/m07-port.md`
- `ボツ-12か月の運営/council/m07-roads.md`
- `ボツ-12か月の運営/council/m07-run.json`
- `ボツ-12か月の運営/council/m07-survey-economy.md`
- `ボツ-12か月の運営/council/m07-survey-health.md`
- `ボツ-12か月の運営/council/m07-survey-roads.md`
- `ボツ-12か月の運営/council/m07-urban.md`
- `ボツ-12か月の運営/council/m08-assembly.json`
- `ボツ-12か月の運営/council/m08-assembly.md`
- `ボツ-12か月の運営/council/m08-bill.md`
- `ボツ-12か月の運営/council/m08-economy.md`
- `ボツ-12か月の運営/council/m08-education.md`
- `ボツ-12か月の運営/council/m08-finance.md`
- `ボツ-12か月の運営/council/m08-fire.md`
- `ボツ-12か月の運営/council/m08-guide.md`
- `ボツ-12か月の運営/council/m08-health.md`
- `ボツ-12か月の運営/council/m08-hooks.log`
- `ボツ-12か月の運営/council/m08-minutes.md`
- `ボツ-12か月の運営/council/m08-policy.md`
- `ボツ-12か月の運営/council/m08-port-cargo-map.jpg`
- `ボツ-12か月の運営/council/m08-port.md`
- `ボツ-12か月の運営/council/m08-roads.md`
- `ボツ-12か月の運営/council/m08-run.json`
- `ボツ-12か月の運営/council/m08-survey-economy.md`
- `ボツ-12か月の運営/council/m08-survey-education.md`
- `ボツ-12か月の運営/council/m08-survey-roads.md`
- `ボツ-12か月の運営/council/m08-urban.md`
- `ボツ-12か月の運営/council/m09-bill.md`
- `ボツ-12か月の運営/council/m09-economy.md`
- `ボツ-12か月の運営/council/m09-education.md`
- `ボツ-12か月の運営/council/m09-finance.md`
- `ボツ-12か月の運営/council/m09-fire.md`
- `ボツ-12か月の運営/council/m09-guide.md`
- `ボツ-12か月の運営/council/m09-health.md`
- `ボツ-12か月の運営/council/m09-hooks.log`
- `ボツ-12か月の運営/council/m09-minutes.md`
- `ボツ-12か月の運営/council/m09-policy.md`
- `ボツ-12か月の運営/council/m09-port.md`
- `ボツ-12か月の運営/council/m09-roads.md`
- `ボツ-12か月の運営/council/m09-run.json`
- `ボツ-12か月の運営/council/m09-survey-economy.md`
- `ボツ-12か月の運営/council/m09-survey-health.md`
- `ボツ-12か月の運営/council/m09-survey-port.md`
- `ボツ-12か月の運営/council/m09-urban.md`
- `ボツ-12か月の運営/council/m10-assembly.json`
- `ボツ-12か月の運営/council/m10-assembly.md`
- `ボツ-12か月の運営/council/m10-bill.md`
- `ボツ-12か月の運営/council/m10-economy.md`
- `ボツ-12か月の運営/council/m10-education.md`
- `ボツ-12か月の運営/council/m10-finance.md`
- `ボツ-12か月の運営/council/m10-fire.md`
- `ボツ-12か月の運営/council/m10-guide.md`
- `ボツ-12か月の運営/council/m10-health-zone-west.jpg`
- `ボツ-12か月の運営/council/m10-health.md`
- `ボツ-12か月の運営/council/m10-hooks.log`
- `ボツ-12か月の運営/council/m10-minutes.md`
- `ボツ-12か月の運営/council/m10-policy.md`
- `ボツ-12か月の運営/council/m10-port.md`
- `ボツ-12か月の運営/council/m10-roads.md`
- `ボツ-12か月の運営/council/m10-run.json`
- `ボツ-12か月の運営/council/m10-survey-economy.md`
- `ボツ-12か月の運営/council/m10-survey-health.md`
- `ボツ-12か月の運営/council/m10-survey-urban.md`
- `ボツ-12か月の運営/council/m10-urban.md`
- `ボツ-12か月の運営/council/m11-assembly.json`
- `ボツ-12か月の運営/council/m11-assembly.md`
- `ボツ-12か月の運営/council/m11-bill.md`
- `ボツ-12か月の運営/council/m11-economy.md`
- `ボツ-12か月の運営/council/m11-education.md`
- `ボツ-12か月の運営/council/m11-finance.md`
- `ボツ-12か月の運営/council/m11-fire.md`
- `ボツ-12か月の運営/council/m11-guide.md`
- `ボツ-12か月の運営/council/m11-health-map-garbage.jpg`
- `ボツ-12か月の運営/council/m11-health.md`
- `ボツ-12か月の運営/council/m11-hooks.log`
- `ボツ-12か月の運営/council/m11-minutes.md`
- `ボツ-12か月の運営/council/m11-policy.md`
- `ボツ-12か月の運営/council/m11-port.md`
- `ボツ-12か月の運営/council/m11-roads.md`
- `ボツ-12か月の運営/council/m11-run.json`
- `ボツ-12か月の運営/council/m11-survey-economy.md`
- `ボツ-12か月の運営/council/m11-survey-fire.md`
- `ボツ-12か月の運営/council/m11-survey-port.md`
- `ボツ-12か月の運営/council/m11-urban.md`
- `ボツ-12か月の運営/council/m12-assembly.json`
- `ボツ-12か月の運営/council/m12-assembly.md`
- `ボツ-12か月の運営/council/m12-bill.md`
- `ボツ-12か月の運営/council/m12-economy.md`
- `ボツ-12か月の運営/council/m12-education.md`
- `ボツ-12か月の運営/council/m12-finance.md`
- `ボツ-12か月の運営/council/m12-fire.md`
- `ボツ-12か月の運営/council/m12-guide.md`
- `ボツ-12か月の運営/council/m12-health-zone-w.jpg`
- `ボツ-12か月の運営/council/m12-health.md`
- `ボツ-12か月の運営/council/m12-hooks.log`
- `ボツ-12か月の運営/council/m12-minutes.md`
- `ボツ-12か月の運営/council/m12-policy.md`
- `ボツ-12か月の運営/council/m12-port.md`
- `ボツ-12か月の運営/council/m12-roads.md`
- `ボツ-12か月の運営/council/m12-run.json`
- `ボツ-12か月の運営/council/m12-survey-economy.md`
- `ボツ-12か月の運営/council/m12-survey-port.md`
- `ボツ-12か月の運営/council/m12-urban.md`
- `ボツ-12か月の運営/mayor-note.md`
- `ボツ-12か月の運営/transcripts/m01-assembly.md`
- `ボツ-12か月の運営/transcripts/m01-economy.md`
- `ボツ-12か月の運営/transcripts/m01-education.md`
- `ボツ-12か月の運営/transcripts/m01-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m01-finance.md`
- `ボツ-12か月の運営/transcripts/m01-fire.md`
- `ボツ-12か月の運営/transcripts/m01-health.md`
- `ボツ-12か月の運営/transcripts/m01-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m01-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m01-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m01-port.md`
- `ボツ-12か月の運営/transcripts/m01-roads.md`
- `ボツ-12か月の運営/transcripts/m01-urban.md`
- `ボツ-12か月の運営/transcripts/m02-assembly.md`
- `ボツ-12か月の運営/transcripts/m02-economy.md`
- `ボツ-12か月の運営/transcripts/m02-education.md`
- `ボツ-12か月の運営/transcripts/m02-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m02-finance.md`
- `ボツ-12か月の運営/transcripts/m02-fire.md`
- `ボツ-12か月の運営/transcripts/m02-health.md`
- `ボツ-12か月の運営/transcripts/m02-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m02-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m02-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m02-port.md`
- `ボツ-12か月の運営/transcripts/m02-roads.md`
- `ボツ-12か月の運営/transcripts/m02-urban.md`
- `ボツ-12か月の運営/transcripts/m03-economy.md`
- `ボツ-12か月の運営/transcripts/m03-education.md`
- `ボツ-12か月の運営/transcripts/m03-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m03-finance.md`
- `ボツ-12か月の運営/transcripts/m03-fire.md`
- `ボツ-12か月の運営/transcripts/m03-health.md`
- `ボツ-12か月の運営/transcripts/m03-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m03-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m03-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m03-port.md`
- `ボツ-12か月の運営/transcripts/m03-roads.md`
- `ボツ-12か月の運営/transcripts/m03-urban.md`
- `ボツ-12か月の運営/transcripts/m04-economy.md`
- `ボツ-12か月の運営/transcripts/m04-education.md`
- `ボツ-12か月の運営/transcripts/m04-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m04-finance.md`
- `ボツ-12か月の運営/transcripts/m04-fire.md`
- `ボツ-12か月の運営/transcripts/m04-health.md`
- `ボツ-12か月の運営/transcripts/m04-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m04-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m04-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m04-port.md`
- `ボツ-12か月の運営/transcripts/m04-roads.md`
- `ボツ-12か月の運営/transcripts/m04-urban.md`
- `ボツ-12か月の運営/transcripts/m05-assembly.md`
- `ボツ-12か月の運営/transcripts/m05-economy.md`
- `ボツ-12か月の運営/transcripts/m05-education.md`
- `ボツ-12か月の運営/transcripts/m05-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m05-finance.md`
- `ボツ-12か月の運営/transcripts/m05-fire.md`
- `ボツ-12か月の運営/transcripts/m05-health.md`
- `ボツ-12か月の運営/transcripts/m05-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m05-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m05-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m05-port.md`
- `ボツ-12か月の運営/transcripts/m05-roads.md`
- `ボツ-12か月の運営/transcripts/m05-urban.md`
- `ボツ-12か月の運営/transcripts/m06-assembly.md`
- `ボツ-12か月の運営/transcripts/m06-economy.md`
- `ボツ-12か月の運営/transcripts/m06-education.md`
- `ボツ-12か月の運営/transcripts/m06-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m06-finance.md`
- `ボツ-12か月の運営/transcripts/m06-fire.md`
- `ボツ-12か月の運営/transcripts/m06-health.md`
- `ボツ-12か月の運営/transcripts/m06-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m06-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m06-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m06-port.md`
- `ボツ-12か月の運営/transcripts/m06-roads.md`
- `ボツ-12か月の運営/transcripts/m06-urban.md`
- `ボツ-12か月の運営/transcripts/m07-assembly.md`
- `ボツ-12か月の運営/transcripts/m07-economy.md`
- `ボツ-12か月の運営/transcripts/m07-education.md`
- `ボツ-12か月の運営/transcripts/m07-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m07-finance.md`
- `ボツ-12か月の運営/transcripts/m07-fire.md`
- `ボツ-12か月の運営/transcripts/m07-health.md`
- `ボツ-12か月の運営/transcripts/m07-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m07-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m07-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m07-port.md`
- `ボツ-12か月の運営/transcripts/m07-roads.md`
- `ボツ-12か月の運営/transcripts/m07-urban.md`
- `ボツ-12か月の運営/transcripts/m08-assembly.md`
- `ボツ-12か月の運営/transcripts/m08-economy.md`
- `ボツ-12か月の運営/transcripts/m08-education.md`
- `ボツ-12か月の運営/transcripts/m08-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m08-finance.md`
- `ボツ-12か月の運営/transcripts/m08-fire.md`
- `ボツ-12か月の運営/transcripts/m08-health.md`
- `ボツ-12か月の運営/transcripts/m08-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m08-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m08-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m08-port.md`
- `ボツ-12か月の運営/transcripts/m08-roads.md`
- `ボツ-12か月の運営/transcripts/m08-urban.md`
- `ボツ-12か月の運営/transcripts/m09-economy.md`
- `ボツ-12か月の運営/transcripts/m09-education.md`
- `ボツ-12か月の運営/transcripts/m09-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m09-finance.md`
- `ボツ-12か月の運営/transcripts/m09-fire.md`
- `ボツ-12か月の運営/transcripts/m09-health.md`
- `ボツ-12か月の運営/transcripts/m09-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m09-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m09-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m09-port.md`
- `ボツ-12か月の運営/transcripts/m09-roads.md`
- `ボツ-12か月の運営/transcripts/m09-urban.md`
- `ボツ-12か月の運営/transcripts/m10-assembly.md`
- `ボツ-12か月の運営/transcripts/m10-economy.md`
- `ボツ-12か月の運営/transcripts/m10-education.md`
- `ボツ-12か月の運営/transcripts/m10-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m10-finance.md`
- `ボツ-12か月の運営/transcripts/m10-fire.md`
- `ボツ-12か月の運営/transcripts/m10-health.md`
- `ボツ-12か月の運営/transcripts/m10-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m10-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m10-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m10-port.md`
- `ボツ-12か月の運営/transcripts/m10-roads.md`
- `ボツ-12か月の運営/transcripts/m10-urban.md`
- `ボツ-12か月の運営/transcripts/m11-assembly.md`
- `ボツ-12か月の運営/transcripts/m11-economy.md`
- `ボツ-12か月の運営/transcripts/m11-education.md`
- `ボツ-12か月の運営/transcripts/m11-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m11-finance.md`
- `ボツ-12か月の運営/transcripts/m11-fire.md`
- `ボツ-12か月の運営/transcripts/m11-health.md`
- `ボツ-12か月の運営/transcripts/m11-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m11-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m11-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m11-port.md`
- `ボツ-12か月の運営/transcripts/m11-roads.md`
- `ボツ-12か月の運営/transcripts/m11-urban.md`
- `ボツ-12か月の運営/transcripts/m12-assembly.md`
- `ボツ-12か月の運営/transcripts/m12-economy.md`
- `ボツ-12か月の運営/transcripts/m12-education.md`
- `ボツ-12か月の運営/transcripts/m12-finance-guide.md`
- `ボツ-12か月の運営/transcripts/m12-finance.md`
- `ボツ-12か月の運営/transcripts/m12-fire.md`
- `ボツ-12か月の運営/transcripts/m12-health.md`
- `ボツ-12か月の運営/transcripts/m12-mayor-desk-see.md`
- `ボツ-12か月の運営/transcripts/m12-mayor-desk.md`
- `ボツ-12か月の運営/transcripts/m12-mayor-field.md`
- `ボツ-12か月の運営/transcripts/m12-port.md`
- `ボツ-12か月の運営/transcripts/m12-roads.md`
- `ボツ-12か月の運営/transcripts/m12-urban.md`
- `試し-改善後1か月目(1回目)/command-log.txt`
- `試し-改善後1か月目(1回目)/council/ledger-older.md`
- `試し-改善後1か月目(1回目)/council/ledger-recent.jsonl`
- `試し-改善後1か月目(1回目)/council/ledger.jsonl`
- `試し-改善後1か月目(1回目)/council/m01-assembly.json`
- `試し-改善後1か月目(1回目)/council/m01-assembly.md`
- `試し-改善後1か月目(1回目)/council/m01-bill-2.md`
- `試し-改善後1か月目(1回目)/council/m01-bill.md`
- `試し-改善後1か月目(1回目)/council/m01-economy.md`
- `試し-改善後1か月目(1回目)/council/m01-education-map.jpg`
- `試し-改善後1か月目(1回目)/council/m01-education.md`
- `試し-改善後1か月目(1回目)/council/m01-finance.md`
- `試し-改善後1か月目(1回目)/council/m01-fire.md`
- `試し-改善後1か月目(1回目)/council/m01-health.md`
- `試し-改善後1か月目(1回目)/council/m01-hooks.log`
- `試し-改善後1か月目(1回目)/council/m01-minutes.md`
- `試し-改善後1か月目(1回目)/council/m01-policy.md`
- `試し-改善後1か月目(1回目)/council/m01-port-map-coast.jpg`
- `試し-改善後1か月目(1回目)/council/m01-port.md`
- `試し-改善後1か月目(1回目)/council/m01-roads.md`
- `試し-改善後1か月目(1回目)/council/m01-run.json`
- `試し-改善後1か月目(1回目)/council/m01-survey-economy.md`
- `試し-改善後1か月目(1回目)/council/m01-survey-port.md`
- `試し-改善後1か月目(1回目)/council/m01-survey-roads.md`
- `試し-改善後1か月目(1回目)/council/m01-urban.md`
- `試し-改善後1か月目(1回目)/council/plan-city.md`
- `試し-改善後1か月目(1回目)/council/plan-economy.md`
- `試し-改善後1か月目(1回目)/council/plan-education.md`
- `試し-改善後1か月目(1回目)/council/plan-finance.md`
- `試し-改善後1か月目(1回目)/council/plan-fire.md`
- `試し-改善後1か月目(1回目)/council/plan-health.md`
- `試し-改善後1か月目(1回目)/council/plan-port.md`
- `試し-改善後1か月目(1回目)/council/plan-review.md`
- `試し-改善後1か月目(1回目)/council/plan-roads.md`
- `試し-改善後1か月目(1回目)/council/plan-urban.md`
- `試し-改善後1か月目(1回目)/mayor-note.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-assembly.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy-fix5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-economy.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-education-recheck.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-education.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance-fix5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-finance.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-fire.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-health-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-health-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-health.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-fix.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-planadj.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review0.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-review5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk-see.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-desk.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-mayor-field.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-port.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix2.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix3.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix4.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads-fix5.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-roads.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-urban-fix1.md`
- `試し-改善後1か月目(1回目)/transcripts/m01-urban.md`

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 9)
