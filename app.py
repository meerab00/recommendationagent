
import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import os

from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# =========================
# 🔐 LOAD ENV (API KEY)
# =========================
load_dotenv()
API_KEY = os.getenv("GROK_API_KEY")

# =========================
# STREAMLIT UI
# =========================
st.title("🤖 AI Graph-Based Recommendation System")
st.write("Upload dataset and get smart recommendations")

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    st.write("📊 Dataset Preview:", df.head())

    # =========================
    # USER-ITEM MATRIX
    # =========================
    matrix = df.pivot_table(
        index='user_id',
        columns='product',
        values='rating',
        fill_value=0
    )

    # =========================
    # COSINE SIMILARITY
    # =========================
    similarity = cosine_similarity(matrix)
    sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

    # =========================
    # GRAPH CREATION
    # =========================
    G = nx.Graph()

    for _, row in df.iterrows():
        G.add_edge(f"User{row['user_id']}", f"Item{row['item_id']}", weight=row['rating'])

    # =========================
    # POPULARITY (COUNT)
    # =========================
    popular_items = df['item_id'].value_counts()

    # =========================
    # SIDEBAR INPUT
    # =========================
    user_id = st.selectbox("Select User ID", df['user_id'].unique())

    # =========================
    # SIMILAR USER
    # =========================
    def get_similar_user(uid):
        sims = sim_df.loc[uid].sort_values(ascending=False)
        return sims.index[1], sims.values[1]

    sim_user, sim_score = get_similar_user(user_id)

    st.subheader("🤝 Similar User")
    st.write(f"User {sim_user} (Similarity: {sim_score:.2f})")

    # =========================
    # RECOMMENDATION LOGIC
    # =========================
    def recommend(uid, sim_uid):

        user_items = set(df[df['user_id'] == uid]['item_id'])
        sim_items = set(df[df['user_id'] == sim_uid]['item_id'])

        recommendations = list(sim_items - user_items)

        # fallback popularity
        if len(recommendations) == 0:
            recommendations = popular_items.index[:5].tolist()

        return recommendations

    recs = recommend(user_id, sim_user)

    st.subheader("🎯 Recommendations")
    st.write(recs)

    # =========================
    # GRAPH VISUALIZATION
    # =========================
    st.subheader("📊 Graph View")

    st.write("Nodes:", len(G.nodes()))
    st.write("Edges:", len(G.edges()))

    # =========================
    # SIMPLE AI AGENT (NO API REQUIRED)
    # =========================
    st.subheader("🤖 AI Agent")

    user_input = st.text_input("Ask something (e.g. sad movies, action items)")

    def ai_agent(text):
        text = text.lower()

        if "sad" in text:
            return "💔 Recommend: Drama / Emotional Items"
        elif "action" in text:
            return "🔥 Recommend: Action Items"
        elif "love" in text:
            return "❤️ Recommend: Romantic Items"
        else:
            return f"Based on your profile, recommending: {recs}"

    if user_input:
        st.write(ai_agent(user_input))

    # =========================
    # OPTIONAL GROK API (if key exists)
    # =========================
    if API_KEY:
        st.info("GROK API KEY detected (optional integration ready)")

        if st.button("Ask AI (Grok)"):
            st.write("⚠️ API integration placeholder (depends on Grok endpoint)")
            st.write("You can connect your API here for advanced responses.")

    # =========================
    # FOOTER
    # =========================
    st.success("System Running Successfully 🚀")
