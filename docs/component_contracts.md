# Component Contracts

This document defines the interface contracts for all major components.

---

# Document Validation Agent

## Purpose

Validate uploaded documents before processing.

## Input

```json
{
  "claim_category": "CONSULTATION",
  "documents": []
}
```

## Output

```json
{
  "valid": true,
  "message": "",
  "provided_types": []
}
```

## Possible Errors

* DOCUMENT_MISSING
* WRONG_DOCUMENT_TYPE
* DOCUMENT_UNREADABLE
* PATIENT_MISMATCH

---

# Information Extraction Agent

## Purpose

Convert documents into structured information.

## Input

```json
{
  "file": "prescription.jpg"
}
```

## Output

```json
{
  "fields": {
    "patient_name": "Rajesh Kumar",
    "diagnosis": "Viral Fever"
  },
  "confidence": 0.92
}
```

## Failure Behaviour

Returns:

```json
{
  "fields": {},
  "confidence": 0.2
}
```

Processing continues.

---

# Policy Adjudication Engine

## Purpose

Evaluate policy rules.

## Input

```json
{
  "member_id": "EMP001",
  "claim_data": {},
  "policy": {}
}
```

## Output

```json
{
  "approved": true,
  "approved_amount": 1350,
  "reasons": []
}
```

## Failure Behaviour

Fatal rule:

```json
{
  "approved": false,
  "reasons": [
    "WAITING_PERIOD"
  ]
}
```

---

# Fraud Detection Agent

## Purpose

Identify suspicious claims.

## Input

```json
{
  "member_id": "EMP008",
  "claim_history": []
}
```

## Output

```json
{
  "risk_score": 0.81,
  "flags": [
    "MULTIPLE_SAME_DAY_CLAIMS"
  ]
}
```

---

# Decision Engine

## Purpose

Generate final outcome.

## Input

```json
{
  "policy_result": {},
  "fraud_result": {},
  "confidence": 0.92
}
```

## Output

```json
{
  "decision": "APPROVED",
  "approved_amount": 1350,
  "confidence": 0.92,
  "trace": []
}
```

---

# Claim Processor

## Purpose

Orchestrate all agents.

## Input

```json
{
  "member_id": "EMP001",
  "claim_category": "CONSULTATION",
  "documents": []
}
```

## Output

```json
{
  "decision": "APPROVED",
  "approved_amount": 1350,
  "trace": []
}
```

---

# Trace Manager

## Purpose

Record every decision step.

## Trace Entry Format

```json
{
  "step": "document_validation",
  "status": "PASSED",
  "details": "Required documents found"
}
```

Every component writes to the trace.

This guarantees complete explainability.
