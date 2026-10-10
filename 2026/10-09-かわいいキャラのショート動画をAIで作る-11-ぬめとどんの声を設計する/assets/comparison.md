# 声の比較メモ

説明文の書き方で声が変わるかを見る。AIは Qwen3-TTS の VoiceDesign に固定する。
説明文はA(#20 のまま)、B(型に沿った英語)、C(Bの日本語版)。各3回作った。
説明文と台詞は `prompts.md`。

`generated/` には、採用した声と、その元になった音声だけを置いた。
このメモに名前が出てくるほかのファイルは、リポジトリに置いていない。

## 見ること

- 遅さ: 間が「考えている」に聞こえるか、ただ遅いだけか
- 方言らしさ: 語尾が柔らかいか。特定の地域や中国語なまりに聞こえないか
- 性別: どちらとも決めにくい声か
- 演技: アニメ調になっていないか

## どん

### A: #20 の説明文

- ファイル: `generated/don_qwen_A_1.wav` 〜 `_3.wav`
- ひとこと: どんのキャラに合わない。いい声すぎる。

### B: 型に沿った英語

- ファイル: `generated/don_qwen_B_1.wav` 〜 `_3.wav`
- ひとこと: B1は良い感じ。ただ、ちょっと怖い。
- B1の話し方(方言らしさ)は良い。声のエッジをもう少し丸くすれば良くなりそう。

### C: Bの日本語版

- ファイル: `generated/don_qwen_C_1.wav` 〜 `_3.wav`
- ひとこと: どれも特徴的。いずれも、もう少し柔らかくしたい。

### D: Bを柔らかくした版

- ファイル: `generated/don_qwen_D_1.wav` 〜 `_3.wav`
- ひとこと: B1と比べると、B1のほうが良い。

### E: Cを柔らかくした版

- ファイル: `generated/don_qwen_E_1.wav` 〜 `_3.wav`
- ひとこと:

### B1の角を丸くする

説明文を変えて作り直すと、声そのものが変わる。B1の話し方を残すため、音声を後から加工した。
高い音(声の角)を弱める加工を、強さを変えて3本作った。手順は `scripts/soften.py`。

- `generated/don_qwen_B_1_soft1.wav`: 弱め。4kHzより上を4dB下げた
- `generated/don_qwen_B_1_soft2.wav`: 中くらい。3kHzより上を8dB下げた
- `generated/don_qwen_B_1_soft3.wav`: 強め。2.5kHzより上を8dB、6kHzより上をさらに10dB下げた
- ひとこと:

### B1を少し高くする

「ほんの少し高く」との感想を受けた。話す速さは変えず、高さだけを上げた。手順は `scripts/pitch.py`。
半音はピアノの隣の鍵盤1つ分の差。

1回目は位相ボコーダ(librosa)で、半音0.5・1.0・1.5上げた。
- ひとこと: エコーが掛かって変な声になった。

2回目は、話し声向けの PSOLA(Praat)に替えた。PSOLAは、声の波を1周期ずつ詰め直して高さを変える。
元には、角を丸くした soft1〜3 を使った。

- `generated/don_qwen_B_1_soft1_up0.5.wav` / `_up1.0.wav`
- `generated/don_qwen_B_1_soft2_up0.5.wav` / `_up1.0.wav`
- `generated/don_qwen_B_1_soft3_up0.5.wav` / `_up1.0.wav`
- ひとこと:

### soft1 の抑揚とかすれを別々に変える

元は `don_qwen_B_1_soft1.wav`。1つの要素だけを動かした。

抑揚は PSOLA で、平均の高さを保って上下の幅だけを変えた。手順は `scripts/intonation.py`。

- `generated/don_qwen_B_1_soft1_into0.7.wav`: 幅を0.7倍。淡々とする
- `generated/don_qwen_B_1_soft1_into1.3.wav`: 幅を1.3倍。表情が出る
- ひとこと: 1.3よりさらに上げたい。
- `generated/don_qwen_B_1_soft1_into1.5.wav` / `_into1.7.wav` / `_into2.0.wav`: 幅を1.5倍・1.7倍・2.0倍
- `generated/don_qwen_B_1_soft1_into2.5.wav` / `_into3.0.wav` / `_into3.5.wav`: 幅を2.5倍・3.0倍・3.5倍
- ひとこと: 3.0倍を採用する。

かすれは WORLD で、雑音成分だけを減らした。手順は `scripts/husky.py`。
WORLD は組み立て直すだけで音が劣化することがある。そのため、加工なしの版も並べた。

- `generated/don_qwen_B_1_soft1_husky0.wav`: 加工なし。組み立て直しただけ
- `generated/don_qwen_B_1_soft1_husky-1.wav`: かすれを少し減らした
- `generated/don_qwen_B_1_soft1_husky-2.wav`: かすれをはっきり減らした
- ひとこと:

### 残す1本

- ファイル: `generated/don_qwen_B_1_soft1_into3.0.wav`
- 理由: B1の話し方(方言らしさ)が良い。角を丸くし(soft1)、抑揚を3倍に広げると、どんに近づいた。

### 本番の台詞(カット6)

採用した声で、本番の台詞「……んー。今日は、ぬるい寄りだな。」を読ませた。
B1の音声と文字起こしを Baseモデルに渡して、声をクローンした。手順は `scripts/clone.py`。
読ませた後に、採用した加工(soft1と抑揚3倍)をかけた。手順は `scripts/finish.py`。

- `generated/don_clone_cut6_1_final.wav` 〜 `_3_final.wav`: 加工済み。3回読ませた
- `generated/don_clone_cut6_1.wav` 〜 `_3.wav`: 加工前
- 採用: `generated/don_clone_cut6_1_final.wav`

1回目はメモリ不足で止めた。Baseモデルは Mac では float32 で動かす必要があり、約7.8GBを使う。
Docker の仮想マシン(8GB)と合わせると16GBを使い切った。Docker を止めた後は、1本10秒ほどで作れた。

## 書き方の問題か、AIの限界か

- AとB・Cの差: Aは「いい声」に寄り、キャラから外れた。B・Cはキャラに近づいた。
- 判断: 書き方の問題が大きい。物語と禁止を並べた長文より、属性を短く並べたほうがキャラに近い。

## ぬめ

どんと同じく、A(#20 のまま)、B(型に沿った英語)、C(Bの日本語版)を各3回作った。
読ませた台詞は、`voice-baseline.md` のぬめ1〜5をつなげたもの。説明文と台詞は `prompts.md`。

### A: #20 の説明文

- ファイル: `generated/nume_qwen_A_1.wav` 〜 `_3.wav`
- ひとこと:

### B: 型に沿った英語

- ファイル: `generated/nume_qwen_B_1.wav` 〜 `_3.wav`
- ひとこと:

### C: Bの日本語版

- ファイル: `generated/nume_qwen_C_1.wav` 〜 `_3.wav`
- ひとこと:

### 候補を2本に絞る

- 候補: `generated/nume_qwen_A_1.wav` と `generated/nume_qwen_C_1.wav`
- 気づき: ぬめでは、#20 のままの説明文(A)も良かった。書き方だけで決まるとは言い切れない。

### 本番の台詞(カット3)と2匹のやりとり

候補2本をそれぞれクローンし、本番の「……んしょ」を3回ずつ読ませた。手順は `scripts/clone.py`。

- `generated/nume_cloneA_cut3_1.wav` 〜 `_3.wav`: A1の声。`_1` は0.2秒で、ほぼ無音
- `generated/nume_cloneC_cut3_1.wav` 〜 `_3.wav`: C1の声
- 採用: `generated/nume_cloneC_cut3_1.wav`

2つの声を並べた差を聞くため、やりとりを1本につないだ。手順は `scripts/exchange.py`。
どんの返事は、採用したどんの声をクローンして作り、soft1と抑揚3倍をかけた。
ぬめが聞いてからどんが答えるまでは1秒、どんの返事から相づちまでは0.6秒空けた。

- `generated/exchange_numeA_1.wav` 〜 `_3.wav`: ぬめはA1の声
- `generated/exchange_numeC_1.wav` 〜 `_3.wav`: ぬめはC1の声
- ひとこと:

### 残す1本

- ファイル: `generated/nume_qwen_C_1.wav`(声の元)
- やりとり: `generated/exchange_numeC_1.wav` を採用
- 理由: どんと並べたときに良かった。
