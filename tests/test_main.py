# test_main.py
import pytest
from unittest.mock import patch, MagicMock
from app.main import main

@pytest.mark.skip(reason="Integration test - requires all components")
def test_main_flow():
    with patch('main.GiftChatbot') as mock_chatbot:
        with patch('main.DataStorage') as mock_storage:
            with patch('main.UI') as mock_ui:
                with patch('streamlit.chat_input') as mock_chat_input:
                    mock_chat_input.return_value = "Je cherche un cadeau pour ma mère"
                    mock_chatbot.return_value.get_response.return_value = "Je peux vous aider avec ça"
                    
                    main()
                    
                    mock_ui.set_page_config.assert_called_once()
                    mock_ui.load_css.assert_called_once()
                    mock_ui.display_header.assert_called_once()