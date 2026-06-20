import streamlit as st
import pandas as pd
import time
from openai import OpenAI

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="SOJOONG AEO Tracker", page_icon="🦷", layout="wide")
st.markdown('''
    <style>
    .main-title { font-size: 26pt; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 12pt; color: #4B5563; margin-bottom: 25px; }
    </style>
''', unsafe_allow_html=True)

st.markdown('<div class="main-title">Dental Clinic SOJOONG - Multi-AI AEO Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">ChatGPT, Claude, Gemini 통합 AI 검색 노출 실시간 분석 시스템</div>', unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import time
from openai import OpenAI

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="SOJOONG AEO Tracker (Free Mode)", page_icon="🦷", layout="wide")
st.markdown('''
    <style>
    .main-title { font-size: 26pt; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 12pt; color: #4B5563; margin-bottom: 25px; }
    </style>
''', unsafe_allow_html=True)

st.markdown('<div class="main-title">Dental Clinic SOJOONG - Multi-AI AEO Tool (무료 모델 모드)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">오픈라우터의 100% 무료 고성능 AI 모델들을 활용한 실시간 검색 노출 분석 시스템</div>', unsafe_allow_html=True)

# 2. 사이드바 - 설정 및 API 키 입력
st.sidebar.header("⚙️ 시스템 설정")

# Streamlit Secrets에 저장된 키가 있으면 자동으로 불러오기
default_key = ""
if "OPENROUTER_API_KEY" in st.secrets:
    default_key = st.secrets["OPENROUTER_API_KEY"]

api_key = st.sidebar.text_input("🔑 OpenRouter API Key", type="password", value=default_key, help="sk-or- 로 시작하는 키를 입력하세요.")

st.sidebar.subheader("🔍 진단 대상 정보")
target_name = st.sidebar.text_input("업체명", value="소중치과")
target_region = st.sidebar.text_input("분석 지역", value="문정동")
target_specialty = st.sidebar.text_area("핵심 강점 (USP)", value="1. 자연치아 살리기 대표원장 & 교정 협진\n2. 충치·임플란트·보철 원스톱 진료\n3. 서울대 출신 교정전문의")

# 3. 메인 로직 함수 정의 (OpenRouter 무료 고성능 모델 연동)
def generate_questions(client, region, specialty):
    prompt = f"너는 환자의 마음을 잘 아는 마케터야. 지역은 '{region}'이고, 찾는 치과의 특징은 '{specialty}'야. 이 조건에 맞는 치과를 찾기 위해 환자가 AI 검색 엔진에 물어볼 법한 길고 구체적인 질문 2가지를 작성해줘. 번호 없이 한 줄에 하나씩 적어줘."
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return [q.strip('- 1234567890.') for q in response.choices[0].message.content.strip().split('\n') if len(q) > 10][:2]

def get_multi_ai_answers(client, questions):
    # 오픈라우터에서 제공하는 대표적인 100% 무료 고성능 모델 3대장으로 매칭
    models = {
        "Llama 3.1 8B (Meta 무료 엔진)": "meta-llama/llama-3.1-8b-instruct:free",
        "Gemma 2 9B (Google 무료 엔진)": "google/gemma-2-9b-it:free",
        "Qwen 2.5 7B (Alibaba 무료 엔진)": "qwen/qwen-2.5-7b-instruct:free"
    }
    
    results = []
    for q in questions:
        for engine_name, model_id in models.items():
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": "너는 환자에게 치과를 추천해주는 친절하고 객관적인 AI 비서야. 다양한 관점에서 병원을 비교해서 알려줘."},
                        {"role": "user", "content": q}
                    ],
                    temperature=0.5
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"오류 발생: {e}"
            
            results.append({"AI 엔진": engine_name, "환자 질문": q, "응답 결과": answer})
    return results

def evaluate_and_recommend(client, target_name, results, specialty):
    data_str = "\n".join([f"[{r['AI 엔진']}] 질문: {r['환자 질문']} \n답변: {r['응답 결과']}" for r in results])
    
    prompt = f'''
    아래는 환자의 질문에 대한 여러 AI 엔진들의 답변들이다.
    타겟 업체명: {target_name}
    업체 강점: {specialty}
    
    데이터:
    {data_str}
    
    이 데이터를 바탕으로 다음 항목을 작성해라:
    1. 종합 AEO Score (100점 만점 중 몇 점인지)
    2. 엔진별 노출 현황 (Llama, Gemma, Qwen 각각 소중치과를 추천했는지 여부 O/X)
    3. 타겟 업체가 모든 AI 검색에서 1순위로 추천받기 위해 당장 실행해야 할 통합 마케팅 액션플랜 2가지 (구체적인 블로그 글 제목 추천 포함)
    '''
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# 4. 분석 실행 UI
if st.button("🚀 통합 AI 포지셔닝 실시간 분석 시작 (100% 무료 모드)", type="primary"):
    if not api_key.startswith("sk-or-"):
        st.error("좌측 사이드바에 유효한 OpenRouter API Key를 입력해주세요!")
    else:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("1단계: 환자 페르소나 질문 자동 생성 중...")
            questions = generate_questions(client, target_region, target_specialty)
            progress_bar.progress(20)
            
            status_text.text("2단계: Llama, Gemma, Qwen 무료 AI 엔진 동시 분석 및 데이터 수집 중...")
            multi_ai_results = get_multi_ai_answers(client, questions)
            progress_bar.progress(70)
            
            status_text.text("3단계: 엔진별 노출도 통합 점수화 및 마케팅 가이드 분석 중...")
            report = evaluate_and_recommend(client, target_name, multi_ai_results, target_specialty)
            progress_bar.progress(100)
            status_text.success("무료 멀티 AI 진단이 완료되었습니다!")
            
            # 결과 화면 출력
            st.write("---")
            st.write("### 🔍 주요 AI 엔진별 응답 원본 데이터")
            
            df = pd.DataFrame(multi_ai_results)
            df['응답 결과 (요약)'] = df['응답 결과'].apply(lambda x: str(x)[:150] + "...") 
            st.table(df[['AI 엔진', '환자 질문', '응답 결과 (요약)']])
            
            st.write("### 📊 통합 AI 평가 리포트 및 액션플랜")
            st.info(report)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
# 2. 사이드바 - 설정 및 API 키 입력
st.sidebar.header("⚙️ 시스템 설정")

# Streamlit Secrets에 저장된 키가 있으면 자동으로 불러오기
default_key = ""
if "OPENROUTER_API_KEY" in st.secrets:
    default_key = st.secrets["OPENROUTER_API_KEY"]

api_key = st.sidebar.text_input("🔑 OpenRouter API Key", type="password", value=default_key, help="sk-or- 로 시작하는 키를 입력하세요.")

st.sidebar.subheader("🔍 진단 대상 정보")
target_name = st.sidebar.text_input("업체명", value="소중치과")
target_region = st.sidebar.text_input("분석 지역", value="문정동")
target_specialty = st.sidebar.text_area("핵심 강점 (USP)", value="1. 자연치아 살리기 대표원장 & 교정 협진\n2. 교정과 함께 충치·임플란트·보철 원스톱 진료\n3. 서울대출신 교정 전문의")

# 3. 메인 로직 함수 정의 (OpenRouter 연동)
def generate_questions(client, region, specialty):
    prompt = f"너는 환자의 마음을 잘 아는 마케터야. 지역은 '{region}'이고, 찾는 치과의 특징은 '{specialty}'야. 이 조건에 맞는 치과를 찾기 위해 환자가 AI 검색 엔진에 물어볼 법한 길고 구체적인 질문 2가지를 작성해줘. 번호 없이 한 줄에 하나씩 적어줘."
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return [q.strip('- 1234567890.') for q in response.choices[0].message.content.strip().split('\n') if len(q) > 10][:2]

def get_multi_ai_answers(client, questions):
    # 테스트할 3대 AI 엔진 세팅 (OpenRouter의 모델명 규격)
    models = {
        "ChatGPT (GPT-4o)": "openai/gpt-4o-mini",
        "Claude (Sonnet 3.5)": "anthropic/claude-3.5-sonnet",
        "Gemini (1.5 Pro)": "google/gemini-1.5-pro"
    }
    
    results = []
    for q in questions:
        for engine_name, model_id in models.items():
            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": "너는 환자에게 치과를 추천해주는 친절하고 객관적인 AI 비서야. 웹 검색 결과를 종합해서 대답하듯 알려줘."},
                        {"role": "user", "content": q}
                    ],
                    temperature=0.5
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"오류 발생: {e}"
            
            results.append({"AI 엔진": engine_name, "환자 질문": q, "응답 결과": answer})
    return results

def evaluate_and_recommend(client, target_name, results, specialty):
    # 수집된 데이터를 문자열로 변환하여 평가 AI에게 전달
    data_str = "\n".join([f"[{r['AI 엔진']}] 질문: {r['환자 질문']} \n답변: {r['응답 결과']}" for r in results])
    
    prompt = f'''
    아래는 환자의 질문에 대한 여러 AI 엔진(ChatGPT, Claude, Gemini)의 답변들이다.
    타겟 업체명: {target_name}
    업체 강점: {specialty}
    
    데이터:
    {data_str}
    
    이 데이터를 바탕으로 다음 항목을 작성해라:
    1. 종합 AEO Score (100점 만점 중 몇 점인지)
    2. 엔진별 노출 현황 (ChatGPT, Claude, Gemini 각각 소중치과를 추천했는지 여부 O/X)
    3. 타겟 업체가 모든 AI 검색에서 1순위로 추천받기 위해 당장 실행해야 할 통합 마케팅 액션플랜 2가지
    '''
    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# 4. 분석 실행 UI
if st.button("🚀 통합 AI 포지셔닝 실시간 분석 시작", type="primary"):
    if not api_key.startswith("sk-or-"):
        st.error("좌측 사이드바에 유효한 OpenRouter API Key를 입력해주세요!")
    else:
        # OpenRouter 전용 클라이언트 세팅 (핵심 변경점)
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("1단계: 환자 페르소나 질문 자동 생성 중...")
            questions = generate_questions(client, target_region, target_specialty)
            progress_bar.progress(20)
            
            status_text.text("2단계: ChatGPT, Claude, Gemini 동시 검색 및 추천 데이터 수집 중...")
            multi_ai_results = get_multi_ai_answers(client, questions)
            progress_bar.progress(70)
            
            status_text.text("3단계: 엔진별 노출도 통합 점수화 및 마케팅 가이드 분석 중...")
            report = evaluate_and_recommend(client, target_name, multi_ai_results, target_specialty)
            progress_bar.progress(100)
            status_text.success("멀티 AI 진단이 완료되었습니다!")
            
            # 결과 화면 출력
            st.write("---")
            st.write("### 🔍 주요 AI 엔진별 응답 원본 데이터")
            
            df = pd.DataFrame(multi_ai_results)
            df['응답 결과 (요약)'] = df['응답 결과'].apply(lambda x: str(x)[:150] + "...") 
            st.table(df[['AI 엔진', '환자 질문', '응답 결과 (요약)']])
            
            st.write("### 📊 통합 AI 평가 리포트 및 액션플랜")
            st.info(report)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
