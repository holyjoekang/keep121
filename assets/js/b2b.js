/* B2B 확장 전략 페이지: data/b2b.json 을 받아 [data-b2b] 자리를 채운다. (원본: scripts/b2b.js) */
(() => {
  'use strict';
  const root = document.querySelector('[data-b2b]');
  if (!root) return;
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const chip = t => `<span class="b2-chip ${/Guide/.test(t) ? 'guide' : /Track/.test(t) ? 'track' : 'tag'}">${E(t)}</span>`;
  const head = (k, h, p) => `<div class="head"><span class="eyebrow">${k}</span><h2>${h}</h2>${p ? `<p>${p}</p>` : ''}</div>`;
  const sec = (id, cls, inner) => `<section id="${id}"${cls ? ` class="${cls}"` : ''}><div class="wrap">${inner}</div></section>`;
  const card = (edge, h, p, extra = '') => `<div class="b2-card edge-${edge}"><h3>${h}</h3><p>${p}</p>${extra}</div>`;

  fetch('data/b2b.json', { cache: 'no-cache' }).then(r => r.json()).then(d => {
    const h = d.hero, v = d.view, sn = d.sensing, f = d.fit, pr = d.precision, m = d.markets, ps = d.prospects, dr = d.direction;
    const html = [
      `<section class="page-hero has-photo" style="--bg:url('https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1800&q=75')"><div class="wrap">
        <nav class="crumb" aria-label="현재 위치"><a href="index.html">홈</a><span aria-hidden="true">/</span><a href="usecases.html">국내 시장</a><span aria-hidden="true">/</span><b>B2B 확장</b></nav>
        <span class="eyebrow">${E(h.eyebrow)}</span><h1>${h.title}</h1><p>${E(h.text)}</p>
        <div class="b2-route">${h.route.map(([c, b, s]) => `<div class="stop ${c}"><b>${E(b)}</b><span>${E(s)}</span></div>`).join('')}</div>
      </div></section>`,
      `<nav class="subnav" aria-label="이 페이지의 내용"><div class="wrap"><span class="subnav-k">이 페이지</span>${d.nav.map(([a, t]) => `<a href="#${a}">${E(t)}</a>`).join('')}</div></nav>`,
      sec('view', '', head('Core View', '판매가 아니라<br><span class="hl">이동 상태의 통합 관리.</span>') +
        `<p class="b2-statement">${v.no ? `<s>${E(v.no)}</s><br>` : ''}${E(v.yes)}</p><div class="b2-grid g2">${v.cards.map(([e, a, b]) => card(e, E(a), E(b))).join('')}</div>`),
      sec('sensing', 'soft', head('Positioning', sn.title) +
        `<div class="b2-layers">${sn.layers.map(([n, s, items, core]) => `<div class="layer${core ? ' core' : ''}"><span class="ln">${E(n)}<small>${E(s)}</small></span><div class="items">${items.map(i => `<span>${E(i)}</span>`).join('')}</div></div>`).join('')}</div>
        <p class="notice mt-s"><span><b>왜</b> · ${E(sn.why)}</span></p>`),
      sec('fit', '', head('Market Fit', f.title) +
        `<div class="b2-qs">${f.qs.map((q, i) => `<div class="q"><span class="mark">${i + 1}</span><p>${E(q)}</p></div>`).join('')}</div>
        <p class="fine">${E(f.stackNote)}</p><div class="b2-stack">${f.stack.map(s => `<span>${E(s)}</span>`).join('<i>+</i>')}</div>`),
      sec('precision', 'soft', head('Precision &amp; Fusion', pr.title) +
        `<div class="b2-err" aria-label="기술별 위치 오차">${pr.bars.map(([l, w, c, t]) => `<div class="erow"><span class="el">${E(l)}</span><div class="et"><b class="${c}" style="width:${w}%"></b></div><span class="ev">${E(t)}</span></div>`).join('')}
          <div class="erow axis"><span></span><div class="ticks"><span>0</span><span>20m</span><span>40m</span><span>60m</span></div><span></span></div></div>
        <div class="b2-grid g2">${pr.cards.map(([e, a, b, k]) => card(e, E(a), E(b), `<p class="big">${E(k)}</p>`)).join('')}</div>
        <h3 class="sub-title mt-m">${E(pr.fusionTitle)}</h3>
        <div class="spec-table-wrap"><table class="spec-table fit"><thead><tr><th scope="col">기술</th><th scope="col">강점</th><th scope="col">한계</th><th scope="col">적합 대상</th></tr></thead><tbody>${pr.fusion.map(r => `<tr><th scope="row">${E(r[0])}</th>${r.slice(1).map(c => `<td>${E(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>
        <div class="b2-flow">${pr.flow.map((s, i) => `<span class="s${i === 2 ? ' add' : i === 3 ? ' now' : ''}">${E(s)}</span>`).join('<i>→</i>')}</div>
        <h3 class="sub-title mt-m">${E(pr.gapTitle)}</h3>
        <div class="b2-grid g2"><div class="b2-card"><h3>SmartTag3 실사용 테스트</h3><p>${E(pr.test.lead)}</p><ul>${pr.test.found.map(x => `<li><b>${E(x)}</b></li>`).join('')}</ul><h3 class="mt-s">원인 추정</h3><ul>${pr.test.cause.map(x => `<li>${E(x)}</li>`).join('')}</ul><p class="big">${E(pr.test.note)}</p></div>
        <div class="b2-card edge-tag"><h3>보완 서비스 제안</h3><ul>${pr.fix.map(([a, b]) => `<li><b>${E(a)}</b>${E(b)}</li>`).join('')}</ul></div></div>`),
      sec('markets', '', head('10 B2B Markets', m.title) +
        `<div class="b2-mkt"><div class="row head" aria-hidden="true"><span>순위</span><span>시장</span><span>주요 고객</span><span>솔루션</span><span>평가</span></div>${m.rows.map(([n, c, s, sc, hl], i) => `<div class="row${hl ? ' hl' : ''}"><span class="rk">${i + 1}</span><span class="nm">${E(n)}</span><span class="cu">${E(c)}</span>${chip(s)}<span class="bar ${/Guide/.test(s) ? 'guide' : 'track'}"><i style="--w:${sc * 20}%"></i><em>${sc.toFixed(1)}</em></span></div>`).join('')}</div>
        <p class="fine mt-s">${E(m.note)}</p>
        <h3 class="sub-title mt-m">${E(m.vsTitle)}</h3>
        <div class="b2-vs">${m.vs.map(([c, t, li, win]) => `<div class="b2-card${win ? ' win' : ''}">${chip(c)}<h3 class="mt-s">${E(t)}</h3><ul>${li.map(x => `<li>${E(x)}</li>`).join('')}</ul></div>`).join('<span class="mid">vs</span>')}</div>
        <p class="notice mt-s"><span><b>교육 분야 수요 근거</b> · ${E(m.edu)}</span></p>`),
      sec('prospects', 'soft', head('Prospects', ps.title, '공개 사업자 정보로 발굴한 후보입니다. 접촉·계약 실적이 아닙니다.') +
        `<h3 class="sub-title">${E(ps.rentalTitle)}</h3>
        <div class="b2-grid g3">${ps.rental.map(([n, t, a, p, first]) => `<div class="b2-card prospect${first ? ' first' : ''}"><div class="top"><h3>${E(n)}</h3>${first ? '<span class="b2-chip tag">우선 접촉</span>' : chip('Track')}</div><p>${E(t)}</p><p class="addr">${E(a)}</p><p class="pitch"><span>제안</span> ${E(p)}</p></div>`).join('')}
          <div class="b2-card dashed"><h3>확인이 필요한 것</h3><p>${E(ps.caveat)}</p></div></div>
        <div class="b2-district"><span class="fine">지역 분포</span>${ps.districts.map(([g, n]) => `<span class="d">${E(g)} <b>${n}</b></span>`).join('')}</div>
        <h3 class="sub-title mt-m">${E(ps.logiTitle)}</h3>
        <div class="b2-grid g2">${ps.logi.map(([n, s, t, w, u, l]) => card('track', E(n), `<span class="fine">${E(s)}</span><br>${t}`, `${w ? `<p class="fine">${E(w)}</p>` : ''}<p class="fine"><a href="${E(u)}" target="_blank" rel="noopener">${E(l)}</a></p>`)).join('')}</div>
        <h3 class="sub-title mt-m">${E(ps.guideTitle)}</h3>
        <div class="spec-table-wrap"><table class="spec-table fit"><thead><tr><th scope="col">잠재 고객</th><th scope="col">제안 서비스</th><th scope="col">우선 검증 내용</th></tr></thead><tbody>${ps.guide.map(([a, b]) => `<tr><th scope="row">${E(a)}</th><td>${chip('Guide')}</td><td>${E(b)}</td></tr>`).join('')}</tbody></table></div>
        <p class="fine mt-s">${E(ps.guideNote)}</p>
        <p class="notice mt-s"><span><b>사람의 위치를 다룰 때 반드시 갖출 것</b> · ${E(ps.privacy)}</span></p>`),
      sec('focus', '', head('Beachhead', '추천 초기 3개 시장.') +
        `<div class="b2-seq">${d.focus.map(([e, t, c, p], i) => `<div class="item"><span class="num">${i + 1}</span>${card(e, `${E(t)} <span class="b2-chip ${e}">${E(c)}</span>`, E(p))}</div>`).join('')}</div>`),
      sec('model', 'soft', head('Business Model', '하나의 플랫폼, 세 개의 상품.') +
        `<div class="b2-grid g3">${d.model.products.map(([e, n, fn, rev]) => card(e, E(n), E(fn), `<p class="b2-rev"><b>${E(rev)}</b>수익 모델</p>`)).join('')}</div>
        <p class="b2-platform">${E(d.model.platform)}</p>`),
      sec('roadmap', 'dark', head('Sensing Roadmap', '센서를 하나씩 더하고,<br>조합을 자동화한다.') +
        `<div class="b2-tl">${d.roadmap.map(([s, a, b]) => `<div class="wk"><b>${E(s)}</b><p><strong>${E(a)}</strong><br>${E(b)}</p></div>`).join('')}</div>`),
      sec('plan', '', head('Next 30 Days', '인터뷰에서 유료 PoC까지 4주.') +
        `<div class="b2-tl light">${d.plan.map(([w, t]) => `<div class="wk"><b>${E(w)}</b><p>${E(t)}</p></div>`).join('')}</div>
        <h3 class="sub-title mt-m">최초 인터뷰에서 던질 질문</h3>
        <div class="b2-ask"><div class="no"><span class="b2-lbl">이렇게 묻지 않는다</span><p>${E(d.ask.no)}</p></div><div class="yes"><span class="b2-lbl">이렇게 묻는다</span><p>${E(d.ask.yes)}</p></div></div>
        <p class="fine mt-s">${E(d.ask.note)}</p>`),
      sec('direction', 'soft', head('Direction', dr.en, `${E(dr.ko)} · 핵심 기반기술 <b>Sensing</b>: 위치 오차 보정과 대상별 최적 센서 조합`) +
        `<div class="b2-flow">${dr.flow.map(([c, t]) => `<span class="s ${c}">${E(t)}</span>`).join('<i>+</i>')}</div>
        <div class="b2-grid g2">${card('ent', '현재 확보한 것', E(dr.have))}${card('tag', '다음에 확인할 것', E(dr.next))}</div>
        <p class="fine mt-s">${E(dr.close)} (갱신 ${E(d.updated)})</p>`)
    ];
    root.innerHTML = html.join('\n');
    if (location.hash) { const t = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t) t.scrollIntoView(); }
  }).catch(() => { root.innerHTML = '<section class="wrap" style="padding:120px 0"><p>내용을 불러오지 못했습니다.</p></section>'; });
})();
