"""
query_parser.py
----------------
Turns a free-text prospecting brief such as:
    "Find dentists around Karachi that still don't have a website"
into structured search parameters: {category, location, intent, target_missing_site}

Two strategies are supported:
1. LLM strategy (Groq, OpenAI-compatible endpoint) - richer understanding of intent.
2. Heuristic strategy - a dependency-free regex/keyword parser used automatically
   whenever no AI key is configured, so the app always works out of the box.
"""

import json
import re
from dataclasses import dataclass, asdict
from typing import Optional

NO_SITE_HINTS = (
    "that don't have a website yet", "that dont have a website yet",
    "that doesn't have a website yet", "who don't have a website yet",
    "without a website yet", "don't have a website yet", "dont have a website yet",
    "doesn't have a website yet", "no website", "without a website",
    "without website", "needs a website", "need a website", "web design",
    "website development", "missing website", "don't have a website",
    "dont have a website", "doesn't have a website", "no site",
    "lacking a website", "still don't have a website", "still dont have a website",
)

CONNECTOR_WORDS = (" in ", " near ", " around ", " at ")

_TRAILING_FILLER = (
    "that", "which", "who", "yet", "still", "currently", "and", "but", ",", ".",
)


def _strip_trailing_filler(text: str) -> str:
    text = re.sub(r"\s{2,}", " ", text).strip(" ,.")
    changed = True
    while changed:
        changed = False
        for filler in _TRAILING_FILLER:
            if text.lower().endswith(f" {filler}") or text.lower() == filler:
                text = text[: len(text) - len(filler)].strip(" ,.")
                changed = True
    return text.strip(" ,.")


@dataclass
class SearchBrief:
    category: str
    location: str
    intent: str
    target_missing_site: bool
    parsed_by: str  # "ai" or "heuristic"


_LEADING_COMMANDS = (
    "find me", "find", "search for", "look for", "show me", "get me", "i need",
    "i want", "give me",
)


def _strip_leading_command(text: str) -> str:
    lowered = text.lower()
    for cmd in sorted(_LEADING_COMMANDS, key=len, reverse=True):
        if lowered.startswith(cmd + " "):
            return text[len(cmd):].strip()
    return text


def _heuristic_parse(raw_text: str) -> SearchBrief:
    text = _strip_leading_command(raw_text.strip())
    lowered = text.lower()

    target_missing_site = any(hint in lowered for hint in NO_SITE_HINTS)

    # strip a bracketed / trailing intent clause, e.g. "cafes in Lahore (web design)"
    intent = ""
    bracket_match = re.search(r"[\(\[]([^\)\]]+)[\)\]]", text)
    if bracket_match:
        intent = bracket_match.group(1).strip()
        text = (text[: bracket_match.start()] + text[bracket_match.end():]).strip()

    split_point = -1
    connector_used = None
    for connector in CONNECTOR_WORDS:
        idx = lowered.find(connector)
        if idx != -1 and (split_point == -1 or idx < split_point):
            split_point = idx
            connector_used = connector

    if split_point != -1:
        category = text[:split_point].strip(" ,.")
        location = text[split_point + len(connector_used):].strip(" ,.")
    else:
        # no clear connector - assume the whole phrase is the category
        category = text.strip(" ,.")
        location = ""

    # remove leftover intent phrasing from the location/category tail
    for hint in NO_SITE_HINTS:
        category = re.sub(re.escape(hint), "", category, flags=re.IGNORECASE)
        location = re.sub(re.escape(hint), "", location, flags=re.IGNORECASE)

    category = _strip_trailing_filler(category)
    location = _strip_trailing_filler(location)

    if not intent and target_missing_site:
        intent = "website development"

    return SearchBrief(
        category=category or text,
        location=location,
        intent=intent,
        target_missing_site=target_missing_site,
        parsed_by="heuristic",
    )


def _ai_parse(raw_text: str, api_key: str, model: str, base_url: str) -> Optional[SearchBrief]:
    try:
        from openai import OpenAI
    except ImportError:
        return None

    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        completion = client.chat.completions.create(
            model=model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract structured prospecting search parameters from the user's "
                        "message. Respond with ONLY a compact JSON object with exactly these "
                        "keys: category (string), location (string), intent (string, may be "
                        "empty), target_missing_site (boolean - true only if the user wants "
                        "businesses that currently lack a website, e.g. for web design / "
                        "website development outreach; false for general or marketing leads)."
                    ),
                },
                {"role": "user", "content": raw_text},
            ],
        )
        content = completion.choices[0].message.content or ""
        content = re.sub(r"```(json)?", "", content).strip()
        match = re.search(r"\{.*\}", content, flags=re.DOTALL)
        payload = json.loads(match.group(0) if match else content)
        return SearchBrief(
            category=str(payload.get("category", "")).strip(),
            location=str(payload.get("location", "")).strip(),
            intent=str(payload.get("intent", "")).strip(),
            target_missing_site=bool(payload.get("target_missing_site", False)),
            parsed_by="ai",
        )
    except Exception:
        return None


def parse_brief(
    raw_text: str,
    ai_api_key: str = "",
    ai_model: str = "llama-3.3-70b-versatile",
    ai_base_url: str = "https://api.groq.com/openai/v1",
) -> SearchBrief:
    """Public entry point. Falls back to the heuristic parser on any AI failure."""
    if ai_api_key:
        result = _ai_parse(raw_text, ai_api_key, ai_model, ai_base_url)
        if result and result.category:
            return result
    return _heuristic_parse(raw_text)


def brief_to_dict(brief: SearchBrief) -> dict:
    return asdict(brief)
