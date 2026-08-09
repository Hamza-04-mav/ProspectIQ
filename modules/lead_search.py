"""
lead_search.py
---------------
Fetches local-business prospects via Serper.dev's Google Maps endpoint and
normalizes them into a flat, scoring-ready record shape.
"""

from typing import List, Dict

import requests

SERPER_ENDPOINT = "https://google.serper.dev/maps"


class LeadSearchError(Exception):
    pass


def _normalize(raw_place: Dict) -> Dict:
    website = raw_place.get("website") or raw_place.get("link") or ""
    phone = raw_place.get("phoneNumber") or raw_place.get("phone") or ""
    return {
        "name": raw_place.get("title", "Unknown Business"),
        "address": raw_place.get("address", "Address unavailable"),
        "phone": phone or "N/A",
        "rating": raw_place.get("rating"),
        "reviews": raw_place.get("ratingCount") or raw_place.get("reviews") or 0,
        "website": website,
        "has_website": bool(website),
        "category_tag": raw_place.get("category", ""),
    }


def search_live(category: str, location: str, api_key: str, country: str = "us") -> List[Dict]:
    """Query Serper.dev Google Maps search. Raises LeadSearchError on failure."""
    if not api_key:
        raise LeadSearchError("Missing Serper API key.")

    query = f"{category} in {location}".strip()
    try:
        response = requests.post(
            SERPER_ENDPOINT,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "gl": country, "hl": "en"},
            timeout=25,
        )
    except requests.RequestException as exc:
        raise LeadSearchError(f"Network error contacting Serper.dev: {exc}") from exc

    if response.status_code != 200:
        raise LeadSearchError(
            f"Serper.dev returned HTTP {response.status_code}: {response.text[:200]}"
        )

    payload = response.json()
    places = payload.get("places", [])
    return [_normalize(p) for p in places]
