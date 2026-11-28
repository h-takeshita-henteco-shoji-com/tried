"""#186 段3: 問題の決め方を変える。5モデル平均、12品目、2019〜2026年の7〜9月。
3a 毎月の見直し: 6月末の3か月先の予測と、各月末の1か月先の予測(見通しで直した版も)を比べる
3b 予測の幅: その年より前の外れ log(実績÷予測) の10%・90%点で80%の幅を作り、実績が入る割合と幅を見る。12品目まとめた幅と、品目ごとの幅
出力: forecast/veg_stage3.csv"""
import pandas as pd, numpy as np, glob
STAT=['SARIMA','指数平滑法','Prophet(Meta)','TimesFM(Google)','Chronos(Amazon)']
f=pd.read_csv('forecast/fukuoka_models.csv')
h3=f[f['モデル'].isin(STAT)].groupby(['年','月','品目'],as_index=False).agg(予測=('予測','mean'),実績=('実績','first')).dropna()
h1=pd.concat([pd.read_csv(p) for p in glob.glob('forecast/h1/*.csv')])
h1=h1[h1['モデル'].isin(STAT)].groupby(['年','月','品目'],as_index=False).agg(予測1=('予測','mean'),実績1=('実績','first'))
ob=pd.read_csv('forecast/veg_outlook_b_5モデル平均.csv')[['年','月','品目','直後']].rename(columns={'直後':'予測1見'})
d=h3.merge(h1,on=['年','月','品目']).merge(ob,on=['年','月','品目'],how='left')
d['予測1見']=d.予測1見.fillna(d.予測1)
T=d[d.年>=2019].copy()
for c in ['予測','予測1','予測1見']: T['e_'+c]=(T[c]/T.実績-1).abs()*100
rng=np.random.default_rng(0)
print('3a 7〜9月、2019〜2026年(12品目)')
for c,lab in [('予測','6月末の3か月先'),('予測1','各月末の1か月先'),('予測1見','各月末の1か月先+見通し')]:
    print(' ',lab,round(T['e_'+c].mean(),2),' 2026',round(T[T.年==2026]['e_'+c].mean(),2), ' 月別',T.groupby('月')['e_'+c].mean().round(1).to_dict())
dd=(T.e_予測1-T.e_予測).values; bs=[rng.choice(dd,len(dd)).mean() for _ in range(2000)]
print('  1か月先 − 3か月先',round(dd.mean(),2),np.percentile(bs,[2.5,97.5]).round(2))
# 3b
d['y']=np.log(d.実績/d.予測)
rows=[]
for Y in range(2019,2027):
    tr=d[d.年<Y]; te=d[d.年==Y]
    for _,r in te.iterrows():
        for kind,src in [('まとめ',tr[tr.月==r.月]),('品目ごと',tr[(tr.月==r.月)&(tr.品目==r.品目)])]:
            lo,hi=np.quantile(src.y,[0.1,0.9])
            rows.append(dict(年=Y,月=r.月,品目=r.品目,幅=kind,下=r.予測*np.exp(lo),上=r.予測*np.exp(hi),実績=r.実績,
                             入る=(lo<=r.y<=hi),幅率=(np.exp(hi)-np.exp(lo))*100))
R=pd.DataFrame(rows); R.round(2).to_csv('forecast/veg_stage3.csv',index=False)
print('3b 80%の幅(2019〜2026年)')
print(R.groupby('幅').agg(入る割合=('入る','mean'),幅の中央値=('幅率','median')).round(2).to_string())
print(R.groupby(['幅','品目']).agg(入る=('入る','mean'),幅=('幅率','median')).unstack(0).round(2).to_string())
print('年ごとの入る割合(まとめ)',R[R.幅=='まとめ'].groupby('年').入る.mean().round(2).to_dict())
