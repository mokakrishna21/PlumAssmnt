def calculate_confidence(extraction_confidence=1.0, fraud_score=0.0, rule_certainty=1.0):
    # Combine factors
    base = 1.0
    base *= extraction_confidence
    base *= (1 - fraud_score * 0.5)  # high fraud reduces confidence
    base *= rule_certainty
    return min(1.0, max(0.0, base))