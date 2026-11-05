# plugin の全命令を順に試す。LibreCAD が落ちたらそこで止まる
from lc import *
import os, sys
T="/tmp/lcmcp"
def step(_n, cmd, **a):
    try:
        r = call(cmd, **a)
    except Exception as e:
        print(f"!! {_n}: {e}"); sys.exit(1)
    print(("OK " if r.get("ok") else "NG ") + _n, short({k:v for k,v in r.items() if k not in ("id","ok")}, 260))
    return r
step("open","open",path=f"{T}/house.dxf")
print("   polyline:", short(call("list_entities",types=["polyline"])["entities"][0],200))
dims = step("dims","list_entities",types=["dim_linear","dim_aligned"])["entities"]
print("   dim sample:", short(dims[0],300) if dims else None)
step("blocks","list_blocks")
ins = step("inserts","list_entities",types=["insert"],expand_blocks=True)["entities"]
step("texts","list_entities",types=["text","mtext"])
step("window filter","list_entities",window=[[0,0],[3000,3000]])
step("fonts","fonts")
step("layers","layers")
step("new","new")
step("set_layer WALL","set_layer",name="WALL",color="#ffffff",current=True)
step("set_layer CENTER","set_layer",name="CENTER",color="#ff0000",linetype="center")
l = step("add_line","add_line",p1=[0,0],p2=[3600,0],layer="WALL")["entity"]
step("add_polyline","add_polyline",points=[[0,0],[3600,0],[3600,2700],[0,2700]],closed=True,layer="WALL")
step("add_arc","add_arc",center=[0,0],r=800,a1=0,a2=90,layer="WALL")
step("add_circle","add_circle",center=[1800,1350],r=100)
t = step("add_text center","add_text",text="洋室 6畳",p=[1800,1350],height=250,align="center",valign="middle",layer="TEXT")["entity"]
print("   text bbox:", t.get("bbox"))
d = step("add_dim_linear","add_dim_linear",p1=[0,0],p2=[3600,0],line=[0,-600],angle=0,layer="DIM")["entity"]
print("   dim:", short(d,300))
step("add_dim_aligned","add_dim_aligned",p1=[3600,0],p2=[3600,2700],line=[4200,0],layer="DIM")
step("add_hatch","add_hatch",points=[[4000,0],[4500,0],[4500,500],[4000,500]],pattern="SOLID",layer="HATCH")
c = step("add_circle for block","add_circle",center=[5000,0],r=200)["entity"]
step("define_block","define_block",name="MARK",base=[5000,0],ids=[c["id"]],replace=True)
step("add_insert","add_insert",block="MARK",p=[6000,0],angle=45)
step("set_props text","set_props",id=t["id"],text="洋室 7畳",color="#00ff00")
step("set_props dim label","set_props",id=d["id"],text="3,500")
r=step("move","move",ids=[l["id"]],offset=[0,-100]); l={"id":r["new_ids"][0]}
step("copy","copy",ids=[l["id"]],offset=[0,-200])
r=step("rotate","rotate",ids=[l["id"]],center=[0,0],angle=10); l={"id":r["new_ids"][0]}
r=step("scale","scale",ids=[l["id"]],center=[0,0],factor=0.5); l={"id":r["new_ids"][0]}
r=step("mirror","mirror",ids=[l["id"]],p1=[0,0],p2=[0,100]); l={"id":r["new_ids"][0]}
step("stretch","stretch",p1=[3500,-1000],p2=[5000,3000],offset=[300,0])
dd = step("dims after stretch","list_entities",types=["dim_linear","dim_aligned"])["entities"]
for x in dd: print("   ", x.get("label"), x.get("measured"), x.get("distance"), x.get("p1"), x.get("p2"))
step("undo 1","undo")
step("redo 1","redo"); l={"id":[e for e in call("list_entities",types=["line"])["entities"]][0]["id"]}
step("delete","delete",ids=[l["id"]])
step("doc_info","doc_info")
step("zoom auto","zoom")
step("screenshot","screenshot",path=f"{T}/shot.png")
step("screenshot window","screenshot",path=f"{T}/shot-win.png",window=[[-500,-1000],[4500,3000]])
step("save_as","save_as",path=f"{T}/out.dxf",overwrite=True)
step("save","save")
step("log","log")
