import json
from utils.date_utils import parse_date, days_between
from datetime import timedelta
from config import POLICY

def evaluate_policy(member_id, category, claimed_amount, extracted_fields, trace):
    member = next((m for m in POLICY.get("members", []) if m["member_id"] == member_id), None)
    if not member:
        trace.add("Policy check failed: Member not found.")
        return {"approved": False, "approved_amount": 0.0, "reasons": ["MEMBER_NOT_FOUND"]}

    # 1. Waiting periods (fatal)
    join_date = parse_date(member["join_date"])
    treatment_date = parse_date(extracted_fields.get("treatment_date"))
    if join_date and treatment_date:
        days_since_join = days_between(join_date, treatment_date)
        waiting = POLICY.get("waiting_periods", {})
        initial = waiting.get("initial_waiting_period_days", 30)
        if days_since_join < initial:
            trace.add(f"Initial waiting period not met (need {initial} days).")
            return {"approved": False, "approved_amount": 0.0, "reasons": ["INITIAL_WAITING"]}
        # specific condition waiting
        diagnosis = extracted_fields.get("diagnosis", "").lower()
        specific = waiting.get("specific_conditions", {})
        for cond, days in specific.items():
            if cond in diagnosis:
                if days_since_join < days:
                    eligible = join_date + timedelta(days=days)
                    trace.add(f"Waiting period for {cond} not met; eligible from {eligible}.")
                    return {"approved": False, "approved_amount": 0.0, "reasons": [f"WAITING_{cond.upper()}"]}
                break

    # 2. Exclusions (fatal)
    global_exclusions = POLICY.get("exclusions", {}).get("conditions", [])
    diagnosis_lower = extracted_fields.get("diagnosis", "").lower()
    for excl in global_exclusions:
        if excl.lower() in diagnosis_lower:
            trace.add(f"Exclusion triggered: {excl}")
            return {"approved": False, "approved_amount": 0.0, "reasons": ["EXCLUDED_CONDITION"]}

    # 3. Pre-authorization (fatal)
    preauth_items = POLICY.get("pre_authorization", {}).get("required_for", [])
    tests = extracted_fields.get("tests_ordered", [])
    line_items = extracted_fields.get("line_items", [])
    for item in preauth_items:
        if "MRI" in item and any("mri" in str(t).lower() for t in tests + line_items):
            trace.add("Pre-authorization required for MRI.")
            return {"approved": False, "approved_amount": 0.0, "reasons": ["PRE_AUTH_MISSING"]}
        if "CT scan" in item and any("ct" in str(t).lower() for t in tests + line_items):
            trace.add("Pre-authorization required for CT scan.")
            return {"approved": False, "approved_amount": 0.0, "reasons": ["PRE_AUTH_MISSING"]}

    # 4. Line‑item adjudication (prune excluded items)
    # We'll use the global exclusions again for line‑item pruning
    line_items = extracted_fields.get("line_items", [])
    adjudicated_base = 0.0
    if not line_items:
        adjudicated_base = float(claimed_amount)
    else:
        for item in line_items:
            desc = item.get("description", "").lower()
            amt = float(item.get("amount", 0))
            if any(excl.lower() in desc for excl in global_exclusions):
                trace.add(f"Pruned line item: {item['description']} (-₹{amt})")
                continue
            adjudicated_base += amt
    if adjudicated_base == 0.0:
        return {"approved": False, "approved_amount": 0.0, "reasons": ["ALL_LINE_ITEMS_EXCLUDED"]}

    # 5. Category‑specific rules (discount, co‑pay, sub‑limit) – non‑fatal (cap)
    category_meta = POLICY.get("opd_categories", {}).get(category.lower(), {})
    if not category_meta:
        return {"approved": False, "approved_amount": 0.0, "reasons": ["UNKNOWN_CATEGORY"]}

    allowed = adjudicated_base

    # Network discount
    hospital_name = extracted_fields.get("hospital_name", "")
    is_network = any(h.lower() in hospital_name.lower() for h in POLICY.get("network_hospitals", []))
    if is_network:
        discount = category_meta.get("network_discount_percent", 0)
        allowed -= allowed * (discount / 100)
        trace.add(f"Network discount {discount}% applied.")

    # Co‑pay
    copay = category_meta.get("copay_percent", 0)
    if copay:
        allowed -= allowed * (copay / 100)
        trace.add(f"Co‑pay {copay}% applied.")

    # Sub‑limit cap
    sub_limit = category_meta.get("sub_limit", float('inf'))
    if allowed > sub_limit:
        allowed = float(sub_limit)
        trace.add(f"Capped at sub‑limit ₹{sub_limit}.")

    # Global per‑claim cap
    per_claim_limit = float(POLICY["coverage"]["per_claim_limit"])
    if allowed > per_claim_limit:
        allowed = per_claim_limit
        trace.add(f"Capped at per‑claim limit ₹{per_claim_limit}.")

    # Annual OPD limit cap (if we had YTD, we'd check, but skip for now)

    return {
        "approved": True,
        "approved_amount": max(0.0, allowed),
        "reasons": ["All rules cleared."]
    }