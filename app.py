import streamlit as st
from resume_processor import extract_text_from_resume
from apikey import analyze_resume
import time
import plotly.express as px

# Streamlit Page Config
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton > button {border-radius: 8px; font-size: 16px;}
    .stTextArea textarea {font-size: 14px;}
    </style>
""", unsafe_allow_html=True)

# Page Title with emoji
st.title("🚀 AI-Powered Resume Analyzer")

# Sidebar for Job Description Input
with st.sidebar:
    st.header("📝 Job Description")
    job_description = st.text_area("Paste the job description here:", height=200)

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload Your Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    with st.spinner("🔍 Extracting text..."):
        time.sleep(1)  # Simulate loading
        resume_text = extract_text_from_resume(uploaded_file)

    if resume_text:
        st.subheader("📄 Extracted Resume Content")
        st.text_area("", resume_text, height=200)

        # Analyzing Resume
        with st.spinner("🤖 Analyzing your resume..."):
            time.sleep(2)  # Simulate processing
            analysis_result = analyze_resume(resume_text, job_description)

        if analysis_result:
            st.markdown("## 📊 AI-Powered Resume Insights")

            # Strengths & Weaknesses in Columns
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Strengths")
                st.success(analysis_result["upsides"])

            with col2:
                st.markdown("### ❌ Weaknesses")
                st.error(analysis_result["downsides"])

            # Resume Rating as a Progress Bar
            rating = int(analysis_result["power_rating"].replace('%', ''))
            st.subheader(f"📈 Resume Power Rating: {rating}/100")
            st.progress(rating / 100)

            # Improvements Section
            with st.expander("💡 Click to see Improvements Based on Job Description"):
                st.markdown(analysis_result["improvements"])

            # Interactive Skill Matching Chart
            skill_labels = ["Technical Skills", "Experience", "Projects", "Soft Skills", "Formatting"]
            skill_values = [rating - 10, rating - 15, rating, rating - 5, rating - 20]

            fig = px.bar(x=skill_labels, y=skill_values, labels={'x': 'Resume Factors', 'y': 'Score'},
                         title="🔎 Resume Factor Analysis", color=skill_values, text=skill_values)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
