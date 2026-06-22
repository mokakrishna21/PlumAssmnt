# Plum Claims Processing System

A multi‑agent, AI‑powered health insurance claims adjudication pipeline built with **Streamlit** and **Groq Llama 3.3‑70B**.

---

## Quick Overview

- **Validates** uploaded documents (type + completeness) with specific error messages.
- **Extracts** structured data from prescriptions, bills, lab reports (OCR + LLM).
- **Applies** policy rules (waiting periods, exclusions, limits, co‑pays, network discounts).
- **Decides** `APPROVED` / `PARTIAL` / `REJECTED` / `MANUAL_REVIEW` with amount, reason, and confidence.
- **Full trace** – every step is logged for full explainability.
- **Graceful degradation** – component failures lower confidence but never crash the system.

---

## Tech Stack

- **UI**: Streamlit
- **LLM**: Groq Llama 3.3‑70B (structured JSON extraction)
- **OCR**: Tesseract
- **PDF parsing**: pdfplumber
- **Policy data**: JSON configuration (`policy_terms.json`)

---

## Installation (5 minutes)

```bash
# 1. Clone / unzip the project
cd claims_system

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Tesseract (system level)
# Ubuntu: sudo apt install tesseract-ocr
# macOS: brew install tesseract
# Windows: download from GitHub and add to PATH

# 4. Set your Groq API key in .env
echo "GROQ_API_KEY=your_key_here" > .env

# 5. Place policy_terms.json and test_cases.json in config/
cp /path/to/policy_terms.json config/
cp /path/to/test_cases.json config/

# 6. Run
streamlit run app.py
