"""WYD 서울 2027 × Keep121 × Galaxy SmartTag3 제안 슬라이드(wyd2027.html)를 만든다. 다시 돌려도 안전.

    python scripts/add_wyd_proposal.py

- data/wyd2027.json          슬라이드 본문·이미지 주소 (assets/js/wyd-slides.js 가 그린다)
- wyd2027.html               독립 슬라이드 껍데기 (사이트 메뉴 없이 전체 화면)
- assets/js·css/wyd-slides.* 원본은 scripts/wyd-slides.*
- data/site.json             바닥글에 링크 한 줄

사진: 2027 서울 세계청년대회 공식 사이트(wydseoul.org) 공개 이미지를 원본 주소로 불러온다(복사본 저장 안 함).
대외 사용 전 조직위원회 홍보팀의 사용 승인을 받는다.
"""
import datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rd = lambda p: (ROOT / p).read_text(encoding="utf-8")  # noqa: E731
wr = lambda p, s: (ROOT / p).write_text(s, encoding="utf-8")  # noqa: E731
V = dt.datetime.now().strftime("%Y%m%d%H%M")

CDN = "https://wizware.dnstrip.net/n/cnla9ryzc1ev/b/wydseoul-public-resources/o/"
ED = CDN + "editor_image_"
IMG = {
 "logo": ED + "1218/editor-image-1764052495508-20251125153456074.png",
 "hanbok": CDN + "assets/images/main/donate-bg-9ca49aa24f372b0c5c0661fdc9679058.webp",
 "hands": CDN + "mainVisual/mainVisual-20261021100752613.webp",
 "gallery": CDN + "mainGallery/mainGallery-20260908150613385.webp",
 "officials": CDN + "112/112-20261109160632541.webp",
 "planting": CDN + "history/history-20260319101840494.png",
 "jp2crowd": ED + "1200/editor-image-1762926449291-20251112144729049.png",
 "checkin": ED + "1202/editor-image-1763599566369-20251120094607422.png",
 "stage": ED + "1202/editor-image-1763599661672-20251120094742739.png",
 "dance": ED + "1202/editor-image-1763599661677-20251120094742762.png",
 "flags": ED + "1202/editor-image-1763599661677-20251120094742768.png",
 "popecar": ED + "1202/editor-image-1763599661679-20251120094742805.png",
 "street": ED + "1702/editor-image-1787807759096-0b9bd3f4513c68e5b14a5181b8fc0446.jpeg",
 "plane": ED + "1708/editor-image-1787808357486-47775ad5d6bee3431354c699388e4c6e.jpeg",
 "bridge": ED + "1720/editor-image-1770776567335-91728ba16684795cf4a136c75745d778.jpeg",
 "hall": ED + "1738/editor-image-1770788842918-f8e4ac42b450c98a564cd939585844e4.jpeg",
 "airport": ED + "1834/editor-image-1773212198375-5374c47e930e791c14309459e6b9760d.jpeg",
 "airportflag": ED + "1834/editor-image-1773216066466-bbf1f80dc5e9c57a8e03af626863dff7.jpeg",
 "procession": ED + "1834/editor-image-1773216066467-7939145ceadbbc298355c9bf29d12a6e.jpeg",
 "crowdroad": ED + "1834/editor-image-1773216066467-81f8c6f961088be2e9b704b84f99b7b7.jpeg",
 "icon": ED + "1834/editor-image-1773216314872-361e60e6b3e2eccf5bb5a3625194bd08.jpeg",
 "friends": ED + "1834/editor-image-1773216314873-5f4cbeab056f2e2acca58b5c92b0f9f0.jpeg",
 "church": ED + "1834/editor-image-1773796681606-ba4dc190970494da19000535432d93d3.jpeg",
 "group": ED + "1834/editor-image-1773797150653-a1710a51d7705d7bbc183cfb4e6b8728.jpeg",
 "sign2027": ED + "1834/editor-image-1773797150656-c8f15a69b5602aee0990e4db08730712.png",
 "selfie": ED + "1834/editor-image-1773797489380-6b741fec22490d6ca6013c89bbbbb21f.jpeg",
 "grass": ED + "1834/editor-image-1773797489381-8242430fab5ff6732b9abfb646322ddc.jpeg",
 "tshirt": ED + "1834/editor-image-1773797489383-4133bf93ee45c975aa6a42aea38fbc70.jpeg",
 "travel": ED + "1834/editor-image-1773797820847-a16fe2c74ac1085d6f2d6acd72ebfcbe.jpeg",
 "beach": ED + "1834/editor-image-1773798016899-6e4aa22cb484c613b16ca5debe84e54a.png",
}
SRC = "사진: 2027 서울 세계청년대회 조직위원회 (wydseoul.org)"

D = {
 "updated": "2026-11-12",
 "footer": "Keep121 · WYD 서울 2027 안전·안내 서비스 제안 · 천주교 서울대교구",
 "img": IMG,
 "slides": [
  {"type": "cover", "img": "hanbok", "src": SRC, "k": "Proposal · 2026.11",
   "title": "40만 명의 순례자,<br><em>한 사람도 놓치지 않는</em><br>2027 서울 세계청년대회",
   "sub": "Keep121 안전·안내 서비스와 삼성전자 Galaxy SmartTag3 공동 마케팅으로 순례자의 이동·소통·안전을 한 화면에서 지킵니다.",
   "meta": [["제안 대상", "천주교 서울대교구 · 2027 서울 WYD 조직위원회"], ["제안", "Keep121"], ["협력 제안", "삼성전자 (B2B · 스폰서)"]]},

  {"type": "glance", "img": "jp2crowd", "src": SRC, "k": "WYD Seoul 2027",
   "title": "아시아에서 다시 열리는<br><em>세계 청년들의 순례.</em>",
   "lead": "2027년 8월 3일부터 8일까지, 서울 곳곳에서 개막미사·교리교육·젊은이 축제·십자가의 길·밤샘 기도·폐막미사가 이어집니다.",
   "stats": [["40", "만 명", "해외 입국 순례자 (추정)"], ["6", "일", "8.3 ~ 8.8 본대회"], ["수십", "개 언어", "전 세계 참가국 언어"], ["수백", "곳", "교구·성당·행사장 분산 일정"]],
   "days": [["8.3 화", "집결·등록, 개막미사"], ["8.4 수", "주교와의 만남, 젊은이 축제"], ["8.5 목", "교황 환영 행사"], ["8.6 금", "십자가의 길"], ["8.7 토", "폐막미사 장소로 순례, 밤샘 기도"], ["8.8 일", "폐막미사, 봉사자와 교황 만남"]]},

  {"type": "story", "k": "Why we started",
   "title": "가족 여행에서도<br><em>한 사람을 잃는 데</em><br>몇 분이면 충분했습니다.",
   "lead": "올봄 가족 여행 중 어르신 한 분이 일행에서 이탈했습니다. 낯선 곳에서 휴대폰도 연결되지 않아 다시 만나기까지 모두가 마음을 졸였습니다.",
   "beats": [["가족 여행", "익숙한 사람 몇 명 사이에서도 이탈은 <b>순식간</b>에 일어납니다."], ["WYD 2027", "말이 다른 <b>40만 명</b>이 낯선 서울을 6일간 함께 이동합니다."], ["질문", "<b>누가, 어디서, 언제</b> 사라졌는지 가장 먼저 알 수 있을까?"]],
   "imgs": ["travel", "airport", "plane", "selfie", "friends", "beach"]},

  {"type": "problems", "k": "Challenges", "title": "대회 운영자가 마주할 <em>네 가지 안전 과제.</em>",
   "items": [["flags", "초대형 인파", "행사장마다 수만~수십만 명이 몰립니다. 일행을 놓치면 육안으로 다시 찾기 어렵습니다."],
             ["friends", "언어 장벽", "길 묻기, 응급 상황 설명, 봉사자 안내가 모두 <b>통역</b>을 필요로 합니다."],
             ["bridge", "분산된 이동", "숙소·교구·행사장을 오가는 그룹별 일정이 서로 다르고 대중교통 이동이 많습니다."],
             ["crowdroad", "늦은 사고 인지", "누가 없는지 알게 되는 순간이 <b>집결 시간 이후</b>라면 이미 늦습니다."]]},

  {"type": "eco", "k": "Solution", "title": "앱 3개와 태그 1개로<br><em>순례자 → 인솔자 → 상황실</em>을 연결합니다.",
   "nodes": [
     {"c": "trip", "img": "airportflag", "who": "순례자", "h": "KeepTrip", "p": "전체 대회 일정과 그룹별 세부 일정을 모국어로 안내합니다. 집결 시간에 늦을 것 같으면 먼저 알려 줍니다.", "f": ["다국어 일정", "집결 알림", "실시간 통역 연동"]},
     {"c": "guide", "img": "procession", "who": "인솔자 · 봉사자", "h": "KeepGuide", "p": "그룹 점호, 미확인 인원 표시, 마지막 확인 위치, SOS 접수로 이탈과 사고를 가장 빨리 확인합니다.", "f": ["1분 점호", "이탈 경보", "SOS"]},
     {"c": "ent", "img": "stage", "who": "조직위 상황실", "h": "KeepEnterprise", "p": "전체 그룹·구역·경보를 한 화면에서 보고 봉사자·의료·경찰에 바로 연결합니다.", "f": ["통합 관제", "구역 밀집도", "사후 보고서"]}],
   "base": [["tag", "Galaxy SmartTag3", "순례자 1인 1태그 · 휴대폰이 꺼져도 태그로 위치 확인"],
            ["tr", "실시간 통역 연동", "hiworker 등 실시간 통역 앱과 연동해 일정 속 대화를 바로 통역"]]},

  {"type": "tag", "k": "Device · Galaxy SmartTag3", "title": "9.5g 태그 하나가<br><em>순례자의 안전 끈</em>이 됩니다.",
   "lead": "10월 7일 출시된 최신 Galaxy SmartTag3는 더 가벼워지고 안드로이드와 아이폰을 모두 지원합니다.",
   "stats": [["9.5", "g", "명찰·가방에 다는 무게"], ["2", "OS", "Android · iPhone 지원"], ["2~3", "천원", "대회 기간 대여료 (안)"]],
   "how": [["공항·등록처에서 수령", "참가 등록 QR로 본인·그룹과 태그를 1분 안에 연결"], ["명찰 케이스에 부착", "휴대폰 배터리가 없어도 태그 위치로 마지막 위치 확인"],
           ["대회 후 반납 또는 기념품", "반납 태그는 다음 행사에 재사용, 원하면 구매 전환"], ["삼성 스폰서 시 무상", "삼성전자 단말 공급으로 순례자 부담 0원 가능"]],
   "note": "태그 위치는 주변 갤럭시 기기를 통해 갱신되므로 ‘반경’과 ‘마지막 확인 시각’으로 표시합니다. 위치 연동 방식은 삼성전자와 B2B 협의로 확정합니다."},

  {"type": "scenario", "k": "Scenario", "title": "출국 전부터 귀국까지, <em>한 순례자의 7일.</em>",
   "steps": [
     {"img": "tshirt", "when": "D-30 · 출국 전", "h": "등록·동의", "p": "참가 등록 시 그룹·언어·비상연락처 입력, 위치 이용 동의.", "apps": [["trip", "KeepTrip"]]},
     {"img": "checkin", "when": "8.1~3 · 입국", "h": "태그 수령", "p": "공항·등록처 부스에서 SmartTag3 수령, QR로 그룹 연결.", "apps": [["tag", "SmartTag3"]]},
     {"img": "dance", "when": "매일 아침", "h": "오늘의 일정", "p": "모국어 일정·집결지·교통편 안내. 늦을 것 같으면 미리 알림.", "apps": [["trip", "KeepTrip"]]},
     {"img": "friends", "when": "행사·이동 중", "h": "실시간 통역", "p": "길 묻기, 식당, 봉사자 안내를 실시간 통역 앱으로 바로 대화.", "apps": [["tr", "통역 연동"]]},
     {"img": "crowdroad", "when": "집결 시간", "h": "점호·이탈 경보", "p": "인솔자가 1분 점호. 미확인자는 마지막 위치와 함께 경보.", "apps": [["guide", "KeepGuide"]]},
     {"img": "stage", "when": "24시간", "h": "상황실 대응", "p": "구역별 밀집도·경보 확인, 가까운 봉사자·의료팀 출동.", "apps": [["ent", "KeepEnterprise"]]},
     {"img": "airport", "when": "8.9~ · 귀국", "h": "반납·보고", "p": "공항에서 태그 반납, 그룹별 안전 리포트, 위치 기록 파기.", "apps": [["tag", "SmartTag3"], ["ent", "리포트"]]}]},

  {"type": "demo", "img": "group", "src": SRC, "k": "Demo 1 · KeepTrip", "title": "내 일정을 <em>내 언어로.</em>",
   "points": ["대회 공식 일정 + 그룹별 세부 일정을 <b>하나의 타임라인</b>으로", "현재 위치와 다음 집결지까지 거리를 계산해 <b>늦을 것 같으면 먼저 알림</b>", "일정 완료 여부를 자동 체크 — 인솔자는 누가 아직 도착 전인지 압니다", "앱 설치 없이 링크로 열고, 언어는 등록 정보에서 자동 선택"],
   "phones": [{"tone": "trip", "app": "KeepTrip · Día 3 · 5 de agosto", "head": "Mi itinerario de hoy", "body": [
     {"t": "item", "tm": "08:00", "b": "Catequesis con obispos", "s": "Parroquia de Myeongdong", "st": "ok", "lab": "✓ Hecho"},
     {"t": "item", "tm": "11:30", "b": "Festival de la Juventud", "s": "Plaza Gwanghwamun", "st": "ok", "lab": "✓ Hecho"},
     {"t": "alert", "b": "⏰ Reunión en 25 min", "s": "Estás a 18 min a pie del punto de encuentro (Salida 3, Est. City Hall). ¡Sal ahora!"},
     {"t": "item", "tm": "14:30", "b": "Punto de encuentro del grupo", "s": "Est. City Hall, salida 3", "st": "now", "lab": "Siguiente", "cur": True},
     {"t": "item", "tm": "16:00", "b": "Bienvenida al Papa", "s": "Sede principal · Puerta B", "st": "nx", "lab": "Pendiente"},
     {"t": "btns", "items": ["Ver ruta", "Traducir"]}]}]},

  {"type": "demo", "img": "grass", "src": SRC, "k": "Demo 2 · 실시간 통역 연동", "title": "말이 달라도 <em>바로 대화.</em>",
   "points": ["일정 화면의 ‘통역’ 버튼 한 번으로 <b>hiworker 등 실시간 통역 앱</b>으로 연결", "현재 일정·장소를 함께 넘겨 <b>상황에 맞는 통역</b> (교통, 식당, 의료)", "봉사자·경찰·의료진과의 응급 대화도 같은 방식으로 지원", "통역 엔진은 교구가 선택한 파트너로 교체 가능"],
   "phones": [{"tone": "tr", "app": "KeepTrip · 실시간 통역 (연동)", "head": "Español ⇄ 한국어", "body": [
     {"t": "lang", "items": ["Español", "한국어"]},
     {"t": "me", "l": "Español → 한국어", "s": "시청역 3번 출구가 어디예요? 우리 그룹이 거기서 모여요."},
     {"t": "you", "l": "봉사자 · 한국어 → Español", "s": "Siga recto 200 metros y gire a la derecha. Le acompaño."},
     {"t": "me", "l": "Español → 한국어", "s": "감사합니다! 2시 30분까지 가야 해요."},
     {"t": "you", "l": "한국어 → Español", "s": "Llegará a tiempo, son 5 minutos."},
     {"t": "mic", "s": "누르고 말하세요 · Mantén pulsado para hablar"}]}]},

  {"type": "demo", "img": "procession", "src": SRC, "k": "Demo 3 · KeepGuide", "title": "누가 없는지,<br><em>집결 1분 만에.</em>",
   "points": ["인솔자는 태그·앱 체크인으로 <b>그룹 점호를 1분 안에</b> 끝냅니다", "미확인자는 <b>마지막 확인 위치·반경·경과 시간</b>과 함께 바로 표시", "전화·통역·상황실 신고를 한 화면에서", "순례자는 SOS 한 번으로 모국어 도움 요청 + 위치 공유"],
   "phones": [
     {"tone": "guide", "app": "KeepGuide · 인솔자", "head": "Manila-07 그룹 · 14:31", "body": [
       {"t": "ring", "v": "30/32", "b": "2명 미확인", "s": "집결지: 시청역 3번 출구"},
       {"t": "alert", "red": True, "b": "Maria S. · 미확인 12분", "s": "마지막 확인 7분 전 · 반경 50m · 광화문광장 남측"},
       {"t": "map", "img": "flags", "pins": [[34, 46, 34, False], [70, 62, 0, True]]},
       {"t": "btns", "items": ["상황실 신고", "전화", "통역"]},
       {"t": "item", "tm": "Juan", "b": "Juan P. · 미확인 3분", "s": "이동 중 · 도착 예상 4분", "st": "now", "lab": "이동 중"}]},
     {"tone": "sos", "app": "KeepGuide · 순례자", "head": "Ayuda · 도움 요청", "body": [
       {"t": "txt", "s": "Mantén pulsado 3 segundos. Tu grupo y la central recibirán tu ubicación."},
       {"t": "sos", "s": "pulsa 3 s"},
       {"t": "alert", "b": "📍 Ubicación compartida", "s": "Inmediaciones de Gwanghwamun · hace 1 min"},
       {"t": "btns", "items": ["Llamar a mi guía", "Traducir"]}]}]},

  {"type": "dash", "k": "Demo 4 · KeepEnterprise", "title": "조직위 상황실, <em>40만 명을 한 화면에.</em>",
   "kpis": [["412,380", "등록 순례자", ""], ["386,102", "태그 연결", "g"], ["12,850", "운영 그룹", ""], ["37", "미확인 경보 (진행 중)", "r"], ["11분", "평균 발견 시간", "y"]],
   "zones": [[8, 14, 150, "hi", "주 행사장<br>밀집 92%"], [52, 10, 120, "md", "광화문 일대<br>71%"], [30, 56, 110, "lo", "교구 행사장<br>38%"], [66, 54, 130, "md", "환승역 주변<br>64%"]],
   "feed": [["r", "14:31 · Manila-07 미확인 2명", "광화문 남측 반경 50m · 봉사자 B-12 출동"], ["g", "14:24 · Lyon-03 미확인 1명 → 발견", "SOS 접수 후 9분 · 그룹 복귀"],
            ["", "14:20 · 주 행사장 게이트 B 밀집", "입장 분산 안내 4개 언어 발송"], ["r", "14:12 · 의료 SOS", "열사병 의심 · 의료팀 3분 내 도착"], ["g", "14:05 · 교구 행사장 점호 완료", "그룹 418개 중 418개"]],
   "note": "시연용 가상 데이터입니다. 실제 위치·인원 수치가 아닙니다."},

  {"type": "benefit", "k": "Value", "title": "누구에게 <em>무엇이 좋아지나.</em>",
   "who": [["officials", "서울대교구 · 조직위", ["이탈·사고를 집결 시간 전에 인지", "상황실 단일 화면, 사후 안전 보고서", "다국어 문의 부담 감소", "‘가장 안전한 WYD’ 대외 메시지"]],
           ["selfie", "순례자 · 가족", ["길을 잃어도 다시 찾는다는 안심", "모국어 일정·통역", "고국 가족에게 안전 소식 공유", "앱 설치 없이 링크로"]],
           ["planting", "인솔자 · 봉사자", ["종이 명단 대신 1분 점호", "미확인자 위치 범위로 바로 수색", "통역으로 현장 소통", "상황실과 즉시 연결"]],
           ["sign2027", "삼성전자", ["40만 글로벌 청년 대상 체험 마케팅", "SmartTag3 대규모 B2B 레퍼런스", "Android·iPhone 모두 체험", "대회 후 재사용·구매 전환"]]],
   "kpi": [["30분+", "5분", "미확인자 인지 시간 (목표)"], ["10분", "1분", "그룹 점호 시간 (목표)"], ["", "30분 내", "이탈자 발견 (목표)"], ["", "0건", "미해결 실종 (목표)"]],
   "note": "목표 수치는 사전 파일럿에서 검증합니다. 현재 실증·계약 실적을 의미하지 않습니다."},

  {"type": "samsung", "img": "hall", "src": SRC, "k": "Samsung Electronics · B2B Co-marketing",
   "title": "<em>Galaxy SmartTag3와 함께하는</em><br>세계청년대회 2027.",
   "items": [["01 · 단말 공급", "공식 스폰서", "SmartTag3 순례자용 태그, 상황실·봉사자용 Galaxy 단말 공급"], ["02 · 광고", "브랜드 노출", "공항·등록처 배부 부스, 앱 내 스폰서 표기, 공식 굿즈 연계"],
             ["03 · 캠페인", "공동 마케팅", "‘한 사람도 놓치지 않는 대회’ 캠페인, 순례자 사연 콘텐츠"], ["04 · 기술 협력", "B2B 연동", "SmartThings Find 단체 위치 연동, 행사용 대량 등록·반납"]],
   "camp": {"b": "Every one, kept.<br><em>모두가 함께 돌아가는 대회.</em>", "t": "삼성전자는 글로벌 청년 40만 명에게 Galaxy 생태계를 체험시키고, 서울대교구는 비용 부담 없이 안전 인프라를 확보합니다. Keep121은 서비스 운영과 데이터 보호를 맡습니다."}},

  {"type": "rules", "k": "Principles & Roadmap", "title": "동의한 기간에만, <em>필요한 만큼만.</em>",
   "items": [["동의 기반", "참가 등록 시 위치 이용 목적·기간을 모국어로 안내하고 동의한 순례자만 연결합니다. 미성년자는 보호자 동의."],
             ["대회 기간 한정", "위치는 8월 대회 기간에만 수집하고, 정확한 좌표 대신 ‘반경·마지막 확인 시각’으로 보여 줍니다."],
             ["종료 후 파기", "대회 종료 후 30일 안에 위치 기록을 파기하고, 통계 보고서만 조직위에 남깁니다."]],
   "road": [["2026.12", "제안·협의", "서울대교구·조직위 설명, 삼성전자 B2B 협의 착수", False], ["2027.1~2", "다국어 구축", "등록 시스템 연계, 5개 언어 우선 지원", False],
            ["2027.3~4", "소규모 파일럿", "교구 청년 행사 500명 대상 점호·태그 검증", False], ["2027.5~6", "확대 검증", "사전 행사 5,000명, 상황실 리허설", False],
            ["2027.7", "운영 준비", "봉사자 교육, 공항·등록처 배부 부스", False], ["2027.8", "본대회", "8.3~8.8 운영, 귀국 후 반납·보고·파기", True]],
   "imgs": ["church", "icon", "gallery", "beach"]},

  {"type": "close", "img": "hands", "src": SRC, "k": "Our ask",
   "title": "서울대교구께 <em>요청드립니다.</em>",
   "ask": ["순례자 등록 시스템과의 연계(그룹·언어·연락처) 협의", "2027년 상반기 교구 청년 행사에서 파일럿 운영 허락", "삼성전자 스폰서 협의에 조직위원회 공동 참여", "개인정보·안전 담당 부서와의 운영 기준 공동 수립"],
   "close": "한 사람도 빠짐없이,<br><em>모두 함께 집으로.</em>", "contact": "Keep121 · Every one, kept."}
 ]
}
wr("data/wyd2027.json", json.dumps(D, ensure_ascii=False, indent=1) + "\n")

title = "WYD 서울 2027 안전·안내 제안 · Keep121"
desc = "Keep121 × Galaxy SmartTag3: 2027 서울 세계청년대회 40만 순례자를 위한 KeepTrip·KeepGuide·KeepEnterprise 안전·안내 서비스 제안 (천주교 서울대교구)."
wr("wyd2027.html", f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://holyjoekang.github.io/keep121/wyd2027.html">
  <meta property="og:image" content="{IMG['hanbok']}">
  <meta name="theme-color" content="#23306B">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=IBM+Plex+Sans+KR:wght@400;500;600;700&display=swap">
  <link rel="stylesheet" href="assets/css/wyd-slides.css?v={V}">
</head>
<body>
<!-- 본문은 data/wyd2027.json → assets/js/wyd-slides.js 가 그린다. 원본 생성: scripts/add_wyd_proposal.py -->
<div class="deck"><div class="stage" data-deck></div></div>
<div class="ui"><button data-prev aria-label="이전">←</button><span class="cnt">1 / 1</span><button data-next aria-label="다음">→</button><div class="bar"><i></i></div><button data-print>PDF 저장</button><a href="index.html">Keep121 홈</a></div>
<script src="assets/js/wyd-slides.js?v={V}"></script>
</body>
</html>
""")
wr("assets/css/wyd-slides.css", rd("scripts/wyd-slides.css"))
wr("assets/js/wyd-slides.js", rd("scripts/wyd-slides.js"))

s = json.loads(rd("data/site.json"))
for c in s["footer"]["columns"]:
    if any(l["href"] == "b2b.html" for l in c["links"]) and not any(l["href"] == "wyd2027.html" for l in c["links"]):
        j = next(j for j, l in enumerate(c["links"]) if l["href"] == "b2b.html") + 1
        c["links"].insert(j, {"href": "wyd2027.html", "label": "WYD 2027 제안"})
wr("data/site.json", json.dumps(s, ensure_ascii=False, indent=2) + "\n")
print("  wyd2027.html · data/wyd2027.json · assets/js/wyd-slides.js · assets/css/wyd-slides.css · site.json(바닥글)")
