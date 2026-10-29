# m03 査定調書

## 案ごとの査定

### urban-1(住宅都市みどり局): 座標(2688, 880)に Regular Plaza を1棟

- 査定: 可
- 理由: 建設費は 2,500(`test_place_building` で確認、ok=true、enoughMoney=true)。建設費の上限 1,050,000 の内。週の維持費の増えは 32(`list_building_types` の Regular Plaza の upkeepPerWeek)で、増やせる幅 4,000 の内。取り壊しは 0(wouldDemolish 0)。
- 減らした形: なし

### roads-1(道路下水道局): 基本道路5区間と2区間を Small 4 Lane Road に差し替える

- 査定: 可
- 理由: 建設費は 0(`test_upgrade_road` の試しで cost 0、paid true)。Basic Road と Small 4 Lane Road は、どちらも costPerKm 5,000、upkeepPerWeekPerKm 40(`list_net_types`)で、維持費の増えは 0。建設費と維持費の上限のどちらにも当たらない。
- 減らした形: なし

### port-1(港湾空港局): バスの予算を 150 から 130 に下げる

- 査定: 可
- 理由: 予算の変更は −20 で、予算の動かせる幅 ±20 の内。建設費は 0。週の維持費は減る(−2,950、`economy_breakdown` の Bus の支出 22,120 を 130/150 に割り引いた見積もり)。増えないため、維持費の上限に当たらない。
- 減らした形: なし

### health-1(保健環境局): 焼却場 2267 を一時停止する(試し)

- 査定: 可
- 理由: 建設なし、取り壊しなし(`set_building_active` で止めるのみ)。建設費は 0。週の維持費は減る(−1,440、`list_building_types` の Combustion Plant の upkeepPerWeek 1,440)。増えないため、維持費の上限に当たらない。
- 減らした形: なし

(urban、roads、port、health の順に並べた。economy、education、fire の局は「案なし」のため査定しない。)

## 合わせた費用と上限

- 「可」と「減額」の案を合わせた建設費: 2,500(urban-1 の 2,500 のみ。roads-1 と health-1 と port-1 は 0)
- 合わせた週の維持費の増え分: +32(urban-1 の 32 のみ)。減る分は −4,390(port-1 の −2,950 と health-1 の −1,440)。差し引きは −4,358
- 市長が選ぶときの建設費の上限: 1,050,000(所持金 2,100,591 の半分。型の上限のまま)
- 市長が選ぶときの週の維持費の上限: 4,000(増やせる幅。今の4案はどれも上限の内で、合わせても増えは 32)

## 税の案

なし。週の収支は +9,694 で黒字、所持金は 2,100,591 で守る線の内。税を動かす理由がないため、添えない。

## 見たもの

- `city_info`: 人口 179,748、所持金 2,100,591、週の収入 348,750、週の支出 339,056、週の収支 +9,694、観光客 1,722(訪問 146)、電気・水・下水が来ない市民 0 / 0 / 0、dialog なし
- `economy`: 税は住宅 低9・高7、商業 低9・高3、工業3、事務所3。bus の予算は昼夜とも 150。火事 140、教育 120、道路 100
- `list_building_types`(Beautification): Regular Plaza 建設費 2,500、維持費 32/週、needsRoad true、電気が要る
- `list_building_types`(Garbage): Combustion Plant 建設費 30,000、維持費 1,440/週
- `list_net_types`(Road、locked=false): Basic Road 5,000/km・40/週/km、Small 4 Lane Road 5,000/km・40/週/km
- `test_place_building`: Regular Plaza(2688, 880、facing west)は ok。cost 2,500、入口の道路 13565 から 9.7m、wouldDemolish 0、電気が要る
- `test_upgrade_road`: Small 4 Lane Road、点列 (3210,-318)→(3420,-318)。matched 3、upgraded 3、skipped 0、demolishedBuildings 0、cost 0、zonesKept true
- `economy_breakdown`: 週の収入 348,750、週の支出 339,056、政策の費用 10,719、Bus の支出 22,120、Garbage 支出 19,920、Road 8,526
- `list_loans`: 3つの枠(BankA、BankB、BankC)とも未借入。融資の週の返済 0

## 判断の根拠

4案の建設費は合わせて 2,500 で、上限 1,050,000 の中に収まる。維持費は増えるのが 32 だけで、減る分のほうが大きい。週の収支は +9,694 の黒字を保ち、所持金の減りは建設費の 2,500 だけになる。4案とも型の上限と要領の枠に収まるため、すべて「可」とした。

## 捨てたもの

- 経済観光文化局、教育委員会、消防局の案: 案なし(それぞれの調書に「案なし」と書かれている)。査定の対象にしていない。
- roads-1 の信号(3162,-255、3162,-300): 信号の建設費と維持費を道具で確かめられていない。この調書の対象外。
- port-1 の政策 FreeTransport と HeavyTrafficBan: 局が出していない案のため、査定の対象外。
- health-1 の焼却場の移し(relocate_building、建設費 6,000): 局が案として出していない。移し先も未確認。
- 税の案: 週の収支と所持金が守る線の中にあり、動かす理由がないため出さない。
