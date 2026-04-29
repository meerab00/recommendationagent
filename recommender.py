
import pandas as pd

def get_recommendations(df, user_input=None):

    # 🧠 safety checks
    if df is None or df.empty:
        return ["❌ No data loaded"]

    # 🔍 check required column
    if "product" not in df.columns:
        return ["❌ 'product' column missing in dataset"]

    # 🧹 clean data
    df = df.dropna(subset=["product"])

    # 🎯 if category filter needed from user input
    if user_input:
        user_input = user_input.lower()

        if "skincare" in user_input and "category" in df.columns:
            df = df[df["category"].str.lower() == "skincare"]

        elif "hair" in user_input and "category" in df.columns:
            df = df[df["category"].str.lower() == "haircare"]

        elif "makeup" in user_input and "category" in df.columns:
            df = df[df["category"].str.lower() == "makeup"]

    # ⭐ remove duplicates
    recommendations = df["product"].drop_duplicates().tolist()

    # 🔥 return top 5
    return recommendations[:5] if recommendations else ["No recommendations found"]
