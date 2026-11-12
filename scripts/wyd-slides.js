/* 제안 슬라이드 엔진: [data-deck data-src="data/xxx.json"] 을 채운다. (원본: scripts/wyd-slides.js)
   WYD 서울 2027(data/wyd2027.json)·제주 이동안전(data/jeju2027.json)이 같이 쓴다.
   ←/→·스페이스·스와이프로 넘김, F 전체화면, P 인쇄(슬라이드당 1장 PDF). */
(() => {
  'use strict';
  const stage = document.querySelector('[data-deck]');
  if (!stage) return;
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  let I = {};
  const img = k => I[k] || k;
  // 이미지 초점: data.img 에 '키@pos' 가 있으면 background-position 으로 쓴다 (예: 사진 위쪽만 보이게)
  const bg = k => `style="background-image:url('${img(k)}')${I[k + '@pos'] ? `;background-position:${I[k + '@pos']}` : ''}"`;
  const H = s => s; // 데이터에 들어 있는 <em>·<b> 강조는 그대로 쓴다

  const foot = (d, n) => `<div class="foot"><span>${E(d.footer)}</span><span>${n}</span></div>`;
  const src = t => t ? `<span class="src">${E(t)}</span>` : '';
  const head = s => `${s.k ? `<p class="k">${E(s.k)}</p>` : ''}<h2>${H(s.title)}</h2>${s.lead ? `<p class="lead">${H(s.lead)}</p>` : ''}`;

  // 시연 화면 조각
  const sb = () => `<div class="sb"><span>14:05</span><span>5G ▮▮▮ 82%</span></div>`;
  const phone = p => `<div class="phone"><div class="scr">${sb()}<div class="ah ${p.tone}"><small>${E(p.app)}</small><b>${E(p.head)}</b></div><div class="sc">${p.body.map(part).join('')}</div></div></div>`;
  const part = b => {
    switch (b.t) {
      case 'item': return `<div class="it${b.cur ? ' cur' : ''}"><span class="tm">${E(b.tm)}</span><div class="ds"><b>${E(b.b)}</b><span>${E(b.s)}</span></div><span class="st ${b.st}">${E(b.lab)}</span></div>`;
      case 'alert': return `<div class="alert${b.red ? ' red' : ''}"><b>${E(b.b)}</b>${E(b.s)}</div>`;
      case 'btns': return `<div class="btns">${b.items.map((x, i) => `<span${i ? ' class="alt"' : ''}>${E(x)}</span>`).join('')}</div>`;
      case 'lang': return `<div class="lang">${b.items.map(x => `<span>${E(x)}</span>`).join('<span>⇄</span>')}</div>`;
      case 'me': case 'you': return `<div class="bub ${b.t}"><small>${E(b.l)}</small>${E(b.s)}</div>`;
      case 'mic': return `<div class="mic">🎙</div><div style="text-align:center;font-size:12px;color:var(--muted)">${E(b.s)}</div>`;
      case 'ring': return `<div class="ring2"><div class="donut"><b>${E(b.v)}</b></div><div class="ds"><b style="font-size:16px">${E(b.b)}</b><span style="font-size:12px;color:var(--muted)">${E(b.s)}</span></div></div>`;
      case 'map': return `<div class="map" ${bg(b.img)}>${b.pins.map(([x, y, r, me]) => `${r ? `<span class="rad" style="left:calc(${x}% - ${r}px);top:calc(${y}% - ${r}px);width:${r * 2}px;height:${r * 2}px"></span>` : ''}<span class="pin${me ? ' me' : ''}" style="left:calc(${x}% - 8px);top:calc(${y}% - 8px)"></span>`).join('')}</div>`;
      case 'sos': return `<div class="sosbtn"><div>SOS<small>${E(b.s)}</small></div></div>`;
      case 'txt': return `<div style="font-size:12.5px;color:var(--muted);line-height:1.5;text-align:center">${E(b.s)}</div>`;
      default: return '';
    }
  };

  const R = {
    cover: s => `<div class="slide photo cover"><div class="bg" ${bg(s.img)}></div><div class="pad">
      <div class="logos">${s.brands ? s.brands.map(([b, sm], i) => `${i ? '<span class="x">×</span>' : ''}<span class="brand">${E(b)}<small>${E(sm)}</small></span>`).join('') : `<img src="${img('logo')}" alt="2027 서울 세계청년대회 로고"><span class="x">×</span><span class="brand">Keep121<small>단체 이동 안전 플랫폼</small></span><span class="x">×</span><span class="brand">Galaxy SmartTag3<small>삼성전자 협력 제안</small></span>`}</div>
      <p class="k">${E(s.k)}</p><h1>${H(s.title)}</h1><p class="sub">${H(s.sub)}</p>
      <div class="meta">${s.meta.map(([a, b]) => `<div><b>${E(b)}</b>${E(a)}</div>`).join('')}</div></div>${src(s.src)}</div>`,

    glance: (s, d, n) => `<div class="slide photo"><div class="bg" ${bg(s.img)}></div><div class="pad">${head(s)}
      <div class="stats">${s.stats.map(([v, u, l]) => `<div class="stat"><b>${E(v)}<small>${E(u)}</small></b><span>${E(l)}</span></div>`).join('')}</div>
      <div class="days">${s.days.map(([a, b]) => `<div class="day"><b>${E(a)}</b><span>${E(b)}</span></div>`).join('')}</div>
      ${s.note ? `<p class="note">${E(s.note)}</p>` : ''}</div>${foot(d, n)}${src(s.src)}</div>`,

    story: (s, d, n) => `<div class="slide"><div class="pad"><div class="row"><div class="col" style="flex:1.05">${head(s)}
      <div style="display:flex;flex-direction:column;gap:14px;margin-top:auto">${s.beats.map(([a, b]) => `<div style="display:flex;gap:18px;align-items:baseline"><b style="font:800 22px var(--display);color:var(--dawn);width:120px;flex:none">${E(a)}</b><span style="font-size:21px;line-height:1.5">${H(b)}</span></div>`).join('')}</div></div>
      <div class="col"><div class="mosaic">${s.imgs.map((k, i) => `<div${i === 0 ? ' class="big"' : ''} ${bg(k)}></div>`).join('')}</div></div></div></div>${foot(d, n)}</div>`,

    problems: (s, d, n) => `<div class="slide" style="background:var(--soft)"><div class="pad">${head(s)}
      <div class="g4" style="flex:1">${s.items.map(([k, h, p], i) => `<div class="card"><div class="im" ${bg(k)} style="height:230px"></div><div class="tx"><span class="n">0${i + 1}</span><h3>${E(h)}</h3><p>${H(p)}</p></div></div>`).join('')}</div></div>${foot(d, n)}</div>`,

    eco: (s, d, n) => `<div class="slide"><div class="pad">${head(s)}
      <div class="eco">${s.nodes.map((x, i) => `${i ? '<div class="arr">→</div>' : ''}<div class="node ${x.c}">${x.img ? `<div class="ph" ${bg(x.img)}></div>` : ''}<span class="who">${E(x.who)}</span><h3>${E(x.h)}</h3><p>${E(x.p)}</p><div>${x.f.map(f => `<span class="pill">${E(f)}</span>`).join('')}</div></div>`).join('')}</div>
      <div class="base">${s.base.map(([c, b, t]) => `<div class="${c}"><b>${E(b)}</b><span>${E(t)}</span></div>`).join('')}</div>
      </div>${foot(d, n)}</div>`,

    tag: (s, d, n) => `<div class="slide dark"><div class="pad"><div class="row"><div class="col">${head(s)}
      <div class="stats" style="margin-bottom:22px">${s.stats.map(([v, u, l]) => `<div class="stat"><b>${E(v)}<small>${E(u)}</small></b><span>${E(l)}</span></div>`).join('')}</div>
      <div class="g2">${s.how.map(([b, t]) => `<div class="glass"><b>${E(b)}</b><span>${E(t)}</span></div>`).join('')}</div>
      <p class="note">${E(s.note)}</p></div>
      <div class="col" style="flex:.7"><div class="tagvis"><span class="ring"></span><span class="ring r2"></span><span class="ring r3"></span><div class="t3"><span>SmartTag3</span></div></div></div></div></div>${foot(d, n)}</div>`,

    scenario: (s, d, n) => `<div class="slide" style="background:var(--soft)"><div class="pad">${head(s)}
      <div class="flow">${s.steps.map((x, i) => `<div class="step"><div class="im" ${bg(x.img)}><i>${i + 1}</i></div><div class="tx"><span class="when">${E(x.when)}</span><b>${E(x.h)}</b><p>${E(x.p)}</p>${x.apps.map(([c, t]) => `<span class="app ${c}">${E(t)}</span>`).join('')}</div></div>`).join('')}</div>
      </div>${foot(d, n)}</div>`,

    demo: (s, d, n) => `<div class="slide photo"><div class="bg" ${bg(s.img)}></div><div class="pad"><div class="demo${s.phones.length > 1 ? ' two' : ''}">
      <div class="points">${head(s)}<ul>${s.points.map(p => `<li><span>${H(p)}</span></li>`).join('')}</ul>${s.note ? `<p class="note">${E(s.note)}</p>` : ''}</div>
      ${s.phones.map(phone).join('')}</div></div>${foot(d, n)}${src(s.src)}</div>`,

    dash: (s, d, n) => `<div class="slide" style="background:#e9ecf4"><div class="pad" style="padding-bottom:56px">${head(s)}
      <div class="dash"><div class="kp">${s.kpis.map(([v, l, c]) => `<div class="${c || ''}"><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div>
      <div class="dmap" data-l="${E(s.mapLabel || '한강')}"><span class="rd" style="left:0;right:0;top:30%;height:6px"></span><span class="rd" style="top:0;bottom:0;left:44%;width:6px"></span><span class="rd" style="top:0;bottom:0;left:76%;width:5px"></span>${s.zones.map(([x, y, w, c, t]) => `<div class="zone ${c}" style="left:${x}%;top:${y}%;width:${w}px;height:${w}px">${t}</div>`).join('')}</div>
      <div class="feed"><h4>실시간 이벤트</h4>${s.feed.map(([c, b, t]) => `<div class="ev ${c}"><b>${E(b)}</b><span>${E(t)}</span></div>`).join('')}</div></div>
      <p class="note" style="margin-top:8px">${E(s.note)}</p></div>${foot(d, n)}</div>`,

    benefit: (s, d, n) => `<div class="slide"><div class="pad">${head(s)}
      <div class="ben">${s.who.map(([k, h, li]) => `<div class="card"><div class="im" ${bg(k)}></div><div class="tx"><h3>${E(h)}</h3><ul>${li.map(x => `<li>${E(x)}</li>`).join('')}</ul></div></div>`).join('')}</div>
      <div class="kpi">${s.kpi.map(([a, b, l]) => `<div><b>${a ? `<s>${E(a)}</s>` : ''}${E(b)}</b><span>${E(l)}</span></div>`).join('')}</div>
      <p class="note">${E(s.note)}</p></div>${foot(d, n)}</div>`,

    samsung: (s, d, n) => `<div class="slide photo"><div class="bg" ${bg(s.img)}></div><div class="pad">${head(s)}
      <div class="sam">${s.items.map(([i, b, t]) => `<div class="glass"><i>${E(i)}</i><b>${E(b)}</b><span>${E(t)}</span></div>`).join('')}</div>
      <div class="camp"><b>${H(s.camp.b)}</b><span>${E(s.camp.t)}</span></div></div>${foot(d, n)}${src(s.src)}</div>`,

    rules: (s, d, n) => `<div class="slide" style="background:var(--soft)"><div class="pad">${head(s)}
      <div class="rules">${s.items.map(([b, p]) => `<div class="rule"><b>${E(b)}</b><p>${E(p)}</p></div>`).join('')}</div>
      <div class="road">${s.road.map(([w, b, p, m]) => `<div class="ms${m ? ' main' : ''}"><span class="w">${E(w)}</span><b>${E(b)}</b><p>${E(p)}</p></div>`).join('')}</div>
      ${s.imgs ? `<div class="strip">${s.imgs.map(k => `<div ${bg(k)}></div>`).join('')}</div>` : ''}</div>${foot(d, n)}</div>`,

    segments: (s, d, n) => `<div class="slide" style="background:var(--soft)"><div class="pad">${head(s)}
      <div class="seg">${s.items.map(x => `<div class="card ${x.c}"><div class="im" ${bg(x.img)}><span class="flag">${E(x.tag)}</span></div><div class="tx">
        <div class="segstat">${x.stats.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div>
        <h3>${E(x.h)}</h3><ul>${x.pain.map(p => `<li>${H(p)}</li>`).join('')}</ul><p class="fix">${H(x.fix)}</p></div></div>`).join('')}</div>
      ${s.note ? `<p class="note">${E(s.note)}</p>` : ''}</div>${foot(d, n)}</div>`,

    cases: (s, d, n) => `<div class="slide"><div class="pad">${head(s)}
      <div class="cases">${s.items.map(([k, who, h, m, lesson]) => `<div class="card"><div class="im" ${bg(k)}><span class="flag">${E(who)}</span></div><div class="tx"><h3>${E(h)}</h3><p class="m">${E(m)}</p><p>${H(lesson)}</p></div></div>`).join('')}</div>
      <div class="gap"><b>${E(s.gap.b)}</b><span>${H(s.gap.t)}</span></div></div>${foot(d, n)}</div>`,

    budget: (s, d, n) => { const tot = s.rows.reduce((a, r) => a + r[1], 0); return `<div class="slide"><div class="pad">${head(s)}
      <div class="row"><div class="col" style="flex:1.25"><table class="bud"><thead><tr><th>항목</th><th>금액(만원)</th><th>산출 근거</th></tr></thead><tbody>
        ${s.rows.map(([a, v, why]) => `<tr><th>${E(a)}</th><td><b>${v.toLocaleString()}</b><i style="--w:${v / tot * 100}%"></i></td><td>${E(why)}</td></tr>`).join('')}
        <tr class="tot"><th>합계 (1년 차 시범)</th><td><b>${tot.toLocaleString()}</b></td><td>${E(s.totNote)}</td></tr></tbody></table></div>
      <div class="col"><h3 class="bh">재원 조합</h3>${s.funds.map(([a, b, t]) => `<div class="fund"><b>${E(a)}</b><em>${E(b)}</em><span>${E(t)}</span></div>`).join('')}
        <div class="unit">${s.unit.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div></div></div>
      <p class="note">${E(s.note)}</p></div>${foot(d, n)}</div>`; },

    close: (s, d, n) => `<div class="slide photo full"><div class="bg" ${bg(s.img)}></div><div class="pad">${head(s)}
      <div class="ask">${s.ask.map((t, i) => `<div><i>${i + 1}</i><span>${E(t)}</span></div>`).join('')}</div>
      <p class="close">${H(s.close)}</p><p style="font-size:20px;color:#dfe4f3;margin:0">${E(s.contact)}</p></div>${foot(d, n)}${src(s.src)}</div>`
  };

  // 상단 고정 메뉴: Keep121 홈 · 맞춤 제안 목록 (슬라이드·휴대폰 모드 공통)
  const top = document.createElement('header');
  top.className = 'dk-top';
  top.innerHTML = `<a class="dk-brand" href="index.html" aria-label="Keep121 홈"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#23306B"/><path d="M9 26V15a7 7 0 0 1 14 0v11" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/><circle cx="16" cy="20.5" r="3" fill="#F2A541"/></svg><b>Keep121</b></a><nav aria-label="제안 메뉴"><a href="index.html">홈</a><a href="proposals.html">맞춤 제안</a><a href="company.html#contact">문의</a></nav>`;
  document.body.prepend(top);

  fetch(stage.dataset.src || 'data/wyd2027.json', { cache: 'no-cache' }).then(r => r.json()).then(d => {
    I = d.img;
    const N = d.slides.length;
    stage.innerHTML = d.slides.map((s, i) => (R[s.type] || (() => ''))(s, d, `${i + 1} / ${N}`)).join('');
    const slides = [...stage.children];
    const bar = document.querySelector('.ui .bar i'), cnt = document.querySelector('.ui .cnt');
    let cur = 0;
    const go = i => {
      cur = Math.max(0, Math.min(N - 1, i));
      slides.forEach((el, j) => el.classList.toggle('on', j === cur));
      bar.style.width = `${(cur + 1) / N * 100}%`; cnt.textContent = `${cur + 1} / ${N}`;
      if (!mob()) history.replaceState(null, '', `#${cur + 1}`);
    };
    // 좁은 화면(휴대폰 세로·가로)은 슬라이드를 세로로 이어 붙인 읽기 모드, 넓은 화면은 16:9 슬라이드 모드
    const mob = () => innerWidth < 900 || innerHeight < 500;
    const fit = () => {
      const m = mob();
      document.documentElement.classList.toggle('m', m);
      if (m) { stage.style.transform = ''; return; }
      const k = Math.min(innerWidth / 1600, innerHeight / 900);
      stage.style.transform = `translate(-50%, -50%) scale(${k})`;
    };
    addEventListener('resize', fit); fit();
    addEventListener('keydown', e => {
      if (mob()) return;
      if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); go(cur + 1); }
      else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); go(cur - 1); }
      else if (e.key === 'Home') go(0); else if (e.key === 'End') go(N - 1);
      else if (e.key === 'f' || e.key === 'F') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen?.();
      else if (e.key === 'p' || e.key === 'P') print();
    });
    let x0 = null;
    addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
    addEventListener('touchend', e => { if (x0 === null || mob()) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1)); x0 = null; });
    stage.addEventListener('click', e => { if (mob() || e.target.closest('a,button')) return; go(cur + (e.clientX > innerWidth / 2 ? 1 : -1)); });
    document.querySelector('[data-prev]').onclick = () => go(cur - 1);
    document.querySelector('[data-next]').onclick = () => go(cur + 1);
    document.querySelector('[data-print]').onclick = () => print();
    go((parseInt(location.hash.slice(1), 10) || 1) - 1);
  });
})();
