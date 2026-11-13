"""사랑글로벌아카데미(SaGA) 맞춤 제안 2건을 만든다. 다시 돌려도 안전.

    python scripts/add_saga_proposals.py

- saga-visiontrip.html · data/saga_visiontrip.json   유럽 종교개혁 비전트립 (체코·독일·네덜란드 9일)
- saga-legacy.html     · data/saga_legacy.json       레거시아카데미 1일 프로그램 (60세 이상, 당일 버스 순례)
- 엔진: assets/js/wyd-slides.js (WYD·제주 제안과 같은 슬라이드 엔진)

근거: 2023 SaGA 유럽 여름 비전트립 운영 문서(일정·여행사 설명회 내용만 사용, 참가자 이름·기도제목 등 개인 정보는 쓰지 않음),
      2026 SaGA STORY 5월호(레거시아카데미 신안 섬티아고 12사도 순례길).
사진: Wikimedia Commons(자유 이용 허락, 파일별 저작자 표기는 원본 페이지), SaGA STORY, 제주관광공사(분위기 이미지).
"""
import datetime as dt, json, re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731

CM = lambda f, w=1600: f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(f)}?width={w}"  # noqa: E731
SG = "https://www.saga121.com/wp-content/uploads/2026/09/"
PH = "https://api.cdn.visitjeju.net/photomng/thumbnailpath/"
MV = "https://api.cdn.visitjeju.net/mainVisualBanner/imageFile/"
IJ = "https://ijto.or.kr/korean/gharhksfl/pgm_slider/img/"

EU = {
 "prague": CM("Prague_07-2016_View_from_Petrinska_Tower_img2.jpg"),
 "bridge_night": CM("Charles_Bridge_at_night_-_Prague_01.jpg"),
 "bridge_crowd": CM("18.12.23_Prague_42_(53410227610).jpg"),
 "oldtown": CM("Prague_07-2016_View_from_Old_Town_Hall_Tower_img3.jpg"),
 "wartburg": CM("Thuringia_Eisenach_asv2020-07_img23_Wartburg_Castle.jpg"),
 "wartburg2": CM("WartburgBeiEisenach.jpg"),
 "zaanse": CM("The_Windmills_of_Zaanse_Schans,_Netherlands.jpg"),
 "amsterdam": CM("Amsterdam_airphoto.jpg"),
 "peace": CM("Friedenspalast_Den_Haag_(100MP).jpg"),
 "peace_night": CM("Peace_Palace_by_Night.jpg"),
 "worms": CM("Lutherdenkmal_Worms_01.jpg"),
 "koln": CM("Kölner_Dom_nachts_2013.jpg"),
 "heidelberg": CM("Heidelberg-Schloß.JPG", 960),
}
LG = {
 "saga_group": SG + "image-17.png",
 "saga_group@pos": "center 0%",
 "saga_night": SG + "image-19.png",
 "trail": PH + "201804/30/e9cb50d3-bb50-4f68-b6ae-05887ec8715d.webp",
 "hike": PH + "202610/13/5ebd8b61-3471-4eb3-ba64-0957ab2d89d5.webp",
 "silver": PH + "202608/27/903c7ad6-c63b-4ef3-bb70-d805d983c0b5.webp",
 "palmpath": PH + "202609/04/90740fb3-90fc-4fc9-864b-b4ef9b0e041f.webp",
 "cliff": PH + "202610/28/d204473d-69e8-47a4-abd6-769798d3295f.webp",
 "meadow": PH + "202611/04/b3fc2f68-86ee-4b38-8951-e133bf47ebc8.webp",
 "bus": PH + "202312/14/bb73e832-d77a-4f72-982b-51ae7dd91d48.webp",
 "coastwide": MV + "202611/06/a03427fb-5ab6-406b-ae9d-995d2c7f97e4.webp",
 "palmroad": MV + "202609/16/96145590-1394-431f-92b5-40d0373141e2.webp",
 "sunrise": IJ + "main_visual02_3.jpg",
 "sunset": IJ + "main_visual03_2.jpg",
 "hill": IJ + "main_visual01_3.jpg",
}
SRC_EU = "사진: Wikimedia Commons (자유 이용 허락 · 저작자는 원본 파일 페이지)"
SRC_LG = "사진: SaGA STORY 2026 5월호 · 제주관광공사 (분위기 이미지)"
BRANDS = [["사랑글로벌아카데미 SaGA", "맞춤 제안"], ["Keep121", "사람·물건 이동 안전 플랫폼"]]

VISION = {
 "updated": "2026-11-13",
 "footer": "SaGA 유럽 종교개혁 비전트립 맞춤 제안 · Keep121",
 "img": EU,
 "slides": [
  {"type": "cover", "img": "prague", "src": SRC_EU, "k": "맞춤 제안 · SaGA 일터선교&글로벌네트워크아카데미", "brands": BRANDS,
   "title": "종교개혁의 길 9일,<br><em>25명 모두 함께</em><br>걷고 돌아오도록.",
   "sub": "유럽 종교개혁 비전트립(체코·독일·네덜란드)을 위한 일정·말씀·인원·짐 통합 관리 제안",
   "meta": [["제안 대상", "사랑글로벌아카데미 SaGA"], ["제안", "Keep121"], ["적용", "차기 비전트립 (2027 여름 안)"]]},

  {"type": "glance", "img": "oldtown", "src": SRC_EU, "k": "2023 SaGA Pilgrim 돌아보기",
   "title": "9일, 3개국, 10여 개 도시.<br><em>하루 2~3곳을 버스로 옮겨 다녔습니다.</em>",
   "lead": "2023년 8월 SaGA Pilgrim은 얀 후스(체코) · 마르틴 루터(독일) · 아브라함 카이퍼(네덜란드)의 발자취를 한 대의 코치버스로 따라갔습니다.",
   "stats": [["25", "명", "최종 참가자"], ["4", "개 조", "조장 4명"], ["9", "일", "8.12 ~ 8.20"], ["3", "명", "국가별 현지 가이드"]],
   "days": [["1일 · 프라하", "인천 T2 집결 → 프라하 도보투어"], ["2일 · 프라하", "프라하성 · 베들레헴교회 · 카를교"], ["3일 · 비텐베르크", "95개조 성안교회 → 아이슬레벤 → 에르푸르트"],
            ["4일 · 아이제나흐", "바르트부르크 성 → 프랑크푸르트"], ["5일 · 보름스→쾰른", "보름스 · 하이델베르크 · 쾰른 260km"], ["6~9일 · 네덜란드", "잔세스칸스 · 암스테르담 · 헤이그 → 귀국"]],
   "note": "출처: 2023 SaGA 유럽 여름 비전트립 운영 문서 (일정 · 여행사 설명회 내용)"},

  {"type": "problems", "k": "What organizers juggle", "title": "인솔자가 9일 동안 <em>챙겨야 했던 것들.</em>",
   "items": [["bridge_crowd", "인파 속 자유시간", "카를교 · 담 광장처럼 붐비는 곳의 자유시간 뒤 <b>집결 지연</b>. 소매치기 때문에 가방은 늘 앞으로."],
             ["heidelberg", "하루 3개 도시 이동", "보름스 → 하이델베르크 → 쾰른 260km. 휴게소(유료 화장실 1유로)마다 <b>재탑승 확인</b>."],
             ["wartburg", "짐 · 해설 수신기", "23kg 캐리어 25개, 공항에서 배부하고 귀국 때 반납하는 해설 수신기 25대. <b>하나라도 없으면 일정이 멈춥니다</b>."],
             ["koln", "흩어진 정보", "일정 · 호텔 · 말씀 · 기도문 · 공지가 단톡방과 문서에 흩어져 <b>그때그때 찾기 어렵습니다</b>."]]},

  {"type": "segments", "k": "People & Things", "title": "비전트립은 <em>사람과 짐이 함께</em> 움직입니다.",
   "items": [
     {"c": "edu", "img": "bridge_night", "tag": "사람 · Keep121 Guide", "stats": [["25명", "참가자"], ["4개 조", "조장 4명"]],
      "h": "조장이 매번 세는 25명", "pain": ["버스 · 유적지 · 휴게소마다 <b>손가락 점호</b>", "자유시간 뒤 미복귀, 어르신 · 첫 해외 순례자의 길 잃음", "국가별로 바뀌는 현지 가이드와의 소통", "한국의 가족은 하루 소식이 궁금"],
      "fix": "→ 조별 1분 점호 + 미복귀 알림 + 가족 안심 리포트"},
     {"c": "cn", "img": "amsterdam", "tag": "물건 · Keep121 Track", "stats": [["25개", "캐리어 23kg"], ["25대", "해설 수신기"]],
      "h": "호텔을 옮길 때마다 세는 짐", "pain": ["공항 배부 · 반납 때 <b>수량 확인</b>", "호텔 체크아웃 · 버스 적재마다 캐리어 확인", "수신기 충전 · 분실", "여권 가방은 소매치기의 표적"],
      "fix": "→ 캐리어 · 수신기 태그 + QR 인계 확인"}]},

  {"type": "eco", "k": "Solution", "title": "참가자 · 조장 · 본부를 <em>하나의 흐름으로.</em>",
   "nodes": [
     {"c": "trip", "img": "worms", "who": "참가자 25명", "h": "KeepTrip", "p": "그날의 일정 · 호텔 · 말씀 · 기도문 · 유적 해설을 한 화면에. 단톡방 공지는 링크 하나로 정리합니다.", "f": ["일정 · 호텔", "오늘의 말씀", "유적 해설"]},
     {"c": "guide", "img": "bridge_crowd", "who": "조장 4명", "h": "KeepGuide", "p": "버스 · 유적지 · 휴게소에서 조별 1분 점호. 미복귀자는 마지막 확인 위치 · 반경과 함께 알립니다.", "f": ["조별 점호", "재탑승 확인", "짐 · 수신기"]},
     {"c": "ent", "img": "peace", "who": "인솔 본부", "h": "KeepEnterprise", "p": "4개 조와 짐 현황을 한 화면에서 보고, 가족 안심 리포트와 순례 기록집을 자동으로 만듭니다.", "f": ["본부 대시보드", "가족 리포트", "순례 기록집"]}],
   "base": [["tag", "Galaxy SmartTag3", "사람 25 + 캐리어 25 · 휴대폰이 꺼져도 마지막 위치 확인"],
            ["tr", "실시간 통역 연동", "체코어 · 독일어 · 네덜란드어 — 식당 · 상점 · 약국에서 바로 대화"]]},

  {"type": "scenario", "k": "Scenario · 9일 중 7장면", "title": "인천에서 헤이그까지, <em>모두 함께.</em>",
   "steps": [
     {"img": "peace_night", "when": "D-30", "h": "준비를 한곳에", "p": "사전 기도회 일정, 준비물 · 짐 규정(23kg/8kg), 보험 안내를 체크리스트로.", "apps": [["trip", "KeepTrip"]]},
     {"img": "prague", "when": "1일 차 · 인천 T2", "h": "집결 · 태그 배부", "p": "3층 C카운터 집결 확인, 사람 · 캐리어 태그와 수신기를 QR로 한 번에 배부.", "apps": [["tag", "SmartTag3"]]},
     {"img": "bridge_crowd", "when": "2일 차 · 프라하", "h": "카를교 자유시간", "p": "집결 15분 전 알림, 미복귀자는 조장에게 마지막 위치 범위로.", "apps": [["guide", "KeepGuide"]]},
     {"img": "worms", "when": "5일 차 · 보름스", "h": "말씀과 해설", "p": "루터 기념비 앞에서 그날의 말씀과 유적 해설을 한 화면으로.", "apps": [["trip", "KeepTrip"]]},
     {"img": "heidelberg", "when": "5일 차 · 260km", "h": "휴게소 재탑승", "p": "버스 출발 전 25/25 자동 확인, 미탑승자만 표시.", "apps": [["guide", "KeepGuide"]]},
     {"img": "amsterdam", "when": "7일 차 · 암스테르담", "h": "짐 · 수신기 점검", "p": "호텔 이동 때 캐리어 25개 적재, 수신기 수량 · 충전 확인.", "apps": [["tag", "Track"]]},
     {"img": "peace_night", "when": "8~9일 차 · 귀국", "h": "반납 · 순례 기록집", "p": "공항에서 태그 · 수신기 반납 확인, 9일의 말씀 · 사진으로 기록집.", "apps": [["ent", "기록집"]]}]},

  {"type": "demo", "img": "wartburg", "src": SRC_EU, "k": "Demo 1 · KeepTrip", "title": "오늘의 일정과 말씀을<br><em>한 화면에.</em>",
   "points": ["일정 · 호텔 · 말씀 · 기도문 · 유적 해설이 <b>하루 한 화면</b>", "담당 목사님의 묵상 자료를 <b>일정에 맞춰 공개</b>", "버스 출발 · 집결 시간을 <b>미리 알림</b>", "단톡방 공지는 KeepTrip 링크 하나로"],
   "phones": [{"tone": "trip", "app": "KeepTrip · SaGA Pilgrim 5일 차", "head": "8/16(수) 보름스 → 쾰른", "body": [
     {"t": "item", "tm": "09:00", "b": "보름스 제국회의장 · 루터 기념비", "s": "해설 12분 · 이어폰", "st": "ok", "lab": "✓ 완료"},
     {"t": "alert", "b": "📖 오늘의 말씀 · 로마서 1:17", "s": "“오직 의인은 믿음으로 말미암아 살리라”"},
     {"t": "item", "tm": "12:30", "b": "하이델베르크 고성 · 성령교회", "s": "점심 후 철학자의 길", "st": "now", "lab": "진행 중", "cur": True},
     {"t": "alert", "b": "🚌 휴게소 출발 10분 전", "s": "버스 앞 집결 · 화장실 1유로 동전 준비"},
     {"t": "item", "tm": "18:00", "b": "쾰른 대성당", "s": "MERCURE KÖLN 숙박", "st": "nx", "lab": "예정"},
     {"t": "btns", "items": ["해설 듣기", "기도문"]}]}]},

  {"type": "demo", "img": "zaanse", "src": SRC_EU, "k": "Demo 2 · KeepGuide · 가족 리포트", "title": "조장은 조원만,<br><em>가족은 안심만.</em>",
   "points": ["조장은 <b>조원 5~6명만</b> 확인 — 4개 조가 동시에 점호", "미복귀자는 마지막 확인 위치 · 반경 · 경과 시간", "<b>캐리어 · 수신기</b>도 같은 화면에서 수량 확인", "가족에게는 하루 한 번 일정별 확인 결과만"],
   "phones": [
     {"tone": "guide", "app": "KeepGuide · 2조 조장", "head": "카를교 자유시간 · 15:00 집결", "body": [
       {"t": "ring", "v": "4/5", "b": "1명 미확인", "s": "집결: 구시가 광장 천문시계 앞"},
       {"t": "alert", "red": True, "b": "2조 조원 1명 · 미확인 6분", "s": "마지막 확인 4분 전 · 반경 50m · 카를교 동쪽"},
       {"t": "map", "img": "bridge_night", "pins": [[36, 52, 30, False], [70, 40, 0, True]]},
       {"t": "btns", "items": ["전화", "본부 공유", "통역"]},
       {"t": "item", "tm": "짐", "b": "2조 캐리어 5/5 · 수신기 5/5", "s": "호텔 적재 14:10 확인", "st": "ok", "lab": "✓ 확인"}]},
     {"tone": "trip", "app": "Keep Home · 가족 안심 리포트", "head": "SaGA Pilgrim 2일 차", "body": [
       {"t": "item", "tm": "09:00", "b": "프라하성 집결", "s": "25명 전원 확인", "st": "ok", "lab": "✓ 확인"},
       {"t": "item", "tm": "15:08", "b": "카를교 자유시간 후 집결", "s": "25명 전원 확인", "st": "ok", "lab": "✓ 확인"},
       {"t": "item", "tm": "19:30", "b": "드레스덴 호텔 도착", "s": "25명 · 캐리어 25개", "st": "ok", "lab": "✓ 확인"},
       {"t": "alert", "b": "📖 오늘의 말씀 · 요한복음 8:32", "s": "“진리를 알지니 진리가 너희를 자유롭게 하리라”"},
       {"t": "txt", "s": "개별 위치는 공유하지 않고, 일정별 확인 결과만 전달합니다."}]}]},

  {"type": "dash", "k": "Demo 3 · 인솔 본부", "title": "학장 · 담당 목사는 <em>4개 조와 짐을 한 화면에.</em>", "mapLabel": "라인 강",
   "kpis": [["25/25", "참가자 확인", "g"], ["4/4", "조 점호 완료", ""], ["25/25", "캐리어 적재", "g"], ["24/25", "해설 수신기", "y"], ["0", "미확인 경보", ""]],
   "zones": [[8, 18, 120, "lo", "보름스<br>09:00 완료"], [40, 50, 120, "md", "하이델베르크<br>진행 중"], [70, 12, 130, "lo", "쾰른<br>18:00 예정"], [66, 58, 110, "hi", "휴게소<br>출발 10분 전"]],
   "feed": [["g", "12:35 · 하이델베르크 도착 점호", "4개 조 25/25 확인"], ["", "12:20 · 수신기 1대 충전 부족", "3조 · 예비 수신기로 교체"],
            ["r", "14:05 · 휴게소 재탑승 1명 미확인", "2조 · 화장실 방향 반경 50m · 3분 뒤 탑승"], ["g", "14:10 · 버스 출발", "25/25 · 캐리어 25/25"], ["", "19:30 · 가족 리포트 발송", "25가정 · 오늘의 말씀 포함"]],
   "note": "시연용 가상 데이터입니다. 실제 인원 · 위치가 아닙니다."},

  {"type": "benefit", "k": "Value", "title": "누구에게 <em>무엇이 좋아지나.</em>",
   "who": [["peace", "학장 · 담당 목사", ["4개 조와 짐을 한 화면에서", "말씀 · 기도문 배포 수고 절감", "가족 문의 대응 감소", "순례 기록이 자동으로 남음"]],
           ["bridge_night", "참가자", ["오늘 일정 · 말씀을 한 화면에", "길을 잃어도 다시 찾는다는 안심", "식당 · 약국에서 통역", "귀국 후 순례 기록집"]],
           ["wartburg2", "조장 4명", ["손가락 점호 대신 1분", "재탑승 · 짐 확인이 자동", "미복귀자 위치 범위", "본부와 즉시 공유"]],
           ["zaanse", "가족 · 교회", ["하루 한 번 안심 리포트", "일정 · 말씀으로 함께 중보", "비상 시 연락 체계", "다음 비전트립 모집 자료"]]],
   "kpi": [["5분+", "1분", "조별 점호 (목표)"], ["", "5분 내", "미복귀 인지 (목표)"], ["", "0건", "캐리어 · 수신기 분실 (목표)"], ["", "90%+", "다음 비전트립 재참여 의향 (목표)"]],
   "note": "목표 수치는 시범 운영에서 측정합니다. 현재 실증 · 계약 실적을 의미하지 않습니다."},

  {"type": "budget", "k": "Cost (안)", "title": "25명 · 9일, <em>첫 회는 무상 시범.</em>",
   "lead": "차기 비전트립 1회 기준 예시 (참가 인원 · 일정에 맞춰 확정)",
   "rows": [["KeepTrip 일정 · 말씀 셋업", 30, "9일 일정 · 호텔 · 말씀 · 해설 입력, 단톡방 링크"], ["KeepGuide 이용료", 22, "1인 8,900원 × 25명"],
            ["SmartTag3 대여", 15, "사람 25 + 캐리어 25 = 50개 × 3,000원"], ["수신기 인계 확인", 3, "수신기 25대 QR 라벨"]],
   "totNote": "첫 회는 Keep121 시범 운영으로 무상",
   "funds": [["첫 회 시범", "무상", "Keep121 실증 파트너로 비용 없이 운영"], ["2회차부터", "1인 2.8만원", "9일 전체 · 여행 경비에 포함 협의"], ["여행사 연계", "선택", "여행사 상품에 포함하는 방식도 가능"]],
   "unit": [["2.8만원", "1인 9일 전체 (2회차부터)"], ["0원", "첫 회 시범"]],
   "note": "추정(안)입니다. 가격 · 범위는 SaGA와 협의해 확정합니다."},

  {"type": "rules", "k": "Principles & Roadmap", "title": "필요한 것만, <em>일정 동안만.</em>",
   "items": [["동의 기반", "참가자 본인 동의로만 연결하고, 가족 리포트는 본인이 지정한 사람에게만 보냅니다."],
             ["민감 정보 제외", "기도제목 · 건강 정보 등은 저장하지 않고 일정과 확인 결과만 다룹니다."],
             ["귀국 후 파기", "귀국 30일 안에 위치 기록을 파기하고, 말씀 · 사진 순례 기록집만 남깁니다."]],
   "road": [["2026.12", "제안 · 협의", "학장 · 담당 목사 협의", False], ["2027.3", "국내 1일 시범", "레거시아카데미 1일 프로그램으로 먼저 검증", False],
            ["2027.5", "비전트립 셋업", "일정 · 말씀 · 조 편성 입력", False], ["2027.6~7", "사전 기도회", "앱 안내 · 태그 배부 리허설", False],
            ["2027.8", "비전트립 운영", "9일 운영, 본부 대시보드", True], ["2027.9", "순례 기록집", "기록집 전달 · 결과 보고", False]],
   "imgs": ["koln", "zaanse", "wartburg2", "peace"]},

  {"type": "close", "img": "bridge_night", "src": SRC_EU, "k": "제안 사항", "title": "SaGA에 <em>제안드립니다.</em>",
   "ask": ["차기 비전트립에 Keep121 시범 적용 (첫 회 무상)", "담당 목사님 묵상 자료를 KeepTrip 일정에 연결", "조장 4명 사전 교육 1회 (30분)", "여행사와 짐 · 수신기 인계 절차 공유"],
   "close": "Let Christ be King!<br><em>25명 모두, 함께 돌아오도록.</em>", "contact": "Keep121 · Every one, kept."}
 ]
}

LEGACY = {
 "updated": "2026-11-13",
 "footer": "SaGA 레거시아카데미 1일 프로그램 맞춤 제안 · Keep121",
 "img": LG,
 "slides": [
  {"type": "cover", "img": "coastwide", "src": SRC_LG, "k": "맞춤 제안 · SaGA 레거시아카데미", "brands": BRANDS,
   "title": "60세 이상 순례자,<br><em>한 분도 빠짐없이</em><br>함께 돌아오는 하루.",
   "sub": "레거시아카데미 1일 프로그램(당일 버스 순례 · 현장 학습)을 위한 점호 · 뒤처짐 확인 · 자녀 안심 알림 제안",
   "meta": [["제안 대상", "SaGA 레거시아카데미"], ["제안", "Keep121"], ["적용", "2027 상반기 1일 프로그램"]]},

  {"type": "glance", "img": "sunrise", "src": SRC_LG, "k": "School of Legacy",
   "title": "2026년 3월, 섬티아고<br><em>12사도 순례길</em>을 걸었습니다.",
   "lead": "레거시아카데미는 2026년 3월 27일 아침 7시, 버스로 4시간 거리의 신안 섬티아고 12사도 순례길로 떠났습니다. 13km를 나눠 걷고, 바닷가 베드로 기념 교회 앞에서 별빛 아래 성찬식을 나눴습니다.",
   "stats": [["60", "세 이상", "레거시 생도"], ["4", "시간", "버스 이동 (편도)"], ["13", "km", "12사도 순례길"], ["1", "대", "버스로 함께"]],
   "days": [["07:00", "교회 출발"], ["11:00", "순례길 도착 · 점심"], ["오후", "12사도 순례길 걷기"], ["저녁", "바닷가 성찬식"], ["귀가", "버스 4시간"], ["2027", "1일형 프로그램 표준화"]],
   "note": "출처: 2026 SaGA STORY 5월호 「레거시는 유머가 살아있다」"},

  {"type": "story", "k": "Why",
   "title": "가족 여행에서<br><em>어르신 한 분을 잃었던</em><br>그날에서 시작했습니다.",
   "lead": "올봄 가족 여행 중 어르신 한 분이 일행에서 떨어졌습니다. 휴대폰도 연결되지 않아 다시 찾기까지의 시간이 길었습니다. Keep121은 그날의 질문에서 시작했습니다.",
   "beats": [["가족", "익숙한 몇 명 사이에서도 어르신의 이탈은 <b>몇 분</b>이면 일어납니다."], ["레거시", "걷는 속도가 다른 <b>60세 이상 수십 명</b>이 섬과 바닷가를 함께 걷습니다."], ["질문", "휴대폰이 익숙하지 않아도, <b>누가 뒤처졌는지</b> 바로 알 수는 없을까?"]],
   "imgs": ["saga_night", "silver", "trail", "hike", "palmpath", "cliff"]},

  {"type": "problems", "k": "Challenges", "title": "하루 순례에서 <em>놓치기 쉬운 네 순간.</em>",
   "items": [["trail", "걷는 속도의 차이", "순례길에서 앞뒤 간격이 벌어지면 <b>뒤처진 분</b>을 놓치기 쉽습니다."],
             ["saga_night", "해 진 뒤 바닷가", "부둣가 성찬식처럼 <b>어두운 야외</b>에서는 인원을 세기 어렵습니다."],
             ["bus", "4시간 버스 · 휴게소", "휴게소마다 화장실 · 간식 뒤 <b>재탑승 확인</b>이 반복됩니다."],
             ["silver", "휴대폰이 낯선 분", "앱 설치 · 위치 공유가 어려운 분이 많아 <b>참가자 앱에 기대기 어렵습니다</b>."]]},

  {"type": "eco", "k": "Solution", "title": "어르신은 명찰만, <em>확인은 인솔자와 자녀가.</em>",
   "nodes": [
     {"c": "trip", "img": "saga_group", "who": "생도 (참가자)", "h": "명찰 태그 하나", "p": "앱 설치 없이 SmartTag3를 명찰에 겁니다. 휴대폰이 꺼져도 마지막 확인 위치를 알 수 있습니다.", "f": ["설치 없음", "명찰형", "당일 대여"]},
     {"c": "guide", "img": "hike", "who": "인솔자 · 봉사자", "h": "KeepGuide", "p": "버스 · 순례길 · 성찬식 장소에서 1분 점호. 걷기 구간은 맨 뒤 봉사자가 ‘후미 확인’을 맡습니다.", "f": ["1분 점호", "후미 확인", "재탑승"]},
     {"c": "ent", "img": "sunset", "who": "자녀 · 가족", "h": "Keep Home", "p": "‘07:05 출발 · 18:40 귀가 버스 탑승 · 22:30 교회 도착’처럼 확인된 사실만 자녀에게 알립니다.", "f": ["출발 · 귀가 알림", "확인된 사실만", "알림톡"]}],
   "base": [["tag", "Galaxy SmartTag3", "1인 1태그 · 당일 대여 후 반납, 휴대폰 없이도 위치 확인"],
            ["tr", "종이 응급 카드", "복약 · 보호자 연락처는 종이 카드로만 지니고 시스템에 저장하지 않음"]]},

  {"type": "scenario", "k": "Scenario · 하루", "title": "아침 7시부터 밤 10시 반까지, <em>모두 함께.</em>",
   "steps": [
     {"img": "silver", "when": "D-7", "h": "신청 · 자녀 등록", "p": "생도 본인 동의, 알림 받을 자녀 1명 등록.", "apps": [["trip", "Keep Home"]]},
     {"img": "bus", "when": "07:00 · 교회", "h": "출발 점호", "p": "명찰 태그로 탑승 확인, 자녀에게 ‘출발’ 알림.", "apps": [["guide", "KeepGuide"]]},
     {"img": "coastwide", "when": "09:30 · 휴게소", "h": "재탑승 확인", "p": "버스 출발 전 자동 확인, 미탑승자만 표시.", "apps": [["guide", "KeepGuide"]]},
     {"img": "trail", "when": "오후 · 순례길", "h": "후미 확인", "p": "맨 뒤 봉사자와 가장 먼 분의 거리 표시, 300m를 넘으면 알림.", "apps": [["guide", "KeepGuide"]]},
     {"img": "saga_night", "when": "저녁 · 바닷가", "h": "야간 성찬식 점호", "p": "어두운 야외에서도 손전등 없이 인원 확인.", "apps": [["guide", "KeepGuide"]]},
     {"img": "sunset", "when": "귀가 버스", "h": "귀가 탑승", "p": "전원 탑승 확인 뒤 자녀에게 ‘귀가 출발’ 알림.", "apps": [["trip", "Keep Home"]]},
     {"img": "hill", "when": "22:30 · 교회", "h": "도착 · 반납", "p": "도착 알림, 태그 반납 확인, 하루 기록 보고.", "apps": [["tag", "반납"], ["ent", "보고"]]}]},

  {"type": "demo", "img": "hike", "src": SRC_LG, "k": "Demo · KeepGuide · Keep Home", "title": "봉사자는 후미 확인,<br><em>자녀는 세 번의 안심.</em>",
   "points": ["어르신은 <b>명찰만</b> — 앱도 휴대폰도 필요 없음", "걷기 구간은 <b>후미 봉사자와의 거리</b>로 뒤처짐 확인", "야간 · 바닷가 행사에서도 손전등 없이 인원 확인", "자녀에게는 출발 · 탑승 · 도착 <b>세 번의 안심 알림</b>"],
   "phones": [
     {"tone": "guide", "app": "KeepGuide · 인솔 봉사자", "head": "순례길 3구간 · 14:20", "body": [
       {"t": "ring", "v": "37/38", "b": "1명 후미 지연", "s": "후미 봉사자 기준"},
       {"t": "alert", "red": True, "b": "생도 1명 · 후미에서 420m", "s": "마지막 확인 3분 전 · 5번 예배당 부근 · 반경 50m"},
       {"t": "map", "img": "trail", "pins": [[34, 46, 30, False], [72, 64, 0, True]]},
       {"t": "btns", "items": ["전화", "후미 호출", "본부"]},
       {"t": "item", "tm": "15:30", "b": "다음 집결 · 6번 예배당", "s": "버스 대기 16:30", "st": "nx", "lab": "예정"}]},
     {"tone": "trip", "app": "Keep Home · 자녀 알림", "head": "어머니의 오늘", "body": [
       {"t": "item", "tm": "07:05", "b": "교회 출발", "s": "버스 탑승 확인", "st": "ok", "lab": "✓ 확인"},
       {"t": "item", "tm": "11:10", "b": "순례길 도착", "s": "점호 확인", "st": "ok", "lab": "✓ 확인"},
       {"t": "item", "tm": "18:40", "b": "귀가 버스 탑승", "s": "전원 탑승 확인", "st": "ok", "lab": "✓ 확인"},
       {"t": "item", "tm": "22:30", "b": "교회 도착 예정", "s": "도착하면 알려 드립니다", "st": "nx", "lab": "대기"},
       {"t": "txt", "s": "확인된 사실만 알려 드리며, 실시간 위치는 공유하지 않습니다."}]}]},

  {"type": "benefit", "k": "Value", "title": "누구에게 <em>무엇이 좋아지나.</em>",
   "who": [["saga_group", "학장 · 인솔자", ["버스 · 순례길 점호가 1분", "뒤처진 분을 바로 확인", "야간 행사도 안심", "하루 운영 기록이 남음"]],
           ["silver", "생도 (60세 이상)", ["명찰만 걸면 끝", "속도 걱정 없이 걷기", "길을 잃어도 다시 찾는 안심", "자녀 걱정 덜기"]],
           ["hike", "봉사자", ["후미 확인을 숫자로", "재탑승 확인 자동", "응급 시 본부 즉시 연결", "역할 분담이 쉬움"]],
           ["palmroad", "자녀 · 가족", ["출발 · 탑승 · 도착 알림 3번", "확인된 사실만 받음", "부모님 행사 참여 응원", "비상 시 연락 체계"]]],
   "kpi": [["10분", "1분", "버스 탑승 점호 (목표)"], ["", "5분 내", "후미 지연 인지 (목표)"], ["", "3회", "자녀 안심 알림"], ["", "0건", "미확인 귀가 (목표)"]],
   "note": "목표 수치는 시범 운영에서 측정합니다. 현재 실증 · 계약 실적을 의미하지 않습니다."},

  {"type": "budget", "k": "Cost (안)", "title": "생도 40명 하루, <em>첫 2회는 무상 시범.</em>",
   "lead": "1일 프로그램 1회 · 생도 40명 기준 예시",
   "rows": [["SmartTag3 대여", 12, "40개 × 3,000원 (당일 반납)"], ["KeepGuide 이용료", 16, "1인 4,000원 × 40명 (1일형, 안)"],
            ["자녀 알림톡", 2, "40가정 × 3회"], ["코스 셋업 · 봉사자 교육", 10, "집결지 · 구간 입력, 30분 교육"]],
   "totNote": "첫 2회는 Keep121 시범 운영으로 무상",
   "funds": [["2027 상반기 2회", "무상", "Keep121 실증 파트너로 운영"], ["3회차부터", "1인 1만원", "1일 프로그램 참가비에 포함"], ["제주 2박 3일", "확장", "같은 방식을 제주 프로그램에 적용"]],
   "unit": [["1만원", "1인 1일 (3회차부터)"], ["0원", "첫 2회 시범"]],
   "note": "추정(안)입니다. 가격 · 범위는 레거시아카데미와 협의해 확정합니다."},

  {"type": "rules", "k": "Principles & Roadmap", "title": "어르신의 정보는 <em>꼭 필요한 만큼만.</em>",
   "items": [["본인 · 자녀 동의", "생도 본인 동의를 먼저 받고, 자녀 알림은 본인이 지정한 1명에게만 보냅니다."],
             ["건강 정보 저장 안 함", "복약 · 지병 정보는 종이 응급 카드로만 지니고 시스템에 저장하지 않습니다."],
             ["귀가 후 파기", "위치 기록은 귀가 7일 안에 파기하고, 출석 · 확인 결과만 남깁니다."]],
   "road": [["2026.12", "제안 · 협의", "학장 · 담당자 협의", False], ["2027.2", "봉사자 교육", "인솔자 · 후미 봉사자 30분", False],
            ["2027.3", "1일 시범 ①", "당일 순례 프로그램", False], ["2027.5", "1일 시범 ②", "개선 반영 재운영", False],
            ["2027.6", "결과 보고", "점호 시간 · 만족도", False], ["2027 하반기", "확장", "제주 2박 3일 · 비전트립", True]],
   "imgs": ["saga_group", "saga_night", "cliff", "meadow"]},

  {"type": "close", "img": "coastwide", "src": SRC_LG, "k": "제안 사항", "title": "레거시아카데미께 <em>제안드립니다.</em>",
   "ask": ["2027 상반기 1일 프로그램 2회 시범 운영 (무상)", "인솔 봉사자 3~4명 사전 교육 30분", "자녀 알림 동의 절차를 신청서에 포함", "결과를 제주 2박 3일 · 비전트립으로 확장"],
   "close": "다음 세대에 남길 레거시,<br><em>오늘 모두 함께 돌아오는 것부터.</em>", "contact": "Keep121 · Every one, kept."}
 ]
}

V = dt.datetime.now().strftime("%Y%m%d%H%M")


def shell(name, data_file, title, desc, og):
    h = rd("jeju2027.html")
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h, count=1)
    h = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + desc, h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, h)
    h = re.sub(r'(<meta property="og:url" content="[^"]*/)[^"/]*"', lambda m: m.group(1) + name + '"', h)
    h = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + og, h)
    h = re.sub(r'data-src="[^"]*"', f'data-src="{data_file}"', h)
    h = re.sub(r"data/\w+\.json → assets/js/wyd-slides\.js 가 그린다\. 원본 생성: scripts/\w+\.py",
               f"{data_file} → assets/js/wyd-slides.js 가 그린다. 원본 생성: scripts/add_saga_proposals.py", h)
    h = re.sub(r"wyd-slides\.(css|js)\?v=\d+", lambda m: f"wyd-slides.{m.group(1)}?v={V}", h)
    wr(name, h)


wr("data/saga_visiontrip.json", json.dumps(VISION, ensure_ascii=False, indent=1) + "\n")
wr("data/saga_legacy.json", json.dumps(LEGACY, ensure_ascii=False, indent=1) + "\n")
shell("saga-visiontrip.html", "data/saga_visiontrip.json", "SaGA 유럽 종교개혁 비전트립 제안 · Keep121",
      "사랑글로벌아카데미 SaGA 유럽 종교개혁 비전트립(체코·독일·네덜란드 9일)을 위한 Keep121 맞춤 제안: 일정·말씀·조별 점호·짐·가족 리포트.", EU["prague"])
shell("saga-legacy.html", "data/saga_legacy.json", "SaGA 레거시아카데미 1일 프로그램 제안 · Keep121",
      "SaGA 레거시아카데미(60세 이상) 1일 순례 프로그램을 위한 Keep121 맞춤 제안: 명찰 태그·후미 확인·자녀 안심 알림.", LG["coastwide"])
# 공용 엔진 사본 갱신 (다른 제안 덱과 같은 파일)
wr("assets/css/wyd-slides.css", rd("scripts/wyd-slides.css"))
wr("assets/js/wyd-slides.js", rd("scripts/wyd-slides.js"))
print("  saga-visiontrip.html · saga-legacy.html · data/saga_*.json")
