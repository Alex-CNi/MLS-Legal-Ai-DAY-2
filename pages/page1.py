import streamlit as st
from common import DIFFICULTY_LABELS, init_state

init_state()

st.title("Settings")

st.session_state.difficulty = st.slider(
    "Difficulty",
    min_value=1,
    max_value=5,
    value=st.session_state.difficulty,
    step=1,
)

st.caption(f"gpt-4o will play at **{DIFFICULTY_LABELS[st.session_state.difficulty]}**.")
st.page_link("pages/page2.py", label="Go play")