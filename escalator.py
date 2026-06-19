# src/escalator.py

import json

from src.config import (
    RETRIEVAL_THRESHOLD,
    SENSITIVE_KEYWORDS
)


def needs_escalation(query, retrieved_docs):

    best_score = 0

    if retrieved_docs:
        best_score = max(
            doc["score"]
            for doc in retrieved_docs
        )

    if best_score < RETRIEVAL_THRESHOLD:
        return True

    query_lower = query.lower()

    for keyword in SENSITIVE_KEYWORDS:

        if keyword in query_lower:
            return True

    return False


def generate_handoff(
    persona,
    query,
    docs
):

    handoff = {
        "persona": persona,
        "issue": query,
        "documents_used": [
            d["source"] for d in docs
        ],
        "attempted_steps": [],
        "recommendation":
            "Human review required."
    }

    return json.dumps(
        handoff,
        indent=4
    )