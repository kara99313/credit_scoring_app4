"""
📖 PAGE DOCUMENTATION - Guide utilisateur et administrateur
==========================================================
Documentation complète pour utilisateurs et administrateurs
"""

import streamlit as st
import sys
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Documentation - Credit Scoring",
    page_icon="📖",
    layout="wide"
)

def show_user_guide():
    """Guide utilisateur"""
    st.markdown("""
    ## 👥 Guide Utilisateur Final
    
    ### 🚀 Démarrage Rapide
    
    #### 1. Accès à l'application
    - Ouvrez votre navigateur web
    - Connectez-vous à l'URL fournie par votre administrateur
    - L'interface s'affiche automatiquement
    
    #### 2. Navigation
    - **🏠 Accueil** : Vue d'ensemble et statistiques générales
    - **🎯 Prédiction** : Analyser le risque d'un client
    - **📊 Dashboard** : Surveillance des performances
    - **📖 Documentation** : Cette page d'aide
    
    ### 🎯 Faire une Prédiction
    
    #### Étape 1 : Saisir les informations client
    1. Cliquez sur "🎯 Prédiction" dans le menu
    2. Remplissez le formulaire avec les données du client :
       - **Informations personnelles** : âge, sexe, profession
       - **Situation financière** : revenus, épargne, comptes
       - **Demande de crédit** : montant, durée, objet
    
    #### Étape 2 : Analyser les résultats
    1. Cliquez sur "🎯 ANALYSER LE RISQUE"
    2. Attendez le traitement (< 2 secondes)
    3. Consultez les résultats :
       - **Score de risque** : 0-100 (plus élevé = plus risqué)
       - **Décision** : ACCORDÉ ou REFUSÉ
       - **Niveau de confiance** : Fiabilité de la prédiction
    
    #### Étape 3 : Interpréter les explications
    - **Graphique SHAP** : Impact de chaque variable
    - **Facteurs positifs** : Éléments favorables au dossier
    - **Points d'attention** : Éléments défavorables
    - **Recommandations** : Suggestions d'amélioration
    
    ### 📊 Utiliser le Dashboard
    
    #### Métriques principales
    - **AUC Modèle** : Performance globale (>0.75 = bon)
    - **Volume/Jour** : Nombre de prédictions quotidiennes
    - **Taux Accord** : Pourcentage de crédits accordés
    - **Temps Réponse** : Rapidité du système
    
    #### Graphiques de suivi
    - **Performance temporelle** : Évolution de la qualité
    - **Volume quotidien** : Activité du système
    - **Distribution scores** : Répartition des niveaux de risque
    - **Taux d'acceptation** : Tendance des décisions
    
    ### ❓ Questions Fréquentes
    
    **Q: Que signifie le score de crédit ?**
    R: Le score va de 0 à 100. Plus il est élevé, plus le risque de défaut est important. Le seuil de décision est fixé à 52.
    
    **Q: Comment interpréter les explications SHAP ?**
    R: Les barres vertes poussent vers l'acceptation, les rouges vers le refus. Plus la barre est longue, plus l'impact est important.
    
    **Q: Le système est-il sûr ?**
    R: Oui, toutes les données sont chiffrées et le modèle est conforme aux exigences réglementaires Bâle III.
    
    **Q: Que faire si j'ai une erreur ?**
    R: Vérifiez vos données saisies. Si le problème persiste, contactez le support technique.
    
    **Q: Puis-je faire plusieurs prédictions ?**
    R: Oui, il n'y a pas de limite. Cliquez sur "Nouvelle Analyse" pour recommencer.
    """)

def show_admin_guide():
    """Guide administrateur"""
    st.markdown("""
    ## 🔧 Guide Administrateur Système
    
    ### 🏗️ Architecture Technique
    
    #### Stack Technologique
    ```
    Frontend : Streamlit 1.28.0+
    Backend  : Python 3.9+
    Modèle   : XGBoost + Scikit-learn
    Cache    : Streamlit native cache
    Export   : Plotly, ReportLab, FPDF
    ```
    
    #### Structure des Fichiers
    ```
    streamlit_app/
    ├── main.py                    # Point d'entrée
    ├── pages/                     # Pages de l'application
    │   ├── 01_🏠_Accueil.py
    │   ├── 02_🎯_Prediction.py
    │   ├── 03_📊_Dashboard.py
    │   └── 04_📖_Documentation.py
    ├── utils/                     # Utilitaires
    │   ├── model_loader.py        # Chargement modèle
    │   └── data_processor.py      # Traitement données
    ├── components/                # Composants réutilisables
    ├── assets/                    # Ressources statiques
    └── requirements_streamlit.txt # Dépendances
    ```
    
    ### 🚀 Installation et Déploiement
    
    #### Prérequis Système
    - Python 3.9 ou supérieur
    - RAM : 4GB minimum, 8GB recommandé
    - Espace disque : 2GB minimum
    - Connexion internet pour les dépendances
    
    #### Installation Étape par Étape
    ```bash
    # 1. Cloner le projet
    git clone <repository-url>
    cd app_credit_scoring4/streamlit_app
    
    # 2. Créer environnement virtuel
    python -m venv streamlit_env
    
    # 3. Activer l'environnement
    # Windows:
    streamlit_env\\Scripts\\activate
    # Linux/Mac:
    source streamlit_env/bin/activate
    
    # 4. Installer les dépendances
    pip install --upgrade pip
    pip install -r requirements_streamlit.txt
    
    # 5. Lancer l'application
    streamlit run main.py
    ```
    
    #### Configuration Serveur
    ```bash
    # Configuration production (streamlit_config.toml)
    [server]
    port = 8501
    enableCORS = false
    enableXsrfProtection = true
    maxUploadSize = 200
    
    [browser]
    gatherUsageStats = false
    
    [theme]
    primaryColor = "#1f77b4"
    backgroundColor = "#ffffff"
    secondaryBackgroundColor = "#f0f2f6"
    textColor = "#262730"
    ```
    
    ### 📊 Monitoring et Maintenance
    
    #### Surveillance Système
    - **Performance** : Temps de réponse < 2 secondes
    - **Disponibilité** : Uptime > 99.5%
    - **Ressources** : CPU < 80%, RAM < 85%
    - **Erreurs** : Taux d'erreur < 1%
    
    #### Logs et Debugging
    ```python
    # Localisation des logs
    logs/
    ├── streamlit_app.log          # Logs application
    ├── model_predictions.log      # Logs prédictions
    └── system_performance.log     # Logs performance
    
    # Niveau de logging configurable dans config/logging_config.yaml
    ```
    
    #### Maintenance Régulière
    - **Quotidien** : Vérification statut système
    - **Hebdomadaire** : Analyse logs et performance
    - **Mensuel** : Mise à jour dépendances
    - **Trimestriel** : Revalidation modèle
    
    ### 🔐 Sécurité et Conformité
    
    #### Mesures de Sécurité
    - Chiffrement HTTPS obligatoire
    - Validation des données d'entrée
    - Protection contre l'injection de code
    - Limitation du taux de requêtes
    
    #### Conformité Réglementaire
    - **Bâle III** : Validation complète du modèle
    - **RGPD** : Anonymisation des données
    - **SOX** : Traçabilité des décisions
    - **Audit** : Logs complets conservés
    
    ### 🔧 Dépannage
    
    #### Problèmes Courants
    
    **Erreur de chargement du modèle**
    ```bash
    # Vérifier la présence du modèle
    ls modeling/models/
    
    # Vérifier les permissions
    chmod 644 modeling/models/*.pkl
    ```
    
    **Performance dégradée**
    ```python
    # Vider le cache Streamlit
    st.cache_data.clear()
    st.cache_resource.clear()
    
    # Redémarrer l'application
    ```
    
    **Erreurs de mémoire**
    ```bash
    # Augmenter la mémoire disponible
    export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=1000
    
    # Optimiser le garbage collector
    export PYTHONOPTIMIZE=1
    ```
    
    ### 📈 Optimisation Performance
    
    #### Cache Configuration
    ```python
    # Cache du modèle (permanent)
    @st.cache_resource
    def load_model():
        # Chargement unique au démarrage
    
    # Cache des données (TTL configuré)
    @st.cache_data(ttl=3600)
    def load_dashboard_data():
        # Rafraîchi toutes les heures
    ```
    
    #### Monitoring Avancé
    - **Prometheus** : Métriques système
    - **Grafana** : Dashboards monitoring
    - **ELK Stack** : Centralisation logs
    - **APM** : Application Performance Monitoring
    
    ### 🔄 Mises à Jour
    
    #### Processus de Déploiement
    1. **Tests** : Validation en environnement test
    2. **Sauvegarde** : Backup de la version actuelle
    3. **Déploiement** : Mise à jour progressive
    4. **Validation** : Tests post-déploiement
    5. **Rollback** : Procédure de retour en arrière
    
    #### Versions et Changelog
    - **v1.0.0** : Version initiale de production
    - Suivi des versions via Git tags
    - Documentation des changements obligatoire
    """)

def show_api_reference():
    """Référence API et intégration"""
    st.markdown("""
    ## 🔌 Référence API et Intégration
    
    ### 📡 Endpoints Disponibles
    
    #### POST /predict
    ```json
    {
        "age": 35,
        "job": "Employé",
        "housing": "Propriétaire",
        "saving_accounts": "Moyen",
        "checking_account": "Peu",
        "credit_amount": 25000,
        "duration": 60,
        "purpose": "Voiture",
        "sex": "Masculin",
        "income": 3000
    }
    ```
    
    **Réponse :**
    ```json
    {
        "prediction": 0,
        "decision": "ACCORDÉ",
        "risk_score": 45,
        "risk_probability": 0.23,
        "confidence": 87.5,
        "timestamp": "2025-06-20T10:30:00Z"
    }
    ```
    
    #### GET /model/info
    ```json
    {
        "model_version": "v1.0",
        "auc_roc": 0.8060,
        "ks_statistic": 0.5024,
        "gini_coefficient": 0.6119,
        "production_ready": true,
        "last_validation": "2025-06-20T10:04:00Z"
    }
    ```
    
    ### 🐍 SDK Python
    
    ```python
    from credit_scoring_client import CreditScoringAPI
    
    # Initialisation
    api = CreditScoringAPI(base_url="https://api.creditscoring.com")
    
    # Prédiction
    client_data = {
        "age": 35,
        "income": 3000,
        "credit_amount": 25000,
        # ... autres champs
    }
    
    result = api.predict(client_data)
    print(f"Décision: {result.decision}")
    print(f"Score: {result.risk_score}")
    ```
    
    ### 🌐 Integration Web
    
    ```javascript
    // Client JavaScript
    const API_BASE = 'https://api.creditscoring.com';
    
    async function predictCredit(clientData) {
        const response = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_TOKEN'
            },
            body: JSON.stringify(clientData)
        });
        
        return await response.json();
    }
    ```
    
    ### 📊 Codes d'Erreur
    
    | Code | Description | Action |
    |------|-------------|--------|
    | 200 | Succès | - |
    | 400 | Données invalides | Vérifier format |
    | 401 | Non autorisé | Vérifier token |
    | 429 | Trop de requêtes | Attendre/réduire fréquence |
    | 500 | Erreur serveur | Contacter support |
    """)

def main():
    """Fonction principale de la documentation"""
    
    # En-tête
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%); 
                padding: 1.5rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>📖 DOCUMENTATION COMPLÈTE</h1>
        <p style="margin: 0;">Guide utilisateur et administrateur du système de credit scoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Retour Accueil", use_container_width=True):
            st.switch_page("main.py")
    
    # Sélection du type de documentation
    st.markdown("## 📚 Sélectionnez votre profil")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        user_doc = st.button("👥 Utilisateur Final", use_container_width=True, type="primary")
    
    with col2:
        admin_doc = st.button("🔧 Administrateur", use_container_width=True)
    
    with col3:
        api_doc = st.button("🔌 Développeur API", use_container_width=True)
    
    # Contenu selon le profil sélectionné
    if user_doc or st.session_state.get('show_user_doc', True):
        st.session_state['show_user_doc'] = True
        st.session_state['show_admin_doc'] = False
        st.session_state['show_api_doc'] = False
        show_user_guide()
    
    if admin_doc or st.session_state.get('show_admin_doc', False):
        st.session_state['show_user_doc'] = False
        st.session_state['show_admin_doc'] = True
        st.session_state['show_api_doc'] = False
        show_admin_guide()
    
    if api_doc or st.session_state.get('show_api_doc', False):
        st.session_state['show_user_doc'] = False
        st.session_state['show_admin_doc'] = False
        st.session_state['show_api_doc'] = True
        show_api_reference()
    
    # Contacts et support
    st.markdown("---")
    st.markdown("## 📞 Support et Contacts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **👥 Support Utilisateur**
        - 📧 support@creditscoring.com
        - 📱 +33 1 23 45 67 89
        - 🕐 Lun-Ven 9h-18h
        """)
    
    with col2:
        st.markdown("""
        **🔧 Support Technique**
        - 📧 admin@creditscoring.com
        - 📱 +33 1 23 45 67 90
        - 🚨 24/7 pour urgences
        """)
    
    with col3:
        st.markdown("""
        **🔌 Support Développeur**
        - 📧 dev@creditscoring.com
        - 📚 docs.creditscoring.com
        - 💬 Slack: #dev-support
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 12px; background: #f8f9fa; 
                padding: 1rem; border-radius: 5px;">
        📖 Documentation mise à jour le 20/06/2025 | 
        📝 Version 1.0.0 | 
        🔄 Mise à jour continue
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()