import requests
import os


# DeepSeek API Endpoint
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Load API key from environment variable (if required)
# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # If DeepSeek requires an API key
DEEPSEEK_API_KEY = 'sk-b828b961ee2d4d6e950a6ebf9f327743' 

def ask_chatgpt(health_plan, diagnosis, procedure, guidelines, source_text, source_pages):
    """Generates an AI response that helps medical staff efficiently file a Prior Authorization request."""

    prompt = f"""
    You are a clinical prior authorization (PA) expert specializing in payer guidelines. Your role is to assist medical staff in submitting accurate and compliant Prior Authorization requests based on evidence-based medical policies.

    ### **1) Medical Necessity & Clinical Validity Check**  
    - Determine if the requested procedure **medically aligns** with the given diagnosis.  
    - If **not clinically appropriate**, state:  
    - "The procedure '{procedure}' is not typically indicated for '{diagnosis}' under standard medical guidelines."  
    - Suggest a **more appropriate diagnostic test or procedure** based on clinical best practices.  
    - **Do NOT** provide prior authorization details for invalid requests.

    ### **2) Prior Authorization (PA) Requirements for {health_plan}**  
    - **Is Prior Authorization (PA) required?** (Yes/No)  
    - If Prior Authorization is required, provide a **detailed list** of approval conditions:  
    - **Medical necessity criteria:** Required clinical justifications for Prior Authorization approval.  
    - **Supporting documentation:** List of required clinical notes (e.g., history of conservative treatments, imaging findings, referrals).  
    - **Imaging/test requirements:** If a prior test (X-ray, CT, etc.) is needed before MRI approval.  
    - **Referral or specialist requirement:** If approval requires a specialist review or referral.  

    ### **3) Submission Guidelines**  
    - Where and how to submit the Prior Authorization request for {health_plan}.  
    - Include payer-specific submission methods (e.g., **electronic portal, fax, or phone**).  
    - Expected processing times and **any follow-up actions required**.

    ### **4) Common Prior Authorization Denial Reasons & How to Avoid Them**  
    - List the most frequent **denial reasons** for this procedure-diagnosis combination.  
    - Provide **actionable steps** to prevent these denials.

    ### **5) Appeal Process for Denied Prior Authorization Requests**  
    If the Prior Authorization is denied:  
    - How to submit an **appeal**.  
    - What **additional documentation** strengthens the appeal.  
    - Contact methods for **payer reconsideration or peer-to-peer review**.  

    ### **6) Relevant Source Information from {health_plan}**  
    To ensure accuracy, the following information is sourced from the official guidelines:  
    - **Page(s):** {', '.join(map(str, source_pages))}  
    # - **Extracted Text from Source Document:**  
    # "{source_text}"

    ### **Case Details**
    - **Health Plan:** {health_plan}  
    - **Diagnosis:** {diagnosis}  
    - **Procedure:** {procedure}  

    ### **Response Guidelines**
    - Provide a structured, **professional, and easy-to-read** response.  
    - Ensure the response is **actionable** for medical staff submitting the PA.  
    - **Do NOT fabricate information**—only use the extracted guideline data.

    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a healthcare prior authorization expert. Always follow medical guidelines."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"