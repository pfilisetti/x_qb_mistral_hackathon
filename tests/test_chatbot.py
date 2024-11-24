import pytest
from unittest.mock import Mock, patch
from app.chatbot import GiftChatbot
from app.rag_engine import RAGEngine
import pandas as pd

# Tests Unitaires
class TestChatbotUnit:
    def test_chatbot_initialization(self):
        with patch('app.chatbot.Mistral') as mock_mistral:
            chatbot = GiftChatbot()
            assert isinstance(chatbot, GiftChatbot)
            assert "assistant spécialisé" in chatbot.system_prompt

    def test_get_response_success(self):
        with patch('app.chatbot.Mistral') as mock_mistral:
            # Setup mock
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="Test response"))]
            mock_mistral.return_value.chat.complete.return_value = mock_response
            
            chatbot = GiftChatbot()
            messages = [
                {"role": "user", "content": "Je cherche un cadeau pour ma mère"}
            ]
            
            response = chatbot.get_response(messages)
            assert response == "Test response"

    def test_get_response_error(self):
        with patch('app.chatbot.Mistral') as mock_mistral:
            mock_mistral.return_value.chat.complete.side_effect = Exception("API Error")
            
            chatbot = GiftChatbot()
            messages = [
                {"role": "user", "content": "Test message"}
            ]
            
            response = chatbot.get_response(messages)
            assert "Erreur avec l'API Mistral" in response

    def test_extract_user_preferences_success(self):
        with patch('app.chatbot.Mistral') as mock_mistral:
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="""
                {
                    "description": "mère de 50 ans",
                    "price_range": "50-100€",
                    "interests": "lecture, jardinage",
                    "context": "anniversaire",
                    "gift_type": "objet physique"
                }
            """))]
            mock_mistral.return_value.chat.complete.return_value = mock_response
            
            chatbot = GiftChatbot()
            messages = [
                {"role": "user", "content": "Je cherche un cadeau pour ma mère qui a 50 ans"},
                {"role": "user", "content": "Elle aime la lecture et le jardinage"}
            ]
            
            prefs = chatbot.extract_user_preferences(messages)
            assert prefs["description"] == "mère de 50 ans"
            assert "lecture" in prefs["interests"]

# Tests d'Intégration
@pytest.mark.integration
class TestChatbotIntegration:
    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'name': ['Livre de jardinage', 'Liseuse Kindle'],
            'main_category': ['Livres', 'Électronique'],
            'sub_category': ['Jardinage', 'Liseuses'],
            'discount_price': [25.99, 89.99],
            'actual_price': [29.99, 99.99],
            'ratings': [4.5, 4.8],
            'no_of_ratings': [100, 500]
        })

    @pytest.fixture
    def rag_chatbot(self, sample_data):
        chatbot = GiftChatbot()
        rag_engine = RAGEngine()
        rag_engine.index_products(sample_data)
        chatbot.set_rag_engine(rag_engine)
        return chatbot

    def test_full_recommendation_flow(self, rag_chatbot):
        messages = [
            {"role": "user", "content": "Je cherche un cadeau pour ma mère qui a 50 ans"},
            {"role": "assistant", "content": "Je peux vous aider. Quels sont ses centres d'intérêt ?"},
            {"role": "user", "content": "Elle aime le jardinage et la lecture"},
            {"role": "assistant", "content": "Quel est votre budget ?"},
            {"role": "user", "content": "Entre 50 et 100 euros"}
        ]
        
        response = rag_chatbot.get_response(messages)
        assert response is not None
        assert len(response) > 0
        # Vérifier que la réponse contient des recommandations pertinentes
        assert any(word in response.lower() for word in ['livre', 'jardinage', 'liseuse'])

# Tests de Performance
@pytest.mark.performance
class TestChatbotPerformance:
    def test_response_time(self):
        with patch('app.chatbot.Mistral') as mock_mistral:
            import time
            
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="Test response"))]
            mock_mistral.return_value.chat.complete.return_value = mock_response
            
            chatbot = GiftChatbot()
            messages = [{"role": "user", "content": "Test message"}]
            
            start_time = time.time()
            response = chatbot.get_response(messages)
            end_time = time.time()
            
            assert (end_time - start_time) < 2  # La réponse doit prendre moins de 2 secondes

if __name__ == "__main__":
    pytest.main(["-v", "-s"])