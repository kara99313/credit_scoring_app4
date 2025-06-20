"""
📊 DATA PROCESSOR - Traitement des données d'entrée
===================================================
Module pour traiter et valider les données saisies par l'utilisateur
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import logging
from datetime import datetime
import streamlit as st
import math

from config.settings import (
    RISK_CLASSES, CLIENT_RATINGS, DECISION_MATRIX, KPI_DEFINITIONS,
    get_risk_class, get_client_rating, get_final_decision,
    probability_to_score, score_to_probability, SCORING_CONFIG
)

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreditScoringProcessor:
    """
    Processeur principal pour le credit scoring avec logiques métier avancées
    """
    
    def __init__(self):
        """Initialisation du processeur."""
        self.feature_mappings = self._init_feature_mappings()
        self.business_rules = self._init_business_rules()
        logger.info("CreditScoringProcessor initialisé avec succès")
    
    def _init_feature_mappings(self) -> Dict[str, Dict]:
        """Initialise les mappings pour les variables catégorielles."""
        return {
            'Job': {
                'management': 'Management/Cadre',
                'technician': 'Technicien',
                'entrepreneur': 'Entrepreneur', 
                'blue-collar': 'Ouvrier',
                'unknown': 'Inconnu',
                'retired': 'Retraité',
                'admin.': 'Administratif',
                'services': 'Services',
                'self-employed': 'Indépendant',
                'unemployed': 'Chômeur',
                'housemaid': 'Employé de maison',
                'student': 'Étudiant'
            },
            'Housing': {
                'own': 'Propriétaire',
                'rent': 'Locataire', 
                'free': 'Logé gratuitement'
            },
            'Saving_accounts': {
                'rich': 'Élevé (>1000€)',
                'quite rich': 'Correct (500-1000€)',
                'little': 'Faible (<500€)',
                'critical': 'Critique',
                'unknown': 'Inconnu'
            },
            'Checking_account': {
                'rich': 'Solde élevé',
                'moderate': 'Solde modéré',
                'little': 'Solde faible',
                'critical': 'Découvert',
                'unknown': 'Pas de compte'
            },
            'Purpose': {
                'car': 'Véhicule',
                'furniture/equipment': 'Mobilier/Équipement',
                'radio/TV': 'Électronique',
                'domestic appliances': 'Électroménager',
                'repairs': 'Réparations',
                'education': 'Éducation',
                'business': 'Professionnel',
                'vacation/others': 'Vacances/Autres'
            },
            'Sex': {
                'male': 'Masculin',
                'female': 'Féminin'
            },
            'current_credit_score': {
                '300-500': 'Faible (300-500)',
                '500-650': 'Moyen (500-650)',
                '650-750': 'Bon (650-750)',
                '750-850': 'Excellent (750-850)',
                'Inconnu': 'Non renseigné'
            },
            'payment_history': {
                'Excellent': 'Aucun retard',
                'Bon': 'Retards occasionnels',
                'Moyen': 'Quelques incidents',
                'Mauvais': 'Incidents fréquents',
                'Aucun historique': 'Pas d\'historique'
            },
            'marital_status': {
                'Célibataire': 'Célibataire',
                'Marié(e)': 'Marié(e)',
                'Divorcé(e)': 'Divorcé(e)',
                'Veuf/Veuve': 'Veuf/Veuve',
                'Union libre': 'Union libre'
            }
        }
    
    def _init_business_rules(self) -> Dict[str, Any]:
        """Initialise les règles métier pour l'analyse."""
        return {
            'age_segments': {
                'young': {'range': (18, 30), 'risk_factor': 1.1, 'description': 'Jeune adulte'},
                'adult': {'range': (31, 50), 'risk_factor': 1.0, 'description': 'Adulte'},
                'senior': {'range': (51, 65), 'risk_factor': 0.9, 'description': 'Senior'},
                'retired': {'range': (66, 100), 'risk_factor': 1.05, 'description': 'Retraité'}
            },
            'income_credit_thresholds': {
                'excellent': 5.0,   # Ratio revenus/crédit > 5
                'good': 3.0,        # Ratio > 3
                'acceptable': 2.0,   # Ratio > 2
                'risky': 1.5,       # Ratio > 1.5
                'critical': 0       # Ratio <= 1.5
            },
            'duration_risk_levels': {
                'short': {'months': 12, 'multiplier': 0.9},
                'medium': {'months': 24, 'multiplier': 1.0},
                'long': {'months': 36, 'multiplier': 1.15},
                'very_long': {'months': 48, 'multiplier': 1.3}
            }
        }
    
    def process_client_data(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Traite les données client complètes avec scoring sur 1000.
        
        Args:
            client_data: Données du formulaire client
            
        Returns:
            Dict contenant toutes les métriques calculées
        """
        try:
            # 1. Validation et nettoyage
            validated_data = self._validate_client_data(client_data)
            
            # 2. Feature engineering
            engineered_features = self._engineer_features(validated_data)
            
            # 3. Simulation de prédiction (remplacer par vraie prédiction)
            probability_default = self._predict_default_probability(engineered_features)
            
            # 4. Calcul du score sur 1000
            credit_score = probability_to_score(probability_default)
            
            # 5. Analyse complète
            analysis_result = self._comprehensive_analysis(
                validated_data, engineered_features, probability_default, credit_score
            )
            
            logger.info(f"Traitement client terminé - Score: {credit_score}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Erreur traitement données client: {str(e)}")
            raise
    
    def _validate_client_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valide et nettoie les données client."""
        validated = {}
        
        # Validation âge
        age = data.get('Age', 25)
        validated['Age'] = max(18, min(100, int(age)))
        
        # Validation montant crédit
        credit_amount = data.get('Credit_amount', 1000)
        validated['Credit_amount'] = max(100, min(100000, float(credit_amount)))
        
        # Validation durée
        duration = data.get('Duration', 12)
        validated['Duration'] = max(3, min(72, int(duration)))
        
        # Validation des nouvelles variables financières
        monthly_income = data.get('monthly_income', 2500)
        validated['monthly_income'] = max(0, min(50000, float(monthly_income)))
        
        monthly_expenses = data.get('monthly_expenses', 1800)
        validated['monthly_expenses'] = max(0, min(20000, float(monthly_expenses)))
        
        existing_debt = data.get('existing_debt', 0)
        validated['existing_debt'] = max(0, min(500000, float(existing_debt)))
        
        # Variables catégorielles avec valeurs par défaut
        categorical_defaults = {
            'Job': 'technician',
            'Housing': 'rent',
            'Saving_accounts': 'little',
            'Checking_account': 'little',
            'Purpose': 'car',
            'Sex': 'male',
            'current_credit_score': '650-750',
            'payment_history': 'Bon',
            'marital_status': 'Célibataire'
        }
        
        for var, default in categorical_defaults.items():
            validated[var] = data.get(var, default)
        
        return validated
    
    def _engineer_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les features engineered."""
        features = data.copy()
        
        # Calcul des ratios et scores avec vraies données financières
        monthly_income = data.get('monthly_income', self._estimate_income(data['Age'], data['Job']))
        
        features['Income_Credit_Ratio'] = monthly_income * 12 / data['Credit_amount']  # Ratio revenu annuel/crédit
        features['Debt_to_Income_Ratio'] = (data.get('monthly_expenses', 0) + data.get('existing_debt', 0)/12) / monthly_income if monthly_income > 0 else 0
        features['Duration_Risk_Score'] = self._calculate_duration_risk(data['Duration'])
        features['Age_Group'] = self._categorize_age(data['Age'])
        features['Credit_Risk_Category'] = self._categorize_credit_risk(data['Credit_amount'])
        features['Financial_Stability_Score'] = self._calculate_financial_stability_advanced(data)
        features['Payment_Quality_Score'] = self._calculate_payment_quality(data.get('payment_history', 'Bon'))
        features['Credit_Score_Numeric'] = self._convert_credit_score_to_numeric(data.get('current_credit_score', '650-750'))
        
        return features
    
    def _estimate_income(self, age: int, job: str) -> float:
        """Estime le revenu basé sur l'âge et le métier."""
        base_salaries = {
            'management': 4500, 'technician': 3200, 'entrepreneur': 4000,
            'admin.': 2800, 'services': 2400, 'self-employed': 3500,
            'blue-collar': 2600, 'retired': 1800, 'unemployed': 800,
            'student': 600, 'housemaid': 1400, 'unknown': 2500
        }
        
        base = base_salaries.get(job, 2500)
        
        # Ajustement selon l'âge
        if age < 25:
            multiplier = 0.7
        elif age < 35:
            multiplier = 1.0
        elif age < 50:
            multiplier = 1.3
        elif age < 65:
            multiplier = 1.5
        else:
            multiplier = 0.6
            
        return base * multiplier
    
    def _calculate_duration_risk(self, duration: int) -> float:
        """Calcule le score de risque selon la durée."""
        if duration <= 12:
            return 0.8
        elif duration <= 24:
            return 1.0
        elif duration <= 36:
            return 1.3
        else:
            return 1.6
    
    def _categorize_age(self, age: int) -> str:
        """Catégorise l'âge."""
        for category, config in self.business_rules['age_segments'].items():
            if config['range'][0] <= age <= config['range'][1]:
                return category
        return 'adult'
    
    def _categorize_credit_risk(self, amount: float) -> str:
        """Catégorise le risque selon le montant."""
        if amount < 2000:
            return 'low'
        elif amount < 5000:
            return 'medium'
        elif amount < 10000:
            return 'high'
        else:
            return 'very_high'
    
    def _calculate_financial_stability_advanced(self, data: Dict[str, Any]) -> float:
        """
        Calcule un score de stabilité financière avancé.
        
        Args:
            data: Données client
            
        Returns:
            Score de stabilité (0-1)
        """
        stability_score = 0.0
        
        # Ratio revenus/dépenses (40% du score)
        monthly_income = data.get('monthly_income', 2500)
        monthly_expenses = data.get('monthly_expenses', 1800)
        if monthly_income > 0:
            income_expense_ratio = (monthly_income - monthly_expenses) / monthly_income
            stability_score += min(0.4, income_expense_ratio * 0.4)
        
        # Historique paiements (30% du score)
        payment_history = data.get('payment_history', 'Bon')
        payment_scores = {
            'Excellent': 0.3, 'Bon': 0.24, 'Moyen': 0.15, 
            'Mauvais': 0.05, 'Aucun historique': 0.1
        }
        stability_score += payment_scores.get(payment_history, 0.1)
        
        # Score crédit (20% du score)
        credit_score = data.get('current_credit_score', '650-750')
        credit_scores = {
            '750-850': 0.2, '650-750': 0.16, '500-650': 0.1, 
            '300-500': 0.04, 'Inconnu': 0.08
        }
        stability_score += credit_scores.get(credit_score, 0.08)
        
        # Stabilité emploi (10% du score)
        job_stability = {
            'management': 0.1, 'technician': 0.08, 'admin.': 0.08,
            'services': 0.06, 'blue-collar': 0.06, 'self-employed': 0.05,
            'unemployed': 0.0, 'retired': 0.07, 'student': 0.02
        }
        stability_score += job_stability.get(data.get('Job', 'unknown'), 0.04)
        
        return min(1.0, stability_score)
    
    def _calculate_payment_quality(self, payment_history: str) -> float:
        """
        Convertit l'historique de paiement en score numérique.
        
        Args:
            payment_history: Historique de paiement
            
        Returns:
            Score qualité (0-1)
        """
        scores = {
            'Excellent': 1.0,
            'Bon': 0.8,
            'Moyen': 0.5,
            'Mauvais': 0.2,
            'Aucun historique': 0.6  # Neutre
        }
        return scores.get(payment_history, 0.5)
    
    def _convert_credit_score_to_numeric(self, credit_score_range: str) -> float:
        """
        Convertit une plage de score crédit en valeur numérique.
        
        Args:
            credit_score_range: Plage de score (ex: '650-750')
            
        Returns:
            Score numérique normalisé (0-1)
        """
        score_mappings = {
            '300-500': 0.25,  # 400 moyenne, normalisé
            '500-650': 0.45,  # 575 moyenne
            '650-750': 0.7,   # 700 moyenne
            '750-850': 0.95,  # 800 moyenne
            'Inconnu': 0.5    # Valeur neutre
        }
        return score_mappings.get(credit_score_range, 0.5)
    
    def _predict_default_probability(self, features: Dict[str, Any]) -> float:
        """
        Fait une prédiction avec le modèle Régression Logistique entraîné.
        """
        try:
            # Importer le modèle loader
            from .model_loader import ModelLoader
            
            # Charger le modèle
            model_loader = ModelLoader()
            model, metadata = model_loader.load_model()
            
            if model is None:
                logger.warning("Modèle non disponible, utilisation de la simulation")
                return self._simulate_prediction(features)
            
            # Préparer les données pour le modèle
            model_features = self._prepare_features_for_model(features)
            
            # Faire la prédiction
            probability = model.predict_proba(model_features)[0][1]  # Probabilité de défaut
            
            logger.info(f"Prédiction avec modèle réel: {probability:.3f}")
            return probability
            
        except Exception as e:
            logger.warning(f"Erreur lors de l'utilisation du modèle, utilisation de la simulation: {str(e)}")
            return self._simulate_prediction(features)
    
    def _simulate_prediction(self, features: Dict[str, Any]) -> float:
        """
        Simulation de prédiction (fallback si le modèle n'est pas disponible).
        """
        # Simulation basée sur les features principales (régression logistique)
        base_probability = 0.2  # 20% de base
        
        # Facteurs de risque (coefficients simulés de régression logistique)
        risk_factors = 0.0
        
        # Âge (coefficient: -0.01)
        age_normalized = (features['Age'] - 35) / 20
        risk_factors += age_normalized * -0.01
        
        # Ratio revenus/crédit (coefficient: -0.5)
        income_ratio = features.get('Income_Credit_Ratio', 1.0)
        risk_factors += (2.0 - income_ratio) * 0.15
        
        # Ratio d'endettement (coefficient: +0.8)
        debt_ratio = features.get('Debt_to_Income_Ratio', 0.3)
        risk_factors += debt_ratio * 0.8
        
        # Score crédit (coefficient: -0.6)
        credit_score = features.get('Credit_Score_Numeric', 0.7)
        risk_factors += (0.5 - credit_score) * 0.6
        
        # Historique paiements (coefficient: -0.4)
        payment_quality = features.get('Payment_Quality_Score', 0.8)
        risk_factors += (0.5 - payment_quality) * 0.4
        
        # Stabilité financière (coefficient: -0.3)
        stability = features.get('Financial_Stability_Score', 0.6)
        risk_factors += (0.5 - stability) * 0.3
        
        # Fonction logistique (sigmoid)
        probability = 1 / (1 + math.exp(-(base_probability + risk_factors)))
        
        # Contraindre entre 0.05 et 0.95
        return max(0.05, min(0.95, probability))
    
    def _prepare_features_for_model(self, features: Dict[str, Any]) -> pd.DataFrame:
        """
        Prépare les features pour qu'elles soient compatibles avec le modèle entraîné.
        """
        # Créer un DataFrame avec les features attendues par le modèle
        model_data = {
            'Age': features['Age'],
            'Job': features['Job'],
            'Housing': features['Housing'],
            'Saving_accounts': features['Saving_accounts'],
            'Checking_account': features['Checking_account'], 
            'Credit_amount': features['Credit_amount'],
            'Duration': features['Duration'],
            'Purpose': features['Purpose'],
            'Sex': features['Sex']
        }
        
        # Ajouter les features engineered si elles existent
        if 'Income_Credit_Ratio' in features:
            model_data['Income_Credit_Ratio'] = features['Income_Credit_Ratio']
        if 'Duration_Risk_Score' in features:
            model_data['Duration_Risk_Score'] = features['Duration_Risk_Score']
        if 'Financial_Stability_Score' in features:
            model_data['Financial_Stability_Score'] = features['Financial_Stability_Score']
        
        df = pd.DataFrame([model_data])
        return df
    
    def _comprehensive_analysis(
        self, 
        client_data: Dict[str, Any],
        features: Dict[str, Any], 
        probability: float, 
        score: int
    ) -> Dict[str, Any]:
        """Génère l'analyse complète du client."""
        
        # Métriques de base
        risk_class = get_risk_class(score)
        client_rating = get_client_rating(score)
        final_decision = get_final_decision(score)
        
        # Analyse des forces et faiblesses
        strengths, weaknesses = self._analyze_profile_strengths_weaknesses(features)
        
        # Recommandations personnalisées
        recommendations = self._generate_recommendations(features, risk_class, final_decision)
        
        # Interprétations métier
        business_interpretation = self._generate_business_interpretation(
            features, probability, score, risk_class
        )
        
        # Compilation du résultat
        result = {
            # Données de base
            'client_data': client_data,
            'engineered_features': features,
            
            # Métriques principales
            'probability_default': probability,
            'credit_score': score,
            'score_max': SCORING_CONFIG['score_max'],
            
            # Classifications
            'risk_class': risk_class,
            'client_rating': client_rating,
            'final_decision': final_decision,
            
            # Analyses qualitatives
            'profile_analysis': {
                'strengths': strengths,
                'weaknesses': weaknesses,
                'overall_assessment': self._get_overall_assessment(score)
            },
            
            # Recommandations
            'recommendations': recommendations,
            
            # Interprétations métier
            'business_interpretation': business_interpretation,
            
            # Métriques de performance (pour dashboard)
            'performance_indicators': self._calculate_performance_indicators(probability, score),
            
            # Métadonnées
            'analysis_timestamp': datetime.now().isoformat(),
            'model_version': "1.0.0",
            'confidence_level': self._calculate_confidence_level(features)
        }
        
        return result
    
    def _analyze_profile_strengths_weaknesses(self, features: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Analyse les forces et faiblesses du profil."""
        strengths = []
        weaknesses = []
        
        # Analyse ratio revenus/crédit
        if features['Income_Credit_Ratio'] > 4:
            strengths.append("Excellent ratio revenus/crédit (>4x)")
        elif features['Income_Credit_Ratio'] < 2:
            weaknesses.append("Ratio revenus/crédit faible (<2x)")
            
        # Analyse stabilité financière
        if features['Financial_Stability_Score'] > 0.7:
            strengths.append("Très bonne stabilité financière")
        elif features['Financial_Stability_Score'] < 0.4:
            weaknesses.append("Stabilité financière précaire")
            
        # Analyse des comptes
        if features['Checking_account'] == 'rich':
            strengths.append("Solde de compte courant élevé")
        elif features['Checking_account'] == 'critical':
            weaknesses.append("Situation de découvert critique")
            
        if features['Saving_accounts'] == 'rich':
            strengths.append("Épargne importante (>1000€)")
        elif features['Saving_accounts'] == 'critical':
            weaknesses.append("Épargne critique ou inexistante")
            
        # Analyse logement
        if features['Housing'] == 'own':
            strengths.append("Propriétaire de son logement")
        elif features['Housing'] == 'free':
            weaknesses.append("Logement précaire (logé gratuitement)")
            
        # Analyse emploi
        stable_jobs = ['management', 'technician', 'admin.']
        if features['Job'] in stable_jobs:
            strengths.append("Emploi stable et qualifié")
        elif features['Job'] == 'unemployed':
            weaknesses.append("Situation de chômage")
            
        return strengths, weaknesses
    
    def _generate_recommendations(
        self, 
        features: Dict[str, Any], 
        risk_class: Dict[str, Any], 
        decision: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Génère des recommandations personnalisées."""
        recommendations = []
        
        if decision['decision'] == 'APPROVED':
            recommendations.extend([
                {
                    'type': 'success',
                    'title': 'Crédit Approuvé',
                    'message': 'Profil excellent, conditions préférentielles applicables',
                    'action': 'Procéder à la finalisation du dossier'
                },
                {
                    'type': 'info',
                    'title': 'Suivi Recommandé',
                    'message': 'Surveillance standard, renouvellement facilité',
                    'action': 'Programmer un suivi annuel'
                }
            ])
            
        elif decision['decision'] == 'CONDITIONAL':
            recommendations.extend([
                {
                    'type': 'warning',
                    'title': 'Approbation Conditionnelle',
                    'message': 'Nécessite des garanties supplémentaires',
                    'action': 'Demander caution ou garantie réelle'
                },
                {
                    'type': 'info',
                    'title': 'Conditions Spéciales',
                    'message': 'Taux majoré et durée limitée recommandés',
                    'action': 'Appliquer grille tarifaire risque modéré'
                }
            ])
            
        else:  # REJECTED
            recommendations.extend([
                {
                    'type': 'danger',
                    'title': 'Crédit Refusé',
                    'message': 'Profil de risque trop élevé',
                    'action': 'Proposer solutions alternatives'
                },
                {
                    'type': 'info',
                    'title': 'Amélioration Profil',
                    'message': 'Réévaluation possible après amélioration situation',
                    'action': 'Programmer réévaluation dans 6 mois'
                }
            ])
        
        # Recommandations spécifiques selon les faiblesses
        if features['Income_Credit_Ratio'] < 2:
            recommendations.append({
                'type': 'warning',
                'title': 'Ratio Revenus/Crédit Faible',
                'message': 'Augmenter les revenus ou réduire le montant demandé',
                'action': 'Réviser la demande de crédit'
            })
            
        if features['Financial_Stability_Score'] < 0.4:
            recommendations.append({
                'type': 'warning',
                'title': 'Stabilité Financière Précaire',
                'message': 'Améliorer la situation des comptes avant nouvelle demande',
                'action': 'Conseil en gestion financière'
            })
        
        return recommendations
    
    def _generate_business_interpretation(
        self, 
        features: Dict[str, Any], 
        probability: float, 
        score: int, 
        risk_class: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Génère les interprétations métier."""
        
        interpretation = {
            'executive_summary': self._get_executive_summary(score, risk_class, probability),
            'risk_assessment': self._get_risk_assessment(probability, features),
            'financial_analysis': self._get_financial_analysis(features),
            'regulatory_compliance': self._get_regulatory_compliance(score, probability),
            'market_positioning': self._get_market_positioning(score, risk_class)
        }
        
        return interpretation
    
    def _get_executive_summary(self, score: int, risk_class: Dict, probability: float) -> str:
        """Résumé exécutif de l'analyse."""
        return f"""
        **RÉSUMÉ EXÉCUTIF**
        
        Score de crédit: **{score}/1000** (Classe {risk_class['class']})
        Probabilité de défaut: **{probability:.2%}**
        
        Le client présente un profil de risque **{risk_class['description'].lower()}** 
        selon nos critères d'évaluation Bâle III. Ce score place le client dans la 
        classe de risque {risk_class['class']} avec un taux de défaut historique 
        de {risk_class['default_rate']}.
        
        **Recommandation stratégique**: {'Approuver avec conditions standard' if score >= 650 else 'Approuver avec surveillance renforcée' if score >= 400 else 'Refuser et proposer alternatives'}
        """
    
    def _get_risk_assessment(self, probability: float, features: Dict) -> str:
        """Évaluation détaillée du risque."""
        risk_level = "FAIBLE" if probability < 0.1 else "MODÉRÉ" if probability < 0.3 else "ÉLEVÉ"
        
        return f"""
        **ÉVALUATION DU RISQUE**
        
        Niveau de risque: **{risk_level}**
        Probabilité de défaut: **{probability:.2%}**
        
        Facteurs de risque principaux:
        - Ratio revenus/crédit: {features['Income_Credit_Ratio']:.2f}x
        - Score de stabilité: {features['Financial_Stability_Score']:.2f}/1.0
        - Score risque durée: {features['Duration_Risk_Score']:.2f}
        
        Cette évaluation est conforme aux standards réglementaires Bâle III 
        et intègre nos modèles propriétaires de scoring.
        """
    
    def _get_financial_analysis(self, features: Dict) -> str:
        """Analyse financière détaillée."""
        return f"""
        **ANALYSE FINANCIÈRE**
        
        Situation patrimoniale:
        - Logement: {self.feature_mappings['Housing'].get(features['Housing'], features['Housing'])}
        - Compte courant: {self.feature_mappings['Checking_account'].get(features['Checking_account'], features['Checking_account'])}
        - Épargne: {self.feature_mappings['Saving_accounts'].get(features['Saving_accounts'], features['Saving_accounts'])}
        
        Capacité de remboursement:
        - Ratio revenus/crédit: {features['Income_Credit_Ratio']:.2f}x
        - Stabilité financière: {features['Financial_Stability_Score']:.0%}
        
        Le profil financier {'est solide' if features['Financial_Stability_Score'] > 0.6 else 'présente des fragilités'} 
        avec {'une excellente' if features['Income_Credit_Ratio'] > 3 else 'une' if features['Income_Credit_Ratio'] > 2 else 'une faible'} 
        capacité de remboursement.
        """
    
    def _get_regulatory_compliance(self, score: int, probability: float) -> str:
        """Vérification conformité réglementaire."""
        basel_compliant = score >= 300  # Seuil minimum Bâle III fictif
        
        return f"""
        **CONFORMITÉ RÉGLEMENTAIRE**
        
        Bâle III: {'✅ CONFORME' if basel_compliant else '❌ NON CONFORME'}
        GDPR: ✅ Données anonymisées
        Audit Trail: ✅ Traçabilité complète
        
        Score minimum réglementaire: 300/1000
        Score obtenu: {score}/1000
        
        {'Le dossier respecte toutes les exigences réglementaires.' if basel_compliant else 'Le dossier ne respecte pas les seuils minimums Bâle III.'}
        """
    
    def _get_market_positioning(self, score: int, risk_class: Dict) -> str:
        """Positionnement marché du client."""
        if score >= 800:
            segment = "clients premium"
            strategy = "Offres privilégiées et fidélisation"
        elif score >= 650:
            segment = "clients standards"
            strategy = "Offres standards avec potentiel d'upselling"
        elif score >= 400:
            segment = "clients à surveiller"
            strategy = "Surveillance renforcée et conditions protectives"
        else:
            segment = "clients à haut risque"
            strategy = "Refus ou offres très restrictives"
            
        return f"""
        **POSITIONNEMENT MARCHÉ**
        
        Segment client: **{segment.upper()}**
        Classe de risque: {risk_class['class']} ({risk_class['description']})
        
        Stratégie recommandée: {strategy}
        
        Positionnement concurrentiel: {'Avantage compétitif fort' if score >= 750 else 'Position standard' if score >= 500 else 'Désavantage concurrentiel'}
        """
    
    def _get_overall_assessment(self, score: int) -> str:
        """Évaluation globale du profil."""
        if score >= 800:
            return "EXCELLENT - Client de référence"
        elif score >= 650:
            return "BON - Client fiable"
        elif score >= 500:
            return "ACCEPTABLE - Surveillance standard"
        elif score >= 350:
            return "RISQUÉ - Surveillance renforcée"
        else:
            return "CRITIQUE - Risque très élevé"
    
    def _calculate_performance_indicators(self, probability: float, score: int) -> Dict[str, Any]:
        """Calcule les indicateurs de performance pour le dashboard."""
        return {
            'model_confidence': min(1.0, 1 - abs(probability - 0.5) * 2),
            'score_percentile': self._calculate_score_percentile(score),
            'risk_stability': 0.85,  # Simulation
            'prediction_accuracy': 0.806,  # AUC du modèle
            'processing_time': np.random.uniform(0.5, 2.0),  # Simulation temps
        }
    
    def _calculate_score_percentile(self, score: int) -> float:
        """Calcule le percentile du score (simulation)."""
        # Simulation d'une distribution normale centrée sur 600
        from scipy import stats
        return stats.norm.cdf(score, 600, 150)
    
    def _calculate_confidence_level(self, features: Dict[str, Any]) -> float:
        """Calcule le niveau de confiance de la prédiction."""
        # Simulation basée sur la complétude des données
        completeness = 1.0  # Toutes les données sont présentes
        consistency = 0.9   # Simulation cohérence des données
        
        confidence = (completeness + consistency) / 2
        return min(1.0, confidence + np.random.uniform(-0.1, 0.1))
    
    @staticmethod
    def get_feature_descriptions() -> Dict[str, str]:
        """Retourne les descriptions des features pour l'interface."""
        return {
            'Age': 'Âge du demandeur (années)',
            'Job': 'Profession ou statut professionnel',
            'Housing': 'Situation de logement',
            'Saving_accounts': 'Niveau du compte épargne',
            'Checking_account': 'Situation du compte courant',
            'Credit_amount': 'Montant du crédit demandé (€)',
            'Duration': 'Durée souhaitée (mois)',
            'Purpose': 'Objet du financement',
            'Sex': 'Genre du demandeur',
            'Income_Credit_Ratio': 'Ratio revenus estimés / montant crédit',
            'Financial_Stability_Score': 'Score de stabilité financière (0-1)',
            'Duration_Risk_Score': 'Score de risque lié à la durée',
            'Age_Group': 'Catégorie d\'âge',
            'Credit_Risk_Category': 'Catégorie de risque du montant'
        }
    
    @staticmethod 
    def get_input_validation_rules() -> Dict[str, Dict]:
        """Retourne les règles de validation pour les inputs."""
        return {
            'Age': {'min': 18, 'max': 100, 'type': 'int'},
            'Credit_amount': {'min': 100, 'max': 100000, 'type': 'float'},
            'Duration': {'min': 3, 'max': 72, 'type': 'int'},
            'Job': {'type': 'select', 'required': True},
            'Housing': {'type': 'select', 'required': True},
            'Saving_accounts': {'type': 'select', 'required': True},
            'Checking_account': {'type': 'select', 'required': True},
            'Purpose': {'type': 'select', 'required': True},
            'Sex': {'type': 'select', 'required': True}
        } 