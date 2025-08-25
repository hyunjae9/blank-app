import streamlit as st
import random

# =============================
# 숫자 맞추기 게임 (세션 상태)
# =============================
st.set_page_config(page_title="숫자 맞추기 게임", page_icon="🎮", layout="centered")

st.title("🎮 숫자 맞추기 게임")
st.caption("1부터 100 사이의 숫자를 맞춰보세요!")

# 세션 상태 초기화
if "target" not in st.session_state:
    st.session_state.target = random.randint(1, 100)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 사용자 입력
guess = st.number_input("예상 숫자 입력 (1~100)", min_value=1, max_value=100, step=1)

col1, col2 = st.columns(2)
with col1:
    if st.button("제출하기", type="primary", use_container_width=True):
        if not st.session_state.game_over:
            st.session_state.attempts += 1
            if guess == st.session_state.target:
                st.success(f"정답입니다! 🎉 {st.session_state.attempts}번 만에 맞췄어요.")
                st.session_state.game_over = True
            elif guess < st.session_state.target:
                st.warning("업! (더 큰 숫자를 입력해보세요)")
            else:
                st.warning("다운! (더 작은 숫자를 입력해보세요)")

with col2:
    if st.button("다시 시작", use_container_width=True):
        st.session_state.target = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.experimental_rerun()

# 게임 상태 안내
st.write(f"시도 횟수: {st.session_state.attempts}")

if st.session_state.game_over:
    st.balloons()
