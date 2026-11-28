"""#186: 東京都中央卸売市場の明細データから、福岡と同じ12品目の月の数量と価格を作る(全国の出荷の目安)。
出力: data/tokyo12_monthly.csv(年,月,品目,数量kg,価格)。2010年以降。"""
import re
from pathlib import Path
import pandas as pd
from veg_parse import files
HERE=Path(__file__).parent
ITEMS=["じゃがいも","ばれいしょ",'キャベツ','はくさい','レタス','こまつな','トマト','きゅうり','なす','ブロッコリー','にんじん','ばれいしょ','たまねぎ','ねぎ']
parts=[]
for p in files():
    if int(re.match(r"y(\d{4})",p.name).group(1))<2009: continue
    for _,d in pd.read_excel(p,sheet_name=None,engine="calamine").items():
        d.columns=[str(c).strip() for c in d.columns]
        n=d["品目名称"].astype(str).str.replace(r"\s","",regex=True)
        d=d[n.isin(ITEMS)].assign(品目=n[n.isin(ITEMS)])
        parts.append(d[["年","月","品目","産地","数量(kg)","金額(円)"]])
    print(p.name,flush=True)
df=pd.concat(parts); df.groupby(["年","月","品目","産地"])[["数量(kg)","金額(円)"]].sum().reset_index().to_csv(HERE/"data/tokyo12_origin_monthly.csv",index=False)
g=df.groupby(["年","月","品目"])[["数量(kg)","金額(円)"]].sum().reset_index()
g["価格"]=g["金額(円)"]/g["数量(kg)"]; g.rename(columns={"数量(kg)":"数量kg"})[["年","月","品目","数量kg","価格"]].round(1).to_csv(HERE/"data/tokyo12_monthly.csv",index=False)
print(g.groupby("品目").size())
