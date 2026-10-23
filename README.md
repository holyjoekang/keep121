# Keep121 — Every one, kept. 한 사람도 빠짐없이, 지키다

단체 안전 플랫폼 Keep121(구 SafeFlock) 소개 홈페이지 (GitHub Pages). 디자인은 Keep121 브랜드 가이드 v1.0(색상·글꼴·로고·명칭 체계)을 따릅니다.

**https://holyjoekang.github.io/keep121/**

## 구성

Keep121 사업계획서(2026-10-17)를 바탕으로 한 한국어 사이트입니다.

- `index.html` — 홈 (히어로 · 문제 · 제품 4종 · 작동 방식 · 여행사 가치 · 파일럿 KPI)
- `solution.html` — 문제 정의 · 해법과 해자 · 점호 체험(인터랙티브) · 설계 원칙
- `product.html` — 제품 체계 · 가이드 앱 · 명찰(Keep Tag · Keep Check) · 9주 MVP · 2027 출시 계획 · 하드웨어 전략
- `family.html` — 신뢰·개인정보: 가족 알림 · 동의 설계 · 책임 구조 · 규제 단계 · 보험 제휴
- `usecases.html` — 시장: 1차 세그먼트 · 시장 규모 · 경쟁 · 고객 획득 · 확장 경로
- `business.html` — 비즈니스 모델: 가격 · 견적 계산기 · 단위경제 · 운영·분실 정책 · 본사 관제
- `evidence.html` — 파일럿·로드맵: 파일럿 설계 · Gate 0 KPI · 9주 실행표 · 성장 로드맵 · 재무 계획 · 리스크
- `company.html` — 비전·가치 · 브랜드 · 창업자·자문 · 팀 구성 계획 · 파일럿 문의
- `assets/css/style.css`, `assets/js/main.js` — 스타일과 인터랙션 (히어로 영상, 점호 체험, 견적 계산기)

### 동적 구성

- 각 `*.html`은 머리말(제목·SEO)과 빈 자리만 담은 껍데기입니다. `assets/js/render.js`가 열릴 때 내용을 받아 그립니다.
- `data/site.json` — 상단 메뉴, 파일럿 문의 단추, 바닥글, 페이지 순서(이전/다음 단추는 이 순서로 자동 생성)
- `content/pages/<페이지>.html` — 페이지 본문. 문구는 여기서 고칩니다.
- 그린 뒤 `assets/js/main.js`(히어로 영상·점호 체험·견적 계산기)를 붙입니다.
- 전환은 `scripts/make_dynamic.py`로 한 번 했습니다. 파일로 직접 열면 내용이 안 뜨니 아래처럼 서버로 여세요.
- `Keep121_솔루션_재설계.html`, `story/` — 이전 버전 문서

## 로컬 실행

```bash
python -m http.server 5173
```

Keep121은 인원 확인 보조 도구이며 안전·구조를 보장하지 않습니다. 시장·재무 수치는 가정이며, 시뮬레이션 수치는 “추정”, 파일럿 결과는 “실측”, 파일럿 목표는 “목표”로 구분해 표기합니다.
