
import streamlit as st
import pandas as pd

# Safe imports (graph optional)
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    GRAPH_AVAILABLE = True
except:
    GRAPH_AVAILABLE = False

from sklearn.metrics.pairwise import cosine_similarity

# =========================
# APP TITLE
# =========================
st.title("🤖 AI Recommendation System")

# =========================
# FILE UPLOAD
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
            return sorted_users.index[1]

        sim_user = get_sim_user(user)

        st.subheader("🤝 Similar User")
        st.write(sim_user)

        # =========================
        # RECOMMENDATION
        # =========================
        user_products = set(df[df["user_id"] == user]["product"])
        sim_products = set(df[df["user_id"] == sim_user]["product"])

        recs = list(sim_products - user_products)

        if len(recs) == 0:
            recs = df["product"].value_counts().head(5).index.tolist()

        st.subheader("🎯 Recommendations")
        st.write(recs)

        # =========================
        # GRAPH (SAFE OPTIONAL)
        # =========================
        if GRAPH_AVAILABLE:

            st.subheader("📊 Graph Visualization")

            G = nx.Graph()

            for _, row in df.iterrows():
                G.add_edge(f"U{row['user_id']}", row["product"])

            fig, ax = plt.subplots(figsize=(6, 4))

            pos = nx.spring_layout(G, seed=42)

            nx.draw(
                G,
                pos,
                with_labels=True,
                node_size=700,
                font_size=8,
                ax=ax
            )

            st.pyplot(fig)

        else:
            st.warning("Graph visualization not available (install matplotlib + networkx)")

else:
    st.info("📂 Please upload CSV file")
