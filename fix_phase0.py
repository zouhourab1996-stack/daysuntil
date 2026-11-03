#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PHASE 0 technical fixes on trustscore per expert plan:
1) prostavive rel compliance  2) per-page ClickBank tids  3) titles ≤60 (12 new + suffix strip)
4) BreadcrumbList on 12 new pages  5) author (Organization) in Article schema
6) top CTA + disclosure after glance box  7) noindex 9 thin YMYL marketplace pages
8) remove noindexed URLs from sitemap"""
import re, glob, json

AFF = 'https://go.fiverr.com/visit/?bta=1177474&amp;brand=fiverrmarketplace'

NEW_TITLES = {
 "costs/ai-agent-development": "AI Agent Development Cost 2026: $500 vs $75,000",
 "costs/shopify-store": "Shopify Store Cost 2026: $100 Store vs $50,000 Build",
 "costs/mobile-app-development": "Mobile App Development Cost 2026: $500 or $150,000",
 "compare/fiverr-vs-99designs": "Fiverr vs 99designs 2026: $25 Gig vs $299 Contest",
 "compare/fiverr-logo-maker-vs-designer": "Fiverr Logo Maker vs Designer 2026: $30 vs $25",
 "compare/upwork-alternatives": "7 Best Upwork Alternatives 2026: Real Costs",
 "compare/99designs-alternatives": "5 Cheaper 99designs Alternatives 2026 (From $10)",
 "guides/fiverr-for-etsy-sellers": "Fiverr for Etsy Sellers 2026: 6 Gigs Worth Buying",
 "guides/fiverr-for-podcasters": "Fiverr for Podcasters 2026: Verified Prices",
 "guides/fiverr-for-youtube-channels": "Faceless YouTube Stack on Fiverr, Priced 2026",
 "guides/how-to-hire-on-fiverr": "How to Hire on Fiverr 2026: Fees, Escrow, 9-Step Vet",
 "guides/how-to-write-a-design-brief": "Design Brief Template 2026: 7 Parts + 3 Examples",
}
NOINDEX = ["javaburn", "citrusburn", "mitolyn", "yogaburn", "sugardefender",
           "glucofort", "amiclear", "cortexi", "gluco6"]

def shortslug(path):
    s = path.rstrip("/").split("/")[-1]
    s = re.sub(r"-marketplace$|-review$", "", s)
    s = re.sub(r"[^a-z0-9]", "", s.lower())
    return ("tsb" + s)[:24]

# ---------- 1) prostavive rel fix ----------
p = "reviews/prostavive-review/index.html"
s = open(p, encoding="utf-8").read()
n = 0
for pat in ['<a class="cta" data-vendor="prostavive"', '<a data-vendor="prostavive"']:
    c = s.count(pat)
    s = s.replace(pat, pat.replace("<a ", '<a rel="sponsored nofollow noopener" '), 1) if c else s
    n += c
open(p, "w", encoding="utf-8").write(s)
print(f"✓ prostavive: rel added to {n} anchors")

# ---------- 2) per-page ClickBank tids ----------
fixed = 0
for f in glob.glob("**/index.html", recursive=True):
    if ".git" in f: continue
    s = open(f, encoding="utf-8").read()
    if "tid=tsb" in s:
        tid = shortslug(f)
        s2 = s.replace("tid=tsb\"", f"tid={tid}\"").replace("tid=tsb&", f"tid={tid}&")
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            fixed += 1
print(f"✓ per-page ClickBank tids on {fixed} files")

# ---------- 3-7) the 12 money pages ----------
for slug, title in NEW_TITLES.items():
    f = f"{slug}/index.html"
    s = open(f, encoding="utf-8").read()
    # 3) title
    old_t = re.search(r"<title>([^<]*)</title>", s).group(1)
    s = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r"\g<1>" + title + r"\g<2>", s, count=1)
    # 4) BreadcrumbList
    if "BreadcrumbList" not in s:
        bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://trustscore.bond/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": f"https://trustscore.bond/{slug}/"}]}
        s = s.replace("</head>", '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + "</script>\n</head>", 1)
    # 5) author
    s = s.replace('"publisher": {"@type": "Organization", "name": "TrustScore"}}',
                  '"publisher": {"@type": "Organization", "name": "TrustScore"}, "author": {"@type": "Organization", "name": "TrustScore Editorial Team", "url": "https://trustscore.bond/how-we-review/"}}', 1)
    # 6) top CTA after glance box
    if "Short on time?" not in s:
        m = re.search(r'<p class="note" style="border:2px solid #1dbf73[^>]*>.*?</small></p>', s, re.S)
        assert m, f"glance box not found in {slug}"
        cta = ('\n<p class="note"><small><b>Disclosure:</b> Fiverr affiliate link — if you order through it '
               'we may earn a commission at no extra cost to you.</small><br>'
               f'<a class="cta" href="{AFF}" rel="sponsored nofollow noopener" target="_blank">Browse Fiverr\'s marketplace (official site) →</a></p>')
        s = s[:m.end()] + cta + s[m.end():]
    for tag in ["a", "p", "main", "article"]:
        o, c = s.count("<" + tag + " ") + s.count("<" + tag + ">"), s.count("</" + tag + ">")
        assert o == c, f"{slug} <{tag}> {o}/{c}"
    open(f, "w", encoding="utf-8").write(s)
    print(f"✓ {slug}: title {len(old_t)}→{len(title)} · breadcrumb · author · top-CTA")

# ---------- 3b) global suffix strip where title>60 ----------
stripped = 0
for f in glob.glob("**/index.html", recursive=True):
    if ".git" in f: continue
    s = open(f, encoding="utf-8").read()
    m = re.search(r"<title>([^<]*)</title>", s)
    if not m: continue
    t = m.group(1)
    if len(t) > 60 and " | TrustScore" in t:
        nt = t.replace(" | TrustScore", "", 1)
        s = s.replace(f"<title>{t}</title>", f"<title>{nt}</title>", 1)
        open(f, "w", encoding="utf-8").write(s)
        stripped += 1
print(f"✓ suffix stripped on {stripped} long titles")

# ---------- 7) noindex 9 thin YMYL marketplaces ----------
nx = 0
for slug in NOINDEX:
    f = f"marketplace/{slug}-marketplace/index.html"
    s = open(f, encoding="utf-8").read()
    s2, c = re.subn(r'<meta name="robots" content="[^"]*"', '<meta name="robots" content="noindex,follow"', s, count=1)
    if c == 0:
        s2 = s.replace("<head>", '<head>\n<meta name="robots" content="noindex,follow">', 1)
    open(f, "w", encoding="utf-8").write(s2)
    nx += 1
print(f"✓ noindex applied to {nx} thin YMYL marketplace pages")

# ---------- 8) sitemap cleanup ----------
sm = open("sitemap.xml", encoding="utf-8").read()
removed = 0
for slug in NOINDEX:
    u = f"https://trustscore.bond/marketplace/{slug}-marketplace/"
    if u in sm:
        sm = re.sub(rf'<url><loc>{re.escape(u)}</loc>[^<]*<lastmod>[^<]*</lastmod>[^<]*<changefreq>[^<]*</changefreq>[^<]*<priority>[^<]*</priority></url>', "", sm, count=1)
        removed += 1
open("sitemap.xml", "w", encoding="utf-8").write(sm)
print(f"✓ sitemap: removed {removed} noindexed URLs → {sm.count('<loc>')} URLs")

# ---------- final verification ----------
bad = 0
for f in glob.glob("**/index.html", recursive=True):
    if ".git" in f: continue
    s = open(f, encoding="utf-8").read()
    m = re.search(r"<title>([^<]*)</title>", s)
    if m and len(m.group(1)) > 60: bad += 1
print(f"→ titles still >60 sitewide: {bad} (was 138; remaining = hub/older pages for weekly refresh)")
print("DONE")
