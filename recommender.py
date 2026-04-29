import pandas as pd

def get_recommendations(df):

    # safety check
    if df is None or df.empty:
        return ["No data found"]

    # column check
    if "product" not in df.columns:
        return ["Column 'product' not found"]

    # remove duplicates + pick top 5
    recommendations = df["product"].dropna().unique().tolist()

    return recommendations[:5]
