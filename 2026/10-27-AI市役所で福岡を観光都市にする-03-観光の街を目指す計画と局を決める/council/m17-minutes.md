# 17か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 18:24〜18:25)

- 元のファイル: [m17-policy.md](m17-policy.md)
- ゲーム内の日付: 2051-05-06、保存: fukuoka-plan-m17
- 重点: 5-1、5-2 観光(旅客の入口、島と空き地の名所)、8-1、6-4 貨物センターの止まりと品物がない店、4-4 資源循環(満杯の埋立地とごみの印)

- 見たもの: [m17-policy.md の「見たもの」](m17-policy.md#見たもの)(15 行)
- 判断の根拠:

  公約4(観光)が2か月ぶりに2つとも減ったので、観光を重点の1つ目に置く。入口と島・空き地の名所は、17か月たっても0棟で、局の案が確かめられるかが鍵になる。貨物センターの止まりとごみの満杯は、目標との差が大きく、他局の案と重ならない。財政は黒字で余裕がある。

- 捨てたもの:

  - 6-3 交通: 流れは52%で動かないが、信号の効きは局所で当たり続けており、今月は重点を貨物とごみに回す。局の案は出してよい
  - 4-3 汚染: 焼却場の停止は2回効かなかった。別の手の案が出れば受ける
  - 4-2 公園: 91棟で目標100にあと9。局の案が出れば受ける
  - 6-1 事務所L3: 3,282棟で目標3,500。税の試しで動かなかった(見立て)ので重点にしない

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

### 住宅都市みどり局(urban)(hooks の記録で 18:26〜18:28)

- 元のファイル: [m17-urban.md](m17-urban.md)
- 案 urban-1: 道に面した空き地(1820,300)に公園 JapaneseGarden を1つ置く
  - 建設費 2500、週の維持費 +40、戻せる
  - 市の計画: 4-2
  - 議決: 要らない

- 見たもの: [m17-urban.md の「見たもの」](m17-urban.md#見たもの)(19 行)
- 判断の根拠:

  - 4-2 は、計画の事業1(第17月は公園を1つ置く)の予定どおり。前の月(第16月)の公園が建って公園の数が 90 から 91 へ増えたので、計画の前提は今月も合う。計画は直さない。
  - 公園は JapaneseGarden(2,500、維持費 40)を、計画どおり使う。候補の (1820,300) は `test_place_building` が ok で、入口の道 29165 に距離 6 で面し、働き口・家を失わない。電気・水は近くの 39519 と 46572 の grid が満たしている。
  - 予備の (1856,356) と (1745,316) も `test_place_building` で ok。別の道(23279、4414)に面し、場所は (1820,300) から 60m 以上離れている。
  - 案は1件だけ。4-2 の手は公園を置くことで、1件の案に別の手を足すと件数を埋めることになるため、2件目は出さない。
  - 政策は、担当の数字(公園の数、地価)に効く政策が一覧にない。RecreationalUse は効果の記述がなく、担当の数字への効きを確かめられないので、今月は見送る。

- 捨てたもの:

  - 2件目の公園(同じ手の増やし): 計画は月1件。件数を埋めるための案にしない。
  - Regular Park(9×8、1,000 / 維持費 8): 維持費は安いが、道に面した空きで 72×64m を確保できるかを未確認。今月の (1820,300) の候補では、隣の 39519 と重なる見込み。次の月に空きを探すときの候補として残す。
  - Parking Lot 系、Decoration 系の Beautification: 4-2 の「花や緑による潤い」に当たらない。数を増やすためだけの置き方になるため、捨てる。
  - RecreationalUse(政策、0 円): 効果の記述が「費用なし」だけで、担当の数字への効きを確かめられない。今月は試しにもしない。
  - 地区の政策(set_district_policy): 地価を上げる効きを確かめる手段がなく、今月の担当の数字に当たらない。
  - (2160,232) の公園: 道路に面していない。高密度の家 2 棟(失う家 6)を壊す必要があるため、捨てる。

### 道路下水道局(roads)(hooks の記録で 18:26〜18:27)

- 元のファイル: [m17-roads.md](m17-roads.md)
- 案 roads-1: 交差点 (2155,330) に信号を置き、東の止まりを減らす
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない
- 案 roads-2: 送電線の網を、名所 11580 と公園 30466 につなぐ
  - 建設費 480、週の維持費 +12、戻せない
  - 市の計画: 5-1、5-2、4-2
  - 議決: 要らない
- 案 roads-3: 政策 FreeTransport を外し、運賃収入を戻す
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m17-roads.md の「見たもの」](m17-roads.md#見たもの)(21 行)
- 判断の根拠:

  事業1の規則に沿い、次の交差点を (2155,330) に決めた。計画の候補 (2648,691) は交差点がなく、blocked の上位は自動の信号か交差点なしで、案にできなかった。事業2は、18月末までの期限の前に、網の端からの経路が試しで通ったので案にした。FreeTransport は 16月の試しで外れが出たので、戻す案として出した。3案は別の手で、件数は効きが見込める3つに絞った。4件目の候補は、道を太くする案(Medium Road)で、今月は測っていないため調査に回した。

- 捨てたもの:

  - 交差点 (2648,691): 40m以内に交差点がない。計画の候補が存在せず、取り下げた
  - 交差点 (694,-703) と (2200,330): 自動の信号が既に付いている。`set_traffic_lights` で足す手がない。流れ(blocked 36)の原因は調査の対象外
  - 交差点 (-1093,-686): 40m以内に交差点がない
  - 名所の枝を敷地の中へ入れる案: `test_build_line` で ObjectCollision。敷地の縁で止める形に変えた
  - 政策 HeavyTrafficBan(無効、費用0): 交通の流れに効く見込みがあるが、トラックを締め出すと、品物がない店と原料がない工場(6-4、8-1)が悪化する懸念がある。効きも未測定のため、今月は出さない
  - Medium Road(x 2200)の Large Road への差し替え: 今は測定が足りないため、調査で見てから決める
  - 事業3(旅客の入口の道と電線): 駅が置かれていない(旅客の入口0、港湾空港局の案待ち)

### 港湾空港局(port)(hooks の記録で 18:26〜18:33)

- 元のファイル: [m17-port.md](m17-port.md)
- 案 port-1: 島Bに旅客の駅(Train Station)を1つ置く
  - 建設費 51840、週の維持費 +994、戻せない
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m17-port.md の「見たもの」](m17-port.md#見たもの)(18 行)
- 判断の根拠:

  島Bの旅客の駅は、5-1、5-2 の旅客の入口を 0 から 1 にする唯一の手で、17か月の観光の重点に当たる。駅と入口の道は道具で通ると確かめた。再調査で、水管(6,200)と電線(200)は test_build_line で通った。ただし整地の実費は、局の道具で test できないため未確認で、必須条件が残る。駅の ports への接続も未確認。実行可否は「未確認」のままとした。案は1件で、ほかの候補(空き地の名所、島の道の接続)は、旅客の入口の数に直接効かないか、同じ整地の条件を持つため、今月は1件に絞った。8-1 は、振り分けの案を取り下げ、止まりの調査を1件出した。

- 捨てたもの:

  - 貨物センター28755 の横に2つ目の Cargo Center(建設費 60,000、週 1,440): 場所と接続が未確認で、週の維持費も重い。止まりの調査の結果を見てから決める
  - 13893 の増車(電車の着きがない): 13893 は電車の着きがなく、車を出さない理由ではない(前の月の調査)。取り上げない
  - 島の旅客の駅を、整地なしで置く案: 入口の道が SlopeTooSteep で通らない(test_build_line の gameCheck)。整地を前提にした案1に含める

### 経済観光文化局(economy)(hooks の記録で 18:26〜18:29)

- 元のファイル: [m17-economy.md](m17-economy.md)
- 案: なし

- 見たもの: [m17-economy.md の「見たもの」](m17-economy.md#見たもの)(20 行)
- 判断の根拠:

  - 観光の数字(観光客1,875、訪問158、Tourism 57、attractiveness 平均2)は、前月から横ばいで動いていない。公約4は2か月連続で未達。
  - 16月の案1(空き地3の Transport Tower)は採られなかった。空き地3の名所 11580 は、電気が来ないまま。今月の計画の「入口の道と水管の先」は、実物がないため消した。
  - 旅客の入口は16月末の期限を過ぎても0。港湾空港局から案が出ていないため、長期計画は入口なしで名所と商業を伸ばす計画に直した(調整6)。
  - 40850 は attractiveness の中心(最大121)だが、道がつながらず、観光客を受けられない。入口の向きは道具で確かめられず、西側の道は店 19275 の取り壊しが要る。実行条件が確認できないため、局の案にしない。道路下水道局に求めることとして渡す。
  - 名所を新しく置く空きは、所有地の中では見つからなかった。所有地の外は買っていない土地で、置けない。
  - 案の数は0件。実行条件を確認できた対象がなく、件数を埋める案は作らない。

- 捨てたもの:

  - 名所 40850 の道(西側の経路と店 19275 の取り壊し): 入口の向きが確認できず、実行条件が未確認。道路下水道局の担当。
  - 所有地の空きに Official Park、Fountain、SeaWorld を置く: 道に面する空きが見つからず、試しの道具で断られた。
  - 放棄された建物を壊して名所を置く(13646、4192、11741、4214): 道路と住宅に当たり、置けない。取り壊しの議決を伴うため、置けない形のまま出さない。
  - 空き地5(4545,2382)に名所を置く: 所有地の外で置けない。
  - 政策 SmallBusiness の再試し: 前の試しで効きが切り分けられず、今月の数字では判定できない。
  - 旅客の入口: 港湾空港局の担当。経済観光文化局は求めることとして渡す。

### 保健環境局(health)(hooks の記録で 18:26〜18:29)

- 元のファイル: [m17-health.md](m17-health.md)
- 案 health-1: 北東の焼却場 10351 を動かし、ごみを減らす
  - 建設費 0、週の維持費 +1440、戻せる
  - 市の計画: 4-4
  - 議決: 要らない

- 見たもの: [m17-health.md の「見たもの」](m17-health.md#見たもの)(13 行)
- 判断の根拠:

  ごみの印 22 は、目標 0 から遠く、満杯の埋立地が3つあるので、受け入れを戻す手が要る。10351 は、動かすだけで処理 60,000 / 週 が始まり、建設費も要らず、電気・水・下水が届いていて、道路からも入れる。確かめた事実に基づき、今月の一番の手にした。北東の新しい埋立地は、入口から道路までを引けないので、実行できない。政策 Recycling は税収 -5%(週 約 -13,089)で、守る線 +3,000 を割るため採らない。案は1件に絞った。道路下水道局の手と重ならない。

- 捨てたもの:

  - 北東に新しい埋立地を置く(1960,440): 道具で置けるが、入口(1960,472)から北の道路(z=560)まで、事務所4棟とぶつかり、道路が引けない。実行できないので、今月は出さない。次の月に、別の平らな空きを道具で探す
  - 政策 Recycling を有効にする: 直接の費用 0 だが、住宅の税収 -5%(週 約 -13,089)で、週の収支が守る線 +3,000 を割る。採らない
  - 政策 SmokeDetectors: 週 57,789 で、収支に合わない
  - 焼却場 2267 の停止: 2回効かず、4月に動かし直した。今月は出さない
  - 満杯の埋立地 12880 の active=false: 満杯が3つあるので、戻さない

### 教育委員会(education)(hooks の記録で 18:26〜18:28)

- 元のファイル: [m17-education.md](m17-education.md)
- 案 education-1: 小学校 43936 を1校止め、維持費を減らす(試し)
  - 建設費 0、週の維持費 +-160、戻せる
  - 市の計画: 2-3
  - 議決: 要らない

- 見たもの: [m17-education.md の「見たもの」](m17-education.md#見たもの)(8 行)
- 判断の根拠:

  - 小学校: 定員 13,920 が子ども 8,786 の1.585倍で、43936 を止めた後も 13,572 で 1.545倍。基準 1.3 を保つ。15301 を止めた後、覆いに0は出ていない(16月の調査、最小 17)。
  - 覆いの確かめ: 43936 の周りの最小は今 8 で0ではない。止めた後の覆いは、道具では事前に測れないため、試しとして出し、0が出たら戻す条件を付けた。
  - 近くの空き: 15022 と 25802 の空きは合わせて約 257 人。43936 の生徒 191 人を受けられる。
  - 費用: 維持費が週 -160(約 -200)減る。建設費はかからない。週の収支 +7,468 は守る線 +3,000 の上。所持金 2,502,262 は守る線 1,874,000 の上。
  - 高校: 余裕 5,632(130%)で基準 1,000 を大きく上回る。休止を続け、今月は置かない。
  - 案の数: 1件。計画の17月の予定(43936 を止める案を試しとして出す)どおり。

- 捨てたもの:

  - 高校を1校置く: 余裕 5,632 で基準 1,000 を大きく上回る。建設費 24,000 と週 560 の増えが要るため、今月は置かない。
  - 小学校 15022 を止める: 15301 と同じ地区で、覆いを同時に減らす。候補に入れない。
  - 小学校 25802 を止める: 43936 を止める案と同じ地区で、覆いの0のリスクを重ねる。今月は1校だけにする。
  - 政策 EducationBoost を外す: 週 7,940 の減りがあるが、大卒の失業 8,522 → 4,608 の効きを、財政の判定で当たりとした。外すと大卒の失業が戻る見込みがあり、政策の変更は月1件の上限もある。局が決める手ではないため、今月は出さない。

### 消防局(fire)(hooks の記録で 18:26〜18:28)

- 元のファイル: [m17-fire.md](m17-fire.md)
- 案 fire-1: 東側の届きに消防署を1つ足す(Fire House)
  - 建設費 12000、週の維持費 +560、戻せる
  - 市の計画: 3-4
  - 議決: 要らない

- 見たもの: [m17-fire.md の「見たもの」](m17-fire.md#見たもの)(16 行)
- 判断の根拠:

  - 17月の数字: 火事0、犯罪1、合計1。3-4 の目標(4以下)を達成している。火事の場所 (1197,-1018) の印は今月消えた。
  - 案は、印を減らす手ではなく、届きを足す手。東側の届きは 0〜4 で、ほかの区域(西は 20 以上)と比べて低い。
  - 費用 12,000 と週 560 は、所持金 2,502,262 と週の収支 +7,468 に対して小さい。守る線(週 +3,000、所持金 1,874,000)を割らない。
  - 効きは火事の印では測れない(今月0)。届きの数字で18月末に判定する。案は1件とする。事業1と事業2は、焼け跡も同じ場所の火事も今月は出ていないため、案にしない。

- 捨てたもの:

  - SmokeDetectors(政策、有効化): 費用が週 57,789 と大きく、火事の印が今月0のため、効きに対して費用が見合わない。
  - (1197,-1018) 周辺に消防署を置く案: 16月の再調査で、電気が来て空いた敷地は取り壊しを伴うか、道路や公園に重なる。今月も (1285,-1040) は取り壊しを伴うため外す。
  - (1325,-1055) の消防署: 電気の点が 0 で、試しの道具は通るが電気の条件が未確認のため外す。
  - Fire Station(建設費 60,000、週 1,440): 届きを補うには費用が大きい。Fire House で足りる。

### 財政局(finance)(hooks の記録で 18:26〜18:26)

- 元のファイル: [m17-finance.md](m17-finance.md)
- 案 finance-1: 政策 FreeTransport を外す(運賃収入を戻す)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの:

  - `city_info`: 人口 175,864、所持金 2,502,262、週の収支 +7,468(収入 333,111、支出 325,643)、観光客 1,875(訪問158)、需要 住26/商2/工45、来ない市民 0/0/0、dialog なし
  - `economy`: 税 住(低)9/住(高)7/商(低)9/商(高)3/工3/事務所3。予算は医療130、道路120、教育120、消防140、警察150、公園150、ごみ150、バス150
  - `list_policies`: FreeTransport active=true、costPerWeek=0(運賃収入が0)。EducationBoost active=true、7,940。SmokingBan active=true、0。BigBusiness active=true、3,888。SmallBusiness active=false、311。RecreationalUse active=false、0。policyExpensesPerWeek 10,766
  - `economy_breakdown`: PublicTransport 収入 0、支出 37,880(バス 21,760)。HealthCare 支出 66,248。Education 支出 47,880。Tourism 週57
  - `list_loans`: 3枠とも未借入。loanExpensesPerWeek 0

- 判断の根拠:

  - FreeTransport の試し(第16月)は外れた。乗客は増えず、流れも 53→52 で動かず、運賃収入 4,796 が消えた。長期計画のやめる条件に当たるため、外す案を1件出す
  - 外すと週の収支は約 +12,260(見積もり)になり、守る線 +3,000 の上の余裕は約 9,260 になる。所持金 2,502,262 は守る線 1,874,000 の上にある
  - 医療の予算 130 は、健康 88(目標80以上)、used 785 / 容量 5,100 で、やめる条件に当たらないため保つ
  - 2267 の停止の枠(約 -1,440)は、今月の見積もりから外した。停止は効かず、2267 は再開済みのため
  - 観光と貨物の事業の維持費(駅 960、名所 640〜720 を2棟、公園、道)は、約 2,550 で、余裕に収まる
  - 案は1件にした。政策の枠は1件で、税は計画どおり18月まで保留。予算の案は、6-3 の流れに効く根拠が測れていないため出さない
  - 調査は1件。人口の減りの原因を、18月の税の見直しの前に確かめるため

- 捨てたもの:

  - 住宅税を下げる案: 人口の減りの原因が未確認。税を動かすと、人口と事務所の数字が同時に動き、切り分けられない。調査の結果を待つ(18月)
  - 道路の予算を 120 から 150 に上げる案: 120 の試し(m01-8)で流れは 51→50 と動かなかった。150 は維持費が約 +2,200/週 増えるうえ、効きの根拠がない
  - 医療の予算を 130 から下げる案: 健康 88 は目標 80 の上だが、やめる条件に近づく。今月は保つ
  - 融資を借りる案: 所持金は守る線の上で足りており、借りる理由がない(利率 5〜15%)

## 4. 差し戻しと再調査

- 港湾空港局: port-1(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m17-bill.md](m17-bill.md)
- 採った m17-1: 公園 JapaneseGarden を (1820,300) に置く(元 urban-1、議決は要らない)
- 採った m17-2: 交差点 (2155,330) に信号を置く(元 roads-1、議決は要らない)
- 採った m17-3: 送電線を名所 11580 と公園 30466 につなぐ(試し)(元 roads-2、議決は要らない)
- 採った m17-4: 政策 FreeTransport を外す(元 finance-1,roads-3、議決は要らない)
- 採った m17-5: 北東の焼却場 10351 を動かす(元 health-1、議決は要らない)
- 採った m17-6: 小学校 43936 を止める(試し)(元 education-1、議決は要らない)
- 採った m17-7: 東側に消防署 Fire House を置く(試し)(元 fire-1、議決は要らない)
- 採らなかった port-1: 整地の実費と水管・電線の経路が未確認で、必須条件が残る。

- 見たもの:

  - `m17-urban.md` ほか7局の案と、`m17-policy.md`、`plan-city.md`、`ledger-recent.jsonl`、`mayor-note.md`(直近の月例と分からないことの一覧)
  - 各局が道具で確かめた結果(`test_place_building`、`test_build_line`、`junction_info`、`list_policies` など)は局の案の値を使った。市長は街の道具を呼んでいない

- 判断の根拠:

  確認済みの7件を採り、未確認が残る port-1 だけを差し戻した。費用は建設費 14,980、週の維持費の増え 1,892 で、運賃収入の戻り約 4,800 を入れると週の収支は約 +10,400 の見込み。守る線(週 +3,000、所持金 1,874,000)の上に収まる。FreeTransport の2案は同じ手なので1件にした。重点1(観光)は m17-3 だけが建設の手で、旅客の入口は port-1 の整地と管の確認待ち。

- 捨てたもの:

  - port-1: 必須条件(整地、水管、電線の経路)が未確認。条件付きで港湾空港局に調べ直させる
  - roads-3: finance-1 と同じ手で、m17-4 に合わせた
  - 道路下水道局の調査(Medium Road の密度): 上限3件のため。信号の結果を見てから第18月に出し直す
  - 満杯の埋立地への新規の埋立地(health の捨てた案): 入口から道路が引けず、局が実行不可と書いている

## 6. 議会: 可決と否決(hooks の記録で 18:34〜18:34)

- 元のファイル: [m17-assembly.md](m17-assembly.md)
- m17-1 財政: 可決。建設費2,500、週40で守る線に収まる。
- m17-2 財政: 可決。建設費0。維持費は小さく余裕の範囲。
- m17-3 財政: 可決。建設費480、週12で小さい。
- m17-4 財政: 可決。政策変更は月1件の内。維持費は増えず運賃収入が戻る。
- m17-5 財政: 可決。週1,440の増えでも収支は+5,576以上で守る線の上。
- m17-6 財政: 可決。週160の減りで守る線に響かない。
- m17-7 財政: 可決。建設費12,000、週560。所持金は守る線を大きく上回る。
- 可決した種類(hooks が見る): なし

- 見たもの:

  - `economy`: 税と予算は変更案なし
  - `city_info`: 所持金 2,502,262、週の収入 333,111、支出 325,643
  - `m17-bill.md`: 7件の費用と政策変更の数

- 判断の根拠:

  収支は +7,468 で、下降規則の +4,900 の上にある。増える維持費 1,892 を引いても +5,576 で、+3,000 を超える。所持金も建設費を引いて約 2,487,300 で、1,874,000 を大きく上回る。型の上限(税、予算、政策の月1件)も超えない。

- 捨てたもの:

  - m17-5: 維持費の増えが最大だが、運賃収入が戻らなくても守る線を破らないため可決

## 7. 実行する市長: 実行と見回り(hooks の記録で 18:35〜18:42)

- 実行してよい施策: m17-1、m17-2、m17-3、m17-4、m17-5、m17-6、m17-7
- 実行した: m17-1、m17-2、m17-3、m17-4、m17-5、m17-6、m17-7
- 失敗した: なし
- 臨時: なし
- 見回り 2051-05-16: 人口 175646、所持金 2502282、週の収支 10541、幸福度 88
- 見回り 2051-05-26: 人口 175488、所持金 2518101、週の収支 10943、幸福度 88
- 報告: 長いので [市政ノート](../mayor-note.md) を見る(1211 字)

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m17、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 18:23〜18:52(hooks の記録の時刻から)、道具の行 253
- 議会が可決した種類: なし
- 議決が要る道具の呼び出し: 0 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 610 件
- hooks の拒否: 2 回

#### 運営のフォルダで、決まりの外の変更(git status)

- `council/m01-port-zonemap-east.jpg`
- `council/m01-roads-zonemap.jpg`
- `council/m01-zonemap-east.jpg`
- `council/m03-zone-a.jpg`
- `council/m05-port-map-south.jpg`
- `council/m06-economy-zonemap-east.jpg`
- `council/m06-port-map-2480.jpg`
- `council/m06-port-map-cargo.jpg`
- `council/m06-port-map-east.jpg`
- `council/m06-port-map-south.jpg`
- `council/m06-roads-map-electric.jpg`
- `council/m07-port-islandB-map.jpg`
- `council/m08-map-city.jpg`
- `council/m08-map-park.jpg`
- `council/m09-economy-map-east.jpg`
- `council/m09-health-map-pollution.jpg`
- `council/m09-port-islandB.jpg`
- `council/m11-port-map-north.jpg`
- `council/m12-port-zonemap.jpg`
- `council/m13-port-zonemap-cargo.jpg`
- `council/m13-port-zonemap-west.jpg`
- `council/m14-urban-map-east.jpg`
- `council/m15-economy-map-east.jpg`
- `council/m15-economy-map-southwest.jpg`
- `council/m15-zonemap-urban.jpg`
- `council/m16-fire-zone.jpg`
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
- `試し-1〜3か月目(改善途中)/command-log.txt`
- `試し-1〜3か月目(改善途中)/council/ledger-older.md`
- `試し-1〜3か月目(改善途中)/council/ledger-recent.jsonl`
- `試し-1〜3か月目(改善途中)/council/ledger.jsonl`
- `試し-1〜3か月目(改善途中)/council/m01-assembly.json`
- `試し-1〜3か月目(改善途中)/council/m01-assembly.md`
- `試し-1〜3か月目(改善途中)/council/m01-bill.md`
- `試し-1〜3か月目(改善途中)/council/m01-economy.md`
- `試し-1〜3か月目(改善途中)/council/m01-education.md`
- `試し-1〜3か月目(改善途中)/council/m01-finance.md`
- `試し-1〜3か月目(改善途中)/council/m01-fire.md`
- `試し-1〜3か月目(改善途中)/council/m01-health.md`
- `試し-1〜3か月目(改善途中)/council/m01-hooks.log`
- `試し-1〜3か月目(改善途中)/council/m01-minutes.md`
- `試し-1〜3か月目(改善途中)/council/m01-policy.md`
- `試し-1〜3か月目(改善途中)/council/m01-port.md`
- `試し-1〜3か月目(改善途中)/council/m01-roads.md`
- `試し-1〜3か月目(改善途中)/council/m01-run.json`
- `試し-1〜3か月目(改善途中)/council/m01-survey-economy.md`
- `試し-1〜3か月目(改善途中)/council/m01-survey-port.md`
- `試し-1〜3か月目(改善途中)/council/m01-survey-roads.md`
- `試し-1〜3か月目(改善途中)/council/m01-urban.md`
- `試し-1〜3か月目(改善途中)/council/m02-assembly.json`
- `試し-1〜3か月目(改善途中)/council/m02-assembly.md`
- `試し-1〜3か月目(改善途中)/council/m02-bill.md`
- `試し-1〜3か月目(改善途中)/council/m02-economy.md`
- `試し-1〜3か月目(改善途中)/council/m02-education.md`
- `試し-1〜3か月目(改善途中)/council/m02-finance.md`
- `試し-1〜3か月目(改善途中)/council/m02-fire.md`
- `試し-1〜3か月目(改善途中)/council/m02-health.md`
- `試し-1〜3か月目(改善途中)/council/m02-hooks.log`
- `試し-1〜3か月目(改善途中)/council/m02-minutes.md`
- `試し-1〜3か月目(改善途中)/council/m02-policy.md`
- `試し-1〜3か月目(改善途中)/council/m02-port.md`
- `試し-1〜3か月目(改善途中)/council/m02-roads.md`
- `試し-1〜3か月目(改善途中)/council/m02-run.json`
- `試し-1〜3か月目(改善途中)/council/m02-survey-finance.md`
- `試し-1〜3か月目(改善途中)/council/m02-survey-health.md`
- `試し-1〜3か月目(改善途中)/council/m02-survey-roads.md`
- `試し-1〜3か月目(改善途中)/council/m02-urban.md`
- `試し-1〜3か月目(改善途中)/council/m03-assembly.json`
- `試し-1〜3か月目(改善途中)/council/m03-assembly.md`
- `試し-1〜3か月目(改善途中)/council/m03-bill.md`
- `試し-1〜3か月目(改善途中)/council/m03-economy.md`
- `試し-1〜3か月目(改善途中)/council/m03-education.md`
- `試し-1〜3か月目(改善途中)/council/m03-finance.md`
- `試し-1〜3か月目(改善途中)/council/m03-fire.md`
- `試し-1〜3か月目(改善途中)/council/m03-health.md`
- `試し-1〜3か月目(改善途中)/council/m03-hooks.log`
- `試し-1〜3か月目(改善途中)/council/m03-minutes.md`
- `試し-1〜3か月目(改善途中)/council/m03-policy.md`
- `試し-1〜3か月目(改善途中)/council/m03-port.md`
- `試し-1〜3か月目(改善途中)/council/m03-roads.md`
- `試し-1〜3か月目(改善途中)/council/m03-run.json`
- `試し-1〜3か月目(改善途中)/council/m03-survey-economy.md`
- `試し-1〜3か月目(改善途中)/council/m03-urban.md`
- `試し-1〜3か月目(改善途中)/council/plan-city.md`
- `試し-1〜3か月目(改善途中)/council/plan-economy.md`
- `試し-1〜3か月目(改善途中)/council/plan-education.md`
- `試し-1〜3か月目(改善途中)/council/plan-finance.md`
- `試し-1〜3か月目(改善途中)/council/plan-fire.md`
- `試し-1〜3か月目(改善途中)/council/plan-health.md`
- `試し-1〜3か月目(改善途中)/council/plan-port.md`
- `試し-1〜3か月目(改善途中)/council/plan-review.md`
- `試し-1〜3か月目(改善途中)/council/plan-roads.md`
- `試し-1〜3か月目(改善途中)/council/plan-urban.md`
- `試し-1〜3か月目(改善途中)/mayor-note.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-assembly.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-economy-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-economy-fix2.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-economy.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-education-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-education.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-finance-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-finance.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-fire-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-fire.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-health-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-health-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-health.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-review0.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-review1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-review2.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk-see.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-desk.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-mayor-field.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-port-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-port-fix2.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-port.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-roads-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-roads.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-urban-fix1.md`
- `試し-1〜3か月目(改善途中)/transcripts/m01-urban.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-assembly.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-economy-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-economy.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-education.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-finance.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-fire.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-health.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-desk-rebill.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-desk-see.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-desk.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-mayor-field.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-port.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-roads.md`
- `試し-1〜3か月目(改善途中)/transcripts/m02-urban.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-assembly.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-economy.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-education.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-finance.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-fire.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-health.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-desk-rebill.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-desk-see.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-desk.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-mayor-field.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-port-recheck.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-port.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-roads.md`
- `試し-1〜3か月目(改善途中)/transcripts/m03-urban.md`
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

#### hooks の拒否

- council-urban `test_place_building`: 1 回
- council-education `Stop`: 1 回

- 2026-10-29T18:27:22+09:00 council-urban `test_place_building`: pay=false(費用なしの建設)は使えない。pay を省くか true にする
- 2026-10-29T18:28:00+09:00 council-education `Stop`: m17-education.md に足りないものがある: 案の欄「市の計画」。書き足してから終える

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 10)
