# 🏥 Plum Health Insurance Claims Processing System

**An explainable, policy-driven, fault-tolerant claims adjudication system built for Plum's AI Engineer Assignment.**

🚀 **Live Demo:** https://plumassmnt.streamlit.app/

---

# Overview

This project automates health insurance claim processing by validating submitted documents, extracting structured medical information, applying policy rules, detecting fraud signals, and producing transparent claim decisions.

The system is designed around five key principles:

* Explainability
* Determinism
* Reliability
* Configurability
* Scalability

Supported decisions:

```text
APPROVED
PARTIAL
REJECTED
MANUAL_REVIEW
```

Every decision includes:

* Approved amount
* Confidence score
* Decision rationale
* Full processing trace

---

# Assignment Deliverables

This repository contains all requested deliverables:

| Deliverable           | Status |
| --------------------- | ------ |
| Working System        | ✅      |
| Architecture Document | ✅      |
| Component Contracts   | ✅      |
| Evaluation Report     | ✅      |
| Setup Instructions    | ✅      |
| Explainable Traces    | ✅      |

---

# Live Application

### Deployed URL

```text
https://plumassmnt.streamlit.app/
```

---

# Repository Documentation

## Architecture Document

Detailed architecture rationale, component interactions, scaling strategy, and design decisions:

```text
docs/architecture.md
```

## Component Contracts

Formal interfaces for every major component including inputs, outputs, and failure behaviour:

```text
docs/component_contracts.md
```

## Evaluation Report

Results for all 12 provided test cases including outcomes, traces, and tradeoffs:

```text
docs/eval_report_full.md
```

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

# Technology Choices

| Technology                 | Why It Was Chosen                                     |
| -------------------------- | ----------------------------------------------------- |
| Python                     | Fast development, strong AI ecosystem                 |
| Streamlit                  | Rapid UI development with minimal frontend complexity |
| Groq + Llama 3             | Fast inference and strong structured extraction       |
| Tesseract OCR              | Open-source OCR for image-based documents             |
| JSON Policy Store          | Dynamic policy configuration without code changes     |
| Modular Agent Architecture | Better observability, testing, and scalability        |

---

# Key Features

### Document Verification

* Missing document detection
* Wrong document detection
* Unreadable document handling
* Validation before processing

### Information Extraction

* Prescriptions
* Hospital bills
* Pharmacy bills
* Diagnostic reports

### Policy Adjudication

* Waiting periods
* Coverage validation
* Exclusions
* Co-pay calculations
* Network hospital discounts
* Pre-authorization checks

### Explainability

Every decision includes a complete trace showing:

* What was checked
* What passed
* What failed
* Why the final decision was reached

### Fault Tolerance

The pipeline gracefully handles:

* OCR failures
* LLM failures
* Parsing errors
* Missing fields

without crashing the system.

---

# Setup

Clone the repository:

```bash
git clone https://github.com/mokakrishna21/PlumAssmnt.git
cd PlumAssmnt
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
GROQ_API_KEY=YOUR_API_KEY
```

Run the application:

```bash
streamlit run app.py
```

---

# Evaluation Summary

The system was evaluated against all 12 provided test cases.

| Metric                      | Result |
| --------------------------- | ------ |
| Total Test Cases            | 12     |
| Exact Matches               | 9      |
| Tradeoffs / Partial Matches | 3      |
| System Crashes              | 0      |

See:

```text
docs/eval_report_full.md
```

for complete traces and analysis.

---

# Design Philosophy

A key design decision was separating:

```text
LLMs → Information Extraction

Rules → Claim Decisions
```

This provides:

* Deterministic outcomes
* Better explainability
* Easier auditing
* Greater operational trust

---

