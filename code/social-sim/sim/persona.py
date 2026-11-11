"""人物像をつくる部品。分布の定義(JSON)から、架空の人物を seed つきで作る。

人物像が似通うと答えも似通うため、作った集団の分布を数えて、定義と比べられるようにする。
"""
import json
import math
import random
from collections import Counter


def load_spec(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _draw(rng, attr):
    if "choices" in attr:                  # {"choices": {"値": 重み, ...}}
        vals, weights = zip(*attr["choices"].items())
        return rng.choices(vals, weights)[0]
    if "range" in attr:                    # {"range": [下限, 上限]} の整数
        lo, hi = attr["range"]
        return rng.randint(lo, hi)
    raise ValueError(f"分布の書き方が分からない: {attr}")


def generate(spec, n, seed):
    rng = random.Random(seed)
    people = []
    for i in range(n):
        p = {"id": f"p{i:03d}"}
        for name, attr in spec["attributes"].items():
            p[name] = _draw(rng, attr)
        people.append(p)
    return people


def describe(person, spec):
    """人物像を、プロンプトに入れる短い文にする。"""
    return spec["template"].format(**person)


def diversity(people, spec):
    """属性ごとに、定義の割合と作った集団の割合を並べる。重なり具合も数える。"""
    report = {}
    n = len(people)
    for name, attr in spec["attributes"].items():
        got = Counter(p[name] for p in people)
        if "choices" in attr:
            total = sum(attr["choices"].values())
            report[name] = {v: {"spec": round(w / total, 3), "got": round(got[v] / n, 3)}
                            for v, w in attr["choices"].items()}
        else:
            vals = [p[name] for p in people]
            report[name] = {"min": min(vals), "max": max(vals),
                            "mean": round(sum(vals) / n, 1)}
    keys = [tuple(p[k] for k in spec["attributes"]) for p in people]
    report["_unique_ratio"] = round(len(set(keys)) / n, 3)
    return report


def entropy(values):
    """答えのばらつき。全員が同じ答えなら0になる。"""
    c = Counter(values)
    n = sum(c.values())
    return round(abs(sum(v / n * math.log2(v / n) for v in c.values())), 3)
