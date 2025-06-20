# 💳 Credit Scoring System

Un système complet de credit scoring utilisant la régression logistique avec des pipelines ML robustes et une interface utilisateur interactive.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table des Matières

- [Aperçu du Projet](#aperçu-du-projet)
- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Configuration](#configuration)
- [Développement](#développement)
- [Déploiement](#déploiement)
- [Documentation](#documentation)

## 🎯 Aperçu du Projet

Le **Credit Scoring System** est une solution complète de machine learning pour l'évaluation du risque de crédit. Il comprend :

### 🔧 **Partie 1 : Pipeline ML & API**
- **Pipeline de données** complet (ETL, nettoyage, validation)
- **Feature Engineering** avancé avec techniques métier
- **Modèle de régression logistique** optimisé avec hyperparamètres
- **API REST FastAPI** pour scoring temps réel
- **MLOps** complet avec CI/CD, monitoring et versioning

### 🖥️ **Partie 2 : Application Interactive**
- **Interface Streamlit** intuitive pour les utilisateurs métier
- **Moteur de scoring** en temps réel
- **Génération de rapports PDF** professionnels
- **Analytics avancés** : analyse de sensibilité, simulations

## 🏗️ Architecture

```mermaid
graph TD
    A[Raw Data] --> B[Data Pipeline]
    B --> C[Feature Engineering]
    C --> D[Model Training]
    D --> E[Model Registry]
    E --> F[API Service]
    E --> G[Streamlit App]
    F --> H[Predictions]
    G --> I[Reports & Analytics]
    
    subgraph "MLOps"
        J[MLflow Tracking]
        K[Model Monitoring]
        L[CI/CD Pipeline]
    end
    
    D --> J
    F --> K
    G --> K
```

## 🚀 Installation

### Prérequis

- Python 3.8+
- Git
- 4GB RAM minimum
- Windows/macOS/Linux

### Installation Rapide

```bash
# 1. Cloner le repository
git clone <repository-url>
cd credit_scoring_project

# 2. Créer l'environnement virtuel
python -m venv credit_scoring_env

# 3. Activer l'environnement virtuel
# Windows
credit_scoring_env\Scripts\activate
# macOS/Linux
source credit_scoring_env/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Vérifier l'installation
python main.py status
```

## 📊 Utilisation

### Commandes Principales

```bash
# Interface en ligne de commande
python main.py --help

# Pipeline complet (recommandé pour commencer)
python main.py full-pipeline

# Étapes individuelles
python main.py process-data      # Traitement des données
python main.py train-model       # Entraînement du modèle
python main.py run-api          # Démarrer l'API
python main.py run-app          # Démarrer Streamlit
python main.py run-mlflow       # Interface MLflow

# Prédictions
python main.py predict --input-data data/new_clients.csv
```

### 🔥 Démarrage Rapide

```bash
# 1. Traiter les données et entraîner le modèle
python main.py full-pipeline

# 2. Dans un nouveau terminal - Démarrer l'API
python main.py run-api

# 3. Dans un autre terminal - Démarrer l'app
python main.py run-app

# 4. Accéder aux interfaces
# - API Docs: http://localhost:8000/docs
# - Streamlit: http://localhost:8501
# - MLflow: http://localhost:5000
```

## 📁 Structure du Projet

```
credit_scoring_project/
├── 📁 config/                    # Configuration
│   ├── config.yaml              # Configuration principale
│   └── logging_config.yaml      # Configuration logging
├── 📁 data/                     # Données
│   ├── raw/                     # Données brutes
│   ├── processed/               # Données traitées
│   └── external/                # Données externes
├── 📁 src/                      # Code source principal
│   ├── __init__.py
│   ├── data_processing.py       # Traitement des données
│   ├── feature_engineering.py  # Ingénierie des features
│   ├── modeling.py             # Modélisation ML
│   ├── backtesting.py          # Validation temporelle
│   └── utils.py                # Utilitaires
├── 📁 pipelines/               # Pipelines ML
│   ├── data_pipeline.py        # Pipeline de données
│   ├── training_pipeline.py    # Pipeline d'entraînement
│   ├── inference_pipeline.py   # Pipeline d'inférence
│   └── monitoring_pipeline.py  # Pipeline de monitoring
├── 📁 api_service/             # Service API REST
│   ├── app.py                  # Application FastAPI
│   ├── endpoints/              # Points de terminaison
│   ├── models/                 # Modèles Pydantic
│   ├── schemas/                # Schémas de données
│   ├── services/               # Services métier
│   └── middleware/             # Middleware
├── 📁 streamlit_app/           # Application Streamlit
│   ├── app.py                  # Application principale
│   ├── pages/                  # Pages de l'app
│   ├── components/             # Composants réutilisables
│   └── utils/                  # Utilitaires Streamlit
├── 📁 models/                  # Modèles entraînés
├── 📁 logs/                    # Logs système
├── 📁 notebooks/               # Notebooks Jupyter
├── 📁 tests/                   # Tests
├── 📁 deployment/              # Configuration déploiement
│   ├── docker-compose.yml
│   ├── Dockerfile.api
│   └── Dockerfile.streamlit
├── main.py                     # Point d'entrée principal
├── requirements.txt            # Dépendances Python
└── README.md                   # Documentation
```

## ⚙️ Configuration

### Configuration Principale (`config/config.yaml`)

```yaml
# Exemple de configuration
model:
  algorithm: "logistic_regression"
  hyperparameters:
    C: [0.001, 0.01, 0.1, 1, 10, 100]
    penalty: ["l1", "l2"]
    
scoring:
  score_range:
    min: 300
    max: 850
  risk_classes:
    very_low: [750, 850]
    low: [650, 749]
    medium: [550, 649]
    high: [450, 549]
    very_high: [300, 449]
```

### Variables d'Environnement

Créer un fichier `.env` :

```bash
# Base
ENVIRONMENT=development
LOG_LEVEL=INFO

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database (optionnel)
DATABASE_URL=postgresql://user:pass@localhost/credit_scoring

# MLflow
MLFLOW_TRACKING_URI=http://localhost:5000
```

## 🧪 Développement

### Tests

```bash
# Exécuter tous les tests
pytest

# Tests avec couverture
pytest --cov=src

# Tests spécifiques
pytest tests/test_data_processing.py
```

### Qualité du Code

```bash
# Formatage du code
black src/

# Linting
flake8 src/

# Type checking
mypy src/
```

### Pre-commit Hooks

```bash
# Installer pre-commit
pip install pre-commit

# Configurer les hooks
pre-commit install

# Exécuter manuellement
pre-commit run --all-files
```

## 🚀 Déploiement

### Docker

```bash
# Construire les images
docker-compose build

# Démarrer les services
docker-compose up -d

# Vérifier le statut
docker-compose ps
```

### Kubernetes

```bash
# Déployer sur Kubernetes
kubectl apply -f deployment/

# Vérifier le déploiement
kubectl get pods -n credit-scoring
```

### Production

```bash
# Configuration production
export ENVIRONMENT=production

# Démarrer avec Gunicorn
gunicorn api_service.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## 📚 API Documentation

### Endpoints Principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/predict` | POST | Prédiction individuelle |
| `/batch-predict` | POST | Prédiction en lot |
| `/model/info` | GET | Information sur le modèle |
| `/health` | GET | Statut de santé |

### Exemple d'Utilisation

```python
import requests

# Prédiction individuelle
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "age": 35,
        "income": 50000,
        "debt_to_income": 0.3,
        "credit_history_length": 10
    }
)

result = response.json()
print(f"Score: {result['score']}")
print(f"Risk Class: {result['risk_class']}")
```

## 📈 Monitoring & Observabilité

### Métriques Disponibles

- **Performance du modèle** : AUC, Précision, Rappel, F1-Score
- **Dérive des données** : PSI, Distribution shifts
- **Métriques système** : Latence, Throughput, Erreurs
- **Métriques métier** : Taux d'approbation, Rentabilité

### Alertes

```yaml
# Configuration des alertes
alerts:
  model_performance:
    auc_threshold: 0.7
    precision_threshold: 0.6
  
  data_drift:
    psi_threshold: 0.1
    
  system:
    latency_threshold: 500ms
    error_rate_threshold: 0.05
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push sur la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📝 Changelog

### Version 1.0.0 (2024-12-XX)
- ✨ Pipeline ML complet avec régression logistique
- 🚀 API REST FastAPI avec documentation automatique
- 📊 Application Streamlit interactive
- 🔧 Configuration flexible et modulaire
- 📈 Monitoring et observabilité
- 🐳 Containerisation Docker
- 🧪 Tests automatisés avec CI/CD

## 📄 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

Pour obtenir de l'aide :

1. 📖 Consultez cette documentation
2. 🐛 Ouvrez une [issue](issues) pour reporter un bug
3. 💬 Rejoignez notre [Discord](discord-link) pour discuter
4. 📧 Contactez l'équipe : team@creditscore.com

---

**Fait avec ❤️ par l'équipe Credit Scoring**

*Système de credit scoring professionnel pour l'industrie financière* 