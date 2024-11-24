# test_storage.py
import pytest
from unittest.mock import Mock, patch
from app.storage import DataStorage
from datetime import datetime

def test_storage_initialization():
    with patch('storage.ServiceAccountCredentials') as mock_creds:
        with patch('storage.gspread') as mock_gspread:
            storage = DataStorage()
            assert isinstance(storage, DataStorage)
            mock_gspread.authorize.assert_called_once()

def test_save_recommendation_success():
    with patch('storage.ServiceAccountCredentials') as mock_creds:
        with patch('storage.gspread') as mock_gspread:
            # Setup mock sheet
            mock_sheet = Mock()
            mock_gspread.authorize.return_value.open_by_key.return_value.sheet1 = mock_sheet
            
            storage = DataStorage()
            test_info = {
                'user_id': '123',
                'description': 'Mère de 50 ans',
                'price_range': '50-100',
                'gift_type': 'Objet physique',
                'interests': 'Lecture, jardinage',
                'context': 'Anniversaire'
            }
            
            result = storage.save_recommendation(test_info)
            assert result == True
            mock_sheet.append_row.assert_called_once()

def test_save_recommendation_failure():
    with patch('storage.ServiceAccountCredentials') as mock_creds:
        with patch('storage.gspread') as mock_gspread:
            mock_sheet = Mock()
            mock_sheet.append_row.side_effect = Exception("Sheet error")
            mock_gspread.authorize.return_value.open_by_key.return_value.sheet1 = mock_sheet
            
            storage = DataStorage()
            test_info = {
                'user_id': '123',
                'description': 'Test',
                'price_range': '50-100',
                'gift_type': 'Test',
                'interests': 'Test',
                'context': 'Test'
            }
            
            result = storage.save_recommendation(test_info)
            assert result == False