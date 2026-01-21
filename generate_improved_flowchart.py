#!/usr/bin/env python3
"""
Generate improved flowchart.json with light mode, detailed mode, and PNG paths
"""
import json
import os

# Process definitions with improved diagrams
processes = [
    {
        "code": "P100",
        "category": "공통",
        "title": "월렛 접근 (walletToken)",
        "summary": "CA 앱이 월렛에 접근하기 위해 walletToken을 발급받는 전체 프로세스",
        "pngPath": "uml/P100_[공통] 월렛접근(walletToken).png",
        "mermaidLite": """flowchart TD
    A[👤 사용자] -->|앱 실행| B[📱 CA앱]
    B -->|토큰 요청| C[🔐 Framework]
    C -->|생성| D[🔑 tempToken]
    D -->|서버 요청| E[🖥️ CAS서버]
    E -->|발급| F[✅ walletToken]
    style A fill:#e3f2fd
    style F fill:#c8e6c9""",
        "mermaid": """sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant CAS as 🖥️ CAS서버
    
    Note over User,CAS: P100: 월렛 접근 (walletToken)
    
    CA->>FW: getWalletState()
    FW-->>CA: {walletStatus}
    
    alt WALLET_NOT_EXIST
        Note right of CA: 1st CA 등록 필요
    else VC_EXIST
        Note right of CA: 2nd CA 등록 가능
    end
    
    CA->>FW: requestTempToken(purpose)
    FW->>TA: tempToken 생성 요청
    TA-->>FW: {nonce, pkgName, purpose, caAppUserId}
    FW->>TA: wrap(tempToken)
    TA-->>FW: wrappedTempToken
    FW-->>CA: {tempToken, wrappedTempToken}
    
    CA->>CAS: walletToken 요청 {tempToken}
    CAS->>CAS: CI 조회 및 sha256_ci 생성
    CAS->>CAS: ECDSA 서명 생성 (Priv_CAS)
    CAS-->>CA: {walletToken, DID_CAS}
    
    CA->>FW: issueWalletHandle(walletToken, did)
    FW->>FW: ECDSA 서명 검증 (Pub_CAS)
    FW->>TA: walletToken 연결 검증
    TA-->>FW: 검증 완료
    FW-->>CA: hWalletToken ✓"""
    },
    {
        "code": "P102",
        "category": "공통",
        "title": "월렛 연결 해제",
        "summary": "사용자가 CA앱과 월렛의 연결을 해제하는 프로세스",
        "pngPath": "uml/P102_[공통] 월렛연결해제.png",
        "mermaidLite": """flowchart TD
    A[👤 사용자] -->|해제 요청| B[📱 CA앱]
    B -->|연결 해제| C[🔧 Framework]
    C -->|토큰 삭제| D[🔐 TrustedApp]
    D -->|통보| E[🖥️ CAS서버]
    E -->|완료| F[✅ 연결 해제]
    style A fill:#e3f2fd
    style F fill:#c8e6c9""",
        "mermaid": """sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant CAS as 🖥️ CAS서버
    
    Note over User,CAS: P102: 월렛 연결 해제
    
    User->>CA: 연결 해제 요청
    CA->>FW: disconnectWallet(hWalletToken)
    FW->>TA: CA 연결정보 삭제
    TA-->>FW: 삭제 완료
    FW->>CAS: 연결해제 통보
    CAS-->>FW: 통보 수신
    FW-->>CA: 해제 완료
    CA->>User: 결과 표시 ✓"""
    },
    {
        "code": "P103",
        "category": "공통",
        "title": "월렛 연결 해제 (CA앱 삭제)",
        "summary": "CA 앱 삭제 시 자동 연결 해제 처리",
        "pngPath": "uml/P103_[공통] 월렛연결해제(CA앱삭제).png",
        "mermaidLite": """flowchart TD
    A[📱 CA앱 삭제] -->|감지| B[🔧 Framework]
    B -->|정리| C[🔐 TrustedApp]
    C -->|통보| D[🖥️ CAS서버]
    D -->|완료| E[✅ 자동 해제]
    style A fill:#ffcdd2
    style E fill:#c8e6c9""",
        "mermaid": """sequenceDiagram
    participant OS as 📲 OS
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant CAS as 🖥️ CAS서버
    
    Note over OS,CAS: P103: CA앱 삭제 시 자동 연결 해제
    
    OS->>FW: 앱 삭제 이벤트 (pkgName)
    FW->>TA: CA 연결정보 조회
    TA-->>FW: {connectedCaInfo}
    FW->>TA: CA 연결정보 삭제
    TA-->>FW: 삭제 완료
    FW->>CAS: 연결해제 통보
    CAS-->>FW: 수신 확인 ✓"""
    },
    {
        "code": "P104",
        "category": "공통",
        "title": "월렛 삭제",
        "summary": "월렛 전체를 삭제하고 모든 VC와 DID를 폐기",
        "pngPath": "uml/P104_[공통] 월렛삭제.png",
        "mermaidLite": """flowchart TD
    A[👤 사용자] -->|삭제 요청| B[📱 CA앱]
    B -->|인증| C[🔐 PIN/생체]
    C -->|삭제| D[🔧 Framework]
    D -->|폐기| E[🖥️ 서버 통보]
    E -->|완료| F[✅ 월렛 삭제]
    style A fill:#e3f2fd
    style F fill:#ffcdd2""",
        "mermaid": """sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant CAS as 🖥️ CAS서버
    
    Note over User,CAS: P104: 월렛 삭제
    
    User->>CA: 월렛 삭제 요청
    CA->>FW: deleteWallet(hWalletToken)
    FW->>User: PIN/생체 인증 요청
    User->>FW: 인증 완료
    FW->>TA: 월렛 데이터 삭제
    TA-->>FW: DID, VC, 키 삭제 완료
    FW->>CAS: 월렛 삭제 통보
    CAS-->>FW: 통보 수신
    FW-->>CA: 삭제 완료
    CA->>User: 결과 표시 ✓"""
    },
    {
        "code": "P105",
        "category": "공통",
        "title": "연결 CA 목록 조회",
        "summary": "월렛에 연결된 CA 앱 목록을 조회",
        "pngPath": "uml/P105_[공통] 연결CA목록조회.png",
        "mermaidLite": """flowchart TD
    A[📱 CA앱] -->|조회 요청| B[🔧 Framework]
    B -->|데이터 조회| C[🔐 TrustedApp]
    C -->|목록 반환| D[📋 CA 목록]
    D -->|표시| E[✅ 조회 완료]
    style A fill:#e3f2fd
    style E fill:#c8e6c9""",
        "mermaid": """sequenceDiagram
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    
    Note over CA,TA: P105: 연결 CA 목록 조회
    
    CA->>FW: getConnectedCaList(hWalletToken)
    FW->>TA: CA 연결 목록 조회
    TA-->>FW: [{pkgName, caAppUserId, connectedAt}]
    FW-->>CA: 연결된 CA 목록 ✓"""
    },
    {
        "code": "P106",
        "category": "공통",
        "title": "월렛 접근 사용",
        "summary": "월렛 데이터 접근 권한 확인 및 사용",
        "pngPath": "uml/P106_[공통] 월렛접근사용.png",
        "mermaidLite": """flowchart TD
    A[📱 CA앱] -->|접근 요청| B[🔧 Framework]
    B -->|권한 확인| C[🔐 TrustedApp]
    C -->|토큰 검증| D[✓ 권한 확인]
    D -->|사용 허용| E[✅ 접근 성공]
    style A fill:#e3f2fd
    style E fill:#c8e6c9""",
        "mermaid": """sequenceDiagram
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    
    Note over CA,TA: P106: 월렛 접근 사용
    
    CA->>FW: accessWallet(hWalletToken, purpose)
    FW->>TA: 토큰 유효성 검증
    TA-->>FW: {isValid, remainingTime}
    FW-->>CA: 접근 허용 ✓"""
    },
    {
        "code": "P107",
        "category": "공통",
        "title": "월렛 PIN 등록/변경",
        "summary": "월렛 PIN 설정 및 변경 프로세스",
        "pngPath": "uml/P107_[공통] 월렛PIN_등록_변경.png",
        "mermaidLite": """flowchart TD
    A[👤 사용자] -->|PIN 설정| B[📱 CA앱]
    B -->|요청| C[🔧 Framework]
    C -->|저장| D[🔐 TrustedApp]
    D -->|암호화 저장| E[🔒 보안 영역]
    E -->|완료| F[✅ PIN 설정 완료]
    style A fill:#e3f2fd
    style F fill:#c8e6c9""",
        "mermaid": """sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    
    Note over User,TA: P107: 월렛 PIN 등록/변경
    
    User->>CA: PIN 설정/변경 요청
    CA->>FW: registerPin(hWalletToken)
    FW->>User: 현재 PIN 입력 (변경 시)
    User->>FW: 현재 PIN
    FW->>TA: PIN 검증
    TA-->>FW: 검증 완료
    FW->>User: 새 PIN 입력
    User->>FW: 새 PIN (2회 입력)
    FW->>TA: 새 PIN 저장 (암호화)
    TA-->>FW: 저장 완료
    FW-->>CA: PIN 설정 완료 ✓"""
    },
    {
        "code": "P108",
        "category": "공통",
        "title": "월렛 PIN 인증",
        "summary": "PIN 입력으로 월렛 접근 인증",
        "pngPath": "uml/P108_[공통] 월렛PIN_인증.png",
        "mermaidLite": """flowchart TD
    A[👤 사용자] -->|PIN 입력| B[📱 CA앱]
    B -->|검증 요청| C[🔧 Framework]
    C -->|PIN 비교| D[🔐 TrustedApp]
    D -->|결과| E{✓ 일치?}
    E -->|성공| F[✅ 인증 완료]
    E -->|실패| G[❌ 재시도]
    style A fill:#e3f2fd
    style F fill:#c8e6c9
    style G fill:#ffcdd2""",
        "mermaid": """sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    
    Note over User,TA: P108: 월렛 PIN 인증
    
    CA->>FW: authenticateWithPin(hWalletToken)
    FW->>User: PIN 입력 요청
    User->>FW: PIN 입력
    FW->>TA: PIN 검증
    
    alt PIN 일치
        TA-->>FW: 인증 성공
        FW-->>CA: 인증 완료 ✓
    else PIN 불일치
        TA-->>FW: 인증 실패 (남은 횟수)
        FW-->>CA: 재시도 요청
    end"""
    },
    {
        "code": "P109",
        "category": "공통",
        "title": "인가 CA 검증",
        "summary": "CA 앱이 정식 인가된 앱인지 검증",
        "pngPath": "uml/P109_[공통] 인가CA검증.png",
        "mermaidLite": """flowchart TD
    A[📱 CA앱] -->|검증 요청| B[🔧 Framework]
    B -->|서명 확인| C[🔐 TrustedApp]
    C -->|정부 서버 조회| D[🏛️ 정부서버]
    D -->|인가 확인| E[✅ 인가된 CA]
    style A fill:#e3f2fd
    style E fill:#c8e6c9""",
        "mermaid": """sequenceDiagram
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant GOV as 🏛️ 정부서버
    
    Note over CA,GOV: P109: 인가 CA 검증
    
    CA->>FW: verifyCaAuthorization()
    FW->>FW: callerInfo 추출 (pkgName, pkgSign)
    FW->>TA: CA 서명 검증
    TA-->>FW: 서명 유효
    FW->>GOV: CA 인가 여부 조회
    GOV-->>FW: {authorized: true, caInfo}
    FW-->>CA: 인가된 CA 확인 ✓"""
    },
    {
        "code": "P110",
        "category": "공통",
        "title": "심카드 검증",
        "summary": "SIM 카드 변경 감지 및 추가 인증",
        "pngPath": "uml/P110_[공통] 심카드검증.png",
        "mermaidLite": """flowchart TD
    A[📲 SIM 변경] -->|감지| B[🔧 Framework]
    B -->|검증| C[🔐 TrustedApp]
    C -->|불일치| D{SIM 일치?}
    D -->|일치| E[✅ 정상 사용]
    D -->|불일치| F[🔒 추가 인증 필요]
    style A fill:#fff3e0
    style E fill:#c8e6c9
    style F fill:#ffcdd2""",
        "mermaid": """sequenceDiagram
    participant OS as 📲 OS
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    
    Note over OS,TA: P110: 심카드 검증
    
    OS->>FW: SIM 상태 변경 감지
    FW->>TA: 저장된 SIM 정보 조회
    TA-->>FW: {storedSimInfo}
    FW->>FW: 현재 SIM과 비교
    
    alt SIM 일치
        FW-->>FW: 정상 진행
    else SIM 불일치
        FW-->>FW: 추가 인증 플래그 설정
        Note right of FW: 다음 접근 시 추가 인증 요구
    end"""
    }
]

# Continue with more processes...
more_processes = [
    {"code": "P111", "category": "공통", "title": "인가 토큰", "summary": "정부 서버 접근을 위한 인가토큰 발급", "pngPath": "uml/P111_[공통] 인가토큰.png"},
    {"code": "P112", "category": "공통", "title": "월렛 삭제 (Push)", "summary": "원격 Push로 월렛 삭제 요청", "pngPath": "uml/P112_[공통] 월렛삭제_push.png"},
    {"code": "P113", "category": "공통", "title": "월렛 삭제 - 안면정보 변경 (Passive)", "summary": "안면정보 변경 시 자동 월렛 삭제", "pngPath": "uml/P113_[공통] 월렛삭제_로컬안면정보변경 (passive).png"},
    {"code": "P114", "category": "공통", "title": "월렛 삭제 - 안면정보 변경 (Active)", "summary": "안면정보 변경 시 재인증 기회 제공", "pngPath": "uml/P114_[공통] 월렛삭제_로컬안면정보변경 (active_exception).png"},
    {"code": "P115", "category": "공통", "title": "월렛 삭제 결과 통보", "summary": "월렛 삭제 완료 후 관련 기관 통보", "pngPath": "uml/P115_[공통] 월렛삭제결과통보.png"},
    {"code": "P116", "category": "공통", "title": "월렛 연결해제 통보", "summary": "연결 해제 완료 후 CA 서버 통보", "pngPath": "uml/P116_[공통] 월렛연결해제통보.png"},
    {"code": "P117", "category": "공통", "title": "월렛 연결 정리 (FW2CA)", "summary": "프레임워크에서 CA로 연결 정리 요청", "pngPath": "uml/P117_[공통] (draft) 월렛연결정리(FW2CA).png"},
    {"code": "P121", "category": "신원인증", "title": "실명 인증 (도관 방식)", "summary": "통신사/카드사를 통한 실명인증", "pngPath": "uml/P121_실명인증(도관방식).png"},
    {"code": "P123", "category": "신원인증", "title": "실명 인증 (직접 방식)", "summary": "신분증 OCR과 진위확인을 통한 실명인증", "pngPath": "uml/P123_실명인증(직접방식).png"},
    {"code": "P130", "category": "신원인증", "title": "IC카드 인증", "summary": "신분증 IC칩 NFC 태깅으로 인증", "pngPath": "uml/P130_[VC 발급] IC카드인증.png"},
    {"code": "P131", "category": "신원인증", "title": "발급 QR 인증", "summary": "창구에서 QR 코드로 발급 인증", "pngPath": "uml/P131_[VC 발급] 발급 QR인증.png"},
    {"code": "P142-2", "category": "신원인증", "title": "로컬 기반 정부 안면인증 (VC 발급)", "summary": "단말기 내에서 안면 비교", "pngPath": "uml/P142-2_로컬기반정부안면인증(VC발급).png"},
    {"code": "P142-3", "category": "신원인증", "title": "서버 기반 정부 안면인증 (VC 발급)", "summary": "정부 서버와 안면 비교", "pngPath": "uml/P142-3_서버기반정부안면인증(VC발급).png"},
    {"code": "P142-4", "category": "신원인증", "title": "로컬 기반 정부 안면인증 (2nd CA)", "summary": "2nd CA 등록을 위한 로컬 안면인증", "pngPath": "uml/P142-4_로컬기반정부안면인증(2nd CA 등록).png"},
    {"code": "P142-5", "category": "신원인증", "title": "서버 기반 정부 안면인증 (2nd CA)", "summary": "2nd CA 등록을 위한 서버 안면인증", "pngPath": "uml/P142-5_서버기반정부안면인증(2nd CA 등록).png"},
    {"code": "P143", "category": "신원인증", "title": "단말 안면인증", "summary": "Face ID를 활용한 빠른 인증", "pngPath": "uml/P143_단말안면인증.png"},
    {"code": "P144", "category": "신원인증", "title": "서버 안면인증", "summary": "서버에서 안면 비교 검증", "pngPath": "uml/P144_서버안면인증.png"},
    {"code": "P150", "category": "신원인증", "title": "지문인증 상태변경 - Suspend", "summary": "지문 변경 시 인증 중지", "pngPath": "uml/P150_지문인증상태변경_suspend (passive).png"},
    {"code": "P151", "category": "신원인증", "title": "지문인증 상태변경 - Resume", "summary": "지문인증 재활성화", "pngPath": "uml/P151_지문인증상태변경_resume.png"},
    {"code": "P190", "category": "VC관리", "title": "walletId 사용가능 여부 조회", "summary": "월렛 ID의 유효성 확인", "pngPath": "uml/P190_walletId 사용가능여부 조회.png"},
    {"code": "P200", "category": "VC관리", "title": "DID 발급", "summary": "분산ID 생성 및 블록체인 등록", "pngPath": "uml/P200_DID 발급.png"},
    {"code": "P210", "category": "VC관리", "title": "발급 가능 VC 리스트 조회", "summary": "사용자가 발급받을 수 있는 VC 목록", "pngPath": "uml/P210_발급가능VC리스트조회.png"},
    {"code": "P211", "category": "VC관리", "title": "VC 발급", "summary": "발급기관이 서명된 VC를 발급", "pngPath": "uml/P211_VC 발급.png"},
    {"code": "P220", "category": "VC관리", "title": "VC 정보 표시", "summary": "월렛에 저장된 VC 정보를 화면에 표시", "pngPath": "uml/P220_VC정보표시.png"},
    {"code": "P230", "category": "VC관리", "title": "주소갱신 VC 발급", "summary": "주소 변경 시 VC 갱신", "pngPath": "uml/P230_주소갱신VC발급.png"},
    {"code": "P240", "category": "VC관리", "title": "VC 삭제", "summary": "특정 VC만 선택적으로 삭제", "pngPath": "uml/P240_VC삭제.png"},
    {"code": "P250", "category": "VC관리", "title": "Holder 개인키 갱신", "summary": "개인키 갱신 및 DID Document 업데이트", "pngPath": "uml/P250_Holder개인키갱신.png"},
    {"code": "P260", "category": "VC관리", "title": "정부앱 지갑 이관", "summary": "기기 변경 시 지갑 이관", "pngPath": "uml/P260_(draft) 정부앱 지갑이관.png"},
    {"code": "P290", "category": "VC관리", "title": "2nd CA 등록 (VP 기반)", "summary": "VP를 활용한 2nd CA 앱 등록", "pngPath": "uml/P290_2nd CA 등록(VP기반_App2App).png"},
    {"code": "P311-1", "category": "VP제출", "title": "QR-MPM Direct Mode (VP)", "summary": "검증기관 QR을 스캔하여 VP 직접 제출", "pngPath": "uml/P311-1_QR-MPM direct mode_VP.png"},
    {"code": "P311-2", "category": "VP제출", "title": "QR-MPM Direct Mode (ZKP)", "summary": "영지식증명으로 최소 정보만 제출", "pngPath": "uml/P311-2_QR-MPM direct mode_ZKP.png"},
    {"code": "P311-3", "category": "VP제출", "title": "QR-MPM Direct Mode (Signature+VP)", "summary": "전자서명 포함 VP 제출", "pngPath": "uml/P311-3_QR-MPM direct mode_Signature+VP.png"},
    {"code": "P312-1", "category": "VP제출", "title": "QR-CPM Proxy Mode (VP)", "summary": "내 QR을 보여주고 중계서버 경유", "pngPath": "uml/P312-1_QR-CPM proxy mode_VP.png"},
    {"code": "P312-2", "category": "VP제출", "title": "QR-CPM Proxy Mode (ZKP)", "summary": "ZKP를 QR로 제시", "pngPath": "uml/P312-2_QR-CPM proxy mode_ZKP.png"},
    {"code": "P312-3", "category": "VP제출", "title": "QR-CPM Proxy Direct Mode (VP)", "summary": "Proxy 경유 후 직접 연결", "pngPath": "uml/P312-3_QR-CPM proxy direct mode_VP.png"},
    {"code": "P312-4", "category": "VP제출", "title": "QR-CPM Proxy Direct Mode (ZKP)", "summary": "ZKP로 Proxy Direct 제출", "pngPath": "uml/P312-4_QR-CPM proxy direct mode_ZKP.png"},
    {"code": "P313-1", "category": "VP제출", "title": "PUSH Direct Mode (VP)", "summary": "Push 알림으로 VP 요청 및 제출", "pngPath": "uml/P313-1_PUSH direct mode_VP.png"},
    {"code": "P313-2", "category": "VP제출", "title": "PUSH Direct Mode (Signature+VP)", "summary": "Push로 전자서명 포함 제출", "pngPath": "uml/P313-2_PUSH direct mode_Signature+VP.png"},
    {"code": "P314-1", "category": "VP제출", "title": "APP2APP Indirect Mode (VP)", "summary": "앱 간 호출로 VP 전달", "pngPath": "uml/P314-1_APP2APP indirect mode_VP.png"},
    {"code": "P314-2", "category": "VP제출", "title": "APP2APP Direct Mode", "summary": "앱 간 호출, 서버로 직접 전송", "pngPath": "uml/P314-2_APP2APP direct mode.png"},
]

# Default templates for processes without custom diagrams
def get_default_lite(title, category):
    return f"""flowchart TD
    A[👤 사용자] -->|시작| B[📱 CA앱]
    B -->|요청| C[🔧 Framework]
    C -->|처리| D[🖥️ 서버]
    D -->|완료| E[✅ 결과]
    style A fill:#e3f2fd
    style E fill:#c8e6c9"""

def get_default_full(code, title, category):
    if category == "신원인증":
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant AUTH as 🔐 인증기관
    participant GOV as 🏛️ 정부서버
    
    Note over User,GOV: {code}: {title}
    
    User->>CA: 인증 시작
    CA->>FW: 인증 화면 요청
    FW->>User: 정보 입력/촬영
    User->>FW: 정보 제출
    FW->>AUTH: 인증 요청
    AUTH->>GOV: 진위 확인
    GOV-->>AUTH: 확인 결과
    AUTH-->>FW: 인증 결과
    
    alt 인증 성공
        FW-->>CA: 인증 성공
        CA->>User: 완료 ✓
    else 인증 실패
        FW-->>CA: 재시도 요청
        CA->>User: 다시 시도
    end"""
    elif category == "VC관리":
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant ISS as 🏛️ 발급기관
    participant BC as ⛓️ 블록체인
    
    Note over User,BC: {code}: {title}
    
    User->>CA: VC 요청
    CA->>FW: 처리 시작
    FW->>User: 본인 인증
    User->>FW: PIN/생체 인증
    FW->>TA: 보안 처리
    TA-->>FW: 처리 완료
    FW->>ISS: VC 요청/처리
    ISS->>BC: 상태 등록
    BC-->>ISS: 등록 완료
    ISS-->>FW: VC 발급/처리
    FW->>TA: 안전 저장
    TA-->>FW: 저장 완료
    FW-->>CA: 완료
    CA->>User: VC 처리 완료 ✓"""
    elif category == "VP제출":
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant SP as 🏢 검증기관
    participant BC as ⛓️ 블록체인
    
    Note over User,BC: {code}: {title}
    
    User->>CA: VP 제출 시작
    CA->>FW: 제출 화면
    FW->>User: 제출 정보 확인
    User->>FW: 동의 + PIN 인증
    FW->>FW: VP 생성
    FW->>SP: VP 전송
    SP->>BC: 서명 검증
    BC-->>SP: 검증 완료
    SP->>SP: 클레임 추출
    SP-->>FW: 검증 결과
    FW-->>CA: 제출 완료
    CA->>User: 본인확인 완료 ✓"""
    else:
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant CAS as 🖥️ CAS서버
    
    Note over User,CAS: {code}: {title}
    
    User->>CA: 기능 요청
    CA->>FW: 처리 요청
    FW->>TA: 보안 처리
    TA-->>FW: 처리 결과
    FW->>CAS: 서버 요청
    CAS-->>FW: 결과 반환
    FW-->>CA: 처리 완료
    CA->>User: 결과 표시 ✓"""

# Merge all processes
all_processes = processes.copy()
for p in more_processes:
    # Check if already exists with custom diagrams
    existing = next((x for x in all_processes if x["code"] == p["code"]), None)
    if not existing:
        p["mermaidLite"] = get_default_lite(p["title"], p["category"])
        p["mermaid"] = get_default_full(p["code"], p["title"], p["category"])
        all_processes.append(p)

# Write to JSON
output_path = os.path.join(os.path.dirname(__file__), "flowchart.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_processes, f, ensure_ascii=False, indent=2)

print(f"✅ Generated flowchart.json with {len(all_processes)} processes")
print(f"   Output: {output_path}")
