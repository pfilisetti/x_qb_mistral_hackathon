from app.chatbot import GiftChatbot
from app.rag_engine import RAGEngine
from app.data_loader import DataLoader
import pandas as pd
import os
from dotenv import load_dotenv
import time

def test_chatbot():
    """Test simple du chatbot avec quelques interactions."""
    
    # 1. Initialisation
    print("\n=== Initialisation du chatbot ===")
    load_dotenv()  # Charge les variables d'environnement (MISTRAL_API_KEY)
    chatbot = GiftChatbot()
    
    # 2. Préparation des données de test
    print("\n=== Préparation des données de test ===")
    sample_data = pd.DataFrame({
        'name': [
            'Kindle Paperwhite',
            'Set de Jardinage Premium',
            'Livre de Cuisine',
            'Robot Cuiseur'
        ],
        'main_category': ['Electronics', 'Garden', 'Books', 'Kitchen'],
        'sub_category': ['E-readers', 'Tools', 'Cooking', 'Appliances'],
        'ratings': [4.5, 4.2, 4.8, 4.3],
        'discount_price': [129.99, 45.99, 24.99, 199.99],
        'actual_price': [149.99, 59.99, 29.99, 249.99]
    })
    
    # 3. Configuration du RAG
    print("\n=== Configuration du RAG ===")
    rag_engine = RAGEngine()
    rag_engine.index_products(sample_data)
    chatbot.set_rag_engine(rag_engine)
    
    # 4. Simulation d'une conversation
    conversation = [
        {
            "role": "system",
            "content": chatbot.system_prompt
        },
        {
            "role": "user",
            "content": "Je cherche un cadeau pour ma mère qui a 50 ans"
        }
    ]
    
    print("\n=== Début de la conversation ===")
    print("\nUTILISATEUR: Je cherche un cadeau pour ma mère qui a 50 ans")
    
    response = chatbot.get_response(conversation)
    print(f"\nASSISTANT: {response}")
    
    # Ajout d'informations sur les intérêts
    conversation.extend([
        {
            "role": "assistant",
            "content": response
        },
        {
            "role": "user",
            "content": "Elle aime beaucoup la cuisine et la lecture. Mon budget est de 100 euros maximum."
        }
    ])
    
    print("\nUTILISATEUR: Elle aime beaucoup la cuisine et la lecture. Mon budget est de 100 euros maximum.")
    
    # Obtention des recommandations
    print("\n=== Obtention des recommandations ===")
    final_response = chatbot.get_response(conversation)
    print(f"\nASSISTANT: {final_response}")

    # 5. Extraction des préférences
    print("\n=== Test de l'extraction des préférences ===")
    preferences = chatbot.extract_user_preferences(conversation)
    print("\nPréférences extraites:")
    for key, value in preferences.items():
        print(f"- {key}: {value}")

if __name__ == "__main__":
    test_chatbot()