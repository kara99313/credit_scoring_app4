"""
Pages package for Credit Scoring Dashboard
==========================================
Contient toutes les pages de l'application Streamlit multi-pages
"""

__version__ = "1.0.0"
__author__ = "Équipe Data Science"

# Pages disponibles dans l'application
AVAILABLE_PAGES = [
    "01_🏠_Accueil.py",
    "02_🎯_Prediction.py", 
    "03_📊_Dashboard.py",
    "04_📖_Documentation.py"
]

# Metadata des pages
PAGES_METADATA = {
    "01_🏠_Accueil.py": {
        "title": "Accueil",
        "icon": "🏠",
        "description": "Vue d'ensemble et métriques principales"
    },
    "02_🎯_Prediction.py": {
        "title": "Prédiction",
        "icon": "🎯", 
        "description": "Interface d'analyse du risque crédit"
    },
    "03_📊_Dashboard.py": {
        "title": "Dashboard",
        "icon": "📊",
        "description": "Monitoring et analytics avancés"
    },
    "04_📖_Documentation.py": {
        "title": "Documentation",
        "icon": "📖",
        "description": "Guides utilisateur et administrateur"
    }
} 