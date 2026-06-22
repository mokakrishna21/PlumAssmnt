import os
import tempfile
import json
import pytesseract
from PIL import Image
import pdfplumber
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EXTRACTION_PROMPT = """
You are a medical document parser. Extract the following fields from the text below.
Return a JSON object with these keys:
- patient_name (string or null)
- patient_age (string or null)
- patient_gender (string or null)
- treatment_date (date YYYY-MM-DD or null)
- doctor_name (string or null)
- doctor_registration (string or null)
- diagnosis (string or null)
- medicines (list of strings)
- tests_ordered (list of strings)
- hospital_name (string or null)
- bill_number (string or null)
- line_items (list of objects with 'description' and 'amount')
- total_amount (float or null)
- pharmacy_name (string or null)
- drug_license (string or null)
- lab_name (string or null)

Only return the JSON. If a field is missing, set it to null.
Text: {text}
"""

def extract_text_from_file(file_obj):
    ext = file_obj.name.split('.')[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{ext}') as tmp:
        tmp.write(file_obj.getvalue())
        tmp_path = tmp.name
    try:
        if ext in ['png', 'jpg', 'jpeg', 'bmp', 'tiff']:
            image = Image.open(tmp_path)
            text = pytesseract.image_to_string(image)
        elif ext == 'pdf':
            with pdfplumber.open(tmp_path) as pdf:
                text = ''.join(page.extract_text() or '' for page in pdf.pages)
        else:
            text = ''
    finally:
        os.unlink(tmp_path)
    return text

def extract_from_document(file_obj, trace):
    text = extract_text_from_file(file_obj)
    if not text.strip():
        trace.add(f"Extraction: No text found in {file_obj.name}")
        return {"fields": {}, "confidence": 0.2}

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(text=text[:6000])}],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        trace.add(f"Extraction: Success for {file_obj.name}")
        # Confidence based on presence of key fields
        confidence = 0.9 if data.get("patient_name") and data.get("diagnosis") else 0.6
        return {"fields": data, "confidence": confidence}
    except Exception as e:
        trace.add(f"Extraction failed for {file_obj.name}: {str(e)}")
        return {"fields": {}, "confidence": 0.2}