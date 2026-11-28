"""#186: 東京の明細データで、6月→7〜9月の値動きの「平年との違い」のうち、産地の割合の違いで説明できる分を測る。"""
import pandas as pd, numpy as np
o=pd.read_csv('data/tokyo12_origin_monthly.csv'); o=o[o['数量(kg)']>0]; o['価']=o['金額(円)']/o['数量(kg)']
def parts(it,y,m):
    a=o[(o.品目==it)&(o.年==y)&(o.月==6)].set_index('産地'); b=o[(o.品目==it)&(o.年==y)&(o.月==m)].set_index('産地')
    avg=np.log((b['金額(円)'].sum()/b['数量(kg)'].sum())/(a['金額(円)'].sum()/a['数量(kg)'].sum()))
    com=a.index.intersection(b.index); w=a.loc[com,'数量(kg)']
    fixed=(w*np.log(b.loc[com,'価']/a.loc[com,'価'])).sum()/w.sum()
    return avg,avg-fixed
rows=[]
for it in o.品目.unique():
    for y in range(2010,2027):
        for m in [7,8,9]:
            a,c=parts(it,y,m); rows.append(dict(品目=it,年=y,月=m,値動き=a,産地の割合の分=c))
r=pd.DataFrame(rows)
for col in ['値動き','産地の割合の分']:
    r[col+'_差']=r.groupby(['品目','月'])[col].transform(lambda s: s-s.expanding().mean().shift())
t=r[r.年>=2016].dropna()
cov=np.cov(t['値動き_差'],t['産地の割合の分_差'])[0,1]/t['値動き_差'].var()
print('2016-2026 東京11品目: 平年と違う値動きのうち、産地の割合の違いで説明できる割合(共分散の比)',round(cov,2),' 相関',round(t[['値動き_差','産地の割合の分_差']].corr().iloc[0,1],2))
print(t.groupby('品目').apply(lambda g: round(np.cov(g['値動き_差'],g['産地の割合の分_差'])[0,1]/g['値動き_差'].var(),2)).to_dict())
print('2026', round(np.cov(t[t.年==2026]['値動き_差'],t[t.年==2026]['産地の割合の分_差'])[0,1]/t[t.年==2026]['値動き_差'].var(),2))
r.to_csv('forecast/tokyo_origin_mix.csv',index=False)
