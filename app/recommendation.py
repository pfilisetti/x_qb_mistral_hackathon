# app/recommendation.py

#gift_database = [
 #   {"name": "Montre connectée", "description": "Une montre moderne pour suivre ses activités.", "price": "150€", "image": "https://via.placeholder.com/150"},
  ##  {"name": "Abonnement Spotify", "description": "Un cadeau parfait pour les amateurs de musique.", "price": "9,99€/mois", "image": "https://via.placeholder.com/150"},
    #{"name": "Coffret de vin", "description": "Un coffret avec des vins soigneusement sélectionnés.", "price": "60€", "image": "https://via.placeholder.com/150"},
    #{"name": "Box DIY", "description": "Une box pour les amateurs de bricolage ou de création.", "price": "30€", "image": "https://via.placeholder.com/150"},
    #{"name": "Ebook Kindle", "description": "Un cadeau pour les passionnés de lecture.", "price": "100€", "image": "https://via.placeholder.com/150"},
    #{"name": "Coffret spa", "description": "Un moment de détente avec un coffret spa à domicile.", "price": "80€", "image": "https://via.placeholder.com/150"},
]

#def generate_recommendations(budget_min, budget_max, category=None):
    """
  #  Filters the gift database based on budget and optional category.
   # """
    #results = []
   # for gift in gift_database:
        # Extract price and filter based on budget
     #   price = float(gift["price"].replace("€", "").replace(",", "").replace(" ", ""))
      #  if budget_min <= price <= budget_max:
       #     if not category or category.lower() in gift["description"].lower():
        #        results.append(gift)
#    return results[:4]  # Return the top 4 results