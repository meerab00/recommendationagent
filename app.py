import streamlit as st
import pandas as pd
from agent import run_agent

st.set_page_config(page_title="AI Recommendation Agent", layout="wide")

st.title("🤖 AI Agent Recommendation System")

# 📂 File Upload
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
    st.write(df.head())

    # 💬 Chat Input
    user_input = st.chat_input("Ask me anything (e.g. recommend me sad movies)")

    if user_input:
        response = run_agent(user_input, df)
        st.write("🤖 AI Response:")
        st.success(response)
