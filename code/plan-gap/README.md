# 計画と提供のずれを見つけさせる(#156)

架空の訪問介護事業所の書類(ケアプラン・訪問介護計画書・サービス提供記録)を AI に点検させ、仕込んだ不備を見つけられるかを測る。すべて架空のデータ。

## 手順

```bash
python3 make_world.py            # v1: data/(不備の人にも変更の特記事項あり)
python3 make_world.py --hard     # v2: data-v2/(不備の人には特記事項なし)
python3 make_office.py           # v3: data-v3/(計画24人分と、全員の実績を日付順の CSV に)

DATA=data-v2 python3 run_check.py sonnet list 1      # 1人ずつ。mode は list(観点あり)か free(観点なし)
DATA=data-v3 python3 run_check.py opus list all1     # all で始まる run は、全員分を1回で渡す
DATA=data-v2 python3 score.py sonnet-list-1 opus-list-1
```

- AI の呼び出しは `claude -p`(道具なし)
- `data*/answers.json` が仕込んだ不備とひっかけの正解。AI には渡さない
- 採点は、指摘が正解と同じものかを opus に判定させる(`data*/judge/`)。ひっかけと問題なしの人への指摘は、すべて誤検知と数える
