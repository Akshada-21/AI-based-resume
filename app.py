import streamlit as st
from users import USERS
from resume_parser import extract_text_from_pdf
from skill_matcher import match_resume_with_jd
from database import store_result, get_all_results

# Set page config
st.set_page_config(page_title="Login | Resume Screening", layout="wide")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login - Resume Screening System")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email in USERS and USERS[email] == password:
            st.session_state.logged_in = True
            st.session_state.user = email
            st.success("Login successful!")
        else:
            st.error("Invalid email or password")

# ---------- Main ATS App ----------
def resume_screening():
    st.title("🧠 AI Resume Screening System")

    jd_file = st.file_uploader("📄 Upload Job Description (PDF)", type=["pdf"])

    if jd_file:
        jd_text = extract_text_from_pdf(jd_file)
        resume_files = st.file_uploader("Upload Resumes", type=["pdf"], accept_multiple_files=True)

        if resume_files:
            candidate_data = []
            for idx, resume_file in enumerate(resume_files):
                with st.expander(f"Resume: {resume_file.name}"):
                    name = st.text_input("Candidate Name", key=f"name_{idx}")
                    email = st.text_input("Candidate Email", key=f"email_{idx}")
                    candidate_data.append((resume_file, name, email))

            if st.button("🚀 Process All Resumes"):
                for resume_file, name, email in candidate_data:
                    if name.strip() == "" or email.strip() == "":
                        st.warning(f"Please enter both name and email for {resume_file.name}")
                        continue
                    resume_text = extract_text_from_pdf(resume_file)
                    score = match_resume_with_jd(resume_text, jd_text)
                    store_result(name, score, email, resume_file.name)
                    st.success(f"{name}'s resume matched with score: {score:.2f}%")
        else:
            st.info("Please upload at least one resume.")

        # Show results
        st.markdown("---")
        st.subheader("📊 ATS Screening Results")
        df = get_all_results()
        if df is not None and not df.empty:
            st.dataframe(df)
        else:
            st.info("No screening results yet.")
    else:
        st.warning("Please upload a Job Description file to start.")

# ---------- Run App ----------
if st.session_state.logged_in:
    resume_screening()
else:
    login()
