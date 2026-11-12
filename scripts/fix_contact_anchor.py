"""'문의' 링크가 정확히 company.html#contact 로 가게 하고, 문의 섹션을 현재 사업(사람+물건, 맞춤 제안)에 맞게 바꾼다. 다시 돌려도 안전.

    python scripts/fix_contact_anchor.py

- assets/js/render.js : 본문을 그린 뒤 사진·삽입 스크립트로 높이가 바뀌어도 #해시 위치로 다시 맞춘다
                        (그리기 직후 · 사진 로드 후 · 1.2초 뒤, 사용자가 먼저 스크롤하면 멈춤). 같은 페이지 내 #링크도 같은 방식.
- assets/css/style.css: 휴대폰에서 고정 띠+메뉴에 가리지 않게 scroll-padding
- content/pages/company.html : #contact 문구 · 목록 · 문의 유형 · 안내 문구
- 모든 페이지 껍데기의 render.js · style.css 캐시 버전 갱신
"""
import datetime as dt, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")

# 1) render.js — 해시 위치 고정
js = rd("assets/js/render.js")
OLD = "    if (location.hash) { const t = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t) t.scrollIntoView(); }\n"
NEW = """    // #해시로 들어오면 본문 · 사진 · 삽입 블록이 다 그려진 뒤에도 그 위치를 지킨다 (사용자가 먼저 스크롤하면 멈춤)
    const toHash = () => { const t = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1))); if (t) t.scrollIntoView({ behavior: 'instant', block: 'start' }); };
    let held = !!location.hash;
    const release = () => { held = false; };
    ['wheel', 'touchstart', 'keydown'].forEach(ev => addEventListener(ev, release, { once: true, passive: true }));
    const hold = () => { if (held) toHash(); };
    hold(); requestAnimationFrame(hold); setTimeout(hold, 400); setTimeout(hold, 1200); addEventListener('load', () => { hold(); setTimeout(() => { hold(); held = false; }, 600); });
    // 같은 페이지 안의 #링크(예: 회사 페이지에서 '파일럿 문의')도 정확히 그 섹션으로
    document.addEventListener('click', e => {
      const a = e.target.closest('a[href*="#"]');
      if (!a) return;
      const u = new URL(a.href, location.href);
      if (u.pathname !== location.pathname || !u.hash) return;
      const t = document.getElementById(decodeURIComponent(u.hash.slice(1)));
      if (!t) return;
      e.preventDefault();
      history.pushState(null, '', u.hash);
      t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
"""
if "const toHash = () =>" not in js:
    assert OLD in js, "render.js hash line not found"
    js = js.replace(OLD, NEW)
wr("assets/js/render.js", js)

# 2) style.css — 고정 메뉴 높이만큼 여백
css = rd("assets/css/style.css")
css = re.sub(r"/\* anchor-offset \(scripts/fix_contact_anchor\.py\) \*/.*?/\* /anchor-offset \*/\n", "", css, flags=re.S)
css = css.rstrip("\n") + "\n\n/* anchor-offset (scripts/fix_contact_anchor.py) — 휴대폰은 Joyhouse 띠(40px)+메뉴(72px) 만큼 */\n@media (max-width: 760px) { html { scroll-padding-top: 124px; } html:has(body.subpage) { scroll-padding-top: 170px; } }\n/* /anchor-offset */\n"
wr("assets/css/style.css", css)

# 3) company.html #contact — 현재 사업에 맞게
p = "content/pages/company.html"
t = rd(p)
LEFT = """      <div class="reveal">
        <span class="eyebrow">Contact · 파일럿 · 맞춤 제안</span>
        <h2>사람과 물건의 이동,<br>함께 지킬 파트너를 찾습니다.</h2>
        <p style="color:#A3AAC4;font-size:18px">학교 현장체험학습 · 수학여행, 여행사 · 교회 단체여행과 순례, 지자체 관광 · 대규모 행사, 장비 렌털 · 수하물까지. 무상 시범 운영(파일럿)부터 현장에 맞춘 맞춤 제안서까지 함께 준비합니다.</p>
        <div class="contact-list">
          <div><svg class="icon"><use href="#i-school"/></svg>학교 · 교육청 — 현장체험학습 · 수학여행 점호와 학부모 알림 (Guide)</div>
          <div><svg class="icon"><use href="#i-bus"/></svg>여행사 · 교회 · 기관 — 단체여행 · 순례 · 어르신 프로그램</div>
          <div><svg class="icon"><use href="#i-flag"/></svg>지자체 · 관광공사 · 행사 — 방문객 · 대규모 행사 통합 관제 (Enterprise)</div>
          <div><svg class="icon"><use href="#i-box"/></svg>렌털 · 물류 · 수하물 — 장비 · 짐의 인계와 회수 (Track)</div>
          <div><svg class="icon"><use href="#i-users"/></svg>기술 · 사업 파트너 — 개발 · 센서 · 통신 · 투자</div>
          <div><svg class="icon"><use href="#i-mail"/></svg><a href="mailto:joekang@naver.com" style="color:#fff;text-decoration:underline;text-underline-offset:3px">joekang@naver.com</a></div>
        </div>
        <p style="color:#A3AAC4;font-size:15px;margin-top:18px">지금까지의 맞춤 제안은 <a href="proposals.html" style="color:#fff;text-decoration:underline;text-underline-offset:3px">맞춤 제안 모음</a>에서 볼 수 있습니다.</p>
      </div>
"""
t, n = re.subn(r'      <div class="reveal">\n        <span class="eyebrow">[^<]*</span>\n        <h2>.*?</h2>.*?\n        </div>\n(?:        <p style="color:#A3AAC4;font-size:15px.*?</p>\n)?      </div>\n(?=      <!-- 제출하면)', lambda m: LEFT, t, count=1, flags=re.S)
assert n == 1, "contact left column not found"
TYPES = ["무상 파일럿(시범 운영) 참여", "맞춤 제안서 요청", "학교 현장체험학습 · 수학여행", "여행사 · 교회 단체여행 · 순례",
         "지자체 · 관광 · 대규모 행사", "장비 · 수하물 추적 (Track)", "기술 · 사업 파트너십 · 투자", "기타 문의"]
t = re.sub(r'<select id="fType" name="type">.*?</select>', '<select id="fType" name="type">' + "".join(f"<option>{x}</option>" for x in TYPES) + "</select>", t, count=1)
t = re.sub(r'(<input id="fOrg" name="org" placeholder=")[^"]*', r"\1○○중학교 · ○○여행사 · ○○기관", t, count=1)
t = re.sub(r'(<textarea id="fMsg" name="message" placeholder=")[^"]*',
           r"\1기관 종류, 행사 · 여행 일정, 인원(학생 · 참가자 수), 함께 관리할 물건(짐 · 장비)을 알려 주시면 맞춤 제안을 준비해 드립니다.", t, count=1)
wr(p, t)

# 4) 캐시 버전
for f in ROOT.glob("*.html"):
    h = f.read_text(encoding="utf-8")
    if "assets/js/render.js" not in h:
        continue
    h2 = re.sub(r'assets/css/style\.css(\?v=\d+)?"', f'assets/css/style.css?v={V}"', h)
    h2 = re.sub(r'assets/js/render\.js(\?v=\d+)?"', f'assets/js/render.js?v={V}"', h2)
    if h2 != h:
        f.write_text(h2, encoding="utf-8")
print("  render.js 해시 이동 · style.css scroll-margin · company #contact 문구")
