import streamlit as st

# =========================================
# MBTI 학습 유형 진단 (세션 상태 사용, 파일 저장 없음)
# =========================================
st.set_page_config(page_title="MBTI 학습 유형 진단", page_icon="🧭", layout="centered")

# 세션 상태 초기화
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "mbti" not in st.session_state:
    st.session_state.mbti = None

st.title("MBTI 학습 유형 진단")
st.caption("간단한 8문항으로 나의 학습 성향을 알아보세요. (로그인/키 불필요)")

st.divider()

st.markdown("### 문항 (각 문항에서 본인에게 더 가까운 쪽을 선택하세요)")

# 문항 정의
# 각 문항은 (문항텍스트, (선택지1, 선택지2), 차원쌍, 가중치)
# 가중치는 동률 방지를 위해 첫 번째 문항을 1.1로, 두 번째를 1.0으로 설정
questions = [
    # E / I
    ("여럿과 함께 공부하면 에너지가 난다.", ("그렇다 (E)", "혼자가 더 편하다 (I)"), ("E", "I"), 1.1),
    ("모르는 부분은 즉석에서 질문하며 해결한다.", ("그렇다 (E)", "먼저 스스로 찾고 정리한다 (I)"), ("E", "I"), 1.0),
    # S / N
    ("설명은 예시·사례가 많을수록 이해가 쉽다.", ("그렇다 (S)", "개념의 큰 흐름이 더 중요하다 (N)"), ("S", "N"), 1.1),
    ("세부 지침(체크리스트)이 있으면 안심된다.", ("그렇다 (S)", "대략 방향만 알면 된다 (N)"), ("S", "N"), 1.0),
    # T / F
    ("답을 고를 때 논리와 근거가 가장 중요하다.", ("그렇다 (T)", "사람·상황을 함께 고려한다 (F)"), ("T", "F"), 1.1),
    ("과제 피드백은 직설적인 편이 좋다.", ("그렇다 (T)", "돌려 말해주면 좋다 (F)"), ("T", "F"), 1.0),
    # J / P
    ("계획표를 만들어 순서대로 진행한다.", ("그렇다 (J)", "상황 보며 유연하게 한다 (P)"), ("J", "P"), 1.1),
    ("마감 직전까지도 더 나은 아이디어가 떠오른다.", ("그렇다 (P)", "아니다, 일찍 마무리한다 (J)"), ("P", "J"), 1.0),
]

# 라디오 위젯으로 응답 받기
responses = []
for idx, (q_text, options, dims, weight) in enumerate(questions, start=1):
    with st.container(border=True):
        choice = st.radio(
            f"{idx}. {q_text}",
            options,
            key=f"q{idx}",
            index=0,  # 기본값 첫 번째
        )
    responses.append(choice)

# 제출 버튼
col1, col2 = st.columns([1, 1])
with col1:
    submit = st.button("제출하기", type="primary", use_container_width=True)
with col2:
    reset = st.button("다시 검사하기", use_container_width=True)

# 결과 계산 로직
def compute_mbti(responses):
    scores = {k: 0.0 for k in ["E", "I", "S", "N", "T", "F", "J", "P"]}
    for (q_text, options, dims, weight), resp in zip(questions, responses):
        left_label, right_label = options
        left_dim, right_dim = dims

        # 어떤 쪽을 골랐는지 판정
        if resp == left_label:
            scores[left_dim] += weight
        else:
            scores[right_dim] += weight

    # 각 축별 타입 선택
    ei = "E" if scores["E"] >= scores["I"] else "I"
    sn = "S" if scores["S"] >= scores["N"] else "N"
    tf = "T" if scores["T"] >= scores["F"] else "F"
    jp = "J" if scores["J"] >= scores["P"] else "P"

    return ei + sn + tf + jp

# 학습 유형 설명(간단 버전)
LEARNING_TIPS = {
    "ISTJ": "체계적·절차적 학습 선호. 체크리스트, 예제풀이 순서화가 효과적.",
    "ISFJ": "친절한 설명과 반복 복습에 강점. 요점정리+오답노트 추천.",
    "INFJ": "큰 그림 속 의미 찾기 선호. 개념 맥락도·마인드맵 활용.",
    "INTJ": "목표지향·자기주도. 커리큘럼 설계와 역산 계획표가 잘 맞음.",
    "ISTP": "직접 만져보며 익힘. 실습·프로젝트형 과제에 몰입.",
    "ISFP": "차분한 환경에서 감각적으로 이해. 시각자료, 예시 중심 학습.",
    "INFP": "흥미·가치와 연결될 때 몰입. 사례 스토리텔링이 도움.",
    "INTP": "원리 파헤치기 선호. 개념 간 연결·비교표, 왜 그런지 따지기.",
    "ESTP": "즉시 적용·피드백 선호. 퀴즈·실습·짧은 과제 반복.",
    "ESFP": "상호작용·재미 중요. 팀활동·시각자료·짧은 목표가 효과적.",
    "ENFP": "아이디어 확장에 강점. 자유 메모→키워드 정리→요약 루틴 추천.",
    "ENTP": "비교·토론으로 이해 심화. 장단점 목록화, 가설-검증 반복.",
    "ESTJ": "규칙·기준을 선호. 일정 관리, 단계별 체크로 안정적 성과.",
    "ESFJ": "협력적 환경에서 동기↑. 스터디와 설명해보기(티칭) 추천.",
    "ENFJ": "맥락·사람 배려. 스토리라인 교안 만들고 발표해보기 효과적.",
    "ENTJ": "목표 역산·지휘형 학습. 마일스톤과 성과 지표로 관리.",
}

if submit:
    st.session_state.submitted = True
    st.session_state.mbti = compute_mbti(responses)

if reset:
    for i in range(1, len(questions) + 1):
        st.session_state.pop(f"q{i}", None)
    st.session_state.submitted = False
    st.session_state.mbti = None
    st.experimental_rerun()

# 결과 영역
st.divider()
st.markdown("### 결과")

if st.session_state.submitted and st.session_state.mbti:
    mbti = st.session_state.mbti
    tip = LEARNING_TIPS.get(mbti, "자신만의 학습 루틴을 관찰하고 조금씩 개선해보세요.")
    st.success(f"당신의 유형: **{mbti}**")
    st.write(f"**학습 유형 설명**: {tip}")

    # 간단 맞춤 팁(축 기반 보너스)
    ei, sn, tf, jp = mbti[0], mbti[1], mbti[2], mbti[3]
    st.markdown("#### 맞춤 미니 팁")
    bullets = []
    bullets.append("• E: 스터디·짧은 발표로 에너지 충전" if ei == "E" else "• I: 조용한 집중 블록으로 몰입도 확보")
    bullets.append("• S: 예제-풀이-요약 순서" if sn == "S" else "• N: 개념 지도로 큰 그림부터")
    bullets.append("• T: 근거-규칙-예외 정리" if tf == "T" else "• F: 사례와 사람·상황 맥락 함께")
    bullets.append("• J: 마감·체크리스트로 흐름 유지" if jp == "J" else "• P: 짧은 스프린트와 빈번한 피드백")
    st.write("\n".join(bullets))
else:
    st.info("문항을 선택한 뒤 **제출하기**를 눌러 결과를 확인하세요.")

st.caption("※ 본 테스트는 간단한 성향 확인용이며, 정밀 심리 평가가 아닙니다.")
