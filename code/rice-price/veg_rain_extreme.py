"""#186 V3x: 6月が大雨の年だけ、#184 の予測が低めに外れるかを確かめる(福岡12品目)。"""
import numpy as np, pandas as pd
# 地点と基準の予測は veg_weather.py(V3)と同じ
ST={'キャベツ':'軽井沢','はくさい':'軽井沢','レタス':'軽井沢','こまつな':'福岡','なす':'福岡','トマト':'熊本','きゅうり':'佐賀',
    'ブロッコリー':'帯広','にんじん':'帯広','ばれいしょ':'帯広','たまねぎ':'網走','ねぎ':'大分'}
f=pd.read_csv('forecast/fukuoka_models.csv')
stat=['SARIMA','指数平滑法','Prophet(Meta)','TimesFM(Google)','Chronos(Amazon)']
base={'指数平滑法':f[f['モデル']=='指数平滑法'],
      '5モデル平均':f[f['モデル'].isin(stat)].groupby(['年','月','品目'],as_index=False).agg(予測=('予測','mean'),実績=('実績','first'))}
w = pd.read_csv('data/weather_monthly.csv')
def z(st, y):
    x = w[(w.地点 == st) & (w.月 == 6)].set_index('年').降水量
    past = x[x.index < y]
    return (x[y] - past.mean()) / past.std()
rng = np.random.default_rng(0)
def boot(df, col):
    g = df.groupby(['年', '品目'])[col].mean().values
    bs = [rng.choice(g, len(g)).mean() for _ in range(5000)]
    return round(g.mean() * 100, 1), np.percentile(bs, [2.5, 97.5]).round(3) * 100, len(g)
rows = []
for bn, b in base.items():
    b = b.copy(); b['y'] = np.log(b['実績'] / b['予測'])
    b['z'] = [z(ST[r.品目], r.年) for r in b.itertuples()]; b['大雨'] = b.z > 1
    print(f'== {bn}  大雨の品目と年の組:', b[b.大雨].groupby(['年', '品目']).ngroups, '/', b.groupby(['年', '品目']).ngroups)
    print('   大雨の組:', sorted(set(zip(b[b.大雨].年, b[b.大雨].品目))))
    for lab, d in (('全部', b), ('2026年を除く', b[b.年 < 2026])):
        for m in ('7〜9月', 7):
            dd = d if m == '7〜9月' else d[d.月 == m]
            print(f'   A {lab} {m}: 大雨 平均%,95%,組数', boot(dd[dd.大雨], 'y'), ' それ以外', boot(dd[~dd.大雨], 'y'))
    out = []
    for Y in range(2019, 2027):
        tr, te = b[b.年 < Y], b[b.年 == Y].copy()
        c = tr[tr.大雨].y.mean() - tr[~tr.大雨].y.mean() if tr.大雨.any() else 0
        te['直後'] = te.予測 * np.exp(np.where(te.大雨, c, 0))
        out.append(te)
    o = pd.concat(out)
    o['元'] = (o.予測 / o.実績 - 1).abs() * 100; o['直'] = (o.直後 / o.実績 - 1).abs() * 100
    d = (o.直 - o.元).values; bs = [rng.choice(d, len(d)).mean() for _ in range(5000)]
    print(f'   B 2019-26: {o.元.mean():.2f} -> {o.直.mean():.2f} 差95%', np.percentile(bs, [2.5, 97.5]).round(2),
          f' 2026: {o[o.年==2026].元.mean():.2f} -> {o[o.年==2026].直.mean():.2f}',
          f' 2019-25: {o[o.年<2026].元.mean():.2f} -> {o[o.年<2026].直.mean():.2f}')
    rows.append(o.assign(基準=bn))
pd.concat(rows).to_csv('forecast/veg_rain_extreme.csv', index=False)
