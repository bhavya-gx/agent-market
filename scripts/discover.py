"""Finds new AI agents from public launch feeds and writes them to catalog-data/queue/<date>.json as candidates.
Sources: Hacker News (Show HN), GitHub (recent agent repos), Product Hunt RSS, Y Combinator launches.
Nothing enters the catalog from here; a maintainer reviews the queue. Standard library only.
Usage: python3 scripts/discover.py [days=1]"""
import json, re, sys, pathlib, datetime, urllib.request, urllib.parse, html, time
root = pathlib.Path(__file__).resolve().parent.parent
cat = json.loads((root / "agent-market" / "catalog" / "agents.json").read_text())
days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
UA = {"User-Agent": "AgentMarketBot/1.0 (+https://github.com/bhavya-gx/agent-market)", "Accept": "application/json, text/xml, */*"}
KEY = re.compile(r"\bagent(s|ic)?\b|\bassistant\b|\bcopilot\b|\bautopilot\b|\bautomat", re.I)
NEWS = {"cbsnews.com","wired.com","arstechnica.com","euronews.com","tomshardware.com","the-decoder.com","theverge.com","techcrunch.com","nytimes.com","bloomberg.com","reuters.com","bbc.com","cnbc.com","forbes.com","businessinsider.com","medium.com","substack.com","anthropic.com","openai.com"}
NOISE = re.compile(r"framework|sdk|library|benchmark|paper|tutorial|course|awesome|list of|template|boilerplate|protocol|\bmcp server\b", re.I)
def get(url, as_json=True):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
            b = r.read().decode("utf-8", "ignore"); return json.loads(b) if as_json else b
    except Exception as e:
        print(f"  skip {url.split('/')[2]}: {e}", file=sys.stderr); return None
def domain(u):
    try: return urllib.parse.urlparse(u).netloc.lower().removeprefix("www.")
    except Exception: return ""
known = {domain(a["url"]) for a in cat["agents"]} | {a["name"].lower() for a in cat["agents"]}
found = {}
def add(name, url, source, score, blurb):
    if not name or not url: return
    d = domain(url)
    if not d or d in known or name.lower() in known: return
    if d in NEWS: return
    if d in ("github.com", "news.ycombinator.com", "ycombinator.com", "x.com", "twitter.com", "gist.github.com") and source != "GitHub": return
    if source == "GitHub" and d == "github.com" and score < 2000: return  # repo-only projects without a product site are developer tools
    if not KEY.search(name + " " + blurb) or NOISE.search(name + " " + blurb): return
    k = d if source != "GitHub" else url
    if k in found and found[k]["score"] >= score: return
    found[k] = {"name": name.strip()[:60], "url": url, "source": source, "score": score, "blurb": re.sub(r"\s+", " ", html.unescape(blurb)).strip()[:160]}

# 1. Hacker News, Show HN and front page posts mentioning agents
hn = get(f"https://hn.algolia.com/api/v1/search_by_date?query=agent&tags=story&numericFilters=created_at_i>{int(since.timestamp())},points>20&hitsPerPage=100")
for h in (hn or {}).get("hits", []):
    t = re.sub(r"^Show HN:\s*", "", h.get("title", "")); m = re.match(r"([^–\-:(]{2,40})[\s–\-:(]", t)
    add(m.group(1).strip() if m else t[:40], h.get("url") or "", "Hacker News", int(h.get("points", 0)), t)
# 2. GitHub, agent repos created in the window with real traction
gh = get(f"https://api.github.com/search/repositories?q=ai+agent+in:name,description+created:>{since.date()}+stars:>100&sort=stars&order=desc&per_page=50")
for r in (gh or {}).get("items", []):
    home = r.get("homepage") or r["html_url"]
    add(r["name"], home, "GitHub", int(r["stargazers_count"]), r.get("description") or "")
# 3. Product Hunt RSS
ph = get("https://www.producthunt.com/feed?category=artificial-intelligence", as_json=False) or get("https://www.producthunt.com/feed", as_json=False)
for e in re.findall(r"<entry>(.*?)</entry>", ph or "", re.S):
    t = re.search(r"<title[^>]*>(.*?)</title>", e, re.S); l = re.search(r'<link[^>]*href="([^"]+)"', e); c = re.search(r"<content[^>]*>(.*?)</content>", e, re.S); p = re.search(r"<published>(.*?)</published>", e)
    if p and datetime.datetime.fromisoformat(p.group(1).replace("Z", "+00:00")) < since: continue
    add(html.unescape(t.group(1)) if t else "", l.group(1) if l else "", "Product Hunt", 0, html.unescape(re.sub(r"<[^>]+>", " ", c.group(1))) if c else "")
# 4. Y Combinator launches, via "Launch HN" posts (YC publishes no launches feed)
yc = get(f"https://hn.algolia.com/api/v1/search_by_date?query=%22Launch%20HN%22&tags=story&numericFilters=created_at_i>{int(since.timestamp())}&hitsPerPage=100")
for h in (yc or {}).get("hits", []):
    t = h.get("title", "")
    if not t.startswith("Launch HN"): continue
    m = re.match(r"Launch HN:\s*([^(–\-:]+)", t)
    add(m.group(1).strip() if m else t, h.get("url") or "", "YC Launches", int(h.get("points", 0)), t)

out = sorted(found.values(), key=lambda x: -x["score"])
q = root / "catalog-data" / "queue"; q.mkdir(parents=True, exist_ok=True)
(q / f"{datetime.date.today().isoformat()}.json").write_text(json.dumps(out, indent=1))
print(f"{len(out)} candidates over {days} days")
for c in out: print(f"- {c['name']} | {c['url']} | {c['source']} | {c['score']} | {c['blurb']}")
