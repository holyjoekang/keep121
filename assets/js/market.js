/* 시장 규모·연도별 목표: data/market.json 으로 [data-market="size|targets|stages"] 자리를 채운다. (원본: scripts/market.js) */
(() => {
  'use strict';
  const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const chip = s => `<span class="b2-chip ${s === 'Guide' ? 'guide' : 'track'}">${E(s)}</span>`;
  const table = (head, rows) => `<div class="spec-table-wrap"><table class="spec-table fit"><thead><tr>${head.map(h => `<th scope="col">${h}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`;
  const R = {
    size: m => `<div class="chart-card"><div class="rc2-k" style="margin-bottom:22px"><div><h3>국내 사람·자산 이동관리에서 Keep121 매출까지</h3><p class="sub">${E(m.basis)}</p></div><span class="lbl est">추정</span></div>
      <div class="funnel">${m.funnel.map(([k, s, b, t], i) => `<div class="f${i + 1}"><span class="k">${E(k)}<small>${E(s)}</small></span><div class="bar"><b>${E(b)}</b><span>${E(t)}</span></div></div>`).join('')}</div></div>
      <div class="split top mt-m"><div><h3 class="sub-title" style="margin-top:0">TAM · 사람 (Guide)</h3>${table(['영역', '산식', '억 원'], m.people.map(([n, f, v, s, inSam]) => `<tr><th scope="row">${E(n)}${inSam ? ' <span class="b2-chip tag">SAM</span>' : ''}</th><td>${E(f)}</td><td class="num">${v.toLocaleString('ko-KR')}</td></tr>`))}
        <h3 class="sub-title">TAM · 자산 (Track · Enterprise)</h3><p class="fine">${E(m.asset.formula)} → <b>${m.asset.lo.toLocaleString('ko-KR')}~${m.asset.hi.toLocaleString('ko-KR')}억 원</b>. 국내 자산 추적 시장 공식 통계가 없어 하향식으로 추정했습니다.</p></div>
      <div><h3 class="sub-title" style="margin-top:0">SAM · 초기 진입 시장 <span class="lbl est">추정</span></h3>${table(['시장', '근거', '억 원'], m.sam.map(([n, b, v]) => `<tr><th scope="row">${E(n)}</th><td>${E(b)}</td><td class="num">${v.toLocaleString('ko-KR')}</td></tr>`).concat(`<tr class="total"><th scope="row">합계</th><td></td><td class="num">${m.samTotal.toLocaleString('ko-KR')}</td></tr>`))}
        <h3 class="sub-title">단가 가정</h3>${table(['대상', '단가'], m.prices.map(([a, b]) => `<tr><th scope="row">${E(a)}</th><td>${E(b)}</td></tr>`))}</div></div>
      <h3 class="sub-title mt-m">출처가 있는 수치</h3>${table(['수치', '출처'], m.sources.map(([a, b, u]) => `<tr><th scope="row" class="wide">${E(a)}</th><td>${u ? `<a href="${E(u)}" target="_blank" rel="noopener">${E(b)}</a>` : E(b)}</td></tr>`))}
      <p class="notice mt-s"><span><b>확인하지 못한 수치</b> · ${E(m.gaps)}</span></p>
      <p class="fine mt-s">${E(m.change)}</p>`,
    targets: m => `<div class="stages">${m.years.map((r, i) => `<div class="stage${i === 0 ? ' now' : ''}"><span class="yr">${E(r.y)}</span><h3>${E(r.stage)}</h3><ul>${r.items.map(x => `<li>${E(x)}</li>`).join('')}</ul>${r.gate ? `<span class="gate-k" style="align-self:flex-start">${E(r.gate)}</span>` : ''}<span class="rev-n">매출 ${r.rev ? r.rev + '억 원' : '0 (무상 PoC)'}</span></div>`).join('')}</div>
      <h3 class="sub-title mt-m">연도별 목표 <span class="lbl est">목표</span></h3>
      ${table(['항목'].concat(m.years.map(r => E(r.y))), [
        ['Guide 매출 (억 원)', 'g'], ['Track 매출 (억 원)', 't'], ['Enterprise 매출 (억 원)', 'e'], ['매출 합계 (억 원)', 'rev'],
        ['Guide 고객', 'gc'], ['Track 고객', 'tc'], ['Track 관리 자산 (점)', 'assets'], ['인원 (명)', 'team']
      ].map(([l, k]) => `<tr${k === 'rev' ? ' class="total"' : ''}><th scope="row">${l}</th>${m.years.map(r => `<td class="num">${typeof r[k] === 'number' ? r[k].toLocaleString('ko-KR') : E(r[k])}</td>`).join('')}</tr>`))}
      <p class="fine mt-s">SOM: 2029년 ${m.years[3].rev}억 원, 2031년 ${m.years[5].rev}억 원 (SAM ${m.samTotal.toLocaleString('ko-KR')}억 원 기준). 모든 수치는 목표이며 계약·매출 실적이 아닙니다. <a href="usecases.html#size">시장 규모 산식 보기</a></p>`,
    pnl: (m, p) => {
      const max = Math.max(...p.chart.map(r => r[1] + r[2] + r[3]));
      const n = v => (typeof v === 'number' ? `<td class="num${v < 0 ? ' neg' : ''}">${v.toLocaleString('ko-KR')}</td>` : `<td class="num">${E(v)}</td>`);
      return `<div class="chart-card"><div class="rc2-k" style="margin-bottom:18px"><div><h3>매출 구성 (억 원) · 2027~2031</h3><p class="sub">${E(p.lead)}</p></div><span class="lbl est">가정</span></div>
        <div class="pl-chart" role="img" aria-label="연도별 매출: ${p.chart.map(r => `${r[0]}년 ${(r[1] + r[2] + r[3]).toFixed(2)}억`).join(', ')} 원">${p.chart.map(([y, g, t, e, op]) => `<div class="col"><span class="tot">${+(g + t + e).toFixed(2)}</span><div class="stk" style="height:${((g + t + e) / max * 100).toFixed(1)}%"><i class="e" style="flex:${e}"></i><i class="t" style="flex:${t}"></i><i class="g" style="flex:${g}"></i></div><b>${y}</b><span class="op${op < 0 ? ' neg' : ''}">${op > 0 ? '+' : ''}${op}</span></div>`).join('')}</div>
        <p class="pl-legend"><span><i class="g"></i>Guide</span><span><i class="t"></i>Track</span><span><i class="e"></i>Enterprise</span><span>아래 숫자 = 영업이익 (억 원)</span></p></div>
        <h3 class="sub-title mt-m">손익표 (억 원)</h3>${table(['항목'].concat(p.years), p.rows.map(([l, v, c]) => `<tr${c ? ` class="${c}"` : ''}><th scope="row">${E(l)}</th>${v.map(n).join('')}</tr>`))}
        <p class="fine mt-s">EBITDA 흑자 ${E(p.breakeven.ebitda)}년 · 영업이익 흑자 ${E(p.breakeven.op)}년 · 누적 현금 최저 ${p.breakeven.trough}억 원 (조달 전)</p>
        <div class="split top mt-m"><div><h3 class="sub-title" style="margin-top:0">주요 가정</h3>${table(['항목', '가정'], p.assumptions.map(([a, b]) => `<tr><th scope="row">${E(a)}</th><td>${E(b)}</td></tr>`))}</div>
        <div><h3 class="sub-title" style="margin-top:0">시나리오 비교</h3>${table(['시나리오', '목표 대비', '2031 매출', 'EBITDA 흑자', '영업이익 흑자', '누적 현금 최저'], p.scenarios.map(r => `<tr${r[0] === '기본' ? ' class="total"' : ''}><th scope="row">${E(r[0])}</th>${r.slice(1).map(c => `<td>${E(c)}</td>`).join('')}</tr>`))}<p class="fine mt-s">${E(p.scenarioNote)}</p></div></div>
        <h3 class="sub-title mt-m">자금 조달 · 기본 경로 ${p.fundingTotal}억 원</h3>${table(['시점', '재원', '금액 (억 원)', '용도 · 조건'], p.funding.map(([a, b, c, d]) => `<tr><th scope="row">${E(a)}</th><td>${E(b)}</td><td class="num">${c}</td><td>${E(d)}</td></tr>`).concat(`<tr class="total"><th scope="row">합계</th><td>보조금·R&amp;D·지분 ${p.grantEquity} / 보증·리스 ${p.debt}</td><td class="num">${p.fundingTotal}</td><td>2031년 말 잔액 ${p.buffer}억 원</td></tr>`))}
        <p class="fine mt-s">${E(p.fundingNote)}</p><p class="fine">${E(p.previous)}</p>`;
    },
    stages: m => `<div class="stages">${m.years.slice(0, 5).map((r, i) => `<div class="stage${i === 0 ? ' now' : ''}"><span class="yr">${E(r.y)}</span><h3>${E(r.stage)}</h3><ul>${r.items.slice(0, 3).map(x => `<li>${E(x)}</li>`).join('')}</ul></div>`).join('')}</div>
      <p class="fine mt-s">연도별 매출·고객 목표는 <a href="evidence.html#growth">실증·로드맵</a>에 있습니다.</p>`
  };
  const mounts = document.querySelectorAll('[data-market]');
  if (!mounts.length) return;
  const get = u => fetch(u, { cache: 'no-cache' }).then(r => r.json());
  Promise.all([get('data/market.json'), document.querySelector('[data-market="pnl"]') ? get('data/pnl.json') : null]).then(([m, p]) => {
    mounts.forEach(el => { const f = R[el.dataset.market]; if (f) el.outerHTML = `<div data-b2b>${f(m, p)}</div>`; });
    if (location.hash) { const t = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t) t.scrollIntoView(); }
  });
})();
