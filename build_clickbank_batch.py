#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ClickBank Wednesday: build 6 new review pages on trustscore.bond."""
import re, json, os, html as HH
import glob as G
from datetime import date

ROOT = "/tmp/ts-live"
TODAY = "October 15, 2026"
DATE = "2026-10-15"
AFF = "heditouati"

def hop(vendor, tid):
    return f"https://hop.clickbank.net/?affiliate={AFF}&amp;vendor={vendor}&amp;tid={tid}"

CATS = {
 "abundance": "🌟 Manifestation, Wealth &amp; Energy",
 "mind": "🔮 Numerology, Astrology &amp; Archetypes",
 "health": "💊 Health, Weight &amp; Supplements",
}
CATS_RAW = {k: v.replace("&amp;", "&") for k, v in CATS.items()}

P = {
 "genius": dict(
  slug="genius-switch-review", name="The Genius Switch", score="6.8", ring="68.0",
  badge_cls="b-amber", badge_txt="Mixed — read the cons", cat="abundance",
  title="The Genius Switch Review 2026: TrustScore 6.8/10",
  desc="Honest Genius Switch review: TrustScore 6.8/10 — the high-gravity manifestation program, what you get, price, pros, cons and who should skip it. Updated October 15, 2026.",
  vendor="THEGENIUSX", tid="tsbgenius", fallback="https://geniusswitchoriginal.com/",
  price_note="~$39–49 one-time (ClickBank reports $45.49 average per sale)",
  lead="A high-gravity manifestation program with a classic long-form sales funnel.",
  what="""The Genius Switch is a digital manifestation and mindset program sold through ClickBank, where it currently carries one of the highest gravity scores in the Spirituality &amp; New Age category (92+ at the time of writing) — marketplace shorthand for "a lot of affiliates are making sales right now." The sales page uses the classic long-form video sales letter format: a personal rags-to-riches story, a "simple switch" mechanism claim, and a discounted one-time price. The product itself is a members-area program: audio/file-based daily exercises framed around activating focus and abundance thinking. What you're really buying is a structured daily mindset ritual, not a business tool.""",
  verdict="Sells like crazy because the funnel is excellent, not because the method is new. As a daily mindset ritual it can help; as a life 'switch' it overpromises. Buy it for the ritual, skip it if you expect the story's results.",
  subs=[("quality","6.6"),("value","6.4"),("delivery","7.2"),("support","6.8")],
  for_you="People who want a low-effort daily mindset/audio ritual and enjoy motivational framing — and who won't be upset if results arrive slower than the sales page implies.",
  skip="Anyone expecting a concrete money-making system (there's no 'how', it's mindset content), and anyone allergic to upsell funnels — the checkout path has them.",
  pros=["Very high marketplace gravity — a proven, smooth funnel with real refund policy via ClickBank",
        "Low one-time price point for a full program",
        "Daily audio rituals can genuinely help focus and habit framing",
        "60-day ClickBank refund window applies"],
  cons=["Heavy 'overnight results' marketing framing — treat the story as marketing, not a promise",
        "The 'switch' mechanism is presentation, not science",
        "Upsell sequence after purchase (typical for this category)",
        "No community or coaching at the base price"],
  price_rows=[("Price", "One-time digital purchase — ClickBank reports $45.49 average per sale (front-end + order bumps vary)"),
              ("Format", "Digital members area — instant access after purchase"),
              ("Guarantee", "60-day ClickBank refund policy — check terms at checkout")],
  faqs=[("What is The Genius Switch?",
         "A digital manifestation/mindset program sold on ClickBank: daily audio-style exercises framed as flipping a mental 'switch' for focus and abundance. It's mindset content, not a business course."),
        ("How much does The Genius Switch cost?",
         "It's a one-time purchase; ClickBank marketplace data shows an average of $45.49 per sale including front-end and bumps. Expect order-bump offers during checkout."),
        ("Is The Genius Switch a scam?",
         "It's a legally sold ClickBank product with a 60-day refund window — not a scam. Our concern is marketing framing: the promise curve is steep for what is essentially a mindset ritual program."),
        ("Does The Genius Switch actually work?",
         "As a daily focus/ritual habit, some users find value. As a literal wealth 'switch', no program delivers that — results depend on what you do outside the audio.")],
  related=[("Wealth DNA Code", "wealth-dna-code-review", "7.4"), ("The Last Wish", "the-last-wish-review", "6.9"), ("The BioEnergy Code", "bioenergy-code-review", "8.0")],
  cat_price="One-time · ~$45 avg sale"),
 "lastwish": dict(
  slug="the-last-wish-review", name="The Last Wish", score="6.9", ring="69.0",
  badge_cls="b-amber", badge_txt="Mixed — read the cons", cat="abundance",
  title="The Last Wish Review 2026: TrustScore 6.9/10",
  desc="Honest The Last Wish review: TrustScore 6.9/10 — the new high-gravity manifestation offer, what's behind the funnel, price, pros, cons. Updated October 15, 2026.",
  vendor="UMAKEBREAD", tid="tsblastwish", fallback="https://messageofmanifestation.org/",
  price_note="~$39–49 one-time (ClickBank reports $48.49 average per sale)",
  lead="The newest heavy-hitter in the manifestation niche — $500k of ad testing behind one VSL.",
  what="""The Last Wish is a 2026 manifestation offer that has climbed fast on ClickBank (gravity ~89 within months of launch). The marketplace listing itself advertises "$500k in ad testing" — translation: the sales funnel is engineered to convert, and it shows: the landing page runs the same long-form video sales letter playbook as the category's biggest hits (it shares its funnel template with The Genius Switch's page). The product behind the VSL is a digital manifestation program in the now-standard format: a personal story hook, a symbolic "wish" mechanism, and members-area content built around guided exercises. Nothing about the format is new — what's new is the marketing budget.""",
  verdict="A well-marketed entry in a crowded genre. If you already know you like guided manifestation content, the refund window makes it a low-risk try. If you're new to this niche, start with an 8+ scored program from our list instead.",
  subs=[("quality","6.7"),("value","6.5"),("delivery","7.0"),("support","6.8")],
  for_you="Manifestation-curious buyers who respond to story-driven programs and want the newest heavily-tested funnel — with the safety of ClickBank's refund policy.",
  skip="Repeat buyers of manifestation courses (you likely own this content under another name), and anyone who researches before emotion — the funnel is built for impulse.",
  pros=["ClickBank's 60-day refund policy applies",
        "High production-value presentation",
        "Gravity ~89 — the funnel converts, so at minimum it's polished",
        "One-time price, no subscription trap"],
  cons=["Brand-new offer with no long-term track record or verified testimonials",
        "Same funnel template as other offers in the genre — the 'new' is mostly the marketing",
        "'$500k in ad testing' optimizes the seller's conversion, not your results",
        "Post-purchase upsell path"],
  price_rows=[("Price", "One-time digital purchase — ClickBank reports $48.49 average per sale"),
              ("Format", "Digital members area — instant access"),
              ("Guarantee", "60-day ClickBank refund policy — check terms at checkout")],
  faqs=[("What is The Last Wish?",
         "A 2026 manifestation program sold on ClickBank — story-driven VSL front, members-area guided exercises behind it. The offer's claim to fame is its marketing budget, not a new method."),
        ("How much does The Last Wish cost?",
         "A one-time purchase; ClickBank data shows a $48.49 average per sale. Order bumps and upsells are part of the path."),
        ("Is The Last Wish different from The Genius Switch?",
         "The landing pages share the same funnel template. Both are manifestation VSL programs from the same production ecosystem — if you own one, you likely know what the other contains."),
        ("Is there a refund policy?",
         "Yes — the standard ClickBank 60-day refund window applies, which is the main safety net for trying new offers like this one.")],
  related=[("The Genius Switch", "genius-switch-review", "6.8"), ("Soul Manifestation", "soul-manifestation-review", "7.8"), ("Manifestation Magic", "manifestation-magic-review", "7.5")],
  cat_price="One-time · ~$48 avg sale"),
 "astrolang": dict(
  slug="astrology-language-review", name="Your Astrology Language", score="7.6", ring="76.0",
  badge_cls="b-amber", badge_txt="Recommended", cat="mind",
  title="Astrology Language Review 2026: TrustScore 7.6/10",
  desc="Honest Your Astrology Language review: TrustScore 7.6/10 — personalized astrology reports, pricing, pros, cons and who should skip it. Updated October 15, 2026.",
  vendor="ASTROLAN", tid="tsbastrolang", fallback="https://start.yourastrologylanguage.net/",
  price_note="Report from ~$20–40 (ClickBank reports $38.62 average per sale)",
  lead="Personalized astrology readings from one of the niche's longest-running platforms.",
  what="""Your Astrology Language is a personalized-astrology-report service with serious staying power: gravity of ~69 after years on ClickBank, in the same league as the niche's established names. The flow is the modern standard: enter your birth details, receive a free teaser reading, then get offered a full personalized report (natal, forecast, and compatibility angles) as a one-time purchase. What distinguishes it from social-media astrologers is depth — the reports are long, chart-based and individually generated rather than generic sun-sign copy. What doesn't change is the funnel math: the free reading exists to sell the full report, and the upsell path includes additional premium reports.""",
  verdict="For astrology fans who want a genuinely personalized, chart-based report (not magazine horoscopes), this is one of the category's reliable choices — with the standard upsell dance at checkout.",
  subs=[("quality","7.8"),("value","7.2"),("delivery","7.8"),("support","7.2")],
  for_you="Astrology enthusiasts who want detailed birth-chart-based reports and don't mind the free-teaser-to-paid-report funnel.",
  skip="Skeptics (obviously), and anyone expecting a live human astrologer — this is generated personalized reports, not a session.",
  pros=["Years of marketplace longevity — an established platform, not a launch-week offer",
        "Reports are chart-based and genuinely personalized to birth data",
        "Free teaser reading lets you judge quality before paying",
        "ClickBank's 60-day refund policy"],
  cons=["The free reading is a lead-in — full reports cost extra",
        "Upsell path pushes additional premium reports after the first purchase",
        "Generated reports, not a live reading with a human astrologer",
        "Depth is impressive, but astrology's predictive claims are belief-based"],
  price_rows=[("Price", "Personalized reports — ClickBank reports $38.62 average per sale (free teaser reading first)"),
              ("Format", "Online personalized report — delivered digitally after birth-details entry"),
              ("Guarantee", "60-day ClickBank refund policy — check terms at checkout")],
  faqs=[("What is Your Astrology Language?",
         "A personalized astrology report service on ClickBank: you enter birth details, get a free teaser, and can buy full chart-based reports (natal, forecast, compatibility)."),
        ("How much does Your Astrology Language cost?",
         "The full reports average $38.62 per sale according to ClickBank data, with a free introductory reading before any payment."),
        ("Is Your Astrology Language legit?",
         "It's a long-running ClickBank offer (gravity ~69) — established and refund-protected. 'Legit' as a product, yes; whether astrology resonates with you is a personal question."),
        ("Do I talk to a real astrologer?",
         "No — the reports are individually generated from your birth data, not live sessions. That keeps the price low but means no back-and-forth.")],
  related=[("Astrology.TV", "astrology-tv-review", "7.9"), ("Numerologist.com", "numerologist-com-review", "8.5"), ("Individualogist", "individualogist-review", "7.3")],
  cat_price="Free teaser · reports ~$39 avg"),
 "soup": dict(
  slug="rapid-soup-diet-review", name="14 Day Rapid Soup Diet", score="7.0", ring="70.0",
  badge_cls="b-amber", badge_txt="Mixed — read the cons", cat="health",
  title="14 Day Rapid Soup Diet Review 2026: 7.0/10",
  desc="Honest 14 Day Rapid Soup Diet review: TrustScore 7.0/10 — the soup-based rapid weight loss plan, price, pros, cons and who should skip it. Updated October 15, 2026.",
  vendor="KETOSOUP82", tid="tsbsoup", fallback="https://foodsthatslim.com/",
  price_note="~$25 one-time (ClickBank reports $24.81 average per sale)",
  lead="A short, soup-forward crash diet that works exactly as long as you can live on soup.",
  what="""The 14 Day Rapid Soup Diet is a keto-aligned, soup-based rapid weight-loss plan sold on ClickBank (gravity ~12, $24.81 average sale — one of the more affordable front-ends in the diet niche). The mechanism is honest and old: low-calorie, high-satiety soups for two weeks produce a fast drop on the scale — a mix of fat, water and glycogen. The program gives you the soup recipes, the schedule and the shopping lists; the current sales page trades as "Flat Belly Soup Diet" (same vendor). As a reset or a kickstart it does what it says. As a lifestyle it is not designed — 14 days of mostly soup is a crash diet, and the research on crash diets is consistent: what comes off fast goes back on fast without a maintenance plan.""",
  verdict="A cheap, structured 14-day reset that delivers a fast scale drop — buy it for the kickstart, not as a permanent diet, and keep expectations about rebound realistic.",
  subs=[("quality","7.0"),("value","7.6"),("delivery","7.2"),("support","6.4")],
  for_you="Someone who wants an inexpensive, tightly structured 14-day kickstart to break a plateau or kick off a longer plan.",
  skip="Anyone with a history of yo-yo dieting, and anyone seeking a sustainable long-term nutrition plan — this is a sprint, not a lifestyle.",
  pros=["Very affordable front-end (~$25)",
        "Soup-based meals are genuinely high-satiety for the calories",
        "Fully structured: recipes, schedule, shopping lists",
        "ClickBank's 60-day refund policy"],
  cons=["Crash-diet physics: fast loss includes water and glycogen, and rebounds without maintenance",
        "14 days of mostly soup is socially and practically hard",
        "Sales page trades as 'Flat Belly Soup Diet' — spot-reduction framing is marketing",
        "Not suitable as a long-term nutrition plan"],
  price_rows=[("Price", "One-time ~$25 — ClickBank reports $24.81 average per sale"),
              ("Format", "Digital plan (recipes + schedule) — instant access"),
              ("Guarantee", "60-day ClickBank refund policy — check terms at checkout")],
  faqs=[("What is the 14 Day Rapid Soup Diet?",
         "A keto-aligned, soup-based 14-day rapid weight-loss plan: low-calorie high-satiety soups, with recipes, schedules and shopping lists included."),
        ("How much weight can you lose on the soup diet?",
         "Short very-low-calorie diets typically show a fast 3–7 lb scale drop in two weeks — a mix of water, glycogen and fat. Sustainable fat loss is slower; plan for the rebound risk."),
        ("Is the Rapid Soup Diet healthy?",
         "For two weeks as a kickstart, most healthy adults tolerate it. As a long-term diet, no — it's too restrictive. Check with a doctor if you have any medical condition."),
        ("How much does it cost?",
         "About $25 one-time — one of the cheapest structured diet programs on ClickBank.")],
  related=[("The Smoothie Diet", "smoothie-diet-review", "7.3"), ("Alpilean", "alpilean-review", "6.9"), ("Mitolyn", "mitolyn-review", "7.1")],
  cat_price="One-time ~$25"),
 "gdi": dict(
  slug="go-digital-income-review", name="Go Digital Income", score="6.0", ring="60.0",
  badge_cls="b-amber", badge_txt="Mixed — read the cons", cat="abundance",
  title="Go Digital Income Review 2026: TrustScore 6.0/10",
  desc="Honest Go Digital Income review: TrustScore 6.0/10 — the new bizopp/MMO offer, red flags, price, pros, cons. Updated October 15, 2026.",
  vendor="SMPM123", tid="tsbgdi", fallback="https://godigitalincome.com/",
  price_note="Low-ticket front-end (ClickBank reports $12.35 average per sale)",
  lead="A low-ticket bizopp with a classic funnel — read this one before the sales page reads you.",
  what="""Go Digital Income is a brand-new "business opportunity / make money online" offer on ClickBank (the marketplace listing literally announces "Brand New BizOpp/MMO Offer"). The numbers tell the story before any review can: $12.35 average per sale means the front-end is a cheap ticket whose real business is the upsell path behind it — that's the standard bizopp architecture. The sales pitch follows the genre: automated income claims, screenshots, urgency. At gravity ~11 it's early days; what we can say with confidence is that no $12 product automates anyone's income, and that the genre's recurring pattern is a low-priced entry that leads to several-hundred-dollar back-end offers.""",
  verdict="If you understand you're buying a cheap intro course and can walk past the upsells, the refund window makes it low-risk. If the sales page made income feel guaranteed — that's the funnel working, not the business.",
  subs=[("quality","5.6"),("value","6.2"),("delivery","6.2"),("support","5.8")],
  for_you="MMO-curious buyers who want to see inside a modern bizopp funnel for the price of a pizza and will refuse every upsell.",
  skip="Anyone investing money they need back, and anyone treating income claims as expectations. New launch + low ticket + big promises = proceed with both eyes open.",
  pros=["Cheap front-end (~$12 average sale)",
        "ClickBank's 60-day refund policy applies",
        "Decent entry glimpse into how digital-offer funnels are built"],
  cons=["'Automated income' framing is the genre's oldest hook — no $12 product delivers it",
        "Real monetization is the upsell path, expect high-pressure back-end offers",
        "Brand new offer: no track record, no verified income proof",
        "Low average sale signals the value is in the funnel, not the product"],
  price_rows=[("Price", "Low-ticket one-time — ClickBank reports $12.35 average per sale (upsells behind it)"),
              ("Format", "Digital members area"),
              ("Guarantee", "60-day ClickBank refund policy — check terms at checkout")],
  faqs=[("What is Go Digital Income?",
         "A new make-money-online / bizopp offer on ClickBank selling a digital course around 'digital income' methods, with a low-ticket front-end and an upsell path behind it."),
        ("Is Go Digital Income a scam?",
         "It's a legally sold ClickBank product with refunds available. Our caution is genre-level: low-ticket MMO offers monetize through upsells, and income is never automated. Treat every claim as marketing."),
        ("How much does it really cost?",
         "The front end averages $12.35 per sale on ClickBank, but budget for the upsell path — that's where these funnels make their money."),
        ("Can you actually make money with it?",
         "Not from the product alone. Any real result comes from work the course won't do for you — and the honest baseline for this genre is most buyers make nothing.")],
  related=[("The Genius Switch", "genius-switch-review", "6.8"), ("The Last Wish", "the-last-wish-review", "6.9"), ("Wealth DNA Code", "wealth-dna-code-review", "7.4")],
  cat_price="Low-ticket ~$12 + upsells"),
 "aiagency": dict(
  slug="instant-ai-agency-review", name="The Instant AI Agency", score="6.5", ring="65.0",
  badge_cls="b-amber", badge_txt="Mixed — read the cons", cat="abundance",
  title="Instant AI Agency Review 2026: TrustScore 6.5/10",
  desc="Honest Instant AI Agency review: TrustScore 6.5/10 — the AI-agency-in-a-box course, price, pros, cons and who should skip it. Updated October 15, 2026.",
  vendor="DWARDROPE", tid="tsbaiagency", fallback="https://try.flexxable.io/",
  price_note="~$32 average per sale (ClickBank marketplace data)",
  lead="An 'AI agency in a box' course — the model is real, the 'instant' is doing heavy lifting.",
  what="""The Instant AI Agency (from the Flexxable ecosystem) is a course teaching the 2024–2026 business-model-of-the-moment: package AI tools and services, sell them to local/small businesses as an agency, and arbitrage the delivery. The pitch: skip years of agency-building with templates, workflows and client-acquisition scripts. To be fair to it, the underlying model is legitimate — AI-service agencies do exist and some make money. The caveats are equally real: the space is crowded with other course-buyers, clients are getting more AI-literate by the month, and 'instant' in the title refers to the setup, not the income. ClickBank shows $32.32 average per sale and gravity ~7 — modest traction compared to the manifestation blockbusters, which at least suggests it isn't riding pure hype.""",
  verdict="A legitimate business model taught at hype-adjacent framing. Worth it if you'll actually do client outreach; a disappointment if 'instant' was the part you believed.",
  subs=[("quality","6.6"),("value","6.2"),("delivery","6.6"),("support","6.0")],
  for_you="Action-takers who want a structured playbook for offering AI services to small businesses and will treat client acquisition as their full-time job.",
  skip="Anyone buying the word 'instant'. Agency models need sales skills and months of grind — the course provides materials, not clients.",
  pros=["The underlying business model (AI service arbitrage) is real and current",
        "Templates and workflows genuinely save setup time",
        "Modest marketplace traction — not a pure hype play",
        "ClickBank's 60-day refund policy"],
  cons=["'Instant' refers to setup, never to income — client acquisition is the hard part",
        "The niche is filling with other course graduates selling the same services",
        "No clients included: you leave with materials, not a business",
        "Income screenshots in this genre reflect the seller, not the student median"],
  price_rows=[("Price", "One-time course purchase — ClickBank reports $32.32 average per sale (tiered offers behind it)"),
              ("Format", "Digital course — instant access"),
              ("Guarantee", "60-day ClickBank refund policy — check terms at checkout")],
  faqs=[("What is The Instant AI Agency?",
         "A course from the Flexxable team teaching you to launch an agency selling AI-powered services to small businesses — templates, workflows and client-acquisition scripts included."),
        ("Can you really make money with an AI agency?",
         "The model is real: businesses pay for AI services. But it requires sales skills and sustained outreach — the course gives you materials, not clients, and the space is getting crowded."),
        ("How much does The Instant AI Agency cost?",
         "ClickBank data shows a $32.32 average per sale, with additional tiers offered behind the front-end."),
        ("Is it suitable for beginners?",
         "The materials are beginner-friendly, but agency work means selling to real businesses. If outreach and client management scare you, no course fixes that.")],
  related=[("Go Digital Income", "go-digital-income-review", "6.0"), ("The Genius Switch", "genius-switch-review", "6.8"), ("Leadpages", "leadpages-review", "8.2")],
  cat_price="Course ~$32 avg sale"),
}

def build(p):
    t = open(f"{ROOT}/reviews/woodpecker-review/index.html", encoding="utf-8").read()
    link = hop(p["vendor"], p["tid"])
    cta_top = f'Try {p["name"]} — official site →'
    cta_bot = f'See {p["name"]} — official site →'
    t = re.sub(r"<title>[^<]*</title>", f'<title>{p["title"]}</title>', t)
    t = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{p["desc"]}"', t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+p["title"]+m.group(2), t)
    t = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1)+p["title"]+m.group(2), t)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+p["desc"]+m.group(2), t)
    t = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1)+p["desc"]+m.group(2), t)
    t = t.replace("Woodpecker Review 2026: Honest TrustScore 7.7/10 (Pros &amp; Cons)", p["title"])
    t = t.replace('href="https://trustscore.bond/reviews/woodpecker-review/"', f'href="https://trustscore.bond/reviews/{p["slug"]}/"')
    t = t.replace("woodpecker-review", p["slug"])
    t = t.replace("Honest Woodpecker review: TrustScore 7.7/10 — what you get, pricing, pros, cons and who should skip it. Updated October 3, 2026.", p["desc"])
    t = t.replace("Updated October 3, 2026", f"Updated {TODAY}")
    t = t.replace('"datePublished": "2026-10-03"', f'"datePublished": "{DATE}"')
    t = t.replace("<h1>Woodpecker Review: TrustScore 7.7/10</h1>", f'<h1>{p["name"]} Review: TrustScore {p["score"]}/10</h1>')
    t = t.replace("<h1>Audiorista Review: TrustScore 7.0/10</h1>", f'<h1>{p["name"]} Review: TrustScore {p["score"]}/10</h1>')
    t = re.sub(r'<p class="lead">[^<]*</p>', f'<p class="lead">{p["lead"]}</p>', t)
    t = t.replace("<span>Woodpecker</span>", f'<span>{p["name"]}</span>')
    t = re.sub(r'<section class="hero">.*?</section>', '', t, flags=re.S)
    hero = f'''<section class="hero">
  <div>
    <p>{p["what"].split(". ")[0]}. {p["what"].split(". ")[1]}.</p>
    <div class="verdict"><b>The verdict:</b> {p["verdict"]}</div>
    <a class="cta" data-vendor="{p["vendor"].lower()}" data-link="{link}" href="{link}" rel="sponsored nofollow noopener" target="_blank">{cta_top}</a>
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
    t = re.sub(r'<h2>What you actually get</h2>\n<p>.*?</p>', f'<h2>What you actually get</h2>\n<p>{p["what"]}</p>', t, flags=re.S)
    t = re.sub(r'<div class="pros"><h3>✔ Made for you if…</h3><p>.*?</p></div>\s*<div class="cons"><h3>✘ Skip it if…</h3><p>.*?</p></div>',
               f'<div class="pros"><h3>✔ Made for you if…</h3><p>{p["for_you"]}</p></div>\n  <div class="cons"><h3>✘ Skip it if…</h3><p>{p["skip"]}</p></div>', t, flags=re.S)
    t = re.sub(r'<div class="pros"><h3>What we liked</h3><ul>.*?</ul></div>',
               '<div class="pros"><h3>What we liked</h3><ul>' + ''.join(f'<li>{x}</li>' for x in p["pros"]) + '</ul></div>', t, flags=re.S)
    t = re.sub(r'<div class="cons"><h3>What could be better</h3><ul>.*?</ul></div>',
               '<div class="cons"><h3>What could be better</h3><ul>' + ''.join(f'<li>{x}</li>' for x in p["cons"]) + '</ul></div>', t, flags=re.S)
    t = re.sub(r'<div class="tablewrap"><table>.*?</table></div>',
               '<div class="tablewrap"><table>\n<tr><th>Item</th><th>Details</th></tr>\n' + ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k,v in p["price_rows"]) + '\n</table></div>', t, flags=re.S)
    # CTAs: replace all woodpecker CTAs with ours
    t = t.replace('Try Woodpecker — official site →', cta_top).replace('See Woodpecker — official site →', cta_bot)
    t = re.sub(r'<a class="cta"[^>]*href="https://woodpecker\.co/\?red=hhgg"[^>]*>',
               f'<a class="cta" data-vendor="{p["vendor"].lower()}" data-link="{link}" href="{link}" rel="sponsored nofollow noopener" target="_blank">', t)
    # also the second woodpecker link inside pricing table
    t = t.replace('<a href="https://woodpecker.co/?red=hhgg" rel="sponsored nofollow noopener" target="_blank">check the official site for current pricing</a>',
                  f'<a href="{link}" rel="sponsored nofollow noopener" target="_blank">check the official site for current pricing</a>')
    t = re.sub(r'<p class="note">See it side-by-side[^<]*</p>', '', t)
    faq_html = '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in p["faqs"]) + '</div>'
    t = re.sub(r'<div class="faq">.*?</div>', faq_html, t, flags=re.S)
    faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faqs"]]}, ensure_ascii=False)
    t = re.sub(r'(<script type="application/ld\+json">)\{"@context": "https://schema.org", "@type": "FAQPage".*?\}(</script>)', lambda m: m.group(1)+faq_ld+m.group(2), t, flags=re.S)
    sw = {"@context":"https://schema.org","@type":"Product","name":p["name"],
          "description":p["lead"]+" "+p["verdict"],
          "image":f"https://trustscore.bond/og/{p['slug']}.png",
          "review":{"@type":"Review","reviewRating":{"@type":"Rating","ratingValue":p["score"],"bestRating":"10","worstRating":"1"},
                    "author":{"@type":"Person","name":"Hamdi Arij","jobTitle":"Pro Reviewer","url":"https://trustscore.bond/how-we-review/#author"},
                    "datePublished":DATE},
          "offers":{"@type":"Offer","price":p["price_rows"][0][1].split("$")[1].split(" ")[0] if "$" in p["price_rows"][0][1] else "0","priceCurrency":"USD","availability":"https://schema.org/InStock","url":f"https://trustscore.bond/reviews/{p['slug']}/"}}
    t = re.sub(r'(<script type="application/ld\+json">)\{"@context": "https://schema.org", "@type": "SoftwareApplication".*?\}(</script>)', lambda m: m.group(1)+json.dumps(sw,ensure_ascii=False)+m.group(2), t, flags=re.S)
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://trustscore.bond/"},
        {"@type":"ListItem","position":2,"name":"Reviews","item":"https://trustscore.bond/reviews/"},
        {"@type":"ListItem","position":3,"name":p["name"],"item":f"https://trustscore.bond/reviews/{p['slug']}/"}]}
    t = re.sub(r'(<script type="application/ld\+json">)\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?\}(</script>)', lambda m: m.group(1)+json.dumps(bc,ensure_ascii=False)+m.group(2), t, flags=re.S)
    # related cards (new pages or existing dirs, real price when available)
    NEWMAP = {"genius-switch-review":"genius","the-last-wish-review":"lastwish","astrology-language-review":"astrolang",
              "rapid-soup-diet-review":"soup","go-digital-income-review":"gdi","instant-ai-agency-review":"aiagency"}
    def existing_price(slug):
        for catf in G.glob(f"{ROOT}/category/*/index.html"):
            cs = open(catf, encoding="utf-8").read()
            m = re.search(r'<a class="card" href="/reviews/'+slug+r'/"><span class="cat">[^<]*</span><b>[^<]*</b><span class="score">[^<]*</span><span class="price">([^<]*)</span>', cs)
            if m: return m.group(1)
        return "Digital program"
    cards = ""
    for (n, s, sc) in p["related"]:
        key = NEWMAP.get(s)
        if key:
            price = P[key]["cat_price"]
        elif os.path.isdir(f"{ROOT}/reviews/{s}"):
            price = existing_price(s)
        else:
            continue
        cards += f'<a class="card" href="/reviews/{s}/"><span class="cat">{CATS[p["cat"]]}</span><b>{n}</b><span class="score">TrustScore {sc}/10</span><span class="price">{HH.escape(price)}</span></a>'
    if not cards:
        cards = f'<a class="card" href="/reviews/genius-switch-review/"><span class="cat">{CATS[p["cat"]]}</span><b>The Genius Switch</b><span class="score">TrustScore 6.8/10</span><span class="price">One-time · ~$45 avg sale</span></a>'

    t = re.sub(r'<section class="cards">.*?</section>', f'<section class="cards">{cards}</section>', t, flags=re.S)
    t = t.replace('alt="Woodpecker TrustScore card — 7.7 out of 10"', f'alt="{p["name"]} TrustScore card — {p["score"]} out of 10"')
    t = t.replace("Try Woodpecker", f'Try {p["name"]}').replace("See Woodpecker", f'See {p["name"]}')
    # clean woodpecker words left in text (should be none)
    leftovers = re.findall(r'[Ww]oodpecker', t)
    os.makedirs(f"{ROOT}/reviews/{p['slug']}", exist_ok=True)
    open(f"{ROOT}/reviews/{p['slug']}/index.html", "w", encoding="utf-8").write(t)
    return len(leftovers)

for slug, p in P.items():
    n = build(p)
    print(f"✓ reviews/{p['slug']}/  (woodpecker leftovers: {n})")

# ---------- OG images ----------
from PIL import Image, ImageDraw, ImageFont
def og(p):
    W,H = 1200,630
    img = Image.new("RGB",(W,H),(16,26,51)); d = ImageDraw.Draw(img)
    for y in range(H): d.line([(0,y),(W,y)], fill=(16+y//22, 26+y//26, 51+min(30,y//14)))
    try:
        f_big=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",84)
        f_mid=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",150)
        f_sm=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",34)
        f_xs=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",26)
    except: f_big=f_mid=f_sm=f_xs=ImageFont.load_default()
    d.rounded_rectangle([60,60,190,190],28,fill=(240,180,41))
    d.text((125,125),"TS",font=f_big,fill=(16,26,51),anchor="mm")
    d.text((90,235),"TrustScore",font=f_big,fill=(255,255,255),anchor="lm")
    d.text((92,330),".bond — honest review",font=f_sm,fill=(170,182,214),anchor="lm")
    d.text((90,470),p["score"],font=f_mid,fill=(240,180,41),anchor="lm")
    d.text((95,600),f"/10 TrustScore · {p['name']}",font=f_xs,fill=(170,182,214),anchor="lm")
    d.text((1140,110),p["name"][:24],font=f_big,fill=(255,255,255),anchor="rm")
    d.text((1140,205),"ClickBank offer review",font=f_sm,fill=(170,182,214),anchor="rm")
    d.text((1140,600),"Updated "+TODAY,font=f_xs,fill=(170,182,214),anchor="rm")
    img.save(f"{ROOT}/og/{p['slug']}.png")
for p in P.values(): og(p)
print("✓ 6 og images")

# ---------- category + reviews index card insertion (per category) ----------
def card_html(p):
    return (f'<a class="card" href="/reviews/{p["slug"]}/"><span class="cat">{CATS_RAW[p["cat"]]}</span>'
            f'<b>{p["name"]}</b><span class="score">TrustScore {p["score"]}/10</span>'
            f'<span class="price">{HH.escape(p["cat_price"])}</span></a>')

def insert_inplace(page_path, cards_new):
    s = open(page_path, encoding="utf-8").read()
    for p in cards_new:
        if p["slug"] in s: continue
        cat_re = re.compile(r'<a class="card" href="/reviews/[a-z0-9-]+/"><span class="cat">' + re.escape(CATS_RAW[p["cat"]]) + r'</span>.*?</a>')
        cards = cat_re.findall(s)
        new = card_html(p)
        if cards:
            best = None
            for c in cards:
                sc = float(re.search(r'TrustScore ([\d.]+)/10', c).group(1))
                if sc < float(p["score"]): best = c; break
            if best is not None: s = s.replace(best, new + best, 1)
            else:
                last = cards[-1]; s = s.replace(last, last + new, 1)
        else:
            m = re.search(r'<section class="cards">', s)
            s = s[:m.end()] + new + s[m.end():]
        open(page_path, "w", encoding="utf-8").write(s)
        s = open(page_path, encoding="utf-8").read()

for cat in ["abundance","mind","health"]:
    items = [p for p in P.values() if p["cat"] == cat]
    insert_inplace(f"{ROOT}/category/{cat}/index.html", items)
    print(f"✓ category/{cat} +{len(items)}")
insert_inplace(f"{ROOT}/reviews/index.html", list(P.values()))
print("✓ reviews/index +6")

# ---------- cross-links on existing related reviews ----------
def add_related(target_slug, items):
    f = f"{ROOT}/reviews/{target_slug}/index.html"
    if not os.path.exists(f): return False
    s = open(f, encoding="utf-8").read()
    m = re.search(r'(<section class="cards">)(.*?)(</section>)', s, re.S)
    added = ''.join(card_html(p) for p in items if p["slug"] not in s)
    if not added: return False
    s = s[:m.end(2)] + added + s[m.end(2):]
    open(f, "w", encoding="utf-8").write(s)
    return True

for target, items in [
    ("wealth-dna-code-review", [P["genius"], P["lastwish"]]),
    ("soul-manifestation-review", [P["lastwish"]]),
    ("manifestation-magic-review", [P["genius"]]),
    ("astrology-tv-review", [P["astrolang"]]),
    ("numerologist-com-review", [P["astrolang"]]),
    ("smoothie-diet-review", [P["soup"]]),
    ("alpilean-review", [P["soup"]]),
]:
    print(f"✓ cross-link {target}: {add_related(target, items)}")

# ---------- sitemap ----------
sm = open(f"{ROOT}/sitemap.xml", encoding="utf-8").read()
m = re.search(r'<url>\s*<loc>https://trustscore.bond/reviews/woodpecker-review/</loc>.*?</url>', sm, re.S)
tpl = m.group(0)
for p in P.values():
    e = re.sub(r'<loc>[^<]*</loc>', f'<loc>https://trustscore.bond/reviews/{p["slug"]}/</loc>', tpl)
    e = re.sub(r'<lastmod>[^<]*</lastmod>', f'<lastmod>{DATE}</lastmod>', e)
    sm = sm.replace("</urlset>", e + "</urlset>")
open(f"{ROOT}/sitemap.xml", "w", encoding="utf-8").write(sm)
print(f"✓ sitemap: {sm.count('<loc>')} entries")
print("DONE")
