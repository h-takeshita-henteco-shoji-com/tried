# 条件を定量的に測る方法の考察

`conditions.md`(第2版)の定義と8条件を、数値で測る方法を考えた。
文献はAI(Claude Opus 5.5 の下で動くエージェント)が検索し、実在を確かめた。どれも要旨か書誌ページまでで、全文は読んでいない。数値を引用する前に本文で確かめる。

## 結論

- **定義の中心「予想を、納得できる形で裏切る」は、AIに読者役をさせれば数値にできる。** 段落ごとに続きや結論を複数回予測させ、予測の散らばりと外れ方を測る。経済学のサスペンスと驚きの定式化(Ely et al. 2015)が、理論の土台になる
- **AIに「面白いか」を点数で答えさせる方法は、主な物差しにしない。** LLMの判定は専門家の評価と相関しなかった例があり(Chakrabarty et al. 2024)、自分の文章を高く評価する偏りもある(Panickssery et al. 2024)
- **妥当性の確かめには、#47 の原文と書き直しの組がそのまま使える。** 面白さの順位が分かっている組で、物差しが同じ順位を出すかを見る
- **日本語の資源に2つの穴がある。** 語ごとの「具体性」の大規模な評定値と、修辞の対句のアノテーションが見つからなかった

## 3つの測り方

測り方を、AIをどう使うかで3つに分ける。

- **文章を数える**: 形態素解析(文を単語に分けて品詞を付ける処理)や言語モデルの確率から、数値を直接出す。AIの判断が入らない
- **AIを測定器にする**: AIに読者役をさせ、予測や問いを出力させる。その出力を数えたり、距離を測ったりする。AIに点数は付けさせない
- **AIに判定させる**: AIに、条件を満たすかを二値で答えさせる。人の判定との一致率を必ず添える

2つ目が今回の要である。「面白いか」を直接聞く代わりに、面白さの手前で読者に起きること(予想する、問いを抱く、予想が外れる)を測る。

## 定義の各項目を測る

### 予想を裏切る(驚き)

**なぜ測れるか。** 驚きは「読む前の予想」と「実際」の差である。AIに予想を出させれば、差を計算できる。

手順:

1. 文章を段落ごとに区切る
2. 各段落の終わりで、AIに「この文章の結論は何か」を N 回(例: 20回)予測させる。対象の読者像を与える
3. 予測を埋め込み(文の意味をベクトルにしたもの)にし、次の2つを計算する
   - **驚き**: 前の段落での予測の中心と、今の段落での予測の中心の距離。読者の考えが動いた量
   - **サスペンス**: 予測の散らばり(分散)。読者が先を読めていない度合い

理論の土台:

- Ely, Frankel & Kamenica (2015) は、サスペンスを「次に信念がどれだけ変わりうるか」、驚きを「信念が実際に変わった量」と定義した。一度に全部明かす開示は、両方を最小にすると導いた [要旨]
- Itti & Baldi (2009) は、事前と事後の分布の差を「ベイズ的驚き」とした。視線の動きを、ほかの既存の指標よりよく予測した [要旨]。単語の珍しさ(surprisal)と、考えを動かす量は別物として扱える

文章で計算した先例:

- Wilmot & Keller (2020) は、物語の表現の上で不確実性の減少を計算した。人のサスペンス評定を最もよく予測した [要旨]
- Fong et al. (arXiv 2024) は、続きをLLMで複数生成して期待と驚きの特徴量を作った。LLMの期待は人の期待と相関した [要旨]
- Sui et al. (COLM 2026) は、各文の時点で結末を100回予測させ、外れた割合を数えた(100-Endings)。LLM判定ではAI作品が上位だったが、この指標では人の作品が上位に来た [要旨]

#47 での予想: A の原文では、72%(「実はソフトウェアの話だった」)で驚きが大きく跳ねるはずである。書き直しは2%で結論を言うので、以降の驚きは小さいはずである。

72%について、3つ注意がある。

- 72%は、本文(空白と改行を除いて2,150字)で、その文が始まる位置の文字数の割合である。Wikisource の本文で計算し直して確かめた。転の位置を決めたのは #47 のAIの読みで、人の判定ではない
- 72%は A だけの値で、ほかの文章に通じる目安ではない。転の位置は文章ごとに違う(B は3%)。物差しが正しければ、驚きは各文章の転で跳ねるはずである
- 題「コードは設計である」と、本の名前『プログラマが知るべき97のこと』が答えを明かしている。原文も「本書の読者は、この話を聞いても驚かないかもしれません」と書く。そこで、題を見せる場合と見せない場合の両方で測る

段落ごとに測る場合、跳ねるのは「本書の読者は」で始まる第6段落(70.6%から)になる。

### 「知りたい」と思わせる(好奇心)

**なぜ測れるか。** 好奇心は「答えの分からない問いを抱えた状態」である(Loewenstein 1994)。読者が抱く問いを集め、それが開いている時間を測ればよい。

手順:

1. 各段落の後で、AIに「読者がここで抱く問い」を出させる
2. 各問いの重要度を付ける
3. 各問いが、後のどの段落で答えられたかを記録する
4. 指標を出す
   - 重要な問いが開いている段落数の合計
   - 最初の重要な問いが立つ位置
   - 答えられなかった重要な問いの数(満たされない好奇心)

使える研究の流れ: QUD(Questions Under Discussion。文章を問いと答えの連鎖とみなす枠組み)。

- INQUISITIVE(Ko et al. 2020)は、ニュースを読み進める読者から約1.9万の問いを集めた [要旨]
- TED-Q(Westera et al. 2020)は、各文の後に喚起された問いと、後で答えられたかを付けた。データが公開されている [要旨]
- QSalience(Wu et al. 2024)は、問いの重要度を予測した。重要度の高い問いほど、同じ記事内で答えられやすかった [要旨]
- QUDeval (Wu et al. 2023) は、LLMが作る問いが制約を満たしきれないと報告した [要旨]。AIの問いは、私の問いと照らし合わせる必要がある

驚きとの違い: 好奇心は「問いが開いている時間」、サスペンスは「答えの候補が散らばっている度合い」である。B の逆説(3%)は、問いを開いたまま約80%を引っぱる。好奇心の指標が高く出るはずである。

### 裏切りに納得できる理由がある

**なぜ測れるか。** 納得とは「先には読めなかったが、後から振り返ると筋が通る」ことである。予測の前と後で、確率の変わり方を比べれば測れる。

手順:

1. 裏切りの文(驚きが跳ねた段落の主張)を特定する
2. 次の3つの条件で、その文の確率を言語モデルで測る
   - 裏切りより前の本文だけを与える(先に読めたか)
   - 本文全体から裏切りの文を除いて与える(振り返ると筋が通るか)
   - さらに理由の段落も除いて与える(理由が効いているか)
3. 「前だけでは低く、全体では高い」ほど納得できる裏切りとみなす。理由を除いて確率が下がれば、その理由が効いている

文献の直接の先例は見つからなかった。Silvia (2005) の「新しく複雑だ」と「自分にも分かりそうだ」の2評価を、確率の2つの条件に対応させた私たちの案である。

### 書き手の視点から来ていると読める

**なぜ測れるか。** 第2版では、視点の中身を素材メモで固定した。測るのは出し方なので、同じ素材メモから書いた文章どうしの差として測れる。

指標:

- **AIの平均からの距離**: 同じ素材メモからAIに10本書かせ、その中心からの距離を測る。Doshi & Hauser (2024) の「集団の中心への類似度」を借りる [要旨]
- **声の印**: 一人称、迷いや推量の表現、機能語の率、名詞化の率
  - LLMで書き直すと、一人称と機能語が減った(van Nuenen, arXiv 2026)[要旨]
  - 指示調整済みのモデルは名詞化が人の1.5〜2倍だった(Reinhart et al. 2025)[要旨]
  - 日本語では、機能語の率だけで人とChatGPTの文章を98.1%判別できた(Zaitsu & Jin 2023)[要旨]
- **視点の復元**: 文章だけを別のAIに読ませ、「書き手はどんな経験をした人か」を答えさせる。素材メモの視点の項目を、何割復元できたかを数える

注意: 声の印は「AIらしくない」を測る。「面白い」を測るわけではない。人の文章でも点が分かれるかを確かめる(初版の注意と同じ)。

### 読みやすさ(迷わず分かる、最後まで読める)

**なぜ測れるか。** 読みやすさは、面白さより先行研究が多い。日本語の式もある。

指標:

- **日本語のリーダビリティ式**: jReadability(Hasebe & Lee 2015、学習者向け)、Obi(Sato et al. 2008、13学年)、建石ら(1988)[要旨]
- **要点の復元**: AIに要点を1文で書かせ、正解の要点との一致を見る
- **読み続ける力**: 段落ごとにAIに「続けて読むか」を二値で答えさせる。判定なので、人の判定との一致率を添える

対象の読者像で結果が変わる。B は、学年で出すObiでは難しい側に出るはずである。第2版の「対象の読者像を決める」を、式の選び方にも当てる。

### 起承転結の4つの要素と、順番の決まり

`conditions.md` の「4つの要素と、順番の決まり1つ」を測る。2段に分ける。

1. **要素がそろっているか(印を付ける)**: 起・承、転、結の位置に印を付ける。AIと私が別々に付け、一致率を出す。転の定義は「起と承で作った予想を外す事実」に固定する
2. **転の時点で、読者が予想を持っているか(AIを測定器にする)**: 転の直前の段落で、AIに結論を予想させる。予想の散らばりが小さく、かつ予想の中心が転の内容から遠ければ、読者は予想を持ったまま転を迎えている。予想の中心が転の内容に近ければ、転は予告済みである

通念を借りる文章(B)では、本文を読ませる前に「この題について、あなたはどう思うか」と答えさせ、それを転の手前の予想とみなす。

順番の決まりが要るかは、次の方法で確かめる。

- 4つの要素を変えずに、段落の順番だけを入れ替えた版を何通りか作る
- 面白さの指標が変わらなければ、要素だけで決まる。変われば、順番の決まりが要る
- A の書き直しは、要素を残して順番を変えた自然な例である。AIの印では面白さが下がった。私の読みで確かめる

## 8条件を測る

| # | 条件 | 測る数値 | 方法 | 主な文献 | 日本語での難しさ |
|---|---|---|---|---|---|
| 1 | 予想から外れ、理由が分かる | 驚き(予測の中心の移動)、納得(確率の前後差) | AIを測定器にする | Ely et al. 2015、Fong et al. 2024、Sui et al. 2026 | 低い。LLMで続きを生成するだけ |
| 2 | 答えの前に問いを置く | 重要な問いの開いている長さ、最初の問いの位置 | AIを測定器にする | Ko et al. 2020、Wu et al. 2024 | 中。逆説を問いとして拾えるかを、私の印で確かめる |
| 3 | 明かす量 | 見出しの具体性(語ごとの抽象度の平均)を、別案と比べる | 文章を数える | Aubin Le Quéré & Matias 2025 | 中。具体性の評定値はないが、抽象度の辞書 AWD-J で代わりにする |
| 4 | 出す順序 | サスペンスの推移。順序を入れ替えた版との差 | AIを測定器にする | Ely et al. 2015、Wilmot & Keller 2020 | 低い |
| 5 | 密度の起伏 | surprisal の移動平均と、段落の境での変化 | 文章を数える | Tsipidi et al. 2024、Kuribayashi et al. 2021 | 中。モデル(llm-jp-3、Swallow、rinna)を複数使う |
| 6 | 型の繰り返し | 隣り合う文の品詞の並びの類似度 | 文章を数える | Menninghaus et al. 2023、Bothwell et al. 2023 | 高い。修辞の対句の資源がない |
| 7 | 具体的な話 | 固有名詞、数字、「たとえば」、呼びかけの数(1,000字あたり)。抽象度の平均 | 文章を数える | Hidi & Baird 1988 | 低い |
| 8 | 寄り道が邪魔しない | 各段落と主題の要約との類似度。遠い段落の数と位置 | 文章を数える | Harp & Mayer 1998 | 低い |

補足:

- **条件3と7の具体性**: 日本語には、語ごとの「具体性」の大規模な評定値が見つからなかった。代わりに AWD-J(NAIST、2019)を使う。人手の評定が15,220語、推定値が約43.7万語ある抽象度の辞書で、CC BY 4.0 である [要旨]
- **条件4の確かめ方**: 同じ文章の段落を入れ替えた版を作り、サスペンスの推移が変わるかを見る。内容が同じで順序だけ違うので、条件4だけを動かせる
- **条件6**: 日本語の修辞の対句を自動で拾う資源は見つからなかった。ラテン語と中国語の検出でも F1 は約0.4だった(Bothwell et al. 2023)[要旨]。当面は印を付ける方法に残す
- **型との関係**: Boyd et al. (2020) は、語のカテゴリの時系列で物語の型を描いた。ただし型への準拠度は人気と無関係だった [要旨]。型を測っても面白さは測れない、という条件6の振り分けと合う

## 物差しが当たっているかを確かめる

**なぜ必要か。** 数値が出ても、それが面白さを表すとは限らない。順位が分かっている文章で試す必要がある。

### #47 の組を使う

#47 には、内容が同じで面白さが違う組がある。

- A、B、D: 原文が面白く、書き直しは面白さが下がった
- C: 両方とも面白くない

物差しは、A、B、D で原文を上に出し、C では差を出さないはずである。差が出なければ、その物差しは使わない。
ただし #47 の順位もAIの印である。先に私が原文と書き直しを伏せて読み、どちらが面白いかを判定する。

### 文章を少しだけ壊して試す

内容を変えずに、1つの条件だけを壊した版を作る。

- 段落を入れ替える(条件4、驚き、サスペンス)
- 結論を冒頭に移す(条件2、好奇心)
- 理由の段落を削る(納得)
- 一人称と迷いを消す(視点の出し方)

壊した条件の指標だけが下がれば、物差しはその条件を測っている。ほかの指標まで動けば、物差しどうしが混ざっている。

### 印の一致率

AIに判定させる指標は、私の判定との一致率を出す。指標には Krippendorff の α を使う。評定者の数や欠損に関わらず使える(Hayes & Krippendorff 2007)[要旨]。

### AIの偏りを避ける

- 文章を書いたAIと、測定器にするAIを分ける(Panickssery et al. 2024)[要旨]
- AIの「面白いか」の点数は補助にとどめる。TTCW の研究では、LLMの判定が専門家と相関しなかった(Chakrabarty et al. 2024)[要旨]
- 一方で、条件を二値のテストに分ける TTCW の設計は借りる。判定を細かく分けるほど、一致率を確かめやすい

## 限界

- 「AIを測定器にする」方法は、AIの予想を読者の予想とみなす。Fong et al. はLLMの期待と人の期待の相関を報告したが、対象は小説である。説明文で同じかは分からない
- AIは人より予想が当たりやすく、裏切りを小さく見積もるかもしれない。Sui (COLM 2026) は、LLMの文章の不確実性が人の文章より低いと報告した [要旨]。測定器のAIにも同じ傾きがありうる
- 1本の文章から言えるのは、やってみ太郎にとっての面白さまでである(初版と同じ)

## 始める順番(案)

1. #47 の4組を、私が伏せて読み、面白さの順位を決める(基準を作る)
2. 「驚き」と「サスペンス」を、A の原文と書き直しで計算する。A の転(72%、段落では第6段落)で驚きが跳ねるかを見る。題を見せる場合と見せない場合の両方で測る。続けて B と D でも測り、それぞれの転で跳ねるかを見る
3. 問いの抽出(条件2)を B で試す。逆説を問いとして拾えるかを、私の印と比べる
4. 条件7と8の数え方を実装する。手間が小さく、壊して試す方法の練習になる
5. surprisal(条件5)は、日本語モデルの用意が要るので最後にする

## 文献

検証状態はすべて [要旨]。全文は読んでいない。著者名の「...」は、確認できた範囲を超える部分である。

- Ely, J., Frankel, A., & Kamenica, E. (2015). Suspense and Surprise. *Journal of Political Economy*, 123(1), 215–260. https://doi.org/10.1086/677350
- Itti, L., & Baldi, P. (2009). Bayesian surprise attracts human attention. *Vision Research*, 49(10), 1295–1306. https://doi.org/10.1016/j.visres.2008.09.007
- Wilmot, D., & Keller, F. (2020). Modelling Suspense in Short Stories as Uncertainty Reduction over Neural Representation. ACL 2020. https://aclanthology.org/2020.acl-main.161/
- Fong, H., Gui, G., & Yang, ... Modeling Story Expectations: A Generative Framework using LLMs. arXiv:2412.15239. https://arxiv.org/abs/2412.15239
- Sui, ... Holtzman, A. Spoiler Alert: Narrative Forecasting as a Metric for Tension in LLM Storytelling. COLM 2026. arXiv:2604.09854
- Sui, ... LLMs Exhibit Significantly Lower Uncertainty in Creative Writing Than Professional Writers. COLM 2026. arXiv:2602.16162
- Xu, W., Jojic, N., Rao, S., Brockett, C., & Dolan, B. (2025). Echoes in AI: Quantifying lack of plot diversity in LLM outputs. *PNAS*, 122(35). https://arxiv.org/abs/2501.00273
- Ko, W.-J., Chen, T., Huang, Y., Durrett, G., & Li, J. J. (2020). Inquisitive Question Generation for High Level Text Comprehension. EMNLP 2020. https://aclanthology.org/2020.emnlp-main.530/
- Westera, M., Mayol, L., & Rohde, H. (2020). TED-Q: TED Talks and the Questions they Evoke. LREC 2020. https://aclanthology.org/2020.lrec-1.141/
- Ko, W.-J., Wu, Y., Dalton, C., Srinivas, D., Durrett, G., & Li, J. J. (2023). Discourse Analysis via Questions and Answers: Parsing Dependency Structures of Questions Under Discussion. Findings of ACL 2023. https://aclanthology.org/2023.findings-acl.710/
- Wu, Y., Mangla, R., Durrett, G., & Li, J. J. (2023). QUDeval: The Evaluation of Questions Under Discussion Discourse Parsing. EMNLP 2023. https://aclanthology.org/2023.emnlp-main.325/
- Wu, Y., Mangla, R., Dimakis, A. G., Durrett, G., & Li, J. J. (2024). Which questions should I answer? Salience Prediction of Inquisitive Questions. EMNLP 2024. https://arxiv.org/abs/2404.10917
- Boyd, R. L., Blackburn, K. G., & Pennebaker, J. W. (2020). The narrative arc: Revealing core narrative structures through text analysis. *Science Advances*, 6(32), eaba2196. https://doi.org/10.1126/sciadv.aba2196
- Chakrabarty, T., Laban, P., Agarwal, D., Muresan, S., & Wu, C.-S. (2024). Art or Artifice? Large Language Models and the False Promise of Creativity. CHI 2024. https://doi.org/10.1145/3613904.3642731
- Lu, X., Sclar, M., ... Choi, Y. AI as Humanity's Salieri: Quantifying Linguistic Creativity of Language Models via Systematic Attribution of Machine Text against Web Text. arXiv:2410.04265. https://arxiv.org/abs/2410.04265
- Panickssery, A., Bowman, S. R., & Feng, S. (2024). LLM Evaluators Recognize and Favor Their Own Generations. NeurIPS 2024. https://arxiv.org/abs/2404.13076
- Zheng, L., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS 2023 Datasets and Benchmarks. https://arxiv.org/abs/2306.05685
- Qiu, L., & Golman, R. (2024). Curiosity in news consumption. *Applied Cognitive Psychology*, 38(2), e4195. https://doi.org/10.1002/acp.4195
- Reinhart, A., et al. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. *PNAS*, 122(8). https://doi.org/10.1073/pnas.2422455122
- van Nuenen, T. (2026). Voice Under Revision. arXiv:2604.22142
- Zaitsu, W., & Jin, M. (2023). *PLOS ONE*. https://doi.org/10.1371/journal.pone.0288453
- Bothwell, S., et al. (2023). Introducing Rhetorical Parallelism Detection. EMNLP 2023. https://arxiv.org/abs/2312.00100
- Hayes, A. F., & Krippendorff, K. (2007). Answering the call for a standard reliability measure for coding data. *Communication Methods and Measures*, 1(1), 77–89. https://doi.org/10.1080/19312450709336664
- Hasebe, Y., & Lee, J.-H. (2015). jReadability. https://jreadability.net/
- Sato, S., Matsuyoshi, S., & Kondoh, Y. (2008). Automatic Assessment of Japanese Text Readability Based on a Textbook Corpus. LREC 2008. https://aclanthology.org/L08-1230/
- 建石由佳・小野芳彦・山田尚勇 (1988). 日本文の読みやすさの評価式. 情報処理学会研究報告 1988-HI-018. https://cir.nii.ac.jp/crid/1570009750935743744
- AWD-J(日本語の語の抽象度辞書). NAIST ソーシャル・コンピューティング研究室 (2019). https://sociocom.naist.jp/awd-j/

初版から引き継いだ文献(Loewenstein 1994、Silvia 2005、Tsipidi et al. 2024、Kuribayashi et al. 2021、Menninghaus et al. 2023、Hidi & Baird 1988、Harp & Mayer 1998、Aubin Le Quéré & Matias 2025、Doshi & Hauser 2024)の書誌は、#45 の資料にある。
