"""Stand-alone articles for daysuntil.bond.

Kept out of generate_site.py on purpose: each article is a function that returns a complete HTML page,
so a rebuild regenerates it (instead of silently dropping a hand-written file) and its numbers refresh
with the build date. The generator passes in its own helpers (head / nav_links / footer / esc ...).
"""
import json
import datetime as dt

YEAR = 2026
END = dt.date(YEAR, 12, 31)

# US federal holidays still on the 2026 calendar after early November.
# Source: OPM, "Federal Holidays" (5 U.S.C. 6103) - Veterans Day Wed Nov 11, Thanksgiving Thu Nov 26, Christmas Fri Dec 25.
# New Year's Day 2027 falls on Friday, January 1, 2027, so it is not part of the 2026 count.
FED_HOLIDAYS = [
    (dt.date(2026, 11, 11), 'Veterans Day', 'veterans-day-2026'),
    (dt.date(2026, 11, 26), 'Thanksgiving Day', 'us-thanksgiving-2026'),
    (dt.date(2026, 12, 25), 'Christmas Day', 'christmas-day-2026'),
]

# (date, label, note, slug-or-None). Astronomy dates are UTC dates; every row was checked against JPL Horizons
# and a published ephemeris (Astro-Seek / USNO via Farmers' Almanac / timeanddate) on 2026-11-03.
AHEAD = [
    (dt.date(2026, 11, 8),  'Diwali (main day)',          'Sunday; middle day of the five-day festival', 'diwali-2026'),
    (dt.date(2026, 11, 9),  'New Moon in Scorpio',        '', 'new-moon-november-2026'),
    (dt.date(2026, 11, 11), 'Veterans Day',               'US federal holiday', 'veterans-day-2026'),
    (dt.date(2026, 11, 13), 'Mercury stations direct',    'Ends the retrograde that began Oct 24 · also Friday the 13th', 'mercury-direct-november-2026'),
    (dt.date(2026, 11, 14), 'Venus stations direct',      'Evening of Nov 13 in the Americas', 'venus-direct-november-2026'),
    (dt.date(2026, 11, 17), 'Leonid meteor shower peaks', 'Peak night Nov 17–18', 'leonids-2026'),
    (dt.date(2026, 11, 24), 'Full Moon in Gemini',        'The Beaver Moon', 'full-moon-november-2026'),
    (dt.date(2026, 11, 26), 'Thanksgiving Day',           'US federal holiday', 'us-thanksgiving-2026'),
    (dt.date(2026, 11, 27), 'Black Friday',               'The day after Thanksgiving', 'black-friday-2026'),
    (dt.date(2026, 11, 30), 'Cyber Monday',               'The Monday after Black Friday', 'cyber-monday-2026'),
    (dt.date(2026, 12, 4),  'Hanukkah begins',            'At sundown; first candle that evening, ends Dec 12', None),
    (dt.date(2026, 12, 9),  'New Moon in Sagittarius',    'Evening of Dec 8 in the Americas', 'new-moon-december-2026'),
    (dt.date(2026, 12, 10), 'Saturn stations direct',     'In Aries', 'saturn-direct-december-2026'),
    (dt.date(2026, 12, 13), 'Geminid meteor shower peaks', 'Peak night Dec 13–14, thin crescent Moon', 'geminids-2026'),
    (dt.date(2026, 12, 13), 'Jupiter stations retrograde', 'In Leo · evening of Dec 12 in the Americas', 'jupiter-retrograde-december-2026'),
    (dt.date(2026, 12, 21), 'Winter solstice',            'Northern Hemisphere winter begins', 'winter-2026'),
    (dt.date(2026, 12, 24), 'Full Moon (Cold Moon)',      'Evening of Dec 23 in the Americas', 'full-moon-december-2026'),
    (dt.date(2026, 12, 24), 'Christmas Eve',              '', 'christmas-eve-2026'),
    (dt.date(2026, 12, 25), 'Christmas Day',              'US federal holiday', 'christmas-day-2026'),
    (dt.date(2026, 12, 31), "New Year's Eve",             'Countdown to 2027', 'new-year-2027'),
]


def weekdays_after(a, b):
    """Monday-Friday days in the range (a, b] - i.e. after a, up to and including b."""
    n, d = 0, a + dt.timedelta(days=1)
    while d <= b:
        if d.weekday() < 5:
            n += 1
        d += dt.timedelta(days=1)
    return n


def holidays_after(a, b):
    return sum(1 for d, _, _ in FED_HOLIDAYS if a < d <= b and d.weekday() < 5)


def rel(days):
    if days < 0:
        return 'passed'
    if days == 0:
        return 'today'
    if days == 1:
        return 'tomorrow'
    return f'in {days} days'


def nice_long(d):
    return d.strftime('%A, %B ') + str(d.day) + d.strftime(', %Y')


def snapshot(today):
    """Every number on the page, as of `today` (the build date). The in-page script recomputes them per visitor."""
    left = (END - today).days
    wd = weekdays_after(today, END)
    hol = holidays_after(today, END)
    nov_a, nov_b = max(today, dt.date(2026, 10, 31)), dt.date(2026, 11, 30)
    dec_a, dec_b = max(today, dt.date(2026, 11, 30)), END
    nov_wd = weekdays_after(nov_a, nov_b) if today < nov_b else 0
    dec_wd = weekdays_after(dec_a, dec_b) if today < dec_b else 0
    nov_h = holidays_after(nov_a, nov_b) if today < nov_b else 0
    dec_h = holidays_after(dec_a, dec_b) if today < dec_b else 0
    doy = today.timetuple().tm_yday
    return dict(
        left=left, weeks=left // 7, rem=left % 7, wd=wd, hol=hol, work=wd - hol, weekend=left - wd,
        doy=doy, pct=f'{doy / 365 * 100:.1f}', nov_work=nov_wd - nov_h, dec_work=dec_wd - dec_h,
        nov_wd=nov_wd, dec_wd=dec_wd, nov_h=nov_h, dec_h=dec_h,
    )


def weeks_text(n, r):
    w = f'{n} week{"" if n == 1 else "s"}'
    return w if r == 0 else f'{w} and {r} day{"" if r == 1 else "s"}'


SCRIPT = '''<script>
(function(){
  function $(id){return document.getElementById(id);}
  var DAY=86400000, END=Date.UTC(2026,11,31);
  var HOL=[Date.UTC(2026,10,11),Date.UTC(2026,10,26),Date.UTC(2026,11,25)];
  var n=new Date(), T=Date.UTC(n.getFullYear(),n.getMonth(),n.getDate());
  function isWd(t){var g=new Date(t).getUTCDay();return g>=1&&g<=5;}
  function wd(a,b){var c=0;for(var t=a+DAY;t<=b;t+=DAY){if(isWd(t))c++;}return c;}
  function hol(a,b){var c=0;for(var i=0;i<HOL.length;i++){var h=HOL[i];if(h>a&&h<=b&&isWd(h))c++;}return c;}
  function set(id,v){var e=$(id);if(e)e.textContent=v;}
  var left=Math.round((END-T)/DAY);
  if(left<0){
    var box=$('dl-ended');
    if(box){box.hidden=false;box.innerHTML='<b>2026 is over.</b> See <a href="/days-in-2027/">how many days there are in 2027</a> or the <a href="/new-year-2027/">live countdown to New Year 2027</a>.';}
    return;
  }
  var weekdays=wd(T,END), holidays=hol(T,END), plural=function(x,w){return x+' '+w+(x===1?'':'s');};
  var weeks=Math.floor(left/7), rem=left%7;
  set('dl-asof',new Date(T).toLocaleDateString('en-US',{weekday:'long',year:'numeric',month:'long',day:'numeric',timeZone:'UTC'}));
  set('dl-left',left); set('dl-left2',left);
  set('dl-weeks',plural(weeks,'week')+(rem?' and '+plural(rem,'day'):''));
  set('dl-weeks2',plural(weeks,'week')+(rem?' and '+plural(rem,'day'):''));
  set('dl-weekdays',weekdays); set('dl-work',weekdays-holidays); set('dl-work2',weekdays-holidays);
  set('dl-weekends',left-weekdays);
  var doy=Math.round((T-Date.UTC(2026,0,1))/DAY)+1;
  set('dl-doy',doy); set('dl-pct',(doy/365*100).toFixed(1)+'%');
  var nA=Math.max(T,Date.UTC(2026,9,31)), nB=Date.UTC(2026,10,30), dA=Math.max(T,Date.UTC(2026,10,30)), dB=END;
  set('dl-nov',T<nB?wd(nA,nB)-hol(nA,nB):0); set('dl-dec',T<dB?wd(dA,dB)-hol(dA,dB):0);
  var cells=document.querySelectorAll('td[data-d]');
  for(var i=0;i<cells.length;i++){
    var p=cells[i].getAttribute('data-d').split('-'), d=Math.round((Date.UTC(+p[0],+p[1]-1,+p[2])-T)/DAY);
    cells[i].textContent=d<0?'passed':d===0?'today':d===1?'tomorrow':'in '+d+' days';
  }
})();
</script>'''


def days_left_in_2026(h, today):
    """Return the full HTML page. `h` = dict(head, nav_links, footer, esc, SITE, BRAND)."""
    s = snapshot(today)
    esc, SITE = h['esc'], h['SITE']
    slug = 'days-left-in-2026'
    url = f'{SITE}/{slug}/'
    title = 'How Many Days Left in 2026? Workdays, Holidays & Sky Events'
    desc = ('How many days are left in 2026? Live count of days, weeks, weekdays and US workdays after '
            'federal holidays, plus every holiday and sky event still ahead.')
    assert len(title) <= 60 and 130 <= len(desc) <= 155, (len(title), len(desc))
    asof = nice_long(today)
    wk = weeks_text(s['weeks'], s['rem'])

    hol_rows = ''.join(
        f'<tr><td>{d.strftime("%a, %b ")}{d.day}</td><td><a href="/{sl}/">{nm}</a></td><td>{rel((d - today).days)}</td></tr>'
        for d, nm, sl in FED_HOLIDAYS)
    ahead_rows = ''
    for d, label, note, sl in AHEAD:
        lab = f'<a href="/{sl}/">{esc(label)}</a>' if sl else esc(label)
        ahead_rows += (f'<tr><td>{d.strftime("%a, %b ")}{d.day}</td><td>{lab}</td>'
                       f'<td data-d="{d.isoformat()}">{rel((d - today).days)}</td><td>{esc(note)}</td></tr>')

    faq = [
        ('How many days are left in 2026?',
         f'As of {asof}, there are {s["left"]} days left in 2026 ({wk}), counting the days after today up to and '
         f'including December 31. Count today as well and the figure is {s["left"] + 1}. The number on this page '
         f'recalculates from your device\'s date, so it stays right every day until the year ends.'),
        ('How many working days are left in 2026 in the US?',
         f'As of {asof}, there are {s["wd"]} weekdays left, and {s["hol"]} of them are US federal holidays (Veterans Day '
         f'on Wednesday, November 11; Thanksgiving on Thursday, November 26; Christmas Day on Friday, December 25), which '
         f'leaves {s["work"]} working days. Your employer may close on other days, such as the Friday after Thanksgiving, '
         f'so treat the figure as a baseline.'),
        ('How many full moons are left in 2026?',
         'Two: Tuesday, November 24 and Thursday, December 24. The December one peaks at about 01:30 UTC on the 24th, '
         'which is still the evening of Wednesday, December 23 in North America.'),
        ('Does the count include today and December 31?',
         'Not here. "Days left" means the days after today through December 31, so the figure reads 0 on New Year\'s Eve. '
         'Counting today as a full day adds one. Many counters do the opposite, which is the most common reason two sites '
         'show different numbers on the same morning.'),
    ]
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}
    art_ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': desc,
              'mainEntityOfPage': url, 'datePublished': today.isoformat(), 'dateModified': today.isoformat(),
              'author': {'@type': 'Organization', 'name': h['BRAND'], 'url': SITE + '/'},
              'publisher': {'@type': 'Organization', 'name': h['BRAND'], 'url': SITE + '/'}}
    bc_ld = h['breadcrumb_ld']([('Home', SITE + '/'), ('Days left in 2026', url)])
    ld = ''.join(f'<script type="application/ld+json">{x if isinstance(x, str) else json.dumps(x)}</script>'
                 for x in (art_ld, faq_ld, bc_ld))
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary>\n<p>{esc(a)}</p>\n</details>' for q, a in faq)

    body = f'''
<section class="home-hero">
  <h1>How Many Days Are Left in 2026?</h1>
  <p class="lead">As of <span id="dl-asof">{asof}</span>, there are <b><span id="dl-left">{s["left"]}</span> days left in 2026</b>,
  which is <span id="dl-weeks">{wk}</span>. Take out weekends and the US federal holidays still ahead and you are left with
  <b><span id="dl-work">{s["work"]}</span> working days</b>. The figures recalculate from your own clock when the page loads.</p>
  <p class="note" id="dl-ended" hidden></p>
</section>

<section class="grid2">
  <div>
    <h2>The count, six ways</h2>
    <div class="tablewrap"><table>
      <tr><th>What you are counting</th><th>Right now</th><th>How it is counted</th></tr>
      <tr><td>Calendar days left</td><td><b><span id="dl-left2">{s["left"]}</span></b></td><td>Days after today through December 31</td></tr>
      <tr><td>Weeks left</td><td><b><span id="dl-weeks2">{wk}</span></b></td><td>Calendar days divided by 7</td></tr>
      <tr><td>Weekdays (Mon–Fri)</td><td><b><span id="dl-weekdays">{s["wd"]}</span></b></td><td>December 31 included</td></tr>
      <tr><td>Working days after US federal holidays</td><td><b><span id="dl-work2">{s["work"]}</span></b></td><td>Weekdays minus Veterans Day, Thanksgiving and Christmas</td></tr>
      <tr><td>Weekend days left</td><td><b><span id="dl-weekends">{s["weekend"]}</span></b></td><td>Saturdays and Sundays</td></tr>
      <tr><td>Year completed</td><td><b><span id="dl-pct">{s["pct"]}%</span></b></td><td>Today is day <span id="dl-doy">{s["doy"]}</span> of 365</td></tr>
    </table></div>
    <p>"Days left" here means the days <i>after</i> today, so the number reads 0 on December 31. Count today as a full day and every figure in the first rows goes up by one.</p>
    <p>Most online day counters stop at the weekday row and add a footnote saying holidays are not subtracted. The working-day row is the one this page adds, because it is the number people planning a deadline actually need.</p>
  </div>
  <aside>
    <h2>US federal holidays still ahead</h2>
    <div class="tablewrap"><table>
      <tr><th>Date</th><th>Holiday</th><th>When</th></tr>
      {hol_rows}
    </table></div>
    <p>These are the only federal holidays left in 2026 on the OPM schedule. New Year's Day 2027 lands on Friday, January 1, so it belongs to next year's count.</p>
    <p>Federal holidays bind federal employees by law. Private employers choose their own days, and many also close on the Friday after Thanksgiving. December 24 falls on a Thursday and is not on OPM's schedule, so check your own calendar.</p>
  </aside>
</section>

<h2>Everything still ahead, in order</h2>
<p>Holidays, moon phases, planetary stations and meteor showers between now and the end of the year. Dates for astronomy rows are UTC dates; where the Americas see the event on the evening before, the last column says so.</p>
<div class="tablewrap"><table>
  <tr><th>Date</th><th>Event</th><th>When</th><th>Good to know</th></tr>
  {ahead_rows}
</table></div>
<p>Every row links to its own live countdown. The planetary stations and moon phases were checked against NASA's JPL Horizons system and a second published ephemeris on {asof}.</p>

<section class="grid2">
  <div>
    <h2>Working days left, month by month</h2>
    <div class="tablewrap"><table>
      <tr><th>Month</th><th>Working days left</th><th>Holidays removed</th></tr>
      <tr><td>November 2026</td><td><b><span id="dl-nov">{s["nov_work"]}</span></b></td><td>Veterans Day, Thanksgiving</td></tr>
      <tr><td>December 2026</td><td><b><span id="dl-dec">{s["dec_work"]}</span></b></td><td>Christmas Day</td></tr>
    </table></div>
    <p>Both months count only the days after today. Early in November, November's row shows nearly the full month; by the first of December it reads zero.</p>
  </div>
  <aside>
    <h2>Do it in a spreadsheet</h2>
    <p>Days left, today excluded: <code>=DATE(2026,12,31)-TODAY()</code></p>
    <p>Working days left after the three holidays, with their dates typed into cells H2:H4: <code>=NETWORKDAYS(TODAY()+1,DATE(2026,12,31),H2:H4)</code></p>
    <p>Skip the holiday range and the second formula returns the plain weekday count that most online counters show.</p>
  </aside>
</section>

<h2>Why two counters show different numbers</h2>
<p><b>Today in or out.</b> Some tools count today as day one, so their answer is one higher than ours on the same morning.</p>
<p><b>December 31 in or out.</b> The last day of the year is either the final day to count or the finish line. Here it is the finish line, so the figure is 0 on December 31 itself.</p>
<p><b>Time zones.</b> A page that counts on a server clock can be a day ahead or behind for you. This one reads your device's date.</p>
<p><b>Old pages.</b> A static number printed without a date goes stale the next morning. If a counter does not say what day it was calculated for, check it against the table above.</p>

<h2>Frequently Asked Questions</h2>
<div class="faq">
{faq_html}
</div>

<h2>More from daysuntil.bond</h2>
<ul>
  <li><a href="/new-year-2027/">Live countdown to New Year 2027</a>, down to the second</li>
  <li><a href="/christmas-day-2026/">Days until Christmas 2026</a> and <a href="/black-friday-2026/">Black Friday 2026</a></li>
  <li><a href="/days-in-2027/">How many days are in 2027?</a> The full year breakdown</li>
  <li><a href="/why-daysuntil-beats-every-other-site/">Why our counts differ from other countdown sites</a></li>
  <li><a href="/moon/">Every full and new moon through 2028</a></li>
</ul>
{SCRIPT}
'''
    return (h['head'](title, desc, url, f'/og/{slug}.png', ld, '..') + h['nav_links']('..') +
            '</nav>\n</header>\n<main id="main">' + body + h['footer']('..'))
