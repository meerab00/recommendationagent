def get_recommendations(df, user_input=None, user_id=None):
    if df is None or df.empty:
        return ["No data found"]

    if "product" not in df.columns:
        return ["Missing 'product' column"]

    df = df.dropna(subset=["product"])

    # Pehle us user ka data lo
    if user_id is not None and 'user_id' in df.columns:
        user_df = df[df['user_id'] == user_id]
        if user_df.empty:
            return ["No data found for this user"]
    else:
        user_df = df

    # Category filter
    if user_input:
        text = user_input.lower()
        if "skincare" in text and "category" in user_df.columns:
            user_df = user_df[user_df["category"].str.lower() == "skincare"]
        elif "hair" in text and "category" in user_df.columns:
            user_df = user_df[user_df["category"].str.lower() == "haircare"]
        elif "makeup" in text and "category" in user_df.columns:
            user_df = user_df[user_df["category"].str.lower() == "makeup"]

    return user_df["product"].drop_duplicates().head(5).tolist()
