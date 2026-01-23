from supabase_client import supabase

def fetch_movies(query: str):
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

    if not response.data:
        return None

    return response.data
