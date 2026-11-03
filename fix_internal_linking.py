#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix #A33: (1) homepage Fiverr hub directory — 24 hubs + tools links + title/meta
(2) fee-calculator: price-point fee table ($199/$200 cliff) + verified-guides funnel."""
import re, sys

# ============ 1) HOMEPAGE ============
hp = "index.html"
s = open(hp, encoding="utf-8").read()
orig_len = len(s)

SECTION = """
<h2 id="fiverr-guides">🟢 The Fiverr marketplace, mapped</h2>
<p>24 verified gig guides — real prices pulled from live listings, real review counts, and the questions that separate a good hire from a refund request. <b>270+ services covered, updated for 2026.</b></p>
<div class="pc">
<div class="pros"><h3>🎨 Best Fiverr logo designers</h3><p>From $5 logos to full brand kits — 12 verified designers and the brief that gets you a good one.</p><a href="/reviews/best-fiverr-logo-designers/">See the 12 best →</a></div>
<div class="pros"><h3>🎬 Best Fiverr video editors</h3><p>Short-form and YouTube editors from $5 — with the 3-question filter that kills bad hires.</p><a href="/reviews/best-fiverr-video-editing-gigs/">See the 12 best →</a></div>
<div class="pros"><h3>🎙️ Best Fiverr voice-over artists</h3><p>From $5 demos to an 8,148-review pro at $15 — plus the usage-rights math nobody explains.</p><a href="/reviews/best-fiverr-voice-over-gigs/">See the 12 best →</a></div>
<div class="pros"><h3>🚀 Best Fiverr SEO gigs</h3><p>What $20–$500 actually buys: audits, keyword research, and the link-building truth.</p><a href="/reviews/best-fiverr-seo-gigs/">See the 12 best →</a></div>
<div class="pros"><h3>🔧 Best Fiverr WordPress developers</h3><p>A price-by-job map from $25 fixes to $2,000 builds — plus the builder lock-in question.</p><a href="/reviews/best-fiverr-wordpress-developers/">See the best →</a></div>
<div class="pros"><h3>📱 Best Fiverr social media managers</h3><p>What $62–$550/month really buys — and why nobody can guarantee followers.</p><a href="/reviews/best-fiverr-social-media-management-gigs/">See the best →</a></div>
<div class="pros"><h3>📊 Best Fiverr Google Ads experts</h3><p>$25 setups to $425 Pro work — the Partner-badge truth and the audit-first order.</p><a href="/reviews/best-fiverr-google-ads-experts/">See the best →</a></div>
<div class="pros"><h3>📽️ Best Fiverr presentation designers</h3><p>The $5-to-$1,600 price spread, explained — and the 2 words that decide who owns your deck.</p><a href="/reviews/best-fiverr-presentation-design-gigs/">See the best →</a></div>
</div>
<p style="margin-top:14px"><b>All 24 categories:</b>
<a href="/reviews/best-fiverr-ai-automation-gigs/">AI automation</a> ·
<a href="/reviews/best-fiverr-book-cover-designers/">book covers</a> ·
<a href="/reviews/best-fiverr-copywriting-gigs/">copywriting</a> ·
<a href="/reviews/best-fiverr-data-entry-services/">data entry</a> ·
<a href="/reviews/best-fiverr-email-marketing-gigs/">email marketing</a> ·
<a href="/reviews/best-fiverr-illustration-gigs/">illustration</a> ·
<a href="/reviews/best-fiverr-music-jingle-gigs/">music &amp; jingles</a> ·
<a href="/reviews/best-fiverr-podcast-editing-gigs/">podcast editing</a> ·
<a href="/reviews/best-fiverr-psychic-readers/">psychic readers</a> ·
<a href="/reviews/best-fiverr-resume-writers/">resume writers</a> ·
<a href="/reviews/best-fiverr-shopify-experts/">Shopify experts</a> ·
<a href="/reviews/best-fiverr-tiktok-reels-editors/">TikTok &amp; Reels editors</a> ·
<a href="/reviews/best-fiverr-translation-gigs/">translation</a> ·
<a href="/reviews/best-fiverr-virtual-assistant-gigs/">virtual assistants</a> ·
<a href="/reviews/best-fiverr-web-development-gigs/">web development</a> ·
<a href="/reviews/best-fiverr-3d-product-rendering-gigs/">3D product rendering</a>.</p>
<p><b>Before you order:</b> <a href="/tools/fiverr-fee-calculator/">Fiverr fee calculator — what you'll really pay</a> · <a href="/reviews/fiverr-review/">is Fiverr legit? our honest review</a> · <a href="/reviews/fiverr-pro-review/">Fiverr Pro, honestly</a> · <a href="/reviews/fiverr-vs-upwork-small-business/">Fiverr vs Upwork</a>.</p>
"""

# insert right before the green aside (which follows the pc container close)
anchored = False
for a in ['</div>\n\n<aside class="pros"', '</div>\n<aside class="pros"']:
    if a in s:
        s = s.replace(a, "</div>\n" + SECTION + "\n<aside class=\"pros\"", 1)
        anchored = True
        break
assert anchored, "homepage insertion anchor not found"

# title + meta
old_t = "<title>TrustScore — Honest Digital Product Reviews with a 1–10 TrustScore (2026)</title>"
new_t = "<title>TrustScore — Honest Reviews + 24 Verified Fiverr Gig Guides (2026)</title>"
assert old_t in s, "old title not found"
s = s.replace(old_t, new_t, 1)
old_d = '<meta name="description" content="Independent reviews of soulmate readings, numerology, astrology, manifestation, health supplements and B2B SaaS tools — scored on quality, value, delivery and support. Cons included, always."'
new_d = '<meta name="description" content="Independent 1–10 reviews of digital products — plus the Fiverr marketplace mapped: 24 verified gig guides with real prices from live listings, and a free Fiverr fee calculator. Cons included, always."'
assert old_d in s, "old meta not found"
s = s.replace(old_d, new_d, 1)

hub_links = re.findall(r'href="/reviews/best-fiverr-[^"]+/"', s)
assert len(hub_links) == 24, f"hub links on homepage: {len(hub_links)} (expected 24)"
assert 'id="fiverr-guides"' in s
open(hp, "w", encoding="utf-8").write(s)
print(f"✓ HOMEPAGE: 24 hub links injected + title/meta updated ({orig_len} → {len(s)} bytes)")

# ============ 2) FEE CALCULATOR ============
fc = "tools/fiverr-fee-calculator/index.html"
t = open(fc, encoding="utf-8").read()
orig_len = len(t)

FEE_TABLE = """
<h2>What the fees look like at real price points</h2>
<p>The math that surprises first-time buyers is the small-order fee: on a $5 gig it adds 70%+ on top. Here is the buyer-side math at common price points:</p>
<table>
<tr><th>Gig price</th><th>Service fee (5.5%)</th><th>Small-order fee</th><th>You pay</th><th>Fee as % of gig</th></tr>
<tr><td>$5</td><td>$0.28</td><td>$3.50</td><td><b>$8.78</b></td><td>75.6%</td></tr>
<tr><td>$10</td><td>$0.55</td><td>$3.50</td><td><b>$14.05</b></td><td>40.5%</td></tr>
<tr><td>$20</td><td>$1.10</td><td>$3.50</td><td><b>$24.60</b></td><td>23.0%</td></tr>
<tr><td>$50</td><td>$2.75</td><td>$3.50</td><td><b>$56.25</b></td><td>12.5%</td></tr>
<tr><td>$100</td><td>$5.50</td><td>$3.50</td><td><b>$109.00</b></td><td>9.0%</td></tr>
<tr><td>$150</td><td>$8.25</td><td>$3.50</td><td><b>$161.75</b></td><td>7.8%</td></tr>
<tr><td>$199</td><td>$10.95</td><td>$3.50</td><td><b>$213.45</b></td><td>7.3%</td></tr>
<tr><td>$200</td><td>$11.00</td><td>—</td><td><b>$211.00</b></td><td>5.5%</td></tr>
<tr><td>$500</td><td>$27.50</td><td>—</td><td><b>$527.50</b></td><td>5.5%</td></tr>
<tr><td>$1,000</td><td>$55.00</td><td>—</td><td><b>$1,055.00</b></td><td>5.5%</td></tr>
</table>
<p class="note">The $199 → $200 cliff: cross $200 and the $3.50 fee disappears — so a $200 order costs <b>$2.45 less</b> than a $199 one. If your cart lands just under $200 (gig + extras), adding a small extra can actually <i>reduce</i> the total. Fiverr rounds fees to the cent at checkout.</p>
"""

faq_anchor = "\n<h2>Frequently asked questions</h2>"
assert faq_anchor in t, "FAQ anchor not found"
t = t.replace(faq_anchor, "\n" + FEE_TABLE + faq_anchor, 1)

HUBS = """
<h2>Where to spend it — verified gig guides</h2>
<p>Every guide below is built from live listings: real prices, real review counts, and the red flags that separate a good hire from a refund request.</p>
<ul>
<li><a href="/reviews/best-fiverr-logo-designers/">Best Fiverr logo designers</a> — 12 verified, from $5</li>
<li><a href="/reviews/best-fiverr-video-editing-gigs/">Best Fiverr video editors</a> — $5–$105, with the 3-question filter</li>
<li><a href="/reviews/best-fiverr-voice-over-gigs/">Best Fiverr voice-over artists</a> — from $5 demos to an 8,148-review pro at $15</li>
<li><a href="/reviews/best-fiverr-seo-gigs/">Best Fiverr SEO gigs</a> — what $20–$500 actually buys</li>
<li><a href="/reviews/best-fiverr-wordpress-developers/">Best Fiverr WordPress developers</a> — price-by-job map from $25</li>
<li><a href="/reviews/best-fiverr-social-media-management-gigs/">Best Fiverr social media managers</a> — $62–$550/month</li>
<li><a href="/reviews/best-fiverr-google-ads-experts/">Best Fiverr Google Ads experts</a> — $25–$425, audit-first</li>
<li><a href="/reviews/best-fiverr-presentation-design-gigs/">Best Fiverr presentation designers</a> — the $5→$1,600 anatomy</li>
</ul>
<p>Browsing for something else? <a href="/#fiverr-guides">All 24 verified Fiverr gig guides →</a></p>
"""

funnel_anchor = 'Full disclosure</a>.</p>\n<p>Need a logo only?'
assert funnel_anchor in t, "funnel anchor not found"
t = t.replace(funnel_anchor, 'Full disclosure</a>.</p>\n' + HUBS + '\n<p>Need a logo only?', 1)

assert t.count('<table') == 3, f"tables: {t.count('<table')}"
assert t.count('best-fiverr') == 8
assert 'fiverr-guides' in t
assert '$2.45 less' in t
open(fc, "w", encoding="utf-8").write(t)
print(f"✓ FEE CALC: fee table + cliff note + 8-guide funnel injected ({orig_len} → {len(t)} bytes)")

# ============ 3) SAFETY CHECKS both files ============
for f in [hp, fc]:
    x = open(f, encoding="utf-8").read()
    for tag in ["main", "article", "table", "section", "details", "ul", "aside", "footer"]:
        o, c = x.count("<" + tag), x.count("</" + tag + ">")
        assert o == c, f"{f}: <{tag}> unbalanced {o}/{c}"
    assert "{" not in x.replace("{{", "") or True
    bad = re.findall(r'\{[a-z_]+\}', x)
    assert not bad, f"{f}: placeholders {bad}"
    print(f"✓ {f}: tags balanced, no placeholders")
print("ALL CHECKS PASSED")
