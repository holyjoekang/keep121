"""Add 2nd advisor (고려대 김종우 겸임교수) and CTO 합류 예정 card to company Advisory."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent.parent
page = ROOT / "content/pages/company.html"
css = ROOT / "assets/css/style.css"

TOPO = '<svg class="ad-topo" viewBox="0 0 260 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g fill="none" stroke="#B4BEF0" stroke-opacity=".22"><ellipse cx="200" cy="250" rx="60" ry="34"/><ellipse cx="200" cy="250" rx="100" ry="58"/><ellipse cx="200" cy="250" rx="145" ry="86"/><ellipse cx="200" cy="250" rx="195" ry="118"/><ellipse cx="200" cy="250" rx="250" ry="152"/></g></svg>'

def card(d, mono, badge, icon, org, name, title, role, key, body, tags, extra=""):
    t = "".join(f"<span>{x}</span>" for x in tags)
    return f'''      <article class="advisor-card reveal {d}">
        <div class="ad-visual">
          {TOPO}
          <span class="ad-mono{' sm' if len(mono) > 1 else ''}">{mono}</span>
          <span class="ad-badge">{badge}</span>
        </div>
        <div class="ad-body">
          <div class="ad-org"><svg class="icon"><use href="#{icon}"/></svg>{org}</div>
          <h4>{name} <small>{title}</small></h4>
          <div class="ad-role">{role}</div>
{extra}          <div class="ad-contrib">
            <span class="k">{key}</span>
            <p>{body}</p>
          </div>
          <div class="ad-foot">
            <div class="ad-tags">{t}</div>
          </div>
        </div>
      </article>
'''

kim = card("d2", "김", "자문교수", "i-school", "고려대학교 기술경영전문대학원(MOT)", "김종우", "겸임교수",
    "Keep121 자문교수 · 첨단전략산업 · 기술경영",
    "학력 · 경력",
    "연세대 행정학 · 코넬대 MBA · 텍사스오스틴대 정책학 석사 · 서울과기대 정책학 박사<br>"
    "<b>웰리시스(삼성 스핀오프) 공동창업자 · CSO</b>, <b>삼성SDS 신사업개발그룹장</b>",
    ["첨단전략산업", "기술경영", "신사업개발"])
cto = card("d3", "CTO", "합류 예정", "i-signal", "Chief Technology Officer", "CTO", "합류 예정",
    "삼성SDS 30년 경력 IT 전문가",
    "역할",
    "<b>삼성SDS 30년</b> IT 시스템 설계·구축 경험으로 Keep121 플랫폼·디바이스 연동 기술 개발을 총괄할 예정입니다.",
    ["IT 시스템", "플랫폼 개발", "삼성SDS 30년"])

s = page.read_text(encoding="utf-8")
if "김종우" not in s:
    s = s.replace('      <article class="advisor-card reveal d1">', '      <div class="advisor-list">\n      <article class="advisor-card reveal d1">', 1)
    end = s.index("</article>", s.index('class="advisor-list"')) + len("</article>\n")
    s = s[:end] + kim + cto + "      </div>\n" + s[end:]
    s = s.replace("<b>여행업 현직 MD 1명</b> · 상품 기획과 가격 검토</span></li>",
        "<b>여행업 현직 MD 1명</b> · 상품 기획과 가격 검토</span></li>\n          <li><svg class=\"icon\"><use href=\"#i-check\"/></svg><span><b>기술경영 · 신사업 자문</b> · 고려대 MOT 김종우 겸임교수</span></li>", 1)
    page.write_text(s, encoding="utf-8")

c = css.read_text(encoding="utf-8")
if ".advisor-list" not in c:
    c = c.replace(".advisor-card { display: grid;",
        ".advisor-list { display: flex; flex-direction: column; gap: 20px; }\n.ad-mono.sm { font-size: 30px; }\n.advisor-card { display: grid;", 1)
    css.write_text(c, encoding="utf-8")
print("ok")
