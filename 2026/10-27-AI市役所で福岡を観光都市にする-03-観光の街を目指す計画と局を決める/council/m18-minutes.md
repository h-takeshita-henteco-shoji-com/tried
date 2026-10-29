# 18か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 18:42〜18:43)

- 元のファイル: [m18-policy.md](m18-policy.md)
- ゲーム内の日付: 2051-06-05、保存: fukuoka-plan-m18
- 重点: 5-1、5-2 観光(旅客の入口、島と空き地の名所)、8-1、6-4 貨物センターの止まりと品物がない店、4-4 資源循環(満杯の埋立地4つ)

- 見たもの: [m18-policy.md の「見たもの」](m18-policy.md#見たもの)(16 行)
- 判断の根拠:

  公約4は、観光客が減り Tourism が増えて、2つがそろわなかった。入口と島・空き地の名所は18か月たっても0棟で、局が確かめた案を出せるかが鍵になる。貨物センターの止まりは589で目標の2.4倍、満杯の埋立地は3から4に増えて、どちらも他局の案と重ならない。財政は黒字で余裕がある。

- 捨てたもの:

  - 6-3 交通: 流れは55%に上がり、信号の効きは続いて当たっている。今月は貨物とごみに重点を回す。局の案は出してよい
  - 4-3 汚染: 印は23で目標15に遠いが、焼却場の停止は2回効かなかった。別の手の案が出れば受ける
  - 4-2 公園: 92棟で目標100にあと8。局の案が出れば受ける
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

### 住宅都市みどり局(urban)(hooks の記録で 18:44〜18:47)

- 元のファイル: [m18-urban.md](m18-urban.md)
- 案 urban-1: 道に面した空き(1795,250)に公園 JapaneseGarden を1つ置く
  - 建設費 2500、週の維持費 +40、戻せる
  - 市の計画: 4-2
  - 議決: 要らない

- 見たもの: [m18-urban.md の「見たもの」](m18-urban.md#見たもの)(15 行)
- 判断の根拠:

  - 4-2 の公園は 92 で、目標 100 まで 8 足りない。残り 7 か月で 8 つを置くには、月1つ以上の空きが要る。今月は (1795, 250) の1か所を、確かめた条件で案にした。道路の入口、電気、水、重なりを、試しの道具と map_layer で確かめた。
  - 道に面した空きは少ない(zone_summary で商業高密度の36マスだけ)。放棄店の跡は、働き口か家を失うものが多く、今月は使わない。長期計画の取り壊しの枠は、12か月で働き口 30 以下に収める。
  - 4-1 の地価は 67(基準 66、+1)。公園の効きとは言えない。事業2の判定は第20月に延ばした(計画の変更)。
  - 案は1件にした。ほかの候補は、試しで置けないか、働き口・家を失うため、確かめた条件を満たさない。件数を埋めるための案は作らない。

- 捨てたもの:

  - JapaneseGarden を (1856, -107) に、east で置く案: 道路 3915 に面して置けるが、取り壊す建物(ホテル 2682、店 11517)で働き口が 24 減る。放棄建物ではないため、今月は見送り
  - JapaneseGarden を (2450, 520) に、north で置く案: 取り壊す事務所 3棟で働き口が 55 減る。入口の道もない。見送り
  - JapaneseGarden を (1856, 48) に、north で置く案: 取り壊す建物で家が 2 減り、入口の道がない。見送り
  - (1800, 285)、(1800, 212)、(2290, 540)、(2224, 170)、(2224, 310)、(2224, -452)、(1588, 483)、(2350, 480)、(1880, 110)、(3560, 552)、(3500, 552)、(3620, 590): 試しで、他の建物、道路、サービス建物、風車と重なり、置けなかった
  - Regular Plaza、Regular Playground(5×5)、ParadoxPlaza(5×5): 1795, 285 で重なった。5×5 は 4×4 の JapaneseGarden より大きく、空きに入りにくい。今月は使わない
  - 装飾の駐車場(Decoration Concrete Parking Lot 01、2×4)など: 4-2 の数える対象は公園なので、置く案にはしない
  - 政策の変更: 4-2 に効く政策は一覧にない。今月は政策の案なし

### 道路下水道局(roads)(hooks の記録で 18:44〜18:45)

- 元のファイル: [m18-roads.md](m18-roads.md)
- 案 roads-1: 止まりの多い幹線 z=10 を4車線にする(試し)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m18-roads.md の「見たもの」](m18-roads.md#見たもの)(14 行)
- 判断の根拠:

  - 6-3 の担当で、確かめた候補は1つだけ残った。(1497,62) の止まりは、交差点のない幹線の密度 100 の区間に近く、信号の手は使えない。4車線化は試しの道具が通り、費用と維持費は0で、戻せる
  - 事務所の道(6-1)は、空きが道に面していないことを確かめた。道を通す効きは見込めるが、区間の受け渡しを経済観光文化局から受けた記録がなく、確かめられない。実行の条件が未確認なので、案にしない
  - 名所 11580 と公園 30466 の電気は届いた。事業2は完了し、今月は新しい手を出さない
  - 案は1件。6-3 の残りの手は、必須の条件が未確認か、同じ手の繰り返しになるため

- 捨てたもの:

  - 事務所の空きに面する道(6-1): 空きは道に面していないと確かめた。ただし、区間を経済観光文化局から受けた記録がなく、実行可否が未確認のため。次の月に、受け渡しを経済観光文化局に確かめる
  - 交差点 (1497,62) の信号: 40m以内に交差点がないため、信号は付けられない
  - 幹線 z=100 の Large Road(区間 11179 を含む、`test_upgrade_road`): 区間 11179 が Crematory 29774 にぶつかる。火葬場は取り壊しの対象にしないため、見送る。試しの費用は 200
  - 政策 HeavyTrafficBan(費用0): 貨物の車を減らし、8-1 と 6-4 の目標(品物がない店 191、原料がない工場 31)に逆らう見込み。政策は月1件の上限もあり、今月は出さない
  - 信号 (2155,330) の効きの判定: 基準を台帳に残していないため、今月は判定前。別の信号を足すのは、判定の後

### 港湾空港局(port)(hooks の記録で 18:44〜18:46)

- 元のファイル: [m18-port.md](m18-port.md)
- 案: なし

- 見たもの: [m18-port.md の「見たもの」](m18-port.md#見たもの)(12 行)
- 判断の根拠:

  - 島Bの旅客駅は、担当の数字(旅客の入口 0、目標 1 以上)に最も効く候補です。ただし入口の道の斜面を越える整地が、局の道具では確かめられません。整地の試しは市長の level_terrain で、結果を次の月に受け取ります。確認できない以上、案にしません(局の決まり「必須条件が未確認の場所を、実行対象に含めません」)。
  - 2つ目の貨物センターは、8-1 の止まりに効く見込みがあります。しかし西の候補には電気・水・下水が届いていません。網の延長と入口の位置が未確認のため、案にしません。
  - 前の月の案 port-1(島B の旅客駅)は、17月に条件付きで差し戻され、18月の再調査でも満たせませんでした。整地と入口の確認は今も未確認のままです。
  - 止まりの原因が道の混みか敷地の中の待ちかで、打つ手が変わります。両方の手を決めずに案を出すと、外れる恐れがあります。そこで調査を出します。
  - 案の数は0件です。財政の守る線は余裕がありますが、守る線の余裕は、未確認の案を通す理由になりません。

- 捨てたもの:

  - 島Bの旅客駅(Train Station (-4700,1600) 南向き): 入口の道は約33%の斜面で、整地が要る。整地の試しは局の道具にない。市長に試しを求めるため、今月は出さない。
  - 島Bの旅客駅の別の候補(北 (-4630,1528) など、南 (-4600,1590) など): 置く試しが既存の道・送電線・建物と重なり、置けない。
  - 西の貨物センター (3340,-1555): 置く試しは ok。電気・水・下水が届かず、入口の位置が未確認。網の延長を確かめてから出す。
  - 旅客の入口を別の名所の近くに足す案: 候補地が確かめられていない。今月は時間を使わない。
  - 政策の変更(港や貨物に効く政策なし): 該当なし。

### 経済観光文化局(economy)(hooks の記録で 18:44〜18:47)

- 元のファイル: [m18-economy.md](m18-economy.md)
- 案: なし

- 見たもの:

  - `list_policies`: 政策一覧を取得。観光・商業に関係する政策(RecreationalUse、SmallBusiness など)は前の月の結果どおりで、今月の新しい手にならなかった
  - `city_info`: 人口175,384、所持金2,531,972、週の収支 +10,007、観光客1,783(訪問159)
  - `list_building_types`(service=Monument、解禁済み): 未建設の名所は週320を超える。最安は Transport Tower(建設費60,000、週960、8x12)
  - `buildings_near`(名所、abandoned=true、brief=true など複数回): Monument 10棟。Official Park と Fountain は建設済み。放棄された店の候補は道路や住宅とぶつかる
  - `zone_summary`: 道に面する空きは、商業(高密度)の36マスだけ
  - `zone_map`: 名所の候補地を地図で確かめた。道に面する大きな空きは見当たらなかった
  - `test_place_building`(4回): 名所を放棄された店の跡と道沿いの空きに試した。道路・住宅との重なりや、Official Park と Fountain の AlreadyExists で断られた
  - `net_reach`: 40850 の周りは accessSegment 0(道に入れない)
  - `economy_breakdown`: Tourism 週74
  - `cargo`: 品物がない店 191、原料がない工場 31
  - `demand_breakdown`: 働き口87,258、空き3,480
  - `map_layer`(attractiveness): 平均2、最大25

- 判断の根拠:

  観光の数字(観光客1,783、訪問159、Tourism 74、attractiveness 2)を動かす手は、名所と入口の2つ。名所は、置ける道沿いの空きがなく、解禁済みの候補は週320の枠を超えた。入口は港湾空港局の担当で、今月は求めることを計画に書くだけにする。40850 の道は道路下水道局の担当で、経済観光文化局の案にはしない。確かめていない場所や費用を案に書くと、実行条件が未確認のまま採られるため、今月は案を出さない。来月は、道路下水道局と港湾空港局の返事と、40850 の道の結果を測ってから、観光の手を決め直す。

- 捨てたもの:

  - 名所 Transport Tower(8x12、建設費60,000、週960): 解禁済みの中で最安だが、週320の枠を超える。道沿いの空きも見つからない。
  - 放棄された店の跡への名所: 道路や住宅とぶつかり、取り壊しを仮定した試しでも置けなかった。
  - Official Park と Fountain の再建: 1種類1棟のため、置けない。
  - 40850 への道の経済観光文化局の案: 道路下水道局の担当。経済観光文化局が出すと、担当が重なる。
  - 旅客の入口の案: 港湾空港局の担当。経済観光文化局は求めることを出すだけにした。
  - 政策の追加: 観光の数字に効く政策の見込みを、道具の記述だけでは確かめられない。前の月の RecreationalUse と SmallBusiness の結果も、観光の数字を動かしていない。

### 保健環境局(health)(hooks の記録で 18:44〜18:49)

- 元のファイル: [m18-health.md](m18-health.md)
- 案 health-1: 満杯の埋立地4つを取り壊し、近くに建て直す
  - 建設費 16920、週の維持費 +7、戻せない
  - 市の計画: 4-4
  - 議決: 要る(取り壊し)

- 見たもの: [m18-health.md の「見たもの」](m18-health.md#見たもの)(20 行)
- 判断の根拠:

  満杯の埋立地4つは、ごみの印 12 の止めている分で、担当の4-4 の目標 0 に直接当たる。4つは取り壊しの影響がない(働き口も家も失わない)ので、建て直しを選んだ。北東の候補は7か所のすべてが道路、学校、取り壊しで通らなかった。一方、4か所の建て直し(3か所は支線つき)は試しの道具で通ったので、この案は確認済みの形で出せる。4-3 の汚染は、2267 の移す先が未確認のため、今月は案にしない。次の月に試す(計画の事業2)。案は1件で、取り壊しの議決1つにまとめた。

- 捨てたもの:

  - 北東の埋立地の新設(7か所): 道路、学校、住宅と事務所に重なり、取り壊しは働き口と家を失う。道が通る候補(2868,478)は学校の支線と衝突。断った理由は `test_place_building` と `test_build_line` の結果
  - 2267 の移動(4-3 汚染): 移す先の敷地、電気、水、下水が未確認。今月は確かめられないので案にしない。次の月に候補を試す
  - 埋立地 12880 の空け: 2か月で 95% → 92% と遅い。建て直しのほうが速い
  - 再利用の政策(Recycling): 週の収入が約13,089 減り、守る線 +3,000 を割る

### 教育委員会(education)(hooks の記録で 18:44〜18:45)

- 元のファイル: [m18-education.md](m18-education.md)
- 案 education-1: 小学校 25802 を1校止める(3校目、試し)
  - 建設費 0、週の維持費 +-160、戻せる
  - 市の計画: 2-3
  - 議決: 要らない

- 見たもの: [m18-education.md の「見たもの」](m18-education.md#見たもの)(9 行)
- 判断の根拠:

  - 2-3 は満たしている: 小学校 13,572 ≥ 子ども 8,929(1.52倍)、高校 24,360 ≥ 10代 18,390(1.32倍)。
  - 43936 の結果: 0 はなし。ただし SW 角の最小が 8 から 3 に下がったため、3校目は SW 角の覆いに効く 43393 と、同じ地区の 15022 を外した。
  - 25802 の候補: 窓の中心の覆いは 127 で、近くの覆いは他の小学校でも残る見立て(寄与は道具で分けられない)。止めた後の定員 13,224 は子どもの 1.48倍で、1.3倍を保つ。
  - 費用: 週 -160(約 -200)。週の収支 +10,007 は守る線 +3,000 の上にあり、財政の圧力はない。効果は小さいが、計画の18月の予定どおりなので出す。
  - 案の数: 1件。高校は余裕 5,970(132%)で基準 1,000 を大きく上回るため、置かない。

- 捨てたもの:

  - 高校を1校置く: 余裕 5,970 で基準 1,000 を大きく上回る。建設費 24,000 と週 560 の増えが要るため、今月は置かない。
  - 小学校 43393 を止める: SW 角の覆い(43936 の窓の最小 3)に効くと見て、0 が出るリスクが高い。
  - 小学校 15022 を止める: 15301 と同じ地区で覆いを重ねて減らす。候補に入れない。

### 消防局(fire)(hooks の記録で 18:44〜18:46)

- 元のファイル: [m18-fire.md](m18-fire.md)
- 案 fire-1: 焼け跡の建物 1573 を取り壊す
  - 建設費 0、週の維持費 +0、戻せない
  - 市の計画: 3-4
  - 議決: 要る(取り壊し)

- 見たもの: [m18-fire.md の「見たもの」](m18-fire.md#見たもの)(11 行)
- 判断の根拠:

  18月の数字は、3-4 の合計が2(火事1、犯罪1)で、目標の4以下を達成している。事業3の届きは 4→130 に上がり、判定は当たりで完了した。焼け跡の建物 1573 が火事の印を出しているため、計画の事業1(焼け跡が出た月の手)に従い、取り壊しを1件出す。失う家と働きは0で、対象は1件に固定できる。効きは火事の印1つ分で小さいが、焼け跡を残す理由がない。案は1件に留める。事業2は、18月の火事の場所 (1012,-1036) が16月の場所(1197,-1019)から約185m離れるため、同じ場所の追跡はまだ続けない。

- 捨てたもの:

  - SmokeDetectors(煙探知機の政策): 週57,902 で、守る線の余裕 7,007 を大きく超えるため、採らない
  - 犯罪の印1(40850)への警察署の追加: 合計は目標内で、警察の使用は 425/1,000 に余裕がある。今月は置かない
  - 火事の調査(同じ場所の火元調査): 18月の火事は1件で、場所も前月と違う。2か月続くまで出さない
  - 消防署を (1012,-1036) 付近に追加: 届きは60〜139 で0の地点がなく、届きを上げる根拠がない

### 財政局(finance)(hooks の記録で 18:44〜18:51)

- 元のファイル: [m18-finance.md](m18-finance.md)
- 案 finance-1: 医療の予算を 130 から 110 に下げる
  - 建設費 0、週の維持費 +-10192、戻せる
  - 市の計画: 6-3
  - 議決: 要る(予算)

- 見たもの: [m18-finance.md の「見たもの」](m18-finance.md#見たもの)(15 行)
- 判断の根拠:

  - 財政の数字は守る線を上回っている(週の収支 +10,007、所持金 2,531,972)。今月の課題は、守る線を割らずに観光の維持費の余裕を増やすこと。
  - 税は動かさない。人口の減りの原因が s17-2 の結果で決まらないため。住宅の税収は 261,279 と大きく、1点の効きは未測。見立てで動かすと、守る線の余裕を使う。
  - 政策は動かさない。政策一覧は効果を書かず、今の政策の効きも切り分けられていない。
  - 医療の予算は、前例で比例の効きが確かめられ、使用率が低い(748/5,100)。健康は 87 で目標 80 を上回る。130→110 は ±20 の上限内。予算の案として出す。
  - 案の数は1件。ほかの候補は捨てた。

- 捨てたもの:

  - 住宅の税(低密度 9→8 など): 人口の原因が未確定で、1点の効きが未測。住宅の税収は 261,279 と大きく、守る線の余裕 約 7,000 に対して大きすぎるおそれがある。今月は見送る
  - 政策 HighTechHousing(有効化): 週 20,260 で、守る線の余裕を超える。効きも未確認。出さない
  - 政策 SmallBusiness(有効化): 週 313 と小さいが、前の試し(m02-4)の Tourism の動きは他の政策と切り分けられなかった。今月は出さない
  - 政策 RecreationalUse(有効化): 費用 0 だが、前の試し(m03-1)で attractiveness は平均2のまま動かなかった。今月は出さない
  - 教育の予算 120 を下げる: 覆いの最小が 3 と低く、予算を下げると覆いが 0 になるおそれがある。教育局の担当で、財政局は案を出さない
  - ごみの予算: すでに 150 で上限。増やせない

## 4. 差し戻しと再調査

- 財政局: finance-1(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m18-bill.md](m18-bill.md)
- 採った m18-1: 空き(1795,250)に公園 JapaneseGarden(元 urban-1、議決は要らない)
- 採った m18-2: 幹線 z=10 の3区間を4車線にする(試し)(元 roads-1、議決は要らない)
- 採った m18-3: 満杯の埋立地4つを取り壊して建て直す(元 health-1、議決が要る(取り壊し))
- 採った m18-4: 焼け跡の建物 1573 を取り壊す(元 fire-1、議決が要る(取り壊し))
- 採らなかった finance-1: 医療予算の下げは墓地・火葬場と霊柩車にも響くが、deathcare の容量と使用、Death 42 との関係が未確認。
- 採らなかった education-1: 43936 の窓の最小が3で、重なる 25802 を同月に止めると調査 s18-2 の測りを濁す。節約は週160で急ぎもない。

- 見たもの:

  - `m18-urban.md` ほか8局の案と、`m18-policy.md`、`plan-city.md`、`m17-bill.md`、`mayor-note.md`(月例18か月目)
  - 各局が道具で確かめた結果(`test_place_building`、`test_build_line`、`test_upgrade_road`、`preview_bulldoze`、`map_layer` など)は局の案の値を使った。市長は街の道具を呼んでいない

- 判断の根拠:

  確認済みの4件を採った。公園1つと4車線化は議決が要らず費用が小さい。埋立地4つの建て直しと焼け跡の取り壊しは、失うもの(働き口・家)が0と `preview_bulldoze` で確かめられており、議決は取り壊しの2件。分からないことの一覧が残るため、試しは m18-2(信号の効きの揺れ)を採った。費用は建設費 19,420、週の維持費の増え 約47で、守る線(週 +3,000、所持金 1,874,000)の上に収まる。財政局の医療予算は deathcare への響きが未確認のため差し戻す。重点1(観光)は、港湾空港局と経済観光文化局が案なしのため、今月は施策に当たる手がない。

- 捨てたもの:

  - finance-1: 医療予算の下げ。deathcare への響きが未確認。条件付きで差し戻す
  - education-1: 25802 を止める案。重なる窓の測りを濁す。19月以降に出し直せる
  - 観光の入口と名所(重点1): 局が案を出せなかった。市長は代案を作らない
  - 政策の変更、税の変更: 局の案になく、今月は動かさない

## 6. 議会: 可決と否決(hooks の記録で 18:53〜18:53)

- 元のファイル: [m18-assembly.md](m18-assembly.md)
- m18-1 財政: 可決。建設費2,500、週40で守る線に余裕がある。
- m18-2 財政: 可決。費用0、維持費0で戻せる試し。
- m18-3 取り壊し: 可決。失うものは働き口0・家0。代わりの手と比べてあり、4-4に沿う。
- m18-4 取り壊し: 可決。失うものは0と数字で書かれ、残す手と比べてある。
- 可決した種類(hooks が見る): 取り壊し

- 見たもの:

  - `city_info`: 所持金 2,531,972、週の収入 338,572、支出 328,565
  - `council/m18-bill.md`: 4施策の費用、失うもの、予想

- 判断の根拠:

  費用の合計は守る線(週 +3,000、所持金 1,874,000)を大きく上回る。下降規則の +4,900 も切っていない。取り壊し2件は、失うものと代わりの手が書かれている。外れた手の続きや、市の計画に逆らう施策は見当たらない。

- 捨てたもの:

  - m18-3: 取り壊し費用が未確認で戻せない手だが、失うものは 0 と書かれ、財政にも余裕があるため可決した。

## 7. 実行する市長: 実行と見回り(hooks の記録で 18:53〜19:00)

- 実行してよい施策: m18-1、m18-2、m18-3、m18-4
- 実行した: m18-1、m18-2、m18-4
- 失敗した: m18-3
- 臨時: なし
- 見回り 2051-06-15: 人口 175191、所持金 2528819、週の収支 10767、幸福度 88
- 見回り 2051-06-25: 人口 175100、所持金 2544341、週の収支 10493、幸福度 88
- 報告:

  4件中3件を実行し、m18-3 は一部だけ実行しました。公園 18474(Beautification 92→93)、幹線 z=10 の4車線化(blocked 67→37、測りは揺れる)、焼け跡 1573 の取り壊しは議案どおりです。m18-3 は埋立地4棟を壊して建て直し、満杯は4→1(3565 のみ)に減りました。ただし支線3本は建て直した埋立地の敷地と重なって引けず、3棟(23459、10676、33216)は入口に道がなく RoadNotConnected です。月末は 2051-07-05。人口 174,778、所持金 2,555,946、週の収支 +7,740、観光客1,795。臨時の境目には当たりませんでした。調査 s18-1 と s18-2 は council の m18-survey-port.md と m18-survey-education.md に書きました。市政ノートとログ(command-log.txt)も保存済みです。

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m18、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 18:41〜19:10(hooks の記録の時刻から)、道具の行 257
- 議会が可決した種類: 取り壊し
- 議決が要る道具の呼び出し: 5 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 610 件
- hooks の拒否: 0 回

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

台帳: [ledger.jsonl](ledger.jsonl)(この月の行 8)
