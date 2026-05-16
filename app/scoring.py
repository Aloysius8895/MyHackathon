from collections import Counter
from math import sqrt


SYNONYMS: dict[str, set[str]] = {
    "fundraising": {"fundraising", "raise", "capital", "venture", "vc", "investment", "seed", "series"},
    "fintech": {"fintech", "finance", "financial", "payments", "banking"},
    "manufacturing": {"manufacturing", "factory", "industrial", "iot", "supply"},
    "marketing": {"marketing", "growth", "brand", "sales", "go-to-market", "gtm"},
    "product": {"product", "ux", "roadmap", "discovery", "saas"},
}


def normalize_token(value: str) -> str:
    return "".join(character.lower() if character.isalnum() else " " for character in value).strip()


def tokenize(values: list[str] | str) -> set[str]:
    raw_values = values if isinstance(values, list) else [values]
    tokens: set[str] = set()
    for value in raw_values:
        for part in normalize_token(value).split():
            if len(part) > 1:
                tokens.add(part)
    return expand_synonyms(tokens)


def expand_synonyms(tokens: set[str]) -> set[str]:
    expanded = set(tokens)
    for canonical, related in SYNONYMS.items():
        if tokens.intersection(related):
            expanded.add(canonical)
            expanded.update(related)
    return expanded


def overlap_score(left: list[str], right: list[str]) -> float:
    left_tokens = tokenize(left)
    right_tokens = tokenize(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens.intersection(right_tokens)) / len(left_tokens)


def binary_overlap(left: list[str], right: list[str]) -> float:
    if not left or not right:
        return 0.5
    return 1.0 if tokenize(left).intersection(tokenize(right)) else 0.0


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0
    dot = sum(left_value * right_value for left_value, right_value in zip(left, right, strict=True))
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return max(0.0, min(1.0, dot / (left_norm * right_norm)))


def text_embedding(values: list[str], dimensions: int = 32) -> list[float]:
    """Small deterministic embedding fallback for local MVP demos."""

    counts: Counter[int] = Counter()
    for token in tokenize(values):
        counts[hash(token) % dimensions] += 1
    vector = [float(counts[index]) for index in range(dimensions)]
    norm = sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def semantic_score(left_values: list[str], right_values: list[str], left_embedding: list[float], right_embedding: list[float]) -> float:
    provided_similarity = cosine_similarity(left_embedding, right_embedding)
    if provided_similarity > 0:
        return provided_similarity
    return cosine_similarity(text_embedding(left_values), text_embedding(right_values))


def bayesian_average(ratings: list[int], prior_score: float = 3.5, prior_weight: int = 3) -> float:
    if not ratings:
        return prior_score
    return ((prior_score * prior_weight) + sum(ratings)) / (prior_weight + len(ratings))
