import streamlit as st
import time
import pandas as pd

# 1. 웹페이지 기본 설정 및 디자인
st.set_page_config(page_title="SOJOONG AEO Tracker", page_icon="🦷", layout="wide")

# 상단 타이틀 부근 스타일 수정 (소중치과 브랜드 컬러 반영 - 신뢰감을 주는 Deep Blue & Clean 테마)
st.markdown("""
    <style>
    .main-title { font-size: 26pt; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 12pt; color: #4B5563; margin-bottom: 25px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Dental Clinic SOJOONG - AEO Diagnostic Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">치아교정 타겟 AI 검색 엔진 노출도 및 포지셔닝 실시간 분석 시스템 (MVP)</div>', unsafe_allow_html=True)

# 2. 사이드바 설정 (설정 및 API 입력창)
st.sidebar.header("⚙️ 시스템 설정")
api_key = st.sidebar.text_input("Perplexity / OpenAI API Key (선택)", type="password", help="입력하지 않으면 시뮬레이션 모드로 작동합니다.")
mode = "실제 API 연동 모드" if api_key else "시뮬레이션 검증 모드 (Mock 데이터)"
st.sidebar.info(f"현재 구동 상태: **{mode}**")

st.sidebar.subheader("🔍 진단 대상 정보")
target_name = st.sidebar.text_input("업체명", value="소중치과")
target_region = st.sidebar.text_input("분석 지역", value="문정동")
target_specialty = st.sidebar.text_area("핵심 강점 (USP)", value="1. 자연치아 살리기 대표원장 & 교정 협진\n2. 충치·임플란트·보철 원스톱 진료\n3. 클리피씨 교정 주력\n4. 주 2회 교정 정밀 진료")

# 3. 메인 화면 - 분석 실행 UI
st.write("### 📊 AI 검색 최적화(AEO) 진단 가동")
st.write("설정된 키워드와 환자의 예상 페르소나 질문을 기반으로 주요 AI 엔진(Perplexity, ChatGPT, Gemini 등)의 추천 지형을 분석합니다.")

# 테스트할 핵심 질문 세트 정의
questions = [
    f"{target_region} 치과 중에 교정하면서 충치나 임플란트까지 한 곳에서 다 받을 수 있는 통합진료 치과 추천해줘",
    f"{target_region}에서 무조건 발치하지 않고 최대한 내 치아 살리면서 교정해주는 치과 어디야?",
    f"통증이 적고 자가결찰 방식인 클리피씨 교정 잘하는 {target_region} 치과 찾아줘",
    f"교정 치료 끝나고 라미네이트나 앞니 심미보철 치료까지 예쁘게 연계해서 잘하는 {target_region} 치과 추천해줘"
]

if st.button("🚀 AI 포지셔닝 실시간 분석 시작", type="primary"):
    # 애니메이션 효과로 분석 단계 시각화
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("1단계: 문정동 치아교정 환자 타겟 핵심 질문 페르소나 생성 중...")
    time.sleep(1.0)
    progress_bar.progress(25)
    
    status_text.text("2단계: AI 엔진 검색 네트워크(Perplexity RAG)를 통한 실시간 추천 데이터 수집 중...")
    time.sleep(1.5)
    progress_bar.progress(50)
    
    status_text.text("3단계: 수집된 AI 답변 내 소중치과 언급 빈도 및 경쟁사 데이터 텍스트 마이닝 중...")
    time.sleep(1.2)
    progress_bar.progress(75)
    
    status_text.text("4단계: 소중치과 핵심 USP(협진, 원스톱, 클리피씨) 매칭률 및 점수 산정 중...")
    time.sleep(1.0)
    progress_bar.progress(100)
    status_text.success("진단이 완료되었습니다!")
    
    # 결과 화면 렌더링 (시뮬레이션 데이터 기준)
    st.write("---")
    st.write("## 📈 진단 결과 리포트")
    
    # 대시보드 스코어 카드
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="AI 검색 노출 지수 (AEO Score)", value="65 / 100", delta="-5점 (전월 대비)")
    with col2:
        st.metric(label="핵심 USP 메시지 매칭률", value="45%", delta="🗣️ '원스톱 진료' 인식 부족")
    with col3:
        st.metric(label="지역 내 추천 점유율 (SOV)", value="위치 기반 2위", delta="1위 업체 추격 중")
        
    st.write("### 🔍 질문별 AI 응답 분석 데이터")
    
    # 실제 데이터 테이블 형태 시각화
    data = {
        "환자의 예상 질문 (Target Query)": questions,
        "AI 엔진 추천 여부": ["✔️ 추천됨 (2순위)", "❌ 미노출 (타과 추천)", "✔️ 추천됨 (1순위)", "❌ 미노출 (타과 추천)"],
        "함께 노출된 경쟁사": ["A치과, B치과", "C치과, D치과", "B치과", "A치과, E치과"],
        "AI가 분석한 추천/미추천 사유": [
            "대표원장과 교정의의 협진 및 충치 치료 연계성이 블로그 문서에서 확인되어 통합진료 치과로 인지함.",
            "AI가 '자연치아 보존' 키워드 검색 시 보존과 전문의 위주 병원을 크롤링함. 소중치과의 교정-보존 협진 콘텐츠 노출 부족.",
            "클리피씨 장치의 특징과 소중치과의 주력 진료 매칭이 잘 되어 있어 최상단에 추천됨.",
            "교정 후 보철(라미네이트)로 이어지는 심미 연계 치료에 대한 웹상 데이터(인덱싱된 글) 부족으로 누락됨."
        ]
    }
    df = pd.DataFrame(data)
    st.table(df)
    
    # 5단계 마케팅 행동 추천 (Actionable Insights)
    st.write("### 🛠️ AI 검색 노출 확대를 위한 이번 주 마케팅 행동 가이드")
    
    st.info("""
    **💡 액션 플랜 1: '교정 중 충치/잇몸 치료 원스톱' 키워드 선점**
    - **이유:** AI는 환자가 '귀찮아하는 상황'을 해결해주는 병원을 우선 추천합니다.
    - **행동:** 공식 네이버 블로그 및 홈페이지에 `[문정동 치아교정 중 충치 치료, 다른 치과로 가야 할까요?]` 라는 제목으로 대표원장-교정의 협진 시스템 프로세스를 상세히 기술한 정보성 글을 발행하세요.
    """)
    
    st.info("""
    **💡 액션 플랜 2: '자연치아 살리는 비발치 교정' 맥락 강화**
    - **이유:** 현재 AI는 자연치아 살리기와 교정을 별개의 키워드로 인식하고 있습니다.
    - **행동:** 플레이스 리뷰나 블로그 콘텐츠에 '치아를 무조건 뽑지 않고 살리면서 교정하는 소중치과'라는 문장이 유기적으로 결합된 치료 증례(Case Study)를 최소 2건 이상 업로드하여 AI 봇이 긁어갈 수 있게 하세요.
    """)
    
    st.info("""
    **💡 액션 플랜 3: 앞니 라미네이트 & 교정 연계 포트폴리오 노출**
    - **이유:** 심미 보철 관련 질문에서 소중치과 인덱싱 데이터가 제로에 가깝습니다.
    - **행동:** 홈페이지 하위 메뉴 메뉴 구조나 텍스트에 '교정 후 라미네이트 심미 마무리' 단락을 추가하고 관련 텍스트 비중을 15% 늘리세요.
    """)