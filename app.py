"""공고 적합도 체커 — 공고를 붙여넣으면 내 조건과 맞는지 항목별로 체크하고 지원 여부를 판정한다.

실행: .venv/bin/streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

from typesafe_sdk import Choice, Noul, TypeSafeClient

load_dotenv()

# 항목별 체크(Noul) + 종합 판정(Choice)
QUESTIONS = {
    "stack_fit": Noul(instructions="지원자의 기술스택이 공고 요구사항과 맞는가?"),
    "career_fit": Noul(instructions="지원자의 경력 수준이 공고가 원하는 경력과 맞는가?"),
    "location_fit": Noul(instructions="근무지 조건이 지원자의 희망과 맞는가?"),
    "salary_fit": Noul(instructions="연봉 조건이 지원자의 희망과 맞는가?"),
    "decision": Choice(
        instructions="지원자 프로필과 공고를 종합할 때 지원 여부는?",
        criteria={
            "apply": "잘 맞음. 지원 권장",
            "maybe": "일부만 맞음. 검토 후 결정",
            "skip": "안 맞음. 지원 비권장",
        },
    ),
}

# 판정값 → 화면 표시용 라벨
DECISION_LABEL = {
    "apply": ("✅ 지원 권장", "normal"),
    "maybe": ("🤔 검토 후 결정", "off"),
    "skip": ("❌ 지원 비권장", "inverse"),
}


def analyze(job_text: str, me: str):
    """공고 + 내 프로필을 Jev 에 보내 판단 결과(answers)를 돌려준다."""
    state = f"[지원자 프로필]\n{me}\n[채용 공고]\n{job_text}"
    client = TypeSafeClient()
    answers = client.system_one(state, QUESTIONS).answers
    client.close()
    return answers


st.title("📋 공고 적합도 체커")
st.caption("공고를 붙여넣으면 내 조건과 맞는지 항목별로 체크해 지원 여부를 알려줍니다.")

st.sidebar.header("내 프로필")
stack = st.sidebar.text_area(
    "기술스택",
    "Java, Spring Boot 백엔드 / Airflow 데이터 파이프라인 / data 정합성 / SQL",
    height=100,
)
career = st.sidebar.text_input("경력", "2년6개월 차")
location = st.sidebar.text_input("근무지", "서울 또는 경기도")
salary = st.sidebar.text_input("연봉", "4500만원 이상 희망")
me = f"- 기술스택: {stack}\n- 경력: {career}\n- 근무지: {location}\n- 연봉: {salary}"

job_text = st.text_area("채용 공고 붙여넣기", height=280, placeholder="공고 전문을 여기에 붙여넣으세요")

if st.button("분석", type="primary"):
    if not job_text.strip():
        st.warning("공고 내용을 붙여넣어 주세요.")
    else:
        with st.spinner("Jev 가 판단 중..."):
            a = analyze(job_text, me)

        st.subheader("항목별 적합도")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("기술스택", f"{a['stack_fit'].noul:.0%}")
        c2.metric("경력", f"{a['career_fit'].noul:.0%}")
        c3.metric("근무지", f"{a['location_fit'].noul:.0%}")
        c4.metric("연봉", f"{a['salary_fit'].noul:.0%}")

        d = a["decision"]
        label, _ = DECISION_LABEL[d.choice]
        st.subheader("종합 판정")
        st.metric(label, f"신뢰도 {d.confidence:.0%}")
        st.caption(f"분포: {d.probabilities}")
