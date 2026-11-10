"""Check catalog/agents.json for required fields and allowed values. Run: python3 scripts/validate.py"""
import json, sys, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / "which-agent" / "catalog" / "agents.json"
data = json.loads(p.read_text())
REQ = ["id","name","category","url","summary","use_cases","tech_level","hosting","verification"]
ALLOWED = {"tech_level":{"no-code","tutorial","terminal"},"hosting":{"hosted","self-hosted","either"},
           "use_cases":{"inbox","meetings","admin","content","research","sales","build"},
           "status":{"page_read","blocked","unchecked"},"works_alongside":{"both","add-on","is-an-llm"}}
errs, ids = [], set()
for a in data["agents"]:
    n = a.get("id","?")
    for k in REQ:
        if a.get(k) in (None, "", []): errs.append(f"{n}: missing {k}")
    if n in ids: errs.append(f"{n}: duplicate id")
    ids.add(n)
    if not str(a.get("url","")).startswith("https://"): errs.append(f"{n}: url must start with https://")
    for k in ("tech_level","hosting","works_alongside"):
        if a.get(k) not in ALLOWED[k]: errs.append(f"{n}: bad {k} {a.get(k)!r}")
    for u in a.get("use_cases",[]):
        if u not in ALLOWED["use_cases"]: errs.append(f"{n}: bad use case {u!r}")
    v = a.get("verification") or {}
    if v.get("status") not in ALLOWED["status"]: errs.append(f"{n}: bad verification status")
    if v.get("status") == "page_read" and not v.get("checked_on"): errs.append(f"{n}: page_read needs checked_on")
print("\n".join(errs) or f"OK, {len(data['agents'])} agents")
sys.exit(1 if errs else 0)
