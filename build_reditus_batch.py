#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 4 new Reditus SaaS review pages on trustscore.bond (salesflow, textexpander, firstquote, expandi)."""
import re, json, os, html
from datetime import date

ROOT = "/tmp/ts-live"
TODAY = "October 14, 2026"
DATE = "2026-10-14"
CAT = "🧰 Software, SaaS &amp; B2B Tools"
CAT_RAW = "🧰 Software, SaaS & B2B Tools"

P = {
 "salesflow": dict(
  slug="salesflow-review", name="Salesflow", score="7.4", ring="74.0",
  badge_cls="b-amber", badge_txt="Mixed — read the cons",
  title="Salesflow Review 2026: Honest TrustScore 7.4/10",
  desc="Honest Salesflow review: TrustScore 7.4/10 — cloud LinkedIn automation, pricing from $79–99/seat, pros, cons and who should skip it. Updated October 14, 2026.",
  link="https://salesflow.io/?red=hhgg",
  lead="Cloud LinkedIn automation that plays it safe — and charges per seat for it.",
  what="""Salesflow automates the LinkedIn prospecting grind: connection requests, follow-up sequences, InMails and profile visits, run from the cloud (not a desktop scraper hammering your IP). A smart inbox consolidates conversations with light CRM-style contact management, and native integrations cover HubSpot, LinkedIn Sales Navigator and Zapier. The pitch is "safest social and email outreach platform" — cloud infrastructure, paced sending, warm-up behaviour — for B2B teams, agencies and startups. The company cites 10,000+ users and names like HubSpot, GoCardless and Verizon among customers.""",
  verdict="A solid, safety-first cloud platform for LinkedIn-heavy outbound. But email enrichment is not included and per-seat pricing stacks up for small teams — read the cons before swiping the card.",
  subs=[("quality","7.6"),("value","6.8"),("delivery","7.6"),("support","7.2")],
  for_you="B2B sales teams and agencies whose pipeline genuinely lives on LinkedIn, who want cloud-based automation with paced limits instead of risky desktop tools.",
  skip="Solo operators on a budget (seat + separate enrichment tool stacks fast), and anyone who expects built-in lead data — Salesflow sends campaigns, it does not source emails.",
  pros=["Cloud-based — no desktop software, no local-IP detection risk",
        "LinkedIn + email outreach combined in one dashboard",
        "Smart inbox with CRM-style contact management",
        "Native HubSpot, Sales Navigator and Zapier integrations",
        "Seat prices drop sharply at volume (down to ~$25–40/seat)"],
  cons=["Email enrichment is NOT included — you pay separately or bring verified emails",
        "Per-seat pricing is expensive for 1–2 person teams at $99/seat monthly",
        "Some users report LinkedIn account disconnections needing manual re-auth",
        "LinkedIn automation always carries account-restriction risk if limits are pushed"],
  price_rows=[("Price", "From $99/seat/mo (monthly) · $79/seat annual · 7-day free trial, no card"),
              ("Format", "Web-based SaaS — cloud dashboard, instant access"),
              ("Guarantee", "7-day free trial — terms on the vendor site")],
  faqs=[("How much does Salesflow cost?",
         "Pricing starts at $99 per seat per month, or $79/seat billed annually. Seat prices drop at volume — roughly $70 at 5 seats, $39.95 at 20 (Pro), down to ~$25 at 100. A 7-day free trial requires no card."),
        ("Is Salesflow safe for my LinkedIn account?",
         "It is cloud-based with paced sending and warm-up behaviour, which is materially safer than desktop scrapers — but no automation tool can promise zero risk. Stay inside LinkedIn's limits and warm new accounts slowly."),
        ("Does Salesflow include lead data or email finding?",
         "No. Enrichment is not bundled — you import your own leads or pay for a separate finder/verifier. Budget for that when comparing against all-in-one competitors."),
        ("Salesflow vs Expandi — which is better?",
         "Both are cloud LinkedIn tools around the same $99/seat price. Expandi adds dedicated country-based IPs and a longer track record; Salesflow's edge is the combined LinkedIn+email smart inbox. See our Expandi review for the full comparison.")],
  related=[("Expandi", "expandi-review", "TrustScore 7.9/10", "From ~$79–99/mo · 7-day free trial"),
           ("Woodpecker", "woodpecker-review", "TrustScore 7.7/10", "From ~$29/mo · 14-day free trial"),
           ("FirstQuote.ai", "firstquote-review", "TrustScore 7.8/10", "From $1.49–2.49/lead · no subscription")],
  cat_price="From ~$79–99/seat/mo · 7-day free trial"),
 "expandi": dict(
  slug="expandi-review", name="Expandi", score="7.9", ring="79.0",
  badge_cls="b-green", badge_txt="Recommended",
  title="Expandi Review 2026: Honest TrustScore 7.9/10",
  desc="Honest Expandi review: TrustScore 7.9/10 — cloud LinkedIn automation with dedicated country IPs and warm-up, pricing, pros, cons. Updated October 14, 2026.",
  link="https://app.expandi.io/?red=hhgg",
  lead="The LinkedIn automation veteran with the strongest safety story in the category.",
  what="""Expandi runs your LinkedIn outreach from the cloud with a safety architecture that is genuinely differentiating: every account gets a dedicated country-based IP address (so your activity looks local, not datacenter), and a profile auto warm-up phase ramps activity gradually with smart limit ranges instead of letting a new account blast 100 messages on day one. On top sit the workflow features: conditional sequences with if/then branching (prospect replied → stop; viewed profile → follow up), personalization with images, LinkedIn + email steps, and campaign analytics. It is one of the oldest tools in the space, which matters in a category full of one-year wonders.""",
  verdict="If LinkedIn outbound is your main channel, Expandi's dedicated IPs and warm-up discipline justify the premium over cheaper rivals. It is still LinkedIn automation — respect the limits — but this is the mature choice.",
  subs=[("quality","8.0"),("value","7.4"),("delivery","8.2"),("support","7.9")],
  for_you="Outbound teams and agencies who want a mature, cloud-based LinkedIn tool with the strongest account-safety features (country IPs, auto warm-up) and conditional sequences.",
  skip="Budget hunters — Dripify and SalesRobot do the basics at $59/mo — and anyone automating a brand-new LinkedIn profile that cannot afford any restriction risk at all.",
  pros=["Dedicated country-based IP per account — the category's best safety feature",
        "Profile auto warm-up with smart daily limit ranges",
        "Conditional (if/then) sequences, not just timed follow-ups",
        "Long-established tool with a large user base and track record",
        "7-day free trial"],
  cons=["$99/mo entry price — cheaper capable rivals exist (from ~$59)",
        "LinkedIn-first: email steps exist but are the side dish",
        "Learning curve on sequence building for non-technical users",
        "Automation risk is reduced, never eliminated — LinkedIn's rules still apply"],
  price_rows=[("Price", "Business from $99/mo (monthly) · ~$79/mo annual (−20%) · 7-day free trial"),
              ("Format", "Web-based SaaS — cloud dashboard, instant access"),
              ("Guarantee", "7-day free trial — terms on the vendor site")],
  faqs=[("How much does Expandi cost?",
         "The Business plan is $99/month, dropping to roughly $79/month billed annually (about 20% off). A 7-day free trial is available. Check the official site for current tiers."),
        ("Is Expandi safe to use with LinkedIn?",
         "Expandi is considered one of the safer options because each account runs on a dedicated country-based IP with automatic warm-up and conservative limits. That reduces risk substantially — but no automation tool can guarantee immunity from LinkedIn restrictions."),
        ("Expandi vs Salesflow — which should I pick?",
         "Both are cloud tools around the same price. Expandi wins on safety architecture (country IPs) and conditional sequences; Salesflow counters with a combined LinkedIn+email smart inbox. Our Salesflow review has the details."),
        ("Can Expandi also send emails?",
         "Yes — sequences can include email steps synced with your mailbox, but Expandi is LinkedIn-first. For cold-email-primary workflows, look at a deliverability-focused tool like Woodpecker.")],
  related=[("Salesflow", "salesflow-review", "TrustScore 7.4/10", "From ~$79–99/seat/mo · 7-day trial"),
           ("Woodpecker", "woodpecker-review", "TrustScore 7.7/10", "From ~$29/mo · 14-day free trial"),
           ("Leadpages", "leadpages-review", "TrustScore 8.2/10", "From ~$99/mo (annual discounts) · 14-day trial")],
  cat_price="From ~$79–99/mo · 7-day free trial"),
 "firstquote": dict(
  slug="firstquote-review", name="FirstQuote.ai", score="7.8", ring="78.0",
  badge_cls="b-amber", badge_txt="Recommended",
  title="FirstQuote.ai Review 2026: Honest TrustScore 7.8/10",
  desc="Honest FirstQuote.ai review: TrustScore 7.8/10 — AI autoresponder for Yelp, Thumbtack and Google LSA leads, pay-per-lead pricing, pros, cons. Updated October 14, 2026.",
  link="https://firstquote.ai/?red=hhgg",
  lead="AI that answers your Yelp and Thumbtack leads in under 10 seconds — and you only pay for qualified ones.",
  what="""FirstQuote.ai solves a pain every local service business owner knows: you're on a job site, a lead arrives on Yelp, Thumbtack or Google Local Services Ads, and the first business to reply wins the job. FirstQuote connects to those lead sources and auto-replies in under 10 seconds — in your own voice and tone — then qualifies the prospect (SMS and two-way calls) and pings you when a lead is ready to book. The dashboard is a plain inbox with conversation summaries. The business model is the interesting part: no subscription. You pay per qualified lead ($2.49 for the first 30 each week, $1.49 after), and unqualified or duplicate leads are not billed.""",
  verdict="For movers, plumbers, cleaners and landscapers bleeding jobs to faster responders, pay-per-qualified-lead beats another $99/mo SaaS seat. Young product — check the trial math on your own lead volume first.",
  subs=[("quality","7.6"),("value","8.4"),("delivery","8.0"),("support","7.4")],
  for_you="Local service businesses (moving, plumbing, cleaning, landscaping…) buying leads on Yelp, Thumbtack or Google LSA who keep losing jobs because they can't answer fast enough while working.",
  skip="Businesses without steady inbound lead volume (there's nothing to auto-answer), anyone needing a full CRM (this is a response layer, not a pipeline manager), and skeptics who want a decade-old vendor — this is a young product.",
  pros=["Pay only for qualified leads — no monthly subscription, no empty months",
        "Sub-10-second replies in the owner's own voice, 24/7",
        "Qualifies leads and alerts you only when they're ready to book",
        "Works where the leads already are: Yelp, Thumbtack, Google LSA",
        "7-day free trial, no card"],
  cons=["Young company — smaller track record than established SaaS vendors",
        "Cost scales with lead volume (a good problem, but a cost)",
        "AI replies occasionally need supervision to stay on-brand",
        "Only relevant if you actually buy leads on the supported platforms"],
  price_rows=[("Price", "$2.49/qualified lead for the first 30 each week · $1.49 after · billed weekly, no subscription"),
              ("Format", "Web app connected to Yelp, Thumbtack & Google LSA — setup in minutes"),
              ("Guarantee", "7-day free trial, no card · unqualified leads not billed")],
  faqs=[("How much does FirstQuote.ai cost?",
         "There is no subscription: you pay $2.49 per qualified lead for the first 30 each week, then $1.49 per qualified lead. Billing is weekly, unqualified and duplicate leads are not charged, and a 7-day trial needs no card."),
        ("Which lead sources does FirstQuote.ai support?",
         "It connects to Yelp, Thumbtack and Google Local Services Ads — the channels where local service businesses buy leads — and replies by SMS and two-way calls."),
        ("Does the AI really sound like my business?",
         "You train it on your tone, services and pricing examples, so replies go out in your voice. It's AI — supervise it early on and correct it when it drifts."),
        ("Is pay-per-lead better than a monthly subscription?",
         "If your lead volume is irregular, yes — quiet weeks cost nothing. If you run high constant volume, do the math: 100+ qualified leads a week at $1.49 adds up, though it's still small next to what one won job earns.")],
  related=[("Salesflow", "salesflow-review", "TrustScore 7.4/10", "From ~$79–99/seat/mo · 7-day trial"),
           ("Woodpecker", "woodpecker-review", "TrustScore 7.7/10", "From ~$29/mo · 14-day free trial"),
           ("noCRM.io", "nocrm-io-review", "TrustScore 7.8/10", "From ~$12/user/mo · 15-day trial, no card")],
  cat_price="From $1.49–2.49/qualified lead · no subscription"),
 "textexpander": dict(
  slug="textexpander-review", name="TextExpander", score="8.4", ring="84.0",
  badge_cls="b-green", badge_txt="Recommended",
  title="TextExpander Review 2026: Honest TrustScore 8.4/10",
  desc="Honest TextExpander review: TrustScore 8.4/10 — the text expansion veteran with a free plan: pricing, pros, cons and who should skip it. Updated October 14, 2026.",
  link="https://textexpander.com/?red=hhgg&amp;utm_source=hhgg&amp;utm_medium=revshare&amp;utm_affiliate_network=reditus",
  lead="The 25-year veteran of typing less — now with a free plan, it's the easiest productivity win left.",
  what="""TextExpander does one thing extremely well: you type a short abbreviation, it expands into whatever text you define — email templates, code snippets, addresses, support macros with fill-in fields and optional scripts. It works across Mac, Windows, Chrome and iPhone/iPad, and the current headline is a free-forever plan, which makes trying it frictionless. For teams, shared snippet groups keep everyone's answers consistent (support, sales, healthcare, legal all use it heavily), and newer AI features surface the right snippet based on what you're working on in Chrome. This is a mature, focused product — category king for a reason.""",
  verdict="If you type the same things twice a week or more, TextExpander pays for itself in the first day. The free plan makes it a no-brainer try; teams pay per user, so count seats first.",
  subs=[("quality","8.6"),("value","8.8"),("delivery","8.0"),("support","8.2")],
  for_you="Anyone who retypes the same content — support agents, recruiters, sales, developers, medical and legal staff — and teams that want consistent answers across every reply.",
  skip="People who type unique prose all day (there's nothing to expand), Android-only users (no native app), and teams needing heavy workflow automation — this expands text, it isn't Zapier.",
  pros=["Free-forever plan — the easiest yes in productivity software",
        "Cross-platform: Mac, Windows, Chrome, iPhone & iPad",
        "Fill-ins, optional scripts and AI snippet recommendations",
        "Shared team snippet groups keep answers consistent",
        "Two decades of development — polished where rivals feel beta"],
  cons=["Team pricing is per user per month — big teams pay accordingly",
        "Advanced features (scripts, nested fill-ins) have a learning curve",
        "No native Android app",
        "Value depends entirely on how much you retype — unique writers gain little"],
  price_rows=[("Price", "Free-forever plan · individual and team paid tiers — current prices on the official site"),
              ("Format", "Native apps (Mac, Windows, iOS) + Chrome extension"),
              ("Guarantee", "Free plan — no card needed")],
  faqs=[("Is TextExpander free?",
         "Yes — TextExpander now has a free-forever plan covering core expansion features. Paid individual and team tiers add sharing, advanced fill-ins and admin controls; check the official site for current pricing."),
        ("Does TextExpander work on Windows and Mac?",
         "Yes — native apps for Mac and Windows, a Chrome extension that covers ChromeOS and Linux workflows, and iPhone/iPad apps. There is no native Android app."),
        ("What is TextExpander actually good for?",
         "Anything you type repeatedly: email replies, support answers, code blocks, addresses, signatures. Fill-in fields turn a snippet into a mini-form so each expansion is tailored in seconds."),
        ("Is TextExpander worth it for teams?",
         "For support, sales, recruiting and medical/legal teams, shared snippet groups standardize answers and cut onboarding time. Pricing is per user, so measure that against hours saved.")],
  related=[("involve.me", "involveme-review", "TrustScore 7.8/10", "Free plan · paid from ~$29/mo"),
           ("AhaSlides", "ahaslides-review", "TrustScore 7.8/10", "Free plan · paid from ~$8/mo (annual)"),
           ("Signitic", "signitic-review", "TrustScore 7.8/10", "Free plan (≤19 staff) · €1/user/mo from 20")],
  cat_price="Free plan · paid tiers per user"),
}

def build(p):
    t = open(f"{ROOT}/reviews/woodpecker-review/index.html", encoding="utf-8").read()
    link_attr = p["link"]  # already &amp;-escaped where needed
    # head
    t = re.sub(r"<title>[^<]*</title>", f'<title>{p["title"]}</title>', t)
    t = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{p["desc"]}"', t)
    t = t.replace('href="https://trustscore.bond/reviews/woodpecker-review/"', f'href="https://trustscore.bond/reviews/{p["slug"]}/"')
    t = t.replace("woodpecker-review", p["slug"]).replace("Woodpecker Review 2026: Honest TrustScore 7.7/10 (Pros &amp; Cons)", p["title"])
    t = t.replace('<meta property="og:title" content="Woodpecker Review 2026: Honest TrustScore 7.7/10 (Pros &amp; Cons)">', f'<meta property="og:title" content="{p["title"]}">')
    t = t.replace('<meta name="twitter:title" content="Woodpecker Review 2026: Honest TrustScore 7.7/10 (Pros &amp; Cons)">', f'<meta name="twitter:title" content="{p["title"]}">')
    t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+p["desc"]+m.group(2), t)
    t = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1)+p["desc"]+m.group(2), t)
    t = t.replace('Honest Woodpecker review: TrustScore 7.7/10 — what you get, pricing, pros, cons and who should skip it. Updated October 3, 2026.', p["desc"])
    t = t.replace("Updated October 3, 2026", f"Updated {TODAY}")
    t = t.replace('content="2026-10-03"', f'content="{DATE}"')
    t = t.replace('"datePublished": "2026-10-03"', f'"datePublished": "{DATE}"')
    # h1/lead/kicker
    t = t.replace("<h1>Woodpecker Review: TrustScore 7.7/10</h1>", f'<h1>{p["name"]} Review: TrustScore {p["score"]}/10</h1>')
    t = t.replace('<p class="lead">Cold email with deliverability as the product\'s spine.</p>', f'<p class="lead">{p["lead"]}</p>')
    t = t.replace(f'<nav class="crumbs"><a href="/">Home</a> › <a href="/reviews/">Reviews</a> › <a href="/category/saas/">Software, SaaS &amp; B2B Tools</a> › <span>Woodpecker</span></nav>',
                  f'<nav class="crumbs"><a href="/">Home</a> › <a href="/reviews/">Reviews</a> › <a href="/category/saas/">Software, SaaS &amp; B2B Tools</a> › <span>{p["name"]}</span></nav>')
    # body sections
    t = re.sub(r'<section class="hero">.*?</section>', '', t, flags=re.S)  # will re-add below
    hero = f'''<section class="hero">
  <div>
    <p>{p["what"].split(". ")[0]}. {p["what"].split(". ")[1] if len(p["what"].split(". "))>1 else ""}</p>
    <div class="verdict"><b>The verdict:</b> {p["verdict"]}</div>
    <a class="cta" href="{link_attr}" rel="sponsored nofollow noopener" target="_blank">Try {p["name"]} — official site →</a>
    <p class="note">Paid link. We earn a commission at no extra cost to you — it funds these reviews. <a href="/disclosure/">Full disclosure</a>.</p>
  </div>
  <div class="scorecard">
    <span class="badge {p["badge_cls"]}">{p["badge_txt"]}</span>
    <div class="ring" style="--p:{p["ring"]}"><span><b>{p["score"]}</b><small>TRUSTSCORE /10</small></span></div>
    <div class="subs">{''.join(f'<div class="row"><span>{k}</span><span class="bar"><i style="width:{float(v)*10}%"></i></span><b>{v}</b></div>' for k,v in p["subs"])}</div>
    <p class="note">Weighted: quality 35% · value 30% · delivery 20% · support 15%. <a href="/methodology/">Methodology</a>.</p>
  </div>
</section>'''
    t = t.replace('<img class="imgfull"', hero + '\n<img class="imgfull"', 1)
    # what you get
    t = re.sub(r'<h2>What you actually get</h2>\n<p>.*?</p>', f'<h2>What you actually get</h2>\n<p>{p["what"]}</p>', t, flags=re.S)
    # for/skip
    t = re.sub(r'<div class="pros"><h3>✔ Made for you if…</h3><p>.*?</p></div>\s*<div class="cons"><h3>✘ Skip it if…</h3><p>.*?</p></div>',
               f'<div class="pros"><h3>✔ Made for you if…</h3><p>{p["for_you"]}</p></div>\n  <div class="cons"><h3>✘ Skip it if…</h3><p>{p["skip"]}</p></div>', t, flags=re.S)
    # pros/cons lists
    t = re.sub(r'<div class="pros"><h3>What we liked</h3><ul>.*?</ul></div>',
               '<div class="pros"><h3>What we liked</h3><ul>' + ''.join(f'<li>{x}</li>' for x in p["pros"]) + '</ul></div>', t, flags=re.S)
    t = re.sub(r'<div class="cons"><h3>What could be better</h3><ul>.*?</ul></div>',
               '<div class="cons"><h3>What could be better</h3><ul>' + ''.join(f'<li>{x}</li>' for x in p["cons"]) + '</ul></div>', t, flags=re.S)
    # pricing
    t = re.sub(r'<div class="tablewrap"><table>.*?</table></div>',
               '<div class="tablewrap"><table>\n<tr><th>Item</th><th>Details</th></tr>\n' + ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k,v in p["price_rows"]) + '\n</table></div>', t, flags=re.S)
    # CTAs
    t = t.replace('Try Woodpecker — official site →', f'Try {p["name"]} — official site →').replace('See Woodpecker — official site →', f'See {p["name"]} — official site →')
    t = t.replace('https://woodpecker.co/?red=hhgg', link_attr)
    t = t.replace('our full comparison table', 'the alternatives in related reviews below')
    t = re.sub(r'<p class="note">See it side-by-side[^<]*</p>', '', t)
    # FAQ
    faq_html = '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in p["faqs"]) + '</div>'
    t = re.sub(r'<div class="faq">.*?</div>', faq_html, t, flags=re.S)
    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faqs"]]}, ensure_ascii=False)
    t = re.sub(r'(<script type="application/ld\+json">)\{"@context": "https://schema.org", "@type": "FAQPage".*?\}(</script>)', lambda m: m.group(1)+faq_ld+m.group(2), t, flags=re.S)
    # software schema
    sw = {"@context":"https://schema.org","@type":"SoftwareApplication","name":p["name"],
          "description":p["lead"]+" "+p["verdict"],"applicationCategory":"BusinessApplication","operatingSystem":"Web",
          "image":f"https://trustscore.bond/og/{p['slug']}.png",
          "review":{"@type":"Review","reviewRating":{"@type":"Rating","ratingValue":p["score"],"bestRating":"10","worstRating":"1"},
                    "author":{"@type":"Person","name":"Hamdi Arij","jobTitle":"Pro Reviewer","url":"https://trustscore.bond/how-we-review/#author"},
                    "datePublished":DATE},
          "offers":{"@type":"Offer","price":p["price_rows"][0][1].split("$")[1].split("/")[0].split(" ")[0] if "$" in p["price_rows"][0][1] else "0","priceCurrency":"USD","availability":"https://schema.org/InStock","url":f"https://trustscore.bond/reviews/{p['slug']}/"}}
    t = re.sub(r'(<script type="application/ld\+json">)\{"@context": "https://schema.org", "@type": "SoftwareApplication".*?\}(</script>)', lambda m: m.group(1)+json.dumps(sw,ensure_ascii=False)+m.group(2), t, flags=re.S)
    # breadcrumb
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://trustscore.bond/"},
        {"@type":"ListItem","position":2,"name":"Reviews","item":"https://trustscore.bond/reviews/"},
        {"@type":"ListItem","position":3,"name":p["name"],"item":f"https://trustscore.bond/reviews/{p['slug']}/"}]}
    t = re.sub(r'(<script type="application/ld\+json">)\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?\}(</script>)', lambda m: m.group(1)+json.dumps(bc,ensure_ascii=False)+m.group(2), t, flags=re.S)
    # related cards
    cards = ''.join(f'<a class="card" href="/reviews/{s}/"><span class="cat">{CAT}</span><b>{n}</b><span class="score">{sc}</span><span class="price">{pr}</span></a>' for n,s,sc,pr in p["related"])
    t = re.sub(r'<section class="cards">.*?</section>', f'<section class="cards">{cards}</section>', t, flags=re.S)
    # alt text
    t = t.replace('alt="Woodpecker TrustScore card — 7.7 out of 10"', f'alt="{p["name"]} TrustScore card — {p["score"]} out of 10"')
    t = t.replace('Try Woodpecker', f'Try {p["name"]}').replace('See Woodpecker', f'See {p["name"]}')
    # leftover woodpecker mentions check happens in validation
    os.makedirs(f"{ROOT}/reviews/{p['slug']}", exist_ok=True)
    open(f"{ROOT}/reviews/{p['slug']}/index.html", "w", encoding="utf-8").write(t)
    return t

for slug, p in P.items():
    build(p)
    print(f"✓ built reviews/{p['slug']}/index.html")

# ---------- OG images ----------
from PIL import Image, ImageDraw, ImageFont
def og(p):
    W,H = 1200,630
    img = Image.new("RGB",(W,H),(16,26,51))
    d = ImageDraw.Draw(img)
    for y in range(H):  # subtle gradient
        d.line([(0,y),(W,y)], fill=(16+y//22, 26+y//26, 51+min(30,y//14)))
    try: f_big=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",88); f_mid=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",150); f_sm=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",34); f_xs=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",26)
    except: f_big=f_mid=f_sm=f_xs=ImageFont.load_default()
    d.rounded_rectangle([60,60,190,190],28,fill=(240,180,41))
    d.text((125,125),"TS",font=f_big,fill=(16,26,51),anchor="mm")
    d.text((90,235),"TrustScore",font=f_big,fill=(255,255,255),anchor="lm")
    d.text((92,330),".bond — honest review",font=f_sm,fill=(170,182,214),anchor="lm")
    d.text((90,470),p["score"],font=f_mid,fill=(240,180,41),anchor="lm")
    d.text((95,600),f"/10 TrustScore · {p['name']} review",font=f_xs,fill=(170,182,214),anchor="lm")
    d.text((1140,110),p["name"],font=f_big,fill=(255,255,255),anchor="rm")
    d.text((1140,205),"Software · SaaS · B2B",font=f_sm,fill=(170,182,214),anchor="rm")
    d.text((1140,600),"Updated "+TODAY,font=f_xs,fill=(170,182,214),anchor="rm")
    img.save(f"{ROOT}/og/{p['slug']}.png")
for p in P.values(): og(p); print(f"✓ og/{p['slug']}.png")

# ---------- category + reviews index cards ----------
def card_html(p):
    return f'<a class="card" href="/reviews/{p["slug"]}/"><span class="cat">{CAT_RAW}</span><b>{p["name"]}</b><span class="score">TrustScore {p["score"]}/10</span><span class="price">{html.escape(p["cat_price"])}</span></a>'

CARD_RE = re.compile(r'<a class="card" href="/reviews/[a-z0-9-]+/"><span class="cat">🧰 Software, SaaS (?:&amp;|&) B2B Tools</span>.*?</a>')
def insert_inplace(page_path, cards_new):
    for p in cards_new:
        s = open(page_path, encoding="utf-8").read()
        if p["slug"] in s: continue
        cards = CARD_RE.findall(s)
        best = None
        for c in cards:
            sc = float(re.search(r'TrustScore ([\d.]+)/10', c).group(1))
            if sc < float(p["score"]): best = c; break
        new = card_html(p)
        if best is not None:
            s = s.replace(best, new + best, 1)
        else:
            last = cards[-1]
            s = s.replace(last, last + new, 1)
        open(page_path, "w", encoding="utf-8").write(s)
    return len(CARD_RE.findall(open(page_path, encoding="utf-8").read()))

n1 = insert_inplace(f"{ROOT}/category/saas/index.html", list(P.values()))
print(f"✓ category/saas — {n1} saas cards sorted")
# reviews/index.html uses same cards — apply
n2 = insert_inplace(f"{ROOT}/reviews/index.html", list(P.values()))
print(f"✓ reviews/index — {n2} saas cards sorted")

# ---------- woodpecker + warmupinbox related cards ----------
for target, extra in [(f"{ROOT}/reviews/woodpecker-review/index.html", [P["salesflow"], P["expandi"], P["firstquote"]]),
                      (f"{ROOT}/reviews/warmupinbox-review/index.html", [P["expandi"], P["salesflow"]])]:
    s = open(target, encoding="utf-8").read()
    m = re.search(r'(<section class="cards">)(.*?)(</section>)', s, re.S)
    added = ''.join(card_html(p) for p in extra)
    s = s[:m.end(2)] + added + s[m.end(2):]
    open(target, "w", encoding="utf-8").write(s)
    print(f"✓ related cards added → {target.split('/')[-2]}")

# ---------- sitemap ----------
sm = open(f"{ROOT}/sitemap.xml", encoding="utf-8").read()
m = re.search(r'<url>\s*<loc>https://trustscore.bond/reviews/woodpecker-review/</loc>.*?</url>', sm, re.S)
tpl = m.group(0)
for p in P.values():
    entry = re.sub(r'<loc>[^<]*</loc>', f'<loc>https://trustscore.bond/reviews/{p["slug"]}/</loc>', tpl)
    entry = re.sub(r'<lastmod>[^<]*</lastmod>', f'<lastmod>{DATE}</lastmod>', entry)
    sm = sm.replace("</urlset>", entry + "</urlset>")
open(f"{ROOT}/sitemap.xml", "w", encoding="utf-8").write(sm)
print(f"✓ sitemap: {sm.count('<loc>')} entries")
print("DONE")
