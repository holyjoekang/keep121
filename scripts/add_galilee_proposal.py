"""갈릴리여행사 맞춤 제안(galilee.html)을 만든다. 다시 돌려도 안전.

    python scripts/add_galilee_proposal.py

- galilee.html · data/galilee.json (엔진: assets/js/wyd-slides.js)
- 맞춤 제안 목록(scripts/add_proposals_page.py) · 메뉴(scripts/update_nav_menu.py)에 등록

근거: 갈릴리여행사 소개(제3자 소개 페이지 기준 — 2002년 설립, 개신교 성지순례 전문, 이스라엘·요르단 구약 코스,
튀르키예·그리스 신약(바울) 코스, 유럽 종교개혁 코스, 지중해 크루즈 순례). 공식 사이트는 이 환경에서 접속이 차단되어 확인하지 못함.
Keep121 기존 인터뷰 후보 목록에 '갈릴리여행사 대표'가 있음(README). 계약 · 실증 실적은 주장하지 않는다.
사진: Wikimedia Commons(자유 이용 허락, 저작자는 원본 파일 페이지) — 성지 사진. SaGA 비전트립 제안과 같은 유럽 사진 일부 재사용.
"""
import datetime as dt, json, re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")
CM = lambda f, w=1600: "https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(f) + f"?width={w}"  # noqa: E731

IMG = {
 "galilee": CM("141151_sea_of_galilee_PikiWiki_Israel.jpg", 960),
 "kinneret": CM("117291_the_kinneret_area_PikiWiki_Israel.jpg"),
 "jerusalem": CM("Dome_of_the_Rock_by_Peter_Mulligan.jpg"),
 "oldcity": CM("106339_the_old_city_of_jerusalem_PikiWiki_Israel.jpg"),
 "deadsea": CM("Dead_Sea_by_David_Shankbone.jpg"),
 "jordan": CM("1(البحر_الميت(الاردن_02.jpg"),
 "galilee_storm": CM("-_panoramio_(2640).jpg"),
 "ephesus": CM("Ephesus_Celsus_Library_Façade.jpg"),
 "athens": CM("Attica_06-13_Athens_50_View_from_Philopappos_-_Acropolis_Hill.jpg"),
 "acropolis": CM("+_1987_wurde_die_Akropolis_Athens_Teil_des_UNESCO-Welterbes._03.jpg"),
 "prague": CM("Prague_07-2016_View_from_Petrinska_Tower_img2.jpg"),
 "wartburg": CM("Thuringia_Eisenach_asv2020-07_img23_Wartburg_Castle.jpg"),
 "worms": CM("Lutherdenkmal_Worms_01.jpg"),
 "bridge_crowd": CM("18.12.23_Prague_42_(53410227610).jpg"),
}
SRC = "사진: Wikimedia Commons (자유 이용 허락 · 저작자는 원본 파일 페이지)"
BRANDS = [["갈릴리여행사", "성지순례 전문 · 맞춤 제안"], ["Keep121", "사람·물건 이동 안전 플랫폼"]]

D = {
 "updated": "2026-11-13",
 "footer": "갈릴리여행사 성지순례 맞춤 제안 · Keep121",
 "img": IMG,
 "slides": [
  {"type": "cover", "img": "galilee", "src": SRC, "k": "맞춤 제안 · 갈릴리여행사", "brands": BRANDS,
   "title": "갈릴리 호숫가에서 예루살렘까지,<br><em>한 성도도 빠짐없이.</em>",
   "sub": "교회 성지순례 단체를 위한 인솔자 1분 점호 · 짐 인계 확인 · 성도 가족 안심 리포트 — ‘안심 순례’ 상품 제안",
   "meta": [["제안 대상", "갈릴리여행사 대표 · 인솔팀"], ["제안", "Keep121"], ["적용", "2027 봄 · 여름 순례 단체"]]},

  {"type": "glance", "img": "jerusalem", "src": SRC, "k": "Galilee Travel",
   "title": "구약 · 신약 · 종교개혁,<br><em>세 갈래 성지순례 전문.</em>",
   "lead": "2002년부터 개신교 성지순례를 전문으로 해 온 여행사입니다. 목회자가 인도하는 교회 단체가 이스라엘 · 요르단, 튀르키예 · 그리스, 유럽 종교개혁지를 순례합니다.",
   "stats": [["2002", "년", "설립 (성지순례 전문)"], ["3", "개 코스", "구약 · 신약 · 종교개혁"], ["10", "일 내외", "일반적인 순례 일정"], ["20~40", "명", "교회 단체 규모 (예시)"]],
   "days": [["구약", "이스라엘 · 요르단"], ["갈릴리", "가버나움 · 팔복교회"], ["예루살렘", "구시가지 · 골고다"], ["신약", "튀르키예 · 그리스 (바울)"], ["종교개혁", "체코 · 독일 · 스위스"], ["크루즈", "지중해 순례"]],
   "note": "출처: 갈릴리여행사 소개 페이지(제3자) — 세부 상품 · 일정은 갈릴리여행사와 확인합니다."},

  {"type": "problems", "k": "On the road", "title": "순례 인솔자가 <em>매일 마주하는 순간들.</em>",
   "items": [["oldcity", "좁은 골목 · 큰 인파", "예루살렘 구시가지 · 비아 돌로로사처럼 <b>좁고 붐비는 길</b>에서 일행이 쉽게 흩어집니다."],
             ["deadsea", "국경 · 검문소 통과", "이스라엘 · 요르단 국경, 성지 검색대마다 <b>여권 · 인원 확인</b>이 반복됩니다."],
             ["ephesus", "넓은 유적지 · 더위", "에베소 · 아크로폴리스 같은 넓은 유적에서 <b>어르신 성도의 뒤처짐 · 탈진</b>."],
             ["kinneret", "짐 · 호텔 · 선박", "매일 호텔을 옮기고 갈릴리 배 · 크루즈를 탑니다. <b>캐리어 수량 확인</b>이 끝이 없습니다."]]},

  {"type": "segments", "k": "People & Luggage", "title": "성도와 짐을 <em>함께</em> 지킵니다.",
   "items": [
     {"c": "edu", "img": "oldcity", "tag": "사람 · Keep121 Guide", "stats": [["30명", "교회 단체 (예시)"], ["60+", "어르신 비중 높음"]],
      "h": "목회자 · 인솔자가 세는 성도", "pain": ["버스 · 성지 · 검문소마다 <b>손가락 점호</b>", "구시가지 · 시장 자유시간 뒤 <b>집결 지연</b>", "현지 가이드 · 국가가 바뀔 때마다 소통", "한국의 가족 · 교회가 매일 소식 궁금"],
      "fix": "→ 1분 점호 + 미복귀 알림 + 교회 · 가족 안심 리포트"},
     {"c": "cn", "img": "kinneret", "tag": "물건 · Keep121 Track", "stats": [["30개", "캐리어"], ["매일", "호텔 이동"]],
      "h": "호텔 · 배 · 국경마다 세는 짐", "pain": ["호텔 체크아웃 · 버스 적재 <b>수량 확인</b>", "국경 통과 때 짐 분리 · 재적재", "갈릴리 배 · 크루즈 승하선", "분실 시 위치 확인 불가"],
      "fix": "→ 캐리어 태그 + QR 인계 확인"}]},

  {"type": "eco", "k": "Solution · 안심 순례 패키지", "title": "성도 · 인솔자 · 본사를 <em>하나의 흐름으로.</em>",
   "nodes": [
     {"c": "trip", "img": "galilee", "who": "성도", "h": "KeepTrip", "p": "그날의 일정 · 말씀 · 성지 해설을 한 화면에. 설치 없이 카카오톡 링크로 엽니다.", "f": ["일정 · 말씀", "성지 해설", "카톡 링크"]},
     {"c": "guide", "img": "oldcity", "who": "목회자 · 인솔자", "h": "KeepGuide", "p": "버스 · 성지 · 국경에서 1분 점호. 미복귀 성도는 마지막 확인 위치 · 반경으로.", "f": ["1분 점호", "국경 재확인", "짐 수량"]},
     {"c": "ent", "img": "jerusalem", "who": "갈릴리여행사 본사", "h": "KeepEnterprise", "p": "동시에 출발한 여러 교회 단체를 한 화면에서 보고, 교회 · 가족에게 안심 리포트를 보냅니다.", "f": ["단체별 현황", "교회 리포트", "순례 기록집"]}],
   "base": [["tag", "Galaxy SmartTag3", "성도 + 캐리어 태그 · 휴대폰이 꺼져도 마지막 위치 확인"],
            ["tr", "실시간 통역 연동", "히브리어 · 아랍어 · 튀르키예어 · 그리스어 — 시장 · 약국 · 병원에서"]]},

  {"type": "scenario", "k": "Scenario · 이스라엘 · 요르단 10일 중 7장면", "title": "인천에서 갈릴리, <em>예루살렘까지.</em>",
   "steps": [
     {"img": "jerusalem", "when": "D-30", "h": "교회 설명회", "p": "순례 설명회에서 동의 · 가족 연락처 등록, 말씀 · 일정 링크 공유.", "apps": [["trip", "KeepTrip"]]},
     {"img": "galilee", "when": "1일 차 · 인천", "h": "태그 배부", "p": "공항 집결, 성도 · 캐리어 태그를 QR로 한 번에 배부.", "apps": [["tag", "SmartTag3"]]},
     {"img": "kinneret", "when": "3일 차 · 갈릴리", "h": "배 승하선 점호", "p": "갈릴리 호수 배 승선 · 하선 때 1분 점호.", "apps": [["guide", "KeepGuide"]]},
     {"img": "deadsea", "when": "5일 차 · 국경", "h": "국경 재확인", "p": "이스라엘 → 요르단 통과 뒤 사람 · 짐 자동 재확인.", "apps": [["tag", "Track"]]},
     {"img": "oldcity", "when": "7일 차 · 구시가지", "h": "비아 돌로로사", "p": "좁은 골목 이동 중 뒤처진 성도 알림, 재집결 지점 안내.", "apps": [["guide", "KeepGuide"]]},
     {"img": "galilee_storm", "when": "매일 저녁", "h": "교회 안심 리포트", "p": "‘오늘 30명 모두 확인’ — 교회 단톡방 · 가족에게.", "apps": [["ent", "리포트"]]},
     {"img": "jordan", "when": "10일 차 · 귀국", "h": "반납 · 순례 기록집", "p": "태그 반납 확인, 말씀 · 사진 순례 기록집을 교회에 전달.", "apps": [["ent", "기록집"]]}]},

  {"type": "demo", "img": "oldcity", "src": SRC, "k": "Demo 1 · KeepGuide", "title": "인솔자는 1분 점호,<br><em>짐도 같은 화면에서.</em>",
   "points": ["버스 · 성지 · 국경마다 <b>30명을 1분 안에</b> 확인", "미복귀 성도는 <b>마지막 확인 위치 · 반경 · 경과 시간</b>", "캐리어 수량도 <b>같은 화면에서</b> 확인", "현지 가이드와 <b>통역 연결</b>"],
   "phones": [
     {"tone": "guide", "app": "KeepGuide · 인솔자", "head": "구시가지 · 다메섹 문 집결 15:00", "body": [
       {"t": "ring", "v": "29/30", "b": "1명 미확인", "s": "○○교회 성지순례 7일 차"},
       {"t": "alert", "red": True, "b": "성도 1명 · 미확인 6분", "s": "마지막 확인 4분 전 · 반경 50m · 비아 돌로로사 5처 부근"},
       {"t": "map", "img": "oldcity", "pins": [[36, 50, 30, False], [70, 40, 0, True]]},
       {"t": "btns", "items": ["전화", "가이드 호출", "통역"]},
       {"t": "item", "tm": "짐", "b": "캐리어 30/30", "s": "호텔 적재 08:10 확인", "st": "ok", "lab": "✓ 확인"}]},
     {"tone": "trip", "app": "Keep Home · 교회 안심 리포트", "head": "○○교회 성지순례 7일 차", "body": [
       {"t": "item", "tm": "08:10", "b": "호텔 출발", "s": "30명 · 캐리어 30개", "st": "ok", "lab": "✓ 확인"},
       {"t": "item", "tm": "12:20", "b": "통곡의 벽 · 점심", "s": "30명 전원 확인", "st": "ok", "lab": "✓ 확인"},
       {"t": "item", "tm": "15:08", "b": "다메섹 문 집결", "s": "30명 전원 확인", "st": "ok", "lab": "✓ 확인"},
       {"t": "alert", "b": "📖 오늘의 말씀 · 요한복음 19:17", "s": "“그들이 예수를 맡으매 예수께서 자기의 십자가를 지시고…”"},
       {"t": "txt", "s": "개별 위치는 공유하지 않고, 일정별 확인 결과만 전달합니다."}]}]},

  {"type": "dash", "k": "Demo 2 · 본사 화면", "title": "본사는 <em>동시에 출발한 교회들을 한 화면에.</em>", "mapLabel": "지중해",
   "kpis": [["4", "순례 중인 교회 단체", ""], ["118/118", "성도 확인", "g"], ["118/118", "캐리어", "g"], ["1", "미확인 (진행 중)", "r"], ["52초", "평균 점호", "y"]],
   "zones": [[8, 14, 130, "lo", "갈릴리<br>A교회 30명"], [40, 46, 130, "hi", "예루살렘<br>B교회 미확인 1"], [70, 10, 120, "md", "에베소<br>C교회 28명"], [72, 56, 110, "lo", "프라하<br>D교회 30명"]],
   "feed": [["r", "15:06 · B교회 구시가지 미확인 1명", "비아 돌로로사 부근 · 인솔자 확인 중"], ["g", "15:12 · B교회 미확인 해소", "6분 만에 합류"],
            ["", "14:40 · C교회 에베소 더위 경보", "35℃ · 그늘 휴식 안내 발송"], ["g", "13:20 · A교회 갈릴리 배 하선", "30/30 · 캐리어 버스 적재"], ["", "19:30 · 교회 안심 리포트 4건", "4개 교회 단톡방 · 가족 118명"]],
   "note": "시연용 가상 데이터입니다."},

  {"type": "benefit", "k": "Value", "title": "누구에게 <em>무엇이 좋아지나.</em>",
   "who": [["jerusalem", "갈릴리여행사", ["‘안심 순례’ 차별화 상품", "교회 재계약 · 추천 증가", "사고 · 분실 대응 비용 감소", "여러 단체를 한 화면에서"]],
           ["oldcity", "목회자 · 인솔자", ["손가락 점호 대신 1분", "국경 · 호텔마다 짐 자동 확인", "뒤처진 성도 바로 확인", "순례에 더 집중"]],
           ["galilee", "성도 (어르신)", ["오늘 일정 · 말씀 한 화면", "길을 잃어도 다시 찾는 안심", "시장 · 약국에서 통역", "귀국 후 순례 기록집"]],
           ["kinneret", "교회 · 가족", ["매일 저녁 안심 리포트", "말씀으로 함께 중보", "비상 시 연락 체계", "다음 순례 모집 자료"]]],
   "kpi": [["5분+", "1분", "단체 점호 (목표)"], ["", "5분 내", "미복귀 인지 (목표)"], ["", "0건", "캐리어 분실 (목표)"], ["", "+10%p", "교회 재계약 (목표)"]],
   "note": "목표 수치는 시범 운영에서 측정합니다. 현재 실증 · 계약 실적을 의미하지 않습니다."},

  {"type": "budget", "k": "Price (안)", "title": "성도 1인 1만원대, <em>첫 2단체는 무상.</em>",
   "lead": "30명 교회 단체 · 10일 순례 1회 기준 예시",
   "rows": [["KeepGuide · KeepTrip", 27, "1인 8,900원 × 30명"], ["SmartTag3 대여", 18, "성도 30 + 캐리어 30 = 60개 × 3,000원"],
            ["교회 · 가족 리포트", 3, "10일 × 30가정"], ["순례 기록집", 5, "말씀 · 사진 PDF 1부"]],
   "totNote": "첫 2단체는 Keep121 시범 운영으로 무상",
   "funds": [["2027 봄 2단체", "무상", "Keep121 실증 파트너"], ["이후 단체", "1인 약 1.8만원", "순례 경비에 포함 (상품가의 1% 미만)"], ["여행사 마진", "협의", "안심 순례 옵션으로 판매"]],
   "unit": [["약 1.8만원", "성도 1인 10일"], ["0원", "첫 2단체"]],
   "note": "추정(안)입니다. 가격 · 범위는 갈릴리여행사와 협의해 확정합니다."},

  {"type": "rules", "k": "Principles & Roadmap", "title": "성도의 정보는 <em>순례 기간에만.</em>",
   "items": [["본인 동의", "설명회에서 본인 동의를 받고, 리포트는 교회 · 지정한 가족에게만 보냅니다."],
             ["민감 정보 제외", "건강 · 기도제목은 저장하지 않고 일정과 확인 결과만 다룹니다."],
             ["귀국 후 파기", "귀국 30일 안에 위치 기록을 파기하고, 순례 기록집만 남깁니다."]],
   "road": [["2026.12", "대표 인터뷰", "인솔 현장 문제 · 비용 확인", False], ["2027.1~2", "상품 설계", "안심 순례 옵션 · 가격", False],
            ["2027.3~4", "시범 ① 이스라엘", "교회 1단체 무상 운영", True], ["2027.5~6", "시범 ② 튀르키예 · 그리스", "교회 1단체 무상 운영", False],
            ["2027.7~8", "종교개혁 코스", "여름 순례 적용", False], ["2027.9", "결과 · 확대", "재계약률 · 만족도 보고", False]],
   "imgs": ["ephesus", "athens", "wartburg", "prague"]},

  {"type": "close", "img": "galilee_storm", "src": SRC, "k": "제안 사항", "title": "갈릴리여행사에 <em>제안드립니다.</em>",
   "ask": ["대표 · 인솔팀 인터뷰 (현장 문제 · 비용 확인)", "2027 봄 · 여름 교회 2단체 무상 시범", "‘안심 순례’ 옵션 공동 상품화", "교회 설명회용 안내 자료 공동 제작"],
   "close": "“바다를 잔잔하게 하신 그분처럼,”<br><em>모든 성도가 함께 돌아오는 순례.</em>", "contact": "Keep121 · Every one, kept."}
 ]
}
wr("data/galilee.json", json.dumps(D, ensure_ascii=False, indent=1) + "\n")

title = "갈릴리여행사 성지순례 맞춤 제안 · Keep121"
desc = "갈릴리여행사 맞춤 제안: 이스라엘 · 요르단, 튀르키예 · 그리스, 종교개혁 성지순례 교회 단체를 위한 1분 점호 · 캐리어 인계 확인 · 교회 안심 리포트 '안심 순례' 상품."
h = rd("ilsandong.html")
h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h, count=1)
h = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + desc, h)
h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, h)
h = re.sub(r'(<meta property="og:url" content="[^"]*/)[^"/]*"', lambda m: m.group(1) + 'galilee.html"', h)
h = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + IMG["galilee"], h)
h = re.sub(r'data-src="[^"]*"', 'data-src="data/galilee.json"', h)
h = re.sub(r"data/\w+\.json → assets/js/wyd-slides\.js 가 그린다\. 원본 생성: scripts/\w+\.py",
           "data/galilee.json → assets/js/wyd-slides.js 가 그린다. 원본 생성: scripts/add_galilee_proposal.py", h)
wr("galilee.html", h)
print("  galilee.html · data/galilee.json")
