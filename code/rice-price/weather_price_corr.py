"""天候と値段の相関(探索、事前登録なし)。値段・天候とも、季節と年の水準を除いた平年からのずれで比べる。出力: forecast/weather_price_corr.csv"""
import pandas as pd, numpy as np
ST={'キャベツ':'軽井沢','はくさい':'軽井沢','レタス':'軽井沢','こまつな':'福岡','なす':'福岡','トマト':'熊本','きゅうり':'佐賀',
    'ブロッコリー':'帯広','にんじん':'帯広','ばれいしょ':'帯広','たまねぎ':'網走','ねぎ':'大分'}
p=pd.read_csv('data/fukuoka_monthly.csv'); p=p[p.品目.isin(ST)&(p.年<=2025)].copy()
p['lp']=np.log(p.価格)
# 季節と年の水準を除く: 品目×月の平均、品目×年の平均を引く
p['a']=p.lp-p.groupby(['品目','月']).lp.transform('mean')
p['a']=p.a-p.groupby(['品目','年']).a.transform('mean')
w=pd.read_csv('data/weather_monthly.csv')
for c in ['降水量','気温','日照']:
    w[c+'_z']=(w[c]-w.groupby(['地点','月'])[c].transform('mean'))/w.groupby(['地点','月'])[c].transform('std')
w['t']=w.年*12+w.月
rows=[]
for it,st in ST.items():
    d=p[p.品目==it].copy(); d['t']=d.年*12+d.月
    ws=w[w.地点==st].set_index('t')
    for lag in [0,1,2]:
        for c in ['降水量','気温','日照']:
            x=ws[c+'_z'].reindex(d.t-lag).values
            m=~np.isnan(x)
            for sub,mask in [('全月',m),('7-9月',m&d.月.isin([7,8,9]).values)]:
                r=np.corrcoef(x[mask],d.a.values[mask])[0,1]
                rows.append((it,st,lag,c,sub,r,mask.sum()))
R=pd.DataFrame(rows,columns=['品目','地点','遅れ','天候','期間','r','n'])
R.to_csv('forecast/weather_price_corr.csv',index=False)
for sub in ['全月','7-9月']:
    print('==',sub)
    t=R[R.期間==sub].pivot_table(index='品目',columns=['天候','遅れ'],values='r').round(2)
    print(t.to_string())
    print('品目の中央値'); print(R[R.期間==sub].groupby(['天候','遅れ']).r.median().round(2).unstack())
print('n例', R.n.min(), R.n.max())
