"""#186: 福岡の予測の外れが、東京(全国の目安)の動きと共通かを見る。V2b(4〜6月の東京の入荷量)も試す。"""
import pandas as pd, numpy as np, statsmodels.api as sm
t=pd.read_csv('data/tokyo12_monthly.csv'); t['lv']=np.log(t.数量kg); t['lp']=np.log(t.価格)
def va(it,y,m,col):
    x=t[(t.品目==it)&(t.月==m)]; return x[x.年==y][col].iloc[0]-x[x.年<y][col].mean()
def surprise(it,y,m):  # 東京の「6月→当月」の値段の動きが、平年の動きとどれだけ違ったか
    x=t[t.品目==it].set_index(['年','月']).lp
    r=lambda yy: x[(yy,m)]-x[(yy,6)]
    return r(y)-np.mean([r(yy) for yy in range(2010,y)])
f=pd.read_csv('forecast/fukuoka_models.csv'); b=f[f['モデル']=='指数平滑法'].copy()
b=b[b.品目.isin(t.品目.unique())]; b['y']=np.log(b.実績/b.予測)
b['東京当月量']=[va(r.品目,r.年,r.月,'lv') for r in b.itertuples()]
b['東京値動き']=[surprise(r.品目,r.年,r.月) for r in b.itertuples()]
b['東京4-6月量']=[np.mean([va(r.品目,r.年,mm,'lv') for mm in [4,5,6]]) for r in b.itertuples()]
for c in ['東京当月量','東京値動き']:
    m=sm.OLS(b.y,sm.add_constant(b[c])).fit(); print('診断',c,'係数',round(m.params.iloc[1],3),'R2',round(m.rsquared,2))
print('品目ごと 東京値動きとの相関', b.groupby('品目').apply(lambda g: round(np.corrcoef(g.y,g.東京値動き)[0,1],2)).to_dict())
rng=np.random.default_rng(0); out=[]
for Y in range(2019,2027):
    tr=b.年<Y; te=b.年==Y; m=sm.OLS(b.y[tr],sm.add_constant(b['東京4-6月量'][tr])).fit()
    p=b.予測[te]*np.exp(m.predict(sm.add_constant(b['東京4-6月量'][te],has_constant='add')))
    out.append(pd.DataFrame({'年':Y,'元':(b.予測[te]/b.実績[te]-1).abs()*100,'直後':(p/b.実績[te]-1).abs()*100}))
o=pd.concat(out); d=(o.直後-o.元).values; bs=[rng.choice(d,len(d)).mean() for _ in range(2000)]
print('V2b 2019-26',round(o.元.mean(),2),'->',round(o.直後.mean(),2),np.percentile(bs,[2.5,97.5]).round(2))
