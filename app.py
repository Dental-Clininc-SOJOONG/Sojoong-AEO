import streamlit as st
import pandas as pd
import time
import google.generativeai as genai

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="SOJOONG AEO Tracker (Gemini)", page_icon="🦷", layout="wide")
st.markdown('''
    <style>
    .main-title { font-size: 26pt; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 12pt; color: #4B5563; margin-bottom: 25px; }
    </style>
''', unsafe_allow_html=True)

st.markdown('<div class="main-title">Dental Clinic SOJOONG - Gemini AEO Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">구글 제미나이 엔진을 활용한 실시간 AI 검색 노출 및 마케팅 포지셔닝 분석 시스템</div>', unsafe_allow_html=True)

# 2. 사이드바 - 설정 및 API 키 입력
st.sidebar.header("⚙️ 시스템 설정")

default_key = ""
if "GEMINI_API_KEY" in st.secrets:
    default_key = st.secrets["GEMINI_API_KEY"]

api_key = st.sidebar.text_input("🔑 Google Gemini API Key", type="password", value=default_key, help="발급받은 구글 API 키를 입력하세요.")

st.sidebar.subheader("🔍 진단 대상 정보")
target_name = st.sidebar.text_input("업체명", value="소중치과")
target_region = st.sidebar.text_input("분석 지역", value="문정동")
target_specialty = st.sidebar.text_area("핵심 강점 (USP)", value="1. 자연치아 살리기 대표원장 & 교정 협진\n2. 충치·임플란트·보철 원스톱 진료\n3. 클리피씨 교정 주력")

# 3. 메인 로직 함수 정의 (Google Gemini 모델 연동)
def generate_questions(region, specialty):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"너는 환자의 마음을 잘 아는 마케터야. 지역은 '{region}'이고, 찾는 치과의 특징은 '{specialty}'야. 이 조건에 맞는 치과를 찾기 위해 환자가 AI 검색 엔진에 물어볼 법한 길고 구체적인 질문 2가지를 작성해줘. 번호 없이 한 줄에 하나씩 적어줘."
    response = model.generate_content(prompt)
    return [q.strip('- 1234567890.') for q in response.text.strip().split('\n') if len(q) > 10][:2]

def get_gemini_answers(questions):
    # 구글 제미나이의 실시간 검색(Search Grounding) 기능 활성화 설정
    model = genai.GenerativeModel(
        "gemini-1.5-flash",
        tools=[{"google_search": {}}]
    )
    
    results = []
    for q in questions:
        try:
            response = model.generate_content(q)
            answer = response.text
        except Exception as e:
            answer = f"오류 발생: {e}"
        results.append({"AI 엔진": "Google Gemini (실시간 검색 모드)", "환자 질문": q, "응답 결과": answer})
    return results

def evaluate_and_recommend(target_name, results, specialty):
    model = genai.GenerativeModel("gemini-1.5-pro") 
    data_str = "\n".join([f"질문: {r['환자 질문']} \n답변: {r['응답 결과']}" for r in results])
    
    prompt = f'''
    아래는 환자의 질문에 대해 구글 제미나이가 실시간 웹 검색을 거쳐 답변한 내용이다.
    타겟 업체명: {target_name}
    업체 강점: {specialty}
    
    데이터:
    {data_str}
    
    이 데이터를 바탕으로 다음 항목을 한국어로 상세히 작성해라:
    1. 종합 AEO Score (100점 만점 중 몇 점인지 - 실시간 답변 내 타겟 업체 언급 비율 기준)
    2. 타겟 업체 노출 현황 및 발견된 경쟁사 분석
    3. 타겟 지표를 달성하기 위해 다음 주에 당장 실행해야 할 블로그 마케팅 액션플랜 2가지 (구체적인 글 제목 추천 포함)
    '''
    response = model.generate_content(prompt)
    return response.text

# 4. 분석 실행 UI
if st.button("🚀 실시간 AI 검색 포지셔닝 분석 시작", type="primary"):
    if len(api_key) < 20:  # 시작 문자열 검사 대신, 키 길이로 유효성 검사 (수정된 부분)
        st.error("좌측 사이드바에 유효한 Google Gemini API Key를 입력해주세요!")
    else:
        # 제미나이 라이브러리에 키 세팅
        genai.configure(api_key=api_key)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("1단계: 환자 페르소나 질문 자동 생성 중...")
            questions = generate_questions(target_region, target_specialty)
            progress_bar.progress(20)
            
            status_text.text("2단계: 구글 실시간 웹 검색 기반 추천 데이터 수집 중 (약 5~10초 소요)...")
            gemini_results = get_gemini_answers(questions)
            progress_bar.progress(70)
            
            status_text.text("3단계: 노출도 점수화 및 향후 마케팅 가이드 분석 중...")
            report = evaluate_and_recommend(target_name, gemini_results, target_specialty)
            progress_bar.progress(100)
            status_text.success("실시간 AI 진단이 완료되었습니다!")
            
            # 결과 화면 출력
            st.write("---")
            st.write("### 🔍 AI 엔진 실시간 추천 응답 데이터")
            
            df = pd.DataFrame(gemini_results)
            st.table(df[['AI 엔진', '환자 질문']])
            
            for idx, r in enumerate(gemini_results):
                with st.expander(f"💬 질문 {idx+1}번에 대한 AI 답변 원본 보기"):
                    st.write(r['응답 결과'])
            
            st.write("### 📊 통합 AI 평가 리포트 및 액션플랜")
            st.info(report)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
