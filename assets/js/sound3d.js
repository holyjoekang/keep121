/* 1분 3D 제안 공용 소리 모듈 (원본: scripts/sound3d.js)
   내레이션: 기기의 한국어 음성(speechSynthesis) · 배경음: Web Audio로 직접 합성 (외부 음원 없음) */
export const createSound = () => {
  let ctx = null, master, music, voice = null, on = false, chordNodes = [];
  const TTS = 'speechSynthesis' in window;
  const pickVoice = () => {
    if (!TTS) return null;
    const ko = speechSynthesis.getVoices().filter(v => /^ko/i.test(v.lang));
    const pref = [/google/i, /yuna|sora|heami|sunhi|injoon|seoyeon/i, /natural|neural|premium|enhanced/i];
    return pref.map(r => ko.find(v => r.test(v.name))).find(Boolean) || ko[0] || null;
  };
  if (TTS) speechSynthesis.onvoiceschanged = () => { voice = pickVoice(); };
  // D장조 진행 (장면마다 화음이 바뀐다) · 마지막 장면은 으뜸화음으로 마무리
  const CH = [[146.83, 220, 293.66, 369.99], [123.47, 185, 246.94, 293.66], [98, 196, 246.94, 293.66], [110, 220, 277.18, 329.63]];
  const DUCK = 0.35;
  const init = () => {
    if (ctx) return;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain(); master.gain.value = 0; master.connect(ctx.destination);
    music = ctx.createGain(); music.gain.value = 1;
    const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 900; lp.Q.value = 0.4;
    const verb = ctx.createDelay(1.2); verb.delayTime.value = 0.38; const fb = ctx.createGain(); fb.gain.value = 0.32;
    music.connect(lp); lp.connect(master); lp.connect(verb); verb.connect(fb); fb.connect(verb); verb.connect(master);
    master.gain.linearRampToValueAtTime(0.32, ctx.currentTime + 2.5);
  };
  const chord = idx => {
    if (!ctx) return;
    const now = ctx.currentTime, notes = CH[idx % CH.length];
    chordNodes.forEach(({ g, o }) => { g.gain.cancelScheduledValues(now); g.gain.setTargetAtTime(0, now, 0.6); o.forEach(x => x.stop(now + 3)); });
    chordNodes = notes.map((f, n) => {
      const g = ctx.createGain(); g.gain.value = 0; g.connect(music);
      const o = [-4, 4].map(det => { const x = ctx.createOscillator(); x.type = n === 0 ? 'sine' : 'triangle'; x.frequency.value = f; x.detune.value = det; x.connect(g); x.start(); return x; });
      g.gain.setTargetAtTime(n === 0 ? 0.16 : 0.07, now, 0.9);
      return { g, o };
    });
    // 장면 전환 종소리
    const b = ctx.createOscillator(), bg = ctx.createGain(); b.type = 'sine'; b.frequency.value = notes[3] * 2;
    bg.gain.setValueAtTime(0.0001, now); bg.gain.exponentialRampToValueAtTime(0.12, now + 0.02); bg.gain.exponentialRampToValueAtTime(0.0001, now + 2.2);
    b.connect(bg); bg.connect(master); b.start(now); b.stop(now + 2.4);
  };
  const say = (text, dur) => {
    if (!TTS || !text) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    voice = voice || pickVoice(); if (voice) u.voice = voice;
    u.lang = 'ko-KR'; u.pitch = 1;
    u.rate = Math.max(0.95, Math.min(1.3, text.replace(/\s/g, '').length / (dur * 0.85 * 5.2)));   // 장면 길이에 맞춤
    u.onstart = () => { if (music) music.gain.setTargetAtTime(DUCK, ctx.currentTime, 0.15); };       // 말할 때 음악을 낮춤
    u.onend = () => { if (music) music.gain.setTargetAtTime(1, ctx.currentTime, 0.4); };
    speechSynthesis.speak(u);
  };
  return {
    get on() { return on; }, hasVoice: () => TTS && !!(voice || pickVoice()),
    start() { init(); on = true; ctx.resume(); },
    toggle() { on = !on; if (!ctx) init(); if (on) { ctx.resume(); master.gain.setTargetAtTime(0.32, ctx.currentTime, 0.3); } else { master.gain.setTargetAtTime(0, ctx.currentTime, 0.2); if (TTS) speechSynthesis.cancel(); } },
    scene(s, i, last) { if (!on) return; chord(last ? 0 : i); say(s.say, s.dur); },
    pause(p) { if (!ctx || !on) return; if (p) { ctx.suspend(); if (TTS) speechSynthesis.pause(); } else { ctx.resume(); if (TTS) speechSynthesis.resume(); } },
    end() { if (!ctx) return; master.gain.setTargetAtTime(0, ctx.currentTime, 1.2); },
    stopVoice() { if (TTS) speechSynthesis.cancel(); }
  };
};
