import os
import csv
from datetime import datetime

class DataStorage:
    def __init__(self):
        """
        Initialize the DataStorage class with local CSV storage
        """
        self.recommendations_path = 'data/recommendations.csv'
        self._initialize_storage()

    def _initialize_storage(self):
        """Initialize the storage system and create necessary directories/files."""
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.recommendations_path):
            with open(self.recommendations_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'user_id', 'description', 
                    'price_range', 'gift_type', 'interests', 'context'
                ])

    def save_recommendation(self, info):
        """Save recommendation information to CSV."""
        try:
            with open(self.recommendations_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    info.get('user_id', ''),
                    info.get('description', ''),
                    info.get('price_range', ''),
                    info.get('gift_type', ''),
                    info.get('interests', ''),
                    info.get('context', '')
                ])
            return True
        except Exception as e:
            print(f"Error saving recommendation: {e}")
            return False

    def get_recommendations(self):
        """Retrieve all recommendations from CSV."""
        try:
            recommendations = []
            with open(self.recommendations_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    recommendations.append(row)
            return recommendations
        except Exception as e:
            print(f"Error retrieving recommendations: {e}")
            return []