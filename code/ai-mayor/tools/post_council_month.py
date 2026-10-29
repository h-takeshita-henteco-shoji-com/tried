"""1か月の運営が終わったあとの後処理を、まとめて行う(#124)。

Workflow の返り値を m<月>-run.json に書き、会話の記録を抜き出し、月の終わりの確かめ、台帳、議事録を作り、
段の数・圧縮の回数・最大の文脈を表示する。commit と push はしない。

    python3 code/ai-mayor/tools/post_council_month.py <運営のフォルダ> <月> <Workflow の記録のフォルダ> <返り値の .output ファイル>
"""
import glob
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
STAGE = {"見る": "mayor-desk-see", "まとめ": "mayor-desk", "再まとめ": "mayor-desk-rebill", "直す": "mayor-desk-fix",
         "計画の調整": "mayor-desk-planadj", "議会": "assembly", "議会2": "assembly-2", "実行": "mayor-field"}


def name_of(label):
    head, *rest = label.split()
    if head == "案":
        return rest[0]
    if head == "再調査":
        return rest[0] + "-recheck"
    if head == "是正":
        return f"{rest[0]}-fix{rest[1].replace('回目', '')}"
    if head == "計画のレビュー":
        return f"mayor-desk-review{rest[0].replace('回目', '')}"
    return STAGE.get(head, head)


def main():
    run_dir, month, wf_dir, out_file = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    mm = f"{month:02d}"
    d = json.load(open(out_file))
    res = d["result"]
    pathlib.Path(run_dir, "council").mkdir(exist_ok=True)
    json.dump(res, open(f"{run_dir}/council/m{mm}-run.json", "w"), ensure_ascii=False, indent=2)
    print("stoppedAt", res.get("stoppedAt"), "stop", (res.get("done") or {}).get("stop"))
    pathlib.Path(run_dir, "transcripts").mkdir(exist_ok=True)
    agents = 0
    for line in open(f"{wf_dir}/journal.jsonl"):
        x = json.loads(line)
        if x.get("type") == "started":
            agents += 1
            r = subprocess.run(["python3", "code/ai-mayor/tools/extract_transcript.py", x["agentId"],
                                f"{run_dir}/transcripts/m{mm}-{name_of(x['label'])}.md", "--dir", wf_dir,
                                "--raw-dir", str(pathlib.Path.home() / "ai-mayor-transcripts/council")],
                               capture_output=True, text=True, cwd=ROOT)
            if r.returncode:
                print("extract NG", x["label"], r.stderr[:80])
    for t in ("check_council_month.py", "make_council_ledger.py", "make_council_minutes.py"):
        r = subprocess.run(["python3", f"code/ai-mayor/tools/{t}", run_dir, str(month)], capture_output=True, text=True, cwd=ROOT)
        if t == "check_council_month.py":
            print("\n".join(r.stdout.splitlines()[:10]))
        else:
            print(t, r.returncode, (r.stdout + r.stderr).strip()[-160:])
    comp, mx = 0, {}
    for f in glob.glob(wf_dir + "/agent-*.jsonl"):
        agent = json.load(open(f[:-6] + ".meta.json"))["agentType"].replace("council-", "")
        for line in open(f):
            if '"compact_boundary"' in line:
                comp += 1
            try:
                m = json.loads(line).get("message")
            except ValueError:
                continue
            u = m.get("usage") if isinstance(m, dict) else None
            if u:
                mx[agent] = max(mx.get(agent, 0), u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0))
    print("agents", agents, "compactions", comp, "最大文脈", sorted(mx.items(), key=lambda a: -a[1])[:3])


if __name__ == "__main__":
    main()
