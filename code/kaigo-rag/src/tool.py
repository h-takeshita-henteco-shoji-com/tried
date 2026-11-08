"""エージェントが Bash から呼ぶ道具。標準ライブラリだけで、server.py に問い合わせる。

  python3 tool.py search "検索語"   検索(上位8件)
  python3 tool.py read 1234         チャンクの全文
  python3 tool.py tree [n12]        目次の1段(省略すると資料の一覧)
  python3 tool.py related 1234      チャンクの用語と参照先(GraphRAG)
  python3 tool.py related 用語       その用語を含むチャンク
環境変数 KAIGO_EXCLUDE: 隠すチャンク id(カンマ区切り)
"""
import json
import os
import sys
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8765"


def get(path, exclude=None, **q):
    ex = os.environ.get("KAIGO_EXCLUDE", "") if exclude is None else ",".join(map(str, exclude))
    req = urllib.request.Request(f"{BASE}{path}?{urllib.parse.urlencode(q)}", headers={"X-Exclude": ex})
    return json.load(urllib.request.urlopen(req, timeout=120))


def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "search":
        for r in get("/search", q=" ".join(args)):
            print(f"[{r['id']}] {r['doc']} > {r['path']}\n{r['text']}\n")
    elif cmd == "read":
        for a in args:
            r = get("/read", id=a)
            print(f"[{a}] {r.get('doc', '')} > {r.get('path', '')}\n{r.get('text', r.get('error'))}\n")
    elif cmd == "tree":
        r = get("/tree", node=args[0] if args else "root")
        if "error" in r:
            print(r["error"])
            return
        print(f"{r['node']}: {r['title']}")
        for c in r["children"]:
            print(f"  {c['node']}  {c['title'][:80]}  ({c['chunks']}件)")
        for c in r["chunks"]:
            print(f"  [{c['id']}] {c['head']}")
    elif cmd == "related":
        r = get("/related", x=" ".join(args))
        if "entities" in r:
            print("用語(括弧はその用語を含むチャンクの数):", "、".join(f"{e['name']}({e['chunks']})" for e in r["entities"]))
            for f in r["refs"]:
                print(f"  {f['kind']} → [{f['id']}] {f['doc']} > {f['path'][:80]}")
        else:
            print(f"用語「{r['entity']}」を含むチャンク: {r['count']}件(先頭30件)")
            for c in r["chunks"]:
                print(f"  [{c['id']}] {c['doc']} > {c['path'][:60]} | {c['head']}")
    else:
        print("usage: tool.py search|read|tree|related ...")


if __name__ == "__main__":
    main()
