# 市役所と議会のハーネス 受け渡しの形

`council-design.md` の部品どうしの約束です。2026-10-24(#100)に決めました。部品を作る人は、この形に合わせます。
形を変えるときは、この文書を先に直します。

## 1. 名前

### 局の英字の名前

| 局 | 名前 |
|---|---|
| 財政局 | `finance` |
| 住宅都市みどり局 | `urban` |
| 道路下水道局 | `roads` |
| 港湾空港局 | `port` |
| 経済観光文化局 | `economy` |
| 保健環境局 | `health` |
| 教育委員会 | `education` |
| 消防局 | `fire` |

案を出す局は `finance` を除く7つ。並びは上の表のとおり。

### サブエージェントの定義(`.claude/agents/`)

| 定義の名前(agentType) | 元 |
|---|---|
| `council-urban` ほか7つ(`council-<局>`) | 雛形 `council-agents/bureau.md` + `bureaus/<局>.md` + `city-plan.md` |
| `council-finance` | 雛形 `council-agents/finance.md` + `bureaus/finance.md` + `city-plan.md` |
| `council-assembly` | 雛形 `council-agents/assembly.md` + `city-plan.md` |
| `council-mayor-desk` | 雛形 `council-agents/mayor-desk.md` + `mayors/plan.md` + `city-plan.md` |
| `council-mayor-field` | 雛形 `council-agents/mayor-field.md` + `mayors/plan.md` + `city-plan.md` |

作るのは `code/ai-mayor/tools/make_council_agents.py`(`make_mayor_agents.py` と同じ作り。`--check` を持つ)。

## 2. 運営のフォルダ

```
<運営のフォルダ>/
  mayor-note.md
  command-log.txt
  assets/
  transcripts/m<月2桁>-<役>.md          役: mayor-desk、mayor-field、finance、assembly、<局>
  council/
    m01-policy.md        見てまとめる市長(編成方針)
    m01-guide.md         財政局(予算編成要領)
    m01-<局>.md          7つの局の案
    m01-finance.md       財政局(査定調書)
    m01-bill.md          見てまとめる市長(まとめと議案)。直したら m01-bill-2.md
    m01-assembly.md      議会の判断。2回目は m01-assembly-2.md
    m01-assembly.json    議会の判断(hooks が読む)。2回目があれば上書きする
    m01-survey-<局>.md   局の調査の結果(実行する市長が見回りと月末に書く。#105 の作り直し)
    m01-hooks.log        hooks の記録
    m01-run.json         Workflow の返り値をそのまま写したもの(親の手順が書く)
    m01-minutes.md       議事録(make_council_minutes.py)
    ledger.jsonl         台帳(make_council_ledger.py)
```

月は2桁(`m01`〜`m12`)。

採択理由を読み取れるよう、`m<月>-bill.md` の各施策には次の2欄を置く。
修正後の `m<月>-bill-2.md` も同じ形にする。

- 採択理由: 確認した数値や条件を挙げ、どの問題に効くと判断したか。1〜2文
- 今月選んだ理由: ほかの案より優先した理由。緊急性、費用、今月の重点など。1〜2文

公約とのつながりや予想とは別の欄にする。
末尾の「判断の根拠」だけで済ませない。

局の案には「ほかの局への響き」の欄を設けない。
各局は、費用と操作の上限の範囲で担当の問題に集中する。
各局は、提案前に `list_policies` で政策一覧を取得する。
政策名、有効状態、週の費用を確認し、担当に関係する政策もほかの手段と比べる。
取得結果は「見たもの」に記録し、取得できなければ未確認と書く。
政策の効果の説明は追加しない。
市長が各案の他局への影響を評価し、採否を決める。
採った案の影響は、まとめと議案の各施策に記録する。

局の案の「目標の数字」は「期待する効果」に置き換える。
改善の見込み、数値と期限、確認方法、不確かな点を記録する。
確認方法には道具と項目、対象の施設・地区・範囲を書く。
数値を見積もれなければ、その旨と確認する変化・期限を書く。
市長は、採った案の予測と確認方法を議案と市政ノートに引き継ぐ。
政策一覧にゲームの効果の説明は追加しない。

前月の非採択や他局の優先順位だけを、案なしの理由にしない。
当月も有効なら同じ案を再提出できる。

局の案には「実行計画」を必須の欄として置く。
実行計画の「実行可否」は、確認済み / 未確認 / 案なしを明記する。
建設は1棟ごとの座標・向き・種類と、設置条件の確認結果を書く。
接続工事も操作と費用に含める。
建設以外も、対象と変更値、道具の引数を書く。
市長は、採った対象の実行計画を議案に引き継ぐ。
実行役は最終確認と操作を行い、新しい候補地を探さない。
条件が違えば、記載された予備候補以外は使わず、見送る。
部分実行は成功済みと未実行を分け、施策の id を `failed` に入れる。

## 3. hooks が読む状態のファイル

`~/.cache/ai-mayor/council-current.json`

```json
{"runDir": "/abs/path/to/run", "month": 3, "advanced": false}
```

- `runDir` と `month` は、親の手順(`/council-month`)が Workflow の前に書く。`advanced` は false にする
- `advanced` は、`advance` の後の hook が true にする

## 4. 議決が要る道具

| 種類 | 道具(MCP の名前は `mcp__cities-skylines__` + これ) |
|---|---|
| 税 | `set_tax` |
| 予算 | `set_budget`、`set_transport_line_budget` |
| 融資 | `take_loan` |
| 取り壊し | `bulldoze`、`remove_line`、`remove_transport_line` |

## 5. 議会の判断の JSON

`council/m<月>-assembly.json`

```json
{
  "month": 3,
  "rulings": [
    {"measureId": "m03-1", "verdict": "可決", "kind": "税", "point": null, "reason": "..."},
    {"measureId": "m03-2", "verdict": "否決", "kind": "取り壊し", "point": 1, "reason": "..."}
  ],
  "approvedKinds": ["税"]
}
```

- `kind`: 税 / 予算 / 融資 / 取り壊し
- `point`: 否決の点の番号(1〜4。`council-design.md` の3.4)。可決は null
- `approvedKinds`: 可決した議案の種類(重ならない)。hooks はこれだけを見る

## 6. hooks の記録

`council/m<月>-hooks.log`。1行1件、タブ区切り。

```
時刻(ISO8601)	agent_type	道具	結果	詳しく
2026-10-30T14:05:12+09:00	council-mayor-field	set_tax	deny	議決のない税の変更
```

- 時刻は実時間(時差つき)。`command-log.txt` と時刻で突き合わせるため、ゲーム内の日付は使わない
- 結果: `ok` / `ng`(道具が ok:false を返した)/ `deny`(hooks が止めた)/ `warn`(MOD に届かず、税と予算の幅を確かめずに通した)
- 道具は `mcp__cities-skylines__` を外した名前。Write は `Write` のまま

## 7. Workflow の返り値の形

`council-month.js` の各段の `schema`。項目はすべて必須(`required`)。

```js
SEEN = { gameDate: string, saveName: string, priorities: string[], stop: boolean, stopReason: string }
GUIDE = { buildCap: number, upkeepCap: number, taxRange: number, budgetRange: number }
PROPOSAL = { bureau: string, hasProposal: boolean, executionReady: boolean, noProposalReason: string,
             title: string, buildCost: number, upkeepPerWeek: number,
             reversible: boolean, planItems: string[], needsVote: boolean, voteKind: string,
             survey: { exists: boolean, question: string, plan: string } }
ASSESSMENT = { assessments: [{ bureau: string, verdict: "可"|"減額"|"不可", reason: string }],
               taxProposal: { exists: boolean, summary: string }, totalCap: number }
BILL = { measures: [{ id: string, fromBureau: string, title: string, needsVote: boolean, voteKind: string, planItems: string[] }],
         rejected: [{ bureau: string, reason: string }],
         surveys: [{ id: string, fromBureau: string, question: string }] }
RULING = { rulings: [{ measureId: string, verdict: "可決"|"否決", kind: string, point: number|null, reason: string }] }
DONE = { executed: string[], failed: string[], failedReasons: [{ id: string, reason: string }], patrols: [{ gameDate: string, population: number, money: number,
         weeklyBalance: number, happiness: number, alert: boolean }], emergency: boolean, stop: boolean,
         stopReason: string, surveysDone: string[], report: string }
```

- 施策の id は `m<月2桁>-<番号>`(例: `m03-1`)。市長がまとめる段で付ける
- 調査の id は `s<月2桁>-<番号>`(例: `s03-1`)。施策の3件とは別に3件まで。査定と議決はいらない。Workflow は、施策の案がなくても調査があれば、まとめる段を呼ぶ
- `voteKind` は議決が要らないとき空文字
- 案がない局は `hasProposal: false`、`executionReady: false`、`title: ""`、数は0。`noProposalReason` に検討した候補と当月の根拠を書く
- 提案がある場合の `noProposalReason` は空文字
- `executionReady` は必須の実行条件を確認した場合だけ true。Workflowは true の局の案だけを採択対象にする
- 財政局の税の追加案は、`taxProposal.exists` が true の場合だけ採択できる
- 対象外の局の案が議案に含まれた場合は `stoppedAt` を返し、実行に進まない
- 返り値はファイルの要約。食い違ったらファイルを正とする

## 8. 台帳の1行

`council/ledger.jsonl`。案1件ごとに1行。月の終わりに `make_council_ledger.py <運営のフォルダ> <月>` が足す。翌月の実行で、前の月の行の `review` を埋める。

```json
{"month": 3, "id": "m03-urban", "bureau": "urban", "title": "...", "hasProposal": true,
 "planItems": ["4-2"], "priority": true,
 "assessment": {"verdict": "可", "reason": "..."},
 "adopted": {"measureId": "m03-1", "reason": null},
 "vote": {"needed": false, "verdict": null, "point": null},
 "executed": {"ok": true, "cost": 1200, "reason": null},
 "review": null,
 "seenCheck": {"claimed": ["city_info", "services"], "unlogged": []}}
```

- `id` は局の案の id(`m<月>-<局>`)。市長の施策の id(`measureId`)とは別
- `adopted.measureId` は、採らなかったら null。`adopted.reason` は採らなかった理由
- `executed.reason`: 打てなかった(`ok` が false)とき、実行する市長が返した理由(`failedReasons`)。翌月の局が読む
- `review`: 翌月に `{"result": "当たり"|"外れ"|"半分", "reason": "..."}`
- `seenCheck`: 各役のファイルの「見たもの」に書かれた道具(`claimed`)のうち、hooks の記録に呼んだ跡がないもの(`unlogged`)

## 9. 各役のファイルの終わりに書く3つ

すべての役のファイル(`m<月>-*.md`)は、最後に次の見出しを持つ。台帳と議事録のスクリプトは、この見出しで読む。

```markdown
## 見たもの

- `city_info`: 人口 100,140、所持金 498,704
- `services`: 小学校の定員 7,200

## 判断の根拠

(確認した数値や条件を挙げ、判断の理由を2〜3文で説明する)

## 捨てたもの

- (比べて選ばなかったものと、その理由)
```

「見たもの」の行は、必ず道具の名前を `` ` `` で囲んで行の頭に置く。

## 10. hooks のスクリプトの呼び方

スクリプトは1つ(`code/ai-mayor/tools/council_hooks/guard.py`)で、引数で場面を分ける。標準入力に Claude Code の hook の JSON を受ける。
定義のフロントマターでは、`"$CLAUDE_PROJECT_DIR"/code/ai-mayor/tools/council_hooks/guard.py` を絶対パスとして呼ぶ。

| 場面 | 引数 | どの定義に付けるか | すること |
|---|---|---|---|
| PreToolUse | `pre` | 5種類すべて(matcher は `mcp__cities-skylines__.*` と `Write`) | 定義(`agent_type`)と道具ごとに、`council-design.md` の6.5の決まりを当てる。止めるときは `permissionDecision: deny` と理由を返す |
| PostToolUse | `post` | 5種類すべて(matcher は `mcp__cities-skylines__.*`) | hooks の記録に1行足す。道具が `advance` なら状態のファイルの `advanced` を true にする |
| Stop | `stop` | 7つの局 | 自分の案のファイルに案の7点と、9の3つの見出しがなければ、終わらせずに書き直させる(exit code 2) |

`pre` で当てる決まり(`council-design.md` の6.5):

- 実行する市長: 議決が要る道具は、その月の `assembly.json` の `approvedKinds` に種類がなければ止める。状態のファイルの `advanced` が true なら、議決が要る道具はすべて止める(臨時)
- 実行する市長: `set_tax` と `set_budget` は、MOD(`http://127.0.0.1:8781/economy`)の今の値と比べ、税±2、予算±20を超えたら止める
- すべての定義: 作る道具の引数に `pay=false`(`pay: false`)があれば止める
- 局、財政局、議会: `Write` の先が、自分に許されたファイル(2の表)でなければ止める
- 状態のファイルがない、または読めないときは止めない(ハーネスの外で呼ばれたとき)

止めたときも、hooks の記録に `deny` で1行足す。
