import gradio as gr
from wishlist import display_wishlist
from chatbot import chatbot_response  # Import chatbot logic

def build_ui():
    """
    Builds the Gradio UI.
    """
    with gr.Blocks() as demo:
        # Header Section with Logo and Wishlist Button
        with gr.Row():
            gr.Image("./data/logo.png", label=None, elem_id="logo", width=150, height=150)
            wishlist_button = gr.Button("🛒 Wishlist", elem_id="wishlist-btn")

        # Chatbot Section
        gr.Markdown("# 🎁 Gift Recommendation Chatbot")
        gr.Markdown("### Chat with GiftBot:")
        chat_history = gr.Chatbot(label="Chat with GiftBot")  # Chat display
        user_input = gr.Textbox(
            placeholder="Describe the person, occasion, or ask a question...",
            label="Your Message"
        )
        submit_button = gr.Button("Send")  # Button to submit user input

        # Link the chatbot function to the Gradio components
        submit_button.click(
            chatbot_response,  # Function handling user input
            inputs=[user_input, chat_history],  # Input components
            outputs=[user_input, chat_history]  # Output components
        )

        # Wishlist Modal
        wishlist_display = gr.Markdown(visible=False)  # Hidden by default
        wishlist_button.click(
            lambda: display_wishlist(),  # Show the wishlist
            inputs=[],
            outputs=[wishlist_display]
        )

    return demo