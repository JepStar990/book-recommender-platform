from typing import Dict, Any

def normalize_volume(volume: Dict[str, Any]) -> Dict[str, Any]:
    info = volume.get("volumeInfo", {})

    return {
        "volume_id": volume.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "published_date": info.get("publishedDate"),
        "page_count": info.get("pageCount"),
        "language": info.get("language"),
        "average_rating": info.get("averageRating"),
        "ratings_count": info.get("ratingsCount"),
        "preview_link": info.get("previewLink"),
        "info_link": info.get("infoLink"),
        "authors": info.get("authors", []),
        "categories": info.get("categories", []),
        "raw_json": volume
    }
