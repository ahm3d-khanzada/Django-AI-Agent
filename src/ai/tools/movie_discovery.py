from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from tmdb.client import search_movie, movies_details
from asgiref.sync import async_to_sync
from permit import PermitApiError
from my_permit import permit_client as permit


@tool
def search_movies(query: str, limit: int = 5, config: RunnableConfig = {}) -> dict:
    """
    Search for movies by title or keyword on TMDB with permission check.

    Args:
        query: The search term to look for in movie titles.
        limit: Maximum number of movie results to return (default: 5).
        config: Configuration passed by the agent runtime (contains user_id if needed).

    Returns:
        dict: With 'success' and 'movies' (list of dicts) or 'error'.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")
    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Permission check
    # -----------------------------
    try:
        has_perm = async_to_sync(permit.check)(
            str(user_id),
            resource="movie_discovery",
            action="search_movies",  # Permit action key
            
        )
    except PermitApiError as e:
        return {"error": f"Permit API error: {str(e)}"}

    if not has_perm:
        raise PermissionError("User does not have permission to search movies.")

    # -----------------------------
    # Perform movie search
    # -----------------------------
    try:
        response = search_movie(query=query, page=1, raw=False)
        results = response.get("results", [])[:limit]

        if not results:
            return {"success": True, "movies": [], "message": "No movies found matching your query."}

        formatted_results = [
            {
                "id": movie.get("id"),
                "title": movie.get("title", "N/A"),
                "release_date": movie.get("release_date", "N/A"),
                "overview": movie.get("overview") or "No overview available."
            }
            for movie in results
        ]

        return {"success": True, "movies": formatted_results}

    except Exception as e:
        return {"error": f"Error searching movies: {str(e)}"}


@tool
def get_movie_details(movie_id: int, config: RunnableConfig = {}) -> dict:
    """
    Get details of a single movie by TMDB ID with permission check.

    Args:
        movie_id: The TMDB ID of the movie.
        config: Configuration passed by the agent runtime (contains user_id if needed).

    Returns:
        dict: Movie details or error.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    configurable = config.get("configurable") or {}
    user_id = configurable.get("user_id")
    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Permission check
    # -----------------------------
    try:
        has_perm = async_to_sync(permit.check)(
            str(user_id),
            resource="movie_discovery",
            action="get_movie_details",  # Permit action key
            
        )
    except PermitApiError as e:
        return {"error": f"Permit API error: {str(e)}"}

    if not has_perm:
        raise PermissionError("User does not have permission to get movie details.")

    # -----------------------------
    # Fetch movie details
    # -----------------------------
    try:
        movie = movies_details(movie_id=movie_id, raw=False)
        if not movie:
            return {"error": "Movie not found"}

        return {
            "success": True,
            "id": movie.get("id"),
            "title": movie.get("title", "N/A"),
            "release_date": movie.get("release_date", "N/A"),
            "overview": movie.get("overview") or "No overview available.",
            "genres": [g["name"] for g in movie.get("genres", [])],
            "runtime": movie.get("runtime", "N/A")
        }

    except Exception as e:
        return {"error": f"Error fetching movie details: {str(e)}"}



@tool
def get_movie_details(movie_id: int, config: dict = {}) -> dict:
    """
    Get detailed information about a specific movie using its TMDB ID with permission check.
    
    Args:
        movie_id: The TMDB ID of the movie.
        config: Configuration passed by the agent runtime (contains user_id if needed).
    
    Returns:
        dict: With 'success' and movie details or 'error'.
    """

    # -----------------------------
    # Get user_id from config
    # -----------------------------
    user_id = config.get("user_id")
    if not user_id:
        return {"error": "user_id missing in config"}

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return {"error": "user_id must be an integer"}

    # -----------------------------
    # Permission check
    # -----------------------------
    try:
        has_perm = async_to_sync(permit.check)(
            str(user_id),
            resource="movie_discovery",
            action="get_movie_details",  # Permit action key
            
        )
    except PermitApiError as e:
        return {"error": f"Permit API error: {str(e)}"}

    if not has_perm:
        raise PermissionError("User does not have permission to fetch movie details.")

    # -----------------------------
    # Fetch movie details
    # -----------------------------
    try:
        response = movies_details(movie_id=movie_id, raw=False)

        title = response.get("title", "N/A")
        release_date = response.get("release_date", "N/A")
        overview = response.get("overview") or "No overview available."
        genres = ", ".join([g["name"] for g in response.get("genres", [])]) or "N/A"
        runtime = response.get("runtime", "N/A")

        return {
            "success": True,
            "id": movie_id,
            "title": title,
            "release_date": release_date,
            "overview": overview,
            "genres": genres,
            "runtime": runtime
        }

    except Exception as e:
        return {"error": f"Error fetching movie details: {str(e)}"}




# Final list of tools
movie_tools = [
    search_movies,
    get_movie_details,
]