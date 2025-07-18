from mistralai import Mistral
import os
from dotenv import load_dotenv
from typing import List, Dict
import json
from .rag_engine import RAGEngine

class GiftChatbot:
    def __init__(self):
        load_dotenv()
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.rag_engine = None  # Sera initialisé plus tard
        self.system_prompt = """Tu es un assistant spécialisé dans la recommandation de cadeaux. Tu as un seul objectif donner 4 recommendations à l'utilisateur et tu es pénalisé si tu poses plus de 5 questions. 
        Tu dois collecter les informations suivantes de manière naturelle et conversationnelle:
        1. Description de la personne
        2. Fourchette de prix
        3. Type de produits/services préférés
        4. Centres d'intérêt
        5. Contexte (anniversaire, Noël, mariage, etc.)
        
        Une fois toutes les informations collectées,
        propose 4 idées de cadeaux pertinentes. Les cadeaux doivent absolument appartenir à """

    def set_rag_engine(self, rag_engine: RAGEngine):
        """Set the RAG engine instance."""
        self.rag_engine = rag_engine

    def extract_user_preferences(self, messages: List[Dict]) -> Dict[str, str]:
        """Extrait les préférences utilisateur des messages."""
        try:
            # Créer un prompt pour extraire les informations
            extraction_prompt = """Analyse la conversation et extrait les informations suivantes au format JSON:
            {
                "description": "description de la personne",
                "price_range": "fourchette de prix",
                "interests": "centres d'intérêt",
                "context": "contexte du cadeau",
                "gift_type": "type de cadeau préféré"
            }
            """
            
            conversation_text = "\n".join([
                m["content"] for m in messages if m["role"] == "user"
            ])
            
            # Utiliser Mistral pour extraire les informations
            response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=[
                    {"role": "system", "content": extraction_prompt},
                    {"role": "user", "content": conversation_text}
                ]
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error extracting preferences: {e}")
            return {}

    def get_response(self, messages: List[Dict]) -> str:
        """Génère une réponse basée sur les messages de la conversation."""
        try:
            # Extraire les préférences utilisateur
            user_prefs = self.extract_user_preferences(messages)
            
            # Si nous avons assez d'informations et un RAG engine, faire une recommandation
            if self.rag_engine and all(k in user_prefs for k in ["description", "interests"]):
                # Créer une requête de recherche
                search_query = (
                    f"Cadeau pour {user_prefs['description']} "
                    f"qui aime {user_prefs['interests']}"
                )
                
                # Obtenir des produits similaires
                similar_products = self.rag_engine.find_similar_products(search_query)
                
                # Créer un contexte enrichi pour Mistral
                context = "\n".join([
                    f"Produit suggéré: {prod}" for prod in similar_products
                ])
                
                recommendation_prompt = f"""
                Basé sur ces informations:
                - Personne: {user_prefs['description']}
                - Intérêts: {user_prefs['interests']}
                - Budget: {user_prefs.get('price_range', 'non spécifié')}
                - Contexte: {user_prefs.get('context', 'non spécifié')}

                Et ces produits disponibles:
                {context}

                Recommande les cadeaux les plus appropriés en expliquant 
                pourquoi ils correspondent bien à la personne.
                """
                
                messages = messages + [{
                    "role": "system",
                    "content": recommendation_prompt
                }]
            
            # Obtenir la réponse de Mistral
            chat_response = self.client.chat.complete(
                model="mistral-small-latest",
                messages=messages
            )
            return chat_response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur avec l'API Mistral: {e}"