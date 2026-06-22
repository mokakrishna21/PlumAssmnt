# Plum Health Insurance Claims Processing System

## Setup
1. Place `policy_terms.json` and `test_cases.json` inside `config/`.
2. Install dependencies: `pip install -r requirements.txt`
3. Install Tesseract OCR (system‑level):
   - Ubuntu: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`
   - Windows: download from GitHub and add to PATH.
4. Create `.env` from `.env.example` and set your `GROQ_API_KEY`.
5. Run: `streamlit run app.py`

## Usage
- Select a member from the sidebar.
- Choose claim category.
- Enter treatment date and claimed amount.
- Upload one or more documents. **You must also select the correct document type** for each file from the dropdown (PRESCRIPTION, HOSPITAL_BILL, etc.).
- Click "Process Claim".

## Architecture
- **Deterministic pipeline** with clear component boundaries.
- **User‑provided doc types** eliminate misclassification.
- **OCR + Llama 3.3‑70B** extract structured information.
- **Policy engine** enforces rules with fatal/non‑fatal distinction.
- **Full trace** for every decision (observability).
- **Graceful degradation** on failures.
