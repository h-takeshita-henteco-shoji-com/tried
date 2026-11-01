# #132 の図面の入手先

`drawing-list.md` の図面を、再配布できる外部の図面で用意できるか調べた。
リポジトリと記事が公開のため、再配布と改変ができるライセンスに限った。
調査は2026-10-30時点。ライセンスは「確認」と「推測」を分けて書く。

## 結論

#132 の図面は、すべて国交省「建築工事標準詳細図（令和4年改定）」から選ぶ（2026-10-31決定）。

| 難易度 | 図面 | DXFの用意 | ライセンス |
|---|---|---|---|
| 低 | 4-01 建具：形状寸法 | ベクターPDFを変換 | PDL1.0（確認） |
| 中 | 4-21 建具取合い：標準型鋼製建具 | ベクターPDFを変換 | PDL1.0（確認） |
| 高 | 9-32 門：引き戸 | ベクターPDFを変換 | PDL1.0（確認） |

- 日本の図面で、公開でき、文字を文字データのまま DXF にできるため。
- PDF からの変換は `code/drawings/pdf_to_dxf.py` で行う。画像は経由しない。
- PDL1.0 は公共データ利用規約（第1.0版）。CC BY 4.0 と互換の政府の規約。出典と、加工したことを書く。
- 民間の DXF 変換版（CAD素材.com）は、規約で公開と AI の用途を禁じているため使わない。

以下は、それまでに調べた候補の記録。
いったん採用した VA の建具図、Big Floor Plans、Schependomlaan は、この決定で使わないことにし、ファイルを消した。
後続の子Issueで使う場合は、ここの入手先から取り直す。

## 建築の候補

### BL 建具図

- **VA 標準詳細図 Division 08（扉と窓）**
  - URL: https://www.cfm.va.gov/til/sDetail/sDetail-Div08-DWG.zip （PDF: https://www.cfm.va.gov/til/sDetail/sDetail-Div08-PDF.pdf ）
  - 中身: 壁の種類ごとの扉枠の断面、鉛入りの扉、観察窓。寸法はインチとmmの併記。
  - ライセンス: 米国連邦政府の著作物でパブリックドメイン（推測）。VAの方針に「government-produced materials ... are not copyright protected」とある。
  - 懸念: 英語。立面より断面が中心。外注で作った図の権利は確認しきれていない。
- **国交省「建築工事標準詳細図」（令和4年改定）第4章 建具**
  - URL: https://www.mlit.go.jp/gobuild/gobuild_tk2_000017.html
  - 中身: 木製・鋼製の建具の納まり、くつずり、シャッター。JIS準拠の注記。
  - ライセンス: 利用ルール（https://www.mlit.go.jp/link.html ）でPDL1.0（確認）。出典の記載と、加工したことの明記が条件。
  - 懸念: 建具ごとの建具表ではなく、納まりの詳細図。民間のDXF変換版（CAD素材.com）は再配布できない。

### BM 戸建て平面図

- **Big Floor Plans の教材用プラン**
  - URL: https://www.bigfloorplans.com/sample-plans
  - 中身: Teaching House（18室）、Tiny House、Café、Trades Bay。ドア・窓・設備の記号がある。
  - 形式: PDF（DXFを添付）と、部屋データ・SVG・DXFを入れたZIP。
  - ライセンス: CC BY 4.0（確認。ページの記載で確かめた）。
  - 懸念: 米国の表記。日本の間取りではない。
- **KIT「FZK-Haus」**（予備）
  - URL: https://www.ifcwiki.org/index.php?title=KIT_IFC_Examples
  - 形式: IFC。2Dの図面は自分で書き出す。
  - ライセンス: 「for unrestricted use」（確認）。出典の記載が要る。

### BH 施工図

- **Schependomlaan**
  - URL: https://github.com/openBIMstandards/Archive-DataSetSchependomlaan
  - 中身: 協力会社が作った図。設備のDWGが18本（給水・ガス・暖房、排水・換気・雨水、スリーブ・開口）。階ごとに分かれる。
  - 中身を確かめた結果: 通り芯、配管、放熱器、温度の表示、系統の凡例がある。壁と部屋はない。系統は線の色で分かれる。
  - 採用したファイル: 1階の暖房・給水・ガス（SONSBEEK-BG Water+Gas+CV.dwg）。
  - ライセンス: LICENSE.MD に「(C) original owners.」と CC BY 4.0（確認）。表示どおり CC BY 4.0 として扱う（2026-10-30決定）。
    - 旧READMEには、持ち主が学術目的の利用を許可したとある。持ち主が CC BY 4.0 に同意したかは書かれていない。
    - LICENSE.MD は2016年から変わらない。buildingSMART のサンプル集（CC BY 4.0）でも配られていた。
    - 使うときは、出典（Schependomlaan、TU Eindhoven、元の持ち主）とライセンスを明記する。DXFへの変換や加工も書く。
  - 懸念: オランダ語。躯体図や鉄骨図そのものではない。断面詳細のDWGはない。
- **米陸軍工兵隊の標準設計図 421-80-10**（予備）
  - 通り芯付きの基礎伏図がある。PDFのみ。パブリックドメイン（推測）。設計図で施工図ではない。

### BH の代わり 矩計図

- **国交省「木造ディテール参考図」令和8年版（2026年7月）**
  - URL: https://www.mlit.go.jp/gobuild/content/002011260.pdf
  - 中身: 木造軸組の部分詳細（1/10）。屋根・軒裏、外壁と基礎の取合い、建具、床・天井。JIS番号付きの注記。
  - ライセンス: PDL1.0（確認）。
  - 懸念: 基礎から屋根まで通した1枚ではない。文字が線になっていて、DXFで文字として残らない。
- **OpeningDesign「The Downtowner」（米国の木造2階建て改修）**
  - URL: https://github.com/OpeningDesign/Vacation_Rental （A350・A351 WALL SECTIONS、A400〜A402）
  - 中身: 基礎から屋根まで切った断面が7本。各階のレベル、通り芯、詳細への参照記号。
  - ライセンス: CC BY-SA 4.0（確認。READMEと図枠の両方に記載）。
  - 懸念: 図枠に実在の住所、施主名、署名がある。改変した図面も CC BY-SA で出す。
- **OpeningDesign「Xcel Sports Complex」**（予備）
  - URL: https://github.com/OpeningDesign/Sports_Complex
  - 鉄骨造の壁断面が6本。CC BY-SA 4.0（README）。図枠に他社のロゴがある。

### BH の代わり 設備図

- **国交省「営繕BIMモデル」の実施設計図書（別紙3）**
  - URL: https://www.mlit.go.jp/gobuild/gobuild_tk6_000132.html
  - 中身: 架空の官庁施設（RC造5階、延べ約3300㎡）。受変電・幹線、空調配管、換気、給排水衛生の平面図（28〜39ページ）。
  - 形式: ベクターPDF（文字データあり）と Revit。Archicad版もある。
  - ライセンス: PDL1.0（確認）。
  - 懸念: 詳細図と自動制御図はない。一部の部品は第三者の標準を参照している。
- **国交省「公共建築設備工事標準図」令和7年版**（凡例として併用）
  - 機械: https://www.mlit.go.jp/gobuild/content/001888832.pdf
  - 電気: https://www.mlit.go.jp/gobuild/content/001879276.pdf
  - 設備記号の凡例と施工要領。建物の図ではない。PDL1.0（推測を含む）。
- **The Downtowner の空調・給排水図**
  - 矩計図と同じ建物。CC BY-SA 4.0（README）。設備図は外部の会社が描いており、ライセンスが及ぶかは推測。
- **buildingSMART の Duplex・Clinic**
  - URL: https://github.com/buildingsmart-community/Community-Sample-Test-Files
  - IFC。READMEは CC BY 4.0。原本は改変禁止だったという情報と食い違う。2Dの記号や注記は付かない。
- **VA 標準詳細図 Division 21〜28**
  - DWG。パブリックドメイン（確認）。詳細図で、建物の平面図ではない。

## 機械の候補

### ML 部品図

- **Tes の tech.drawings**
  - URL: https://www.tes.com/en-us/teaching-resource/tech-drawings-dxf-files-and-freecad-fcstd-12489941
  - DXF、FreeCAD、JPG。「Creative Commons 'Attribution'」と表示。版は不明。
- **QCAD 付属の例（example01、flange、bracket）**
  - URL: https://github.com/qcad/qcad/tree/master/examples
  - DXF。公差、はめあい、面取り、幾何公差、断面、表題欄がある。
  - ライセンス: 例のファイルに記載がない。リポジトリはGPLv3（推測）。
- **Precious Plastic 破砕機の部品図**
  - URL: https://github.com/ONEARMY/precious-plastic-kit
  - PDF。DXFは外形だけ。CC BY-SA 4.0（確認）。
- **LifeTrac v25 の部品図（Open Source Ecology）**
  - URL: https://github.com/OpenSourceEcology/LifeTrac
  - PDF。表題欄に材質・加工・仕上げ。DXFは外形だけ。リポジトリにライセンスの記載がない（OSEのwikiはCC BY-SA）。

### MM 構想図

- **Precious Plastic 破砕機・射出機の全体図**: PDF。部品表付き。CC BY-SA 4.0（確認）。
- **OSE CEB Press の製作図面**: PDF 61ページ。部品番号と部品表。CC BY-SA 4.0（確認）。
- **国会図書館『国産機械図集 工作機械』（1941年）**: 画像。パブリックドメイン（確認）。

### MH 工程図

- **国会図書館『旋盤教程』（1944年）**
  - URL: https://dl.ndl.go.jp/pid/1059168 （44コマ目付近）
  - 丸棒の段付けを4工程に分け、途中の形と寸法、取付け、工具、材質を示す。日本語。
  - パブリックドメイン（確認）。画像のみで、旧字体。
- DXFの工程図は見つからない。部品図をもとに自作する。

## DXFへの変換

| 元の形式 | 方法 |
|---|---|
| ベクターPDF | Inkscape か pstoedit |
| DWG | ODA File Converter か LibreDWG |
| Revit | Revit（Windowsのみ）でDWGに書き出し、DXFへ |
| IFC | IfcOpenShell、Bonsai、FreeCAD |
| JWW | ezjww（Mac で使えるPythonライブラリ） |

## 使えない入手先

規約で再配布や改変物の公開を禁じているか、許可が要る。

| 入手先 | 中身 | 理由 |
|---|---|---|
| PSYCROSS（http://psycross.com/Selfbuild/download.html ） | 2×4住宅の図面一式（DXF・JWW、日本語） | 管理者の同意なく第三者に譲渡しないよう求めている |
| CAD素材.com | 国交省の標準詳細図のDXF変換版 | 再配布、改変物の公開、AIの学習を禁止 |
| Draftsperson.net | CADブロック | 再ホスティングを禁止 |
| CAD-DATA.com、Jw_cad超初心者道場 | JWWの建具・部品 | 二次配布を禁止 |
| jwcad.setsubit.com | 設備の標準図・施工図（JWW） | 業務以外の利用には許可が要る |
| BLCJ「BIM図面審査支援ツール」 | 設備のRevitモデル付きのサンプル | 無断の再配布を禁止 |
| TraceParts、GrabCAD | 部品のCADデータ | 掲載や配布に許可が要る、または内部利用に限る |
| 職業能力開発総合大学校（JEED）の訓練課題 | XYステージ（DWG、JIS） | 無断の複製・頒布・改変を禁止 |
| 市販のCAD教本の付録 | 練習用の図面 | 購入者の学習用に限る |
| Autodesk の Revit サンプル | Snowdon Towers など | 再配布を許す記載がない（推測） |

市販の教本は、エクスナレッジ、日経BP、技術評論社、ソーテック社、日刊工業新聞社、インプレスの規約を確かめた。
記事で図の一部を引用する余地はある。図面ファイルをリポジトリに置くのは引用にならない。

## 未確認のもの

- Jw_cad 付属の「木造平面例」。無償の再配布の可否が規約にない。使うなら作者に確かめる。
- 国内メーカーや便覧サイトの無料DXF、大学の製図講義のPDF、FreeCAD の例。
