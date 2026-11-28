"""#186 V4(実行: DYLD_LIBRARY_PATH に torch の lib を足す。libomp のため): 12品目をまとめて1つの LightGBM で学ぶ(6月末→7〜9月、2019〜2026年を1年ずつ)。"""
import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, lightgbm as lgb
ITEMS = ["キャベツ","はくさい","レタス","こまつな","トマト","きゅうり","なす","ブロッコリー","にんじん","ばれいしょ","たまねぎ","ねぎ"]
ST = {'キャベツ':'軽井沢','はくさい':'軽井沢','レタス':'軽井沢','こまつな':'福岡','なす':'福岡','トマト':'熊本','きゅうり':'佐賀',
      'ブロッコリー':'帯広','にんじん':'帯広','ばれいしょ':'帯広','たまねぎ':'網走','ねぎ':'大分'}
a = pd.read_csv('data/fukuoka_monthly.csv'); b = pd.read_csv('data/fukuoka_daily_monthly.csv')
for d in (a, b): d['品目'] = d['品目'].str.strip()
v = pd.concat([a[a.年 < 2026][['年','月','品目','数量t','価格']], b[b.年 == 2026][['年','月','品目','数量t','価格']]])
v = v[v.品目.isin(ITEMS)]
P = v.set_index(['品目','年','月']).価格; Q = np.log(v.set_index(['品目','年','月']).数量t)
w = pd.read_csv('data/weather_monthly.csv'); w['lp'] = np.log(w.降水量 + 1); W = w.set_index(['地点','年','月'])
def lp(it, y, m): return np.log(P[(it, y, m)])
def anomQ(it, y, m):
    past = [Q[(it, yy, m)] for yy in range(2010, y) if (it, yy, m) in Q.index]
    return Q[(it, y, m)] - np.mean(past)
def anomW(st, y, m, var):
    past = W.loc[[(st, yy, m) for yy in range(2009, y)], var]
    return W.loc[(st, y, m), var] - past.mean(), past.std()
rows = []
for it in ITEMS:
    for y in range(2011, 2027):
        p6 = lp(it, y, 6)
        base = dict(品目=it, 年=y, d65=p6 - lp(it, y, 5), d64=p6 - lp(it, y, 4),
                    lvl=p6 - np.mean([lp(it, yy, 6) for yy in range(max(2010, y - 3), y)]))
        st = ST[it]
        ex = dict(qAMJ=np.mean([anomQ(it, y, m) for m in (4, 5, 6)]), qJ=anomQ(it, y, 6),
                  tAMJ=np.mean([anomW(st, y, m, '気温')[0] for m in (4, 5, 6)]),
                  sAMJ=np.mean([anomW(st, y, m, '日照')[0] for m in (4, 5, 6)]),
                  pAMJ=np.mean([anomW(st, y, m, 'lp')[0] for m in (4, 5, 6)]))
        dz, sd = anomW(st, y, 6, '降水量'); ex['zJ'] = dz / sd
        for m in (7, 8, 9):
            rows.append({**base, **ex, '月': m, 'y': lp(it, y, m) - p6, 'p6': np.exp(p6), '実績': P[(it, y, m)],
                         'prev': lp(it, y - 1, m) - lp(it, y - 1, 6) if y > 2010 else np.nan})
D = pd.DataFrame(rows)
D['item'] = D.品目.map({k: i for i, k in enumerate(ITEMS)}).astype('category')
FA = ['item', '月', 'd65', 'd64', 'lvl', 'seas', 'prev']; FB = FA + ['qAMJ', 'qJ', 'tAMJ', 'sAMJ', 'pAMJ', 'zJ']
PAR = dict(objective='regression', num_leaves=7, min_data_in_leaf=20, learning_rate=0.03, verbose=-1, seed=0, deterministic=True, num_threads=1)
out = []
for Y in range(2019, 2027):
    d = D.copy()
    # 過去の年の「6月→その月」の比の平均は、各行について、その行の年より前の年だけで作る
    d['seas'] = [D[(D.品目 == r.品目) & (D.月 == r.月) & (D.年 < r.年)].y.mean() for r in d.itertuples()]
    tr, te = d[(d.年 < Y) & (d.年 >= 2012)], d[d.年 == Y].copy()
    te['季節の比だけ'] = te.p6 * np.exp(te.seas)
    for name, F in (('V4a', FA), ('V4b', FB)):
        m = lgb.train(PAR, lgb.Dataset(tr[F], tr.y, categorical_feature=['item']), num_boost_round=200)
        te[name] = te.p6 * np.exp(m.predict(te[F]))
    out.append(te)
o = pd.concat(out)
f = pd.read_csv('forecast/fukuoka_models.csv')
M = ['SARIMA', '指数平滑法', 'Prophet(Meta)', 'TimesFM(Google)', 'Chronos(Amazon)']
mean5 = f[f.モデル.isin(M)].groupby(['年','月','品目']).予測.mean()
o['5モデル平均'] = [mean5[(r.年, r.月, r.品目)] for r in o.itertuples()]
C = ['5モデル平均', '季節の比だけ', 'V4a', 'V4b']
E = pd.DataFrame({c: (o[c] / o.実績 - 1).abs() * 100 for c in C}); E['年'] = o.年.values
print('2019-26', E[C].mean().round(2).to_dict()); print('2026', E[E.年 == 2026][C].mean().round(2).to_dict())
rng = np.random.default_rng(0)
for c, ref in (('V4a', '5モデル平均'), ('V4b', '5モデル平均'), ('V4b', 'V4a'), ('季節の比だけ', '5モデル平均')):
    dd = (E[c] - E[ref]).values; bs = [rng.choice(dd, len(dd)).mean() for _ in range(5000)]
    print(c, '-', ref, round(dd.mean(), 2), '95%', np.percentile(bs, [2.5, 97.5]).round(2))
o.to_csv('forecast/veg_v4.csv', index=False)
