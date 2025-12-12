import json
import os

# UML 파일 목록과 정보
uml_data = [
    {"code": "P100", "category": "공통", "title": "월렛 접근 (walletToken)", "summary": "CA 앱이 월렛에 접근하기 위해 walletToken을 발급받는 전체 프로세스"},
    {"code": "P102", "category": "공통", "title": "월렛 연결 해제", "summary": "사용자가 CA앱과 월렛의 연결을 해제하는 프로세스"},
    {"code": "P103", "category": "공통", "title": "월렛 연결 해제 (CA앱 삭제)", "summary": "CA 앱 삭제 시 자동 연결 해제 처리"},
    {"code": "P104", "category": "공통", "title": "월렛 삭제", "summary": "월렛 전체를 삭제하고 모든 VC와 DID를 폐기"},
    {"code": "P105", "category": "공통", "title": "연결 CA 목록 조회", "summary": "월렛에 연결된 CA 앱 목록을 조회"},
    {"code": "P106", "category": "공통", "title": "월렛 접근 사용", "summary": "월렛 데이터 접근 권한 확인 및 사용"},
    {"code": "P107", "category": "공통", "title": "월렛 PIN 등록/변경", "summary": "월렛 PIN 설정 및 변경 프로세스"},
    {"code": "P108", "category": "공통", "title": "월렛 PIN 인증", "summary": "PIN 입력으로 월렛 접근 인증"},
    {"code": "P109", "category": "공통", "title": "인가 CA 검증", "summary": "CA 앱이 정식 인가된 앱인지 검증"},
    {"code": "P110", "category": "공통", "title": "심카드 검증", "summary": "SIM 카드 변경 감지 및 추가 인증"},
    {"code": "P111", "category": "공통", "title": "인가 토큰", "summary": "정부 서버 접근을 위한 인가토큰 발급"},
    {"code": "P112", "category": "공통", "title": "월렛 삭제 (Push)", "summary": "원격 Push로 월렛 삭제 요청"},
    {"code": "P113", "category": "공통", "title": "월렛 삭제 - 안면정보 변경 (Passive)", "summary": "안면정보 변경 시 자동 월렛 삭제"},
    {"code": "P114", "category": "공통", "title": "월렛 삭제 - 안면정보 변경 (Active)", "summary": "안면정보 변경 시 재인증 기회 제공"},
    {"code": "P115", "category": "공통", "title": "월렛 삭제 결과 통보", "summary": "월렛 삭제 완료 후 관련 기관 통보"},
    {"code": "P116", "category": "공통", "title": "월렛 연결해제 통보", "summary": "연결 해제 완료 후 CA 서버 통보"},
    {"code": "P117", "category": "공통", "title": "월렛 연결 정리 (FW2CA)", "summary": "프레임워크에서 CA로 연결 정리 요청"},
    {"code": "P121", "category": "신원인증", "title": "실명 인증 (도관 방식)", "summary": "통신사/카드사를 통한 실명인증"},
    {"code": "P123", "category": "신원인증", "title": "실명 인증 (직접 방식)", "summary": "신분증 OCR과 진위확인을 통한 실명인증"},
    {"code": "P130", "category": "신원인증", "title": "IC카드 인증", "summary": "신분증 IC칩 NFC 태깅으로 인증"},
    {"code": "P131", "category": "신원인증", "title": "발급 QR 인증", "summary": "창구에서 QR 코드로 발급 인증"},
    {"code": "P142-2", "category": "신원인증", "title": "로컬 기반 정부 안면인증 (VC 발급)", "summary": "단말기 내에서 안면 비교"},
    {"code": "P142-3", "category": "신원인증", "title": "서버 기반 정부 안면인증 (VC 발급)", "summary": "정부 서버와 안면 비교"},
    {"code": "P142-4", "category": "신원인증", "title": "로컬 기반 정부 안면인증 (2nd CA)", "summary": "2nd CA 등록을 위한 로컬 안면인증"},
    {"code": "P142-5", "category": "신원인증", "title": "서버 기반 정부 안면인증 (2nd CA)", "summary": "2nd CA 등록을 위한 서버 안면인증"},
    {"code": "P143", "category": "신원인증", "title": "단말 안면인증", "summary": "Face ID를 활용한 빠른 인증"},
    {"code": "P144", "category": "신원인증", "title": "서버 안면인증", "summary": "서버에서 안면 비교 검증"},
    {"code": "P150", "category": "신원인증", "title": "지문인증 상태변경 - Suspend", "summary": "지문 변경 시 인증 중지"},
    {"code": "P151", "category": "신원인증", "title": "지문인증 상태변경 - Resume", "summary": "지문인증 재활성화"},
    {"code": "P190", "category": "VC관리", "title": "walletId 사용가능 여부 조회", "summary": "월렛 ID의 유효성 확인"},
    {"code": "P200", "category": "VC관리", "title": "DID 발급", "summary": "분산ID 생성 및 블록체인 등록"},
    {"code": "P210", "category": "VC관리", "title": "발급 가능 VC 리스트 조회", "summary": "사용자가 발급받을 수 있는 VC 목록"},
    {"code": "P211", "category": "VC관리", "title": "VC 발급", "summary": "발급기관이 서명된 VC를 발급"},
    {"code": "P220", "category": "VC관리", "title": "VC 정보 표시", "summary": "월렛에 저장된 VC 정보를 화면에 표시"},
    {"code": "P230", "category": "VC관리", "title": "주소갱신 VC 발급", "summary": "주소 변경 시 VC 갱신"},
    {"code": "P240", "category": "VC관리", "title": "VC 삭제", "summary": "특정 VC만 선택적으로 삭제"},
    {"code": "P250", "category": "VC관리", "title": "Holder 개인키 갱신", "summary": "개인키 갱신 및 DID Document 업데이트"},
    {"code": "P260", "category": "VC관리", "title": "정부앱 지갑 이관", "summary": "기기 변경 시 지갑 이관"},
    {"code": "P290", "category": "VC관리", "title": "2nd CA 등록 (VP 기반)", "summary": "VP를 활용한 2nd CA 앱 등록"},
    {"code": "P311-1", "category": "VP제출", "title": "QR-MPM Direct Mode (VP)", "summary": "검증기관 QR을 스캔하여 VP 직접 제출"},
    {"code": "P311-2", "category": "VP제출", "title": "QR-MPM Direct Mode (ZKP)", "summary": "영지식증명으로 최소 정보만 제출"},
    {"code": "P311-3", "category": "VP제출", "title": "QR-MPM Direct Mode (Signature+VP)", "summary": "전자서명 포함 VP 제출"},
    {"code": "P312-1", "category": "VP제출", "title": "QR-CPM Proxy Mode (VP)", "summary": "내 QR을 보여주고 중계서버 경유"},
    {"code": "P312-2", "category": "VP제출", "title": "QR-CPM Proxy Mode (ZKP)", "summary": "ZKP를 QR로 제시"},
    {"code": "P312-3", "category": "VP제출", "title": "QR-CPM Proxy Direct Mode (VP)", "summary": "Proxy 경유 후 직접 연결"},
    {"code": "P312-4", "category": "VP제출", "title": "QR-CPM Proxy Direct Mode (ZKP)", "summary": "ZKP로 Proxy Direct 제출"},
    {"code": "P313-1", "category": "VP제출", "title": "PUSH Direct Mode (VP)", "summary": "Push 알림으로 VP 요청 및 제출"},
    {"code": "P313-2", "category": "VP제출", "title": "PUSH Direct Mode (Signature+VP)", "summary": "Push로 전자서명 포함 제출"},
    {"code": "P314-1", "category": "VP제출", "title": "APP2APP Indirect Mode (VP)", "summary": "앱 간 호출로 VP 전달"},
    {"code": "P314-2", "category": "VP제출", "title": "APP2APP Direct Mode", "summary": "앱 간 호출, 서버로 직접 전송"},
    {"code": "P314-3", "category": "VP제출", "title": "APP2APP Indirect Mode (Signature+VP)", "summary": "앱 간 전자서명 포함 전달"},
    {"code": "P314-4", "category": "VP제출", "title": "APP2APP Direct Mode (Signature+VP)", "summary": "앱 간 호출, 서명+VP 직접 전송"},
    {"code": "P315-1", "category": "VP제출", "title": "NFC Indirect Mode (VP)", "summary": "NFC 태깅으로 VP 제출"},
    {"code": "P410", "category": "조회", "title": "중계서버 주소 조회", "summary": "VP 제출 시 사용할 중계서버 주소 조회"},
    {"code": "P420", "category": "조회", "title": "VC 상태 상세사유 조회", "summary": "VC 정지/폐기 사유 확인"},
    {"code": "P430", "category": "조회", "title": "장애여부 조회", "summary": "시스템 장애 상태 확인"},
]

# 라이트 버전 (간단한 플로우차트)
def get_lite_mermaid(code, title):
    templates = {
        "공통": "flowchart TD\n    A[사용자] -->|요청| B[CA앱]\n    B -->|처리| C[Framework]\n    C -->|검증| D[서버]\n    D -->|응답| E[완료 ✓]\n    style A fill:#e1f5fe\n    style E fill:#c8e6c9",
        "신원인증": "flowchart TD\n    A[사용자] -->|인증시작| B[CA앱]\n    B -->|인증요청| C[인증기관]\n    C -->|검증| D{성공?}\n    D -->|예| E[인증완료 ✓]\n    D -->|아니오| F[재시도]\n    style A fill:#e1f5fe\n    style E fill:#c8e6c9",
        "VC관리": "flowchart TD\n    A[사용자] -->|VC요청| B[CA앱]\n    B -->|처리| C[Framework]\n    C -->|발급/관리| D[발급기관]\n    D -->|블록체인등록| E[블록체인]\n    E -->|완료| F[VC처리완료 ✓]\n    style A fill:#e1f5fe\n    style F fill:#c8e6c9",
        "VP제출": "flowchart TD\n    A[사용자] -->|VP제출| B[CA앱]\n    B -->|VP생성| C[Framework]\n    C -->|전송| D[검증기관]\n    D -->|서명검증| E[블록체인]\n    E -->|확인| F[본인확인완료 ✓]\n    style A fill:#e1f5fe\n    style F fill:#c8e6c9",
        "조회": "flowchart TD\n    A[CA앱] -->|조회요청| B[서버]\n    B -->|상태확인| C[DB/블록체인]\n    C -->|결과| D[응답]\n    D -->|표시| E[조회완료 ✓]\n    style A fill:#fff3e0\n    style E fill:#c8e6c9",
    }
    return templates.get(code.split("-")[0][:1] == "P" and uml_data[0]["category"], templates["공통"])

# 상세 버전 시퀀스 다이어그램 템플릿
def get_full_mermaid(item):
    code = item["code"]
    cat = item["category"]
    
    if cat == "공통":
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant CAS as 🖥️ CAS서버
    participant GOV as 🏛️ 정부서버
    
    Note over User,GOV: {code}: {item['title']}
    
    User->>CA: 기능 요청
    CA->>FW: 처리 요청
    FW->>TA: 보안 처리
    TA-->>FW: 처리 결과
    FW->>CAS: 서버 요청
    CAS->>GOV: 정부 연동
    GOV-->>CAS: 응답
    CAS-->>FW: 결과 반환
    FW-->>CA: 처리 완료
    CA->>User: 결과 표시 ✓"""
    
    elif cat == "신원인증":
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant AUTH as 🔐 인증기관
    participant GOV as 🏛️ 정부서버
    
    Note over User,GOV: {code}: {item['title']}
    
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
    
    elif cat == "VC관리":
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant TA as 🔐 TrustedApp
    participant ISS as 🏛️ 발급기관
    participant BC as ⛓️ 블록체인
    
    Note over User,BC: {code}: {item['title']}
    
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
    
    elif cat == "VP제출":
        return f"""sequenceDiagram
    participant User as 👤 사용자
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant SP as 🏢 검증기관
    participant BC as ⛓️ 블록체인
    
    Note over User,BC: {code}: {item['title']}
    
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
    
    else:  # 조회
        return f"""sequenceDiagram
    participant CA as 📱 CA앱
    participant FW as 🔧 Framework
    participant CAS as 🖥️ CAS서버
    participant BC as ⛓️ 블록체인
    
    Note over CA,BC: {code}: {item['title']}
    
    CA->>FW: 조회 요청
    FW->>CAS: API 호출
    CAS->>BC: 상태 조회
    BC-->>CAS: 상태 정보
    CAS-->>FW: 결과 반환
    FW-->>CA: 조회 완료 ✓"""

# JSON 생성
flowchart_items = []
for item in uml_data:
    flowchart_items.append({
        "code": item["code"],
        "category": item["category"],
        "title": item["title"],
        "summary": item["summary"],
        "mermaidLite": f"flowchart TD\n    A[사용자] -->|시작| B[CA앱]\n    B -->|처리| C[서버]\n    C -->|완료| D[결과 ✓]\n    style A fill:#e1f5fe\n    style D fill:#c8e6c9",
        "mermaid": get_full_mermaid(item)
    })

# 저장
output_path = os.path.join(os.path.dirname(__file__), "flowchart.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(flowchart_items, f, ensure_ascii=False, indent=2)

print(f"✅ flowchart.json 생성 완료! ({len(flowchart_items)}개 항목)")
