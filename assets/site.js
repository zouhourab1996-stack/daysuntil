/* TrustScore — site behaviour: hoplink rewriting + config. No dependencies. */
(function () {
  'use strict';
  var C = window.SITE_CONFIG || {};

  // Rewrite every affiliate button to the live ClickBank hoplink.
  // Buttons carry data-vendor; fallback URLs live in data-fallback for noscript safety.
  document.querySelectorAll('a[data-vendor]').forEach(function (a) {
    var vendor = a.getAttribute('data-vendor');
    if (!vendor) return;
    var aff = C.clickbankAffiliate || '';
    var tid = C.clickbankTid || '';
    if (aff) {
      /* data-link = full hoplink URL (encrypted short links) — used as-is. */
      a.href = a.getAttribute('data-link') ||
               ('https://hop.clickbank.net/?affiliate=' + encodeURIComponent(aff) +
               '&vendor=' + encodeURIComponent(vendor) +
               (tid ? '&tid=' + encodeURIComponent(tid) : ''));
      a.setAttribute('rel', 'nofollow sponsored noopener');
      a.setAttribute('target', '_blank');
    }
  });

  // Current year in footer
  document.querySelectorAll('[data-year]').forEach(function (n) { n.textContent = new Date().getFullYear(); });
})();
