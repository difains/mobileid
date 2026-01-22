/**
 * 모바일 신분증 통합 가이드 - 메인 애플리케이션
 * @description 용어집, 코드집, 플로우차트, 체크리스트 등 통합 관리
 */

// ========================================
// 전역 상태 관리
// ========================================
const AppState = {
    glossaryData: [],
    codeData: [],
    flowchartData: [],
    currentView: 'glossary',
    currentData: [],
    searchQuery: '',
    categoryFilter: '',
    checklistCatFilter: '전체',
    screenTypeFilter: '전체',
    screenMgmtData: [],
    screenMgmtL1Filter: '',
    screenMgmtTypeFilter: '',
    screenMgmtSearchQuery: '',
    flowchartVersion: 'full',
    umlVersion: '1.5.0'  // 기본 UML 버전 (1.4.2 또는 1.5.0)
};

// ========================================
// 쉬운 해설 데이터
// ========================================
const easyExplanations = {
    "모바일신분증신원관리 플랫폼": "휴대폰으로 신분증을 발급받고 사용할 수 있게 해주는 전체 시스템이에요. 🎢",
    "모바일신분증서버": "정부에서 운영하는 큰 컴퓨터예요. 여러분의 모바일 신분증을 만들어주고 관리해줘요. 👨‍🏫",
    "클레임 (Claim)": "신분증에 적혀있는 정보 하나하나예요. '이름: 홍길동' 같은 것들이죠! 🧩",
    "크리덴셜 (Credential)": "여러 개의 정보를 모아놓은 것이에요. 신분증 전체라고 생각하면 돼요! 🖼️",
    "VC (Verified Credential)": "진짜인지 확인된 디지털 신분증이에요. 선생님이 도장 찍어준 학생증 같아요! ✅",
    "VP (Verified Presentation)": "확인된 신분증에서 필요한 정보만 보여주는 거예요. 📝",
    "분산ID (DID)": "인터넷에서 쓰는 특별한 이름표예요. 여러곳에서 함께 관리해서 더 안전해요! 🌐",
    "월렛(Wallet)": "디지털 신분증을 안전하게 보관하는 전자 지갑이에요! 👛",
    "CA (Certified App)": "모바일 신분증을 보여주고 사용할 수 있는 앱이에요! 📱",
    "TEE (신뢰실행환경)": "휴대폰 안에 있는 아주 안전한 금고 같은 곳이에요! 🔐",
    "QR-CPM": "내가 QR코드를 보여주면 상대방이 스캔하는 방식이에요! 📲",
    "QR-MPM": "상대방 QR코드를 내가 스캔하는 방식이에요! 📷",
    "NFC": "휴대폰을 가까이 대면 정보가 전달되는 기술이에요! 💳",
    "ZKP": "비밀을 지키면서 증명하는 마법 같은 기술이에요! 🎩✨"
};

// ========================================
// 체크리스트 데이터
// ========================================
const checklistData = [
    { category: "규격", item: "CAS 서버, SP 서버, Proxy 서버 연계 구축", detail: "기존 시스템과 독립적인 구성 및 행정안전부 서버와의 통신 인터페이스 구현." },
    { category: "규격", item: "모바일 신분증 서버 기능 구현", detail: "인가 토큰/월렛 토큰 생성, 발급 요청, 본인확인 및 실명확인 처리." },
    { category: "규격", item: "모바일 신분증 앱 구현", detail: "VC 발급, 삭제, 상태 조회, 목록 조회 기능." },
    { category: "규격", item: "2nd CA 등록 및 2nd VC 발급", detail: "월렛에 추가 모바일 신분증 발급을 위한 절차 구현." },
    { category: "규격", item: "월렛 연결/해제/삭제 기능", detail: "CA 앱 로그인 시 월렛 연결, 사용자 변경 시 해제 로직." },
    { category: "규격", item: "VP 제출 기능 구현", detail: "QR-CPM, QR-MPM, App2App, Push 등 다양한 제출 방식 지원." },
    { category: "규격", item: "삼성전자 월렛 연결 기능", detail: "로컬 기반 정부 안면인증, DID 발급, IC카드 인증 구현." },
    { category: "규격", item: "신분증 선택 및 약관 동의", detail: "발급 가능한 신분증 목록 제공, 이용약관 동의 절차." },
    { category: "규격", item: "IC카드 PIN 입력 및 인증", detail: "IC카드 신분증 태깅 후 PIN 입력 인증 구현." },
    { category: "규격", item: "신분증 발급 완료 프로세스", detail: "안면인증 성공 후 VC 발급 및 월렛 비밀번호 입력." },
    { category: "규격", item: "OS 지문 정보 변경 대응", detail: "지문 등록 정보 변경 시 인증 상태 변경." },
    { category: "규격", item: "CA-신분증 조회 및 갱신", detail: "VC 상태 확인, 주소 갱신, 개인키 만료 알림." },
    { category: "규격", item: "CA 처리 모니터링 인터페이스", detail: "CA 처리 내역 수집 및 모니터링 시스템." },
    { category: "보안", item: "독립적인 시스템 구축", detail: "CA 사업자 평가기준 충족을 위한 독립 시스템." },
    { category: "보안", item: "암호화 알고리즘 및 규격 준수", detail: "안전한 암호화 및 행정안전부 기술 규격 준수." },
    { category: "보안", item: "통신 구간 보호", detail: "모든 통신에 TLS 1.2 이상 암호화 적용." },
    { category: "보안", item: "클라이언트(앱) 보안", detail: "루팅/탈옥 탐지, 앱 난독화, 스크린샷 방지." },
    { category: "보안", item: "서버 보안", detail: "CSRF 방지, SQL Injection 방어, IP 접근 제어." },
    { category: "보안", item: "데이터 관리", detail: "개인정보보호법에 따른 암호화 및 파기 정책." },
    { category: "보안", item: "FDS 연동", detail: "이상 행위 탐지 FDS 룰 추가." },
    { category: "보안", item: "데이터 최소화 원칙", detail: "필요한 최소한의 정보만 요구하고 처리." },
    { category: "관리", item: "안정적 서비스 운영", detail: "24/365 서비스 및 재해복구시스템(DR) 구축." },
    { category: "관리", item: "표준 개발방법론 적용", detail: "IT 표준절차, 개발방법론, 프로젝트 관리 도구." },
    { category: "관리", item: "품질 관리 활동", detail: "품질 관리 조직, 품질 보증, 소스코드 인스펙션." },
    { category: "관리", item: "모니터링 및 로깅", detail: "성공률, 실패 건수 실시간 대시보드." },
    { category: "관리", item: "장애 대응 계획", detail: "API 서버, 네트워크 장애 대응 시나리오." },
    { category: "관리", item: "고객 지원 체계", detail: "콜센터, 영업점 직원 교육 및 매뉴얼." },
    { category: "관리", item: "CMS 활용", detail: "안내 페이지, UI 텍스트, 이용약관 관리." },
    { category: "관리", item: "그룹웨어/KMS 연계", detail: "업무 절차, 매뉴얼 게시 및 공지." },
    { category: "통신", item: "모든 통신 구간 암호화", detail: "클라이언트-서버, 서버-행안부 TLS 1.2 이상." },
    { category: "통신", item: "보안 채널 구축", detail: "진위확인 API 연동 전문 개발, 방화벽 정책." }
];

// ========================================
// 화면목록 데이터 (1Depth~4Depth 포함)
// ========================================
const screenData = [
    // 발급
    { no: 1, d1: "발급", d2: "VC발급", d3: "공통", d4: "메인", id: "VC_ISS_000", name: "모바일 신분증 메인", desc: "신분증 발급 서비스 진입 화면", type: "발급" },
    { no: 2, d1: "발급", d2: "VC발급", d3: "공통", d4: "안내", id: "VC_ISS_001", name: "신분증 발급 안내", desc: "서비스 소개 및 발급 안내", type: "발급" },
    { no: 3, d1: "발급", d2: "VC발급", d3: "공통", d4: "약관", id: "VC_ISS_002", name: "약관 동의", desc: "서비스 이용 약관 동의", type: "발급" },
    { no: 4, d1: "발급", d2: "VC발급", d3: "본인인증", d4: "선택", id: "VC_ISS_003", name: "본인 인증 선택", desc: "인증 방법 선택 화면", type: "발급" },
    { no: 5, d1: "발급", d2: "VC발급", d3: "본인인증", d4: "간편인증", id: "VC_ISS_004", name: "간편인증", desc: "PASS, 카카오, 네이버 등", type: "발급" },
    { no: 6, d1: "발급", d2: "VC발급", d3: "본인인증", d4: "공동인증서", id: "VC_ISS_005", name: "공동인증서", desc: "공동인증서 인증", type: "발급" },
    { no: 7, d1: "발급", d2: "VC발급", d3: "보안설정", d4: "PIN", id: "VC_ISS_006", name: "PIN 설정", desc: "6자리 보안 PIN 설정", type: "발급" },
    { no: 8, d1: "발급", d2: "VC발급", d3: "보안설정", d4: "생체인증", id: "VC_ISS_007", name: "생체 인증 등록", desc: "Face ID / Touch ID 등록", type: "발급" },
    { no: 9, d1: "발급", d2: "VC발급", d3: "신분증선택", d4: "종류", id: "VC_ISS_008", name: "신분증 종류 선택", desc: "주민/운전면허 선택", type: "발급" },
    { no: 10, d1: "발급", d2: "VC발급", d3: "발급처리", d4: "진행", id: "VC_ISS_009", name: "발급 진행", desc: "발급 처리 중 로딩", type: "발급" },
    { no: 11, d1: "발급", d2: "VC발급", d3: "발급처리", d4: "완료", id: "VC_ISS_010", name: "발급 완료", desc: "발급 완료 안내", type: "발급" },
    { no: 12, d1: "발급", d2: "주민등록증", d3: "정보확인", d4: "확인", id: "VC_ISS_ID_001", name: "주민등록증 정보 확인", desc: "발급 정보 확인 화면", type: "발급" },
    { no: 13, d1: "발급", d2: "주민등록증", d3: "발급완료", d4: "미리보기", id: "VC_ISS_ID_002", name: "주민등록증 발급 완료", desc: "발급된 신분증 미리보기", type: "발급" },
    { no: 14, d1: "발급", d2: "운전면허증", d3: "정보입력", d4: "입력", id: "VC_ISS_DL_001", name: "운전면허증 정보 입력", desc: "면허번호 등 정보 입력", type: "발급" },
    { no: 15, d1: "발급", d2: "운전면허증", d3: "정보확인", d4: "확인", id: "VC_ISS_DL_002", name: "운전면허증 정보 확인", desc: "발급 정보 확인 화면", type: "발급" },
    { no: 16, d1: "발급", d2: "운전면허증", d3: "발급완료", d4: "미리보기", id: "VC_ISS_DL_003", name: "운전면허증 발급 완료", desc: "발급된 신분증 미리보기", type: "발급" },
    // 사용
    { no: 17, d1: "사용", d2: "메인", d3: "홈", d4: "목록", id: "VC_USE_000", name: "모바일 신분증 홈", desc: "발급된 신분증 목록 표시", type: "사용" },
    { no: 18, d1: "사용", d2: "메인", d3: "상세", d4: "정보", id: "VC_USE_001", name: "신분증 상세", desc: "선택한 신분증 상세 정보", type: "사용" },
    { no: 19, d1: "사용", d2: "메인", d3: "인증", d4: "요청", id: "VC_USE_002", name: "인증 요청", desc: "Face ID / PIN 인증", type: "사용" },
    { no: 20, d1: "사용", d2: "제시", d3: "방법선택", d4: "선택", id: "VC_PRES_001", name: "제시 방법 선택", desc: "QR코드 / NFC 선택", type: "사용" },
    { no: 21, d1: "사용", d2: "제시", d3: "QR", d4: "생성", id: "VC_PRES_002", name: "QR 코드 생성", desc: "동적 QR 코드 표시", type: "사용" },
    { no: 22, d1: "사용", d2: "제시", d3: "NFC", d4: "대기", id: "VC_PRES_003", name: "NFC 대기", desc: "NFC 태그 대기 화면", type: "사용" },
    { no: 23, d1: "사용", d2: "제시", d3: "완료", d4: "결과", id: "VC_PRES_004", name: "제시 완료", desc: "제시 결과 안내", type: "사용" },
    { no: 24, d1: "사용", d2: "VP제출", d3: "요청수신", d4: "표시", id: "VP_SUB_001", name: "VP 요청 수신", desc: "VP 요청 내용 표시", type: "사용" },
    { no: 25, d1: "사용", d2: "VP제출", d3: "항목선택", d4: "체크", id: "VP_SUB_002", name: "제출 항목 선택", desc: "필수/선택 항목 체크", type: "사용" },
    { no: 26, d1: "사용", d2: "VP제출", d3: "확인", d4: "최종확인", id: "VP_SUB_003", name: "제출 확인", desc: "제출 전 최종 확인", type: "사용" },
    { no: 27, d1: "사용", d2: "VP제출", d3: "완료", d4: "안내", id: "VP_SUB_004", name: "제출 완료", desc: "VP 제출 완료 안내", type: "사용" },
    { no: 28, d1: "사용", d2: "검증", d3: "진입", d4: "선택", id: "VC_VRF_001", name: "검증 모드 진입", desc: "QR 스캔 / NFC 인식 선택", type: "사용" },
    { no: 29, d1: "사용", d2: "검증", d3: "QR", d4: "스캔", id: "VC_VRF_002", name: "QR 스캔", desc: "카메라로 QR 코드 스캔", type: "사용" },
    { no: 30, d1: "사용", d2: "검증", d3: "NFC", d4: "인식", id: "VC_VRF_003", name: "NFC 인식", desc: "NFC 태그 인식", type: "사용" },
    { no: 31, d1: "사용", d2: "검증", d3: "결과", d4: "유효", id: "VC_VRF_004", name: "검증 결과(유효)", desc: "유효한 신분증 정보 표시", type: "사용" },
    { no: 32, d1: "사용", d2: "검증", d3: "결과", d4: "무효", id: "VC_VRF_005", name: "검증 결과(무효)", desc: "무효/만료 안내", type: "사용" },
    { no: 33, d1: "사용", d2: "설정", d3: "메인", d4: "목록", id: "VC_SET_001", name: "설정 메인", desc: "설정 메뉴 목록", type: "사용" },
    { no: 34, d1: "사용", d2: "설정", d3: "보안", d4: "변경", id: "VC_SET_002", name: "보안 설정", desc: "PIN/생체인증 변경", type: "사용" },
    { no: 35, d1: "사용", d2: "설정", d3: "신분증", d4: "관리", id: "VC_SET_003", name: "신분증 관리", desc: "갱신/삭제 관리", type: "사용" },
    { no: 36, d1: "사용", d2: "설정", d3: "이용내역", d4: "조회", id: "VC_SET_004", name: "이용 내역", desc: "제시/검증 이력 조회", type: "사용" },
    { no: 37, d1: "사용", d2: "설정", d3: "알림", d4: "설정", id: "VC_SET_005", name: "알림 설정", desc: "푸시 알림 설정", type: "사용" }
];

// ========================================
// 초기화 함수
// ========================================
mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' });

/**
 * 데이터 로드 함수
 * @description JSON 파일들을 비동기로 로드하고 초기화
 */
async function loadData() {
    try {
        const [glossaryRes, codeRes, flowchartRes] = await Promise.all([
            fetch('glossary.json'),
            fetch('code.json'),
            fetch('flowchart.json')
        ]);

        AppState.glossaryData = await glossaryRes.json();
        AppState.codeData = await codeRes.json();
        AppState.flowchartData = await flowchartRes.json();

        // 탭 카운트 업데이트
        document.getElementById('glossaryCount').textContent = `(${AppState.glossaryData.length})`;
        document.getElementById('codeCount').textContent = `(${AppState.codeData.length})`;
        document.getElementById('flowchartCount').textContent = `(${AppState.flowchartData.length})`;

        AppState.currentData = AppState.glossaryData;
        init();
        initChecklist();

    } catch (error) {
        console.error('데이터 로드 실패:', error);
        showErrorMessage('데이터를 불러오는 중 오류가 발생했습니다. 페이지를 새로고침해 주세요.');
    }
}

/**
 * 에러 메시지 표시
 * @param {string} message - 표시할 에러 메시지
 */
function showErrorMessage(message) {
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #c62828;">
                <h2>⚠️ 오류 발생</h2>
                <p>${message}</p>
                <button onclick="location.reload()" style="margin-top: 20px; padding: 10px 20px; background: #1a73e8; color: white; border: none; border-radius: 8px; cursor: pointer;">
                    새로고침
                </button>
            </div>
        `;
    }
}

// ========================================
// 뷰 전환 함수
// ========================================
function switchView(view) {
    AppState.currentView = view;

    if (view === 'glossary') {
        AppState.currentData = AppState.glossaryData;
    } else if (view === 'code') {
        AppState.currentData = AppState.codeData;
    } else if (view === 'flowchart') {
        AppState.currentData = AppState.flowchartData;
    } else {
        AppState.currentData = [];
    }

    // 탭 버튼 활성화
    document.querySelectorAll('.tab-button:not(.faq-chatbot):not(.law-btn)').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));

    const tabEl = document.getElementById(view + 'Tab');
    if (tabEl) tabEl.classList.add('active');
    document.getElementById(view + 'View').classList.add('active');

    // 사이드바 표시/숨김
    if (view === 'checklist' || view === 'law' || view === 'screen' || view === 'screenMgmt') {
        document.getElementById('sidebar').style.display = 'none';
        if (view === 'screen') {
            initScreenList();
        } else if (view === 'screenMgmt') {
            initScreenMgmt();
        }
    } else {
        document.getElementById('sidebar').style.display = '';
        AppState.searchQuery = '';
        AppState.categoryFilter = '';
        document.getElementById('searchInput').value = '';
        renderCategoryFilters();
        applyFilters();
    }
}

// ========================================
// 필터 및 렌더링 함수
// ========================================
function renderCategoryFilters() {
    const container = document.getElementById('categoryFilters');
    let categories = [];

    if (AppState.currentView === 'flowchart') {
        categories = ['전체', ...new Set(AppState.flowchartData.map(d => d.category))];
    } else if (AppState.currentView === 'glossary') {
        categories = ['전체', ...new Set(AppState.glossaryData.map(d => d.구분))];
    } else {
        categories = ['전체', ...new Set(AppState.codeData.map(d => d.구분))];
    }

    container.innerHTML = categories.map(cat =>
        `<div class="filter-chip ${AppState.categoryFilter === cat || (AppState.categoryFilter === '' && cat === '전체') ? 'active' : ''}" data-cat="${cat}">${cat}</div>`
    ).join('');

    container.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            AppState.categoryFilter = chip.dataset.cat === '전체' ? '' : chip.dataset.cat;
            container.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            applyFilters();
        });
    });
}

function applyFilters() {
    const filtered = AppState.currentData.filter(item => {
        if (AppState.currentView === 'flowchart') {
            if (AppState.categoryFilter && item.category !== AppState.categoryFilter) return false;
            if (AppState.searchQuery && !item.title.toLowerCase().includes(AppState.searchQuery.toLowerCase()) && !item.code.toLowerCase().includes(AppState.searchQuery.toLowerCase())) return false;
        } else {
            const catKey = '구분';
            if (AppState.categoryFilter && item[catKey] !== AppState.categoryFilter) return false;
            if (AppState.searchQuery) {
                const searchField = AppState.currentView === 'glossary' ? '용어' : '코드이명';
                if (!item[searchField]?.toLowerCase().includes(AppState.searchQuery.toLowerCase())) return false;
            }
        }
        return true;
    });

    renderItemList(filtered);
    if (filtered.length > 0) selectItem(0, filtered);
}

function renderItemList(items) {
    const list = document.getElementById('itemList');
    list.innerHTML = items.map((item, idx) => {
        if (AppState.currentView === 'flowchart') {
            return `<li class="term-item" onclick="selectItem(${idx})" title="${item.title}"><span class="term-code">${item.code}</span>${item.title}</li>`;
        } else {
            const title = AppState.currentView === 'glossary' ? item.용어 : (item.코드이명 || item.코드);
            return `<li class="term-item" onclick="selectItem(${idx})" title="${title}">${title}</li>`;
        }
    }).join('');
}

function selectItem(idx, items = null) {
    if (!items) {
        items = AppState.currentData.filter(item => {
            if (AppState.currentView === 'flowchart') {
                if (AppState.categoryFilter && item.category !== AppState.categoryFilter) return false;
                if (AppState.searchQuery && !item.title.toLowerCase().includes(AppState.searchQuery.toLowerCase())) return false;
            }
            return true;
        });
    }

    if (idx >= items.length) return;

    const item = items[idx];
    document.querySelectorAll('.term-item').forEach((el, i) => el.classList.toggle('active', i === idx));

    if (AppState.currentView === 'flowchart') {
        renderFlowchart(item);
    } else {
        renderCard(item);
    }
}

// ========================================
// 플로우차트 렌더링
// ========================================
function renderFlowchart(item) {
    const container = document.getElementById('flowchartContent');
    const hasBothVersions = item.mermaidLite && item.mermaid;

    // 버전별 PNG 경로 결정
    const getPngPath = () => {
        if (AppState.umlVersion === '1.5.0' && item.pngPath_v150) {
            return item.pngPath_v150;
        }
        return item.pngPath; // 기본 (v1.4.2)
    };

    const currentPngPath = getPngPath();
    const hasPng = currentPngPath;

    // PNG 이미지 뷰 모드인 경우
    if (AppState.flowchartVersion === 'png' && hasPng) {
        const versionDropdown = `
            <div style="display:flex;align-items:center;gap:8px;margin-left:auto;">
                <label style="font-size:13px;color:#666;">📦 UML 버전:</label>
                <select onchange="setUmlVersion(this.value,'${item.code}')" style="padding:6px 12px;border:1px solid #ddd;border-radius:8px;font-size:13px;background:#fff;cursor:pointer;">
                    <option value="1.4.2" ${AppState.umlVersion === '1.4.2' ? 'selected' : ''}>v1.4.2</option>
                    <option value="1.5.0" ${AppState.umlVersion === '1.5.0' ? 'selected' : ''}>v1.5.0 (최신)</option>
                </select>
            </div>`;
        const versionToggle = `
            <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;align-items:center;">
                <button onclick="setFlowchartVersion('lite','${item.code}')" class="filter-btn" style="padding:8px 16px;border-radius:20px;cursor:pointer;font-size:13px;border:1px solid #ddd;background:#f5f5f5;color:#333">📊 라이트 모드</button>
                <button onclick="setFlowchartVersion('full','${item.code}')" class="filter-btn" style="padding:8px 16px;border-radius:20px;cursor:pointer;font-size:13px;border:1px solid #ddd;background:#f5f5f5;color:#333">📋 상세 모드</button>
                <button onclick="setFlowchartVersion('png','${item.code}')" class="filter-btn active" style="padding:8px 16px;border-radius:20px;cursor:pointer;font-size:13px;border:1px solid #ddd;background:#ff6b35;color:white">🖼️ 원본 UML</button>
                ${versionDropdown}
            </div>`;

        container.innerHTML = `<div class="flowchart-card">
            <div class="flowchart-title"><span class="flowchart-code">${item.code}</span>${item.title}</div>
            <div class="flowchart-category">${item.category}</div>
            ${versionToggle}
            <div class="flowchart-summary">📌 ${item.summary}</div>
            <div class="flowchart-diagram" style="overflow:auto;max-height:70vh;background:#fff;border-radius:8px;padding:16px;">
                <img src="${currentPngPath}" alt="${item.title} UML 다이어그램 (v${AppState.umlVersion})" style="max-width:100%;height:auto;display:block;margin:0 auto;" loading="lazy" />
            </div>
        </div>`;
        return;
    }

    const currentMermaid = AppState.flowchartVersion === 'lite' && item.mermaidLite ? item.mermaidLite : item.mermaid;

    const versionToggle = hasBothVersions || hasPng ? `
        <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;">
            <button onclick="setFlowchartVersion('lite','${item.code}')" class="filter-btn ${AppState.flowchartVersion === 'lite' ? 'active' : ''}" style="padding:8px 16px;border-radius:20px;cursor:pointer;font-size:13px;border:1px solid #ddd;background:${AppState.flowchartVersion === 'lite' ? '#1a73e8' : '#f5f5f5'};color:${AppState.flowchartVersion === 'lite' ? 'white' : '#333'}">📊 라이트 모드</button>
            <button onclick="setFlowchartVersion('full','${item.code}')" class="filter-btn ${AppState.flowchartVersion === 'full' ? 'active' : ''}" style="padding:8px 16px;border-radius:20px;cursor:pointer;font-size:13px;border:1px solid #ddd;background:${AppState.flowchartVersion === 'full' ? '#1a73e8' : '#f5f5f5'};color:${AppState.flowchartVersion === 'full' ? 'white' : '#333'}">📋 상세 모드</button>
            ${hasPng ? `<button onclick="setFlowchartVersion('png','${item.code}')" class="filter-btn" style="padding:8px 16px;border-radius:20px;cursor:pointer;font-size:13px;border:1px solid #ddd;background:#f5f5f5;color:#333">🖼️ 원본 UML</button>` : ''}
        </div>` : '';

    container.innerHTML = `<div class="flowchart-card">
        <div class="flowchart-title"><span class="flowchart-code">${item.code}</span>${item.title}</div>
        <div class="flowchart-category">${item.category}</div>
        ${versionToggle}
        <div class="flowchart-summary">📌 ${item.summary}</div>
        <div class="flowchart-diagram"><div class="mermaid">${currentMermaid}</div></div>
    </div>`;

    mermaid.run({ nodes: container.querySelectorAll('.mermaid') });
}

function setFlowchartVersion(ver, code) {
    AppState.flowchartVersion = ver;
    const item = AppState.flowchartData.find(f => f.code === code);
    if (item) renderFlowchart(item);
}

function setUmlVersion(ver, code) {
    AppState.umlVersion = ver;
    const item = AppState.flowchartData.find(f => f.code === code);
    if (item) renderFlowchart(item);
}

// ========================================
// 카드 렌더링
// ========================================
function renderCard(item) {
    const area = AppState.currentView === 'glossary'
        ? document.getElementById('glossaryContent')
        : document.getElementById('codeContent');

    const term = AppState.currentView === 'glossary' ? item.용어 : item.코드이명;
    const easyExp = easyExplanations[term] || easyExplanations[item.용어];

    const easySection = easyExp ? `
        <div class="easy-explanation">
            <div class="easy-explanation-title">🎈 쉬운 해설</div>
            <div class="easy-explanation-content">${easyExp}</div>
        </div>` : '';

    if (AppState.currentView === 'glossary') {
        area.innerHTML = `<div class="item-card">
            <div class="item-title">${item.용어}</div>
            <div class="item-meta">
                <div class="meta-badge"><strong>수정일:</strong> ${item.수정일}</div>
                <div class="meta-badge"><strong>구분:</strong> ${item.구분}</div>
            </div>
            <div class="item-description">${item.설명}</div>
            ${easySection}
        </div>`;
    } else {
        area.innerHTML = `<div class="item-card">
            <div class="item-title">${item.코드이명 || item.코드}(${item.코드})</div>
            <div class="item-meta">
                <div class="meta-badge"><strong>수정일:</strong> ${item.수정일}</div>
                <div class="meta-badge"><strong>구분:</strong> ${item.구분}</div>
                <div class="meta-badge"><strong>그룹명:</strong> ${item.그룹명}</div>
            </div>
            <div class="item-description">${item.설명}</div>
            ${easySection}
        </div>`;
    }
}

// ========================================
// 체크리스트 함수
// ========================================
function initChecklist() {
    renderChecklist();
    document.getElementById('checklistFilters').querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#checklistFilters .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            AppState.checklistCatFilter = btn.dataset.cat;
            renderChecklist();
        });
    });
}

function renderChecklist() {
    const tbody = document.getElementById('checklistBody');
    const savedState = JSON.parse(localStorage.getItem('checklistState') || '{}');
    const filtered = AppState.checklistCatFilter === '전체'
        ? checklistData
        : checklistData.filter(d => d.category === AppState.checklistCatFilter);

    tbody.innerHTML = filtered.map((item, i) => {
        const origIdx = checklistData.indexOf(item);
        const isChecked = savedState[origIdx] || false;
        return `<tr class="${isChecked ? 'checked' : ''}" data-idx="${origIdx}">
            <td style="text-align:center"><input type="checkbox" class="custom-checkbox" ${isChecked ? 'checked' : ''} onchange="toggleCheck(${origIdx},this)"></td>
            <td><span class="category-badge ${item.category}">${item.category}</span></td>
            <td><strong>${item.item}</strong></td>
            <td>${item.detail}</td>
        </tr>`;
    }).join('');

    updateChecklistStats();
}

function toggleCheck(idx, cb) {
    const savedState = JSON.parse(localStorage.getItem('checklistState') || '{}');
    savedState[idx] = cb.checked;
    localStorage.setItem('checklistState', JSON.stringify(savedState));
    const row = cb.closest('tr');
    row.classList.toggle('checked', cb.checked);
    updateChecklistStats();
}

function updateChecklistStats() {
    const savedState = JSON.parse(localStorage.getItem('checklistState') || '{}');
    const complete = Object.values(savedState).filter(v => v).length;
    document.getElementById('completeCount').textContent = complete;
    document.getElementById('incompleteCount').textContent = checklistData.length - complete;
}

function exportToExcel() {
    const savedState = JSON.parse(localStorage.getItem('checklistState') || '{}');
    const data = checklistData.map((item, i) => ({
        구분: item.category,
        체크리스트: item.item,
        주요사항: item.detail,
        완료여부: savedState[i] ? '완료' : '미완료'
    }));
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'CA평가체크리스트');
    XLSX.writeFile(wb, 'CA평가체크리스트.xlsx');
}

// ========================================
// 화면 목록 함수
// ========================================
function initScreenList() {
    renderScreenList();
    document.getElementById('screenFilters').querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#screenFilters .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            AppState.screenTypeFilter = btn.dataset.type;
            renderScreenList();
        });
    });
}

function renderScreenList() {
    const tbody = document.getElementById('screenBody');
    const filtered = AppState.screenTypeFilter === '전체'
        ? screenData
        : screenData.filter(d => d.type === AppState.screenTypeFilter);

    tbody.innerHTML = filtered.map((item) => `
        <tr style="background:${item.d1 === '발급' ? '#f8f9fa' : '#fff'}">
            <td style="text-align:center;font-weight:600">${item.no}</td>
            <td><span style="background:${item.d1 === '발급' ? '#e3f2fd' : '#fce4ec'};color:${item.d1 === '발급' ? '#1565c0' : '#c2185b'};padding:4px 8px;border-radius:12px;font-size:11px;font-weight:600">${item.d1}</span></td>
            <td style="color:#1a73e8;font-weight:500">${item.d2}</td>
            <td style="color:#666">${item.d3}</td>
            <td style="color:#999;font-size:12px">${item.d4}</td>
            <td><code style="background:#e8f0fe;padding:3px 6px;border-radius:4px;font-size:11px;color:#1a73e8">${item.id}</code></td>
            <td><strong>${item.name}</strong></td>
            <td style="font-size:13px;color:#555">${item.desc}</td>
        </tr>
    `).join('');
}

// ========================================
// 화면목록 관리 함수
// ========================================
async function initScreenMgmt() {
    const savedData = localStorage.getItem('screenMgmtData');
    if (savedData) {
        AppState.screenMgmtData = JSON.parse(savedData);
    } else {
        try {
            const res = await fetch('screenlist_data.json');
            AppState.screenMgmtData = await res.json();
        } catch (e) {
            console.error('screenlist_data.json 로드 실패:', e);
            AppState.screenMgmtData = [];
        }
    }

    // L1 필터 옵션 설정
    const l1Set = new Set(AppState.screenMgmtData.map(d => d.l1).filter(v => v));
    const l1Select = document.getElementById('screenMgmtL1Filter');
    l1Select.innerHTML = '<option value="">전체 L1</option>' +
        [...l1Set].map(l1 => `<option value="${l1}">${l1}</option>`).join('');

    // 이벤트 바인딩
    document.getElementById('screenMgmtSearch').oninput = (e) => {
        AppState.screenMgmtSearchQuery = e.target.value;
        renderScreenMgmtList();
    };
    document.getElementById('screenMgmtL1Filter').onchange = (e) => {
        AppState.screenMgmtL1Filter = e.target.value;
        renderScreenMgmtList();
    };
    document.getElementById('screenMgmtTypeFilter').onchange = (e) => {
        AppState.screenMgmtTypeFilter = e.target.value;
        renderScreenMgmtList();
    };

    renderScreenMgmtList();
}

function renderScreenMgmtList() {
    const tbody = document.getElementById('screenMgmtBody');
    let filtered = AppState.screenMgmtData;

    if (AppState.screenMgmtL1Filter) filtered = filtered.filter(d => d.l1 === AppState.screenMgmtL1Filter);
    if (AppState.screenMgmtTypeFilter) filtered = filtered.filter(d => d.type === AppState.screenMgmtTypeFilter);
    if (AppState.screenMgmtSearchQuery) {
        const q = AppState.screenMgmtSearchQuery.toLowerCase();
        filtered = filtered.filter(d =>
            d.screenId?.toLowerCase().includes(q) ||
            d.screenName?.toLowerCase().includes(q) ||
            d.d1?.toLowerCase().includes(q) ||
            d.d2?.toLowerCase().includes(q)
        );
    }

    tbody.innerHTML = filtered.map((item) => {
        const idx = AppState.screenMgmtData.indexOf(item);
        return `<tr data-idx="${idx}">
            <td style="text-align:center;font-weight:600">${item.no}</td>
            <td><input type="text" value="${item.l1 || ''}" onchange="updateScreenMgmtField(${idx},'l1',this.value)" style="width:70px;padding:4px;border:1px solid #ddd;border-radius:3px"></td>
            <td><select onchange="updateScreenMgmtField(${idx},'type',this.value)" style="padding:4px;border:1px solid #ddd;border-radius:3px">
                <option value="HTML" ${item.type === 'HTML' ? 'selected' : ''}>HTML</option>
                <option value="NATIVE" ${item.type === 'NATIVE' ? 'selected' : ''}>NATIVE</option>
            </select></td>
            <td><input type="text" value="${item.screenId || ''}" onchange="updateScreenMgmtField(${idx},'screenId',this.value)" style="width:110px;padding:4px;border:1px solid #ddd;border-radius:3px;font-family:monospace;font-size:11px"></td>
            <td><input type="text" value="${item.screenName || ''}" onchange="updateScreenMgmtField(${idx},'screenName',this.value)" style="width:150px;padding:4px;border:1px solid #ddd;border-radius:3px"></td>
            <td><input type="text" value="${item.d1 || ''}" onchange="updateScreenMgmtField(${idx},'d1',this.value)" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:3px;font-size:12px"></td>
            <td><input type="text" value="${item.d2 || ''}" onchange="updateScreenMgmtField(${idx},'d2',this.value)" style="width:110px;padding:4px;border:1px solid #ddd;border-radius:3px;font-size:12px"></td>
            <td><input type="text" value="${item.d3 || ''}" onchange="updateScreenMgmtField(${idx},'d3',this.value)" style="width:110px;padding:4px;border:1px solid #ddd;border-radius:3px;font-size:12px"></td>
            <td><input type="text" value="${item.d4 || ''}" onchange="updateScreenMgmtField(${idx},'d4',this.value)" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:3px;font-size:12px"></td>
            <td><input type="text" value="${item.d5 || ''}" onchange="updateScreenMgmtField(${idx},'d5',this.value)" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:3px;font-size:12px"></td>
            <td><input type="text" value="${item.d6 || ''}" onchange="updateScreenMgmtField(${idx},'d6',this.value)" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:3px;font-size:12px"></td>
            <td><input type="text" value="${item.reqId || ''}" onchange="updateScreenMgmtField(${idx},'reqId',this.value)" style="width:90px;padding:4px;border:1px solid #ddd;border-radius:3px;font-size:11px"></td>
            <td><button onclick="deleteScreenItem(${idx})" style="background:#f44336;color:white;border:none;padding:4px 8px;border-radius:4px;cursor:pointer;font-size:11px">🗑️</button></td>
        </tr>`;
    }).join('');

    // 통계 업데이트
    const stats = document.getElementById('screenMgmtStats');
    const htmlCount = AppState.screenMgmtData.filter(d => d.type === 'HTML').length;
    const nativeCount = AppState.screenMgmtData.filter(d => d.type === 'NATIVE').length;
    stats.innerHTML = `📊 <strong>전체:</strong> ${AppState.screenMgmtData.length}개 | <strong>HTML:</strong> ${htmlCount}개 | <strong>NATIVE:</strong> ${nativeCount}개 | <strong>필터 결과:</strong> ${filtered.length}개`;
}

function updateScreenMgmtField(idx, field, value) {
    AppState.screenMgmtData[idx][field] = value;
}

function addScreenItem() {
    const newNo = AppState.screenMgmtData.length > 0
        ? Math.max(...AppState.screenMgmtData.map(d => d.no)) + 1
        : 1;
    AppState.screenMgmtData.push({
        no: newNo, l1: "", l2: "", type: "HTML", screenId: "", screenName: "",
        d1: "", d2: "", d3: "", d4: "", d5: "", d6: "", designType: "", note: "", reqId: ""
    });
    renderScreenMgmtList();
}

function deleteScreenItem(idx) {
    if (confirm(`항목 #${AppState.screenMgmtData[idx].no}을(를) 삭제하시겠습니까?`)) {
        AppState.screenMgmtData.splice(idx, 1);
        AppState.screenMgmtData.forEach((item, i) => item.no = i + 1);
        renderScreenMgmtList();
    }
}

function saveScreenMgmtData() {
    localStorage.setItem('screenMgmtData', JSON.stringify(AppState.screenMgmtData));
    alert(`✅ ${AppState.screenMgmtData.length}개 항목이 저장되었습니다!`);
}

function exportScreenMgmtToExcel() {
    const exportData = AppState.screenMgmtData.map(item => ({
        'No': item.no,
        'L1': item.l1,
        'TYPE': item.type,
        '화면ID': item.screenId,
        '화면명': item.screenName,
        '1Depth': item.d1,
        '2Depth': item.d2,
        '3Depth': item.d3,
        '4Depth': item.d4,
        '5Depth': item.d5,
        '6Depth': item.d6,
        '비고': item.note,
        '요구사항ID': item.reqId
    }));
    const ws = XLSX.utils.json_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, '화면목록');
    XLSX.writeFile(wb, 'SOL_D04_화면목록_export.xlsx');
}

// ========================================
// 모바일 메뉴 함수
// ========================================
function closeMobileMenu() {
    document.getElementById('hamburger').classList.remove('active');
    document.getElementById('sidebar').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
}

function mobileSwitch(view) {
    closeMobileMenu();
    switchView(view);
}

// ========================================
// 초기화
// ========================================
function init() {
    renderCategoryFilters();
    applyFilters();
}

// ========================================
// 이벤트 리스너 바인딩
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    // 탭 버튼 이벤트
    ['glossaryTab', 'codeTab', 'flowchartTab', 'checklistTab', 'lawTab', 'screenTab', 'screenMgmtTab'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('click', () => switchView(id.replace('Tab', '')));
        }
    });

    // 검색 입력 이벤트
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', e => {
            AppState.searchQuery = e.target.value;
            applyFilters();
        });
    }

    // 햄버거 메뉴 이벤트
    const hamburger = document.getElementById('hamburger');
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('overlay').classList.toggle('active');
        });
    }

    // 오버레이 클릭 이벤트
    const overlay = document.getElementById('overlay');
    if (overlay) {
        overlay.addEventListener('click', closeMobileMenu);
    }

    // 데이터 로드
    loadData();
});
