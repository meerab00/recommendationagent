
import streamlit as st
import pandas as pd
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

st.title("📊 Graph-Based Recommendation System")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    st.write("📄 Data Preview", df.head())

    # =========================
    # USER-ITEM MATRIX
    # =========================
    matrix = df.pivot_table(
        index='user_id',
        columns='item_id',
        values='rating',
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

    def get_sim_user(u):
        s = sim_df[u].sort_values(ascending=False)
        return s.index[1]

    sim_user = get_sim_user(user)

    st.write("🤝 Similar User:", sim_user)

    # =========================
    # RECOMMENDATION
    # =========================
    user_items = set(df[df['user_id'] == user]['item_id'])
    sim_items = set(df[df['user_id'] == sim_user]['item_id'])

    recs = list(sim_items - user_items)

    st.subheader("🎯 Recommendations")
    st.write(recs)

    # =========================
    # GRAPH
    # =========================
    G = nx.Graph()

    for _, row in df.iterrows():
        G.add_edge(f"U{row['user_id']}", f"I{row['item_id']}")

    st.subheader("📊 Graph Info")
    st.write("Nodes:", len(G.nodes))
    st.write("Edges:", len(G.edges))
