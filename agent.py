from recommender import get_recommendations

def run_agent(user_input, df):
    user_input = user_input.lower()

    # simple intent detection
    if "recommend" in user_input or "suggest" in user_input:
        result = get_recommendations(df)
        return f"Here are your recommendations:\n\n{result}"

    elif "sad" in user_input:
        result = get_recommendations(df)
        return f"For sad mood, I suggest:\n\n{result}"

    else:
        return "Please ask for recommendations like 'suggest me products or movies'"
