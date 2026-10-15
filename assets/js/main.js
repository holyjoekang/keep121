/* SafeFlock — site interactions */
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

  const navLinks = $$('#navLinks a');
  const sectionObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  navLinks.forEach(a => {
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

  /* ---------- Hero flock animation ---------- */
  (function hero() {
    const g = $('#heroDots');
    if (!g) return;
    const C = 280, FENCE = 122, PX_PER_M = FENCE / 10, LOST = 13; // member #14
    const golden = Math.PI * (3 - Math.sqrt(5));
    const members = Array.from({ length: 26 }, (_, i) => {
      const r = 36 + ((i * 53) % 62);
      const a = i * golden;
      const el = svgEl('circle', { r: 7.5, fill: '#6eeedb', stroke: '#0a1a2e', 'stroke-width': 2.5 });
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
      lost.el.setAttribute('fill', out ? '#ff6a4d' : '#6eeedb');
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
      const c = svgEl('circle', { cx: x, cy: y, r: 9.5, fill: '#3b5672', stroke: '#0a1a2e', 'stroke-width': 2 });
      const t = svgEl('text', { x, y: y + 3.5, 'text-anchor': 'middle', 'font-size': 9, 'font-weight': 800, fill: '#fff' });
      t.textContent = n;
      grp.append(c, t);
      if (n === 14) {
        const lbl = svgEl('text', { x: x + 16, y: y - 10, 'font-size': 11, 'font-weight': 800, fill: '#ff8a70' });
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
          p.c.setAttribute('fill', inside ? '#17c3a5' : '#ff6a4d');
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
        L.polyline(arc, { color: '#0a1a2e', weight: 2.5, dashArray: '6 8', opacity: .8 }),
        label(ICN, '인천'), label(LJG, '윈난 · 리장', 'now'),
      ]).addTo(map);

      // Day route + spots
      const route = L.layerGroup([
        L.polyline(SPOTS.map(s => s.ll), { color: '#17c3a5', weight: 4, opacity: .9, dashArray: '2 9', lineCap: 'round' }),
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
        m.marker = L.circleMarker([0, 0], { radius: 7, color: '#fff', weight: 2.5, fillColor: '#17c3a5', fillOpacity: 1 })
          .bindTooltip(`${i + 1}번`, { className: 'member-tip', direction: 'top', offset: [0, -6] });
        return m;
      });
      const fence = L.circle(GROUP, { radius: FENCE_M, color: '#17c3a5', weight: 2, dashArray: '6 7', fillColor: '#17c3a5', fillOpacity: .12 });
      const tether = L.polyline([GROUP, GROUP], { color: '#ff6a4d', weight: 2, dashArray: '4 6' });
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
        lost.marker.setStyle({ fillColor: out ? '#ff6a4d' : '#17c3a5', radius: out ? 9 : 7 });
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
          if (isMom) el.setStyle({ fillColor: fam ? '#ff8a63' : '#17c3a5', radius: fam ? 11 : 7 });
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
        { t: '09:40', n: '쿤밍 창수이 국제공항', d: '윈난성의 관문. 일행 26명 전원 도착을 확인하고 리장으로 이동했어요.', c: '#3a7bfd', i: 'i-pin' },
        { t: '15:20', n: '리장 고성', d: '물길 따라 이어진 나시족의 옛 도시. 1997년 유네스코 세계문화유산에 등재되었어요.', c: '#17c3a5', i: 'i-camera' },
        { t: '19:00', n: '사방가 야경', d: '고성의 중심 광장. 홍등이 켜진 골목과 나시족 전통 춤이 유명해요.', c: '#a48ef0', i: 'i-heart' },
      ]},
      { title: 'DAY 2 · 옥룡설산과 람월곡', spots: [
        { t: '10:40', n: '옥룡설산 빙천공원', d: '해발 5,596m의 설산. 케이블카로 4,506m 전망대까지 올라 빙하를 가까이에서 봤어요.', c: '#0f2b47', i: 'i-mountain' },
        { t: '14:30', n: '람월곡 (블루문밸리)', d: '빙하 녹은 물이 만든 에메랄드빛 계단식 호수. 설산이 비치는 사진 명소예요.', c: '#17c3a5', i: 'i-camera' },
        { t: '16:30', n: '인상리장 공연', d: '장이머우 감독이 연출한 야외 공연. 설산을 배경으로 한 웅장한 무대를 감상했어요.', c: '#ff6a4d', i: 'i-users' },
      ]},
      { title: 'DAY 3 · 수허 고진과 호도협', spots: [
        { t: '09:30', n: '수허 고진', d: '차마고도의 옛 역참 마을. 리장 고성보다 한적하고 소박한 분위기예요.', c: '#f3a93c', i: 'i-route' },
        { t: '13:00', n: '호도협', d: '진사강이 만든 깊은 협곡. 호랑이가 바위를 딛고 건넜다는 전설에서 이름이 왔어요.', c: '#0f2b47', i: 'i-mountain' },
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
    const TIER_LABEL = { lite: 'Lite', plus: 'Plus', safety: 'Plus · Safety 모드' };
    const CASES = [
      { name: '효도·패키지', sub: '해외 다일', tier: 'plus', period: '3~10일', abroad: '예', remote: '필수', risk: '중', wearer: '어르신', price: '중',
        strong: ['remote'], a1: '필수 → GPS·셀룰러 탑재', a2: '중간 → 떨어졌을 때만 추적', config: 'Plus 전원', cost: '약 25달러' },
      { name: '산악·고위험', sub: '설산·트레킹', tier: 'safety', period: '1~2일 구간', abroad: '예', remote: '실시간 필수', risk: '높음', wearer: '어르신·일반', price: '낮음',
        strong: ['remote', 'risk'], a1: '실시간 필수 → GPS·셀룰러 상시 동작', a2: '높음 → 30초~1분 추적 + SOS·넘어짐 감지', config: 'Plus 전원, 해당일만 Safety 모드', cost: '약 25달러' },
      { name: '1일 투어', sub: '국내·해외', tier: 'lite', period: '1일', abroad: '국내·해외', remote: '있으면 좋음', risk: '낮음', wearer: '일반', price: '높음 (매일 회수)',
        strong: ['price'], a1: '있으면 좋음 → 가이드 예비 Plus로 보완', a2: '낮음 → BLE 인원 확인 중심', config: 'Lite 전원 + 가이드 예비 Plus 2개', cost: '약 4달러' },
      { name: '수학여행·체험학습', sub: '대부분 국내', tier: 'lite', period: '1~4일', abroad: '대부분 국내', remote: '자유활동 때 필요', risk: '중', wearer: '학생', price: '높음 (대량)',
        strong: ['price'], a1: '자유활동 때만 → 조장만 Plus (해외는 Plus)', a2: '중간 → BLE + 일부 원격 위치', config: 'Lite 전원 + 자유활동 조장만 Plus', cost: '약 6달러 (국내)' },
      { name: '공공 행사·연수', sub: '수백 명 규모', tier: 'lite', period: '반나절~1일', abroad: '국내', remote: '거의 불필요', risk: '낮음', wearer: '일반', price: '매우 높음 (수백 명)',
        strong: ['price'], a1: '거의 불필요 → BLE만으로 충분', a2: '낮음 → 단가 최소화가 우선', config: 'Lite 전원 (스티커·목걸이형)', cost: '약 3달러' },
      { name: '제주 관광', sub: '제주 특화', tier: 'plus', period: '2~4일 (체류 중)', abroad: '아니오 (국내)', remote: '조난 시 필수', risk: '높음 (이안류·중산간)', wearer: '아이·어르신·관광객', price: '높음 (공항 대량 배포)',
        strong: ['remote', 'risk', 'price'], a1: '조난 시 필수 → 해변·산간 활동엔 GPS·셀룰러', a2: '높음 → 해변·올레길 구간은 Safety 모드', config: '공항 배포 Lite (아이·일반) + 해변·중산간·올레길은 Plus', cost: '약 4~25달러 (구성별)' },
      { name: '가족·아이', sub: '개인 구매', tier: 'lite', period: '수시', abroad: '국내', remote: '있으면 좋음', risk: '중', wearer: '어린이', price: '소비자 가격대',
        strong: [], a1: '있으면 좋음 → 우선 부모 휴대폰이 허브', a2: '중간 → 부저·LED “찾기” 기능', config: 'Lite (부모 휴대폰이 허브) → 추후 Plus', cost: '소비자가 1~2만 원대' },
    ];
    const REQS = [['period', '기간'], ['abroad', '해외'], ['remote', '떨어졌을 때 원격 위치'], ['risk', '위험도'], ['wearer', '착용자'], ['price', '회전율·단가 민감도']];
    const pickerEl = $('#picker'), tiers = $$('#lineup .tier');

    list.innerHTML = CASES.map((c, i) =>
      `<button role="tab" data-i="${i}"><span>${c.name}</span><small class="t-${c.tier}">${c.tier === 'safety' ? 'Safety' : TIER_LABEL[c.tier]}</small></button>`).join('');

    function show(i) {
      const c = CASES[i];
      pickerEl.className = pickerEl.className.replace(/\bt-\w+/g, '').trim() + ' t-' + c.tier;
      $$('button', list).forEach(b => { const on = +b.dataset.i === i; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
      $('#pkName').textContent = `${c.name} · ${c.sub}`;
      $('#pkTier').textContent = TIER_LABEL[c.tier];
      $('#pkReqs').innerHTML = REQS.map(([k, label]) =>
        `<div class="req${c.strong.includes(k) ? ' strong' : ''}"><span class="k">${label}</span><b>${c[k]}</b></div>`).join('');
      $('#pkAxis1').textContent = c.a1;
      $('#pkAxis2').textContent = c.a2;
      $('#pkConfig').textContent = c.config;
      $('#pkCost').textContent = c.cost;
      tiers.forEach(t => t.classList.toggle('match', t.dataset.tier === c.tier));
    }
    list.addEventListener('click', e => { const b = e.target.closest('button'); if (b) show(+b.dataset.i); });
    show(0);
  })();

  /* ---------- Device lineup: Plus battery estimate ---------- */
  (function battery() {
    const hours = $('#bHours'), modem = $('#bModem');
    if (!hours) return;
    const CAPACITY = 350, MARGIN = 1.25;            // mAh, efficiency/temperature headroom
    const TRACK_PER_HOUR = 30 * (0.14 + 0.2);        // 2-min fixes: GNSS + uplink per fix
    function update() {
      const h = +hours.value;
      const parts = [
        { label: 'BLE 상시 송신 (약 15µA × 24h)', v: 0.4, c: '#3a7bfd' },
        { label: '대기 (모뎀 완전 차단)', v: 1.0, c: '#8a98aa' },
        { label: `이탈 시 추적 (${h}시간, 2분 간격)`, v: TRACK_PER_HOUR * h, c: '#17c3a5' },
      ];
      if (modem.checked) parts.push({ label: '셀룰러 모뎀 대기 유지', v: 20, c: '#ff6a4d' });
      const total = parts.reduce((s, p) => s + p.v, 0);
      const days = CAPACITY / (total * MARGIN);

      $('#oHours').textContent = h + '시간';
      hours.style.setProperty('--p', (h / 4 * 100) + '%');
      $('#batLegend').innerHTML = parts.map(p => `<li><i style="background:${p.c}"></i><span>${p.label}</span><b>${p.v.toFixed(1)}mAh</b></li>`).join('');
      $('#batBar').innerHTML = parts.map(p => `<i style="background:${p.c};width:${p.v / total * 100}%"></i>`).join('');
      $('#bDaily').textContent = total.toFixed(1);
      const d = $('#bDays');
      d.textContent = days > 60 ? '60+' : Math.round(days);
      d.classList.toggle('low', days < 15);
      const goal = $('#batGoal');
      goal.classList.toggle('warn', days < 15);
      goal.textContent = days >= 15
        ? '✓ 목표 15일 충족 — 여유를 두고 잡은 목표치입니다.'
        : '⚠ 목표 15일 미달 — 모뎀 완전 차단과 추적 간격 조정이 필요합니다.';
    }
    hours.addEventListener('input', update);
    modem.addEventListener('change', update);
    update();
  })();

  /* ---------- Jeju scenarios ---------- */
  (function jeju() {
    const tabs = $('#jejuTabs'), map = $('#jejuMap'), pinsG = $('#jejuPins');
    if (!tabs || !map) return;
    const ICON = { ok: 'i-check', alert: 'i-alert', '': 'i-pin' };
    const S = [
      { c: '#6eeedb', place: '제주국제공항', pin: [298, 98], lbl: [298, 62],
        kicker: '시나리오 01 · Lite', title: '공항 배포 · 미아 방지',
        meta: [['장소', '제주국제공항 → 시내 관광지'], ['시기', '연중 · 주말·성수기 혼잡 시간대'], ['인물', '7살 아이와 부모, 2박 3일 가족 여행']],
        problem: '붐비는 관광지에서 아이 손을 한순간 놓치면, 부모는 어디서부터 찾아야 할지 모릅니다.',
        device: [['lite', 'Lite 태그 (손목·클립)'], ['', '부모 휴대폰이 허브'], ['', '부저 “찾기”'], ['', '번호판으로 보호자 확인']],
        check: '공항·렌터카 업체와의 배포 채널, 태그 회수율 관리 방식은 협의·검증이 필요합니다.',
        steps: [
          ['ok', '10:20', '도착 · 태그 수령', '공항 안내 데스크에서 아이 손목에 Lite 태그를 채우고, QR을 찍어 부모 휴대폰과 연결합니다.'],
          ['', '13:30', '관광지 도착', '부모 휴대폰이 허브가 되어 아이와의 거리를 조용히 확인합니다. 반경은 15m로 설정.'],
          ['alert', '13:42', '아이와 떨어짐', '반경을 벗어나는 순간 부모 휴대폰이 진동하고, 마지막으로 확인된 위치와 시각을 표시합니다.'],
          ['', '13:44', '부저로 찾기', '“찾기” 버튼으로 태그 부저를 울려 근처에서 소리로 찾습니다. 번호판을 본 직원이 안내소에 연락할 수도 있습니다.'],
          ['ok', '13:47', '재회 · 마지막 날 반납', '5분 만에 재회. 여행 마지막 날 공항 반납함에 태그를 넣으면 끝입니다.'],
        ] },
      { c: '#ff8a70', place: '중문색달해수욕장', pin: [330, 330], lbl: [214, 360],
        kicker: '시나리오 02 · Plus → Safety 모드', title: '이안류 조난 위치 특정',
        meta: [['장소', '중문색달해수욕장 (서귀포)'], ['시기', '7~8월 해수욕철 오후'], ['인물', '물놀이에 나선 대학생 MT 일행 20명']],
        problem: '이안류는 순식간에 사람을 먼바다 쪽으로 밀어냅니다. 구조대는 어디부터 수색할지 빠르게 판단해야 합니다.',
        device: [['plus', 'Plus 방수 밴드'], ['safety', 'Safety 모드 (30초 간격)'], ['', '바다 쪽 급이동 감지'], ['', '인솔자·안전요원 알림']],
        check: '물속에서는 GPS·통신 신호가 약합니다. 수면 위 송신 방식, 부유형·고방수 설계, 해경·119 연계는 검증·협의가 필요합니다.',
        steps: [
          ['ok', '14:00', '입수 전 모드 전환', '해변 지오펜스에 들어서면 Plus 밴드가 Safety 모드로 바뀌어 30초 간격으로 위치를 기록합니다.'],
          ['', '14:20', '물놀이 중', '인솔자 앱에서 20명이 모두 해변 구역 안에 있는지 한눈에 확인합니다.'],
          ['alert', '14:31', '바다 쪽 급이동 감지', '한 명이 해안선에서 바다 쪽으로 빠르게 멀어지는 패턴. 인솔자와 안전요원에게 즉시 경보를 보냅니다.'],
          ['', '14:32', '마지막 위치·방향 전달', '수면에서 송신된 마지막 좌표와 이동 방향을 지도에 표시해 수색 범위를 좁힙니다.'],
          ['ok', '14:38', '구조 · 기록', '수상구조대가 표시된 좌표를 중심으로 접근해 구조합니다. 경보·대응 기록은 안전 리포트로 남습니다.'],
        ] },
      { c: '#f3c15d', place: '동부 중산간', pin: [552, 232], lbl: [552, 270],
        kicker: '시나리오 03 · Plus', title: '고사리 채취 길 잃음',
        meta: [['장소', '동부 중산간 들판·숲 인근'], ['시기', '4~5월 고사리 철 이른 아침'], ['인물', '고사리를 꺾으러 나선 70대 어르신']],
        problem: '고개를 숙이고 고사리를 따라 걷다 보면 방향을 잃기 쉽고, 비슷한 덤불과 숲이 이어져 스스로 위치를 설명하기 어렵습니다.',
        device: [['plus', 'Plus 밴드'], ['', '채취 구역 지오펜스'], ['', 'SOS 길게 누르기'], ['', '가족 안심 링크']],
        check: '중산간 LTE 음영 지역 확인과, 마을·지자체 단위 공동 보급 모델 검토가 필요합니다.',
        steps: [
          ['ok', '06:30', '출발', 'Plus 밴드를 차고 나섭니다. 가족 휴대폰에 안심 링크가 열리고, 채취 구역(반경 500m)을 지정합니다.'],
          ['', '08:50', '구역 밖으로 이동', '구역을 벗어나면 GPS가 켜지고, 가족에게 “구역 밖 이동” 알림이 갑니다.'],
          ['alert', '09:35', 'SOS 요청', '길을 잃은 어르신이 버튼을 길게 눌러 SOS. 좌표가 가족과 비상 연락처로 전송됩니다.'],
          ['', '09:40', '좌표 전달', '가족이 좌표를 119에 바로 전달합니다. “어디쯤인지” 설명할 필요가 없습니다.'],
          ['ok', '10:05', '발견 · 귀가', '좌표를 따라 수색을 시작해 빠르게 발견, 무사히 귀가합니다.'],
        ] },
      { c: '#a48ef0', place: '동부 해안 올레길', pin: [658, 240], lbl: [672, 276],
        kicker: '시나리오 04 · Safety 모드', title: '올레길 조난',
        meta: [['장소', '동부 해안 올레길 (성산 일대)'], ['시기', '연중 · 평일 오전'], ['인물', '혼자 올레길을 걷는 50대 트레커']],
        problem: '인적이 드문 구간에서 넘어지거나 탈진하면, 도움을 요청할 사람도 위치를 설명할 방법도 없습니다.',
        device: [['safety', 'Safety 모드'], ['', '넘어짐 감지 (가속도·기압계)'], ['', '예정 시간 초과 알림'], ['', '비상 연락처 자동 공유']],
        check: '넘어짐 감지 오경보율 검증이 필요하며, 제주올레 측과의 협력은 아직 협의 전입니다.',
        steps: [
          ['ok', '08:00', '코스 시작', '시작점에서 Safety 모드를 켜고 예상 완주 시간(5시간)을 등록합니다.'],
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
        <text x="${x}" y="${y + 4}" text-anchor="middle" font-size="11" font-weight="800" fill="#0a1a2e">${i + 1}</text>
        <g class="jpin-box"><rect x="${lx - w / 2}" y="${ly - 13}" width="${w}" height="24" rx="12" fill="#fff" fill-opacity=".95"/>
        <circle cx="${lx - w / 2 + 13}" cy="${ly - 1}" r="4" fill="${s.c}"/>
        <text class="jpin-lbl" x="${lx - w / 2 + 23}" y="${ly + 3}" fill="#0a1a2e">${s.place}</text></g>`;
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

  /* ---------- Pricing calculator ---------- */
  (function calc() {
    const p = $('#cPeople'), d = $('#cDays'), t = $('#cTours');
    if (!p) return;
    const fill = el => el.style.setProperty('--p', ((el.value - el.min) / (el.max - el.min) * 100) + '%');
    function update() {
      const people = +p.value, days = +d.value, tours = +t.value;
      const saas = people * 500, rent = people * days * 400, tour = saas + rent;
      $('#oPeople').textContent = people + '명';
      $('#oDays').textContent = days + '일';
      $('#oTours').textContent = tours + '회';
      $('#rSaas').textContent = won(saas);
      $('#rRent').textContent = won(rent);
      $('#rTour').textContent = won(tour);
      $('#rMonth').textContent = won(tour * tours + 29000);
      $('#rPer').textContent = won(Math.round(tour / people));
      [p, d, t].forEach(fill);
    }
    [p, d, t].forEach(el => el.addEventListener('input', update));
    update();
  })();

  /* ---------- Contact form (demo) ---------- */
  const form = $('#contactForm');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    $('#formNote').classList.add('show');
  });
})();
