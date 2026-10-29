# m02 経済観光文化局の案

## 案なし

今月は案を出さない。理由は2つある。

- 2棟目の名所(Official Park など)の候補地を、道路に面した店の跡3か所と、建物の隙間1か所で試したが、どれも置けなかった。街の中は道路の間隔が狭く、名所の6×6(大きさは list_building_types の width, length)が道路に当たる。空き地は道路が要るため、道路下水道局の道を待つ必要がある。
- B の周り(半径150m、n=9)の attractiveness 平均は8で、基準14に届かない。計画の見送り条件に当たる。基準の測り方が確かめられないため、名所の効きは調査で測り直す。

名所の増設は止めず、調査を1件出して、効きを観光客と Tourism で見る。入口と品物の対策は、他局への求めとして計画に残す。

## 調査

- 調査: あり
- 問い: 名所2棟(B、A)の効きが、観光客、訪問、Tourism の収入、B の周りの attractiveness に出るか
- 見る道具と引数: `city_info`(引数なし。tourists.now と visits を見る)、`economy_breakdown`(Tourism の週の収入)、`map_layer` の attractiveness(x=2118、z=482、radius=150、n=9)
- いつ見るか: 見回り1、見回り2、月末
- 何が分かれば次の手が決まるか: 観光客が2,000以上になる、または Tourism が増えたら、空き地3の道を待って候補を準備する。観光客も Tourism も動かなければ、名所の増設を止め、入口と品物の対策に移す。B の周りが n=9 で14を超えれば、基準を n=9 で取り直す
- 担当の問題: 5-1、5-2 観光

## 見たもの

- `list_policies`: 政策は全部で23。有効なのは EducationBoost(週7,940)、BigBusiness(週3,872)。RecreationalUse は無効で費用0、SmallBusiness は無効で週311。policyExpensesPerWeek は10,676。観光への効きの記述はない
- `city_info`: 人口178,859、所持金2,015,489、週の収支 +8,421、観光客1,747(訪問139)、来ない市民 0/0/0
- `economy_breakdown`: Tourism 週42(動かず)。PublicTransport の支出38,200。Monument の支出2,728
- `list_building_types`(service=Monument、解禁済み): 21種。Official Park(6×6、45,000、週128)、Countdown Clock(12×12、37,500、週80)、Fountain of LifeDeath(7×7、30,000、週240)、StatueOfWealth(8×8、25,000、週400)、SeaWorld と ScienceCenter(12×12 と 11×14、20,000、週320)
- `buildings_near`(service=Monument、半径5,000): 8棟。SeaWorld(-1350,-796)、Friendly Neighborhood(2290,972)、Countdown Clock(1765,622)、ScienceCenter(-1130,-804)、Winter Market 01(-1550,-205)、Fountain of LifeDeath(1804,170)、Plaza of Transference(-1560,-855)、Official Park(B、2118,482)
- `map_layer`(attractiveness): B の周り(x=2118、z=482、r=150)は n=5 で平均9、n=9 で平均8。中心は120。A の周り(x=2290、z=972、r=200、n=9)は平均15。新しい候補の店の跡(x=2224、z=-142、r=150、n=9)は平均0
- `zone_summary`(grid=1000): 道路に面した空きの商業(高密度)は、(2500,500) の区域に145。ほかの区域は空きが後ろ側(建物の裏)が多い
- `zone_map`(中心 2000,700 ほか3か所): 街の中は建物が詰まり、道路に面した空きは少ない。(2720,-520) の付近は道路の間隔が狭い。(3250,480) は Regular Park(id 12504)
- `buildings_near`(abandoned=true、店の跡): (2224,-142) の H3 2x2 Shop01(id 8281)、(540,-23) の H3 3x2 Shop04(id 5094)、(-632,132) の H3 3x3 Shop06(id 10642)。ほかに (2999,126) の L3 2x2 Shop19(id 6747)
- `test_place_building`(Official Park、StatueOfWealth、Fountain of LifeDeath、Countdown Clock など): 上の店の跡3か所、(2999,126) は道路と衝突で不可。(2720,-520)、(2720,-600)、(600,-560)、(480,420)、(1500,-480)、(2600,-200)、(2520,-430)は建物か道路と衝突で不可。(712,1644) は AlreadyExists で、道路がないため未確認
- `preview_bulldoze`(x=2224、z=-142、r=25): 壊す建物3棟、失う働き口0、家11。ただし候補としては置けない
- 名所の効きの答え合わせ(m01-1、B): 予想は B の周りの平均が14を超える。結果は測り方で27、9、8と振れる。判定は半分。中心の値120は、名所があるところだけ高い。次の扱い: 続けるが、測り方を n=9 に固定して測る

## 判断の根拠

- 観光: 観光客は1,747で、出発点1,646から増えた。Tourism の収入は週42で、動いていない。観光客が店で使うお金が増えないのは、店に品物が届いていないためとみられる(cargo の品物がない店222)。店は他局の担当なので、今月は求めるだけにする。
- 名所: B は効きが中心に出ている。A は n=9 で9から15に上がった。一方、B の周りの平均は8で、計画の基準14を下回る。基準の測り方が違うため、2棟目は見送り、観光客と Tourism で効きを見る調査にした。
- 2棟目の候補地: 店の跡3か所は、名所が道路に当たった。道路の間隔が狭く、6×6は入らない。試しの道具で確かめた結果、実行条件が揃わないため、案にできない。
- 案の数: 実行できる案がないため0件。調査を1件出す。政策(RecreationalUse、SmallBusiness)は、計画の調整15により、名所と道の結果が出た後の月に回す。

## 捨てたもの

- 2棟目 Official Park を店の跡(8281、5094、10642)に置く案: 名所が道路に当たり、置けない(test_place_building で確認)。
- 2棟目を Regular Park(id 12504、3250,482)の跡に置く案: 既存の公園を壊すため、4-2 の公園の数(Beautification)が減る。取り壊しの議決も要るため、今月は見送る。
- 空き地3(712,1644)の Official Park: 道路がなく、test_place_building は AlreadyExists で未確認。道路下水道局の道が要るため、第5月に確かめる。
- RecreationalUse(無効、費用0)と SmallBusiness(無効、週311): 効きが観光の数で測れていない。調整15により、名所の結果が出てから。SmallBusiness は商業の店が使うため、品物がない店の問題が先。
- 店の消費を上げる商業の税の変更: 商業の需要が2で、税を下げても店が増えない(税の変更は議決が要る)。
