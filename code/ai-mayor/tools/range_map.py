"""再現範囲の地図を描く。OpenStreetMap のタイルに、建設範囲(9.6km四方)と地図全体(17.28km四方)の枠を重ねる。

使い方: OUT=range-map.png SCALE=1 python3 range_map.py
SCALE は実際の距離÷ゲーム上の距離。2なら水平の縮尺1/2で、2倍の範囲を収める。
"""
import math, os, time, urllib.request, json
from PIL import Image, ImageDraw, ImageFont
SCALE=float(os.environ.get("SCALE","1"))
BUILD81=os.environ.get("BUILD81")=="1"  # 81 Tiles 2 Mod で全81区画を建設範囲にする場合
Z=13 if SCALE<1.5 else 12
CACHE=os.path.expanduser("~/.cache/ai-mayor-tiles")
os.makedirs(CACHE,exist_ok=True)
c=(33.59018,130.40987)
R=6371008.8
def ll(e,n): return (c[0]+math.degrees(n/R), c[1]+math.degrees(e/(R*math.cos(math.radians(c[0])))))
def px(lat,lon):
    x=(lon+180)/360*2**Z*256
    s=math.sin(math.radians(lat)); y=(0.5-math.log((1+s)/(1-s))/(4*math.pi))*2**Z*256
    return x,y
H=9300*SCALE
x0,y0=px(*ll(-H,H)); x1,y1=px(*ll(H,-H))
tx0,ty0,tx1,ty1=int(x0//256),int(y0//256),int(x1//256),int(y1//256)
W=(tx1-tx0+1)*256; Hh=(ty1-ty0+1)*256
img=Image.new("RGB",(W,Hh))
for tx in range(tx0,tx1+1):
    for ty in range(ty0,ty1+1):
        f=f"{CACHE}/{Z}_{tx}_{ty}.png"
        if not os.path.exists(f):
            r=urllib.request.Request(f"https://tile.openstreetmap.org/{Z}/{tx}/{ty}.png",headers={"User-Agent":"tried-ai-mayor-research/0.1 (personal blog figure)"})
            open(f,"wb").write(urllib.request.urlopen(r,timeout=30).read()); time.sleep(0.3)
        img.paste(Image.open(f).convert("RGB"),((tx-tx0)*256,(ty-ty0)*256))
img=Image.blend(img,Image.new("RGB",img.size,"white"),0.25)
d=ImageDraw.Draw(img,"RGBA")
def P(lat,lon):
    x,y=px(lat,lon); return x-tx0*256,y-ty0*256
def sq(half,**kw):
    a=P(*ll(-half,half)); b=P(*ll(half,-half)); d.rectangle([a,b],**kw)
# 9x9 grid faint, 5x5 grid
T=1920*SCALE
for i in range(10):
    v=(i-4.5)*T
    d.line([P(*ll(v,4.5*T)),P(*ll(v,-4.5*T))],fill=(80,80,80,60),width=1)
    d.line([P(*ll(-4.5*T,v)),P(*ll(4.5*T,v))],fill=(80,80,80,60),width=1)
for i in range(6):
    v=(i-2.5)*T
    d.line([P(*ll(v,2.5*T)),P(*ll(v,-2.5*T))],fill=(200,30,30,110),width=2)
    d.line([P(*ll(-2.5*T,v)),P(*ll(2.5*T,v))],fill=(200,30,30,110),width=2)
sq(8640*SCALE,outline=(30,60,200,255),width=5)
sq(4800*SCALE,outline=(200,30,30,255),width=6)
fb="/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
F=ImageFont.truetype(fb,30); Fs=ImageFont.truetype(fb,24)
def label(xy,t,font,col):
    d.text(xy,t,font=font,fill=col,stroke_width=4,stroke_fill="white")
label((P(*ll(-8600*SCALE,-8600*SCALE))[0]+10,P(*ll(-8600*SCALE,-8600*SCALE))[1]-80),(f"建設範囲 実寸{17.28*SCALE:g}km四方(81タイル、Modで解放)" if BUILD81 else f"ゲームの地図 実寸{17.28*SCALE:g}km四方(外周は建設不可)"),F,(30,60,200))
label((P(*ll(-4760*SCALE,4760*SCALE))[0]+10,P(*ll(-4760*SCALE,4760*SCALE))[1]+8),(f"中央25タイル 実寸{9.6*SCALE:g}km四方" if BUILD81 else f"建設範囲 実寸{9.6*SCALE:g}km四方(25タイル)"),F,(200,30,30))
pts=[("天神",33.5903225,130.3998391),("博多駅",33.5900413,130.4199026),("福岡空港",33.586802,130.4473939),("福岡タワー",33.5932744,130.3514862),("PayPayドーム",33.5953196,130.3621171),("大濠公園",33.5861214,130.3763612),("博多ポートタワー",33.6043006,130.3977599),("筥崎宮",33.617503,130.41535),("アイランドシティ",33.6643552,130.4207819),("福岡大学",33.5484434,130.3645137),("大橋駅",33.5622159,130.4289661),("香椎駅",33.659655,130.4441037),("姪浜駅",33.5837095,130.3251041)]
if SCALE>=1.5:
    pts=[q for q in pts if q[0] in ("天神","博多駅","福岡空港","福岡タワー","大濠公園")]+[("油山 597m",33.5120,130.3645),("脊振山 1055m",33.4364,130.3687),("宝満山 830m",33.5398,130.5692),("若杉山 681m",33.5978,130.5448),("立花山 367m",33.6798,130.4682),("叶岳 341m",33.5504,130.2898),("井原山 982m",33.4704,130.2498),("雷山 955m",33.4787,130.2235),("能古島",33.6224,130.3059),("志賀島",33.6741,130.3005),("太宰府天満宮",33.5213,130.5353)]
if SCALE>=2.5:
    pts=[q for q in pts if q[0] not in ("大濠公園","太宰府天満宮")]+[("九千部山 848m",33.4167,130.4460),("九大伊都",33.5957,130.2176),("太宰府",33.5213,130.5353),("糸島(前原)",33.5577,130.1963),("宗像",33.8053,130.5404),("鳥栖",33.3779,130.5063),("二日市",33.4983,130.5236),("篠栗",33.6244,130.5263)]
for n,la,lo in pts:
    x,y=P(la,lo); d.ellipse([x-9,y-9,x+9,y+9],fill=(255,140,0,255),outline="black",width=2)
    off={"福岡空港":(-40,14),"福岡タワー":(-150,-40),"PayPayドーム":(12,-14),"天神":(-70,-34),"博多駅":(12,-34),"宝満山 830m":(-150,14),"脊振山 1055m":(12,-44)}.get(n,(12,-14))
    label((x+off[0],y+off[1]),n,Fs,(20,20,20))
x,y=P(*c); d.line([x-16,y,x+16,y],fill="black",width=4); d.line([x,y-16,x,y+16],fill="black",width=4)
label((x+4,y+8),"中心",Fs,(0,0,0))
# crop to outer frame + margin
a=P(*ll(-9100*SCALE,9100*SCALE)); b=P(*ll(9100*SCALE,-9100*SCALE))
img=img.crop((int(a[0]),int(a[1]),int(b[0]),int(b[1])))
d=ImageDraw.Draw(img)
label((10,img.size[1]-36),"中心 33.59018, 130.40987(天神と博多駅の中間)  地図: © OpenStreetMap contributors",Fs,(0,0,0))
img.save(os.environ.get("OUT","range-map.png"),optimize=True); print(img.size)
