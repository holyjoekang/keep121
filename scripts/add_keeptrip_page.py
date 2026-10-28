"""KeepTrip(자매 앱) 소개 페이지를 사이트에 붙인다(다시 돌려도 안전).

- data/site.json: 상단 메뉴(회사 앞) · 바닥글 Service 열 · 페이지 순서에 keeptrip 추가
- keeptrip.html: family.html 껍데기를 복사해 제목·SEO·data-page 만 바꾼다
- content/pages/keeptrip.html: 본문 (아래 BODY)
- content/pages/index.html: 홈 'Explore'에 KeepTrip 카드 + 제품 섹션 아래 자매 앱 띠
- assets/css/style.css: KeepTrip 전용 스타일 추가
- README.md: 구성 목록에 한 줄
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

# KeepTrip 로고: Keep121 문 마크 + 핀(Dawn), 선으로만 그림
PIN = "M24 23.6c-3.4 0-5.8 2.5-5.8 5.7 0 4 5.8 9.6 5.8 9.6s5.8-5.6 5.8-9.6c0-3.2-2.4-5.7-5.8-5.7z"
DOOR = "M12 40V22a12 12 0 0 1 24 0v18"
WORD = ('<g fill="none" stroke="currentColor" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M0 8V40M19 8L3 25M8 20L20 40 M28 29H50A11 11 0 1 0 48 35.3 M56 29H78A11 11 0 1 0 76 35.3 M86 18V52"/>'
        '<circle cx="97" cy="29" r="11"/><path d="M116 8H142 M129 8V40 M150 18V40 M150 28C150 21.5 154 18 160 18 M168 20V40 M178 18V52"/>'
        '<circle cx="189" cy="29" r="11"/></g><circle cx="168" cy="9.5" r="3.2" fill="currentColor"/>')
def lockup(w, hole="#fff"):
    return (f'<svg class="kt-lock" viewBox="-3 3 268 54" width="{w}" role="img" aria-label="KeepTrip">'
            f'<path d="{DOOR}" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{PIN}" fill="#F2A541"/><circle cx="24" cy="29.3" r="2" fill="{hole}"/>'
            f'<g transform="translate(62 0)">{WORD}</g></svg>')
def mark(size, pin=True):
    inner = (f'<path d="{PIN}" fill="#F2A541"/><circle cx="24" cy="29.3" r="2" fill="#fff"/>' if pin
             else '<circle cx="24" cy="31" r="4.5" fill="#F2A541"/>')
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}" role="img" aria-label="{"KeepTrip" if pin else "Keep121"} 마크">'
            f'<path d="{DOOR}" fill="none" stroke="#23306B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>{inner}</svg>')

PHOTO = "https://images.unsplash.com/photo-1607068891828-f16297950a66?auto=format&fit=crop&w=1800&q=75"

BODY = f"""<!-- ============ PAGE HEADER ============ -->
<section class="page-hero has-photo" style="--bg:url('{PHOTO}')">
  <div class="wrap">
    <nav class="crumb" aria-label="현재 위치"><a href="index.html">홈</a><span aria-hidden="true">/</span><b>KeepTrip</b></nav>
    <div class="page-hero-grid">
      <div>
        <span class="eyebrow">Sister App · KeepTrip</span>
        <h1>단체여행이 끝나도,<br>여행은 계속됩니다.</h1>
        <p>Keep121이 단체를 지킨다면, KeepTrip은 한 사람의 여행을 간직합니다. 일정을 넣으면 챙길 것을 골라 주고, 도착하면 해설을 열어 주고, 말로 남긴 기록을 여행기로 엮어 가족과 나눕니다. 앱 설치 없이 링크로 엽니다.</p>
      </div>
      <div class="page-facts"><div><b>0<small>개</small></b><span>설치할 앱</span></div><div><b>5<small>가지</small></b><span>준비부터 공유까지</span></div><div><b>D-3</b><span>바뀌는 조건 재확인</span></div><div><b>1<small>개</small></b><span>가족에게 보낼 링크</span></div></div>
    </div>
  </div>
</section>

<nav class="subnav" id="subnav" aria-label="이 페이지의 내용">
  <div class="wrap">
    <span class="subnav-k">이 페이지</span>
      <a href="#brand">브랜드</a>
      <a href="#features">다섯 가지 기능</a>
      <a href="#onsite">여행 중</a>
      <a href="#story">여행 후</a>
      <a href="#link">Keep121 연동</a>
  </div>
</nav>

<!-- ============ BRAND ============ -->
<section id="brand">
  <div class="wrap feature-grid">
    <div class="kt-brand reveal">
      <div class="kt-brand-lock">{lockup(320)}</div>
      <div class="kt-marks"><div>{mark(64, False)}<b>Keep121</b><span>점 = 끝까지 지키는 그 한 사람</span></div><div>{mark(64)}<b>KeepTrip</b><span>핀 = 지금 내가 있는 곳</span></div></div>
    </div>
    <div class="feature-copy reveal d1">
      <span class="eyebrow">Every trip, kept.</span>
      <h2>같은 문,<br><span class="hl">다른 점.</span></h2>
      <p>Keep121의 1·2·1 문 마크와 선 굵기, 글자 획은 그대로 두고 문 안의 Dawn 점만 핀으로 바꿨습니다. 슬로건 “다녀온 길까지, 간직하다”는 Keep121의 “Every one, kept.”와 짝을 이룹니다.</p>
      <ul class="feature-list">
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>나가고 들어오는 동안만</b> 위치는 여행 기간에만 씁니다</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>기록은 내 것</b> 보이스 기록·사진·여행기는 본인 소유, 공유는 본인이 켜고 끕니다</span></li>
      </ul>
    </div>
  </div>
</section>

<!-- ============ FEATURES ============ -->
<section class="soft" id="features">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Five Features</span>
      <h2>준비부터 공유까지,<br><span class="hl">한 링크 안에서.</span></h2>
      <p>여행 준비는 할 일이 산더미인데 조건은 자주 바뀝니다. KeepTrip은 내 일정과 이미 가진 카드·폰을 기준으로, 아낄 것은 아끼고 무시할 것은 무시하게 돕습니다.</p>
    </div>
    <div class="products kt-features">
      <div class="prod reveal"><span class="ic"><svg class="icon"><use href="#i-check"/></svg></span><span class="role">Prep</span><h3>맞춤 준비</h3><p>꼭 챙길 것 · 돈 아끼는 것 · 신경 끌 것을 나눠 줍니다. 결제 수수료처럼 자주 바뀌는 항목은 출발 3일 전 다시 확인합니다.</p></div>
      <div class="prod reveal d1"><span class="ic"><svg class="icon"><use href="#i-phone"/></svg></span><span class="role">Today</span><h3>오늘</h3><p>다음 일정, 길찾기, 현지어 택시 주소 카드, 오늘 꼭 챙길 것을 한 화면에.</p></div>
      <div class="prod reveal d2"><span class="ic"><svg class="icon"><use href="#i-pin"/></svg></span><span class="role">Arrive</span><h3>도착 해설</h3><p>박물관·명소에 도착하면 짧은 음성 해설과 “여기서 꼭 볼 것”이 먼저 열립니다.</p></div>
      <div class="prod reveal"><span class="ic"><svg class="icon"><use href="#i-message"/></svg></span><span class="role">Voice</span><h3>보이스 기록</h3><p>말로 남기면 AI가 장소·음식·동행·추천으로 정리하고 그 시각의 사진과 묶습니다.</p></div>
      <div class="prod reveal d1"><span class="ic"><svg class="icon"><use href="#i-heart"/></svg></span><span class="role">Story</span><h3>여행 스토리</h3><p>일정 + 기록 + 사진으로 여행기 초안을 만들고, 카카오톡 링크 하나로 가족·지인과 나눕니다.</p></div>
    </div>
    <p class="fine mt-m reveal">결제·환전 수수료와 카드사 프로모션은 수시로 바뀝니다. KeepTrip은 출발 시점의 공식 안내를 기준으로 다시 확인하도록 설계합니다.</p>
  </div>
</section>

<!-- ============ ON SITE ============ -->
<section id="onsite">
  <div class="wrap feature-grid">
    <div class="kt-phone reveal" aria-label="도착 해설 화면 예시">
      <div class="kt-ph-top"><span>DAY 3 · 청두</span><b>방금 도착했어요</b></div>
      <h4>수정방 박물관</h4><p class="kt-ph-sub">水井坊博物馆</p>
      <div class="kt-ph-play"><span class="kt-ph-btn" aria-hidden="true"><svg class="icon"><use href="#i-play"/></svg></span><div><b>3분 음성 해설</b><i><em></em></i></div></div>
      <ol class="kt-ph-list"><li>600년 양조 유적</li><li>전통 양조기술 전시</li><li>시음 코너 · 운영 여부 현장 확인</li></ol>
      <div class="kt-ph-voice">말로 느낌 남기기</div>
    </div>
    <div class="feature-copy reveal d1">
      <span class="eyebrow">On the Road</span>
      <h2>도착하면 열리고,<br><span class="hl">말하면 남습니다.</span></h2>
      <p>현장에 가도 무엇을 봐야 할지 몰라 지나치는 경우가 많습니다. 걸으면서 글을 쓰기도 어렵습니다. KeepTrip은 처음 짠 일정과 지금 위치를 맞춰, 도착한 곳의 해설을 먼저 보여 주고 말로 남긴 느낌을 받아 적습니다.</p>
      <ul class="feature-list">
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>도착 감지</b> 본인이 동의한 경우, 여행 기간에만</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>AI 정리</b> 장소 · 음식 · 함께한 사람 · 추천으로 자동 분류</span></li>
        <li><svg class="icon"><use href="#i-check"/></svg><span><b>사진과 묶음</b> 같은 시각·장소의 사진을 기록에 붙임</span></li>
      </ul>
      <p class="fine">화면은 예시입니다.</p>
    </div>
  </div>
</section>

<!-- ============ STORY ============ -->
<section class="soft" id="story">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">After the Trip</span>
      <h2>도구를 다루는 사람만 하던 일을,<br><span class="hl">누구나.</span></h2>
      <p>다녀와서 메모를 모으고, AI로 정리하고, 사이트로 옮기는 일은 지금까지 손이 많이 갔습니다. KeepTrip은 여행 중 남긴 것으로 여행기를 만들어 링크로 건넵니다.</p>
    </div>
    <div class="spec-table-wrap reveal">
      <table class="spec-table">
        <thead><tr><th scope="col">단계</th><th scope="col">지금 방식</th><th scope="col">KeepTrip</th></tr></thead>
        <tbody>
          <tr><th scope="row">정리</th><td>메모를 문서에 모으고 AI로 다시 정리</td><td>여행 중 남긴 기록이 날짜별로 자동 정리</td></tr>
          <tr><th scope="row">만들기</th><td>블로그·사이트용으로 직접 편집, 코딩</td><td>대표 사진·추천 장소가 담긴 여행기 초안</td></tr>
          <tr><th scope="row">나누기</th><td>올린 뒤 링크를 따로 공유</td><td>카카오톡 링크 한 번, 블로그로 내보내기</td></tr>
          <tr><th scope="row">추천</th><td>지인에게 말로 전함</td><td>“강추” 표시한 식당·박물관이 다음 여행자의 살아 있는 추천으로</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<!-- ============ KEEP121 LINK ============ -->
<section id="link">
  <div class="wrap">
    <div class="head reveal">
      <span class="eyebrow">Keep121 × KeepTrip</span>
      <h2>단체여행 고객이,<br><span class="hl">다음 여행의 KeepTrip 사용자로.</span></h2>
      <p>여행사의 일정과 가이드의 확인 기록이 개인의 여행 기록이 됩니다. B2B에서 만난 고객이 B2C로 이어지는 재구매 접점입니다.</p>
    </div>
    <div class="spec-table-wrap reveal">
      <table class="spec-table">
        <thead><tr><th scope="col">Keep121 (단체)</th><th scope="col">KeepTrip (개인)</th></tr></thead>
        <tbody>
          <tr><td>여행사 일정 · 상품 정보</td><td>맞춤 준비 · 오늘</td></tr>
          <tr><td>가이드 도착 확인 기록</td><td>도착 해설 · 날짜별 기록</td></tr>
          <tr><td>Keep Journey 여행 기록 앨범</td><td>여행 스토리 (같은 엔진)</td></tr>
          <tr><td>Keep Home 가족 알림 (여행 중)</td><td>스토리 링크 (귀국 후)</td></tr>
        </tbody>
      </table>
    </div>
    <p class="fine mt-m reveal">KeepTrip은 설계 중인 콘셉트입니다. 화면과 기능은 예시이며 출시 일정은 정해지지 않았습니다. 단체여행 기록을 KeepTrip으로 옮기는 것은 여행객 본인 동의를 전제로 합니다.</p>
  </div>
</section>
"""

CSS = """
/* KeepTrip 자매 앱 페이지 */
.kt-lock { display: block; max-width: 100%; height: auto; color: var(--ink-3); }
.kt-brand { display: grid; gap: 22px; padding: 36px; border-radius: 28px; background: var(--bg-soft); border: 1px solid var(--line); }
.kt-marks { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.kt-marks > div { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 18px 12px; border-radius: 18px; background: #fff; border: 1px solid var(--line); text-align: center; }
.kt-marks span { font-size: 13px; color: var(--muted); }
.kt-features { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.kt-phone { max-width: 340px; margin: 0 auto; padding: 20px; border: 8px solid var(--ink); border-radius: 38px; background: var(--bg-soft); box-shadow: 0 24px 60px rgba(20,26,46,.18); display: grid; gap: 10px; }
.kt-ph-top { display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: var(--muted); }
.kt-ph-top b { background: #fff; color: var(--ink-3); border-radius: 10px; padding: 3px 10px; font-size: 12px; }
.kt-phone h4 { margin: 4px 0 0; font-size: 22px; }
.kt-ph-sub { margin: 0; font-size: 13px; color: var(--muted); }
.kt-ph-play { display: flex; gap: 12px; align-items: center; padding: 12px; border-radius: 16px; background: var(--ink-3); color: #fff; }
.kt-ph-play > div { flex: 1; display: grid; gap: 6px; font-size: 14px; }
.kt-ph-play i { display: block; height: 4px; border-radius: 2px; background: rgba(255,255,255,.25); }
.kt-ph-play em { display: block; width: 30%; height: 4px; border-radius: 2px; background: var(--mint); }
.kt-ph-btn { width: 40px; height: 40px; border-radius: 20px; background: #fff; color: var(--ink-3); display: grid; place-items: center; flex: none; }
.kt-ph-btn .icon { width: 18px; height: 18px; fill: currentColor; }
.kt-ph-list { margin: 0; padding: 0; list-style: none; counter-reset: k; display: grid; gap: 6px; }
.kt-ph-list li { counter-increment: k; background: #fff; border-radius: 12px; padding: 10px 12px; font-size: 14px; }
.kt-ph-list li::before { content: counter(k); font-weight: 700; color: var(--ink-3); margin-right: 10px; }
.kt-ph-voice { text-align: center; padding: 12px; border-radius: 14px; background: #F2A541; color: var(--ink); font-weight: 700; font-size: 14px; }
.kt-band { display: flex; flex-wrap: wrap; align-items: center; gap: 20px 32px; margin-top: 28px; padding: 24px 28px; border-radius: 22px; background: #fff; border: 1px solid var(--line); text-decoration: none; color: inherit; }
.kt-band .kt-lock { width: 200px; }
.kt-band p { flex: 1 1 320px; margin: 0; color: var(--muted); font-size: 15px; }
.kt-band:hover { border-color: var(--ink-3); }
@media (max-width: 900px) { .kt-features { grid-template-columns: 1fr; } .kt-brand { padding: 24px; } }
"""

# 1) site.json
site = json.loads(rd("data/site.json"))
if not any(n["href"] == "keeptrip.html" for n in site["nav"]):
    i = next(k for k, n in enumerate(site["nav"]) if n["href"] == "company.html")
    site["nav"].insert(i, {"href": "keeptrip.html", "label": "KeepTrip"})
svc = next(c for c in site["footer"]["columns"] if c["title"] == "Service")
if not any(l["href"] == "keeptrip.html" for l in svc["links"]):
    svc["links"].append({"href": "keeptrip.html", "label": "KeepTrip (자매 앱)"})
if not any(p["id"] == "keeptrip" for p in site["pages"]):
    i = next(k for k, p in enumerate(site["pages"]) if p["id"] == "company")
    site["pages"].insert(i, {"id": "keeptrip", "file": "keeptrip.html", "name": "KeepTrip"})
wr("data/site.json", json.dumps(site, ensure_ascii=False, indent=1) + "\n")

# 2) 껍데기
title = "KeepTrip · Keep121 자매 앱"
desc = "설치 없이 링크로 여는 나만의 여행 가이드 KeepTrip. 맞춤 준비, 도착 해설, 보이스 기록, 여행 스토리, Keep121 단체여행과의 연동."
shell = rd("family.html")
shell = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", shell)
shell = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', rf"\g<1>{desc}", shell)
shell = re.sub(r'(<meta property="og:title" content=")[^"]*', rf"\g<1>{title}", shell)
shell = shell.replace("keep121/family.html", "keep121/keeptrip.html").replace('data-page="family"', 'data-page="keeptrip"')
assert 'data-page="keeptrip"' in shell
wr("keeptrip.html", shell)

# 3) 본문
wr("content/pages/keeptrip.html", BODY)

# 4) 홈
home = rd("content/pages/index.html")
if "keeptrip.html" not in home:
    band = (f'\n    <a class="kt-band reveal" href="keeptrip.html">{lockup(200)}'
            '<p><b style="color:var(--ink)">자매 앱 KeepTrip</b> — 단체여행이 끝나도 여행은 계속됩니다. 설치 없이 링크로 여는 나만의 여행 가이드: '
            '맞춤 준비, 도착 해설, 보이스 기록, 가족과 나누는 여행기.</p><svg class="icon"><use href="#i-arrow"/></svg></a>')
    anchor = "넘어짐 감지·SOS는 오감지와 책임 리스크 때문에 비활성으로 둡니다.</p>"
    assert anchor in home
    home = home.replace(anchor, anchor + band, 1)
    card = """
      <a class="ex reveal" href="keeptrip.html">
        <div class="ex-img"><img src="https://images.unsplash.com/photo-1607068891828-f16297950a66?auto=format&fit=crop&w=800&q=70" alt="함께 길을 걷는 여행 일행" loading="lazy"><span class="ex-tag">Sister App</span></div>
        <div class="ex-body"><b>KeepTrip</b><p>설치 없이 쓰는 개인 여행 가이드 — 준비, 도착 해설, 보이스 기록, 여행 스토리</p></div>
        <div class="ex-foot"><span class="ex-stat">0개 <small>설치할 앱</small></span><svg class="icon"><use href="#i-arrow"/></svg></div>
      </a>"""
    m = list(re.finditer(r"\n    </div>\n  </div>\n</section>", home))
    ex = home.index('id="explore"')
    end = next(x for x in m if x.start() > ex)
    home = home[:end.start()] + card + home[end.start():]
    wr("content/pages/index.html", home)

# 5) CSS
css = rd("assets/css/style.css")
if "/* KeepTrip 자매 앱 페이지 */" not in css:
    wr("assets/css/style.css", css.rstrip("\n") + "\n" + CSS)

# 6) README
md = rd("README.md")
if "keeptrip.html" not in md:
    line = "- `company.html` — 비전·가치 · 브랜드 · 창업자·자문 · 팀 구성 계획 · 파일럿 문의\n"
    assert line in md
    md = md.replace(line, "- `keeptrip.html` — 자매 앱 KeepTrip(설치 없는 개인 여행 가이드): 브랜드 · 다섯 가지 기능 · 여행 중 · 여행 후 · Keep121 연동. 생성은 `scripts/add_keeptrip_page.py`\n" + line, 1)
    wr("README.md", md)
print("keeptrip 페이지 연결 완료", file=sys.stderr)
