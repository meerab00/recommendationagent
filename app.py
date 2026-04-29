import streamlit as st
import pandas as pd
from recommender import get_recommendations

st.title("🤖 AI Recommendation Agent")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("File Loaded Successfully!")
    st.write(df.head())

    # User IDs properly lo
    user_ids = sorted(df['user_id'].unique().tolist())
    selected_user = st.selectbox("Select User ID:", user_ids,
                                  format_func=lambda x: f"User {x}")

    user_input = st.chat_input("Ask: recommend me products")

    if user_input:
        result = get_recommendations(df, user_input, selected_user)

        st.subheader(f"Recommendations for User {selected_user}:")
        for item in result:
            st.write("🎯", item)
