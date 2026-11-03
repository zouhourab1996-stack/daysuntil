"""Fixed & verified events for daysuntil.bond -> data/fixed_events.json
All dates either computed programmatically or verified against sources (Oct 2026)."""
import os, json, datetime as dt, re

D = dt.date
EV = []

def slugify(s, y):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9-]', '', s.lower().replace(' ', '-').replace("'", ''))) + f"-{y}"

def add(slug, title, category, date, desc, facts=None, tagline=None, kind='date'):
    EV.append(dict(slug=slug, title=title, category=category, kind=kind,
                   date=date.isoformat(), desc=desc, facts=facts or [], tagline=tagline or ''))

def wk(y, m, weekday, n):
    """n-th weekday (0=Mon) of month; n=-1 = last."""
    d = D(y, m, 1) + dt.timedelta(days=(weekday - D(y, m, 1).weekday()) % 7)
    if n > 0:
        return d + dt.timedelta(days=(n - 1) * 7)
    while (d + dt.timedelta(days=7)).month == m:
        d += dt.timedelta(days=7)
    return d

def easter(y):
    a = y % 19; b, c = divmod(y, 100); d, e = divmod(b, 4)
    f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4); l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return D(y, month, day + 1)

# ---------------- fixed-date observances (name, month, day, blurb) ----------------
FIXED = [
 ("New Year's Day", 1, 1, "The world's most celebrated reset: January 1 kicks off the Gregorian calendar year with fireworks at midnight, resolutions, and — for about a week — genuinely hopeful gym attendance."),
 ("Orthodox Christmas", 1, 7, "Christmas Day for Orthodox churches that follow the Julian calendar — celebrated by hundreds of millions across Eastern Europe, the Balkans, Russia, Egypt and Ethiopia."),
 ("Valentine's Day", 2, 14, "The feast day of love: cards, flowers, dinner reservations and the year's most-watched countdown by anyone in a relationship. Roughly a billion valentines are sent annually."),
 ("Pi Day", 3, 14, "March 14 — 3/14 — is the world's favorite mathematical holiday, celebrating the circle constant π ≈ 3.14159. Traditionally observed with pie, at 1:59 PM if you're serious about it."),
 ("April Fools' Day", 4, 1, "The one day the internet becomes 40% less trustworthy. Pranks, fake product launches and hoaxes are the whole point — verified news published on April 1 is the ultimate test of media literacy."),
 ("Earth Day", 4, 22, "The world's largest environmental observance, marked by more than a billion people in 190+ countries since 1970 — a day of cleanups, tree plantings and climate action."),
 ("Star Wars Day", 5, 4, "May the Fourth be with you: the fan-created holiday that became an official one, celebrated with marathons, merchandise sales and groan-worthy puns across the galaxy."),
 ("Cinco de Mayo", 5, 5, "May 5 commemorates Mexico's 1862 victory at the Battle of Puebla — a modest holiday in Mexico, an enormous celebration of Mexican culture in the United States."),
 ("Juneteenth", 6, 19, "America's newest federal holiday: June 19, 1865 was the day the last enslaved people in Texas learned they were free — now celebrated nationwide as a day of Black history, family and freedom."),
 ("US Independence Day", 7, 4, "The Fourth of July: fireworks, cookouts and the Star-Spangled Banner, marking the 1776 adoption of the Declaration of Independence."),
 ("Bastille Day", 7, 14, "France's national day: July 14, 1789, the storming of the Bastille and the start of the French Revolution — celebrated with the oldest and largest military parade in Europe on the Champs-Élysées."),
 ("International Dog Day", 8, 26, "Founded in 2004 to celebrate all dogs and encourage adoption — the internet's highest-engagement holiday, and a very good excuse for a long walk."),
 ("World Teachers' Day", 10, 5, "UNESCO's annual tribute to teachers worldwide, held on October 5 since 1994 — the day students and parents thank the people who do the most underrated job in the world."),
 ("Halloween", 10, 31, "All Hallows' Eve: costumes, candy, haunted houses and the year's spookiest full-moon energy. The second-largest commercial holiday in the US after Christmas, with roots going back to the Celtic festival of Samhain."),
 ("All Saints' Day", 11, 1, "The Christian feast honoring all saints, known in Mexico as the first day of Día de los Muertos — when the souls of departed children are believed to return for one night."),
 ("Day of the Dead", 11, 2, "Día de los Muertos: Mexico's vibrant two-day reunion with the departed — ofrendas, marigolds, sugar skulls and cemetery vigils. UNESCO-recognized intangible heritage of humanity."),
 ("Guy Fawkes Night", 11, 5, "Remember, remember the fifth of November: bonfires and fireworks across Britain commemorating the failed 1605 Gunpowder Plot — an anniversary that inspired a famous mask and a famous film."),
 ("Veterans Day", 11, 11, "November 11 honors military veterans — armistice day of World War I, at the eleventh hour of the eleventh day of the eleventh month. (Commonwealth countries mark it as Remembrance Day.)"),
 ("International Men's Day", 11, 19, "November 19 celebrates men's positive contributions to family and community and spotlights men's health and wellbeing — observed in 80+ countries."),
 ("World Kindness Day", 11, 13, "November 13: a day to deliberately choose kindness — small acts, big ripples. Launched in 1998 by the World Kindness Movement, now observed in 30+ countries."),
 ("Human Rights Day", 12, 10, "December 10 marks the 1948 adoption of the Universal Declaration of Human Rights — the most translated document in the world."),
 ("Christmas Eve", 12, 24, "The night before Christmas: last-minute wrapping, candlelight services, and radar tracking of a certain sleigh. In many European and Latin cultures, this — not the 25th — is the main celebration."),
 ("Christmas Day", 12, 25, "The big one: the Christian celebration of the nativity and the world's most widely observed holiday — two billion people, one tree, and an economy the size of a small nation resting on what's under it."),
 ("Boxing Day", 12, 26, "December 26: a public holiday across the UK, Canada, Australia and much of the Commonwealth — historically the day boxes of gifts went to servants and the poor, now better known for football fixtures and the year's biggest sales."),
 ("Kwanzaa", 12, 26, "The seven-day African-American cultural celebration founded in 1966, honoring seven principles from Umoja (unity) to Imani (faith), one candle lit per night."),
 ("Festivus", 12, 23, "For the rest of us: the fictional holiday from Seinfeld (1997) that became a real anti-holiday — featuring the airing of grievances and feats of strength around an unadorned aluminum pole."),
 ("International Women's Day", 3, 8, "March 8: a global day celebrating women's achievements and campaigning for equality, with roots in early-20th-century labor movements — an official holiday in many countries."),
 ("World Environment Day", 6, 5, "The United Nations' principal vehicle for environmental advocacy, held every June 5 since 1974 — the planet's biggest day for nature, hosted by a different country each year."),
 ("International Coffee Day", 10, 1, "October 1: the day the world agrees that its collective productivity is a group hallucination funded by caffeine — celebrated with (what else) a second cup."),
]
FIXED = [f for f in FIXED if f[0] != "A holiday that doesn't exist in my data — placeholder to remove"]

YEARS = (2026, 2027, 2028)
TODAY = D(2026, 10, 2)
for name, m, d, blurb in FIXED:
    for y in YEARS:
        date = D(y, m, d)
        if date < TODAY:
            continue
        year_s = str(y)
        slug = slugify(name, y)
        weekday = date.strftime('%A')
        desc = [f"{name} {year_s} falls on {weekday}, {date.strftime('%B %-d, %Y')}. {blurb}",
                f"The live counter above counts down the days, hours and minutes to {name} {y} in your local time zone, and switches to a 'days since' counter once it arrives."]
        add(slug, f"{name} {y}", 'holidays', date, desc,
            facts=[["Date", f"{weekday}, {date.strftime('%B %-d, %Y')}"], ["Category", "Holiday / observance"]],
            tagline=f"{weekday}, {date.strftime('%B %-d')}")

# ---------------- computed-move holidays ----------------
def add_computed(label, y, date, blurb, tagline_extra='', cat='holidays'):
    if date < TODAY:
        return
    slug = slugify(label, y)
    weekday = date.strftime('%A')
    desc = [f"{label} {y} falls on {weekday}, {date.strftime('%B %-d, %Y')}. {blurb}",
            "The live counter above updates every second and automatically switches to 'days since' once the day arrives."]
    add(slug, f"{Label(label)} {y}", cat, date, desc,
        facts=[["Date", f"{weekday}, {date.strftime('%B %-d, %Y')}"], ["Category", "Holiday / observance"]],
        tagline=f"{weekday}, {date.strftime('%B %-d')}{tagline_extra}")

def Label(s):
    return ' '.join(w if (w.isupper() or len(w) <= 3 and w.upper() == w) else (w.capitalize() if w.lower() not in ('of', 'the') else w.lower()) for w in s.split())

for y in YEARS:
    e = easter(y); add_computed("Easter", y, e, "The most important feast in Christianity, celebrating the resurrection — eggs, bunnies and spring festivals came along later. Easter is set by the first Sunday after the first full moon of spring, which is why it moves every year.")
    add_computed("Good Friday", y, e - dt.timedelta(days=2), "The solemn Christian commemoration of the crucifixion, two days before Easter — a public holiday in more than 100 countries.")
    add_computed("Mardi Gras", y, e - dt.timedelta(days=47), "Fat Tuesday: the last hurrah before Lent, celebrated biggest in New Orleans, Rio de Janeiro and Venice — beads, masks, king cakes and impressive self-restraint starting the next morning.")
    add_computed("Mother's Day", y, wk(y, 5, 6, 2), "The second Sunday of May in the US and dozens of other countries: the one day a year brunch reservations become a competitive sport. (The UK, Ireland and Nigeria mark Mothering Sunday on a different date.)", ' (US)')
    add_computed("Father's Day", y, wk(y, 6, 6, 3), "The third Sunday of June: ties, tools, barbecues and long phone calls. Father's Day was founded in 1910 and took 62 years to become a US national holiday.")
    add_computed("Memorial Day", y, wk(y, 5, 0, -1), "The last Monday of May: America's day of remembrance for fallen service members, and the unofficial start of summer.")
    add_computed("Labor Day", y, wk(y, 9, 0, 1), "The first Monday of September: the US and Canada's tribute to workers — parades, last-of-summer barbecues, and the traditional end of white-pants season.")
    add_computed("US Thanksgiving", y, wk(y, 11, 3, 4), "The fourth Thursday of November: turkey, gratitude, football and complicated family logistics — America's most-traveled holiday week.")
    bf = wk(y, 11, 3, 4) + dt.timedelta(days=1)
    add_computed("Black Friday", y, bf, "The day after US Thanksgiving and one of the biggest shopping events on Earth — doorbuster deals, long lines (increasingly online), and the unofficial kickoff of the Christmas shopping season.")
    add_computed("Cyber Monday", y, bf + dt.timedelta(days=3), "The Monday after Black Friday, invented in 2005 as the online answer to in-store doorbusters — now the year's single biggest e-commerce day in many countries.")
    add_computed("MLK Day", y, wk(y, 1, 0, 3), "The third Monday of January, honoring Dr. Martin Luther King Jr. around his January 15 birthday — the only federal holiday designated a national day of service.")
    add_computed("Presidents' Day", y, wk(y, 2, 0, 3), "The third Monday of February, honoring US presidents — born from Washington's Birthday and now best known for mattress sales and a long weekend.")
    add_computed("Canadian Thanksgiving", y, wk(y, 10, 0, 2), "The second Monday of October: Canada's harvest feast, which predates the American version by decades and lands while the maple leaves are at their best.")
    add_computed("Daylight Saving Ends (US)", y, wk(y, 11, 6, 1), "The first Sunday of November at 2:00 AM: clocks fall back, everyone gets one glorious extra hour of sleep, and evening commutes go dark. (Most of Europe changed a week earlier; Arizona and Hawaii sit it out entirely.)")
    add_computed("Daylight Saving Starts (US)", y, wk(y, 3, 6, 2), "The second Sunday of March at 2:00 AM: clocks spring forward and the internet fills with takes about sleep science — the price of summer evening light.")

# ---------------- New Year countdowns ----------------
for y in (2027, 2028, 2029):
    date = D(y, 1, 1)
    if date < TODAY:
        continue
    add(f"new-year-{y}", f"New Year {y}", 'holidays', date,
        [f"January 1, {y}: the fireworks, the countdown, the resolutions. New Year's Eve is the most-watched countdown on the planet — every time zone on Earth counts down to its own midnight, 26 times across one rotating day.",
         "The counter above runs to your local midnight on January 1 — the moment {y} begins where you are.".replace('{y}', str(y))],
        facts=[["Date", f"January 1, {y}"], ["Countdowns worldwide", "26 time-zone midnights"], ["Followed by", "the year's least productive morning"]],
        tagline="The original countdown")

# ---------------- Friday the 13th ----------------
m = D(2026, 10, 1)
while m < D(2029, 1, 1):
    d13 = D(m.year, m.month, 13)
    if d13.weekday() == 4 and d13 >= TODAY:
        add(f"friday-the-13th-{d13.strftime('%B-%Y').lower()}", f"Friday the 13th {d13.strftime('%B %Y')}", 'holidays', d13,
            [f"Friday the 13th {d13.strftime('%B %Y')} falls on a {d13.strftime('%A')}, {d13.strftime('%B %-d, %Y')}. The unluckiest date on the Western calendar: paraskevidekatriaphobia is the genuine word for fear of it.",
             "Statistically, Friday the 13th happens one to three times a year. The counter above tells you exactly how long the superstition industry has to prepare."],
            tagline="Watch for black cats")
    m = D(m.year + (m.month == 12), (m.month % 12) + 1, 1)

# ---------------- cultural / lunar-calendar dates ----------------
CULT = [
 ("chinese-new-year-2027", "Chinese New Year 2027", D(2027, 2, 6), "Lunar New Year 2027 welcomes the Year of the Goat (Fire Goat): the world's largest annual human migration as billions travel home for reunion dinners, red envelopes and fifteen days of festivities."),
 ("chinese-new-year-2028", "Chinese New Year 2028", D(2028, 1, 26), "Lunar New Year 2028 welcomes the Year of the Monkey: spring festival travel, lanterns, firecrackers and the biggest annual celebration on Earth."),
 ("diwali-2026", "Diwali 2026", D(2026, 11, 8), "The five-day festival of lights, celebrated by over a billion Hindus, Jains, Sikhs and Buddhists: lamps, sweets, fireworks and the victory of light over darkness."),
 ("diwali-2027", "Diwali 2027", D(2027, 10, 28), "The festival of lights returns: five days of diyas, rangoli and family feasts marking the triumph of light over darkness."),
 ("ramadan-2027", "Ramadan 2027 (expected)", D(2027, 2, 8), "The month of fasting, prayer and community for the world's ~2 billion Muslims — from dawn to sunset without food or water, broken daily with the iftar meal. Dates follow the lunar calendar and moon sighting, so the start may shift by a day."),
 ("eid-al-fitr-2027", "Eid al-Fitr 2027 (expected)", D(2027, 3, 10), "The festival of breaking the fast: three days of feasts, gifts and prayers marking the end of Ramadan — one of the two biggest holidays in Islam. Exact date depends on moon sighting."),
 ("eid-al-adha-2027", "Eid al-Adha 2027 (expected)", D(2027, 5, 17), "The festival of sacrifice, honoring Abraham's willingness to sacrifice his son: Qurbani (animal sacrifice), charity to the poor, and family gatherings. Exact date depends on moon sighting."),
 ("1111-portal-2026", "The 11/11 Portal 2026", D(2026, 11, 11), "November 11 — 11/11 — is the internet's favorite manifestation day: a numerological 'gateway' beloved by angel-number communities, and in 2026 it opens with both Venus and Mercury retrograde, stationing direct within 48 hours after it. Full analysis on <a href=\"https://prophetic.pw/blog/1111-portal-2026/\" target=\"_blank\" rel=\"noopener\">Prophetic's 11/11 portal guide</a>."),
 ("leap-day-2028", "Leap Day 2028", D(2028, 2, 29), "February 29 — the day that only exists every four years. Leap years keep the calendar aligned with Earth's 365.2422-day orbit. Leaplings (people born on Feb 29) get a real birthday at last; everyone else gets an extra day of Q1."),
]
for slug, title, date, blurb in CULT:
    if date < TODAY:
        continue
    add(slug, title, 'holidays', date, [f"{title} falls on {date.strftime('%A, %B %-d, %Y')}. {blurb}",
        "The live counter above ticks down to the day in your time zone."],
        facts=[["Date", date.strftime('%A, %B %-d, %Y')], ["Category", "Cultural observance"]],
        tagline=date.strftime('%B %-d, %Y'))

# ---------------- eclipses (verified) ----------------
ECL = [
 ("total-solar-eclipse-august-2026", "Total Solar Eclipse August 12, 2026", D(2026, 8, 12),
  "The first total solar eclipse anywhere on Earth since April 2024 — and the first visible from mainland Europe since 1999. Totality sweeps Greenland, Iceland and northern Spain; most of Europe and northeastern North America see a deep partial eclipse.",
  "Total eclipse · Iceland & Spain · first in Europe since 1999"),
 ("partial-lunar-eclipse-august-2026", "Partial Lunar Eclipse August 28, 2026", D(2026, 8, 28),
  "The Moon slips partway into Earth's shadow, visible across most of North America, South America, Europe and Africa — a warm-up act for the total solar eclipse two weeks earlier.",
  "Visible from the Americas, Europe & Africa"),
 ("annular-solar-eclipse-february-2027", "Annular Solar Eclipse February 6, 2027", D(2027, 2, 6),
  "A 'ring of fire' annular eclipse crossing Chile, Argentina, Uruguay and Brazil, then the Atlantic to West Africa (Ghana, Togo, Benin, Nigeria) at sunset.",
  "Ring of fire · South America & West Africa"),
 ("penumbral-lunar-eclipse-february-2027", "Penumbral Lunar Eclipse February 20, 2027", D(2027, 2, 20),
  "The full Moon at 2° Virgo glides through Earth's outer shadow — a subtle dimming rather than a red eclipse, with retrograde Mars sitting under two degrees away (we computed 0°14′ separation). Visible from the Americas, Europe and Africa.",
  "Subtle dimming · Moon beside retrograde Mars"),
 ("penumbral-lunar-eclipse-july-2027", "Penumbral Lunar Eclipse July 18, 2027", D(2027, 7, 18),
  "A faint penumbral eclipse of the full Moon, best from the eastern Americas, Europe and Africa — two weeks before the main event of the decade.",
  "Two weeks before the big one"),
 ("total-solar-eclipse-august-2027", "Total Solar Eclipse August 2, 2027", D(2027, 8, 2),
  "The eclipse of the century: up to 6 minutes 23 seconds of totality — the longest over land until 2114 — crossing southern Spain, Morocco, Algeria, TUNISIA, Libya, Egypt (Luxor gets 6+ minutes) and Saudi Arabia. If you've ever wanted to chase a total eclipse, this is the one to chase.",
  "6m23s totality · Spain → North Africa (Tunisia!) → Egypt"),
 ("penumbral-lunar-eclipse-august-2027", "Penumbral Lunar Eclipse August 17, 2027", D(2027, 8, 17),
  "A quiet penumbral eclipse two weeks after the August 2 total solar eclipse, visible from the Pacific, the Americas, Europe and Africa.",
  "Visible across four continents"),
 ("partial-lunar-eclipse-january-2028", "Partial Lunar Eclipse January 12, 2028", D(2028, 1, 12),
  "The year's first eclipse: part of the Moon enters Earth's dark umbral shadow, visible from the Americas, Europe and Africa.",
  "Visible from the Americas, Europe & Africa"),
 ("annular-solar-eclipse-january-2028", "Annular Solar Eclipse January 26, 2028", D(2028, 1, 26),
  "A ring-of-fire eclipse crossing the Galápagos, the Amazon, the Atlantic and southern Spain — one for the travel-mapped eclipse chaser.",
  "Ring of fire · Galápagos, Amazon & Spain"),
 ("partial-solar-eclipse-july-2028", "Partial Solar Eclipse July 6, 2028", D(2028, 7, 6),
  "A partial solar eclipse visible from the southern Pacific, southern South America and Antarctica.",
  "Southern skies"),
 ("total-lunar-eclipse-july-2028", "Total Lunar Eclipse July 21, 2028", D(2028, 7, 21),
  "The Moon turns deep red as it dives fully into Earth's shadow — a blood moon visible across much of Asia, Australia and the Americas.",
  "Blood moon · Asia, Australia & the Americas"),
]
for slug, title, date, blurb, tag in ECL:
    if date < TODAY:
        continue
    add(slug, title, 'eclipses', date, [blurb,
        "Eclipse timing depends on your location — the counter above runs to the calendar date worldwide. Never look at the Sun without certified eclipse glasses; the Moon's red glow during a total lunar eclipse is completely safe to watch."],
        facts=[["Date", date.strftime('%A, %B %-d, %Y')], ["Type", title.split(' ', 1)[0].title() + ' eclipse'], ["Safety", "Solar: certified glasses only · Lunar: safe to watch"]],
        tagline=tag)

# ---------------- meteor showers ----------------
SHOWERS = [
 ("quadrantids", "Quadrantids", 1, 3, "The year's first major meteor shower — short, sharp and often stormy, with peak rates of 60–200 meteors per hour compressed into just six hours."),
 ("lyrids", "Lyrids", 4, 22, "April's classic: a shower with 2,700 years of recorded observations, known for occasional bright fireballs. Peak ~18 meteors/hour under dark skies."),
 ("eta-aquariids", "Eta Aquariids", 5, 5, "Debris from Halley's Comet burning up above the southern hemisphere's autumn skies — fast, bright meteors with long trains."),
 ("perseids", "Perseids", 8, 12, "The people's meteor shower: warm August nights, 50–100 meteors per hour at peak, and more photogenic fireballs than any other annual shower. Halley's comet's bigger, better-known sibling stream."),
 ("orionids", "Orionids", 10, 21, "Halley's Comet's second annual gift: fast meteors radiating from Orion's club in the pre-dawn hours of late October."),
 ("leonids", "Leonids", 11, 17, "The legendary storm shower: usually 10–15 meteors per hour, but every ~33 years it erupts into thousands per hour (last storm: 2001). Radiates from the Lion."),
 ("geminids", "Geminids", 12, 13, "The best meteor shower of the year, no contest: 120–150 bright, slow, colorful meteors per hour at peak from asteroid 3200 Phaethon — and it happens in December, so dress like it."),
 ("ursids", "Ursids", 12, 22, "The year's quiet closer: a modest shower (5–10 per hour) radiating from Ursa Minor, occasionally surprising with outbursts — for the dedicated, on the longest nights."),
]
for slugbase, name, m, d, blurb in SHOWERS:
    for y in YEARS:
        date = D(y, m, d)
        if date < TODAY:
            continue
        add(f"{slugbase}-{y}", f"{name} {y}", 'meteor-showers', date,
            [f"The {name} meteor shower peaks on the night of {date.strftime('%B %-d, %Y')} ({date.strftime('%B %-d')}/{(date+dt.timedelta(days=1)).strftime('%-d')}). {blurb}",
             "Best practice for any meteor shower: dark sky, no telescope, eyes adjusted for 30 minutes, look halfway up toward the radiant's constellation. The counter above runs to the peak night; meteors are visible several nights either side."],
            facts=[["Peak night", date.strftime('%B %-d–') + (date+dt.timedelta(days=1)).strftime('%-d, %Y')], ["Best viewing", "After midnight to pre-dawn"], ["Equipment", "None — naked eye only"]],
            tagline="Peak night " + date.strftime('%B %-d'))

# ---------------- movies / gaming / sports (verified) ----------------
MEDIA = [
 ("gta-6-release", "GTA 6 Release Date", D(2026, 11, 19), 'gaming',
  "Grand Theft Auto VI launches Thursday, November 19, 2026 on PlayStation 5 and Xbox Series X|S — after two delays (2025 → May 26, 2026 → November 19, 2026), Rockstar and Take-Two have held the date. Standard Edition $79.99, digital pre-loading from November 12; no PC date announced yet.",
  "The most anticipated entertainment release in history — by pre-orders, it is already the biggest game ever, and the entire games industry moved its Q4 releases to get out of its way."),
 ("avengers-doomsday", "Avengers: Doomsday", D(2026, 12, 18), 'movies',
  "The MCU's biggest assembly ever — Avengers, X-Men, Fantastic Four and Thunderbolts against Robert Downey Jr.'s Doctor Doom — directed by the Russo brothers, in theaters Friday, December 18, 2026 (165 minutes).",
  "It shares its release date with Dune: Part Three — a box-office showdown the internet has already named 'Dunesday'."),
 ("dune-part-three", "Dune: Part Three", D(2026, 12, 18), 'movies',
  "Denis Villeneuve's adaptation of Dune Messiah concludes the trilogy, in theaters and IMAX Friday, December 18, 2026 — with a three-week IMAX exclusivity window over Avengers: Doomsday.",
  "Same day as Avengers: Doomsday. One weekend, two event films, one very full cinema."),
 ("star-wars-starfighter", "Star Wars: Starfighter", D(2027, 5, 28), 'movies',
  "The next theatrical Star Wars film — directed by Shawn Levy, starring Ryan Gosling — a standalone adventure set five years after The Rise of Skywalker. In theaters May 28, 2027.",
  "The first new Star Wars movie in theaters since 2019."),
 ("shrek-5", "Shrek 5", D(2027, 6, 30), 'movies',
  "The swamp is back: Shrek, Donkey and Fiona return in the first mainline Shrek film since 2010, with the original voice cast. In US theaters June 30, 2027.",
  "Somebody once told him it'd be 17 years between sequels."),
 ("avengers-secret-wars", "Avengers: Secret Wars", D(2027, 12, 17), 'movies',
  "The finale of the Multiverse Saga and the film Avengers: Doomsday builds toward — in theaters December 17, 2027.",
  "The MCU's endgame for this era, one year after Doomsday."),
 ("avatar-4", "Avatar 4", D(2029, 12, 21), 'movies',
  "James Cameron's next chapter of Pandora, currently scheduled for December 21, 2029 — because Cameron plans in decades, not release windows.",
  "The longest-range countdown on this site."),
 ("super-bowl-lxi", "Super Bowl LXI (2027)", D(2027, 2, 14), 'sports',
  "Super Bowl LXI — the first Super Bowl ever scheduled on Valentine's Day — kicks off Sunday, February 14, 2027 at ~6:30 PM ET at SoFi Stadium, Inglewood, on ESPN and ABC.",
  "Championship Sunday shares a calendar with cupid: flowers AND a 70-inch TV."),
 ("la28-olympics-opening", "LA28 Olympics Opening Ceremony", D(2028, 7, 14), 'sports',
  "The Summer Games return to Los Angeles for the first time since 1984, opening July 14, 2028 — with competitions spread across LA's most iconic venues, flag football making its Olympic debut, and SoFi Stadium hosting the opening ceremony.",
  "LA hosts the world: first Summer Games in the US since Atlanta 1996."),
 ("la28-olympics-closing", "LA28 Olympics Closing Ceremony", D(2028, 7, 30), 'sports',
  "Seventeen days of competition end July 30, 2028 with the closing ceremony — the handover to Brisbane 2032, and the end of the last countdown of the Games.",
  "The final day of LA28."),
]
for slug, title, date, cat, blurb, hook in MEDIA:
    add(slug, title, cat, date, [blurb, hook + " The live counter above runs to the release/event date worldwide (local time zones may shift availability by hours)."],
        facts=[["Date", date.strftime('%A, %B %-d, %Y')], ["Days away", "Live counter above"]],
        tagline=date.strftime('%A, %B %-d, %Y'))

os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'), exist_ok=True)
json.dump(EV, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'fixed_events.json'), 'w'), indent=1)
print(f"fixed events: {len(EV)}")
cats = {}
for e in EV:
    cats[e['category']] = cats.get(e['category'], 0) + 1
print(cats)
