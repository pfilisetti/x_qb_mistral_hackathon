import requests
import os
from dotenv import load_dotenv

# Load environment variables (e.g., API keys)
load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")  # Store this key in a `.env` file
MISTRAL_API_URL = "https://api.mistral.ai/v1/completions"  # Replace with actual endpoint

def call_mistral_api(prompt, max_tokens=200, temperature=0.7):
    """
    Sends a prompt to the Mistral API and retrieves the response.
    
    Args:
        prompt (str): The input prompt for the LLM.
        max_tokens (int): Maximum number of tokens to generate.
        temperature (float): Sampling temperature (higher = more creative).

    Returns:
        str: The response text from the LLM.
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-7b",  # Update with the specific model name
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("choices", [{}])[0].get("text", "").strip()  # Adjust based on API response format
    except requests.exceptions.RequestException as e:
        print(f"Error calling Mistral API: {e}")
        return "I'm sorry, I couldn't process your request at the moment."

# Example usage
if __name__ == "__main__":
    test_prompt = "Suggest a gift for a tech enthusiast with a budget of 100-150€."
    print(call_mistral_api(test_prompt))