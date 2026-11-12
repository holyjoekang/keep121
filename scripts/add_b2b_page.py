"""B2B 확장 전략 페이지(b2b.html)를 붙인다. 다시 돌려도 안전.

    python scripts/add_b2b_page.py

- data/b2b.json               본문 데이터 (Sensing 기반 Guide·Track·Enterprise 확장 전략)
- b2b.html                    modoo.html 껍데기 복사 (제목·SEO·data-page)
- content/pages/b2b.html      [data-b2b] 자리 — assets/js/b2b.js 가 data/b2b.json 으로 그린다
- assets/css/b2b.css          페이지 전용 스타일 (껍데기에 링크)
- data/site.json              메뉴(국내 시장 다음)·페이지 순서·바닥글
- usecases/product/evidence   관련 섹션에 안내 한 줄
"""
import datetime as dt, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")

D = {
 "updated": "2026-11-12",
 "nav": [["view", "핵심 관점"], ["sensing", "Sensing"], ["fit", "진입 기준"], ["precision", "정밀도·중첩"], ["markets", "10개 시장"], ["prospects", "잠재고객"], ["focus", "초기 3개 시장"], ["model", "사업 모델"], ["roadmap", "로드맵"], ["plan", "30일 계획"], ["direction", "최종 방향"]],
 "hero": {"eyebrow": "B2B Expansion · Sensing 기술 기반 확장 전략",
   "title": "사람의 이동 안전관리에서<br>물품·장비·자산 추적까지.",
   "text": "단체 이동 안전관리(Guide)와 수하물·물품 추적관리(Track)를 결합해 더 넓은 B2B 시장으로 확장합니다. 세 상품 모두 공통 기반기술 Keep121 Sensing 위에서 동작합니다.",
   "route": [["guide", "Keep121 Guide", "사람·단체 이동 안전관리"], ["track", "Keep121 Track", "수하물·장비·물품 추적"], ["ent", "Keep121 Enterprise", "통합 관제·API·분석"]]},
 "view": {"no": "", "yes": "기업·기관이 관리해야 하는 사람·물품·장비의 이동 상태를 통합 관리하는 플랫폼으로 발전한다",
   "cards": [["guide", "기존 · Keep121 Guide", "단체 이동 안전관리. 인원 점호, 이탈 확인, 복귀 관리."], ["track", "신규 · Keep121 Track", "수하물·물품 추적관리. 출고, 인계, 회수, 분실 방지."]]},
 "sensing": {"title": "서비스 기업이 아닌<br>Sensing 기술 기업으로.",
   "layers": [["서비스", "고객이 쓰는 상품", ["Guide", "Track", "Enterprise"], False],
              ["Keep121 Sensing", "핵심 기반기술", ["위치 오차 보정", "대상별 최적 센서 선택", "기술 중첩(Fusion)", "최적화 솔루션 조합"], True],
              ["센서", "교체·추가 가능한 입력", ["SmartTag3", "GPS", "능동형 RFID", "QR"], False]],
   "why": "같은 서비스를 해도 기술 기업으로 포지셔닝할 때 평가가 높아집니다. 강점은 특정 센서가 아니라, 여러 센서 중 가장 적합한 조합을 찾아내고 오차를 보정하는 능력입니다."},
 "fit": {"title": "세 가지 질문에 모두<br>“예”인 시장부터.",
   "qs": ["추적해야 할 대상이 많고 반복적으로 이동하는가?", "분실·이탈·인계 누락으로 인한 운영 손실이 발생하는가?", "문제 해결을 위해 실제 예산을 집행할 기업·기관이 존재하는가?"],
   "stackNote": "SmartTag3는 위치 갱신이 불규칙할 수 있어, 산업별로 센서를 중첩·조합합니다.",
   "stack": ["QR 인계관리", "SmartTag 위치확인", "GPS 선택 적용", "능동형 RFID"]},
 "precision": {"title": "사람은 ‘범위’, 물건은 ‘위치’.",
   "bars": [["QR · 능동형 RFID", 4, "ink", "지점·구역 확정"], ["GPS", 33, "guide", "10~20m"], ["SmartTag3", 83, "track", "약 50m + 갱신 지연"]],
   "cards": [["guide", "사람 · Guide", "반경만 알면 충분합니다. 근처에 가서 찾으면 되므로 GPS 수준의 10~20m 오차는 큰 문제가 아닙니다.", "핵심: 이탈했는가, 복귀했는가"],
             ["track", "물건 · Track", "정확한 위치와 인계 시점이 필요합니다. 회수·미반납 판단은 ‘어디 근처’로는 부족합니다.", "핵심: 어디에 있고, 누구에게 넘어갔는가"]],
   "fusionTitle": "가장 간단한 해법은 기술을 중첩하는 것",
   "fusion": [["QR 인계", "인계 시점과 담당자를 확정", "스캔 행동 필요, 실시간 아님", "모든 인계 증명"],
              ["SmartTag3", "저비용, 별도 인프라 불필요", "주변 갤럭시 의존, 약 50m 오차, 갱신 지연", "수하물·소지품"],
              ["GPS", "독립적인 실시간 위치, 10~20m", "배터리·단가, 실내에 약함", "사람·단체 이동"],
              ["능동형 RFID", "리더 구역 내 자동 인식, 대량 일괄 확인", "리더·게이트 설치 필요", "전시·행사 장비 렌털"]],
   "flow": ["센서별 수집", "위치 오차 보정", "대상·환경별 최적 조합 선택", "범위 또는 위치로 출력"],
   "gapTitle": "통제할 수 없는 지연은 서비스로 메운다",
   "test": {"lead": "핸드백에 태그를 넣고 확인한 결과", "found": ["현재 위치는 정확", "업데이트는 늦음"],
            "cause": ["주변 갤럭시 단말이 감지하는 구조라 약 50m 오차", "보안 구조로 인한 전송 지연 가능성"],
            "note": "삼성 인프라 영역이라 기술적 주도권이 우리에게 없음"},
   "fix": [["QR 체크포인트", "로 탑승·인계 시점을 확정"], ["마지막 확인 위치와 경과 시간", "을 함께 표시 (예: “7분 전, 반경 50m”)"],
           ["확인 요청 알림", " — 갱신이 일정 시간 없으면 인솔자·담당자에게"], ["GPS·능동형 RFID로 보강", " — 정밀도가 필요한 구간만"]]},
 "markets": {"title": "확장 가능한 B2B 시장<br>10개 전략 평가.",
   "rows": [["공항·호텔 수하물 배송", "배송 운영사·호텔", "Track", 4.5, False], ["전시·행사 장비 렌털", "장비 렌털사·행사 대행사", "Track·RFID", 4.5, True],
            ["단체여행·성지순례", "여행사·교회·기관", "Guide", 4.5, False], ["학교 현장체험학습", "학교·교육청·여행사", "Guide", 4.0, False],
            ["IT·산업 장비 렌털", "기업 렌털사", "Track", 4.0, False], ["의료기기 대여·회수", "의료기기 렌털사", "Track", 3.5, False],
            ["복지시설 외부활동", "복지관·요양시설", "Guide", 3.5, False], ["기업 행사·해외 연수", "기업·연수 운영사", "Guide", 3.5, False],
            ["물류 회수용 자산", "3PL·운송사", "Track", 3.0, False], ["건설·현장 공용장비", "건설사·장비 렌털사", "Track", 3.0, False]],
   "note": "평가는 시장 규모 통계가 아니라 초기 고객 확보 가능성, 문제의 심각성, 기술 적합성, 수익화 가능성을 기준으로 한 전략적 판단(5점 만점)입니다.",
   "vsTitle": "전시·행사 장비 렌털이 경제성에서 앞선다",
   "vs": [["Track", "공항 수하물", ["고객 편익이 분명함", "태그 부착·반납에 추가 작업이 발생"], False],
          ["주목", "렌털 장비", ["기업이 자산을 직접 소유", "반복적으로 회수 → 태그 재사용 가능", "자산관리 경제성 확보에 유리", "능동형 RFID로 반입·반출 자동 인식 가능"], True]],
   "edu": "2026학년도 현장체험학습 운영 매뉴얼이 인솔 인력, 안전요원, 안전관리 계획 등을 상세히 규정하고 있어, 학교 현장의 안전관리 지원 소프트웨어 수요를 검증할 근거가 있습니다."},
 "prospects": {"title": "실제 발굴한 B2B 잠재고객.",
   "rentalTitle": "서울의 장비 렌털 기업 5곳",
   "rental": [["알앤텍", "PC, 영상·음향, 행사·전시 장비 B2B 렌털. 행사별 출고·설치·회수 및 미반납 관리에 적용.", "강남구 삼성로 555", "고가 렌털 장비 30~50대 회수관리 PoC", True],
              ["한국렌탈", "IT·계측·산업 장비 렌털과 자산관리. 기존 자산관리 시스템에 위치정보·인수인계 이벤트 추가.", "성동구 연무장11길 10, 3층", "계측장비·공용장비 이동 이력관리", False],
              ["스마트렌탈 렌트닷컴", "스마트기기 대량 렌털, 행사·교육용 장비 배송·회수. 소규모 실증에 적합.", "중구", "교육·전시용 태블릿 배송 및 반납관리", False],
              ["이레렌탈", "전시회 장비·비품 렌털. 전시장 반입·반출 및 장비 인계관리 검증에 적합.", "강남구 영동대로 513, 코엑스 4층", "전시행사 단위 장비 위치·회수 대시보드", False],
              ["(주)유유테이진메디케어", "가정용 의료기기 대여·설치·점검. 장비 회수 및 서비스 이력관리 시장 후보.", "중구 동호로15길 27", "의료기기 회수·재배치 이력관리", False]],
   "caveat": "공개 사업자 정보 기반으로 선정했으며 도입 의사·예산은 미확인입니다. 기존 추적 솔루션, 실제 분실률, 구매 의사는 인터뷰로 확인합니다.",
   "districts": [["강남구", 2], ["중구", 2], ["성동구", 1]],
   "logiTitle": "공항 수하물 흐름을 함께 검증할 두 파트너",
   "logi": [["서울도시철도엔지니어링 · 또타러기지", "수하물 배송 서비스 운영", "QR 접수·배송조회·공항 인계 시스템에 <b>가방별 위치정보</b>를 결합하는 PoC를 제안합니다.", "", "https://www.tluggage.co.kr/", "tluggage.co.kr"],
            ["한진", "B2B 물류 및 공항 수하물 서비스", "또타러기지의 공항 수령 과정과 연결되는 <b>인계 증명·배송 추적</b>을 공동 검증할 후보입니다.", "기존 화물추적 역량을 보유하고 있어, 중복 기능이 아닌 보완 가치를 제시해야 합니다.", "https://www.hanjin.com/", "hanjin.com"]],
   "guideTitle": "기존 Guide 고객 확대 — 이미 확보한 네트워크부터",
   "guide": [["사랑의교회 단체여행·성지순례 운영", "버스 승하차 자동 점호"], ["사랑글로벌아카데미", "단체 현장학습 출석·이동 관리"], ["갈릴리여행사", "여행 인솔자용 위치·복귀 확인"],
             ["일산 지역 중학교", "수학여행·현장체험학습 안전관리"], ["제주 지역 여행사", "단체관광 인원·수하물 통합 관리"], ["복지관·주간보호센터", "외부활동 참여자 출석·복귀 확인"]],
   "guideNote": "기존에 논의한 인터뷰·실증 후보이며, 계약이 확보된 고객은 아닙니다.",
   "privacy": "보호자 동의, 정보 보유기간, 접근 권한, 긴급상황 대응절차. SmartTag3의 소비자용 분실방지 기능을 사람의 상시 안전추적 수단으로 그대로 사용해서는 안 됩니다."},
 "focus": [["guide", "단체여행·교육기관", "가장 빠른 실증", "기존 Keep121 Guide 개발 성과와 인터뷰 네트워크를 그대로 활용할 수 있습니다."],
           ["track", "전시·IT 장비 렌털", "정량화 용이", "고가 장비의 회수·분실·인계관리 문제를 수치로 보여주기 쉽고, 태그 재사용이 가능합니다. 능동형 RFID 게이트로 반입·반출 확인을 자동화할 수 있습니다."],
           ["tag", "공항 수하물 배송", "대표 사례", "삼성전자에 제시할 대표 B2B 활용 사례로 적합하지만, 배송 운영사와의 시스템 연계가 필요합니다."]],
 "model": {"products": [["guide", "Keep121 Guide", "사람·단체 이동 안전관리", "행사·여행 단위 이용료"], ["track", "Keep121 Track", "수하물·장비·물품 추적", "자산 수량 기반 구독료"], ["ent", "Keep121 Enterprise", "통합 관제·API·분석", "기업별 구축비 + SaaS"]],
   "platform": "공통 기반기술 Keep121 Sensing(위치 보정·센서 최적 조합)을 사용하되, 고객별 권한·개인정보·업무 프로세스는 분리합니다."},
 "roadmap": [["1단계 · 현재", "QR 인계 + SmartTag3", "Guide 실증, 수하물 PoC"], ["2단계", "GPS 선택 적용", "오차 보정과 갱신 지연 보완 로직"],
             ["3단계", "능동형 RFID 도입", "전시·행사 장비 렌털의 반입·반출 자동 인식"], ["4단계", "Sensing Fusion 엔진", "대상·환경별 최적 센서 조합 자동 선택, Enterprise API"]],
 "plan": [["1주 차", "또타러기지, 알앤텍, 한국렌탈 등 5개 기업에 인터뷰 요청"], ["2주 차", "단체여행·교육기관 기존 접점 3곳과 요구사항 인터뷰"],
          ["3주 차", "고객별 문제 비용을 산정하고 QR 중심 MVP, SmartTag 확장형, 능동형 RFID 적용안 비교"], ["4주 차", "유료 PoC 의향이 가장 높은 고객 1~2곳 선정, 삼성전자 협력 제안서 보완"]],
 "ask": {"no": "“실시간 위치를 보고 싶습니까?”", "yes": "“현재 물품이나 인원을 찾고 확인하는 데 얼마나 많은 시간과 비용이 발생합니까?”",
   "note": "원하는 기능이 아니라 이미 치르고 있는 비용을 물어야 실제 구매 가능성을 더 잘 구분할 수 있습니다."},
 "direction": {"en": "People &amp; Asset Movement Assurance Platform", "ko": "사람과 자산의 이동·인계 신뢰성 관리 플랫폼",
   "flow": [["now", "단체여행 실증 지속"], ["add", "렌털 장비 관리 검증"], ["add", "공항 수하물 배송 검증"]],
   "have": "실제 사업을 운영하는 잠재고객 목록과 고객 문제에 대한 가설", "next": "문제 발생 빈도, 지불 의사, 구매 의사결정자 → 실질적인 영업 파이프라인으로 전환",
   "close": "10개 산업에 한꺼번에 진출하지 않고 단계적으로 검증해, 삼성전자에는 단순한 수하물 추적 앱이 아닌 여러 산업에 재사용 가능한 Sensing 기술 기반 B2B 플랫폼으로 제안합니다."}
}
wr("data/b2b.json", json.dumps(D, ensure_ascii=False, indent=1) + "\n")

# 껍데기
title = "B2B 확장 전략 · Keep121"
desc = "Sensing 기술 기반 Keep121 B2B 확장: 단체 이동 안전관리(Guide)에서 수하물·장비·자산 추적(Track), 통합 관제(Enterprise)까지 — 10개 시장 평가, 잠재고객, 30일 실행 계획."
shell = rd("modoo.html")
shell = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", shell)
shell = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + desc, shell)
shell = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, shell)
shell = shell.replace("keep121/modoo.html", "keep121/b2b.html").replace('data-page="modoo"', 'data-page="b2b"')
shell = re.sub(r'\s*<link rel="stylesheet" href="assets/css/b2b\.css[^"]*">', "", shell)
shell = shell.replace("</head>", f'  <link rel="stylesheet" href="assets/css/b2b.css?v={V}">\n</head>', 1)
wr("b2b.html", shell)
wr("content/pages/b2b.html", "<!-- B2B 확장 전략: assets/js/b2b.js 가 data/b2b.json 으로 이 자리를 채운다. -->\n<div data-b2b></div>\n")
wr("assets/css/b2b.css", rd("scripts/b2b.css"))
wr("assets/js/b2b.js", rd("scripts/b2b.js"))

# 메뉴·페이지 순서·바닥글
s = json.loads(rd("data/site.json"))
if not any(n["href"] == "b2b.html" for n in s["nav"]):
    i = next(i for i, n in enumerate(s["nav"]) if n["href"] == "usecases.html") + 1
    s["nav"].insert(i, {"href": "b2b.html", "label": "B2B 확장"})
pages = [p for p in s["pages"] if p["id"] != "b2b"]
i = next(i for i, p in enumerate(pages) if p["id"] == "usecases") + 1
pages.insert(i, {"id": "b2b", "file": "b2b.html", "name": "B2B 확장 전략", "script": f"assets/js/b2b.js?v={V}"})
s["pages"] = pages
for c in s["footer"]["columns"]:
    if any(l["href"] == "usecases.html" for l in c["links"]) and not any(l["href"] == "b2b.html" for l in c["links"]):
        j = next(j for j, l in enumerate(c["links"]) if l["href"] == "usecases.html") + 1
        c["links"].insert(j, {"href": "b2b.html", "label": "B2B 확장 전략"})
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=2) + "\n")

# 관련 섹션에 안내 한 줄
def note(page, anchor_re, html, before):
    p = f"content/pages/{page}.html"
    t = rd(p)
    if 'data-b2b-link' in t:
        t = re.sub(r'<p class="notice[^"]*" data-b2b-link>.*?</p>\n', "", t, flags=re.S)
    m = re.search(anchor_re, t, flags=re.S)
    if not m:
        raise SystemExit(f"{page}: anchor not found")
    k = m.start() if before else m.end()
    wr(p, t[:k] + f'<p class="notice mt-s" data-b2b-link><svg class="icon"><use href="#i-route"/></svg><span>{html}</span></p>\n' + t[k:])

note("usecases", r'<section class="soft" id="expansion">.*?(?=<div class="stages">)',
     '<b>2026.11 B2B 확장</b> · 사람(Guide)에서 수하물·장비·자산(Track)으로 넓히는 10개 B2B 시장 평가와 실제 잠재고객은 <a href="b2b.html#markets">B2B 확장 전략</a>에 정리했습니다.', False)
note("product", r'<section id="lineup">\s*<div class="wrap">',
     '<b>Keep121 Track · Enterprise</b> · Guide와 같은 Sensing 기반 위에서 수하물·장비 추적(Track)과 통합 관제·API(Enterprise)를 더하는 계획은 <a href="b2b.html#model">B2B 확장 전략</a>을 참고하세요.', False)
note("evidence", r'<section class="v-soft" id="location-roadmap-2026"><div class="wrap">.*?</h2>',
     '<b>Sensing 로드맵 · 30일 실행</b> · QR+SmartTag3 → GPS → 능동형 RFID → Fusion 엔진 단계와 렌털·수하물 잠재고객 인터뷰 계획은 <a href="b2b.html#roadmap">B2B 확장 전략</a>에 있습니다.', False)
print("  b2b.html · content/pages/b2b.html · data/b2b.json · assets/js/b2b.js · assets/css/b2b.css · site.json · usecases/product/evidence")
