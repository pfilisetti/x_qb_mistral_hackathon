import pandas as pd
import os
from typing import Optional

class DataLoader:
    def __init__(self, data_path: str = "data/gift_dataset.csv"):
        self.data_path = data_path

    def load_amazon_dataset(self) -> Optional[pd.DataFrame]:
        """Charge et prépare le dataset des cadeaux."""
        try:
            # Charger le dataset
            df = pd.read_csv(self.data_path)
            print(f"Données chargées : {len(df)} produits")

            # Vérifier les colonnes requises
            required_columns = [
                'name', 'main_category', 'sub_category', 'gift_category',
                'ratings', 'discount_price', 'actual_price', 'rich_description'
            ]
            
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Colonne manquante dans le dataset : {col}")

            # S'assurer que les types de données sont corrects
            df['discount_price'] = pd.to_numeric(df['discount_price'])
            df['actual_price'] = pd.to_numeric(df['actual_price'])
            df['ratings'] = pd.to_numeric(df['ratings'])
            
            print("Données validées et préparées avec succès")
            return df

        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            return None

    def get_categories(self) -> dict:
        """Retourne les catégories disponibles."""
        try:
            df = pd.read_csv(self.data_path)
            categories = {
                'main_categories': df['main_category'].unique().tolist(),
                'gift_categories': df['gift_category'].unique().tolist()
            }
            return categories
        except Exception as e:
            print(f"Erreur lors de la récupération des catégories : {e}")
            return {'main_categories': [], 'gift_categories': []}

    def get_price_range(self) -> tuple:
        """Retourne la fourchette de prix disponible."""
        try:
            df = pd.read_csv(self.data_path)
            return (df['discount_price'].min(), df['discount_price'].max())
        except Exception as e:
            print(f"Erreur lors de la récupération des prix : {e}")
            return (0, 0)