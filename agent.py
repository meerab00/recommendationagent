
from recommender import recommend_items

def run_agent(user_input, df):

    user_input = user_input.lower()

    # Intent handling (simple AI brain)
    if "recommend" in user_input or "suggest" in user_input:

        result = recommend_items(df, user_input)

        return f"Here are smart recommendations based on your data:\n\n{result}"

    elif "sad" in user_input:
        result = recommend_items(df, user_input)
        return f"For sad mood, I found these:\n\n{result}"

    else:
        return "Tell me like: recommend me products or movies 😊"
