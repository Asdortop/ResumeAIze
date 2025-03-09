import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Set up Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Error: GEMINI_API_KEY not found. Make sure it's set in .env (local) or GitHub Secrets (deployment).")

genai.configure(api_key=api_key)

def analyze_resume(resume_text, job_description):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    # Well-structured prompt for a clean response
    prompt = f"""
    You are an AI Resume Analyzer. Given a resume and job description, analyze and return a structured response.

    **Resume Analysis:**
    1. **Strengths**: List key strengths in bullet points.
    2. **Weaknesses**: List weaknesses in bullet points.
    3. **Resume Power Rating**: Give a score out of 100%.
    4. **Improvements Based on Job Description**: List resume changes required to align better with the job description.

    **Resume Text:**  
    {resume_text}  

    **Job Description:**  
    {job_description}  

    **Format Response Strictly as Below (Ensure Newlines for Formatting)**  
    - Strengths:  
      - Bullet 1  
      - Bullet 2  
      - Bullet 3  

    - Weaknesses:  
      - Bullet 1  
      - Bullet 2  
      - Bullet 3  

    - Resume Power Rating: XX%    

    - Improvements Based on Job Description:  
      - Bullet 1  
      - Bullet 2  
      - Bullet 3  
    """

    response = model.generate_content(prompt)

    if response and response.text:
        try:
            data = response.text.split("\n\n")
            return {
                "upsides": "\n".join(data[0].split("\n")[1:]).strip(),  # Extract bullet points correctly
                "downsides": "\n".join(data[1].split("\n")[1:]).strip(),
                "power_rating": data[2].split(":")[1].strip(),
                "improvements": "\n".join(data[3].split("\n")[1:]).strip()
            }
        except:
            return {
                "upsides": "N/A", 
                "downsides": "N/A", 
                "power_rating": "N/A", 
                "improvements": "N/A"
            }
    return None
