def chatbot_response(user_input, chat_history):
    """
    Gère l'entrée utilisateur et génère une réponse simple.
    - user_input : Message de l'utilisateur (texte).
    - chat_history : Historique des messages (liste de tuples).
    """
    # Logique de réponse simple
    if "anniversaire" in user_input.lower():
        response = "C'est un cadeau pour un anniversaire ? Quels sont les centres d'intérêt de la personne ?"
    elif "budget" in user_input.lower():
        response = "Quel est le budget que vous envisagez pour ce cadeau ?"
    else:
        response = "Merci pour les informations ! Voici quelques idées que je peux générer."

    # Ajouter à l'historique de chat
    chat_history.append((user_input, response))
    return "", chat_history