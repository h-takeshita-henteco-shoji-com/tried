"""その月の要点を1画面で出す(#124)。python3 month_summary.py <運営のフォルダ> <月>"""
import json, sys
R, m = sys.argv[1], int(sys.argv[2])
d = json.load(open(f"{R}/council/m{m:02d}-run.json"))
props = [x for b in d.get("proposals", []) for x in (b or {}).get("proposals", [])]
bill = d.get("bill") or {}
dn = d.get("done") or {}
print(f"案{len(props)} 採{len(bill.get('measures', []))} 却下{[(r['proposal'], r['kind']) for r in bill.get('rejected', [])]} "
      f"レビュー{len(d.get('planReviews') or [])} 再調査{[x['bureau'] for x in (d.get('rechecks') or []) if x]}")
print("議会", [(r["measureId"], r["verdict"], r["point"]) for r in (d.get("ruling") or {}).get("rulings", []) if r["verdict"] == "否決"] or "否決なし",
      "plan", (d.get("planCheck") or {}).get("verdict"))
print("実行", dn.get("executed"), "失敗", dn.get("failed"))
for f in dn.get("failedReasons", []):
    print("  -", f["id"], f["reason"][:150])
print("見回り", [(p["gameDate"], p["population"], p["weeklyBalance"]) for p in dn.get("patrols", [])], "臨時", dn.get("emergency"))
print((dn.get("report") or "")[-420:])
