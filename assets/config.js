/* ==========================================================================
   TRUSTSCORE — SITE CONFIGURATION
   The ONLY file you ever need to edit. Change a value, commit, done.
   Affiliate links: every button with data-vendor is rewritten to
   https://hop.clickbank.net/?affiliate=<you>&vendor=<vendor>&tid=<tid>
   ========================================================================== */

var SITE_CONFIG = {

  /* ---- MONETIZATION ------------------------------------------------------ */
  clickbankAffiliate: "heditouati",   // your ClickBank nickname (same as twinflame.bond)
  clickbankTid:       "tsb",          // tracking id for THIS site's reports (tfb = twinflame)
  network: [
    { name: "Twin Flame Bond", url: "https://twinflame.bond" },
    { name: "Prophetic",       url: "https://prophetic.pw" },
    { name: "daysuntil.bond",  url: "https://daysuntil.bond" },
    { name: "BMR Calc",        url: "https://www.bmrcalc.bond" },
  ],

  /* ---- GOOGLE ANALYTICS (GA4) -------------------------------------------- */
  gaMeasurementId: "G-1W7PC1JDKH",

  /* ---- ADSENSE (flip adsenseEnabled after the site is added in AdSense) --- */
  adsenseEnabled: false,
  adsenseClient:  "ca-pub-3898992716389443",

  /* ---- SITE -------------------------------------------------------------- */
  siteName: "TrustScore",
  siteUrl:  "https://trustscore.bond",
  contactEmail: "anistouati74@gmail.com"
};
