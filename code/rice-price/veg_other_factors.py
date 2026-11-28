"""野菜の値段と、天候以外の要因の相関(探索、事前登録なし)。値段は weather_price_corr.py と同じ「平年からのずれ」。
1) 前の年の同じ時期のずれ(高いと翌年は作付けが増えて安い、という周期)
2) 品目どうしの相関(共通の動き)
3) 同じ月の福岡の入荷量のずれ
出力: 画面のみ"""
import pandas as pd, numpy as np
IT=['キャベツ','はくさい','レタス','こまつな','トマト','きゅうり','なす','ブロッコリー','にんじん','ばれいしょ','たまねぎ','ねぎ']
p=pd.read_csv('data/fukuoka_monthly.csv'); p=p[p.品目.isin(IT)&(p.年<=2025)].copy()
p['lp']=np.log(p.価格); p['lq']=np.log(p.数量t)
for c in ['lp','lq']:
    p[c+'a']=p[c]-p.groupby(['品目','月'])[c].transform('mean')
# 季節だけ除いたずれ(年の水準は残す。前年との比較に年の水準が要るため)。トレンドは品目ごとに直線で除く
for c in ['lpa','lqa']:
    p[c]=p.groupby('品目',group_keys=False).apply(lambda g: g[c]-np.polyval(np.polyfit(g.年+g.月/12,g[c],1),g.年+g.月/12))
s=p[p.月.isin([7,8,9])].groupby(['品目','年'])[['lpa','lqa']].mean().reset_index()
print('1) 7〜9月の値段のずれと、前の年の7〜9月のずれの相関')
r1={it:np.corrcoef(g.lpa.values[1:],g.lpa.values[:-1])[0,1] for it,g in s.groupby('品目')}
print(pd.Series(r1).round(2).sort_values().to_string()); print('中央値',round(np.median(list(r1.values())),2))
print('1b) 前の年の7〜9月の値段のずれと、今年の7〜9月の入荷量のずれ')
r1b={it:np.corrcoef(g.lqa.values[1:],g.lpa.values[:-1])[0,1] for it,g in s.groupby('品目')}
print('中央値',round(np.median(list(r1b.values())),2), '負の品目',sum(v<0 for v in r1b.values()))
w=p.pivot_table(index=['年','月'],columns='品目',values='lpa')
c=w.corr().values; off=c[np.triu_indices(12,1)]
print('2) 品目どうしの月の値段のずれの相関: 中央値',round(np.median(off),2),'正の組',(off>0).sum(),'/',len(off))
pc=np.linalg.eigh(np.corrcoef(w.dropna().T.values))[0][::-1]
print('   第1主成分の説明割合',round(pc[0]/pc.sum(),2))
print('3) 同じ月の値段のずれと入荷量のずれ(全月)')
r3={it:np.corrcoef(g.lpa,g.lqa)[0,1] for it,g in p.groupby('品目')}
print(pd.Series(r3).round(2).sort_values().to_string()); print('中央値',round(np.median(list(r3.values())),2))
