"""홈 첫 화면과 대표 키 메시지를 '사람 + 물건(수하물·장비·자산)'으로 넓힌다. 다시 돌려도 안전.

    python scripts/update_home_key_message.py

- content/pages/index.html  히어로 문구·태그·지표·확장 안내
- index.html                <title>·설명·공유 미리보기
- data/site.json            바닥글 태그라인
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

KEY = "사람도 물건도, 빠짐없이."
TITLE = f"Keep121 · {KEY}"
DESC = ("Keep121은 단체로 이동하는 사람과 수하물·장비·자산의 이동과 인계를 확인하는 Sensing 기반 이동 안전 플랫폼입니다. "
        "사람은 Keep121 Guide, 물건은 Keep121 Track, 통합 관제는 Keep121 Enterprise. 현재 고객 인터뷰와 실증을 준비하고 있습니다.")

HERO = """    <div class="hv-copy">
      <span class="eyebrow">People &amp; Asset Movement · Keep121</span>
      <h1><span class="kept" lang="en">Every one, kept</span>사람도 물건도<br><em>빠짐없이.</em></h1>
      <p class="hero-lead">단체로 이동하는 사람은 점호와 이탈 대응으로, 수하물·장비·자산은 인계와 회수 확인으로. 이동하는 모든 것의 ‘지금 어디에, 누구 손에’를 하나의 Sensing 플랫폼과 기록으로 연결합니다.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="company.html#contact">파일럿 문의 <svg class="icon"><use href="#i-arrow"/></svg></a>
        <a class="btn btn-ghost" href="b2b.html"><svg class="icon"><use href="#i-play"/></svg>Guide · Track · Enterprise 보기</a>
      </div>
      <div class="hero-meta">
        <span class="tag ghost"><svg class="icon" style="width:14px;height:14px"><use href="#i-check"/></svg>모두의창업 2기 1차 선정</span>
        <span class="tag ghost">사람 · Guide</span>
        <span class="tag ghost">물건 · Track</span>
        <span class="tag ghost">통합 관제 · Enterprise</span>
      </div>
    </div>
"""
STATS = """    <div class="hero-stats">
      <div><b>30<small>초</small></b><span>단체 점호 · 사람 (Guide 파일럿 목표)</span></div>
      <div><b>3<small>분</small></b><span>버스 출발 후 미승차 인지 (Guide 목표)</span></div>
      <div><b>1<small>스캔</small></b><span>수하물·장비 인계 확인 · 물건 (Track 목표)</span></div>
      <div><b>1<small>화면</small></b><span>사람·물건 통합 관제 (Enterprise)</span></div>
    </div>
"""
NOTICE = ('<div class="wrap"><p class="notice reveal mt-s"><span><b>2026.11 확장</b> · 사람의 이동 안전(Guide)에서 수하물·장비·자산 추적(Track), '
          '통합 관제(Enterprise)로 넓혔습니다. 세 상품은 같은 Keep121 Sensing 위에서 동작합니다. 아래 여행 장면은 초기 사용 시나리오입니다. '
          '<a href="b2b.html">B2B 확장 전략 보기</a></span></p></div>\n')

p = "content/pages/index.html"
t = rd(p)
t, a = re.subn(r'    <div class="hv-copy">\n.*?\n    </div>\n(?=\n    <div class="hv-ui")', lambda m: HERO, t, count=1, flags=re.S)
t, b = re.subn(r'    <div class="hero-stats">\n.*?\n    </div>\n', lambda m: STATS, t, count=1, flags=re.S)
t, c = re.subn(r'<div class="wrap"><p class="notice reveal mt-s"><span><b>2026\.11 확장[^\n]*\n', lambda m: NOTICE, t, count=1)
assert (a, b, c) == (1, 1, 1), (a, b, c)
wr(p, t)

h = rd("index.html")
h = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", h, count=1)
h = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + DESC, h)
h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE, h)
wr("index.html", h)

s = json.loads(rd("data/site.json"))
s["footer"]["tagHtml"] = f'<span lang="en">Every one, kept.</span> {KEY}'
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=2) + "\n")
print("  index 히어로·지표·안내 · index.html 메타 · 바닥글 태그라인")
