import streamlit as st
import uuid
import logging.config
from datetime import datetime
from app.chatbot import GiftChatbot
from app.storage import DataStorage
from app.ui import UI
from app.config import CREDENTIALS_PATH, LOGGING_CONFIG

# Setup logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def initialize_session_state():
    """Initialize all session state variables if they don't exist."""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'show_filters' not in st.session_state:
        st.session_state.show_filters = False
    
    if 'price_range' not in st.session_state:
        st.session_state.price_range = (0, 1_000_000)
    
    if 'gift_type' not in st.session_state:
        st.session_state.gift_type = None
    
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []

def display_chat_interface(chatbot):
    """Display and handle the chat interface."""
    # Display existing messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Chat input
    prompt = st.chat_input(
        "Votre message..." if st.session_state.messages 
        else "Décrivez qui recevra le cadeau..."
    )
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            # Get chatbot response
            response = chatbot.get_response(st.session_state.messages)
            
            if response:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                with st.chat_message("assistant"):
                    st.write(response)

        except Exception as e:
            logger.error(f"Error getting chatbot response: {str(e)}")
            st.error("Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer.")

def save_recommendation(storage, recommendation_data):
    """Save recommendation to storage with error handling."""
    try:
        if storage.save_recommendation(recommendation_data):
            logger.info(f"Saved recommendation for user {st.session_state.user_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error saving recommendation: {str(e)}")
        return False

def display_welcome():
    """Display welcome message and instructions."""
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h2>Bienvenue sur KdostraI 🎁</h2>
            <p>Je suis votre assistant personnel pour trouver le cadeau parfait !</p>
            <p>Commencez par me dire pour qui vous cherchez un cadeau, et je vous aiderai à trouver des idées personnalisées.</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    try:
        # Page config
        UI.set_page_config()
        
        # Initialize components
        storage = DataStorage(credentials_path=CREDENTIALS_PATH)
        chatbot = GiftChatbot()
        
        # Initialize session state
        initialize_session_state()
        
        # Add system message if messages are empty
        if not st.session_state.messages:
            st.session_state.messages = [{
                "role": "system",
                "content": chatbot.system_prompt
            }]

        # Display header
        UI.display_header()
        
        # Show welcome message if no conversation started
        if len(st.session_state.messages) <= 1:
            display_welcome()

        # Sidebar for filters
        with st.sidebar:
            st.markdown("### 🔍 Filtres de recherche")
            UI.display_filters(st.session_state)
            
            # Display current filters if set
            if st.session_state.price_range != (0, 1_000_000):
                st.info(f"Prix: {st.session_state.price_range[0]}€ - {st.session_state.price_range[1]}€")
            if st.session_state.gift_type:
                st.info(f"Type: {st.session_state.gift_type}")

        # Main chat interface
        display_chat_interface(chatbot)

        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
            "Powered by Mistral AI 🤖 | Développé par l'équipe KdostraI"
            "</div>",
            unsafe_allow_html=True
        )

        # Error handling for storage
        if not storage.sheet:
            logger.warning("Google Sheets connection not initialized")
            # Continue without storage functionality
            
    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}")
        st.error(
            "Une erreur s'est produite. "
            "Veuillez rafraîchir la page ou réessayer plus tard."
        )

if __name__ == "__main__":
    main()