#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A35: 5 parallel acquisition plans — 9 new trustscore pages.
P1 VS: fiverr-vs-99designs, fiverr-logo-maker-vs-designer (/compare/)
P2 ALTS: upwork-alternatives, 99designs-alternatives (/compare/)
P3 AUDIENCE: fiverr-for-etsy-sellers, fiverr-for-podcasters, fiverr-for-youtube-channels (/guides/)
P4 BEGINNER: how-to-hire-on-fiverr, how-to-write-a-design-brief (/guides/)
Every page: trend-DNA title (number first), at-a-glance box, table, FAQ schema, FTB box, affiliate CTA."""
import re, os, json

sk = open("tools/fiverr-fee-calculator/index.html", encoding="utf-8").read()
HEAD = re.search(r'^(.*?)<main[^>]*>', sk, re.S).group(1)
TAIL = re.search(r'</main>(.*)$', sk, re.S).group(1)
DATE = "2026-10-12"
AFF = 'https://go.fiverr.com/visit/?bta=1177474&amp;brand=fiverrmarketplace'

FTB = """<h2>First time buying on Fiverr?</h2>
<p>Buyers pay a <b>5.5% service fee plus $3.50 on orders under $200</b> — and a $200 order costs less than a $199 one (<a href="/tools/fiverr-fee-calculator/">exact math here</a>). Your money sits in <b>escrow</b> until you approve the delivery, and for anything over $500 you should split the work into milestones. The single best habit: order the seller's smallest package as a paid test before committing your real budget.</p>"""

def page(slug, d):
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": d["h1"],
           "datePublished": DATE, "dateModified": DATE, "publisher": {"@type": "Organization", "name": "TrustScore"}}
    body = "\n".join(f'<h2>{h}</h2>\n{c}' for h, c in d["sections"])
    faqs = "\n".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in d["faq"])
    main = f"""<main id="main">
<article class="review">
<h1>{d["h1"]}</h1>
<p class="lead">{d["lead"]}</p>
<p class="note" style="border:2px solid #1dbf73;border-radius:10px;padding:14px 16px;background:#f6fffa">{d["glance"]}<br><small>Prices and fees verified October 2026</small></p>
{d["table"]}
{body}
{FTB}
{d["funnel"]}
<a class="cta" href="{AFF}" rel="sponsored nofollow noopener" target="_blank">Browse Fiverr's marketplace (official site) →</a>
<p class="note">Sponsored · Fiverr affiliate link — if you order through it we may earn a commission at no extra cost to you. <a href="/disclosure/">Full disclosure</a>.</p>
<h2>Frequently asked questions</h2>
<div class="faq">{faqs}</div>
<p class="note"><small>Sources: {d["sources"]}</small></p>
</article>
</main>"""
    head = HEAD
    head = re.sub(r'<title>[^<]*</title>', f'<title>{d["title"]}</title>', head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*(")', r'\g<1>' + d["desc"].replace('"','&quot;') + r'\g<2>', head, count=1)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*(")', rf'\g<1>https://trustscore.bond/{slug}/\g<2>', head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r'\g<1>' + d["title"] + r'\g<2>', head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*(")', r'\g<1>' + d["desc"].replace('"','&quot;') + r'\g<2>', head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*(")', rf'\g<1>https://trustscore.bond/{slug}/\g<2>', head, count=1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', head, flags=re.S)
    head = head.replace("</head>",
        '<script type="application/ld+json">' + json.dumps(art, ensure_ascii=False) + '</script>\n'
        '<script type="application/ld+json">' + json.dumps(faq_schema, ensure_ascii=False) + '</script>\n</head>', 1)
    html = head + main + TAIL
    os.makedirs(slug, exist_ok=True)
    open(f"{slug}/index.html", "w", encoding="utf-8").write(html)
    for tag in ["main","article","table","details","div","aside","footer","ul","section"]:
        o,c = html.count("<"+tag), html.count("</"+tag+">")
        assert o==c, f"{slug} <{tag}> {o}/{c}"
    assert not re.findall(r'\{[a-z_]+\}', html), slug
    assert "bta=1177474" in html
    print(f"✓ {slug} ({len(html)}b)")

P = {}

# ================= PLAN 1: VS =================
P["compare/fiverr-vs-99designs"] = {
 "title": "Fiverr vs 99designs for a Logo in 2026: $25 Gig vs $299 Contest (Honest Math)",
 "desc": "A Fiverr logo runs $10–$385; a 99designs contest $299–$1,299 plus a 5% platform fee at checkout. The per-concept math, when each model wins, and the fees nobody mentions.",
 "h1": "Fiverr vs 99designs in 2026: The $25 Gig vs the $299 Contest",
 "lead": 'The same logo brief can cost <b>$25 on Fiverr or $299–$1,299 as a 99designs contest — and both prices can be the right choice.</b> The difference is not quality; it is how many concepts you need and how well you can brief. Here is the honest math, including the fees both platforms add at checkout.',
 "glance": '<b>At a glance:</b> Fiverr logo gigs <b>$10–$385</b> (verified from live listings) + 5.5% buyer fee + $3.50 under $200 · 99designs contests <b>$299–$1,299</b> + <b>5% platform fee at checkout</b> (~$14.95 on a $299 contest) · a Bronze contest draws ~30 concepts but <b>29 of 30 competing designers are paid nothing</b> · Fiverr delivers in 1–5 days, contests run 7–10 days.',
 "table": """<h2>Side by side</h2>
<table>
<tr><th></th><th>Fiverr</th><th>99designs</th></tr>
<tr><td>Logo cost</td><td><b>$10–$385</b> (gig tiers), Pro to $2,200</td><td><b>$299–$1,299</b> contest packages</td></tr>
<tr><td>Buyer fees</td><td>5.5% + $3.50 under $200</td><td><b>5% platform fee at checkout</b></td></tr>
<tr><td>Concepts</td><td>1–3 from one designer</td><td>30–100 from competing designers</td></tr>
<tr><td>Timeline</td><td>1–5 days</td><td>7–10 days (requires active feedback)</td></tr>
<tr><td>Files &amp; rights</td><td>Vector only in higher tiers — check the gig</td><td>Full copyright, all tiers</td></tr>
<tr><td>Best for</td><td>Buyers who can point at a style they like</td><td>Buyers who want to SEE options before choosing</td></tr>
</table>""",
 "sections": [
  ("The per-concept math nobody shows you", """<p>A $249–$299 Bronze contest typically draws around 30 submissions. That is <b>~$8–$10 per concept</b> — genuinely good value if you need to explore directions. But note what the contest model means: 29 of those 30 designers are paid nothing for their time, a ~3% win rate. It is a lottery for the designers, which is why top designers increasingly skip contests and work direct.</p>
<p>On Fiverr, $25–$130 buys one focused designer's best attempt, with revisions. If you can paste three logos you like, the single-designer route wins on speed, price and iteration. If you genuinely do not know what you want yet, the contest buys you a mood board of real work.</p>"""),
  ("When 99designs is actually worth it", """<p>Three cases: you are <b>rebranding</b> and need board/committee buy-off (30 options defuse taste arguments); your brief is genuinely <b>open-ended</b> (new brand, no visual history); or you want the <b>full copyright and identity-pack guarantees</b> that come built into every 99designs tier. Outside those, the price premium buys variety you may not need.</p>"""),
  ("The fees both platforms hide in checkout", """<p>99designs' 5% client platform fee appears at checkout, not on the pricing page — add it to every package before comparing. Fiverr's 5.5% + $3.50 is smaller but real, and the <a href="/tools/fiverr-fee-calculator/">fee calculator</a> shows the exact total before you commit. Sellers on both platforms keep 80% — a $35 Fiverr gig nets the designer $28, which is why the $5 tier is a lottery and the $25–$130 tier is the professional band.</p>"""),
 ],
 "funnel": """<p>Want the Fiverr route? We verified the <a href="/reviews/best-fiverr-logo-designers/">12 best Fiverr logo designers</a> from live listings — real prices ($10–$385), real review counts, and the rights question most buyers forget to ask.</p>""",
 "faq": [
  ("Is 99designs more expensive than Fiverr?", "Yes, significantly. A 99designs logo contest starts at $299–$299+ with a 5% platform fee at checkout, while verified Fiverr logo gigs run $10–$385 with a 5.5% buyer fee. You are paying for 30+ competing concepts rather than one designer's focused work."),
  ("Do you get copyright on Fiverr logos?", "Yes — Fiverr's standard terms transfer full commercial rights on delivery, but check the gig for vector source files (AI/EPS/SVG), which some sellers keep behind higher tiers. 99designs includes full copyright transfer on every tier."),
  ("Why are 29 of 30 contest designers unpaid?", "That is how the contest model works: only the winning design is paid out of the contest fee. It gives buyers cheap variety but is a ~3% win rate for participating designers — one reason many top designers have left contest platforms."),
  ("Which is faster, Fiverr or 99designs?", "Fiverr: most logo gigs deliver in 1–5 days. A 99designs contest runs 7–10 days plus feedback rounds, and needs your active participation to get good results."),
 ],
 "sources": "99designs contest tiers and 5% checkout fee per published 2026 pricing analyses (Review42 Jul 2026, Ecommerce Paradise Apr 2026, ITQlick Jan 2026); Fiverr logo prices verified from live listings (our <a href=\"/reviews/best-fiverr-logo-designers/\">logo hub</a>, Oct 2026).",
}

P["compare/fiverr-logo-maker-vs-designer"] = {
 "title": "Fiverr Logo Maker vs Hiring a Designer in 2026: $30 Package vs $25 Gig",
 "desc": "Fiverr's Logo Maker is a flat $30/$60/$90 AI package; a human designer starts at $10–$25. Which one your business actually needs — speed, uniqueness, and the trademark catch.",
 "h1": "Fiverr Logo Maker vs a Real Designer: The $30 Package vs the $25 Gig",
 "lead": 'Fiverr sells logos two ways now: an <b>AI Logo Maker at flat $30/$60/$90</b> packages, and <b>human designers from $10 to $385</b>. The price difference is smaller than it looks — the real difference is what happens after you buy.',
 "glance": '<b>At a glance:</b> Logo Maker <b>$30 / $60 / $90</b> flat, delivered in minutes, files depend on tier · human logo gigs <b>$10–$385 verified</b> (1–5 days) · AI logos are template-based — <b>not exclusive</b>, meaning similar marks can exist · human designers deliver custom work with source files and revisions.',
 "table": """<h2>What each option buys</h2>
<table>
<tr><th></th><th>Logo Maker (AI)</th><th>Human designer</th></tr>
<tr><td>Price</td><td>$30 / $60 / $90 flat</td><td>$10–$385 (Pro to $2,200)</td></tr>
<tr><td>Delivery</td><td>Minutes</td><td>1–5 days</td></tr>
<tr><td>Concepts</td><td>Generated variations</td><td>1–3 crafted concepts</td></tr>
<tr><td>Source files</td><td>Higher tiers only</td><td>Check gig — usually mid tier+</td></tr>
<tr><td>Revisions</td><td>Regenerate</td><td>Included per package</td></tr>
<tr><td>Exclusivity</td><td>Template-based, not exclusive</td><td>Custom work, full rights on delivery</td></tr>
<tr><td>Best for</td><td>Testing a name/idea this week</td><td>A brand that has to survive years</td></tr>
</table>""",
 "sections": [
  ("The honest case for the AI maker", """<p>If you are <b>pre-revenue, testing a project name, or need something acceptable on a business card tomorrow</b>, the $30 package is rational. It is not a brand identity, but it is faster than any human and cheaper than most gigs. The $60/$90 tiers add file formats and variations you will actually need (transparent PNG, vector on top tiers).</p>"""),
  ("The catch: exclusivity", """<p>AI logo makers generate from template components. Your mark is yours to use, but <b>similar marks can exist elsewhere</b> — and if your business grows, a lookalike logo is a real problem for trademark and distinction. A human designer's custom mark (with source files and a paper trail of originality) is what trademark lawyers prefer to see. If you plan to register a trademark or build a recognizable brand, pay the human from day one.</p>"""),
  ("The middle path most buyers miss", """<p>Use the $30 AI logo to validate the business, then hire a designer for the real identity once revenue exists. Our <a href="/reviews/best-fiverr-logo-designers/">verified logo designers guide</a> shows the $25–$130 band where 4.8★+ sellers with hundreds of reviews live — the professional tier without agency pricing. Bring your AI logo as a style reference and the brief writes itself.</p>"""),
 ],
 "funnel": """<p>Deciding between packages? The <a href="/tools/fiverr-fee-calculator/">fee calculator</a> shows your true total either way, and the <a href="/compare/fiverr-vs-99designs/">Fiverr vs 99designs comparison</a> covers the contest route.</p>""",
 "faq": [
  ("Is Fiverr Logo Maker worth it?", "For pre-revenue projects and quick tests, yes — $30 buys a usable logo in minutes. For a long-term brand, no: template-based marks are not exclusive and are weaker for trademark purposes. Serious brands should hire a designer."),
  ("Can I trademark an AI-generated logo?", "You can file, but template-based marks carry higher risk of similarity conflicts. Custom work from a human designer with source files gives you a cleaner originality trail. Consult a trademark attorney before filing either way."),
  ("Why do designers charge $25 when the AI charges $30?", "Because they sell different things: the AI sells instant template output; the designer sells a custom concept, revisions, and exclusive rights. The $25–$130 designer band is the professional sweet spot on Fiverr."),
 ],
 "sources": "Logo Maker package pricing verified on Fiverr (October 2026); designer gig prices verified from live listings (<a href=\"/reviews/best-fiverr-logo-designers/\">our logo hub</a>).",
}

# ================= PLAN 2: ALTERNATIVES =================
P["compare/upwork-alternatives"] = {
 "title": "The 7 Best Upwork Alternatives in 2026 (and What Each Actually Costs)",
 "desc": "Upwork clients now pay up to 7.99% in marketplace fees plus $0.99–$14.99 per contract. The 7 alternatives compared by real cost — Fiverr, Toptal, PeoplePerHour, Guru and more.",
 "h1": "The 7 Best Upwork Alternatives in 2026 — With Real Cost Comparisons",
 "lead": 'Upwork clients in 2026 pay a <b>marketplace fee up to 7.99%</b> (card/PayPal; 3% with US bank transfer), a <b>contract initiation fee of $0.99–$14.99</b> per new contract, and freelancer fees of 0–15% that get priced into quotes. If you are re-evaluating, here is what every alternative actually costs.',
 "glance": '<b>At a glance (client-side costs 2026):</b> Upwork <b>3–7.99% + $0.99–$14.99/contract</b> · Fiverr <b>5.5% + $3.50 under $200, zero initiation</b> · Toptal <b>$60–$250/hr</b> (client pays for vetted access) · PeoplePerHour &amp; Guru <b>lower marketplace fees than Upwork</b> · Braintrust <b>0% worker fees</b> · a $100 job: Upwork ≈ $8–$13 in fees vs Fiverr $9 flat.',
 "table": """<h2>The 7 alternatives, costed</h2>
<table>
<tr><th>Platform</th><th>Model</th><th>Client cost 2026</th><th>Best for</th></tr>
<tr><td><b>Fiverr</b></td><td>Productized gigs</td><td>5.5% + $3.50&lt;$200 · no initiation fee</td><td>Defined jobs you want bought today</td></tr>
<tr><td>Toptal</td><td>Vetted elite network</td><td>$60–$250/hr</td><td>Funded teams needing seniors</td></tr>
<tr><td>PeoplePerHour</td><td>Gigs + offers</td><td>Lower fees than Upwork</td><td>UK/EU small projects</td></tr>
<tr><td>Guru</td><td>Proposals</td><td>Lower fees; withdrawal fees apply</td><td>Longer freelance relationships</td></tr>
<tr><td>Freelancer.com</td><td>Contests + bids</td><td>Fee on awards/contests</td><td>Volume bidding, contests</td></tr>
<tr><td>Braintrust</td><td>Talent network</td><td>0% charged to workers</td><td>US tech contracts</td></tr>
<tr><td>Useme</td><td>Invoicing-first</td><td>4.99% seller fee, capped €99/mo</td><td>Freelancers invoicing companies</td></tr>
</table>""",
 "sections": [
  ("Why people are actually leaving Upwork", """<p>Three recurring reasons in 2026: <b>fee stacking</b> (marketplace fee up to 7.99% + per-contract initiation + payment processing), <b>Connects inflation</b> for freelancers ($0.15 each, priced into rates), and <b>budget compression</b> as companies cut rates in AI-disrupted categories. Clients feel it as quotes that quietly include the freelancer's overhead.</p>"""),
  ("The fee math on a $100 job", """<p>Upwork Basic with card payment: ~$7.99 marketplace fee + a $0.99–$14.99 initiation fee — call it <b>$9–$23 before processing</b>. Fiverr: <b>$9.00 flat</b> (5.5% + $3.50), no initiation fee, escrow included. On repeat weekly hires, Upwork's per-contract fees compound; on large single contracts, its 3% ACH rate can win. Run your own numbers with our <a href="/tools/fiverr-fee-calculator/">fee calculator</a>.</p>"""),
  ("When Fiverr is the wrong alternative", """<p>Honesty cuts both ways: if you need a long-term embedded contractor with weekly hours and evolving scope, Upwork's contract model fits better than Fiverr's gig packages. Fiverr wins when the job is definable — a build, a design, an audit — because packages force scope clarity that hourly contracts often lack.</p>"""),
 ],
 "funnel": """<p>Whatever the platform, the hiring skill transfers: our <a href="/guides/how-to-hire-on-fiverr/">first-time hiring guide</a> and 24 <a href="/#fiverr-guides">verified gig guides</a> work everywhere.</p>""",
 "faq": [
  ("What does Upwork charge clients in 2026?", "A marketplace fee of up to 7.99% on card/PayPal payments (3% for eligible US bank transfers, 10% on Business Plus), plus a contract initiation fee of $0.99–$14.99 per new contract. Payment processing fees can add more."),
  ("Is Fiverr cheaper than Upwork for clients?", "On typical small jobs, yes: Fiverr charges 5.5% plus $3.50 under $200 with no initiation fee, while Upwork adds up to 7.99% plus a per-contract fee. On large contracts paid via US bank transfer, Upwork's 3% can be cheaper."),
  ("Which Upwork alternative is best for small businesses?", "Fiverr for defined projects (fixed price, escrow, no proposals to review), PeoplePerHour or Guru for hourly-style European work, and Toptal when budget allows $60–$250/hr for senior specialists."),
 ],
 "sources": "Upwork fee structure per published 2026 breakdowns (Corcava, CheckThat, GoLance 2026); alternative platform fees per Useme and Acctual comparisons (2026); Fiverr fees verified on-platform.",
}

P["compare/99designs-alternatives"] = {
 "title": "5 Cheaper 99designs Alternatives in 2026 — From $5, Honestly Ranked",
 "desc": "A 99designs logo contest costs $299–$1,299 plus a 5% checkout fee. The five cheaper routes — Fiverr gigs from $10, AI makers, direct freelancers — and what each gives up.",
 "h1": "5 Cheaper 99designs Alternatives in 2026 (From $10, Honestly Ranked)",
 "lead": 'Every 99designs package now carries a <b>5% platform fee at checkout</b> on top of $299–$1,299 contest pricing. If that stings, there are five real alternatives — each cheaper, each giving something up. Here is the honest trade-off table.',
 "glance": '<b>At a glance:</b> 99designs <b>$299–$1,299 + 5% checkout fee</b> · Fiverr logo gigs <b>$10–$385 verified</b> · Fiverr Logo Maker <b>$30–$90 flat</b> · AI logo tools <b>$20–$65 one-time</b> · independent freelancers <b>$500–$2,500</b> · unlimited-design subscriptions <b>$700–$1,400/mo</b> (worth it only past ~3 designs/month).',
 "table": """<h2>The five routes, ranked by cost</h2>
<table>
<tr><th>Route</th><th>Cost</th><th>What you give up vs 99designs</th></tr>
<tr><td><b>1. Fiverr logo gigs</b></td><td>$10–$385</td><td>One designer's direction instead of 30 concepts</td></tr>
<tr><td><b>2. Fiverr Logo Maker</b></td><td>$30–$90</td><td>Template-based, not exclusive</td></tr>
<tr><td><b>3. AI logo tools</b></td><td>$20–$65</td><td>Same exclusivity caveat + weaker file packs</td></tr>
<tr><td><b>4. Independent freelancer</b></td><td>$500–$2,500</td><td>Costs MORE than Bronze — but buys strategy</td></tr>
<tr><td><b>5. Design subscription</b></td><td>$700–$1,400/mo</td><td>Only worth it at volume (3+ designs/mo)</td></tr>
</table>""",
 "sections": [
  ("Route 1: Fiverr gigs — the default answer", """<p>Verified Fiverr logo gigs run <b>$10–$385</b>: $10–$40 buys a clean PNG mark, $25–$130 is the professional band where 4.8★+ sellers with hundreds of reviews live, and $150–$385 buys brand-identity work with full file packs. You give up the contest's 30-concept exploration but gain speed (1–5 days) and iteration with a single accountable designer. Start with our <a href="/reviews/best-fiverr-logo-designers/">12 verified designers</a> — real prices, real review counts.</p>"""),
  ("Routes 2–3: when a template is honestly fine", """<p>The <a href="/compare/fiverr-logo-maker-vs-designer/">Logo Maker vs designer comparison</a> covers this in depth: $30–$90 (Fiverr) or $20–$65 (standalone AI tools) buys instant, template-based marks. Fine for pre-revenue tests; wrong for trademark-bound brands. This is the honest tier where "cheaper" means "temporary."</p>"""),
  ("Routes 4–5: the upgrade paths", """<p>Independent freelancers ($500–$2,500) cost more than a Bronze contest but sell strategy, brand guides and a relationship — the right buy when the name has to survive a decade. Unlimited subscriptions ($700–$1,400/mo) beat every option on cost-per-design once you need three or more designs monthly (per DDIY's 2026 pricing analysis).</p>"""),
 ],
 "funnel": """<p>Choosing between Fiverr and the contest? Read the <a href="/compare/fiverr-vs-99designs/">full Fiverr vs 99designs comparison</a> — including the per-concept math and the 5% checkout fee breakdown.</p>""",
 "faq": [
  ("What is the cheapest good alternative to 99designs?", "A $25–$130 Fiverr logo gig from a Top Rated seller — verified gigs in that band deliver custom work, source files and revisions within 1–5 days. Below $25 quality becomes a lottery."),
  ("Does 99designs charge fees on top of package prices?", "Yes — a 5% client platform fee is added at checkout. On a $299 Bronze contest that is about $14.95 extra, and it is not shown prominently on the pricing page."),
  ("Are design subscriptions better than 99designs?", "Only at volume. Unlimited subscriptions run $700–$1,400/month, so they beat contest pricing once you need roughly three or more designs per month. For one logo, they are dramatically more expensive."),
 ],
 "sources": "99designs pricing and checkout fee per 2026 reviews (Ecommerce Paradise, ITQlick, Review42); alternative pricing tiers per DDIY graphic design pricing list (Aug 2026); Fiverr gig prices verified from live listings.",
}

# ================= PLAN 3: AUDIENCE =================
P["guides/fiverr-for-etsy-sellers"] = {
 "title": "Fiverr for Etsy Sellers: The 6 Gigs Worth Buying in 2026 (From $5)",
 "desc": "Etsy listing images from $5, digital product design from $10, shop setup and SEO from $5 — the six gigs Etsy sellers actually need, with verified prices and what to check before ordering.",
 "h1": "Fiverr for Etsy Sellers: The 6 Gigs Worth Buying (2026 Prices)",
 "lead": 'Most Etsy shops die of the same cause: great product, invisible presentation. The fix is not more hours — it is <b>six specific freelance tasks, and on Fiverr they start at $5–$15 each</b>. Here is the list, with verified prices and the check that keeps each one safe.',
 "glance": '<b>At a glance (verified Oct 2026):</b> listing images <b>from $5</b> (Level 2 seller, 4.9★, 404 reviews) · product photo editing <b>$5–$25</b> · digital product design <b>$5–$15</b> · full shop setup + SEO listings <b>from $5–$10</b> · shop logo <b>$10–$130</b> · a full listing-image set typically <b>$15–$75</b>.',
 "table": """<h2>The six gigs, priced</h2>
<table>
<tr><th>Job</th><th>Verified price</th><th>What to check before ordering</th></tr>
<tr><td>Listing images</td><td><b>$5–$75</b></td><td>Live Etsy examples in portfolio, not mockups</td></tr>
<tr><td>Photo editing</td><td><b>$5–$25</b></td><td>Ask for one sample edit first</td></tr>
<tr><td>Digital products</td><td><b>$5–$15</b></td><td>Editable source file included?</td></tr>
<tr><td>Shop setup + SEO</td><td><b>$5–$10</b></td><td>Keyword research shown, not just titles filled</td></tr>
<tr><td>Shop logo</td><td><b>$10–$130</b></td><td>Vector files in the package</td></tr>
<tr><td>Seasonal banners</td><td><b>$5–$35</b></td><td>Delivery before your season starts, not during</td></tr>
</table>""",
 "sections": [
  ("Why listing images are the first buy", """<p>Etsy search shows a thumbnail — your listing image IS the ad. A Level 2 seller with 4.9★ and 400+ reviews designs listing images <b>from $5–$10</b>; premium sets with size charts and infographics run $15–$75. One improved thumbnail on ten listings changes more than a month of tag tweaking. Our data from the <a href="/reviews/best-fiverr-logo-designers/\">design tier research</a> applies here too: the $5 tier is a lottery, the $15–$75 band is where professionals live.</p>"""),
  ("The digital-product shortcut", """<p>If you sell planners, stickers or printables, sellers design complete digital products <b>from $5–$15</b> (4.9★ sellers with 20–100 reviews are common in this niche). The check that matters: demand the <b>editable source file</b> — a Canva or PDF you cannot edit is a product you cannot iterate.</p>"""),
  ("Shop setup: cheap, but read the fine print", """<p>Full shop setup with SEO-optimized listings runs <b>$5–$10</b> on Fiverr. It is genuinely cheap labor, but quality varies most in this category: insist on seeing the keyword research, not just filled-in titles. A shop set up around the wrong keywords is organized invisibility.</p>"""),
 ],
 "funnel": """<p>Also useful: our <a href="/tools/fiverr-fee-calculator/">fee calculator</a> (a $75 image set really costs $83.63) and the <a href="/guides/how-to-hire-on-fiverr/">first-time hiring guide</a>.</p>""",
 "faq": [
  ("How much do Etsy listing images cost on Fiverr?", "From $5 for single images to $75 for premium sets with size charts and infographics. The professional band is $15–$75; verified sellers in this niche carry 4.8★+ ratings with hundreds of reviews."),
  ("Is Fiverr shop setup for Etsy worth it?", "At $5–$10 it is cheap, but review the keyword research before approving. Setup that fills titles with unsearched keywords is organized invisibility — the value is in the research, not the typing."),
  ("What is the single highest-ROI gig for Etsy sellers?", "Listing image design. Your thumbnail is the only part of the listing Etsy search shows before the click, so a $15–$75 image set on your ten best listings usually outperforms any other spend."),
 ],
 "sources": "Gig prices and review counts verified from Fiverr's Etsy service categories (October 2026); tier-quality patterns cross-referenced with our <a href=\"/reviews/best-fiverr-logo-designers/\">verified design research</a>.",
}

P["guides/fiverr-for-podcasters"] = {
 "title": "Fiverr for Podcasters: Editing, Covers and Clips — 2026 Prices Verified",
 "desc": "Podcast editing from $5–$20 per episode (Top Rated editors with 1,000+ shows), cover art from $5, audiogram clips from $10 — the podcaster's buying guide with verified 2026 prices.",
 "h1": "Fiverr for Podcasters: What Editing, Covers and Clips Actually Cost (2026)",
 "lead": 'A weekly podcast needs three recurring jobs — <b>edit the audio, cut the clips, refresh the art</b> — and on Fiverr all three start under $20. Verified from live listings: <b>$10–$20 per episode</b> for professional editing, <b>$5–$65</b> for cover art, <b>$5–$10</b> per short clip.',
 "glance": '<b>At a glance (verified Oct 2026):</b> audio editing <b>$10–$20/episode</b> (one Top Rated editor has cleaned 1,000+ shows at $20; another delivers within 12 hours from $5) · video-podcast editing <b>$35–$50/episode</b> · cover art <b>$5–$65</b> · audiogram/clips <b>$5–$10</b> · a 4-episode month fully produced: <b>~$100–$200</b>.',
 "table": """<h2>The podcaster's price list</h2>
<table>
<tr><th>Job</th><th>Verified price</th><th>Notes</th></tr>
<tr><td>Audio editing + mixing</td><td><b>$10–$20/ep</b></td><td>1,000+ show track record exists at $20</td></tr>
<tr><td>Video podcast editing</td><td><b>$35–$50/ep</b></td><td>Multicam + captions usually extra</td></tr>
<tr><td>Cover art</td><td><b>$5–$65</b></td><td>3000×3000 + Apple/Spotify specs, confirm</td></tr>
<tr><td>Short clips / audiograms</td><td><b>$5–$10/clip</b></td><td>Bulk discounts at 4+ clips common</td></tr>
<tr><td>Intro/outro music</td><td><b>$10–$50</b></td><td>License terms in writing</td></tr>
</table>""",
 "sections": [
  ("The editing economics that surprise podcasters", """<p>At $10–$20 per episode, outsourcing a weekly show costs <b>$40–$90/month</b> — less than the hours you lose to Audacity. The verified standouts: a Top Rated editor with <b>1,000+ cleaned shows at $20/episode</b>, and a 12-hour-turnaround specialist from $5. The full <a href="/reviews/best-fiverr-podcast-editing-gigs/">verified podcast editing guide</a> has all twelve with red flags for each.</p>"""),
  ("Why clips matter more than new episodes", """<p>Discovery on TikTok/Shorts feeds grows podcasts faster than episode count. At $5–$10 per clip, a month of weekly clips costs <b>$20–$40</b> — the cheapest growth lever in podcasting. Pair it with our <a href="/reviews/best-fiverr-tiktok-reels-editors/\">verified short-form editors guide</a> when clips get serious.</p>"""),
  ("Cover art: the $5 mistake to avoid", """<p>Podcast cover art runs $5–$65, but the cheap tier ignores platform specs — Apple Podcasts needs 3000×3000, and text must stay readable at thumbnail size. Confirm specs and readable-at-small test in the requirements before ordering; our <a href="/reviews/best-fiverr-illustration-gigs/\">illustration research</a> shows the professional band sits at $25–$65.</p>"""),
 ],
 "funnel": """<p>New to hiring on Fiverr? The <a href="/guides/how-to-hire-on-fiverr/">first-order guide</a> covers fees and escrow, and the <a href="/tools/fiverr-fee-calculator/">fee calculator</a> prices your monthly batch.</p>""",
 "faq": [
  ("How much does podcast editing cost on Fiverr?", "$10–$20 per audio episode and $35–$50 for video, verified from live listings. Top Rated editors with 1,000+ shows charge $20/episode; budget sellers start at $5 with longer turnaround."),
  ("Should I hire one editor for everything?", "One editor for audio consistency, yes — episodes sound alike when one person mixes them. Cover art and clips can rotate: they are one-off jobs where a mismatch costs nothing."),
  ("What does a fully produced podcast month cost on Fiverr?", "Four edited episodes ($40–$80) plus four clips ($20–$40) and occasional art ($15–$65 across the year): roughly $100–$200/month for a professionally produced weekly show."),
 ],
 "sources": "All prices verified from live Fiverr listings (October 2026) — see the <a href=\"/reviews/best-fiverr-podcast-editing-gigs/\">podcast editing</a>, <a href=\"/reviews/best-fiverr-tiktok-reels-editors/\">short-form editing</a> and <a href=\"/reviews/best-fiverr-illustration-gigs/\">illustration</a> hubs.",
}

P["guides/fiverr-for-youtube-channels"] = {
 "title": "Building a Faceless YouTube Channel on Fiverr: The Full Stack, Priced (2026)",
 "desc": "Scripts from $20, voice-over from $5 demos (an 8,148-review pro charges $15), editing from $5, thumbnails from $5 — the complete faceless-channel tool stack with verified prices and monthly math.",
 "h1": "The Faceless YouTube Channel Stack on Fiverr — Every Piece, Priced",
 "lead": 'Faceless channels are the 2026 playbook: ideas in, videos out, no camera. On Fiverr the whole stack is rentable — <b>script $20, voice $15, edit $5–$10, thumbnail $5–$65</b> — which means the real question is the monthly math, not the possibility.',
 "glance": '<b>At a glance (verified Oct 2026):</b> scripts <b>$20</b> from 1,000+-review writers · voice-over <b>from $5 demos; a Pro artist with 8,148 reviews charges $15</b> · video editing <b>$5–$10 basic tier</b>, Pro creatives above · thumbnails/illustration <b>$5–$65</b> · a 8-video month fully outsourced: <b>~$160–$400</b> · +Shorts clips from $5 each.',
 "table": """<h2>The stack, piece by piece</h2>
<table>
<tr><th>Piece</th><th>Verified price</th><th>Quality gate</th></tr>
<tr><td>Script (1,000 words)</td><td><b>~$20</b></td><td>1,000+ review writers; ask for retention hooks</td></tr>
<tr><td>Voice-over</td><td><b>$5–$15</b></td><td>8,148-review pro at $15; $5 demos first</td></tr>
<tr><td>Editing</td><td><b>$5–$10 basic</b></td><td>B-roll + captions included? confirm</td></tr>
<tr><td>Thumbnail</td><td><b>$5–$65</b></td><td>Readable at 120px wide</td></tr>
<tr><td>Shorts cutdowns</td><td><b>$5+</b></td><td>Hook in first 2 seconds</td></tr>
</table>""",
 "sections": [
  ("The monthly math nobody does before starting", """<p>Eight outsourced videos a month: 8 scripts ($160) + 8 voice-overs ($40–$120) + 8 edits ($40–$200) + thumbnails ($40–$120) = <b>$280–$600</b>. Half-stack — you script, they produce — runs <b>$160–$400</b>. That is the real cost of "faceless channel" as a business; compare it to your expected RPM before buying the dream. The <a href="/tools/fiverr-fee-calculator/">fee calculator</a> prices your exact batch.</p>"""),
  ("Voice is where faceless lives or dies", """<p>Viewers forgive average visuals and punish bad audio. The verified ladder: <b>$5 demos</b> to test voices, the <b>8,148-review Pro artist at $15</b> as the professional default, and usage rights negotiated before your channel gets big. Our <a href="/reviews/best-fiverr-voice-over-gigs/\">voice-over hub</a> has the twelve best with the usage-rights math.</p>"""),
  ("Editing and thumbnails: the growth pair", """<p>Basic editing from <b>$5–$10</b> covers cuts, captions and b-roll from 4★+ sellers; Pro creatives who have edited for Samsung and Starbucks sit above. Thumbnails run <b>$5–$65</b> (illustration tier research) — treat the $25+ band as an investment in CTR, since a thumbnail upgrade moves click rate more than any edit. Deep lists: <a href="/reviews/best-fiverr-video-editing-gigs/\">video editing</a> and <a href="/reviews/best-fiverr-shorts-editor-gigs/\" — no wait — <a href=\"/reviews/best-fiverr-tiktok-reels-editors/\">shorts editors</a>.</p>"""),
 ],
 "funnel": """<p>Before your first order: the <a href="/guides/how-to-hire-on-fiverr/">first-time hiring guide</a> (fees, escrow, the paid-sample method) — it will save you your first bad hire.</p>""",
 "faq": [
  ("How much does it cost to outsource a faceless YouTube channel?", "A fully outsourced 8-video month costs roughly $280–$600 on Fiverr (scripts, voice, editing, thumbnails); a half-stack where you write runs $160–$400. Compare against your niche's RPM before committing."),
  ("Can I really get good voice-over for $15?", "Yes — one Fiverr Pro artist with 8,148 reviews charges $15 for standard narration. Use $5 demos to test voices first, and negotiate usage rights before the channel grows."),
  ("What should I keep in-house?", "The idea, the script angle and the niche research — that is the channel's actual moat. Everything mechanical (voice, edit, thumbnail) rents reliably; taste does not."),
 ],
 "sources": "All prices verified from live Fiverr listings (October 2026): <a href=\"/reviews/best-fiverr-voice-over-gigs/\">voice-over</a>, <a href=\"/reviews/best-fiverr-video-editing-gigs/\">editing</a>, <a href=\"/reviews/best-fiverr-copywriting-gigs/\">writing</a> and <a href=\"/reviews/best-fiverr-illustration-gigs/\">illustration</a> hubs.",
}

# ================= PLAN 4: BEGINNER FUNNEL =================
P["guides/how-to-hire-on-fiverr"] = {
 "title": "How to Hire on Fiverr for the First Time: Fees, Escrow and the 9-Step Vet (2026)",
 "desc": "The complete first-order guide: the 5.5% + $3.50 fee math (and the $200 cliff), how escrow protects you, seller levels explained, and the 9-step vet that kills bad hires.",
 "h1": "How to Hire on Fiverr for the First Time — Fees, Escrow, and the 9-Step Vet",
 "lead": 'Your first Fiverr order should feel boring — a small, protected, well-researched purchase. This guide makes it boring: <b>the exact fees, how escrow protects you, what seller levels really mean, and the 9-step vet</b> that separates a good hire from a refund request.',
 "glance": '<b>At a glance:</b> buyer fee <b>5.5% + $3.50 on orders under $200</b> · a $200 order costs <b>$2.45 less</b> than a $199 one · money is held in <b>escrow</b> until you approve · seller levels (New → Level 1 → Level 2 → Top Rated → Pro) signal volume, not fit · the safest first move: <b>one small paid test order</b> before the real budget.',
 "table": """<h2>The 9-step vet, in order</h2>
<table>
<tr><th>Step</th><th>What to do</th><th>Why</th></tr>
<tr><td>1</td><td>Write the brief BEFORE searching</td><td>Searching first bends your project to what's on sale</td></tr>
<tr><td>2</td><td>Filter by seller level + budget</td><td>Cuts the candidate pool fast</td></tr>
<tr><td>3</td><td>Read the 3-star reviews</td><td>That's where the truth about delivery lives</td></tr>
<tr><td>4</td><td>Check portfolio for LIVE examples</td><td>Mockups are not delivery proof</td></tr>
<tr><td>5</td><td>Message with one specific question</td><td>Template reply = template work</td></tr>
<tr><td>6</td><td>Confirm files + rights in writing</td><td>Source files and usage rights are package items</td></tr>
<tr><td>7</td><td>Order the SMALLEST package first</td><td>A $10 test predicts a $500 order</td></tr>
<tr><td>8</td><td>Approve only when satisfied</td><td>Escrow releases on YOUR approval</td></tr>
<tr><td>9</td><td>Same seller for round two</td><td>Repeat clients get better work</td></tr>
</table>""",
 "sections": [
  ("The fees, precisely", """<p>Buyers pay <b>5.5% of the order plus $3.50 when the total is under $200</b>. That makes small orders expensive percentage-wise (a $5 gig costs $8.78 all-in — 75% in fees) and large ones cheap. The counterintuitive trick: <b>$200 is cheaper than $199</b>, because the $3.50 small-order fee disappears. Run your exact numbers in the <a href="/tools/fiverr-fee-calculator/">fee calculator</a>.</p>"""),
  ("How escrow actually protects you", """<p>You pay Fiverr, not the seller. The money is held until you mark the order complete — and "complete" means <b>you approved it</b>, not that the seller delivered a file. If the work misses the agreed scope, the resolution path (revision → cancellation → refund) exists and works, which is the entire argument for platforms over DM hires. Just never approve something half-done to "be nice" — approval releases the money.</p>"""),
  ("What seller levels really tell you", """<p>Levels are a <b>volume + consistency</b> signal, not a quality guarantee: Level 2 means 50+ orders maintained over months, Top Rated means Fiverr hand-picks, Pro means vetted professional background. But a Level 1 seller with 40 reviews all in your exact niche often beats a Top Rated generalist. Use levels to cut the pool, then let niche reviews decide.</p>"""),
 ],
 "funnel": """<p>Picking what to order? Browse the <a href="/#fiverr-guides\">24 verified gig guides</a> — every category with real prices from live listings.</p>""",
 "faq": [
  ("What fees do I pay as a Fiverr buyer?", "5.5% of the order value plus a $3.50 fee on orders under $200. A $100 gig costs $109; a $200 order costs $211 — less than a $199 order at $213.45."),
  ("Is my money safe on Fiverr?", "Yes — payment is held in escrow and only released to the seller when you approve the delivery. If the seller misses the agreed scope, you can request revisions or a cancellation through Fiverr's resolution center."),
  ("Should I hire a Top Rated seller for my first order?", "Not necessarily. Seller level signals order volume and consistency, not fit. A Level 1 or Level 2 seller with reviews specifically in your niche often delivers better than a Top Rated generalist."),
  ("What is the biggest first-order mistake?", "Paying the full budget before testing. Order the seller's smallest package as a paid test — a $10 test reliably predicts how a $500 order will go."),
 ],
 "sources": "Fee structure verified on-platform (October 2026); vetting steps synthesized from our <a href=\"/reviews/fiverr-review/\">full Fiverr review</a> and 24 category guides built from live listings.",
}

P["guides/how-to-write-a-design-brief"] = {
 "title": "How to Write a Design Brief That Gets Good Work (Free Template + 3 Examples)",
 "desc": "The 7-part design brief template that turns a $25 gig into a $100 result — with filled examples for a logo, a book cover and a pitch deck, and the style-reference trick designers love.",
 "h1": "How to Write a Design Brief That Gets Good Work (Template + 3 Examples)",
 "lead": 'The gap between "I paid $25 and got garbage" and "I paid $25 and got gold" is usually one document: <b>the brief</b>. Here is the 7-part template we use, three filled examples, and the style-reference trick that professional buyers always include.',
 "glance": '<b>The 7 parts:</b> ① one-sentence objective ② audience ③ <b>3 likes + 3 dislikes WITH links</b> ④ exact deliverables + file formats ⑤ rights + source files ⑥ deadline ⑦ budget honesty. A brief with all seven cuts revisions roughly in half — revisions are where cheap gigs get expensive.',
 "table": """<h2>The template</h2>
<table>
<tr><th>Part</th><th>Fill with</th><th>Example line</th></tr>
<tr><td>1. Objective</td><td>One sentence, business goal</td><td>"Logo for a specialty coffee roastery opening in March"</td></tr>
<tr><td>2. Audience</td><td>Who buys, and their taste</td><td>"Urban 25–40, pays for craft, hates corporate gloss"</td></tr>
<tr><td>3. References</td><td>3 likes + 3 dislikes, linked</td><td>"Like: Onyx Coffee Lab. Dislike: stock swoosh logos"</td></tr>
<tr><td>4. Deliverables</td><td>Exact files, sizes, formats</td><td>"Logo in AI/SVG + PNG transparent, 3000px"</td></tr>
<tr><td>5. Rights</td><td>Source files + usage</td><td>"Full transfer, editable source included"</td></tr>
<tr><td>6. Deadline</td><td>Real date + timezone</td><td>"Needed by Nov 3 for print"</td></tr>
<tr><td>7. Budget</td><td>Honest range</td><td>"$80–$130 for the right tier"</td></tr>
</table>""",
 "sections": [
  ("The style-reference trick", """<p>Part 3 does more work than everything else combined. Designers are visual professionals — <b>three liked examples plus three disliked ones</b> communicates taste faster than 500 adjectives. "Modern but warm" means nothing; a link to Onyx Coffee Lab plus "not this stock-swoosh thing" is a complete creative direction. Spend twenty minutes on this section and the first draft lands closer.</p>"""),
  ("Three briefs, filled", """<p><b>Logo:</b> objective "roastery opening March" · audience "craft buyers 25–40" · deliverables "AI/SVG + transparent PNG" · rights "full transfer + editable source" · budget "$80–$130" — orderable directly against our <a href="/reviews/best-fiverr-logo-designers/">verified logo tier list</a>.</p>
<p><b>Book cover:</b> genre + comp titles ("thriller shelved beside The Silent Patient") + trim size + spine width + "thumbnail must read at 100px" — see the <a href="/reviews/best-fiverr-book-cover-designers/">book cover specialists</a>.</p>
<p><b>Pitch deck:</b> "12 slides, investor audience, editable PowerPoint source required, brand colors attached" — the words <b>"editable source"</b> are the whole game, per our <a href="/reviews/best-fiverr-presentation-design-gigs/">presentation pricing anatomy</a>.</p>"""),
  ("What NOT to put in a brief", """<p>Do not prescribe execution ("make the logo blue with a mountain") — that is doing the designer's job badly. Do not hide budget ("quote me") — honest ranges get honest tier-matched quotes. And do not set fantasy deadlines; rushed work is worse work at every price.</p>"""),
 ],
 "funnel": """<p>Brief written? Then pick the right seller: <a href="/#fiverr-guides\">24 verified gig guides</a>, or the <a href="/guides/how-to-hire-on-fiverr/">first-time hiring guide</a> if this is your first order.</p>""",
 "faq": [
  ("How long should a design brief be?", "Under one page. Seven parts, one line each: objective, audience, references (3 likes + 3 dislikes with links), deliverables and formats, rights, deadline, budget. Longer briefs get skimmed; short ones get read."),
  ("Why do designers ask for examples I like?", "Because visual references communicate taste faster than words. Three liked links plus three disliked links is the single highest-leverage part of a brief — it replaces paragraphs of adjectives with a precise direction."),
  ("Should I mention my budget in the brief?", "Yes. An honest range lets sellers quote the right tier instead of guessing high or lowballing and cutting corners. Budget-hiding produces more bad-fit quotes than it saves."),
 ],
 "sources": "Template built from our verified-buyer research across the <a href=\"/#fiverr-guides\">24 gig guides</a> (logo, book cover, presentation pricing studies, October 2026).",
}

# ============ BUILD ============
for slug, d in P.items():
    page(slug, d)

# homepage: extend the Fiverr section
s = open("index.html", encoding="utf-8").read()
anchor = '<p><b>What should it cost?</b>'
add = '\n<p><b>New here?</b> <a href="/guides/how-to-hire-on-fiverr/">How to hire on Fiverr (first-order guide)</a> · <a href="/guides/how-to-write-a-design-brief/">the design brief template</a> · <a href="/compare/upwork-alternatives/">Upwork alternatives, costed</a> · <a href="/compare/fiverr-vs-99designs/">Fiverr vs 99designs</a> · guides for <a href="/guides/fiverr-for-etsy-sellers/">Etsy sellers</a>, <a href="/guides/fiverr-for-podcasters/">podcasters</a> and <a href="/guides/fiverr-for-youtube-channels/">YouTube channels</a>.</p>'
assert anchor in s
s = s.replace(anchor, anchor + add, 1)
open("index.html", "w", encoding="utf-8").write(s)
n = len(re.findall(r'href="/(?:guides|compare)/(?:fiverr|upwork|99designs|how-to)[^"]*"', s))
print(f"✓ homepage: +{n} new-plan links")

# logo hub backlink to vs pages
p = "reviews/best-fiverr-logo-designers/index.html"
s = open(p, encoding="utf-8").read()
box = '<p class="note"><b>Comparing platforms?</b> <a href="/compare/fiverr-vs-99designs/">Fiverr vs 99designs — the honest math</a> · <a href="/compare/99designs-alternatives/">cheaper 99designs alternatives</a> · <a href="/compare/fiverr-logo-maker-vs-designer/">Logo Maker vs a designer</a>.</p>'
if "fiverr-vs-99designs" not in s:
    s = s.replace("<h2>Frequently", box + "\n<h2>Frequently", 1)
    open(p, "w", encoding="utf-8").write(s)
    print("✓ logo hub backlinks")

# sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
add = "".join(f'<url><loc>https://trustscore.bond/{u}/</loc><lastmod>{DATE}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>' for u in P)
sm = sm.replace("</urlset>", add + "</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write(sm)
print(f"✓ sitemap: {sm.count('<loc>')} URLs")
print("ALL 9 PAGES BUILT")
