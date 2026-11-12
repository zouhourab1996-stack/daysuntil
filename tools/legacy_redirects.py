"""Redirect stubs for guessable / legacy URLs that Google reports as 404.

GSC "Not found (404)" on daysuntil.bond listed URLs such as /days-until-christmas
that never existed on this build. GitHub Pages has no server redirects, so each
alias gets a tiny HTML page with meta refresh 0 + rel=canonical + location.replace
to the current next-occurrence page. Stubs are NOT added to the sitemap and are
rewritten on every build, so their targets roll forward to the next year.

Run standalone (python3 tools/legacy_redirects.py) or from generate_site.py.
"""
import os, re, json, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'docs')
SITE = 'https://daysuntil.bond'

# Friendly names people (and old links) use -> event base slug
EXTRA_ALIASES = {
    'christmas': 'christmas-day',
    'thanksgiving': 'us-thanksgiving',
    'new-years': 'new-year',
    'new-years-eve': 'new-year',
    'nye': 'new-year',
    '4th-of-july': 'us-independence-day',
    'fourth-of-july': 'us-independence-day',
    'independence-day': 'us-independence-day',
    'valentines': 'valentines-day',
    'gta-6': 'gta-6-release',
    'gta6': 'gta-6-release',
    'super-bowl': 'super-bowl-lxi',
    'olympics': 'la28-olympics-opening',
    'mothers-day': 'mothers-day',
    'fathers-day': 'fathers-day',
}


def _base(slug):
    return re.sub(r'-(\d{4})$', '', slug)


def _event_dt(e):
    if e['kind'] == 'datetime':
        return dt.datetime.fromisoformat(e['utc'].replace('Z', '')).replace(tzinfo=dt.timezone.utc)
    y, m, d = map(int, e['date'].split('-'))
    return dt.datetime(y, m, d, tzinfo=dt.timezone.utc)


def next_of():
    events = []
    for f in ('astro_events.json', 'fixed_events.json'):
        events += json.load(open(os.path.join(DATA, f)))
    now = dt.datetime.now(dt.timezone.utc)
    groups = {}
    for e in events:
        groups.setdefault(_base(e['slug']), []).append(e)
    out = {}
    for b, items in groups.items():
        fut = sorted([x for x in items if _event_dt(x) >= now], key=_event_dt)
        out[b] = (fut[0] if fut else max(items, key=_event_dt))['slug']
    return out


def stub(target_url):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Redirecting…</title>
<link rel="canonical" href="{target_url}">
<meta http-equiv="refresh" content="0; url={target_url}">
<script>location.replace("{target_url}")</script>
</head><body><p>This countdown moved to <a href="{target_url}">{target_url}</a>.</p></body></html>
'''


def aliases():
    nxt = next_of()
    pairs = {}
    for base, slug in nxt.items():
        pairs[f'days-until-{base}'] = slug
        pairs[f'how-many-days-until-{base}'] = slug
        if base != slug:            # year-suffixed series: bare base name too
            pairs[base] = slug
    for alias, base in EXTRA_ALIASES.items():
        if base in nxt:
            pairs[f'days-until-{alias}'] = nxt[base]
            pairs[f'how-many-days-until-{alias}'] = nxt[base]
            pairs.setdefault(alias, nxt[base])
    return pairs


def write_stubs(out=OUT):
    n = 0
    for alias, slug in sorted(aliases().items()):
        d = os.path.join(out, alias)
        idx = os.path.join(d, 'index.html')
        # never overwrite a real page (hand-written guides, categories, events)
        if os.path.exists(idx) and 'http-equiv="refresh"' not in open(idx, errors='ignore').read():
            continue
        if alias == slug:
            continue
        os.makedirs(d, exist_ok=True)
        open(idx, 'w').write(stub(f'{SITE}/{slug}/'))
        n += 1
    print(f'legacy redirects: {n} stub pages written')
    return n


if __name__ == '__main__':
    write_stubs()
