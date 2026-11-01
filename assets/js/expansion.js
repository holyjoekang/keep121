/* 확장 사업계획 페이지: data/expansion.json 을 받아 [data-expansion] 자리에 페이지 전체를 그린다. */
(() => {
  'use strict';
  const box = document.querySelector('[data-expansion]');
  if (!box) return;
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const ul = a => `<ul class="sp-list">${a.map(x => `<li>${E(x)}</li>`).join('')}</ul>`;
  const table = (head, rows, cls = '') => `<div class="spec-table-wrap reveal"><table class="spec-table ${cls}"><thead><tr>${head.map(h => `<th scope="col">${E(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map((c, i) => i ? `<td>${E(c)}</td>` : `<th scope="row">${E(c)}</th>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  const sec = (id, cls, eyebrow, title, lead, body) => `<section class="${cls}" id="${id}"><div class="wrap"><div class="head reveal"><span class="eyebrow">${E(eyebrow)}</span><h2>${title}</h2>${lead ? `<p>${E(lead)}</p>` : ''}</div>${body}</div></section>`;
  const bar = (v, max, label) => `<div class="xp-bar"><i style="width:${Math.max(2, v / max * 100)}%"></i><span>${E(label)}</span></div>`;

  const render = d => {
    const h = d.hero, z = d.size, maxT = Math.max(...z.rows.map(r => r[1])), maxR = Math.max(...d.revenue.rows.map(r => r[1]));
    box.innerHTML = [
      `<section class="page-hero"><div class="wrap"><nav class="crumb" aria-label="현재 위치"><a href="index.html">홈</a><span aria-hidden="true">/</span><a href="usecases.html">시장</a><span aria-hidden="true">/</span><b>확장 사업계획</b></nav>
<div class="page-hero-grid"><div><span class="eyebrow">${E(h.eyebrow)}</span><h1>${h.title}</h1><p>${E(h.text)}</p><p class="modoo-updated">작성 <b>${E(d.updated)}</b> · 추정치는 인터뷰·파일럿으로 검증 예정</p></div>
<div class="page-facts">${h.facts.map(([v, u, l]) => `<div><b>${E(v)}<small>${E(u)}</small></b><span>${E(l)}</span></div>`).join('')}</div></div></div></section>`,
      `<nav class="subnav" id="subnav" aria-label="이 페이지의 내용"><div class="wrap"><span class="subnav-k">이 페이지</span>${d.nav.map(([id, l]) => `<a href="#${id}">${E(l)}</a>`).join('')}</div></nav>`,
      sec('why', '', 'Why Expand', '여행만으로는<br><span class="hl">천장이 10억 원대.</span>', d.why.lead,
        `<div class="xp-cards">${d.why.cards.map(([k, v, p]) => `<article class="reveal"><span>${E(k)}</span><b>${E(v)}</b><p>${E(p)}</p></article>`).join('')}</div><p class="xp-callout reveal">${E(d.why.callout)}</p>`),
      sec('engine', 'soft', 'Same Engine', '파는 것은 추적기가 아니라<br><span class="hl">빠짐없이 확인했다는 사실.</span>', d.engine.lead, table(['엔진', '여행 (현재)', '확장 세그먼트'], d.engine.rows)),
      sec('segments', '', 'New Segments', '국내에서 매일 반복되는<br><span class="hl">보호가 필요한 이동.</span>', '',
        `<div class="xp-segs">${d.segments.map(s => `<article class="xp-seg reveal" id="seg-${E(s.id)}"><div class="xp-seg-top"><span class="lbl plan">${E(s.tag)}</span><h3>${E(s.name)}</h3><em>${E(s.people)}</em></div>
<div class="xp-facts">${s.facts.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div>
<dl><dt>문제</dt><dd>${E(s.pain)}</dd><dt>Keep121이 주는 것</dt><dd>${E(s.value)}</dd><dt>결제자</dt><dd>${E(s.payer)}</dd><dt>제품</dt><dd>${E(s.product)}</dd><dt>가격 (가정)</dt><dd><b>${E(s.price)}</b></dd></dl></article>`).join('')}</div>`),
      sec('size', 'soft', 'Market Size', 'TAM 약 2,600억 · SAM 약 890억,<br><span class="hl">현재의 약 8배.</span>', z.lead,
        `<div class="xp-totals reveal">${z.totals.map(([k, v]) => `<div><span>${E(k)}</span><b>${E(v)}</b></div>`).join('')}</div>
<div class="spec-table-wrap reveal"><table class="spec-table"><thead><tr><th scope="col">세그먼트</th><th scope="col">TAM (억 원)</th><th scope="col">SAM (억 원)</th><th scope="col">산출</th><th scope="col">SAM 기준</th></tr></thead><tbody>
${z.rows.map(([n, t, s, f, b]) => `<tr><th scope="row">${E(n)}</th><td>${bar(t, maxT, t.toLocaleString('ko-KR'))}</td><td>${s ? bar(s, maxT, s.toLocaleString('ko-KR')) : '—'}</td><td>${E(f)}</td><td>${E(b)}</td></tr>`).join('')}</tbody></table></div>
<h3 class="xp-h reveal">SAM 비교</h3><div class="xp-compare reveal">${z.compare.map(([n, v, l]) => `<div><span>${E(n)}</span>${bar(v, 891, l)}</div>`).join('')}</div><p class="xp-note reveal">${E(z.note)}</p>`),
      sec('priority', '', 'Priority', '진입 순서는<br><span class="hl">학교 → 유치원 → 치매.</span>', d.priority.lead,
        `<div class="spec-table-wrap reveal"><table class="spec-table xp-score"><thead><tr>${d.priority.head.map(x => `<th scope="col">${E(x)}</th>`).join('')}</tr></thead><tbody>${d.priority.rows.map(r => `<tr><th scope="row">${E(r[0])}</th>${r.slice(1, -1).map(n => `<td><span class="xp-dot" style="--n:${n}">${n}</span></td>`).join('')}<td><b>${r.at(-1)}</b></td></tr>`).join('')}</tbody></table></div>${ul(d.priority.why)}`),
      sec('products', 'soft', 'Product Lineup', '엔진은 하나,<br><span class="hl">화면 모드와 케이스만 다르게.</span>', '', table(d.products.head, d.products.rows) + `<p class="xp-note reveal">${E(d.products.note)}</p>`),
      sec('roadmap', 'dark', 'Roadmap', '관문을 넘을 때만<br><span class="hl">다음 세그먼트로.</span>', '',
        `<ol class="xp-road">${d.roadmap.map(([t, n, p]) => `<li class="reveal"><span>${E(t)}</span><b>${E(n)}</b><p>${E(p)}</p></li>`).join('')}</ol>`),
      sec('revenue', '', 'Revenue Path', '2031년 45억 원,<br><span class="hl">SAM의 5%.</span>', d.revenue.lead,
        `<div class="xp-rev reveal">${d.revenue.rows.map(([y, v, p]) => `<div><span>${E(y)}</span><div class="xp-col"><i style="height:${v / maxR * 100}%"></i></div><b>${v}억</b><em>${E(p)}</em></div>`).join('')}</div><p class="xp-note reveal">${E(d.revenue.note)}</p>`),
      sec('competition', 'soft', 'Competition', '개인 추적기가 아니라<br><span class="hl">기관용 1:N 도구.</span>', '', table(d.competition.head, d.competition.rows) + `<p class="xp-callout reveal">${E(d.competition.callout)}</p>`),
      sec('risk', '', 'Regulation · Risk', '규제와 리스크.', '', table(['항목', '내용', '대응'], d.risk)),
      sec('psst', 'soft', 'PSST', '모두의 창업 사업계획서<br><span class="hl">v2.1에 이렇게 넣습니다.</span>', '멘토링 1회차 피드백(문제 5개, SOM 3년 3%·5년 5%, 실제 고객 인터뷰)과 연결합니다.', table(['항목', '반영 내용'], d.psst) + `<p class="sp-back reveal"><a class="btn btn-primary" href="modoo-m1.html#feedback">멘토링 1회차 피드백 보기</a></p>`),
      sec('next', '', 'Next 30 Days', '다음 30일.', '', table(['과제', '내용', '시점'], d.next)),
      sec('sources', 'soft', 'Sources', '출처.', '수치는 보도·공공자료 기준이며, 사업계획서에 쓰기 전 원자료로 다시 확인합니다.', `<ol class="xp-src reveal">${d.sources.map(([t, u]) => `<li><a href="${E(u)}" target="_blank" rel="noopener">${E(t)} ↗</a></li>`).join('')}</ol>`),
    ].join('');
    box.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
    const links = [...box.querySelectorAll('#subnav a')], secs = links.map(a => box.querySelector(a.hash));
    const spy = () => { const cur = secs.filter(x => x && x.getBoundingClientRect().top < innerHeight * .4).at(-1); links.forEach(a => a.classList.toggle('active', !!cur && a.hash === '#' + cur.id)); };
    addEventListener('scroll', spy, { passive: true }); spy();
    if (location.hash) box.querySelector(decodeURIComponent(location.hash))?.scrollIntoView();
  };
  fetch('data/expansion.json', { cache: 'no-cache' }).then(r => r.json()).then(render)
    .catch(() => { box.innerHTML = '<section class="wrap" style="padding:120px 0"><p>내용을 불러오지 못했습니다. 잠시 뒤 다시 열어 주세요.</p></section>'; });
})();
