"""#186 V2: #184 の予測の外れを入荷量の差で直す(福岡12品目)。診断として当月の入荷量も見る。"""
import pandas as pd, numpy as np, statsmodels.api as sm
a=pd.read_csv('data/fukuoka_monthly.csv'); b2=pd.read_csv('data/fukuoka_daily_monthly.csv')
b2['品目']=b2['品目'].str.strip(); a['品目']=a['品目'].str.strip()
v=pd.concat([a[a.年<2026][['年','月','品目','数量t']],b2[['年','月','品目','数量t']]])
v['lv']=np.log(v['数量t'])
def anom(item,y,m):
    x=v[(v.品目==item)&(v.月==m)]; return x[x.年==y].lv.iloc[0]-x[x.年<y].lv.mean()
f=pd.read_csv('forecast/fukuoka_models.csv')
stat=['SARIMA','指数平滑法','Prophet(Meta)','TimesFM(Google)','Chronos(Amazon)']
base={'指数平滑法':f[f['モデル']=='指数平滑法'].copy(),
      '5モデル平均':f[f['モデル'].isin(stat)].groupby(['年','月','品目'],as_index=False).agg(予測=('予測','mean'),実績=('実績','first'))}
rng=np.random.default_rng(0)
for bn,b in base.items():
    b['y']=np.log(b['実績']/b['予測'])
    b['V2']=[np.mean([anom(r.品目,r.年,mm) for mm in [4,5,6]]) for r in b.itertuples()]
    b['当月']=[anom(r.品目,r.年,r.月) for r in b.itertuples()]
    out=[]
    for Y in range(2019,2027):
        tr=b.年<Y; te=b.年==Y
        m=sm.OLS(b.y[tr],sm.add_constant(b.V2[tr])).fit()
        p=b.予測[te]*np.exp(m.predict(sm.add_constant(b.V2[te],has_constant='add')))
        out.append(pd.DataFrame({'年':Y,'元':(b.予測[te]/b.実績[te]-1).abs()*100,'直後':(p/b.実績[te]-1).abs()*100}))
    o=pd.concat(out); d=(o.直後-o.元).values; bs=[rng.choice(d,len(d)).mean() for _ in range(2000)]
    print(bn,'V2 2019-26',round(o.元.mean(),2),'->',round(o.直後.mean(),2),'差95%',np.percentile(bs,[2.5,97.5]).round(2),' 2026',round(o[o.年==2026].元.mean(),2),'->',round(o[o.年==2026].直後.mean(),2))
    dm=sm.OLS(b.y,sm.add_constant(b.当月)).fit(); print('  診断 当月の入荷量: 係数',round(dm.params.iloc[1],3),'R2',round(dm.rsquared,2))
    pi=b.groupby('品目').apply(lambda g: sm.OLS(g.y,sm.add_constant(g.当月)).fit().rsquared).round(2); print('  品目ごとR2',dict(pi))
