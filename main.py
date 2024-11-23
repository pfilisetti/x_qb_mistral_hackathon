import os
import sys
from pathlib import Path

# Obtenir le chemin absolu du répertoire racine du projet
ROOT_DIR = Path(__file__).resolve().parent

# Ajouter le répertoire racine au sys.path s'il n'y est pas déjà
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import gradio as gr
from ui import build_ui

if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_port=7870)