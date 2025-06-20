"""
⚙️ CONFIGURATION - Paramètres de l'application
==============================================
Fichier de configuration centralisé pour l'application Streamlit
"""

import os
from pathlib import Path
from typing import Dict, Any

# ============================================================================
# CONFIGURATION GÉNÉRALE
# ============================================================================

APP_CONFIG = {
    "name": "Credit Scoring Dashboard",
    "version": "1.0.0",
    "description": "Système intelligent d'évaluation du risque crédit",
    "author": "Équipe Data Science",
    "contact": {
        "support": "support@creditscoring.com",
        "admin": "admin@creditscoring.com",
        "dev": "dev@creditscoring.com"
    }
}

# ============================================================================
# CHEMINS ET DOSSIERS
# ============================================================================

# Chemin racine du projet
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Chemins vers les dossiers importants
PATHS = {
    "project_root": PROJECT_ROOT,
    "streamlit_app": PROJECT_ROOT / "streamlit_app",
    "modeling": PROJECT_ROOT / "modeling",
    "models": PROJECT_ROOT / "modeling" / "models",
    "final_models": PROJECT_ROOT / "modeling" / "models" / "final_models",
    "data": PROJECT_ROOT / "data",
    "processed_data": PROJECT_ROOT / "data" / "processed",
    "reports": PROJECT_ROOT / "reports",
    "logs": PROJECT_ROOT / "logs",
    "assets": PROJECT_ROOT / "streamlit_app" / "assets"
}

# ============================================================================
# CONFIGURATION STREAMLIT
# ============================================================================

STREAMLIT_CONFIG = {
    "page_title": "Credit Scoring Dashboard",
    "page_icon": "🏆",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "theme": {
        "primaryColor": "#1f77b4",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#262730"
    }
}

# ============================================================================
# CONFIGURATION MODÈLE
# ============================================================================

MODEL_CONFIG = {
    "model_type": "XGBoost",
    "version": "1.0.0",
    "auc_score": 0.8060,
    "threshold_default": 0.52,
    "cache_ttl": 3600,  # 1 heure
}

# =============================================================================
# LOGIQUES MÉTIER CREDIT SCORING
# =============================================================================

# Score sur 1000 et classes de risque
SCORING_CONFIG = {
    "score_max": 1000,
    "score_min": 0,
    "threshold_probability": 0.52,  # Seuil probabilité de défaut
}

# Classes de risque selon normes Bâle III
RISK_CLASSES = {
    "AAA": {"range": (950, 1000), "color": "#00C851", "description": "Risque minimal", "default_rate": "< 0.1%"},
    "AA": {"range": (900, 949), "color": "#2BBBAD", "description": "Très faible risque", "default_rate": "0.1% - 0.3%"},
    "A": {"range": (800, 899), "color": "#4285F4", "description": "Faible risque", "default_rate": "0.3% - 1%"},
    "BBB": {"range": (650, 799), "color": "#FF8F00", "description": "Risque modéré", "default_rate": "1% - 5%"},
    "BB": {"range": (500, 649), "color": "#FF6F00", "description": "Risque élevé", "default_rate": "5% - 15%"},
    "B": {"range": (350, 499), "color": "#F44336", "description": "Très haut risque", "default_rate": "15% - 30%"},
    "CCC": {"range": (200, 349), "color": "#D32F2F", "description": "Risque critique", "default_rate": "30% - 50%"},
    "D": {"range": (0, 199), "color": "#B71C1C", "description": "Défaut quasi-certain", "default_rate": "> 50%"}
}

# Notation client (rating interne)
CLIENT_RATINGS = {
    "PREMIUM": {"score_min": 850, "benefits": "Taux préférentiel, limite élevée", "color": "#FFD700"},
    "EXCELLENT": {"score_min": 750, "benefits": "Conditions avantageuses", "color": "#00C851"},
    "GOOD": {"score_min": 650, "benefits": "Conditions standard", "color": "#4285F4"},
    "STANDARD": {"score_min": 500, "benefits": "Surveillance renforcée", "color": "#FF8F00"},
    "SUBPRIME": {"score_min": 350, "benefits": "Conditions restrictives", "color": "#F44336"},
    "HIGH_RISK": {"score_min": 0, "benefits": "Refus recommandé", "color": "#B71C1C"}
}

# Décisions finales
DECISION_MATRIX = {
    "APPROVED": {
        "score_threshold": 520,
        "color": "#00C851",
        "icon": "✅",
        "message": "Crédit approuvé",
        "confidence": "Élevée"
    },
    "CONDITIONAL": {
        "score_threshold": 400,
        "color": "#FF8F00", 
        "icon": "⚠️",
        "message": "Approbation conditionnelle",
        "confidence": "Modérée"
    },
    "REJECTED": {
        "score_threshold": 0,
        "color": "#F44336",
        "icon": "❌", 
        "message": "Crédit refusé",
        "confidence": "Élevée"
    }
}

# =============================================================================
# INDICATEURS DE PERFORMANCE
# =============================================================================

KPI_DEFINITIONS = {
    "auc_score": {
        "name": "AUC Score",
        "description": "Area Under Curve - Mesure la capacité discriminante du modèle",
        "target": 0.80,
        "excellent": 0.85,
        "format": "percentage",
        "interpretation": {
            "> 0.85": "Performance excellente",
            "0.80-0.85": "Performance très bonne", 
            "0.70-0.80": "Performance acceptable",
            "< 0.70": "Performance insuffisante"
        }
    },
    "precision": {
        "name": "Précision",
        "description": "Proportion de vrais positifs parmi les prédictions positives",
        "target": 0.75,
        "format": "percentage"
    },
    "recall": {
        "name": "Rappel",
        "description": "Proportion de vrais positifs correctement identifiés",
        "target": 0.70,
        "format": "percentage"
    },
    "f1_score": {
        "name": "F1-Score",
        "description": "Moyenne harmonique entre précision et rappel",
        "target": 0.72,
        "format": "percentage"
    },
    "gini_coefficient": {
        "name": "Coefficient de Gini",
        "description": "Mesure de discrimination (2*AUC - 1)",
        "target": 0.60,
        "format": "percentage"
    }
}

# =============================================================================
# CONFIGURATION UI ET ESTHÉTIQUE PROFESSIONNELLE
# =============================================================================

# Palette de couleurs professionnelle internationale
COLOR_PALETTE = {
    "primary": "#1E3A8A",        # Bleu professionnel
    "secondary": "#059669",       # Vert business
    "accent": "#DC2626",         # Rouge alerte
    "warning": "#D97706",        # Orange attention
    "info": "#0891B2",           # Cyan information
    "success": "#065F46",        # Vert succès
    "background": "#F8FAFC",     # Gris très clair
    "surface": "#FFFFFF",        # Blanc pur
    "text_primary": "#1F2937",   # Gris foncé
    "text_secondary": "#6B7280", # Gris moyen
    "border": "#E5E7EB"          # Gris bordure
}

# Style CSS professionnel
PROFESSIONAL_CSS = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Variables CSS globales */
:root {
    --primary-color: #1E3A8A;
    --secondary-color: #059669;
    --accent-color: #DC2626;
    --warning-color: #D97706;
    --info-color: #0891B2;
    --success-color: #065F46;
    --background-color: #F8FAFC;
    --surface-color: #FFFFFF;
    --text-primary: #1F2937;
    --text-secondary: #6B7280;
    --border-color: #E5E7EB;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Reset et base */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Typography */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
}

/* Sidebar professionnelle */
.css-1d391kg {
    background: linear-gradient(145deg, var(--primary-color), #1E40AF);
}

.css-1d391kg .css-17lntkn {
    color: white;
    font-weight: 500;
}

/* Cards et containers */
.metric-card {
    background: var(--surface-color);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border-color);
    transition: all 0.2s ease;
}

.metric-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

.risk-card {
    background: var(--surface-color);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: var(--shadow-lg);
    border-left: 4px solid var(--primary-color);
    margin: 1rem 0;
}

/* Buttons et interactions */
.stButton > button {
    background: linear-gradient(145deg, var(--primary-color), #1E40AF);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 500;
    transition: all 0.2s ease;
    box-shadow: var(--shadow);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* Status indicators */
.status-excellent {
    background: linear-gradient(135deg, #10B981, #059669);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    text-align: center;
}

.status-good {
    background: linear-gradient(135deg, #3B82F6, #2563EB);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    text-align: center;
}

.status-warning {
    background: linear-gradient(135deg, #F59E0B, #D97706);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    text-align: center;
}

.status-danger {
    background: linear-gradient(135deg, #EF4444, #DC2626);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    text-align: center;
}

/* Progress bars */
.progress-container {
    background: #E5E7EB;
    border-radius: 10px;
    overflow: hidden;
    height: 8px;
    margin: 0.5rem 0;
}

.progress-bar {
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translate3d(0, 30px, 0);
    }
    to {
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

/* Responsive design */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .metric-card {
        padding: 1rem;
    }
    
    .risk-card {
        padding: 1.5rem;
    }
}

/* Graphiques Plotly */
.js-plotly-plot {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

/* Formulaires */
.stSelectbox > div > div {
    border-radius: 8px;
    border: 2px solid var(--border-color);
}

.stTextInput > div > div > input {
    border-radius: 8px;
    border: 2px solid var(--border-color);
}

/* Alertes personnalisées */
.alert-success {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    border-left: 4px solid var(--success-color);
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.alert-warning {
    background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
    border-left: 4px solid var(--warning-color);
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.alert-danger {
    background: linear-gradient(135deg, #FEF2F2, #FECACA);
    border-left: 4px solid var(--accent-color);
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}
</style>
"""

# Configuration des graphiques Plotly
PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ['pan2d', 'lasso2d'],
    "responsive": True
}

PLOTLY_LAYOUT = {
    "font": {"family": "Inter, sans-serif"},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "colorway": [COLOR_PALETTE["primary"], COLOR_PALETTE["secondary"], 
                 COLOR_PALETTE["accent"], COLOR_PALETTE["warning"]],
    "margin": {"l": 50, "r": 50, "t": 50, "b": 50}
}

# ============================================================================
# CONFIGURATION INTERFACE
# ============================================================================

UI_CONFIG = {
    "colors": {
        "primary": "#1f77b4",
        "success": "#2ca02c",
        "warning": "#ff7f0e",
        "danger": "#d62728",
        "info": "#17a2b8",
        "light": "#f8f9fa",
        "dark": "#343a40"
    },
    "messages": {
        "welcome": "Bienvenue dans le Credit Scoring Dashboard",
        "loading": "Chargement en cours...",
        "error": "Une erreur s'est produite",
        "success": "Opération réussie",
        "no_data": "Aucune donnée disponible"
    },
    "limits": {
        "age_min": 18,
        "age_max": 100,
        "credit_min": 100,
        "credit_max": 100000,
        "duration_min": 1,
        "duration_max": 120,
        "income_min": 500,
        "income_max": 50000
    }
}

# ============================================================================
# CONFIGURATION DASHBOARD
# ============================================================================

DASHBOARD_CONFIG = {
    "refresh_interval": 30,  # secondes
    "max_alerts": 10,
    "alert_retention": 24,   # heures
    "chart_height": 400,
    "kpi_refresh": 60,       # secondes
}

# ============================================================================
# CONFIGURATION LOGGING
# ============================================================================

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": {
        "file": {
            "filename": PATHS["logs"] / "streamlit_app.log",
            "max_bytes": 10485760,  # 10MB
            "backup_count": 5
        },
        "console": {
            "enabled": True
        }
    }
}

# ============================================================================
# CONFIGURATION SÉCURITÉ
# ============================================================================

SECURITY_CONFIG = {
    "rate_limit": 100,       # requêtes par minute
    "session_timeout": 3600, # secondes
    "max_file_size": 10,     # MB
    "allowed_file_types": [".csv", ".xlsx"],
    "log_level": "INFO",
}

# ============================================================================
# VARIABLES D'ENVIRONNEMENT
# ============================================================================

def get_env_config() -> Dict[str, Any]:
    """
    Récupère la configuration depuis les variables d'environnement
    """
    return {
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "cache_enabled": os.getenv("CACHE_ENABLED", "True").lower() == "true",
        "model_path": os.getenv("MODEL_PATH", str(PATHS["models"] / "best_model.pkl")),
        "data_path": os.getenv("DATA_PATH", str(PATHS["processed_data"])),
        "port": int(os.getenv("STREAMLIT_PORT", "8501")),
        "host": os.getenv("STREAMLIT_HOST", "localhost")
    }

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def get_full_config() -> Dict[str, Any]:
    """
    Retourne la configuration complète de l'application
    """
    return {
        "app": APP_CONFIG,
        "paths": {k: str(v) for k, v in PATHS.items()},
        "streamlit": STREAMLIT_CONFIG,
        "model": MODEL_CONFIG,
        "ui": UI_CONFIG,
        "dashboard": DASHBOARD_CONFIG,
        "logging": LOGGING_CONFIG,
        "security": SECURITY_CONFIG,
        "environment": get_env_config()
    }

def validate_config() -> bool:
    """
    Valide la configuration et vérifie les chemins
    """
    try:
        # Vérifier les chemins critiques
        critical_paths = ["project_root", "streamlit_app", "modeling"]
        for path_name in critical_paths:
            path = PATHS[path_name]
            if not path.exists():
                print(f"⚠️ Chemin manquant: {path_name} -> {path}")
                return False
        
        # Vérifier les dossiers de logs
        PATHS["logs"].mkdir(exist_ok=True)
        
        # Vérifier les assets
        PATHS["assets"].mkdir(exist_ok=True)
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur validation config: {str(e)}")
        return False

# =============================================================================
# FONCTIONS UTILITAIRES MÉTIER
# =============================================================================

def get_risk_class(score: float) -> Dict[str, Any]:
    """Retourne la classe de risque basée sur le score."""
    for class_name, config in RISK_CLASSES.items():
        if config["range"][0] <= score <= config["range"][1]:
            return {
                "class": class_name,
                "description": config["description"],
                "color": config["color"],
                "default_rate": config["default_rate"],
                "range": config["range"]
            }
    return RISK_CLASSES["D"]  # Par défaut

def get_client_rating(score: float) -> Dict[str, Any]:
    """Retourne la notation client basée sur le score."""
    for rating, config in CLIENT_RATINGS.items():
        if score >= config["score_min"]:
            return {
                "rating": rating,
                "benefits": config["benefits"],
                "color": config["color"],
                "score_min": config["score_min"]
            }
    return CLIENT_RATINGS["HIGH_RISK"]  # Par défaut

def get_final_decision(score: float) -> Dict[str, Any]:
    """Retourne la décision finale basée sur le score."""
    for decision, config in DECISION_MATRIX.items():
        if score >= config["score_threshold"]:
            return {
                "decision": decision,
                "message": config["message"],
                "color": config["color"],
                "icon": config["icon"],
                "confidence": config["confidence"],
                "threshold": config["score_threshold"]
            }
    return DECISION_MATRIX["REJECTED"]  # Par défaut

def probability_to_score(probability: float) -> int:
    """Convertit une probabilité de défaut en score sur 1000."""
    # Transformation inverse : plus la probabilité de défaut est élevée, plus le score est bas
    score = int((1 - probability) * SCORING_CONFIG["score_max"])
    return max(SCORING_CONFIG["score_min"], min(SCORING_CONFIG["score_max"], score))

def score_to_probability(score: int) -> float:
    """Convertit un score sur 1000 en probabilité de défaut."""
    return 1 - (score / SCORING_CONFIG["score_max"])

def print_config_summary():
    """
    Affiche un résumé de la configuration
    """
    env_config = get_env_config()
    
    print("🔧 CONFIGURATION STREAMLIT APP")
    print("=" * 50)
    print(f"📱 Application: {APP_CONFIG['name']} v{APP_CONFIG['version']}")
    print(f"🌍 Environnement: {env_config['environment']}")
    print(f"🏠 Projet: {PATHS['project_root']}")
    print(f"🤖 Modèles: {PATHS['models']}")
    print(f"📊 Données: {PATHS['processed_data']}")
    print(f"🎯 Seuil décision: {MODEL_CONFIG['threshold_default']}")
    print(f"📈 AUC cible: {MODEL_CONFIG['auc_score']}")
    print(f"🖥️ Host:Port: {env_config['host']}:{env_config['port']}")
    print("=" * 50)

# Test de la configuration au chargement
if __name__ == "__main__":
    print_config_summary()
    if validate_config():
        print("✅ Configuration validée avec succès")
    else:
        print("❌ Erreurs dans la configuration")