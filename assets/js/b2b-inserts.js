/* B2B 확장 내용을 기존 페이지 곳곳에 끼워 넣는다. (원본: scripts/b2b-inserts.js)
   [data-b2b-insert="키"] 자리를 data/b2b-inserts.json(배치·제목) + data/b2b.json(내용)으로 채운다. */
(() => {
  'use strict';
  const mounts = document.querySelectorAll('[data-b2b-insert]');
  if (!mounts.length) return;
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const tone = t => (/Guide/.test(t) ? 'guide' : /Track/.test(t) ? 'track' : 'tag');
  const card = (edge, h, p, extra = '') => `<div class="b2-card edge-${edge}"><h3>${h}</h3><p>${p}</p>${extra}</div>`;
  const T = {
    route: d => `<div class="b2-grid g3">${d.model.products.map(([e, n, fn, rev]) => card(e, E(n), E(fn), `<p class="b2-rev"><b>${E(rev)}</b>수익 모델</p>`)).join('')}</div>
      <div class="b2-layers mt-s"><div class="layer core"><span class="ln">Keep121 Sensing<small>공통 기반기술</small></span><div class="items">${d.sensing.layers[1][2].map(i => `<span>${E(i)}</span>`).join('')}</div></div></div>`,
    precision: d => `<div class="b2-grid g2">${d.precision.cards.map(([e, a, b, k]) => card(e, E(a), E(b), `<p class="big">${E(k)}</p>`)).join('')}</div>`,
    fusion: d => `<div class="spec-table-wrap"><table class="spec-table fit"><thead><tr><th scope="col">기술</th><th scope="col">강점</th><th scope="col">한계</th><th scope="col">적합 대상</th></tr></thead><tbody>${d.precision.fusion.map(r => `<tr><th scope="row">${E(r[0])}</th>${r.slice(1).map(c => `<td>${E(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>
      <div class="b2-flow">${d.precision.flow.map((s, i) => `<span class="s${i === 2 ? ' add' : i === 3 ? ' now' : ''}">${E(s)}</span>`).join('<i>→</i>')}</div>`,
    trackflow: (d, x) => `<div class="b2-tl light">${x.steps.map(([a, b]) => `<div class="wk"><b>${E(a)}</b><p>${E(b)}</p></div>`).join('')}</div>
      <p class="b2-note"><b>사람의 위치를 다룰 때</b> · ${E(d.prospects.privacy)}</p>`,
    markets: d => `<div class="b2-mkt">${d.markets.rows.map(([n, c, s, sc, hl], i) => `<div class="row${hl ? ' hl' : ''}"><span class="rk">${i + 1}</span><span class="nm">${E(n)}</span><span class="cu">${E(c)}</span><span class="b2-chip ${tone(s)}">${E(s)}</span><span class="bar ${tone(s) === 'guide' ? 'guide' : 'track'}"><i style="--w:${sc * 20}%"></i><em>${sc.toFixed(1)}</em></span></div>`).join('')}</div><p class="fine mt-s">${E(d.markets.note)}</p>`,
    ask: d => `<div class="b2-ask"><div class="no"><span class="b2-lbl">이렇게 묻지 않는다</span><p>${E(d.ask.no)}</p></div><div class="yes"><span class="b2-lbl">이렇게 묻는다</span><p>${E(d.ask.yes)}</p></div></div><p class="fine mt-s">${E(d.ask.note)}</p>`,
    revenue: d => T.route(d).split('<div class="b2-layers')[0] + `<p class="b2-platform">${E(d.model.platform)}</p>`,
    focus: d => `<div class="b2-seq">${d.focus.map(([e, t, c, p], i) => `<div class="item"><span class="num">${i + 1}</span>${card(e, `${E(t)} <span class="b2-chip ${e}">${E(c)}</span>`, E(p))}</div>`).join('')}</div>`,
    roadmap: d => `<div class="b2-tl light">${d.roadmap.map(([s, a, b]) => `<div class="wk"><b>${E(s)}</b><p><strong>${E(a)}</strong><br>${E(b)}</p></div>`).join('')}</div>`,
    plan: d => `<div class="b2-tl light">${d.plan.map(([w, t]) => `<div class="wk"><b>${E(w)}</b><p>${E(t)}</p></div>`).join('')}</div>`,
    smarttag: d => { const p = d.precision; return `<div class="b2-grid g2"><div class="b2-card"><h3>실사용 테스트</h3><p>${E(p.test.lead)}</p><ul>${p.test.found.map(x => `<li><b>${E(x)}</b></li>`).join('')}${p.test.cause.map(x => `<li>${E(x)}</li>`).join('')}</ul><p class="big">${E(p.test.note)}</p></div><div class="b2-card edge-tag"><h3>보완 서비스</h3><ul>${p.fix.map(([a, b]) => `<li><b>${E(a)}</b>${E(b)}</li>`).join('')}</ul></div></div>`; },
    direction: d => `<div class="b2-flow">${d.direction.flow.map(([c, t]) => `<span class="s ${c}">${E(t)}</span>`).join('<i>+</i>')}</div><p class="fine">${E(d.direction.close)}</p>`,
    partners: d => `<div class="b2-grid g3">${d.prospects.rental.slice(0, 3).map(([n, t, a, p]) => card('track', E(n), E(p))).join('')}</div><p class="fine mt-s">렌털·물류 후보 ${d.prospects.rental.length + d.prospects.logi.length}곳은 공개 사업자 정보로 발굴했으며 도입 의사·예산은 미확인입니다.</p>`
  };
  const get = u => fetch(u, { cache: 'no-cache' }).then(r => r.json());
  Promise.all([get('data/b2b.json'), get('data/b2b-inserts.json')]).then(([d, ins]) => {
    mounts.forEach(m => {
      const x = ins.inserts[m.dataset.b2bInsert];
      if (!x || !T[x.type]) return;
      m.outerHTML = `<section class="b2x ${x.tone || ''}" id="${E(x.id)}" data-b2b><div class="wrap">
        <span class="eyebrow">${E(x.kicker)}</span><h2>${x.title}</h2>${x.text ? `<p class="b2x-lead">${E(x.text)}</p>` : ''}
        ${T[x.type](d, x)}
        <p class="b2x-more"><a href="b2b.html#${E(x.more)}">B2B 확장 전략에서 자세히 보기 →</a></p></div></section>`;
    });
  }).catch(() => mounts.forEach(m => m.remove()));
})();
