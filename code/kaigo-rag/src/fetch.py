"""原文を data/raw に取る。Q&A集(Excel)と、全老健の法令検索の本文。"""
import html
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw"
UA = {"User-Agent": "Mozilla/5.0 (kaigo-rag research)"}
QA_XLSX = "https://www.mhlw.go.jp/content/12300000/001751835.xlsx"
ROKEN_UIDS = [11, 22, 14, 6, 19, 17]


def get(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def to_text(t: str) -> str:
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    t = re.sub(r"[ \t　]+\n", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "qa_all.xlsx").write_bytes(get(QA_XLSX))
    for uid in ROKEN_UIDS:
        t = get(f"https://hourei.roken.or.jp/detail.php?uid={uid}").decode("utf-8", "replace")
        (RAW / f"roken_{uid}.txt").write_text(to_text(t))
        time.sleep(1)
    print("ok")


if __name__ == "__main__":
    main()
