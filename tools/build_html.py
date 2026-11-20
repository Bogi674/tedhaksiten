"""Generates public/index.html. Layer coordinates are in a 500-unit wide grid
(the reference layout); CSS scales 1 unit = column width / 500."""
import os

A = '/assets/art/'

def L(src, x, y=None, w=100, b=None, cls='', anim='', ent='', flip=False, extra=''):
    pos = f'--x:{x};--w:{w};' + (f'--b:{b};' if b is not None else f'--y:{y};')
    k = 'L' + (' bt' if b is not None else '') + (f' {ent}' if ent else '') + (f' {cls}' if cls else '')
    inner_cls = (f'{anim}' + (' fx' if flip else '')).strip()
    return (f'<div class="{k}" style="{pos}{extra}"><img class="{inner_cls}" src="{A}{src}.webp" alt="" loading="lazy" decoding="async"></div>')

def forest(cls=''):
    return f'<div class="bgf {cls}" style="background-image:url({A}forest.webp)"></div>'

def top_set(hero=False):
    g = L('garland', 0, -42, 500, ent='fade d3') if hero else L('garland', -125, -95, 750, ent='fade d3')
    return (g +
            L('corner', -39, -8, 163, anim='a-flc', ent='from-top d5', cls='o-tl') +
            L('corner', 339, -5, 165, anim='a-fla', ent='from-top d5', flip=True, cls='o-tr') +
            L('cloud', -44, 1, 250, cls='cloud c12') +
            L('cloud', 77, 8, 150, cls='cloud c10'))

def bottom_set(peacock=False, wide=True, bouquets=True):
    s = ''
    if peacock:
        s += L('peacocks', 170, b=0, w=160, ent='from-bottom d1')
    s += (L('flowerbed', -125, b=-12, w=750, ent='from-bottom') if wide else L('flowerbed', 0, b=-11, w=500, ent='from-bottom'))
    if bouquets:
        s += (L('stem-a', 17, b=-1, w=83, anim='a-fla', ent='from-bottom d5', cls='o-b') +
              L('stem-b', 399, b=-4, w=81, anim='a-fla2', ent='from-bottom d6', cls='o-b') +
              L('bouquet', 0, b=-12, w=200, ent='from-bottom d2') +
              L('bouquet', 300, b=-12, w=200, ent='from-bottom d3', flip=True))
    s += (L('butterfly-a', 435, b=121, w=65, anim='a-stop', ent='fade d6') +
          L('butterfly-b', 0, b=36, w=75, anim='a-stop2', ent='fade d6'))
    return s

def oval(img, x=138, y=182, w=225, h=337, alt=''):
    return (f'<div class="L frame-oval zoomblur d5" style="--x:{x};--y:{y};--w:{w};--h:{h}">'
            f'<img src="{img}" alt="{alt}"></div>' +
            L('stem-a', x - 23, y + 175, 50, anim='a-fla', ent='from-bottom d6', cls='o-b') +
            L('stem-b', x + w - 42, y + 176, 79, anim='a-fla2', ent='from-bottom d6', cls='o-b'))

ICON = {
 'home': '<path d="M4 11l8-7 8 7v9h-5v-6H9v6H4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
 'kids': '<circle cx="8.5" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="15.5" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6M10 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6" fill="none" stroke="currentColor" stroke-width="1.6"/>',
 'event': '<rect x="3.5" y="5" width="17" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 10h17M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="8" cy="14.5" r="1" fill="currentColor"/><circle cx="12" cy="14.5" r="1" fill="currentColor"/><circle cx="16" cy="14.5" r="1" fill="currentColor"/>',
 'gallery': '<rect x="3.5" y="4.5" width="17" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="9" cy="10" r="1.8" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M4 18l5-5 4 4 3-3 4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
 'heart': '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
 'mail': '<path d="M3 9l9-6 9 6v11H3z M3 9l9 6 9-6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
 'cal': '<rect x="3.5" y="5" width="17" height="15" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3.5 10h17M8 3v4M16 3v4M9 15l2 2 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
 'search': '<circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>',
 'mark': '<path d="M7 3h10v18l-5-4-5 4z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>',
 'music': '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="2.5" fill="currentColor"/><path d="M12 3a9 9 0 0 1 9 9" stroke="currentColor" stroke-width="1.5" fill="none" opacity=".5"/>',
}
def ico(n): return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICON[n]}</svg>'

HTML = f'''<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Tedhak Siten Giaksa &amp; Giakta</title>
<meta name="description" content="Undangan Tedhak Siten Kagiaksa Faeyza Le Givanzka &amp; Kagiakta Raeyza Le Givanzka. Minggu, 29 November 2026, 13.00 WIB.">
<meta property="og:title" content="Tedhak Siten Giaksa &amp; Giakta">
<meta property="og:description" content="Minggu, 29 November 2026 · 13.00 WIB · Podomoro Golf View, Cluster Juniper 8/12, Tapos, Depok">
<meta property="og:image" content="/assets/img/og.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#f3ead9">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Great+Vibes&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{A}forest.webp">
<link rel="stylesheet" href="/style.css">
</head>
<body class="locked">

<!-- ===== DESKTOP LEFT PANEL ===== -->
<aside class="side">
  <div class="side-bg" style="background-image:url({A}forest.webp)"></div>
  <img class="side-stem l a-fla" src="{A}stem-a.webp" alt="">
  <img class="side-stem r a-fla2 fx" src="{A}stem-b.webp" alt="">
  <div class="side-text">
    <p class="cap gold">TEDHAK SITEN</p>
    <h1 class="side-name">Kagiaksa &amp; Kagiakta</h1>
  </div>
</aside>

<main class="phone" id="phone">

  <!-- ================= COVER ================= -->
  <section class="cover" id="cover">
    {forest()}
    {top_set(hero=True)}
    <div class="L txt cover-cap fade d3" style="--x:0;--y:88;--w:500"><p class="cap gold">TEDHAK SITEN</p></div>
    {oval('/assets/img/cover.jpg', 175, 118, 150, 225, 'Giaksa dan Giakta')}
    <div class="cover-text">
      <h2 class="name-xl from-bottom d5">Giaksa &amp; Giakta</h2>
      <p class="small from-bottom d6">Kepada Yth.</p>
      <p class="guest from-bottom d6" id="guestName">Bapak/Ibu/Saudara/i</p>
      <button class="btn from-bottom d6" id="openBtn" type="button">{ico('mail')} Buka Undangan</button>
    </div>
    {bottom_set(peacock=True, wide=False)}
  </section>

  <!-- ================= HOME ================= -->
  <section class="sec hero" id="home">
    {forest('from-top')}
    {top_set(hero=True)}
    <div class="L txt" style="--x:0;--y:150;--w:500"><p class="cap gold fade d5">TEDHAK SITEN</p></div>
    {oval('/assets/img/cover.jpg', alt='Giaksa dan Giakta')}
    <div class="L txt hero-text" style="--x:0;--y:522;--w:500">
      <h2 class="name-l fade d5">Kagiaksa &amp; Kagiakta</h2>
      <p class="date fade d5">Minggu, 29 November 2026</p>
    </div>
    {bottom_set(peacock=True, wide=False)}
  </section>

  <!-- ================= TEDHAK SITEN MEANING ================= -->
  <section class="sec about" id="about">
    <div class="about-bg" style="background-image:url(/assets/img/orang-tua.jpg)"></div>
    <div class="about-shade"></div>
    <div class="about-text">
      <h3 class="about-title from-bottom"><span></span>Tedhak Sitèn<span></span></h3>
      <p class="from-bottom d2">Tedhak Sitèn /te·dhak/ v. Turun /si·tèn/ n. Tanah. Upacara Tedhak Sitèn merupakan prosesi tradisional adat Jawa yang umumnya diselenggarakan ketika seorang anak mulai belajar menginjak tanah dan berjalan. Pelaksanaan upacara ini merupakan bentuk syukur kami atas kelahiran putra kembar kami, serta mencakup harapan kami mengajarkan anak tentang konsep kemandirian, tanggung jawab, tangguh dalam menghadapi persoalan, serta bersifat dermawan terhadap sesamanya.</p>
    </div>
  </section>

  <!-- ================= SALAM + CHILDREN ================= -->
  <section class="sec kids dome" id="anak">
    {forest()}
    {top_set()}
    <div class="flow">
      <p class="script from-bottom">Assalamu&#8217;alaikum Wr. Wb.</p>
      <p class="body from-bottom d2">Dengan memohon rahmat dan ridho Allah Subhanahu Wa Ta&#8217;ala, InsyaAllah kami akan menyelenggarakan acara Tedhak Siten untuk kedua anak kami:</p>

      <div class="kid">
        <div class="arch-wrap zoomblur d2">
          <div class="frame-arch"><img src="/assets/img/giaksa.jpg" alt="Kagiaksa Faeyza Le Givanzka" loading="lazy"></div>
          <img class="kid-stem l a-fla" src="{A}stem-a.webp" alt="">
          <img class="kid-stem r a-fla2" src="{A}stem-b.webp" alt="">
        </div>
        <h3 class="name-m from-bottom">Kagiaksa Faeyza Le Givanzka</h3>
      </div>

      <p class="amp from-bottom">&amp;</p>

      <div class="kid">
        <div class="arch-wrap zoomblur d2">
          <div class="frame-arch"><img src="/assets/img/giakta.jpg" alt="Kagiakta Raeyza Le Givanzka" loading="lazy"></div>
          <img class="kid-stem l a-fla" src="{A}stem-a.webp" alt="">
          <img class="kid-stem r a-fla2" src="{A}stem-b.webp" alt="">
        </div>
        <h3 class="name-m from-bottom">Kagiakta Raeyza Le Givanzka</h3>
      </div>

      <div class="parents from-bottom d2">
        <p>Putra dari :</p>
        <p class="pn">Bapak Bogiva Mirdyanto</p>
        <p>&amp;</p>
        <p class="pn">Ibu Gienzka</p>
      </div>
    </div>
    {bottom_set(bouquets=False)}
  </section>

  <!-- ================= COUNTDOWN (Candi) ================= -->
  <section class="sec countdown" id="countdown">
    {forest()}
    <div class="candi-wrap zoomin">
      <div class="door-view" style="background-image:url({A}forest.webp)"></div>
      <img class="candi" src="{A}candi.webp" alt="Candi">
      <div class="door-content">
        <p class="body sm">Giaksa &amp; Giakta akan menjalani prosesi Tedhak Siten, dan kami ingin Anda menjadi bagian dari hari istimewa kami!</p>
        <div class="timer">
          <div><b id="cd-d">00</b><span>Hari</span></div>
          <div><b id="cd-h">00</b><span>Jam</span></div>
          <div><b id="cd-m">00</b><span>Menit</span></div>
          <div><b id="cd-s">00</b><span>Detik</span></div>
        </div>
        <p class="date">Minggu, 29 November 2026</p>
        <a class="btn" id="saveDate" target="_blank" rel="noopener">{ico('cal')} Simpan Tanggal</a>
      </div>
    </div>
    {L('cloud', 300, 40, 200, cls='cloud c12')}
    {L('cloud', 20, 120, 130, cls='cloud c10')}
    {bottom_set(peacock=True, wide=False)}
  </section>

  <!-- ================= EVENT ================= -->
  <section class="sec event" id="event">
    {forest('dim')}
    <div class="capsule from-top">
      {forest()}
      {L('garland', -103, -8, 618, ent='fade d3')}
      {L('cloud', 230, 4, 206, cls='cloud c12')}
      {L('cloud', -20, 10, 124, cls='cloud c10')}
      <div class="cap-content">
        <img class="emblem zoomin d2" src="{A}emblem.webp" alt="">
        <h3 class="ev-title from-bottom d2">TEDHAK SITEN</h3>
        <p class="ev-big from-bottom d3">MINGGU<br>29 NOVEMBER 2026</p>
        <p class="ev-time from-bottom d3">Pukul 13.00 WIB s.d. Selesai</p>
        <div class="rule"></div>
        <p class="ev-place from-bottom d5">Podomoro Golf View, Cluster Juniper 8/12</p>
        <p class="ev-addr from-bottom d5">Tapos, Depok</p>
        <a class="btn from-bottom d5" href="https://maps.app.goo.gl/UvSDBrSH3n6os9UJ9" target="_blank" rel="noopener">{ico('search')} Lihat Maps</a>
        <div class="rule icon">{ico('mark')}</div>
        <p class="dc-label from-bottom">Dress Code</p>
        <p class="dc-value from-bottom">Batik / Cokelat / Krem</p>
      </div>
      {L('flowerbed', -103, b=-12, w=618, ent='from-bottom')}
      {L('butterfly-b', 20, b=40, w=41, anim='a-stop2', ent='fade d6')}
      {L('butterfly-a', 359, b=90, w=54, anim='a-stop', ent='fade d6')}
    </div>
  </section>

  <!-- ================= GALLERY ================= -->
  <section class="sec gallery" id="gallery">
    {forest()}
    {top_set()}
    <div class="flow">
      <div class="title-cloud"><img class="cloud-static" src="{A}cloud.webp" alt=""><h3 class="sec-title zoomin">OUR GALLERY</h3></div>
      <div class="grid" id="galleryGrid"></div>
    </div>
  </section>

  <!--
    UCAPAN & RSVP : ditunda dulu karena butuh database. Lihat README.
  -->

  <!-- ================= CLOSING ================= -->
  <section class="sec closing" id="closing">
    {forest()}
    {top_set()}
    <div class="flow">
      <div class="oval-inline zoomblur">
        <div class="frame-oval static"><img src="/assets/img/penutup.jpg" alt="Keluarga Bogiva dan Gienzka" loading="lazy"></div>
        <img class="kid-stem l a-fla" src="{A}stem-a.webp" alt="">
        <img class="kid-stem r a-fla2" src="{A}stem-b.webp" alt="">
      </div>
      <p class="body from-bottom">Atas kehadiran dan do&#8217;a dari Bapak/Ibu/Saudara/i sekalian, kami mengucapkan Terima Kasih.</p>
      <p class="script sm from-bottom d2">Wassalamu&#8217;alaikum Wr. Wb.</p>
      <p class="body from-bottom d3">Kami yang berbahagia</p>
      <p class="name-l from-bottom d3">Bogiva &amp; Gienzka</p>
      <p class="body it from-bottom d3">beserta Giaksa &amp; Giakta</p>
    </div>
    {bottom_set(bouquets=False)}
  </section>

  <nav class="dock" id="dock" aria-label="Navigasi">
    <a href="#home" data-label="Home">{ico('home')}</a>
    <a href="#anak" data-label="Anak">{ico('kids')}</a>
    <a href="#countdown" data-label="Acara">{ico('event')}</a>
    <a href="#gallery" data-label="Galeri">{ico('gallery')}</a>
    <a href="#closing" data-label="Penutup">{ico('heart')}</a>
  </nav>
  <button class="music" id="musicBtn" type="button" aria-label="Musik" hidden>{ico('music')}</button>
  <audio id="bgm" src="/music.mp3" loop preload="none"></audio>
</main>

<div class="lightbox" id="lightbox" hidden>
  <button class="lb-close" id="lbClose" aria-label="Tutup">&#215;</button>
  <button class="lb-nav prev" id="lbPrev" aria-label="Sebelumnya">&#8249;</button>
  <img id="lbImg" alt="">
  <button class="lb-nav next" id="lbNext" aria-label="Berikutnya">&#8250;</button>
</div>

<script src="/script.js"></script>
</body>
</html>
'''

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
open(os.path.join(root, 'public', 'index.html'), 'w').write(HTML)
print('index.html written', len(HTML))
