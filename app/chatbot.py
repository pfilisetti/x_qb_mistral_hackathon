# chatbot.py
from mistralai import Mistral
import os
from dotenv import load_dotenv

class GiftChatbot:
    def __init__(self):
        load_dotenv()
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.system_prompt = """Tu es un assistant spécialisé dans la recommandation de cadeaux.
        Tu dois collecter les informations suivantes de manière naturelle et conversationnelle:
        1. Description de la personne
        2. Fourchette de prix
        3. Type de produits/services préférés
        4. Centres d'intérêt
        5. Contexte (anniversaire, Noël, mariage, etc.)
        
        Pose une question à la fois. Une fois toutes les informations collectées,
        propose 4 idées de cadeaux pertinentes."""

    def get_response(self, messages):
        try:
            chat_response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=messages
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            return f"Erreur avec l'API Mistral: {e}"