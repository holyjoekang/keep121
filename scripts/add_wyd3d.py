"""WYD 서울 2027 제안을 1분짜리 3D(three.js) 영상형 페이지로 만든다. 다시 돌려도 안전.

    python scripts/add_wyd3d.py

- wyd2027-3d.html            페이지 껍데기 (three.js 0.160 · jsDelivr importmap)
- data/wyd2027_3d.json       장면 8개 · 합계 60초 (문구 · 숫자 · 카메라 · 입자 배치)
- assets/js/wyd3d.js         원본 scripts/wyd3d.js
- scripts/update_nav_menu.py · add_proposals_page.py 에 링크 등록 후 다시 실행
내용은 data/wyd2027.json(15장 제안서)의 핵심을 1분으로 줄인 것이다.
"""
import datetime as dt, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")

D = {
 "title": "WYD 서울 2027 · Keep121 1분 제안",
 "scenes": [
  {"layout": "globe", "dur": 7, "cam": {"p": [0, 3, 17]}, "orbit": 0.12, "align": "left",
   "k": "WYD Seoul 2027 · Keep121 × Galaxy SmartTag3",
   "title": "전 세계 40만 순례자가<br><em>서울로 옵니다.</em>",
   "sub": "2027 서울 세계청년대회 — 천주교 서울대교구 · 조직위원회 제안"},
  {"layout": "days", "dur": 7, "cam": {"p": [0, 2.5, 15], "look": 0.5}, "orbit": 0.05,
   "k": "2027.8.3 ~ 8.8", "title": "6일, 서울 곳곳에서<br><em>함께 이동합니다.</em>",
   "sub": "개막미사 · 교리교육 · 교황 환영 · 십자가의 길 · 밤샘 기도 · 폐막미사",
   "stats": [["40만", "해외 순례자 (추정)"], ["6일", "본대회"], ["수십", "개 언어"]]},
  {"layout": "crowd", "dur": 8, "cam": {"p": [0, 9, 13]}, "orbit": 0.04, "pings": 1, "align": "left",
   "k": "The Problem", "title": "인파 속 한 사람,<br><em>누가 먼저 알 수 있을까?</em>",
   "sub": "말이 다르고 길이 낯선 도시에서, 집결 시간이 지나서야 알게 된다면 이미 늦습니다."},
  {"layout": "groups", "dur": 8, "cam": {"p": [0, 11, 10]}, "orbit": 0.03, "pings": 14,
   "k": "Galaxy SmartTag3 · 9.5g", "title": "명찰 태그 하나,<br><em>그룹 점호는 1분.</em>",
   "sub": "인솔자는 32명 그룹을 1분 만에 확인하고, 미확인자는 마지막 위치 · 반경과 함께 알립니다.",
   "stats": [["9.5g", "SmartTag3"], ["1분", "그룹 점호"], ["2~3천원", "대여료 (안)"]]},
  {"layout": "layers", "dur": 8, "cam": {"p": [9, 4, 11], "look": 0}, "orbit": 0.05, "align": "left",
   "k": "Solution", "title": "순례자 · 인솔자 · 상황실을<br><em>하나의 흐름으로.</em>",
   "sub": "KeepTrip 다국어 일정 · 통역 → KeepGuide 점호 · SOS → KeepEnterprise 통합 관제",
   "stats": [["KeepTrip", "순례자"], ["KeepGuide", "인솔자"], ["Enterprise", "상황실"]]},
  {"layout": "route", "dur": 7, "cam": {"p": [0, 7, 12]}, "orbit": 0.02,
   "k": "Scenario", "title": "출국 전부터 귀국까지,<br><em>한 순례자의 7일.</em>",
   "sub": "등록 · 태그 수령 → 모국어 일정 → 실시간 통역 → 점호 · 이탈 경보 → 상황실 대응 → 반납"},
  {"layout": "dash", "dur": 7, "cam": {"p": [8, 8, 10]}, "orbit": 0.06, "align": "left",
   "k": "KeepEnterprise", "title": "조직위 상황실,<br><em>40만 명을 한 화면에.</em>",
   "sub": "구역 밀집도 · 미확인 경보 · SOS를 보고 가까운 봉사자 · 의료팀을 바로 연결합니다. (시연용)",
   "stats": [["11분", "평균 발견 (목표)"], ["5분", "미확인 인지 (목표)"], ["0건", "미해결 실종 (목표)"]]},
  {"layout": "arch", "dur": 8, "cam": {"p": [0, 0.5, 13]}, "orbit": 0.0,
   "k": "Samsung × 서울대교구 × Keep121", "title": "Every one, kept.<br><em>모두가 함께 돌아가는 대회.</em>",
   "sub": "삼성전자 단말 스폰서 · 공동 캠페인, 2027 상반기 교구 청년 행사 파일럿부터 함께합니다.",
   "cta": [["15장 제안서 보기", "wyd2027.html"], ["맞춤 제안 모음", "proposals.html"]]}
 ]
}
assert sum(s["dur"] for s in D["scenes"]) == 60
wr("data/wyd2027_3d.json", json.dumps(D, ensure_ascii=False, indent=1) + "\n")

HTML = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WYD 서울 2027 · 1분 3D 제안 · Keep121</title>
  <meta name="description" content="Keep121 × Galaxy SmartTag3 — 2027 서울 세계청년대회 40만 순례자 안전 · 안내 제안을 60초 3D로.">
  <meta property="og:title" content="WYD 서울 2027 · 1분 3D 제안 · Keep121">
  <meta property="og:description" content="40만 순례자, 한 사람도 놓치지 않는 WYD 서울 2027 — 60초 3D 제안">
  <meta property="og:url" content="https://keep121.co.kr/wyd2027-3d.html">
  <meta name="theme-color" content="#0b0f24">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600..800&family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap">
  <style>
    :root{{--dawn:#F2A541;--ink:#0b0f24}}
    *{{box-sizing:border-box}} html,body{{margin:0;height:100%;background:var(--ink);color:#fff;font-family:"IBM Plex Sans KR",system-ui,sans-serif;overflow:hidden}}
    #scene{{position:fixed;inset:0;width:100%;height:100%;display:block}}
    .top{{position:fixed;left:16px;right:16px;top:14px;display:flex;justify-content:space-between;align-items:center;gap:12px;z-index:3}}
    .top a{{color:#fff;text-decoration:none}}
    .brand{{display:flex;align-items:center;gap:8px;font:800 16px "Bricolage Grotesque",sans-serif;background:rgba(11,15,36,.6);padding:6px 12px 6px 8px;border-radius:12px;backdrop-filter:blur(8px)}}
    .brand svg{{width:24px;height:24px}}
    .nav{{display:flex;gap:4px;background:rgba(11,15,36,.6);padding:4px;border-radius:12px;backdrop-filter:blur(8px);font-size:14px}}
    .nav a{{padding:6px 10px;border-radius:9px;opacity:.85}} .nav a:hover{{background:rgba(255,255,255,.12);opacity:1}}
    .shade{{position:fixed;inset:0;z-index:1;pointer-events:none;background:linear-gradient(0deg,rgba(11,15,36,.85) 0%,rgba(11,15,36,.4) 30%,rgba(11,15,36,0) 55%)}}
    .cap{{position:fixed;left:50%;bottom:120px;transform:translate(-50%,16px);width:min(900px,calc(100% - 32px));text-align:center;z-index:2;opacity:0;transition:opacity .5s,transform .5s;pointer-events:none}}
    .cap.on{{opacity:1;transform:translate(-50%,0)}} .cap.left{{left:clamp(16px,6vw,96px);transform:translateY(16px);text-align:left;width:min(620px,calc(100% - 32px))}} .cap.left.on{{transform:none}}
    .cap .k{{font:700 13px "Bricolage Grotesque",sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--dawn);margin:0 0 12px}}
    .cap h2{{font-size:clamp(30px,5vw,60px);line-height:1.15;margin:0 0 14px;letter-spacing:-.02em;text-shadow:0 4px 30px rgba(0,0,0,.6)}} .cap h2 em{{font-style:normal;color:var(--dawn)}}
    .cap .sub{{font-size:clamp(15px,1.7vw,20px);line-height:1.6;color:#d3d9f5;margin:0;text-shadow:0 2px 16px rgba(0,0,0,.7)}}
    .stats{{display:flex;gap:10px;margin-top:20px;justify-content:center;flex-wrap:wrap}} .cap.left .stats{{justify-content:flex-start}}
    .stats div{{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:14px;padding:10px 16px;backdrop-filter:blur(6px);min-width:110px}}
    .stats b{{display:block;font:800 26px "Bricolage Grotesque",sans-serif;color:var(--dawn)}} .stats span{{font-size:13px;color:#c9d0ee}}
    .cta{{display:flex;gap:10px;justify-content:center;margin-top:22px;pointer-events:auto}} .cta a{{background:var(--dawn);color:#2a1a00;font-weight:700;padding:12px 20px;border-radius:12px;text-decoration:none}} .cta a.ghost{{background:rgba(255,255,255,.1);color:#fff;border:1px solid rgba(255,255,255,.25)}}
    .ctl{{position:fixed;left:16px;right:16px;bottom:22px;z-index:3;display:flex;align-items:center;gap:12px}}
    .ctl button{{border:0;background:rgba(255,255,255,.12);color:#fff;border-radius:10px;height:36px;min-width:40px;padding:0 12px;font:inherit;cursor:pointer}}
    #dots{{display:flex;gap:6px}} #dots button{{min-width:0;width:26px;height:26px;padding:0;background:transparent;display:grid;place-items:center}} #dots i{{width:9px;height:9px;border-radius:50%;background:rgba(255,255,255,.35)}} #dots button.on i{{background:var(--dawn);transform:scale(1.4)}}
    .track{{flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,.15);overflow:hidden}} #bar{{height:100%;width:0;background:var(--dawn)}}
    #time{{font-size:13px;color:#aab3d8;min-width:72px;text-align:right}} #replay{{display:none}} body.ended #replay{{display:inline-block}}
    @media (max-width:640px){{.nav a:not(:last-child){{display:none}} .cap,.cap.left{{left:16px;transform:translateY(16px);text-align:left;bottom:110px}} .cap.on,.cap.left.on{{transform:none}} .stats{{justify-content:flex-start}} .stats div{{min-width:0;padding:8px 12px}} .stats b{{font-size:20px}} #dots{{display:none}} .cta{{justify-content:flex-start}}}}
  </style>
  <script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}}}</script>
</head>
<body>
<!-- 장면 데이터: data/wyd2027_3d.json · 렌더러: assets/js/wyd3d.js · 생성: scripts/add_wyd3d.py -->
<canvas id="scene" aria-label="3D 애니메이션: 순례자를 나타내는 입자들이 장면마다 모양을 바꿉니다"></canvas>
<header class="top">
  <a class="brand" href="index.html" aria-label="Keep121 홈"><svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#23306B"/><path d="M9 26V15a7 7 0 0 1 14 0v11" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/><circle cx="16" cy="20.5" r="3" fill="#F2A541"/></svg>Keep121</a>
  <nav class="nav" aria-label="제안 메뉴"><a href="index.html">홈</a><a href="proposals.html">맞춤 제안</a><a href="wyd2027.html">15장 제안서</a></nav>
</header>
<div class="shade" aria-hidden="true"></div>
<section class="cap" id="cap" aria-live="polite"></section>
<div class="ctl"><button id="play" aria-label="재생 / 정지">❚❚</button><div id="dots"></div><div class="track"><div id="bar"></div></div><span id="time">0s</span><button id="replay">다시 보기</button></div>
<h1 id="title" hidden></h1>
<script type="module" src="assets/js/wyd3d.js?v={V}"></script>
</body>
</html>
"""
wr("wyd2027-3d.html", HTML)
wr("assets/js/wyd3d.js", rd("scripts/wyd3d.js"))

# 메뉴 · 맞춤 제안 목록에 링크
p = "scripts/update_nav_menu.py"; t = rd(p)
if "wyd2027-3d.html" not in t:
    t = t.replace('L("wyd2027.html", "WYD 서울 2027 제안"),', 'L("wyd2027.html", "WYD 서울 2027 제안"), L("wyd2027-3d.html", "WYD 서울 2027 · 1분 3D"),')
    wr(p, t)
p = "scripts/add_proposals_page.py"; t = rd(p)
if "wyd2027-3d.html" not in t:
    t = t.replace('"stats": [["40만", "해외 순례자(추정)"]', '"extra": ["▶ 1분 3D 제안", "wyd2027-3d.html"], "stats": [["40만", "해외 순례자(추정)"]', 1)
    wr(p, t)
p = "scripts/proposals.js"; t = rd(p)
if "p.extra" not in t:
    t = t.replace("<a class=\"btn btn-primary pp-go\" href=\"${E(p.href)}\">", "${p.extra ? `<a class=\"btn btn-ghost pp-go pp-extra\" href=\"${E(p.extra[1])}\">${E(p.extra[0])}</a>` : ''}<a class=\"btn btn-primary pp-go\" href=\"${E(p.href)}\">", 1)
    wr(p, t)
p = "scripts/proposals.css"; t = rd(p)
if ".pp-extra" not in t:
    wr(p, t + ".pp-extra{color:var(--indigo)!important;border:1px solid var(--line)!important;background:#fff!important}\n")
subprocess.run([sys.executable, str(ROOT / "scripts/add_proposals_page.py")], check=True)
print("  wyd2027-3d.html · data/wyd2027_3d.json · assets/js/wyd3d.js")
