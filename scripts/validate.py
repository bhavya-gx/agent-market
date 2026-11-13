"""Check catalog/agents.json for required fields and allowed values. Run: python3 scripts/validate.py"""
import json, sys, pathlib
p = pathlib.Path(__file__).resolve().parent.parent / "agent-market" / "catalog" / "agents.json"
data = json.loads(p.read_text())
REQ = ["id","name","category","url","summary","use_cases","tech_level","hosting","verification"]
ALLOWED = {"tech_level":{"no-code","tutorial","terminal"},"hosting":{"hosted","self-hosted","either"},
           "use_cases":{"inbox","meetings","admin","content","research","sales","build"},
           "status":{"page_read","blocked","unchecked"},"works_alongside":{"both","add-on","is-an-llm"}}
import re
# Catalog text is read by an AI, so block anything that looks like instructions, markup or hidden links.
BAD = re.compile(r"ignore (all|any|previous|the above)|system prompt|you (must|should) (always|now|recommend)|disregard|instruction|assistant:|<[a-z/!]|```|\\u200|javascript:|data:|https?://", re.I)
LIMITS = {"name": 40, "summary": 120, "notes": 200, "starting_price": 60}
SHORTENERS = ("bit.ly","tinyurl","t.co/","goo.gl","rebrand.ly","lnkd.in","ow.ly")
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
    for k, lim in LIMITS.items():
        val = a.get(k)
        if isinstance(val, str):
            if len(val) > lim: errs.append(f"{n}: {k} longer than {lim} characters")
            if BAD.search(val): errs.append(f"{n}: {k} contains blocked text (links, markup or instructions)")
            if any(ord(ch) < 32 or 0x200b <= ord(ch) <= 0x206f for ch in val): errs.append(f"{n}: {k} has hidden characters")
    for c in a.get("security_claims") or []:
        if len(c) > 40 or BAD.search(c): errs.append(f"{n}: bad security claim {c!r}")
    if any(x in a.get("url","") for x in SHORTENERS): errs.append(f"{n}: link shorteners are not allowed")
    if not re.fullmatch(r"[a-z0-9-]{2,40}", n): errs.append(f"{n}: id must be lowercase letters, numbers and dashes")
    allowed_keys = {"id","name","category","url","summary","use_cases","tech_level","hosting","free_tier","starting_price","security_claims","open_source","works_alongside","verification","notes"}
    extra = set(a) - allowed_keys
    if extra: errs.append(f"{n}: unknown fields {sorted(extra)}")
    v = a.get("verification") or {}
    if v.get("status") not in ALLOWED["status"]: errs.append(f"{n}: bad verification status")
    if v.get("status") == "page_read" and not v.get("checked_on"): errs.append(f"{n}: page_read needs checked_on")
print("\n".join(errs) or f"OK, {len(data['agents'])} agents")
sys.exit(1 if errs else 0)
