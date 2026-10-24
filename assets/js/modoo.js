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
    log: m => m.log.map(r => `<li class="reveal"><time datetime="${E(r.date)}">${E(r.date.length === 7 ? `${+r.date.slice(5)}월` : r.date.slice(5).replace('-', '/'))}</time><span class="lbl ${r.kind === '메일' ? 'est' : r.kind === '지출' ? 'chk' : 'meas'}">${E(r.kind)}</span><div><b>${E(r.title)}</b><p>${E(r.text)}</p></div></li>`).join(''),
  };

  fetch('data/modoo.json', { cache: 'no-cache' }).then(r => r.json()).then(m => {
    document.querySelectorAll('[data-modoo]').forEach(el => { const f = R[el.dataset.modoo]; if (f) el.innerHTML = f(m); });
    // main.js 가 먼저 붙었으면 새로 그린 .reveal 도 보이게
    document.querySelectorAll('[data-modoo] .reveal').forEach(el => el.classList.add('in'));
  });
})();
