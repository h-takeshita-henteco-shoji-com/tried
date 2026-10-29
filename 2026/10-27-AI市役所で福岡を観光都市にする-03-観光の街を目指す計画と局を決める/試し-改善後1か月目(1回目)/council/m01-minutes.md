# 1か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 08:14〜08:14)

- 元のファイル: [m01-policy.md](m01-policy.md)
- ゲーム内の日付: 2050-01-01、保存: fukuoka-plan-m01
- 重点: 5-1、5-2 観光、6-3 公共交通を主軸とした交通体系、8-1 物流・人流のゲートウェイ

- 見たもの: [m01-policy.md の「見たもの」](m01-policy.md#見たもの)(17 行)
- 判断の根拠:

  公約1〜3は出発点で満たしているので、遠い数字を優先する。観光客 1,646、Tourism 週45、旅客の入口0棟は、目標との差が最も大きい。交通の流れ 51% と、敷地内の止まったトラック 506台が、次に遠い。港湾空港局が観光の入口と物流の両方を担当するため、8-1 を重点に入れ、手を合わせる。

- 捨てたもの:

  - 4-4 資源循環: ごみの印は 15、満杯の埋立地 7。目標0に遠いが、観光と交通を先にする。局の案は受ける
  - 4-3 脱炭素社会: 汚染の印 32(目標 15以下)。今月は重点にしない。局の案は受ける
  - 6-4、7-1 企業の立地: 品物がない店 228、原料がない工場 24。8-1 の物流が進めば連動して減る見込みで、今月は重点にしない
  - 4-2 花や緑による潤い: 公園など 81棟(目標 100以上)。観光の名所の案と合わせて、局が出す

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

### 住宅都市みどり局(urban)(hooks の記録で 08:15〜08:24)

- 元のファイル: [m01-urban.md](m01-urban.md)
- 案 urban-1: 空き地3に公園1棟と幹線・送電線を引く
  - 建設費 9780、週の維持費 +79、戻せる
  - 市の計画: 4-2
  - 議決: 要らない

- 見たもの: [m01-urban.md の「見たもの」](m01-urban.md#見たもの)(7 行)
- 判断の根拠:

  指摘1: 空き地3(712,1644)から、道路網の node 1812(-346,1441)まで、Basic Road を試しで引けた(断りなし、費用 7,700、橋 3区間)。始点は公園の入口から12m西にずらし、公園との重なりを避けた。送電線も試しで引けた(費用 1,080)。道路が引けたので、案1 の実行条件が確認できた。
  指摘2: 取り壊しを使う5か所を、assume_removed_buildings 付きで試した。道路・現役の建物にぶつかるか、家 36 または働き口 32 を失うため、取り壊しの案は今は出さない。取り壊しの議決は、置ける候補が見つかった月に出す。
  指摘3: 公園20棟の費用に、幹線と送電線の費用を足した(plan-urban.md の事業の費用)。建設費 約31,500、週の維持費 約295。
  案の数は1件とした。2棟目以降は、幹線が建ってから、入口の位置を試す必要がある。今の時点で案にすると、実行できない案になる。

- 捨てたもの:

  - 空き地3(712,1644)に公園を置く案を、道路なしで出す案: 幹線の経路が確かめられたため、道路つきの案1 にした
  - 放棄された店の跡(-696,132)、(2150,820)、(2152,900)、(2300,1000)に公園を置く案: 道路・現役の建物にぶつかるか、家 36 を失う。取り壊しの案にはしない
  - (-648,40)に広場を置く案: 現役の建物を4棟取り壊し、働き口 32 を失う
  - (1780,1388)へ幹線を引く案: 風車 25669 と警察 33595 にぶつかる。案1 の幹線で足りる
  - 灰色の空き(2240,522)、(2525,522)、(1200,-1200)、(2575,1224)、(-1000,1350): 前の月と同じ。埋立地、取り壊しで家を失う、海の上、建物と道路に重なる、のいずれか
  - 2棟目以降の公園の案: 幹線が建ってから、入口の位置を試す。今月は出さない
  - 政策の変更: 今月は政策一覧を取り直していない。4-2、4-1 に効く政策は、前の月に見た一覧にない

### 道路下水道局(roads)(hooks の記録で 08:15〜08:39)

- 元のファイル: [m01-roads.md](m01-roads.md)
- 案 roads-1: 止まりの多い交差点 (2110, 330) に信号を1基付ける
  - 建設費 208287、週の維持費 +468、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m01-roads.md の「見たもの」](m01-roads.md#見たもの)(39 行)
- 判断の根拠:

  - 担当の数字は、交通の流れ 51%(目標 60%)。止まった車は 1,008台。電気・水・下水が来ない市民は 0 で、今は達成している
  - 止まりの局所的な集まりを3つ見た。(2150, 350) の周り、半径 250 に止まった車が 163台で、そのうち交差点 (2110, 330) が近い。信号は道具で付けられる(canEnableLights=true)
  - 是正(第2回): 信号の建設費と維持費は道具で確かめられない。1基目を付けて、前後の所持金と週の支出を測ってから2基目を決める。1基目の上限は、所持金の余力 208,287 と、財政局の1月の表の余力 468 にする
  - 是正(第3回): 信号の費用は、道具の一覧にも既存の施設の記録にもない。見積もりの代わりに上限(建設費 208,287、週 468)を書いた。財政局は、この上限を超えるかどうかで置く可否を判定する。実際の額は、置いた後の差で確かめる
  - 2280付近の狭まりは、広げ直しで効きそうだが、取り壊しの議決が要る。失うゾーニングは、36011 だけの数が数えられないので、今月は案にせず、調査で見る
  - 是正(第2回): 事業3の道は、道具の試しで通った。駅と空港の道は、建物の翌月に引く。島の橋と水道管は、試しで通ったが 47,420 で、経済観光文化局の 42,500 より多い
  - 是正(第3回): 島Bの橋と水道管は、5月に引く形にした。名所の前月にあたる。他局との合意は、局では確かめられない。市長の調整で確かめる
  - 是正(第4回): 島Bの橋と水道管は7月に引く(財政局の表に合わせた)。名所は8月。費用は 47,420 のまま。4車線化は9月に実行し、取り壊しの議決は8月の議会に出す(計画の事業2)。流れの積み上げは、`traffic` の範囲の外の3か所(138台)で書いた。届く見込みは未確認(計画の「流れの積み上げ」)
  - 案は1件だけにした。ほかの候補は、手として効く見込みがないか、実行条件が確認できないか、今月の根拠が足りないため、捨てた

- 捨てたもの:

  - 2280付近の狭まりを4車線にする案(取り壊し): 36011 の取り壊しで、失うゾーニング(事務所・商業・工業)の数が数えられない。取り壊しの議決も要る。調査で止まりが続くと分かってから出す
  - (2236, -905)〜(2236, -860) の区間を4車線にする案: 消防署と診療所が衝突で断られた。サービスの建物は壊せないため、実行できない
  - HeavyTrafficBan(政策): 維持費は 0 だが、トラックが街の道を通れなくなり、品物がない店 228(6-4、7-1 の担当)を増やすおそれがある。局の担当の外の数字が悪くなるため、採らない
  - FreeTransport(政策): 運賃の収入が 0 になる。交通の流れには直接効かない。採らない
  - (-726, -736) の大通りの案: 原因が分からない(交差点がなく、止まりは道の途中)。今月は調査で確かめる
  - (2280, -950) の交差点に信号を付ける案: 入口が2本しかないため、信号の効きが見込めない。広げ直しの案で扱う
  - 2基同時に付ける案(1か月目): 信号の費用が未確認のまま2基を付けると、財政局の1月の表の余力 468 を超えるおそれがあるため、1基目の結果を待つ形に直した

### 港湾空港局(port)(hooks の記録で 08:15〜08:33)

- 元のファイル: [m01-port.md](m01-port.md)
- 案 port-1: 公共交通の運賃を0にして、交通の流れを試す
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m01-port.md の「見たもの」](m01-port.md#見たもの)(45 行)
- 判断の根拠:

  - 担当の数字の現状: 交通の流れ 51%(目標 60%)、旅客の入口 0 棟(目標 1 以上)、敷地の中の止まったトラック 506(目標 250 以下)。3 つとも目標まで届いていない
  - 案1 を選んだ理由: 政策 FreeTransport は費用の建設も維持もなく、戻せる。運賃の収入の減り(約5,179/週)を織り込んでも、局だけの週の収支は +4,786 の見込みで、守る線 +3,000 を超える。ただし全局の案を合わせると、他局の維持費の増え 2,903 を足して約 +1,883 となり、守る線を下回る。そのため採るかは市長が全局の合計で決め、採った後も月末に効きがなければ必ず外す。6-3 に直接当たる。効きは測るまで分からないので試しとし、月末に流れを比べる
  - 旅客の入口は、今月は案にしない。駅と空港の試しを1月に済ませた。駅は (1250,-2012) の向き north で置ける。入口の道路は担当を roads に渡し、港湾空港局は引かない(roads の経路 4,800。港の試しの経路 3,960 は予備)。水道管は (950,-1966) → (1215,-1966) → (1215,-2000) で 720 で引ける。電気は、送電線 (1246,-2012) → (1225,-2012) → (1225,-1500) → (1220,-1345) の 1,720 で試しが通った。ただし、発電所への接続は建てるときの ends で確かめるまで未確認。駅の案は6月に出す(4〜5月は財政局の凍結)
  - 貨物駅 28755 の枠待ちは、原因が決まっていない。枠が足りないのか、道路の混みなのかで手が変わる。今月は調査にする
  - 案は1件にした。駅と空港は、置き場所と道路は確認できたが、電気の接続が未確認のため、案にすると実行条件が未確認になる。件数を埋めるための案は作らない

- 捨てたもの:

  - 旅客の港(Harbor)を海岸に置く案: 西の海岸と北西の海岸で17か所を試したが、すべて断られた(ObjectCollision、HeightTooHigh、CannotConnect)。置ける場所が見つかるまで案にしない
  - 空港(Airport)を空き地1(1477,-3148)に置く案: 置く場所は試しで置けた。入口の道路は、地下で線路を横切る経路で試しが通った(16,160)。ただし、電気・水・下水が未確認で、費用 150,000 と週の維持 4,800 が大きいため、今月は案にしない。駅の効きを見てから決める
  - 旅客の駅(Train Station)の案: 置き場所、水道管、電気の経路は試しで通った。入口の道路は roads の担当に渡した。接続先の確認を含めて、今月は案にしない。6月に案にして置く
  - 名所(Monument)を中心部に置く案: 中心部は道路と建物で空きがない。放棄ホテル 5266 を壊す案も、道路に重なり置けなかった
  - 政策 HeavyTrafficBan: 交通の流れは上がる見込みがあるが、トラックを道路から締め出し、店の品物(228 軒が品物なし)を減らす。6-4、7-1 を悪くするので採らない
  - 貨物駅 28755 の道路を太くする案: 原因が枠なのか道路なのかが未確認。道路下水道局の担当にもかかるので、調査の結果を見てから判断する
  - 公共交通の予算(路線の台数)の変更: 乗客の少ない路線が多いが、効きを測る数が今月は揃わない。議決も要るので、政策の効きを見た後に検討する

### 経済観光文化局(economy)(hooks の記録で 08:15〜08:39)

- 元のファイル: [m01-economy.md](m01-economy.md)
- 案: なし

- 見たもの: [m01-economy.md の「見たもの」](m01-economy.md#見たもの)(33 行)
- 判断の根拠:

  - 観光の数字は、目標から遠い。観光客 1,646(目標 3,000)、Tourism 週 45(目標 1,000)、名所 6棟(目標 10)、attractiveness 6(目標 12)。名所を増やすのが、担当の一番の手になる。
  - しかし、名所は 12m 四方の場所と、道路に面した入口が要る。試した 5地区の道路沿いは、事務所と住宅で埋まっていた。放棄された店を取り壊す想定でも、隣の建物と道路に重なった。空き地3の幹線沿いの9地点も、置けなかった。今月、置ける場所を1つも確認できていない。
  - 島Bは、道路と水道管の経路が試しで通った。下水は、島の水道管の網に排水口があると確かめた(water_trace)。残るのは、橋と水道管を引く受け皿で、道路下水道局の計画に見当たらない。今月は実行できないので、案にしない。次の月に、道路下水道局への求めとして出す。
  - 週の収支は、守る線 +3,000 に対して余りが小さい。1回目のレビューの見込みでは、週 約+1,883 しかなく、名所も駅も入れられない。FreeTransport を外す求めを港湾空港局に出す。
  - 置ける場所が確認できないので、今月は案を出しません。必須の実行条件が未確認の案は、採択の対象にしないと決めています。
  - 観光客が増えない原因が分かっていない。名所を増やしても、観光客が増えるかは確かめていない。そのため、調査を1件出します。見る数は観光客と Tourism の収入で、担当の範囲です。
  - 旅客の入口は港湾空港局の担当です。経済観光文化局は、長期計画の「求めること」に書きました。

- 捨てたもの:

  - 西の (-2400, 180) の Modern Art Museum、(-2400, 60) の SeaWorld、(-2600, 60) の Friendly Neighborhood: 道路・水塔・店と重なり、置けない
  - 中央の (880, -300) の Official Park: 置けるが、事務所2棟を取り壊す。失う働き口は 33。放棄された建物ではないので、今は出さない
  - 中央東の (870, -420)、(2600, 480)、(2175, 540)、(2240, 540): 道路・事務所・埋立地と重なり、置けない
  - 東の (2590, 989)、(2150, 808) の取り壊し案: 取り壊しの後も、住宅・事務所・店と道路に重なり、置けない
  - 東端の (3700, -345) の SeaWorld: 警察署と風車と重なり、置けない
  - 空き地3(712, 1644)の幹線沿いの9地点: 置けない(AlreadyExists と、水と Water Outlet の重なり)。道路の幹線は引けるが、名所の場所がない。空き地3は事業に入れない
  - 空き地1(1477, -3148): 道路の試しが建物と重なり、経路が見つからない
  - 政策の変更(SmallBusiness、FreeTransport): 観光の数字に効く見込みを確かめられなかった。週の費用が増える案は、効き目が分からないまま出さない
  - 税を下げて事務所と店の需要を上げる案: 税率1%あたり約8,200/週(見積もり)の税収が減り、週の収支が守る線の +3,000 を割るので出さない

### 保健環境局(health)(hooks の記録で 08:15〜08:26)

- 元のファイル: [m01-health.md](m01-health.md)
- 案 health-1: 南西に埋立地を1か所増やす
  - 建設費 4280、週の維持費 +163、戻せない
  - 市の計画: 4-4
  - 議決: 要らない
- 案 health-2: 焼却場の近くの空き地に木を植え、汚染が下がるかを試す
  - 建設費 500、週の維持費 +0、戻せる
  - 市の計画: 4-3
  - 議決: 要らない

- 見たもの: [m01-health.md の「見たもの」](m01-health.md#見たもの)(42 行)
- 判断の根拠:

  - 担当の問題は、ごみ 15、汚染 32、健康 78。ごみは、南西の収集車の渋滞と、西の満杯の埋立地 7 から来ている。埋立地の案(案1)は、道具で置ける場所と道路の経路を確かめられたため、案に出す
  - 汚染は、焼却場 2267 の北の住宅地が 255 付近で飽和している。前の月に測った (3610, -190) は、道具の再測定で 0〜4 だった。試しは、空きの多い所ではなく、住宅の汚染の場所で測り直した。木は安く、戻せるので、効き目を試す(案2)。3月に下がらなければ、焼却場の移しを次の手にする
  - 体調の悪い市民 2,391 の原因は、まだ確かめられていない。汚染、医療の届き方、霊柩車の渋滞の3つを、調査で見る。死体の調査は、この調査の候補の1つとして入れた
  - 案は2件。3件目を埋めるための案は作らなかった

- 捨てたもの:

  - Recycling(政策): 費用は 0 だが、住宅の税収の -5%(約 13,256/週)。週の収支 9,965 から -3,291 になり、財政の守る線(+3,000 以上)を破る。ごみの -15% を足しても約 -303 で届かない
  - HeavyTrafficBan(政策): 費用 0 で汚染と騒音を下げうる。ただし重い車(貨物のトラック)を道から締め出す。港の貨物の流れ(8-1)と、店の品物(NoGoods 228)に効く。この街の物流の目標と逆になるので、今月は出さない
  - 火葬場を足す: 死体の印の周りに火葬場が 3〜4 か所あり、覆いは足りている。問題は渋滞なので、建てても効かない
  - 焼却場 2267 を移す: 今月は出さない。木の試しが3月に効かなければ、3月の案で出す(計画の事業2)。移す先は空き地5(4545, 2382)だけにする(空き地1は港湾空港局の空港候補と重なるので外した)。3月に `test_place_building` で確かめる
  - 放棄された店を壊して埋立地を置く: 取り壊しの議決が要り、戻せない。空き地が見つかった案1で足りる
  - 満杯の埋立地を空にする(empty_building): 空きは約 35M で、満杯の 7か所の中身 56M を移し切れない。移した先もすぐ満杯になる
  - 診療所・病院を増やす: 医療の使用は 1,953/5,000 で余裕がある。health 0 の所に住民が偏るかは、調査で確かめてから出す。今月は、効き目を見積もれないので出さない

### 教育委員会(education)(hooks の記録で 08:15〜08:45)

- 元のファイル: [m01-education.md](m01-education.md)
- 案 education-1: 高校1棟を北東の住宅地に足す
  - 建設費 24000、週の維持費 +560、戻せる
  - 市の計画: 2-3
  - 議決: 要らない

- 見たもの: [m01-education.md の「見たもの」](m01-education.md#見たもの)(20 行)
- 判断の根拠:

  - 教育の数字は出発点で目標を満たしている(小学校の定員 14,268 ≥ 子ども 11,344、高校の定員 24,360 ≥ 10代 22,372)。ただし高校の余裕は約9%で、10代の増えにつれて早く詰まる
  - 今月の案は、高校1棟の増設1件。定員を先に増やし、10代が定員を超えるのを防ぐ。候補 (2700, 850) は、取り壊しなし、道路に面する、電気・水・下水が届く、の3条件を確認した
  - 案の数を1件にした理由: 教育の数字は目標内で、ほかに効く手がない。件数を埋めるための案は作らない。編成方針の重点の外なので、市長が採るかを判断する
  - 調査は出さない。教育の問題の原因は分かっている(定員の余裕の少なさ)
  - 1か月目に作った地図の画像 `council/m01-education-map.jpg` は、zone_map の save_to で保存された。局が書くファイルの範囲の外。市長が使わなければ削除してよい
  - 再調査: 条件1(10代 95% 超)は未達(91.8%)。条件2は、運賃0を外せば満たす(余力約5,215)。運賃0を残すなら満たさない。案の配置は変えず、採否は市長に任せる

- 捨てたもの:

  - 小学校の増設: 子ども 11,344 に対して小学校の定員 14,268 で余裕は約26%。今月は必要ない。12か月の計画では、子どもの数を見て判断する
  - 大学の増設: 教育の担当の数字(小学校・高校)の外。大学の定員 36,540 は余裕がある。建設費 75,000 と維持費 1,920 を払う根拠がない
  - EducationBoost の変更: すでに有効で、学校の維持費に +25% 乗っている(週 7,940)。外すと教育の質が落ちる見込み。今月は触らない
  - 高校の増設を (2700, 800) に置く案: 取り壊しで住宅 2 棟(失う家 31)が要る。取り壊しの議決が要るため、(2700, 850) の案を採る
  - 高校を (2524, 522)、(2240, 522) に置く案: Landfill Site と重なり、置けない
  - 高校を (1420, -1150) に置く案: 道路がなく、道路を引く工事が要る。接続工事を確かめていないので、今月は案にしない
  - 高校を水の上(1300, -900)、(1400, -900)、(1720, -1120)に置く案: 水の上で置けない

### 消防局(fire)(hooks の記録で 08:15〜08:18)

- 元のファイル: [m01-fire.md](m01-fire.md)
- 案 fire-1: 犯罪の多い地区に警察署を置く(放棄されたホテルを壊す)
  - 建設費 12000、週の維持費 +480、戻せない
  - 市の計画: 3-4
  - 議決: 要る(取り壊し)

- 見たもの: [m01-fire.md の「見たもの」](m01-fire.md#見たもの)(26 行)
- 判断の根拠:

  - 担当の数字は、火事 4 と犯罪 3 の合計 7。目標の合計 4 以下に、3 足りない。どちらも件数は少ないが、目標に届くまで減らす必要がある
  - 犯罪は、(2055,1036) の周りに警察署がない。近くの警察署は、今の車の出動が多い。新しい警察署の案(fire-1)は、取り壊しで失うものが 0 の放棄されたホテルを使う。確かめた事実の範囲で、置けて、道に面し、失うものがない
  - 火事は、原因が分からない。近くの消防署は 0 台か 1 台しか出ていない。道の詰まり(110 台)が原因かもしれない。これは道路下水道局の担当に当たるので、局の案にせず、調査で原因を確かめる
  - 案は 1 件。予算の増やしは、守る線の中で選べるが、今の確かめで効く場所が決まらないため、案にしない。政策 SmokeDetectors は週 57,718 かかり、週の収支を赤字にするので採らない
  - 案の数を 1 件にした理由: 3-4 の目標に効く手で、確かめられる手は犯罪の警察署だけ。火事の手は、調査の結果を待つ

- 捨てたもの:

  - 政策 SmokeDetectors(火災報知器、週 57,718): 火事の印を減らす見込みはあるが、週の収支を +9,965 から約 -47,750 にする。守る線(+3,000 以上)を破るので採らない
  - 消防署の追加(Fire House、(2184,-918) 付近の工場の隣): 近くの消防署 32853 が出られない原因が道の詰まりなら、追加しても出られない。原因を調べてから決める(調査で確かめる)
  - 犯罪の印の住宅 16778 と 27404 を別の場所へ移すこと: 住宅を動かすのは、住宅の需要に関わり、局の担当外
  - 警察署を (2075,1050)、(2000,1060)、(2290,1040)、(2286,1080) に置く案: ぶつかる、または働き口を 19〜41 失うため採らない

### 財政局(finance)(hooks の記録で 08:15〜08:40)

- 元のファイル: [m01-finance.md](m01-finance.md)
- 案 finance-1: 道路の予算を120%にして、交通の流れを試す
  - 建設費 0、週の維持費 +1700、戻せる
  - 市の計画: 6-3
  - 議決: 要る(予算)

- 見たもの:

  - `list_building_types`(Monument): 名所の一覧。SeaWorld、ScienceCenter、Servicing Services、Friendly Neighborhood は各 20,000(週 320)。Countdown Clock は 37,500(週 80)、Colossal Offices は 70,000(週 1,200)。名所4棟の建設費は 80,000。
  - `list_building_types`(Beautification): Regular Park は 1,000(週 8)。名所ではない。公園の表は urban の値(1棟 15)を使い、多めに見ている。
  - `list_building_types`(PublicTransport): 旅客の駅 45,000(週 960)、港 80,000(週 1,600)、空港 150,000(週 4,800)。
  - `list_building_types`(Electricity): 風車 Wind Turbine は 6,000(週 80)。

- 判断の根拠:

  - 第4回の是正で、島Bの橋・水道管・風車を5月、名所を6月(2棟)と8月(2棟)に揃えた。
  - 第5回の是正で、信号を1月・上限 468 に直し、4車線化を9月に動かし、公園を4〜7月に分けた。週の収支の最小は 1・2月の +3,003、所持金の最小は8月の 1,984,099(守る線に +110,099)。
  - 信号の週の維持費は、道具で見積もれない(`set_traffic_lights` は費用を返さない)。上限 468 は、置いた後の週の収支で確かめ、超えたら外す。
  - 案の数は0件。1月は守る線を保つ手がなく、道路の試しは5月へずらす。

- 捨てたもの:

  - 道路の予算 105%(1月の小さな試し): 週 −426 で守る線を通るが、効き目が小さく、流れの変化を測れない。切り分けにも向かないため出さなかった。
  - 道路の予算 120%(finance-1): 上の理由で1月は取り下げ。5月に移す。
  - 旅客の駅・港・空港を1月に置く案: 週の余力がほぼ 0 のため。
  - 港を8月に置く案: port の計画に港がない。港を置くかは port が決める。
  - 税を変える案: 税の効きを道具で確かめる段階にない。守る線を支える手として今月は出さない。

## 4. 差し戻しと再調査

- 教育委員会: education-1(実行可 True)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m01-bill.md](m01-bill.md)、直した議案 [m01-bill-2.md](m01-bill-2.md)
- 採った m01-1: 空き地3に公園1棟と幹線・送電線(元 urban-1、議決は要らない)
- 採った m01-2: 交差点(2110,330)に信号1基(元 roads-1、議決は要らない)
- 採った m01-3: 運賃0(FreeTransport)で流れを試す(元 port-1、議決は要らない)
- 採った m01-4: 南西に埋立地を1か所増やす(元 health-1、議決は要らない)
- 採った m01-5: 焼却場の北に木を植える試し(元 health-2、議決は要らない)
- 採った m01-6: 放棄ホテルを壊して警察署を置く(元 fire-1、議決が要る(取り壊し))
- 採らなかった education-1: 実行条件は確認済みだが、10代は定員を超えておらず、維持費560を足すと1月の週の収支の余裕が約36しか残らない。
- 採らなかった finance-1: 局が1月に取り下げ(案なし)。週の余力がなく、道路の予算120%は5月に出し直す計画。

- 見たもの:

  - `m01-bill.md`、`m01-assembly.md`、`mayor-note.md` を読んだ。ゲームの道具は呼んでいない
  - 局の案の数字: 週の収支 +9,965、所持金 2,082,287。週の増減の合計 -5,901(運賃0 5,179、警察 480、埋立地 163、公園・幹線 79)。差し引き +4,064
  - 議会の財政の確認: 信号を除いた可決分で、建設費 26,560、維持費の増え 722、所持金 約 2,055,727

- 判断の根拠:

  否決は信号1件の費用(上限 208,287)だけが理由だった。実額の見積もりは今月示せず、費用を減らす手もない。そこで信号を取り下げた。残る5件は議会が可決した内容のまま変えない。週の収支は +4,064 で守る線 +3,000 を保ち、所持金は 約 2,055,727 で 1,874,000 を上回る。6-3 は運賃0(m01-3)と調査 s01-3 で進める。

- 捨てたもの:

  - roads-1(信号): 上のとおり。2月に実額を示して出し直せる
  - education-1: 10代の増え方を見て、2月に再提出できる
  - 経済観光文化局の名所の案: 局が案なし。島B、空き地3の候補を2月以降に試す(plan-city.md の調整)
  - 旅客の駅・空港・港: 局が案にしていない(電気の接続が未確認)。6月の事業として plan-city.md に入れ、前倒しの可否を2月に求める
  - health・fire の調査、urban の調査、finance の調査: 今月は3件の枠を重点(観光、交通、物流)に使った。または、ほかの試しが同じ数字を測る

## 6. 議会: 可決と否決(hooks の記録で 08:46〜08:46)

- 元のファイル: [m01-assembly.md](m01-assembly.md)
- m01-1 財政: 可決。建設費 9,780、維持費 +79 で守る線に収まる。
- m01-2 財政: 否決(点 5)。信号の建設費の上限 208,287 を入れると所持金の見込みが 1,847,440 となり、守る線 1,874,000 を下回る。実額の見積もりを示して出し直す。
- m01-3 財政: 可決。建設費 0。可決分で週の収支 約 +4,064 と守る線を保つ。戻せる。
- m01-4 財政: 可決。建設費 4,280、維持費 +163 で守る線に収まる。
- m01-5 財政: 可決。建設費 約500、維持費 0 で守る線に収まる。
- m01-6 取り壊し: 可決。壊すのは放棄された1棟で失う働き口・家は 0。代わりの手と比べてあり、費用 12,000・維持費 480 は守る線に収まる。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `city_info`: 週の収入 342,140、支出 332,175(収支 +9,965)、所持金 2,082,287
  - `m01-bill.md`、`plan-city.md` を読んだ。ほかの局の計画ファイルは、`plan-city.md` が要約しているので財政面は `plan-city.md` で確かめた

- 判断の根拠:

  守る線のうち、週の収支は全6件で +3,596 と守れる。所持金は、信号の上限 208,287 を建設費に入れると 1,847,440 になり、1,874,000 を割る。信号の上限は実績のない数字で、払った後に外しても戻らないので、見込みとして扱う。1件で解消できる m01-2 を否決し、重点の 6-3 のうち運賃0(m01-3)は残した。

- 捨てたもの:

  - m01-3(運賃0): 週の収支 -5,179 は大きいが、可決分で +4,064 が残り、戻せる政策なので可決
  - m01-4(埋立地、戻せない): 4,280 と小さく、守る線を破らないので可決

## 7. 実行する市長: 実行と見回り(hooks の記録で 08:48〜08:56)

- 実行してよい施策: m01-1、m01-3、m01-4、m01-5、m01-6
- 実行した: m01-1、m01-3、m01-5
- 失敗した: m01-4、m01-6
- 臨時: なし
- 見回り 2050-01-12: 人口 178710、所持金 2074930、週の収支 3808、幸福度 85
- 見回り 2050-01-22: 人口 178696、所持金 2082872、週の収支 5613、幸福度 85
- 報告:

  m01-1(公園、幹線、送電線)、m01-3(運賃0)、m01-5(木20本)は実行できた。m01-1 は送電線の始点が公園本体に当たり、(664,1622) に動かした。公園の電気は来ている。m01-4 は埋立地だけ置け、道路が overlaps で断られたので、中止条件に従い道路は引かなかった。m01-6 は、送電線の確認で advance(1) を先に呼んだため、hook が取り壊しを止めた。実行側の順序の誤りで、警察署は未実行のまま。見回りは2回とも境目に当たらず、臨時はなし。月末(2050-02-01)は人口178,670、所持金2,089,547、週の収支+4,562、観光客1,658、Tourism週41、街全体でなく範囲限定の traffic flow 52。貨物駅28755の中の台数は632、605、589で、7日以上止まった車は470台台のまま。13893は0台。市政ノートと3つの調査ファイルは更新済み。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m01、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 08:13〜09:06(hooks の記録の時刻から)、道具の行 631
- 議会が可決した種類: 取り壊し
- 議決が要る道具の呼び出し: 0 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 388 件
- hooks の拒否: 2 回

#### hooks が止めた Write

- 2026-10-29T08:24:45+09:00 council-port: この役が書いてよいのは m01-port.md, plan-port.md だけ。書こうとした先: ~/orca/workspaces/tried/issue-124/2026/10-27-AI市役所で福岡を観光都市にする-03-観光の街を目指す計画と局を決める/council/m01-port.md.tmp-unused

#### council/ にある、決まりにない名前のファイル

- `m01-education-map.jpg`
- `m01-port-map-coast.jpg`

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

#### hooks の拒否

- council-port `Write`: 1 回
- council-mayor-field `bulldoze`: 1 回

- 2026-10-29T08:24:45+09:00 council-port `Write`: この役が書いてよいのは m01-port.md, plan-port.md だけ。書こうとした先: ~/orca/workspaces/tried/issue-124/2026/10-27-AI市役所で福岡を観光都市にする-03-観光の街を目指す計画と局を決める/council/m01-port.md.tmp-unused
- 2026-10-29T08:49:47+09:00 council-mayor-field `bulldoze`: advance の後(臨時)は、議決が要る手(取り壊し)を打たない

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 9)
