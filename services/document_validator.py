from config import POLICY

def validate_documents(claim_category, uploaded_files_with_types, trace):
    """
    uploaded_files_with_types: list of dicts with keys 'file' and 'doc_type'
    doc_type is one of PRESCRIPTION, HOSPITAL_BILL, PHARMACY_BILL, LAB_REPORT
    """
    req_rules = POLICY.get("document_requirements", {}).get(claim_category, {})
    required_types = req_rules.get("required", [])
    optional_types = req_rules.get("optional", [])

    if not required_types:
        trace.add("No document requirements defined for this category.")
        return {"valid": False, "message": f"No requirements for category {claim_category}"}

    # Collect user‑provided types
    provided_types = [item["doc_type"] for item in uploaded_files_with_types if item["doc_type"]]
    provided_set = set(provided_types)
    required_set = set(required_types)

    # Check if all required are present
    missing = required_set - provided_set
    if missing:
        msg = f"Missing required document(s): {', '.join(missing)}. You uploaded: {', '.join(provided_types) if provided_types else 'none'}."
        trace.add("Validation failed: " + msg)
        return {"valid": False, "message": msg}

    trace.add("Document validation passed: all required types present.")
    return {"valid": True, "provided_types": provided_types}