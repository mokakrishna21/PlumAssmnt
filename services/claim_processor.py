from services.document_validator import validate_documents
from services.extractor import extract_from_document
from services.policy_engine import evaluate_policy
from services.fraud_detector import detect_fraud
from services.decision_engine import generate_decision
from services.trace_manager import TraceManager

def process_claim(member_id, claim_category, claimed_amount, uploaded_files_with_types):
    trace = TraceManager()
    trace.add("Claim processing started.")

    # 1. Document validation
    validation = validate_documents(claim_category, uploaded_files_with_types, trace)
    if not validation["valid"]:
        return {
            "decision": "REJECTED",
            "approved_amount": 0.0,
            "confidence": 0.0,
            "trace": trace.get_trace(),
            "review_notes": f"Document validation failed: {validation['message']}"
        }

    # 2. Extract from each document and merge results
    all_fields = {}
    confidence_sum = 0.0
    count = 0
    for item in uploaded_files_with_types:
        file_obj = item["file"]
        result = extract_from_document(file_obj, trace)
        if result["fields"]:
            # Merge: we'll take the first non‑null value for each field
            for key, value in result["fields"].items():
                if value is not None and all_fields.get(key) is None:
                    all_fields[key] = value
            confidence_sum += result["confidence"]
            count += 1

    extraction_confidence = confidence_sum / count if count > 0 else 0.2
    trace.add(f"Extraction completed. Overall confidence: {extraction_confidence:.2f}")

    # 3. Policy evaluation
    policy_result = evaluate_policy(member_id, claim_category, claimed_amount, all_fields, trace)

    # 4. Fraud detection (stub)
    fraud_result = detect_fraud(member_id)

    # 5. Final decision
    decision = generate_decision(
        policy_result,
        fraud_result,
        trace.get_trace(),
        extraction_confidence
    )

    # Ensure trace is included
    decision["trace"] = trace.get_trace()
    return decision