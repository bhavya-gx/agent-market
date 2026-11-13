"""Merges verified candidate JSON (from the page-reading agents) into the catalog. Usage: python3 scripts/merge_results.py /tmp/am/result*.json"""
import json, re, sys, pathlib, datetime
root = pathlib.Path(__file__).resolve().parent.parent; cat = root / "agent-market" / "catalog" / "agents.json"
data = json.loads(cat.read_text()); have = {a["id"] for a in data["agents"]} | {a["name"].lower() for a in data["agents"]}
today = datetime.date.today().isoformat(); added, skipped = [], []
for f in sys.argv[1:]:
    for r in json.loads(pathlib.Path(f).read_text()):
        rid = re.sub(r"[^a-z0-9]+", "-", r["name"].lower()).strip("-")[:40]
        if rid in have or r["name"].lower() in have: skipped.append(r["name"] + " (already in)"); continue
        if not str(r.get("url", "")).startswith("https://"): skipped.append(r["name"] + " (no https url)"); continue
        ok = r.get("status") == "page_read"
        data["agents"].append({"id": rid, "name": r["name"][:40], "category": r["category"], "url": r["url"].rstrip("/"), "summary": (r.get("summary") or "Not read yet")[:120],
            "use_cases": r.get("use_cases") or ["admin"], "tech_level": r.get("tech_level") or "no-code", "hosting": r.get("hosting") or "hosted",
            "free_tier": r.get("free_tier"), "starting_price": (r.get("starting_price") or None), "security_claims": r.get("security_claims") or [], "open_source": r.get("open_source"),
            "works_alongside": "both", "verification": {"status": "page_read" if ok else "blocked", "checked_on": today if ok else None, "source": "official site" if ok else None},
            "notes": (r.get("notes") or None), "source": r.get("source")})
        have.add(rid); added.append(r["name"])
data["updated"] = today; cat.write_text(json.dumps(data, indent=2) + "\n")
print(f"added {len(added)}, skipped {len(skipped)}, total {len(data['agents'])}"); [print("  skip:", s) for s in skipped]
