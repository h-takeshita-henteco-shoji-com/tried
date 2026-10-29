# m15 経済観光文化局の案

## 案なし

今月は案を出しません。検討した候補と、案なしにした根拠は次のとおりです。

- 名所(Monument)の型: Friendly Neighborhood、SeaWorld、StatueOfWealth は、3型とも建設済みで置けない(test_place_building が AlreadyExists)。未建設の型(Transport Tower、Colossal Offices、Library など)を候補にした。
- 島B(-4620,1608、南向き)の Transport Tower: 道路に面し、置けることは確かめた(ok、費用 60,000、入口は segment 13902 の 0.6m)。ただし、需要として水と下水が要る。最寄りの水の管網は島から700m以上離れ、本土の網までは数km。管の経路は未確認で、建設費と維持費(管の延長に比例)も試していない。必須条件が未確認なので、実行対象に含めない。
- 本土の候補: 2500,500 付近の空きは、事務所と住宅の建物が多く、Transport Tower(8x12)の敷地が取れなかった(test_place_building の Transport Tower (2715,470) は建物と道路に重なり、ObjectCollision)。
- 事務所の道(働き口): (-1500,-500)〜(-500,-500) の test_build_line は、水塔、高層住宅、埋立地と重なり断られた。zone_summary の空きは、この帯では使えない。
- 政策: list_policies で一覧を確認した。観光に効く政策(RecreationalUse、SmallBusiness)の効きは、過去の試しでも確認できていない。今月は新しい政策の案を出す根拠がない。

週の収支は +4,256 で、守る線 +3,000 まで余裕 1,256。名所1棟(週960)は入るが、島の管を足すと割る見込みのため、島の案は未確認のまま見送る。

## 調査

- 調査: なし

## 見たもの

- `list_policies`: 政策一覧。有効は SmokingBan、EducationBoost(7,940)、BigBusiness(3,832)。RecreationalUse、SmallBusiness(313)は無効。政策費用の合計 10,598
- `zones_at`: (2500,500) r150。事務所 258(空き3)、住宅(高) 26(空き0)、未指定 60、商業(高) 17(空き4)
- `list_net_types`: Water Pipe、建設 2,500/km、維持 10/週/km
- `net_near`: (-4300,1600) r700、Water の管 0 本
- `water_trace`: (-4620,1608) の島B。水と下水は届かず、管網なし。本土の網(2445 区間、取水塔多数、排水の処理場あり)
- `water_trace`: (2692,463) 本土の商店。水と下水は届く
- `test_place_building`: Transport Tower (2715,470) 西向き、ObjectCollision(道路 6704、33471、商店3棟)
- `test_place_building`: Transport Tower (-4620,1608) 南向き、ok、費用 60,000、needs 電気・水・下水、入口 segment 13902(0.6m)
- `test_build_line`: Basic Road (-1500,-500)〜(-500,-500)、建物の重なりで断り(水塔 26691、30116、高層住宅 8353、21746、13598、16024、事務所 31488、埋立地 46633)

## 判断の根拠

- 名所の型は、未建設のもので試す必要がある。3型の AlreadyExists は、計画の前提(3型を建てる)を外した。計画は直した。
- 島Bの候補は、水と下水の接続が確かめられない。必須条件が残るので、実行対象にしない。
- 本土の候補と事務所の道は、今回の確認で通らなかった。16月に、重ならない場所を探し直す。
- 週の収支の余裕 1,256 は、名所1棟で使い切りに近い。島の管を足すと守る線を割るため、案は見送る。

## 捨てたもの

- Transport Tower 島B(-4620,1608): 入口と置く場所は確かめた。水と下水の管が未確認(最寄りの網まで数km)。試しは作れるが、接続の手がないため実行可否は未確認。今月は出さない。
- 事務所の道 (-1500,-500)〜(-500,-500): 建物と重なり、通らない。
- Colossal Offices、Library: 費用 70,000〜90,000、週 1,200〜1,360。Library は守る線を割る。Colossal Offices は余裕を約 56 にする。敷地が未確認のため、今月は出さない。
- 政策 RecreationalUse、SmallBusiness: 観光への効きが確かめられていない。今月は採らない。
