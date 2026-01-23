from router import classify_query
from movie_db import fetch_movies
from embedding_db import fetch_from_embeddings

def handle_query(query: str):
    intent = classify_query(query)
    print(f"[Intent] → {intent}")

    if intent == "movie_db":
        return fetch_movies(query)

    if intent == "embedding_db":
        return fetch_from_embeddings(query)

    return None


if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (type exit to quit): ")
        if q.lower() == "exit":
            break

        result = handle_query(q)

        if result is None:
            print("❌ No relevant data found.")
        else:
            print("✅ Result:", result)
