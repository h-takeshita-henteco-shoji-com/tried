# 記事の図2枚(two-axes.html / three-texts.html)を作る。PNG化は Chrome のヘッドレスで行う
FONT='"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif'
C={'ink':'#222','sub':'#666','line':'#c9d1d6','yoso':'#3b6ea5','riyu':'#2e8b57','toi':'#d2691e','saki':'#b22222',
   'blk':'#eef2f5','blkline':'#9aa8b2','ten':'#fff1d6','tenline':'#d4a017','good':'#2e8b57','bad':'#b22222'}

def head(title, sub, w, h):
    return f'''<!doctype html><html lang="ja"><meta charset="utf-8">
<style>body{{margin:0;background:#fff;font-family:{FONT};color:{C['ink']}}}</style>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family='{FONT}'>
<rect width="{w}" height="{h}" fill="#fff"/>
<text x="40" y="52" font-size="28" font-weight="700">{title}</text>
<text x="40" y="84" font-size="16" fill="{C['sub']}">{sub}</text>
'''

def block(x,y,w,h,role,label,ten=False):
    f,l=(C['ten'],C['tenline']) if ten else (C['blk'],C['blkline'])
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{f}" stroke="{l}" stroke-width="1.5"/>'
            f'<text x="{x+w/2}" y="{y+26}" font-size="17" font-weight="700" text-anchor="middle">{role}</text>'
            f'<text x="{x+w/2}" y="{y+50}" font-size="13" fill="{C["sub"]}" text-anchor="middle">{label}</text>')

def arc(x1,x2,y,hgt,color,label=None,up=True,lx=None,dash=False):
    d=-1 if up else 1
    cy=y+d*hgt
    s=f'<path d="M{x1},{y} C{x1},{cy} {x2},{cy} {x2},{y}" fill="none" stroke="{color}" stroke-width="2.5"{" stroke-dasharray=&quot;7 5&quot;" if dash else ""}/>'
    s+=f'<polygon points="{x2-6},{y+d*12} {x2+6},{y+d*12} {x2},{y}" fill="{color}"/>'
    if label:
        lx=lx if lx is not None else (x1+x2)/2
        s+=f'<text x="{lx}" y="{y+d*hgt*0.75+(-6 if up else 16)}" font-size="14" fill="{color}" font-weight="700" text-anchor="middle">{label}</text>'
    return s

# ---------- 図1 ----------
W,H=1240,1010
roles=[('起','建設業にロボット',False),('承','設計を軽んじる',False),('結(先置き)','品質を気にしない理由',False),
       ('転(内側)','品質が下がる',True),('転(全体)','実はソフトウェア',True),('問い','どうすればいい?',False),
       ('答え','自動テスト',False),('結び','設計できる人が要る',False)]
x0,bw,gap=60,132,12
xs=[x0+i*(bw+gap) for i in range(len(roles))]
cx=lambda i: xs[i]+bw/2
svg=head('文章を、構成と文の2つの軸で評価する',
         '例:「コードは設計である」(原文)を、役割を担う文に分けた模式図。数値はまだ測っていない',W,H)

# panel 1
py=120
svg+=f'<rect x="30" y="{py}" width="{W-60}" height="430" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
svg+=f'<text x="56" y="{py+40}" font-size="22" font-weight="700" fill="{C["yoso"]}">構成の軸 ― 文と文の関連を評価する</text>'
svg+=f'<text x="56" y="{py+68}" font-size="15" fill="{C["sub"]}">役割の文がそろっているか、どうつながっているかを見る。文章だけを見て決める(AIが文の役割を見分ける)</text>'
by=py+250
svg+=arc(cx(0),cx(4),by,150,C['yoso'],'予想を作る',lx=(cx(0)+cx(4))/2)
svg+=arc(cx(1),cx(4),by,95,C['yoso'])
svg+=arc(cx(2),cx(3),by,45,C['riyu'],'理由を渡す',lx=cx(2)+70)
svg+=arc(cx(5),cx(6),by,60,C['toi'],'答える')
svg+=arc(cx(2),cx(4),by+64,60,C['riyu'],'理由を渡す(転より前に置く)',up=False)
for i,(r,l,t) in enumerate(roles): svg+=block(xs[i],by,bw,64,r,l,t)
svg+=f'<text x="56" y="{py+410}" font-size="14" fill="{C["sub"]}">数えるもの: 役割がそろっているか / 弧の長さ(読者が答えを待つ長さ)/ 理由を先に置くか、答えを先に出すか</text>'

# panel 2
py2=py+460
svg+=f'<rect x="30" y="{py2}" width="{W-60}" height="400" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
svg+=f'<text x="56" y="{py2+40}" font-size="22" font-weight="700" fill="{C["good"]}">文の軸 ― 1文ごとに、役割を果たしたかを評価する</text>'
svg+=f'<text x="56" y="{py2+68}" font-size="15" fill="{C["sub"]}">読者(AIと自分)に1段落ずつ読ませ、予想・驚き・納得を聞く。役割を担う文の位置で、読者に何が起きたかを見る</text>'
by2=py2+92
for i,(r,l,t) in enumerate(roles): svg+=block(xs[i],by2,bw,64,r,l,t)
checks={4:('読者の予想は','大きく動いたか'),2:('転を読んだあと','納得したか'),5:('読者は問いを','抱いたか'),6:('問いは','解けたか'),0:('読者は予想を','持てたか')}
for i,(a,b) in checks.items():
    x=cx(i); y=by2+64
    svg+=f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+36}" stroke="{C["good"]}" stroke-width="2"/>'
    svg+=f'<rect x="{x-64}" y="{y+36}" width="128" height="62" rx="8" fill="#eaf5ee" stroke="{C["good"]}"/>'
    svg+=f'<text x="{x}" y="{y+61}" font-size="14" text-anchor="middle">{a}</text><text x="{x}" y="{y+82}" font-size="14" text-anchor="middle" font-weight="700">{b}</text>'
svg+=f'<text x="56" y="{py2+300}" font-size="15">例: 転の文 → 読者の予想が、ふつうの段落の2倍以上動いたら「果たした」とみなす(仮の目安)</text>'
svg+=f'<text x="56" y="{py2+328}" font-size="15">例: 結の文 → 読者の過半数が「納得した」と答えたら「果たした」とみなす</text>'
svg+=f'<text x="56" y="{py2+370}" font-size="14" fill="{C["sub"]}">その文だけで意味が分かるか(1文の分かりやすさ)は、役割を果たしたかとは別に、読みやすさの側で測る</text>'
svg+='</svg></html>'
open('two-axes.html','w',encoding='utf-8').write(svg)

# ---------- 図2 ----------
W2,H2=1240,980
svg=head('2つの軸で見ると、3本の文章が分かれる',
         '#47 の文章をAIが評価した結果を、2つの軸に置き直した模式図。数値はまだ測っていない',W2,H2)
rows=[
 ('「コードは設計である」','原文',
  [('起',0),('承',0),('結',0),('転',1),('問い',0),('答え',0)],
  [(0,3,'yoso',True),(2,3,'riyu',False),(4,5,'toi',True)], None,
  ('そろっている',True),('転が果たした',True),'読者は建設業の話だと思って読み、72%で裏切られる','面白い'),
 ('「コードは設計である」','AIの書き直し',
  [('答え',0),('起',0),('承',0),('転',1),('結',0)],
  [(1,3,'yoso',True),(4,3,'riyu',True)], (0,3),
  ('そろっている(順番が違う)',True),('転が果たせない',False),'冒頭2%で答えを渡し、転の前に予想が直されていた','面白くない'),
 ('「竜巻などの激しい突風」','AIの書き直し',
  [('起',3),('題',2),('説明',0),('説明',0),('転',1),('結',0)],
  [(0,4,'yoso',True),(5,4,'riyu',True)], (1,4),
  ('そろっている',True),('転が果たせない',False),'題「竜巻だけではない」が、転を先に明かしていた。起は本文になく、読者の思い込みを借りる(点線)','面白くない'),
]
y=120
for name,ver,blks,arcs,saki,kosei,bun,why,verdict in rows:
    svg+=f'<rect x="30" y="{y}" width="{W2-60}" height="250" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
    svg+=f'<text x="56" y="{y+36}" font-size="20" font-weight="700">{name}<tspan font-size="16" fill="{C["sub"]}" font-weight="400"> {ver}</tspan></text>'
    bx0,bw2,g2=56,92,10
    xs2=[bx0+i*(bw2+g2) for i in range(len(blks))]
    c2=lambda i: xs2[i]+bw2/2
    yb=y+120
    for a,b,col,up in arcs: svg+=arc(c2(a),c2(b),yb,46 if abs(a-b)<3 else 70,C[col])
    if saki: svg+=arc(c2(saki[0]),c2(saki[1]),yb+50,44,C['saki'],'先に明かす',up=False)
    for i,(r,t) in enumerate(blks):
        f,l=((C['ten'],C['tenline']) if t==1 else ('#fde8e8',C['saki']) if t==2 else ('#fff',C['yoso']) if t==3 else (C['blk'],C['blkline']))
        if r=='答え' and saki and i==0: f,l='#fde8e8',C['saki']
        dash=' stroke-dasharray="6 4"' if t==3 else ''
        svg+=f'<rect x="{xs2[i]}" y="{yb}" width="{bw2}" height="50" rx="7" fill="{f}" stroke="{l}" stroke-width="1.5"{dash}/>'
        svg+=f'<text x="{c2(i)}" y="{yb+31}" font-size="16" font-weight="700" text-anchor="middle">{r}</text>'
    tx=720
    def mark(ok): return ('○',C['good']) if ok else ('×',C['bad'])
    m,cl=mark(kosei[1]); svg+=f'<text x="{tx}" y="{y+76}" font-size="17"><tspan fill="{C["yoso"]}" font-weight="700">構成の軸 </tspan><tspan fill="{cl}" font-weight="700">{m}</tspan> {kosei[0]}</text>'
    m,cl=mark(bun[1]); svg+=f'<text x="{tx}" y="{y+110}" font-size="17"><tspan fill="{C["good"]}" font-weight="700">文の軸 </tspan><tspan fill="{cl}" font-weight="700">{m}</tspan> {bun[0]}</text>'
    svg+=f'<text x="{tx}" y="{y+144}" font-size="14" fill="{C["sub"]}">{why[:34]}</text>'
    if len(why)>34: svg+=f'<text x="{tx}" y="{y+164}" font-size="14" fill="{C["sub"]}">{why[34:]}</text>'
    vc=C['good'] if verdict=='面白い' else C['bad']
    svg+=f'<text x="{tx}" y="{y+204}" font-size="18" font-weight="700" fill="{vc}">→ {verdict}</text>'
    y+=266
svg+=f'<text x="40" y="{y+24}" font-size="16">構成の軸だけでは3本とも「そろっている」。違いは、文の軸に出る</text>'
svg+='</svg></html>'
open('three-texts.html','w',encoding='utf-8').write(svg)
