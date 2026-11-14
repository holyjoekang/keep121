"""맞춤 제안 목록 페이지(proposals.html)를 만든다. 다시 돌려도 안전.

    python scripts/add_proposals_page.py

- data/proposals.json            제안 카드 목록 (대표 이미지 · 핵심 내용 · 자세히 보기 링크)
- proposals.html                 b2b.html 껍데기 복사 (render.js 사이트 페이지)
- content/pages/proposals.html   [data-proposals] 자리
- assets/js/proposals.js · assets/css/proposals.css  (원본 scripts/proposals.*)
- data/site.json                 페이지 순서
- scripts/update_nav_menu.py 를 이어서 돌려 메뉴 · 바닥글의 '맞춤 제안'을 갱신

새 제안을 추가할 때: ITEMS 에 카드 하나, update_nav_menu.py 의 PROPOSALS 에 한 줄을 넣고 두 스크립트를 돌린다.
"""
import datetime as dt, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")

ITEMS = [
 {"href": "wyd2027.html", "tag": "대규모 행사", "date": "2026.11", "client": "천주교 서울대교구 · WYD 서울 2027",
  "title": "WYD 서울 2027 · 40만 순례자 안전 · 안내",
  "img": "https://wizware.dnstrip.net/n/cnla9ryzc1ev/b/wydseoul-public-resources/o/assets/images/main/donate-bg-9ca49aa24f372b0c5c0661fdc9679058.webp",
  "summary": "세계청년대회에 오는 해외 순례자를 위해 KeepTrip · KeepGuide · KeepEnterprise와 Galaxy SmartTag3 공동 마케팅으로 이동 · 소통 · 안전을 한 화면에서 지킵니다.",
  "points": ["다국어 일정과 실시간 통역", "인솔자 1분 점호 · 순례자 SOS", "삼성전자 단말 스폰서 · 공동 캠페인"],
  "extra": ["▶ 1분 3D 제안", "wyd2027-3d.html"], "stats": [["40만", "해외 순례자(추정)"], ["6일", "8.3 ~ 8.8"], ["4개", "앱 · 태그 구성"]], "mix": ["Guide", "Enterprise"]},
 {"href": "jeju2027.html", "tag": "지자체 · 관광", "date": "2026.11", "client": "제주관광공사 · 제주대학교 경영학과 (안)",
  "title": "제주 방문객 이동 안전 · 중국인 단체와 수학여행",
  "img": "https://ijto.or.kr/korean/gharhksfl/pgm_slider/img/main_visual01_3.jpg",
  "summary": "외국인 방문객의 70%인 중국인 단체와 연 수만 명의 수학여행단을 위해 중국어 일정 · 실시간 통역 · 1분 점호 · 학부모 리포트를 시범 운영합니다.",
  "points": ["위챗으로 여는 중국어 일정과 실시간 통역", "수학여행 1분 점호 · 숙소 야간 점호", "관광공사 대시보드 · 1년 차 약 2억 원(안)"],
  "extra": ["▶ 1분 3D 제안", "jeju2027-3d.html"], "stats": [["224만", "2025 외국인"], ["8.7만", "상반기 수학여행"], ["8,000명", "1년 차 시범"]], "mix": ["Guide", "Enterprise"]},
 {"href": "ilsandong.html", "tag": "학교 · 교육", "date": "2026.11", "client": "일산동중학교 (경기 고양)",
  "title": "일산동중학교 현장체험학습 · 수학여행 · 바뀐 안전 지침 대응",
  "img": "https://commons.wikimedia.org/wiki/Special:FilePath/Korea-Busan-Doosong_Middle_School-02.jpg?width=1200",
  "summary": "보조인력 학급당 1명 · 교원 면책 강화 등 2026년 바뀐 지침에 맞춰, 교사와 보조인력이 같은 명단으로 1분 점호하고 안전조치 이행 기록이 자동으로 남게 합니다.",
  "points": ["담임 · 보조인력 역할 분담 1분 점호", "활동이 끝나면 안전조치 이행 기록 자동 생성", "2027학년도 연간 12회 체험 · 캠프 운영 예시"],
  "stats": [["564명", "22학급"], ["12회", "연간 체험 · 캠프"], ["무상", "첫 학기 시범"]], "mix": ["Guide", "Enterprise"]},
 {"href": "galilee.html", "tag": "여행사 · 성지순례", "date": "2026.11", "client": "갈릴리여행사",
  "title": "갈릴리여행사 · 교회 성지순례 ‘안심 순례’ 상품",
  "img": "https://commons.wikimedia.org/wiki/Special:FilePath/141151_sea_of_galilee_PikiWiki_Israel.jpg?width=960",
  "summary": "이스라엘 · 요르단, 튀르키예 · 그리스, 종교개혁지로 떠나는 교회 단체를 위해 인솔자 1분 점호 · 캐리어 인계 확인 · 교회 안심 리포트를 한 상품으로 묶었습니다.",
  "points": ["성지 · 국경 · 배 승하선마다 1분 점호", "호텔 이동 때 캐리어 자동 확인", "매일 저녁 교회 · 가족 안심 리포트"],
  "stats": [["30명", "교회 단체 예시"], ["10일", "이스라엘 · 요르단"], ["무상", "첫 2단체 시범"]], "mix": ["Guide", "Track", "Enterprise"]},
 {"href": "saga2027.html", "tag": "교회 · 시니어", "date": "2026.11", "client": "사랑글로벌아카데미 · 2027 통합",
  "title": "사랑글로벌아카데미 2027 · 레거시부터 비전트립까지",
  "img": "https://commons.wikimedia.org/wiki/Special:FilePath/Geumseoru_Gate_Pavilion_of_Gongsanseong_Fortress_(2).jpg?width=1200",
  "summary": "4.12 워커톤 · 강화 · 공주 하루 코스로 파일럿을 하고, 나가사키 · 신안 · 안동 1박 2일 · 일터선교 비전트립 · 세미나 · 포에버 · 반포종합사회복지관까지 2027 한 해를 같은 도구로 운영합니다.",
  "points": ["레거시 교재의 ‘레거시 활동’을 조별 미션으로", "워커톤 체크포인트 · 후미 확인 · 자녀 알림", "파일럿 2회 무상 → 실제 운영 1인 1만원대"],
  "stats": [["10+", "2027 여정"], ["4.12", "첫 파일럿"], ["무상", "파일럿 2회"]], "mix": ["Guide", "Track", "Enterprise"]},
 {"href": "saga-visiontrip.html", "tag": "교회 · 해외 순례", "date": "2026.11", "client": "사랑글로벌아카데미 · 일터선교아카데미",
  "title": "유럽 종교개혁 비전트립 · 9일 3개국 25명",
  "img": "https://commons.wikimedia.org/wiki/Special:FilePath/Prague_07-2016_View_from_Petrinska_Tower_img2.jpg?width=1200",
  "summary": "체코 · 독일 · 네덜란드를 버스로 잇는 9일 순례에서 일정 · 말씀 · 조별 점호 · 캐리어와 해설 수신기까지 한 흐름으로 관리합니다.",
  "points": ["그날의 일정 · 말씀 · 유적 해설을 한 화면에", "조장 4명이 조별 1분 점호, 휴게소 재탑승 확인", "캐리어 25 · 수신기 25 인계 확인과 가족 리포트"],
  "stats": [["25명", "4개 조"], ["9일", "3개국"], ["50개", "사람 · 짐 태그"]], "mix": ["Guide", "Track", "Enterprise"]},
 {"href": "saga-legacy.html", "tag": "교회 · 시니어", "date": "2026.11", "client": "사랑글로벌아카데미 · 레거시아카데미",
  "title": "레거시아카데미 1일 프로그램 · 60세 이상 순례자 안전",
  "img": "https://www.saga121.com/wp-content/uploads/2026/09/image-19.png",
  "summary": "버스로 4시간 떨어진 순례길을 하루에 다녀오는 60세 이상 생도들을 위해, 앱 없이 명찰 태그만으로 점호 · 뒤처짐 확인 · 자녀 안심 알림을 제공합니다.",
  "points": ["어르신은 명찰 태그만 — 앱 · 휴대폰 불필요", "걷기 구간 ‘후미 확인’과 야간 행사 점호", "자녀에게 출발 · 탑승 · 도착 세 번의 알림"],
  "stats": [["60+", "생도 연령"], ["1일", "당일 버스 순례"], ["무상", "첫 2회 시범"]], "mix": ["Guide", "Track"]}
]
D = {
 "updated": "2026-11-13",
 "hero": {"eyebrow": "Custom Proposals · 맞춤 제안",
          "title": "고객의 이동에 맞춘<br>Keep121 맞춤 제안.",
          "text": "행사 · 관광 · 교회 순례 · 학교마다 이동의 모습이 다릅니다. 사람(Guide) · 물건(Track) · 관제(Enterprise)를 그 현장에 맞게 조합한 제안서를 모았습니다.",
          "count": "10건 이상 준비 중",
          "img": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1800&q=75"},
 "items": ITEMS,
 "next": {"title": "우리 기관에 맞춘 제안이 필요하신가요?", "text": "학교 · 여행사 · 교회 · 복지기관 · 렌털 · 물류까지, 이동하는 사람과 물건이 있는 곳이라면 현장 일정을 받아 맞춤 제안서를 만들어 드립니다."},
 "note": "각 제안서는 검토용 초안(안)이며, 수치 · 예산 · 목표는 협의와 시범 운영으로 확정합니다. 제안서의 사진은 각 기관의 공개 자료 및 자유 이용 허락 이미지를 원본 주소로 불러옵니다.",
}
wr("data/proposals.json", json.dumps(D, ensure_ascii=False, indent=1) + "\n")

title = "맞춤 제안 · Keep121"
desc = "Keep121 맞춤 제안 모음: WYD 서울 2027, 제주 방문객 이동 안전, SaGA 유럽 종교개혁 비전트립, 레거시아카데미 1일 프로그램 등 현장별 사람 · 물건 이동 안전 제안서."
shell = rd("b2b.html")
shell = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", shell)
shell = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + desc, shell)
shell = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, shell)
shell = shell.replace("keep121/b2b.html", "keep121/proposals.html").replace('data-page="b2b"', 'data-page="proposals"')
shell = re.sub(r'\s*<link rel="stylesheet" href="assets/css/(?:b2b|b2b-inserts|proposals)\.css[^"]*">', "", shell)
shell = shell.replace("</head>", f'  <link rel="stylesheet" href="assets/css/proposals.css?v={V}">\n</head>', 1)
wr("proposals.html", shell)
wr("content/pages/proposals.html", "<!-- 맞춤 제안 목록: assets/js/proposals.js 가 data/proposals.json 으로 이 자리를 채운다. -->\n<div data-proposals></div>\n")
wr("assets/css/proposals.css", rd("scripts/proposals.css"))
wr("assets/js/proposals.js", rd("scripts/proposals.js"))

s = json.loads(rd("data/site.json"))
pages = [p for p in s["pages"] if p["id"] != "proposals"]
i = next(i for i, p in enumerate(pages) if p["id"] == "b2b") + 1
pages.insert(i, {"id": "proposals", "file": "proposals.html", "name": "맞춤 제안", "script": f"assets/js/proposals.js?v={V}"})
s["pages"] = pages
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=2) + "\n")

subprocess.run([sys.executable, str(ROOT / "scripts/update_nav_menu.py")], check=True)
print("  proposals.html · data/proposals.json · assets/js·css/proposals.* · site.json")
