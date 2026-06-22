# 🏥 Plum Health Insurance Claims Processing System

## Overview

This project is an AI-powered Health Insurance Claims Processing System built for the Plum AI Engineer Assignment.

The system automates the end-to-end claim adjudication workflow by validating uploaded documents, extracting medical information, applying policy rules, detecting risk signals, and generating explainable claim decisions.

The solution is built using:

* Streamlit (User Interface)
* Groq API
* Llama 3.3 70B Versatile
* Python
* OCR-based document extraction
* Configuration-driven policy evaluation

The system is designed to be:

* Explainable
* Deterministic
* Testable
* Maintainable
* Fault tolerant

---

# Design Philosophy

The goal of this assignment was not to build the most complex system possible.

Instead, the goal was to build a system that is:

* Explainable
* Testable
* Deterministic
* Easy to maintain

For this reason, a pipeline architecture was chosen instead of a fully autonomous agent framework.

Every stage has a clearly defined responsibility:

1. Document Triage
2. Document Validation
3. Information Extraction
4. Policy Evaluation
5. Fraud Detection
6. Decision Generation

This improves:

* Debugging
* Observability
* Failure isolation
* Development speed

A reviewer should be able to identify exactly where a failure occurred and why a particular decision was made.

---

# Why Not LangGraph?

A graph-based agent architecture was considered.

However:

* The assignment requires deterministic decisions.
* Insurance claims require auditability.
* Policy validation is primarily rule-based.
* Failure handling must be predictable.
* Decision paths must be explainable.

A sequential pipeline provides:

* Lower latency
* Easier debugging
* Better observability
* More predictable execution
* Easier testing

For these reasons, a pipeline architecture was selected over a fully autonomous agent workflow.

---

# System Architecture

```text
User Upload
    │
    ▼
Document Triage
    │
    ▼
Document Validation
    │
    ▼
Information Extraction
    │
    ▼
Policy Evaluation
    │
    ▼
Fraud Detection
    │
    ▼
Decision Engine
    │
    ▼
Reviewer Notes
    │
    ▼
Confidence Engine
    │
    ▼
Final Output
```

---

# Project Structure

```text
health_claims_ai/

├── app.py
│
├── config/
│   └── policy_terms.json
│
├── services/
│   ├── claim_processor.py
│   ├── document_triage.py
│   ├── document_validator.py
│   ├── extractor.py
│   ├── policy_engine.py
│   ├── fraud_detector.py
│   ├── confidence_engine.py
│   ├── decision_engine.py
│   ├── reviewer_notes.py
│   └── trace_manager.py
│
├── utils/
│   ├── groq_client.py
│   ├── pdf_parser.py
│   ├── image_parser.py
│   └── schema_validator.py
│
├── tests/
│   ├── test_runner.py
│   └── eval_report_generator.py
│
├── requirements.txt
├── README.md
└── test_cases.json
```

---

# End-to-End Flow

## Step 1: Claim Submission

The user submits:

* Member ID
* Claim Category
* Claimed Amount
* Treatment Date
* Supporting Documents

through the Streamlit interface.

---

## Step 2: Document Triage Agent

Purpose:

Identify document type and quality before processing.

Checks:

* Prescription
* Hospital Bill
* Pharmacy Bill
* Lab Report
* Unreadable Documents

Output:

```json
{
  "document_type": "PRESCRIPTION",
  "confidence": 0.95,
  "readable": true
}
```

This stage helps solve:

* Wrong document uploads
* Unreadable documents
* Misclassified files

---

## Step 3: Document Validation Agent

Validates uploaded documents against policy requirements.

Example:

CONSULTATION claims require:

* PRESCRIPTION
* HOSPITAL_BILL

If documents are missing:

```text
Missing Required Document:

Required:
HOSPITAL_BILL

Uploaded:
PRESCRIPTION
```

The pipeline stops immediately.

---

## Step 4: Information Extraction Agent

Purpose:

Convert unstructured medical documents into structured JSON.

Technology:

* OCR
* Groq
* Llama 3.3 70B Versatile

Extracted Fields:

* Patient Name
* Doctor Name
* Registration Number
* Diagnosis
* Treatment
* Date
* Amount
* Line Items

Example:

```json
{
  "patient_name": "Rajesh Kumar",
  "doctor_name": "Dr Arun Sharma",
  "diagnosis": "Viral Fever",
  "amount": 1500
}
```

---

## Step 5: Policy Engine

The policy engine applies all business rules from:

```text
policy_terms.json
```

No rules are hardcoded.

Checks include:

* Member validation
* Waiting periods
* Exclusions
* Coverage categories
* Pre-authorization requirements
* Network hospital discounts
* Co-pay calculations
* Category limits

Example:

```text
Waiting Period Check
Result: PASSED
```

---

## Step 6: Fraud Detection

Purpose:

Identify suspicious claim patterns.

Current Signals:

* Same day claims
* High frequency claims
* Unusual claim volume

Output:

```json
{
  "risk_score": 0.12,
  "signals": []
}
```

High risk claims are routed to:

```text
MANUAL_REVIEW
```

instead of automatic rejection.

---

## Step 7: Decision Engine

Produces one of:

```text
APPROVED
PARTIAL
REJECTED
MANUAL_REVIEW
```

Decision factors:

* Policy results
* Fraud score
* Extraction confidence
* System health

Output:

```json
{
  "decision": "APPROVED",
  "approved_amount": 1350
}
```

---

# Human-Centered Features

A major goal of the system is explainability.

The following features are designed specifically for claim reviewers.

---

## Claim Timeline

Every action is timestamped.

Example:

```text
14:02:01
Claim Received

14:02:03
Prescription Detected

14:02:04
Hospital Bill Detected

14:02:06
Policy Validation Passed

14:02:07
Decision Generated
```

This allows operations teams to understand the complete decision path.

---

## Reviewer Notes

Llama generates a concise explanation.

Example:

```text
The submitted diagnosis and treatment
appear clinically consistent.

All required documents were present.

No policy exclusions were triggered.

The claim amount falls within
approved category limits.
```

---

## Confidence Breakdown

Instead of showing only a final score:

```text
Confidence: 89%
```

the system provides a breakdown.

```text
Document Quality      95%
Extraction Quality    90%
Policy Validation    100%
Fraud Signals         -5%

Final Confidence      89%
```

---

## Degraded Mode

If a component fails:

* The pipeline continues
* Confidence is reduced
* Manual review is recommended

Example:

```text
Extractor Service Failed

Decision Generated Using
Available Information

Manual Review Recommended
```

This satisfies the graceful degradation requirement.

---

# Failure Handling Strategy

Every major component is wrapped in safe execution blocks.

Example:

```python
safe_execute(
    extract_information,
    "Extractor"
)
```

If a component fails:

1. Log the error
2. Continue processing
3. Reduce confidence
4. Surface failure in trace
5. Recommend manual review

The system never crashes due to a single component failure.

---

# Component Contracts

## Document Triage

Input:

```python
uploaded_files
```

Output:

```python
{
    "document_type": str,
    "confidence": float,
    "readable": bool
}
```

---

## Document Validation

Input:

```python
claim_category
documents
```

Output:

```python
{
    "valid": bool,
    "message": str
}
```

---

## Extraction Agent

Input:

```python
documents
```

Output:

```python
{
    "patient_name": str,
    "diagnosis": str,
    "doctor_name": str
}
```

---

## Policy Engine

Input:

```python
member
claim
documents
```

Output:

```python
{
    "approved": bool,
    "approved_amount": float,
    "reasons": list
}
```

---

## Fraud Detector

Input:

```python
member_id
```

Output:

```python
{
    "risk_score": float,
    "signals": list
}
```

---

## Decision Engine

Input:

```python
policy_result
fraud_result
confidence
```

Output:

```python
{
    "decision": str,
    "approved_amount": float,
    "confidence": float
}
```

---

# Why Groq + Llama 3.3 70B?

The assignment requires handling:

* Inconsistent document formats
* Medical terminology
* OCR noise
* Semi-structured data

Groq's Llama 3.3 70B Versatile was selected because it provides:

* Fast inference
* Strong structured JSON generation
* Low latency
* Reliable extraction performance

This makes it suitable for real-time claim processing workflows.

---

# Why Streamlit?

Streamlit was chosen because it allows rapid development of:

* File upload workflows
* Interactive dashboards
* Trace visualization
* Decision review interfaces

Benefits:

* Simple deployment
* Minimal frontend code
* Easy reviewer demonstration
* Fast iteration

---

# Running the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create:

```text
.env
```

```env
GROQ_API_KEY=your_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

# Running Test Cases

Execute:

```bash
python tests/test_runner.py
```

Example Output:

```text
TC001 PASS
TC002 PASS
TC003 PASS
TC004 PASS
...
```

Generated reports include:

* Actual Result
* Expected Result
* Match Status
* Trace Output

---

# Tradeoffs

### Chosen

* Deterministic pipeline
* Rule-based adjudication
* Configuration-driven policy engine
* Groq-based extraction

### Not Chosen

* Autonomous agent loops
* Complex graph orchestration
* Reinforcement-based workflows
* Dynamic planning systems

Reason:

The assignment prioritizes:

* Explainability
* Reliability
* Auditability

over autonomous behavior.

---

# Future Improvements

1. Vision-language extraction models
2. Real fraud scoring engine
3. PostgreSQL storage
4. Async processing
5. Human review dashboard
6. Feedback learning loop
7. Vector search for historical claims
8. Analytics dashboard
9. Production monitoring
10. Automated policy updates

---

# Conclusion

This solution implements a deterministic, explainable, and fault-tolerant claims processing pipeline using Streamlit and Groq Llama 3.3 70B.

The architecture emphasizes:

* Clear component boundaries
* Policy-driven decisions
* Human-readable explanations
* Robust failure handling
* Strong observability

The result is a maintainable system capable of automating insurance claim adjudication while preserving transparency and operational trust.
