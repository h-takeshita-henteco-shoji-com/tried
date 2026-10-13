"""文ごとのサプライザル(1文字あたり)を、3つの言語モデルで出す。

各文について、それより前の本文(題を含む)を全部与えたうえで、その文のトークンの
サプライザル(-log2 p)を合計し、文の文字数で割る。
一度に読める長さを超える文章は、窓をずらしながら測る。

使い方: python surprisal.py <texts_dir> <out.tsv>
"""
import glob
import math
import os
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, os.path.dirname(__file__))
from segment import load  # noqa: E402

MODELS = {
    "llmjp": "llm-jp/llm-jp-3-1.8b",
    "sarashina": "sbintuitions/sarashina2.2-1b",
    "rinna": "rinna/japanese-gpt2-medium",
}
DEVICE = os.environ.get("YARDSTICK_DEVICE", "cpu")  # MPS は転送と計算が止まったため、既定を CPU にした


def build(doc):
    """全文の文字列と、各文の文字範囲を作る。段落の間は改行でつなぐ。"""
    text = doc["title"] + "\n"
    spans = []
    prev_par = None
    for s in doc["sents"]:
        if prev_par is not None and s["par"] != prev_par:
            text += "\n"
        start = len(text)
        text += s["text"]
        spans.append((start, len(text)))
        prev_par = s["par"]
    return text, spans


def token_surprisals(tok, model, text, max_len):
    enc = tok(text, return_offsets_mapping=True, add_special_tokens=False)
    ids = enc["input_ids"]
    offs = enc["offset_mapping"]
    bos = tok.bos_token_id if tok.bos_token_id is not None else tok.eos_token_id
    ids = [bos] + ids
    sur = [None] * len(ids)
    stride = max_len // 2
    # 窓 [b, e) で、前半の文脈を与えて後半のトークンを測る
    done = 1
    b = 0
    while done < len(ids):
        e = min(len(ids), b + max_len)
        x = torch.tensor([ids[b:e]], device=DEVICE)
        with torch.no_grad():
            logp = torch.log_softmax(model(x).logits[0].float(), -1)
        for t in range(max(done, b + 1), e):
            sur[t] = -logp[t - b - 1, ids[t]].item() / math.log(2)
        done = e
        b = e - stride if e < len(ids) else e
    return list(zip(offs, sur[1:]))


def main(texts_dir, out):
    docs = {os.path.basename(f)[:-4]: load(f) for f in sorted(glob.glob(f"{texts_dir}/*.txt"))}
    rows = []
    for key, name in MODELS.items():
        tok = AutoTokenizer.from_pretrained(name)
        model = AutoModelForCausalLM.from_pretrained(name, dtype=torch.float32).to(DEVICE)
        model.train(False)
        max_len = min(getattr(model.config, "max_position_embeddings", 1024) or 1024, 2048)
        for doc_id, doc in docs.items():
            text, spans = build(doc)
            ts = token_surprisals(tok, model, text, max_len)
            for s, (a, z) in zip(doc["sents"], spans):
                total = sum(v for (o, v) in ts if a <= o[0] < z)
                rows.append((key, doc_id, s["id"], s["par"], s["len"], total / max(s["len"], 1)))
            print(key, doc_id, "done", file=sys.stderr)
        del model
        if DEVICE == "mps":
            torch.mps.empty_cache()
    with open(out, "w") as f:
        f.write("model\tdoc\tsent\tpar\tlen\tsurprisal_per_char\n")
        for r in rows:
            f.write("\t".join(map(str, r[:5])) + f"\t{r[5]:.4f}\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
