import pandas as pd

def get_recommendations(df):

    # simple scoring system (you can improve later)
    if "rating" in df.columns:
        top_items = df.sort_values(by="rating", ascending=False)
    else:
        top_items = df.head(5)

    recommendations = top_items.iloc[:, 0].tolist()

    return recommendations[:5]
