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
  // ---------------- custom, private countdown tool ----------------
  var customForm = document.getElementById('custom-countdown-form');
  if (customForm) {
    var byId = function (id) { return document.getElementById(id); };
    var customTarget = null, customTimer = null;
    var nameInput = byId('custom-event-name'), dateInput = byId('custom-event-date'),
        timeInput = byId('custom-event-time'), resultBox = byId('custom-countdown-result');
    function customWeekdays(a, b) {
      var start = new Date(a), end = new Date(b), count = 0;
      start.setHours(0, 0, 0, 0); end.setHours(0, 0, 0, 0);
      if (start > end) { var swap = start; start = end; end = swap; }
      while (start < end) {
        start.setDate(start.getDate() + 1);
        var day = start.getDay();
        if (day !== 0 && day !== 6) count++;
      }
      return count;
    }
    function updateCustomCountdown() {
      if (customTarget === null) return;
      var now = Date.now(), diff = customTarget - now, past = diff < 0, abs = Math.abs(diff);
      var days = Math.floor(abs / DAY), hours = Math.floor(abs % DAY / 3600000);
      var minutes = Math.floor(abs % 3600000 / 60000), seconds = Math.floor(abs % 60000 / 1000);
      byId('custom-days').textContent = fmtInt(days);
      byId('custom-hours').textContent = String(hours).padStart(2, '0');
      byId('custom-minutes').textContent = String(minutes).padStart(2, '0');
      byId('custom-seconds').textContent = String(seconds).padStart(2, '0');
      byId('custom-total-hours').textContent = fmtInt(Math.floor(abs / 3600000));
      byId('custom-weeks').textContent = (abs / DAY / 7).toFixed(1);
      var weekdays = customWeekdays(now, customTarget);
      var calendarDays = Math.ceil(abs / DAY);
      byId('custom-weekdays').textContent = fmtInt(weekdays);
      byId('custom-weekends').textContent = fmtInt(Math.max(0, calendarDays - weekdays));
      var title = nameInput.value.trim() || 'Your event';
      byId('custom-result-title').textContent = title;
      var dateText = new Date(customTarget).toLocaleString(undefined, {dateStyle:'full', timeStyle:'short'});
      byId('custom-result-status').textContent = past
        ? title + ' was set for ' + dateText + '. Time elapsed: ' + fmtInt(days) + ' day(s).'
        : title + ' is scheduled for ' + dateText + '. Time remaining: ' + fmtInt(days) + ' day(s).';
      byId('custom-timezone').textContent = 'Displayed in ' + (Intl.DateTimeFormat().resolvedOptions().timeZone || 'your device time zone') + '. Calculated locally in this browser.';
    }
    function startCustomCountdown() {
      var title = nameInput.value.trim(), date = dateInput.value, time = timeInput.value;
      var error = byId('custom-error');
      error.hidden = true;
      if (!title || !date) {
        error.textContent = 'Enter an event name and choose a target date.';
        error.hidden = false; return false;
      }
      var parsed = new Date(date + 'T' + (time || '00:00'));
      if (Number.isNaN(parsed.getTime())) {
        error.textContent = 'That date or time could not be read. Please choose it again.';
        error.hidden = false; return false;
      }
      customTarget = parsed.getTime();
      resultBox.hidden = false;
      updateCustomCountdown();
      if (customTimer) clearInterval(customTimer);
      customTimer = setInterval(updateCustomCountdown, 1000);
      return true;
    }
    customForm.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!startCustomCountdown()) return;
      var url = new URL(location.href);
      url.searchParams.set('event', nameInput.value.trim());
      url.searchParams.set('date', dateInput.value);
      if (timeInput.value) url.searchParams.set('time', timeInput.value);
      else url.searchParams.delete('time');
      history.replaceState({}, '', url.pathname + url.search + url.hash);
    });
    byId('custom-share').addEventListener('click', function () {
      var url = new URL(location.href);
      url.searchParams.set('event', nameInput.value.trim());
      url.searchParams.set('date', dateInput.value);
      if (timeInput.value) url.searchParams.set('time', timeInput.value);
      else url.searchParams.delete('time');
      var text = url.toString(), button = byId('custom-share'), status = byId('custom-share-status');
      function done() { button.textContent = 'Link copied'; status.textContent = 'Anyone with this link can open the same countdown.'; setTimeout(function(){button.textContent='Copy share link';},1800); }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function(){ window.prompt('Copy this countdown link:', text); });
      } else { window.prompt('Copy this countdown link:', text); }
    });
    function resetCustom() {
      if (customTimer) clearInterval(customTimer);
      customTimer = null; customTarget = null; resultBox.hidden = true;
      byId('custom-error').hidden = true; byId('custom-share-status').textContent = '';
      var url = new URL(location.href);
      ['event','date','time'].forEach(function(k){url.searchParams.delete(k);});
      history.replaceState({}, '', url.pathname + url.search + url.hash);
    }
    byId('custom-new').addEventListener('click', function () {
      customForm.reset(); resetCustom(); nameInput.focus();
    });
    customForm.addEventListener('reset', function () {
      setTimeout(function(){ resetCustom(); }, 0);
    });
    // A shared URL restores the event locally; no account or server storage is used.
    var params = new URLSearchParams(location.search);
    if (params.has('event') && params.has('date')) {
      nameInput.value = params.get('event') || '';
      dateInput.value = params.get('date') || '';
      timeInput.value = params.get('time') || '';
      startCustomCountdown();
    }
  }

})();
