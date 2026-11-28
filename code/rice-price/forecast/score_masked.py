"""#186 段2の採点。使い方: ../.venv/bin/python score_masked.py"""
import json, glob
from pathlib import Path
import numpy as np, pandas as pd
import run_claude_masked as m
HERE=Path(__file__).parent
f=pd.read_csv(HERE/'fukuoka_models.csv')
STAT=['SARIMA','指数平滑法','Prophet(Meta)','TimesFM(Google)','Chronos(Amazon)']
act=f.groupby(['年','月','品目']).実績.first()
base=f[f['モデル'].isin(STAT)].groupby(['年','月','品目']).予測.mean()
rows=[]; cost=0
for d in sorted((HERE/'runs/masked').iterdir()):
    cond,y=d.name.split('_'); y=int(y)
    runs=[json.load(open(p)) for p in sorted(d.glob('[0-9].json'))]; cost+=sum(r['cost_usd'] for r in runs)
    for it in m.ITEMS:
        for mo in (7,8,9):
            vals=[r['answer'][f'{m.LAB[it]}_{mo}'] for r in runs]
            rows.append(dict(条件=cond,年=y,品目=it,月=mo,予測=np.median(vals),実績=act[(y,mo,it)],基準=base[(y,mo,it)],
                             know=runs[0]['answer']['knowledge'][:20]))
R=pd.DataFrame(rows); R['誤差']=(R.予測/R.実績-1).abs()*100; R['基準誤差']=(R.基準/R.実績-1).abs()*100
R['符号']=(R.予測/R.実績-1)*100
R.to_csv(HERE/'masked_scores.csv',index=False)
Y=R.pivot_table(index='年',columns='条件',values='誤差').round(2)
Y['5モデル平均']=R[R.条件=='ma'].groupby('年').基準誤差.mean().round(2); Y['mv-ma']=Y.mv-Y.ma
print(Y.to_string()); print('費用',round(cost,2))
rng=np.random.default_rng(0)
for lab,yrs in [('2019〜2025',range(2019,2026)),('2019〜2026',range(2019,2027))]:
    s=Y.loc[list(yrs)]
    for a,b in [('mv','ma'),('ma','5モデル平均'),('mv','5モデル平均')]:
        d=(s[a]-s[b]).values; bs=[rng.choice(d,len(d)).mean() for _ in range(5000)]
        print(lab,a,'-',b,round(d.mean(),2),np.percentile(bs,[2.5,97.5]).round(2))
    print(lab,'平均', s[['ma','mv','5モデル平均']].mean().round(2).to_dict())
print('偏り',R.groupby('条件').符号.mean().round(1).to_dict())
print('knowledge',R.know.unique()[:5])
print(R.pivot_table(index='品目',columns='条件',values='誤差').round(1).assign(基準=R[R.条件=='ma'].groupby('品目').基準誤差.mean().round(1)).to_string())
