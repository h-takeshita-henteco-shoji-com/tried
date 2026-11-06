"""AI が MCP で LibreCAD に作図する様子を、OBS で録画しながら1回流す(#136)。

建設業の人に、AI が図面を描く様子を見せる動画の素材を作る。
採点用の記録(run_eval_mcp.py)と同じく、毎回 LibreCAD を起動し直し、図面の写しを開いてから AI を呼ぶ。

- OBS は websocket(4455)で操作する。合言葉は OBS の設定ファイルから読み、どこにも書き出さない
- 利用者の OBS の設定を変えないよう、録画用のプロファイルとシーンコレクション(tried-librecad)を作って切り替え、
  終わったら元に戻す。録画は 1920x1080、30fps。LibreCAD の窓だけを映す
- AI の出力(stream-json)は、1行ごとに録画の開始からの秒数を付けて残す。字幕を作るため
- 動画は大きいので、リポジトリに置かない(既定は ~/henrobo-video/<Issue番号>/)

使い方:
  uv run --with obsws-python --with pyobjc-framework-Quartz python code/librecad-mcp/record_run.py \\
    --drawing <図面.dxf> --prompt <指示文.txt> --model claude-opus-5-5 --out <記録のフォルダ> \\
    --view 47500,-11000,51500,-6400 [--no-record]
"""
import argparse
import datetime as dt
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from run_eval_mcp import HERE, SERVER, lc_call, librecad_alive

NAME = "tried-librecad"
SCENE = "LibreCAD"
SOURCE = "LibreCAD窓"
WIN = (0, 25, 1920, 1080)  # LibreCAD の窓の位置と大きさ(画面の点)


def obs_client():
    import obsws_python as obs
    conf = Path.home() / "Library/Application Support/obs-studio/plugin_config/obs-websocket/config.json"
    pw = json.loads(conf.read_text())["server_password"]
    return obs.ReqClient(host="localhost", port=4455, password=pw, timeout=10)


def librecad_window_id():
    """LibreCAD の一番大きい窓の番号(CGWindowID)。"""
    import Quartz
    wins = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    cands = [(w["kCGWindowBounds"]["Width"] * w["kCGWindowBounds"]["Height"], w["kCGWindowNumber"])
             for w in wins if w.get("kCGWindowOwnerName") == "LibreCAD" and w.get("kCGWindowLayer") == 0]
    if not cands:
        raise RuntimeError("LibreCAD の窓が見つかりません")
    return max(cands)[1]


def place_librecad_window():
    x, y, w, h = WIN
    subprocess.run(["osascript", "-e", f'''tell application "System Events" to tell process "LibreCAD"
  set frontmost to true
  repeat with w in windows
    if (count of (get size of w)) > 0 then
      if item 1 of (get size of w) > 600 then
        set position of w to {{{x}, {y}}}
        set size of w to {{{w}, {h}}}
      end if
    end if
  end repeat
end tell'''], check=True, capture_output=True)


def retry(fn, *args, tries=5):
    """プロファイルやシーンコレクションを作った直後は、切り替えが失敗することがある。少し待ってやり直す。"""
    for i in range(tries):
        try:
            return fn(*args)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(1.5)


class Recorder:
    """録画用のプロファイルとシーンに切り替え、終わったら元に戻す。"""

    def __init__(self, out_dir):
        self.cl = obs_client()
        self.out_dir = out_dir

    def __enter__(self):
        cl = self.cl
        self.prev_profile = cl.get_profile_list().current_profile_name
        self.prev_coll = cl.get_scene_collection_list().current_scene_collection_name
        if NAME not in cl.get_profile_list().profiles:
            cl.create_profile(NAME)
            time.sleep(2)
        if cl.get_profile_list().current_profile_name != NAME:
            retry(cl.set_current_profile, NAME)
        time.sleep(1)
        cl.set_video_settings(numerator=30, denominator=1, base_width=1920, base_height=1080,
                              out_width=1920, out_height=1080)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        cl.set_record_directory(str(self.out_dir))
        if NAME not in cl.get_scene_collection_list().scene_collections:
            cl.create_scene_collection(NAME)
            time.sleep(2)
        if cl.get_scene_collection_list().current_scene_collection_name != NAME:
            retry(cl.set_current_scene_collection, NAME)
        time.sleep(2)
        if SCENE not in [s["sceneName"] for s in cl.get_scene_list().scenes]:
            cl.create_scene(SCENE)
        cl.set_current_program_scene(SCENE)
        settings = {"type": 1, "window": librecad_window_id(), "show_cursor": False}
        if SOURCE in [i["inputName"] for i in cl.get_input_list().inputs]:
            cl.set_input_settings(SOURCE, settings, True)
        else:
            cl.create_input(SCENE, SOURCE, "screen_capture", settings, True)
        time.sleep(1)
        item = cl.get_scene_item_id(SCENE, SOURCE).scene_item_id
        # 窓を画面いっぱいに、縦横比を保って合わせる
        cl.set_scene_item_transform(SCENE, item, {"boundsType": "OBS_BOUNDS_SCALE_INNER", "boundsWidth": 1920,
                                                  "boundsHeight": 1080, "positionX": 0, "positionY": 0,
                                                  "boundsAlignment": 0})
        return self

    def start(self):
        self.cl.start_record()
        time.sleep(0.5)

    def stop(self):
        return self.cl.stop_record().output_path

    def __exit__(self, *exc):
        cl = self.cl
        try:
            if cl.get_record_status().output_active:
                cl.stop_record()
                time.sleep(1)
        finally:
            retry(cl.set_current_scene_collection, self.prev_coll)
            time.sleep(1)
            retry(cl.set_current_profile, self.prev_profile)


def claude_command(model, effort, prompt, mcp_conf):
    return ["claude", "-p", prompt, "--setting-sources", "", "--disable-slash-commands",
            "--model", model, "--effort", effort,
            "--permission-mode", "bypassPermissions", "--no-session-persistence",
            "--mcp-config", str(mcp_conf), "--strict-mcp-config",
            "--disallowedTools=WebFetch,WebSearch,Bash,Write,Edit,NotebookEdit,Glob,Grep,Agent,Workflow",
            "--output-format", "stream-json", "--verbose"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drawing", required=True, help="元の図面。写しを開く")
    ap.add_argument("--prompt", required=True, help="指示文のファイル。{file} と {changed} を置き換える")
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--out", required=True, help="記録(events.jsonl、run.json、変更後の DXF)を置くフォルダ")
    ap.add_argument("--video-dir", default=str(Path.home() / "henrobo-video/136"))
    ap.add_argument("--view", default=None, help="録画の始めに映す範囲 x0,y0,x1,y1")
    ap.add_argument("--timeout", type=int, default=3600)
    ap.add_argument("--no-record", action="store_true")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="record-run-"))
    drawing = work / "drawing.dxf"
    shutil.copy(a.drawing, drawing)
    changed = work / "drawing-changed.dxf"
    prompt = Path(a.prompt).read_text().format(file=str(drawing), changed=str(changed))
    mcp_conf = work.parent / f"{work.name}-mcp.json"
    mcp_conf.write_text(json.dumps({"mcpServers": {"librecad": {"command": "uv", "args": ["run", "-q", str(SERVER)]}}}))

    for _ in range(3):
        if subprocess.run([str(HERE / "restart.sh")], capture_output=True).returncode == 0:
            break
    else:
        raise RuntimeError("LibreCAD を起動できません")
    if not lc_call("open", path=str(drawing)).get("ok"):
        raise RuntimeError("図面を開けません")
    place_librecad_window()
    time.sleep(1)
    if a.view:
        x0, y0, x1, y1 = map(float, a.view.split(","))
        lc_call("zoom", window=[[x0, y0], [x1, y1]])

    cmd = claude_command(a.model, a.effort, prompt, mcp_conf)
    events = (out / "events.jsonl").open("w")
    rec = None if a.no_record else Recorder(Path(a.video_dir))
    video = None
    started = dt.datetime.now().astimezone()
    try:
        if rec:
            try:
                rec.__enter__()
            except Exception:
                rec.__exit__(None, None, None)
                raise
            rec.start()
        t0 = time.monotonic()
        p = subprocess.Popen(cmd, cwd=work, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        view = [[x0, y0], [x1, y1]] if a.view else None
        for line in p.stdout:
            # AI の道具が1つ終わるたびに、表示を描いている範囲に戻す。AI が全体を読むと、作図の場所が画面から外れるため。
            # plugin は命令を1つずつ処理するので、AI の命令の途中には割り込まない
            if view and '"tool_result"' in line:
                try:
                    lc_call("zoom", window=view)
                except OSError:
                    pass
            events.write(json.dumps({"t": round(time.monotonic() - t0, 2), "line": line.rstrip("\n")},
                                    ensure_ascii=False) + "\n")
            events.flush()
            if time.monotonic() - t0 > a.timeout:
                p.kill()
                break
        p.wait()
        seconds = round(time.monotonic() - t0, 1)
        time.sleep(2)  # 最後の描画を映すため
        if rec:
            video = rec.stop()
    finally:
        events.close()
        if rec:
            rec.__exit__(None, None, None)

    if changed.exists():
        shutil.copy(changed, out / "drawing-changed.dxf")
    run = {"model": a.model, "effort": a.effort, "command": cmd[:1] + ["<prompt>"] + cmd[3:],
           "prompt": prompt, "started": started.isoformat(timespec="seconds"), "seconds": seconds,
           "exit": p.returncode, "stderr": p.stderr.read(), "video": video, "librecad_alive": librecad_alive(),
           "cli_version": subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()}
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=2))
    print(json.dumps({k: run[k] for k in ("seconds", "exit", "video", "librecad_alive")}, ensure_ascii=False))
    shutil.rmtree(work, ignore_errors=True)
    mcp_conf.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
