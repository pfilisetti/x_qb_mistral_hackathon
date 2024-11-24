from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import pandas as pd
from typing import List, Optional

class RAGEngine:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./data/chroma_db"
        ))
        self.collection = self._init_collection()
        self.products_df = None

    def _init_collection(self):
        """Initialise ou récupère la collection ChromaDB."""
        try:
            return self.chroma_client.get_collection("products")
        except:
            return self.chroma_client.create_collection("products")

    def _create_search_description(self, row) -> str:
        """Crée une description enrichie pour la recherche."""
        return (f"{row['name']} - {row['gift_category']} - "
                f"{row['main_category']} - {row['sub_category']} - "
                f"Prix: {row['discount_price']}€ - "
                f"Note: {row['ratings']}/5 - {row['rich_description']}")

    def index_products(self, df: pd.DataFrame):
        """Indexe les produits dans la base vectorielle."""
        try:
            print("Début de l'indexation des produits...")
            self.products_df = df
            
            # Créer les descriptions de recherche
            search_descriptions = df.apply(self._create_search_description, axis=1).tolist()
            
            # Créer les embeddings
            embeddings = self.embedding_model.encode(
                search_descriptions,
                batch_size=32,
                show_progress_bar=True
            )
            
            # Ajouter à ChromaDB
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=search_descriptions,
                ids=[str(i) for i in range(len(df))]
            )
            
            print(f"Indexation terminée : {len(df)} produits indexés")
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'indexation : {e}")
            return False

    def find_similar_products(self, query: str, n_results: int = 4) -> List[dict]:
        """Trouve les produits similaires basés sur la requête."""
        try:
            # Créer l'embedding de la requête
            query_embedding = self.embedding_model.encode(query)
            
            # Rechercher les produits similaires
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results
            )
            
            # Récupérer les indices des produits trouvés
            found_products = []
            for i, doc in enumerate(results['documents'][0]):
                if self.products_df is not None:
                    product_idx = int(results['ids'][0][i])
                    product = self.products_df.iloc[product_idx]
                    found_products.append({
                        'name': product['name'],
                        'price': product['discount_price'],
                        'rating': product['ratings'],
                        'category': product['gift_category'],
                        'description': product['rich_description']
                    })
            
            return found_products
            
        except Exception as e:
            print(f"Erreur lors de la recherche : {e}")
            return []