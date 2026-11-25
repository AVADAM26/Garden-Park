/* Garden Park Guest House · Entwurf 2027 */
(function () {
  var root = document.documentElement;

  // Hell/Dunkel, Wahl wird gespeichert
  var themeBtn = document.querySelector('.theme-toggle');
  function isDark() {
    var t = root.dataset.theme;
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = isDark() ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('gp-theme', next); } catch (e) {}
  });

  // Menü auf dem Handy
  var menuBtn = document.querySelector('.menu-toggle');
  var nav = document.getElementById('main-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open);
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Kopf mit Schatten, Eule und Buchungsknopf erscheinen beim Scrollen
  var header = document.querySelector('.site-header');
  var toTop = document.querySelector('.to-top');
  var mobileBook = document.querySelector('.mobile-book');
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (toTop && !toTop.classList.contains('fly')) toTop.classList.toggle('show', y > 700);
    if (mobileBook) mobileBook.classList.toggle('show', y > 500);
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  // Back to Top: der Waldkauz blinzelt ab und zu und fliegt beim Klick nach oben
  if (toTop) {
    setInterval(function () {
      if (!toTop.classList.contains('show')) return;
      toTop.classList.add('blink');
      setTimeout(function () { toTop.classList.remove('blink'); }, 300);
    }, 4200);
    toTop.addEventListener('click', function () {
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (reduce) { window.scrollTo(0, 0); return; }
      toTop.classList.add('fly');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      setTimeout(function () {
        toTop.classList.remove('fly', 'show');
      }, 1200);
    });
  }

  // Titelbild: immer so viel vom Haus wie möglich zeigen, unten bis knapp unter die Hände (84 % der Bildhöhe)
  var heroImg = document.querySelector('.hero-img');
  function fitHero() {
    if (!heroImg || !heroImg.naturalWidth) return;
    var hero = heroImg.parentNode;
    var W = hero.clientWidth, H = hero.clientHeight;
    var r = heroImg.naturalWidth / heroImg.naturalHeight;
    var TOP = 0.06, BOTTOM = 0.84;                 // sichtbarer Bereich: Dach bis knapp unter die Hände
    var maxIh = H / (BOTTOM - TOP);                 // nie stärker zoomen als nötig
    var Ih = Math.max(H, W / r);
    if (Ih > maxIh) {                               // sehr breiter Bildschirm: Foto nicht strecken, Seiten weich ausblenden
      Ih = maxIh;
      heroImg.classList.add('framed');
      heroImg.style.width = (Ih * r) + 'px';
    } else {
      heroImg.classList.remove('framed');
      heroImg.style.width = '';
    }
    var p = Ih <= H + 1 ? 0.5 : Math.min(1, Math.max(0, (BOTTOM * Ih - H) / (Ih - H)));
    heroImg.style.objectPosition = '50% ' + (p * 100).toFixed(1) + '%';
  }
  if (heroImg) {
    if (heroImg.complete) fitHero(); else heroImg.addEventListener('load', fitHero);
    window.addEventListener('resize', fitHero, { passive: true });
  }

  // Buchungsknopf oben: Daten im Link immer auf heute und morgen setzen
  document.querySelectorAll('[data-direct-booking]').forEach(function (a) {
    function iso(d) { return d.toISOString().slice(0, 10); }
    var d1 = new Date(), d2 = new Date(Date.now() + 864e5);
    a.href = a.href.replace(/%22checkInDate%22:%22[0-9-]+%22/, '%22checkInDate%22:%22' + iso(d1) + '%22')
                   .replace(/%22checkOutDate%22:%22[0-9-]+%22/, '%22checkOutDate%22:%22' + iso(d2) + '%22');
  });

  // Video erst beim Klick laden (schneller, keine YouTube-Cookies vorher)
  document.querySelectorAll('.video-facade').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = btn.getAttribute('data-yt');
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      f.title = 'Garden Park Guest House, short video';
      f.allow = 'autoplay; encrypted-media; picture-in-picture';
      f.allowFullscreen = true;
      btn.appendChild(f);
      btn.querySelector('.play').remove();
    }, { once: true });
  });

  // Aktiven Menüpunkt markieren
  var links = nav ? Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]')) : [];
  if ('IntersectionObserver' in window && links.length) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(function (a) { var s = document.querySelector(a.getAttribute('href')); if (s) obs.observe(s); });
  }
})();
