"""Nightly re-check of every agent's official page.
Fetches each URL, extracts a few facts (title, prices seen, security claims seen, acquisition/shutdown words),
compares with the last snapshot in catalog-data/snapshots, updates verification.checked_on, and writes
catalog-data/CHANGES.md for the pull request body. Standard library only. Run from the repo root."""
import json, re, pathlib, datetime, urllib.request, html, hashlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
cat = root / "agent-market" / "catalog" / "agents.json"
snaps = root / "catalog-data" / "snapshots"; snaps.mkdir(parents=True, exist_ok=True)
today = datetime.date.today().isoformat()
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36 AgentMarketBot/1.0 (+https://github.com/bhavya-gx/agent-market)"}
SEC = ["SOC 2", "SOC2", "ISO 27001", "ISO 42001", "HIPAA", "GDPR", "FedRAMP"]
EVENTS = ["acquired", "acquisition", "joins", "now part of", "shutting down", "sunset", "discontinued", "rebrand", "renamed"]

def fetch(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
            return r.status, r.geturl(), r.read(400_000).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e: return e.code, url, ""
    except Exception as e: return 0, url, ""

def facts(page):
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", page, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text)); text = re.sub(r"\s+", " ", text)
    title = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
    prices = sorted(set(re.findall(r"(?:\$|€|£)\s?\d{1,4}(?:[.,]\d{2})?(?:\s?/\s?(?:mo|month|user|seat|yr|year))?", text)))[:12]
    return {"title": html.unescape(title.group(1)).strip()[:120] if title else None,
            "prices": prices,
            "security": [s for s in SEC if s.lower() in text.lower()],
            "events": sorted({w for w in EVENTS if re.search(r"\b" + w + r"\b", text, re.I)}),
            "words": len(text.split()), "hash": hashlib.sha1(text.lower().encode()).hexdigest()[:12]}

data = json.loads(cat.read_text()); changes, blocked = [], []
for a in data["agents"]:
    status, final, page = fetch(a["url"])
    snap = snaps / f"{a['id']}.json"
    old = json.loads(snap.read_text()) if snap.exists() else None
    if status != 200 or len(page) < 500:
        blocked.append(f"- {a['name']}: HTTP {status or 'no response'}")
        a["verification"]["status"] = "blocked" if a["verification"]["status"] != "page_read" else "page_read"
        continue
    new = {"checked": today, "status": status, "final_url": final, **facts(page)}
    diff = []
    if old:
        if set(new["prices"]) != set(old.get("prices", [])): diff.append(f"prices seen: {old.get('prices')} -> {new['prices']}")
        if new["security"] != old.get("security"): diff.append(f"security claims seen: {old.get('security')} -> {new['security']}")
        if new["events"] != old.get("events"): diff.append(f"event words: {old.get('events')} -> {new['events']}")
        if new["title"] != old.get("title"): diff.append(f"title: {old.get('title')!r} -> {new['title']!r}")
        if final.rstrip("/") != old.get("final_url", "").rstrip("/"): diff.append(f"redirects to {final}")
    snap.write_text(json.dumps(new, indent=1))
    a["verification"].update({"status": "page_read", "checked_on": today, "source": "official site"})
    if diff: changes.append(f"### {a['name']} ({a['url']})\n" + "\n".join(f"- {d}" for d in diff))
data["updated"] = today
cat.write_text(json.dumps(data, indent=2) + "\n")
body = [f"# Re-check {today}", f"{len(data['agents']) - len(blocked)} pages read, {len(blocked)} blocked.", ""]
body += ["## Changes to review"] + (changes or ["None."]) + ["", "## Blocked"] + (blocked or ["None."])
body += ["", "Dates were refreshed automatically. Prices and claims in the catalog are not changed by this job; edit them by hand after reading the diff."]
(root / "catalog-data" / "CHANGES.md").write_text("\n".join(body) + "\n")
print("\n".join(body))
