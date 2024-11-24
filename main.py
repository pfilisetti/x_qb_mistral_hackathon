import streamlit as st
import uuid
import logging.config
from datetime import datetime
from app.chatbot import GiftChatbot
from app.storage import DataStorage
from app.ui import UI
from app.config import CREDENTIALS_PATH, LOGGING_CONFIG
from app.data_loader import DataLoader
from app.rag_engine import RAGEngine

# Setup logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def initialize_rag_components():
    """Initialize RAG system and chatbot."""
    try:
        with st.spinner('Chargement de la base de données des produits...'):
            # Charger les données
            data_loader = DataLoader()
            gift_data = data_loader.load_amazon_dataset()
            
            if gift_data is None:
                raise ValueError("Impossible de charger le dataset")
            
            # Initialiser RAG
            rag_engine = RAGEngine()
            if not rag_engine.index_products(gift_data):
                raise ValueError("Échec de l'indexation des produits")
            
            # Initialiser Chatbot
            chatbot = GiftChatbot()
            chatbot.set_rag_engine(rag_engine)
            
            # Stocker les catégories et plages de prix
            st.session_state.categories = data_loader.get_categories()
            st.session_state.price_range = data_loader.get_price_range()
            
            return chatbot, data_loader
            
    except Exception as e:
        logger.error(f"Error initializing RAG components: {str(e)}")
        st.error("Erreur lors du chargement de la base de données des produits.")
        return None, None

def initialize_session_state():
    """Initialize all session state variables."""
    if 'initialized' not in st.session_state:
        st.session_state.update({
            'user_id': str(uuid.uuid4()),
            'messages': [],
            'show_filters': False,
            'price_range': (0, 1_000_000),
            'gift_type': None,
            'recommendations': [],
            'rag_initialized': False,
            'categories': {},
            'current_preferences': {},
            'conversation_stage': 'initial',
            'initialized': True
        })

def display_chat_interface(chatbot):
    """Display and handle the chat interface."""
    # Afficher les messages existants
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Input du chat
    prompt = st.chat_input(
        "Votre message..." if st.session_state.messages 
        else "Décrivez qui recevra le cadeau..."
    )
    
    if prompt:
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        try:
            # Obtenir la réponse du chatbot
            response = chatbot.get_response(st.session_state.messages)
            
            if response:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                with st.chat_message("assistant"):
                    st.write(response)

                # Mettre à jour les recommandations si disponibles
                if hasattr(chatbot, 'last_recommendations'):
                    st.session_state.recommendations = chatbot.last_recommendations

        except Exception as e:
            logger.error(f"Error getting chatbot response: {str(e)}")
            st.error("Désolé, je n'ai pas pu générer une réponse. Veuillez réessayer.")

def display_recommendations():
    """Display product recommendations."""
    if st.session_state.recommendations:
        st.markdown("### 🎁 Recommandations personnalisées")
        
        cols = st.columns(2)
        for idx, rec in enumerate(st.session_state.recommendations):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style='padding: 15px; border: 1px solid #ddd; border-radius: 5px; 
                     margin: 5px; background-color: white;'>
                    <h4 style='color: #1e88e5;'>{rec['name']}</h4>
                    <p><strong>Prix:</strong> {rec['price']}€</p>
                    <p><strong>Catégorie:</strong> {rec.get('category', 'Non spécifié')}</p>
                    <p>{rec['description']}</p>
                    <p style='color: #ffd700;'>{'⭐' * int(rec['rating'])} {rec['rating']}/5</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Ajouter à ma liste 💝", key=f"add_{idx}"):
                    # Ajouter à la wishlist (à implémenter)
                    st.toast(f"✨ {rec['name']} ajouté à votre liste!")

def display_welcome():
    """Display welcome message and instructions."""
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h2>Bienvenue sur KdostraI 🎁</h2>
            <p>Je suis votre assistant personnel pour trouver le cadeau parfait !</p>
            <p>Décrivez-moi la personne à qui vous souhaitez offrir un cadeau, 
            et je vous aiderai à trouver des idées personnalisées.</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    try:
        # Configuration de la page
        UI.set_page_config()
        
        # Initialisation du state
        initialize_session_state()
        
        # Initialisation des composants
        storage = DataStorage(credentials_path=CREDENTIALS_PATH)
        
        # Initialisation du RAG et chatbot
        if not st.session_state.rag_initialized:
            chatbot, data_loader = initialize_rag_components()
            if chatbot and data_loader:
                st.session_state.rag_initialized = True
                st.session_state.chatbot = chatbot
                st.session_state.data_loader = data_loader
        else:
            chatbot = st.session_state.chatbot
            data_loader = st.session_state.data_loader
        
        if not chatbot:
            st.error("Impossible d'initialiser le système de recommandation.")
            return
        
        # Message système initial
        if not st.session_state.messages:
            st.session_state.messages = [{
                "role": "system",
                "content": chatbot.system_prompt
            }]

        # Affichage du header
        UI.display_header()
        
        # Message de bienvenue
        if len(st.session_state.messages) <= 1:
            display_welcome()

        # Sidebar avec filtres
        with st.sidebar:
            st.markdown("### 🔍 Affiner la recherche")
            
            # Utiliser les catégories du dataset
            if st.session_state.categories:
                gift_categories = st.session_state.categories.get('gift_categories', [])
                selected_category = st.selectbox(
                    "Type de cadeau",
                    options=['Tous'] + gift_categories
                )
                
                if selected_category != 'Tous':
                    st.session_state.gift_type = selected_category
            
            # Utiliser la plage de prix du dataset
            if hasattr(st.session_state, 'price_range'):
                min_price, max_price = st.session_state.price_range
                selected_range = st.slider(
                    "Budget (€)",
                    min_value=float(min_price),
                    max_value=float(max_price),
                    value=(float(min_price), float(max_price/2))
                )
                st.session_state.price_range = selected_range

        # Interface de chat principale
        display_chat_interface(chatbot)
        
        # Affichage des recommandations
        display_recommendations()

        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
            "Powered by Mistral AI 🤖 | Développé par l'équipe KdostraI"
            "</div>",
            unsafe_allow_html=True
        )
            
    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}")
        st.error(
            "Une erreur s'est produite. "
            "Veuillez rafraîchir la page ou réessayer plus tard."
        )

if __name__ == "__main__":
    main()