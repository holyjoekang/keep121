/* 모두의 창업 멘토링 회차 상세 페이지: content/modoo/sessions/NN.json 을 받아 [data-session] 자리에 페이지 전체를 그린다. */
(() => {
  'use strict';
  const box = document.querySelector('[data-session]');
  if (!box) return;
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const NUM = '①②③④⑤⑥⑦⑧⑨⑩';
  const ul = a => `<ul class="sp-list">${a.map(x => `<li>${E(x)}</li>`).join('')}</ul>`;
  const table = (rows, cls = '') => `<div class="spec-table-wrap"><table class="spec-table ${cls}"><thead><tr>${rows[0].map(h => `<th scope="col">${E(h)}</th>`).join('')}</tr></thead><tbody>${rows.slice(1).map(r => `<tr>${r.map((c, i) => i ? `<td>${E(c)}</td>` : `<th scope="row">${E(c)}</th>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  const B = {
    p: t => `<p>${E(t)}</p>`,
    list: ul,
    quote: t => `<blockquote class="sp-quote">${E(t)}</blockquote>`,
    warn: t => `<p class="sp-warn"><b>멘토링 반영</b> ${E(t)}</p>`,
    table: r => table(r),
    steps: a => `<ol class="sp-steps">${a.map(([t, s]) => `<li><b>${E(t)}</b><span>${E(s)}</span></li>`).join('')}</ol>`,
  };
  const blocks = bs => bs.map(b => Object.entries(b).map(([k, v]) => (B[k] || (() => ''))(v)).join('')).join('');
  const sec = (id, cls, eyebrow, title, lead, body) => `<section class="${cls}" id="${id}"><div class="wrap"><div class="head reveal"><span class="eyebrow">${E(eyebrow)}</span><h2>${title}</h2>${lead ? `<p>${E(lead)}</p>` : ''}</div>${body}</div></section>`;

  const render = s => {
    const fbTitle = i => `${NUM[i - 1]} ${s.feedback[i - 1].title}`;
    const nav = [['overview', '개요'], ['notes', '회의 메모'], ['feedback', '멘토 피드백'], ['changes', '바꿀 것'], ['problems', '문제 5개'], ['som', 'SOM 다시 보기'], ['interview', '인터뷰 계획'], ['actions', '후속 과제'], ['prompt', '작성 프롬프트'], ['plan', '사업계획서 v2.0']];
    const parts = [
      `<section class="page-hero"><div class="wrap">
<nav class="crumb" aria-label="현재 위치"><a href="index.html">홈</a><span aria-hidden="true">/</span><a href="modoo.html">모두의 창업</a><span aria-hidden="true">/</span><b>멘토링 ${s.n}회차</b></nav>
<div class="page-hero-grid"><div><span class="eyebrow">Mentoring ${s.n} · ${E(s.kind)}</span><h1>멘토링 ${s.n}회차,<br>${E(s.title)}.</h1><p>${E(s.summary)}</p></div>
<div class="page-facts">${s.facts.map(([k, v]) => `<div><b class="sp-fk">${E(k)}</b><span>${E(v)}</span></div>`).join('')}</div></div></div></section>`,
      `<nav class="subnav" id="subnav" aria-label="이 페이지의 내용"><div class="wrap"><span class="subnav-k">이 페이지</span>${nav.map(([id, l]) => `<a href="#${id}">${E(l)}</a>`).join('')}</div></nav>`,
      sec('overview', '', 'Overview', '무엇을 들고 가서,<br><span class="hl">무엇을 받아 왔나.</span>', '', `<ol class="ses-flow reveal">${s.process.map(([t, p]) => `<li><b>${E(t)}</b><p>${E(p)}</p></li>`).join('')}</ol>
<div class="sp-two reveal"><a class="sp-doc" href="#prompt"><span>검토 자료 ①</span><b>${E(s.prompt.title)}</b><em>${E(s.prompt.structure.length)}개 장 · 대화형 작성 가이드</em></a><a class="sp-doc" href="#plan"><span>검토 자료 ②</span><b>${E(s.plan.title)}</b><em>${E(s.plan.meta)}</em></a></div>`),
      sec('notes', 'soft', 'Meeting Memo · ' + s.when, '회의 메모.', '멘토가 한 말을 회의 직후 받아 적은 메모입니다. 녹음 끝부분의 마이크 점검 대화는 뺐습니다.', `<ol class="sp-notes reveal">${s.notes.map(t => `<li>${E(t)}</li>`).join('')}</ol>`),
      sec('feedback', '', 'Mentor Feedback', `멘토 피드백 ${s.feedback.length}가지.`, '메모를 주제별로 정리하고, 사업계획서에 어떻게 반영할지 붙였습니다.', `<div class="ses-fb">${s.feedback.map((f, i) => `<article class="reveal" id="fb-${i + 1}"><div class="t"><span>${i + 1}</span><em>${E(f.tag)}</em></div><b>${E(f.title)}</b><blockquote>${E(f.body)}</blockquote><p><strong>→ 반영</strong> ${E(f.apply)}</p></article>`).join('')}</div>`),
      sec('changes', 'soft', 'Before → After', '사업계획서에서<br><span class="hl">바꿀 것.</span>', '', `<div class="reveal">${table([['항목', '지금 (v2.0)', '멘토링 후'], ...s.gaps])}</div>`),
      sec('problems', '', 'Feedback ⑦', '솔루션 5개에 맞춘<br><span class="hl">문제 정의 5개.</span>', s.problems5.lead, `<div class="reveal">${table([['문제', '누가 겪나', '대응 구성'], ...s.problems5.rows])}</div>`),
      sec('som', 'soft', 'Feedback ⑥', 'SOM 다시 보기<br><span class="hl">3년 3% · 5년 5%.</span>', s.somCheck.lead, `<div class="reveal">${table([['구분', '규모', '산출 기준'], ...s.somCheck.rows])}</div><p class="sp-warn reveal"><b>해석</b> ${E(s.somCheck.note)}</p>`),
      sec('interview', '', 'Feedback ④ · ⑤', '실제 타겟 고객<br><span class="hl">인터뷰 계획.</span>', s.interviewPlan.lead, `<div class="sp-groups">${s.interviewPlan.groups.map(([g, n, qs]) => `<article class="reveal"><span>${E(n)}</span><h3>${E(g)}</h3>${ul(qs)}</article>`).join('')}</div><p class="sp-warn reveal"><b>기록 원칙</b> ${E(s.interviewPlan.rule)}</p>`),
      sec('actions', 'soft', 'Next Actions', '후속 과제.', '11월 30일 사업계획서 v2.1 완성을 목표로 합니다.', `<div class="reveal">${table([['과제', '내용', '목표 시점'], ...s.actions])}</div>`),
      sec('prompt', '', 'Material ①', E(s.prompt.title) + '.', s.prompt.text, `<ul class="ses-struct sp-struct reveal">${s.prompt.structure.map(([n, t, p]) => `<li><span>${E(n)}</span><b>${E(t)}</b><p>${E(p)}</p></li>`).join('')}</ul><p class="sp-warn reveal"><b>주의</b> ${E(s.prompt.caution)}</p>`),
      sec('plan', 'soft', 'Material ② · ' + s.plan.meta, E(s.plan.title) + ',<br><span class="hl">장별로 다시 읽기.</span>', '각 장에 해당하는 멘토 피드백을 함께 표시했습니다.', `<p class="ses-head sp-headline reveal">${E(s.plan.headline)}</p>
<div class="ses-kpis reveal">${s.plan.kpis.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div>
<div class="sp-chapters">${s.plan.chapters.map(c => `<details class="sp-ch reveal"${c.no === '0' ? ' open' : ''}><summary><span>${E(c.no)}</span><b>${E(c.title)}</b>${c.fb.length ? `<em>${c.fb.map(i => `<a href="#fb-${i}" title="${E(fbTitle(i))}">${NUM[i - 1]}</a>`).join('')}</em>` : ''}</summary><div class="sp-body">${blocks(c.blocks)}</div></details>`).join('')}</div>
<button type="button" class="sp-all">모든 장 펼치기</button><p class="sp-warn">${E(s.plan.note)}</p>
<p class="sp-back"><a class="btn btn-primary" href="modoo.html#sessions">모두의 창업 진행 기록으로</a></p>`),
    ];
    box.innerHTML = parts.join('');
    box.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
    const all = box.querySelector('.sp-all'), chs = [...box.querySelectorAll('.sp-ch')];
    all.addEventListener('click', () => { const o = chs.some(d => !d.open); chs.forEach(d => (d.open = o)); all.textContent = o ? '모든 장 접기' : '모든 장 펼치기'; });
    const links = [...box.querySelectorAll('#subnav a')], secs = links.map(a => box.querySelector(a.hash));
    const spy = () => { const cur = secs.filter(x => x && x.getBoundingClientRect().top < innerHeight * .4).at(-1); links.forEach(a => a.classList.toggle('active', cur && a.hash === '#' + cur.id)); };
    addEventListener('scroll', spy, { passive: true }); spy();
    if (location.hash) box.querySelector(decodeURIComponent(location.hash))?.scrollIntoView();
  };

  fetch(`content/modoo/sessions/${box.dataset.session}.json`, { cache: 'no-cache' }).then(r => r.json()).then(render)
    .catch(() => { box.innerHTML = '<section class="wrap" style="padding:120px 0"><p>기록을 불러오지 못했습니다. 잠시 뒤 다시 열어 주세요.</p></section>'; });
})();
