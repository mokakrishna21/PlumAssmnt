from services.confidence_engine import calculate_confidence

def generate_decision(policy_result, fraud_result, trace, extraction_confidence=1.0):
    if fraud_result.get("risk_score", 0) > 0.8:
        decision = "MANUAL_REVIEW"
        notes = "Fraud risk threshold exceeded."
        approved_amt = 0.0
        confidence = calculate_confidence(extraction_confidence, fraud_result["risk_score"], 0.5)
    elif not policy_result["approved"]:
        decision = "REJECTED"
        notes = f"Claim rejected: {', '.join(policy_result['reasons'])}"
        approved_amt = 0.0
        confidence = calculate_confidence(extraction_confidence, fraud_result["risk_score"], 0.9)
    else:
        decision = "APPROVED" if policy_result["approved_amount"] > 0 else "REJECTED"
        approved_amt = policy_result["approved_amount"]
        notes = f"Claim approved for ₹{approved_amt}"
        confidence = calculate_confidence(extraction_confidence, fraud_result["risk_score"], 1.0)

    # Override to MANUAL_REVIEW if confidence < 0.5
    if confidence < 0.5 and decision != "REJECTED":
        decision = "MANUAL_REVIEW"
        notes += " (low confidence)"

    return {
        "decision": decision,
        "approved_amount": approved_amt,
        "confidence": confidence,
        "trace": trace,
        "review_notes": notes
    }