# ui.py
import streamlit as st

class UI:
    @staticmethod
    def set_page_config():
        st.set_page_config(
            page_title="KdostraI - Assistant Cadeaux",
            page_icon="🎁",
            layout="centered"
        )

    @staticmethod
    def load_css():
        st.markdown("""
            <style>
            /* Your CSS styles here */
            </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_header():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://i.imgur.com/jhYA0PZ.png", width=300)

    @staticmethod
    def display_filters(session_state):
        if st.button("Plus de filtres", key="toggle_filters"):
            session_state.show_filters = not session_state.show_filters
        
        if session_state.show_filters:
            st.markdown("### Filtres avancés :")
            
            session_state.price_range = st.slider(
                "Sélectionnez une plage de prix (€)",
                0, 1_000_000, session_state.price_range, step=50
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