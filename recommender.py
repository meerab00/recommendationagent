
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_items(df, user_input):

    # combine text data
    df["combined"] = df.astype(str).agg(" ".join, axis=1)

    # vectorization
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(df["combined"])

    # similarity
    similarity = cosine_similarity(matrix)

    # simple scoring
    scores = similarity.mean(axis=1)

    df["score"] = scores

    # top recommendations
    top = df.sort_values(by="score", ascending=False).head(5)

    return top.iloc[:, 0].tolist()
