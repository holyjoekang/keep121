/* 1분 3D 제안 · 포토 스테이지 엔진 (원본: scripts/stage3d.js)
   - 배경: 각 제안서의 사진 (CSS 레이어 · 천천히 확대 · 마우스/기울기 시차)
   - 전경: 장면마다 다른 3D 오브젝트 (지도 핀 · 인파 · SmartTag · 휴대폰/문서 · 카드 회전목마 · 막대 · 경로 · Keep121 문)
   - 상호작용: 끌어서 돌리기 · 마우스를 올리면 설명 · 길 잃은 사람을 눌러 찾기
   - 소리: 장면별 내레이션 + 합성 배경음 (sound3d.js)
   <body data-src="data/xxx_stage.json"> · ?t=초 · ?pause */
import * as THREE from 'three';
import { createSound } from './sound3d.js?v=1';

const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const $ = s => document.querySelector(s);
const COL = { dawn: '#F2A541', indigo: '#5b6fd6', mint: '#3fbf8f', red: '#ff5a5a', white: '#f4f6ff', ink: '#141a2e', sky: '#8fa0ff' };
const easeOutBack = x => 1 + 2.4 * Math.pow(x - 1, 3) + 1.4 * Math.pow(x - 1, 2);
const clamp01 = x => Math.max(0, Math.min(1, x));

// ── 렌더러 ─────────────────────────────────────────────────
const canvas = $('#scene');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setClearColor(0x000000, 0);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
camera.position.set(0, 3.2, 12);
scene.add(new THREE.HemisphereLight('#dfe6ff', '#1b2350', 1.6));
const sun = new THREE.DirectionalLight('#ffffff', 1.6); sun.position.set(4, 8, 6); scene.add(sun);
const stage = new THREE.Group(); scene.add(stage);           // 끌어서 돌리는 전경 무대
let content = null, ticks = [], hits = [];                   // 현재 장면의 오브젝트 · 매 프레임 갱신 · 클릭/호버 대상

const std = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.45, metalness: 0.1, ...extra });
const glow = color => new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.9 });

// HTML 라벨 (3D 좌표를 화면에 투영)
const labelsBox = $('#labels');
let labels = [];
const addLabel = (obj, html, cls = '', dy = 0.5) => { const el = document.createElement('div'); el.className = `lbl ${cls}`; el.innerHTML = html; labelsBox.appendChild(el); labels.push({ obj, el, dy }); return el; };
const v3 = new THREE.Vector3();
const placeLabels = () => {
  const w = innerWidth, h = innerHeight;
  for (const L of labels) {
    L.obj.getWorldPosition(v3); v3.y += L.dy; v3.project(camera);
    const vis = v3.z < 1 && L.obj.visible && content && content.scale.x > 0.6 && Math.abs(v3.x) < 1.05 && Math.abs(v3.y) < 1.05;
    L.el.style.transform = `translate(-50%,-100%) translate(${(v3.x * 0.5 + 0.5) * w}px,${(-v3.y * 0.5 + 0.5) * h}px)`;
    L.el.style.opacity = vis ? '' : 0;
  }
};

// 캔버스 텍스처 (휴대폰 화면 · 문서 · 카드)
const canvasTex = (w, h, draw) => {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const paint = () => { g.clearRect(0, 0, w, h); draw(g, w, h); tex.needsUpdate = true; };
  paint(); document.fonts && document.fonts.ready.then(paint);
  return tex;
};
const FONT = '"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif';
const wrapText = (g, text, x, y, maxW, lh) => {
  let line = '';
  for (const ch of String(text)) { if (g.measureText(line + ch).width > maxW && line) { g.fillText(line, x, y); y += lh; line = ch; } else line += ch; }
  if (line) g.fillText(line, x, y); return y + lh;
};
const rrect = (g, x, y, w, h, r) => { g.beginPath(); g.roundRect ? g.roundRect(x, y, w, h, r) : g.rect(x, y, w, h); };

// ── 오브젝트 만들기 ───────────────────────────────────────────
const B = {
  // 지도 핀: [x, z, 이름, 색]
  pins(o, g) {
    const base = new THREE.Mesh(new THREE.CircleGeometry(5.2, 64), new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0.08 }));
    base.rotation.x = -Math.PI / 2; base.scale.set(1.35, 0.7, 1); g.add(base);
    o.items.forEach(([x, z, name, c = COL.dawn, note = ''], i) => {
      const pin = new THREE.Group(); pin.position.set(x, 0, z);
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 24), std(c, { emissive: c, emissiveIntensity: 0.35 }));
      const cone = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.5, 20), std(c)); cone.rotation.x = Math.PI; cone.position.y = 0.3; head.position.y = 0.62;
      const ring = new THREE.Mesh(new THREE.RingGeometry(0.25, 0.32, 40), glow(c)); ring.rotation.x = -Math.PI / 2; ring.position.y = 0.02;
      pin.add(cone, head, ring); g.add(pin);
      head.userData.tip = `<b>${E(name)}</b>${note ? `<br>${E(note)}` : ''}`; hits.push(head);
      addLabel(head, E(name), 'pin', 0.35);
      ticks.push((t, lt) => { pin.position.y = Math.sin(t * 2 + i) * 0.08 + 0.1; const k = (t * 0.8 + i * 0.3) % 1; ring.scale.setScalar(1 + k * 2.5); ring.material.opacity = (1 - k) * 0.9; });
    });
  },
  // 인파 속 한 사람: 그룹 · 인솔자(주황) · 길 잃은 사람(빨강, 눌러서 찾기)
  crowd(o, g) {
    const groups = o.groups || 6, per = o.per || 8, body = new THREE.CapsuleGeometry(0.1, 0.26, 4, 10);
    const lostAt = new THREE.Vector3(3.4, 0.23, 1.6);
    for (let k = 0; k < groups; k++) {
      const cx = ((k % 3) - 1) * 2.6, cz = (Math.floor(k / 3) - 0.5) * 2.4;
      const lead = new THREE.Mesh(body, std(COL.dawn)); lead.position.set(cx, 0.23, cz); lead.scale.setScalar(1.25); g.add(lead);
      for (let j = 0; j < per; j++) {
        const a = j / per * Math.PI * 2, m = new THREE.Mesh(body, std(COL.sky)); m.position.set(cx + Math.cos(a) * 0.62, 0.23, cz + Math.sin(a) * 0.62); g.add(m);
        ticks.push(t => { m.position.y = 0.23 + Math.abs(Math.sin(t * 3 + j + k)) * 0.04; });
      }
    }
    const lost = new THREE.Mesh(body, std(COL.red, { emissive: COL.red, emissiveIntensity: 0.4 })); lost.scale.setScalar(1.2); g.add(lost);
    const ring = new THREE.Mesh(new THREE.RingGeometry(0.4, 0.48, 48), glow(COL.red)); ring.rotation.x = -Math.PI / 2; g.add(ring);
    const tipEl = addLabel(lost, E(o.lostLabel || '미확인 1명 · 눌러서 찾기'), 'warn', 0.45);
    let found = false;
    lost.userData.tip = '<b>마지막 확인 위치</b><br>반경 50m · 눌러서 찾기';
    lost.userData.onClick = () => {
      if (found) return; found = true; lost.material.color.set(COL.mint); lost.material.emissive.set(COL.mint); ring.material.color.set(COL.mint);
      tipEl.innerHTML = E(o.foundLabel || '찾았습니다 · 그룹 합류'); tipEl.className = 'lbl ok'; toast(o.foundToast || '✓ 마지막 위치 반경에서 1분 만에 찾았습니다');
    };
    hits.push(lost);
    ticks.push((t, lt) => {
      const away = found ? Math.max(0, 1 - (lt - 0.6) * 3) : clamp01(lt * 1.6);
      lost.position.lerpVectors(new THREE.Vector3(1.0, 0.23, 1.2), lostAt, away);
      const k = (t * 0.9) % 1; ring.position.set(lost.position.x, 0.02, lost.position.z); ring.scale.setScalar(1 + k * (found ? 1 : 3)); ring.material.opacity = (1 - k) * 0.9;
      if (!found && lt > 0.82) lost.userData.onClick();               // 아무도 누르지 않으면 자동으로 찾는다
    });
  },
  // Galaxy SmartTag3 모양 (둥근 사각 + 고리 구멍) · 신호 파동
  tag(o, g) {
    const s = new THREE.Shape(), w = 1.7, r = 0.5; s.moveTo(-w / 2 + r, -w / 2);
    s.lineTo(w / 2 - r, -w / 2); s.quadraticCurveTo(w / 2, -w / 2, w / 2, -w / 2 + r); s.lineTo(w / 2, w / 2 - r); s.quadraticCurveTo(w / 2, w / 2, w / 2 - r, w / 2);
    s.lineTo(-w / 2 + r, w / 2); s.quadraticCurveTo(-w / 2, w / 2, -w / 2, w / 2 - r); s.lineTo(-w / 2, -w / 2 + r); s.quadraticCurveTo(-w / 2, -w / 2, -w / 2 + r, -w / 2);
    const hole = new THREE.Path(); hole.absarc(0.42, 0.42, 0.16, 0, Math.PI * 2, true); s.holes.push(hole);
    const geo = new THREE.ExtrudeGeometry(s, { depth: 0.22, bevelEnabled: true, bevelThickness: 0.08, bevelSize: 0.08, bevelSegments: 6 }); geo.center();
    const tag = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ color: '#eef1f8', roughness: 0.25, metalness: 0.2, clearcoat: 1 }));
    tag.position.y = 1.4; g.add(tag);
    const logo = new THREE.Mesh(new THREE.CircleGeometry(0.12, 24), glow(COL.dawn)); logo.position.set(-0.3, -0.25, 0.2); tag.add(logo);
    tag.userData.tip = `<b>${E(o.name || 'Galaxy SmartTag3')}</b><br>${E(o.note || '9.5g · Android · iPhone')}`; hits.push(tag);
    const rings = [0, 1, 2].map(() => { const m = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.025, 8, 80), glow(COL.dawn)); m.position.y = 1.4; g.add(m); return m; });
    (o.chips || []).forEach(([txt], i) => { const a = i / o.chips.length * Math.PI * 2, d = new THREE.Object3D(); d.position.set(Math.cos(a) * 2.9, 1.4 + Math.sin(a * 2) * 0.5, Math.sin(a) * 2.2); g.add(d); addLabel(d, E(txt), 'chip', 0); });
    ticks.push(t => { tag.rotation.y = t * 0.7; tag.rotation.x = Math.sin(t * 0.8) * 0.25; rings.forEach((m, i) => { const k = (t * 0.45 + i / 3) % 1; m.scale.setScalar(0.6 + k * 1.8); m.material.opacity = (1 - k) * 0.7; m.rotation.x = Math.PI / 2 + Math.sin(t) * 0.1; }); });
  },
  // 휴대폰(앱 화면) 또는 문서(이행 기록): 캔버스에 그린 화면
  phone(o, g) {
    const doc = o.style === 'doc', W = doc ? 3.4 : 2.2, H = doc ? 4.45 : 4.4;
    const tex = canvasTex(doc ? 760 : 520, doc ? 1000 : 1040, (c, w, h) => {
      c.fillStyle = doc ? '#ffffff' : '#f4f6fa'; c.fillRect(0, 0, w, h);
      c.fillStyle = doc ? '#141a2e' : (o.color || '#4A5BB0'); c.fillRect(0, 0, w, doc ? 120 : 190);
      c.fillStyle = '#fff'; c.font = `600 ${doc ? 24 : 26}px ${FONT}`; c.fillText(o.app || '', 36, doc ? 48 : 92);
      c.font = `800 ${doc ? 36 : 40}px ${FONT}`; c.fillText(o.title || '', 36, doc ? 96 : 150);
      let y = doc ? 170 : 240;
      for (const [a, b, st] of o.rows || []) {
        const ok = st === 'ok', warn = st === 'no', now = st === 'now';
        if (!doc) { c.fillStyle = now ? '#FFF4E2' : '#ffffff'; rrect(c, 24, y - 44, w - 48, 112, 18); c.fill(); if (now) { c.strokeStyle = '#F2A541'; c.lineWidth = 4; c.stroke(); } }
        else { c.strokeStyle = '#e1e5ef'; c.lineWidth = 2; c.beginPath(); c.moveTo(36, y + 60); c.lineTo(w - 36, y + 60); c.stroke(); }
        c.fillStyle = '#5e667d'; c.font = `700 ${doc ? 24 : 24}px ${FONT}`; c.fillText(a, doc ? 36 : 44, y);
        c.fillStyle = '#141a2e'; c.font = `600 ${doc ? 26 : 25}px ${FONT}`; wrapText(c, b, doc ? 230 : 140, y, doc ? w - 400 : w - 300, 32);
        c.fillStyle = ok ? '#E3F1EB' : warn ? '#FBEAEA' : now ? '#FFE7C2' : '#eef0f5'; rrect(c, w - (doc ? 150 : 140), y - 30, doc ? 114 : 100, 44, 22); c.fill();
        c.fillStyle = ok ? '#3E8E6E' : warn ? '#D64545' : now ? '#8a5a00' : '#5e667d'; c.font = `800 20px ${FONT}`; c.fillText(ok ? '✓ 완료' : warn ? '미확인' : now ? '진행' : '예정', w - (doc ? 134 : 126), y);
        y += doc ? 120 : 132;
      }
      if (o.foot) { c.fillStyle = '#5e667d'; c.font = `500 20px ${FONT}`; wrapText(c, o.foot, 36, h - 60, w - 72, 28); }
    });
    const dev = new THREE.Group(); dev.position.y = 2.1; g.add(dev);
    const frame = new THREE.Mesh(new THREE.BoxGeometry(W + 0.14, H + 0.14, 0.12), std(doc ? '#d9deea' : '#0b0e1c', { metalness: doc ? 0 : 0.5, roughness: doc ? 0.9 : 0.3 }));
    const screen = new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshBasicMaterial({ map: tex })); screen.position.z = 0.065;
    dev.add(frame, screen); screen.userData.tip = `<b>${E(o.title)}</b><br>${E(o.tip || '끌어서 돌려 보세요')}`; hits.push(screen);
    (o.callouts || []).forEach(([txt, side], i) => { const d = new THREE.Object3D(); d.position.set(side === 'l' ? -W * 0.5 - 0.9 : W * 0.5 + 0.9, H * 0.3 - i * 1.0, 0.2); dev.add(d); addLabel(d, E(txt), 'chip', 0); });
    ticks.push((t, lt) => { dev.rotation.y = Math.sin(t * 0.6) * 0.35; dev.rotation.x = -0.08 + Math.sin(t * 0.4) * 0.05; dev.position.y = 2.1 + Math.sin(t * 1.2) * 0.06; });
  },
  // 카드 회전목마: [머리말, 본문, 색]
  cards(o, g) {
    const n = o.items.length, R = o.radius || 3.1, ring = new THREE.Group(); ring.position.set(0, 1.6, -1.6); g.add(ring);
    o.items.forEach(([head, body, c = COL.dawn], i) => {
      const tex = canvasTex(520, 360, (x, w, h) => {
        x.fillStyle = 'rgba(255,255,255,.96)'; rrect(x, 0, 0, w, h, 28); x.fill();
        x.fillStyle = c; x.fillRect(0, 0, 14, h);
        x.fillStyle = '#141a2e'; x.font = `800 38px ${FONT}`; wrapText(x, head, 44, 76, w - 80, 46);
        x.fillStyle = '#5e667d'; x.font = `500 26px ${FONT}`; wrapText(x, body, 44, 176, w - 80, 36);
      });
      const card = new THREE.Mesh(new THREE.PlaneGeometry(2.3, 1.6), new THREE.MeshBasicMaterial({ map: tex, transparent: true, side: THREE.DoubleSide }));
      const a = i / n * Math.PI * 2; card.position.set(Math.sin(a) * R, 0, Math.cos(a) * R); card.rotation.y = a; ring.add(card);
      card.userData.tip = `<b>${E(head)}</b><br>${E(body)}`; hits.push(card);
    });
    ticks.push(t => { ring.rotation.y = -t * (o.speed || 0.35); });
  },
  // 막대 대시보드: [이름, 높이, 색, 설명]
  bars(o, g) {
    const n = o.items.length, cols = Math.min(n, 4);
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(9, 5.5), new THREE.MeshBasicMaterial({ color: '#0f1430', transparent: true, opacity: 0.7 })); floor.rotation.x = -Math.PI / 2; g.add(floor);
    o.items.forEach(([name, h, c = COL.mint, note = ''], i) => {
      const x = ((i % cols) - (cols - 1) / 2) * 2.1, z = (Math.floor(i / cols) - (Math.ceil(n / cols) - 1) / 2) * 2.2;
      const bar = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1, 0.9), std(c, { emissive: c, emissiveIntensity: 0.25, transparent: true, opacity: 0.92 }));
      bar.position.set(x, 0, z); g.add(bar);
      const top = new THREE.Object3D(); g.add(top);
      addLabel(top, `<b>${E(name)}</b>${note ? `<span>${E(note)}</span>` : ''}`, 'bar', 0.2);
      bar.userData.tip = `<b>${E(name)}</b>${note ? `<br>${E(note)}` : ''}`; hits.push(bar);
      ticks.push((t, lt) => { const k = easeOutBack(clamp01(lt * 2.2 - i * 0.08)); const hh = Math.max(0.05, h * k); bar.scale.y = hh; bar.position.y = hh / 2; top.position.set(x, hh, z); });
    });
  },
  // 경로: 정류장 [이름, 설명] · 움직이는 사람
  route(o, g) {
    const n = o.stops.length, pts = o.stops.map((_, i) => new THREE.Vector3((i / (n - 1) - 0.5) * 9, 0.15, Math.sin(i * 1.3) * 1.8));
    const curve = new THREE.CatmullRomCurve3(pts);
    g.add(new THREE.Mesh(new THREE.TubeGeometry(curve, 200, 0.06, 10), std(COL.white, { emissive: COL.sky, emissiveIntensity: 0.6 })));
    const dots = pts.map((p, i) => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.2, 20, 20), std('#8a93b8')); m.position.copy(p); g.add(m); addLabel(m, `<b>${E(o.stops[i][0])}</b>${o.stops[i][1] ? `<span>${E(o.stops[i][1])}</span>` : ''}`, 'stop', 0.35); m.userData.tip = `<b>${E(o.stops[i][0])}</b><br>${E(o.stops[i][1] || '')}`; hits.push(m); return m; });
    const walker = new THREE.Mesh(new THREE.CapsuleGeometry(0.14, 0.3, 4, 10), std(COL.dawn, { emissive: COL.dawn, emissiveIntensity: 0.5 })); g.add(walker);
    ticks.push((t, lt) => {
      const u = clamp01(lt * 1.1); walker.position.copy(curve.getPointAt(u)); walker.position.y += 0.3 + Math.abs(Math.sin(t * 6)) * 0.08;
      dots.forEach((d, i) => { const on = u >= i / (n - 1) - 0.01; d.material.color.set(on ? COL.mint : '#8a93b8'); d.scale.setScalar(on ? 1.25 : 1); });
    });
  },
  // Keep121 문 마크
  arch(o, g) {
    const path = new THREE.CurvePath(), l = new THREE.Vector3(-1.6, 0, 0), r = new THREE.Vector3(1.6, 0, 0);
    path.add(new THREE.LineCurve3(new THREE.Vector3(-1.6, -1.8, 0), l));
    path.add(new THREE.CubicBezierCurve3(l, new THREE.Vector3(-1.6, 2.15, 0), new THREE.Vector3(1.6, 2.15, 0), r));
    path.add(new THREE.LineCurve3(r, new THREE.Vector3(1.6, -1.8, 0)));
    const arch = new THREE.Group(); arch.position.y = 2; g.add(arch);
    arch.add(new THREE.Mesh(new THREE.TubeGeometry(path, 160, 0.26, 20), new THREE.MeshPhysicalMaterial({ color: '#ffffff', roughness: 0.2, clearcoat: 1, emissive: '#5b6fd6', emissiveIntensity: 0.25 })));
    const dot = new THREE.Mesh(new THREE.SphereGeometry(0.42, 32, 32), std(COL.dawn, { emissive: COL.dawn, emissiveIntensity: 0.7 })); dot.position.y = -0.6; arch.add(dot);
    const motes = new THREE.Group(); arch.add(motes);
    for (let i = 0; i < 60; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(0.04, 8, 8), glow(i % 4 ? COL.white : COL.dawn)); m.userData.a = Math.random() * Math.PI * 2; m.userData.r = 2.6 + Math.random() * 1.6; m.userData.y = (Math.random() - 0.5) * 4; motes.add(m); }
    dot.userData.tip = '<b>Every one, kept.</b><br>한 사람도 빠짐없이'; hits.push(dot);
    ticks.push((t, lt) => {
      arch.rotation.y = Math.sin(t * 0.5) * 0.5; dot.scale.setScalar(1 + Math.sin(t * 3) * 0.08);
      motes.children.forEach((m, i) => { const a = m.userData.a + t * 0.3, rr = m.userData.r * (1 - easeOutBack(clamp01(lt * 1.4)) * 0.55); m.position.set(Math.cos(a) * rr, m.userData.y * (1 - clamp01(lt)), Math.sin(a) * rr); });
    });
  }
};

// ── 장면 교체 ────────────────────────────────────────────────
const disposeContent = () => {
  labels.forEach(L => L.el.remove()); labels = []; ticks = []; hits = [];
  if (!content) return;
  const old = content; content = null;
  const t0 = performance.now();
  const fade = () => { const k = clamp01((performance.now() - t0) / 350); old.scale.setScalar(1 - k); if (k < 1) requestAnimationFrame(fade); else { stage.remove(old); old.traverse(o => { o.geometry && o.geometry.dispose(); }); } };
  fade();
};
let built = 0;
const build = s => {
  disposeContent();
  content = new THREE.Group(); content.scale.setScalar(0.001); stage.add(content); built = performance.now();
  (B[s.obj.type] || (() => {}))(s.obj, content);
};

// 배경 사진: 두 레이어를 번갈아 교체 (천천히 확대)
const bgl = [$('#bg .a'), $('#bg .b')]; let bgi = 0;
const setBg = (url, pos) => {
  const el = bgl[bgi = 1 - bgi], other = bgl[1 - bgi];
  el.style.backgroundImage = `url("${url}")`; el.style.backgroundPosition = pos || 'center';
  el.classList.remove('on'); void el.offsetWidth; el.classList.add('on'); other.classList.remove('on');
};

// ── 데이터 · 자막 ─────────────────────────────────────────────
const D = await fetch(document.body.dataset.src, { cache: 'no-cache' }).then(r => r.json());
const S = D.scenes; let acc = 0; S.forEach(s => { s.t0 = acc; acc += s.dur; }); const TOTAL = acc;
const IMG = D.img || {};
S.forEach(s => { const u = IMG[s.bg] || s.bg; if (u) { const im = new Image(); im.src = u; } });            // 미리 받기
$('#dots').innerHTML = S.map((s, i) => `<button data-i="${i}" aria-label="${E(s.k)}"><i></i></button>`).join('');
const cap = $('#cap');
const showCaption = s => {
  cap.classList.remove('on');
  setTimeout(() => {
    cap.innerHTML = `<p class="k">${E(s.k)}</p><h2>${s.title}</h2>${s.sub ? `<p class="sub">${E(s.sub)}</p>` : ''}
      ${s.stats ? `<div class="stats">${s.stats.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div>` : ''}
      ${s.hint ? `<p class="hint">👆 ${E(s.hint)}</p>` : ''}
      ${s.cta ? `<div class="cta">${s.cta.map(([t, h], i) => `<a class="${i ? 'ghost' : ''}" href="${E(h)}">${E(t)}</a>`).join('')}</div>` : ''}`;
    cap.className = 'cap on';
  }, 250);
};
const toastEl = $('#toast'); let toastT = 0;
const toast = msg => { toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove('on'), 2600); };

// ── 상호작용: 끌어서 돌리기 · 호버 설명 · 클릭 ─────────────────────
const ray = new THREE.Raycaster(), ptr = new THREE.Vector2(); const tip = $('#tip');
let drag = null, yaw = 0, yawV = 0, tilt = 0, par = { x: 0, y: 0 };
const pick = e => { ptr.set(e.clientX / innerWidth * 2 - 1, -(e.clientY / innerHeight) * 2 + 1); ray.setFromCamera(ptr, camera); const h = ray.intersectObjects(hits, false)[0]; return h && h.object; };
canvas.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY, moved: 0 }; canvas.setPointerCapture(e.pointerId); });
canvas.addEventListener('pointermove', e => {
  par = { x: e.clientX / innerWidth - 0.5, y: e.clientY / innerHeight - 0.5 };
  if (drag) { const dx = e.clientX - drag.x; drag.moved += Math.abs(dx) + Math.abs(e.clientY - drag.y); yawV = dx * 0.005; yaw += dx * 0.008; tilt = Math.max(-0.35, Math.min(0.35, tilt + (e.clientY - drag.y) * 0.003)); drag.x = e.clientX; drag.y = e.clientY; tip.classList.remove('on'); return; }
  const o = pick(e);
  if (o && o.userData.tip) { tip.innerHTML = o.userData.tip; tip.style.transform = `translate(${e.clientX + 14}px,${e.clientY + 14}px)`; tip.classList.add('on'); canvas.style.cursor = o.userData.onClick ? 'pointer' : 'grab'; }
  else { tip.classList.remove('on'); canvas.style.cursor = 'grab'; }
});
canvas.addEventListener('pointerup', e => { if (drag && drag.moved < 6) { const o = pick(e); if (o && o.userData.onClick) o.userData.onClick(); else if (o && o.userData.tip) { tip.innerHTML = o.userData.tip; tip.style.transform = `translate(${Math.min(e.clientX, innerWidth - 240)}px,${e.clientY + 14}px)`; tip.classList.add('on'); } } drag = null; });
addEventListener('deviceorientation', e => { if (e.gamma != null) par = { x: e.gamma / 90, y: (e.beta - 45) / 90 }; });

// ── 소리 · 재생 제어 ───────────────────────────────────────────
const Sound = createSound();
const q = new URLSearchParams(location.search);
let t = Math.min(TOTAL - 0.01, parseFloat(q.get('t')) || 0), playing = false, cur = -1, last = performance.now();
const setPlaying = p => { if (p === playing) return; playing = p; Sound.pause(!p); };
const restartScene = () => { cur = -1; Sound.stopVoice(); };
const seek = i => { t = S[Math.max(0, Math.min(S.length - 1, i))].t0 + 0.01; restartScene(); };
$('#dots').addEventListener('click', e => { const b = e.target.closest('button'); if (b) seek(+b.dataset.i); });
$('#play').addEventListener('click', () => { if (t >= TOTAL - 0.02) { t = 0; restartScene(); } setPlaying(!playing); });
$('#replay').addEventListener('click', () => { t = 0; restartScene(); if (Sound.on) Sound.start(); setPlaying(true); });
$('#mute').addEventListener('click', () => { Sound.toggle(); if (Sound.on) restartScene(); });
addEventListener('keydown', e => { if (e.key === ' ') { e.preventDefault(); setPlaying(!playing); } else if (e.key === 'ArrowRight') seek(cur + 1); else if (e.key === 'ArrowLeft') seek(cur - 1); });
const gate = $('#gate');
const go = withSound => { gate.hidden = true; document.body.classList.remove('gating'); if (withSound) Sound.start(); restartScene(); setPlaying(true); };
if (q.has('t') || q.has('pause')) { gate.hidden = true; playing = !q.has('pause'); }
else { document.body.classList.add('gating'); $('#go-sound').addEventListener('click', () => go(true)); $('#go-mute').addEventListener('click', () => go(false)); }

let wide = true;
const resize = () => { const w = innerWidth, h = innerHeight; wide = w > h * 1.1 && w > 820; renderer.setSize(w, h, false); camera.aspect = w / h; camera.fov = w < h ? 64 : 42; camera.updateProjectionMatrix(); stage.position.set(wide ? 3.3 : 0, wide ? 0 : 1.6, wide ? -0.5 : 0); stage.scale.setScalar(wide ? 1 : 0.74); };
addEventListener('resize', resize); resize();
const bgWrap = $('#bg');

const frame = now => {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (playing) t = Math.min(TOTAL, t + dt);
  if (t >= TOTAL && playing) { playing = false; Sound.end(); }
  const i = Math.max(0, S.findIndex((s, k) => t >= s.t0 && (k === S.length - 1 || t < S[k + 1].t0)));
  const s = S[i], lt = (t - s.t0) / s.dur;
  if (i !== cur) {
    cur = i; showCaption(s); build(s); setBg(IMG[s.bg] || s.bg, IMG[s.bg + '@pos']);
    document.querySelectorAll('#dots button').forEach((b, k) => b.classList.toggle('on', k === i));
    if (playing) Sound.scene(s, i, i === S.length - 1);
  }
  if (content) content.scale.setScalar(Math.max(0.001, easeOutBack(clamp01((now - built) / 900))));
  ticks.forEach(f => f(now / 1000, lt));
  if (!drag) { yaw += yawV; yawV *= 0.94; yaw *= 0.995; tilt *= 0.97; }
  stage.rotation.y = yaw + Math.sin(now / 4000) * 0.12; stage.rotation.x = tilt;
  camera.position.x += (par.x * 1.2 - camera.position.x) * 0.04; camera.position.y += (3.2 - par.y * 0.8 - camera.position.y) * 0.04; camera.position.z = innerWidth < innerHeight ? 12.5 : 12; camera.lookAt(wide ? 1.6 : 0, 1.3, 0);
  bgWrap.style.transform = `translate(${-par.x * 18}px,${-par.y * 12}px)`;
  placeLabels();
  $('#bar').style.width = `${t / TOTAL * 100}%`; $('#time').textContent = `${Math.floor(t)}s / ${TOTAL}s`;
  $('#play').textContent = playing ? '❚❚' : '▶'; $('#mute').textContent = Sound.on ? '🔊' : '🔇';
  document.body.classList.toggle('ended', t >= TOTAL);
  renderer.render(scene, camera);
  requestAnimationFrame(frame);
};
requestAnimationFrame(frame);
