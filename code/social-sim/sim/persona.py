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


def _quota(rng, attr, n):
    """{"quota": {"値": 割合, ...}} を、n 人に割合どおり(最大剰余法)に割り振り、順を混ぜる。"""
    items = list(attr["quota"].items())
    total = sum(w for _, w in items)
    exact = [(v, w / total * n) for v, w in items]
    counts = {v: int(x) for v, x in exact}
    rest = n - sum(counts.values())
    for v, x in sorted(exact, key=lambda t: t[1] - int(t[1]), reverse=True)[:rest]:
        counts[v] += 1
    vals = [v for v, c in counts.items() for _ in range(c)]
    rng.shuffle(vals)
    return vals


def generate(spec, n, seed):
    rng = random.Random(seed)
    quotas = {name: _quota(rng, attr, n) for name, attr in spec["attributes"].items() if "quota" in attr}
    people = []
    for i in range(n):
        p = {"id": f"p{i:03d}"}
        for name, attr in spec["attributes"].items():
            p[name] = quotas[name][i] if name in quotas else _draw(rng, attr)
        people.append(p)
    return people


def describe(person, spec):
    """人物像を、プロンプトに入れる短い文にする。texts があれば、値を文に置き換えてから埋める。"""
    vals = dict(person)
    for name, table in spec.get("texts", {}).items():
        vals[name] = table[person[name]]
    return spec["template"].format(**vals)


def diversity(people, spec):
    """属性ごとに、定義の割合と作った集団の割合を並べる。重なり具合も数える。"""
    report = {}
    n = len(people)
    for name, attr in spec["attributes"].items():
        got = Counter(p[name] for p in people)
        dist = attr.get("choices") or attr.get("quota")
        if dist:
            total = sum(dist.values())
            report[name] = {v: {"spec": round(w / total, 3), "got": round(got[v] / n, 3)}
                            for v, w in dist.items()}
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
