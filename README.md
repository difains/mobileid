# 모바일 신분증 (Mobile ID)

> 모바일 신분증 월렛 시스템 연동 개발 가이드

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)
[![GitHub Pages](https://img.shields.io/badge/demo-live-green.svg)](https://difains.github.io/mobileid/)

---

## 📌 프로젝트 개요

우리은행 모바일 신분증 CA(Credential Agent) 앱 개발을 위한 종합 가이드입니다.

- **용어집**: 모바일 신분증 관련 표준 용어 정의
- **코드집**: API 코드 및 상태 코드 정의
- **프로세스 도해**: 56개 연동 프로세스 플로우차트

---

## 🌐 웹 뷰어

**[https://difains.github.io/mobileid/](https://difains.github.io/mobileid/)**

| 탭 | 내용 |
|---|---|
| 용어집 | DID, VC, VP 등 표준 용어 정의 |
| 코드집 | API 요청/응답 코드 정의 |
| 프로세스 도해 | 56개 연동 프로세스 플로우차트 |

---

## 📂 문서 구조

```
mobileid/
├── index.html               # 웹 뷰어 (메인 페이지)
├── glossary.json            # 용어집 데이터
├── code.json                # 코드집 데이터
├── README.md                # 프로젝트 설명
├── LICENSE.txt              # MIT 라이센스
│
└── docs/                    # 📁 프로세스 도해화 문서
    ├── README.md            # 목차 및 전체 개요
    ├── flowcharts_part1_common.md   # Part 1: 공통 프로세스 (18개)
    ├── flowcharts_part2_auth.md     # Part 2: 신원 인증 (12개)
    ├── flowcharts_part3_vc.md       # Part 3: VC 관리 (10개)
    ├── flowcharts_part4_vp.md       # Part 4: VP 제출 (13개)
    └── flowcharts_part5_query.md    # Part 5: 조회 서비스 (3개)
```

---

## 📊 프로세스 요약 (총 56개)

| 카테고리 | 프로세스 수 | 주요 내용 |
|----------|:---:|------|
| **공통 프로세스** | 18개 | 월렛 접근(walletToken), PIN 인증, 연결 해제, 삭제, 심카드 검증 등 |
| **신원 인증** | 12개 | 실명인증(도관/직접), IC카드 인증, 안면인증(로컬/서버), 지문인증 등 |
| **VC 관리** | 10개 | DID 발급, VC 발급/조회/삭제, 개인키 갱신, 월렛 이관 등 |
| **VP 제출** | 13개 | QR-MPM/CPM, PUSH, App2App, NFC 방식 (Direct/Indirect/Proxy) |
| **조회 서비스** | 3개 | 중계서버 주소, VC 상태, 장애 여부 조회 |

---

## 🔗 바로가기

- 📖 [프로세스 도해 문서](./docs/README.md)
- 🌐 [웹 뷰어 (GitHub Pages)](https://difains.github.io/mobileid/)
- 📋 [용어집 JSON](./glossary.json)
- 📋 [코드집 JSON](./code.json)

---

## 📝 라이센스

이 프로젝트는 [MIT License](LICENSE.txt)를 따릅니다.

---

## 📅 업데이트 이력

| 날짜 | 내용 |
|------|------|
| 2025-12-10 | 프로세스 도해 문서 56개 추가 (우리은행 CA 앱 개발 관점) |
| 2025-12-10 | index.html에 프로세스 도해 탭 추가 |

---

*© 2025 Mobile ID Project*
