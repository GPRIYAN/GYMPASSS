import requests
import json

# Define your Groq API key
API_KEY = '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'

# Groq API URL
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq_api(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Define the data payload
    data = {
        "model": "llama3-8b-8192",  # Or use the model you prefer
        "messages": [{"role": "user", "content": query}],
    }
    
    try:
        # Send POST request to Groq API
        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))
        
        # Check the response status code and log it
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed with status code: {response.status_code}, {response.text}"}
    except requests.exceptions.RequestException as e:
        # Handle error in case of request failure
        return {"error": str(e)}

