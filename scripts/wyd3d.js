/* 1분 3D 제안 엔진 (원본: scripts/wyd3d.js)
   <body data-src="data/xxx_3d.json"> 의 장면 목록을 받아 60초 동안 자동 재생한다. (WYD 서울 2027 · 제주 공용)
   하나의 입자 무리(순례자 4,000명)가 장면마다 다른 모양으로 모인다.
   조작: 스페이스 재생/정지 · ←/→ 장면 이동 · ?t=초 로 특정 시점 열기 */
import * as THREE from 'three';

const E = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const $ = s => document.querySelector(s);
const N = 4000;
const C = { indigo: new THREE.Color('#8fa0ff'), dawn: new THREE.Color('#F2A541'), mint: new THREE.Color('#5fd3a1'), red: new THREE.Color('#ff5a5a'), white: new THREE.Color('#e8ecff'), dim: new THREE.Color('#3a4a8c') };

// ── 장면별 입자 배치 ─────────────────────────────────────────
const rnd = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
const R = Array.from({ length: N * 3 }, rnd);            // 고정 난수 (장면이 매번 같게)
const LOST = 17;                                         // 길을 잃는 한 사람
const layouts = {
  globe(i) {                                             // 지구 위 순례자 → 서울로
    const u = R[i * 3], v = R[i * 3 + 1], th = 2 * Math.PI * u, ph = Math.acos(2 * v - 1), r = 6;
    return [r * Math.sin(ph) * Math.cos(th), r * Math.cos(ph), r * Math.sin(ph) * Math.sin(th)];
  },
  days(i) {                                              // 8.3 ~ 8.8, 6개의 기둥
    const k = i % 6, h = R[i * 3] * (4 + k * 0.9), a = R[i * 3 + 1] * Math.PI * 2, r = R[i * 3 + 2] * 0.55;
    return [(k - 2.5) * 2.2 + Math.cos(a) * r, h - 3.5, Math.sin(a) * r];
  },
  crowd(i) {                                             // 큰 인파, 한 사람이 떨어져 나감
    if (i === LOST) return [7.5, 0.2, 3.5];
    const a = R[i * 3] * Math.PI * 2, r = Math.sqrt(R[i * 3 + 1]) * 6.2;
    return [Math.cos(a) * r, (R[i * 3 + 2] - 0.5) * 0.25, Math.sin(a) * r];
  },
  groups(i) {                                            // 32명씩 그룹 · 인솔자 중심
    const g = Math.floor(i / 32), gx = g % 12, gz = Math.floor(g / 12);
    const a = (i % 32) / 32 * Math.PI * 2, r = 0.25 + R[i * 3] * 0.35;
    return [(gx - 5.5) * 1.15 + Math.cos(a) * r, (R[i * 3 + 1] - 0.5) * 0.15, (gz - 5) * 1.15 + Math.sin(a) * r];
  },
  layers(i) {                                            // 순례자 → 인솔자 → 상황실, 세 층
    const k = i < N * 0.6 ? 0 : i < N * 0.9 ? 1 : 2, w = [8, 6, 4][k];
    return [(R[i * 3] - 0.5) * w * 1.6, [-2.6, 0, 2.6][k] + (R[i * 3 + 2] - 0.5) * 0.08, (R[i * 3 + 1] - 0.5) * w];
  },
  route(i) {                                             // 7일의 길: 입국 → 귀국
    const t = (i % 700) / 700, lane = Math.floor(i / 700);
    const x = (t - 0.5) * 16, z = Math.sin(t * Math.PI * 2) * 2.4 + (lane - 2.5) * 0.18;
    return [x, Math.sin(t * Math.PI * 4) * 0.4 + (R[i * 3] - 0.5) * 0.2, z + (R[i * 3 + 1] - 0.5) * 0.25];
  },
  dash(i) {                                              // 상황실: 구역별 밀집도 막대
    const cell = i % 64, cx = cell % 8, cz = Math.floor(cell / 8);
    const hgt = [0.6, 1.4, 3.8, 2.2, 1, 4.6, 0.8, 2.8][(cx * 3 + cz * 5) % 8];
    return [(cx - 3.5) * 1.3 + (R[i * 3] - 0.5) * 0.6, R[i * 3 + 1] * hgt - 2.5, (cz - 3.5) * 1.3 + (R[i * 3 + 2] - 0.5) * 0.6];
  },
  island(i) {                                            // 제주: 타원형 섬과 한라산
    const a = R[i * 3] * Math.PI * 2, r = Math.sqrt(R[i * 3 + 1]);
    const x = Math.cos(a) * r * 7.2, z = Math.sin(a) * r * 3.4;
    return [x, Math.max(0, 2.6 * (1 - r * 1.25)) - 0.4 + (R[i * 3 + 2] - 0.5) * 0.15, z];
  },
  split(i) {                                             // 두 고객: 왼쪽 중국인 단체 · 오른쪽 수학여행
    const left = i % 2 === 0, a = R[i * 3] * Math.PI * 2, r = Math.sqrt(R[i * 3 + 1]) * 3;
    return [(left ? -4.2 : 4.2) + Math.cos(a) * r, (R[i * 3 + 2] - 0.5) * 0.3, Math.sin(a) * r];
  },
  arch(i) {                                              // Keep121 문 마크 + 안의 점
    if (i < 520) { const a = R[i * 3] * Math.PI * 2, r = Math.sqrt(R[i * 3 + 1]) * 0.75; return [Math.cos(a) * r, -1.1 + Math.sin(a) * r, (R[i * 3 + 2] - 0.5) * 0.4]; }
    const t = R[i * 3], w = (R[i * 3 + 1] - 0.5) * 0.9, d = (R[i * 3 + 2] - 0.5) * 0.5;
    let x, y;
    if (t < 0.3) { x = -2.6 + w; y = -3.6 + (t / 0.3) * 3.6; }
    else if (t < 0.7) { const a = Math.PI * (1 - (t - 0.3) / 0.4); x = Math.cos(a) * (2.6 - w); y = Math.sin(a) * (2.6 - w); }
    else { x = 2.6 + w; y = -3.6 + ((1 - t) / 0.3) * 3.6; }
    return [x, y + 0.6, d];
  }
};
const colorFor = {
  globe: i => (i % 9 === 0 ? C.dawn : C.indigo), days: i => (i % 6 === 2 ? C.dawn : C.indigo),
  crowd: i => (i === LOST ? C.red : C.dim), groups: i => (i % 32 === 0 ? C.dawn : C.mint),
  layers: i => (i < N * 0.6 ? C.indigo : i < N * 0.9 ? C.mint : C.dawn), route: i => (i % 7 === 0 ? C.dawn : C.indigo),
  island: i => (i % 11 === 0 ? C.dawn : i % 3 === 0 ? C.mint : C.indigo), split: i => (i % 2 === 0 ? C.red : C.mint),
  dash: i => ([2, 5].includes(((i % 64) % 8 * 3 + Math.floor((i % 64) / 8) * 5) % 8) ? C.red : C.mint), arch: i => (i < 520 ? C.dawn : C.white)
};

// ── 렌더러 ─────────────────────────────────────────────────
const canvas = $('#scene');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0b0f24');
scene.fog = new THREE.FogExp2('#0b0f24', 0.035);
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 200);

const geo = new THREE.BufferGeometry();
const pos = new Float32Array(N * 3), col = new Float32Array(N * 3);
geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
const dot = (() => { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); const r = g.createRadialGradient(32, 32, 0, 32, 32, 32); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.35, 'rgba(255,255,255,.85)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();
const mat = new THREE.PointsMaterial({ size: 0.16, map: dot, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending });
scene.add(new THREE.Points(geo, mat));

// 바닥 격자 · 태그 신호(ring) · 서울 표시
const grid = new THREE.GridHelper(40, 40, '#24306b', '#18204a'); grid.position.y = -3.8; scene.add(grid);
const rings = Array.from({ length: 14 }, () => {
  const m = new THREE.Mesh(new THREE.RingGeometry(0.92, 1, 48), new THREE.MeshBasicMaterial({ color: '#F2A541', transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; scene.add(m); return m;
});
const seoul = new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 24), new THREE.MeshBasicMaterial({ color: '#F2A541' }));
scene.add(seoul);
const lostMark = new THREE.Mesh(new THREE.SphereGeometry(0.16, 20, 20), new THREE.MeshBasicMaterial({ color: '#ff5a5a' }));   // 길을 잃은 한 사람
scene.add(lostMark);

// ── 데이터 · 타임라인 ─────────────────────────────────────────
const D = await fetch(document.body.dataset.src || 'data/wyd2027_3d.json', { cache: 'no-cache' }).then(r => r.json());
const S = D.scenes;
let acc = 0; S.forEach(s => { s.t0 = acc; acc += s.dur; });
const TOTAL = acc;
const targets = {};
for (const s of S) if (!targets[s.layout]) {
  const p = new Float32Array(N * 3), c = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) { p.set(layouts[s.layout](i), i * 3); const k = colorFor[s.layout](i); c.set([k.r, k.g, k.b], i * 3); }
  targets[s.layout] = { p, c };
}
pos.set(targets[S[0].layout].p); col.set(targets[S[0].layout].c);

$('#title').textContent = D.title;
$('#dots').innerHTML = S.map((s, i) => `<button data-i="${i}" aria-label="${E(s.k)}"><i></i></button>`).join('');
const cap = $('#cap');
const showCaption = s => {
  cap.classList.remove('on');
  setTimeout(() => {
    cap.innerHTML = `<p class="k">${E(s.k)}</p><h2>${s.title}</h2>${s.sub ? `<p class="sub">${E(s.sub)}</p>` : ''}
      ${s.stats ? `<div class="stats">${s.stats.map(([v, l]) => `<div><b data-n="${E(v)}">${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div>` : ''}
      ${s.cta ? `<div class="cta">${s.cta.map(([t, h], i) => `<a class="${i ? 'ghost' : ''}" href="${E(h)}">${E(t)}</a>`).join('')}</div>` : ''}`;
    cap.className = `cap on ${s.align || ''}`;
  }, 250);
};

// ── 재생 제어 ───────────────────────────────────────────────
const q = new URLSearchParams(location.search);
let t = Math.min(TOTAL - 0.01, parseFloat(q.get('t')) || 0), playing = !q.has('pause'), cur = -1, last = performance.now();
const seek = i => { t = S[Math.max(0, Math.min(S.length - 1, i))].t0 + 0.01; };
$('#dots').addEventListener('click', e => { const b = e.target.closest('button'); if (b) seek(+b.dataset.i); });
$('#play').addEventListener('click', () => { if (t >= TOTAL - 0.02) t = 0; playing = !playing; });
$('#replay').addEventListener('click', () => { t = 0; playing = true; });
addEventListener('keydown', e => {
  if (e.key === ' ') { e.preventDefault(); playing = !playing; }
  else if (e.key === 'ArrowRight') seek(cur + 1); else if (e.key === 'ArrowLeft') seek(cur - 1);
});
const resize = () => { const w = innerWidth, h = innerHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.fov = w < h ? 62 : 45; camera.updateProjectionMatrix(); };
addEventListener('resize', resize); resize();

const ease = x => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const tmpA = new THREE.Vector3(), tmpB = new THREE.Vector3();
const frame = now => {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (playing) t = Math.min(TOTAL, t + dt);
  if (t >= TOTAL) playing = false;
  const i = Math.max(0, S.findIndex((s, k) => t >= s.t0 && (k === S.length - 1 || t < S[k + 1].t0)));
  const s = S[i], local = (t - s.t0) / s.dur;
  if (i !== cur) { cur = i; showCaption(s); document.querySelectorAll('#dots button').forEach((b, k) => b.classList.toggle('on', k === i)); }

  // 입자: 목표 배치로 부드럽게 이동 (장면 시작 1.6초 동안)
  const tg = targets[s.layout], k = Math.min(1, dt * 3.2);
  for (let j = 0; j < N * 3; j++) { pos[j] += (tg.p[j] - pos[j]) * k; col[j] += (tg.c[j] - col[j]) * k; }
  if (s.layout === 'crowd') { pos[LOST * 3] = 2 + local * 6; pos[LOST * 3 + 2] = 1 + local * 3; }      // 한 사람이 멀어진다
  if (s.layout === 'globe') {                                                                           // 순례자가 서울로
    const pull = ease(Math.min(1, local * 1.2));
    for (let j = 0; j < N; j += 4) { pos[j * 3] *= 1 - pull * 0.02; pos[j * 3 + 1] = pos[j * 3 + 1] * (1 - pull * 0.02) + 2.6 * pull * 0.02; pos[j * 3 + 2] = pos[j * 3 + 2] * (1 - pull * 0.02) + 5.4 * pull * 0.02; }
  }
  geo.attributes.position.needsUpdate = true; geo.attributes.color.needsUpdate = true;

  // 카메라 경로
  const cam = s.cam, nxt = (S[i + 1] || s).cam, m = ease(Math.max(0, (local - 0.75) / 0.25));
  tmpA.set(...cam.p).lerp(tmpB.set(...nxt.p), m);
  const orbit = now / 1000 * (s.orbit || 0);
  camera.position.set(tmpA.x * Math.cos(orbit) - tmpA.z * Math.sin(orbit), tmpA.y, tmpA.x * Math.sin(orbit) + tmpA.z * Math.cos(orbit));
  camera.lookAt(0, cam.look || 0, 0);

  // 태그 신호 · 서울 표시
  const pings = s.pings || 0;
  rings.forEach((r, n) => {
    if (n >= pings) { r.material.opacity = 0; return; }
    const ph = ((now / 1000) * 0.6 + n / pings) % 1;
    const g = n * 7 % 144, gx = g % 12, gz = Math.floor(g / 12);
    const at = s.layout === 'crowd' ? [pos[LOST * 3], pos[LOST * 3 + 1], pos[LOST * 3 + 2]] : [(gx - 5.5) * 1.15, -0.05, (gz - 5) * 1.15];
    r.position.set(at[0], at[1], at[2]); r.scale.setScalar(0.2 + ph * (s.layout === 'crowd' ? 2.2 : 1.1));
    r.material.color.set(s.layout === 'crowd' ? '#ff5a5a' : '#F2A541'); r.material.opacity = (1 - ph) * 0.9;
  });
  const mk = s.marker || (s.layout === 'globe' ? [0, 2.6, 5.4] : null);
  seoul.visible = !!mk; if (mk) seoul.position.set(mk[0], mk[1], mk[2]); seoul.scale.setScalar(1 + Math.sin(now / 200) * 0.25);
  grid.visible = !['globe', 'arch', 'island'].includes(s.layout);
  lostMark.visible = s.layout === 'crowd'; lostMark.position.set(pos[LOST * 3], pos[LOST * 3 + 1] + 0.1, pos[LOST * 3 + 2]); lostMark.scale.setScalar(1 + Math.sin(now / 150) * 0.3);

  $('#bar').style.width = `${t / TOTAL * 100}%`;
  $('#time').textContent = `${Math.floor(t)}s / ${TOTAL}s`;
  $('#play').textContent = playing ? '❚❚' : '▶';
  document.body.classList.toggle('ended', t >= TOTAL);
  renderer.render(scene, camera);
  requestAnimationFrame(frame);
};
requestAnimationFrame(frame);
