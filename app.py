
import streamlit as st
import pandas as pd
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

st.title("🤖 Product Recommendation System (Graph + Cosine)")

# =========================
# UPLOAD CSV
# =========================
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.write(df.head())

    # =========================
    # CHECK REQUIRED COLUMNS
    # =========================
    required_cols = {"user_id", "product", "rating", "frequency"}

    if not required_cols.issubset(df.columns):
        st.error("CSV must have: user_id, product, rating, frequency")

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
        sim_matrix = cosine_similarity(matrix)
        sim_df = pd.DataFrame(sim_matrix, index=matrix.index, columns=matrix.index)

        # =========================
        # USER SELECT
        # =========================
        user_id = st.selectbox("Select User", matrix.index)

        # =========================
        # FIND SIMILAR USER
        # =========================
        def get_sim_user(u):
            sorted_users = sim_df[u].sort_values(ascending=False)
            return sorted_users.index[1], sorted_users.values[1]

        sim_user, sim_score = get_sim_user(user_id)

        st.subheader("🤝 Similar User")
        st.write(f"User {sim_user} (Score: {sim_score:.2f})")

        # =========================
        # RECOMMENDATION LOGIC
        # =========================
        user_products = set(df[df["user_id"] == user_id]["product"])
        sim_products = set(df[df["user_id"] == sim_user]["product"])

        recommendations = list(sim_products - user_products)

        # =========================
        # FALLBACK
        # =========================
        if len(recommendations) == 0:
            recommendations = df["product"].value_counts().head(5).index.tolist()

        # =========================
        # OUTPUT
        # =========================
        st.subheader("🎯 Recommended Products")
        st.write(recommendations)

        # =========================
        # GRAPH
        # =========================
        G = nx.Graph()

        for _, row in df.iterrows():
            G.add_edge(f"U{row['user_id']}", row['product'], weight=row['rating'])

        st.subheader("📊 Graph Info")
        st.write("Nodes:", len(G.nodes))
        st.write("Edges:", len(G.edges))

else:
    st.info("📂 Upload your CSV file to start")
