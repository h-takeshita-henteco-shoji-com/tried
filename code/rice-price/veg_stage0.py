"""#186 段0: 答えに近い材料で直したときの誤差(改善の上限)。予測の手法ではない。
出力: forecast/veg_stage0.csv"""
import pandas as pd, numpy as np, statsmodels.api as sm
STAT=['SARIMA','指数平滑法','Prophet(Meta)','TimesFM(Google)','Chronos(Amazon)']
f=pd.read_csv('forecast/fukuoka_models.csv')
b=f[f['モデル'].isin(STAT)].groupby(['年','月','品目'],as_index=False).agg(予測=('予測','mean'),実績=('実績','first'))
b=b[b.品目!='ばれいしょ'].dropna().reset_index(drop=True); b['y']=np.log(b.実績/b.予測)
# O1 東京の値動きの平年との違い(6月→当月)
t=pd.read_csv('data/tokyo12_monthly.csv'); t['lp']=np.log(t.価格); tx=t.set_index(['品目','年','月']).lp
def surprise(it,y,m):
    r=lambda yy: tx[(it,yy,m)]-tx[(it,yy,6)]
    return r(y)-np.mean([r(yy) for yy in range(2010,y)])
b['O1']=[surprise(r.品目,r.年,r.月) for r in b.itertuples()]
# O2 産地の割合の分
o2=pd.read_csv('forecast/tokyo_origin_mix.csv')[['品目','年','月','産地の割合の分_差']].rename(columns={'産地の割合の分_差':'O2'})
b=b.merge(o2,on=['品目','年','月'],how='left')
# O3 産地で重みをつけた同じ月の天候(地点×月で標準化)
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
o=pd.read_csv('data/tokyo12_origin_monthly.csv'); o=o[o['数量(kg)']>0]
o['st']=[station(i,p) for i,p in zip(o.品目,o.産地)]
cov=[]; O3={}
for (it,y,m),g in o[o.月.isin([7,8,9])].groupby(['品目','年','月']):
    h=g.dropna(subset=['st']); cov.append(h['数量(kg)'].sum()/g['数量(kg)'].sum())
    ww=h.groupby('st')['数量(kg)'].sum(); ww=ww/ww.sum()
    O3[(it,y,m)]=[sum(ww[s]*W.loc[(s,y,m),c] for s in ww.index) for c in ['降水量','気温','日照']]
print('O3 の地点で覆えた出荷量の割合: 中央値',round(np.median(cov),2),'最小',round(min(cov),2))
b[['O3雨','O3温','O3日']]=[O3.get((r.品目,r.年,r.月),[np.nan]*3) for r in b.itertuples()]
SETS={'O1':['O1'],'O2':['O2'],'O3':['O3雨','O3温','O3日'],'O1+O2+O3':['O1','O2','O3雨','O3温','O3日']}
rng=np.random.default_rng(0); out=[]
for Y in range(2019,2027):
    te=b[b.年==Y].copy(); te['元']=(te.予測/te.実績-1).abs()*100
    for k,cols in SETS.items():
        tr=b[(b.年<Y)].dropna(subset=cols); m=sm.OLS(tr.y,sm.add_constant(tr[cols])).fit()
        p=te.予測*np.exp(m.predict(sm.add_constant(te[cols],has_constant='add')))
        te['誤差_'+k]=(p/te.実績-1).abs()*100
    out.append(te)
o=pd.concat(out); o.round(3).to_csv('forecast/veg_stage0.csv',index=False)
print('11品目 2019〜2026 元',round(o.元.mean(),2),' 2026',round(o[o.年==2026].元.mean(),2))
for k in SETS:
    d=(o['誤差_'+k]-o.元).values; bs=[rng.choice(d,len(d)).mean() for _ in range(2000)]
    print(k,round(o['誤差_'+k].mean(),2),'差',round(d.mean(),2),np.percentile(bs,[2.5,97.5]).round(2),' 2026',round(o[o.年==2026]['誤差_'+k].mean(),2))
