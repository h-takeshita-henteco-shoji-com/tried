# 1か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 14:47〜14:54)

- 元のファイル: [m01-policy.md](m01-policy.md)
- ゲーム内の日付: 2050-01-01、保存: fukuoka-plan-m01
- 重点: 5-1、5-2 観光、8-1 物流・人流のゲートウェイ、6-3 公共交通を主軸とした交通体系

- 見たもの: [m01-policy.md の「見たもの」](m01-policy.md#見たもの)(15 行)
- 判断の根拠:

  公約4は市長の方針なので、観光を重点の1つ目に置く。残り2つは、市の計画の目標から遠い施策を選んだ。8-1 は506に対して目標250以下で、差がもっとも大きい。6-3 は51%に対して60%以上で、公約1の人口を支える移動にも関わる。ごみ(4-4)の満杯の埋立地7棟も気になるが、ごみの印は15で差が小さいため、今月は重点にしない。

- 捨てたもの:

  - 4-4 資源循環: 満杯の埋立地7棟は気がかりだが、ごみの印15と差が小さい。保健環境局の案としては出してよい
  - 6-4、7-1 企業の立地、地場企業: 品物がない店228は 8-1 の物流の改善で一緒に動く見込み
  - 3-3 安全で快適な生活基盤: 電気・水・下水が来ない市民は0で、目標を満たしている

## 2. 財政局: 今月の枠(hooks の記録で 14:48〜14:53)

- 元のファイル: [m01-guide.md](m01-guide.md)
- 建設費の上限 300000、週の維持費の増えの上限 4900、税の幅 ±2、予算の幅 ±20

## 3. 7つの局の案

### 住宅都市みどり局(urban)(hooks の記録で 14:48〜14:50)

- 元のファイル: [m01-urban.md](m01-urban.md)
- 案 urban-1: 街全体の娯楽の政策 RecreationalUse を試しでかける
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 4-1、5-1、5-2
  - 議決: 要らない

- 見たもの: [m01-urban.md の「見たもの」](m01-urban.md#見たもの)(19 行)
- 判断の根拠:

  - 担当の数字は、住宅(高密度)の地価 58(目標 62 以上)と、公園などの Beautification 81(目標 100 以上、市政ノートの値)。どちらも目標に届いていない
  - Beautification を増やす手は、建設費 1,000(Regular Park)で効きは大きいと見込める。しかし、空きがある場所を 12 回の試しで確かめたが、どれも別の建物か道路に当たった。取り壊しで働き口を失う案になるため、今月は採らない。次の月に、放棄された建物の跡を確かめる案を出す
  - 政策の RecreationalUse は、費用 0 で、取り壊しも建設もない。確認した事実は「費用 0、政策の一覧にある」の 2 つ。効きの方向と大きさは分からないため、試しとして 1 件出す。測る数は、担当の範囲の地価と、重点 5-1、5-2 の魅力度
  - 案の数は 1 件。ほかの候補は場所がなく、実行条件が確認できなかったため、件数を埋める案は出さない

- 捨てたもの: [m01-urban.md の「捨てたもの」](m01-urban.md#捨てたもの)(12 行)

### 道路下水道局(roads)(hooks の記録で 14:48〜14:51)

- 元のファイル: [m01-roads.md](m01-roads.md)
- 案 roads-1: 交通の流れの悪い区間(Basic Road)を4車線に差し替える
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 4方向の交差点(2152,560)に信号を付ける
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m01-roads.md の「見たもの」](m01-roads.md#見たもの)(30 行)
- 判断の根拠:

  - 6-3 の交通の流れは 51%(目標 60%以上)。閉塞は、西の 1 車線の交差点、(703,-686)、(2157,474) の 1 車線の道路に集まっている。
  - 案1 は、閉塞の多い 2 地区の 1 車線の道路を 4 車線に差し替える。Basic Road と Small 4 Lane Road は 1km あたりの建設費と維持費が同じなので、費用は 0 で、週の維持費も増えない。
  - 案2 は、4 方向が 1 車線の交差点に信号を付ける。道路を変えず、信号だけ付ける。効き目は見積もれないので試しにする。
  - 2 案は、道を太くする手と、信号で流す手で別の手にした。案の数は 2 件とした。どちらも道路の仕組みに当たるが、手が違う。
  - 西の 2280 本線の交差点は、短い 1 車線(36011、16m)が 4 車線の差し替えをふさいでいる。この区間の付け替えは取り壊しの議決が要り、道具の試しでも差し替えができないため、今月は案にしない。調査で閉塞の時間の動きを見る。
  - 貨物駅 28755 の止まりは、道の上の閉塞ではなく敷地の中の空き待ちで、周りの道は詰まっていない(`traffic` の blocked 0)。道を広げても効かないと見て、8-1 の案としては出さない。

- 捨てたもの: [m01-roads.md の「捨てたもの」](m01-roads.md#捨てたもの)(10 行)

### 港湾空港局(port)(hooks の記録で 14:48〜14:50)

- 元のファイル: [m01-port.md](m01-port.md)
- 案 port-1: 乗客の少ないバス路線の台数を減らす
  - 建設費 0、週の維持費 +-940、戻せる
  - 市の計画: 6-3
  - 議決: 要る(予算)

- 見たもの: [m01-port.md の「見たもの」](m01-port.md#見たもの)(20 行)
- 判断の根拠:

  - 8-1 の貨物駅 28755 の詰まり(492 台が敷地の中で空き待ち)は、出口につながる道が細く、勾配や工場に邪魔されて、今月は道の差し替えで直せない。道の差し替えは、取り壊しの議決を伴うか、断られるため案にしない。詰まりが続くかは、調査で見る。
  - 6-3 の交通の流れ 51%(目標 60%)に、バスの過剰が効いていると見た。バス 1,916 台に対し、乗客は少ない。今回は、乗客 2 人/台 未満の路線だけを、上限の ±20 で減らす。これは予算の手で、議決が要る。効き目は見積もれないので試しにする。
  - 案は 1 件にした。ほかの手は、道の差し替え(取り壊し・断り)、信号の付け替え(効き目と費用が未確認)、空港・港の新設(維持費 4,800/週 と 1,600/週 が、週の黒字 9,965 に比べて重い)。いずれも、今月の担当の問題に確かな効き目を示せない。

- 捨てたもの:

  - 貨物駅 28755 の出口道路を太くする案: 試しの道具が、勾配・隣の道・工場の取り壊しで断った。取り壊しを含む案は、今月の数字だけでは効き目と損失の釣り合いが取れない。調査の結果を見て出し直す。
  - 交差点 (3480,-1340) に信号を付ける案: 信号は付けられるが、効き目の見込みが薄く、費用を道具で確かめられない。
  - 空港の新設(Airport 150,000、維持 4,800/週): 週の黒字 9,965 を超える維持費になるため。観光の効き目も示せない。
  - HeavyTrafficBan(トラックを道路から締め出す政策): 費用は 0 だが、品物がない店 228 と原料がない工場 24 をさらに悪くするため。
  - 路線の台数の割合を一度に大きく下げる案(-50 など): 予算の上限が ±20 のため。来月も同じ手を続けて段階的に下げる。

### 経済観光文化局(economy)(hooks の記録で 14:48〜14:50)

- 元のファイル: [m01-economy.md](m01-economy.md)
- 案 economy-1: 東の商業街に名所 Friendly Neighborhood を1棟置く(道路の支線つき)
  - 建設費 20480、週の維持費 +324、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない
- 案 economy-2: 観光の街全体の政策 RecreationalUse をかける(試し)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m01-economy.md の「見たもの」](m01-economy.md#見たもの)(34 行)
- 判断の根拠:

  - 担当の数字: 観光客 1,646 は目標 3,000 に対して低い。Tourism の週の収入は 45 で、目標 1,000 から大きく離れる。名所は 6 で、目標 10 まで 4 つ足りない。attractiveness の平均は 6 で、目標 12 まで届かない。
  - 原因の見立て: 商業(高)の廃墟 114 棟のほとんどが品物がない店(NoGoods)で、店が営業しなければ観光客が落とすお金も増えない。品物の流れは 8-1 の港湾空港局の課題に当たるため、この局では調査にして、施策とは分けた。
  - 案1(名所): 名所を増やすのは観光の市の計画の施策(5-1、5-2)に当たる。場所は、取り壊しなしで置けて、道路の支線(約 90m)で接続できる東の商業の近くの空きを選んだ。費用は建設費 20,480、維持費の増え分は約 324 / 週で、枠の範囲内。ただし支線の施工後にしか入口の道路は確かめられず、未確認なので実行可否は未確認にした。
  - 案2(政策の試し): RecreationalUse は costPerWeek=0 で、議決が要らず、戻せる。政策の一覧には効果の記述しかないので、効き目は試しとして、attractiveness と Tourism で確かめる。
  - 案の数を 2 件にした理由: 名所の場所は、取り壊しを避けて置ける場所が少なく、確認できたのは東の 1 か所だけだった。確認できない場所を案にしないため。試しの政策は、ほかの手と別に効きを測れる。
  - 調査を 1 件出した理由: 品物がない店が 228 のまま減らない原因が、貨物駅 28755 の周りの渋滞か、道の上の混雑かが分からないため。月末の見る道具で止まったトラックを確かめる。

- 捨てたもの:

  - 名所 Countdown Clock(37,500、週 80)を東の商業の近くに置く案: 候補の 2765, 1010 は断られ(AlreadyExists)、別の場所では埋立地に重なるため、確認できる場所がなかった
  - 名所を 2 棟目以降に増やす案: 1 棟目の効きが分からないうちは、場所の確認ができた範囲で増やさない
  - 廃墟のホテル(5266、12373、44162)を取り壊して名所を置く案: 取り壊しの議決が要る。廃墟のホテルの周りには営業中の店が 11 棟あり、一緒に壊すと働き口 46 を失う。確かめた範囲では、取り壊さない手を先にする
  - 店の品物を増やすため、貨物駅 28755 の周りに道路や駅を足す案: 8-1 の港湾空港局の課題で、この局の案としては、原因を調査で確かめてから出す
  - 政策 BigBusiness や SmallBusiness の変更: 商業の需要は 2 で、店は足りている。品物がない店が増える理由は解消しないので、効き目が見込めない
  - 税率の変更: 担当の数字(観光、働き口、品物)に効くと確かめられる根拠がない

### 保健環境局(health)(hooks の記録で 14:48〜14:51)

- 元のファイル: [m01-health.md](m01-health.md)
- 案 health-1: 汚染の源の近くに木を植えて、汚染の印を減らす(試し)
  - 建設費 15000、週の維持費 +0、戻せる
  - 市の計画: 4-3
  - 議決: 要らない
- 案 health-2: 満杯の埋立地を2か所空けて、ごみを集めやすくする
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 4-4
  - 議決: 要らない
- 案 health-3: 禁煙の政策をかけて、健康の平均を上げる(試し)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 1-2
  - 議決: 要らない

- 見たもの: [m01-health.md の「見たもの」](m01-health.md#見たもの)(35 行)
- 判断の根拠:

  汚染の印 32 は目標 15 から遠く、燃焼工場 2267 と工業帯の周りの住宅に集まっている。案1は、木で汚染を吸わせる手で、費用が約 15,000 と小さい。効き目の大きさは確かめていないため試しにした。ごみの印 15 は、近くの埋立地が満杯なのが主な原因と見た。案2は、満杯の埋立地を空けて受け入れを戻す手で、費用が 0 で、空きの推定 35M に対して 16M の移動に収まる。案3は、禁煙の政策で健康の平均 78 を上げる試しで、政策の週の費用は 0 だが、効果は道具で確かめられない。死体の印 52 は、火葬場が近くに 3 つあり処理の容量も余っているため、増設ではなく霊柩車の渋滞が原因と見た。そこで調査にした。
  案を3件にした理由: 担当の3つの問題(汚染、ごみ、健康)に、それぞれ別の手で効く案を1つずつ出した。案1と案2は費用が小さく、即座に実行できる。案3は費用 0 だが効果が不確かなため、試しとして出した。ほかに実行できる案は、次の「捨てたもの」の理由で外した。

- 捨てたもの:

  - 政策「Recycling」(ごみ -15%、住宅の税 -5%): 住宅の税 265,121/週の 5% は約 13,256/週で、週の黒字 9,965 を超えて赤字になる。赤字は公約 3 に反するため、出さない。
  - 政策「HeavyTrafficBan」(トラックの通行を止める): 8-1 の物流(トラック 506 台が止まっている)を悪くする。汚染への効き目も確かめられない。編成方針の重点(8-1)と逆になるため、出さない。
  - 燃焼工場 2267 を移す、または止める: 中の量が 328,033/400,000(82%)で、ごみを処理する主力。止めるとごみが溜まり、ごみの印が増える。移す先の工業帯は、汚染が増えるため、汚染の源を移すだけになる。
  - 埋立地を新しく建てる(ごみの印の近く): 試した 5 か所は、道路と建物の詰まりで断られた。-620,-1620 は置けるが、住宅 3 棟(40 戸)を取り壊し、入口の道路も無い。取り壊しの議決を要し、住宅を失うため、今月は出さない(来月、道路と取り壊しの範囲を決め直して再検討する)。
  - 火葬場または墓地を新しく建てる(死体の印の近く): 2240,186 の近くに火葬場が 3 件(130m 以内)あり、処理の容量も余っている。増やしても霊柩車の渋滞は減らないため、効かないと見た。
  - 診療所を南東に建てる(健康の平均): 健康の範囲が 0 の南東は住宅が無く(zone_map)、建てても健康の住民が増えない。
  - 木を植える範囲を北へ広げる(燃焼工場の北側): 範囲の北側は住宅と道路が多く、本数が出ない見込み。案1の範囲を取り、次の月に決め直す。

### 教育委員会(education)(hooks の記録で 14:48〜14:48)

- 元のファイル: [m01-education.md](m01-education.md)
- 案: なし

- 見たもの:

  - `city_info`: 人口 178,872、所持金 2,082,287、週の収支 +9,965、幸福度 85、観光客 now 1,646 / visits 139、citizensWithoutService は電気・水・下水すべて 0
  - `services`: 小学校の定員 14,268、高校 24,360、大学 36,540。働き手 82,895、働き口 86,175。埋立地の満杯 7 棟(ごみ担当の問題で、教育とは関係なし)
  - `citizens_summary`: 子ども(child)11,344、10代(teen)22,372、若者 32,246、大人 68,040。大学卒の失業 6,483(失業の内訳で、10代・子どもは含まない)
  - `list_policies`: 政策の一覧を取得。教育に関係するのは EducationBoost(有効、週の費用 7,940。学校の維持費の +25% として教育の支出に入る)。ほかに、教育に直接かかる政策はなし。政策の費用の合計は 10,665 / 週

- 判断の根拠:

  担当の数字である学校の定員は、子ども・10代の数を両方上回っており、市の計画 2-3 の目標(12か月後も維持)を満たしている。目標を満たしている以上、学校を増やすと維持費だけが増え、効き目を測る数もない。原因が分からない問題もないため、調査も出さない。大学卒の失業 6,483 は働き口の問題で、経済観光文化局の担当である。大学の定員は足りているため、教育の手で直せる見込みはない。EducationBoost の解除は週 7,940 の支出を減らすが、教育の質への効きを道具で確かめられず、担当の数字にも表れないため、今月は案にしない。以上より、案なしとする。

- 捨てたもの:

  - 小学校・高校の新設: 定員は子ども・10代の数を上回っている。新設は維持費だけを増やし、目標(定員が年齢層を下回らないこと)にも効かない。
  - 大学の新設: 大学の定員 36,540 は足りており、大学卒の失業 6,483 は働き口の不足で、学校の数では直らない。働き口の問題は経済観光文化局の案として扱う。
  - EducationBoost の解除(週 7,940 の削減): 教育の質への効きを測る道具がなく、担当の数字(定員と年齢層)にも表れない。政策の判断は財政面から市長が決める。
  - 学校の取り壊し: 定員を減らし、目標を悪くする。取り壊しは戻せないため、採らない。

### 消防局(fire)(hooks の記録で 14:48〜14:49)

- 元のファイル: [m01-fire.md](m01-fire.md)
- 案 fire-1: 火事の印の近くに消防署を置く(店2軒を取り壊す)
  - 建設費 12000、週の維持費 +560、戻せない
  - 市の計画: 3-4
  - 議決: 要る(取り壊し)
- 案 fire-2: 犯罪の印の近くに警察署を置く(高層住宅2棟を取り壊す・試し)
  - 建設費 12000、週の維持費 +480、戻せない
  - 市の計画: 3-4
  - 議決: 要る(取り壊し)
- 案 fire-3: 禁煙の政策を試す(火事の印を測る・試し)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 3-4
  - 議決: 要らない

- 見たもの: [m01-fire.md の「見たもの」](m01-fire.md#見たもの)(21 行)
- 判断の根拠:

  火事 4 と犯罪 3 は合わせて 7 で、目標 4 以下に 3 足りません。案1は、火事の建物 villa 41298(3305.7, 644)に最も近い消防署が約980m 離れていることを根拠にします。(3300, 600) の消防署は、道路に面して1つだけ置けました。案2は、犯罪の建物 2 軒が警察署の近くに入ることを根拠にします。(2300, 850) の警察署は道路に面しますが、高層住宅2棟(家44)を取り壊します。取り壊しは失う家が大きいため、試しとして出し、市長が採るかを決めます。案3は、費用0で、火事への効きを仮説として測るために出します。政策は火事に関係する3つのうち、週 57,718 の SmokeDetectors を除外し、費用0の SmokingBan のみを候補にしました。案は3件です。ほかの手として、消防の予算を増やす案は、火事や犯罪の数が消防や警察の容量の不足で増えている証拠がないため出しませんでした。調査は、火事の印が消防署の距離で減るかを、見回りと月末に見るために1件出します。

- 捨てたもの:

  - 消防署(Fire Station、建設 60,000、週 1,440)を置く案: 火事の数が 4 と少ないため、容量の大きさに見合わない。Fire House で足りると判断した。
  - 警察本部(Police Headquarters、建設 60,000、週 1,600)を置く案: 犯罪の数が 3 と少ないため、同じ理由で見送った。
  - SmokeDetectors の政策: 週 57,718 で、週の維持費の上限 4,900 を超えるため、実行できない。
  - 消防・警察の予算を増やす案: 容量の使用は警察 446/960 と余裕があり、予算を増やす根拠がない。予算の案は議決が要るため、今月は出さない。
  - 警察署を道路沿いの空きに置く案(2290, 900、2120, 900、2200, 780、2300, 860、3380, 660): 入口の道路がなく、道路を引く工事が要るため、今月は確かめた範囲で採らなかった。
  - 犯罪の建物の近くの空きに置く案(2260, 728、2180, 752、2330, 752、2300, 842、2200, 842、2340, 842): 建物か道路とぶつかって断られた。

## 4. 財政局: 査定

- 元のファイル: [m01-finance.md](m01-finance.md)
- urban-1: 可。政策 RecreationalUse の1件で、costPerWeek 0。建設費0、維持費の増え分0で上限に収まる。
- roads-1: 可。Basic Road と Small 4 Lane Road は同じ 5,000/km・40/km/週で差額0。建設費0、維持費の増え分0。
- roads-2: 不可。信号の建設費と維持費を道具で確かめられず、上限に当てられない。費用を確かめてから出し直す。
- port-1: 減額。建設費0で維持費は減る方向。ただし line 136(乗客34)と line 127(乗客41)は案の中止条件(乗客30超は外す)に当たるため、この2本を外して17本にする。
- economy-2: 減額。RecreationalUse は costPerWeek 0 だが urban-1 と同じ政策で、政策の変更は1つまでのため、urban-1 と1回にまとめる。
- health-1: 可。木の建設費は約15,000(1本10 × 約1,500本)で上限内。維持費は道具で確かめられないが、週3,860を超えなければ上限に収まる。
- health-2: 可。empty_building は建設費も維持費も増やさず、増え分0。
- health-3: 減額。SmokingBan は costPerWeek 0 だが、urban-1 の RecreationalUse と合わせると政策の変更が2つになるため、どちらか1つを市長が選ぶ。
- fire-1: 可。Fire House の建設費12,000、維持費の増え分560で、上限内。取り壊し2軒は議決の対象で、財政の査定の外。
- fire-2: 可。Police Station の建設費12,000、維持費の増え分480で、上限内。取り壊す住宅44戸の税への影響は見積もっていない。
- fire-3: 減額。SmokingBan は費用0だが、health-3 と同じ政策で政策の変更は1つまでのため、health-3 と1回にまとめる。
- 税の案: なし
- 市長が選ぶときの上限: 300000

- 見たもの: [m01-finance.md の「見たもの」](m01-finance.md#見たもの)(9 行)
- 判断の根拠:

  週の収支は +9,965 の黒字で、所持金も多い。建設費の合計は 39,000 で、上限の 300,000 に収まる。政策の変更は1つまでという型の上限があり、RecreationalUse と SmokingBan の2種類を同時に入れられないため、どちらか1つを市長が選ぶ形にした。

- 捨てたもの:

  - economy-1(経済観光文化局: 名所 Friendly Neighborhood の新設): 査定対象外。実行可否が未確認で、入口の道路は支線の施工後にしか確かめられないため。案が出し直されたときに査定する。
  - roads-2 の「可」: 信号の費用を確かめられないため、可にしなかった。不可にして、費用を確かめてから出し直す形にした。
  - health-3 と fire-3 の「可」: 同じ SmokingBan を2件とも通すと、政策の変更が2種類(RecreationalUse と合わせて)になり、上限を超える。どちらも減額にした。
  - port-1 の「可」: 案の中止条件に当たる line 136 と line 127 を含めると、案の条件と合わない。2本を外す減額にした。
  - fire-2 の取り壊し44戸: 費用の上限には収まるが、住宅税への影響は見積もっていない。取り壊しの議決は別に必要。

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m01-bill.md](m01-bill.md)
- 採った m01-1: 街全体の政策 RecreationalUse を試しでかける(元 urban-1,economy-2、議決は要らない)
- 採った m01-2: 1車線の3か所を4車線に差し替える(元 roads-1、議決は要らない)
- 採った m01-3: 汚染の源の近くに木を植える(元 health-1、議決は要らない)
- 採った m01-4: 満杯の埋立地を2か所空ける(元 health-2、議決は要らない)
- 採った m01-5: 火事の印の近くに消防署を置く(元 fire-1、議決が要る(取り壊し))
- 採った m01-6: 犯罪の印の近くに警察署を置く(元 fire-2、議決が要る(取り壊し))
- 採らなかった roads-2: 信号の費用が未確認で査定が不可。m01-2と同じ周辺のblockedを測り場所が重なる
- 採らなかった port-1: 測る数の街全体のflowがm01-2の2地点と重なる。路線の経路を調べ、来月に絞って出し直す
- 採らなかった health-3: 政策の変更は今月1つまで。観光が重点のためm01-1のRecreationalUseを選んだ
- 採らなかった fire-3: health-3と同じSmokingBanで、同じ理由により採らない
- 採らなかった economy-1: 実行可否が未確認で、支線の施工後でないと入口の道路を確かめられない

- 見たもの:

  - `test_place_building`(Fire House、3300,600,north): ok、道路 18595、費用 12,000、取り壊し 2 棟(働き口 32、家 0)
  - `test_place_building`(Police Station、2300,850,south): ok、道路 26130、費用 12,000、取り壊し 2 棟(家 44、働き口 0)
  - `test_upgrade_road`(Small 4 Lane Road、[[700,-440],[700,-530],[640,-530]]): upgraded 3、skipped 0、cost 0
  - 局の案7件と調査、査定調書、編成方針、予算編成要領、`tool-reference.md`(set_policy、upgrade_road、plant_trees、empty_building、place_building の引数)

- 判断の根拠:

  重点は観光(5-1、5-2)、物流(8-1)、交通(6-3)。観光は m01-1 の試しで、交通は m01-2 で動く。8-1 は貨物駅の敷地の中の待ちで、道の手が効かないと局が見ており、原因が分かるまで調査 s01-1 にとどめた。建設費は 39,000 で、上限 300,000 に収まる。週の維持費の増え分は 1,040(木の維持費は未確認)で、上限 4,900 に収まる。政策の変更は m01-1 の1つ。測る数が重ならないよう、交通の試しは m01-2 に絞り、port-1 は来月に回した。

- 捨てたもの:

  - port-1(バス台数の削減): 週の維持費を約 700 減らせるが、m01-2 と測る場所が重なる。来月に絞り直す。
  - SmokingBan(health-3、fire-3): 政策は今月1つまで。観光の試しを優先した。
  - roads-2(信号): 費用が未確認で、m01-2 と場所が重なる。
  - economy-1(名所 Friendly Neighborhood): 入口の道路が未確認。名所の棟数(6 → 10)は来月以降に出し直しを待つ。
  - 8-1 の重点に当たる施策: 局の案がなく、調査 s01-1 だけを採った。市長が代案は作らない。

## 6. 議会: 可決と否決

- 元のファイル: [m01-assembly.md](m01-assembly.md)
- m01-5 取り壊し: 可決。失うもの(店2軒、働き口32、家0)が数字で書かれ、代わりの手とも比べている。響きは0.04%で小さい。
- m01-6 取り壊し: 可決。失うもの(高層住宅2棟、家44)と人口への響きが書かれ、空き家4,935戸で受け止められる。代わりの手とも比べている。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `m01-bill.md`: 議決が要る議案は m01-5 と m01-6 の取り壊し2件。ほかの m01-1〜4 は議決が要らないため見ない
  - `m01-bill.md` の「見たもの」: 市長の `test_place_building` で、失う働き口32と家44を確認済み

- 判断の根拠:

  1か月目なので、点3(外れた手の継続)に当たる前月の記録はない。点4では、貨物港など計画の目標に関わる建物は壊さない。取り壊しの2件は、失うものが数字で書かれ、代わりの手と比べ、響き(人口、働き口)も書かれている。型の上限と費用の高さは財政局の査定の範囲なので見直さない。

- 捨てたもの:

  - m01-6: 家44を失い戻せないため否決も考えた。空き家が多く、人口への響きを書いているので可決にした。

## 7. 実行する市長: 実行と見回り(hooks の記録で 14:56〜15:03)

- 実行してよい施策: m01-1、m01-2、m01-3、m01-4、m01-5、m01-6
- 実行した: m01-1、m01-2、m01-3、m01-4、m01-5、m01-6
- 失敗した: なし
- 臨時: なし
- 見回り 2050-01-11: 人口 178808、所持金 2057196、週の収支 5815、幸福度 85
- 見回り 2050-01-21: 人口 178707、所持金 2067511、週の収支 7400、幸福度 85
- 報告:

  議案の6件をすべて計画どおり実行した。m01-1 は RecreationalUse をかけた。費用は 0 だった。m01-2 は 3 か所を 4 車線にした。事前の test と本番はどちらも upgraded 3/1/1、費用 0。m01-3 は木 898 本を植えた。費用は 8,980。m01-4 は埋立地 16914 と 23032 を空け、20 日目に満杯が 7 から 5 に減ったので受け入れを戻した。m01-5 は Fire House(id 49063)を置いた。取り壊しは 27549 と 42278 のみ、費用 12,000。m01-6 は Police Station(id 4636)を置いた。取り壊しは 11247 と 36659 のみ、費用 12,000。見回りでは境目に当たらず、臨時もなかった。月末の数字は次のとおり。人口 178,861(月初 178,872。わずかに減)、所持金 2,077,453、週の収支 +6,910(黒字を維持)、観光客 1,633/144(月初 1,646/139)、Tourism 44(月初 45)、attractiveness の平均 6(変わらず)。したがって公約1(人口)と公約4(観光)は、月初より増えていない。交通は (703,-600) の blocked が 50 から 13、(2157,474) が 36 から 0 に減った。ただし街全体の流れは 52% でほぼ変わらない。汚染の印は 32 から 30。ごみの印は 15 から 26 に増えた。死体の印は 52 から 38 に減った。火事の印は 4 のまま。調査 s01-1 から s01-3 は council/m01-survey-*.md に記録した。港の貨物駅の待ちは約 500 台のまま減らなかった。hooks に止められた手はなかった。保存は人に頼まれていないため行っていない。市政ノートとログは更新済み。"

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m01、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-28 14:46〜15:13(hooks の記録の時刻から)、道具の行 314
- 議会が可決した種類: 取り壊し
- 議決が要る道具の呼び出し: 0 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 145 件
- hooks の拒否: 0 回

#### 運営のフォルダで、決まりの外の変更(git status)

- `council-aborted-1/m01-economy.md`
- `council-aborted-1/m01-education.md`
- `council-aborted-1/m01-fire.md`
- `council-aborted-1/m01-guide.md`
- `council-aborted-1/m01-health.md`
- `council-aborted-1/m01-hooks.log`
- `council-aborted-1/m01-policy.md`
- `council-aborted-1/m01-port.md`
- `council-aborted-1/m01-roads.md`
- `run-haiku45-bureaus/command-log.txt`
- `run-haiku45-bureaus/ledger.jsonl`
- `run-haiku45-bureaus/m01-bill.md`
- `run-haiku45-bureaus/m01-economy.md`
- `run-haiku45-bureaus/m01-education.md`
- `run-haiku45-bureaus/m01-finance.md`
- `run-haiku45-bureaus/m01-fire.md`
- `run-haiku45-bureaus/m01-guide.md`
- `run-haiku45-bureaus/m01-health.md`
- `run-haiku45-bureaus/m01-hooks.log`
- `run-haiku45-bureaus/m01-minutes.md`
- `run-haiku45-bureaus/m01-policy.md`
- `run-haiku45-bureaus/m01-port.md`
- `run-haiku45-bureaus/m01-roads.md`
- `run-haiku45-bureaus/m01-run.json`
- `run-haiku45-bureaus/m01-survey-economy.md`
- `run-haiku45-bureaus/m01-survey-roads.md`
- `run-haiku45-bureaus/m01-survey-urban.md`
- `run-haiku45-bureaus/m01-urban.md`
- `run-haiku45-bureaus/mayor-note.md`
- `run-haiku45-bureaus/transcripts/m01-economy.md`
- `run-haiku45-bureaus/transcripts/m01-education.md`
- `run-haiku45-bureaus/transcripts/m01-finance-guide.md`
- `run-haiku45-bureaus/transcripts/m01-finance.md`
- `run-haiku45-bureaus/transcripts/m01-fire.md`
- `run-haiku45-bureaus/transcripts/m01-health.md`
- `run-haiku45-bureaus/transcripts/m01-mayor-desk-see.md`
- `run-haiku45-bureaus/transcripts/m01-mayor-desk.md`
- `run-haiku45-bureaus/transcripts/m01-mayor-field.md`
- `run-haiku45-bureaus/transcripts/m01-port.md`
- `run-haiku45-bureaus/transcripts/m01-roads.md`
- `run-haiku45-bureaus/transcripts/m01-urban.md`
- `run-haiku55-bureaus/command-log.txt`
- `run-haiku55-bureaus/ledger.jsonl`
- `run-haiku55-bureaus/m01-bill.md`
- `run-haiku55-bureaus/m01-economy.md`
- `run-haiku55-bureaus/m01-education-zonemap.jpg`
- `run-haiku55-bureaus/m01-education.md`
- `run-haiku55-bureaus/m01-finance.md`
- `run-haiku55-bureaus/m01-fire.md`
- `run-haiku55-bureaus/m01-guide.md`
- `run-haiku55-bureaus/m01-health-garbage-map.jpg`
- `run-haiku55-bureaus/m01-health.md`
- `run-haiku55-bureaus/m01-hooks.log`
- `run-haiku55-bureaus/m01-minutes.md`
- `run-haiku55-bureaus/m01-policy.md`
- `run-haiku55-bureaus/m01-port.md`
- `run-haiku55-bureaus/m01-roads-cargo-map.jpg`
- `run-haiku55-bureaus/m01-roads.md`
- `run-haiku55-bureaus/m01-run.json`
- `run-haiku55-bureaus/m01-survey-fire.md`
- `run-haiku55-bureaus/m01-survey-roads.md`
- `run-haiku55-bureaus/m01-survey-urban.md`
- `run-haiku55-bureaus/m01-urban.md`
- `run-haiku55-bureaus/mayor-note.md`
- `run-haiku55-bureaus/transcripts/m01-economy.md`
- `run-haiku55-bureaus/transcripts/m01-education.md`
- `run-haiku55-bureaus/transcripts/m01-finance-guide.md`
- `run-haiku55-bureaus/transcripts/m01-finance.md`
- `run-haiku55-bureaus/transcripts/m01-fire.md`
- `run-haiku55-bureaus/transcripts/m01-health.md`
- `run-haiku55-bureaus/transcripts/m01-mayor-desk-see.md`
- `run-haiku55-bureaus/transcripts/m01-mayor-desk.md`
- `run-haiku55-bureaus/transcripts/m01-mayor-field.md`
- `run-haiku55-bureaus/transcripts/m01-port.md`
- `run-haiku55-bureaus/transcripts/m01-roads.md`
- `run-haiku55-bureaus/transcripts/m01-urban.md`
- `run-sonnet-bureaus/command-log.txt`
- `run-sonnet-bureaus/ledger.jsonl`
- `run-sonnet-bureaus/m01-assembly.json`
- `run-sonnet-bureaus/m01-assembly.md`
- `run-sonnet-bureaus/m01-bill.md`
- `run-sonnet-bureaus/m01-economy.md`
- `run-sonnet-bureaus/m01-education.md`
- `run-sonnet-bureaus/m01-finance.md`
- `run-sonnet-bureaus/m01-fire.md`
- `run-sonnet-bureaus/m01-guide.md`
- `run-sonnet-bureaus/m01-health.md`
- `run-sonnet-bureaus/m01-hooks.log`
- `run-sonnet-bureaus/m01-minutes.md`
- `run-sonnet-bureaus/m01-policy.md`
- `run-sonnet-bureaus/m01-port.md`
- `run-sonnet-bureaus/m01-roads.md`
- `run-sonnet-bureaus/m01-run.json`
- `run-sonnet-bureaus/m01-survey-economy.md`
- `run-sonnet-bureaus/m01-survey-health.md`
- `run-sonnet-bureaus/m01-survey-port.md`
- `run-sonnet-bureaus/m01-urban.md`
- `run-sonnet-bureaus/mayor-note.md`
- `run-sonnet-bureaus/transcripts/m01-assembly.md`
- `run-sonnet-bureaus/transcripts/m01-economy.md`
- `run-sonnet-bureaus/transcripts/m01-education.md`
- `run-sonnet-bureaus/transcripts/m01-finance-guide.md`
- `run-sonnet-bureaus/transcripts/m01-finance.md`
- `run-sonnet-bureaus/transcripts/m01-fire.md`
- `run-sonnet-bureaus/transcripts/m01-health.md`
- `run-sonnet-bureaus/transcripts/m01-mayor-desk-see.md`
- `run-sonnet-bureaus/transcripts/m01-mayor-desk.md`
- `run-sonnet-bureaus/transcripts/m01-mayor-field.md`
- `run-sonnet-bureaus/transcripts/m01-port.md`
- `run-sonnet-bureaus/transcripts/m01-roads.md`
- `run-sonnet-bureaus/transcripts/m01-urban.md`
- `trial-month1-haiku55-tuned/ledger.jsonl`
- `trial-month1-haiku55-tuned/m01-assembly.json`
- `trial-month1-haiku55-tuned/m01-assembly.md`
- `trial-month1-haiku55-tuned/m01-bill.md`
- `trial-month1-haiku55-tuned/m01-economy.md`
- `trial-month1-haiku55-tuned/m01-education.md`
- `trial-month1-haiku55-tuned/m01-finance.md`
- `trial-month1-haiku55-tuned/m01-fire.md`
- `trial-month1-haiku55-tuned/m01-guide.md`
- `trial-month1-haiku55-tuned/m01-health.md`
- `trial-month1-haiku55-tuned/m01-hooks.log`
- `trial-month1-haiku55-tuned/m01-minutes.md`
- `trial-month1-haiku55-tuned/m01-policy.md`
- `trial-month1-haiku55-tuned/m01-port.md`
- `trial-month1-haiku55-tuned/m01-roads.md`
- `trial-month1-haiku55-tuned/m01-run.json`
- `trial-month1-haiku55-tuned/m01-survey-health.md`
- `trial-month1-haiku55-tuned/m01-survey-port.md`
- `trial-month1-haiku55-tuned/m01-survey-roads.md`
- `trial-month1-haiku55-tuned/m01-urban.md`
- `trial-month1-haiku55-tuned/mayor-note.md`
- `trial-month1-haiku55-tuned/transcripts/m01-assembly.md`
- `trial-month1-haiku55-tuned/transcripts/m01-economy.md`
- `trial-month1-haiku55-tuned/transcripts/m01-education.md`
- `trial-month1-haiku55-tuned/transcripts/m01-finance-guide.md`
- `trial-month1-haiku55-tuned/transcripts/m01-finance.md`
- `trial-month1-haiku55-tuned/transcripts/m01-fire.md`
- `trial-month1-haiku55-tuned/transcripts/m01-health.md`
- `trial-month1-haiku55-tuned/transcripts/m01-mayor-desk-see.md`
- `trial-month1-haiku55-tuned/transcripts/m01-mayor-desk.md`
- `trial-month1-haiku55-tuned/transcripts/m01-mayor-field.md`
- `trial-month1-haiku55-tuned/transcripts/m01-port.md`
- `trial-month1-haiku55-tuned/transcripts/m01-roads.md`
- `trial-month1-haiku55-tuned/transcripts/m01-urban.md`

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 13)
