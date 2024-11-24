# test_chatbot.py
import pytest
from unittest.mock import Mock, patch
from app.chatbot import GiftChatbot

def test_chatbot_initialization():
    with patch('chatbot.Mistral') as mock_mistral:
        chatbot = GiftChatbot()
        assert isinstance(chatbot, GiftChatbot)
        assert "assistant spécialisé" in chatbot.system_prompt

def test_get_response_success():
    with patch('chatbot.Mistral') as mock_mistral:
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

def test_get_response_error():
    with patch('chatbot.Mistral') as mock_mistral:
        mock_mistral.return_value.chat.complete.side_effect = Exception("API Error")
        
        chatbot = GiftChatbot()
        messages = [
            {"role": "user", "content": "Test message"}
        ]
        
        response = chatbot.get_response(messages)
        assert "Erreur avec l'API Mistral" in response