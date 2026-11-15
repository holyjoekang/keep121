(() => {
'use strict';
const KEY = 'keep121_guide_v3', OLD = 'keep121_guide_v2', root = document.getElementById('app');
let C, s, tab = 'home', q = '', group = '', onlyLeft = false, sheet = null, toastT = null, scanStop = null, err = '';
const e = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const now = () => new Date().toISOString();
const hm = t => t ? new Date(t).toLocaleTimeString('ko-KR', {hour: '2-digit', minute: '2-digit'}) : '';
const dt = t => new Date(t).toLocaleString('ko-KR', {month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'});
const dur = ms => { const m = Math.round(ms / 60000); return m < 1 ? '1분 미만' : m < 60 ? m + '분' : Math.floor(m / 60) + '시간 ' + (m % 60) + '분'; };
const buzz = n => { try { navigator.vibrate && navigator.vibrate(n); } catch {} };

const I = {
  home: '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
  roll: '<path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9"/>',
  people: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><circle cx="17" cy="9" r="2.6"/><path d="M16.5 14.6c2.4.2 4.2 1.8 5 4.4"/>',
  log: '<path d="M8 6h12M8 12h12M8 18h12"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/>',
  plane: '<path d="M10.5 21 12 17l5 3v-2l-5-4V8.5a1.5 1.5 0 0 0-3 0V14l-5 4v2l5-3z" transform="rotate(45 12 12)"/>',
  school: '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>',
  bus: '<rect x="4" y="3" width="16" height="14" rx="3"/><path d="M4 11h16M7 21v-4M17 21v-4"/><circle cx="8" cy="14" r=".8"/><circle cx="16" cy="14" r=".8"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
  scan: '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M4 12h16"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  chev: '<path d="M9 6l6 6-6 6"/>',
  phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
  alert: '<path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17v.5"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  pin: '<path d="M12 21s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
  tag: '<path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>'
};
const ic = (n, cls = '') => `<svg class="ic ${cls}" viewBox="0 0 24 24" aria-hidden="true">${I[n] || ''}</svg>`;

document.body.insertAdjacentHTML('beforeend', '<div id="toast" class="toast" role="status"></div><div id="sheet" class="sheet-wrap"></div>');
/* ---------- state ---------- */
const blank = () => ({v: 3, trip: null, people: [], rounds: [], events: [], closed: false, big: false});
function load() {
  try { s = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { err = '저장 데이터를 읽지 못했습니다. 덮어쓰지 않도록 앱을 멈췄습니다.'; return false; }
  if (!s) { s = blank(); migrate(); }
  return true;
}
function migrate() {
  let o; try { o = JSON.parse(localStorage.getItem(OLD) || 'null'); } catch { return; }
  if (!o || !o.trip) return;
  s.trip = {...o.trip, started: o.events?.[0]?.time || now()};
  s.people = o.people.map(p => ({...p, group: '', phone: '', note: '', left: ''}));
  if (o.round) s.rounds = [{id: 'r1', name: o.round.name, started: now(), done: o.round.departed ? now() : '', checks: o.round.checks}];
  s.events = o.events || []; s.closed = !!o.closed;
  log('이관', 'v2 기록을 v3로 가져왔습니다');
}
function save() {
  try { localStorage.setItem(KEY, JSON.stringify(s)); err = ''; }
  catch { err = '저장 실패 — 기록 탭에서 JSON 백업을 내려받으세요.'; }
  render();
}
const log = (type, detail) => s.events.push({time: now(), type, detail, actor: s.trip?.actor || ''});
const M = () => C.modes[s.trip?.mode] || C.modes.travel;
const live = () => s.trip && !s.closed;
const round = () => s.rounds[s.rounds.length - 1];
const open = () => { const r = round(); return r && !r.done ? r : null; };
const inScope = p => !p.left;
const pending = (r = open()) => r ? s.people.filter(p => inScope(p) && !r.checks[p.id]) : [];
const issues = () => s.people.filter(p => p.issue);
const unreturned = () => s.people.filter(p => p.device && !p.returned);
const groups = () => [...new Set(s.people.map(p => p.group).filter(Boolean))];
const find = id => s.people.find(p => p.id === id);

function parseRoster(text) {
  return text.split('\n').map(l => l.trim()).filter(Boolean).map(l => l.split(/\t|,/).map(x => x.trim()))
    .map(([name, group = '', phone = '', ...note], i) => ({id: 'p' + (i + 1), name, group, phone, note: note.join(', '), tag: 'check', device: '', issue: '', issueAt: '', returned: false, left: '', loc: null}))
    .filter(p => p.name).slice(0, 300);
}

/* ---------- actions ---------- */
function check(p, method) {
  const r = open(); if (!live() || !r || !p || r.checks[p.id] || p.left) return false;
  r.checks[p.id] = {time: now(), method}; log('인원 확인', `${p.name} · ${method} · ${r.name}`);
  buzz(12); save(); toast(`${p.name} 확인됨`, () => { if (r.checks[p.id] && !r.done) { delete r.checks[p.id]; log('확인 실행취소', p.name + ' · 즉시 취소'); save(); } });
  if (!pending().length) buzz([20, 60, 20]);
  return true;
}
function toast(msg, undo) {
  clearTimeout(toastT); const t = document.getElementById('toast');
  t.innerHTML = `<span>${e(msg)}</span>${undo ? '<button data-act="undoToast">실행 취소</button>' : ''}`; t.className = 'toast show';
  t._undo = undo; toastT = setTimeout(() => { t.className = 'toast'; t._undo = null; }, 4000);
}
function download(name, text, type) { const u = URL.createObjectURL(new Blob([text], {type})); const a = document.createElement('a'); a.href = u; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(u), 1000); }
const csvCell = v => '"' + String(v ?? '').replace(/^[=+@\-]/, "'$&").replace(/"/g, '""') + '"';

/* ---------- views ---------- */
function nav(title, sub = '', right = '') {
  return `<header class="nav"><div class="nav-top"><a class="nav-brand" href="../index.html">Keep121</a>${right}</div><h1>${e(title)}</h1>${sub ? `<p class="nav-sub">${sub}</p>` : ''}</header>`;
}
const row = (main, detail = '', act = '', id = '', cls = '') => `<button class="row ${cls}" ${act ? `data-act="${act}" data-id="${e(id)}"` : 'disabled'}><span class="row-main">${main}</span>${detail ? `<span class="row-detail">${detail}</span>` : ''}${act ? ic('chev', 'chev') : ''}</button>`;
const sect = (title, body, foot = '') => `<section class="group">${title ? `<h2 class="group-h">${title}</h2>` : ''}<div class="card">${body}</div>${foot ? `<p class="group-f">${foot}</p>` : ''}</section>`;

function ring(done, total, size = 132) {
  const r = size / 2 - 9, c = 2 * Math.PI * r, f = total ? done / total : 0;
  return `<svg class="ring" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" role="img" aria-label="${done}/${total} 확인"><circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="ring-bg"/><circle cx="${size / 2}" cy="${size / 2}" r="${r}" class="ring-fg ${f === 1 ? 'full' : ''}" stroke-dasharray="${c}" stroke-dashoffset="${c * (1 - f)}"/><text x="50%" y="47%" class="ring-n">${done}</text><text x="50%" y="66%" class="ring-t">/ ${total}명</text></svg>`;
}

function vSetup() {
  const modes = Object.entries(C.modes).map(([k, m]) => `<label class="mode"><input type="radio" name="mode" value="${k}" ${k === 'travel' ? 'checked' : ''}><span class="mode-ic">${ic(m.icon)}</span><b>${e(m.label)}</b><small>${e(m.sub)}</small></label>`).join('');
  return nav(s.closed ? '다음 행사' : '새 행사', '명단을 붙여넣고 바로 점호를 시작하세요.') +
  (s.closed ? sect('', `<div class="pad"><p>이전 행사 「${e(s.trip.name)}」는 종료되었습니다. 새로 만들면 기록이 교체됩니다.</p><button class="btn tinted" data-act="backup">이전 기록 JSON 백업</button></div>`) : '') +
  `<form id="setup"><section class="group"><h2 class="group-h">운영 환경</h2><div class="modes">${modes}</div></section>` +
  sect('행사 정보', `<label class="field"><span>행사명</span><input name="name" required maxlength="80" placeholder="경주 5학년 현장학습"></label><label class="field"><span>담당자</span><input name="actor" required maxlength="40" placeholder="이름"></label><label class="field"><span>기본 장비</span><select name="tag">${Object.entries(C.hardware).map(([k, h]) => `<option value="${k}">${e(h.label)} · ${e(h.sub)}</option>`).join('')}</select></label>`) +
  sect('참가자 명단', `<textarea name="roster" rows="7" required placeholder="이름, 조/반/정류장, 연락처, 메모&#10;김민수, 1호차, 010-1234-5678&#10;이영희, 1호차, , 알레르기"></textarea>`, '한 줄에 한 명. 쉼표 또는 탭으로 구분 — 엑셀에서 그대로 붙여넣을 수 있습니다. 조·연락처·메모는 선택.') +
  `${s.closed ? `<label class="confirm"><input type="checkbox" required> 이전 기록을 백업했고 새 행사로 전환합니다.</label>` : ''}<div class="pad-x"><button class="btn primary big">행사 만들기</button><button type="button" class="btn plain" data-act="sample">샘플 명단으로 체험하기</button><button type="button" class="btn plain" data-act="import">JSON 백업 복원</button></div></form>`;
}

function vHome() {
  if (!s.trip || s.closed) return vSetup();
  const m = M(), r = open(), last = round(), total = s.people.filter(inScope).length;
  const day = Math.floor((Date.now() - new Date(s.trip.started).setHours(0, 0, 0, 0)) / 864e5) + 1;
  let hero;
  if (r) { const done = total - pending().length;
    hero = `<div class="hero">${ring(done, total)}<div><small class="eyebrow">진행 중 점호 · ${hm(r.started)} 시작</small><h3>${e(r.name)}</h3><p>${pending().length ? `미확인 ${pending().length}명` : '전원 확인 완료'}${issues().length ? ` · 대응 ${issues().length}건` : ''}</p><button class="btn primary" data-tab="roll">점호 계속</button></div></div>`;
  } else {
    hero = `<div class="hero"><div class="hero-ic">${ic('roll')}</div><div><small class="eyebrow">${last ? `최근: ${e(last.name)} · ${hm(last.done)} 확정` : '첫 점호 전'}</small><h3>다음 집결 점호</h3><p>지난 확인은 새 점호에 자동 적용되지 않습니다.</p><button class="btn primary" data-act="newRound">점호 시작</button></div></div>`;
  }
  const alerts = [
    ...issues().map(p => row(`<span class="dot red"></span><b>${e(p.name)}</b> · 대응 중`, e(p.issue), 'person', p.id)),
    ...(s.people.some(p => !p.device) ? [row(`<span class="dot orange"></span>장비 미배정 ${s.people.filter(p => !p.device).length}명`, '명단에서 배정', 'goPeople')] : []),
  ];
  return nav(s.trip.name, `${ic(m.icon)} ${e(m.label)} · ${day}일차 · 담당 ${e(s.trip.actor)}`) +
    `<section class="group"><div class="card">${hero}</div></section>` +
    (alerts.length ? sect('확인 필요', alerts.join('')) : '') +
    sect('오늘 현황', `<div class="stats"><div><b>${total}</b><span>참가</span></div><div><b>${s.rounds.filter(r => r.done).length}</b><span>완료 점호</span></div><div><b>${s.people.filter(p => p.left).length}</b><span>불참·귀가</span></div><div><b>${unreturned().length}</b><span>미회수</span></div></div>`) +
    sect('빠른 시작', m.rounds.map(n => row(e(n), '', 'quickRound', n)).join(''), r ? '진행 중인 점호를 확정한 뒤 새 점호를 시작할 수 있습니다.' : '자주 쓰는 집결 단계를 눌러 바로 시작합니다.') +
    sect('', row('행사 종료 · 인계 및 회수', '', 'finish'), '최종 점호 확정, 대응 종료, 장비 회수 후 종료할 수 있습니다.') +
    `<p class="foot">${err ? `<b class="red-t">${e(err)}</b><br>` : ''}이 기기에만 저장 · ${navigator.onLine ? '온라인' : '오프라인'} · BLE·GPS 자동 수신과 보호자 알림은 아직 연결되지 않았습니다. 장치 신호를 인원 확인으로 간주하지 않습니다.</p>`;
}

function filtered() {
  const r = open() || round(), k = q.trim().toLowerCase();
  return s.people.filter(p => (!group || p.group === group) && (!k || (p.name + p.group + p.device).toLowerCase().includes(k)) && (!onlyLeft || (r && !r.checks[p.id] && inScope(p))));
}
function seg() {
  const g = groups(); if (!g.length) return '';
  return `<div class="seg" role="tablist">${['', ...g].map(x => `<button data-act="group" data-id="${e(x)}" aria-pressed="${group === x}">${x ? e(x) : '전체'}</button>`).join('')}</div>`;
}
function vRoll() {
  if (!s.trip || s.closed) return vSetup();
  const r = open(), m = M();
  if (!r) return nav('점호', '집결 단계를 골라 시작하세요.') +
    sect('빠른 시작', m.rounds.map(n => row(e(n), '', 'quickRound', n)).join('') + row(`${ic('plus')} 직접 입력`, '', 'newRound')) +
    (s.rounds.length ? sect('지난 점호', s.rounds.slice().reverse().map(x => row(e(x.name), `${Object.keys(x.checks).length}명 · ${hm(x.started)}–${hm(x.done)}`)).join('')) : '');
  const total = s.people.filter(inScope).length, left = pending().length, list = filtered();
  const tiles = list.sort((a, b) => (!!r.checks[a.id] - !!r.checks[b.id]) || (!!b.issue - !!a.issue)).map(p => {
    const c = r.checks[p.id], st = p.left ? 'out' : c ? 'ok' : p.issue ? 'warn' : '';
    return `<div class="tile ${st}"><button class="tile-hit" data-act="${p.left ? 'person' : c ? 'person' : 'tap'}" data-id="${p.id}" aria-label="${e(p.name)} ${c ? '확인됨' : '확인하기'}"><span class="tile-mark">${c ? ic('check') : p.issue ? '!' : ''}</span><b>${e(p.name)}</b><small>${p.left ? e(p.left) : c ? hm(c.time) + ' · ' + e(c.method) : p.group ? e(p.group) : '미확인'}</small></button><button class="tile-info" data-act="person" data-id="${p.id}" aria-label="${e(p.name)} 상세">⋯</button></div>`;
  }).join('');
  const blocked = left || issues().length;
  return nav(r.name, `${hm(r.started)} 시작 · ${dur(Date.now() - new Date(r.started))} 경과`, `<button class="nav-btn" data-act="scan">${ic('scan')}스캔</button>`) +
    `<div class="sticky"><div class="progress"><div class="bar"><i style="width:${total ? (total - left) / total * 100 : 0}%"></i></div><span><b>${total - left}</b>/${total} · 남은 ${left}명</span></div>
     <div class="tools"><label class="search">${ic('search')}<input id="q" type="search" placeholder="이름·조·태그 검색" value="${e(q)}"></label><button class="chip" data-act="onlyLeft" aria-pressed="${onlyLeft}">남은 사람</button></div>${seg()}</div>
     <div class="grid ${s.big ? 'bigtxt' : ''}">${tiles || '<p class="empty">조건에 맞는 사람이 없습니다.</p>'}</div>
     <div class="dock"><button class="btn ${blocked ? 'gray' : 'primary'} big" data-act="depart">${blocked ? `${left ? `미확인 ${left}명` : ''}${left && issues().length ? ' · ' : ''}${issues().length ? `대응 ${issues().length}건` : ''} — 보류` : e(m.complete)}</button></div>`;
}

function vPeople() {
  if (!s.trip) return vSetup();
  const list = filtered(), r = open() || round();
  const rows = list.map(p => {
    const c = r?.checks[p.id];
    const badge = p.left ? '<span class="pill gray">불참·귀가</span>' : p.issue ? '<span class="pill red">대응 중</span>' : c && open() ? '<span class="pill green">확인</span>' : '';
    return row(`<span class="av">${e(p.name.slice(0, 1))}</span><span class="who"><b>${e(p.name)}</b> ${badge}<small>${[p.group, C.hardware[p.tag]?.label, p.device || '태그 미배정', p.device ? (p.returned ? '회수됨' : '') : ''].filter(Boolean).map(e).join(' · ')}</small></span>`, '', 'person', p.id);
  }).join('');
  return nav('명단', `${s.people.length}명 · 장비 배정 ${s.people.filter(p => p.device).length} · 회수 ${s.people.filter(p => p.returned).length}`) +
    `<div class="sticky"><div class="tools"><label class="search">${ic('search')}<input id="q" type="search" placeholder="이름·조·태그 검색" value="${e(q)}"></label></div>${seg()}</div>` +
    sect('', rows || '<p class="empty">없음</p>') +
    (live() ? sect('', row(`${ic('plus')} 참가자 추가`, '', 'addPerson') + row(`${ic('tag')} 장비 일괄 회수 확인`, `${unreturned().length}개 남음`, 'returnAll')) : '');
}

function vLog() {
  if (!s.trip) return vSetup();
  const rs = s.rounds.map(r => row(`<b>${e(r.name)}</b><small class="blk">${dt(r.started)} 시작</small>`, r.done ? `${Object.keys(r.checks).length}명 · ${dur(new Date(r.done) - new Date(r.started))}` : '진행 중')).join('');
  const ev = s.events.slice().reverse().slice(0, 200).map(x => `<li><time>${dt(x.time)}</time><b>${e(x.type)}</b><p>${e(x.detail)}${x.actor ? ' · ' + e(x.actor) : ''}</p></li>`).join('');
  return nav('기록', `감사 로그 ${s.events.length}건`) +
    sect('점호 소요시간', rs || '<p class="empty">아직 점호가 없습니다.</p>', '점호 시작부터 확정까지의 시간 — 현장 실증 지표로 사용합니다.') +
    sect('내보내기', row('JSON 백업', '', 'backup') + row('CSV 감사 로그', '', 'csv') + row('JSON 백업 복원', '', 'import')) +
    sect('설정', `<label class="row switch"><span class="row-main">점호 큰 글씨</span><input type="checkbox" data-act="big" ${s.big ? 'checked' : ''}></label>`) +
    sect('타임라인', `<ol class="timeline">${ev}</ol>`);
}

/* ---------- sheets ---------- */
function openSheet(kind, id) { const t = document.getElementById('toast'); t.className = 'toast'; t._undo = null; sheet = {kind, id}; renderSheet(); }
function closeSheet() { if (scanStop) { scanStop(); scanStop = null; } sheet = null; renderSheet(); }
const chips = (list, name) => `<div class="chips">${list.map(x => `<button type="button" class="chip" data-fill="${name}" data-v="${e(x)}">${e(x)}</button>`).join('')}</div>`;
function renderSheet() {
  const el = document.getElementById('sheet');
  if (!sheet) { el.className = 'sheet-wrap'; el.innerHTML = ''; return; }
  const p = find(sheet.id), r = open(), m = live() ? M() : null; let h = '';
  if (sheet.kind === 'person' && p) {
    const c = r?.checks[p.id];
    h = `<h3>${e(p.name)}</h3><p class="sub">${[p.group, p.note].filter(Boolean).map(e).join(' · ') || '추가 정보 없음'}</p>
    ${p.phone ? `<a class="btn tinted" href="tel:${e(p.phone.replace(/[^0-9+]/g, ''))}">${ic('phone')} ${e(p.phone)} 전화</a>` : ''}
    ${live() && r && !p.left ? (c ? `<form data-form="undo"><div class="card"><div class="pad"><b class="green-t">✓ ${hm(c.time)} · ${e(c.method)}</b></div></div><label class="field-s">확인 취소 사유<input name="v" required placeholder="오인 확인 등"></label><button class="btn destructive">확인 취소</button></form>` : `<button class="btn primary big" data-act="tap" data-id="${p.id}">${ic('check')} 직접 확인</button>`) : ''}
    ${live() ? (p.issue ? `<form data-form="resolve"><div class="card warnbox"><div class="pad"><b>대응 중</b> · ${hm(p.issueAt)}<br>${e(p.issue)}</div></div>${chips(C.resolveReasons, 'v')}<label class="field-s">종료 근거<input name="v" required></label><button class="btn primary">대응 종료</button></form>`
      : `<form data-form="issue"><h4>미확인 대응 시작</h4>${chips(C.issueReasons, 'v')}<label class="field-s">담당·조치 내용<input name="v" required placeholder="누가 무엇을 하는지"></label><button class="btn tinted-red">대응 기록</button></form>`) : ''}
    ${live() ? `<details><summary>장비 · 위치 · 상태</summary>
      <form data-form="device"><label class="field-s">장비<select name="tag">${Object.entries(C.hardware).map(([k, x]) => `<option value="${k}" ${k === p.tag ? 'selected' : ''}>${e(x.label)} · ${e(x.sub)}</option>`).join('')}</select></label><label class="field-s">태그 ID<input name="device" value="${e(p.device)}" placeholder="인쇄된 ID 또는 NFC 일련번호"></label><button class="btn tinted">장비 저장</button>${p.device && !p.returned ? `<button type="button" class="btn plain" data-act="return" data-id="${p.id}">회수 확인</button>` : p.returned ? '<p class="sub">회수됨</p>' : ''}</form>
      <form data-form="loc"><label class="field-s">${ic('pin')} 참고 위치 (공식 앱에서 수동 확인)<input name="note" value="${e(p.loc?.note || '')}" placeholder="예: 정문 주차장 부근"></label><label class="field-s">원본 갱신 시각<input name="at" value="${e(p.loc?.at || '')}" placeholder="모르면 비워두기"></label><button class="btn tinted">위치 기록</button><p class="sub">위치는 탑승·점호 완료를 의미하지 않습니다.</p></form>
      ${p.left ? `<button class="btn tinted" data-act="rejoin" data-id="${p.id}">다시 참가로 전환</button>` : `<form data-form="leave">${chips(C.leaveReasons, 'v')}<label class="field-s">불참·귀가 사유<input name="v" required></label><button class="btn plain-red">점호 대상에서 제외</button></form>`}
      <label class="field-s">연락처<input data-edit="phone" value="${e(p.phone)}"></label><label class="field-s">메모<input data-edit="note" value="${e(p.note)}"></label>
    </details>` : ''}`;
  }
  if (sheet.kind === 'round') h = `<h3>새 점호</h3><form data-form="round">${chips(M().rounds, 'v')}<label class="field-s">집결지 / 확인 단계<input name="v" required placeholder="박물관 출발 · 버스 탑승"></label><button class="btn primary big">시작</button></form>`;
  if (sheet.kind === 'add') h = `<h3>참가자 추가</h3><form data-form="add"><label class="field-s">이름<input name="name" required></label><label class="field-s">${e(M().groupLabel)}<input name="group" list="gl"><datalist id="gl">${groups().map(g => `<option value="${e(g)}">`).join('')}</datalist></label><label class="field-s">연락처<input name="phone" type="tel"></label><button class="btn primary">추가</button></form>`;
  if (sheet.kind === 'depart' && r) {
    const left = pending(), is = issues();
    h = `<h3>${e(m.complete)} · ${e(r.name)}</h3>` + (left.length || is.length
      ? `<p class="sub">아래 항목이 해결되어야 확정할 수 있습니다.</p><div class="card">${left.map(p => row(`<span class="dot orange"></span>${e(p.name)} 미확인`, e(p.group), 'person', p.id)).join('')}${is.map(p => row(`<span class="dot red"></span>${e(p.name)} 대응 중`, e(p.issue), 'person', p.id)).join('')}</div>`
      : `<form data-form="depart"><div class="hero mini">${ring(s.people.filter(inScope).length, s.people.filter(inScope).length, 96)}<p>전원 직접 확인 · 소요 ${dur(Date.now() - new Date(r.started))}</p></div><label class="confirm"><input type="checkbox" required> 차량·현장 인원을 눈으로 최종 확인했습니다.</label>${s.trip.mode === 'shuttle' ? `<label class="confirm"><input type="checkbox" required> ${e(m.finishChecks[0])}</label>` : ''}<button class="btn primary big">${e(m.complete)}</button></form>`);
  }
  if (sheet.kind === 'finish') {
    const blocks = [...(open() ? [`진행 중 점호 「${e(open().name)}」 미확정`] : []), ...(!s.rounds.some(r => r.done) ? ['확정된 점호 없음'] : []), ...issues().map(p => `${e(p.name)} 대응 미종료`), ...unreturned().map(p => `${e(p.name)} 장비(${e(p.device)}) 미회수`)];
    h = `<h3>행사 종료</h3>` + (blocks.length ? `<p class="sub">종료 전 확인할 항목</p><div class="card">${blocks.map(b => row(`<span class="dot orange"></span>${b}`)).join('')}</div>${unreturned().length ? '<button class="btn tinted" data-act="returnAll">장비 일괄 회수 확인</button>' : ''}`
      : `<form data-form="finish">${M().finishChecks.map(c => `<label class="confirm"><input type="checkbox" required> ${e(c)}</label>`).join('')}<button class="btn primary big">인솔 종료</button></form>`);
  }
  if (sheet.kind === 'scan') {
    h = `<h3>태그 스캔</h3><p class="sub">${e(open()?.name || '')} · 남은 ${pending().length}명</p><div class="scanbox"><video id="cam" playsinline muted></video><p id="scanmsg">QR 카메라 또는 NFC를 사용하세요.</p></div><div class="row2"><button class="btn tinted" data-act="cam">${ic('scan')} QR 카메라</button><button class="btn tinted" data-act="nfc">NFC 탭</button></div><form data-form="scanid"><label class="field-s">태그 ID 직접 입력<input name="v" required autocomplete="off"></label><button class="btn primary">확인</button></form>`;
  }
  if (sheet.kind === 'import') h = `<h3>JSON 백업 복원</h3><p class="sub">현재 기기의 기록이 백업 내용으로 교체됩니다.</p><input type="file" id="file" accept="application/json,.json"><button class="btn destructive" data-act="doImport">복원</button>`;
  el.className = 'sheet-wrap show';
  el.innerHTML = `<div class="scrim" data-act="close"></div><div class="sheet" role="dialog" aria-modal="true"><div class="grabber"></div><button class="sheet-x" data-act="close" aria-label="닫기">완료</button>${h}</div>`;
}
const scanMsg = t => { const x = document.getElementById('scanmsg'); if (x) x.textContent = t; };
function byTag(v) { const p = s.people.find(p => p.device && p.device === String(v).trim()); if (!p) { scanMsg('등록되지 않은 태그: ' + v); buzz([60, 40, 60]); return; } if (open()?.checks[p.id]) { scanMsg(p.name + ' — 이미 확인됨 (중복 무시)'); return; } check(p, '태그 스캔'); scanMsg(p.name + ' 확인 · 남은 ' + pending().length + '명'); }
async function startCam() {
  if (!('BarcodeDetector' in window) || !navigator.mediaDevices) return scanMsg('이 브라우저는 QR 카메라 인식을 지원하지 않습니다. ID를 직접 입력하세요.');
  try {
    const v = document.getElementById('cam'), st = await navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}}), det = new BarcodeDetector({formats: ['qr_code']});
    v.srcObject = st; await v.play(); v.classList.add('on'); let on = true, lastV = '', lastT = 0;
    scanStop = () => { on = false; st.getTracks().forEach(t => t.stop()); };
    (async function loop() { if (!on) return; try { const [c] = await det.detect(v); if (c && (c.rawValue !== lastV || Date.now() - lastT > 3000)) { lastV = c.rawValue; lastT = Date.now(); byTag(c.rawValue); } } catch {} setTimeout(loop, 250); })();
  } catch { scanMsg('카메라 권한을 확인하세요.'); }
}
async function startNfc() {
  if (!('NDEFReader' in window)) return scanMsg('이 브라우저는 Web NFC를 지원하지 않습니다 (Android Chrome에서 지원).');
  try { const rd = new NDEFReader(), ac = new AbortController(); await rd.scan({signal: ac.signal}); scanMsg('NFC 명찰을 휴대폰 뒷면에 대세요.'); rd.onreading = x => byTag(x.serialNumber); const prev = scanStop; scanStop = () => { ac.abort(); prev && prev(); }; } catch { scanMsg('NFC 권한·설정을 확인하세요.'); }
}

/* ---------- render ---------- */
function render() {
  const y = window.scrollY, f = document.activeElement?.id, ss = document.activeElement?.selectionStart;
  if (err && !s) { root.innerHTML = `<p class="fatal">${e(err)}</p>`; return; }
  const v = {home: vHome, roll: vRoll, people: vPeople, log: vLog}[tab]();
  const badge = {roll: open() ? pending().length : 0, people: issues().length};
  root.innerHTML = `<main class="view v-${tab}">${v}</main>${s.trip && !s.closed ? `<nav class="tabbar">${[['home', '오늘'], ['roll', '점호'], ['people', '명단'], ['log', '기록']].map(([k, n]) => `<button data-tab="${k}" aria-current="${tab === k}">${ic(k === 'people' ? 'people' : k)}${badge[k] ? `<i class="tb-badge">${badge[k]}</i>` : ''}<span>${n}</span></button>`).join('')}</nav>` : ''}`;
  document.body.classList.toggle('big', !!s.big);
  window.scrollTo(0, y); if (f === 'q') { const i = document.getElementById('q'); i.focus(); try { i.setSelectionRange(ss, ss); } catch {} }
  if (!sheet || sheet.kind !== 'scan') renderSheet();
}

/* ---------- events ---------- */
document.addEventListener('input', ev => {
  if (ev.target.id === 'q') { q = ev.target.value; render(); }
  const k = ev.target.dataset.edit; if (k && sheet) { const p = find(sheet.id); p[k] = ev.target.value.trim(); try { localStorage.setItem(KEY, JSON.stringify(s)); } catch {} }
});
document.addEventListener('change', ev => { if (ev.target.dataset.act === 'big') { s.big = ev.target.checked; save(); } const k = ev.target.dataset.edit; if (k && sheet) { log('정보 수정', find(sheet.id).name + ' · ' + k); save(); } });
document.addEventListener('click', ev => {
  const fill = ev.target.closest('[data-fill]'); if (fill) { const i = fill.closest('form').elements[fill.dataset.fill]; i.value = fill.dataset.v; i.focus(); return; }
  const b = ev.target.closest('[data-tab],[data-act]'); if (!b || b.tagName === 'INPUT') return;
  if (b.dataset.tab) { tab = b.dataset.tab; q = ''; onlyLeft = false; window.scrollTo(0, 0); render(); return; }
  const a = b.dataset.act, id = b.dataset.id, p = find(id);
  const A = {
    close: closeSheet,
    undoToast: () => { const t = document.getElementById('toast'); t._undo && t._undo(); t.className = 'toast'; },
    tap: () => { if (!open()) return openSheet('round'); check(p, '직접 확인'); if (sheet) closeSheet(); },
    person: () => openSheet('person', id),
    group: () => { group = id; render(); },
    onlyLeft: () => { onlyLeft = !onlyLeft; render(); },
    newRound: () => open() ? (tab = 'roll', render()) : openSheet('round'),
    quickRound: () => { if (open()) { tab = 'roll'; render(); return toast('진행 중인 점호를 먼저 확정하세요'); } startRound(id); },
    depart: () => openSheet('depart'), finish: () => openSheet('finish'), scan: () => openSheet('scan'),
    addPerson: () => openSheet('add'), goPeople: () => { tab = 'people'; render(); },
    cam: startCam, nfc: startNfc, import: () => openSheet('import'),
    return: () => { p.returned = true; log('장비 회수', p.name + ' · ' + p.device); save(); },
    returnAll: () => { const l = unreturned(); if (!l.length) return; if (!confirm(`장비 ${l.length}개를 실물로 회수했습니까?`)) return; l.forEach(p => { p.returned = true; log('장비 회수', p.name + ' · ' + p.device); }); save(); },
    rejoin: () => { p.left = ''; log('참가 복귀', p.name); save(); },
    backup: () => download(`keep121-${(s.trip?.name || 'backup').replace(/\s+/g, '_')}.json`, JSON.stringify(s, null, 2), 'application/json'),
    csv: () => download('keep121-events.csv', '﻿' + [['시각', '행동', '내용', '담당자'], ...s.events.map(x => [x.time, x.type, x.detail, x.actor])].map(r => r.map(csvCell).join(',')).join('\r\n'), 'text/csv;charset=utf-8'),
    sample: () => { const f = document.getElementById('setup'), k = f.elements.mode.value, x = C.samples[k]; f.elements.name.value = x.name; f.elements.actor.value = x.actor; f.elements.roster.value = x.roster; },
    doImport: () => { const fl = document.getElementById('file').files[0]; if (!fl) return; fl.text().then(t => { const d = JSON.parse(t); if (d.v !== 3 || !Array.isArray(d.people)) throw 0; s = d; sheet = null; save(); toast('복원 완료'); }).catch(() => toast('올바른 v3 백업 파일이 아닙니다')); }
  };
  if (A[a]) { if (!live() && !['close', 'backup', 'csv', 'sample', 'import', 'doImport', 'person'].includes(a)) return; A[a](); }
});
function startRound(name) { s.rounds.push({id: 'r' + (s.rounds.length + 1), name, started: now(), done: '', checks: {}}); log('점호 시작', name); tab = 'roll'; group = ''; onlyLeft = false; q = ''; sheet = null; save(); }
document.addEventListener('submit', ev => {
  ev.preventDefault(); const f = ev.target, d = new FormData(f), t = n => String(d.get(n) || '').trim(), p = sheet && find(sheet.id), k = f.dataset.form;
  if (f.id === 'setup') {
    const people = parseRoster(t('roster')); if (!people.length) return toast('명단을 입력하세요');
    people.forEach(x => x.tag = t('tag'));
    s = {...blank(), big: s.big, trip: {name: t('name'), actor: t('actor'), mode: t('mode'), started: now()}, people};
    log('행사 시작', `${s.trip.name} · ${people.length}명`); tab = 'home'; return save();
  }
  if (!live()) return;
  if (k === 'round') return open() ? null : startRound(t('v'));
  if (k === 'scanid') { byTag(t('v')); f.reset(); return; }
  if (k === 'undo') { delete open().checks[p.id]; log('확인 취소', `${p.name} · ${t('v')}`); }
  if (k === 'issue') { p.issue = t('v'); p.issueAt = now(); log('대응 시작', `${p.name} · ${p.issue}`); }
  if (k === 'resolve') { log('대응 종료', `${p.name} · ${t('v')}`); p.issue = ''; p.issueAt = ''; }
  if (k === 'leave') { p.left = t('v'); p.issue = ''; log('점호 제외', `${p.name} · ${p.left}`); }
  if (k === 'device') { const dv = t('device'); if (dv && s.people.some(x => x !== p && x.device === dv)) return toast('이미 다른 사람에게 연결된 태그입니다'); p.tag = t('tag'); p.device = dv; p.returned = false; log('장비 연결', `${p.name} · ${C.hardware[p.tag].label} · ${dv || '해제'}`); toast('장비 저장됨'); }
  if (k === 'loc') { if (!t('note')) return; p.loc = {note: t('note'), at: t('at') || '미제공', recorded: now()}; log('참고 위치 수동 기록', `${p.name} · ${p.loc.note} · 원본 갱신 ${p.loc.at}`); toast('참고 위치 기록됨'); }
  if (k === 'add') { const n = {id: 'p' + Date.now(), name: t('name'), group: t('group'), phone: t('phone'), note: '', tag: 'check', device: '', issue: '', issueAt: '', returned: false, left: '', loc: null}; s.people.push(n); log('참가자 추가', n.name); sheet = null; }
  if (k === 'depart') { const r = open(); if (pending().length || issues().length) return; r.done = now(); log(M().complete, `${r.name} · ${Object.keys(r.checks).length}명 · ${dur(new Date(r.done) - new Date(r.started))}`); sheet = null; tab = 'home'; buzz([30, 50, 30]); toast(`${r.name} 확정 완료`); }
  if (k === 'finish') { if (open() || issues().length || unreturned().length) return; s.closed = true; log('인솔 종료', s.trip.name); sheet = null; tab = 'home'; }
  if (['undo', 'issue', 'resolve', 'leave'].includes(k)) sheet = null;
  save();
});
addEventListener('keydown', ev => { if (ev.key === 'Escape' && sheet) closeSheet(); });
addEventListener('online', render); addEventListener('offline', render);
setInterval(() => { if (tab === 'roll' && open() && !sheet && document.activeElement?.id !== 'q') render(); }, 30000);

fetch('v3-config.json').then(r => r.json()).then(c => { C = c; if (load()) render(); else root.innerHTML = `<p class="fatal">${e(err)}</p>`; })
  .catch(() => { root.innerHTML = '<p class="fatal">설정을 불러오지 못했습니다. 네트워크를 확인하세요.</p>'; });
if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
})();
