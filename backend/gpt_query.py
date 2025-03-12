import requests
import os


# DeepSeek API Endpoint
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Load API key from environment variable (if required)
# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # If DeepSeek requires an API key
DEEPSEEK_API_KEY = 'sk-b828b961ee2d4d6e950a6ebf9f327743' 

def ask_chatgpt(health_plan, diagnosis, procedure, guidelines):
    prompt = f"""
    You are a prior authorization expert reviewing payer guidelines. Your task is to determine:
    
    **1) Eligibility Check:** Does the procedure "{procedure}" for the diagnosis "{diagnosis}" under the health plan "{health_plan}" require prior authorization?
    **2) PA Requirements:** If prior authorization is required, what are the conditions to get it approved?
    **3) Best Way to File PA:** Provide expert recommendations to maximize approval chances.

    **Guidelines to Check:**
    {guidelines}
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a healthcare prior authorization expert."},
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
