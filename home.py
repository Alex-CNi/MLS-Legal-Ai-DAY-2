import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv() 

st.set_page_config(page_title="LAWS90286 Day 2", layout="centered")

st.markdown("""
<style>
  [data-testid="stHorizontalBlock"] { gap: 6px !important; }
  [data-testid="stColumn"] { padding: 0 !important; }
  .stButton > button {
      height: 96px; width: 100%;
      font-size: 2.6rem !important; font-weight: 700; line-height: 1;
      border: 2px solid #3a3f4b; border-radius: 10px; background: #171a21;
  }
  .stButton > button p { font-size: 2.6rem !important; margin: 0; }
  .stButton > button:hover:not(:disabled) { background: #1f2630; border-color: #6c7a8f; }
  .stButton > button:disabled { opacity: 1 !important; background: #12151b; border-color: #2a2e38; }
</style>
""", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/page1.py",  title="Settings",    icon="⚙️", default=True),
    st.Page("pages/page2.py", title="Tic Tac Toe", icon="🎮"),
    st.Page("pages/exercise2.1.py", title="Exercise 2.1", icon="📝"),
    st.Page("pages/exercise2.2.py", title="Exercise 2.2", icon="📝"),
    st.Page("pages/exercise2.3.py", title="Exercise 2.3", icon="📝"),
    st.Page("pages/exercise2.4.py", title="Exercise 2.4", icon="📝"),
])
pg.run()