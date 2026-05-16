"""
Hybrid Matching Engine — Steps 2, 4, 5, 6, 10
Runs BEFORE Gemini. gemini_engine.py handles Step 7 (grounded explanation).
"""

import re

MAX_CAPACITY = 5
_PRIOR_MEAN = 3.0
_PRIOR_WEIGHT = 3

_WEIGHTS = {
    "industry":            0.20,
    "needs_expertise":     0.25,
    "stage_context":       0.15,
    "semantic_similarity": 0.15,
    "availability":        0.10,
    "historical_feedback": 0.10,
    "programme_geography": 0.05,
}

_STAGE_MAP = {
    "early": {
        "seed", "early", "pre-revenue", "prototype", "mvp",
        "ideation", "pre-seed", "bootstrap", "pre-series",
    },
    "growth": {
        "series a", "series-a", "growth", "scaling", "traction", "revenue-generating",
    },
    "scale": {
        "series b", "series c", "mature", "enterprise", "ipo", "unicorn",
    },
}


# ── Step 2: Eligibility Filter ────────────────────────────────────────────────

def filter_eligible_candidates(target, candidates, linkages, max_capacity=MAX_CAPACITY):
    """Remove candidates that violate hard rules before any AI scoring is run."""
    target_id = target["id"]

    already_linked = {
        (l["actor_b_id"] if l["actor_a_id"] == target_id else l["actor_a_id"])
        for l in linkages
        if l["status"] == "active"
        and (l["actor_a_id"] == target_id or l["actor_b_id"] == target_id)
    }

    capacity_used: dict[int, int] = {}
    for l in linkages:
        if l["status"] == "active":
            for aid in (l.get("actor_a_id"), l.get("actor_b_id")):
                if aid is not None:
                    capacity_used[aid] = capacity_used.get(aid, 0) + 1

    return [
        c for c in candidates
        if c["id"] not in already_linked
        and capacity_used.get(c["id"], 0) < max_capacity
    ]


# ── Step 10: Bayesian Feedback Score ─────────────────────────────────────────

def bayesian_feedback_score(candidate_id, linkages, engagements):
    """
    Smoothed historical rating using Bayesian average.
    Prevents one 5-star rating from looking like a perfect track record.
    Returns 0.0–1.0.
    """
    candidate_linkage_ids = {
        l["id"] for l in linkages
        if l.get("actor_a_id") == candidate_id or l.get("actor_b_id") == candidate_id
    }
    ratings = [
        e["rating"] for e in engagements
        if e.get("linkage_id") in candidate_linkage_ids and e.get("rating") is not None
    ]
    if not ratings:
        return round(_PRIOR_MEAN / 5.0, 4)
    adjusted = (_PRIOR_MEAN * _PRIOR_WEIGHT + sum(ratings)) / (_PRIOR_WEIGHT + len(ratings))
    return round(adjusted / 5.0, 4)


# ── Scoring helpers ───────────────────────────────────────────────────────────

def _tokenize(text: str) -> set[str]:
    return set(re.sub(r"[^a-z0-9 ]", "", str(text).lower()).split())


def _word_overlap(text1, text2) -> float:
    if not text1 or not text2:
        return 0.0
    w1, w2 = _tokenize(text1), _tokenize(text2)
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / len(w1 | w2)


def _industry_score(target, candidate) -> float:
    t = (target.get("industry") or "").lower().strip()
    c = (candidate.get("industry") or "").lower().strip()
    if not t or not c:
        return 0.3
    if t == c:
        return 1.0
    return max(_word_overlap(t, c), 0.3)


def _skills_overlap_score(target, candidate) -> float:
    t_skills = {s.lower() for s in (target.get("skills") or [])}
    c_skills = {s.lower() for s in (candidate.get("skills") or [])}
    if not t_skills or not c_skills:
        return 0.2
    union = t_skills | c_skills
    return round(len(t_skills & c_skills) / len(union), 4) if union else 0.0


def _detect_stage(actor) -> str:
    text = f"{actor.get('description', '')} {actor.get('industry', '')}".lower()
    for stage, keywords in _STAGE_MAP.items():
        if any(kw in text for kw in keywords):
            return stage
    return "unknown"


def _stage_score(target, candidate) -> float:
    t, c = _detect_stage(target), _detect_stage(candidate)
    if t == "unknown" or c == "unknown":
        return 0.5
    return 1.0 if t == c else 0.3


def _semantic_proxy_score(target, candidate) -> float:
    """
    Proxy for vector similarity (no embeddings in MVP).
    Uses token overlap across description + industry + skills.
    """
    def _flatten(actor):
        return " ".join([
            actor.get("description", ""),
            actor.get("industry", ""),
            " ".join(actor.get("skills", [])),
        ])
    return round(_word_overlap(_flatten(target), _flatten(candidate)), 4)


def _capacity_score(candidate_id, linkages, max_capacity=MAX_CAPACITY) -> float:
    active = sum(
        1 for l in linkages
        if l["status"] == "active"
        and (l.get("actor_a_id") == candidate_id or l.get("actor_b_id") == candidate_id)
    )
    return round(max(0, max_capacity - active) / max_capacity, 4)


def _geography_score(target, candidate) -> float:
    t_loc = (target.get("location") or "").lower()
    c_loc = (candidate.get("location") or "").lower()
    if not t_loc or not c_loc:
        return 0.5
    if t_loc == c_loc:
        return 1.0
    t_parts = set(re.sub(r"[^a-z ]", "", t_loc).split())
    c_parts = set(re.sub(r"[^a-z ]", "", c_loc).split())
    return 0.7 if (t_parts & c_parts) else 0.2


# ── Step 4: Weighted Match Scoring ────────────────────────────────────────────

def compute_match_score(target, candidate, linkages, engagements,
                         programme="", max_capacity=MAX_CAPACITY) -> dict:
    """
    Transparent formula-based score for one candidate against a target.
    Returns: {actor_id, name, final_score, breakdown}
    """
    breakdown = {
        "industry":            _industry_score(target, candidate),
        "needs_expertise":     _skills_overlap_score(target, candidate),
        "stage_context":       _stage_score(target, candidate),
        "semantic_similarity": _semantic_proxy_score(target, candidate),
        "availability":        _capacity_score(candidate["id"], linkages, max_capacity),
        "historical_feedback": bayesian_feedback_score(candidate["id"], linkages, engagements),
        "programme_geography": _geography_score(target, candidate),
    }
    final_score = sum(breakdown[k] * _WEIGHTS[k] for k in _WEIGHTS)
    return {
        "actor_id":    candidate["id"],
        "name":        candidate["name"],
        "final_score": round(final_score, 4),
        "breakdown":   {k: round(v, 4) for k, v in breakdown.items()},
    }


# ── Step 5: Graph-lite Relationship Boost ────────────────────────────────────

def graph_relationship_boost(target, candidate, all_actors, linkages, engagements) -> float:
    """
    Treat ecosystem history as a lightweight graph.
    Boost if candidate has highly-rated completed linkages with actors similar to target.
    Returns additive float 0.0–0.10.
    """
    candidate_id = candidate["id"]
    target_industry = (target.get("industry") or "").lower()
    target_skills = {s.lower() for s in (target.get("skills") or [])}

    completed = {
        l["id"]: l for l in linkages
        if l.get("status") == "completed"
        and (l.get("actor_a_id") == candidate_id or l.get("actor_b_id") == candidate_id)
    }
    high_rated_ids = {
        e["linkage_id"] for e in engagements
        if e.get("linkage_id") in completed and (e.get("rating") or 0) >= 4
    }
    if not high_rated_ids:
        return 0.0

    boost = 0.0
    for lid in high_rated_ids:
        link = completed[lid]
        partner_id = link["actor_b_id"] if link["actor_a_id"] == candidate_id else link["actor_a_id"]
        partner = next((a for a in all_actors if a["id"] == partner_id), None)
        if not partner:
            continue
        p_industry = (partner.get("industry") or "").lower()
        p_skills = {s.lower() for s in (partner.get("skills") or [])}
        if target_industry and p_industry and target_industry == p_industry:
            boost += 0.05
        if target_skills & p_skills:
            boost += 0.03

    return round(min(boost, 0.10), 4)


# ── Step 6: Greedy Assignment ─────────────────────────────────────────────────

def greedy_assign(scored_candidates, linkages, max_capacity=MAX_CAPACITY) -> list:
    """
    Sort candidates by score descending, keep only those still under capacity.
    Does not create linkage entities — caller does that after admin approval.
    """
    capacity_used: dict[int, int] = {}
    for l in linkages:
        if l["status"] == "active":
            for aid in (l.get("actor_a_id"), l.get("actor_b_id")):
                if aid is not None:
                    capacity_used[aid] = capacity_used.get(aid, 0) + 1

    return [
        c for c in sorted(scored_candidates, key=lambda x: x["final_score"], reverse=True)
        if capacity_used.get(c["actor_id"], 0) < max_capacity
    ]
