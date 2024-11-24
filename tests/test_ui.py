# test_ui.py
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st
from app.ui import UI

@pytest.mark.skip(reason="Streamlit can't be tested directly in pytest")
def test_display_header():
    with patch('streamlit.columns') as mock_columns:
        with patch('streamlit.image') as mock_image:
            UI.display_header()
            mock_image.assert_called_once_with(
                "https://i.imgur.com/jhYA0PZ.png", 
                width=300
            )

# conftest.py
import pytest

@pytest.fixture
def mock_session_state():
    class MockSessionState:
        def __init__(self):
            self.user_id = "test_user"
            self.messages = []
            self.show_filters = False
            self.price_range = (0, 1_000_000)
            self.gift_type = None
    
    return MockSessionState()