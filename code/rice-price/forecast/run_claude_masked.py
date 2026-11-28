"""#186 段2: V5 が過去の年でも効くかを、年と品目名を伏せて確かめる。
条件 ma: 価格の表だけ(fukuoka_a と同じ文面を伏せた版)。mv: 価格・入荷量・天候の表(V5 を伏せた版)。
年は「1年目」=2010年として数える。品目は品目A〜L、地点は地点1〜7。
使い方: ../.venv/bin/python run_claude_masked.py <年...>   (各年・各条件3回。並列4本)
出力: runs/masked/<条件>_<年>/<n>.json"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd
import run_claude as rc

HERE = Path(__file__).parent
ITEMS = ["キャベツ", "はくさい", "レタス", "こまつな", "トマト", "きゅうり", "なす", "ブロッコリー", "にんじん", "ばれいしょ", "たまねぎ", "ねぎ"]
LAB = dict(zip(ITEMS, "GDKAJBHLECIF"))  # 固定の並べ替え(表の列の順も品目名の順にしない)
ST = ["福岡", "佐賀", "熊本", "大分", "軽井沢", "帯広", "網走"]
SLAB = dict(zip(ST, ["地点5", "地点2", "地点7", "地点4", "地点1", "地点6", "地点3"]))
MAP = {"キャベツ": "軽井沢", "はくさい": "軽井沢", "レタス": "軽井沢", "こまつな": "福岡", "なす": "福岡", "トマト": "熊本",
       "きゅうり": "佐賀", "ブロッコリー": "帯広", "にんじん": "帯広", "ばれいしょ": "帯広", "たまねぎ": "網走", "ねぎ": "大分"}
ORDER = sorted(ITEMS, key=lambda i: LAB[i])
KEYS = [f"{LAB[i]}_{m}" for i in ORDER for m in (7, 8, 9)]
rc.SCHEMA = {"type": "object", "properties": {"knowledge": {"type": "string"}, "reason": {"type": "string"},
             **{k: {"type": "number"} for k in KEYS}}, "required": ["knowledge", "reason", *KEYS]}

def table(name, year, cols_fn):
    d = pd.read_csv(HERE / f"inputs/{name}")
    y = d.年月.str[:4].astype(int); m = d.年月.str[5:7].astype(int)
    d = d[(y < year) | ((y == year) & (m <= 6))].copy()
    d.insert(0, "年月", [f"{yy - 2009}年目-{mm:02d}" for yy, mm in zip(y[d.index], m[d.index])], allow_duplicates=True)
    d = d.iloc[:, [0] + list(range(2, d.shape[1]))]
    return cols_fn(d).to_csv(index=False)

def items_cols(d):
    return d[["年月"] + ORDER].rename(columns=LAB)

def wx_cols(d):
    ren = {c: SLAB[c.split("_")[0]] + "_" + c.split("_")[1] for c in d.columns if c != "年月"}
    d = d.rename(columns=ren)
    return d[["年月"] + sorted([c for c in d.columns if c != "年月"])]

def build(cond, year):
    n = year - 2009
    s = (f"今日は{n}年目の6月30日です。年は伏せてあり、1年目から数えています。\n\n"
         "次の表は、日本のある中央卸売市場の野菜12品目の、月ごとの卸売価格(円/kg)です。品目名は伏せて、品目A〜Lとしています。\n"
         "出どころは農林水産省「青果物卸売市場調査」です。\n\n" + table("fukuoka_to_202606.csv", year, items_cols) + "\n")
    if cond == "mv":
        s += ("次の表は、同じ市場の同じ12品目の、月ごとの入荷量(トン)です。出どころと作り方は、価格の表と同じです。\n\n"
              + table("fukuoka_volume_to_202606.csv", year, items_cols) + "\n"
              "次の表は、気象庁の観測による、主な産地に近い7地点の月ごとの天候です。地点名は伏せています。降水量は月の合計(mm)、気温は月の平均(℃)、日照は月の合計(時間)です。\n"
              "品目と地点の対応の目安: " + "、".join(f"品目{LAB[i]}={SLAB[MAP[i]]}" for i in ORDER) + "。\n\n"
              + table("weather_to_202606.csv", year, wx_cols) + "\n")
    tabs = "上の3つの表" if cond == "mv" else "上の表"
    s += (f"\n予測には、{tabs}から読み取れることだけを使ってください。年や品目を推し量って、あなたが知っている出来事やニュースを使うことはしないでください。knowledge には「使わない」と書いてください。\n"
          f"\n問い: {n}年目の7月・8月・9月の、12品目それぞれの月ごとの卸売価格(円/kg)を予測してください。\n"
          "キーは A_7 のように「品目の記号_月」とします。\n理由を reason に、品目ごとに短く書いてください。\n")
    return s

def job(cond, year, i):
    d = HERE / "runs" / "masked" / f"{cond}_{year}"; d.mkdir(parents=True, exist_ok=True)
    p = d / f"{i}.json"
    if p.exists(): return
    pr = build(cond, year); (d / "prompt.txt").write_text(pr)
    ans, cost = rc.call(pr)
    p.write_text(json.dumps({"answer": ans, "cost_usd": cost, "model": rc.MODEL}, ensure_ascii=False, indent=1))
    print(cond, year, i, cost, flush=True)

if __name__ == "__main__":
    years = [int(a) for a in sys.argv[1:]]
    if years == [0]:  # 文面の確認だけ
        print(build("mv", 2019)[:1500]); print(build("mv", 2019)[-900:]); sys.exit()
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(lambda a: job(*a), [(c, y, i) for y in years for c in ("ma", "mv") for i in range(3)]))
