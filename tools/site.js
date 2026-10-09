/* daysuntil.bond — countdown engine, cards, search, share. No dependencies. */
(function () {
  'use strict';
  var DAY = 86400000;

  function target(ev) {
    if (ev.kind === 'datetime' && ev.utc) return new Date(ev.utc).getTime();
    return new Date(ev.y, ev.m - 1, ev.d, 0, 0, 0, 0).getTime(); // local midnight
  }

  function fmtInt(n) { return Math.floor(Math.abs(n)).toLocaleString('en-US'); }

  function weekdaysBetween(a, b) {
    var d = new Date(a), n = 0;
    while (d.getTime() < b) { var w = d.getDay(); if (w !== 0 && w !== 6) n++; d.setDate(d.getDate() + 1); }
    return n;
  }

  // ---------------- event page countdown ----------------
  var ev = window.EVENT;
  if (ev) {
    var t = target(ev), el = function (id) { return document.getElementById(id); };
    function tick() {
      var now = Date.now(), diff = t - now, past = diff <= 0, ad = Math.abs(diff);
      var days = Math.floor(ad / DAY), hrs = Math.floor(ad % DAY / 3600000),
          min = Math.floor(ad % 3600000 / 60000), sec = Math.floor(ad % 60000 / 1000);
      if (el('cd-d')) el('cd-d').textContent = past && ad < DAY ? 0 : fmtInt(days);
      if (el('cd-h')) el('cd-h').textContent = hrs;
      if (el('cd-m')) el('cd-m').textContent = min;
      if (el('cd-s')) el('cd-s').textContent = sec;
      if (el('cd-status')) el('cd-status').innerHTML = past
        ? 'It\u2019s been <b>' + fmtInt(days) + '</b> day' + (days === 1 ? '' : 's') + ' since ' + ev.title + ' (' + ev.dateNice + ').'
        : ev.title + ' falls on <b>' + ev.dateNice + '</b> \u2014 <b>' + fmtInt(days) + '</b> day' + (days === 1 ? '' : 's') + ' to go.';
      var sign = past ? -1 : 1, a = past ? t : now, b = past ? now : t;
      if (el('ch-weeks')) el('ch-weeks').textContent = (ad / DAY / 7).toFixed(1);
      if (el('ch-wd')) el('ch-wd').textContent = fmtInt(weekdaysBetween(a, b));
      if (el('ch-we')) el('ch-we').textContent = fmtInt(Math.max(0, Math.round((ad / DAY) - weekdaysBetween(a, b))));
      if (el('ch-months')) el('ch-months').textContent = (ad / DAY / 30.44).toFixed(1);
      // live FAQ day counts
      document.querySelectorAll('.faq [data-live-days]').forEach(function (n) { n.textContent = fmtInt(days); });
    }
    tick(); setInterval(tick, 1000);

    var url = location.href, ttl = document.title;
    function share(net) {
      var u = { tw: 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(ttl) + '&url=' + encodeURIComponent(url),
                fb: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url),
                wa: 'https://wa.me/?text=' + encodeURIComponent(ttl + ' ' + url) }[net];
      if (u) window.open(u, '_blank', 'noopener');
    }
    var cp = el('sh-cp');
    if (cp) cp.addEventListener('click', function () {
      navigator.clipboard.writeText(url).then(function () { cp.textContent = 'Copied!'; setTimeout(function () { cp.textContent = 'Copy link'; }, 1600); });
    });
    ['tw', 'fb', 'wa'].forEach(function (n) { var b = el('sh-' + n); if (b) b.addEventListener('click', function () { share(n); }); });
  }

  // ---------------- cards: relative days ----------------
  document.querySelectorAll('.card-days[data-ms]').forEach(function (n) {
    var diff = parseInt(n.getAttribute('data-ms'), 10) - Date.now(), d = Math.floor(Math.abs(diff) / DAY);
    n.textContent = diff > 0 ? 'in ' + fmtInt(d) + ' day' + (d === 1 ? '' : 's') : fmtInt(d) + ' days ago';
  });

  // ---------------- home search ----------------
  var q = document.getElementById('q'), res = document.getElementById('q-results');
  if (q && res && window.EVENTS) {
    function run() {
      var v = q.value.trim().toLowerCase();
      if (v.length < 2) { res.hidden = true; return; }
      var hits = window.EVENTS.filter(function (e) {
        return e.t.toLowerCase().indexOf(v) !== -1 || e.c.replace('-', ' ').indexOf(v) !== -1;
      }).sort(function (a, b) { return a.m - b.m; }).slice(0, 9);
      res.innerHTML = hits.length
        ? hits.map(function (e) { return '<a href="' + e.s + '/"><span>' + e.t + '</span><span class="when">' + e.n + '</span></a>'; }).join('')
        : '<a><span>No match — try “moon”, “2027”, “eid”…</span><span></span></a>';
      res.hidden = false;
    }
    q.addEventListener('input', run);
    q.addEventListener('blur', function () { setTimeout(function () { res.hidden = true; }, 250); });
    if (location.search.indexOf('q=') !== -1) {
      q.value = decodeURIComponent(location.search.split('q=')[1] || '');
      run(); setTimeout(function () { res.hidden = false; }, 100);
    }
  }
})();
