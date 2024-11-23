from mistral_integration import chat_with_mistral  # Import your Mistral integration

def chatbot_response(user_input, chat_history):
    """
    Handles user input and generates a response using the Mistral LLM.
    
    Args:
        user_input (str): The user's input message.
        chat_history (list): The conversation history (list of tuples).
    
    Returns:
        tuple: An empty string (clears the input field) and the updated chat history.
    """
    # Add the user's input to the chat history
    chat_history.append(("User", user_input))
    
    # Create a conversation context for the Mistral API
    conversation = [{"role": "system", "content": "You are a helpful assistant."}]  # System role
    conversation.extend([{"role": "user" if i % 2 == 0 else "assistant", "content": message[1]} 
                         for i, message in enumerate(chat_history)])
    conversation.append({"role": "user", "content": user_input})  # Add current user input
    
    # Get a response from Mistral
    try:
        response = chat_with_mistral(conversation)
    except Exception as e:
        response = f"An error occurred while processing your request: {e}"
    
    # Add the response to the chat history
    chat_history.append(("Assistant", response))
    return "", chat_history