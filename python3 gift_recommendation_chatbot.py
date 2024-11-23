import gradio as gr
import random

# Simulated database of gift recommendations
gift_database = [
    {"name": "Montre connectée", "description": "Une montre moderne pour suivre ses activités.", "price": "150€", "image": "https://via.placeholder.com/150"},
    {"name": "Abonnement Spotify", "description": "Un cadeau parfait pour les amateurs de musique.", "price": "9,99€/mois", "image": "https://via.placeholder.com/150"},
    {"name": "Coffret de vin", "description": "Un coffret avec des vins soigneusement sélectionnés.", "price": "60€", "image": "https://via.placeholder.com/150"},
    {"name": "Box DIY", "description": "Une box pour les amateurs de bricolage ou de création.", "price": "30€", "image": "https://via.placeholder.com/150"},
    {"name": "Ebook Kindle", "description": "Un cadeau pour les passionnés de lecture.", "price": "100€", "image": "https://via.placeholder.com/150"},
    {"name": "Coffret spa", "description": "Un moment de détente avec un coffret spa à domicile.", "price": "80€", "image": "https://via.placeholder.com/150"},
]

# Function to generate 4 random gift recommendations
def generate_recommendations(user_input):
    # Simulate recommendation logic
    suggestions = random.sample(gift_database, 4)
    results = []
    for gift in suggestions:
        results.append(f"**{gift['name']}**\n{gift['description']}\n**Prix**: {gift['price']}\n![Image]({gift['image']})")
    return "\n\n".join(results)

# Chatbot logic
def chatbot(user_input, chat_history):
    # Example of chatbot's interpretation of input
    if "anniversaire" in user_input.lower():
        response = "C'est un cadeau pour un anniversaire ? Quels sont les centres d'intérêt de la personne ?"
    elif "budget" in user_input.lower():
        response = "Quel est le budget que vous envisagez pour ce cadeau ?"
    else:
        response = "Merci pour les informations ! Voici quelques recommandations :"
        response += "\n\n" + generate_recommendations(user_input)
    chat_history.append((user_input, response))
    return "", chat_history

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🎁 Chatbot Recommandation de Cadeaux")
    gr.Markdown(
        "Interagissez avec le chatbot pour décrire la personne, ses centres d'intérêt, le budget, et le contexte du cadeau."
    )
    
    chat_history = gr.Chatbot(label="Historique du Chat")
    user_input = gr.Textbox(label="Votre message", placeholder="Décrivez la personne ou posez une question...")
    
    with gr.Row():
        submit_button = gr.Button("Envoyer")
        reset_button = gr.Button("Réinitialiser")
    
    submit_button.click(chatbot, [user_input, chat_history], [user_input, chat_history])
    reset_button.click(lambda: [], None, chat_history)

# Launch app
demo.launch(server_port=7861)