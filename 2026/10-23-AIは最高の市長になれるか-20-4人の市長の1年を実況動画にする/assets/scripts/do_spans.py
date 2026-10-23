import json,glob,datetime as dt
T=json.load(open('video-timeline.json'))
dirs={'base':'16-基準','money':'17-お金','population':'18-人口','livable':'19-住みやす'}
ACT={'place_building','build_line','bulldoze','zone_area','zone_rect','zone_polygon','set_tax','set_budget','set_policy','upgrade_road','create_transport_line','set_building_active','paint_district','set_district_policy','remove_line','relocate_building','empty_building'}
def vsec(m,t):
    for s in T:
        if s['mayor']!=m: continue
        r=dt.datetime.strptime(s['real_start'],'%Y-%m-%d %H:%M:%S')
        d=(t-r).total_seconds()
        if 0<=d<=s['duration']: return s['video_start']+d
P=lambda s:dt.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
fmt=lambda v:f'{int(v//3600)}:{int(v%3600//60):02d}:{int(v%60):02d}'
res={}
for m,k in dirs.items():
    seen=set();rows=[]
    for f in sorted(glob.glob(f'../*{k}*/command-log-*.txt')):
        L=[l.split('\t') for l in open(f,encoding='utf-8-sig').read().splitlines()]
        L=[p for p in L if len(p)>=4 and p[0][:2]=='20']
        for i,p in enumerate(L):
            if p[2]!='DO' or (p[0],p[3]) in seen: continue
            seen.add((p[0],p[3]))
            t0=P(p[0]);last=t0;n=0
            for q in L[i+1:]:
                if q[2] in('DO','TITLE'): break
                tool=q[3].split(' ')[0]
                if tool=='advance' and q[2]=='OK': break
                if q[2]=='OK' and tool in ACT and (P(q[0])-t0).total_seconds()<600: last=P(q[0]);n+=1
            v=vsec(m,t0)
            rows.append(dict(t=p[0],date=p[1],do=p[3],v0=v,v1=vsec(m,last) or v,n=n))
    res[m]=rows
    for r in rows: print(m,fmt(r['v0']),fmt(r['v1']),r['n'],r['date'],r['do'][:60],sep='\t')
json.dump(res,open('/tmp/scenes/spans.json','w'),ensure_ascii=False,indent=1)
