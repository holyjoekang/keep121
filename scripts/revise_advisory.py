"""Rewrite company Advisory block (조부연·김종우·CTO + 추가 자문 계획) and drop CTO 모집 tile."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent.parent
page = ROOT / "content/pages/company.html"
css = ROOT / "assets/css/style.css"

TOPO = '<svg class="ad-topo" viewBox="0 0 260 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g fill="none" stroke="#B4BEF0" stroke-opacity=".22"><ellipse cx="200" cy="250" rx="60" ry="34"/><ellipse cx="200" cy="250" rx="100" ry="58"/><ellipse cx="200" cy="250" rx="145" ry="86"/><ellipse cx="200" cy="250" rx="195" ry="118"/><ellipse cx="200" cy="250" rx="250" ry="152"/></g></svg>'
ICON = lambda i: f'<svg class="icon"><use href="#{i}"/></svg>'

ADVISORS = [
  dict(mono="조", badge="자문교수", icon="i-school", org="제주대학교 경영대학", name="조부연", title="교수",
       role="Keep121 자문교수 · 관광 · 공공 시나리오",
       blocks=[("주요 자문", "공항 배포를 통한 미아 방지, 올레길 조난 대응 등 <b>제주 공공 시나리오</b>를 제안했습니다."),
               ("사업 반영", "지자체·관광공사 대상 <b>기관·공공 시장(2027 하반기~)</b> 진입 시나리오와 제주 실증 후보지 검토에 반영합니다.")],
       tags=["제주 공공 시나리오", "관광 안전", "지자체 실증"]),
  dict(mono="김", badge="자문교수", icon="i-school", org="고려대학교 기술경영전문대학원(MOT)", name="김종우", title="겸임교수",
       role="Keep121 자문교수 · 첨단전략산업 · 기술경영",
       blocks=[("학력 · 경력", "연세대 행정학 · 코넬대 MBA · 텍사스오스틴대 정책학 석사 · 서울과기대 정책학 박사<br><b>웰리시스(삼성 스핀오프) 공동창업자 · CSO</b> · <b>삼성SDS 신사업개발그룹장</b>"),
               ("자문 영역", "대기업 신사업·스핀오프 창업 경험을 바탕으로 <b>사업화 전략과 B2B 판매 구조</b>, 정부 R&amp;D·정책 과제 대응, 투자 유치 단계 설계를 검토합니다.")],
       tags=["기술경영", "신사업 · 스핀오프", "정책 · 정부과제"]),
  dict(mono="CTO", badge="합류 예정", icon="i-signal", org="Chief Technology Officer · 공동창업", name="CTO", title="합류 예정",
       role="삼성SDS 30년 경력 IT 전문가",
       blocks=[("경력", "<b>삼성SDS 30년</b> — 대규모 IT 시스템 설계·구축과 기업·공공 프로젝트 수행"),
               ("담당 영역", "Android 네이티브(BLE·NFC·Foreground Service), 서버·IoT 플랫폼 API 연동, <b>보안·로그 설계</b>를 총괄합니다. 펌웨어는 ODM 단계에서 외주·계약직으로 해결합니다.")],
       tags=["IT 시스템", "IoT 플랫폼", "보안 · 로그"]),
]

PLANNED = [  # (영역, 내용, 시점)
  ("i-shield", "위치정보 · 개인정보 법률", "전문 변호사 · 바우처 활용, 개인위치정보사업 신고·동의 설계", "운영 중"),
  ("i-globe", "여행업 실무", "현직 여행사 MD 1명 · 상품 기획과 가격 검토", "운영 중"),
  ("i-factory", "하드웨어 · ODM · 인증", "Keep Tag 양산, KC·전파인증, 수리·교체 공급망", "2027 확보"),
  ("i-school", "교육기관 · 현장체험학습", "학교·통학·돌봄기관 안전 지침과 조달 절차", "2027 확보"),
  ("i-shield", "정보보호 · 컴플라이언스", "ISMS-P 대비, 위치 로그 보관·파기 정책 점검", "2028 확보"),
  ("i-flag", "보험 · 배상책임", "여행자보험·영업배상 연계, 사고 대응 프로세스", "2028 확보"),
]

def card(i, a):
    mono_cls = "ad-mono sm" if len(a["mono"]) > 1 else "ad-mono"
    blocks = "".join(f'''          <div class="ad-contrib">
            <span class="k">{k}</span>
            <p>{v}</p>
          </div>
''' for k, v in a["blocks"])
    tags = "".join(f"<span>{t}</span>" for t in a["tags"])
    return f'''      <article class="advisor-card reveal d{i}">
        <div class="ad-visual">
          {TOPO}
          <span class="{mono_cls}">{a["mono"]}</span>
          <span class="ad-badge">{a["badge"]}</span>
        </div>
        <div class="ad-body">
          <div class="ad-org">{ICON(a["icon"])}{a["org"]}</div>
          <h4>{a["name"]} <small>{a["title"]}</small></h4>
          <div class="ad-role">{a["role"]}</div>
{blocks}          <div class="ad-foot">
            <div class="ad-tags">{tags}</div>
          </div>
        </div>
      </article>
'''

checks = [
  ("CTO 합류 예정", "삼성SDS 30년 경력 IT 전문가 · 기술 개발 총괄"),
  ("김종우 겸임교수", "고려대 MOT · 사업화 전략과 정책 과제"),
  ("조부연 교수", "제주대 경영대학 · 관광 공공 시나리오"),
  ("위치정보 · 개인정보 전문 변호사", "바우처 활용"),
  ("여행업 현직 MD 1명", "상품 기획과 가격 검토"),
]
check_html = "\n".join(f'          <li>{ICON("i-check")}<span><b>{b}</b> · {t}</span></li>' for b, t in checks)
plan_html = "\n".join(
  f'          <li>{ICON(ic)}<div><b>{k}</b><span>{v}</span></div><em class="{"on" if s == "운영 중" else ""}">{s}</em></li>'
  for ic, k, v, s in PLANNED)

block = f'''    <div class="advisory">
      <div class="advisory-head reveal">
        <span class="eyebrow">Advisory</span>
        <h3>기술 · 사업 · 현장을 아는<br>자문진과 함께합니다.</h3>
        <p>삼성 출신 기술·신사업 전문가, 관광 공공 시나리오 연구자, 법률·여행업 실무자가 제품과 사업을 단계별로 검토합니다.</p>
        <ul class="checks">
{check_html}
        </ul>
      </div>
      <div class="advisor-list">
{"".join(card(i + 1, a) for i, a in enumerate(ADVISORS))}      </div>
      <div class="ad-plan reveal">
        <div class="ad-plan-head">
          <span class="eyebrow">Advisory Plan</span>
          <h4>사업 단계에 맞춰 자문 영역을 넓힙니다.</h4>
          <p>규제·하드웨어·기관 시장 진입 시점에 맞춰 분야별 자문을 순차 확보합니다.</p>
        </div>
        <ul class="ad-plan-list">
{plan_html}
        </ul>
      </div>
    </div>
'''

s = page.read_text(encoding="utf-8")
start = s.index('    <div class="advisory">')
end = s.index("  </div>\n</section>\n\n<!-- ============ ORG PLAN")
s = s[:start] + block + s[end:]
# remove CTO 모집 tile
s = re.sub(r'\s*<h3 class="sub-title">CTO · 공동창업자를 찾습니다</h3>\s*<div class="tile" style="padding:24px">.*?</div>', "", s, count=1, flags=re.S)
page.write_text(s, encoding="utf-8")

c = css.read_text(encoding="utf-8")
if ".ad-plan" not in c:
    add = """.ad-plan { grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1.7fr; gap: 48px; padding: 34px; border-radius: 26px; background: #fff; border: 1px solid var(--line); }
.ad-plan-head h4 { font-size: 22px; letter-spacing: -.03em; margin: 12px 0 8px; }
.ad-plan-head p { color: var(--muted); font-size: 14.5px; }
.ad-plan-list { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.ad-plan-list li { display: grid; grid-template-columns: 22px 1fr auto; gap: 10px; align-items: start; padding: 14px 16px; border-radius: 14px; background: var(--bg-soft); border: 1px solid var(--line); }
.ad-plan-list .icon { width: 20px; height: 20px; color: var(--mint-2); margin-top: 2px; }
.ad-plan-list b { display: block; font-size: 14.5px; color: var(--ink); }
.ad-plan-list span { display: block; font-size: 13px; color: var(--muted); line-height: 1.55; margin-top: 2px; }
.ad-plan-list em { font-style: normal; font-size: 11.5px; font-weight: 800; white-space: nowrap; padding: 4px 9px; border-radius: 999px; background: #fff; color: var(--muted); border: 1px solid var(--line); }
.ad-plan-list em.on { background: var(--mint-soft); color: #23306B; border-color: transparent; }
@media (max-width: 900px) { .ad-plan { grid-template-columns: 1fr; gap: 20px; padding: 24px 20px; } .ad-plan-list { grid-template-columns: 1fr; } }
"""
    c = c.replace("/* ---------- Sourcing ---------- */", add + "\n/* ---------- Sourcing ---------- */", 1)
    css.write_text(c, encoding="utf-8")
print("ok")
