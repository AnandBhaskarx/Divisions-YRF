import os
from groq import Groq
from supabase import create_client

# -----------------------------
# Environment variables (FIXED)
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase credentials not set")


# -----------------------------
# Clients
# -----------------------------
groq_client = Groq(api_key=GROQ_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# Prompt for classification
# -----------------------------
ROUTER_PROMPT = """
You are a query classifier for a Yash Raj Films (YRF) AI system.

Classify the user query into exactly ONE category:

movie_db →
- Questions about individual movies
- Movie names, actors, directors, cast
- Release year, ratings, box office

embedding_db →
- Yash Raj Films policies, rules, booking, theatres
- Distribution strategy, partnerships, contracts
- Internal documents and guidelines

unknown →
- Unrelated questions

Return ONLY one word:
movie_db OR embedding_db OR unknown

Query: {query}
"""

# -----------------------------
# Intent classification
# -----------------------------
def classify_query(query: str) -> str:
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": ROUTER_PROMPT.format(query=query)}
        ],
        temperature=0
    )

    intent = response.choices[0].message.content.strip().lower()
    return intent if intent in {"movie_db", "embedding_db", "unknown"} else "unknown"


# -----------------------------
# Movie DB search (Supabase)
# -----------------------------
def search_movies(query: str):
    response = (
        supabase
        .table("movies")
        .select("title, director, release_year, rating")
        .or_(
            f"title.ilike.%{query}%,director.ilike.%{query}%"
        )
        .limit(5)
        .execute()
    )

    return response.data if response.data else None


# -----------------------------
# Embedding DB search (Supabase)
# -----------------------------
def search_embeddings(query: str):
    """
    Simple text search on content.
    (Vector search can be added later)
    """
    response = (
        supabase
        .table("embeddings")
        .select("content")
        .ilike("content", f"%{query}%")
        .limit(3)
        .execute()
    )

    return response.data if response.data else None


# -----------------------------
# Main execution
# -----------------------------
def handle_query(query: str):
    intent = classify_query(query)
    print(f"\n[Intent detected] → {intent}")

    if intent == "movie_db":
        return search_movies(query)

    if intent == "embedding_db":
        return search_embeddings(query)

    return None


if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (type exit to quit): ")
        if user_query.lower() == "exit":
            break

        result = handle_query(user_query)

        if result is None:
            print("❌ No data found.")
        else:
            print("✅ Result:", result)
