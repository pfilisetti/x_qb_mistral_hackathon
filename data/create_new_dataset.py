import pandas as pd
import numpy as np
import os

def create_complete_dataset():
    """Crée un dataset complet pour le système de recommandation de cadeaux."""
    
    # Définition étendue des catégories et sous-catégories
    categories = {
        'Electronics': {
            'sub_categories': ['Smartphones', 'Tablettes', 'Liseuses', 'Écouteurs', 'Enceintes', 'Montres connectées', 'Appareils photo', 'Consoles de jeux'],
            'gift_category': 'Tech',
            'prix_min': 30,
            'prix_max': 800
        },
        'Books': {
            'sub_categories': ['Romans', 'Cuisine', 'Développement personnel', 'Sciences', 'Art', 'Voyages', 'BD & Mangas', 'Histoire'],
            'gift_category': 'Culture',
            'prix_min': 10,
            'prix_max': 50
        },
        'Home & Kitchen': {
            'sub_categories': ['Petit électroménager', 'Arts de la table', 'Décoration', 'Accessoires cuisine', 'Machine à café', 'Ustensiles'],
            'gift_category': 'Maison',
            'prix_min': 20,
            'prix_max': 400
        },
        'Beauty & Health': {
            'sub_categories': ['Soins visage', 'Parfums', 'Bien-être', 'Massage', 'Spa', 'Cosmétiques', 'Soins cheveux'],
            'gift_category': 'Bien-être',
            'prix_min': 15,
            'prix_max': 200
        },
        'Sports & Fitness': {
            'sub_categories': ['Yoga', 'Fitness', 'Running', 'Sports d\'équipe', 'Randonnée', 'Natation', 'Cyclisme'],
            'gift_category': 'Sport',
            'prix_min': 20,
            'prix_max': 300
        },
        'Toys & Games': {
            'sub_categories': ['Jeux de société', 'Puzzles', 'Jeux créatifs', 'Jeux éducatifs', 'Jeux de construction', 'Jeux d\'extérieur'],
            'gift_category': 'Loisirs',
            'prix_min': 15,
            'prix_max': 150
        },
        'Jewelry': {
            'sub_categories': ['Colliers', 'Bagues', 'Bracelets', 'Boucles d\'oreilles', 'Montres', 'Bijoux personnalisés'],
            'gift_category': 'Mode',
            'prix_min': 20,
            'prix_max': 500
        },
        'Art & Crafts': {
            'sub_categories': ['Peinture', 'Dessin', 'Scrapbooking', 'Poterie', 'Couture', 'Tricot'],
            'gift_category': 'Créatif',
            'prix_min': 15,
            'prix_max': 200
        },
        'Gourmet Food': {
            'sub_categories': ['Chocolats', 'Thés', 'Cafés', 'Vins', 'Épicerie fine', 'Box découverte'],
            'gift_category': 'Gastronomie',
            'prix_min': 20,
            'prix_max': 150
        },
        'Garden': {
            'sub_categories': ['Outils', 'Plantes', 'Décoration extérieure', 'Jardinage urbain', 'Accessoires'],
            'gift_category': 'Nature',
            'prix_min': 15,
            'prix_max': 250
        },
        'Musical Instruments': {
            'sub_categories': ['Guitares', 'Pianos', 'Percussion', 'Accessoires', 'Débutant', 'Instruments traditionnels'],
            'gift_category': 'Musique',
            'prix_min': 30,
            'prix_max': 600
        },
        'Experience Gifts': {
            'sub_categories': ['Spa & Bien-être', 'Gastronomie', 'Sport & Aventure', 'Culture', 'Séjours', 'Ateliers'],
            'gift_category': 'Expérience',
            'prix_min': 50,
            'prix_max': 500
        }
    }

    products = []
    
    for main_category, info in categories.items():
        for sub_category in info['sub_categories']:
            # Générer 8-12 produits par sous-catégorie
            num_products = np.random.randint(8, 13)
            
            for _ in range(num_products):
                actual_price = round(np.random.uniform(info['prix_min'], info['prix_max']), 2)
                discount = np.random.uniform(0.1, 0.3)
                discount_price = round(actual_price * (1 - discount), 2)
                rating = round(np.random.uniform(3.8, 5), 1)
                num_ratings = np.random.randint(50, 2000)

                # Noms de produits plus réalistes
                brands = {
                    'Electronics': ['Samsung', 'Sony', 'Apple', 'Philips', 'Bose', 'JBL'],
                    'Books': ['Larousse', 'Marabout', 'Hachette', 'Gallimard', 'Flammarion'],
                    'Home & Kitchen': ['Moulinex', 'Tefal', 'KitchenAid', 'Bosch', 'Siemens'],
                    'Beauty & Health': ['L\'Oréal', 'Yves Rocher', 'Nivea', 'Clarins', 'Lancôme'],
                    'Sports & Fitness': ['Nike', 'Adidas', 'Puma', 'Decathlon', 'Under Armour'],
                    'Toys & Games': ['Ravensburger', 'Lego', 'Playmobil', 'Mattel', 'Hasbro'],
                    'Jewelry': ['Swarovski', 'Pandora', 'Thomas Sabo', 'Fossil', 'Michael Kors'],
                    'Art & Crafts': ['Faber-Castell', 'Staedtler', 'Moleskine', 'Leuchtturm1917'],
                    'Gourmet Food': ['Valrhona', 'Kusmi Tea', 'Nespresso', 'Mariage Frères'],
                    'Garden': ['Gardena', 'Weber', 'Fiskars', 'Hozelock', 'Bosch'],
                    'Musical Instruments': ['Yamaha', 'Roland', 'Fender', 'Gibson', 'Casio'],
                    'Experience Gifts': ['Wonderbox', 'Smartbox', 'Buyagift', 'Virgin Experience']
                }

                brand = np.random.choice(brands[main_category])
                name = f"{brand} {sub_category} {np.random.randint(100, 999)}"

                # Descriptions plus détaillées
                descriptions = {
                    'Electronics': f"Produit tech innovant avec les dernières fonctionnalités. Design élégant et performances optimales. {rating}/5 étoiles basé sur {num_ratings} avis.",
                    'Books': f"Un ouvrage captivant qui vous transportera dans un nouvel univers. {rating}/5 étoiles selon {num_ratings} lecteurs.",
                    'Home & Kitchen': f"Accessoire de cuisine indispensable alliant praticité et style. Note de {rating}/5 par {num_ratings} utilisateurs satisfaits.",
                    'Beauty & Health': f"Produit de beauté haute qualité pour des résultats professionnels. {rating}/5 étoiles selon {num_ratings} clients.",
                    'Sports & Fitness': f"Équipement sportif performant pour atteindre vos objectifs. {rating}/5 basé sur {num_ratings} sportifs.",
                    'Toys & Games': f"Jeu divertissant pour des heures de plaisir. Note moyenne de {rating}/5 par {num_ratings} joueurs.",
                    'Jewelry': f"Bijou élégant fait avec des matériaux de qualité. {rating}/5 étoiles selon {num_ratings} acheteurs.",
                    'Art & Crafts': f"Matériel créatif de qualité professionnelle. {rating}/5 basé sur {num_ratings} artistes.",
                    'Gourmet Food': f"Produit gastronomique sélectionné pour sa qualité exceptionnelle. Note de {rating}/5 par {num_ratings} gourmets.",
                    'Garden': f"Outil de jardinage robuste et ergonomique. {rating}/5 étoiles selon {num_ratings} jardiniers.",
                    'Musical Instruments': f"Instrument de qualité avec un son exceptionnel. {rating}/5 basé sur {num_ratings} musiciens.",
                    'Experience Gifts': f"Expérience unique et mémorable. Note de {rating}/5 par {num_ratings} participants."
                }

                products.append({
                    'name': name,
                    'main_category': main_category,
                    'sub_category': sub_category,
                    'gift_category': info['gift_category'],
                    'ratings': rating,
                    'no_of_ratings': num_ratings,
                    'discount_price': discount_price,
                    'actual_price': actual_price,
                    'rich_description': descriptions[main_category]
                })

    df = pd.DataFrame(products)
    
    # Sauvegarde du dataset
    if not os.path.exists('data'):
        os.makedirs('data')
        
    df.to_csv("data/gift_dataset.csv", index=False, encoding='utf-8')
    
    print(f"Dataset créé avec {len(df)} produits")
    print("\nNombre de produits par catégorie principale:")
    print(df['main_category'].value_counts())
    return df

if __name__ == "__main__":
    df = create_complete_dataset()
    
    # Afficher quelques statistiques
    print("\nStatistiques des prix:")
    print(f"Prix moyen: {df['discount_price'].mean():.2f}€")
    print(f"Prix minimum: {df['discount_price'].min():.2f}€")
    print(f"Prix maximum: {df['discount_price'].max():.2f}€")
    
    print("\nNotes moyennes par catégorie:")
    print(df.groupby('main_category')['ratings'].mean().round(2))