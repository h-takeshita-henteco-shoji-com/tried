"""#186 段1: 6月末に分かる材料で、5モデル平均の7〜9月の予測を直す。
1a 6月の福岡と東京の値段の差(平年との違い)、1b 6月に東京へ入った夏の産地の量(平年との違い)、1c 夏の産地で重みをつけた6月の天候(7月だけ直す)
出力: forecast/veg_stage1.csv"""
import pandas as pd, numpy as np, statsmodels.api as sm
STAT=['SARIMA','指数平滑法','Prophet(Meta)','TimesFM(Google)','Chronos(Amazon)']
f=pd.read_csv('forecast/fukuoka_models.csv')
b=f[f['モデル'].isin(STAT)].groupby(['年','月','品目'],as_index=False).agg(予測=('予測','mean'),実績=('実績','first'))
b=b[b.品目!='ばれいしょ'].dropna().reset_index(drop=True); b['y']=np.log(b.実績/b.予測)
# 1a
fk=pd.concat([pd.read_csv('data/fukuoka_monthly.csv'),pd.read_csv('data/fukuoka_daily_monthly.csv')]).drop_duplicates(['年','月','品目'],keep='last')
fk=fk[fk.月==6].set_index(['品目','年']).価格
t=pd.read_csv('data/tokyo12_monthly.csv'); tk=t[t.月==6].set_index(['品目','年']).価格
gap=np.log(fk/tk).dropna()
def g1a(it,y): return gap[(it,y)]-gap[it][gap[it].index<y].mean()
# 1b 夏の産地 = その年より前の7〜9月で東京への量が多い順に、累計8割までの県
o=pd.read_csv('data/tokyo12_origin_monthly.csv'); o=o[o['数量(kg)']>0]
def summer(it,y):
    s=o[(o.品目==it)&(o.月.isin([7,8,9]))&(o.年<y)].groupby('産地')['数量(kg)'].sum().sort_values(ascending=False)
    c=(s/s.sum()).cumsum(); return list(c[c.shift(fill_value=0)<0.8].index), s/s.sum()
jun=o[o.月==6].groupby(['品目','年','産地'])['数量(kg)'].sum()
def vol(it,y,pr): return sum(jun.get((it,y,p),0) for p in pr)
def g1b(it,y):
    pr,_=summer(it,y); past=[vol(it,yy,pr) for yy in range(max(2010,y-5),y)]
    return np.log((vol(it,y,pr)+1)/(np.mean(past)+1))
# 1c
w=pd.concat([pd.read_csv('data/weather_monthly.csv'),pd.read_csv('data/weather_monthly_more.csv')])
for c in ['降水量','気温','日照']:
    g=w.groupby(['地点','月'])[c]; w[c]=(w[c]-g.transform('mean'))/g.transform('std')
W=w.set_index(['地点','年','月'])
HIGH={'キャベツ','レタス','はくさい'}
def station(it,pref):
    if pref=='長野': return '軽井沢' if it in HIGH else '長野'
    if pref=='群馬': return '軽井沢' if it in HIGH else '前橋'
    if pref=='北海道': return '網走' if it=='たまねぎ' else '帯広'
    return {'岩手':'盛岡','福島':'福島','茨城':'水戸','栃木':'宇都宮','青森':'青森','秋田':'秋田','山形':'山形','兵庫':'洲本',
            '佐賀':'佐賀','熊本':'熊本','福岡':'福岡','大分':'大分'}.get(pref)
def g1c(it,y):
    _,sh=summer(it,y); ws={}
    for p,v in sh.items():
        s=station(it,p)
        if s: ws[s]=ws.get(s,0)+v
    tot=sum(ws.values())
    return [sum(v/tot*W.loc[(s,y,6),c] for s,v in ws.items()) for c in ['降水量','日照']]
key=b[['品目','年']].drop_duplicates()
F={}
for r in key.itertuples():
    F[(r.品目,r.年)]=[g1a(r.品目,r.年),g1b(r.品目,r.年)]+g1c(r.品目,r.年)
b[['1a','1b','1c雨','1c日']]=[F[(r.品目,r.年)] for r in b.itertuples()]
SETS={'1a':(['1a'],[7,8,9]),'1b':(['1b'],[7,8,9]),'1c':(['1c雨','1c日'],[7])}
rng=np.random.default_rng(0); out=[]; coef={k:[] for k in SETS}
for Y in range(2019,2027):
    te=b[b.年==Y].copy(); te['元']=(te.予測/te.実績-1).abs()*100
    for k,(cols,ms) in SETS.items():
        tr=b[(b.年<Y)&b.月.isin(ms)]; m=sm.OLS(tr.y,sm.add_constant(tr[cols])).fit(); coef[k].append(m.params.iloc[1:].round(3).tolist())
        adj=np.where(te.月.isin(ms),m.predict(sm.add_constant(te[cols],has_constant='add')),0)
        te[k]=(te.予測*np.exp(adj)/te.実績-1).abs()*100
    out.append(te)
o=pd.concat(out); o.round(3).to_csv('forecast/veg_stage1.csv',index=False)
print('11品目 2019〜2026 元',round(o.元.mean(),2),' 2026',round(o[o.年==2026].元.mean(),2))
for k in SETS:
    d=(o[k]-o.元).values; bs=[rng.choice(d,len(d)).mean() for _ in range(2000)]
    print(k,round(o[k].mean(),2),'差',round(d.mean(),2),np.percentile(bs,[2.5,97.5]).round(2),' 2026',round(o[o.年==2026][k].mean(),2),' 係数(2019,2026)',coef[k][0],coef[k][-1])
# 全期間(2016〜2025)の相関の診断
d=b[b.年<=2025]
for c in ['1a','1b']: print('相関 y と',c, round(np.corrcoef(d.y,d[c])[0,1],2))
d7=d[d.月==7]
for c in ['1c雨','1c日']: print('相関 7月の y と',c, round(np.corrcoef(d7.y,d7[c])[0,1],2))
