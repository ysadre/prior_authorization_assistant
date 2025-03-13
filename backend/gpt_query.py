import requests
import os


# DeepSeek API Endpoint
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Load API key from environment variable (if required)
# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # If DeepSeek requires an API key
DEEPSEEK_API_KEY = 'sk-b828b961ee2d4d6e950a6ebf9f327743' 

def ask_chatgpt(health_plan, diagnosis, procedure, guidelines, source_text, source_pages):
    """Generates an AI response that helps medical staff efficiently file a PA request."""

    prompt = f"""
    You are a clinical prior authorization expert, specialized in medical guidelines for healthcare payers. 
    Your role is to assist medical staff in ensuring that PA requests are submitted correctly and efficiently.

    **Medical Necessity Check:**  
    If the requested procedure does not align with the diagnosis, state:  
    - "The procedure '{procedure}' is not typically recommended for '{diagnosis}'."  
    - Suggest a more appropriate test based on clinical best practices.  
    - Do not provide PA details for invalid requests.

    **Prior Authorization Requirements:**  
    If the procedure is appropriate for the diagnosis, determine if prior authorization is required under {health_plan}.  
    If PA is required, provide the necessary documentation including:  
    - Medical necessity criteria  
    - Required clinical notes (e.g., failed conservative treatments, physical exam findings)  
    - Imaging or test reports needed for approval  
    - Referral requirements  

    **Submission Guidelines:**  
    - Clearly explain where and how to submit the PA request.  
    - Provide payer-specific submission methods (e.g., portal, fax, or email).  
    - Indicate expected processing times and follow-up actions.  

    **Avoiding PA Denials:**  
    - List the most common denial reasons for this procedure-diagnosis combination.  
    - Provide specific ways to avoid these errors when submitting the request.  

    **Appeal Process for Denied Requests:**  
    If PA is denied, outline the next steps:  
    - How to submit an appeal  
    - What additional documentation is needed  
    - Where to send the appeal request  

    **Relevant Source Information:**  
    - Extracted from the official payer guidelines:  
      - **Page(s):** {', '.join(map(str, source_pages))}  
      - **Text from source document:**  
        "{source_text}"  

    **Health Plan:** {health_plan}  
    **Diagnosis:** {diagnosis}  
    **Procedure:** {procedure}  

    Provide a structured, professional response that is easy for medical staff to follow.
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