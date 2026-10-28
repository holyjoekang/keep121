/* Keep121 Guide v0 — 점호 · 출발 3분 미승차 경보 · 원탭 라벨 · 종료 리포트
 * 서버 연동 전 로컬 데모 모드: 상태와 이벤트 로그는 이 기기에만 저장된다.
 * Keep Tag 위치는 시뮬레이션, Keep Check는 Web NFC(Android Chrome)로 실제 탭을 읽는다.
 */
(() => {
  'use strict';

  const KEY = 'keep121_guide_v0';
  const $app = document.getElementById('app');
  const NFC_OK = 'NDEFReader' in window;
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const now = () => Date.now();
  const hm = ts => { const d = new Date(ts); return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`; };
  const mmss = sec => { sec = Math.max(0, Math.round(sec)); return `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, '0')}`; };
  const uid = () => Math.random().toString(36).slice(2, 10);

  // ---------- icons (lucide 계열 선 아이콘) ----------
  const P = {
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    check: '<path d="M5 12l5 5L20 7"/>',
    usercheck: '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6"/><path d="M16 11l2 2 4-4"/>',
    users: '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6"/><path d="M16 3.5a4 4 0 0 1 0 8M22 21c0-3-1.8-5-4.5-5.7"/>',
    file: '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    nfc: '<rect x="3" y="6" width="11" height="15" rx="2.2"/><path d="M6.5 10.5h4M6.5 14h4"/><path d="M17 9.5a4.5 4.5 0 0 1 0 6M19.6 7a8 8 0 0 1 0 11"/>',
    bus: '<rect x="4" y="3" width="16" height="15" rx="3"/><path d="M4 11h16M8 18v3M16 18v3"/><circle cx="8" cy="14.5" r="1"/><circle cx="16" cy="14.5" r="1"/>',
    pin: '<path d="M12 21s7-6.3 7-12a7 7 0 0 0-14 0c0 5.7 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    alert: '<path d="M12 3l10 18H2z"/><path d="M12 10v4M12 17.5v.5"/>',
    x: '<path d="M6 6l12 12M18 6L6 18"/>',
    upload: '<path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    download: '<path d="M12 4v12M7 11l5 5 5-5"/><path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    send: '<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/>',
    edit: '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
    refresh: '<path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/>',
    flag: '<path d="M5 21V4h11l-1.5 4L16 12H5"/>',
    hand: '<path d="M8 12V5.5a1.5 1.5 0 0 1 3 0V11M11 10V4a1.5 1.5 0 0 1 3 0v6M14 10V5.5a1.5 1.5 0 0 1 3 0V14c0 4-2.5 7-6 7-2.6 0-4-1.3-5.5-3.6L3.8 14.6a1.5 1.5 0 0 1 2.4-1.8L8 15"/>'
  };
  const I = (n, s = 20) => `<svg class="icon" viewBox="0 0 24 24" width="${s}" height="${s}" style="width:${s}px;height:${s}px" aria-hidden="true">${P[n]}</svg>`;

  // ---------- demo data ----------
  const NAMES = ['김○자', '이○순', '박○호', '최○희', '정○수', '강○옥', '조○래', '윤○숙', '김○자', '장○식', '임○분', '한○철', '오○례', '박○순', '서○덕', '신○남', '권○영', '황○길', '안○님', '송○현', '전○례', '홍○기', '유○화', '고○석', '문○자', '양○춘'];
  const DAYS = [
    { day: 1, label: 'DAY 1', city: '다낭', stops: [
      { id: 's11', time: '13:40', name: '다낭 공항 도착', local: 'Sân bay Đà Nẵng', place: '입국장 3번 출구 앞' },
      { id: 's12', time: '16:00', name: '미케 비치', local: 'Bãi biển Mỹ Khê', place: '해변 입구 버스 하차 지점' },
      { id: 's13', time: '19:00', name: '호텔 체크인', local: 'Khách sạn', place: '호텔 로비' } ] },
    { day: 2, label: 'DAY 2', city: '호이안', stops: [
      { id: 's21', time: '08:30', name: '호텔 출발', local: 'Khách sạn', place: '호텔 로비' },
      { id: 's22', time: '11:30', name: '마블 마운틴', local: 'Ngũ Hành Sơn', place: '매표소 앞' },
      { id: 's23', time: '14:30', name: '호이안 구시가지', local: 'Phố cổ Hội An', place: '내원교(일본교) 앞' },
      { id: 's24', time: '18:42', name: '호텔 도착', local: 'Khách sạn', place: '호텔 로비' } ] },
    { day: 3, label: 'DAY 3', city: '바나힐', stops: [
      { id: 's31', time: '08:00', name: '호텔 출발', local: 'Khách sạn', place: '호텔 로비' },
      { id: 's32', time: '12:30', name: '바나힐 골든브릿지', local: 'Cầu Vàng, Bà Nà Hills', place: '케이블카 하차장' },
      { id: 's33', time: '18:30', name: '호텔 도착', local: 'Khách sạn', place: '호텔 로비' } ] }
  ];
  const BASE = { lat: 15.8771, lng: 108.3266 }; // 호이안 구시가지 부근 (데모 좌표)

  function demoState() {
    return {
      v: 1,
      tour: { name: '다낭 5일', agency: '○○여행사', guide: '가이드', day: 2, stopId: 's23' },
      days: DAYS,
      travelers: NAMES.map((n, i) => ({
        id: 't' + (i + 1), no: i + 1, name: n, phone: '', family: '',
        tagType: i % 3 === 2 ? 'check' : 'tag', nfc: '', consent: i !== 20
      })),
      rc: null,      // { id, stopId, startedAt, endedAt, checks: {tid:{m,ts}}, dist: {tid:m}, departAt, deadline, alerted }
      alerts: [],    // { id, tid, rcId, raisedAt, label, labeledAt, resolvedAt }
      events: [],
      settings: { fast: true, radius: 40 }
    };
  }

  // ---------- state ----------
  let S;
  try { S = JSON.parse(localStorage.getItem(KEY)) || demoState(); } catch { S = demoState(); }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch {} };
  let tab = 'rollcall';
  let modal = null; // {type, ...}
  let toastMsg = '', toastTimer = 0;

  // 이벤트 로그 (스키마는 설계 문서 v0의 event 테이블)
  function log(type, extra = {}) {
    S.events.push({ id: uid(), tour: S.tour.name, ts: now(), device_ts: now(), actor: extra.actor || 'guide', type, stop_id: S.tour.stopId, ...extra });
    save();
  }

  const day = () => S.days.find(d => d.day === S.tour.day) || S.days[0];
  const stop = () => day().stops.find(s => s.id === S.tour.stopId) || day().stops[0];
  const tById = id => S.travelers.find(t => t.id === id);
  const checked = () => S.rc ? Object.keys(S.rc.checks).length : 0;
  const total = () => S.travelers.length;
  const unchecked = () => S.rc ? S.travelers.filter(t => !S.rc.checks[t.id]) : S.travelers;
  const isCand = t => S.rc && !S.rc.checks[t.id] && t.tagType === 'tag' && (S.rc.dist[t.id] ?? 999) <= S.settings.radius;
  const openAlerts = () => S.alerts.filter(a => !a.resolvedAt);
  const lastSeen = tid => { const e = [...S.events].reverse().find(e => e.traveler_id === tid && /checkin|confirmed/.test(e.type)); return e ? hm(e.ts) : '—'; };

  function toast(m) { toastMsg = m; clearTimeout(toastTimer); toastTimer = setTimeout(() => { toastMsg = ''; render(); }, 2200); render(); }

  // ---------- Keep Tag 시뮬레이션 ----------
  // 실제 연동 시 위치정보사업자 API 어댑터가 이 함수를 대신한다.
  function simDistances() {
    const d = {};
    S.travelers.forEach(t => { if (t.tagType === 'tag') d[t.id] = Math.round(Math.random() < .8 ? 5 + Math.random() * 35 : 60 + Math.random() * 180); });
    return d;
  }
  function driftDistances() {
    if (!S.rc) return;
    S.travelers.forEach(t => {
      if (t.tagType !== 'tag' || S.rc.checks[t.id]) return;
      const cur = S.rc.dist[t.id] ?? 100;
      S.rc.dist[t.id] = Math.max(3, Math.round(cur + (Math.random() - .62) * 25));
    });
  }

  // ---------- 점호 ----------
  let wakeLock = null, nfcAbort = null;
  async function keepAwake(on) {
    try {
      if (on && 'wakeLock' in navigator) wakeLock = await navigator.wakeLock.request('screen');
      if (!on && wakeLock) { await wakeLock.release(); wakeLock = null; }
    } catch {}
  }

  function startRollcall() {
    if (S.rc && !S.rc.endedAt) return;
    S.rc = { id: uid(), stopId: S.tour.stopId, startedAt: now(), endedAt: null, checks: {}, dist: simDistances(), departAt: null, deadline: null, alerted: false };
    log('rollcall_start', { rollcall_id: S.rc.id });
    keepAwake(true);
    if (NFC_OK) startNfc();
    tab = 'rollcall';
    render();
  }

  function endRollcall() {
    if (!S.rc || S.rc.endedAt) return;
    S.rc.endedAt = now();
    const sec = Math.round((S.rc.endedAt - S.rc.startedAt) / 1000);
    log('rollcall_end', { rollcall_id: S.rc.id, duration_sec: sec, checked: checked(), total: total() });
    keepAwake(false); stopNfc();
    toast(`점호 종료 · ${checked()}/${total()} · ${mmss(sec)}`);
  }

  function checkIn(tid, method) {
    if (!S.rc || S.rc.checks[tid]) return;
    S.rc.checks[tid] = { m: method, ts: now() };
    const type = method === 'nfc' ? 'checkin' : method === 'tag_candidate' ? 'candidate_confirmed' : 'manual_confirmed';
    log(type, { rollcall_id: S.rc.id, traveler_id: tid, method, distance_m: S.rc.dist[tid] ?? null });
    if (navigator.vibrate) navigator.vibrate(40);
    // 모두 확인되면 자동 종료
    if (checked() === total() && !S.rc.departAt) endRollcall();
    render();
  }

  function demoTap() {
    const pool = unchecked();
    if (!pool.length) return;
    const t = pool[Math.floor(Math.random() * pool.length)];
    checkIn(t.id, 'nfc');
    toast(`${t.no} ${t.name} 님 · 명찰 탭`);
  }

  // ---------- Web NFC ----------
  let bindTarget = null; // 명찰 등록 대상 traveler id
  async function startNfc() {
    if (!NFC_OK) return;
    try {
      stopNfc();
      nfcAbort = new AbortController();
      const r = new NDEFReader();
      await r.scan({ signal: nfcAbort.signal });
      r.onreading = ev => onNfc(ev.serialNumber || '');
      r.onreadingerror = () => toast('명찰을 다시 대 주세요');
    } catch (e) {
      toast('NFC 권한이 필요합니다 (설정 → NFC 켜기)');
    }
  }
  function stopNfc() { if (nfcAbort) { nfcAbort.abort(); nfcAbort = null; } }
  function onNfc(serial) {
    if (!serial) return;
    if (bindTarget) {
      const t = tById(bindTarget);
      S.travelers.forEach(x => { if (x.nfc === serial) x.nfc = ''; });
      t.nfc = serial; bindTarget = null; save();
      if (!S.rc || S.rc.endedAt) stopNfc();
      modal = null; toast(`${t.no} ${t.name} 님 명찰 등록됨`);
      return;
    }
    const t = S.travelers.find(x => x.nfc === serial);
    if (!t) { toast('등록되지 않은 명찰입니다 · 명단에서 등록'); return; }
    if (S.rc && !S.rc.endedAt) { checkIn(t.id, 'nfc'); toast(`${t.no} ${t.name} 님 확인`); }
  }
  async function bindTag(tid) {
    if (!NFC_OK) { toast('이 기기는 Web NFC를 지원하지 않습니다 (Android Chrome 필요)'); return; }
    bindTarget = tid;
    modal = { type: 'bind', tid };
    render();
    await startNfc();
  }

  // ---------- 출발 · 3분 경보 ----------
  const WAIT = () => (S.settings.fast ? 15 : 180) * 1000;
  function depart() {
    if (!S.rc) return;
    if (!S.rc.endedAt) { S.rc.endedAt = now(); log('rollcall_end', { rollcall_id: S.rc.id, duration_sec: Math.round((S.rc.endedAt - S.rc.startedAt) / 1000), checked: checked(), total: total() }); }
    S.rc.departAt = now();
    S.rc.deadline = now() + WAIT();
    S.rc.alerted = false;
    log('depart', { rollcall_id: S.rc.id, unchecked: unchecked().length });
    keepAwake(false); stopNfc();
    toast(unchecked().length ? `출발 · ${mmss(WAIT() / 1000)} 뒤 미확인자 경보` : '출발 · 전원 확인됨');
  }

  function checkDeadline() {
    if (!S.rc || !S.rc.deadline || S.rc.alerted) return;
    if (now() < S.rc.deadline) return;
    S.rc.alerted = true;
    const miss = unchecked();
    miss.forEach(t => {
      const a = { id: uid(), tid: t.id, rcId: S.rc.id, raisedAt: now(), label: null, labeledAt: null, resolvedAt: null, dist: S.rc.dist[t.id] ?? null };
      S.alerts.push(a);
      log('alert_raised', { actor: 'system', rollcall_id: S.rc.id, traveler_id: t.id, alert_grade: '긴급', distance_m: a.dist, since_depart_sec: Math.round((now() - S.rc.departAt) / 1000) });
    });
    if (miss.length) {
      if (navigator.vibrate) navigator.vibrate([300, 120, 300, 120, 300]);
      notify(`미승차 ${miss.length}명`, miss.map(t => `${t.no} ${t.name} 님`).join(', '));
      modal = { type: 'alert' };
    }
    save();
  }

  function notify(title, body) {
    try {
      if (!('Notification' in window) || Notification.permission !== 'granted') return;
      navigator.serviceWorker?.ready.then(r => r.showNotification('Keep121 · ' + title, { body, icon: 'icon.svg', tag: 'keep-alert', renotify: true })).catch(() => {});
    } catch {}
  }

  function labelAlert(aid, label) {
    const a = S.alerts.find(x => x.id === aid);
    if (!a || a.label) return;
    a.label = label; a.labeledAt = now();
    log('alert_labeled', { traveler_id: a.tid, label, alert_id: a.id });
    if (label === 'false_alarm') {
      // 실제로는 탑승 → 확인 처리하고 해결
      if (S.rc && !S.rc.checks[a.tid]) { S.rc.checks[a.tid] = { m: 'manual', ts: now() }; log('manual_confirmed', { traveler_id: a.tid, method: 'manual', note: 'false_alarm' }); }
      resolveAlert(aid, true);
    }
    const pending = S.alerts.filter(x => !x.label);
    modal = pending.length ? { type: 'alert' } : null;
    save(); render();
  }

  function resolveAlert(aid, silent) {
    const a = S.alerts.find(x => x.id === aid);
    if (!a || a.resolvedAt) return;
    a.resolvedAt = now();
    if (S.rc && !S.rc.checks[a.tid]) { S.rc.checks[a.tid] = { m: 'manual', ts: now() }; log('manual_confirmed', { traveler_id: a.tid, method: 'manual', note: 'rejoined' }); }
    log('alert_resolved', { traveler_id: a.tid, alert_id: a.id, resolution_sec: Math.round((a.resolvedAt - a.raisedAt) / 1000) });
    if (!silent) toast(`${tById(a.tid).name} 님 합류 · 해결 ${mmss((a.resolvedAt - a.raisedAt) / 1000)}`);
    save(); render();
  }

  // ---------- 가족 알림 (알림톡 연동 전: 공유/복사) ----------
  async function familyNotice() {
    const s = stop();
    const msg = `[Keep121] ${S.tour.name} · ${hm(now())} ${s.name} 도착, 가이드 확인됨`;
    log('family_notified', { channel: 'share', message: msg, recipients: S.travelers.filter(t => t.consent).length });
    try {
      if (navigator.share) await navigator.share({ text: msg });
      else { await navigator.clipboard.writeText(msg); toast('문구를 복사했습니다'); }
    } catch {}
    render();
  }

  // ---------- 명단 업로드 (CSV · XLSX) ----------
  function parseRows(rows) {
    // 헤더: 번호, 이름, 연락처, 가족연락처, 명찰(tag|check)
    const head = rows[0].map(h => String(h).trim());
    const col = k => head.findIndex(h => h.includes(k));
    const ci = { no: col('번호'), name: col('이름'), phone: col('연락처'), fam: col('가족'), tag: col('명찰') };
    if (ci.name < 0) throw new Error('이름 열이 없습니다');
    const list = rows.slice(1).filter(r => r[ci.name]).map((r, i) => ({
      id: 't' + uid(), no: Number(r[ci.no]) || i + 1, name: String(r[ci.name]).trim(),
      phone: ci.phone >= 0 ? String(r[ci.phone] ?? '') : '',
      family: ci.fam >= 0 ? String(r[ci.fam] ?? '') : '',
      tagType: ci.tag >= 0 && /check|nfc|체크/i.test(String(r[ci.tag])) ? 'check' : 'tag',
      nfc: '', consent: false
    }));
    if (!list.length) throw new Error('명단이 비어 있습니다');
    return list;
  }
  function csvRows(text) {
    return text.replace(/^﻿/, '').split(/\r?\n/).filter(Boolean).map(l => l.split(',').map(c => c.replace(/^"|"$/g, '').trim()));
  }
  async function loadXlsx() {
    if (window.XLSX) return;
    await new Promise((ok, no) => { const s = document.createElement('script'); s.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js'; s.onload = ok; s.onerror = no; document.head.appendChild(s); });
  }
  async function importFile(file) {
    try {
      let rows;
      if (/\.xlsx?$/i.test(file.name)) {
        await loadXlsx();
        const wb = XLSX.read(await file.arrayBuffer());
        rows = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1 });
      } else rows = csvRows(await file.text());
      const list = parseRows(rows);
      S.travelers = list; S.rc = null; S.alerts = [];
      log('roster_uploaded', { count: list.length, file: file.name });
      toast(`명단 ${list.length}명 업로드`);
    } catch (e) { toast('업로드 실패: ' + e.message); }
  }
  function download(name, text, type = 'text/csv') {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob(['﻿' + text], { type }));
    a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  }
  const template = () => download('keep121_명단_양식.csv', '번호,이름,연락처,가족연락처,명찰\n1,홍길동,010-0000-0000,010-1111-1111,tag\n2,김영희,010-2222-2222,010-3333-3333,check\n');
  function exportEvents() {
    const cols = ['ts', 'type', 'actor', 'stop_id', 'traveler_id', 'method', 'alert_grade', 'label', 'distance_m', 'resolution_sec', 'duration_sec'];
    const lines = [cols.join(',')].concat(S.events.map(e => cols.map(c => c === 'ts' ? new Date(e.ts).toISOString() : (e[c] ?? '')).join(',')));
    download(`keep121_event_log_${new Date().toISOString().slice(0, 10)}.csv`, lines.join('\n'));
  }

  // ---------- metrics (모두 event에서 계산) ----------
  function metrics() {
    const ends = S.events.filter(e => e.type === 'rollcall_end');
    const durs = ends.map(e => e.duration_sec).filter(n => n >= 0);
    const raised = S.events.filter(e => e.type === 'alert_raised');
    const labeled = S.events.filter(e => e.type === 'alert_labeled');
    const fa = labeled.filter(e => e.label === 'false_alarm').length;
    const res = S.events.filter(e => e.type === 'alert_resolved').map(e => e.resolution_sec);
    const inform = raised.map(e => e.since_depart_sec).filter(n => n >= 0);
    const avg = a => a.length ? a.reduce((x, y) => x + y, 0) / a.length : null;
    return {
      rollcalls: ends.length, avgDur: avg(durs), alerts: raised.length,
      faRate: labeled.length ? Math.round(fa / labeled.length * 100) : null,
      avgRes: avg(res), avgInform: avg(inform),
      notices: S.events.filter(e => e.type === 'family_notified').length
    };
  }

  // ---------- views ----------
  function header() {
    const d = day();
    const live = S.rc && !S.rc.endedAt;
    const dep = S.rc && S.rc.deadline && !S.rc.alerted;
    const pill = openAlerts().length ? `<span class="pill live">${I('alert', 13)}경보 ${openAlerts().length}</span>`
      : live ? `<span class="pill live">점호 중</span>`
      : dep ? `<span class="pill live">${I('bus', 13)}<span class="timer" data-timer>${mmss((S.rc.deadline - now()) / 1000)}</span></span>`
      : `<span class="pill demo">데모</span>`;
    return `<header class="hdr"><div class="hdr-in">
      <div class="hdr-logo"><svg viewBox="0 0 48 48" width="26" height="26"><path d="M14 38V23a10 10 0 0 1 20 0v15" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/><circle cx="24" cy="30.5" r="3.8" fill="#F2A541"/></svg></div>
      <div class="hdr-t"><b>${esc(S.tour.name)} · ${esc(d.label)}</b><span>${esc(stop().name)} · ${esc(S.tour.agency)}</span></div>
      ${pill}
    </div></header>`;
  }

  function viewToday() {
    const d = day(), s = stop();
    const m = metrics();
    const [gh, gm] = s.time.split(':').map(Number);
    const g = new Date(); g.setHours(gh, gm, 0, 0);
    const late = now() > g.getTime() + 5 * 60000 && !(S.rc && S.rc.stopId === s.id && S.rc.departAt);
    return `
      ${openAlerts().length ? `<button class="banner bad" data-act="open-alerts">${I('alert')}처리 중인 경보 ${openAlerts().length}건 · 눌러서 보기</button>` : ''}
      <section class="card hero">
        <div class="k">지금 정차지</div>
        <h3>${esc(s.name)}</h3>
        <div class="local">${esc(s.local)}</div>
        <div class="gather">${I('pin')}<div class="grow"><div class="small" style="color:#C9CFE6">집합 · ${esc(s.place)}</div><b>${esc(s.time)}</b></div>
          <button class="btn btn-sm btn-dawn" data-act="edit-stop">${I('edit', 16)}변경</button></div>
      </section>
      ${late ? `<div class="banner warn">${I('clock')}집합 시각 +5분이 지났습니다. 점호·출발을 기록하세요.</div>` : ''}
      <div class="days">${S.days.map(x => `<button class="${x.day === d.day ? 'on' : ''}" data-day="${x.day}">${esc(x.label)} · ${esc(x.city)}</button>`).join('')}</div>
      <section class="card">
        ${d.stops.map(x => `<div class="stop ${x.id === s.id ? 'cur' : ''}">
          <div class="tm">${esc(x.time)}</div>
          <div class="grow"><b>${esc(x.name)}</b><div class="meta">${esc(x.place)}</div></div>
          ${x.id === s.id ? '<span class="pill ok">현재</span>' : `<button class="btn btn-sm btn-line" data-stop="${x.id}">선택</button>`}
        </div>`).join('')}
      </section>
      <div class="sec-t"><h2>오늘 기록</h2><span>이벤트 로그 기준</span></div>
      <div class="stats">
        <div class="stat"><b>${m.rollcalls}</b><span>점호 횟수</span></div>
        <div class="stat"><b>${m.avgDur == null ? '—' : mmss(m.avgDur)}</b><span>평균 점호 시간 (목표 0:30)</span></div>
      </div>
      <p class="fine">로컬 데모 모드 · 데이터는 이 기기에만 저장됩니다. Keep Tag 위치는 시뮬레이션입니다.</p>`;
  }

  function viewRollcall() {
    const live = S.rc && !S.rc.endedAt;
    const rc = S.rc;
    if (!rc) {
      return `<section class="card big">
          <div class="n">0<small>/${total()}</small></div>
          <div class="s muted">${esc(stop().name)} · 집합 ${esc(stop().time)}</div>
        </section>
        <button class="btn btn-block btn-dawn" data-act="start">${I('nfc')}점호 시작</button>
        <p class="fine">${NFC_OK ? '점호를 시작하면 여행객이 가이드 휴대폰 뒷면에 명찰을 대기만 하면 됩니다.' : '이 기기는 Web NFC를 지원하지 않아 데모 탭 버튼으로 체험합니다. 실제 탭은 Android Chrome에서 동작합니다.'}</p>`;
    }
    const miss = unchecked();
    const cands = miss.filter(isCand);
    const rest = miss.filter(t => !isCand(t));
    const dep = rc.departAt;
    const elapsed = ((rc.endedAt || now()) - rc.startedAt) / 1000;
    const done = S.travelers.filter(t => rc.checks[t.id]).sort((a, b) => rc.checks[b.id].ts - rc.checks[a.id].ts).slice(0, 6);
    return `
      <section class="card big">
        <div class="n">${checked()}<small>/${total()}</small></div>
        ${miss.length ? `<div class="s bad">${I(dep ? 'bus' : 'usercheck')}${dep ? '미승차' : '미확인'} ${miss.length}명</div>` : `<div class="s good">${I('check')}전원 확인</div>`}
        <div class="meter">
          <span class="pill">이번 점호 <b class="timer" data-elapsed>${mmss(elapsed)}</b></span>
          <span class="pill">목표 0:30</span>
          ${dep && !rc.alerted ? `<span class="pill live">${I('bus', 13)}경보까지 <b class="timer" data-timer>${mmss((rc.deadline - now()) / 1000)}</b></span>` : ''}
          ${dep && rc.alerted ? `<span class="pill">출발 ${hm(dep)}</span>` : ''}
        </div>
      </section>
      ${live ? `<div class="nfc-wait"><span class="dot">${I('nfc', 22)}</span><div class="grow"><b>${NFC_OK ? '명찰 탭 대기 중' : '명찰 탭 (데모)'}</b><span>${NFC_OK ? '휴대폰 뒷면에 명찰을 대 주세요' : '오른쪽 버튼으로 탭을 흉내 냅니다'}</span></div>${NFC_OK ? '' : `<button class="btn btn-sm btn-dawn" data-act="demo-tap">탭</button>`}</div>` : ''}
      ${cands.length ? `<div class="sec-t"><h2>Keep Tag 후보 · 확인 필요</h2><span>${S.settings.radius}m 이내 ${cands.length}명</span></div>
        <div class="list">${cands.map(t => `<div class="p cand"><span class="no">${t.no}</span><div class="grow"><b>${esc(t.name)} 님</b><span class="meta">Keep Tag · 집합 장소에서 ${rc.dist[t.id]}m</span></div>
          <div class="acts"><button class="btn btn-sm btn-indigo" data-cand="${t.id}">${I('check', 16)}확인</button></div></div>`).join('')}</div>` : ''}
      ${rest.length ? `<div class="sec-t"><h2>${dep ? '미승차' : '미확인'}</h2><span>${rest.length}명</span></div>
        <div class="list">${rest.map(t => `<div class="p miss"><span class="no">${t.no}</span><div class="grow"><b>${esc(t.name)} 님</b><span class="meta">${t.tagType === 'tag' ? `Keep Tag · ${rc.dist[t.id] ?? '—'}m` : 'Keep Check (위치 없음)'} · 마지막 확인 ${lastSeen(t.id)}</span></div>
          <div class="acts">${t.tagType === 'tag' ? `<button class="btn btn-sm btn-line" data-loc="${t.id}" aria-label="위치 보기">${I('pin', 16)}</button>` : ''}<button class="btn btn-sm btn-line" data-man="${t.id}">직접 확인</button></div></div>`).join('')}</div>` : ''}
      ${!dep ? `<button class="btn btn-block btn-indigo" data-act="depart">${I('bus')}버스 출발</button>` : `<button class="btn btn-block btn-line" data-act="reset-rc">${I('refresh')}다음 정차지 점호 준비</button>`}
      ${done.length ? `<div class="sec-t"><h2>최근 확인</h2><span>${checked()}명</span></div>
        <div class="list">${done.map(t => `<div class="p done"><span class="no">${t.no}</span><div class="grow"><b>${esc(t.name)} 님</b><span class="meta">${({ nfc: '명찰 탭', tag_candidate: 'Keep Tag 후보 확인', manual: '직접 확인' })[rc.checks[t.id].m]} · ${hm(rc.checks[t.id].ts)}</span></div><span class="chk">${I('check')}</span></div>`).join('')}</div>` : ''}`;
  }

  function viewRoster() {
    const consent = S.travelers.filter(t => t.consent).length;
    const bound = S.travelers.filter(t => t.nfc).length;
    return `
      <section class="card">
        <h3>${esc(S.tour.name)} 명단 · ${total()}명</h3>
        <p class="sub">동의 ${consent}/${total()} · NFC 명찰 등록 ${bound}/${total()}</p>
        <div class="grid2" style="margin-top:12px">
          <label class="btn btn-indigo btn-sm" style="cursor:pointer">${I('upload', 16)}엑셀·CSV 업로드<input type="file" accept=".csv,.xlsx,.xls" data-file hidden></label>
          <button class="btn btn-line btn-sm" data-act="template">${I('download', 16)}양식 받기</button>
        </div>
      </section>
      <div class="list">${S.travelers.map(t => `<div class="p ${t.consent ? '' : 'miss'}">
        <span class="no">${t.no}</span>
        <div class="grow"><b>${esc(t.name)} 님</b><span class="meta">${t.tagType === 'tag' ? 'Keep Tag' : 'Keep Check'}${t.nfc ? ' · NFC 등록' : ''} · ${t.consent ? '동의함' : '동의 미확인'}</span></div>
        <div class="acts">
          <button class="btn btn-sm btn-line" data-consent="${t.id}">${t.consent ? '동의 취소' : '구두 동의'}</button>
          <button class="btn btn-sm btn-line" data-bind="${t.id}" aria-label="NFC 명찰 등록">${I('nfc', 16)}</button>
        </div></div>`).join('')}</div>
      <p class="fine">동의 기본값은 좌표가 아니라 확인 상태입니다. 동의하지 않은 분은 위치를 표시하지 않습니다.</p>`;
  }

  const LABEL = {
    rollcall_start: ['점호 시작', ''], rollcall_end: ['점호 종료', 'ok'], checkin: ['명찰 탭', 'ok'], candidate_confirmed: ['후보 확인', 'ok'],
    manual_confirmed: ['직접 확인', 'ok'], depart: ['버스 출발', ''], alert_raised: ['미승차 경보', 'bad'], alert_labeled: ['라벨', 'warn'],
    alert_resolved: ['경보 해결', 'ok'], family_notified: ['가족 알림', ''], roster_uploaded: ['명단 업로드', ''], consent_recorded: ['동의 기록', ''], stop_changed: ['정차지 변경', '']
  };
  function evText(e) {
    const t = e.traveler_id ? tById(e.traveler_id) : null;
    const who = t ? `${t.no} ${t.name} 님` : '';
    switch (e.type) {
      case 'rollcall_end': return `${e.checked}/${e.total} · ${mmss(e.duration_sec)}`;
      case 'depart': return `미확인 ${e.unchecked}명`;
      case 'alert_raised': return `${who} · 출발 후 ${mmss(e.since_depart_sec)}`;
      case 'alert_labeled': return `${who} · ${e.label === 'false_alarm' ? '오경보' : '확인함'}`;
      case 'alert_resolved': return `${who} · ${mmss(e.resolution_sec)}`;
      case 'family_notified': return `${e.recipients}가구 · ${esc(e.message)}`;
      case 'roster_uploaded': return `${e.count}명`;
      default: return who;
    }
  }

  function viewReport() {
    const m = metrics();
    const evs = [...S.events].reverse().slice(0, 60);
    const oa = openAlerts();
    return `
      ${oa.length ? `<div class="sec-t"><h2>처리 중인 경보</h2><span>${oa.length}건</span></div>
      <div class="list">${oa.map(a => { const t = tById(a.tid); return `<div class="p miss"><span class="no">${t.no}</span><div class="grow"><b>${esc(t.name)} 님</b><span class="meta">${a.label ? '확인함' : '라벨 대기'} · 발생 ${hm(a.raisedAt)}</span></div>
        <div class="acts">${a.label ? `<button class="btn btn-sm btn-indigo" data-resolve="${a.id}">합류</button>` : `<button class="btn btn-sm btn-coral" data-act="open-alerts">라벨</button>`}</div></div>`; }).join('')}</div>` : ''}
      <div class="sec-t"><h2>파일럿 지표</h2><span>실측 · 이 기기</span></div>
      <div class="stats">
        <div class="stat"><b>${m.avgDur == null ? '—' : mmss(m.avgDur)}</b><span>평균 점호 시간 · ${m.rollcalls}회</span></div>
        <div class="stat"><b>${m.avgInform == null ? '—' : mmss(m.avgInform)}</b><span>출발 후 미승차 인지</span></div>
        <div class="stat"><b>${m.alerts}</b><span>경보 · 오경보 ${m.faRate == null ? '—' : m.faRate + '%'}</span></div>
        <div class="stat"><b>${m.avgRes == null ? '—' : mmss(m.avgRes)}</b><span>평균 경보 해결 시간</span></div>
      </div>
      <section class="card">
        <h3>가족 알림 (Keep Home)</h3>
        <p class="sub">${esc(stop().name)} 도착을 가이드 확인 후 보냅니다. 알림톡 연동 전에는 공유·복사로 대신합니다. 지금까지 ${m.notices}회.</p>
        <button class="btn btn-dawn btn-block" style="margin-top:12px" data-act="family">${I('send')}도착 알림 보내기</button>
      </section>
      <div class="sec-t"><h2>이벤트 로그</h2><span>${S.events.length}건</span></div>
      <section class="card tl">${evs.length ? evs.map(e => `<div class="tl-i"><span class="t">${hm(e.ts)}</span><div><span class="tag ${LABEL[e.type]?.[1] || ''}">${LABEL[e.type]?.[0] || esc(e.type)}</span>${evText(e)}</div></div>`).join('') : '<p class="sub">아직 기록이 없습니다. 점호를 시작해 보세요.</p>'}</section>
      <div class="grid2">
        <button class="btn btn-line btn-sm" data-act="export">${I('download', 16)}로그 CSV</button>
        <button class="btn btn-line btn-sm" data-act="settings">설정</button>
      </div>`;
  }

  function viewModal() {
    if (!modal) return '';
    if (modal.type === 'alert') {
      const pend = S.alerts.filter(a => !a.label);
      if (!pend.length) { modal = null; return ''; }
      const a = pend[0], t = tById(a.tid);
      return `<div class="scrim"><div class="sheet alert" role="alertdialog" aria-label="미승차 경보">
        <div class="k">${I('alert', 16)} 미승차 경보 · 출발 ${hm(S.rc?.departAt || a.raisedAt)}${pend.length > 1 ? ` · 외 ${pend.length - 1}명` : ''}</div>
        <div class="who"><span class="no">${t.no}</span><div><b>${esc(t.name)} 님</b><span>${t.tagType === 'tag' ? `Keep Tag · 집합 장소에서 ${a.dist ?? '—'}m` : 'Keep Check · 위치 없음'} · 마지막 확인 ${lastSeen(t.id)}</span></div></div>
        ${t.tagType === 'tag' ? `<button class="btn btn-line btn-block" data-loc="${t.id}">${I('pin')}위치 보기</button>` : ''}
        <div class="grid2">
          <button class="btn btn-white btn-block" data-label="${a.id}:confirmed">확인함</button>
          <button class="btn btn-line btn-block" data-label="${a.id}:false_alarm">오경보 (탑승함)</button>
        </div>
        <p class="fine" style="color:#FFE1E1">라벨을 남겨야 닫힙니다. 라벨은 경보 규칙 튜닝에 쓰입니다.</p>
      </div></div>`;
    }
    if (modal.type === 'loc') {
      const t = tById(modal.tid), s = stop();
      const d = S.rc?.dist[t.id] ?? 50;
      const ang = (t.no * 47) % 360;
      const lat = BASE.lat + d / 111000 * Math.cos(ang * Math.PI / 180), lng = BASE.lng + d / 107000 * Math.sin(ang * Math.PI / 180);
      const dir = ['북', '북동', '동', '남동', '남', '남서', '서', '북서'][Math.round(ang / 45) % 8];
      return `<div class="scrim" data-close><div class="sheet">
        <div class="row"><h3 class="grow">${t.no} ${esc(t.name)} 님 위치</h3><button class="btn btn-sm btn-line" data-close aria-label="닫기">${I('x', 16)}</button></div>
        <div class="stats"><div class="stat"><b>${d}m</b><span>집합 장소에서</span></div><div class="stat"><b>${dir}</b><span>방향 (시뮬레이션)</span></div></div>
        <a class="btn btn-indigo btn-block" href="https://www.google.com/maps/search/?api=1&query=${lat.toFixed(6)},${lng.toFixed(6)}" target="_blank" rel="noopener">${I('pin')}지도에서 열기</a>
        <div class="taxi"><div class="small muted">택시 기사에게 보여 주세요</div><div class="loc">${esc(s.local)}</div><div class="small">${esc(s.place)}</div></div>
        <p class="fine">좌표는 경보·미확인자에게만 표시되고, 투어 종료 후 파기합니다.</p>
      </div></div>`;
    }
    if (modal.type === 'stop') {
      const s = stop();
      return `<div class="scrim" data-close><form class="sheet" data-form="stop">
        <div class="row"><h3 class="grow">집합 시각·장소 변경</h3><button type="button" class="btn btn-sm btn-line" data-close aria-label="닫기">${I('x', 16)}</button></div>
        <div class="field"><label>정차지</label><input name="name" value="${esc(s.name)}" required></div>
        <div class="grid2"><div class="field"><label>집합 시각</label><input name="time" type="time" value="${esc(s.time)}" required></div>
        <div class="field"><label>현지어 이름</label><input name="local" value="${esc(s.local)}"></div></div>
        <div class="field"><label>집합 장소</label><input name="place" value="${esc(s.place)}" required></div>
        <button class="btn btn-indigo btn-block" type="submit">저장</button>
      </form></div>`;
    }
    if (modal.type === 'bind') {
      const t = tById(modal.tid);
      return `<div class="scrim" data-close><div class="sheet">
        <h3>${t.no} ${esc(t.name)} 님 명찰 등록</h3>
        <div class="nfc-wait"><span class="dot">${I('nfc', 22)}</span><div><b>명찰을 휴대폰 뒷면에 대 주세요</b><span>NFC 명찰의 고유번호를 이 분께 연결합니다</span></div></div>
        <button class="btn btn-line btn-block" data-close>취소</button>
      </div></div>`;
    }
    if (modal.type === 'settings') {
      return `<div class="scrim" data-close><div class="sheet">
        <div class="row"><h3 class="grow">설정</h3><button class="btn btn-sm btn-line" data-close aria-label="닫기">${I('x', 16)}</button></div>
        <label class="switch"><span><b>빠른 경보 (데모)</b><br><span class="small muted">출발 후 3분 대신 15초에 경보</span></span><input type="checkbox" data-set="fast" ${S.settings.fast ? 'checked' : ''}></label>
        <div class="field"><label>Keep Tag 후보 반경 (m)</label><input type="number" min="10" max="200" step="5" value="${S.settings.radius}" data-set="radius"></div>
        <label class="switch"><span><b>경보 알림 받기</b><br><span class="small muted">화면이 꺼져 있을 때 시스템 알림</span></span><button class="btn btn-sm btn-line" data-act="perm">${('Notification' in window && Notification.permission === 'granted') ? '허용됨' : '허용'}</button></label>
        <button class="btn btn-line btn-block" data-act="reset">${I('refresh')}데모 데이터로 초기화</button>
        <p class="fine">Keep121 Guide v0 · 로컬 데모 모드 · Web NFC ${NFC_OK ? '사용 가능' : '미지원 기기'}</p>
      </div></div>`;
    }
    return '';
  }

  function nav() {
    const live = S.rc && !S.rc.endedAt;
    const tabs = [['today', '오늘', 'clock'], ['rollcall', '점호', 'usercheck'], ['roster', '명단', 'users'], ['report', '리포트', 'file']];
    const badge = { rollcall: S.rc && !S.rc.endedAt ? unchecked().length : 0, report: openAlerts().length };
    return `${!modal ? (live ? `<button class="fab stop" data-act="end">${I('check')}점호 종료</button>` : (!S.rc || S.rc.departAt || S.rc.endedAt) && tab !== 'roster' ? `<button class="fab" data-act="start">${I('nfc')}점호 시작</button>` : '') : ''}
      <nav class="bnav" aria-label="하단 메뉴"><div class="bnav-in">${tabs.map(([k, l, ic]) => `<button class="${tab === k ? 'on' : ''}" data-tab="${k}" ${tab === k ? 'aria-current="page"' : ''}>${I(ic)}<span>${l}</span>${badge[k] ? `<span class="badge">${badge[k]}</span>` : ''}</button>`).join('')}</div></nav>`;
  }

  function render() {
    const body = { today: viewToday, rollcall: viewRollcall, roster: viewRoster, report: viewReport }[tab]();
    $app.innerHTML = `<div class="shell">${header()}<main>${body}</main></div>${nav()}${viewModal()}${toastMsg ? `<div class="toast" role="status">${esc(toastMsg)}</div>` : ''}`;
  }

  // ---------- events ----------
  $app.addEventListener('click', e => {
    const el = e.target.closest('[data-tab],[data-act],[data-cand],[data-man],[data-loc],[data-label],[data-resolve],[data-day],[data-stop],[data-consent],[data-bind],[data-close]');
    if (!el) return;
    const d = el.dataset;
    if (d.close !== undefined) { if (el.classList.contains('scrim') && e.target !== el) return; if (modal?.type === 'bind') { bindTarget = null; if (!S.rc || S.rc.endedAt) stopNfc(); } modal = null; return render(); }
    if (d.tab) { tab = d.tab; window.scrollTo(0, 0); return render(); }
    if (d.cand) return checkIn(d.cand, 'tag_candidate');
    if (d.man) return checkIn(d.man, 'manual');
    if (d.loc) { modal = { type: 'loc', tid: d.loc }; return render(); }
    if (d.label) { const [id, l] = d.label.split(':'); return labelAlert(id, l); }
    if (d.resolve) return resolveAlert(d.resolve);
    if (d.day) { S.tour.day = Number(d.day); S.tour.stopId = day().stops[0].id; save(); return render(); }
    if (d.stop) { S.tour.stopId = d.stop; log('stop_changed', { to: d.stop }); return render(); }
    if (d.consent) { const t = tById(d.consent); t.consent = !t.consent; log('consent_recorded', { traveler_id: t.id, consent: t.consent, method: 'verbal' }); return render(); }
    if (d.bind) return bindTag(d.bind);
    switch (d.act) {
      case 'start': return startRollcall();
      case 'end': endRollcall(); return render();
      case 'demo-tap': return demoTap();
      case 'depart': depart(); return render();
      case 'reset-rc': S.rc = null; save(); return render();
      case 'open-alerts': modal = S.alerts.some(a => !a.label) ? { type: 'alert' } : null; tab = 'report'; return render();
      case 'edit-stop': modal = { type: 'stop' }; return render();
      case 'family': return familyNotice();
      case 'template': return template();
      case 'export': return exportEvents();
      case 'settings': modal = { type: 'settings' }; return render();
      case 'perm': if ('Notification' in window) Notification.requestPermission().then(render); return;
      case 'reset': if (confirm('모든 기록을 지우고 데모 데이터로 되돌릴까요?')) { S = demoState(); save(); modal = null; tab = 'rollcall'; render(); } return;
    }
  });
  $app.addEventListener('change', e => {
    const el = e.target;
    if (el.matches('[data-file]') && el.files[0]) return importFile(el.files[0]).then(render);
    if (el.dataset.set === 'fast') { S.settings.fast = el.checked; save(); }
    if (el.dataset.set === 'radius') { S.settings.radius = Math.max(10, Math.min(200, Number(el.value) || 40)); save(); }
  });
  $app.addEventListener('submit', e => {
    if (!e.target.matches('[data-form="stop"]')) return;
    e.preventDefault();
    const f = new FormData(e.target), s = stop();
    ['name', 'time', 'local', 'place'].forEach(k => { s[k] = String(f.get(k) || '').trim() || s[k]; });
    log('stop_changed', { to: s.id, time: s.time, place: s.place });
    modal = null; toast('집합 정보를 바꿨습니다'); render();
  });

  // 1초 루프: 타이머 표시, 경보 판정, 위치 변화(시뮬레이션)
  let tick = 0;
  setInterval(() => {
    tick++;
    const before = !!modal;
    checkDeadline();
    if (S.rc && !S.rc.endedAt && tick % 4 === 0) { driftDistances(); save(); if (!modal) render(); return; }
    if (modal && !before) return render();
    document.querySelectorAll('[data-timer]').forEach(n => { if (S.rc?.deadline) n.textContent = mmss((S.rc.deadline - now()) / 1000); });
    document.querySelectorAll('[data-elapsed]').forEach(n => { if (S.rc && !S.rc.endedAt) n.textContent = mmss((now() - S.rc.startedAt) / 1000); });
  }, 1000);

  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && S.rc && !S.rc.endedAt) keepAwake(true); });
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
  render();
})();
