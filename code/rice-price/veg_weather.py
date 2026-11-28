"""#186 V3/V3+: #184 の予測の外れを天候の差で直す(福岡12品目)。"""
import pandas as pd, numpy as np, statsmodels.api as sm
ST={'キャベツ':'軽井沢','はくさい':'軽井沢','レタス':'軽井沢','こまつな':'福岡','なす':'福岡','トマト':'熊本','きゅうり':'佐賀',
    'ブロッコリー':'帯広','にんじん':'帯広','ばれいしょ':'帯広','たまねぎ':'網走','ねぎ':'大分'}
w=pd.read_csv('data/weather_monthly.csv'); w['lp']=np.log(w['降水量']+1)
f=pd.read_csv('forecast/fukuoka_models.csv')
stat=['SARIMA','指数平滑法','Prophet(Meta)','TimesFM(Google)','Chronos(Amazon)']
base={'指数平滑法':f[f['モデル']=='指数平滑法'],
      '5モデル平均':f[f['モデル'].isin(stat)].groupby(['年','月','品目'],as_index=False).agg(予測=('予測','mean'),実績=('実績','first'))}
def anom(st,y,m,var):
    x=w[(w['地点']==st)&(w['月']==m)]
    clim=x[(x['年']<y)][var].mean(); return x[x['年']==y][var].iloc[0]-clim
VARS=[('気温','気温'),('日照','日照'),('降水','lp')]
def feats(item,y,m,kind):
    st=ST[item]; r={}
    months=[4,5,6] if kind=='V3' else [m-1,m]
    for k,v in VARS: r[k]=np.mean([anom(st,y,mm,v) for mm in months])
    return r
out=[]
for bname,b in base.items():
    b=b.copy(); b['y']=np.log(b['実績']/b['予測'])
    for kind in ['V3','V3+']:
        X=pd.DataFrame([feats(r.品目,r.年,r.月,kind) for r in b.itertuples()],index=b.index)
        X=(X-X.mean())/X.std()
        for Y in range(2019,2027):
            tr=b['年']<Y; te=b['年']==Y
            mdl=sm.OLS(b.y[tr],sm.add_constant(X[tr])).fit()
            pred=b['予測'][te]*np.exp(mdl.predict(sm.add_constant(X[te],has_constant='add')))
            for i in b.index[te]:
                out.append(dict(基準=bname,段=kind,年=Y,月=b.月[i],品目=b.品目[i],実績=b.実績[i],元の予測=b.予測[i],直した予測=pred[i]))
o=pd.DataFrame(out)
o['元の誤差']=(o.元の予測/o.実績-1).abs()*100; o['直した誤差']=(o.直した予測/o.実績-1).abs()*100
o.to_csv('forecast/veg_weather.csv',index=False)
g=o.groupby(['基準','段']).agg(元=('元の誤差','mean'),直後=('直した誤差','mean')).round(2); print('2019-2026'); print(g)
print('2026'); print(o[o.年==2026].groupby(['基準','段']).agg(元=('元の誤差','mean'),直後=('直した誤差','mean')).round(2))
# bootstrap diff over year-item clusters
rng=np.random.default_rng(0)
for (bn,k),g2 in o.groupby(['基準','段']):
    d=(g2.直した誤差-g2.元の誤差).values; bs=[rng.choice(d,len(d)).mean() for _ in range(2000)]
    print(bn,k,'差',round(d.mean(),2),'95%',np.percentile(bs,[2.5,97.5]).round(2))
# full-sample coefficients for interpretation (V3+, ETS)
b=base['指数平滑法'].copy(); b['y']=np.log(b['実績']/b['予測'])
X=pd.DataFrame([feats(r.品目,r.年,r.月,'V3+') for r in b.itertuples()],index=b.index); X=(X-X.mean())/X.std()
print(sm.OLS(b.y,sm.add_constant(X)).fit().summary().tables[1])
