import streamlit as st
from config import POLICY
from services.claim_processor import process_claim

st.set_page_config(page_title="Plum Claims Processing", layout="wide")
st.title("🏥 Health Insurance Claims Processing")

# Sidebar: member selection
members = {m['member_id']: m['name'] for m in POLICY.get('members', [])}
member_id = st.sidebar.selectbox("Select Member", options=list(members.keys()), format_func=lambda x: f"{x} - {members[x]}")

# Claim details
claim_category = st.sidebar.selectbox("Claim Category", options=list(POLICY.get('document_requirements', {}).keys()))
treatment_date = st.sidebar.date_input("Treatment Date")
claimed_amount = st.sidebar.number_input("Claimed Amount (₹)", min_value=0, value=1000, step=100)

# File upload with type selection
uploaded_files = st.file_uploader("Upload Medical Documents", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'pdf'])

uploaded_with_types = []
if uploaded_files:
    st.subheader("Specify Document Types")
    for file in uploaded_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(file.name)
        with col2:
            doc_type = st.selectbox(
                "Type",
                options=["PRESCRIPTION", "HOSPITAL_BILL", "PHARMACY_BILL", "LAB_REPORT"],
                key=f"type_{file.name}"
            )
            uploaded_with_types.append({"file": file, "doc_type": doc_type})

if st.button("Process Claim"):
    if not member_id or not claim_category or not uploaded_files:
        st.error("Please fill all fields and upload at least one document.")
    else:
        with st.spinner("Processing claim..."):
            result = process_claim(member_id, claim_category, claimed_amount, uploaded_with_types)

            st.subheader("Decision")
            col1, col2, col3 = st.columns(3)
            col1.metric("Decision", result["decision"])
            col2.metric("Approved Amount", f"₹{result['approved_amount']:,.2f}")
            col3.metric("Confidence", f"{result['confidence']*100:.0f}%")

            st.write("**Review Notes:**", result.get("review_notes", ""))

            with st.expander("Full Trace (Explainability)"):
                st.json(result["trace"])