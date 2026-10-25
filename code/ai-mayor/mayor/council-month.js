export const meta = {
  name: 'council-month',
  description: '市役所と議会のハーネスで、Cities: Skylines の街を1か月運営する(#100)',
  whenToUse: '/council-month から呼ぶ。args は { runDir, month }',
  phases: [
    { title: '見る', detail: '見てまとめる市長が街を見て、編成方針を書く' },
    { title: '要領', detail: '財政局が今月の予算の枠を書く' },
    { title: '案', detail: '7つの局が案を1件まで出す(並べて呼ぶ)' },
    { title: '査定', detail: '財政局が7つの案を査定する' },
    { title: 'まとめ', detail: '見てまとめる市長が施策を3件まで選ぶ' },
    { title: '議会', detail: '議決が要る施策だけを議会が確かめる' },
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
const council = `${runDir}/council`
const BUREAUS = ['urban', 'roads', 'port', 'economy', 'health', 'education', 'fire']
const VOTE_KINDS = ['税', '予算', '融資', '取り壊し']

// 役ごとのモデル(council-design.md の6.4)。Workflow では定義の model が効かず、親の会話のモデルになる(#100 の試運転で確かめた)。
// そのため、呼ぶときに opts.model で渡す。モデルは council-design.md の6.4のとおり
const MODEL = { desk: 'opus', field: 'opus', assembly: 'opus', finance: 'sonnet', bureau: 'sonnet' }

// 返り値の形(council-interfaces.md の7)
const str = { type: 'string' }
const num = { type: 'number' }
const bool = { type: 'boolean' }
const strs = { type: 'array', items: str }
const obj = (properties) => ({ type: 'object', properties, required: Object.keys(properties) })

const SEEN = obj({ gameDate: str, saveName: str, priorities: strs, stop: bool, stopReason: str })
const GUIDE = obj({ buildCap: num, upkeepCap: num, taxRange: num, budgetRange: num })
const PROPOSAL = obj({
  bureau: str, hasProposal: bool, executionReady: bool, noProposalReason: str, title: str, buildCost: num, upkeepPerWeek: num,
  reversible: bool, planItems: strs, needsVote: bool, voteKind: str,
})
const ASSESSMENT = obj({
  assessments: { type: 'array', items: obj({ bureau: str, verdict: { type: 'string', enum: ['可', '減額', '不可'] }, reason: str }) },
  taxProposal: obj({ exists: bool, summary: str }),
  totalCap: num,
})
const BILL = obj({
  measures: {
    type: 'array',
    items: obj({ id: str, fromBureau: str, title: str, needsVote: bool, voteKind: str, planItems: strs }),
  },
  rejected: { type: 'array', items: obj({ bureau: str, reason: str }) },
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
})
const DONE = obj({
  executed: strs,
  failed: strs,
  patrols: {
    type: 'array',
    items: obj({ gameDate: str, population: num, money: num, weeklyBalance: num, happiness: num, alert: bool }),
  },
  emergency: bool,
  stop: bool,
  stopReason: str,
  report: str,
})

const common = `運営のフォルダ: ${runDir}\n何か月目: ${month}\n`

// 1. 見る
phase('見る')
const seen = await agent(
  `${common}段: 見る段\n` +
  `判断の型の順番で街を見て、市政ノートに前の月の答え合わせと数字の表を書く。` +
  `最後に編成方針を ${council}/m${m}-policy.md に書く。` +
  `同じ月の保存がすでにあるときは、save_city の overwrite=true で上書きしてよい(同じ月のやり直しのため)。`,
  { agentType: 'council-mayor-desk', model: MODEL.desk, label: `見る m${m}`, schema: SEEN },
)
if (!seen || seen.stop) {
  return { month, stoppedAt: '見る', seen }
}

// 2. 要領
phase('要領')
const guide = await agent(
  `${common}段: 予算編成要領\n` +
  `今月の予算の枠を ${council}/m${m}-guide.md に書く。読む: ${council}/m${m}-policy.md`,
  { agentType: 'council-finance', model: MODEL.finance, label: `要領 m${m}`, schema: GUIDE },
)

// 3. 案(財政局が7つの案を一度に読むので、全部そろうまで待つ)
phase('案')
const proposals = await parallel(BUREAUS.map((b) => () => agent(
  `${common}段: 案を出す\n` +
  `読む: ${council}/m${m}-policy.md、${council}/m${m}-guide.md、市政ノートの数字の表、${council}/ledger.jsonl の自分の局の行\n` +
  `案を決める前に list_policies で政策名・有効状態・週の費用を確認し、担当する問題に関係する政策の変更をほかの手段と比較する。取得結果は「見たもの」に記録し、取得できなければ未確認と書く。\n` +
  `建設場所や接続条件は局が調べ、確認済みの座標・操作・予備候補を実行計画に書く。実行役に場所探しを残さない。\n` +
  `期待する効果に、改善の見込み、数値と期限、確認方法、不確かな点、試しを書く。確認した事実と局の予測を分け、数値を見積もれなければその旨を書く。効き目が分からない案は試しとして、仮説・測る数・場所・基準を書く。\n` +
  `前月の非採択や他局の優先順位を理由に提案を控えない。当月も有効なら同じ案を再提出する。案なしなら当月の根拠を noProposalReason に書く。必須の実行条件が未確認なら executionReady=false とし、置いてから確かめる案は採択対象にしない。\n` +
  `書くファイル: ${council}/m${m}-${b}.md(このファイルだけを書く。ほかの局の案は読まない)`,
  { agentType: `council-${b}`, model: MODEL.bureau, label: `案 ${b}`, phase: '案', schema: PROPOSAL },
)))

// 条件未確認の案は、費用の査定が可でも採択・実行に進めない。
const withProposal = proposals.filter((p, i) => p && p.bureau === BUREAUS[i] && p.hasProposal && p.executionReady === true)
const readyBureaus = withProposal.map((p) => p.bureau)
const excludedProposals = proposals.filter((p) => p && p.hasProposal && !withProposal.includes(p))
if (excludedProposals.length) {
  log(`m${m}: 実行条件を確認できない案を採択対象から除外: ${excludedProposals.map((p) => p.bureau).join('、')}`)
}
const validSources = (measures, taxProposal) => (measures || []).every((x) => {
  const sources = typeof x.fromBureau === 'string' ? x.fromBureau.split(',').map((b) => b.trim()) : []
  return sources.length > 0 && sources.every((b) => readyBureaus.includes(b) || (b === 'finance' && taxProposal?.exists === true))
})
let assessed = null
let bill = null
let ruling = null
let ruling2 = null
let allowed = []

if (withProposal.length > 0) {
  // 4. 査定
  phase('査定')
  assessed = await agent(
    `${common}段: 査定\n` +
    `読む: ${BUREAUS.map((b) => `${council}/m${m}-${b}.md`).join('、')}、${council}/m${m}-guide.md\n` +
    `査定する局: ${readyBureaus.join("、")}。それ以外の案は実行条件を確認できていないため査定対象外と記録する。\n` +
    `書くファイル: ${council}/m${m}-finance.md`,
    { agentType: 'council-finance', model: MODEL.finance, label: `査定 m${m}`, schema: ASSESSMENT },
  )

  // 5. まとめ
  phase('まとめ')
  bill = await agent(
    `${common}段: まとめる段\n` +
    `読む: ${council}/m${m}-finance.md と7つの局の案\n` +
    `採択できる局: ${readyBureaus.join("、")}。本文にも必須条件の未確認が残る案は採らない。前月の採否ではなく当月の根拠で選ぶ。\n` +
    `書くファイル: ${council}/m${m}-bill.md。施策の id は m${m}-1、m${m}-2 のように付ける`,
    { agentType: 'council-mayor-desk', model: MODEL.desk, label: `まとめ m${m}`, schema: BILL },
  )
  const measures = (bill && bill.measures) || []
  if (!validSources(measures, assessed?.taxProposal)) {
    return { month, stoppedAt: 'まとめ', stopReason: '実行条件を確認できていない局の案、または提案のない財政局の案が議案に含まれる', seen, guide, proposals, assessed, bill }
  }
  allowed = measures.filter((x) => !x.needsVote).map((x) => x.id)

  // 6. 議会(議案がある月だけ)
  if (measures.some((x) => x.needsVote)) {
    phase('議会')
    ruling = await agent(
      `${common}段: 議案を確かめる\n` +
      `読む: ${council}/m${m}-bill.md\n` +
      `書くファイル: ${council}/m${m}-assembly.md と ${council}/m${m}-assembly.json`,
      { agentType: 'council-assembly', model: MODEL.assembly, label: `議会 m${m}`, schema: RULING },
    )
    const rulings = (ruling && ruling.rulings) || []
    allowed = allowed.concat(rulings.filter((r) => r.verdict === '可決').map((r) => r.measureId))

    // 否決があれば、市長が1回だけ直す。1回目で否決されなかった施策は変えない
    const rejected = rulings.filter((r) => r.verdict === '否決')
    if (rejected.length > 0) {
      const revised = await agent(
        `${common}段: 直す段\n` +
        `否決された議案: ${JSON.stringify(rejected)}\n` +
        `否決された施策だけを直し、${council}/m${m}-bill-2.md に書く。否決されなかった施策は変えない。` +
        `直した施策の id は元の id を使う`,
        { agentType: 'council-mayor-desk', model: MODEL.desk, label: `直す m${m}`, phase: '議会', schema: BILL },
      )
      if (!validSources(revised?.measures, assessed?.taxProposal)) {
        return { month, stoppedAt: '議会', stopReason: '修正した議案に実行条件を確認できていない局の案が含まれる', seen, guide, proposals, assessed, bill, revised, ruling }
      }
      const fixed = ((revised && revised.measures) || []).filter((x) => rejected.some((r) => r.measureId === x.id))
      if (fixed.some((x) => x.needsVote)) {
        ruling2 = await agent(
          `${common}段: 直した議案を確かめる(2回目)\n` +
          `読む: ${council}/m${m}-bill-2.md\n` +
          `書くファイル: ${council}/m${m}-assembly-2.md。${council}/m${m}-assembly.json は、1回目と2回目を合わせた形で上書きする`,
          { agentType: 'council-assembly', model: MODEL.assembly, label: `議会2 m${m}`, phase: '議会', schema: RULING },
        )
        const rulings2 = (ruling2 && ruling2.rulings) || []
        allowed = allowed.concat(rulings2.filter((r) => r.verdict === '可決').map((r) => r.measureId))
      }
      // 直して議決が要らなくなった施策は、そのまま打ってよい
      allowed = allowed.concat(fixed.filter((x) => !x.needsVote).map((x) => x.id))
    }
  }
} else {
  log(`m${m}: 実行条件を確認済みの提案なし。査定とまとめを飛ばす`)
}

allowed = [...new Set(allowed)]

// 7. 実行と見回り
phase('実行')
const done = await agent(
  `${common}段: 実行と見回り\n` +
  `実行してよい施策の id: ${allowed.length ? allowed.join('、') : 'なし'}\n` +
  `施策の中身は ${council}/m${m}-bill.md(直したときは ${council}/m${m}-bill-2.md も)から読む。` +
  `実行してよい施策のほかは打たない。実行計画の対象を最終確認して操作し、新しい候補地を探さない。条件が違えば記載の予備候補を使い、解決しなければ見送って報告する。臨時では議決が要る道具を使わない`,
  { agentType: 'council-mayor-field', model: MODEL.field, label: `実行 m${m}`, schema: DONE },
)

return { month, seen, guide, proposals, assessed, bill, ruling, ruling2, allowed, done }
