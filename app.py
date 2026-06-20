import streamlit as st
import pandas as pd
import time
from openai import OpenAI
import json

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="SOJOONG AEO Tracker", page_icon="🦷", layout="wide")
st.markdown("""
    <style>
    .main-title { font-size: 26pt; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 12pt; color: #4B5563; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Dental Clinic SOJOONG - AEO Diagnostic Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">치아교정 타겟 AI 검색 엔진 노출도 및 포지셔닝 실시간 분석 시스템</div>', unsafe_allow_html=True)

# 2. 사이드바 - 설정 및 API 키 입력
st.sidebar.header("⚙️ 시스템 설정")
api_key = st.sidebar.text_input("🔑 OpenAI API Key 필수 입력", type="password", help="sk- 로 시작하는 OpenAI API 키를 입력하세요.")

st.sidebar.subheader("🔍 진단 대상 정보")
target_name = st.sidebar.text_input("업체명", value="소중치과")
target_region = st.sidebar.text_input("분석 지역", value="문정동")
target_specialty = st.sidebar.text_area("핵심 강점 (USP)", value="1. 자연치아 살리기 대표원장 & 교정 협진\n2. 충치·임플란트·보철 원스톱 진료\n3. 클리피씨 교정 주력")

# 3. 메인 로직 함수 정의
def generate_questions(client, region, specialty):
    prompt = f"너는 환자의 마음을 잘 아는 마케터야. 지역은 '{region}'이고, 찾는 치과의 특징은 '{specialty}'야. 이 조건에 맞는 치과를 찾기 위해 환자가 AI 검색 엔진(ChatGPT 등)에 물어볼 법한 길고 구체적인 질문 3가지를 작성해줘. 번호 없이 한 줄에 하나씩 적어줘."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip().split('\n')

def get_ai_answers(client, questions):
    answers = []
    for q in questions:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 환자에게 치과를 추천해주는 친절하고 객관적인 AI 비서야. 웹 검색 결과를 종합해서 대답하듯 알려줘."},
                {"role": "user", "content": q}
            ],
            temperature=0.5
        )
        answers.append(response.choices[0].message.content)
    return answers

def evaluate_and_recommend(client, target_name, questions, answers, specialty):
    prompt = f"""
    아래는 환자의 질문 3개와 그에 대한 AI의 답변들이다.
    타겟 업체명: {target_name}
    업체 강점: {specialty}
    
    질문/답변 데이터:
    1. 질문: {questions[0]} / 답변: {answers[0]}
    2. 질문: {questions[1]} / 답변: {answers[1]}
    3. 질문: {questions[2]} / 답변: {answers[2]}
    
    이 데이터를 바탕으로 다음 항목을 작성해라:
    1. AEO Score (100점 만점 중 몇 점인지, 타겟 업체 언급 빈도 기준)
    2. 언급된 주요 경쟁사 이름들 (없으면 '없음')
    3. 타겟 업체가 AI 검색에서 1순위로 추천받기 위해 다음 주에 당장 실행해야 할 마케팅 액션플랜 2가지 (블로그 제목 추천 포함)
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# 4. 분석 실행 UI
if st.button("🚀 AI 포지셔닝 실시간 분석 시작", type="primary"):
    if not api_key.startswith("sk-"):
        st.error("좌측 사이드바에 유효한 OpenAI API Key를 입력해주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 1단계: 예상 질문 생성
            status_text.text("1단계: 환자 페르소나 기반 타겟 질문 3개 자동 생성 중...")
            questions = generate_questions(client, target_region, target_specialty)
            # 빈 줄이나 불필요한 문자열 제거
            questions = [q.strip('- 1234567890.') for q in questions if len(q) > 10][:3] 
            progress_bar.progress(30)
            
            # 2단계: AI 검색 시뮬레이션
            status_text.text("2단계: AI 엔진을 통한 검색 및 추천 데이터 수집 중...")
            answers = get_ai_answers(client, questions)
            progress_bar.progress(70)
            
            # 3단계: 점수화 및 마케팅 행동 추천
            status_text.text("3단계: 노출도 점수화 및 마케팅 액션플랜 분석 중...")
            report = evaluate_and_recommend(client, target_name, questions, answers, target_specialty)
            progress_bar.progress(100)
            status_text.success("실시간 AEO 진단이 완료되었습니다!")
            
            # 결과 화면 출력
            st.write("---")
            st.write("### 🔍 생성된 타겟 질문 및 AI 응답 결과")
            data = {"환자의 실제 검색 질문": questions, "AI의 추천 답변 요약": [ans[:100]+"..." for ans in answers]}
            st.table(pd.DataFrame(data))
            
            st.write("### 📊 AI 평가 리포트 및 액션플랜")
            st.info(report)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
