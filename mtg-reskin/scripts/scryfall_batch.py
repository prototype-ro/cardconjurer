import json
import re
import sys
import urllib.request

SCRYFALL_COLLECTION_URL = "https://api.scryfall.com/cards/collection"
USER_AGENT = "mtg-reskin/1.0"


def parse_decklist(text: str) -> list[dict]:
    """Parse Moxfield-style export text into [{quantity, name}, ...]."""
    entries = []
    line_re = re.compile(r"^(\d+)\s+(.+?)\s*$")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("//") or line.startswith("#"):
            continue
        match = line_re.match(line)
        if not match:
            continue
        quantity, name = match.groups()
        entries.append({"quantity": int(quantity), "name": name})
    return entries


def chunk_identifiers(identifiers: list[dict], size: int = 75):
    for i in range(0, len(identifiers), size):
        yield identifiers[i : i + size]


def fetch_collection(identifiers: list[dict]) -> list[dict]:
    """POST one chunk (<=75 identifiers) to /cards/collection, return card objects."""
    payload = json.dumps({"identifiers": identifiers}).encode("utf-8")
    request = urllib.request.Request(
        SCRYFALL_COLLECTION_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        body = json.loads(response.read())
    return body.get("data", [])


def enrich_decklist(decklist_text: str) -> list[dict]:
    """Parse decklist, batch-fetch Scryfall data, return one enriched record per card entry."""
    entries = parse_decklist(decklist_text)
    identifiers = [{"name": entry["name"]} for entry in entries]

    by_name = {}
    for chunk in chunk_identifiers(identifiers):
        for card in fetch_collection(chunk):
            by_name[card["name"].lower()] = card

    enriched = []
    for entry in entries:
        card = by_name.get(entry["name"].lower(), {})
        enriched.append(
            {
                "quantity": entry["quantity"],
                "name": entry["name"],
                "type_line": card.get("type_line", ""),
                "color_identity": card.get("color_identity", []),
                "mana_value": card.get("cmc"),
                "oracle_text": card.get("oracle_text", ""),
                "keywords": card.get("keywords", []),
            }
        )
    return enriched


if __name__ == "__main__":
    decklist_text = sys.stdin.read()
    result = enrich_decklist(decklist_text)
    json.dump(result, sys.stdout, indent=2)
