/* Keep121 — site interactions */
(() => {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const NS = 'http://www.w3.org/2000/svg';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Fills {name} placeholders in a UI string.
  const tx = (s, v) => v ? s.replace(/\{(\w+)\}/g, (_, k) => v[k]) : s;
  const won = n => n.toLocaleString('ko-KR') + '원';
  const svgEl = (tag, attrs) => {
    const el = document.createElementNS(NS, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    return el;
  };

  /* ---------- Nav ---------- */
  const nav = $('#nav');
  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  const toggle = $('#navToggle');
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
    if (open) nav.classList.add('scrolled');
    else onScroll();
  });
  $$('#navLinks a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }));

  /* ---------- Sub-page section tabs ---------- */
  const subLinks = $$('#subnav a');
  const sectionObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      subLinks.forEach(a => {
        const on = a.getAttribute('href') === '#' + e.target.id;
        a.classList.toggle('active', on);
        if (on) a.parentElement.scrollLeft = a.offsetLeft - 24;   // keep the active tab visible on narrow screens
      });
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  subLinks.forEach(a => {
    const sec = $(a.getAttribute('href'));
    if (sec) sectionObserver.observe(sec);
  });

  /* ---------- Reveal on scroll ---------- */
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); revealObserver.unobserve(e.target); }
    });
  }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  $$('.reveal').forEach(el => revealObserver.observe(el));

  /* ---------- Hero motion "video": 4 auto-playing scenes ---------- */
  (function heroVideo() {
    const root = $('#heroVideo');
    if (!root) return;
    const scenes = $$('.hv-scene', root), panels = $$('.hv-panel', root);
    const chapters = $$('#hvChapters button'), fills = chapters.map(b => $('i b', b));
    const playBtn = $('#hvPlay'), caption = $('#hvCaption');
    const CAPTIONS = [
      '09:10 · 호이안 — 정차지 점호, 명찰 탭으로 26명 28초',
      '14:20 · 휴게소 — 버스 출발 3분 안에, 타지 않은 한 명을 알아챕니다',
      '14:23 · Keep Tag가 위치를 알려주고, 가이드가 직접 확인합니다',
      '18:42 · 가족에게는 “호텔 도착, 가이드 확인됨” 한 줄',
    ].map(s => tx(s));
    const DUR = [5200, 6000, 6000, 5600];

    // scene 1 radar: 26 dots appear one by one
    const dotsG = $('#hvDots');
    for (let i = 0; i < 26; i++) {
      const a = i * 2.39996, r = 18 + Math.sqrt(i / 26) * 46;
      const c = svgEl('circle', { cx: (120 + Math.cos(a) * r).toFixed(1), cy: (120 + Math.sin(a) * r).toFixed(1), r: 4.5 });
      c.style.animationDelay = (0.3 + i * 0.06) + 's';
      dotsG.appendChild(c);
    }
    const counter = $('.hv-count', root);
    function countUp() {
      const t0 = performance.now();
      const tick = now => {
        const k = Math.min(1, (now - t0 - 300) / 1600);
        counter.textContent = Math.max(0, Math.round(k * 26));
        if (k < 1 && cur === 0) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }

    let cur = 0, elapsed = 0, last = 0, playing = !reduceMotion, visible = true, raf = 0;
    function show(i) {
      cur = i; elapsed = 0;
      scenes.forEach((s, k) => s.classList.toggle('on', k === i));
      panels.forEach((p, k) => {
        p.classList.remove('on');
        if (k === i) { void p.offsetWidth; p.classList.add('on'); }   // restart entrance animations
      });
      chapters.forEach((b, k) => b.classList.toggle('on', k === i));
      fills.forEach((f, k) => f.style.width = k < i ? '100%' : '0%');
      caption.textContent = CAPTIONS[i];
      if (i === 0) countUp();
      // replay the Ken Burns move on the photo
      const img = $('img', scenes[i]); img.style.animation = 'none'; void img.offsetWidth; img.style.animation = '';
    }
    function frame(now) {
      raf = requestAnimationFrame(frame);
      const dt = last ? now - last : 0; last = now;
      if (!playing || !visible) return;
      elapsed += dt;
      fills[cur].style.width = Math.min(100, elapsed / DUR[cur] * 100) + '%';
      if (elapsed >= DUR[cur]) show((cur + 1) % scenes.length);
    }
    function setPlaying(on) {
      playing = on;
      playBtn.classList.toggle('paused', !on);
      playBtn.setAttribute('aria-label', tx(on ? '일시정지' : '재생'));
    }
    playBtn.addEventListener('click', () => setPlaying(!playing));
    chapters.forEach(b => b.addEventListener('click', () => { show(+b.dataset.i); }));
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; }, { threshold: .15 }).observe(root);
    document.addEventListener('visibilitychange', () => { last = 0; });

    show(0);
    setPlaying(playing);
    if (reduceMotion) fills[0].style.width = '100%';
    raf = requestAnimationFrame(frame);
  })();

  /* ---------- Roll-call demo: NFC taps, BLE candidates, departure alert ---------- */
  (function rollcall() {
    const grid = $('#rc2Grid');
    if (!grid) return;
    const TOTAL = 26, CAND = [5, 21], LATE = 9, MISSING = 14;
    const numEl = $('#rc2Num'), msgEl = $('#rc2Msg'), timeEl = $('#rc2Time');
    const startBtn = $('#rc2Start'), confirmBtn = $('#rc2Confirm'), departBtn = $('#rc2Depart');
    const badges = Array.from({ length: TOTAL }, (_, i) => {
      const b = document.createElement('span');
      b.className = 'b';
      b.textContent = String(i + 1).padStart(2, '0');
      grid.appendChild(b);
      return b;
    });
    const timers = [];
    let count = 0;
    const later = (fn, ms) => timers.push(setTimeout(fn, reduceMotion ? 0 : ms));
    const set = (n, cls) => { badges[n - 1].className = 'b ' + cls; };
    const setCount = n => { count = n; numEl.textContent = n; };
    const setTime = s => { timeEl.textContent = tx('{n}초', { n: s }); };
    const enable = (btn, on) => { btn.disabled = !on; };

    function reset() {
      timers.splice(0).forEach(clearTimeout);
      badges.forEach(b => { b.className = 'b'; });
      setCount(0); setTime(0);
      msgEl.textContent = tx('① 점호를 시작하세요. 여행객은 가이드 휴대폰에 명찰을 대기만 하면 됩니다.');
      enable(confirmBtn, false); enable(departBtn, false);
    }
    function start() {
      reset();
      enable(startBtn, false);
      startBtn.textContent = tx('다시 하기');
      msgEl.textContent = tx('명찰을 탭하는 중…');
      const taps = badges.map((_, i) => i + 1).filter(n => !CAND.includes(n) && n !== LATE && n !== MISSING);
      for (let i = taps.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [taps[i], taps[j]] = [taps[j], taps[i]]; }
      taps.forEach((n, k) => later(() => {
        set(n, 'in tap');
        later(() => badges[n - 1].classList.remove('tap'), 180);
        setCount(k + 1);
        setTime(Math.round((k + 1) * 1.1));
      }, 120 * (k + 1)));
      later(() => {
        CAND.forEach(n => set(n, 'cand'));
        [LATE, MISSING].forEach(n => set(n, 'miss'));
        msgEl.innerHTML = tx('<b>{n}/26 확인</b> · BLE 근접 후보 2명(05, 21번)은 가이드가 한 번 확인합니다.', { n: count });
        enable(confirmBtn, true); enable(startBtn, true);
      }, 120 * taps.length + 400);
    }
    function confirm() {
      enable(confirmBtn, false);
      CAND.forEach(n => set(n, 'in'));
      setCount(count + CAND.length);
      setTime(28);
      msgEl.innerHTML = tx('<b>미확인 2명</b> · 09번 김○자 님, 14번 박○순 님. 화면에는 찾아야 할 사람만 남습니다.');
      later(() => {
        set(LATE, 'in tap');
        setCount(count + 1);
        msgEl.innerHTML = tx('09번이 돌아와 명찰을 탭했습니다. <b>미확인 1명</b> · 14번 박○순 님.');
        enable(departBtn, true);
      }, 1400);
    }
    function depart() {
      enable(departBtn, false);
      msgEl.textContent = tx('버스 출발 · 미승차 확인 중…');
      later(() => {
        badges[MISSING - 1].classList.add('tap');
        msgEl.innerHTML = tx('<b>출발 2분 40초 · 미승차 1명</b> · 14번 Keep Tag 위치: 2번 버스 옆 140m. 가이드가 확인하면 “확인함” 라벨이 기록됩니다.');
      }, 1200);
    }
    startBtn.addEventListener('click', start);
    confirmBtn.addEventListener('click', confirm);
    departBtn.addEventListener('click', depart);
    reset();
  })();

  /* ---------- Quote calculator (business plan prices) ---------- */
  (function calc() {
    const p = $('#cPeople'), d = $('#cDays'), t = $('#cTours');
    if (!p) return;
    const TEAM_MIN = { tag: 150000, check: 40000 };
    const CONSOLE = 49000, KIT_MONTH = 390000, KIT_PER = 2000;
    let product = 'tag', round = 1;
    const unitPrice = days => product === 'check' ? 2000
      : days <= 2 ? 5900 : days <= 6 ? 8900 : days <= 10 ? 11900 : 11900 + (days - 10) * 1000;
    const fill = el => el.style.setProperty('--p', ((el.value - el.min) / (el.max - el.min) * 100) + '%');
    const seg = (id, onPick) => $$('#' + id + ' button').forEach(b => b.addEventListener('click', () => {
      $$('#' + id + ' button').forEach(x => x.classList.toggle('on', x === b));
      onPick(b.dataset.v);
      update();
    }));
    function update() {
      const people = +p.value, days = +d.value, tours = +t.value;
      const unit = unitPrice(days);
      const raw = people * unit, min = TEAM_MIN[product];
      const team = Math.max(raw, min);
      const tour = Math.round(team * round);
      const consoleFee = tours < 4 ? CONSOLE : 0;
      const month = team * tours + consoleFee;
      $('#oPeople').textContent = tx('{n}명', { n: people });
      $('#oDays').textContent = tx('{n}일', { n: days });
      $('#oTours').textContent = tx('{n}회', { n: tours });
      $('#rUnit').textContent = tx('{w} / 인', { w: won(unit) });
      $('#lTeam').textContent = raw < min ? tx('팀 금액 (팀 최소 {w} 적용)', { w: won(min) }) : tx('팀 금액 ({n}명 × {w})', { n: people, w: won(unit) });
      $('#rTeam').textContent = won(team);
      $('#rTour').textContent = won(tour);
      $('#rPer').textContent = won(Math.round(tour / people / 10) * 10);
      $('#rMonth').textContent = won(month);
      const hint = $('#rHint');
      if (product === 'check') {
        hint.innerHTML = tx('Keep Check는 회수가 없고 위치를 저장하지 않는 진입 상품입니다. 이탈 시 위치 확인이 필요하면 <b>Keep Tag</b>로 전환하세요.');
      } else if (tours >= 4) {
        const kit = KIT_MONTH + KIT_PER * people * tours;
        hint.innerHTML = kit < month
          ? tx('같은 운영량이면 <b>상주 키트 월 {k}</b>로 {s} 줄어듭니다. (2028 출시 · 12개월 약정)', { k: won(kit), s: won(month - kit) })
          : tx('이 운영량에서는 렌탈이 상주 키트(월 {k})보다 유리합니다.', { k: won(kit) });
      } else {
        hint.innerHTML = tx('월 4투어 미만은 여행사 콘솔 월 <b>{w}</b>이 포함됩니다. 4투어 이상이면 무료입니다.', { w: won(CONSOLE) });
      }
      [p, d, t].forEach(fill);
    }
    seg('cProduct', v => { product = v; });
    seg('cRound', v => { round = +v; });
    [p, d, t].forEach(el => el.addEventListener('input', update));
    update();
  })();

  /* ---------- Contact form (demo) ---------- */
  const form = $('#contactForm');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const v = n => (form.elements[n].value || '').trim();
    const subject = `[Keep121 문의] ${v('type')}${v('org') ? ' · ' + v('org') : ''}`;
    const body = [`이름: ${v('name')}`, `소속: ${v('org')}`, `문의 유형: ${v('type')}`, `연락처: ${v('contact')}`, '', v('message')].join('\n');
    location.href = `mailto:${form.dataset.mail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    $('#formNote').classList.add('show');
  });
})();
