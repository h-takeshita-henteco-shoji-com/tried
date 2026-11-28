"""#186 V3: 気象庁「過去の気象データ」の月ごとの値(気温・降水量・日照)を取る。出典: 気象庁ホームページ。"""
import pandas as pd, requests, io, time, re
ST={'福岡':(82,47807),'熊本':(86,47819),'佐賀':(85,47813),'大分':(83,47815),'軽井沢':(48,47622),'帯広':(20,47417),'網走':(17,47409)}
num=lambda v: pd.to_numeric(re.sub(r'[^0-9.\-]','',str(v)) or 'nan',errors='coerce')
rows=[]
for name,(pn,bn) in ST.items():
    for y in range(2009,2027):
        u=f'https://www.data.jma.go.jp/stats/etrn/view/monthly_s1.php?prec_no={pn}&block_no={bn}&year={y}&month=&day=&view='
        r=requests.get(u,headers={'User-Agent':'research-script (tried repo)'},timeout=30); r.encoding='utf-8'
        x=[t for t in pd.read_html(io.StringIO(r.text)) if t.shape[0]>=12][0]
        for _,row in x.iterrows():
            rows.append(dict(地点=name,年=y,月=int(row.iloc[0]),降水量=num(row.iloc[3]),気温=num(row.iloc[7]),日照=num(row.iloc[19])))
        time.sleep(1)
w=pd.DataFrame(rows); w.to_csv('data/weather_monthly.csv',index=False); print(w.groupby('地点').size(), w.tail(3))
