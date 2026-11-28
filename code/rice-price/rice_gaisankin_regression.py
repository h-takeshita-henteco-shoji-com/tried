"""#186 R3: 年産平均(税抜)を、新潟一般コシヒカリの概算金(当初額)で回帰する。"""
import pandas as pd, numpy as np, statsmodels.api as sm
m=pd.read_csv('data/monthly.csv',parse_dates=['month'])
m['ex']=m['all']/np.where(m.month<'2014-04-01',1.05,1.08)
m['cy']=m.month.dt.year.where(m.month.dt.month>=9,m.month.dt.year-1)
p=m.groupby('cy')['ex'].mean(); p.loc[2009]=14470/1.05
g=pd.read_csv('data/gaisankin.csv'); g=g[g.銘柄=='新潟一般コシヒカリ'].dropna(subset=['当初額']).set_index('年産').当初額
d=pd.DataFrame({'P':p,'G':g}).dropna(); d['lp']=np.log(d.P); d['lg']=np.log(d.G)
rows=[]
for t in range(2019,2027):
    tr=d[d.index<t]; mdl=sm.OLS(tr.lp,sm.add_constant(tr.lg)).fit()
    fr=mdl.get_prediction(np.array([[1,d.lg[t]]])).summary_frame(alpha=0.2)
    e=np.exp(fr[['mean','obs_ci_lower','obs_ci_upper']].iloc[0])
    rows.append(dict(年=t,学習点数=len(tr),概算金=int(d.G[t]),実績=round(d.P[t]),予測=round(e['mean']),幅80下=round(e.obs_ci_lower),幅80上=round(e.obs_ci_upper),傾き=round(mdl.params.iloc[1],2),誤差=round((e['mean']/d.P[t]-1)*100,1)))
r=pd.DataFrame(rows); r.to_csv('forecast/rice_gaisankin_regression.csv',index=False); print(r.to_string(index=False))
print('実績/概算金 の比', (d.P/d.G).round(3).to_dict())
