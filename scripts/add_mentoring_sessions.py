"""모두의 창업 페이지에 '멘토링 회차 기록'을 붙이고 갱신한다. 다시 돌려도 안전.

    python scripts/add_mentoring_sessions.py

- content/modoo/sessions/NN.json  회차별 기록 원천 (새 회차는 파일만 추가) → data/modoo.json 의 sessions
- content/pages/modoo.html        #sessions 섹션 · 이 페이지 목차 링크
- assets/js/modoo.js              R.sessions 렌더러
- assets/css/style.css            scripts/modoo_sessions.css 덧붙임
- data/modoo.json                 1회차 결과 반영 (멘토링·일정·지금 할 일·작성 단계·로그)
"""
import datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

# 1) 데이터
m = json.loads(rd("data/modoo.json"))
m["sessions"] = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "content/modoo/sessions").glob("*.json"))]
m["sessions"].sort(key=lambda s: s["n"])
r = next(r for r in m["mentoring"] if r["n"] == 1)
r.update(date="10/29(목) 15:00", result="사업계획서 v2.0 검토 — 실제 고객 인터뷰, 문제 정의 5개, SOM 3년 3%·5년 5% 재산정. 아래 1회차 기록 참고.")
s = next(r for r in m["schedule"] if r["when"].startswith("10/29"))
s.update(status="done", label="완료", note="사업계획서 v2.0 검토 · 기록 아래")
for r in m["schedule"]:
    if r["when"].startswith("10/20~11/30"):
        r["label"] = "1회차 완료"
m["now"] = [c for c in m["now"] if not c["title"].startswith(("멘토링 1회차", "타겟 고객 인터뷰"))]
m["now"].insert(0, {"title": "타겟 고객 인터뷰 · 11월 2~3주", "facts": [["대상", "여행사 MD · 인솔자 · 랜드사 가이드 · 시니어·가족"], ["근거", "멘토링 1회차 피드백"]],
                    "text": "사업계획서 v2.0의 가정값 인터뷰를 실제 인터뷰로 바꿉니다. 문제 정의 5개와 SOM 재산정도 함께 반영해 v2.1을 만듭니다."})
p = next(r for r in m["planSteps"] if r["step"].startswith("아이디어 진단"))
p.update(status="due", basis="사업계획서 v2.0(10/29) + 멘토링 1회차 피드백")
if not any(r["date"] == "2026-10-29" and r["kind"] == "멘토링" for r in m["log"]):
    m["log"].insert(0, {"date": "2026-10-29", "kind": "멘토링", "title": "멘토링 1회차 · 사업계획서 v2.0 검토",
                        "text": "이광일 멘토와 PSST 사업계획서 v2.0 검토. 분기별 계획·예산, 실제 타겟 고객 인터뷰, 문제 정의 5개, SOM 3년 3%·5년 5% 기준 재산정을 보완하기로 함."})
    m["log"].insert(1, {"date": "2026-10-29", "kind": "사업계획서", "title": "사업계획서 v2.0 (PSST) 작성",
                        "text": "합격 사업계획서 기반 PSST 작성 프롬프트로 v1.1을 예비창업패키지 발표 구조로 재구성한 28쪽 v2.0 작성."})
m["log"].sort(key=lambda r: r["date"], reverse=True)
m["updated"] = dt.date.today().isoformat()
wr("data/modoo.json", json.dumps(m, ensure_ascii=False, indent=1) + "\n")
print(f"  data/modoo.json  (회차 기록 {len(m['sessions'])}건)")

# 2) 페이지 섹션
P = "content/pages/modoo.html"
h = rd(P)
if 'id="sessions"' not in h:
    sec = """<!-- ============ MENTORING SESSIONS ============ -->
<section class="soft" id="sessions">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Mentoring Notes</span>
      <h2>멘토링 회차별 기록.</h2>
      <p>회차마다 검토한 자료, 멘토 피드백, 사업계획서에 반영할 것과 후속 과제를 남깁니다.</p>
    </div>
    <div data-modoo="sessions"></div>
  </div>
</section>

<!-- ============ FUNDS ============ -->"""
    h = h.replace("<!-- ============ FUNDS ============ -->", sec, 1) if "<!-- ============ FUNDS ============ -->" in h else h.replace('<section id="funds">', sec.rsplit("\n", 1)[0] + '\n<section id="funds">', 1)
    h = h.replace('<a href="#mentoring">멘토링</a>', '<a href="#mentoring">멘토링</a>\n      <a href="#sessions">회차 기록</a>', 1)
    wr(P, h)
    print(f"  {P}")

# 3) 렌더러
J = "assets/js/modoo.js"
js = rd(J)
if "sessions:" not in js:
    fn = r"""    sessions: m => (m.sessions || []).map(s => `<article class="ses reveal" id="session-${s.n}">
<div class="ses-top"><div><span class="ses-badge">${s.n}회차 · ${E(s.kind)}</span><h3>${E(s.title)}</h3><p>${E(s.summary)}</p></div>
<dl class="ses-facts">${s.facts.map(([k, v]) => `<div><dt>${E(k)}</dt><dd>${E(v)}</dd></div>`).join('')}</dl></div>
${s.process ? `<h4>진행 과정</h4><ol class="ses-flow">${s.process.map(([t, p]) => `<li><b>${E(t)}</b><p>${E(p)}</p></li>`).join('')}</ol>` : ''}
<h4>멘토 피드백 ${s.feedback.length}가지</h4><div class="ses-fb">${s.feedback.map((f, i) => `<article><div class="t"><span>${i + 1}</span><em>${E(f.tag)}</em></div><b>${E(f.title)}</b><blockquote>${E(f.body)}</blockquote><p><strong>→ 반영</strong> ${E(f.apply)}</p></article>`).join('')}</div>
${s.gaps ? `<h4>사업계획서에서 바꿀 것</h4><div class="spec-table-wrap"><table class="spec-table"><thead><tr><th scope="col">항목</th><th scope="col">지금 (v2.0)</th><th scope="col">멘토링 후</th></tr></thead><tbody>${s.gaps.map(([a, b, c]) => `<tr><th scope="row">${E(a)}</th><td class="was">${E(b)}</td><td class="to">${E(c)}</td></tr>`).join('')}</tbody></table></div>` : ''}
${s.actions ? `<h4>후속 과제</h4><div class="spec-table-wrap"><table class="spec-table"><thead><tr><th scope="col">과제</th><th scope="col">내용</th><th scope="col">목표 시점</th></tr></thead><tbody>${s.actions.map(([a, b, c]) => `<tr><th scope="row">${E(a)}</th><td>${E(b)}</td><td>${E(c)}</td></tr>`).join('')}</tbody></table></div>` : ''}
${s.prompt ? `<details><summary>검토 자료 ① ${E(s.prompt.title)} <small>구조 요약</small></summary><div class="ses-in"><p>${E(s.prompt.text)}</p><ul class="ses-struct">${s.prompt.structure.map(([n, t, p]) => `<li><span>${E(n)}</span><b>${E(t)}</b><p>${E(p)}</p></li>`).join('')}</ul>${s.prompt.caution ? `<p class="ses-note">${E(s.prompt.caution)}</p>` : ''}</div></details>` : ''}
${s.plan ? `<details><summary>검토 자료 ② ${E(s.plan.title)} <small>${E(s.plan.meta)}</small></summary><div class="ses-in"><p class="ses-head">${E(s.plan.headline)}</p><div class="ses-kpis">${s.plan.kpis.map(([v, l]) => `<div><b>${E(v)}</b><span>${E(l)}</span></div>`).join('')}</div><div class="ses-secs">${s.plan.sections.map(([t, items]) => `<section><h5>${E(t)}</h5><ul>${items.map(x => `<li>${E(x)}</li>`).join('')}</ul></section>`).join('')}</div>${s.plan.note ? `<p class="ses-note">${E(s.plan.note)}</p>` : ''}</div></details>` : ''}
</article>`).join(''),
"""
    js = js.replace("    log: m =>", fn + "    log: m =>", 1)
    js = js.replace("r.kind === '지출' ? 'chk' : 'meas'", "r.kind === '지출' ? 'chk' : r.kind === '사업계획서' ? 'plan' : 'meas'")
    wr(J, js)
    print(f"  {J}")

# 4) 스타일
C = "assets/css/style.css"
css = rd(C)
if "/* 모두의 창업 멘토링 회차 기록 */" not in css:
    wr(C, css.rstrip("\n") + "\n" + rd("scripts/modoo_sessions.css"))
    print(f"  {C}")
