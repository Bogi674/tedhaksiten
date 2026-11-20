(function () {
  'use strict';

  // ---------- Event config ----------
  var EVENT_START = new Date('2026-11-29T13:00:00+07:00');
  var EVENT_END = new Date('2026-11-29T16:00:00+07:00');
  var EVENT_TITLE = 'Tedhak Siten Giaksa & Giakta';
  var EVENT_PLACE = 'Podomoro Golf View, Cluster Juniper 8/12, Tapos, Depok';
  var EVENT_MAPS = 'https://maps.app.goo.gl/UvSDBrSH3n6os9UJ9';

  // ---------- Guest name (?to=Nama+Tamu) ----------
  var params = new URLSearchParams(location.search);
  var to = params.get('to');
  if (to) document.getElementById('guestName').textContent = to;

  // ---------- Open invitation ----------
  var cover = document.getElementById('cover');
  var audio = document.getElementById('bgm');
  var musicBtn = document.getElementById('musicBtn');
  var hasMusic = false;

  fetch('/music.mp3', { method: 'HEAD' }).then(function (r) {
    if (r.ok) { hasMusic = true; }
  }).catch(function () {});

  document.getElementById('openBtn').addEventListener('click', function () {
    cover.classList.add('opened');
    document.body.classList.remove('locked');
    document.body.classList.add('open');
    window.scrollTo(0, 0);
    watchPage();
    if (hasMusic) {
      musicBtn.hidden = false;
      audio.play().then(function () { musicBtn.classList.add('playing'); }).catch(function () {});
    }
  });

  musicBtn.addEventListener('click', function () {
    if (audio.paused) { audio.play(); musicBtn.classList.add('playing'); }
    else { audio.pause(); musicBtn.classList.remove('playing'); }
  });

  // ---------- Countdown ----------
  function pad(n) { return String(n).padStart(2, '0'); }
  function tick() {
    var diff = Math.max(0, EVENT_START - new Date());
    var d = Math.floor(diff / 864e5);
    var h = Math.floor(diff / 36e5) % 24;
    var m = Math.floor(diff / 6e4) % 60;
    var s = Math.floor(diff / 1e3) % 60;
    document.getElementById('cd-d').textContent = pad(d);
    document.getElementById('cd-h').textContent = pad(h);
    document.getElementById('cd-m').textContent = pad(m);
    document.getElementById('cd-s').textContent = pad(s);
  }
  tick();
  setInterval(tick, 1000);

  // ---------- Save the date (Google Calendar) ----------
  function gcal(dt) { return dt.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, ''); }
  document.getElementById('saveDate').href =
    'https://calendar.google.com/calendar/render?action=TEMPLATE' +
    '&text=' + encodeURIComponent(EVENT_TITLE) +
    '&dates=' + gcal(EVENT_START) + '/' + gcal(EVENT_END) +
    '&details=' + encodeURIComponent('Dresscode: Batik / Cokelat / Krem\nMaps: ' + EVENT_MAPS) +
    '&location=' + encodeURIComponent(EVENT_PLACE) +
    '&ctz=Asia/Jakarta';

  // ---------- Gallery (reads /gallery.json, generated from /gallery folder at build) ----------
  var grid = document.getElementById('galleryGrid');
  var photos = [];
  var current = 0;

  function renderGallery(list) {
    photos = list;
    grid.innerHTML = '';
    list.forEach(function (src, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'zoomblur';
      b.style.animationDelay = (i % 4) * 0.15 + 's';
      b.setAttribute('aria-label', 'Lihat foto ' + (i + 1));
      var img = new Image();
      img.loading = 'lazy';
      img.src = src;
      img.alt = 'Galeri ' + (i + 1);
      b.appendChild(img);
      b.addEventListener('click', function () { openLb(i); });
      grid.appendChild(b);
      observer.observe(b);
    });
  }

  // ---------- Lightbox ----------
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lbImg');
  function openLb(i) { current = i; lbImg.src = photos[i]; lb.hidden = false; }
  function closeLb() { lb.hidden = true; }
  function step(n) { current = (current + n + photos.length) % photos.length; lbImg.src = photos[current]; }
  document.getElementById('lbClose').onclick = closeLb;
  document.getElementById('lbPrev').onclick = function () { step(-1); };
  document.getElementById('lbNext').onclick = function () { step(1); };
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') closeLb();
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });
  var touchX = null;
  lb.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 40) step(dx < 0 ? 1 : -1);
    touchX = null;
  });

  // ---------- Reveal on scroll (entrance animations) ----------
  var REVEAL = '.from-top,.from-bottom,.fade,.zoomin,.zoomblur';
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); observer.unobserve(en.target); }
    });
  }, { threshold: 0.12 });
  // cover animates immediately; page content only after the invitation is opened
  cover.querySelectorAll(REVEAL).forEach(function (el) { el.classList.add('in'); });
  function watchPage() {
    document.querySelectorAll('.phone > .sec ' + REVEAL.split(',').join(', .phone > .sec ')).forEach(function (el) {
      observer.observe(el);
    });
    document.querySelectorAll('.phone > .sec').forEach(function (sec) {
      sec.querySelectorAll(':scope > .bgf').forEach(function (el) { observer.observe(el); });
    });
  }

  fetch('/gallery.json', { cache: 'no-store' })
    .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
    .then(renderGallery)
    .catch(function () {
      renderGallery(['/gallery/01.jpg', '/gallery/02.jpg', '/gallery/03.jpg', '/gallery/04.jpg']);
    });

  // ---------- Dock active state ----------
  var links = document.querySelectorAll('.dock a');
  var map = { home: 0, about: 0, anak: 1, countdown: 2, event: 2, gallery: 3, closing: 4 };
  var secObs = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        links.forEach(function (l) { l.classList.remove('active'); });
        var idx = map[en.target.id];
        if (idx !== undefined) links[idx].classList.add('active');
      }
    });
  }, { rootMargin: '-45% 0px -45% 0px' });
  Object.keys(map).forEach(function (id) {
    var el = document.getElementById(id);
    if (el) secObs.observe(el);
  });
})();
