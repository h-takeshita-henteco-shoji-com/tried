"""動画を YouTube に上げ、タイトル・説明・サムネイルを付ける(#106)。

YouTube Data API(プログラムから YouTube を操作する窓口)を使う。chrome-devtools の Chrome では
Google にログインできなかったため、cutout-chronicles と同じ許可のしるしを使う(同じチャンネル)。
許可のしるしは ~/.config/cutout-chronicles/youtube/token.json。リポジトリには入れない。

設定は #98 の動画にそろえる: カテゴリ 20(ゲーム)、言語 ja、子ども向けではない。
公開は記事と同時に人が決めるので、ここでは非公開(private)で上げる。

使い方:
  uv run --with google-auth --with google-api-python-client python assets/scripts/youtube_upload.py
  uv run ... youtube_upload.py --update <動画ID>   タイトルと説明だけ送り直す(記事の URL を入れたあとなど)
文面は youtube.md から読む。記事の URL がまだ「(URL)」のときは、その行を外す。
"""
import os
import re
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

DAY = Path(__file__).resolve().parents[2]
VIDEO = Path.home() / "ai-mayor-recordings/numedon2/numedon-2runs.mp4"
THUMB = DAY / "assets/thumbnail.jpg"
TOKEN = Path.home() / ".config/cutout-chronicles/youtube/token.json"


def texts():
    s = (DAY / "youtube.md").read_text(encoding="utf-8")
    sec = lambda name: s.split(f"## {name}\n", 1)[1].split("\n## ", 1)[0].strip()
    title = sec("タイトル")
    desc = "\n".join(l for l in sec("説明").splitlines() if "(URL)" not in l)
    desc = re.sub(r"\n{3,}", "\n\n", desc)
    tags = [t.strip() for t in sec("タグ").split(",") if t.strip()]
    return title, desc, tags


def youtube():
    c = Credentials.from_authorized_user_file(str(TOKEN))
    if not c.valid:
        c.refresh(Request())
    return build("youtube", "v3", credentials=c)


def main():
    title, desc, tags = texts()
    yt = youtube()
    snippet = {"title": title, "description": desc, "tags": tags, "categoryId": "20",
               "defaultLanguage": "ja", "defaultAudioLanguage": "ja"}
    if len(sys.argv) > 2 and sys.argv[1] == "--update":
        vid = sys.argv[2]
        yt.videos().update(part="snippet", body={"id": vid, "snippet": snippet}).execute()
        print("updated", vid)
        return
    body = {"snippet": snippet, "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}}
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(VIDEO), chunksize=16 * 1024 * 1024, resumable=True))
    res = None
    while res is None:
        status, res = req.next_chunk()
        if status:
            print(f"送信中 {status.progress() * 100:.0f}%", flush=True)
    vid = res["id"]
    print("uploaded", vid, f"https://youtu.be/{vid}")
    yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(THUMB), mimetype="image/jpeg")).execute()
    print("thumbnail set")


if __name__ == "__main__":
    main()
