import gradio as gr
from app.recommendation import generate_recommendations
from app.wishlist import add_to_wishlist, display_wishlist
from app.chatbot import chatbot_response  # Import chatbot logic

def build_ui():
    """
    Builds the Gradio UI.
    """
    with gr.Blocks() as demo:
        # Logo and Header
        gr.Image("./data/logo.png", label=None, elem_id="logo", width=300, height=300)
        gr.Markdown("# 🎁 Gift Recommendation Chatbot")

        # Chatbot Section
        gr.Markdown("### Chat with GiftBot:")
        chat_history = gr.Chatbot(label="Chat with GiftBot")  # Chat display
        user_input = gr.Textbox(
            placeholder="Describe the person, occasion, or ask a question...",
            label="Your Message"
        )
        submit_button = gr.Button("Send")  # Button to submit user input
        submit_button.click(chatbot_response, [user_input, chat_history], [user_input, chat_history])

        # Search Bar
        user_input_search = gr.Textbox(
            placeholder="Describe the person or occasion...",
            label="Hi! What kind of present are you looking for?",
            elem_id="search-bar"
        )

        # Budget Slider
        gr.Markdown("### Select a Budget Range:")
        budget_slider = gr.Slider(1, 7300, step=1, label="Budget Range (€)")
        go_button = gr.Button("Go")

        # Recommendations
        recommendations_display = gr.Markdown("### Recommendations will appear here.")
        go_button.click(
            lambda budget: generate_recommendations(budget, 7300),
            inputs=[budget_slider],
            outputs=[recommendations_display]
        )

        # Wishlist
        gr.Markdown("### Wishlist:")
        wishlist_display = gr.Markdown(display_wishlist())

    return demo