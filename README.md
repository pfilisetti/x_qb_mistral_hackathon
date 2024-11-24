# ChatBot Kdostral

## Objectif principal

Ce projet vise à créer une web application permettant d'aider les utilisateurs à trouver des idées cadeaux pour leurs proches. Grâce à un chatbot, l'utilisateur pourra interagir avec le système pour affiner sa recherche de cadeau en répondant à plusieurs questions. Le chatbot, basé sur un modèle de conversation, recommendera ensuite les 4 cadeaux les plus pertinents issus d'une base de données, et l'utilisateur pourra les ajouter à sa liste d'envies. La discussion continuera ensuite pour affiner les offres de cadeaux proposées à l'utilisateur.

## Fonctionnalités

1. **Page d'accueil :** L'utilisateur arrive sur une page simple avec une brève présentation du service et une barre de chat pour démarrer une conversation. Le chatbot initie la conversation en invitant l'utilisateur à présenter son problème.
2. **Interaction avec le Chatbot :**
   - L'utilisateur décrit brièvement son idée de cadeau ou ses préférences.
   - Le chatbot pose une série de questions pour mieux comprendre les besoins de l'utilisateur (ex: prix, catégorie, préférences).
   - Sur la base des réponses données, le chatbot génère un / plusieurs tags afin de pouvoir filtrer la base de donnée de produits selon les besoins de l'utilisateur:
   (ex: "Je cherche un cadeau pour ma grand-mère de 70 ans qui aime cuisiner. Elle adore voyager.
        - tags: cuisiner, grand-mère, 70 ans, voyager)
2. **Recherche de produits correspondants :**
   - Une fois les tags obtenus après la phase de discussion, un agent est chargé d'explorer la base de données filtrée selon les tags identifiés afin d'en réduire sa taille et de permettre une exploration sans long temps d'attente.
   - L'agent sélectionne ensuite les produits les plus cohérents avec le besoin exprimé par l'utilisateur et lui présente les différents produits en justifiant ses choix.
   (ex: "Un cadeau original pour votre mère serait 'LIVRE DE RECETTES DU MONDE'"
        "D'autre suggestions seraient ...., ...., ...")
3. **Génération d'images :** Pour chaque idée cadeau proposée, une image est générée, permettant à l'utilisateur de visualiser les produits recommandés sur la webapp. Le lien d'accès à cette image doit figurer dans la base de données.
4. **Ajout à la liste d'envie :** L'utilisateur peut sélectionner et ajouter des cadeaux à sa liste d'envies. Il peut aussi choisir d'affiner la recherche en demandant au chatbot de générer de nouveaux exemples.
5. **Commande pour de nouveaux exemples :** Si l'utilisateur souhaite explorer d'autres options, il peut demander 4 nouveaux exemples de cadeaux en utilisant continuant sa discussion avec le premier agent afin d'affiner les tags.

## Fonctionnement du projet par sections :

**Embedding** : la section embedding prend en entrée le fichier data_gifts.csv, dans lequel est stocké le catalogue de produits proposés (nom, catégorie, note, prix). En utilisant la fonction embedding, on facilite l'exploitation de la colonne "sub_category". Le premier agent génère un certain nombre de labels, résumés en un label principal (compris dans les valeurs de la colonne "sub_category"). Cette information est utilisée afin de faire ressortir les produits correspondants à cette sous-catégorie, ainsi que ceux appartenant aux deux sous-catégories les plus proches du label. Enfin, l'information "customer_budget" permet d'éliminer les produits trop onéreux. Le second agent prendra cette table en entrée ainsi que les labels générés par le premier agent pour formuler quatre recommandations.

### Architecture
- **ChatBot** : Le chatbot interagit avec l'utilisateur en posant des questions ciblées pour mieux comprendre ses besoins. Après plusieurs questions, il génère des suggestions basées sur une liste de produits.
- **Base de données des produits** : La base de données contient des informations détaillées sur chaque produit : prix, catégorie, nom, description, et évaluations. Le chatbot utilise cette base pour sélectionner les produits les plus appropriés en fonction des réponses de l'utilisateur.
- **Liste d'envies** : L'utilisateur peut ajouter des produits à sa liste d'envies, ce qui lui permet de garder une trace des idées de cadeaux intéressantes.

### Technologies utilisées
- **Streamlit** : Utilisé pour créer l'interface web interactive et gérer l'affichage du chatbot.
- **Python** : Langage principal pour la logique du backend.
- **Pandas** : Utilisé pour la gestion des données des produits.
- **Modèle de ChatBot (Mistral)** : Utilisé pour générer les questions et suggestions de produits.
