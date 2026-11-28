"""#186 V1: #184 の5つの統計モデルの予測を組み合わせる(福岡12品目、2019〜2026年を1年ずつ)。"""
import numpy as np, pandas as pd
f = pd.read_csv('forecast/fukuoka_models.csv')
M = ['SARIMA', '指数平滑法', 'Prophet(Meta)', 'TimesFM(Google)', 'Chronos(Amazon)']
w = f[f.モデル.isin(M)].pivot_table(index=['年', '月', '品目'], columns='モデル', values='予測').reset_index()
act = f.drop_duplicates(['年', '月', '品目']).set_index(['年', '月', '品目']).実績
w['実績'] = [act[(r.年, r.月, r.品目)] for r in w.itertuples()]
ae = lambda p, a: (p / a - 1).abs() * 100
for m in M: w['e_' + m] = ae(w[m], w.実績)
out = []
for Y in range(2019, 2027):
    tr, te = w[w.年 < Y], w[w.年 == Y].copy()
    te['5モデル平均'] = te[M].mean(axis=1)
    te['V1a 中央値'] = te[M].median(axis=1)
    pe = tr.groupby('品目')[['e_' + m for m in M]].mean()
    best = pe.idxmin(axis=1).str[2:]
    te['V1b 品目ごとに最良'] = [r[best[r.品目]] for _, r in te.iterrows()]
    wt = 1 / pe; wt = wt.div(wt.sum(axis=1), axis=0); wt.columns = M
    te['V1c 誤差の逆数で重み'] = [sum(r[m] * wt.loc[r.品目, m] for m in M) for _, r in te.iterrows()]
    gbest = tr[['e_' + m for m in M]].mean().idxmin()[2:]
    te['V1d 全体で最良'] = te[gbest]; te['V1d の選択'] = gbest
    out.append(te)
o = pd.concat(out)
C = ['5モデル平均', 'V1a 中央値', 'V1b 品目ごとに最良', 'V1c 誤差の逆数で重み', 'V1d 全体で最良']
E = pd.DataFrame({c: ae(o[c], o.実績) for c in C}); E['年'] = o.年.values
rng = np.random.default_rng(0)
print('2019-26', E[C].mean().round(2).to_dict()); print('2026', E[E.年 == 2026][C].mean().round(2).to_dict())
for c in C[1:]:
    d = (E[c] - E['5モデル平均']).values; bs = [rng.choice(d, len(d)).mean() for _ in range(5000)]
    print(c, '差', round(d.mean(), 2), '95%', np.percentile(bs, [2.5, 97.5]).round(2))
print('V1d が選んだモデル', o.groupby('年')['V1d の選択'].first().to_dict())
o.to_csv('forecast/veg_v1.csv', index=False)
