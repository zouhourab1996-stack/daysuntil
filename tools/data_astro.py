"""Compute astronomy events for daysuntil.bond from our own ephemeris engines.
Outputs data/astro_events.json — moons, solstices/equinoxes, planetary stations."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                      # moon_quick + planets_ephem live next to this file? no:
sys.path.insert(0, '/home/user/astro-seo/tools')  # reuse the battle-tested engines
from moon_quick import phases
from planets_ephem import geo_lon, stations, when_lon, fmt, U, show
from datetime import datetime, timezone

EV = []

# ---------- full & new moons, Oct 2026 – Dec 2028 (with blue/black moons) ----------
NOW = U(2026, 10, 2)
_seen = {}
for ts, name, lon in phases(U(2026, 10, 1), U(2028, 12, 31)):
    if ts < NOW:
        continue
    y, m = ts.year, ts.month
    kind = 'full' if name == 'Full Moon' else 'new'
    month_name = ts.strftime('%B')
    sign = lon.split()[-1]
    key = (kind, y, m)
    second = _seen.get(key, 0)
    _seen[key] = second + 1
    if second == 0:
        slug = f"{kind}-moon-{ts.strftime('%B-%Y').lower()}"
        title = f"{month_name} {ts.year} Full Moon" if kind == 'full' else f"{month_name} {ts.year} New Moon"
    else:
        kind2 = 'blue' if kind == 'full' else 'black'
        slug = f"{kind2}-moon-{ts.strftime('%B-%Y').lower()}"
        title = f"Blue Moon {month_name} {ts.year}" if kind == 'full' else f"Black Moon {month_name} {ts.year}"
    if slug.startswith('blue-') or slug.startswith('black-'):
        what = 'a second full moon in a single calendar month — the famous Blue Moon' if slug.startswith('blue-') else 'a second new moon in a single calendar month — a Black Moon, the new moon\'s answer to the Blue'
        desc = [
            f"{ts.strftime('%B %d, %Y at %H:%M')} UTC brings {what}. It happens only every two to three years, which is exactly why the phrase \'once in a blue moon\' means what it means.",
            f"This one peaks at {lon}. Nothing looks different from an ordinary full or new moon — the rarity is purely calendrical, and the counter above treats it like any other: with perfect accuracy.",
        ]
        facts = [["Peak (UTC)", ts.strftime('%B %d, %Y · %H:%M')], ["Zodiac position", lon], ["Rarity", "Every ~2.5 years"], ["Fun fact", "The next one is never far — the calendar always catches up"]]
        EV.append(dict(slug=slug, title=title, category='moon', kind='datetime',
                       utc=ts.strftime('%Y-%m-%dT%H:%M:00Z'), desc=desc, facts=facts,
                       tagline=f"Second {kind} moon of {month_name} {y}"))
        continue
    if kind == 'full':
        desc = [
            f"The {month_name} {y} full moon peaks at {ts.strftime('%H:%M')} UTC on {ts.strftime('%B %d, %Y')}, at {lon} in the tropical zodiac. Full moons always rise at sunset and set at sunrise, so the best viewing is any time the Moon is up that night — no equipment needed.",
            f"In astrology, the full moon in {sign} is considered the month's closing chapter: what began at the {sign} new moon six months earlier reaches fullness, and what is no longer working becomes impossible to ignore. Monthly full moons are the sky's built-in review meetings.",
        ]
        facts = [["Peak (UTC)", ts.strftime('%B %d, %Y · %H:%M')], ["Zodiac position", lon], ["Moon phase", "Full Moon (100% illumination)"], ["Cycle", "Lunation ~29.5 days"]]
    else:
        desc = [
            f"The {month_name} {y} new moon falls at {ts.strftime('%H:%M')} UTC on {ts.strftime('%B %d, %Y')}, at {lon}. The Moon sits between Earth and Sun, so its dark side faces us: no Moon visible for about a day on either side.",
            f"A new moon in {sign} is the traditional planting moment of the month — the sky's blank page. Anything begun in the days around it shares the sign's flavor, and the intentions you set now come to full light at the {sign} full moon six months later.",
        ]
        facts = [["Exact (UTC)", ts.strftime('%B %d, %Y · %H:%M')], ["Zodiac position", lon], ["Moon phase", "New Moon (0% illumination)"], ["Best viewing", "Moonless night — ideal for stars, meteors and the Milky Way"]]
    EV.append(dict(slug=slug, title=title, category='moon', kind='datetime',
                   utc=ts.strftime('%Y-%m-%dT%H:%M:00Z'), desc=desc, facts=facts,
                   tagline=f"{lon} · {ts.strftime('%H:%M')} UTC"))

# ---------- solstices & equinoxes 2026–2028 ----------
SEASONS = [(0, 'March', 'spring', 'March Equinox', 'the moment the Sun crosses the celestial equator heading north — autumn in the Southern Hemisphere'),
           (90, 'June', 'summer', 'June Solstice', 'the Sun at its northernmost point — summer begins in the north, winter in the south'),
           (180, 'September', 'fall', 'September Equinox', 'the Sun crosses the equator heading south — spring in the Southern Hemisphere'),
           (270, 'December', 'winter', 'December Solstice', 'the Sun at its southernmost point — winter begins in the north, summer in the south')]
MONTHN = {'March': 3, 'June': 6, 'September': 9, 'December': 12}
for year in (2026, 2027, 2028):
    for target, month, season, name, expl in SEASONS:
        ts = when_lon('sun', target, U(year, MONTHN[month], 1), U(year, 12, 31))
        if ts is None or ts.year != year or ts < NOW:
            continue
        slug = f"{season}-{year}"
        nice = {'spring': 'First Day of Spring', 'summer': 'First Day of Summer (Northern Hemisphere)',
                'fall': 'First Day of Fall', 'winter': 'First Day of Winter (Northern Hemisphere)'}[season]
        title = f"{nice} {ts.year}"
        desc = [
            f"The {name.lower()} of {ts.year} falls on {ts.strftime('%B %d, %Y')} at {ts.strftime('%H:%M')} UTC — the astronomical start of {season} in the Northern Hemisphere ({'autumn' if season=='spring' else 'winter' if season=='summer' else 'spring' if season=='fall' else 'summer'} below the equator).",
            f"Astronomically, this is {expl}. It is also the day the tide of daylight turns: after the {month} solstice the change is barely minutes per week, then accelerates — the reason the weeks after a solstice feel darker (or lighter) faster than the solstice day itself.",
        ]
        EV.append(dict(slug=slug, title=title, category='seasons', kind='datetime',
                       utc=ts.strftime('%Y-%m-%dT%H:%M:00Z'), desc=desc,
                       facts=[["Exact moment (UTC)", ts.strftime('%B %d, %Y · %H:%M')], ["Event", name], ["Hemisphere note", "Seasons flip in the Southern Hemisphere"]],
                       tagline=f"{ts.strftime('%B %d')} · {ts.strftime('%H:%M')} UTC"))

# ---------- planetary stations (our exact computations) ----------
GUIDE = {'venus': '/blog/venus-retrograde-2026/', 'mercury': '/blog/mercury-retrograde-2026/',
         'mars': '/blog/mars-retrograde-2027/', 'jupiter': '/blog/jupiter-retrograde-2026/'}
NICE = {'mercury': 'Mercury', 'venus': 'Venus', 'mars': 'Mars', 'jupiter': 'Jupiter',
        'saturn': 'Saturn', 'uranus': 'Uranus', 'neptune': 'Neptune', 'pluto': 'Pluto'}
WHAT = {
 'mercury': "Mercury retrograde is the famous three-week review of communication, travel and contracts that happens three or four times a year.",
 'venus': "Venus retrograde is the rare six-week audit of love, money and values — it comes only every 18 months.",
 'mars': "Mars retrograde is the two-year energy audit: drive, desire, temper and stamina all get re-priced. It happens roughly every 26 months.",
 'jupiter': "Jupiter retrograde is the four-month review of growth, beliefs and plans — about a third of every year, every year.",
 'saturn': "Saturn retrograde is the yearly four-and-a-half-month stress test of commitments, structures and responsibilities.",
 'uranus': "Uranus retrograde turns the planet of disruption and freedom inward for about five months each year — rebellion becomes review.",
 'neptune': "Neptune retrograde is the annual five-month dissolve of illusions — dreams and deceptions both get a second look.",
 'pluto': "Pluto retrograde is the yearly five-month descent into power, control and what needs to be transformed from the roots.",
}
for body in ('mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'):
    for ts, lon, kind in stations(body, U(2026, 10, 1), U(2028, 12, 31)):
        if ts < NOW:
            continue
        lon = fmt(lon)  # numeric longitude -> '20\u00b059\u2032 Scorpio'
        word = 'retrograde' if kind == 'Rx' else 'direct'
        gerund = 'Retrograde' if kind == 'Rx' else 'Direct'
        slug = f"{body}-{word}-{ts.strftime('%B-%Y').lower()}"
        title = f"{NICE[body]} {gerund} {ts.strftime('%B %Y')}"
        link = f" Full guide with a free chart checker: <a href=\"https://prophetic.pw{GUIDE[body]}\" target=\"_blank\" rel=\"noopener\">the {NICE[body]} retrograde guide on Prophetic</a>." if body in GUIDE else ""
        desc = [
            f"{NICE[body]} stations {word} on {ts.strftime('%B %d, %Y')} at {ts.strftime('%H:%M')} UTC, at {lon} — computed to the minute with our own Keplerian ephemeris.",
            f"{WHAT[body]} The station is the turning point itself: the day the planet's apparent motion reaches zero before reversing. In tradition, days around a station carry the event's themes most intensely — decisions made at a station are said to set the tone for the whole season that follows.{link}",
        ]
        EV.append(dict(slug=slug, title=title, category='planets', kind='datetime',
                       utc=ts.strftime('%Y-%m-%dT%H:%M:00Z'), desc=desc,
                       facts=[["Station moment (UTC)", ts.strftime('%B %d, %Y · %H:%M')], ["Zodiac position", lon], ["Direction", f"Turning {kind}"], ["Duration of phase", f"~{'3 weeks' if body=='mercury' else '6 weeks' if body=='venus' else '11 weeks' if body=='mars' else '4 months' if body=='jupiter' else '4.5 months' if body=='saturn' else '5 months'}"]],
                       tagline=f"{lon} · {ts.strftime('%H:%M')} UTC"))

json.dump(EV, open(os.path.join(HERE, '..', 'data', 'astro_events.json'), 'w'), indent=1)
fulls = sum(1 for e in EV if e['slug'].startswith('full'))
news = sum(1 for e in EV if e['slug'].startswith('new'))
seasons = sum(1 for e in EV if e['category'] == 'seasons')
stations_n = sum(1 for e in EV if e['category'] == 'planets')
print(f"astro events: {len(EV)}  (full moons {fulls}, new moons {news}, seasons {seasons}, stations {stations_n})")
for e in EV[:3] + EV[-3:]:
    print(' ', e['slug'], e.get('utc'))
