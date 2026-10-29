#!/bin/zsh
# 1か月の終わりの手順をまとめる(#124): 録画を止め、後処理をして、次の月の状態と録画を用意する。
# 使い方: finish_council_month.sh <月> <Workflow の run id(wf_...)> <task id> [--last]
set -e
month="$1"; wf="$2"; task="$3"
root="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$root"
run=$(ls -d "$root"/2026/10-27-*-03-*決める | head -1)
wfdir=$(ls -d /Users/takeshita/.claude/projects/*/*/subagents/workflows/$wf | head -1)
out=$(ls /private/tmp/claude-501/*/*/tasks/$task.output | head -1)
uv run --with obsws-python --with pillow python code/ai-mayor/tools/obs_record.py stop 2>&1 | tail -1
python3 code/ai-mayor/tools/post_council_month.py "$run" "$month" "$wfdir" "$out"
if [ "$4" != "--last" ]; then
  next=$((month + 1))
  python3 -c 'import json,sys; json.dump({"runDir": sys.argv[1], "month": int(sys.argv[2]), "advanced": False}, open(sys.argv[3], "w"))' "$run" "$next" ~/.cache/ai-mayor/council-current.json
  uv run --with obsws-python --with pillow python code/ai-mayor/tools/obs_record.py start ~/ai-mayor-recordings/council 2>&1 | tail -1
fi
