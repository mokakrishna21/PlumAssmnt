# Architecture Document

## Overview

The Health Insurance Claims Processing System is designed as an explainable, policy-driven, fault-tolerant pipeline for automating claim adjudication.

The system processes medical claims by validating documents, extracting structured information, applying policy rules, evaluating fraud signals, and producing transparent claim decisions.

The architecture prioritizes:

* Explainability
* Determinism
* Reliability
* Configurability
* Scalability

---

# System Goals

The assignment specifies six non-negotiable requirements:

1. Accept claim submissions
2. Detect document problems early
3. Extract structured information
4. Make claim decisions
5. Explain every decision
6. Handle failures gracefully

The architecture was designed specifically around these requirements.

---

# High-Level Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
Claim Processor
 │
 ├── Document Validation Agent
 ├── Information Extraction Agent
 ├── Policy Adjudication Engine
 ├── Fraud Detection Agent
 └── Decision Engine
 │
 ▼
Decision + Trace
```

---

# Components

## 1. Streamlit UI

Responsibilities:

* Claim submission
* Member selection
* Document upload
* Result visualization
* Trace visualization

The UI contains no business logic.

---

## 2. Claim Processor

Responsibilities:

* Workflow orchestration
* Agent execution order
* Error handling
* Result aggregation

The processor acts as the system coordinator.

---

## 3. Document Validation Agent

Responsibilities:

* Validate document types
* Verify required documents
* Detect missing documents
* Detect invalid uploads

Example:

Consultation claims require:

* PRESCRIPTION
* HOSPITAL_BILL

If a user uploads two prescriptions, processing stops before extraction.

---

## 4. Information Extraction Agent

Responsibilities:

* OCR processing
* PDF text extraction
* LLM-based structuring

Extracted fields:

* Patient information
* Doctor information
* Diagnosis
* Treatments
* Medicines
* Billing details

---

## 5. Policy Adjudication Engine

Responsibilities:

* Coverage validation
* Waiting period checks
* Exclusion checks
* Co-pay calculations
* Sub-limit calculations
* Pre-authorization validation
* Network hospital discounts

All rules are dynamically loaded from:

```text
policy_terms.json
```

No policy rules are hardcoded.

---

## 6. Fraud Detection Agent

Responsibilities:

* Same-day claim analysis
* High-value claim monitoring
* Risk scoring

Current implementation uses rule-based checks.

Future versions can incorporate ML-based fraud scoring.

---

## 7. Decision Engine

Responsibilities:

* Aggregate agent outputs
* Generate final decision
* Compute confidence score
* Produce explanation trace

Supported outcomes:

* APPROVED
* PARTIAL
* REJECTED
* MANUAL_REVIEW

---

# Explainability Design

Every component writes entries into a trace object.

Example:

```json
{
  "step": "waiting_period_check",
  "result": "FAILED",
  "reason": "Diabetes waiting period not completed"
}
```

This enables:

* Auditing
* Debugging
* Regulatory review
* Operations transparency

---

# Fault Tolerance

The system follows graceful degradation.

Example:

If OCR fails:

* Processing continues
* Confidence decreases
* Trace records the failure
* Manual review recommendation is added

The system never crashes due to a single component failure.

---

# Design Decisions

## Why Rules Instead of LLM Decisions?

LLMs are excellent for extraction but poor for deterministic financial decisions.

Insurance adjudication requires:

* Reproducibility
* Auditability
* Determinism

Therefore:

* LLMs extract
* Rules decide

---

## Why JSON-Based Policy Configuration?

Benefits:

* No code changes for policy updates
* Easy auditing
* Better maintainability

---

## Why Multi-Agent Design?

Benefits:

* Clear responsibilities
* Independent testing
* Better observability
* Easier future scaling

---

# Scaling Strategy

For 10× traffic:

1. Move agents to independent services
2. Introduce message queues
3. Parallelize extraction
4. Store claims in PostgreSQL
5. Add Redis caching

The current modular architecture supports this migration with minimal redesign.

---

# Conclusion

The architecture prioritizes explainability, determinism, and reliability while maintaining clear separation of concerns and scalability potential.
