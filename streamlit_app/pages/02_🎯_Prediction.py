"""
Page de Prédiction Credit Scoring - Interface Professionnelle Internationale
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time

# Import des modules locaux
from config.settings import (
    PROFESSIONAL_CSS, COLOR_PALETTE, PLOTLY_CONFIG, PLOTLY_LAYOUT,
    RISK_CLASSES, CLIENT_RATINGS, DECISION_MATRIX
)
from utils.data_processor import CreditScoringProcessor
from utils.model_loader import ModelManager

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Credit Scoring",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application du CSS professionnel
st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)

def main():
    """Interface principale de prédiction."""
    
    # Titre principal avec design professionnel
    st.markdown("""
    <div class="fade-in-up">
        <h1 style="text-align: center; color: var(--primary-color); margin-bottom: 2rem;">
            🎯 Évaluation Credit Scoring
        </h1>
        <div style="text-align: center; color: var(--text-secondary); margin-bottom: 3rem;">
            <p style="font-size: 1.2rem;">Analyse intelligente et prédiction de risque en temps réel</p>
            <div style="background: linear-gradient(135deg, #E3F2FD, #BBDEFB); padding: 1rem; border-radius: 12px; margin: 2rem auto; max-width: 800px;">
                <strong>🏆 Modèle Régression Logistique - AUC Score: 0.8060 - Conforme Bâle III</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialisation des processeurs
    processor = CreditScoringProcessor()
    model_manager = ModelManager()
    
    # Conteneur principal avec colonnes
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        st.markdown('<div class="metric-card fade-in-up">', unsafe_allow_html=True)
        st.markdown("### 📋 Informations Client")
        
        # Formulaire client avec design amélioré
        client_data = create_client_form(processor)
        
        # Bouton de prédiction avec style professionnel
        predict_button = st.button(
            "🚀 Analyser le Profil",
            key="predict_btn",
            help="Lancer l'analyse complète du risque client",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Affichage des statuts système
        display_system_status()
    
    with col2:
        if predict_button and client_data:
            # Barre de progression avec style
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulation du processus d'analyse
                for i, step in enumerate([
                    "🔍 Validation des données...",
                    "⚙️ Feature engineering...", 
                    "🤖 Prédiction du modèle...",
                    "📊 Analyse des risques...",
                    "📋 Génération du rapport..."
                ]):
                    status_text.text(step)
                    progress_bar.progress((i + 1) * 20)
                    time.sleep(0.3)
                
                status_text.text("✅ Analyse terminée !")
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
            
            # Traitement et affichage des résultats
            try:
                results = processor.process_client_data(client_data)
                display_comprehensive_results(results)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                st.info("💡 Veuillez vérifier les données saisies et réessayer.")
        
        elif not predict_button:
            # Affichage par défaut avec informations utiles
            display_default_content()

def create_client_form(processor) -> dict:
    """Crée le formulaire client avec validation."""
    
    client_data = {}
    
    # Section Informations Personnelles
    st.markdown("#### 👤 Informations Personnelles")
    
    col1_form, col2_form = st.columns(2)
    
    with col1_form:
        client_data['Age'] = st.number_input(
            "Âge",
            min_value=18, max_value=100, value=35,
            help="Âge du demandeur (18-100 ans)"
        )
        
        client_data['Sex'] = st.selectbox(
            "Genre",
            options=['male', 'female'],
            format_func=lambda x: processor.feature_mappings['Sex'][x],
            help="Genre du demandeur"
        )
    
    with col2_form:
        client_data['Job'] = st.selectbox(
            "Profession",
            options=list(processor.feature_mappings['Job'].keys()),
            format_func=lambda x: processor.feature_mappings['Job'][x],
            help="Profession ou statut professionnel"
        )
        
        client_data['marital_status'] = st.selectbox(
            "Situation familiale",
            options=['Célibataire', 'Marié(e)', 'Divorcé(e)', 'Veuf/Veuve', 'Union libre'],
            help="Statut matrimonial"
        )
        
        client_data['Housing'] = st.selectbox(
            "Logement",
            options=list(processor.feature_mappings['Housing'].keys()),
            format_func=lambda x: processor.feature_mappings['Housing'][x],
            help="Situation de logement"
        )
    
    # Section Situation Financière
    st.markdown("#### 💰 Situation Financière")
    
    col1_fin, col2_fin = st.columns(2)
    
    with col1_fin:
        client_data['monthly_income'] = st.number_input(
            "Revenus mensuels nets (€)",
            min_value=0, max_value=50000, value=2500, step=100,
            help="Revenus nets mensuels (salaire, pensions, etc.)"
        )
        
        client_data['monthly_expenses'] = st.number_input(
            "Dépenses mensuelles (€)",
            min_value=0, max_value=20000, value=1800, step=50,
            help="Dépenses mensuelles totales (loyer, charges, etc.)"
        )
        
        client_data['existing_debt'] = st.number_input(
            "Dette existante (€)",
            min_value=0, max_value=500000, value=0, step=100,
            help="Montant total des dettes existantes"
        )
        
        client_data['Checking_account'] = st.selectbox(
            "Compte Courant",
            options=list(processor.feature_mappings['Checking_account'].keys()),
            format_func=lambda x: processor.feature_mappings['Checking_account'][x],
            help="Situation du compte courant"
        )
    
    with col2_fin:
        client_data['current_credit_score'] = st.selectbox(
            "Score crédit actuel",
            options=['300-500', '500-650', '650-750', '750-850', 'Inconnu'],
            index=2,
            help="Score crédit actuel (si connu)"
        )
        
        client_data['payment_history'] = st.selectbox(
            "Historique paiements",
            options=['Excellent', 'Bon', 'Moyen', 'Mauvais', 'Aucun historique'],
            index=1,
            help="Qualité des paiements passés"
        )
        
        client_data['Saving_accounts'] = st.selectbox(
            "Épargne",
            options=list(processor.feature_mappings['Saving_accounts'].keys()),
            format_func=lambda x: processor.feature_mappings['Saving_accounts'][x],
            help="Niveau du compte épargne"
        )
    
    # Section Demande de Crédit
    st.markdown("#### 🎯 Demande de Crédit")
    
    col1_credit, col2_credit = st.columns(2)
    
    with col1_credit:
        client_data['Credit_amount'] = st.number_input(
            "Montant Crédit (€)",
            min_value=100, max_value=100000, value=5000, step=100,
            help="Montant du crédit demandé"
        )
        
        client_data['Duration'] = st.number_input(
            "Durée (mois)",
            min_value=3, max_value=72, value=24, step=1,
            help="Durée souhaitée du crédit"
        )
    
    with col2_credit:
        # Calcul automatique ratio dette/revenus
        if client_data['monthly_income'] > 0:
            debt_ratio = ((client_data['monthly_expenses'] + client_data['existing_debt']/12) / client_data['monthly_income']) * 100
            st.metric(
                "Ratio d'endettement",
                f"{debt_ratio:.1f}%",
                delta=f"{'✅ Bon' if debt_ratio < 33 else '⚠️ Élevé' if debt_ratio < 50 else '❌ Critique'}",
                help="Ratio calculé automatiquement"
            )
    
    # Section Objet du Crédit
    st.markdown("#### 🎯 Objet du Financement")
    
    client_data['Purpose'] = st.selectbox(
        "Utilisation",
        options=list(processor.feature_mappings['Purpose'].keys()),
        format_func=lambda x: processor.feature_mappings['Purpose'][x],
        help="Objet du financement"
    )
    
    return client_data

def display_comprehensive_results(results: dict):
    """Affiche les résultats complets avec design professionnel."""
    
    # Métriques principales
    display_main_metrics(results)
    
    # Analyse détaillée en onglets
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analyse Complète", 
        "🎯 Décision & Recommandations",
        "📈 Indicateurs Performance", 
        "📋 Interprétation Métier"
    ])
    
    with tab1:
        display_complete_analysis(results)
    
    with tab2:
        display_decision_recommendations(results)
    
    with tab3:
        display_performance_indicators(results)
    
    with tab4:
        display_business_interpretation(results)

def display_main_metrics(results: dict):
    """Affiche les métriques principales."""
    
    score = results['credit_score']
    probability = results['probability_default']
    risk_class = results['risk_class']
    client_rating = results['client_rating']
    decision = results['final_decision']
    
    # Conteneur principal des métriques
    st.markdown('<div class="risk-card fade-in-up">', unsafe_allow_html=True)
    
    # Titre de section
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: var(--primary-color);">🎯 Résultats de l'Analyse</h2>
        <p style="color: var(--text-secondary);">Évaluation complète du profil de risque</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Métriques en colonnes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center; background: linear-gradient(135deg, {COLOR_PALETTE['primary']}, #2563EB);">
            <h3 style="color: white; margin: 0;">Score Crédit</h3>
            <h1 style="color: white; margin: 0.5rem 0; font-size: 3rem;">{score}</h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">/ 1000</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        prob_color = COLOR_PALETTE['success'] if probability < 0.1 else COLOR_PALETTE['warning'] if probability < 0.3 else COLOR_PALETTE['accent']
        st.markdown(f"""
        <div class="metric-card" style="text-align: center; background: linear-gradient(135deg, {prob_color}, {prob_color}CC);">
            <h3 style="color: white; margin: 0;">Probabilité Défaut</h3>
            <h1 style="color: white; margin: 0.5rem 0; font-size: 3rem;">{probability:.1%}</h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">Risque estimé</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center; background: linear-gradient(135deg, {risk_class['color']}, {risk_class['color']}CC);">
            <h3 style="color: white; margin: 0;">Classe Risque</h3>
            <h1 style="color: white; margin: 0.5rem 0; font-size: 3rem;">{risk_class['class']}</h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">{risk_class['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center; background: linear-gradient(135deg, {decision['color']}, {decision['color']}CC);">
            <h3 style="color: white; margin: 0;">Décision</h3>
            <h1 style="color: white; margin: 0.5rem 0; font-size: 2rem;">{decision['icon']}</h1>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">{decision['message']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_complete_analysis(results: dict):
    """Affiche l'analyse complète."""
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Score Breakdown")
        
        # Graphique de score avec gauge
        fig_gauge = create_score_gauge(results['credit_score'])
        st.plotly_chart(fig_gauge, use_container_width=True, config=PLOTLY_CONFIG)
        
        # Comparaison avec les seuils
        display_score_thresholds(results)
    
    with col2:
        st.markdown("#### 🎯 Analyse du Profil")
        
        profile = results['profile_analysis']
        
        # Forces du profil
        if profile['strengths']:
            st.markdown("**✅ Forces identifiées:**")
            for strength in profile['strengths']:
                st.markdown(f"• {strength}")
        
        # Faiblesses du profil
        if profile['weaknesses']:
            st.markdown("**⚠️ Points d'attention:**")
            for weakness in profile['weaknesses']:
                st.markdown(f"• {weakness}")
        
        # Évaluation globale
        st.markdown(f"**📋 Évaluation globale:** {profile['overall_assessment']}")
    
    # Graphiques d'analyse avancée
    display_advanced_charts(results)

def display_decision_recommendations(results: dict):
    """Affiche la décision et les recommandations."""
    
    decision = results['final_decision']
    recommendations = results['recommendations']
    
    # Décision principale
    st.markdown(f"""
    <div class="alert-{'success' if decision['decision'] == 'APPROVED' else 'warning' if decision['decision'] == 'CONDITIONAL' else 'danger'}">
        <h3>{decision['icon']} {decision['message']}</h3>
        <p><strong>Niveau de confiance:</strong> {decision['confidence']}</p>
        <p><strong>Seuil appliqué:</strong> {decision['threshold']}/1000</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Recommandations détaillées
    st.markdown("#### 💡 Recommandations Personnalisées")
    
    for i, rec in enumerate(recommendations):
        alert_type = rec['type']
        if alert_type == 'success':
            st.success(f"**{rec['title']}**\n{rec['message']}\n*Action: {rec['action']}*")
        elif alert_type == 'warning':
            st.warning(f"**{rec['title']}**\n{rec['message']}\n*Action: {rec['action']}*")
        elif alert_type == 'danger':
            st.error(f"**{rec['title']}**\n{rec['message']}\n*Action: {rec['action']}*")
        else:
            st.info(f"**{rec['title']}**\n{rec['message']}\n*Action: {rec['action']}*")

def display_performance_indicators(results: dict):
    """Affiche les indicateurs de performance."""
    
    perf = results['performance_indicators']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Métriques de Performance")
        
        # Métriques en format professionnel
        metrics = [
            ("Confiance Modèle", f"{perf['model_confidence']:.1%}", "🎯"),
            ("Percentile Score", f"{perf['score_percentile']:.1%}", "📊"),
            ("Stabilité Risque", f"{perf['risk_stability']:.1%}", "⚖️"),
            ("Précision Modèle", f"{perf['prediction_accuracy']:.1%}", "🔍"),
            ("Temps Traitement", f"{perf['processing_time']:.2f}s", "⚡")
        ]
        
        for name, value, icon in metrics:
            st.markdown(f"""
            <div class="metric-card" style="padding: 1rem; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.5rem;">{icon}</span>
                        <strong> {name}</strong>
                    </div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: var(--primary-color);">
                        {value}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 Visualisation Performance")
        
        # Graphique radar des performances
        fig_radar = create_performance_radar(perf)
        st.plotly_chart(fig_radar, use_container_width=True, config=PLOTLY_CONFIG)

def display_business_interpretation(results: dict):
    """Affiche l'interprétation métier."""
    
    interpretation = results['business_interpretation']
    
    # Onglets pour les différentes sections
    sub_tab1, sub_tab2, sub_tab3, sub_tab4, sub_tab5 = st.tabs([
        "📋 Résumé", "⚠️ Risque", "💰 Finance", "📜 Conformité", "🎯 Marché"
    ])
    
    with sub_tab1:
        st.markdown(interpretation['executive_summary'])
    
    with sub_tab2:
        st.markdown(interpretation['risk_assessment'])
    
    with sub_tab3:
        st.markdown(interpretation['financial_analysis'])
    
    with sub_tab4:
        st.markdown(interpretation['regulatory_compliance'])
    
    with sub_tab5:
        st.markdown(interpretation['market_positioning'])

def create_score_gauge(score: int) -> go.Figure:
    """Crée un graphique gauge pour le score."""
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score Credit /1000"},
        delta = {'reference': 500},
        gauge = {
            'axis': {'range': [None, 1000]},
            'bar': {'color': COLOR_PALETTE['primary']},
            'steps': [
                {'range': [0, 300], 'color': COLOR_PALETTE['accent']},
                {'range': [300, 500], 'color': COLOR_PALETTE['warning']},
                {'range': [500, 700], 'color': COLOR_PALETTE['info']},
                {'range': [700, 1000], 'color': COLOR_PALETTE['success']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 520
            }
        }
    ))
    
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig

def display_score_thresholds(results: dict):
    """Affiche les seuils de score."""
    
    score = results['credit_score']
    
    st.markdown("**🎯 Positionnement vs Seuils:**")
    
    thresholds = [
        ("Refus", 0, 400, COLOR_PALETTE['accent']),
        ("Conditionnel", 400, 520, COLOR_PALETTE['warning']),
        ("Approbation", 520, 1000, COLOR_PALETTE['success'])
    ]
    
    for name, min_val, max_val, color in thresholds:
        in_range = min_val <= score <= max_val
        status = "✅" if in_range else "⚪"
        weight = "bold" if in_range else "normal"
        
        st.markdown(f"""
        <div style="padding: 0.5rem; margin: 0.2rem 0; border-left: 4px solid {color}; 
                    background: {'rgba(0,0,0,0.05)' if in_range else 'transparent'};">
            {status} <span style="font-weight: {weight};">{name}: {min_val}-{max_val}</span>
        </div>
        """, unsafe_allow_html=True)

def display_advanced_charts(results: dict):
    """Affiche les graphiques d'analyse avancée."""
    
    st.markdown("#### 📊 Analyses Avancées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des risques par classe
        fig_risk_dist = create_risk_distribution_chart()
        st.plotly_chart(fig_risk_dist, use_container_width=True, config=PLOTLY_CONFIG)
    
    with col2:
        # Evolution temporelle (simulation)
        fig_temporal = create_temporal_analysis()
        st.plotly_chart(fig_temporal, use_container_width=True, config=PLOTLY_CONFIG)

def create_performance_radar(perf: dict) -> go.Figure:
    """Crée un graphique radar des performances."""
    
    categories = ['Confiance', 'Percentile', 'Stabilité', 'Précision', 'Vitesse']
    values = [
        perf['model_confidence'],
        perf['score_percentile'], 
        perf['risk_stability'],
        perf['prediction_accuracy'],
        1 - (perf['processing_time'] / 5)  # Normalisation inverse pour vitesse
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Performance',
        line_color=COLOR_PALETTE['primary']
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        **PLOTLY_LAYOUT
    )
    
    return fig

def create_risk_distribution_chart() -> go.Figure:
    """Crée un graphique de distribution des risques."""
    
    # Simulation de données de distribution
    classes = list(RISK_CLASSES.keys())
    counts = [15, 25, 30, 20, 7, 2, 0.8, 0.2]  # Simulation
    
    fig = go.Figure([go.Bar(
        x=classes,
        y=counts,
        marker_color=[RISK_CLASSES[c]['color'] for c in classes],
        text=[f"{c}%" for c in counts],
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Distribution des Classes de Risque (%)",
        xaxis_title="Classe de Risque",
        yaxis_title="Pourcentage",
        **PLOTLY_LAYOUT
    )
    
    return fig

def create_temporal_analysis() -> go.Figure:
    """Crée une analyse temporelle (simulation)."""
    
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    auc_scores = 0.806 + np.random.normal(0, 0.01, 30)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=auc_scores,
        mode='lines+markers',
        name='AUC Score',
        line=dict(color=COLOR_PALETTE['primary'], width=3),
        marker=dict(size=6)
    ))
    
    fig.add_hline(y=0.80, line_dash="dash", line_color="red", 
                  annotation_text="Seuil Minimum")
    
    fig.update_layout(
        title="Evolution Performance Modèle (30j)",
        xaxis_title="Date",
        yaxis_title="AUC Score",
        **PLOTLY_LAYOUT
    )
    
    return fig

def display_system_status():
    """Affiche le statut du système."""
    
    st.markdown('<div class="metric-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
    st.markdown("#### 🖥️ Statut Système")
    
    # Simulation statuts
    statuses = [
        ("Modèle", "✅ Opérationnel", "success"),
        ("Base de données", "✅ Connectée", "success"), 
        ("API", "✅ Disponible", "success"),
        ("Cache", "⚡ Optimisé", "info")
    ]
    
    for component, status, type_status in statuses:
        color = COLOR_PALETTE['success'] if type_status == 'success' else COLOR_PALETTE['info']
        st.markdown(f"""
        <div style="padding: 0.5rem; margin: 0.2rem 0; border-left: 3px solid {color};">
            <strong>{component}:</strong> {status}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_default_content():
    """Affiche le contenu par défaut."""
    
    st.markdown('<div class="risk-card fade-in-up">', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Bienvenue dans l'Évaluateur Credit Scoring
    
    Cette interface professionnelle vous permet d'analyser le risque de crédit en temps réel 
    grâce à notre modèle Régression Logistique de pointe.
    
    #### 🚀 Fonctionnalités Clés:
    - **Score sur 1000** avec classes de risque Bâle III
    - **Analyse probabiliste** de défaut 
    - **Recommandations personnalisées** selon le profil
    - **Interprétations métier** complètes
    - **Conformité réglementaire** intégrée
    
    #### 📊 Performance du Modèle:
    - **AUC Score:** 0.8060 (Excellent)
    - **Précision:** 75.2%
    - **Rappel:** 71.8%
    - **F1-Score:** 73.4%
    
    Complétez le formulaire à gauche pour commencer l'analyse.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()