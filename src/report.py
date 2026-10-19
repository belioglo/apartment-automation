from collections import Counter

def create_report(requests: list[dict]) -> dict:
    successful = [
        item for item in requests
        if not item.get("errors")
        and "category" in item
    ]

    needs_review = [
        item for item in requests
        if item.get("errors")
    ]

    possible_duplicates = [
        item for item in requests
        if "Возможный дубликат" in item.get("errors", "")
    ]

    return {
        "total_requests": len(requests),
        "classified_requests": len(successful),
        "needs_review": len(needs_review),
        "possible_duplicate_requests": len(possible_duplicates),
        "by_category": dict(
            Counter(item["category"] for item in successful)
        ),
        "by_priority": dict(
            Counter(item["priority"] for item in successful)
        ),
    }

