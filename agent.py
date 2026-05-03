
import streamlit as st

st.title("🤖 AI Recommendation Agent")

st.write("Ask anything like: sad movies, action items, love songs")

# simple memory-based recommendations
default_recs = {
    "sad": ["Drama Movie 1", "Drama Movie 2"],
    "action": ["Action Movie 1", "Action Movie 2"],
    "love": ["Romantic Movie 1", "Romantic Movie 2"]
}

user_input = st.text_input("Talk to AI Agent")

def agent(text):
    text = text.lower()

    if "sad" in text:
        return default_recs["sad"]
    elif "action" in text:
        return default_recs["action"]
    elif "love" in text:
        return default_recs["love"]
    else:
        return ["General Recommendation 1", "General Recommendation 2"]

if user_input:
    st.subheader("🤖 Agent Response")
    st.write(agent(user_input))
