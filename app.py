
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# APP TITLE
# =========================
st.title("🤖 AI Graph Recommendation System")

# =========================
# UPLOAD CSV
# =========================
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.write(df.head())

    # =========================
    # CHECK COLUMNS
    # =========================
    if not {"user_id", "product", "rating"}.issubset(df.columns):
        st.error("CSV must have: user_id, product, rating")

    else:

        # =========================
        # USER-PRODUCT MATRIX
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
        sim = cosine_similarity(matrix)
        sim_df = pd.DataFrame(sim, index=matrix.index, columns=matrix.index)

        # =========================
        # USER SELECT
        # =========================
        user = st.selectbox("Select User", matrix.index)

        # =========================
        # SIMILAR USER
        # =========================
        def get_sim_user(u):
            sorted_users = sim_df[u].sort_values(ascending=False)
            return sorted_users.index[1], sorted_users.values[1]

        sim_user, sim_score = get_sim_user(user)

        st.subheader("🤝 Similar User")
        st.write(f"User {sim_user} (Score: {sim_score:.2f})")

        # =========================
        # USER ITEMS
        # =========================
        user_products = set(df[df["user_id"] == user]["product"])
        sim_products = set(df[df["user_id"] == sim_user]["product"])

        # =========================
        # SCORE SYSTEM (IMPORTANT)
        # =========================
        popularity = df["product"].value_counts().to_dict()

        score_list = []

        for item in sim_products:

            pop_score = popularity.get(item, 0)

            score = (sim_score * 10) + pop_score

            score_list.append((item, score))

        # sort by score
        score_list = sorted(score_list, key=lambda x: x[1], reverse=True)

        recommendations = [i[0] for i in score_list]

        # =========================
        # FALLBACK
        # =========================
        if len(recommendations) == 0:
            recommendations = df["product"].value_counts().head(5).index.tolist()

        # =========================
        # OUTPUT
        # =========================
        st.subheader("🎯 Recommendations")
        st.write(recommendations)

        # =========================
        # GRAPH VISUALIZATION
        # =========================
        st.subheader("📊 Graph Visualization")

        G = nx.Graph()

        for _, row in df.iterrows():
            G.add_edge(f"U{row['user_id']}", row["product"])

        fig, ax = plt.subplots(figsize=(10, 6))

        pos = nx.spring_layout(G, seed=42)

        nx.draw_networkx_nodes(G, pos, node_size=800, node_color="lightblue", ax=ax)
        nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)

        ax.set_title("User-Product Graph")
        ax.axis("off")

        st.pyplot(fig)

else:
    st.info("📂 Upload CSV file to start")
