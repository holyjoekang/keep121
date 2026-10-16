# SafeFlock Lite 단말 소싱 조사 결과

조사 범위는 **1차 파일럿용 BLE 단말**입니다. GPS·셀룰러 원격 추적이 아니라, 가이드 휴대폰이 여행객 단말의 신호를 수신해 그룹 확인과 근거리 이탈 알림을 시험하는 용도로 평가했습니다.

## 업체 선정 결과

**우선 RFQ 대상은 HoneyComm, MOKOSmart, BNCOM 3곳**으로 제안합니다. HoneyComm은 착용형 제품 후보, MOKOSmart는 소형·저가 기준 제품, BNCOM은 국내 구매·인증 확인이 쉬운 비교 후보입니다. 샘플 시험 전 단계이므로 이들은 최종 공급사가 아니라 **요구사양과 서류를 확인할 가치가 있는 후보**입니다.

| 순위 | 업체·제품 | 확인된 공개 사양 | SafeFlock Lite 적합성 및 확인할 점 |
|---|---|---|---|
| **1** | [HoneyComm HCBB16](https://www.honeycomm.net/product/waterproof-ultrasonic-welding-100meters-ble-5-0-wearable-low-power-bluetooth-beacon-tag-for-personnel-management/) | 착용·목걸이형 사용 가능, BLE 4.2/5.0, IP67, 크기 40×10mm, 광고 간격 100ms~10초 설정 가능, CR2 배터리. 제조사는 3초 광고 기준 최대 3년 수명을 제시합니다. | **착용형 파일럿에 가장 직접적인 후보**입니다. 무게가 공개되지 않았고, 광고 간격을 1초로 설정했을 때의 전류·수명도 확인이 필요합니다. 배터리가 동전전지보다 크므로 실물 무게와 착용감을 먼저 받아보세요. |
| **2** | [MOKOSmart M1](https://store.mokosmart.com/product/m1-coin-tag/) / [M1P](https://store.mokosmart.com/product/m1p-led-tag/) | M1은 26mm·5.4g, 교체형 CR2032, 모션 센서, 기본 설정 수명 1.5년이며 온라인 스토어 가격은 **US$5~7**입니다. M1P는 30×8mm·6.2g, 교체형 CR2032, LED, 기본 설정 수명 9개월입니다. [BLE Beacons, LoRaWAN Sensors & Gateways](https://store.mokosmart.com/?utm_source=chatgpt.com)
- **HoneyComm:** 제조사 페이지에 이메일 `sue@honeycomm.net`, 전화·WhatsApp `+86 18813863699`가 공개돼 있습니다. 색상 변경은 3,000대 이상 주문 조건이 안내돼 있어, 소량 샘플은 기본 색상·기성품 기준으로 문의해야 합니다. [HoneyComm](https://www.honeycomm.net/product/waterproof-ultrasonic-welding-100meters-ble-5-0-wearable-low-power-bluetooth-beacon-tag-for-personnel-management/?utm_source=chatgpt.com)
- **BNCOM:** 국내 공급 후보지만, 제품 페이지에 ‘KC 인증’이라고 적혀 있다는 사실만으로 인증 상태가 확인된 것은 아닙니다. **인증번호·인증서·정확한 모델명**을 받은 뒤 국립전파연구원에서 조회하세요. 방송통신기자재를 제조·판매·수입할 때는 해당 제품에 필요한 적합성평가 여부를 확인해야 합니다. [RRA](https://www.rra.go.kr/ko/license/A_a_about.do?utm_source=chatgpt.com)

## 추천 구매 순서

### 1단계: 견적·자료 요청

우선 아래 세 곳에 동일한 RFQ를 보냅니다.

1. **HoneyComm:** HCBB16의 무게·샘플가·1초 광고 설정 시 전력소모·인증서 요청
2. **MOKOSmart:** M1 및 M1P 샘플가, 손목밴드·클립 부속품, 구성 변경 방법 요청
3. **BNCOM:** MIDASCON 현재 공급 가능 여부, 모델별 KC 인증번호, 앱·SDK·광고 설정 가능 범위 요청

Feasycom에는 Safety 모드까지 염두에 둔 비교견적만 별도로 문의합니다.

### 2단계: 샘플 구매

자료와 답변을 받은 후 **HoneyComm 2대와 MOKOSmart M1/M1P 각 1~2대**를 우선 구매하는 구성이 적절합니다. HoneyComm은 착용형, MOKOSmart는 크기·가격 기준으로 비교합니다. BNCOM은 KC 증빙과 현재 공급 가능성이 확인되면 국내 대안 샘플을 추가합니다.

MOKOSmart 스토어의 M1 공개 가격을 기준으로 보면 2~3대 단말 자체 가격은 소액이지만, **배송·세금·통관비와 스트랩 비용은 별도**입니다. HoneyComm·BNCOM·Feasycom 가격은 공개 자료에서 확인되지 않아 공급사 견적을 받아야 합니다.

## 샘플 구매 전에 받을 자료

견적만 비교하지 말고, 아래 자료를 답변과 함께 요청하세요.

- 정확한 제품 모델명과 최신 데이터시트
- 단말 본체 무게와 스트랩·배터리 포함 무게
- 광고 주기 1초 설정 가능 여부와 설정 방법
- 실제 광고 데이터 형식, ID 변경·암호화 지원 여부
- Android 휴대폰 한 대로 10·25·50대를 식별할 수 있는지
- 앱·SDK·API 또는 설정 도구 제공 여부와 라이선스 비용
- 광고 간격·송신 세기별 전류 측정값과 배터리 수명 산정 조건
- IP 등급 시험자료와 해당 모델의 KC·CE·FCC 인증서
- 샘플가, MOQ, 수량별 단가, 운송비, 납기, 불량 대응 조건

특히 “최대 100m/400m”는 제조사 표기상 **장애물이 없는 개방 공간 조건**이므로, 실제 여행 현장의 거리 성능으로 간주하지 마세요. 단체 인원 확인은 실내·차량·사람이 밀집한 환경에서 별도로 시험해야 합니다.

## 업체별 요청 메일 초안

해외 업체에는 아래 영문 메일을 개별 발송하면 됩니다. MOKOSmart는 `sales@mokosmart.com`이 회사 자료에 기재돼 있으나, 공식 도메인 이메일인지 확인하면서 발송하세요. MOKOSmart는 사칭 이메일 주의를 공지하고 공식 주소가 `@mokotechnology.com` 또는 `@mokosmart.com`으로 끝난다고 안내합니다. [mokosmart.com](https://www.mokosmart.com/ko/beware-of-fraudulent-emails-impersonating-mokosmart/?utm_source=chatgpt.com)

Dear Sales Team,

I am evaluating BLE tags for a small pilot of SafeFlock, a group travel safety service. The guide will use an Android smartphone to detect and identify travelers’ BLE tags during tours.

At this stage, we are looking for an off-the-shelf BLE device for sample testing. GPS and cellular connectivity are not required.

Could you please recommend the most suitable model and provide the following information?

**Preferred requirements**

- BLE 5.0 or later preferred; BLE 4.2 may be considered for sample evaluation
- Configurable advertising interval, including 1 second
- Configurable device identifier or advertising payload
- Replaceable battery preferred
- Wearable by wristband, lanyard, or clip; an accessory option is acceptable
- Lightweight and compact; please state the complete weight including battery and wearable accessory
- IP67 preferred
- LED, buzzer, or motion sensor is optional

**Please provide**

1. Recommended model number and latest datasheet  
2. Sample price and availability for 2–5 units  
3. Price breaks at 50, 500, and 2,000 units  
4. MOQ, sample and production lead time, and shipping cost to South Korea  
5. Battery type, measured current, and battery-life test conditions  
6. Configuration app, Android SDK/API, protocol documentation, and any license fees  
7. Whether one Android phone can scan and identify at least 25 tags in a tour environment  
8. Available wristband, lanyard, or clip accessories  
9. Copies of certificates for the exact model offered  
10. Warranty, defect handling, and options for branding or enclosure customization

Please confirm whether the sample can operate with our own Android application without requiring your cloud platform.

We are evaluating samples only and have not committed to production. If the pilot results are satisfactory, we may discuss a larger order and customization.

Best regards,  
[Name]  
SafeFlock  
[Email]  
[Phone / WhatsApp]

BNCOM에는 아래 한글 메일로 보내면 됩니다.

안녕하세요.

단체여행객의 인원 확인과 가이드 알림을 지원하는 SafeFlock 서비스를 준비하고 있습니다. 1차 파일럿에서 가이드 Android 휴대폰이 여행객의 BLE 단말을 스캔하는 방식으로 검증하고자 하며, GPS·셀룰러 기능은 이번 샘플 범위에 포함하지 않습니다.

귀사의 MIDASCON Beacon Tag가 현재 공급 가능한 제품인지와 아래 사항을 확인 부탁드립니다.

- 현재 공급 모델명, 최신 사양서 및 샘플 구매 가능 수량·단가
- 배터리와 스트랩·부속품을 포함한 실측 무게
- 광고 주기를 1초로 설정할 수 있는지와 설정 방법
- 기기 ID 또는 광고 데이터 변경 가능 여부
- 가이드 Android 앱에서 25대 이상을 동시에 식별할 수 있는지
- 앱·SDK·API·통신 프로토콜 문서 및 제공 비용
- 제품에 적용된 KC 인증번호와 해당 모델 인증서
- 샘플 납기, MOQ, 수량별 단가(50대·500대·2,000대)
- 밴드·목걸이·클립 등 착용 부속품 제공 여부
- 불량 대응 및 보증 조건

초기에는 샘플 검증만 진행하며, 양산이나 맞춤 제작은 파일럿 결과와 수요를 확인한 뒤 별도 협의하고자 합니다.

검토 후 자료와 견적을 회신해 주시면 감사하겠습니다.

감사합니다.

[이름]  
SafeFlock  
[연락처]  
[이메일]

## 시험 판정 기준

샘플을 받으면 단말별로 다음 항목을 같은 조건에서 비교하세요.

| 시험 항목 | 방법 | 기록할 결과 |
|---|---|---|
| 동시 식별 | Android 휴대폰 1대로 10대·25대 태그를 동시에 스캔 | 누락 대수, 오식별, 목록 갱신시간 |
| 거리·차폐 | 개방 공간·건물 내부·버스 안에서 거리별 수신 | 수신 가능 거리와 신호 끊김까지의 시간 |
| 1초 광고 설정 | 공급사 설정 앱 또는 SDK로 변경 후 패킷 확인 | 실제 광고 간격과 설정 유지 여부 |
| 휴대·착용 | 손목·목걸이·클립으로 1~2시간 착용 | 무게감, 흔들림, 분실 위험, 착용 거부감 |
| LED·부저 | 앱에서 근거리 찾기 작동 여부 시험 | 찾기 성공률과 조작 난이도 |
| 배터리 | 최소 72시간 동작 후 전압 또는 소비전류 확인 | 사용 설정별 잔량 변화 |

**BLE 수신 신호만으로 정확한 GPS 위치를 얻을 수는 없습니다.** 가이드 휴대폰에서 신호가 사라지는지, 어느 정도 거리에서 사라지는지를 검증하는 것이 Lite 샘플 시험의 범위입니다.

## 최종 권고

1. **HoneyComm HCBB16과 MOKOSmart M1/M1P에 우선 RFQ를 발송**합니다.
2. **BNCOM에는 제품 최신 공급 여부와 KC 인증 증빙을 확인**합니다.
3. 자료 검토 뒤 HoneyComm의 무게가 허용 범위에 들어오면 착용형 샘플을 주문하고, MOKOSmart는 경량·가격 비교용으로 함께 시험합니다.
4. 샘플 시험에서 25대 동시 식별과 실제 착용성이 확인되면 파일럿 수량을 결정합니다.
5. 파일럿 참여자에게 배포·판매하기 전에는 모델별 국내 적합성평가 요건을 확인합니다. RRA는 방송통신기자재의 인증·등록·잠정인증 등 적합성평가 제도를 운영하고 인증 현황을 검색할 수 있습니다. [RRA](https://www.rra.go.kr/ko/license/A_a_about.do?utm_source=chatgpt.com)

이 방식이면 현재 예산을 금형이나 맞춤 개발에 쓰기 전에 **착용형·초경량형·국내 조달형**을 실제 단말로 비교할 수 있습니다.
