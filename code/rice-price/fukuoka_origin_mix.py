"""#186: 福岡の2026年の日別データで、産地の割合が変わったことによる値動きを測る。
6月から7〜9月への値段の変化を、(a) 平均価格と (b) 6月の産地の割合で固定した価格で比べる。"""
import pandas as pd, glob, numpy as np
fs=sorted(glob.glob('data/raw_estat_daily/2026-*.csv'))
d=pd.concat([pd.read_csv(f,encoding='cp932',dtype=str) for f in fs])
for c in ['数量','価格','月']: d[c]=pd.to_numeric(d[c].str.replace(',',''),errors='coerce')
d=d.dropna(subset=['数量','価格']); d=d[d.数量>0]
d['品目名']=d['品目名'].str.strip(); d['産地名']=d['産地名'].fillna('').str.replace('　','')
items=['キャベツ','はくさい','レタス','こまつな','トマト','きゅうり','なす','ブロッコリー','にんじん','ばれいしょ','たまねぎ','ねぎ']
d=d[d.品目名.isin(items)]; d['金']=d.数量*d.価格
tot=d[d.産地名==''].groupby(['品目名','月']).agg(量=('数量','sum'),金=('金','sum')); tot['価']=tot.金/tot.量
og=d[d.産地名!=''].groupby(['品目名','月','産地名']).agg(量=('数量','sum'),金=('金','sum')); og['価']=og.金/og.量
rows=[]
for it in items:
    x=og.loc[it]
    for m in [7,8,9]:
        a=x.loc[6]; b=x.loc[m]; com=a.index.intersection(b.index)
        avg=(tot.loc[(it,m),'価']/tot.loc[(it,6),'価']-1)*100
        cover=b.loc[com,'量'].sum()/tot.loc[(it,m),'量']
        if len(com)==0: rows.append(dict(品目=it,月=m,平均価格の変化=round(avg,1))); continue
        w=a.loc[com,'量']; fixed=(np.exp((w*np.log(b.loc[com,'価']/a.loc[com,'価'])).sum()/w.sum())-1)*100
        rows.append(dict(品目=it,月=m,共通の産地=len(com),共通の産地の量の割合=round(cover,2),平均価格の変化=round(avg,1),産地固定の変化=round(fixed,1)))
r=pd.DataFrame(rows); r['差']=(r.平均価格の変化-r.産地固定の変化).round(1)
r.to_csv('forecast/fukuoka_origin_mix.csv',index=False); print(r.to_string(index=False))
ok=r[r.共通の産地の量の割合>=0.5]; print('6月と同じ産地が量の5割以上の組',len(ok),'/',len(r),' 差の絶対値の平均',round(ok.差.abs().mean(),1))
