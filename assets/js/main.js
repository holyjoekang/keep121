/* Keep121 — site interactions */
(() => {
  'use strict';

  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const NS = 'http://www.w3.org/2000/svg';
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
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
      '10:00 · 리장 — 26명, 버튼 한 번으로 인원 확인',
      '14:20 · 휴게소 — 한 분이 다른 버스에 올랐습니다. 전화는 받지 않습니다.',
      '14:23 · 태그가 대답합니다 — Keep121 Guide 앱에 위치가 뜹니다',
      '14:31 · 가족에게는, 가이드가 확인한 한 줄만',
    ];
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
      playBtn.setAttribute('aria-label', on ? '일시정지' : '재생');
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

  /* ---------- Hero flock animation ---------- */
  (function hero() {
    const g = $('#heroDots');
    if (!g) return;
    const C = 280, FENCE = 122, PX_PER_M = FENCE / 10, LOST = 13; // member #14
    const golden = Math.PI * (3 - Math.sqrt(5));
    const members = Array.from({ length: 26 }, (_, i) => {
      const r = 36 + ((i * 53) % 62);
      const a = i * golden;
      const el = svgEl('circle', { r: 7.5, fill: '#B4BEF0', stroke: '#141A2E', 'stroke-width': 2.5 });
      g.appendChild(el);
      return { r, a, el, ph: Math.random() * 6.28, sp: .4 + Math.random() * .5 };
    });
    const lost = members[LOST];
    const label = svgEl('text', { 'font-size': 12, 'font-weight': 800, fill: '#fff', 'text-anchor': 'middle', opacity: 0 });
    label.textContent = '14';
    g.appendChild(label);

    const tether = $('#heroTether'), num = $('#heroNum'), state = $('#heroState'), bar = $('#heroBar'), alertCard = $('#heroAlert');
    const OUT_R = 222, CYCLE = 11000;
    const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    let wasOut = null;

    function frame(ts) {
      const t = reduceMotion ? 0 : ts % CYCLE;
      let k = 0;
      if (t > 4000 && t <= 6500) k = ease((t - 4000) / 2500);
      else if (t > 6500 && t <= 9500) k = 1;
      else if (t > 9500 && t <= 11000) k = 1 - ease((t - 9500) / 1500);

      members.forEach((m, i) => {
        const wob = reduceMotion ? 0 : Math.sin(ts / 1000 * m.sp + m.ph) * 4;
        let r = m.r + wob, a = m.a + (reduceMotion ? 0 : Math.sin(ts / 2400 + m.ph) * .05);
        if (i === LOST) r = m.r + (OUT_R - m.r) * k;
        m.x = C + Math.cos(a) * r;
        m.y = C + Math.sin(a) * r;
        m.el.setAttribute('cx', m.x.toFixed(1));
        m.el.setAttribute('cy', m.y.toFixed(1));
        m.cr = r;
      });

      const out = lost.cr > FENCE;
      lost.el.setAttribute('fill', out ? '#D64545' : '#B4BEF0');
      lost.el.setAttribute('r', out ? 10 : 7.5);
      tether.setAttribute('x2', lost.x.toFixed(1));
      tether.setAttribute('y2', lost.y.toFixed(1));
      tether.setAttribute('opacity', out ? .9 : 0);
      label.setAttribute('x', lost.x.toFixed(1));
      label.setAttribute('y', (lost.y - 16).toFixed(1));
      label.setAttribute('opacity', out ? 1 : 0);

      if (out !== wasOut) {
        wasOut = out;
        num.textContent = out ? 25 : 26;
        bar.style.width = out ? '96%' : '100%';
        bar.style.background = out ? 'var(--coral)' : 'var(--mint)';
        state.classList.toggle('warn', out);
        state.querySelector('span').textContent = out ? '1명 확인 필요' : '전원 확인 완료';
        state.querySelector('use').setAttribute('href', out ? '#i-alert' : '#i-check');
        alertCard.classList.toggle('show', out);
      }
      if (out) $('#heroDist').textContent = Math.round(lost.cr / PX_PER_M);
      if (!reduceMotion) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  })();

  /* ---------- Roll-call demo ---------- */
  (function rollcall() {
    const dotsG = $('#rcDots');
    if (!dotsG) return;
    const C = 210;
    // Non-linear metres → px so the tight core of the group stays readable (5m→70, 10m→110, 20m→160).
    const toPx = d => d <= 5 ? 18 + d * 10.4 : d <= 10 ? 70 + (d - 5) * 8 : d <= 20 ? 110 + (d - 10) * 5 : 192;
    const DIST = [2.1, 3.4, 7.2, 1.6, 4.1, 2.8, 12.4, 3.9, 1.2, 4.4, 2.5, 3.1, 4.6, 82, 1.9, 3.6, 2.3, 4.0, 16.3, 2.9, 3.3, 8.6, 1.4, 4.2, 2.7, 3.0];
    const golden = Math.PI * (3 - Math.sqrt(5));
    const chipsEl = $('#rcChips'), fence = $('#rcFence'), svg = $('#rcSvg');
    const resultEl = $('#rcResult'), numEl = $('#rcNum');
    let radius = 10, busy = false;

    const people = DIST.map((d, i) => {
      const n = i + 1;
      const a = n === 14 ? -Math.PI / 5 : i * golden + .4;
      const r = toPx(d);
      const x = C + Math.cos(a) * r, y = C + Math.sin(a) * r;
      const grp = svgEl('g', { class: 'rc-dot' });
      const c = svgEl('circle', { cx: x, cy: y, r: 9.5, fill: '#3b5672', stroke: '#141A2E', 'stroke-width': 2 });
      const t = svgEl('text', { x, y: y + 3.5, 'text-anchor': 'middle', 'font-size': 9, 'font-weight': 800, fill: '#fff' });
      t.textContent = n;
      grp.append(c, t);
      if (n === 14) {
        const lbl = svgEl('text', { x: x + 16, y: y - 10, 'font-size': 11, 'font-weight': 800, fill: '#E06A6A' });
        lbl.textContent = '82m →';
        grp.appendChild(lbl);
      }
      dotsG.appendChild(grp);
      const chip = document.createElement('span');
      chip.className = 'chip';
      chip.textContent = String(n).padStart(2, '0');
      chipsEl.appendChild(chip);
      return { n, d, c, chip };
    });

    function setRadius(r) {
      radius = r;
      fence.setAttribute('r', toPx(r));
      fence.style.r = toPx(r) + 'px';
      $$('#rcRadius button').forEach(b => b.classList.toggle('on', +b.dataset.r === r));
      reset();
    }
    function reset() {
      people.forEach(p => { p.c.setAttribute('fill', '#3b5672'); p.chip.className = 'chip'; });
      numEl.textContent = '–';
      resultEl.className = 'rc-result';
      resultEl.querySelector('.msg').textContent = '버튼을 눌러 반경 안의 인원을 확인하세요.';
    }
    function check() {
      if (busy) return;
      busy = true;
      reset();
      svg.classList.remove('scanning');
      void svg.getBoundingClientRect();
      svg.classList.add('scanning');
      setTimeout(() => {
        const missing = [];
        people.forEach(p => {
          const inside = p.d <= radius;
          p.c.setAttribute('fill', inside ? '#3E8E6E' : '#D64545');
          p.chip.className = 'chip ' + (inside ? 'in' : 'out');
          if (!inside) missing.push(p);
        });
        const count = 26 - missing.length;
        numEl.textContent = count;
        resultEl.className = 'rc-result ' + (missing.length ? 'warn' : 'ok');
        const msg = resultEl.querySelector('.msg');
        msg.innerHTML = missing.length
          ? `<b>미확인 ${missing.length}명</b> · ` + missing.map(p => `${p.n}번(${p.d}m)`).join(', ')
          : '<b>전원 확인 완료</b> · 출발해도 좋습니다.';
        svg.classList.remove('scanning');
        busy = false;
      }, reduceMotion ? 50 : 1300);
    }
    $$('#rcRadius button').forEach(b => b.addEventListener('click', () => setRadius(+b.dataset.r)));
    $('#rcCheck').addEventListener('click', check);
    setRadius(10);
  })();

  /* ---------- Live map demo (Leaflet) ---------- */
  (function liveMap() {
    const mapEl = $('#liveMap');
    if (!mapEl) return;

    const ICN = [37.4602, 126.4407], LJG = [26.6799, 100.2457];
    const SPOTS = [
      { name: '리장 고성', time: '08:30', ll: [26.8721, 100.2353], st: 'done' },
      { name: '옥룡설산 빙천공원', time: '10:40', ll: [27.1012, 100.1905], st: 'now' },
      { name: '람월곡', time: '14:30', ll: [27.1135, 100.2410], st: 'next' },
      { name: '인상리장 공연', time: '16:30', ll: [27.0962, 100.2276], st: '' },
    ];
    const GROUP = SPOTS[1].ll;
    const MOM = 11, LOST = 13;
    const FENCE_M = 20;

    // Itinerary lists in the side panel
    const itin = SPOTS.map(s => `<li class="${s.st}"><span class="dot"></span><span>${s.name}${s.st === 'now' ? '<span class="badge">현재</span>' : s.st === 'next' ? '<span class="badge next">다음</span>' : ''}</span><time>${s.time}</time></li>`).join('');
    $('#itinGuide').innerHTML = itin;
    $('#itinFamily').innerHTML = itin;

    let map, started = false;
    const io = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && !started) { started = true; io.disconnect(); init(); }
    }, { threshold: .25 });
    io.observe(mapEl);

    function init() {
      if (!window.L) {
        // Leaflet loads with `defer`; wait briefly before falling back.
        let tries = 0;
        const wait = setInterval(() => {
          if (window.L) { clearInterval(wait); build(); }
          else if (++tries > 40) { clearInterval(wait); $('#mapFallback').classList.add('show'); }
        }, 150);
        return;
      }
      build();
    }

    function build() {
      const L = window.L;
      const small = mapEl.clientWidth < 640;
      map = L.map(mapEl, {
        zoomControl: false, scrollWheelZoom: false, attributionControl: true,
        minZoom: 2, maxZoom: 20, worldCopyJump: true,
      }).setView([32, 112], small ? 3 : 4);
      L.control.zoom({ position: 'bottomleft' }).addTo(map);

      // OSM tiles suit a demo; switch to a keyed provider (e.g. Google Maps, Mapbox) for production traffic.
      const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxNativeZoom: 19, maxZoom: 20,
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);
      let tileErrors = 0;
      tiles.on('tileerror', () => { if (++tileErrors > 25) $('#mapFallback').classList.add('show'); });
      tiles.on('tileload', () => { tileErrors = 0; });

      // Flight arc ICN → LJG
      const ctrl = [37.5, 110];
      const arc = [];
      for (let i = 0; i <= 48; i++) {
        const t = i / 48, u = 1 - t;
        arc.push([u * u * ICN[0] + 2 * u * t * ctrl[0] + t * t * LJG[0], u * u * ICN[1] + 2 * u * t * ctrl[1] + t * t * LJG[1]]);
      }
      const label = (ll, text, cls = '') => L.marker(ll, {
        icon: L.divIcon({ className: '', html: `<div class="spot-pin ${cls}"><i></i><span>${text}</span></div>`, iconSize: [0, 0] }),
        keyboard: false,
      });
      const world = L.layerGroup([
        L.polyline(arc, { color: '#141A2E', weight: 2.5, dashArray: '6 8', opacity: .8 }),
        label(ICN, '인천'), label(LJG, '윈난 · 리장', 'now'),
      ]).addTo(map);

      // Day route + spots
      const route = L.layerGroup([
        L.polyline(SPOTS.map(s => s.ll), { color: '#3E8E6E', weight: 4, opacity: .9, dashArray: '2 9', lineCap: 'round' }),
        ...SPOTS.map(s => label(s.ll, `${s.time} ${s.name}`, s.st === 'now' ? 'now' : '')),
      ]);

      // Group: guide, fence, members
      const mToLat = m => m / 111320;
      const mToLng = m => m / (111320 * Math.cos(GROUP[0] * Math.PI / 180));
      const golden = Math.PI * (3 - Math.sqrt(5));
      const members = Array.from({ length: 26 }, (_, i) => {
        const d = 4 + ((i * 37) % 90) / 10; // 4 – 13m
        const a = i * golden;
        const m = { i, base: d, a, d, ph: Math.random() * 6.28 };
        m.marker = L.circleMarker([0, 0], { radius: 7, color: '#fff', weight: 2.5, fillColor: '#3E8E6E', fillOpacity: 1 })
          .bindTooltip(`${i + 1}번`, { className: 'member-tip', direction: 'top', offset: [0, -6] });
        return m;
      });
      const fence = L.circle(GROUP, { radius: FENCE_M, color: '#3E8E6E', weight: 2, dashArray: '6 7', fillColor: '#3E8E6E', fillOpacity: .12 });
      const tether = L.polyline([GROUP, GROUP], { color: '#D64545', weight: 2, dashArray: '4 6' });
      const guide = L.marker(GROUP, {
        icon: L.divIcon({ className: '', html: '<div class="guide-pin"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="6.5" y="2.5" width="11" height="19" rx="2.8"/><path d="M10.5 18.5h3"/></svg></div>', iconSize: [34, 34], iconAnchor: [17, 17] }),
        zIndexOffset: 1000,
      }).bindTooltip('가이드', { className: 'member-tip', direction: 'top', offset: [0, -16] });
      const group = L.layerGroup([fence, tether, ...members.map(m => m.marker), guide]);

      function place(m) {
        const ll = [GROUP[0] + mToLat(Math.sin(m.a) * m.d), GROUP[1] + mToLng(Math.cos(m.a) * m.d)];
        m.marker.setLatLng(ll);
        m.ll = ll;
      }
      members.forEach(place);

      // Zoom-based layer visibility
      const syncLayers = () => {
        const z = map.getZoom();
        z <= 8 ? world.addTo(map) : world.remove();
        z >= 10 && z < 17 ? route.addTo(map) : route.remove();
        z >= 16 ? group.addTo(map) : group.remove();
      };
      map.on('zoomend', syncLayers);
      syncLayers();

      // HUD steps & zoom-in sequence
      const hudBtns = $$('#mapHud button');
      const setHud = i => hudBtns.forEach(b => b.classList.toggle('on', +b.dataset.step === i));
      const routeBounds = L.latLngBounds(SPOTS.map(s => s.ll)).pad(.35);
      let token = 0;
      const views = [
        (anim) => map.flyTo([32, 112], small ? 3 : 4, { duration: anim ? 2.2 : 0, animate: anim }),
        (anim) => map.flyToBounds(routeBounds, { duration: anim ? 2.6 : 0, animate: anim }),
        (anim) => map.flyTo([GROUP[0] - mToLat(8), GROUP[1] + mToLng(14)], small ? 18 : 19, { duration: anim ? 2.6 : 0, animate: anim }),
      ];
      function go(i, anim = !reduceMotion) {
        setHud(i);
        views[i](anim);
      }
      function play() {
        const my = ++token;
        go(0, false);
        const next = (i, delay) => setTimeout(() => {
          if (my !== token) return;
          go(i);
          if (i < 2) map.once('moveend', () => next(i + 1, 1200));
        }, delay);
        next(1, 1300);
      }
      hudBtns.forEach(b => b.addEventListener('click', () => { token++; go(+b.dataset.step); }));
      $('#mapReplay').addEventListener('click', play);
      reduceMotion ? go(2, false) : play();

      // Live simulation: member #14 drifts away, then returns
      const numEl = $('#liveNum'), stateEl = $('#liveState'), alertEl = $('#liveAlert'), distEl = $('#liveDist');
      let tick = 0, view = 'guide';
      const lost = members[LOST];
      lost.a = -0.6;
      function step() {
        tick = (tick + 1) % 30;
        members.forEach(m => {
          if (m.i === LOST) return;
          m.d = m.base + Math.sin(tick / 2 + m.ph) * .8;
          place(m);
        });
        if (tick < 6) lost.d = lost.base;
        else if (tick < 15) lost.d = lost.base + (tick - 5) * 6;
        else if (tick < 24) lost.d = Math.min(lost.d + 1.2, 70);
        else lost.d = Math.max(lost.base, lost.d - 16);
        place(lost);

        const out = lost.d > FENCE_M;
        lost.marker.setStyle({ fillColor: out ? '#D64545' : '#3E8E6E', radius: out ? 9 : 7 });
        tether.setLatLngs(out ? [GROUP, lost.ll] : [GROUP, GROUP]);
        numEl.textContent = out ? 25 : 26;
        stateEl.classList.toggle('warn', out);
        stateEl.textContent = out ? '1명 펜스 밖 · 확인 필요' : `전원 펜스 안 · ${FENCE_M}m`;
        alertEl.classList.toggle('show', out);
        distEl.textContent = Math.round(lost.d);
        applyView();
      }
      function applyView() {
        const fam = view === 'family';
        members.forEach(m => {
          const isMom = m.i === MOM;
          const el = m.marker;
          if (fam && !isMom) { el.setStyle({ opacity: 0, fillOpacity: 0 }); return; }
          el.setStyle({ opacity: 1, fillOpacity: 1 });
          if (isMom) el.setStyle({ fillColor: fam ? '#F2A541' : '#3E8E6E', radius: fam ? 11 : 7 });
        });
        fence.setStyle({ opacity: fam ? 0 : 1, fillOpacity: fam ? 0 : .12 });
        tether.setStyle({ opacity: fam ? 0 : 1 });
      }
      if (!reduceMotion) setInterval(step, 1000);
      step();

      $('#liveAck').addEventListener('click', () => {
        token++;
        setHud(2);
        map.flyTo(lost.ll, 19, { duration: 1.2 });
        tick = 24;
      });

      $$('#viewSeg button').forEach(b => b.addEventListener('click', () => {
        view = b.dataset.view;
        $$('#viewSeg button').forEach(x => x.classList.toggle('on', x === b));
        $('#view-guide').classList.toggle('on', view === 'guide');
        $('#view-family').classList.toggle('on', view === 'family');
        if (view === 'family' && map.getZoom() < 16) { token++; go(2); }
        else if (view === 'family') { members[MOM].marker.openTooltip(); }
        members[MOM].marker.setTooltipContent(view === 'family' ? '어머니 · 12번' : '12번');
        applyView();
      }));
    }
  })();

  /* ---------- Band color picker ---------- */
  (function swatches() {
    const straps = $$('#bandSvg .strap');
    const name = $('#swatchName');
    $$('#swatches .swatch').forEach(s => s.addEventListener('click', () => {
      $$('#swatches .swatch').forEach(x => x.classList.toggle('on', x === s));
      straps.forEach(r => r.setAttribute('fill', s.dataset.c));
      name.textContent = s.dataset.n;
    }));
  })();

  /* ---------- Travel memory days ---------- */
  (function memory() {
    const DAYS = [
      { title: 'DAY 1 · 쿤밍 도착, 리장 고성으로', spots: [
        { t: '09:40', n: '쿤밍 창수이 국제공항', d: '윈난성의 관문. 일행 26명 전원 도착을 확인하고 리장으로 이동했어요.', c: '#4A5BB0', i: 'i-pin' },
        { t: '15:20', n: '리장 고성', d: '물길 따라 이어진 나시족의 옛 도시. 1997년 유네스코 세계문화유산에 등재되었어요.', c: '#3E8E6E', i: 'i-camera' },
        { t: '19:00', n: '사방가 야경', d: '고성의 중심 광장. 홍등이 켜진 골목과 나시족 전통 춤이 유명해요.', c: '#a48ef0', i: 'i-heart' },
      ]},
      { title: 'DAY 2 · 옥룡설산과 람월곡', spots: [
        { t: '10:40', n: '옥룡설산 빙천공원', d: '해발 5,596m의 설산. 케이블카로 4,506m 전망대까지 올라 빙하를 가까이에서 봤어요.', c: '#1B2347', i: 'i-mountain' },
        { t: '14:30', n: '람월곡 (블루문밸리)', d: '빙하 녹은 물이 만든 에메랄드빛 계단식 호수. 설산이 비치는 사진 명소예요.', c: '#3E8E6E', i: 'i-camera' },
        { t: '16:30', n: '인상리장 공연', d: '장이머우 감독이 연출한 야외 공연. 설산을 배경으로 한 웅장한 무대를 감상했어요.', c: '#D64545', i: 'i-users' },
      ]},
      { title: 'DAY 3 · 수허 고진과 호도협', spots: [
        { t: '09:30', n: '수허 고진', d: '차마고도의 옛 역참 마을. 리장 고성보다 한적하고 소박한 분위기예요.', c: '#B7791F', i: 'i-route' },
        { t: '13:00', n: '호도협', d: '진사강이 만든 깊은 협곡. 호랑이가 바위를 딛고 건넜다는 전설에서 이름이 왔어요.', c: '#1B2347', i: 'i-mountain' },
        { t: '18:30', n: '나시족 전통 저녁', d: '야크 샤브샤브와 리장 바바(납작하게 구운 빵)를 맛본 저녁이었어요.', c: '#e05470', i: 'i-heart' },
      ]},
    ];
    const list = $('#spotList'), title = $('#dayTitle');
    if (!list) return;
    function render(i) {
      title.textContent = DAYS[i].title;
      list.innerHTML = DAYS[i].spots.map(s => `
        <li><span class="thumb" style="background:${s.c}"><svg class="icon"><use href="#${s.i}"/></svg></span>
        <div><time>${s.t}</time><b>${s.n}</b><p>${s.d}</p></div></li>`).join('');
      $$('#dayTabs button').forEach(b => b.classList.toggle('on', +b.dataset.d === i));
    }
    $$('#dayTabs button').forEach(b => b.addEventListener('click', () => render(+b.dataset.d)));
    render(1);
  })();

  /* ---------- Device lineup: use-case picker ---------- */
  (function picker() {
    const list = $('#pickerList');
    if (!list) return;
    const TIER_LABEL = { lite: 'Keep Tag', plus: 'Keep Tag+', safety: 'Keep Tag+ + 구간 Shelter' };
    const CASES = [
      { name: '효도·패키지', sub: '해외 다일', tier: 'safety', device: 'Keep Tag+ 전원', mode: '케이블카·설산 등 위험 구간만 Shelter', wearer: '어르신',
        a1: '집결지 30m, 자유구역 다각형, 위험 구역 체류 제한 60분', a2: '허브 이탈 180초, 위험 구역 정지 10분',
        config: '위험 노출 80% 감소, 설산 낙상 위치 파악 65분 → 2분', cost: '26명·5일 184,600원' },
      { name: '산악·트레킹', sub: '잔도·절벽', tier: 'safety', device: 'Keep Tag+ 전원 + 허브 2대 (선두·후미)', mode: '잔도·절벽 등 표시 구간만 Shelter', wearer: '일반·어르신',
        a1: '가이드 중심 동적 30m, 후미 허브 기준 낙오 판정', a2: '정지 10분, 음영 구간 신호 끊김은 주의 등급',
        config: '위험 노출 94% 감소 (상시 Shelter면 배터리 1.6일분)', cost: '18명·4일 50,400원' },
      { name: '1일 투어', sub: '국내·해외', tier: 'plus', device: 'Keep Tag+ 전원', mode: '없음 (필요하면 구간 Shelter)', wearer: '일반',
        a1: '차량 펜스(BLE), 시장·혼잡 구역 다각형, 해산지 회수 펜스', a2: '다른 차량 이동, 구역 이탈 3분',
        config: 'Keep Tag+ 39~57% 감소, Keep Tag는 3%', cost: '30명 18,000원' },
      { name: '수학여행·체험학습', sub: '반 단위', tier: 'plus', device: '자유활동 있으면 Keep Tag+, 없으면 Keep Tag', mode: '없음', wearer: '학생',
        a1: '반별 허브(담임 휴대폰), 자유활동 구역 다각형', a2: '허브 이탈 180초 이상 (60초 금지), 반 단위 묶음 알림',
        config: 'Keep Tag+ 58% 감소, 무단 이탈 위치 파악 약 90분 → 12분', cost: '120명·2일 144,000원' },
      { name: '공공 행사·대규모', sub: '수백 명', tier: 'plus', device: 'Keep Tag+ 전원, 고위험 신청자만 Shelter', mode: '없음', wearer: '일반',
        a1: '체크포인트 고정 허브, 코스 이탈', a2: '체크포인트 미통과, 정지 10분',
        config: 'Keep Tag+ 81%·Shelter 96% 감소 (Shelter 전원이면 넘어짐 오감지 하루 10건)', cost: '200명 (고위험 20명) 124,000원 + 설치비' },
      { name: '기업 연수·산행', sub: '인솔 산행', tier: 'lite', device: 'Keep Tag + 허브 2대', mode: '정상부만 Keep Tag+ 대여 (선택)', wearer: '직장인',
        a1: '선두·후미 허브 사이 동적 펜스', a2: '허브 이탈 180초',
        config: 'Keep Tag 74% 감소, Keep Tag+·Shelter와 차이 2~3%', cost: '40명·1일 8,000원' },
      { name: '가족·아이', sub: '놀이공원', tier: 'plus', device: 'Keep Tag+', mode: '없음', wearer: '어린이',
        a1: '부모 휴대폰 2대 = 허브', a2: '허브 이탈 60초, 추적 시작 60초',
        config: 'Keep Tag+ 92% vs Keep Tag 50% 감소', cost: '가격 미정 (여행업 검증 후)' },
    ];
    const REQS = [['device', '기본 단말'], ['mode', '자동 모드 전환'], ['wearer', '착용자']];
    const pickerEl = $('#picker'), tiers = $$('#lineup .tier');

    list.innerHTML = CASES.map((c, i) =>
      `<button role="tab" data-i="${i}"><span>${c.name}</span><small class="t-${c.tier}">${c.tier === 'safety' ? 'Keep Tag+·Shelter' : TIER_LABEL[c.tier]}</small></button>`).join('');

    function show(i) {
      const c = CASES[i];
      pickerEl.className = pickerEl.className.replace(/\bt-\w+/g, '').trim() + ' t-' + c.tier;
      $$('button', list).forEach(b => { const on = +b.dataset.i === i; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
      $('#pkName').textContent = `${c.name} · ${c.sub}`;
      $('#pkTier').textContent = TIER_LABEL[c.tier];
      $('#pkReqs').innerHTML = REQS.map(([k, label]) =>
        `<div class="req${k === 'device' ? ' strong' : ''}"><span class="k">${label}</span><b>${c[k]}</b></div>`).join('');
      $('#pkAxis1').textContent = c.a1;
      $('#pkAxis2').textContent = c.a2;
      $('#pkConfig').textContent = c.config;
      $('#pkCost').textContent = c.cost;
      tiers.forEach(t => t.classList.toggle('match', t.dataset.tier === c.tier || (c.tier === 'safety' && t.dataset.tier === 'plus')));
    }
    list.addEventListener('click', e => { const b = e.target.closest('button'); if (b) show(+b.dataset.i); });
    show(0);
  })();

  /* ---------- Device lineup: Keep Tag+ battery estimate ---------- */
  (function battery() {
    const hours = $('#bHours'), safety = $('#bSafety'), modem = $('#bModem');
    if (!hours) return;
    const CAPACITY = 380, MARGIN = 1.25;            // mAh, efficiency/temperature headroom
    const TRACK_PER_HOUR = 30 * (0.14 + 0.2);        // 2-min fixes: GNSS + uplink per fix
    const SAFETY_PER_HOUR = 19;                      // 1-min fixes + fall detection (sim: trekking ~190mAh / 10h)
    function update() {
      const h = +hours.value, sh = +safety.value;
      const parts = [
        { label: 'BLE 상시 송신 (약 15µA × 24h)', v: 0.4, c: '#4A5BB0' },
        { label: '대기 (모뎀 완전 차단)', v: 1.0, c: '#8A91A8' },
        { label: `허브 이탈 추적 (${h}시간, 2분 간격)`, v: TRACK_PER_HOUR * h, c: '#3E8E6E' },
      ];
      if (sh) parts.push({ label: `Shelter 구간 (${sh}시간, 1분 간격)`, v: SAFETY_PER_HOUR * sh, c: '#B7791F' });
      if (modem.checked) parts.push({ label: '셀룰러 모뎀 대기 유지', v: 20, c: '#D64545' });
      const total = parts.reduce((s, p) => s + p.v, 0);
      const days = CAPACITY / (total * MARGIN);

      $('#oHours').textContent = h + '시간';
      $('#oSafety').textContent = sh + '시간';
      hours.style.setProperty('--p', (h / 4 * 100) + '%');
      safety.style.setProperty('--p', (sh / 12 * 100) + '%');
      $('#batLegend').innerHTML = parts.map(p => `<li><i style="background:${p.c}"></i><span>${p.label}</span><b>${p.v.toFixed(1)}mAh</b></li>`).join('');
      $('#batBar').innerHTML = parts.map(p => `<i style="background:${p.c};width:${p.v / total * 100}%"></i>`).join('');
      $('#bDaily').textContent = total.toFixed(1);
      const d = $('#bDays');
      d.textContent = days > 60 ? '60+' : days < 10 ? days.toFixed(1) : Math.round(days);
      d.classList.toggle('low', days < 3);
      const goal = $('#batGoal');
      goal.classList.toggle('warn', days < 3);
      goal.textContent = days >= 10
        ? '✓ 3일마다, 또는 출발 전 1회 충전으로 충분합니다.'
        : days >= 3
          ? '✓ 위험 구간 전날 밤 케이스 충전을 권장합니다.'
          : '⚠ 매일 밤 케이스 충전 필수 — Shelter를 위험 구간에만 켜는 이유입니다.';
    }
    [hours, safety].forEach(el => el.addEventListener('input', update));
    modem.addEventListener('change', update);
    update();
  })();

  /* ---------- Simulation evidence: dot plot ---------- */
  (function simPlot() {
    const el = $('#simPlot');
    if (!el) return;
    // [team, name, manual, lite, plus, safety] — risk exposure, 241-seed mean; first 5 = free-time incidents
    const T = [
      ['T06', '경주 수학여행', 396, 413, 167, 174],
      ['T02', '규슈 온천 4일', 152, 153, 78, 48],
      ['T04', '서울 1일 투어', 152, 148, 66, 42],
      ['T05', '방콕 1일 투어', 263, 254, 160, 126],
      ['T07', '오사카 수학여행', 37, 34, 19, 19],
      ['T08', '걷기대회 200명', 627, 512, 116, 24],
      ['T01', '윈난 효도 5일', 840, 495, 292, 165],
      ['T10', '가족 놀이공원', 360, 181, 30, 30],
      ['T09', '연수 산행', 169, 43, 40, 39],
      ['T03', '장가계 트레킹', 511, 80, 69, 32],
    ];
    const W = 760, L = 200, R = 736, TOP = 44, ROW = 32, H = TOP + T.length * ROW + 24;
    const MIN = -10, MAX = 100, x = v => L + (v - MIN) / (MAX - MIN) * (R - L);
    const red = (m, v) => (m - v) / m * 100;
    let g = `<rect x="4" y="${TOP - 34}" width="${W - 8}" height="${5 * ROW + 20}" rx="12" class="sp-band"/>` +
            `<text x="16" y="${TOP - 16}" class="sp-axis">자유시간 사고 팀</text>`;
    [0, 25, 50, 75, 100].forEach(t => {
      g += `<line x1="${x(t)}" x2="${x(t)}" y1="${TOP - 8}" y2="${H - 22}" class="sp-grid${t === 0 ? ' zero' : ''}"/>` +
           `<text x="${x(t)}" y="${H - 4}" text-anchor="middle" class="sp-axis">${t}%</text>`;
    });
    T.forEach(([id, name, m, lite, plus, safe], i) => {
      const y = TOP + i * ROW + 10;
      const r = [lite, plus, safe].map(v => red(m, v)), xs = r.map(x);
      const tip = (k, v, rr) => `<title>${id} ${k}: 위험 노출 ${m} → ${v} (${Math.round(rr)}% 감소)</title>`;
      g += `<text x="16" y="${y + 4}" class="sp-id">${id}</text><text x="50" y="${y + 4}" class="sp-name">${name}</text>` +
           `<line x1="${Math.min(...xs)}" x2="${Math.max(...xs)}" y1="${y}" y2="${y}" class="sp-range"/>` +
           `<circle cx="${xs[0]}" cy="${y}" r="5.5" class="sp-lite">${tip('Keep Tag', lite, r[0])}</circle>` +
           `<circle cx="${xs[2]}" cy="${y}" r="5.5" class="sp-safety">${tip('Shelter', safe, r[2])}</circle>` +
           `<circle cx="${xs[1]}" cy="${y}" r="6.5" class="sp-plus">${tip('Keep Tag+', plus, r[1])}</circle>` +
           `<text x="${xs[1]}" y="${y - 10}" text-anchor="middle" class="sp-val">${Math.round(r[1])}%</text>`;
    });
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" xmlns="${NS}">${g}</svg>`;
  })();

  /* ---------- Alerts: hub-exit threshold ---------- */
  (function thresh() {
    const seg = $('#threshSeg');
    if (!seg) return;
    const D = {
      60: [100, '오경보 하루 약 100건. 버스·식당에서 조금만 멀어져도 울려, 가이드가 결국 경보를 무시하게 됩니다. 학생 단체에서는 60초를 쓰지 않습니다.'],
      180: [25, '기본값. 반 단위 묶음 알림과 억제 규칙을 더해 가이드가 처리할 수 있는 수준으로 줄입니다.'],
      300: [7, '오경보는 하루 7건으로 줄지만 떨어진 사람을 그만큼 늦게 찾습니다. 아이 프리셋(T10)에서는 위험 노출이 160 → 235로 늘었습니다.'],
    };
    function set(v) {
      $$('button', seg).forEach(b => b.classList.toggle('on', b.dataset.v === v));
      const [n, note] = D[v];
      $('#threshNum').textContent = n;
      $('#threshNum').classList.toggle('low', n >= 50);
      $('#threshBar').style.width = n + '%';
      $('#threshNote').textContent = note;
    }
    seg.addEventListener('click', e => { const b = e.target.closest('button'); if (b) set(b.dataset.v); });
    set('180');
  })();

  /* ---------- Jeju scenarios ---------- */
  (function jeju() {
    const tabs = $('#jejuTabs'), map = $('#jejuMap'), pinsG = $('#jejuPins');
    if (!tabs || !map) return;
    const ICON = { ok: 'i-check', alert: 'i-alert', '': 'i-pin' };
    const S = [
      { c: '#B4BEF0', place: '제주국제공항', pin: [298, 98], lbl: [298, 62],
        kicker: '시나리오 01 · Keep Tag', title: '공항 배포 · 미아 방지',
        meta: [['장소', '제주국제공항 → 시내 관광지'], ['시기', '연중 · 주말·성수기 혼잡 시간대'], ['인물', '7살 아이와 부모, 2박 3일 가족 여행']],
        problem: '붐비는 관광지에서 아이 손을 한순간 놓치면, 부모는 어디서부터 찾아야 할지 모릅니다.',
        device: [['lite', 'Keep Tag (손목·클립)'], ['', '부모 휴대폰이 허브'], ['', '부저 “찾기”'], ['', '번호판으로 보호자 확인']],
        check: '공항·렌터카 업체와의 배포 채널, 태그 회수율 관리 방식은 협의·검증이 필요합니다.',
        steps: [
          ['ok', '10:20', '도착 · 태그 수령', '공항 안내 데스크에서 아이 손목에 Keep Tag를 채우고, QR을 찍어 부모 휴대폰과 연결합니다.'],
          ['', '13:30', '관광지 도착', '부모 휴대폰이 허브가 되어 아이와의 거리를 조용히 확인합니다. 반경은 15m로 설정.'],
          ['alert', '13:42', '아이와 떨어짐', '반경을 벗어나는 순간 부모 휴대폰이 진동하고, 마지막으로 확인된 위치와 시각을 표시합니다.'],
          ['', '13:44', '부저로 찾기', '“찾기” 버튼으로 태그 부저를 울려 근처에서 소리로 찾습니다. 번호판을 본 직원이 안내소에 연락할 수도 있습니다.'],
          ['ok', '13:47', '재회 · 마지막 날 반납', '5분 만에 재회. 여행 마지막 날 공항 반납함에 태그를 넣으면 끝입니다.'],
        ] },
      { c: '#E06A6A', place: '중문색달해수욕장', pin: [330, 330], lbl: [214, 360],
        kicker: '시나리오 02 · Keep Tag+ → Shelter 모드', title: '이안류 조난 위치 특정',
        meta: [['장소', '중문색달해수욕장 (서귀포)'], ['시기', '7~8월 해수욕철 오후'], ['인물', '물놀이에 나선 대학생 MT 일행 20명']],
        problem: '이안류는 순식간에 사람을 먼바다 쪽으로 밀어냅니다. 구조대는 어디부터 수색할지 빠르게 판단해야 합니다.',
        device: [['plus', 'Keep Tag+ 방수 밴드'], ['safety', 'Shelter 모드 (30초 간격)'], ['', '바다 쪽 급이동 감지'], ['', '인솔자·안전요원 알림']],
        check: '물속에서는 GPS·통신 신호가 약합니다. 수면 위 송신 방식, 부유형·고방수 설계, 해경·119 연계는 검증·협의가 필요합니다.',
        steps: [
          ['ok', '14:00', '입수 전 모드 전환', '해변 지오펜스에 들어서면 Keep Tag+ 밴드가 Shelter 모드로 바뀌어 30초 간격으로 위치를 기록합니다.'],
          ['', '14:20', '물놀이 중', '인솔자 앱에서 20명이 모두 해변 구역 안에 있는지 한눈에 확인합니다.'],
          ['alert', '14:31', '바다 쪽 급이동 감지', '한 명이 해안선에서 바다 쪽으로 빠르게 멀어지는 패턴. 인솔자와 안전요원에게 즉시 경보를 보냅니다.'],
          ['', '14:32', '마지막 위치·방향 전달', '수면에서 송신된 마지막 좌표와 이동 방향을 지도에 표시해 수색 범위를 좁힙니다.'],
          ['ok', '14:38', '구조 · 기록', '수상구조대가 표시된 좌표를 중심으로 접근해 구조합니다. 경보·대응 기록은 안전 리포트로 남습니다.'],
        ] },
      { c: '#f3c15d', place: '동부 중산간', pin: [552, 232], lbl: [552, 270],
        kicker: '시나리오 03 · Keep Tag+', title: '고사리 채취 길 잃음',
        meta: [['장소', '동부 중산간 들판·숲 인근'], ['시기', '4~5월 고사리 철 이른 아침'], ['인물', '고사리를 꺾으러 나선 70대 어르신']],
        problem: '고개를 숙이고 고사리를 따라 걷다 보면 방향을 잃기 쉽고, 비슷한 덤불과 숲이 이어져 스스로 위치를 설명하기 어렵습니다.',
        device: [['plus', 'Keep Tag+ 밴드'], ['', '채취 구역 지오펜스'], ['', 'SOS 길게 누르기'], ['', 'Keep Home 링크']],
        check: '중산간 LTE 음영 지역 확인과, 마을·지자체 단위 공동 보급 모델 검토가 필요합니다.',
        steps: [
          ['ok', '06:30', '출발', 'Keep Tag+ 밴드를 차고 나섭니다. 가족 휴대폰에 안심 링크가 열리고, 채취 구역(반경 500m)을 지정합니다.'],
          ['', '08:50', '구역 밖으로 이동', '구역을 벗어나면 GPS가 켜지고, 가족에게 “구역 밖 이동” 알림이 갑니다.'],
          ['alert', '09:35', 'SOS 요청', '길을 잃은 어르신이 버튼을 길게 눌러 SOS. 좌표가 가족과 비상 연락처로 전송됩니다.'],
          ['', '09:40', '좌표 전달', '가족이 좌표를 119에 바로 전달합니다. “어디쯤인지” 설명할 필요가 없습니다.'],
          ['ok', '10:05', '발견 · 귀가', '좌표를 따라 수색을 시작해 빠르게 발견, 무사히 귀가합니다.'],
        ] },
      { c: '#a48ef0', place: '동부 해안 올레길', pin: [658, 240], lbl: [672, 276],
        kicker: '시나리오 04 · Shelter 모드', title: '올레길 조난',
        meta: [['장소', '동부 해안 올레길 (성산 일대)'], ['시기', '연중 · 평일 오전'], ['인물', '혼자 올레길을 걷는 50대 트레커']],
        problem: '인적이 드문 구간에서 넘어지거나 탈진하면, 도움을 요청할 사람도 위치를 설명할 방법도 없습니다.',
        device: [['safety', 'Shelter 모드'], ['', '넘어짐 감지 (가속도·기압계)'], ['', '예정 시간 초과 알림'], ['', '비상 연락처 자동 공유']],
        check: '넘어짐 감지 오경보율 검증이 필요하며, 제주올레 측과의 협력은 아직 협의 전입니다.',
        steps: [
          ['ok', '08:00', '코스 시작', '시작점에서 Shelter 모드를 켜고 예상 완주 시간(5시간)을 등록합니다.'],
          ['', '10:40', '구간 통과 기록', '30초~1분 간격으로 위치가 기록돼, 비상 연락처가 지금 어느 구간인지 확인할 수 있습니다.'],
          ['alert', '11:20', '넘어짐 감지', '급격한 충격 뒤 3분간 움직임이 없으면 넘어짐으로 판단하고 밴드가 진동으로 확인을 요청합니다.'],
          ['', '11:23', '자동 알림', '응답이 없으면 비상 연락처에 위치와 코스 구간을 자동 전송합니다.'],
          ['ok', '11:55', '구조 · 시간 감시', '좌표로 구조대가 도착합니다. 넘어짐이 없어도 예정 시간을 넘기면 확인 메시지를 보냅니다.'],
        ] },
    ];

    // Map pins with label chips
    const pins = S.map((s, i) => {
      const g = svgEl('g', { class: 'jpin', tabindex: 0, role: 'button', 'aria-label': `${i + 1}. ${s.title}` });
      const [x, y] = s.pin, [lx, ly] = s.lbl;
      const w = s.place.length * 12.5 + 34;
      g.innerHTML = `
        <circle class="ring" cx="${x}" cy="${y}" r="14" fill="${s.c}" fill-opacity=".3"><animate attributeName="r" values="12;26;12" dur="2s" repeatCount="indefinite"/></circle>
        <circle cx="${x}" cy="${y}" r="11" fill="${s.c}" stroke="#fff" stroke-width="3"/>
        <text x="${x}" y="${y + 4}" text-anchor="middle" font-size="11" font-weight="800" fill="#141A2E">${i + 1}</text>
        <g class="jpin-box"><rect x="${lx - w / 2}" y="${ly - 13}" width="${w}" height="24" rx="12" fill="#fff" fill-opacity=".95"/>
        <circle cx="${lx - w / 2 + 13}" cy="${ly - 1}" r="4" fill="${s.c}"/>
        <text class="jpin-lbl" x="${lx - w / 2 + 23}" y="${ly + 3}" fill="#141A2E">${s.place}</text></g>`;
      g.addEventListener('click', () => show(i));
      g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(i); } });
      pinsG.appendChild(g);
      return g;
    });

    tabs.innerHTML = S.map((s, i) => `<button role="tab" style="--c:${s.c}" data-i="${i}"><i>${i + 1}</i><span>${s.title}<small>${s.place}</small></span></button>`).join('');
    tabs.addEventListener('click', e => { const b = e.target.closest('button'); if (b) show(+b.dataset.i); });

    const panel = $('#jejuScenario');
    function show(i) {
      const s = S[i];
      map.dataset.s = i;
      map.classList.add('has-sel');
      pins.forEach((p, k) => p.classList.toggle('on', k === i));
      pinsG.appendChild(pins[i]); // bring active pin to front
      const wrap = map.parentElement;
      if (wrap.scrollWidth > wrap.clientWidth) {
        const scale = map.clientWidth / 776;
        wrap.scrollTo({ left: (s.pin[0] - 24) * scale - wrap.clientWidth / 2, behavior: reduceMotion ? 'auto' : 'smooth' });
      }
      $$('button', tabs).forEach((b, k) => { b.classList.toggle('on', k === i); b.setAttribute('aria-selected', k === i); });
      panel.style.setProperty('--c', s.c);
      $('#scNum').textContent = String(i + 1).padStart(2, '0');
      $('#scKicker').textContent = s.kicker;
      $('#scTitle').textContent = s.title;
      $('#scMeta').innerHTML = s.meta.map(([k, v]) => `<div><dt>${k}</dt><dd>${v}</dd></div>`).join('');
      $('#scProblem').textContent = s.problem;
      $('#scDevice').innerHTML = s.device.map(([cls, t]) => `<span class="sc-chip ${cls}">${t}</span>`).join('');
      $('#scCheck').innerHTML = `<b>검증 과제</b><span>${s.check}</span>`;
      $('#scTimeline').innerHTML = s.steps.map(([cls, t, h, d]) =>
        `<li class="${cls}"><time>${t}</time><span class="pt"><svg class="icon"><use href="#${ICON[cls]}"/></svg></span><div><b>${h}</b><p>${d}</p></div></li>`).join('');
    }
    show(0);
  })();

  /* ---------- Pricing calculator (use-case presets) ---------- */
  (function calc() {
    const p = $('#cPeople'), d = $('#cDays'), sd = $('#cSafety'), t = $('#cTours'), fam = $('#cFamily'), sel = $('#cPreset');
    if (!p) return;
    const LITE = 200, PLUS = 600, SAFETY = 200, FAMILY = 3900, BASE = 29000;
    // [label, tag unit, people, days, safety days, family link, share of people on Shelter]
    const PRESETS = [
      ['효도·패키지', PLUS, 26, 5, 1, true, 1],
      ['산악·트레킹', PLUS, 18, 4, 2, false, 1],
      ['1일 투어', PLUS, 30, 1, 0, false, 1],
      ['수학여행', PLUS, 120, 2, 0, false, 1],
      ['공공 행사 (고위험 10%만 Shelter)', PLUS, 200, 1, 1, false, 0.1],
      ['기업 연수 (Keep Tag)', LITE, 40, 1, 0, false, 1],
    ];
    sel.innerHTML = PRESETS.map((x, i) => `<option value="${i}">${x[0]}</option>`).join('');
    const fill = el => el.style.setProperty('--p', ((el.value - el.min) / (el.max - el.min) * 100) + '%');
    function applyPreset() {
      const [, , people, days, sdays, family] = PRESETS[+sel.value];
      p.value = people; d.value = days; sd.value = sdays; fam.checked = family;
      update();
    }
    function update() {
      const [, unit, , , , , share] = PRESETS[+sel.value];
      if (+sd.value > +d.value) sd.value = d.value;
      const people = +p.value, days = +d.value, sdays = +sd.value, tours = +t.value;
      const safetyPeople = Math.round(people * share);
      const tag = people * days * unit;
      const safety = safetyPeople * sdays * SAFETY;
      const family = fam.checked ? people * FAMILY : 0;
      const tour = tag + safety + family;
      $('#oPeople').textContent = people + '명';
      $('#oDays').textContent = days + '일';
      $('#oSafetyDays').textContent = sdays + '일';
      $('#oTours').textContent = tours + '회';
      $('#lTag').textContent = `${unit === LITE ? 'Keep Tag' : 'Keep Tag+'} 태그 (${unit}원 × 인 × 일)`;
      $('#lSafety').textContent = share < 1 ? `Shelter 구간 (200원 × 고위험 ${safetyPeople}명 × 일)` : 'Shelter 구간 (200원 × 인 × 일)';
      $('#rTag').textContent = won(tag);
      $('#rSafety').textContent = won(safety);
      $('#rFamily').textContent = won(family);
      $('#rTour').textContent = won(tour);
      $('#rMonth').textContent = won(tour * tours + BASE);
      $('#rPer').textContent = won(Math.round(tour / people / 100) * 100);
      [p, d, sd, t].forEach(fill);
    }
    sel.addEventListener('change', applyPreset);
    [p, d, sd, t].forEach(el => el.addEventListener('input', update));
    fam.addEventListener('change', update);
    applyPreset();
  })();

  /* ---------- Contact form (demo) ---------- */
  const form = $('#contactForm');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    $('#formNote').classList.add('show');
  });
})();
