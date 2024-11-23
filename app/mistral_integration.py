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


##########################################################################################


!pip install mistralai pandas

import os
from mistralai import Mistral
import random

# Mistral API key and model
api_key = "wz0Op3zc13PBQ7NAswiJfpzWrdkBMhdF"  # Replace with your API key
model = "mistral-small-latest"

# Initialize Mistral client
client = Mistral(api_key=api_key)

# List of product names (already stored)
product_list = [
    "Smartphone", "Laptop", "Running Shoes", "Yoga Mat", "Bluetooth Speaker",
    "Coffee Maker", "T-shirt", "Smartwatch", "Electric Toothbrush"
]

# Function to interact with Mistral API and get a response
def chat_with_mistral(messages):
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    return chat_response.choices[0].message.content

# Function to dynamically gather information based on user responses
def gather_product_info():
    product_info = {}

    # Initialize the conversation with an introductory message
    conversation = [
        {"role": "system", "content": "You are a helpful assistant. Ask questions to understand the user's purchasing needs."},
        {"role": "user", "content": "Hello, I need help finding a product."}
    ]
    
    print("Chatbot: Let's start by understanding what you're looking for.")

    # Ask the first question: why the user wants to buy something
    first_question = "Why do you want to buy this product?"
    conversation.append({"role": "user", "content": first_question})
    print(f"Chatbot: {first_question}")
    product_info["why"] = input("You: ")  # User provides input here

    # Add the user's response to the conversation context
    conversation.append({"role": "user", "content": product_info["why"]})

    # Ask the second question dynamically
    while len(conversation) < 6:  # 3 user inputs means 6 conversation entries (system + 3 questions + 3 responses)
        # Get the next follow-up question from Mistral based on the current conversation
        bot_response = chat_with_mistral(conversation)
        print(f"Chatbot: {bot_response}")
        
        # Ask the user for input
        user_response = input("You: ")
        
        # Allow the user to exit the conversation if they type "stop" or "exit"
        if user_response.lower() in ["stop", "exit"]:
            print("Chatbot: Thank you for your responses! Ending the conversation.")
            break  # Exit the conversation
        
        # Add the user's response to the conversation context
        conversation.append({"role": "user", "content": user_response})
        
        # Store the user's answers in the appropriate product_info fields
        if "who" not in product_info:
            product_info["who"] = user_response
        elif "type_of_person" not in product_info:
            product_info["type_of_person"] = user_response
        elif "context" not in product_info:
            product_info["context"] = user_response

    # After gathering responses, ask Mistral to recommend a product
    print("\nChatbot: Based on your answers, I will now recommend the best product.")
    recommended_product = recommend_product_with_mistral(product_info, product_list)

    # Propose the recommended product
    print(f"\nChatbot: Based on your responses, I recommend the {recommended_product}.")
    print("Chatbot: Thank you for your time. Goodbye!")

# Function to ask Mistral to recommend the best product
def recommend_product_with_mistral(product_info, product_list):
    # Creating the prompt for Mistral to evaluate the best product
    products_string = ", ".join(product_list)
    user_info_string = f"User's answers: Why: {product_info.get('why', '')}, Who: {product_info.get('who', '')}, Context: {product_info.get('context', '')}"

    prompt = f"Given the following user information: {user_info_string}, and a list of products: {products_string}, which product would you recommend as the best fit for the user?"

    # Sending the prompt to Mistral AI
    conversation = [
        {"role": "system", "content": "You are a helpful assistant. Recommend the best product from the list based on user responses."},
        {"role": "user", "content": prompt}
    ]
    
    # Get the recommendation from Mistral
    response = chat_with_mistral(conversation)
    return response.strip()  # Clean the response from Mistral

# Start the conversation and gather product information
gather_product_info()