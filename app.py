
import streamlit as st
import pandas as pd
import networkx as nx
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Recommendation System", layout="centered")

st.title("🤖 Hybrid AI Recommendation System")
st.write("Graph + Cosine Similarity + Smart Scoring")

# =========================
# OPTIONAL API KEY (NOT REQUIRED FOR CORE SYSTEM)
# =========================
api_key = os.getenv("GROK_API_KEY")

if api_key:
    import requests

headers = {"Authorization": f"Bearer {api_key}"}

# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.write(df.head())

    # =========================
    # VALIDATION
    # =========================
    required_cols = {"user_id", "item_id", "rating"}

    if not required_cols.issubset(df.columns):
        st.error("CSV must have columns: user_id, item_id, rating")

    else:

        # =========================
        # USER-ITEM MATRIX
        # =========================
        matrix = df.pivot_table(
            index="user_id",
            columns="product",
            values="rating",
            fill_value=0
        )

        # =========================
        # COSINE SIMILARITY
        # =========================
        sim_matrix = cosine_similarity(matrix)
        sim_df = pd.DataFrame(sim_matrix, index=matrix.index, columns=matrix.index)

        # =========================
        # GRAPH CREATION
        # =========================
        G = nx.Graph()

        for _, row in df.iterrows():
            G.add_edge(f"User{row['user_id']}", f"Item{row['item_id']}", weight=row['rating'])

        # =========================
        # USER SELECTION
        # =========================
        user = st.selectbox("👤 Select User", matrix.index)

        # =========================
        # SIMILAR USER FUNCTION
        # =========================
        def get_sim_user(u):
            sorted_users = sim_df[u].sort_values(ascending=False)
            return sorted_users.index[1], sorted_users.values[1]

        sim_user, sim_score = get_sim_user(user)

        st.subheader("🤝 Similar User")
        st.write(f"User {sim_user} (Score: {sim_score:.2f})")

        # =========================
        # ITEMS
        # =========================
        user_items = set(df[df["user_id"] == user]["item_id"])
        sim_items = set(df[df["user_id"] == sim_user]["item_id"])

        raw_recs = list(sim_items - user_items)

        # =========================
        # POPULARITY SCORE
        # =========================
        popularity = df["item_id"].value_counts().to_dict()

        # =========================
        # SMART SCORING FUNCTION
        # =========================
        def score_item(item):
            return 0.6 * popularity.get(item, 0) + 0.4 * sim_score * 10

        scored_recs = []

        for item in raw_recs:
            scored_recs.append((item, score_item(item)))

        scored_recs.sort(key=lambda x: x[1], reverse=True)

        recommendations = [i[0] for i in scored_recs]

        # =========================
        # FALLBACK SYSTEM
        # =========================
        if len(recommendations) == 0:
            recommendations = df["item_id"].value_counts().head(5).index.tolist()

        # =========================
        # OUTPUT
        # =========================
        st.subheader("🎯 Recommendations")
        st.write(recommendations)

        # =========================
        # GRAPH INFO
        # =========================
        st.subheader("📊 Graph Info")
        st.write("Nodes:", len(G.nodes))
        st.write("Edges:", len(G.edges))

        # =========================
        # SIMPLE AI AGENT (NO API REQUIRED)
        # =========================
        st.subheader("🤖 AI Agent")

        user_input = st.text_input("Ask (e.g. sad, action, skincare)")

        def agent(text):
            text = text.lower()

            if "sad" in text:
                return "💔 Recommend: Emotional / Drama items"
            elif "action" in text:
                return "🔥 Recommend: Action items"
            elif "skincare" in text:
                return "🧴 Recommend: Cleanser, Serum, Sunscreen"
            else:
                return f"🎯 Based on your profile: {recommendations}"

        if user_input:
            st.write(agent(user_input))

else:
    st.info("📂 Please upload a CSV file to start")
