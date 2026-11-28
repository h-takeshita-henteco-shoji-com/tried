"""農林水産省「野菜の生育状況及び価格見通し」を品目×月の表にする。

使い方 (PDF は信頼できないデータなので -I を付けて実行する):
  python3 -I maff_outlook_parse.py download   # 一覧から PDF を取得 (1.5秒間隔)
  python3 -I maff_outlook_parse.py parse      # PDF を読んで CSV を書く
"""
import csv
import json
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAW = BASE / "data" / "raw_maff_outlook"
OUT = BASE / "data" / "maff_veg_outlook.csv"
INDEX_URL = "https://www.maff.go.jp/j/seisan/ryutu/yasai_zyukyu/index.html"
UA = {"User-Agent": "Mozilla/5.0 (research; rice-price)"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def era_to_year(era, y):
    y = 1 if y == "元" else int(y)
    return {"平成": 1988, "令和": 2018}[era] + y


def list_links():
    html = fetch(INDEX_URL).decode("utf-8", "replace")
    s = html.find("1．野菜の生育状況")
    e = html.find("<h2", s + 10)
    sec = html[s:e]
    out = []
    for m in re.finditer(r'href="([^"]+\.pdf)"[^>]*>(.*?)</a>', sec, re.S):
        href, text = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        text = unicodedata.normalize("NFKC", text)
        mm = re.search(r"(平成|令和)(元|\d+)年(\d+)月(後半)?", text)
        if not mm or "生育状況及び価格見通し" not in text:
            continue
        y = era_to_year(mm.group(1), mm.group(2))
        mo = int(mm.group(3))
        if not (2016 <= y <= 2026):
            continue
        out.append({"year": y, "month": mo, "label": text.strip(),
                    "url": urllib.parse.urljoin(INDEX_URL, href)})
    return out


def download():
    RAW.mkdir(parents=True, exist_ok=True)
    links = list_links()
    (RAW / "links.json").write_text(json.dumps(links, ensure_ascii=False, indent=1))
    for L in links:
        fn = RAW / f"{L['year']}-{L['month']:02d}.pdf"
        if fn.exists():
            continue
        try:
            fn.write_bytes(fetch(L["url"]))
            print("ok", fn.name)
        except Exception as ex:  # noqa
            print("NG", fn.name, L["url"], ex)
        time.sleep(1.5)


# ---------------------------------------------------------------- 読み取り

WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>')
PAGE_RE = re.compile(r"<page [^>]*>(.*?)</page>", re.S)
KANA_RE = re.compile(r"^[ぁ-んァ-ヶー・\s]+$")
PRICE_WORD_RE = re.compile(
    r"平年|水準|推移|で推|^移$|回復|戻る|^[<〈＜].*[>〉＞]$|上回|下回|高値|安値|^る$|^み$|並み")
PERIODS = ["上旬", "中旬", "下旬", "前半", "後半"]


def nfkc(s):
    return unicodedata.normalize("NFKC", s)


def words_by_page(pdf):
    out = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"],
                         capture_output=True, check=True).stdout.decode("utf-8", "replace")
    pages = []
    for pg in PAGE_RE.findall(out):
        ws = []
        for m in WORD_RE.finditer(pg):
            x0, y0, x1, y1 = map(float, m.groups()[:4])
            t = nfkc(m.group(5)).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
            if t.strip():
                ws.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1, "t": t})
        pages.append(ws)
    return pages


HEAD_RE = re.compile(r"主産地|書き|入荷|シェ|^ア$|品目|^目$|今後|見通し|平年|平均|比\)|前半|後半|上旬|中旬|下旬"
                     r"|\d+年|\d+月|^\(|※|^[今後の生育及び出荷見通し品目]$")


def find_header(ws):
    """各論の表の見出しを探す。列の境目を返す。"""
    for an in [w for w in ws if w["t"].replace(" ", "") == "主産地"]:
        hm = [w for w in ws if w["t"].replace(" ", "") in ("品目", "目")
              and -10 < w["y0"] - an["y0"] < 60 and w["x1"] < an["x0"] + 5]
        ph = [w for w in ws if ("価格見通し" in w["t"] or "価格の見通し" in w["t"])
              and abs(w["y0"] - an["y0"]) < 60 and w["x0"] > an["x1"] + 100]
        if not hm or not ph:
            continue
        ph = ph[0]
        near = [w for w in ws if -30 < w["y0"] - an["y0"] < 72 and len(w["t"]) <= 22
                and HEAD_RE.search(w["t"]) and not re.search(r"並み|推移|水準|%\)", w["t"])]
        ytop = max(w["y1"] for w in near)
        pgroup = [w for w in near if w["x0"] > ph["x0"] - 60 and "生育" not in w["t"]
                  and "見通し" not in w["t"].replace("価格見通し", "")
                  and not re.fullmatch(r"[ぁ-んァ-ヶ一-龥]", w["t"])] or [ph]
        sub = [w for w in pgroup if re.search(r"\d+月(前半|後半|上旬|中旬|下旬)$", w["t"])]
        px = min(w["x0"] for w in pgroup) - 15
        share_x = max(w["x1"] for w in hm) + 3
        return {"share_x": share_x, "price_x": px, "ytop": ytop,
                "sub": sorted(sub, key=lambda w: w["x0"]),
                "head_text": "".join(w["t"] for w in pgroup)}
    return None


def parse_pdf(pdf):
    pages = words_by_page(pdf)
    hdr = None
    rows = []  # {item, yc, page, desc[], price[], share[]}
    definition = ""
    done = False
    for pi, ws in enumerate(pages):
        alltxt = "".join(w["t"] for w in ws).replace(" ", "")
        m = re.search(r"「平年並み」とは、?(.*?)(?:であること|。)", alltxt)
        if m:
            definition = m.group(1)
        if done:
            continue
        h = find_header(ws)
        if h:
            hdr = h
            body = [w for w in ws if w["y0"] > h["ytop"]]
        elif hdr:
            body = ws
        else:
            continue
        # 表の終わり (注 / 添付資料)
        ends = [w["y0"] for w in body if re.match(r"^(注|<添付|〈添付|\(参考\)|これまでの公表)", w["t"])
                and w["x0"] < hdr["share_x"] + 30]
        yend = min(ends) if ends else 1e9
        if ends and rows or (ends and h):
            done = True
        body = [w for w in body if w["y0"] < yend
                and not re.fullmatch(r"\(?\d+/\d+\)?|-\d+-", w["t"].replace(" ", ""))]
        longw = [w["x0"] for w in body if len(w["t"]) >= 12
                 and hdr["share_x"] + 20 < w["x0"] < hdr["price_x"]]
        if longw:
            hdr["desc_x"] = min(longw) - 3
        items = []
        for w in body:
            if w["x0"] < hdr["share_x"]:
                mm = re.match(r"^([ぁ-んァ-ヶー\s]+)", w["t"])
                if mm:
                    items.append({"t": mm.group(1).replace(" ", ""), "x0": w["x0"],
                                  "y0": w["y0"], "y1": w["y1"]})
        items.sort(key=lambda w: (round(w["y0"]), w["x0"]))
        merged = []
        for it in items:
            if merged and it["y0"] - merged[-1]["y1"] < 6:
                merged[-1]["t"] += it["t"]
                merged[-1]["y1"] = max(it["y1"], merged[-1]["y1"])
            else:
                merged.append(dict(it))
        others = sorted([w for w in body if w["x0"] >= hdr["share_x"]], key=lambda w: w["y0"])
        if not merged:
            if rows:
                for w in others:
                    put(rows[-1], w, hdr)
            continue
        page_rows = [{"item": it["t"], "yc": (it["y0"] + it["y1"]) / 2, "page": pi,
                      "desc": [], "price": [], "share": []} for it in merged]
        blocks = []
        for w in others:
            if blocks and w["y0"] - blocks[-1]["y1"] < 9:
                blocks[-1]["ws"].append(w)
                blocks[-1]["y1"] = max(blocks[-1]["y1"], w["y1"])
            else:
                blocks.append({"ws": [w], "y0": w["y0"], "y1": w["y1"]})
        for b in blocks:
            inside = [r for r in page_rows if b["y0"] - 3 <= r["yc"] <= b["y1"] + 3]
            for w in b["ws"]:
                if len(inside) == 1:
                    tgt = inside[0]
                elif inside:
                    tgt = min(inside, key=lambda r: abs(r["yc"] - (w["y0"] + w["y1"]) / 2))
                else:
                    bc = (b["y0"] + b["y1"]) / 2
                    tgt = min(page_rows, key=lambda r: abs(r["yc"] - bc))
                    # ページ先頭で品目より上にあるまとまりは、前ページの行の続き
                    if rows and b["y1"] < page_rows[0]["yc"] - 40 and h is None:
                        tgt = rows[-1]
                put(tgt, w, hdr)
        rows.extend(page_rows)
    return hdr, rows, definition


def put(row, w, hdr):
    t = w["t"]
    if w["x0"] >= hdr["price_x"]:
        row["price"].append(w)
    elif w["x0"] < hdr.get("desc_x", hdr["share_x"] + 40):
        row["share"].append(w)
    else:
        row["desc"].append(w)


# ---------------------------------------------------------------- 区分の言葉

def score_word(s):
    """区分の言葉を点に直す。(点, 一致したか)"""
    s = s.replace(" ", "")
    if not s:
        return None, False
    if re.search(r"平年並", s) and not re.search(r"上回|下回|多|少|高値|安値", s):
        return 0, True
    sl = "やや" in s or "わずかに" in s
    if s == "平年で":
        return 0, False
    if re.search(r"大幅に上回|大きく上回", s):
        return 2, False
    if re.search(r"大幅に下回|大きく下回", s):
        return -2, False
    if "上回" in s:
        return (1 if sl else 2), True
    if "下回" in s:
        return (-1 if sl else -2), True
    if "高値" in s and "回復" in s:
        return 1, False
    if "安値" in s and "回復" in s:
        return -1, False
    if "高値" in s:
        return 2, False
    if "安値" in s:
        return -2, False
    if re.search(r"増加|減少", s):  # 平年との比較ではない言い方は弱めに当てる
        return (1 if "増加" in s else -1), False
    if re.search(r"多い|多く|潤沢", s):
        return (1 if sl else 2), False
    if re.search(r"少な", s):
        return (-1 if sl else -2), False
    return None, False


def clean_price(txt):
    t = txt.replace(" ", "")
    t = re.sub(r"\(\d+/\d+\)|-\d+-", "", t)
    t = re.sub(r"[<〈＜>〉＞]", "", t)
    return t


def price_by_period(row, hdr, target_m, whole_label):
    ps = sorted(row["price"], key=lambda w: (round(w["y0"] / 4), w["x0"]))
    if not ps:
        return {}
    sub = hdr["sub"]
    if len(sub) >= 2:
        res = {}
        bounds = [(sub[i]["x0"] + sub[i + 1]["x0"]) / 2 for i in range(len(sub) - 1)]
        for w in ps:
            k = sum(1 for b in bounds if (w["x0"] + w["x1"]) / 2 > b + 5)
            per = re.search(r"(前半|後半|上旬|中旬|下旬)", sub[k]["t"]).group(1)
            res.setdefault(per, []).append(w)
        return {k: clean_price("".join(w["t"] for w in sorted(v, key=lambda w: w["y0"])))
                for k, v in res.items()}
    ps = sorted(ps, key=lambda w: (w["y0"], w["x0"]))
    txt = "".join(w["t"] for w in ps).replace(" ", "")
    parts = re.split(r"[<〈＜]\s*(?:\d+月)?(前半|後半|上旬|中旬|下旬|上中旬|中下旬)\s*[>〉＞]", txt)
    if len(parts) > 1:
        res = {}
        for i in range(1, len(parts), 2):
            res[parts[i]] = clean_price(parts[i + 1])
        return res
    return {whole_label: clean_price(txt)}


QTY_RE = re.compile(
    r"(?:(\d+)月(上中旬|中下旬|前半|後半|上旬|中旬|下旬)?(?:までは|については|の|も|は)?)?"
    r"(?:出荷|入荷)(?:数量|数要|量)"
    r"(?P<conn>全体では|[、・]価格は?とも(?:に)?|(?:及び|並びに)価格は、?(?:総じて|ともに)?|[、・]価格は?|は総じて|は|が|も)?"
    r"(?P<cmp>(?:概ね|やや|わずかに|大幅に|大きく)?(?:平年を?(?:やや|わずかに|大幅に|大きく)?"
    r"(?:上回|下回)|平年並み|多(?:い|く)|少な(?:い|く)|潤沢|増加|減少|平年で))")


def norm_cmp(c):
    c = c.replace(" ", "")
    if c.endswith(("上回", "下回")):
        c += "る"
    c = re.sub(r"^平年(?=やや|上回|下回)", "平年を", c)
    c = re.sub(r"(多|少な)く$", r"\1い", c)
    return c


def qty_by_period(desc, target_m, whole_label, prev_m):
    """説明文から数量の見通しを期間ごとに取る。"""
    txt = desc.replace(" ", "").replace("\n", "")
    sents = [s for s in re.split(r"(?<=。)", txt) if s]
    found = {}  # period -> list of (cmp, priority)
    for s in sents:
        if s.startswith(("・前月は", "前月は")):
            continue
        prio = 2 if "全体として" in s else 1
        for m in QTY_RE.finditer(s):
            mo, per = m.group(1), m.group(2)
            explicit = mo is not None
            before, after = s[max(0, m.start() - 10):m.start()], s[m.end():m.end() + 8]
            if "平年の" in before or re.match(r"(状態|状況)が解消", after):
                continue  # 季節の一般論や、多い状態の解消
            local = bool(re.search(r"(産|県)の$", before[-4:]))
            if mo is None:
                # 同じ文の中で直前の節が「◯月(前半)は」で始まれば、それを使う
                pre = s[:m.start()].split("、")
                for seg in reversed(pre[-3:]):
                    mm = re.match(r"^・?(\d+)月(上中旬|中下旬|前半|後半|上旬|中旬|下旬)?(?:までは|については|は|も|に)", seg)
                    if mm:
                        mo, per = mm.group(1), mm.group(2)
                        break
            if mo is None:
                # 文頭の主題「◯月(前半)は/も」を月とみなす
                tm = re.match(r"^・?(?:また、|なお、|このため、|これらのことから、|全体として、|一方、)?"
                              r"(\d+)月(上中旬|中下旬|前半|後半|上旬|中旬|下旬)?(?:までは|については|は|も|、)", s)
                if tm:
                    mo, per = tm.group(1), tm.group(2)
            if mo is None:
                # 後ろに「◯月前半の価格は」などが続けば、その期間とみなす
                am = re.match(r"[^。]*?ため、(\d+)月(前半|後半|上旬|中旬|下旬)(?:の|も|は)", s[m.end():])
                if am:
                    mo, per = am.group(1), am.group(2)
            if mo is not None and int(mo) != target_m:
                continue
            if mo is None and "見込" not in s[m.start():] and "見込" not in s:
                continue
            per = per or whole_label
            if per in ("上中旬", "中下旬"):
                pass
            if local:
                prio = 0  # 産地別の記述は、全体の記述がないときだけ使う
            found.setdefault(per, []).append((norm_cmp(m.group("cmp")), prio + (0.5 if explicit else 0)))
    res = {}
    for per, lst in found.items():
        top = max(p for _, p in lst)
        if top < 1:
            res[per] = ("", ["産地別の記述のみ"])
            continue
        vals = [c for c, p in lst if p == top]
        res[per] = (vals[-1], sorted(set(c for c, _ in lst)))
    return res


def row_desc(r):
    ws = sorted(r["desc"], key=lambda w: (round(w["y0"] / 3), w["x0"]))
    t = "".join(w["t"] for w in ws).replace(" ", "")
    return re.sub(r"\(\d+/\d+\)|-\d+-", "", t)


def parse_all():
    links = json.loads((RAW / "links.json").read_text())
    out_rows = []
    defs = {}
    diag = []
    for L in sorted(links, key=lambda l: (l["year"], l["month"])):
        y, mo = L["year"], L["month"]
        pdf = RAW / f"{y}-{mo:02d}.pdf"
        if not pdf.exists():
            continue
        hdr, rows, definition = parse_pdf(pdf)
        defs[f"{y}-{mo:02d}"] = definition
        whole = "後半" if "後半" in L["label"] else "全体"
        prev_m = 12 if mo == 1 else mo - 1
        pub = pub_date(pdf, L["url"], y, mo)
        if hdr is None or not rows:
            diag.append((y, mo, "表なし"))
            continue
        for r in rows:
            desc = row_desc(r)
            pr = price_by_period(r, hdr, mo, whole)
            qt = qty_by_period(desc, mo, whole, prev_m)
            if whole == "後半":
                qt = {k: v for k, v in qt.items() if k == "後半"} or (
                    {"後半": qt["全体"]} if "全体" in qt else {})
            # 行の期間は価格の欄に合わせる。数量だけ前半・後半が両方あれば分ける
            pers = [p for p in PERIODS if p in pr]
            if not pers:
                if whole not in qt and "前半" in qt and "後半" in qt:
                    pers = ["前半", "後半"]
                else:
                    pers = [whole]
            for per in pers:
                notes = []
                pw = pr.get(per, pr.get(whole, pr.get("全体", "")))
                qv = qt.get(per) or qt.get(whole) or qt.get("全体")
                if not qv and per in ("全体", whole):
                    part = [k for k in PERIODS if k in qt and k != per]
                    if part:
                        qv = qt[part[0]]
                        notes.append(f"数量は{mo}月{part[0]}の記述のみ")
                qw = qv[0] if qv else ""
                if qv and qv[1] == ["産地別の記述のみ"]:
                    notes.append("数量は産地別の記述のみ")
                elif qv and len(qv[1]) > 1:
                    notes.append("数量の記述が複数(" + "/".join(qv[1]) + ")")
                ps, pok = score_word(pw)
                qs, qok = score_word(qw)
                if pw and not pok:
                    notes.append(f"価格の原文「{pw}」を近い区分に当てた")
                if qw and not qok:
                    notes.append(f"数量の原文「{qw}」を近い区分に当てた")
                if not pw:
                    notes.append("価格の区分なし")
                if not qw and not (qv and qv[1] == ["産地別の記述のみ"]):
                    notes.append("数量の記述なし")
                if not pub:
                    notes.append("公表日の記載なし")
                out_rows.append({
                    "対象年": y, "対象月": mo, "公表日": pub, "品目": r["item"],
                    "期間": per, "数量の区分": qw, "数量_点": "" if qs is None else qs,
                    "価格の区分": pw, "価格_点": "" if ps is None else ps,
                    "出典URL": L["url"], "備考": "; ".join(notes)})
    return out_rows, defs, diag


def pub_date(pdf, url, ty, tm):
    """公表日。PDF の日付、なければ URL の日付(YYMMDD)。どちらもなければ空。"""
    out = subprocess.run(["pdftotext", "-l", "1", str(pdf), "-"], capture_output=True).stdout
    t = nfkc(out.decode("utf-8", "replace")).replace(" ", "")
    m = re.search(r"(平成|令和)(元|\d+)?年(\d+)月(\d+)日", t)
    if m:
        mo, d = int(m.group(3)), int(m.group(4))
        if m.group(2):
            y = era_to_year(m.group(1), m.group(2))
        else:  # 年の数字が抜けている資料は、対象月から年を決める
            y = ty if mo <= tm else ty - 1
        return f"{y}-{mo:02d}-{d:02d}"
    m = re.search(r"/(\d{2})(\d{2})(\d{2})_yasai", url)
    if m:
        return f"20{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return ""


def write_csv(rows):
    cols = ["対象年", "対象月", "公表日", "品目", "期間", "数量の区分", "数量_点",
            "価格の区分", "価格_点", "出典URL", "備考"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "parse"
    if cmd == "download":
        download()
    elif cmd == "missing":  # 数量が取れなかった行の説明文を見る
        rows = list(csv.DictReader(open(OUT, encoding="utf-8")))
        cache = {}
        for r in rows:
            if r["数量の区分"] or "数量" not in r["備考"]:
                continue
            key = (int(r["対象年"]), int(r["対象月"]))
            if key not in cache:
                cache[key] = parse_pdf(RAW / f"{key[0]}-{key[1]:02d}.pdf")[1]
            for rr in cache[key]:
                if rr["item"] == r["品目"]:
                    print(key, r["品目"], r["期間"], "|", row_desc(rr)[:300])
    elif cmd == "dump":  # 1件の読み取り結果を確かめる
        hdr, rows, d = parse_pdf(Path(sys.argv[2]))
        print(hdr and {k: v for k, v in hdr.items() if k != "sub"}, [s["t"] for s in hdr["sub"]] if hdr else None)
        for r in rows:
            print("##", r["item"], "| P:", " ".join(w["t"] for w in r["price"]))
            print("   D:", row_desc(r)[:400])
    else:
        rows, defs, diag = parse_all()
        write_csv(rows)
        print("rows", len(rows), "diag", diag)
        print(json.dumps(defs, ensure_ascii=False))
