# app/storage.py
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
from .config import CREDENTIALS_PATH, GOOGLE_SHEETS_ID

class DataStorage:
    def __init__(self, credentials_path=CREDENTIALS_PATH):
        """
        Initialize the DataStorage class with Google Sheets connection.
        
        Args:
            credentials_path (str): Path to the Google Sheets credentials file
        """
        self.sheet = self._connect_to_sheets(credentials_path)

    def _connect_to_sheets(self, credentials_path):
        """
        Establish connection to Google Sheets.
        
        Args:
            credentials_path (str): Path to the credentials file
            
        Returns:
            gspread.Worksheet: Connected worksheet or None if connection fails
        """
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credentials_path, 
                scope
            )
            
            gc = gspread.authorize(credentials)
            return gc.open_by_key(GOOGLE_SHEETS_ID).sheet1
            
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")
            return None

    def save_recommendation(self, info):
        """
        Save recommendation information to Google Sheets.
        
        Args:
            info (dict): Dictionary containing recommendation information
            
        Returns:
            bool: True if save successful, False otherwise
        """
        if self.sheet:
            try:
                # Format the data row
                row = [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    info['user_id'],
                    info['description'],
                    info['price_range'],
                    info['gift_type'],
                    info['interests'],
                    info['context']
                ]
                
                # Append the row to the sheet
                self.sheet.append_row(row)
                return True
                
            except Exception as e:
                print(f"Error saving to sheet: {e}")
                return False
        return False

    def get_recommendations(self):
        """
        Retrieve all recommendations from the sheet.
        
        Returns:
            list: List of dictionaries containing recommendation data
        """
        if self.sheet:
            try:
                records = self.sheet.get_all_records()
                return records
            except Exception as e:
                print(f"Error retrieving recommendations: {e}")
                return []
        return []