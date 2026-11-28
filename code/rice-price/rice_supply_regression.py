"""#186 R2: R1 の在庫率を供給率((6月末在庫 + その年産の生産量) ÷ 需要)に替える。R2a は生産量を面積×過去5年の単収で見込む。R2b は実績。"""
import pandas as pd, numpy as np, statsmodels.api as sm
m=pd.read_csv('data/monthly.csv',parse_dates=['month'])
m['ex']=m['all']/np.where(m.month<'2014-04-01',1.05,1.08)
m['cy']=m.month.dt.year.where(m.month.dt.month>=9,m.month.dt.year-1)
p=m.groupby('cy')['ex'].mean(); p.loc[2009]=14470/1.05; p=p.sort_index()
s=pd.read_csv('data/supply_annual.csv').set_index('年'); q=pd.read_csv('data/production_annual.csv').set_index('年産')
d=pd.DataFrame({'P':p,'S':s.iloc[:,0],'D':s.iloc[:,1],'Q':q.iloc[:,0],'A':q['主食用作付面積_万ha']})
d['yld']=d.Q/d.A
d['Qhat']=[d.A[t]*d.yld.loc[t-5:t-1].mean() if t-5>=d.index.min() else np.nan for t in d.index]
d['dlp']=np.log(d.P).diff()
for k,Qc in (('a','Qhat'),('b','Q')):
    d['dlr'+k]=np.log((d.S+d[Qc])/d.D).diff()
def fit(t,k,start=2010,end=None):
    x='dlr'+k; tr=d.loc[start:(end or t-1)].dropna(subset=['dlp',x])
    B=sm.OLS(tr.dlp,sm.add_constant(tr[x])).fit()
    pr=B.get_prediction(np.array([[1,d[x][t]]])).summary_frame(alpha=0.2)
    f=lambda v: d.P[t-1]*np.exp(v)
    return f(pr['mean'].iloc[0]),f(pr['obs_ci_lower'].iloc[0]),f(pr['obs_ci_upper'].iloc[0]),B.params.iloc[1],len(tr)
rows=[]
for k,lab in (('a','R2a 見込み'),('b','R2b 実績')):
    for t in range(2016,2027):
        for name,kw in [('全期間',{}),('2023年まで',{'end':min(t-1,2023)}),('2018年から',{'start':2018})]:
            if name=='2018年から' and t<2022: continue
            pt,lo,hi,b,n=fit(t,k,**kw)
            if n<5: continue
            rows.append(dict(段=lab,年=t,学習=name,学習の年数=n,実績=round(d.P[t]),予測=round(pt),幅80下=round(lo),幅80上=round(hi),傾き=round(b,2),誤差=round((pt/d.P[t]-1)*100,1)))
r=pd.DataFrame(rows); r.to_csv('forecast/rice_supply_regression.csv',index=False)
r1=pd.read_csv('forecast/rice_stock_regression.csv'); r1['段']='R1 在庫率'
a=pd.concat([r1,r])
for lab,g in a[a.学習=='全期間'].groupby('段'):
    print(lab,'2016-23 平均|誤差|',round(g[g.年<=2023].誤差.abs().mean(),1),'(',g[g.年<=2023].年.min(),'から) 2019-23',round(g[(g.年>=2019)&(g.年<=2023)].誤差.abs().mean(),1),' 2024',g[g.年==2024].誤差.iloc[0],' 2025',g[g.年==2025].誤差.iloc[0],
          ' 2026',g[g.年==2026].誤差.iloc[0],'予測',g[g.年==2026].予測.iloc[0],'幅',g[g.年==2026].幅80下.iloc[0],'-',g[g.年==2026].幅80上.iloc[0])
print(a[a.年==2026][['段','学習','予測','誤差','傾き']].to_string(index=False))
print(d[['S','Q','Qhat','D']].loc[2022:].round(1))
