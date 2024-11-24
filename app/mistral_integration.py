
# %%
import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables (e.g., API keys)
load_dotenv(dotenv_path=".env")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-small-latest"

print(f"Loaded API key: {MISTRAL_API_KEY[:5]}****")  # Partial key for security

# %%

# Initialize the Mistral client
client = Mistral(api_key=MISTRAL_API_KEY)

def chat_with_mistral(messages):
    """
    Sends a conversation history to Mistral and retrieves the next response.

    Args:
        messages (list): A list of messages in the format [{"role": "user/system", "content": "message"}].

    Returns:
        str: The response text from the Mistral LLM.
    """
    try:
        chat_response = client.chat.complete(model=MODEL, messages=messages)
        return chat_response.choices[0].message.content
    except Exception as e:
        print(f"Error interacting with Mistral API: {e}")
        return "Sorry, I couldn't process your request."

def gather_product_info():
    """
    Gathers user input interactively through a chatbot conversation to understand user preferences.

    Returns:
        dict: A dictionary containing the collected product information.
    """
    product_info = {}
    conversation = [
        {"role": "system", "content": "You are a helpful assistant. Ask questions to understand the user's purchasing needs."},
        {"role": "user", "content": "Hello, I need help finding a product."}
    ]
    print("Chatbot: Let's start by understanding what you're looking for.")

    # Ask initial questions and collect answers
    questions = [
        "Why do you want to buy this product?",
        "Who is this product for?",
        "What is the context of the purchase? (e.g., birthday, anniversary, etc.)"
    ]
    
    for question in questions:
        print(f"Chatbot: {question}")
        user_response = input("You: ")
        
        # Allow the user to stop the conversation
        if user_response.lower() in ["stop", "exit"]:
            print("Chatbot: Thank you for your responses! Ending the conversation.")
            break

        # Store the user's response
        key = question.split()[0].lower()  # Use the first word of the question as the key
        product_info[key] = user_response
        conversation.append({"role": "user", "content": user_response})

    return product_info

def recommend_product_with_mistral(product_info, product_list):
    """
    Recommends the best product based on user input using Mistral AI.

    Args:
        product_info (dict): User input data (e.g., why, who, context).
        product_list (list): A list of available products.

    Returns:
        str: The recommended product.
    """
    products_string = ", ".join(product_list)
    user_info_string = f"Why: {product_info.get('why', '')}, Who: {product_info.get('who', '')}, Context: {product_info.get('context', '')}"

    prompt = (
        f"Given the following user information: {user_info_string}, "
        f"and a list of products: {products_string}, which product would you recommend as the best fit for the user?"
    )
    
    conversation = [
        {"role": "system", "content": "You are a helpful assistant. Recommend the best product from the list based on user responses."},
        {"role": "user", "content": prompt}
    ]

    response = chat_with_mistral(conversation)
    return response.strip()

def main():
    """
    Main function to run the chatbot for gathering product information and recommending a product.
    """
    # Product list (can be replaced by a database or API in the future)
    product_list = [
        "Smartphone", "Laptop", "Running Shoes", "Yoga Mat", "Bluetooth Speaker",
        "Coffee Maker", "T-shirt", "Smartwatch", "Electric Toothbrush"
    ]

    # Step 1: Gather user information
    product_info = gather_product_info()

    # Step 2: Recommend a product
    print("\nChatbot: Based on your responses, I will now recommend the best product.")
    recommended_product = recommend_product_with_mistral(product_info, product_list)
    print(f"\nChatbot: Based on your responses, I recommend the {recommended_product}.")
    print("Chatbot: Thank you for your time. Goodbye!")

# Run the script
if __name__ == "__main__":
    main()
