/* 모두의 창업 페이지: data/modoo.json(진행 상태)을 받아 [data-modoo] 자리를 채운다. */
(() => {
  'use strict';
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const won = n => (n % 10000 === 0 ? `${(n / 10000).toLocaleString('ko-KR')}만 원` : `${n.toLocaleString('ko-KR')}원`);
  const STATUS = { done: ['meas', '완료'], due: ['due', '할 일'], check: ['chk', '확인 필요'], plan: ['plan', '예정'] };
  const lbl = (st, text) => { const [c, t] = STATUS[st] || STATUS.plan; return `<span class="lbl ${c}">${E(text || t)}</span>`; };
  const d = i => (i % 4 ? ` d${i % 4}` : '');
  const empty = (cols, msg) => `<tr><td colspan="${cols}" class="none">${E(msg)}</td></tr>`;

  const R = {
    updated: m => E(m.updated),
    now: m => m.now.map((c, i) => `<article class="pilot reveal${d(i)}"><span class="id">${i + 1}</span><h3>${E(c.title)}</h3><dl>${c.facts.map(([k, v]) => `<dt>${E(k)}</dt><dd>${E(v)}</dd>`).join('')}</dl><p>${E(c.text)}</p></article>`).join(''),
    schedule: m => m.schedule.map(r => `<tr><th scope="row">${E(r.when)}</th><td>${r.key ? `<b>${E(r.task)}</b>` : E(r.task)}</td><td>${E(r.note)}</td><td>${lbl(r.status, r.label)}</td></tr>`).join(''),
    mentor: m => E(m.mentor),
    mentoring: m => m.mentoring.map((r, i) => `<li class="reveal${d(i)}${r.n <= 2 ? ' hl2' : ''}"><span class="w">${r.n}회차</span><span class="d">${E(r.kind)}</span><p>${E(r.topic)}</p>${r.result ? `<p><b>결과</b> · ${E(r.result)}</p>` : ''}<span class="g">${r.date ? E(r.date) : (r.n <= 2 ? '일정 미정' : '')}</span></li>`).join(''),
    spendPlan: m => m.spendPlan.map(r => `<tr><th scope="row">${E(r.item)}</th><td class="num">${won(r.amount)}</td><td>${r.cat === '확인 필요' ? '<b>확인 필요</b>' : E(r.cat)}</td></tr>`).join('')
      + `<tr class="total"><th scope="row">합계</th><td class="num">${won(m.spendPlan.reduce((a, r) => a + r.amount, 0))}</td><td></td></tr>`,
    expenses: m => (m.expenses.length
      ? m.expenses.map(r => `<tr><td>${E(r.date)}</td><td>${E(r.cat)}</td><td>${E(r.desc)}</td><td class="num">${won(r.amount)}</td><td>${E(r.proof)}</td></tr>`).join('')
        + `<tr class="total"><td colspan="3">사용 합계 · 잔액</td><td class="num">${won(m.expenses.reduce((a, r) => a + r.amount, 0))}</td><td>${won(2000000 - m.expenses.reduce((a, r) => a + r.amount, 0))}</td></tr>`
      : empty(5, '아직 집행 내역이 없습니다. 카드 충전 후 건별로 기록합니다.')),
    ai: m => m.ai.map(r => `<tr><th scope="row">${E(r.round)}</th><td>${E(r.apply)}</td><td>${E(r.use)}</td><td${r.solutions.length ? '' : ' class="none"'}>${r.solutions.length ? r.solutions.map(s => `<b>${E(s.name)}</b> ${won(s.amount)}${s.purpose ? ` · ${E(s.purpose)}` : ''}`).join('<br>') : '신청 후 기록'}</td></tr>`).join(''),
    planSteps: m => m.planSteps.map(r => `<tr><th scope="row">${E(r.step)}</th><td>${E(r.when)}</td><td>${E(r.basis)}</td><td>${lbl(r.status)}</td></tr>`).join(''),
    planV21: m => { const v = m.planV21; if (!v) return ''; const T = (h, rows) => `<div class="spec-table-wrap dark-table"><table class="spec-table"><thead><tr>${h.map(x => `<th scope="col">${x}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr><th scope="row">${E(r[0])}</th>${r.slice(1).map((c, i) => `<td${i === r.length - 2 ? ' class="to"' : ' class="was"'}>${E(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      return `<h3 class="sub-title">${E(v.title)}</h3><p class="fine">${E(v.lead)}</p>${T(['항목', 'v2.0', 'v2.1'], v.compare)}
<h4 class="sub-title">SOM 점검 · 멘토 피드백 ⑥</h4>${T(['기준', 'SAM 기준 금액', 'v2.1'], v.somCheck)}<p class="fine">${E(v.somNote)}</p>
<details class="mt-s"><summary>장별 문안 (PSST 1.2 · 3장) 펼치기</summary><div class="ses-secs">${v.chapters.map(([t, items]) => `<section><h5>${E(t)}</h5><ul>${items.map(x => `<li>${E(x)}</li>`).join('')}</ul></section>`).join('')}</div></details>
<p class="fine mt-s">${E(v.note)} 붙여 넣기용 문서: <a href="${E(v.doc)}">${E(v.doc)}</a> · 상세: <a href="usecases.html#size">시장 규모</a> · <a href="evidence.html#finance">손익표</a></p>`; },
    sessions: m => (m.sessions || []).map(s => `<article class="ses reveal" id="session-${s.n}">
<div class="ses-top"><div><span class="ses-badge">${s.n}회차 · ${E(s.kind)}</span><h3>${E(s.title)}</h3><p>${E(s.summary)}</p></div>
<dl class="ses-facts">${s.facts.map(([k, v]) => `<div><dt>${E(k)}</dt><dd>${E(v)}</dd></div>`).join('')}</dl></div>
${s.process ? `<h4>진행 과정</h4><ol class="ses-flow">${s.process.map(([t, p]) => `<li><b>${E(t)}</b><p>${E(p)}</p></li>`).join('')}</ol>` : ''}
<h4>멘토 피드백 ${s.feedback.length}가지</h4><div class="ses-fb">${s.feedback.map((f, i) => `<article><div class="t"><span>${i + 1}</span><em>${E(f.tag)}</em></div><b>${E(f.title)}</b><blockquote>${E(f.body)}</blockquote><p><strong>→ 반영</strong> ${E(f.apply)}</p></article>`).join('')}</div>
${s.gaps ? `<h4>사업계획서에서 바꿀 것</h4><div class="spec-table-wrap"><table class="spec-table"><thead><tr><th scope="col">항목</th><th scope="col">지금 (v2.0)</th><th scope="col">멘토링 후</th></tr></thead><tbody>${s.gaps.map(([a, b, c]) => `<tr><th scope="row">${E(a)}</th><td class="was">${E(b)}</td><td class="to">${E(c)}</td></tr>`).join('')}</tbody></table></div>` : ''}
${s.actions ? `<h4>후속 과제</h4><div class="spec-table-wrap"><table class="spec-table"><thead><tr><th scope="col">과제</th><th scope="col">내용</th><th scope="col">목표 시점</th></tr></thead><tbody>${s.actions.map(([a, b, c]) => `<tr><th scope="row">${E(a)}</th><td>${E(b)}</td><td>${E(c)}</td></tr>`).join('')}</tbody></table></div>` : ''}
${s.prompt ? `<details><summary>검토 자료 ① ${E(s.prompt.title)} <small>구조 요약</small></summary><div class="ses-in"><p>${E(s.prompt.text)}</p><ul class="ses-struct">${s.prompt.structure.map(([n, t, p]) => `<li><span>${E(n)}</span><b>${E(t)}</b><p>${E(p)}</p></li>`).join('')}</ul>${s.prompt.caution ? `<p class="ses-note">${E(s.prompt.caution)}</p>` : ''}</div></details>` : ''}
${s.plan ? `<details><summary>검토 자료 ② ${E(s.plan.title)} <small>${E(s.plan.meta)}</small></summary><div class="ses-in"><p class="ses-head">${E(s.plan.headline)}</p><div class="ses-kpis">${s.plan.kpis.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div><div class="ses-secs">${s.plan.sections.map(([t, items]) => `<section><h5>${E(t)}</h5><ul>${items.map(x => `<li>${E(x)}</li>`).join('')}</ul></section>`).join('')}</div>${s.plan.note ? `<p class="ses-note">${E(s.plan.note)}</p>` : ''}</div></details>` : ''}
${s.page ? `<p class="ses-more"><a class="btn btn-primary" href="${E(s.page)}">${s.n}회차 상세 페이지 보기 →</a></p>` : ''}
</article>`).join(''),
    log: m => m.log.map(r => `<li class="reveal"><time datetime="${E(r.date)}">${E(r.date.length === 7 ? `${+r.date.slice(5)}월` : r.date.slice(5).replace('-', '/'))}</time><span class="lbl ${r.kind === '메일' ? 'est' : r.kind === '지출' ? 'chk' : r.kind === '사업계획서' ? 'plan' : 'meas'}">${E(r.kind)}</span><div><b>${E(r.title)}</b><p>${E(r.text)}</p></div></li>`).join(''),
  };

  fetch('data/modoo.json', { cache: 'no-cache' }).then(r => r.json()).then(m => {
    document.querySelectorAll('[data-modoo]').forEach(el => { const f = R[el.dataset.modoo]; if (f) el.innerHTML = f(m); });
    // main.js 가 먼저 붙었으면 새로 그린 .reveal 도 보이게
    document.querySelectorAll('[data-modoo] .reveal').forEach(el => el.classList.add('in'));
  });
})();
