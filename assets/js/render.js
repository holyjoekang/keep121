/* Keep121 — 페이지 그리기: data/site.json(메뉴·바닥글·페이지 순서)과 content/pages/<id>.html(본문)을 받아
   화면을 채운 뒤 assets/js/main.js(영상·점호 체험·견적 계산기)를 붙인다. */
(() => {
  'use strict';
  const main = document.querySelector('main[data-page]');
  const id = main.dataset.page;
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const brand = '<svg class="brand-mark"><use href="#logo"/></svg><svg class="brand-word" role="img" aria-label="Keep121"><use href="#wordmark"/></svg>';
  const here = id + '.html';

  const nav = s => `<div class="wrap">
    <a class="brand" href="index.html" aria-label="Keep121 홈">${brand}</a>
    <nav class="nav-links" id="navLinks" aria-label="주요 메뉴">
      ${s.nav.map(n => `<a href="${E(n.href)}"${n.href === here ? ' class="active" aria-current="page"' : ''}>${E(n.label)}</a>`).join('\n      ')}
    </nav>
    <a class="btn btn-primary" href="${E(s.cta.href)}">${E(s.cta.label)}</a>
    <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기" aria-expanded="false"><svg class="icon"><use href="#i-menu"/></svg></button>
  </div>`;

  // 이전/다음: site.json 의 페이지 순서를 한 바퀴로 잇는다. 홈에는 달지 않는다.
  const pager = s => {
    const i = s.pages.findIndex(p => p.id === id);
    if (i <= 0) return '';
    const prev = s.pages[(i - 1 + s.pages.length) % s.pages.length], next = s.pages[(i + 1) % s.pages.length];
    return `<nav class="pager" aria-label="페이지 이동">
  <div class="wrap">
    <a class="pg-prev" href="${E(prev.file)}"><span>이전</span><b>${E(prev.name)}</b></a>
    <a class="pg-next" href="${E(next.file)}"><span>다음</span><b>${E(next.name)}</b></a>
  </div>
</nav>`;
  };

  const footer = f => `<div class="wrap">
    <div class="footer-top">
      <div>
        <a class="brand" href="index.html">${brand}</a>
        <div class="footer-tag">${f.tagHtml}</div>
      </div>
      <div class="footer-links">
        ${f.columns.map(c => `<div><h4>${E(c.title)}</h4>${c.links.map(l => `<a href="${E(l.href)}">${E(l.label)}</a>`).join('')}</div>`).join('\n        ')}
      </div>
    </div>
    <p class="disclaimer">${E(f.disclaimer)}</p>
    <p class="copy">${E(f.copy)}</p>
    <p class="photo-credit">${f.creditHtml}</p>
  </div>`;

  const get = (u, as) => fetch(u, { cache: 'no-cache' }).then(r => { if (!r.ok) throw new Error(u + ' ' + r.status); return r[as](); });
  Promise.all([get('data/site.json', 'json'), get(`content/pages/${id}.html`, 'text')]).then(([s, body]) => {
    document.querySelector('[data-mount="nav"]').innerHTML = nav(s);
    main.innerHTML = body + pager(s);
    document.querySelector('[data-mount="footer"]').innerHTML = footer(s.footer);
    if (location.hash) { const t = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t) t.scrollIntoView(); }
    const js = document.createElement('script');
    js.src = 'assets/js/main.js';
    document.body.appendChild(js);
    const pg = s.pages.find(p => p.id === id);
    if (pg && pg.script) { const x = document.createElement('script'); x.src = pg.script; document.body.appendChild(x); }
  }).catch(e => {
    main.innerHTML = `<section class="wrap" style="padding:120px 0"><p>내용을 불러오지 못했습니다 (${E(e.message)}). 잠시 뒤 다시 열어 주세요.</p></section>`;
  });
})();
