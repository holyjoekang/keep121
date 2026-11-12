/* 맞춤 제안 목록: data/proposals.json 을 받아 [data-proposals] 를 카드로 채운다. (원본: scripts/proposals.js) */
(() => {
  'use strict';
  const root = document.querySelector('[data-proposals]');
  if (!root) return;
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);

  fetch('data/proposals.json', { cache: 'no-cache' }).then(r => r.json()).then(d => {
    const h = d.hero;
    const tags = ['전체', ...new Set(d.items.map(i => i.tag))];
    root.innerHTML = `
      <section class="page-hero has-photo" style="--bg:url('${E(h.img)}')"><div class="wrap">
        <nav class="crumb" aria-label="현재 위치"><a href="index.html">홈</a><span aria-hidden="true">/</span><b>맞춤 제안</b></nav>
        <span class="eyebrow">${E(h.eyebrow)}</span><h1>${h.title}</h1><p>${E(h.text)}</p>
        <div class="pp-count"><b>${d.items.length}</b>건 공개 · ${E(h.count)}</div>
      </div></section>
      <section class="pp-wrap"><div class="wrap">
        <div class="pp-filter" role="tablist" aria-label="제안 분류">${tags.map((t, i) => `<button role="tab" aria-selected="${i === 0}" data-t="${E(t)}">${E(t)}</button>`).join('')}</div>
        <div class="pp-grid">${d.items.map(p => `
          <article class="pp-card" data-tag="${E(p.tag)}">
            <a class="pp-im" href="${E(p.href)}" style="background-image:url('${E(p.img)}');background-position:${E(p.pos || 'center')}" aria-label="${E(p.title)} 자세히 보기">
              <span class="pp-tag">${E(p.tag)}</span><span class="pp-date">${E(p.date)}</span></a>
            <div class="pp-body">
              <span class="pp-client">${E(p.client)}</span>
              <h3>${E(p.title)}</h3>
              <p>${E(p.summary)}</p>
              <ul>${p.points.map(x => `<li>${E(x)}</li>`).join('')}</ul>
              <div class="pp-stats">${p.stats.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div>
              <div class="pp-foot"><span class="pp-mix">${p.mix.map(m => `<i class="${E(m.toLowerCase())}">${E(m)}</i>`).join('')}</span>
                <a class="btn btn-primary pp-go" href="${E(p.href)}">자세히 보기 <svg class="icon"><use href="#i-arrow"/></svg></a></div>
            </div>
          </article>`).join('')}
          <article class="pp-card pp-next"><div class="pp-body"><span class="pp-client">Coming next</span><h3>${E(d.next.title)}</h3><p>${E(d.next.text)}</p>
            <a class="btn btn-ghost pp-go" href="company.html#contact">맞춤 제안 요청하기 <svg class="icon"><use href="#i-arrow"/></svg></a></div></article>
        </div>
        <p class="fine mt-m">${E(d.note)}</p>
      </div></section>`;
    const btns = [...root.querySelectorAll('.pp-filter button')];
    btns.forEach(b => b.addEventListener('click', () => {
      btns.forEach(x => x.setAttribute('aria-selected', x === b));
      root.querySelectorAll('.pp-card[data-tag]').forEach(c => { c.hidden = !(b.dataset.t === '전체' || c.dataset.tag === b.dataset.t); });
    }));
  });
})();
