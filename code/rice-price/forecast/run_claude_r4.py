"""#186 R4: Claude に過去の年の需給(と概算金)の表を渡して、2026年産を予測させる。知識は使わせない。
使い方: ../.venv/bin/python run_claude_r4.py <r4a|r4b> <回数>   r4a=在庫・需要・価格の表、r4b=それに概算金を足す
"""
import json, sys
from pathlib import Path
from run_claude import HERE, P, MODEL, call
CONDS={'r4a':('history_nogaisan.md','history_nogaisan_202608.md'),'r4b':('history.md','history_202608.md')}
def build(c):
    pr,tb=CONDS[c]
    t=(P/'common.md').read_text().replace('{price_csv}',(HERE/'inputs/price_to_202608.csv').read_text())
    t+=(P/pr).read_text().replace('{history_table}',(HERE/'inputs'/tb).read_text())
    t+=(P/'no_knowledge.md').read_text()+"knowledge には「使わない」と書いてください。\n"
    return t+(P/'ask.md').read_text()
def main():
    c,n=sys.argv[1],int(sys.argv[2]); d=HERE/'runs'/c; d.mkdir(parents=True,exist_ok=True)
    prompt=build(c); (d/'prompt.txt').write_text(prompt)
    if len(sys.argv)>3: print(prompt); return
    for i in range(n):
        f=d/f'{i}.json'
        if f.exists(): continue
        ans,cost=call(prompt)
        f.write_text(json.dumps({'answer':ans,'cost_usd':cost,'model':MODEL},ensure_ascii=False,indent=1))
        print(c,i,ans['sep_oct_point'],ans['sep_oct_low80'],ans['sep_oct_high80'],cost,flush=True)
if __name__=='__main__': main()
