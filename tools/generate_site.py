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
        cands = [f"How Many Days Until {base}? {dd} Day{'' if dd == 1 else 's'} Left",
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
            f"Live countdown to {ev['title']} on {nice} — {_pl(dd, 'day')} to go, with weeks, weekdays and hours remaining.",
            f"{_pl(dd, 'day')} to {ev['title']}, on {nice}. Live countdown in days, hours, minutes and seconds.",
            f"{_pl(dd, 'day')} until {ev['title']} ({nice}). Live countdown, updated every second.",
            f"{_pl(dd, 'day')} until {ev['title']} on {nice}. Live countdown, updated every second.",
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

    evdeep = event_deep_html(e, '..')
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
    {evdeep}
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
{_variant_nav(e, '..') if indexable else ''}
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

# ------------------------------------------------------------------ variants
# days.to outranks every countdown site on identical dates because it publishes a
# separate URL for each question modifier ("how many WEEKS", "how many WEEKDAYS",
# "WHEN IS"). These variants mirror that coverage. Each one answers a DIFFERENT
# question and ships its own computed table, so each page is an answer rather
# than a doorway page.

VARIANT_KINDS = ('weeks', 'weekdays', 'sleeps')


def _pl(n, w):
    return f"{n} {w}" + ("" if n == 1 else "s")


def _wk_phrase(dd):
    wk, rd = divmod(dd, 7)
    if wk == 0: return _pl(rd, 'day')
    if rd == 0: return _pl(wk, 'week')
    return f'{_pl(wk, "week")} and {_pl(rd, "day")}'


def _month_span(a, b):
    out, y, m = [], a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append((y, m)); m += 1
        if m > 12: m, y = 1, y + 1
    return out


def _month_stats(y, m, start, end):
    import calendar as _c
    last = _c.monthrange(y, m)[1]
    lo = max(start, dt.date(y, m, 1)); hi = min(end, dt.date(y, m, last))
    if lo > hi: return 0, 0
    n = (hi - lo).days + 1
    wd = sum(1 for i in range(n) if (lo + dt.timedelta(days=i)).weekday() < 5)
    return wd, n - wd


def _variant_nav(e, pp):
    """cross-links between the four ways of asking the same question"""
    s = e['slug']
    items = [('weeks/', 'How many weeks?'), ('weekdays/', 'How many weekdays?'),
             ('sleeps/', 'How many sleeps?')]
    links = ''.join(f'<a href="{u}">{lbl}</a>' for u, lbl in items)
    links += f'<a href="{pp}when-is/{s}/">When is it?</a>'
    return (f'<nav class="varnav" style="display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0">'
            f'<a href="{pp}{s}/" style="padding:.4rem .8rem;border:1px solid #ccc;border-radius:99px;'
            f'text-decoration:none;font-size:.9rem">← Main countdown</a>'
            + ''.join(f'<a href="{u}" style="padding:.4rem .8rem;border:1px solid #ccc;border-radius:99px;'
                      f'text-decoration:none;font-size:.9rem">{lbl}</a>' for u, lbl in items)
            + f'<a href="{pp}when-is/{s}/" style="padding:.4rem .8rem;border:1px solid #ccc;border-radius:99px;'
              f'text-decoration:none;font-size:.9rem">When is it?</a></nav>')


def _table(head_cells, rows, cap=''):
    h = ''.join(f'<th>{esc(c)}</th>' for c in head_cells)
    b = ''.join('<tr>' + ''.join(f'<td>{esc(str(c))}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tablewrap"><table class="facts">{f"<caption>{esc(cap)}</caption>" if cap else ""}<tr>{h}</tr>{b}</table></div>'


def _variant_title_desc(kind, e, d):
    """Titles/descriptions fitted to Google's display limits, per variant."""
    t = e['title']
    today = dt.date.today()
    dd = (d.date() - today).days
    wk, rd = divmod(dd, 7)
    nice = date_nice(d)
    if kind == 'weeks':
        cand = [f'How Many Weeks Until {t}?', f'Weeks Until {t}', f'Weeks Until {t} — Count']
        body = (f'{t} falls on {nice}. That is {_wk_phrase(dd)} away. '
                f'Week-by-week countdown showing exactly when each milestone lands, updated live.')
    elif kind == 'weekdays':
        cand = [f'How Many Weekdays Until {t}?', f'Weekdays Until {t}', f'Weekdays Until {t} — Count']
        body = (f'{t} falls on {nice}. See how many of the days between now and then are working '
                f'days and how many fall on a weekend, broken down month by month.')
    elif kind == 'sleeps':
        cand = [f'How Many Sleeps Until {t}?', f'Sleeps Until {t}', f'Sleeps Until {t} — Count']
        body = (f'{t} falls on {nice}, which is {_pl(dd, 'sleep')} away. A sleep countdown is one more '
                f'than the number of full nights left. Live count, updated every second.')
    else:
        cand = [f'When Is {t}?', f'When Is {t} — Date', f'When is {t}?']
        body = (f'{t} falls on {nice} — a {d.strftime("%A")}. Exact date and time, plus the date '
                f'for the next five years so you can plan ahead.')
    title = next((c for c in cand if len(c) <= TITLE_MAX), _trim_words(cand[0], TITLE_MAX))
    if len(body) > DESC_MAX:
        cut = body[:DESC_MAX]
        p = max(cut.rfind('. '), cut.rfind('! '))
        body = (cut[:p + 1] if p > DESC_MAX * 0.6 else _trim_words(cut, DESC_MAX)).strip()
    return title, body


def _variant_faq(kind, e, d):
    t = e['title']; nice = date_nice(d); dow = d.strftime('%A')
    today = dt.date.today()
    dd = (d.date() - today).days
    wk, rd = divmod(dd, 7)
    if kind == 'weeks':
        return [(f'How many weeks until {t}?', f'{_wk_phrase(dd)}, as of today. {t} falls on {nice}.'),
                (f'Is that full weeks or rounded?', f'Full weeks: {wk}. The remaining {_pl(rd, "day")} do not add up to a whole one, which is why the plain week count and the weeks-and-days count differ.'),
                (f'When does the week count tick over?', 'Every seven days, counted to the second. The countdown runs in your own time zone rather than UTC, so it changes when your clock says it should.'),
                (f'What date is {t}?', f'{nice} — a {dow}.')]
    if kind == 'weekdays':
        wdays = sum(1 for i in range(1, dd + 1) if (today + dt.timedelta(days=i)).weekday() < 5) if dd > 0 else 0
        return [(f'How many weekdays until {t}?', f'{wdays} weekdays, with {dd - wdays} days falling on a weekend, out of {dd} days in total.'),
                (f'Does that include public holidays?', 'No. The count is Monday to Friday only. Public holidays differ by country and employer, so subtract them from the month-by-month table below to get your own figure.'),
                (f'Why count weekdays instead of days?', 'Because it is the number that maps onto real working time. A 60-day countdown sounds generous until you realise 16 of those days are a weekend.'),
                (f'What date is {t}?', f'{nice} — a {dow}.')]
    if kind == 'sleeps':
        return [(f'How many sleeps until {t}?', f'{_pl(dd, 'sleep')}. {t} falls on {nice}.'),
                (f'How is a sleep counted?', 'One sleep equals one night still to go. On the morning of the day before, the answer is one; on the morning of the day itself, it is zero.'),
                (f'Is the number of sleeps the same as the number of days?', f'Almost. A sleep count is the number of nights remaining, which is one more than the number of whole days left when the event lands mid-morning.'),
                (f'What date is {t}?', f'{nice} — a {dow}.')]
    return [(f'When is {t}?', f'{t} falls on {nice} — a {dow}.'),
            (f'What day of the week is {t}?', f'A {dow}. The day of the week shifts by one each year, and by two when a leap year intervenes.'),
            (f'Has the date for {t} been confirmed?', f'Yes — this page uses the confirmed date for {t}. The table below carries the date forward for the next five years.'),
            (f'How many days until {t}?', f'{dd} days. The live countdown on the main page gives it to the second.')]


def _variant_body(kind, e, d, pp):
    t = e['title']; nice = date_nice(d); dow = d.strftime('%A')
    today = dt.date.today()
    dd = (d.date() - today).days
    wk, rd = divmod(dd, 7)
    slug = e['slug']
    about = ''.join(f'<p>{p}</p>' for p in (e.get('desc') or [])[:2])

    if kind == 'weeks':
        rows = [(k, (d.date() - dt.timedelta(days=k * 7)).strftime('%a %d %b %Y'))
                for k in range(wk, 0, -1)]
        if len(rows) > 26:
            rows = rows[:12] + [('…', '…')] + rows[-12:]
        tbl = _table(['Weeks to go', 'Starts on'], rows,
                     f'Week-by-week countdown to {t}')
        lead = (f'<p>{t} falls on <b>{nice}</b> — a {dow}. As of today that is <b>{dd} days</b>, '
                f'or <b>{_wk_phrase(dd)}</b>. The table below lists every "weeks to go" '
                f'milestone between now and the date, so you can work backwards from the day itself '
                f'instead of counting forward from today.</p>')
        note = ('<p>Weeks are the unit people actually plan in. Deadlines, notice periods and '
                'rotas run in weeks, which is why a week count tends to be more useful than a raw '
                'day count once you are more than a fortnight out. Note that the two figures answer '
                'slightly different questions: "how many weeks" is full weeks only, while '
                '"weeks and days" keeps the remainder.</p>')
        h2b = 'Why the week count moves the way it does'
    elif kind == 'weekdays':
        wdays = sum(1 for i in range(1, dd + 1) if (today + dt.timedelta(days=i)).weekday() < 5) if dd > 0 else 0
        rows, twd, twe = [], 0, 0
        for (y, m) in _month_span(today, d.date())[:26]:
            a, b = _month_stats(y, m, today + dt.timedelta(days=1), d.date())
            twd += a; twe += b
            rows.append((dt.date(y, m, 1).strftime('%B %Y'), a, b, a + b))
        if len(rows) > 26: rows = rows[:26]
        tbl = _table(['Month', 'Weekdays', 'Weekend days', 'Total'], rows,
                     f'Working days between today and {t}')
        lead = (f'<p>{t} falls on <b>{nice}</b> — a {dow}. Of the <b>{dd} days</b> between today and '
                f'that date, <b>{wdays}</b> are weekdays (Monday to Friday) and <b>{dd - wdays}</b> '
                f'fall on a weekend. The month-by-month split below is the practical version of that '
                f'number: it tells you where your working time actually goes.</p>')
        note = ('<p>This count is Monday to Friday only and does <b>not</b> strip out public '
                'holidays. Those vary by country, state and employer, so subtract the ones you '
                'actually get from the month that contains them. If you work a non-standard rota, '
                'the weekend column is the figure to adjust rather than the weekday column.</p>')
        h2b = 'What this count leaves out'
    else:
        rows = [(k, (d.date() - dt.timedelta(days=k)).strftime('%a %d %b'))
                for k in range(min(dd, 10), 0, -1)]
        tbl = _table(['Sleeps left', 'Morning of'], rows, f'Final nights before {t}')
        lead = (f'<p>{t} falls on <b>{nice}</b>, which is <b>{dd} sleeps</b> away. A sleep count is '
                f'the number of nights still to come rather than the number of days, which is why '
                f'it is the version adults reach for when the person asking is a child — and why it '
                f'stays intuitive long after the day count stops meaning much.</p>')
        note = ('<p>The convention: one sleep means one night still to go. On the morning before, '
                'the answer is one. On the morning of the day itself, it is zero — you have run out '
                'of nights to sleep through. Because it tracks nights rather than 24-hour periods, '
                'the figure can read one higher than the day count for an event that lands in the '
                'morning.</p>')
        h2b = 'How a sleep count works'

    faq = _variant_faq(kind, e, d)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage',
                     'mainEntity': [{'@type': 'Question', 'name': q,
                                     'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
    crumb = breadcrumb_ld([('Home', SITE + '/'), (CATS[e['category']]['name'], f'{SITE}/{e["category"]}/'),
                           (t, f'{SITE}/{slug}/'), (kind.capitalize(), f'{SITE}/{slug}/{kind}/')])
    ldb = ('<script type="application/ld+json">' + ld + '</script>\n'
           '<script type="application/ld+json">' + crumb + '</script>')
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
    title, desc = _variant_title_desc(kind, e, d)
    cfg = json.dumps({'kind': e['kind'], 'y': d.year, 'm': d.month, 'd': d.day,
                      'utc': e.get('utc'), 'title': t, 'dateNice': nice})
    rel = related_events(e, 6)
    cards = ''.join(f'''<a class="card" href="{pp}{r['slug']}/"><span class="card-cat">{CATS[r['category']]['icon']} {CATS[r['category']]['name']}</span>
      <b>{esc(r['title'])}</b><span class="card-date">{date_nice(r['dt'])}</span></a>''' for r in rel)

    return head(title, desc, f'{SITE}/{slug}/{kind}/', f'/og/{slug}.png', ldb, pp, True) + nav_links(pp) + f'''</nav>
</header>
<main id="main">
<nav class="crumbs"><a href="{pp}">Home</a> › <a href="{pp}{e['category']}/">{CATS[e['category']]['name']}</a> › <a href="{pp}{slug}/">{esc(t)}</a> › <span>{kind.capitalize()}</span></nav>
<h1>{esc(_variant_title_desc(kind, e, d)[0])}</h1>
<section class="hero" data-cat="{e['category']}">
  <div class="cd">
    <div class="cd-days"><span id="cd-d">–</span><small>days</small></div>
    <div class="cd-grid">
      <div><b id="cd-h">–</b><small>hours</small></div>
      <div><b id="cd-m">–</b><small>minutes</small></div>
      <div><b id="cd-s">–</b><small>seconds</small></div>
    </div>
    <p class="cd-status" id="cd-status">{esc(t)} falls on {nice}.</p>
  </div>
  <div class="chips">
    <span class="chip">📅 <b id="ch-weeks">–</b> weeks</span>
    <span class="chip">💼 <b id="ch-wd">–</b> weekdays</span>
    <span class="chip">🛌 <b id="ch-we">–</b> weekend days</span>
    <span class="chip">🗓️ <b id="ch-months">–</b> months (approx)</span>
  </div>
</section>
{_variant_nav(e, pp)}
{lead}
{tbl}
<h2>{h2b}</h2>
{note}
<h2>About {esc(t)}</h2>
{about}
<section class="grid2">
  <div><h2>Quick facts</h2><table class="facts">{''.join(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in e['facts'])}</table></div>
  <aside><h2>FAQ</h2><div class="faq">{faq_html}</div></aside>
</section>
<h2>Related countdowns</h2>
<section class="cards">{cards}</section>
</main>
<script>window.EVENT={cfg};</script>
<script src="{pp}assets/site.js" defer></script>
''' + footer(pp)


def when_is_page(e):
    t = e['title']; d = e['dt']; nice = date_nice(d); dow = d.strftime('%A')
    today = dt.date.today(); dd = (d.date() - today).days
    years = []
    for k in range(6):
        try:
            nd = d.replace(year=d.year + k)
        except ValueError:
            nd = d.replace(year=d.year + k, day=28)
        years.append((nd.year, nd.strftime('%a %d %b %Y'), nd.strftime('%A')))
    tbl = _table(['Year', 'Date', 'Day of week'], years, f'{t} — date by year')
    about = ''.join(f'<p>{p}</p>' for p in (e.get('desc') or [])[:3])
    faq = _variant_faq('when', e, d)
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage',
                     'mainEntity': [{'@type': 'Question', 'name': q,
                                     'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
    crumb = breadcrumb_ld([('Home', SITE + '/'), (t, f'{SITE}/when-is/{e["slug"]}/')])
    ldb = ('<script type="application/ld+json">' + ld + '</script>\n'
           '<script type="application/ld+json">' + crumb + '</script>')
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)
    title, desc = _variant_title_desc('when', e, d)
    cfg = json.dumps({'kind': e['kind'], 'y': d.year, 'm': d.month, 'd': d.day,
                      'utc': e.get('utc'), 'title': t, 'dateNice': nice})
    pp = '..'
    rel = related_events(e, 6)
    cards = ''.join(f'''<a class="card" href="{pp}/{r['slug']}/"><span class="card-cat">{CATS[r['category']]['icon']} {CATS[r['category']]['name']}</span>
      <b>{esc(r['title'])}</b><span class="card-date">{date_nice(r['dt'])}</span></a>''' for r in rel)
    return head(title, desc, f'{SITE}/when-is/{e["slug"]}/', f'/og/{e["slug"]}.png', ldb, pp, True) + nav_links(pp) + f'''</nav>
</header>
<main id="main">
<nav class="crumbs"><a href="{pp}/">Home</a> › <a href="{pp}/{e['category']}/">{CATS[e['category']]['name']}</a> › <span>When is {esc(t)}?</span></nav>
<h1>When Is {esc(t)}?</h1>
<section class="hero" data-cat="{e['category']}">
  <div class="cd">
    <div class="cd-days"><span id="cd-d">–</span><small>days</small></div>
    <div class="cd-grid">
      <div><b id="cd-h">–</b><small>hours</small></div>
      <div><b id="cd-m">–</b><small>minutes</small></div>
      <div><b id="cd-s">–</b><small>seconds</small></div>
    </div>
    <p class="cd-status" id="cd-status">{esc(t)} falls on {nice}.</p>
  </div>
</section>
{_variant_nav(e, pp + '/')}
<p><b>{esc(t)} falls on {nice} — a {dow}.</b> That is <b>{dd} days</b> from today. The date is confirmed, so the only thing that moves is the countdown itself.</p>
{tbl}
<h2>Why the day of the week moves</h2>
<p>A date advances by one weekday each year, because 365 days is 52 weeks plus one day. In a leap year it advances by two, which is why the weekday occasionally jumps. Over the six years in the table above you can watch both patterns: the single-step years and the leap-year double step.</p>
<p>This matters more than it sounds if you are planning around a weekend. An event that lands on a Saturday this year may fall midweek in two years' time, which changes everything from travel to time off.</p>
<h2>About {esc(t)}</h2>
{about}
<section class="grid2">
  <div><h2>Quick facts</h2><table class="facts">{''.join(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in e['facts'])}</table></div>
  <aside><h2>FAQ</h2><div class="faq">{faq_html}</div></aside>
</section>
<h2>Related countdowns</h2>
<section class="cards">{cards}</section>
</main>
<script>window.EVENT={cfg};</script>
<script src="{pp}/assets/site.js" defer></script>
''' + footer(pp)


# ------------------------------------------------------- category deep content
# Category hubs were the thinnest pages on the site (144-301 words) despite
# being the most heavily linked pages after the homepage. Each one now carries a
# computed table of what is coming up, an honest note on how those dates are
# actually arrived at, and four real questions.

CAT_DEEP = {
 'holidays': dict(
   how=("Some of these dates never move and some move every year, and the two need different kinds of "
        "confidence. Christmas is 25 December by definition; the only question is which weekday it lands "
        "on. Easter is the opposite: it falls on the first Sunday after the Paschal full moon, which is "
        "why it can land anywhere between 22 March and 25 April. Thanksgiving in the United States is the "
        "fourth Thursday of November, and in Canada the second Monday of October — so the same holiday "
        "sits six weeks apart depending on which side of the border you are counting down to."),
   faq=[('Why do some holiday dates change every year?',
         'Because they are anchored to something other than the calendar. Easter follows the moon, '
         'Thanksgiving follows a weekday count, and Ramadan follows a sighting. Fixed-date holidays '
         'like Christmas only change their weekday.'),
        ('Are these dates confirmed?',
         'Fixed-date holidays are known years ahead. Moveable ones are computed from the rule that '
         'defines them. Where a date depends on a religious authority or a sighting, we say so on the '
         'page rather than presenting it as settled.'),
        ('Do you count in my time zone?',
         'Yes. Countdowns run in your local time zone, not UTC, so the number changes when your clock '
         'says it should.'),
        ('What about public holidays that differ by country?',
         'We list the date as it is observed in the country the holiday belongs to. If a country moves '
         'it to a Monday, that is noted on the event page.')]),
 'moon': dict(
   how=("A full moon is the moment the Moon sits opposite the Sun in ecliptic longitude, not a whole "
        "night. That is why the date can differ by a day depending on where you are, and why the Moon "
        "can look full on two consecutive evenings. The gap between one full moon and the next is the "
        "synodic month: 29 days, 12 hours and 44 minutes on average. Because that is not a whole number "
        "of days, full moon dates drift about eleven days earlier each year until a thirteenth full moon "
        "resets the sequence — the blue moon."),
   faq=[('What exactly is a full moon?',
         'The instant the Moon and Sun are opposite each other in ecliptic longitude. It lasts a moment, '
         'though the Moon looks full for roughly a day either side.'),
        ('Why does the date differ between sources?',
         'Because the moment is converted into different time zones. A full moon at 23:40 UTC is already '
         'the next day in Sydney and still the previous evening in Los Angeles.'),
        ('What is a blue moon?',
         'Two full moons in one calendar month. It happens roughly every two to three years because the '
         'synodic month is shorter than most calendar months.'),
        ('How accurate are these times?',
         'They are computed from lunar theory and are accurate to within a minute or so, which is far '
         'finer than anything you could observe by eye.')]),
 'eclipses': dict(
   how=("Eclipses come in seasons. Roughly every six months the new or full moon passes close enough to "
        "a lunar node for the three bodies to line up, and an eclipse happens somewhere on Earth. A "
        "solar eclipse is the Moon's shadow touching the Earth's surface — which is why it is only "
        "visible from a narrow track a couple of hundred kilometres wide, and why totality at any one "
        "spot lasts minutes. A lunar eclipse is the Earth's shadow falling on the Moon, visible from "
        "the whole night side at once and lasting over an hour. Eclipses repeat in families called saros "
        "series, each one shifted a third of the way around the globe."),
   faq=[('What is the difference between a total and an annular eclipse?',
         'In a total eclipse the Moon covers the Sun completely. In an annular one the Moon is near its '
         'farthest point and appears slightly too small, leaving a ring of Sun visible.'),
        ('Can I see this one where I live?',
         'Only if you are inside the visibility region, which for a solar eclipse is a narrow track. '
         'Each event page states where it is visible.'),
        ('Is it safe to look at a solar eclipse?',
         'Not without proper solar filters. Looking at the partially covered Sun is as damaging as '
         'looking at the full Sun, and the damage is painless, so you will not notice it happening.'),
        ('Why are lunar eclipses more common to see?',
         'A lunar eclipse is visible from anywhere on the night side of the Earth at once, so roughly '
         'half the planet can watch it. A solar eclipse is visible only from a narrow track.')]),
 'planets': dict(
   how=("Retrograde is not a planet moving backwards. It is an overtaking. Earth and the other planet "
        "are both orbiting the Sun at different speeds, and when Earth catches up and passes, the other "
        "planet appears to stall and reverse against the background stars for a few weeks before "
        "resuming its normal direction. It is the same effect as being passed on a motorway: the car you "
        "overtake seems to slide backwards even though it is still moving forward. These pages give the "
        "station dates — the moments the apparent motion turns — computed from Keplerian orbital "
        "elements rather than read off a table."),
   faq=[('Does a planet actually move backwards?',
         'No. The apparent reversal is a line-of-sight effect caused by the Earth overtaking a slower '
         'orbiting planet.'),
        ('How long does a retrograde last?',
         'Mercury about three weeks, three or four times a year. The slower outer planets stay retrograde '
         'for four to five months at a time.'),
        ('What is a shadow period?',
         'The stretch either side of the retrograde when the planet is retracing ground it will cover '
         'again, or already did. Many astrologers treat it as part of the same window.'),
        ('Are these dates computed or copied?',
         'Computed from orbital elements, then checked against published ephemerides. They are the '
         'astronomical station dates, not a symbolic one.')]),
 'meteor-showers': dict(
   how=("A meteor shower happens when the Earth ploughs through a trail of debris left by a comet or, "
        "occasionally, an asteroid. The bits burn up in the upper atmosphere, and because they are all "
        "travelling in parallel they appear to radiate from a single point in the sky — which is why "
        "each shower is named after the constellation it seems to come from. The peak is the night the "
        "Earth passes through the densest part of the trail, and it can be sharp or broad depending on "
        "how old and spread out that trail is. Moonlight is the other variable: a bright Moon washes out "
        "everything except the brightest meteors."),
   faq=[('What time of night is best?',
         'After midnight, and best of all in the hour or two before dawn. Before midnight you are on the '
         'trailing side of the Earth and see fewer meteors.'),
        ('Do I need a telescope?',
         'No, and it would get in the way. Meteors are best seen with the naked eye from a dark site '
         'with as wide a view of the sky as you can find.'),
        ('How many will I actually see?',
         'The quoted zenithal hourly rate is a theoretical maximum under a perfectly dark sky with the '
         'radiant overhead. Realistic counts are usually well below it.'),
        ('Does the Moon ruin it?',
         'It can. A full Moon near the radiant cuts the visible count substantially, which is why the '
         'same shower is excellent one year and disappointing the next.')]),
 'seasons': dict(
   how=("An equinox or solstice is a single moment, not a day. The March and September equinoxes are "
        "when the Sun crosses the celestial equator and day and night come closest to equal; the June "
        "and December solstices are when the Earth's axial tilt is at its most extreme toward or away "
        "from the Sun, giving the longest and shortest days. Because the Earth's orbit is elliptical "
        "and the calendar year is not a whole number of days, the exact minute shifts from year to "
        "year, and the date can move by a day across a leap-year cycle."),
   faq=[('Is the solstice a whole day?',
         'No — it is the exact moment the tilt is at its maximum. We call the whole day the solstice '
         'because that is how calendars work, but the astronomical event lasts an instant.'),
        ('Why is the longest day not the hottest?',
         'Because the oceans and land take weeks to warm up. The seasonal lag means peak temperatures '
         'arrive a month or more after peak sunlight.'),
        ('Why does the date move?',
         'The tropical year is about 365.2422 days, not 365. The leap-year system absorbs the difference, '
         'which makes the exact moment drift and then snap back.'),
        ('Are the equinoxes really equal day and night?',
         'Very nearly, but not exactly: refraction lifts the Sun slightly and the day is measured from '
         'the edge of the disc rather than its centre.')]),
 'gaming': dict(
   how=("Game release dates are announcements, not astronomical events, which makes them a different "
        "kind of countdown. A date is real when the publisher has put it in a financial filing or a "
        "dated trailer, and provisional until then. Slips are normal and usually land two to six months "
        "after the original window, so treat any date more than a year out as a placeholder. Where a "
        "title has a confirmed date and a previous slipped one, we count to the confirmed date."),
   faq=[('Are these release dates confirmed?',
         'Only where stated. A date quoted from a publisher announcement is firmer than one quoted from '
         'a retailer listing, and we label which is which.'),
        ('Do release dates slip often?',
         'Frequently. Industry-wide, a majority of titles with dates more than a year out move at least '
         'once.'),
        ('Why is the countdown in my time zone?',
         'Because unlocks are usually simultaneous worldwide at a stated UTC hour, so your local unlock '
         'time depends on where you are.'),
        ('What if the date changes after you publish?',
         'We update the page. If you spot a slip before we do, the about page has a contact route.'), ('Why do game release dates slip so often?',
           'Because a date is a marketing commitment made before the work is finished. A slip is usually a sign the studio wants the game to work rather than a sign of trouble, and it is common enough that we treat any date more than a year out as provisional.'), ('Do release times differ by platform?',
           'Often. Console and PC unlocks are frequently staggered, and a simultaneous global unlock is the exception. Check the platform-specific time before planning around it.')]),
 'movies': dict(
   how=("Theatrical dates work like game releases: they are commercial announcements and they move. A "
        "date is firm once the studio has it on a dated trailer or in exhibition materials, and soft "
        "before that. Studios also shift dates to avoid colliding with a competing tentpole, which is "
        "why a release can move twice in a year without anything having gone wrong."),
   faq=[('How reliable are these dates?',
         'Reasonably firm inside six months, much less so beyond a year. We mark the source on each page.'),
        ('Do release dates differ by country?',
         'Often. A global release is the exception rather than the rule, and territories frequently open '
         'a week or two apart.'),
        ('Why do studios move dates?',
         'Mostly to avoid competition, sometimes because post-production ran long. Neither is unusual.'),
        ('Will you update if it slips?',
         'Yes. The countdown updates to the corrected date when the studio confirms one.'), ('Do release dates differ by country?',
           'Frequently. A simultaneous global release is the exception rather than the rule, and territories often open a week or two apart.'), ('How far ahead are film dates settled?',
           'Studios announce dates years out and then move them to avoid competition. A date inside six months is reasonably firm; anything beyond a year is a placeholder.')]),
 'sports': dict(
   how=("Sporting fixtures are scheduled years ahead and are the most reliable dates on this site — a "
        "Super Bowl or an Olympic opening ceremony is fixed by contract and broadcast deal long in "
        "advance. The one thing that does move is kickoff time, which is set for a television audience "
        "and can shift by an hour or three depending on the territory. The date, unlike the start time, "
        "essentially never changes."),
   faq=[('Are these dates confirmed?',
         'Yes. Major finals and opening ceremonies are contracted years ahead of time.'),
        ('Do kickoff times change?',
         'They can, and broadcasters adjust them for their audience. The date is stable; the hour is not.'),
        ('Why is the countdown in my time zone?',
         'So it matches your own clock. A fixture that starts Sunday evening in the United States starts '
         'early Monday morning in Europe.'),
        ('What about events that get postponed?',
         'Rare, but it happens. If a fixture moves we update the countdown to the rescheduled date.'), ('How far ahead are sporting fixtures set?',
           'Major finals and opening ceremonies are contracted years in advance, which makes them among the most reliable dates on this site. Kickoff times are set much later, for television.'), ('What happens if a fixture is postponed?',
           'It is rare for a final. Where it happens we update the countdown to the rescheduled date rather than leaving the old one running.')]),
}


def _cat_table(cat):
    today = dt.date.today()
    rows, shown = [], 0
    for e in events:
        if e['category'] != cat: continue
        d = e['dt'].date()
        if d < today: continue
        if shown >= 18: break
        rows.append((esc(e['title']), date_nice(e['dt']), d.strftime('%A'), (d - today).days))
        shown += 1
    if not rows: return ''
    body = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{n}</td></tr>' for a, b, c, n in rows)
    return ('<div class="tablewrap"><table class="facts"><tr><th>Event</th><th>Date</th>'
            '<th>Day</th><th>Days away</th></tr>' + body + '</table></div>')


# ------------------------------------------------------- event deep content
# The event pages themselves were the thinnest indexable pages left on the site
# (~390-500 words). Two blocks are added, both computed from the event's own
# date, so every page gets different content rather than a shared template.


def _milestones(e, today):
    """Dates on which the countdown passes each milestone — unique per event."""
    d = e['dt'].date()
    rows = []
    for n in (365, 200, 100, 50, 30, 14, 7, 3, 1):
        md = d - dt.timedelta(days=n)
        if md >= today:
            rows.append((n, md))
    return rows


def _breakdown(e, today):
    d = e['dt'].date()
    dd = (d - today).days
    if dd <= 0:
        return None, dd
    wk, rd = divmod(dd, 7)
    wdays = sum(1 for i in range(1, dd + 1) if (today + dt.timedelta(days=i)).weekday() < 5)
    months = round(dd / 30.4375, 1)
    return dict(days=dd, weeks=f'{wk} weeks and {rd} days', months=months,
                weekdays=wdays, weekends=dd - wdays, hours=dd * 24,
                sleeps=dd, seconds=dd * 86400), dd


def _past_html(e, today):
    """For events that have already happened: what it was, when, and what is next."""
    d = e['dt'].date()
    ago = (today - d).days
    t = esc(e['title'])
    base = _base(e['slug'])
    nxt = None
    for x in events:
        if x['slug'] == e['slug']:
            continue
        if _base(x['slug']) == base and x['dt'].date() >= today:
            nxt = x
            break
    if nxt is None:
        for x in events:
            if x['category'] == e['category'] and x['dt'].date() >= today:
                nxt = x
                break
    nxt_html = ''
    if nxt:
        nd = nxt['dt'].date()
        nxt_html = (f'<h2>What comes next</h2><p>The next one on our calendar is '
                    f'<a href="../{nxt["slug"]}/">{esc(nxt["title"])}</a>, on '
                    f'<b>{date_nice(nxt["dt"])}</b> — a {nd.strftime("%A")}, '
                    f'{_pl((nd - today).days, "day")} from today.</p>')
    return (f'<h2>This one has already passed</h2>'
            f'<p>{t} fell on <b>{date_nice(e["dt"])}</b> — a {d.strftime("%A")} — which is '
            f'<b>{_pl(ago, "day")}</b> ago. The countdown on this page now counts up rather than down, '
            f'and the date is kept because people look it up after the fact as often as before it.</p>'
            + nxt_html)


def event_deep_html(e, pp):
    today = dt.date.today()
    br, dd = _breakdown(e, today)
    if br is None:
        return _past_html(e, today)
    t = esc(e['title'])

    ms = _milestones(e, today)
    out = ''
    if len(ms) >= 2:
        rows = ''.join(
            f'<tr><td><b>{n} days</b></td><td>{md.strftime("%A")}</td>'
            f'<td>{md.strftime("%d %B %Y")}</td><td>{_pl(n, "day")} to go</td></tr>'
            for n, md in ms)
        first = ms[-1]
        out += (f'<h2>Your {t} countdown milestones</h2>'
                f'<p>It is easier to plan against fixed points than against a number that moves. These '
                f'are the dates on which the countdown to {t} passes each marker between now and the '
                f'day itself — the last one falls on <b>{first[1].strftime("%A %d %B")}</b>, when there '
                f'will be {_pl(first[0], "day")} left.</p>'
                f'<div class="tablewrap"><table class="facts">'
                f'<tr><th>Milestone</th><th>Day</th><th>Date</th><th>Remaining</th></tr>'
                f'{rows}</table></div>')

    out += (f'<h2>How the remaining time breaks down</h2>'
            f'<p>{_pl(br["days"], "day")} is the headline, but it is rarely the number that helps. '
            f'<b>{br["weekdays"]}</b> of those are weekdays and <b>{br["weekends"]}</b> fall on a '
            f'weekend, which is the split that matters if you are planning around work. It is '
            f'{br["weeks"]}, or roughly {br["months"]} months, or about {br["hours"]:,} hours.</p>'
            f'<div class="tablewrap"><table class="facts">'
            f'<tr><th>Unit</th><th>Until {t}</th></tr>'
            f'<tr><td>Days</td><td>{br["days"]}</td></tr>'
            f'<tr><td>Weeks</td><td>{br["weeks"]}</td></tr>'
            f'<tr><td>Months (approx)</td><td>{br["months"]}</td></tr>'
            f'<tr><td>Weekdays</td><td>{br["weekdays"]}</td></tr>'
            f'<tr><td>Weekend days</td><td>{br["weekends"]}</td></tr>'
            f'<tr><td>Hours</td><td>{br["hours"]:,}</td></tr>'
            f'<tr><td>Sleeps</td><td>{br["sleeps"]}</td></tr>'
            f'</table></div>'
            f'<p>Working days are Monday to Friday and do not subtract public holidays, which vary by '
            f'country and employer — <a href="weekdays/">the full month-by-month split</a> is on our '
            f'weekday page for {t}.</p>')
    return out


CAT_EXTRA = {'gaming': '<h2>How we decide a release date is real</h2>\n<p>A date earns a place on this site when it comes from the publisher directly — a dated trailer, a\nfinancial filing, or a store listing the publisher controls. A date found only on a retailer page or\nin a rumour round-up does not, because those are wrong often enough to be worse than useless. Where a\ntitle has both a confirmed date and an earlier one it has since missed, we count to the confirmed one\nand say which is which.</p>\n<p>Unlock times are the other half of the question and work differently. Most launches unlock at a\nstated global moment, which lands at a different local hour depending on where you are counting from,\nso two people can be counting to the same instant and see it fall on different days.</p>', 'movies': '<h2>How we decide a theatrical date is real</h2>\n<p>We take a date from the studio or the distributor, not from a listing aggregator. A dated trailer,\na press release or exhibition material counts; a cinema chain page does not, because those are\nprovisional until the studio confirms. Studios also move dates to avoid colliding with a competing\nrelease, which is why a film can shift twice in a year without anything having gone wrong in\nproduction.</p>\n<p>Territory is the part people miss. A "global release" is the exception rather than the rule, and\nmost films open in some markets a week or two before or after the domestic date. If you are counting\ndown outside the film\'s home market, check the local date before trusting the countdown.</p>', 'sports': '<h2>Why these are the most reliable dates here</h2>\n<p>A major final or an opening ceremony is fixed by contract and broadcast deal years ahead — a host\ncity is awarded, a venue is booked, and television rights are sold against specific dates. That makes\nsporting fixtures considerably firmer than anything else on this site, including astronomical events,\nwhich shift by minutes as the calculations are refined.</p>\n<p>The one thing that does move is the start time, and it moves for television rather than for sport:\nbroadcasters shift kickoff to suit their audience, sometimes by several hours. So the date you are\ncounting down to is stable, and the hour you need to be free is not. If the fixture matters, confirm\nthe local start time closer to the day.</p>'}


def category_page(cat):
    c = CATS[cat]
    evs = [e for e in events if e['category'] == cat]
    cards = ''.join(card_html(e, '../') for e in evs)
    ld = breadcrumb_ld([('Home', SITE + '/'), (c['name'], f'{SITE}/{cat}/')])
    _d = CAT_DEEP.get(cat, {})
    cat_how = _d.get('how', '')
    cat_extra = CAT_EXTRA.get(cat, '')
    cat_tbl = _cat_table(cat)
    _fq = _d.get('faq') or []
    cat_faq = ld_faq = ''
    if _fq:
        cat_faq = '<h2>FAQ</h2><div class="faq">' + ''.join(
            f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in _fq) + '</div>'
        _ld2 = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage',
                           'mainEntity': [{'@type': 'Question', 'name': q,
                                           'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in _fq]})
        ld_faq = '\n<script type="application/ld+json">' + _ld2 + '</script>'
    t = _trim_words(f'{c["name"]} — Live Countdowns ({len(evs)} events)', TITLE_MAX)
    desc = _trim_words(f'Live countdowns to {len(evs)} {c["name"].lower()} — days, hours, minutes and seconds, updated every second in your time zone.', DESC_MAX)
    return head(t, desc, f'{SITE}/{cat}/', f'/og/cat-{cat}.png', '<script type="application/ld+json">' + ld + '</script>' + ld_faq) + nav_links('..') + f'''</nav>
</header>
<main id="main">
<nav class="crumbs"><a href="../">Home</a> › <span>{c['name']}</span></nav>
<h1>{c['icon']} {c['name']}</h1>
<p class="lead">{c['blurb']}</p>
<h2>Coming up next</h2>
{cat_tbl}
<h2>How these dates are worked out</h2>
<p>{cat_how}</p>
{cat_extra}
{AD_LB}<section class="cards">{cards}</section>
{cat_faq}
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
<p>Lunar-calendar observances (Ramadan, Eid, Diwali, Chinese New Year) are marked "expected" where moon sighting can shift the date by a day. Countdowns to date-only events run to midnight in <em>your</em> local time zone; timed astronomical events count to the exact UTC moment.</p>
<h2>Why the countdowns are per-event rather than one big clock</h2>
<p>Search behaviour decides this. Someone wanting to know how long until Halloween does not want a widget they have to configure — they want the number, and they want it to be right for where they are. So every event gets its own page, its own date table and its own set of ways to count it: days, weeks, weekdays, sleeps and the exact date. The number is computed in your browser against your own clock, which is why it changes when your day does rather than when ours does.</p>
<h2>What we get wrong, and how it gets fixed</h2>
<p>Dates slip. A game moves six months, a studio shifts a release, a lunar observance lands a day either side of a prediction. Where a date depends on a sighting or an announcement we mark it rather than presenting it as settled, and when something moves we correct the page. If you spot a date that is wrong, the footer links to other sites in our network and any of them reaches us — corrections are the one kind of email we answer fastest.</p>
<h2>What this site is not</h2>
<p>It is not an astrology service, and the planetary station dates here are astronomical rather than interpretive: they say when Mercury's apparent motion turns, not what that means for your week. There is no horoscope, no reading and nothing to sign up for. The countdowns are the product.</p>'''),
 'privacy': ('Privacy Policy', '''<h1>Privacy Policy</h1>
<p>daysuntil.bond is a static website. We do not require accounts, we do not collect personal information, and the countdowns you view are not tied to you.</p>
<h2>Cookies &amp; analytics</h2>
<p>We may use privacy-respecting analytics and advertising partners (such as Google AdSense) that use cookies or similar technologies to serve and measure ads. You can control personalized advertising through your Google settings. No countdown data or searches you type on this site are stored by us.</p>
<h2>Third-party links</h2>
<p>Our pages link to third-party sites (including sites in our network). We are not responsible for their privacy practices.</p>
<h2>Contact</h2>
<p>Questions? Reach us via any site in our network footer.</p>
<h2>Advertising in more detail</h2>
<p>We serve advertising through Google AdSense. Google and its partners use cookies to build a profile of interests across the sites you visit, which is how interest-based advertising works generally on the web. None of it sees anything you do on a countdown page, because there is nothing to see: the countdowns are calculated on your device and no input is ever sent anywhere.</p>
<p>You can opt out of personalised advertising through Google's ad settings, or industry-wide through the Network Advertising Initiative and the Digital Advertising Alliance. Blocking third-party cookies in your browser achieves much the same, and every page here works without them.</p>
<h2>Your rights</h2>
<p>Because we hold no accounts and collect no personal information, there is normally nothing for us to produce, correct or delete — and we will tell you that plainly rather than going quiet. If you are in a jurisdiction with access or erasure rights and you want them exercised, reach us through any site in the network footer. If our answer does not satisfy you, your local data protection authority is the escalation route.</p>
<h2>What the countdowns do with your device</h2>
<p>Nothing beyond arithmetic. When a page loads, your browser works out the remaining time from the event date and the clock on your own machine. That is why the countdown stays accurate offline once the page has loaded, and why two people in different time zones see different numbers for the same event. No input is uploaded, no preference is stored beyond what your browser keeps for any web page, and closing the tab discards everything.</p>
<h2>Changes to this policy</h2>
<p>If the way the site handles data changes materially, this page changes with it. We are not going to start collecting personal information quietly — the whole point of a static site is that it does not need to.</p>
<h2>Children</h2>
<p>The site is general-audience and not directed at children. Since nothing is collected in the first place, there is nothing to collect from a child either.</p>'''),
 'disclosure': ('Advertising & Affiliate Disclosure', '''<h1>Advertising & Affiliate Disclosure</h1>
<p>daysuntil.bond is reader-supported. The site may display advertising (including Google AdSense) and may contain affiliate links — links to products or services from which we may earn a commission if you make a purchase, at no additional cost to you.</p>
<p>Astronomical data and countdown dates are never influenced by advertisers. Sponsored or affiliate content, where it appears, will be identifiable.</p>
<h2>How the commission actually works</h2>
<p>When you follow one of our links and then buy something, the seller's network records that the visit came from us and pays us a share. That share comes out of the seller's margin, not out of your price — you pay the same using our link as going directly, and occasionally less, because some links carry a discount the public listing does not.</p>
<p>If you would rather we earned nothing, type the seller's address in directly. The price is identical and we lose the commission, which is a perfectly reasonable preference.</p>
<h2>What commission cannot buy here</h2>
<p>Three things, stated plainly because they are the ones that matter. It cannot move a date: every countdown on this site is computed from the event's own data, and an advertiser has no mechanism and no route to change it. It cannot add or remove an event: the calendar is built from what we can verify. And it cannot change which countdown appears where — ordering follows the date.</p>
<p>Advertising pays for the site to exist. It does not get a vote on what it says.</p>
<h2>Who pays, and where</h2>
<p>Advertising on the site is served by Google AdSense, which fills the ad slots and pays us for the impressions. Separately, some pages carry affiliate links — mostly to products reviewed by sites in our network. Both are the same arrangement any ad-supported publisher has, and neither is hidden: the ad slots are labelled, and affiliate links on review pages carry a disclosure above them rather than in the footer where nobody reads it.</p>
<h2>Editorial independence, stated plainly</h2>
<p>No advertiser has reviewed or approved anything on this site, and none has been shown it in advance. Dates come from the event data, text is written by us, and the two do not meet. If a page ever carries sponsored placement, it will say so on the page itself rather than relying on you to infer it.</p>'''),
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
        if (e['dt'].date() - dt.date.today()).days > 0:
            for _k in VARIANT_KINDS:
                _vd = os.path.join(OUT, e['slug'], _k)
                os.makedirs(_vd, exist_ok=True)
                open(os.path.join(_vd, 'index.html'), 'w').write(_variant_body(_k, e, e['dt'], '../..'))
                urls.append(f'{SITE}/{e["slug"]}/{_k}/')
            _wd = os.path.join(OUT, 'when-is', e['slug'])
            os.makedirs(_wd, exist_ok=True)
            open(os.path.join(_wd, 'index.html'), 'w').write(when_is_page(e))
            urls.append(f'{SITE}/when-is/{e["slug"]}/')
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
