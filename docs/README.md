# 모바일 신분증 월렛 프로세스 도해화 (전체 56개)

> 복잡한 UML 시퀀스 다이어그램을 일반인이 이해하기 쉬운 플로우차트로 정리한 문서입니다.
> 
> **관점: 우리은행 모바일 신분증 CA 앱 개발**

---

## 📋 문서 목록

| Part | 카테고리 | 프로세스 수 | 링크 |
|:---:|----------|:---:|------|
| 1 | 공통 프로세스 (P100~P117) | 18개 | [flowcharts_part1_common.md](./flowcharts_part1_common.md) |
| 2 | 신원 인증 (P121~P151) | 12개 | [flowcharts_part2_auth.md](./flowcharts_part2_auth.md) |
| 3 | VC 관리 (P190~P290) | 10개 | [flowcharts_part3_vc.md](./flowcharts_part3_vc.md) |
| 4 | VP 제출 (P311~P315) | 13개 | [flowcharts_part4_vp.md](./flowcharts_part4_vp.md) |
| 5 | 조회 서비스 (P410~P430) + 용어정리 | 3개 | [flowcharts_part5_query.md](./flowcharts_part5_query.md) |

**총 56개 프로세스**

---

## 📑 전체 프로세스 목록

### Part 1. 공통 프로세스 (18개)
| 코드 | 프로세스명 |
|------|----------|
| P100 | 월렛 접근 (walletToken) |
| P102 | 월렛 연결 해제 |
| P103 | 월렛 연결 해제 (CA앱 삭제) |
| P104 | 월렛 삭제 |
| P105 | 연결 CA 목록 조회 |
| P106 | 월렛 접근 사용 |
| P107 | 월렛 PIN 등록/변경 |
| P108 | 월렛 PIN 인증 |
| P109 | 인가 CA 검증 |
| P110 | 심카드 검증 |
| P111 | 인가 토큰 |
| P112 | 월렛 삭제 (Push) |
| P113 | 월렛 삭제 - 로컬 안면정보 변경 (Passive) |
| P114 | 월렛 삭제 - 로컬 안면정보 변경 (Active Exception) |
| P115 | 월렛 삭제 결과 통보 |
| P116 | 월렛 연결해제 통보 |
| P117 | 월렛 연결 정리 (FW2CA) [Draft] |

---

### Part 2. 신원 인증 (12개)
| 코드 | 프로세스명 |
|------|----------|
| P121 | 실명 인증 (도관 방식) |
| P123 | 실명 인증 (직접 방식) |
| P130 | IC카드 인증 (VC 발급용) |
| P131 | 발급 QR 인증 (VC 발급용) |
| P142-2 | 로컬 기반 정부 안면인증 (VC 발급) |
| P142-3 | 서버 기반 정부 안면인증 (VC 발급) |
| P142-4 | 로컬 기반 정부 안면인증 (2nd CA 등록) |
| P142-5 | 서버 기반 정부 안면인증 (2nd CA 등록) |
| P143 | 단말 안면인증 |
| P144 | 서버 안면인증 |
| P150 | 지문인증 상태변경 - Suspend (Passive) |
| P151 | 지문인증 상태변경 - Resume |

---

### Part 3. VC 관리 (10개)
| 코드 | 프로세스명 |
|------|----------|
| P190 | walletId 사용가능 여부 조회 |
| P200 | DID 발급 |
| P210 | 발급 가능 VC 리스트 조회 |
| P211 | VC 발급 |
| P220 | VC 정보 표시 |
| P230 | 주소갱신 VC 발급 |
| P240 | VC 삭제 |
| P250 | Holder 개인키 갱신 |
| P260 | 정부앱 지갑 이관 [Draft] |
| P290 | 2nd CA 등록 (VP 기반 App2App) |

---

### Part 4. VP 제출 (13개)
| 코드 | 프로세스명 |
|------|----------|
| P311-1 | QR-MPM Direct Mode (VP) |
| P311-2 | QR-MPM Direct Mode (ZKP) |
| P311-3 | QR-MPM Direct Mode (Signature+VP) |
| P312-1 | QR-CPM Proxy Mode (VP) |
| P312-2 | QR-CPM Proxy Mode (ZKP) |
| P312-3 | QR-CPM Proxy Direct Mode (VP) |
| P312-4 | QR-CPM Proxy Direct Mode (ZKP) |
| P313-1 | PUSH Direct Mode (VP) |
| P313-2 | PUSH Direct Mode (Signature+VP) |
| P314-1 | APP2APP Indirect Mode (VP) |
| P314-2 | APP2APP Direct Mode |
| P314-3 | APP2APP Indirect Mode (Signature+VP) |
| P314-4 | APP2APP Direct Mode (Signature+VP) |
| P315-1 | NFC Indirect Mode (VP) |

---

### Part 5. 조회 서비스 (3개)
| 코드 | 프로세스명 |
|------|----------|
| P410 | 중계서버 주소 조회 |
| P420 | VC 상태 상세사유 조회 |
| P430 | 장애여부 조회 |

---

*작성일: 2025-12-10*
