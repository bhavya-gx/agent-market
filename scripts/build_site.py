"""Generates the public Agent Market site into site/ from the catalog: one page per agent, a filterable index,
sitemap.xml, llms.txt, robots.txt, a change log and a copy of the catalog. Standard library only."""
import json, pathlib, html, datetime, shutil
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "agent-market" / "catalog" / "agents.json").read_text())
out = root / "site"; shutil.rmtree(out, ignore_errors=True); (out / "agents").mkdir(parents=True)
BASE = "https://agent-market-orpin.vercel.app"
today = datetime.date.today().isoformat()
e = html.escape
CAT = {"coding": "Coding", "general-agent": "General agents", "workflow-automation": "Workflow automation", "meetings": "Meetings", "content": "Content", "personal-assistant": "Personal assistants", "browser-agent": "Browser agents", "inbox": "Inbox", "calendar": "Calendar", "sales": "Sales", "research": "Research"}
CSS = """
:root{--ink:#1b1430;--muted:#6b6280;--line:#ece6f7;--acc:#4c6bff;--acc2:#eef1ff;--ok:#1a8cff;--bg:#fff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Poppins,system-ui,sans-serif;line-height:1.55}
.wrap{max-width:1040px;margin:0 auto;padding:28px max(16px,env(safe-area-inset-left)) 60px}
header{display:flex;align-items:center;gap:12px;flex-wrap:wrap}header a{color:inherit;text-decoration:none}
.mark{width:34px;height:34px;border-radius:10px;background:var(--acc);color:#fff;display:grid;place-items:center;font-weight:800}
h1{font-size:clamp(1.8rem,5vw,2.6rem);margin:28px 0 8px;line-height:1.1}h2{font-size:1.3rem;margin:28px 0 10px}
p{margin:0 0 10px}.lead{color:var(--muted);max-width:62ch}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}.filters button{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:7px 13px;font:inherit;font-size:.9rem;cursor:pointer}
.filters button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.card{border:1.5px solid var(--line);border-radius:16px;padding:16px;display:grid;gap:6px;text-decoration:none;color:inherit}
.card:hover{border-color:var(--acc)}.card b{font-size:1.05rem;display:flex;align-items:center;gap:6px}.card small{color:var(--muted)}
.chk{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;background:var(--ok);color:#fff;font-size:.65rem;font-weight:800}
.facts{display:grid;grid-template-columns:max-content 1fr;gap:8px 18px;border:1.5px solid var(--line);border-radius:16px;padding:18px;margin:18px 0}
.facts dt{color:var(--muted);font-size:.9rem}.facts dd{margin:0}
.r{color:#a8302a}
footer{margin-top:40px;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line);padding-top:16px}
a{color:var(--acc)}
"""


def page(title, body, desc, path, extra_head=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap"><style>{CSS}</style>{extra_head}</head>
<body><div class="wrap"><header><a href="/" style="display:flex;align-items:center;gap:10px"><span class="mark">A</span><b>Agent Market</b></a>
<span style="color:var(--muted)">·</span><a href="/#catalog">Catalog</a><a href="/changelog/">Change log</a><a href="https://github.com/bhavya-gx/agent-market">GitHub</a></header>
{body}
<footer>Free and open source, MIT licensed. Nobody pays to be listed or ranked. "Page checked" means someone read the vendor's own page on that date; it never means the agent was tested. Catalog updated {e(data.get('updated', today))}.</footer></div></body></html>"""


cards = []
for a in data["agents"]:
    v = a["verification"]; ok = v["status"] == "page_read"
    free = "free tier" if a["free_tier"] else "no free tier" if a["free_tier"] is False else "free tier unknown"
    price = (" · from " + e(a["starting_price"])) if a["starting_price"] else ""
    cards.append(f"""<a class="card" href="/agents/{a['id']}/" data-cat="{a['category']}"><b>{e(a['name'])}{' <span class="chk">✓</span>' if ok else ''}</b><span>{e(a['summary'])}</span><small>{e(CAT.get(a['category'], a['category']))} · {free}{price}</small></a>""")
    sec = ", ".join(a["security_claims"]) or "none found on the page"
    ld = json.dumps({"@context": "https://schema.org", "@type": "SoftwareApplication", "name": a["name"], "url": a["url"], "description": a["summary"], "applicationCategory": CAT.get(a["category"]), "offers": {"@type": "Offer", "price": "0" if a["free_tier"] else None, "description": a["starting_price"]}})
    verif = ("Official page checked on " + e(v["checked_on"])) if ok else ("Site blocked the check" if v["status"] == "blocked" else "Not checked yet")
    body = f"""<h1>{e(a['name'])}{' <span class="chk" style="width:26px;height:26px;font-size:.9rem;vertical-align:middle">✓</span>' if ok else ''}</h1>
<p class="lead">{e(a['summary'])}</p><p><a href="{e(a['url'])}" rel="noopener">{e(a['url'].replace('https://', ''))}</a></p>
<dl class="facts"><dt>Category</dt><dd>{e(CAT.get(a['category'], a['category']))}</dd><dt>Good for</dt><dd>{e(', '.join(a['use_cases']))}</dd>
<dt>Setup</dt><dd>{e(a['tech_level'])} · {e(a['hosting'])}</dd><dt>Free tier</dt><dd>{'Yes' if a['free_tier'] else 'No' if a['free_tier'] is False else 'Not listed'}</dd>
<dt>Starting price</dt><dd>{e(a['starting_price'] or 'Not listed')}</dd><dt>Security claims</dt><dd>{e(sec)}</dd><dt>Open source</dt><dd>{'Yes' if a['open_source'] else 'No'}</dd>
<dt>Works with your chat</dt><dd>{e(a['works_alongside'])}</dd><dt>Verification</dt><dd>{verif}</dd></dl>
{('<p class="r"><b>Red flag:</b> ' + e(a['notes']) + '</p>') if a.get('notes') else ''}
<p><a href="https://github.com/bhavya-gx/agent-market/blob/main/agent-market/catalog/agents.json">Correct this entry on GitHub</a></p>"""
    d = out / "agents" / a["id"]; d.mkdir()
    (d / "index.html").write_text(page(f"{a['name']} · Agent Market", body, a["summary"], f"/agents/{a['id']}/", f'<script type="application/ld+json">{ld}</script>'))

cats = sorted({a["category"] for a in data["agents"]}, key=lambda c: -sum(1 for a in data["agents"] if a["category"] == c))
filters = '<button aria-pressed="true" data-f="all">All</button>' + "".join(f'<button aria-pressed="false" data-f="{c}">{e(CAT.get(c, c))}</button>' for c in cats)
index = f"""<h1>Which AI agent fits your work?</h1><p class="lead">{len(data['agents'])} agents, every one checked against its own official page, with the date it was checked. No listing can be bought.</p>
<p><a href="https://github.com/bhavya-gx/agent-market">Install the skill</a> and your chat recommends these as you work.</p>
<div class="filters" id="catalog">{filters}</div><div class="grid">{''.join(cards)}</div>
<script>document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.filters button').forEach(x=>x.setAttribute('aria-pressed',x==b));document.querySelectorAll('.card').forEach(c=>c.style.display=(b.dataset.f=='all'||c.dataset.cat==b.dataset.f)?'':'none')}})</script>"""
(out / "index.html").write_text(page("Agent Market", index, "Open directory of AI agents, each checked against its official page. Free, open source, no pay-to-play.", "/"))
ch = root / "catalog-data" / "CHANGES.md"
log = e(ch.read_text()) if ch.exists() else "No checks recorded yet."
(out / "changelog").mkdir(); (out / "changelog" / "index.html").write_text(page("Change log · Agent Market", f"<h1>Change log</h1><pre style='white-space:pre-wrap;font-family:inherit'>{log}</pre>", "What changed on the official pages at the last nightly check.", "/changelog/"))
(out / "catalog.json").write_text(json.dumps(data, indent=1))
urls = [f"{BASE}/", f"{BASE}/changelog/"] + [f"{BASE}/agents/{a['id']}/" for a in data["agents"]]
(out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>")
(out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
lines = [f"- [{a['name']}]({BASE}/agents/{a['id']}/): {a['summary']}. {CAT.get(a['category'])}. {'Free tier. ' if a['free_tier'] else ''}{('From ' + a['starting_price'] + '. ') if a['starting_price'] else ''}Page checked {a['verification']['checked_on'] or 'never'}." for a in data["agents"]]
(out / "llms.txt").write_text(f"# Agent Market\n\n> Open directory of {len(data['agents'])} AI agents, each checked against its official page. Free, open source, no paid listings. Catalog JSON: {BASE}/catalog.json\n\n## Agents\n\n" + "\n".join(lines) + "\n\n## Source\n\n- GitHub: https://github.com/bhavya-gx/agent-market\n")
print(f"site: {len(data['agents'])} agent pages, {len(urls)} urls")
