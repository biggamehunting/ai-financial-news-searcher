

def calculate_confidence(rerank_scores: list[float]) -> tuple[float, str]:
    if not rerank_scores:
        return 0.0, "Low"

    score = max(rerank_scores)

    if score >= 0.80:
        level = "High"
    elif score >= 0.60:
        level = "Medium"
    else:
        level = "Low"

    return round(score, 2), level




# def calculate_confidence(rerank_scores: list[float]) -> float:
#     if not rerank_scores:
#         return 0.0

#     return round(max(rerank_scores), 2)