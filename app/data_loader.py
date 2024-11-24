# app/data_loader.py
import pandas as pd
import os
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, data_path: str = None):
        """Initialize the DataLoader with the path to the gift dataset."""
        if data_path is None:
            # Try multiple possible paths
            possible_paths = [
                "data/data_gifts.csv",
                "./data/data_gifts.csv",
                "../data/data_gifts.csv",
                "data_gifts.csv"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.data_path = path
                    logger.info(f"Found dataset at: {path}")
                    break
            else:
                current_dir = os.getcwd()
                logger.error(f"No dataset found. Current directory: {current_dir}")
                self.data_path = "data/data_gifts.csv"  # default path
        else:
            self.data_path = data_path

    def load_amazon_dataset(self) -> Optional[pd.DataFrame]:
        """Load and prepare the gift dataset."""
        try:
            logger.info(f"Attempting to load dataset from: {self.data_path}")
            
            # Check if file exists
            if not os.path.exists(self.data_path):
                logger.error(f"Dataset not found at {self.data_path}")
                logger.info(f"Current working directory: {os.getcwd()}")
                logger.info(f"Directory contents: {os.listdir('.')}")
                raise FileNotFoundError(f"Dataset not found at {self.data_path}")
            
            # Try different encodings
            encodings = ['latin1', 'utf-8', 'utf-8-sig']
            df = None
            
            for encoding in encodings:
                try:
                    logger.info(f"Trying to read CSV with encoding: {encoding}")
                    df = pd.read_csv(self.data_path, sep=';', encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    logger.error(f"Error with encoding {encoding}: {str(e)}")
                    continue
            
            if df is None:
                raise ValueError("Could not read the CSV file with any encoding")

            # Log the column names we found
            logger.info(f"Columns found in dataset: {df.columns.tolist()}")
            
            # Add rich description if it doesn't exist
            if 'rich_description' not in df.columns:
                df['rich_description'] = df.apply(
                    lambda row: f"{row['name_of_the_product']} - {row['main_category']} - {row['sub_category']}", 
                    axis=1
                )

            # Rename columns if needed
            column_mapping = {
                'name_of_the_product': 'name',
                'discounted_price': 'discount_price'
            }
            df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
            
            # Clean price columns
            for col in ['discount_price', 'actual_price']:
                if df[col].dtype == 'object':
                    df[col] = df[col].apply(lambda x: str(x).replace('₹', '').replace(',', '')).astype(float)

            # Add gift category if it doesn't exist
            if 'gift_category' not in df.columns:
                df['gift_category'] = df['main_category']

            # Validate the final dataframe
            required_columns = ['name', 'main_category', 'sub_category', 'discount_price', 'actual_price', 'ratings']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                raise ValueError(f"Dataset missing required columns: {missing_columns}")

            logger.info(f"Successfully loaded {len(df)} products")
            logger.info(f"Sample of data:\n{df.head()}")
            
            return df

        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}", exc_info=True)
            return None

    def get_categories(self) -> dict:
        """Get available categories from the dataset."""
        try:
            df = pd.read_csv(self.data_path, sep=';', encoding='latin1')
            categories = {
                'main_categories': sorted(df['main_category'].unique().tolist()),
                'gift_categories': sorted(df['sub_category'].unique().tolist())
            }
            logger.info(f"Found categories: {categories}")
            return categories
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            return {'main_categories': [], 'gift_categories': []}

    def get_price_range(self) -> Tuple[float, float]:
        """Get the price range from the dataset."""
        try:
            df = pd.read_csv(self.data_path, sep=';', encoding='latin1')
            if 'discounted_price' in df.columns:
                price_col = 'discounted_price'
            else:
                price_col = 'discount_price'
                
            prices = df[price_col].astype(str).str.replace('₹', '').str.replace(',', '').astype(float)
            price_range = (prices.min(), prices.max())
            logger.info(f"Price range found: {price_range}")
            return price_range
        except Exception as e:
            logger.error(f"Error getting price range: {str(e)}")
            return (0.0, 1000000.0)