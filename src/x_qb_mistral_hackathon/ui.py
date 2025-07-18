import streamlit as st
from x_qb_mistral_hackathon.data_loader import DataLoader

class UI:
    @staticmethod
    def set_page_config():
        """Configure la page Streamlit."""
        st.set_page_config(
            page_title="KdostraI - Assistant Cadeaux",
            page_icon="🎁",
            layout="centered"
        )

    @staticmethod
    def display_header():
        """Affiche le header de l'application."""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://i.imgur.com/jhYA0PZ.png", width=300)

    @staticmethod
    def display_filters(session_state):
        """Affiche les filtres de recherche."""
        if st.button("Plus de filtres", key="toggle_filters"):
            session_state.show_filters = not session_state.show_filters

        if session_state.show_filters:
            st.markdown("### Filtres avancés :")

            session_state.price_range = st.slider(
                "Sélectionnez une plage de prix (€)",
                0, 10_000, session_state.price_range, step=50
            )

            session_state.gift_type = st.selectbox(
                "Choisissez un type de cadeau",
                [
                    None,
                    "Objet physique (livre, gadget, vêtement, etc.)",
                    "Expérience (billet de concert, cours de cuisine, abonnement, etc.)",
                    "Cadeau personnalisé (objet gravé, photo personnalisée, etc.)"
                ],
            )

    @staticmethod
    def display_categories(data_loader):
        """Affiche les catégories disponibles."""
        try:
            categories = data_loader.get_categories()
            if categories['main_categories']:
                st.sidebar.markdown("### Catégories")
                selected = st.sidebar.multiselect(
                    "Filtrer par catégorie",
                    options=categories['main_categories']
                )
                return selected
        except Exception as e:
            st.sidebar.warning("Impossible de charger les catégories")
            return []

    @staticmethod
    def display_price_filter(data_loader):
        """Affiche le filtre de prix."""
        try:
            min_price, max_price = data_loader.get_price_range()
            st.sidebar.markdown("### Prix")
            price_range = st.sidebar.slider(
                "Fourchette de prix (€)",
                min_value=float(min_price),
                max_value=float(max_price),
                value=(float(min_price), float(max_price))
            )
            return price_range
        except Exception as e:
            st.sidebar.warning("Impossible de charger les prix")
            return (0, 10_000)

    @staticmethod
    def display_error(message: str):
        """Affiche un message d'erreur."""
        st.error(message)

    @staticmethod
    def display_success(message: str):
        """Affiche un message de succès."""
        st.success(message)

    @staticmethod
    def display_info(message: str):
        """Affiche un message d'information."""
        st.info(message)

    @staticmethod
    def display_warning(message: str):
        """Affiche un message d'avertissement."""
        st.warning(message)

    @staticmethod
    def display_chatbot_button():
        """Affiche le bouton pour obtenir des idées de cadeaux."""
        # Create a single column that spans the entire width
        col = st.columns([1])[0]

        # Center the button within the column using HTML/CSS
        with col:
            st.markdown(
                """
                <div style="display: flex; justify-content: center;">
                    <button style="background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                        Give me your ideas
                    </button>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Check if the button is clicked
            if st.button("Give me your ideas", key="chatbot_button"):
                st.session_state.chatbot_prompt = "Give me your recommendations now"
