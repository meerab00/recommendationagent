
import streamlit as st
import pandas as pd
from agent import run_agent

st.set_page_config(page_title="Advanced AI Agent", layout="wide")

st.title("🤖 Advanced AI Recommendation Agent")

# 📂 Upload file
uploaded_file = st.file_uploader("Upload CSV dataset", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset Loaded Successfully!")
    st.write(df.head())

    # 💬 Chat UI
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("Ask me anything (e.g. recommend sad movies)")

    if user_input:
        response = run_agent(user_input, df)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AI", response))

    # Show chat
    for role, msg in st.session_state.chat_history:
        st.write(f"**{role}:** {msg}")
