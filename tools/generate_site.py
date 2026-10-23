"""daysuntil.bond static site generator — one-time build, zero dependencies beyond stdlib+PIL.
Reads data/*.json, writes docs/ (GitHub Pages ready)."""
import os, json, math, random, hashlib, datetime as dt
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'docs')
SITE = 'https://daysuntil.bond'
BRAND = 'daysuntil.bond'
BUILD_DATE = dt.date(2026, 10, 2)
INDEXNOW_KEY = 'd91f4c7b2a8e6350f1c9d8a4b7e2f6c3'

CATS = {
 'holidays':       dict(name='Holidays & Observances', icon='🎉', c1=(194,24,91),  c2=(71,20,100),  blurb='Every major holiday and observance on the calendar — Christmas, Halloween, Easter, Thanksgiving, New Year and dozens more — each with a live countdown to the second.'),
 'moon':           dict(name='Moon Phases',            icon='🌕', c1=(96,125,139), c2=(25,42,64),   blurb='Every full moon and new moon through 2028, with exact peak times computed from lunar theory — plus the rare blue moons and black moons.'),
 'eclipses':       dict(name='Eclipses',               icon='🌘', c1=(230,81,0),   c2=(20,20,26),   blurb='Every solar and lunar eclipse from late 2026 through 2028 — including the eclipse of the century on August 2, 2027, whose shadow crosses Spain, North Africa and Egypt.'),
 'planets':        dict(name='Planetary Stations',     icon='🪐', c1=(81,45,168),  c2=(16,14,40),   blurb='Every retrograde and direct station of Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune and Pluto through 2028 — computed to the minute with our own Keplerian ephemeris.'),
 'meteor-showers': dict(name='Meteor Showers',         icon='☄️', c1=(0,105,92),   c2=(6,26,34),    blurb='All the major annual meteor showers — Perseids, Geminids, Quadrantids and more — with peak nights and viewing tips.'),
 'seasons':        dict(name='Solstices & Equinoxes',  icon='🍂', c1=(85,139,47),  c2=(28,42,51),   blurb='The exact moments spring, summer, fall and winter begin in 2026, 2027 and 2028 — down to the minute, UTC.'),
 'gaming':         dict(name='Games',                  icon='🎮', c1=(124,77,255), c2=(12,10,36),   blurb='The biggest game launches on the calendar — headlined by the most anticipated release in entertainment history.'),
 'movies':         dict(name='Movies',                 icon='🎬', c1=(183,28,28),  c2=(24,10,14),   blurb='Major theatrical release dates, from the Dunesday showdown of December 2026 to the far horizon of Pandora.'),
 'sports':         dict(name='Sports',                 icon='🏆', c1=(46,125,50),  c2=(10,25,41),   blurb='The dates that stop the sporting world — the Valentine\'s Day Super Bowl and the Los Angeles 2028 Olympic Games.'),
}

NETWORK = [
    ('Prophetic', 'https://prophetic.pw'),
    ('Twin Flame Bond', 'https://twinflame.bond'),
    ('BMR Calc', 'https://www.bmrcalc.bond'),
    ('Pro Reviewer', 'https://pro-reviewer.cyou'),
    ('Prophetic Guidance', 'https://propheticguidance2026.blogspot.com'),
    ('TrustScore', 'https://trustscore.bond'),
]

# ---------------------------------------------------------------- load & merge
events = []
for f in ('astro_events.json', 'fixed_events.json'):
    events += json.load(open(os.path.join(DATA, f)))

def target_ms(e):
    if e['kind'] == 'datetime':
        y, mo, rest = e['utc'].split('-')
        d, hms = rest.split('T')
        h, mi, _ = hms.split(':')
        return dt.datetime(int(y), int(mo), int(d), int(h), int(mi), tzinfo=dt.timezone.utc).timestamp() * 1000
    y, mo, d = map(int, e['date'].split('-'))
    return dt.datetime(y, mo, d, tzinfo=dt.timezone.utc).timestamp() * 1000

for e in events:
    e['ms'] = target_ms(e)
    e['dt'] = dt.datetime.fromtimestamp(e['ms'] / 1000, dt.timezone.utc)
events.sort(key=lambda e: e['ms'])
assert len({e['slug'] for e in events}) == len(events), 'duplicate slugs!'
print(f'{len(events)} events loaded')

# ---------------------------------------------------------------- deep content
# Thin-content fix: long-form, genuinely specific sections for the pages that
# matter, kept in data/deep_content.json so hand-written copy survives a rebuild.
_deep_path = os.path.join(DATA, 'deep_content.json')
DEEP = json.load(open(_deep_path)) if os.path.exists(_deep_path) else {}
if DEEP:
    print(f'{len(DEEP)} deep-content page(s) loaded')

# ------------------------------------------------- duplicate consolidation rule
# Events that repeat by year (christmas-day-2026/2027/2028, full-moon-may-2027/2028…)
# produce near-identical pages that compete with each other. Only the NEXT
# occurrence is indexable; the rest stay live but carry noindex + canonical to
# the next one, and are dropped from the sitemap.
import re as _re
PRIORITY_SLUGS = {
    'avengers-doomsday', 'dune-part-three', 'black-friday-2026', 'halloween-2026',
    'gta-6-release', '1111-portal-2026', 'christmas-day-2026', 'cyber-monday-2026',
    'us-thanksgiving-2026', 'new-year-2027', 'ramadan-2027',
}
def _base(slug):
    return _re.sub(r'-(\d{4})$', '', slug)

_today = dt.datetime.now(dt.timezone.utc)
_groups = {}
for _e in events:
    _groups.setdefault(_base(_e['slug']), []).append(_e)
NEXT_OF = {}
for _b, _items in _groups.items():
    _future = sorted([x for x in _items if x['dt'] >= _today], key=lambda x: x['dt'])
    _pick = _future[0] if _future else max(_items, key=lambda x: x['dt'])
    NEXT_OF[_b] = _pick['slug']
INDEXABLE = set(NEXT_OF.values()) | PRIORITY_SLUGS

def date_nice(d, with_year=True):
    s = d.strftime('%A, %B ') + str(d.day)
    return s + f', {d.year}' if with_year else s

def esc(s):
    s = str(s)
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# ---------------------------------------------------------------- OG image maker
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_R = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def og_image(path, title, chip, cat_key, salt=''):
    W, H = 1200, 630
    c1, c2 = CATS[cat_key]['c1'], CATS[cat_key]['c2']
    img = Image.new('RGB', (W, H))
    dr = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        dr.line([(0, y), (W, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    rnd = random.Random(hashlib.md5((salt + title).encode()).hexdigest())
    for _ in range(140):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        r = rnd.choice([1, 1, 1, 2, 3])
        b = rnd.randint(120, 255)
        dr.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 20)))
    icon = CATS[cat_key]['icon']
    dr.text((70, 66), icon + '  ' + CATS[cat_key]['name'].upper(), font=ImageFont.truetype(FONT_R, 30), fill=(235, 235, 245))
    fb = ImageFont.truetype(FONT_B, 74)
    words, lines, cur = title.split(), [], ''
    for w in words:
        t2 = (cur + ' ' + w).strip()
        if fb.getbbox(t2)[2] > 1010 and cur:
            lines.append(cur); cur = w
        else:
            cur = t2
    lines.append(cur)
    if len(lines) > 3:
        lines = lines[:3]; lines[2] = lines[2][:24].rsplit(' ', 1)[0] + '…'
    y = 200
    for ln in lines:
        dr.text((70, y), ln, font=fb, fill=(255, 255, 255))
        y += 96
    fr = ImageFont.truetype(FONT_B, 40)
    tw = fr.getbbox(chip)[2]
    dr.rounded_rectangle([70, y + 26, 70 + tw + 56, y + 104], radius=18, fill=(255, 255, 255))
    dr.text((98, y + 36), chip, font=fr, fill=(18, 18, 28))
    fs = ImageFont.truetype(FONT_R, 30)
    dr.text((70, H - 74), BRAND + '  ·  live countdowns to the events the world is waiting for', font=fs, fill=(215, 215, 230))
    img.save(path, 'PNG', optimize=True)

# ---------------------------------------------------------------- shared HTML chunks
GA_ID = 'G-1W7PC1JDKH'  # same GA4 account as prophetic.pw
GA_TAGS = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '"></script>\n'
           '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}'
           "gtag('js',new Date());gtag('config','" + GA_ID + "');</script>")

# ---------------------------------------------------------------- ads (AdSense-only: daysuntil under Google review — no third-party ad code)
NATIVE_AD = ''
AD_LB = ''
AD_MREC = ''
AD_LOADER = ''


CSS = open(os.path.join(ROOT, 'tools', 'site.css')).read()
JS = open(os.path.join(ROOT, 'tools', 'site.js')).read()

def head(title, desc, canonical, ogimg, ld_extra='', path_prefix='..', indexable=True):
    robots = 'index,follow,max-snippet:-1,max-image-preview:large' if indexable else 'noindex,follow'
    return f'''<!doctype html>
<html lang="en">
<head><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3898992716389443" crossorigin="anonymous"></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}{ogimg}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@daysuntilbond">
<meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}{ogimg}">
<link rel="icon" href="{path_prefix}/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{path_prefix}/assets/style.css">
{GA_TAGS}
{ld_extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <a class="logo" href="{path_prefix}/"><span class="logo-dot"></span> daysuntil<b>.bond</b></a>
  <nav class="nav">'''

def nav_links(pp):
    return ''.join(f'<a href="{pp}/{c}/">{CATS[c]["icon"]} {CATS[c]["name"].split(" &")[0].split(" (")[0]}</a>' for c in
                   ('holidays', 'eclipses', 'moon', 'planets', 'gaming', 'movies')) + f'<a href="{pp}/about/">ℹ️ About</a>'

def footer(pp='..'):
    net = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in NETWORK)
    cats = ''.join(f'<a href="{pp}/{c}/">{CATS[c]["icon"]} {CATS[c]["name"]}</a>' for c in CATS)
    return f'''</main>
<footer class="foot">
  <div class="foot-grid">
    <div><div class="logo small"><span class="logo-dot"></span> daysuntil<b>.bond</b></div>
      <p>Live countdowns to the dates the world is waiting for — holidays, eclipses, moon phases, planetary stations, game launches, movies and sport. Astronomy events are computed with our own Keplerian ephemeris; verified dates are checked against primary sources.</p></div>
    <div><b>Categories</b>{cats}</div>
    <div><b>Our network</b>{net}</div>
    <div><b>Site</b><a href="{pp}/about/">About</a><a href="{pp}/privacy/">Privacy policy</a><a href="{pp}/disclosure/">Advertising &amp; affiliate disclosure</a></div>
  </div>
  <p class="tiny">© 2026 {BRAND}. Countdowns run in your local time zone. Dates marked "expected" depend on moon sighting and may shift by a day.</p>
</footer>
</body></html>'''

def breadcrumb_ld(trail):
    items = ','.join(f'{{"@type":"ListItem","position":{i+1},"name":"{esc(n)}","item":"{u}"}}' for i, (n, u) in enumerate(trail))
    return '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[' + items + ']}'

# ─────────────────────────────────────────────────────────────────────────────
# Title / description fitting (SEO hygiene).
# Google truncates titles around 60 chars and descriptions around 155-160.
# These helpers guarantee both stay in range no matter how long the event name is,
# while keeping the money phrase ("How Many Days Until X?") whenever it fits.
# ─────────────────────────────────────────────────────────────────────────────
TITLE_MAX = 60
DESC_MAX = 155

def _trim_words(s, limit):
    s = s.strip()
    if len(s) <= limit: return s
    cut = s[:limit].rstrip()
    i = cut.rfind(' ')
    if i >= int(limit * 0.55): cut = cut[:i]
    return cut.rstrip(' ,;:—–-')

def fit_title(ev, dd):
    base = ev['title']
    if dd == 0:
        cands = [f"How Many Days Until {base}? It's Today",
                 f"{base}: It's Today", f"Days Until {base}"]
    elif dd > 0:
        cands = [f"How Many Days Until {base}? {dd} Days Left",
                 f"How Many Days Until {base}?",
                 f"Days Until {base} — {dd} Days",
                 f"Days Until {base}"]
    else:
        cands = [f"How Many Days Until {base}? Live Countdown",
                 f"How Many Days Until {base}?",
                 f"Days Until {base}"]
    for c in cands:
        if len(c) <= TITLE_MAX: return c
    return _trim_words(cands[-1], TITLE_MAX)

def fit_desc(ev, d, dd):
    nice = date_nice(d)
    if dd > 0:
        cands = [
            f"Live countdown to {ev['title']} on {nice} — {dd} days to go, with weeks, weekdays and hours remaining.",
            f"{dd} days to {ev['title']}, on {nice}. Live countdown in days, hours, minutes and seconds.",
            f"{dd} days until {ev['title']} ({nice}). Live countdown, updated every second.",
            f"{dd} days until {ev['title']} on {nice}. Live countdown, updated every second.",
        ]
    elif dd == 0:
        cands = [
            f"{ev['title']} is today, {nice}. Live countdown with the hours, minutes and seconds remaining.",
            f"{ev['title']} is today ({nice}). Live countdown in hours, minutes and seconds.",
            f"{ev['title']} is today. Live countdown.",
        ]
    else:
        cands = [
            f"{ev['title']} fell on {nice}. See the exact date, the weekday, and how long ago it was.",
            f"{ev['title']} was on {nice}. Exact date, weekday and time since.",
            f"{ev['title']} was on {nice} — a {d.strftime('%A')}. Exact date and weekday.",
        ]
    for c in cands:
        if len(c) <= DESC_MAX: return c
    return _trim_words(cands[-1], DESC_MAX)

def event_page(e):
    slug, cat = e['slug'], e['category']
    d = e['dt']
    today = dt.date.today()
    dd = (d.date() - today).days
    # Title/description are fitted to Google's display limits — the live number
    # still goes in the title for close events (the pattern every top-ranking
    # countdown competitor uses), but only when it fits inside 60 characters.
    title_tag = fit_title(e, dd)
    desc = fit_desc(e, d, dd)
    if dd >= 0:
        wk, rd = divmod(dd, 7)
        wdays = sum(1 for i in range(1, dd + 1) if (today + dt.timedelta(days=i)).weekday() < 5)
        glance = (f'As of {today.strftime("%B")} {today.day}, {today.year}: <b>{dd} days</b> to go — '
                  f'{wk} weeks and {rd} days, {wdays} weekdays ({dd - wdays} weekend days), about {dd * 24:,} hours.')
        glance_html = f'<p class="cd-status">{glance}</p>'
    else:
        glance_html = ''
    faq = e.get('faq') or [
        (f'How many days until {e["title"]}?', f'{e["title"]} falls on {date_nice(d)}. The live countdown at the top of this page shows the exact days, hours and minutes remaining from this very moment, in your time zone.'),
        (f'What date is {e["title"]}?', f'{e["title"]} is on {date_nice(d)} — a {d.strftime("%A")}.'),
        (f'How many weeks until {e["title"]}?', 'The counter on this page converts the remaining time to weeks, days, hours and seconds automatically, so the answer is always current no matter when you visit.'),
    ]
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage',
                     'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
    ld_crumb = breadcrumb_ld([('Home', SITE + '/'), (CATS[cat]['name'], f'{SITE}/{cat}/'), (e['title'], f'{SITE}/{slug}/')])
    ld_block = ('<script type="application/ld+json">' + ld + '</script>\n'
                '<script type="application/ld+json">' + ld_crumb + '</script>')

    cfg = json.dumps({'kind': e['kind'], 'y': d.year, 'm': d.month, 'd': d.day,
                      'utc': e.get('utc'), 'title': e['title'], 'dateNice': date_nice(d)})

    facts = ''.join(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in e['facts'])
    paras = ''.join(f'<p>{p}</p>' for p in e['desc'])
    deep = DEEP.get(slug) or {}
    deep_html = ''
    for sec in deep.get('sections') or []:
        deep_html += f'<h2>{esc(sec.get("h2", ""))}</h2>'
        for para in sec.get('p') or []:
            deep_html += f'<p>{para}</p>'
        tbl = sec.get('table')
        if tbl:
            head_row = ''.join(f'<th>{esc(c)}</th>' for c in tbl['head'])
            body_rows = ''.join('<tr>' + ''.join(f'<td>{esc(c)}</td>' for c in r) + '</tr>' for r in tbl['rows'])
            deep_html += f'<div class="tablewrap"><table class="facts"><tr>{head_row}</tr>{body_rows}</table></div>'
    if deep.get('faq'):
        faq = faq + [(q, a) for q, a in deep['faq']]
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)

    related = related_events(e)
    rel = ''.join(f'''<a class="card" href="../{r['slug']}/"><span class="card-cat">{CATS[r['category']]['icon']} {CATS[r['category']]['name']}</span>
      <b>{esc(r['title'])}</b><span class="card-date">{date_nice(r['dt'])}</span><span class="card-days" data-ms="{r['ms']}"></span></a>''' for r in related)

    indexable = slug in INDEXABLE
    canonical = f'{SITE}/{slug}/' if indexable else f'{SITE}/{NEXT_OF.get(_base(slug), slug)}/'
    return head(title_tag, desc, canonical, f'/og/{slug}.png', ld_block, '..', indexable) + nav_links('..') + f'''</nav>
</header>
<main id="main">
<nav class="crumbs"><a href="../">Home</a> › <a href="../{cat}/">{CATS[cat]['name']}</a> › <span>{esc(e['title'])}</span></nav>
<h1>How Many Days Until {esc(e['title'])}?</h1>
<section class="hero" data-cat="{cat}">
  <div class="cd">
    <div class="cd-days"><span id="cd-d">–</span><small>days</small></div>
    <div class="cd-grid">
      <div><b id="cd-h">–</b><small>hours</small></div>
      <div><b id="cd-m">–</b><small>minutes</small></div>
      <div><b id="cd-s">–</b><small>seconds</small></div>
    </div>
    <p class="cd-status" id="cd-status">{esc(e['title'])} falls on {date_nice(d)}.</p>
    {glance_html}
  </div>
  <div class="chips">
    <span class="chip">📅 <b id="ch-weeks">–</b> weeks</span>
    <span class="chip">💼 <b id="ch-wd">–</b> weekdays</span>
    <span class="chip">🛌 <b id="ch-we">–</b> weekend days</span>
    <span class="chip">🗓️ <b id="ch-months">–</b> months (approx)</span>
  </div>
</section>
{AD_LB}<figure class="hero-img"><img src="../og/{slug}.png" alt="{esc(e['title'])} — countdown card" loading="lazy" width="1200" height="630"></figure>
{NATIVE_AD}
<section class="grid2">
  <div>
    <h2>Quick facts</h2>
    <table class="facts">{facts}</table>
    <h2>About {esc(e["title"])}</h2>
    {paras}
    {deep_html}
    {AD_MREC}  </div>
  <aside>
    <h2>Share this countdown</h2>
    <div class="share">
      <button id="sh-tw">Share on X</button><button id="sh-fb">Facebook</button><button id="sh-wa">WhatsApp</button><button id="sh-cp">Copy link</button>
    </div>
    <h2>FAQ</h2>
    <div class="faq">{faq_html}</div>
  </aside>
</section>
<h2>Related countdowns</h2>
<section class="cards">{rel}</section>
{AD_LOADER}</main>
<script>window.EVENT={cfg};</script>
<script src="../assets/site.js" defer></script>
''' + footer()

_related_cache = {}
def related_events(e, n=6):
    scored = sorted((x for x in events if x['slug'] != e['slug']),
                    key=lambda x: (0 if x['category'] == e['category'] else 1, abs(x['ms'] - e['ms'])))
    return scored[:n]

def card_html(e, pp=''):
    return f'''<a class="card" href="{pp}{e['slug']}/"><span class="card-cat">{CATS[e['category']]['icon']} {CATS[e['category']]['name']}</span>
      <b>{esc(e['title'])}</b><span class="card-date">{date_nice(e['dt'])}</span><span class="card-days" data-ms="{e['ms']}"></span></a>'''

def category_page(cat):
    c = CATS[cat]
    evs = [e for e in events if e['category'] == cat]
    cards = ''.join(card_html(e, '../') for e in evs)
    ld = breadcrumb_ld([('Home', SITE + '/'), (c['name'], f'{SITE}/{cat}/')])
    t = _trim_words(f'{c["name"]} — Live Countdowns ({len(evs)} events)', TITLE_MAX)
    desc = _trim_words(f'Live countdowns to {len(evs)} {c["name"].lower()} — days, hours, minutes and seconds, updated every second in your time zone.', DESC_MAX)
    return head(t, desc, f'{SITE}/{cat}/', f'/og/cat-{cat}.png', '<script type="application/ld+json">' + ld + '</script>') + nav_links('..') + f'''</nav>
</header>
<main id="main">
<nav class="crumbs"><a href="../">Home</a> › <span>{c['name']}</span></nav>
<h1>{c['icon']} {c['name']}</h1>
<p class="lead">{c['blurb']}</p>
{AD_LB}<section class="cards">{cards}</section>
{NATIVE_AD}{AD_LOADER}</main>
''' + footer()

def home_page():
    TRENDING = ['avengers-doomsday', 'halloween-2026', 'new-year-2027', 'gta-6-release', 'black-friday-2026', '1111-portal-2026']
    by_slug = {e['slug']: e for e in events}
    trend = ''.join(card_html(by_slug[s]) for s in TRENDING if s in by_slug and by_slug[s]['ms'] > dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
    upcoming = [e for e in events if e['ms'] > dt.datetime.now(dt.timezone.utc).timestamp() * 1000][:12]
    cards = ''.join(card_html(e) for e in upcoming)
    cats = ''.join(f'''<a class="cat-tile" href="{c}/" style="--c1:rgb{CATS[c]['c1']}"><span class="big">{CATS[c]['icon']}</span><b>{CATS[c]['name']}</b><span class="count">{sum(1 for e in events if e["category"]==c)} countdowns</span></a>''' for c in CATS)
    idx = json.dumps([{'s': e['slug'], 't': e['title'], 'c': e['category'], 'n': date_nice(e['dt']), 'm': e['ms']} for e in events])
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'WebSite', 'name': BRAND, 'url': SITE,
                     'description': 'Live countdowns to holidays, eclipses, moon phases, planetary stations, game launches, movies and sporting events.',
                     'potentialAction': {'@type': 'SearchAction', 'target': {'@type': 'EntryPoint', 'urlTemplate': SITE + '/?q={search_term_string}'}, 'query-input': 'required name=search_term_string'}})
    return head(_trim_words(f'{BRAND} — Live Countdowns to Every Event', TITLE_MAX),
                _trim_words('How many days until Christmas, GTA 6, the next solar eclipse or the next full moon? Live countdowns in days, hours, minutes and seconds to {n} verified dates.'.replace('{n}', str(len(events))), DESC_MAX),
                SITE + '/', '/og/home.png', '<script type="application/ld+json">' + ld + '</script>', '') + f'''<a href="about/">About</a>
</nav>
</header>
<main id="main">
<section class="home-hero">
  <h1>How many days until…?</h1>
  <p class="lead">{len(events)} live countdowns — every tick computed in your time zone, from Christmas and GTA 6 to the eclipse of the century.</p>
  <div class="searchbox"><input id="q" type="search" placeholder="Search an event — try “eclipse”, “Christmas”, “GTA”, “full moon”…" autocomplete="off"><div id="q-results" class="q-results" hidden></div></div>
</section>
<section class="grid2">
  <div>
    <h2>How our countdowns work</h2>
    <p>Every timer on this site runs <b>in your browser, on your device's clock</b>. That sounds like a technical detail, and it is the whole point: a countdown calculated on a server in one country is a day out for anyone whose calendar date differs at that instant, which is why so many countdown sites disagree with each other — and with your phone.</p>
    <p>Each page shows the exact days, hours, minutes and seconds remaining, plus weeks, weekdays, weekend days and an approximate month count. For events with a precise moment — an eclipse, a solstice, a full moon — we also give the UTC time, because "June 21" is not an answer when the event happens at 08:25 UTC and your neighbour is eight hours behind.</p>
    <h2>Why our number can differ from another site's</h2>
    <p>Two reasons, and neither site is broken. The first is the <b>counting convention</b>: some tools count today as day one, so their answer is always one higher than ours. We count whole days remaining — <b>1 means tomorrow, 0 means today</b> — which is what most people mean when they ask. The second is the <b>time zone</b>, and ours always matches yours.</p>
  </div>
  <aside>
    <h2>What's on the calendar</h2>
    <p><b>267 dates</b> across nine categories. Holidays and observances through 2028; every full and new moon with its peak time; every solar and lunar eclipse from late 2026 through 2028 — including the eclipse of the century on August 2, 2027; every retrograde and direct station of all eight planets; the major annual meteor showers; solstices and equinoxes to the minute; and the big game launches, film releases and sporting dates.</p>
    <p>The astronomy is computed with our own Keplerian ephemeris rather than copied from another site, which is why our times occasionally differ from theirs by a few minutes. Where a date depends on observation rather than calculation — a moon sighting, an announced release date — the page says so explicitly instead of presenting an estimate as fact.</p>
    <p><a class="cta" href="about/">How we compute the dates →</a></p>
  </aside>
</section>
<h2>🔥 Trending countdowns</h2>
<section class="cards">{trend}</section>
<h2>⏳ Counting down right now</h2>
<section class="cards">{cards}</section>
{AD_LB}<h2>🗂 Browse by category</h2>
<section class="cat-grid">{cats}</section>
{AD_LOADER}</main>
<script>window.EVENTS={idx};</script>
<script src="assets/site.js" defer></script>
''' + footer('')

INFO = {
 'about': ('About daysuntil.bond', f'''<h1>About {BRAND}</h1>
<p>{BRAND} is a library of live countdowns to the dates the world is actually waiting for — {len(events)} of them at launch and growing: holidays and observances, eclipses, full and new moons, planetary stations, meteor showers, solstices and equinoxes, and the biggest confirmed dates in gaming, movies and sport.</p>
<h2>How the dates are computed</h2>
<p>Astronomical events — moon phases, solstices, equinoxes and every planetary station — are computed to the minute with our own Keplerian ephemeris (JPL/Standish approximate elements, 1800–2050, tropical zodiac), cross-validated against published ephemerides. Holiday dates that move (Easter, Mother's Day, Thanksgiving and friends) are computed algorithmically. Entertainment and sports dates are verified against official announcements.</p>
<h2>Accuracy notes</h2>
<p>Lunar-calendar observances (Ramadan, Eid, Diwali, Chinese New Year) are marked "expected" where moon sighting can shift the date by a day. Countdowns to date-only events run to midnight in <em>your</em> local time zone; timed astronomical events count to the exact UTC moment.</p>'''),
 'privacy': ('Privacy Policy', '''<h1>Privacy Policy</h1>
<p>daysuntil.bond is a static website. We do not require accounts, we do not collect personal information, and the countdowns you view are not tied to you.</p>
<h2>Cookies &amp; analytics</h2>
<p>We may use privacy-respecting analytics and advertising partners (such as Google AdSense) that use cookies or similar technologies to serve and measure ads. You can control personalized advertising through your Google settings. No countdown data or searches you type on this site are stored by us.</p>
<h2>Third-party links</h2>
<p>Our pages link to third-party sites (including sites in our network). We are not responsible for their privacy practices.</p>
<h2>Contact</h2>
<p>Questions? Reach us via any site in our network footer.</p>'''),
 'disclosure': ('Advertising & Affiliate Disclosure', '''<h1>Advertising & Affiliate Disclosure</h1>
<p>daysuntil.bond is reader-supported. The site may display advertising (including Google AdSense) and may contain affiliate links — links to products or services from which we may earn a commission if you make a purchase, at no additional cost to you.</p>
<p>Astronomical data and countdown dates are never influenced by advertisers. Sponsored or affiliate content, where it appears, will be identifiable.</p>'''),
}

def info_page(key):
    title, body = INFO[key]
    ld = breadcrumb_ld([('Home', SITE + '/'), (title, f'{SITE}/{key}/')])
    return head(f'{title} | {BRAND}', f'{title} — {BRAND}: live countdowns to the events the world is waiting for.',
                f'{SITE}/{key}/', '/og/home.png', '<script type="application/ld+json">' + ld + '</script>') + nav_links('..') + f'''</nav>
</header>
<main id="main"><article class="prose">
{body}
</article></main>
''' + footer()

def page404():
    cards = ''.join(card_html(e, '/') for e in events[:6])
    return head(f'Page not found | {BRAND}', 'This countdown does not exist — browse {len(events)} live countdowns instead.', SITE + '/404.html', '/og/home.png', path_prefix='') + nav_links('') + f'''</nav>
</header>
<main id="main">
<h1>404 — this countdown doesn't exist (yet)</h1>
<p>The page you asked for isn't here, but the clock is still ticking on everything below. Or start from the <a href="/">home page</a>.</p>
<section class="cards">{cards}</section>
</main>
<script src="/assets/site.js" defer></script>
''' + footer('')

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#101426"/><circle cx="32" cy="36" r="17" fill="none" stroke="#e8b64c" stroke-width="5"/><path d="M32 6l4 9h-8z" fill="#e8b64c"/><rect x="8" y="10" width="10" height="5" rx="2.5" fill="#5c6bc0"/><rect x="46" y="10" width="10" height="5" rx="2.5" fill="#5c6bc0"/></svg>'

# ---------------------------------------------------------------- write everything
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'og'), exist_ok=True)
open(os.path.join(OUT, 'assets', 'style.css'), 'w').write(CSS)
open(os.path.join(OUT, 'assets', 'site.js'), 'w').write(JS)
open(os.path.join(OUT, 'favicon.svg'), 'w').write(FAVICON)
open(os.path.join(OUT, 'CNAME'), 'w').write('daysuntil.bond\n')
open(os.path.join(OUT, '.nojekyll'), 'w').write('')
open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w').write(INDEXNOW_KEY)
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')

urls = [SITE + '/', SITE + '/about/', SITE + '/privacy/', SITE + '/disclosure/']
for key in ('about', 'privacy', 'disclosure'):
    os.makedirs(os.path.join(OUT, key), exist_ok=True)
    open(os.path.join(OUT, key, 'index.html'), 'w').write(info_page(key))
open(os.path.join(OUT, '404.html'), 'w').write(page404())

for cat in CATS:
    os.makedirs(os.path.join(OUT, cat), exist_ok=True)
    open(os.path.join(OUT, cat, 'index.html'), 'w').write(category_page(cat))
    og_image(os.path.join(OUT, 'og', f'cat-{cat}.png'), CATS[cat]['name'], f'{sum(1 for e in events if e["category"]==cat)} live countdowns', cat)
    urls.append(f'{SITE}/{cat}/')

for e in events:
    os.makedirs(os.path.join(OUT, e['slug']), exist_ok=True)
    open(os.path.join(OUT, e['slug'], 'index.html'), 'w').write(event_page(e))
    if e['slug'] in INDEXABLE:
        urls.append(f'{SITE}/{e["slug"]}/')
    og_image(os.path.join(OUT, 'og', e['slug'] + '.png'), e['title'],
             e['dt'].strftime('%b %-d, %Y') + (' · %d UTC' % e['dt'].hour if e['kind'] == 'datetime' else ''), e['category'])

open(os.path.join(OUT, 'index.html'), 'w').write(home_page())
og_image(os.path.join(OUT, 'og', 'home.png'), 'How Many Days Until…?', f'{len(events)} live countdowns', 'planets', salt='home')

today = BUILD_DATE.isoformat()
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
seen = set()
urls = [u for u in urls if not (u in seen or seen.add(u))]
for u in urls:
    sitemap += f'<url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>{"1.0" if u.endswith("/") and u.count("/") < 4 else "0.8"}</priority></url>\n'
sitemap += '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sitemap)

html_files = sum(len(files) for _, _, files in os.walk(OUT) if files and files[0].endswith('.html'))
print(f'DONE: {html_files} HTML pages, {len(urls)} sitemap URLs, {len(events)} event OG images')
print(f'output: {OUT} ({sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs) // 1024 // 1024} MB)')
