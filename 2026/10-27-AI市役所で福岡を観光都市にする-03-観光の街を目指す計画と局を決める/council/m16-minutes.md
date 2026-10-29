# 16か月目の議事録

make_council_minutes.py が、各役のファイルと Workflow の返り値をつないで作った。新しい判断は書いていない。
長い欄は元のファイルへのリンクにした。

## 1. 市長: 見た数字と編成方針(hooks の記録で 18:04〜18:05)

- 元のファイル: [m16-policy.md](m16-policy.md)
- ゲーム内の日付: 2051-04-06、保存: fukuoka-plan-m16
- 重点: 5-1・5-2 観光(入口、名所、島・空き地)、8-1・6-4 貨物センターの止まりと品物がない店、4-2 花や緑による潤い(公園)

- 見たもの: [m16-policy.md の「見たもの」](m16-policy.md#見たもの)(15 行)
- 判断の根拠:

  前月の6施策はすべて予想どおりかほぼ当たり、週の収支が +12,150 に戻って守る線に余裕ができた。観光は人数と収入が前月より増えたが、入口0と attractiveness 平均2が16か月動かず、市長の方針でもあるので第1の重点にした。貨物センターの止まり(671)は8-1 の目標の2.7倍で最も目標から遠いため第2に、公園は目標に10棟と近く、確かめられた手が続くため第3にした。

- 捨てたもの:

  - 6-3 公共交通を主軸とした交通体系: 流れ53%(目標60)は3月の55%から下がったが、信号の効きが揺れて測れない。局が案を出すなら受ける
  - 4-3 脱炭素社会: 汚染の印21(目標15以下)は2月の18から悪化したが、出どころが分からず、重点にするほどの手がない。試しの案が出れば受ける
  - 6-1 都心部の機能強化: 事務所L3 3,281は目標3,500に遠いが、税を動かしても効かなかった(m09、m11)。重点にしない
  - 4-1、1-2、3-3、3-4、2-3: 目標に達したか、あと少しで、今月の重点にしない

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

### 住宅都市みどり局(urban)(hooks の記録で 18:06〜18:09)

- 元のファイル: [m16-urban.md](m16-urban.md)
- 案 urban-1: 道に面した空き地(1820,355)に公園 JapaneseGarden を1つ置く
  - 建設費 2500、週の維持費 +40、戻せる
  - 市の計画: 4-2
  - 議決: 要らない

- 見たもの: [m16-urban.md の「見たもの」](m16-urban.md#見たもの)(13 行)
- 判断の根拠:

  - 4-2 は 90 で、目標 100 まで10。第16〜24月に1か月1つの計画のとおりに、今月は1つ置く。
  - 計画は放棄店の跡を第一候補にしていたが、今月 放棄店の跡を10か所試したところ、置けるものがなかった。残りは稼働中の店を壊す(働き口 6〜17 を失う)、道に面していない、家を失う、のいずれか。計画の決まり(空きに置けるなら空きに置く)に従い、空き地の (1820, 355) を選んだ。
  - (1820, 355) は、道に面し(入口の道まで1m)、壊す建物がなく、電気と水が届く。費用は 2,500 で、所持金は足りる。
  - 予備は (1820, 300)。同じ道沿いで、道に面し、壊す建物がない。
  - 案の数は1件。計画の今月の予定は1つだから。試しは出さない。
  - 調査は出さない。原因が分からない問題はない。

- 捨てたもの:

  - 放棄店の跡の候補(試した10か所): (2176, 222) は既存の公園 12077 に重なる。(2224, 170) は道と建物に重なる。(1856, 236) は働き口15を失い、入口に道がない。(2176, -6) は建物 41234 に重なる。(2228, 102) は道に重なる。(2168, 18) は稼働中の店 1045(働き口8)を壊し、入口に道がない。(1856, -132) は稼働中の店 1110(働き口6)を壊し、入口に道がない。(2128, 613) は働き口17を失う。(2176, 703) は働き口10と家6を失う。(1856, -287) は働き口15を失い、入口に道がない。いずれも12か月の失う働き口の上限(30以下)に響くため、今月は採らない。
  - Regular Park(1,000、週8)の (1820, 355): 9×8 の大きさが道路に重なり、置けない。
  - HighTechHousing(政策): 週 20,268 で守る線を割る。4-1 への効きも確かめられていない。
  - 4-1 の地価を、公園の周りで測る以外の手: 今月は計画の予定にない。第18月に事業2の判断をする。

### 道路下水道局(roads)(hooks の記録で 18:06〜18:09)

- 元のファイル: [m16-roads.md](m16-roads.md)
- 案 roads-1: 交差点 (1692,100) に信号を置き、東の止まりを減らす
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m16-roads.md の「見たもの」](m16-roads.md#見たもの)(24 行)
- 判断の根拠:

  - 6-3 の交通の流れ 53%(目標 60%)に効く場所を、`traffic` の blocked 上位で探した。最も多いのは (1703,104) の 64 台で、Large Road が Medium Road へ細くなる交差点の近く。道を太くする案は、High School 1226 と Bus Depot 30483 にぶつかって断られたため、信号にした。
  - 信号は、13月と15月に同じ手で blocked が 51→30、26→9 と下がった実績があり、建設費が 0。交差点が canEnableLights の条件を満たし、実行条件は確認済み。
  - 名所 11580 と公園 30466 の電気(5-1、4-2)は、送電線の経路を8通り試したが、どれも建物の敷地にぶつかった。電気が通る位置が決まらないため、今月の案にしない。事業2として17月と18月に経路を探す。
  - 案の数は1件。ほかの候補は、同じ手(信号)か、学校の取り壊しを要するか、確認できる経路がないため。件数を埋めるための案は作らなかった。
  - 調査は出さない。止まりの原因は、この交差点の付近で分かっている(細くなる所)。東の出口(3297)の止まりは、16月の計画の調査で場所が動いていたが、17月の手に回す。

- 捨てたもの:

  - 交差点 (1692,100) の道を Medium から Large へ太くする案: `test_upgrade_road` が断った。High School 1226(1640,134)と Bus Depot 30483(1652,66)を取り壊す必要があり、学校の定員と働き口が減る。取り壊しの案は、学校を残す代わりの手を比べたうえで、今月は出さない
  - 名所 11580 と公園 30466 に電気を引く案: `test_build_line`(Power Line)で8通りを試したが、どれも建物の敷地に当たって断られた。電気が届く位置が未確認のため、実行可にできない。17月と18月に経路を探す(事業2)
  - 交差点 (2648,691) の信号: 近くに交差点がなく(`junction_info` 40m 以内になし)、信号を置ける位置を確かめられなかった。17月に探す
  - 交差点 (-937,-694) の信号: 同じ手の別の場所で、今月の案は1件に絞った。17月の候補
  - HeavyTrafficBan(トラックを減らす政策、週0): 6-3 の流れに効く見込みはあるが、8-1 と 6-4 の荷物の流れを止めるおそれがあり、経済・港湾の局の担当を動かす。政策の変更は市長が決める
  - 経済観光文化局の事務所の道の区間(16月の依頼): この月の依頼の中身は読んでいない(他局の案は読まない)。18月の案に持ち越す

### 港湾空港局(port)(hooks の記録で 18:06〜18:08)

- 元のファイル: [m16-port.md](m16-port.md)
- 案: なし

- 見たもの: [m16-port.md の「見たもの」](m16-port.md#見たもの)(21 行)
- 判断の根拠:

  - 駅(島B): 第16月の試しで、駅本体は断られず、入口の道は傾きが原因で断られると分かった。仮定の整地(71.5m)で道が通ると確かめた。実際の整地の費用と土は未確認。駅の案は、Boost の判定(16月末)の後の第17月に出す(調整3)。
  - 8-1: 空き待ちは減らない。道の混みではなく、敷地の内側の受け入れが詰まっていると見る。入口はすでに2本あり、東側に道もないため、入口の道を足す根拠がない。13893 が車を出していない理由を見るのが、いまの最も近い手段になる。
  - 案の数: 今月は0件。駅は第17月の計画、8-1 は調査の結果を待つ。

- 捨てたもの:

  - 28755 に入口の道を足す案: 道の混みが見えず(blocked 0)、入口はすでに2本あるため効く根拠がない。道を試すのは、13893 の調査の結果が出てから
  - 28755 の振り分けを 3940 や 4740 へ移す案: 両方とも車が0で、振り分けの道がない(第15月の確認)
  - 新しい貨物駅の建設(Cargo Center 60,000、維持費1,440): 置く場所と鉄道の接続が未確認。列車がつながらなければ車は出ず、週の維持費だけ増える
  - 政策 RecreationalUse・SmallBusiness の有効化: m03〜m05 の試しで、観光の数字と切り分けられなかった。今月は動かさない

### 経済観光文化局(economy)(hooks の記録で 18:06〜18:15)

- 元のファイル: [m16-economy.md](m16-economy.md)
- 案 economy-1: 空き地3に Transport Tower を置く(試し、再調査)
  - 建設費 62040、週の維持費 +978、戻せる
  - 市の計画: 5-1、5-2
  - 議決: 要らない

- 見たもの: [m16-economy.md の「見たもの」](m16-economy.md#見たもの)(23 行)
- 判断の根拠:

  確認した事実は次のとおり。空き地3(712,1644)の道、電線、水管は、道具で重なりなく引けた。建物の (712,1730) は、取り壊しなしで置ける。ほかの候補は、取り壊しが要るか、道具で置けなかった。
  - 西中央 (-1500,-500): 置けるが、住宅と店の7棟を取り壊す(働き口 97、家 31 を失う)。取り壊しの議決が要るため、今月は出さない
  - 西 (-690,-60): 13棟を取り壊す(住宅 72、働き口 56)。出さない
  - 東 (2600,-1000) Observatory: 道がなく、住宅3棟(家9)を取り壊す。出さない
  - 中央 (500,-500)、東 (2500,-500)、東の空き (3455,-270)、(3620,-270)、(3620,-370)、(3450,-390)、(3720,-440)、(3300,-400): 風力、事務所、学校、道と重なり置けない
  - 北東の空き地4 (1728,3269)、空き地5 (4545,2382): 置けるが、道が400m以内にない。道、電線、水管が数 km 要る
  案は1件に絞った。ほかの地区は、置くために住宅か働き口を壊すか、道と水管が長くなる。案1は、取り壊しなしで、既存の道・電線・水管につながる。3地区の条件は、西中央・西・東・北東で確かめた。
  ### 注意(調整8)
  案1の建物は週960で、調整8(名所は週320以下の1棟まで、2267停止後に2棟まで)を超える。2267は停止していない。調整14(医療予算130)で維持費の枠が空いたことを理由に、この案を出す。採るかは市長が決める。採られなければ、名所は10棟で保つ。
  ### 事務所の道(6-1、働き口)
  16月に別の帯を探した。道に面する事務所の空きは0だった(zone_summary の Office 1,642 の空きは、すべて道の背後)。区間を渡せないので、事務所の道は閉じる。

- 捨てたもの:

  - 2件目の名所(西中央 (-1500,-500) の Transport Tower、西 (-690,-60)、東 (2600,-1000) の Observatory): 住宅と働き口を失う取り壊しが要る。今月は出さない
  - 空き地4 (1728,3269)、空き地5 (4545,2382): 建物は置けたが、道と電線と水管が数 km 要る。費用と操作の上限に収まらない
  - 事務所の道(別の帯): 道に面する事務所の空きが0。区間を渡せないので閉じる
  - 政策 RecreationalUse の有効化: m03 に採ったが効きは見られず、m04 に外れた。今月は戻さない
  - 島B(-4862,1731、能古島の候補): 水と下水の網が700m以上離れ、接続が未確認。今月は外す

### 保健環境局(health)(hooks の記録で 18:06〜18:08)

- 元のファイル: [m16-health.md](m16-health.md)
- 案 health-1: 焼却場 2267 を止め、汚染の印を減らす(試し)
  - 建設費 0、週の維持費 +-1440、戻せる
  - 市の計画: 4-3
  - 議決: 要らない

- 見たもの: [m16-health.md の「見たもの」](m16-health.md#見たもの)(16 行)
- 判断の根拠:

  - 汚染の印 21 は目標 15 以下に6足りない。近くの 2267 は止めれば汚染を減らした前例(m02-3: 45→35)がある。ごみは 4 で、停止の条件(9以下、満杯0、東の埋立地の空き)を満たした。埋立地 39575 は 7% なので、運搬先の余裕は十分と見込む。電気の余裕も確かめた(容量 2,318,624 に対し使用 1,707,040)。維持費は約 -1,440 で減る。以上から、試しとして案1を出す。
  - 死体の印は、東の火葬場 39843 の処理が 0 / 週で、霊柩車が東の幹線の混みで止まっていた。原因の道路の混みは、局の手の外(道路下水道局の担当)にある。案は出さず、道路の混みとして求めることに渡す。混みが続くかを見るため、調査を1件出す。
  - 案は1件。政策の Recycling は、住宅の税収 -5% の額が確かめられず、週の収支の守る線(+3,000)との余裕を見られないので出さない。

- 捨てたもの:

  - 政策 Recycling を有効にする(ごみ -15%、週の費用 0): ごみの印 4 を 0 に近づける手として比べた。ただし住宅税収 -5% の額を道具で確かめられていない。政策の変更は月1件で、2267 の試しと同じ月に行うと効きが混ざる。来月以降、税収の額を確かめてから出す。
  - 東の火葬場を増やす(Crematory 25,000、週 720、または墓地 8,000、週 160): 東にはすでに火葬場 39843 と墓地 9364 があり、死体の印は、場所が遠いのではなく霊柩車の道の混みで起きている。足しても混みは減らない。取り下げ。
  - 霊柩車の混みを減らす道路の拡張: 道路下水道局の担当で、局の案にできない。求めることとして市長に渡す(今月の案には入れない)。

### 教育委員会(education)(hooks の記録で 18:06〜18:07)

- 元のファイル: [m16-education.md](m16-education.md)
- 案: なし

- 見たもの: [m16-education.md の「見たもの」](m16-education.md#見たもの)(11 行)
- 判断の根拠:

  - 小学校: 定員 13,920 が子ども 8,782 の1.59倍で、15301 を止めた後も1.3倍を超える。覆いの最小 17 は0ではない。止めた効きは週 -160 の維持費の減りで、2校目を止めると定員は 13,572 になり、1.55倍で1.3倍を保つ。ただし、2校目(43936)の覆いが他校で保てるかは、止める前後の寄与を道具で切り分けられない。覆いは学校ごとの寄与を返さないため、17月に調査の結果を見てから決める。
  - 高校: 余裕 5,297(128%)で、1,000 の基準を大きく上回る。休止を続ける。
  - 2-3 の目標(小学校と高校の定員が、子どもと10代以上)は、今月も満たしている。
  - 週の維持費の減りは約 -160(-200)で、週の収支 +12,150 に対して小さい。覆いの確かめが1か月分しかないため、今月の2校目は見送る。
  - 案の数: 0件。学校の定員は目標を満たしており、今月の手は観察と覆いの調査だけで足りる。

- 捨てたもの:

  - 小学校 43936 を止める(2校目): 定員の比は1.55倍で条件を満たすが、止めた後の覆いの0を道具で確かめられない。覆いの寄与を切り分けられないため、17月に調査の結果を見てから決める。
  - 小学校 15022 を止める: 15301 と 90m しか離れず、同じ地区の覆いを一度に減らす。候補に入れない。
  - 高校を1校置く: 余裕 5,297 で基準(1,000)を大きく上回る。建設費 24,000 と週 560 の増えが要るため、今月は置かない。

### 消防局(fire)(hooks の記録で 18:06〜18:15)

- 元のファイル: [m16-fire.md](m16-fire.md)
- 案 fire-1: 火事の集まる住宅地に消防署を置く(Fire House、送電線1本)
  - 建設費 12040、週の維持費 +561、戻せる
  - 市の計画: 3-4
  - 議決: 要らない

- 見たもの: [m16-fire.md の「見たもの」](m16-fire.md#見たもの)(29 行)
- 判断の根拠:

  - 担当の数字は、火事の印 4 と犯罪の印 1 で、合計 5。目標の 4 以下より1多い。犯罪の印は、事業3(警察署)の効きで、32211 付近から消えた(当たり)。残りの火事は、住宅の3棟が消防の届き 11(0 に近い区域)にあり、消防署が街にない。
  - 焼け跡ではなく、住んでいる建物(住民 31)なので、事業1(取り壊し)は当たらない。火元の2か月の追跡(事業2)は、15月の記録がなく、同じ場所かは未確認。調査で続けて見る。
  - 消防署の手は、Fire House 12,000(維持 560)。週の収支 +12,150 の余裕で収まる。SmokeDetectors(週 57,718)は収支に合わない。
  - 案は1件。電気が未確認なので、実行可否は未確認。2件目は、担当の問題に効く別の手が確かめられないため出さない。
  - 調査は1件: 火事の場所の続きと届きの効き目を、見回りと月末で追う。

- 捨てたもの:

  - 消防署 Fire Station(60,000、維持 1,440): 届きは Fire House と同じ区域に出るが、費用が5倍。まず Fire House を試す。
  - SmokeDetectors 政策: 週 57,718。週の収支 +12,150 では払えず、守る線(+3,000)を割る。
  - (1320,-1040) 付近の Fire House: 道路(入口)が未確認。(1325,-1055) に替えた。
  - (1050,-1110) の Fire House: 図書館 37605 と重なる。
  - (1325,-1100) の Fire House: 入口道路がない。
  - (1265,-1100) の Fire House: 取り壊しが要り(住宅 16家)、取り壊し案が要る。今月は外す。
  - 犯罪の印 1棟(40850、(1580,-530)): 届きは 100 以上の区域。原因は道の未接続で、消防局の手ではない。道路下水道局の担当。

### 財政局(finance)(hooks の記録で 18:06〜18:10)

- 元のファイル: [m16-finance.md](m16-finance.md)
- 案 finance-1: 公共交通の運賃を無料にする試し(FreeTransport)
  - 建設費 0、週の維持費 +0、戻せる
  - 市の計画: 6-3
  - 議決: 要らない

- 見たもの: [m16-finance.md の「見たもの」](m16-finance.md#見たもの)(10 行)
- 判断の根拠:

  - 週の収支は +12,150 で、守る線 +3,000 に9,150の余裕がある。所持金 2,473,305 は守る線 1,874,000 より十分上。政策の試しを1件入れても、守る線を割らない
  - EducationBoost は第16月末の判定で条件を満たし、残す。医療 130 は健康 88 を保ち、支出も減ったので、第17月まで保つ
  - 観光を伸ばす財政の手は、前の月の試し(SmallBusiness、RecreationalUse、商業の税)がどれも効きを示せていない。局から出せる観光の手は今は見つからない。貨物の止まり(6-4、8-1)は、財政の手(税、予算)で動かす根拠が見つからない
  - 政策の枠は1か月1件。候補は FreeTransport(費用は運賃の収入の減りだけ、戻せる)と IndustrySpace(費用4,779/週、効きは未確認で、働き口の空き3,097があるため働き手の不足が原因かもしれない)。費用が小さく戻せる FreeTransport を、6-3 の試しとして1件出す
  - 案は1件にした。政策の枠が1件のため、2件目の政策は出せない。税・予算の案は、判定の根拠が足りないため出さない

- 捨てたもの:

  - IndustrySpace(政策、週 4,779): 6-4 の働き口を増やす見込みはあるが、空きの働き口が 3,097 あり、働き手の不足が原因かどうかが未確認。効きが測れず、政策の枠を1件しか使えない今月は、費用が大きい方を後に回す
  - 医療の予算をさらに下げる(130 → 110 など): 健康 88 は目標 80 を上回るが、第17月の判定を待つ。今月は2回目の変更をしない
  - 商業(低)の税を 9 → 7(観光の収入の試し): 前の月の商業の税の試しが効きを示していない(m01-finance-3 は不採用、m09 の事務所税は働き口に効かなかった)。今月は重ねない
  - 道路の予算を 120 → 140(交通の流れの試し): 道路の予算は市全体にかかり、交通の流れの効きが信号と分けられない。案1の政策の試しと同じ数字を測るため、今月は重ねない

## 4. 差し戻しと再調査

- 経済観光文化局: economy-1(実行可 False)
- 消防局: fire-1(実行可 False)

## 5. 市長: 採った施策と採らなかった案

- 元のファイル: [m16-bill.md](m16-bill.md)
- 採った m16-1: 空き地(1820,355)に公園 JapaneseGarden(元 urban-1、議決は要らない)
- 採った m16-2: 交差点(1692,100)に信号(元 roads-1、議決は要らない)
- 採った m16-3: 焼却場2267を止める(試し)(元 health-1、議決は要らない)
- 採った m16-4: 政策 FreeTransport の試し(元 finance-1、議決は要らない)
- 採らなかった economy-1: 建物の port と下水が未確認で、週の維持費約978が調整8の枠を超える。
- 採らなかった fire-1: 電気が建てて確かめるまで未確認のため、必須条件が残る。

- 見たもの:

  - `explain` 以外の街の道具は使っていない。局の案 8件(`council/m16-*.md`)と編成方針 `council/m16-policy.md`、市政ノートの数字の表と m16 月例を読んだ
  - `city_info`(局の案から): 人口 176,528、所持金 2,473,305、週の収支 +12,150、観光客 1,937
  - `traffic`(局の案から): 流れ 53%、止まった車 862。(1703,104) r100 は blocked 64
  - `complaints`(局の案から): Pollution 21、Garbage 4、Fire 4、死亡 32

- 判断の根拠:

  採れる案は4件(urban-1、roads-1、health-1、finance-1)で、実行条件が確かめられている。費用は、建設費 2,500、週の収支は約 +12,150 -4,796 +1,440 -40 = 約 +8,750 で、守る線 +3,000 の上。所持金も約 2,470,000 で線の 1,874,000 の上。分からないことの一覧からは、汚染の出どころ(m16-3)と6-3 の効き(m16-4)を試しにした。場所が重なる試しは出ていない。観光(重点1)の案 economy-1 は接続が未確認で、島や入口の案は port が第17月に回したため、今月は施策にできない。

- 捨てたもの:

  - economy-1: 必須条件(建物の port、下水)の未確認と維持費の枠超え。条件付きで、同じ月に1回調べ直す。
  - fire-1: 電気が置いてから確かめる前提。条件付き。
  - 調査 fire(火事の印の続き): 上限3件のため。fire-1 の調べ直しで電気の経路を確かめる。
  - 調査の追加の代案づくり: 市長は代案を作らない。port と education の案なしは、局の役割から外れた理由ではなく、計画の月が違う、と読んだ。

## 6. 議会: 可決と否決(hooks の記録で 18:16〜18:16)

- 元のファイル: [m16-assembly.md](m16-assembly.md)
- m16-1 財政: 可決。建設費2,500、維持費+40で守る線に響かない。
- m16-2 財政: 可決。建設費0。収支の余裕で維持費の増えを吸収できる。
- m16-3 財政: 可決。維持費が約1,440減る。ごみの印の上限と戻す手が書かれている。
- m16-4 財政: 可決。運賃収入が約4,796減っても見込みは約+8,750で線+3,000の上。
- 可決した種類(hooks が見る): なし

- 見たもの:

  - `city_info`: 所持金 2,473,305、週の収支 +12,150、観光客 1,937
  - `economy`: 税と予算の現状。今月の議案に税と予算の変更なし
  - `council/m16-bill.md`: 4件の施策と調査3件

- 判断の根拠:

  議決が要る施策はなく、4件とも点5だけで確かめた。見込みの週の収支は約 +8,750 で、+3,000 を大きく上回る。収支は +4,900 を切っておらず、下降の規則の対象でもない。m16-3 は4-4 のごみの印を一時的に悪くし得るが、上限と戻す手が書かれている。

- 捨てたもの:

  - m16-4: 運賃収入の減りが最大だが、線に余裕があり、試しの枠として可決した。

## 7. 実行する市長: 実行と見回り(hooks の記録で 18:17〜18:24)

- 実行してよい施策: m16-1、m16-2、m16-3、m16-4
- 実行した: m16-1、m16-2、m16-3、m16-4
- 失敗した: なし
- 臨時: あり
- 見回り 2051-04-16: 人口 176242、所持金 2483188、週の収支 8218、幸福度 88
- 見回り 2051-04-26: 人口 176042、所持金 2491964、週の収支 5951、幸福度 88
- 報告: 長いので [市政ノート](../mayor-note.md) を見る(1048 字)

## 8. hooks の拒否と、型から外れたこと

### 型から外れたことの確かめ(m16、check_council_month.py)

- 見た範囲: command-log.txt の 2026-10-29 18:03〜18:34(hooks の記録の時刻から)、道具の行 361
- 議会が可決した種類: なし
- 議決が要る道具の呼び出し: 0 回
- 議決のない呼び出し: 0 回
- 臨時(advance の後)の呼び出し: 0 回
- 許されていない Write: 610 件
- hooks の拒否: 0 回

#### council/ にある、決まりにない名前のファイル

- `m16-fire-zone.jpg`

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
