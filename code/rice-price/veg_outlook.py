"""#186 V6: 農水省「野菜の生育状況及び価格見通し」の価格の点で、予測を直す。

使い方: .venv/bin/python veg_outlook.py [a|b|diag]
  diag: 見通しの点と、東京の価格の平年(過去5年の同じ月の平均)との比を比べる
  a: 6月末の予測(#184)の7〜9月を、7月の見通しで直す
  b: 1か月先の予測(forecast/h1)を、その月の見通しで直す
"""
import sys
import numpy as np, pandas as pd, statsmodels.api as sm
o = pd.read_csv('data/maff_veg_outlook.csv')
S = o.groupby(['対象年', '対象月', '品目'])['価格_点'].mean()  # 前半・後半は平均
M5 = ['SARIMA', '指数平滑法', 'Prophet(Meta)', 'TimesFM(Google)', 'Chronos(Amazon)']
rng = np.random.default_rng(0)
def score(y, m, it): return S.get((y, m, it), np.nan)
def boot(d):
    bs = [rng.choice(d, len(d)).mean() for _ in range(5000)]; return np.percentile(bs, [2.5, 97.5]).round(2)

def correct(b, label):
    """b: 年, 品目, 予測, 実績, 点。点が NaN の行は直さない。2019〜2026年を1年ずつ。"""
    b = b.copy(); b['y'] = np.log(b.実績 / b.予測); out = []
    for Y in range(2019, 2027):
        tr = b[(b.年 < Y) & b.点.notna()]; te = b[b.年 == Y].copy()
        B = sm.OLS(tr.y, sm.add_constant(tr.点)).fit()
        adj = B.params.iloc[0] + B.params.iloc[1] * te.点
        te['直後'] = np.where(te.点.notna(), te.予測 * np.exp(adj), te.予測); te['傾き'] = B.params.iloc[1]
        out.append(te)
    r = pd.concat(out); r['元'] = (r.予測 / r.実績 - 1).abs() * 100; r['直'] = (r.直後 / r.実績 - 1).abs() * 100
    d = (r.直 - r.元).values; c = r[r.点.notna()]
    print(f'{label}: 2019-26 {r.元.mean():.2f} -> {r.直.mean():.2f} 差95% {boot(d)}  2026 {r[r.年==2026].元.mean():.2f} -> {r[r.年==2026].直.mean():.2f}'
          f'  見通しのある行 {len(c)}/{len(r)} でだけ: {c.元.mean():.2f} -> {c.直.mean():.2f}  傾き(2026学習) {r[r.年==2026].傾き.iloc[0]:.3f}')
    return r

mode = sys.argv[1]
if mode == 'diag':
    t = pd.read_csv('data/tokyo12_monthly.csv')
    t = t.groupby(['品目', '年', '月']).価格.mean()
    rows = []
    for (it, y, m), p in t.items():
        past = [t.get((it, yy, m)) for yy in range(y - 5, y)]
        if None in past or np.isnan(score(y, m, it)): continue
        rows.append(dict(品目=it, 年=y, 月=m, 点=score(y, m, it), 比=np.log(p / np.mean(past))))
    d = pd.DataFrame(rows)
    print('行', len(d), '年', d.年.min(), '-', d.年.max(), ' 相関', round(d.点.corr(d.比), 2))
    print(d.groupby('品目').apply(lambda g: round(g.点.corr(g.比), 2)).to_dict())
    print('点ごとの東京の平年比(平均%)', (d.groupby(d.点.round())['比'].mean().apply(np.exp) * 100 - 100).round(1).to_dict())
    d.to_csv('forecast/veg_outlook_diag.csv', index=False)
elif mode == 'a':
    f = pd.read_csv('forecast/fukuoka_models.csv')
    bases = {'指数平滑法': f[f.モデル == '指数平滑法'],
             '5モデル平均': f[f.モデル.isin(M5)].groupby(['年', '月', '品目'], as_index=False).agg(予測=('予測', 'mean'), 実績=('実績', 'first'))}
    for bn, b in bases.items():
        b = b.copy(); b['点'] = [score(r.年, 7, r.品目) for r in b.itertuples()]
        r7 = correct(b[b.月 == 7], f'V6a {bn} 7月だけ')
        correct(b, f'V6a {bn} 7〜9月(7月の点を8・9月にも)')
        r7.assign(基準=bn).to_csv(f'forecast/veg_outlook_a_{bn}.csv', index=False)
elif mode == 'b':
    import glob
    h = pd.concat(pd.read_csv(p) for p in glob.glob('forecast/h1/*.csv'))
    bases = {'指数平滑法': h[h.モデル == '指数平滑法'], '前の月のまま': h[h.モデル == '前の月のまま'],
             '5モデル平均': h[h.モデル.isin(M5)].groupby(['年', '月', '品目'], as_index=False).agg(予測=('予測', 'mean'), 実績=('実績', 'first'))}
    for bn, b in bases.items():
        b = b.copy(); b['点'] = [score(r.年, r.月, r.品目) for r in b.itertuples()]
        r = correct(b, f'V6b {bn}')
        r.assign(基準=bn).to_csv(f'forecast/veg_outlook_b_{bn}.csv', index=False)
