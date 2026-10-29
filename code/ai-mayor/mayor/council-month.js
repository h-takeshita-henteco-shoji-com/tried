export const meta = {
  name: 'council-month',
  description: '市役所と議会のハーネスで、Cities: Skylines の街を1か月運営する(#100、#105 で調査と道具の説明を足し、#124 で長期計画・差し戻し・議会の財政確認に直した)',
  whenToUse: '/council-month から呼ぶ。args は { runDir, month }',
  phases: [
    { title: '見る', detail: '見てまとめる市長が街と地形を見て、編成方針を書く' },
    { title: '案', detail: '8つの局が案を5件まで出す(並べて呼ぶ)。1か月目は、各局が長期計画も立てる' },
    { title: '計画のレビュー', detail: '1か月目だけ。市長が8つの長期計画を見て、直すべき局を差し戻す(最大5回)' },
    { title: '計画の是正', detail: '1か月目だけ。差し戻された局が、長期計画を直す' },
    { title: 'まとめ', detail: '見てまとめる市長が施策を選ぶ(件数の上限なし)。長期計画をまとめる。条件付きで採らない案は差し戻す' },
    { title: '差し戻し', detail: '条件付きの案を出した局が、1回だけ調べ直す(#124)' },
    { title: '再まとめ', detail: '見てまとめる市長が、調べ直した案を採るかを決める' },
    { title: '議会', detail: '議会が、議案の4つの点と、すべての施策の財政の点を確かめる。1か月目は長期計画の財政面も見る' },
    { title: '実行', detail: '実行する市長が施策を打ち、見回りを2回する' },
  ],
}

// 設計は code/ai-mayor/mayor/council-design.md、受け渡しの形は council-interfaces.md。
// このスクリプトはファイルを書かない。各役がファイルを書き、返り値は分かれ道を決めるためだけに使う。
// 返り値は親の手順(/council-month)が council/m<月>-run.json に写す。

const { runDir, month } = args
if (!runDir || !month) {
  throw new Error('args に runDir と month が要る')
}
const m = String(month).padStart(2, '0')
const prev = month > 1 ? String(month - 1).padStart(2, '0') : null
// 年の最初の月(1、13、25か月目)は、長期計画を立て直す(#124。2年目から)
const first = (Number(month) - 1) % 12 === 0
const yearNo = Math.floor((Number(month) - 1) / 12)  // 0=1年目。2年目の最初の月は 1
const council = `${runDir}/council`
// 案を出す局。財政局も、ほかの局と同じ立場で案を出す(#124)
const BUREAUS = ['urban', 'roads', 'port', 'economy', 'health', 'education', 'fire', 'finance']
const VOTE_KINDS = ['税', '予算', '融資', '取り壊し', '財政']
const MAP_FILES = '地形の資料 code/ai-mayor/mayor/city-map.md と図 code/ai-mayor/mayor/city-map.png'

// 役ごとのモデル(council-design.md の6.4)。Workflow では定義の model が効かず、親の会話のモデルになる(#100 の試運転で確かめた)。
// そのため、呼ぶときに opts.model で渡す。モデルは council-design.md の6.4のとおり
const MODEL = { desk: 'sonnet', field: 'sonnet', assembly: 'sonnet', bureau: 'claude-haiku-5-5' }

// 返り値の形(council-interfaces.md の7)
const str = { type: 'string' }
const num = { type: 'number' }
const bool = { type: 'boolean' }
const strs = { type: 'array', items: str }
const obj = (properties) => ({ type: 'object', properties, required: Object.keys(properties) })

const SEEN = obj({ gameDate: str, saveName: str, priorities: strs, stop: bool, stopReason: str })
// 局の案は5件まで(#124)。案ごとに id(<局>-<番号>)を持つ
const MAX_PROPOSALS = 5
const ONE_PROPOSAL = obj({
  id: str, title: str, executionReady: bool, buildCost: num, upkeepPerWeek: num,
  reversible: bool, planItems: strs, needsVote: bool, voteKind: str,
})
const PROPOSAL = obj({
  bureau: str, hasProposal: bool, noProposalReason: str,
  proposals: { type: 'array', items: ONE_PROPOSAL, maxItems: MAX_PROPOSALS },
  survey: obj({ exists: bool, question: str, plan: str }),
})
const PLAN_REVIEW = obj({
  reviews: { type: 'array', items: obj({ bureau: str, verdict: { type: 'string', enum: ['可', '要是正'] }, corrections: strs }) },
  // 局をまたぐ調整(月、費用の数字、担当)。市長が1回で決め、関係する局に渡す
  adjustments: { type: 'array', items: obj({ bureaus: strs, decision: str }) },
})
const BILL = obj({
  measures: {
    type: 'array',
    items: obj({ id: str, fromBureau: str, title: str, needsVote: bool, voteKind: str, planItems: strs }),
  },
  rejected: { type: 'array', items: obj({ proposal: str, reason: str, kind: { type: 'string', enum: ['不可', '条件付き'] }, condition: str }) },
  surveys: { type: 'array', items: obj({ id: str, fromBureau: str, question: str }) },
})
const RULING = obj({
  rulings: {
    type: 'array',
    items: obj({
      measureId: str,
      verdict: { type: 'string', enum: ['可決', '否決'] },
      kind: { type: 'string', enum: VOTE_KINDS },
      point: { type: ['number', 'null'] },
      reason: str,
    }),
  },
  planCheck: obj({ verdict: { type: 'string', enum: ['可', '要直し'] }, reason: str }),
})
const PLAN_ADJ = obj({ done: bool, summary: str })
const DONE = obj({
  executed: strs,
  failed: strs,
  // 打てなかった理由。道具が返した理由(ぶつかった相手など)を、翌月の局が台帳で読めるようにする(#105)
  failedReasons: { type: 'array', items: obj({ id: str, reason: str }) },
  patrols: {
    type: 'array',
    items: obj({ gameDate: str, population: num, money: num, weeklyBalance: num, happiness: num, alert: bool }),
  },
  emergency: bool,
  stop: bool,
  stopReason: str,
  surveysDone: strs,
  report: str,
})

const common = `運営のフォルダ: ${runDir}\n何か月目: ${month}\n`

// 1. 見る
phase('見る')
const seen = await agent(
  `${common}段: 見る段\n` +
  `判断の型の順番で街を見て、市政ノートに前の月の答え合わせと数字の表を書く。` +
  `${MAP_FILES}も読み、島と空き地を使う手を編成方針の「局への伝え」に書く。` +
  `最後に編成方針を ${council}/m${m}-policy.md に書く。` +
  `同じ月の保存がすでにあるときは、save_city の overwrite=true で上書きしてよい(同じ月のやり直しのため)。`,
  { agentType: 'council-mayor-desk', model: MODEL.desk, label: `見る m${m}`, schema: SEEN },
)
if (!seen || seen.stop) {
  return { month, stoppedAt: '見る', seen }
}

// 2. 案(8つの局を並べて呼ぶ。全部そろうまで待つ)
phase('案')
const proposals = await parallel(BUREAUS.map((b) => () => agent(
  `${common}段: 案を出す\n` +
  `読む: ${council}/m${m}-policy.md、市政ノートの数字の表、${council}/ledger-recent.jsonl(直近3か月)と ${council}/ledger-older.md(それ以前の要約)の自分の局の行` +
  (first ? (yearNo > 0 ? `、前の年の長期計画 ${council}/plan-year${yearNo}/plan-${b}.md と、前の年の結果の要約 ${council}/ledger-older.md` : '') : `、自分の長期計画 ${council}/plan-${b}.md、市長がまとめた計画 ${council}/plan-city.md`) +
  (prev ? `、前の月の自分の調査の結果 ${council}/m${prev}-survey-${b}.md(あれば)` : '') +
  `、街を作る・変える道具の説明 code/ai-mayor/mayor/tool-reference.md、${MAP_FILES}\n` +
  (first
    ? `${yearNo > 0 ? `${yearNo + 1}年目の最初の月なので、前の年の計画と結果を踏まえ、続きの12か月の長期計画を立て直す。市の計画の目標(city-plan.md)は変わらない。前の年に閉じた事業を、確かめずに繰り返さない。` : '1か月目なので、'}案を出す前に、12か月の長期計画を ${council}/plan-${b}.md に書く(定義の「長期計画」の形)。案は、その計画の第1月に沿って出す。\n`
    : `案は、自分の長期計画の「今月の予定」に沿って出す。前提が違うなら、計画を直し「計画の変更」に理由を書いてから、案を出す。\n`) +
  `道具の名前と引数は tool-reference.md で確かめ、実行計画に道具の名前と引数の値を書く。そうすれば引数は確かめたことになる。\n` +
  `案は5件まで出せる。案ごとに別の手にし、件数を埋めるための案は作らない。案の id は ${b}-<番号>。\n` +
  `原因が分からない、確証が持てない問題は、案なしで終えず、調査(見る道具だけ、見回りと月末に実行する市長が測る)を1件まで出せる。\n` +
  `案を決める前に list_policies で政策名・有効状態・週の費用を確認し、担当する問題に関係する政策の変更をほかの手段と比較する。取得結果は「見たもの」に記録し、取得できなければ未確認と書く。\n` +
  `建設場所や接続条件は局が調べ、確認済みの座標・操作・予備候補を実行計画に書く。実行役に場所探しを残さない。\n` +
  `期待する効果に、改善の見込み、数値と期限、確認方法、不確かな点、試しを書く。確認した事実と局の予測を分け、数値を見積もれなければその旨を書く。効き目が分からない案は試しとして、仮説・測る数・場所・基準を書く。\n` +
  `前月の非採択や他局の優先順位を理由に提案を控えない。当月も有効なら同じ案を再提出する。案なしなら当月の根拠を noProposalReason に書く。必須の実行条件が未確認なら executionReady=false とし、置いてから確かめる案は採択対象にしない。\n` +
  `書くファイル: ${council}/m${m}-${b}.md(案)と ${council}/plan-${b}.md(長期計画)だけ。ほかの局の案は読まない`,
  { agentType: `council-${b}`, model: MODEL.bureau, label: `案 ${b}`, phase: '案', schema: PROPOSAL },
)))

// 再調査・是正で直った案を、案の一覧に入れ直す。入れ直した案の一覧を返す
const mergeInto = (r) => {
  if (!r || !BUREAUS.includes(r.bureau)) return []
  const i = BUREAUS.indexOf(r.bureau)
  const old = proposals[i] || { bureau: r.bureau, hasProposal: true, noProposalReason: '', proposals: [], survey: { exists: false, question: '', plan: '' } }
  const byId = {}
  for (const x of r.proposals || []) byId[x.id] = x
  const merged = (old.proposals || []).map((x) => byId[x.id] || x)
  for (const x of r.proposals || []) if (!merged.some((y) => y.id === x.id)) merged.push(x)
  proposals[i] = { ...old, hasProposal: merged.length > 0, proposals: merged }
  return r.proposals || []
}

// 1か月目: 市長が長期計画をレビューし、直すべき局へ差し戻す。差し戻しは最大5回(#124)
const MAX_PLAN_REVISIONS = 2
const planReviews = []
const allAdjustments = []
if (first) {
  for (let round = 0; round <= MAX_PLAN_REVISIONS; round++) {
    phase('計画のレビュー')
    const review = await agent(
      `${common}段: 計画のレビュー\n` +
      `何回目のレビューか: ${round}回目(0回目が最初)。差し戻しは最大${MAX_PLAN_REVISIONS}回。局をまたぐ調整は、局へ差し戻さず、あなたが1回で決める。\n` +
      (allAdjustments.length ? `前の回までに決めた調整: ${JSON.stringify(allAdjustments)}\n` : '') +
      `読む: ${BUREAUS.map((b) => `${council}/plan-${b}.md`).join('、')}、1か月目の案 ${BUREAUS.map((b) => `${council}/m${m}-${b}.md`).join('、')}` + (round > 0 ? `、前回までの ${council}/plan-review.md` : '') + `\n` +
      `書くファイル: ${council}/plan-review.md(前の回の節は消さず、この回の節を足す)`,
      { agentType: 'council-mayor-desk', model: MODEL.desk, label: `計画のレビュー ${round}回目`, schema: PLAN_REVIEW },
    )
    planReviews.push(review)
    for (const a of (review && review.adjustments) || []) allAdjustments.push(a)
    const targets = ((review && review.reviews) || []).filter((r) => r.verdict === '要是正' && BUREAUS.includes(r.bureau))
    if (targets.length === 0 || round === MAX_PLAN_REVISIONS) break
    phase('計画の是正')
    const fixes = await parallel(targets.map((t) => () => agent(
      `${common}段: 計画の是正\n` +
      `市長の指摘(第${round + 1}回の差し戻し。自分の局の中で直せる点): ${JSON.stringify(t.corrections)}\n` +
      `市長が決めた、局をまたぐ調整(自分の局に関わるもの。計画に、そのまま反映する): ${JSON.stringify(allAdjustments.filter((a) => (a.bureaus || []).includes(t.bureau)))}\n` +
      `読む: ${council}/plan-${t.bureau}.md、${council}/m${m}-${t.bureau}.md、${council}/plan-review.md の自分の局の行、code/ai-mayor/mayor/tool-reference.md、${MAP_FILES}\n` +
      `指摘を道具で確かめて直す。指摘が求めること以外に、計画を広げない。第1月の予定が変わったら、1か月目の案も直す。返り値の proposals には、いまの案のすべてを入れる。\n` +
      `書くファイル: ${council}/plan-${t.bureau}.md と ${council}/m${m}-${t.bureau}.md だけ`,
      { agentType: `council-${t.bureau}`, model: MODEL.bureau, label: `是正 ${t.bureau} ${round + 1}回目`, phase: '計画の是正', schema: PROPOSAL },
    )))
    for (const r of fixes) mergeInto(r)
  }
}

// 案ごとに見る。1つの局の案は5件まで。条件未確認の案は、採択・実行に進めない
const allProposals = proposals.flatMap((p, i) => (p && p.bureau === BUREAUS[i] ? (p.proposals || []).slice(0, MAX_PROPOSALS).map((x) => ({ ...x, bureau: p.bureau })) : []))
const readyProposals = allProposals.filter((x) => x.executionReady === true)
const withProposal = proposals.filter((p, i) => p && p.bureau === BUREAUS[i] && readyProposals.some((x) => x.bureau === p.bureau))
// 調査(#105 の作り直し)。街を変えないので、議決はいらない。採るかは市長が決める
const withSurvey = proposals.filter((p, i) => p && p.bureau === BUREAUS[i] && p.survey && p.survey.exists === true)
const readyIds = readyProposals.map((x) => x.id)
const excludedProposals = allProposals.filter((x) => !readyProposals.includes(x))
if (excludedProposals.length) {
  log(`m${m}: 実行条件を確認できない案を採択対象から除外: ${excludedProposals.map((x) => x.id).join('、')}`)
}
// 市長が元の案を、案の id(finance-1)でなく、局の名前(finance)だけで書いたとき、その局のいまの実行可の案が1件だけなら、その案の id に直す(#124。9か月目に、この書き方の違いで Workflow が止まった)
const normalizeSources = (measures) => {
  for (const x of measures || []) {
    if (typeof x.fromBureau !== 'string') continue
    x.fromBureau = x.fromBureau.split(',').map((raw) => {
      const b = raw.trim()
      if (readyIds.includes(b) || !BUREAUS.includes(b)) return b
      const own = readyIds.filter((id) => id.startsWith(b + '-'))
      return own.length === 1 ? own[0] : b
    }).join(',')
  }
  return measures
}
const validSources = (measures) => normalizeSources(measures).every((x) => {
  const sources = typeof x.fromBureau === 'string' ? x.fromBureau.split(',').map((b) => b.trim()) : []
  return sources.length > 0 && sources.every((b) => readyIds.includes(b))
})
let bill = null
let ruling = null
let ruling2 = null
let allowed = []
let rechecks = null
let planCheck = null
let planRevised = null

if (withProposal.length > 0 || withSurvey.length > 0) {
  // 3. まとめ
  phase('まとめ')
  bill = await agent(
    `${common}段: まとめる段\n` +
    `読む: 8つの局の案(${BUREAUS.map((b) => `${council}/m${m}-${b}.md`).join('、')})と、各局の長期計画 ${council}/plan-<局>.md\n` +
    `採択できる案: ${readyIds.length ? readyIds.join("、") : 'なし(施策の案はない)'}。施策の件数に上限はない(費用は財政の守る線に収める。守れているかは議会が確かめる)。本文にも必須条件の未確認が残る案は採らない。前月の採否ではなく当月の根拠で選ぶ。\n` +
    (first
      ? `1か月目なので、8つの長期計画を並べて、${council}/plan-city.md に、事業の一覧、依存と順番、費用の合計、調整を書く(定義の「長期計画をまとめる」)。計画のレビューで未解決の点があれば、「未解決」に書く(${council}/plan-review.md)。\n`
      : `局が長期計画を直していたら、${council}/plan-city.md に反映する。\n`) +
    `調査を出した局: ${withSurvey.length ? withSurvey.map((p) => p.bureau).join('、') : 'なし'}。調査は施策とは別に3件まで採れる(議決はいらない)。\n` +
    `道具の引数は code/ai-mayor/mayor/tool-reference.md で確かめる。\n` +
    `採らない案は、kind を「不可」か「条件付き」に分け、条件付きには道具で確かめられる condition を書く(実行条件が未確認の案も、直せば採れるなら条件付き)。条件付きは、出した局が同じ月のうちに1回だけ調べ直す。\n` +
    `書くファイル: ${council}/m${m}-bill.md。施策の id は m${m}-1、m${m}-2 のように付ける`,
    { agentType: 'council-mayor-desk', model: MODEL.desk, label: `まとめ m${m}`, schema: BILL },
  )
  // 差し戻し(#124): 条件付きで採らない案を、出した局が1回だけ調べ直す。局ごとに3件まで
  const conditional = ((bill && bill.rejected) || []).filter((r) => r.kind === '条件付き')
  const byBureau = {}
  for (const r of conditional) {
    const b = String(r.proposal).replace(/-\d+$/, '')
    if (BUREAUS.includes(b)) {
      byBureau[b] = byBureau[b] || []
      if (byBureau[b].length < 3) byBureau[b].push(r)
    }
  }
  const recheckBureaus = Object.keys(byBureau)
  if (recheckBureaus.length > 0) {
    phase('差し戻し')
    rechecks = await parallel(recheckBureaus.map((b) => () => agent(
      `${common}段: 再調査\n` +
      `市長が条件付きで差し戻した案: ${JSON.stringify(byBureau[b])}\n` +
      `読む: ${council}/m${m}-${b}.md、${council}/m${m}-bill.md の「採らなかった案」、${council}/ledger-recent.jsonl の自分の局の行、code/ai-mayor/mayor/tool-reference.md、${MAP_FILES}\n` +
      `条件を道具で確かめ、差し戻された案の節だけを直す。再調査は1回だけ。返り値の proposals には、再調査した案だけを入れる。\n` +
      `書くファイル: ${council}/m${m}-${b}.md(このファイルと、長期計画 ${council}/plan-${b}.md だけを書く)`,
      { agentType: `council-${b}`, model: MODEL.bureau, label: `再調査 ${b}`, phase: '差し戻し', schema: PROPOSAL },
    )))
    // 再調査した案を、案の一覧に入れ直す
    const newlyReady = []
    for (const r of rechecks) {
      if (!r || !BUREAUS.includes(r.bureau)) continue
      for (const x of mergeInto(r)) {
        // 再調査した案は、前から実行可だった案も含めて、市長が再まとめで採るかを決め直す(前から実行可の案も、条件付きで採られていなかった)
        if (x.executionReady === true && byBureau[r.bureau].some((c) => c.proposal === x.id)) {
          if (!readyIds.includes(x.id)) readyIds.push(x.id)
          newlyReady.push(x.id)
        }
      }
    }
    if (newlyReady.length > 0) {
      phase('再まとめ')
      bill = await agent(
        `${common}段: 再まとめ\n` +
        `再調査して実行条件がそろった案: ${newlyReady.join('、')}\n` +
        `読む: ${council}/m${m}-bill.md、${recheckBureaus.map((b) => `${council}/m${m}-${b}.md`).join('、')}\n` +
        `書くファイル: ${council}/m${m}-bill.md(上書き。最初のまとめの施策は変えずに残し、新しく採る施策は番号を続けて足す)`,
        { agentType: 'council-mayor-desk', model: MODEL.desk, label: `再まとめ m${m}`, schema: BILL },
      )
    }
  }
  const measures = (bill && bill.measures) || []
  if (!validSources(measures)) {
    return { month, stoppedAt: 'まとめ', stopReason: '実行条件を確認できていない局の案が議案に含まれる', seen, proposals, bill, rechecks }
  }

  // 費用の合計は、スクリプトが案の数字から計算して、議会に渡す(AIの暗算にしない)
  const byIdAll = {}
  for (const p of proposals) for (const x of (p && p.proposals) || []) byIdAll[x.id] = x
  const costOf = (ms) => {
    const rows = (ms || []).map((x) => {
      const src = String(x.fromBureau || '').split(',').map((b) => b.trim())
      const build = src.reduce((a, id) => a + ((byIdAll[id] && byIdAll[id].buildCost) || 0), 0)
      const upkeep = src.reduce((a, id) => a + ((byIdAll[id] && byIdAll[id].upkeepPerWeek) || 0), 0)
      return { id: x.id, build, upkeepPerWeek: upkeep }
    })
    return { rows, totalBuild: rows.reduce((a, r) => a + r.build, 0), totalUpkeepPerWeek: rows.reduce((a, r) => a + r.upkeepPerWeek, 0) }
  }
  // 4. 議会(#124): 議案は4つの点と財政の点、議決が要らない施策は財政の点で確かめる。1か月目は長期計画の財政面も見る
  if (measures.length > 0) {
    phase('議会')
    ruling = await agent(
      `${common}段: 施策を確かめる\n` +
      `読む: ${council}/m${m}-bill.md` + (first ? `、${council}/plan-city.md、${BUREAUS.map((b) => `${council}/plan-${b}.md`).join('、')}` : '') + `\n` +
      `スクリプトが案の数字から計算した費用: ${JSON.stringify(costOf(measures))}。点5(財政)は、この値と案のファイルの数字を照らして確かめる。\n` +
      `すべての施策に判断を書く。議案(議決が要る施策)は点1〜5、議決が要らない施策は点5(財政)だけ。` +
      (first ? `1か月目なので、長期計画の財政面も確かめ、planCheck に「可」か「要直し」を書く。` : `2か月目以降の planCheck は {"verdict":"可","reason":""} とする。`) + `\n` +
      `書くファイル: ${council}/m${m}-assembly.md と ${council}/m${m}-assembly.json`,
      { agentType: 'council-assembly', model: MODEL.assembly, label: `議会 m${m}`, schema: RULING },
    )
    const rulings = (ruling && ruling.rulings) || []
    planCheck = (ruling && ruling.planCheck) || null
    const judged = new Set(rulings.map((r) => r.measureId))
    // 判断がない施策は、議決が要らないものだけ打ってよい(議決が要るものは、hooks も止める)
    allowed = measures.filter((x) => !x.needsVote && !judged.has(x.id)).map((x) => x.id)
    allowed = allowed.concat(rulings.filter((r) => r.verdict === '可決').map((r) => r.measureId))

    // 否決があれば、市長が1回だけ直す。1回目で否決されなかった施策は変えない
    const rejected = rulings.filter((r) => r.verdict === '否決')
    if (rejected.length > 0) {
      const revised = await agent(
        `${common}段: 直す段\n` +
        `否決された施策: ${JSON.stringify(rejected)}\n` +
        `否決された施策だけを直し、${council}/m${m}-bill-2.md に書く。否決されなかった施策は変えない。` +
        `点5(財政)で否決された施策は、費用を減らすか、採るのをやめる。直した施策の id は元の id を使う`,
        { agentType: 'council-mayor-desk', model: MODEL.desk, label: `直す m${m}`, phase: '議会', schema: BILL },
      )
      if (!validSources(revised?.measures)) {
        return { month, stoppedAt: '議会', stopReason: '修正した議案に実行条件を確認できていない局の案が含まれる', seen, proposals, bill, revised, ruling }
      }
      const fixed = ((revised && revised.measures) || []).filter((x) => rejected.some((r) => r.measureId === x.id))
      if (fixed.length > 0) {
        ruling2 = await agent(
          `${common}段: 直した施策を確かめる(2回目)\n` +
          `読む: ${council}/m${m}-bill-2.md\n` +
          `直した施策は、議案なら点1〜5、議決が要らない施策なら点5で確かめる。直したあとの費用(スクリプトの計算): ${JSON.stringify(costOf((revised && revised.measures) || []))}\n` +
          `書くファイル: ${council}/m${m}-assembly-2.md。${council}/m${m}-assembly.json は、1回目と2回目を合わせた形で上書きする`,
          { agentType: 'council-assembly', model: MODEL.assembly, label: `議会2 m${m}`, phase: '議会', schema: RULING },
        )
        const rulings2 = (ruling2 && ruling2.rulings) || []
        allowed = allowed.concat(rulings2.filter((r) => r.verdict === '可決').map((r) => r.measureId))
      }
    }
    // 1か月目: 長期計画の財政面が「要直し」なら、市長が計画の順番や月を1回だけ調整する
    if (first && planCheck && planCheck.verdict === '要直し') {
      planRevised = await agent(
        `${common}段: 計画の調整\n` +
        `議会が、長期計画の財政面を「要直し」とした。理由: ${planCheck.reason}\n` +
        `読む: ${council}/plan-city.md、${council}/m${m}-assembly.md\n` +
        `${council}/plan-city.md の「調整」に、事業の順番や月の置き直しを書く。局の計画は書き換えない(局が2か月目に、調整を読んで自分で直す)`,
        { agentType: 'council-mayor-desk', model: MODEL.desk, label: `計画の調整 m${m}`, schema: PLAN_ADJ },
      )
    }
  }
} else {
  log(`m${m}: 実行条件を確認済みの提案も調査もなし。まとめを飛ばす`)
}

allowed = [...new Set(allowed)]
const surveys = ((bill && bill.surveys) || []).filter((x) => withSurvey.some((p) => p.bureau === x.fromBureau))

// 5. 実行と見回り
phase('実行')
const done = await agent(
  `${common}段: 実行と見回り\n` +
  `実行してよい施策の id: ${allowed.length ? allowed.join('、') : 'なし'}\n` +
  `実行してよい調査の id: ${surveys.length ? surveys.map((x) => `${x.id}(${x.fromBureau})`).join('、') : 'なし'}。調査は bill の「調査」から読み、決められた見る道具を見回りと月末に呼んで ${council}/m${m}-survey-<局>.md に書く\n` +
  `施策の中身は ${council}/m${m}-bill.md(直したときは ${council}/m${m}-bill-2.md も)から読む。` +
  `実行してよい施策のほかは打たない。実行計画の対象を最終確認して操作し、新しい候補地を探さない。条件が違えば記載の予備候補を使い、解決しなければ見送って報告する。臨時では議決が要る道具を使わない`,
  { agentType: 'council-mayor-field', model: MODEL.field, label: `実行 m${m}`, schema: DONE },
)

return { month, seen, proposals, planReviews, bill, rechecks, ruling, ruling2, planCheck, planRevised, allowed, surveys, done }
