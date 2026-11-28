"""#186 段0 O3: 夏の主な産地の気象台を足す。気象庁「過去の気象データ」の月ごとの値。出典: 気象庁ホームページ。出力: data/weather_monthly_more.csv"""
import pandas as pd, requests, io, time, re
ST={'前橋':(42,47624),'長野':(48,47610),'盛岡':(33,47584),'福島':(36,47595),'水戸':(40,47629),'宇都宮':(41,47615),
    '青森':(31,47575),'秋田':(32,47582),'山形':(35,47588),'洲本':(63,47776)}
num=lambda v: pd.to_numeric(re.sub(r'[^0-9.\-]','',str(v)) or 'nan',errors='coerce')
rows=[]
for name,(pn,bn) in ST.items():
    for y in range(2009,2027):
        u=f'https://www.data.jma.go.jp/stats/etrn/view/monthly_s1.php?prec_no={pn}&block_no={bn}&year={y}&month=&day=&view='
        r=requests.get(u,headers={'User-Agent':'research-script (tried repo)'},timeout=30); r.encoding='utf-8'
        if y==2009: print(name, name in r.text, flush=True)
        x=[t for t in pd.read_html(io.StringIO(r.text)) if t.shape[0]>=12][0]
        for _,row in x.iterrows():
            rows.append(dict(地点=name,年=y,月=int(row.iloc[0]),降水量=num(row.iloc[3]),気温=num(row.iloc[7]),日照=num(row.iloc[19])))
        time.sleep(1)
w=pd.DataFrame(rows); w.to_csv('data/weather_monthly_more.csv',index=False); print(w.groupby('地点').size()); print(w[(w.年==2025)&(w.月==8)])
