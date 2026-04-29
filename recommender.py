
def get_recommendations(df, user_input=None):

    # safety check
    if df is None or df.empty:
        return ["No data found"]

    if "product" not in df.columns:
        return ["Missing 'product' column"]

    df = df.dropna(subset=["product"])

    # simple filtering by input (optional)
    if user_input:
        text = user_input.lower()

        if "skincare" in text and "category" in df.columns:
            df = df[df["category"].str.lower() == "skincare"]

        elif "hair" in text and "category" in df.columns:
            df = df[df["category"].str.lower() == "haircare"]

        elif "makeup" in text and "category" in df.columns:
            df = df[df["category"].str.lower() == "makeup"]

    return df["product"].drop_duplicates().head(5).tolist()
