# 💱 USD/KRW Rate Alert

> 매시간 자동으로 환율을 확인하고, 일정 기준 이상 변동하면 이메일과 디스코드로 알려주는 자동화 프로그램

[![Run Status](https://github.com/DUDINGDDI/usdkrw-rate-alert/actions/workflows/check_rate.yml/badge.svg)](https://github.com/DUDINGDDI/usdkrw-rate-alert/actions/workflows/check_rate.yml)

---

## 📌 프로젝트 소개

환율은 매일 조금씩 움직이지만, 매번 직접 찾아보는 건 번거롭습니다.
이 프로젝트는 **정해진 시간마다 자동으로 환율을 확인하고, 특정 기준 이상 변동했을 때만 알림을 보내는** 자동화 프로그램입니다.

사람이 개입하지 않아도 정해진 스케줄에 따라 서버에서 자동으로 실행되며, 결과는 이메일과 디스코드 채널로 받아볼 수 있습니다.

---

## ✨ 주요 기능

- ⏰ **자동 스케줄링**: 평일 오전 9시 ~ 오후 6시, 매시간 자동 실행
- 📊 **환율 데이터 수집**: 야후 파이낸스(Yahoo Finance) 기준 USD/KRW 실시간 시세 조회
- 🔔 **조건부 알림**: 전일 종가 대비 설정한 비율(%) 이상 변동 시에만 알림 발송 (스팸 방지)
- 📧 **이메일 알림**: Gmail을 통한 자동 메일 발송
- 💬 **디스코드 알림**: 웹훅을 통한 실시간 채널 알림
- 📝 **실행 이력 관리**: 알림 발송 여부를 파일로 기록해 하루 중복 발송 방지

---

## 🛠 어떻게 동작하나요?

```
[GitHub Actions 스케줄러]
        │  (매시간 자동 실행)
        ▼
[환율 데이터 조회] ──▶ 야후 파이낸스 API
        │
        ▼
[전일 대비 변동률 계산]
        │
        ▼
   변동폭이 기준 이상? ──No──▶ 종료
        │ Yes
        ▼
┌───────────────┬───────────────┐
▼               ▼
[이메일 발송]    [디스코드 발송]
```

별도의 서버를 운영할 필요 없이, GitHub Actions가 정해진 시간마다 코드를 대신 실행해주는 방식으로 구성했습니다.

---

## 🧰 사용 기술

| 분류 | 내용 |
|---|---|
| 언어 | Python 3.11 |
| 데이터 수집 | yfinance (Yahoo Finance) |
| 자동 실행 환경 | GitHub Actions (cron 스케줄) |
| 알림 | Gmail SMTP, Discord Webhook |
| 이력 관리 | JSON 파일 기반 상태 저장 |

---

## 📂 폴더 구조

```
usdkrw-rate-alert/
├── check_rate.py              # 환율 조회 및 알림 발송 메인 스크립트
├── requirements.txt           # 필요한 패키지 목록
├── last_rate.json             # 마지막 알림 발송 이력
└── .github/
    └── workflows/
        └── check_rate.yml     # 자동 실행 스케줄 설정
```

---

## 🚀 실행 방법

1. 저장소를 클론합니다.
2. GitHub 저장소 설정에서 아래 Secrets를 등록합니다.
   - `SENDER_EMAIL`, `APP_PASSWORD`, `RECEIVER_EMAIL`
   - `DISCORD_WEBHOOK_URL`
3. Actions 탭에서 워크플로우를 확인하고, `Run workflow` 버튼으로 수동 테스트할 수 있습니다.
4. 이후에는 별도 조작 없이 설정된 스케줄에 따라 자동으로 실행됩니다.

---

## 💡 이 프로젝트를 통해 배운 것

- 반복적인 확인 업무를 프로그램으로 자동화하는 경험
- 외부 데이터(환율 API)를 주기적으로 수집하고 조건에 따라 처리하는 로직 설계
- 클라우드 기반 스케줄러(GitHub Actions)를 활용한 무중단 자동 실행 구성
- 민감한 정보(비밀번호, 웹훅 주소)를 코드에 노출하지 않고 안전하게 관리하는 방법

---

## 📄 라이선스

개인 학습 및 포트폴리오 목적으로 자유롭게 참고할 수 있습니다.