"""
scoring.py
----------
A transparent, explainable heuristic that ranks how "workable" a prospect is,
so results aren't just a flat list - the best outreach targets float to the top.
"""

from typing import Dict


def score_lead(lead: Dict, target_missing_site: bool) -> int:
    score = 35  # baseline

    if target_missing_site:
        score += 35 if not lead.get("has_website") else -15
    else:
        score += 10 if lead.get("has_website") else 0

    rating = lead.get("rating")
    if isinstance(rating, (int, float)):
        score += min(rating * 6, 30)

    reviews = lead.get("reviews") or 0
    try:
        reviews = int(reviews)
    except (TypeError, ValueError):
        reviews = 0
    if reviews >= 100:
        score += 12
    elif reviews >= 25:
        score += 7
    elif reviews >= 5:
        score += 3

    if lead.get("phone") and lead.get("phone") != "N/A":
        score += 8

    return max(5, min(100, round(score)))


def score_tier(score: int) -> str:
    if score >= 75:
        return "Hot"
    if score >= 50:
        return "Warm"
    return "Cool"


def tier_color(tier: str) -> str:
    return {"Hot": "#DC2626", "Warm": "#D97706", "Cool": "#2563EB"}.get(tier, "#64748B")


def enrich_with_scores(leads, target_missing_site: bool):
    for lead in leads:
        lead["prospect_score"] = score_lead(lead, target_missing_site)
        lead["tier"] = score_tier(lead["prospect_score"])
    return sorted(leads, key=lambda l: l["prospect_score"], reverse=True)
