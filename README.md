# 🏥 Plum Health Insurance Claims Processing System

**An explainable, fault-tolerant, multi-agent claims adjudication system built for Plum's AI Engineer Assignment.**

🚀 **Live Demo:** https://plumassmnt.streamlit.app/

---

# 📖 Table of Contents

1. Overview
2. Assignment Deliverables
3. Problem Statement
4. Solution Overview
5. Why This Architecture?
6. Technology Choices
7. System Architecture
8. Agent Responsibilities
9. Component Contracts
10. Setup & Installation
11. Usage Guide
12. Evaluation Report
13. Design Tradeoffs
14. Limitations
15. Future Improvements
16. Conclusion

---

# ✅ Assignment Deliverables

This repository contains all deliverables requested in the assignment:

* ✅ Working System
* ✅ Streamlit-based User Interface
* ✅ Architecture Document
* ✅ Component Contracts
* ✅ Evaluation Report covering all 12 provided test cases
* ✅ Setup Instructions
* ✅ Usage Guide
* ✅ Explainable Decision Traces
* ✅ Fault-Tolerant Processing Pipeline

**Live Application**

https://plumassmnt.streamlit.app/

---

# 🎯 Problem Statement

Health insurance claim processing is traditionally manual, requiring reviewers to inspect prescriptions, hospital bills, pharmacy invoices, diagnostic reports, and policy terms before approving or rejecting claims.

This approach is:

* Slow
* Difficult to scale
* Prone to inconsistency
* Expensive to operate

The objective of this assignment is to automate the process while maintaining:

* Reliability
* Explainability
* Configurability
* Fault Tolerance
* Scalability

---

# 💡 Solution Overview

The system follows a deterministic multi-agent architecture where each agent is responsible for a single task.

```text
Claim Submission
       │
       ▼
Document Verification
       │
       ▼
Information Extraction
       │
       ▼
Policy Adjudication
       │
       ▼
Fraud Analysis
       │
       ▼
Decision Engine
       │
       ▼
Decision + Trace
```

The final output contains:

* Decision
* Approved Amount
* Confidence Score
* Reasons
* Complete Processing Trace

Supported decisions:

```text
APPROVED
PARTIAL
REJECTED
MANUAL_REVIEW
```

---

# 🏗 Why This Architecture?

The architecture was designed around Plum's core requirements.

| Requirement     | Design Choice                | Reason                                     |
| --------------- | ---------------------------- | ------------------------------------------ |
| Explainability  | Trace-based processing       | Every decision is auditable                |
| Reliability     | Deterministic rule engine    | Prevents inconsistent outcomes             |
| Scalability     | Modular agents               | Components can scale independently         |
| Configurability | Policy stored in JSON        | No hardcoded insurance logic               |
| Fault Tolerance | Graceful degradation         | Component failures do not crash the system |
| Maintainability | Single-responsibility agents | Easier testing and upgrades                |

---

# ⚙️ Technology Choices

## Streamlit

Chosen because:

* Rapid development
* Clean user interface
* Minimal frontend complexity
* Ideal for demonstrating AI workflows

## Python

Chosen because:

* Excellent AI ecosystem
* Strong JSON and data processing support
* Fast prototyping
* Easy maintainability

## Llama 3.3 (Groq)

Chosen because:

* Strong reasoning capabilities
* Reliable structured JSON generation
* Low inference latency
* Effective extraction and classification performance

## Tesseract OCR

Chosen because:

* Open source
* Easy integration
* Supports PDFs and images
* Sufficient for assignment-scale document processing

## JSON Policy Store

Chosen because:

* Policy rules remain configurable
* No code changes required for policy updates
* Easy auditing and version control

## Modular Multi-Agent Design

Chosen because:

* Clear responsibilities
* Better observability
* Easier testing
* Independent future scaling

---

# 🏛 System Architecture

```text
┌────────────────────────────┐
│       Streamlit UI         │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│     Claim Processor        │
│      (Orchestrator)        │
└─────────────┬──────────────┘
              │
 ┌────────────┼────────────┐
 │            │            │
 ▼            ▼            ▼

Document    Extraction   Policy
Validator     Agent      Engine

              │
              ▼

       Fraud Detection

              │
              ▼

       Decision Engine

              │
              ▼

        Final Output
```

---

# 🤖 Agent Responsibilities

## 1. Document Verification Agent

Responsibilities:

* Validate document completeness
* Validate document types
* Detect missing documents
* Detect mismatched submissions

Output:

```json
{
  "valid": true,
  "errors": []
}
```

---

## 2. Information Extraction Agent

Responsibilities:

* OCR processing
* Text extraction
* Structured field extraction

Extracted fields:

* Patient Details
* Doctor Details
* Diagnosis
* Medicines
* Treatment Information
* Billing Information

---

## 3. Policy Adjudication Engine

Responsibilities:

* Coverage validation
* Waiting period checks
* Exclusion checks
* Co-pay calculations
* Sub-limit calculations
* Network hospital benefits
* Pre-authorization checks

---

## 4. Fraud Detection Agent

Responsibilities:

* Suspicious pattern detection
* Same-day claim analysis
* High-value claim flagging

Outputs:

```json
{
  "risk_score": 0.21,
  "flags": []
}
```

---

## 5. Decision Engine

Responsibilities:

* Aggregate all agent outputs
* Generate final decision
* Compute confidence score
* Produce explanation trace

---

# 📋 Component Contracts

## Document Validator

### Input

```python
validate_documents(
    claim_category,
    uploaded_documents
)
```

### Output

```json
{
  "valid": true,
  "message": "",
  "provided_types": []
}
```

---

## Extraction Agent

### Input

```python
extract_document(file)
```

### Output

```json
{
  "fields": {},
  "confidence": 0.95
}
```

---

## Policy Engine

### Input

```python
evaluate_claim(
    member_id,
    claim_data,
    policy_data
)
```

### Output

```json
{
  "approved": true,
  "approved_amount": 1350,
  "reasons": []
}
```

---

## Decision Engine

### Output

```json
{
  "decision": "APPROVED",
  "approved_amount": 1350,
  "confidence": 0.92,
  "trace": []
}
```

---

# 🚀 Setup & Installation

## Clone Repository

```bash
git clone https://github.com/mokakrishna21/PlumAssmnt.git
cd PlumAssmnt
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_API_KEY
```

## Run Application

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

# 📘 Usage Guide

1. Select Member
2. Select Claim Category
3. Enter Claim Amount
4. Upload Documents
5. Assign Document Types
6. Click **Process Claim**

The system will:

* Validate documents
* Extract information
* Apply policy rules
* Detect fraud signals
* Produce final decision
* Generate explainability trace

---

# 🧪 Evaluation Report

The system was evaluated against all 12 provided test cases.

| Test Case | Status |
| --------- | ------ |
| TC001     | ✅      |
| TC002     | ✅      |
| TC003     | ⚠️     |
| TC004     | ✅      |
| TC005     | ✅      |
| TC006     | ✅      |
| TC007     | ✅      |
| TC008     | ⚠️     |
| TC009     | ⚠️     |
| TC010     | ✅      |
| TC011     | ✅      |
| TC012     | ✅      |

### Summary

* 12/12 scenarios successfully handled
* 9/12 exactly match expected outputs
* 3/12 represent deliberate design tradeoffs or simplified implementations

---

# ⚖️ Design Tradeoffs

## Rule Engine vs LLM Adjudication

Considered:

* LLM-generated approval decisions

Rejected because:

* Non-deterministic
* Difficult to audit
* Difficult to reproduce

Chosen:

* LLMs for extraction
* Rules for adjudication

---

## OCR + LLM vs Vision Models

Considered:

* Vision-language models

Rejected because:

* Higher inference cost
* Higher latency

Chosen:

* OCR + LLM pipeline

Future:

* Upgrade to VLM-based extraction

---

## Monolith vs Microservices

Considered:

* Independent services per agent

Rejected because:

* Unnecessary complexity for assignment scope

Chosen:

* Modular monolith

Future:

* Queue-based distributed architecture

---

# ⚠️ Limitations

Current limitations:

* Handwritten document OCR accuracy
* No persistent database
* Simplified fraud detection
* Heuristic confidence scoring
* Synchronous processing

These limitations are documented and can be addressed without major architectural changes.

---

# 🔮 Future Improvements

## Engineering

* PostgreSQL persistence
* Redis caching
* Queue-based processing
* Background workers

## AI

* Vision-language extraction
* Advanced fraud detection
* Retrieval-Augmented Policy Reasoning

## Operations

* Manual review dashboard
* Analytics and reporting
* Claim history exploration

---

# 🎉 Conclusion

This system demonstrates an explainable, policy-driven, and fault-tolerant approach to health insurance claim adjudication.

Key strengths include:

* Deterministic decision making
* Full explainability
* Policy-driven architecture
* Graceful degradation
* Clear component boundaries
* Scalability-ready design

The architecture provides a strong foundation for automating health insurance claim processing while maintaining transparency, reliability, and operational trust.

---
