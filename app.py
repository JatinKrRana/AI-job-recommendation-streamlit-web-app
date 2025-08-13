# app.py
import os
import streamlit as st
from dotenv import load_dotenv

# Load env (helpful even though src modules also load .env)
load_dotenv()

# Import your modules (make sure src/ is a package or in PYTHONPATH)
from src.job_scraper import get_google_jobs
from src.resume_parser import extract_text_from_pdf, extract_text_from_docx
from src.recommender import get_recommendations

# ---------- Page config & simple styling ----------
st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="💼",
    layout="wide"
)

# Simple CSS to make UI colorful and pleasant
st.markdown(
    """
    <style>
    .app-header {background: linear-gradient(90deg, #4f46e5, #06b6d4); padding:18px; border-radius:10px;}
    .job-card { background: linear-gradient(180deg, #ffffff, #f8fafc); border-radius:12px; padding:14px; box-shadow: 0 4px 10px rgba(2,6,23,0.08); }
    .job-title { font-size:18px; font-weight:700; color:#0f172a; }
    .company { font-weight:600; color:#334155; }
    .meta { color:#475569; font-size:13px; }
    .apply-link { color:#064e3b; font-weight:600; text-decoration: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-header"><h1 style="color:white;margin:0">💼 AI-Powered Job Recommendation System</h1></div>', unsafe_allow_html=True)
st.write("Enter your skills or upload a resume — the app will fetch jobs and the AI will recommend the best matches.")

# ---------- Sidebar: controls ----------
with st.sidebar:
    st.header("Search settings")
    default_q = "Data Analyst"
    job_query = st.text_input("Job title / keywords", value=default_q)
    location = st.text_input("Location", value="India")
    job_type = st.selectbox("Job type (optional)", ["", "Internship", "Full-time", "Part-time", "Contract", "Remote"])
    max_jobs = st.slider("Max jobs to fetch (for AI input)", min_value=3, max_value=25, value=10)
    max_recs = st.slider("Number of AI recommendations", min_value=1, max_value=10, value=5)
    show_raw = st.checkbox("Show raw job JSON (debug)", value=False)

# ---------- Main UI: profile input ----------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Profile input")
    input_mode = st.radio("How do you want to provide your profile?", ["Manual text", "Upload resume (PDF/DOCX)"])
    if input_mode == "Manual text":
        skills_text = st.text_area("Paste your skills / summary / experience (comma-separated is fine)", height=140,
                                   placeholder="e.g., Python, SQL, Excel, Tableau, data analysis, internships")
    else:
        uploaded_file = st.file_uploader("Upload resume", type=["pdf", "docx"])
        skills_text = ""
        if uploaded_file is not None:
            # Save/Streamlit file-like works with pdfplumber/docx.Document directly
            if uploaded_file.name.lower().endswith(".pdf"):
                try:
                    skills_text = extract_text_from_pdf(uploaded_file)
                except Exception as e:
                    st.error(f"Failed to parse PDF: {e}")
            else:
                try:
                    skills_text = extract_text_from_docx(uploaded_file)
                except Exception as e:
                    st.error(f"Failed to parse DOCX: {e}")

            if skills_text:
                st.success("Resume parsed — text extracted.")
                with st.expander("Preview extracted text (first 800 chars)"):
                    st.write(skills_text[:800] + ("..." if len(skills_text) > 800 else ""))

# ---------- Search & Recommend ----------
if st.button("🔎 Fetch jobs & Get AI recommendations"):
    if not job_query.strip():
        st.error("Please enter a job title or keywords in the sidebar.")
    else:
        with st.spinner("Fetching jobs from Google Jobs (SerpAPI)..."):
            try:
                # Call scraper (job_scraper handles using SERPAPI_KEY from .env)
                raw_jobs = get_google_jobs(job_query, location, job_type if job_type else None) or []
            except Exception as e:
                st.error(f"Job scraping failed: {e}")
                raw_jobs = []

        if not raw_jobs:
            st.warning("No jobs returned by the scraper. Try broader keywords or check your SerpAPI key/quota.")
        else:
            st.success(f"Fetched {len(raw_jobs)} jobs. Showing up to {max_jobs} for AI ranking.")
            # Optionally show raw JSON
            if show_raw:
                st.subheader("Raw job results (first 5)")
                st.write(raw_jobs[:5])

            # Display jobs in a grid - first show simple cards
            st.subheader("Jobs (top results)")
            display_jobs = raw_jobs[: max_jobs ]
            cols = st.columns(2)
            for i, job in enumerate(display_jobs):
                col = cols[i % 2]
                with col:
                    st.markdown('<div class="job-card">', unsafe_allow_html=True)
                    title = job.get("title") or job.get("position") or "No title"
                    company = job.get("company_name") or job.get("company") or "N/A"
                    location_text = job.get("location") or "N/A"
                    description = job.get("description") or job.get("snippet") or ""
                    link = job.get("link") or job.get("apply_link") or "#"

                    st.markdown(f'<div class="job-title">{i+1}. {title}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="company">🏢 {company}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="meta">📍 {location_text}</div>', unsafe_allow_html=True)
                    if description:
                        st.write(description[:300] + ("..." if len(description) > 300 else ""))
                    st.markdown(f'<a class="apply-link" href="{link}" target="_blank">🔗 View / Apply</a>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            # ---------- Call the recommender (LLM) ----------
            st.markdown("---")
            st.subheader("AI Recommendations")
            if not skills_text or not skills_text.strip():
                st.warning("No skills/profile text provided. AI recommendations will be generic. Provide skills or upload resume for personalised results.")
                # optionally set skills_text to job_query if empty:
                skills_text = job_query

            # Prepare job slice to send to model (simple, textual)
            # Build simplified job list so prompt is smaller
            model_jobs = []
            for job in display_jobs:
                title = job.get("title") or job.get("position") or "No title"
                company = job.get("company_name") or job.get("company") or ""
                loc = job.get("location") or ""
                snippet = (job.get("description") or job.get("snippet") or "")[:400]
                model_jobs.append({"title": title, "company_name": company, "location": loc, "snippet": snippet})

            # Call the LLM and display recommendations
            try:
                with st.spinner("Asking the AI to rank and explain the best matches... (this may take a few seconds)"):
                    ai_response = get_recommendations(skills=skills_text, jobs=model_jobs)
                st.markdown("**AI output:**")
                # get_recommendations returns raw text (per your recommender). Show it nicely.
                st.write(ai_response)
            except Exception as e:
                st.error(f"AI recommendation failed: {e}")
