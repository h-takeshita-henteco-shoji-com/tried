import csv,sys,json,urllib.request,urllib.parse,difflib,time,re
def get(u):
    r=urllib.request.Request(u,headers={'User-Agent':'tried-repo/1.0'})
    return json.load(urllib.request.urlopen(r,timeout=30))
def norm(s): return re.sub(r'[^a-z0-9 ]','',s.lower().replace('—',' '))
def sim(a,b): return difflib.SequenceMatcher(None,norm(a),norm(b)).ratio()
rows=list(csv.DictReader(open(sys.argv[1]),delimiter='\t'))
out=[]
for r in rows:
    best=None
    try:
        cr=get('https://api.crossref.org/works?rows=5&query.bibliographic='+urllib.parse.quote(r['title']+' '+r['authors'].split(',')[0]))['message']['items']
        for it in cr:
            t=(it.get('title') or [''])[0]; s=sim(t,r['title'])
            if not best or s>best[0]:
                y=(it.get('issued',{}).get('date-parts') or [[None]])[0][0]
                best=(s,'crossref',t,y,(it.get('container-title') or [''])[0],it.get('volume',''),it.get('issue',''),it.get('page',''),it.get('DOI',''),(it.get('author') or [{}])[0].get('family',''))
    except Exception as e: print('crossref err',r['id'],e,file=sys.stderr)
    try:
        oa=get('https://api.openalex.org/works?per-page=5&search='+urllib.parse.quote(r['title']))['results']
        for it in oa:
            t=it.get('title') or ''; s=sim(t,r['title'])
            if not best or s>best[0]+0.02:
                b=it.get('biblio',{}); src=((it.get('primary_location') or {}).get('source') or {}).get('display_name','')
                pg=f"{b.get('first_page') or ''}-{b.get('last_page') or ''}"
                au=(it.get('authorships') or [{}])[0].get('author',{}).get('display_name','')
                best=(s,'openalex',t,it.get('publication_year'),src,b.get('volume',''),b.get('issue',''),pg,(it.get('doi') or '').replace('https://doi.org/',''),au)
    except Exception as e: print('openalex err',r['id'],e,file=sys.stderr)
    out.append({**r,'match':round(best[0],2) if best else 0,'via':best[1] if best else '','f_title':best[2] if best else '','f_year':best[3] if best else '','f_venue':best[4] if best else '','f_vip':f"{best[5]}({best[6]}), {best[7]}" if best else '','doi':best[8] if best else '','f_author1':best[9] if best else ''})
    time.sleep(0.3)
w=csv.DictWriter(open(sys.argv[2],'w'),fieldnames=list(out[0].keys()),delimiter='\t'); w.writeheader(); w.writerows(out)
