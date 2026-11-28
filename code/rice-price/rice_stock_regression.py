"""#186 R1: 年産平均(税抜)の前年比を、6月末在庫率(在庫/需要)の前年差で回帰する。"""
import pandas as pd, numpy as np, statsmodels.api as sm
m=pd.read_csv('data/monthly.csv',parse_dates=['month'])
m['ex']=m['all']/np.where(m.month<'2014-04-01',1.05,1.08)
m['cy']=m.month.dt.year.where(m.month.dt.month>=9,m.month.dt.year-1)
p=m.groupby('cy')['ex'].mean(); p.loc[2009]=14470/1.05; p=p.sort_index()
s=pd.read_csv('data/supply_annual.csv').set_index('年')
d=pd.DataFrame({'P':p,'S':s.iloc[:,0],'D':s.iloc[:,1]})
d['lr']=np.log(d.S/d.D); d['dlp']=np.log(d.P).diff(); d['dlr']=d.lr.diff()
def fit(t,start=2010,end=None):
    tr=d.loc[start:(end or t-1)].dropna(subset=['dlp','dlr'])
    B=sm.OLS(tr.dlp,sm.add_constant(tr.dlr)).fit()
    x=np.array([[1,d.dlr[t]]]); pr=B.get_prediction(x).summary_frame(alpha=0.2)
    f=lambda v: d.P[t-1]*np.exp(v)
    return f(pr['mean'].iloc[0]),f(pr['obs_ci_lower'].iloc[0]),f(pr['obs_ci_upper'].iloc[0]),B.params.iloc[1]
rows=[]
for t in range(2016,2027):
    for name,kw in [('全期間',{}),('2023年まで',{'end':min(t-1,2023)}),('2018年から',{'start':2018})]:
        if name=='2018年から' and t<2022: continue
        pt,lo,hi,b=fit(t,**kw)
        rows.append(dict(年=t,学習=name,実績=round(d.P[t]),予測=round(pt),幅80下=round(lo),幅80上=round(hi),傾き=round(b,2),誤差=round((pt/d.P[t]-1)*100,1)))
r=pd.DataFrame(rows); r.to_csv('forecast/rice_stock_regression.csv',index=False)
print(r.to_string(index=False))
