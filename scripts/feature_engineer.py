"""
Feature Engineering Module for Credit Scoring System

This module implements comprehensive business feature engineering according to 
the specifications defined in PROJET_COMPLET_SPECIFICATION.md

Author: Credit Scoring Team
Created: 2024
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, List, Any
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')


class FeatureEngineer:
    """
    ÉTAPE 3: Feature Engineering Métier
    
    Implémente la création de features métier selon l'architecture définie :
    - Features métier (ratios financiers, comportement crédit)
    - Features d'interaction
    - Features temporelles
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialisation du Feature Engineer
        
        Args:
            config: Configuration pour le feature engineering
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.feature_info = {}  # Information sur les features créées
        
        # Configuration par défaut
        self.default_config = {
            'create_ratios': True,
            'create_interactions': True,
            'create_temporal': True,
            'create_risk_indicators': True
        }
        
    def create_business_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 3.1: Création des features métier
        
        Crée les features business selon les spécifications :
        - Ratios financiers (dette/revenus, épargne, etc.)
        - Score comportement crédit
        - Indicateurs de risque
        - Features démographiques
        """
        print("\n🔧 ÉTAPE 3.1: CRÉATION DES FEATURES MÉTIER")
        print("=" * 55)
        
        df_features = df.copy()
        created_features = []
        
        # 1. Ratios financiers
        print("\n💰 Création des ratios financiers...")
        df_features, ratio_features = self._create_financial_ratios(df_features)
        created_features.extend(ratio_features)
        
        # 2. Features de comportement crédit
        print("\n📊 Création des features comportement crédit...")
        df_features, credit_features = self._create_credit_behavior_features(df_features)
        created_features.extend(credit_features)
        
        # 3. Indicateurs de risque
        print("\n⚠️ Création des indicateurs de risque...")
        df_features, risk_features = self._create_risk_indicators(df_features)
        created_features.extend(risk_features)
        
        # 4. Features démographiques
        print("\n👥 Création des features démographiques...")
        df_features, demo_features = self._create_demographic_features(df_features)
        created_features.extend(demo_features)
        
        self.feature_info['business_features'] = created_features
        print(f"\n✅ {len(created_features)} features métier créées avec succès!")
        
        return df_features
    
    def _create_financial_ratios(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des ratios financiers"""
        created_features = []
        
        # 1. Ratio dette/revenus (Dette totale / Revenus estimés)
        # Conversion du taux d'endettement texte en numérique
        taux_mapping = {
            'inferieur a 20%': 15,
            'compris entre 20% et 25%': 22.5,
            'compris entre 25% et 35%': 30,
            'superieur a 35%': 40
        }
        df['taux_endettement_num'] = df['taux_endettement'].map(taux_mapping).fillna(25)
        
        # Estimation des revenus basée sur le montant demandé et le taux d'endettement
        df['revenus_estimes'] = np.where(
            df['taux_endettement_num'] > 0,
            df['montant'] / (df['taux_endettement_num'] / 100),
            df['montant'] * 5  # Estimation conservative
        )
        
        df['debt_to_income_ratio'] = np.where(
            df['revenus_estimes'] > 0,
            df['montant'] / df['revenus_estimes'],
            0
        )
        created_features.append('debt_to_income_ratio')
        
        # 2. Taux d'utilisation crédit (basé sur le montant vs capacité estimée)
        df['credit_utilization_ratio'] = np.clip(df['taux_endettement_num'] / 100, 0, 1)
        created_features.append('credit_utilization_ratio')
        
        # 3. Taux d'épargne (basé sur la variable épargne)
        epargne_mapping = {
            'A11': 0.0,   # < 100 DM
            'A12': 0.1,   # 100-500 DM
            'A13': 0.3,   # 500-1000 DM
            'A14': 0.6,   # >= 1000 DM
            'A15': 0.0    # Inconnu
        }
        df['savings_rate'] = df['epargne'].map(epargne_mapping).fillna(0)
        created_features.append('savings_rate')
        
        # 4. Ratio dépenses/revenus estimé
        df['expense_to_income_ratio'] = np.where(
            df['revenus_estimes'] > 0,
            (df['montant'] * 0.1) / df['revenus_estimes'],  # 10% du montant comme proxy dépenses
            0
        )
        created_features.append('expense_to_income_ratio')
        
        # 5. Capacité de remboursement
        df['repayment_capacity'] = df['revenus_estimes'] - (df['revenus_estimes'] * df['credit_utilization_ratio'])
        created_features.append('repayment_capacity')
        
        print(f"   ✅ {len(created_features)} ratios financiers créés")
        return df, created_features
    
    def _create_credit_behavior_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des features de comportement crédit"""
        created_features = []
        
        # 1. Score historique paiements (basé sur historique)
        historique_scores = {
            'A30': 1.0,   # Pas de crédit / tous payés
            'A31': 0.9,   # Tous payés à temps
            'A32': 0.7,   # Payés à temps jusqu'à présent
            'A33': 0.4,   # Retard dans le passé
            'A34': 0.1    # Compte critique
        }
        df['payment_history_score'] = df['historique'].map(historique_scores).fillna(0.5)
        created_features.append('payment_history_score')
        
        # 2. Diversité des types de crédit (credit mix)
        objet_diversity = {
            'A40': 0.2,   # Voiture neuve
            'A41': 0.3,   # Voiture occasion  
            'A42': 0.6,   # Mobilier/équipement
            'A43': 0.4,   # Radio/TV
            'A44': 0.5,   # Électroménager
            'A45': 0.7,   # Réparations
            'A46': 0.8,   # Éducation
            'A47': 0.6,   # Vacances
            'A48': 0.9,   # Reconversion
            'A49': 0.8,   # Entreprise
            'A410': 0.5   # Autres
        }
        df['credit_mix_diversity'] = df['objet'].map(objet_diversity).fillna(0.5)
        created_features.append('credit_mix_diversity')
        
        # 3. Nombre de demandes récentes (basé sur nombre_credit)
        df['recent_inquiries_count'] = np.where(
            df['nombre_credit'].isin(['A141', 'A142']),  # Banque/magasins
            df['nombre_credit'].map({'A141': 2, 'A142': 1}).fillna(0),
            0
        )
        created_features.append('recent_inquiries_count')
        
        # 4. Âge moyen des comptes (basé sur ancienneté emploi)
        anciennete_mapping = {
            'A71': 0.5,   # Chômeur
            'A72': 1,     # < 1 an
            'A73': 2.5,   # 1-4 ans
            'A74': 7,     # 4-7 ans
            'A75': 10     # >= 7 ans
        }
        df['account_age_average'] = df['anciennete_emploi'].map(anciennete_mapping).fillna(0)
        created_features.append('account_age_average')
        
        print(f"   ✅ {len(created_features)} features comportement crédit créées")
        return df, created_features
    
    def _create_risk_indicators(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des indicateurs de risque"""
        created_features = []
        
        # 1. Score risque faillite (combinaison de facteurs)
        df['bankruptcy_risk_score'] = (
            (1 - df['payment_history_score']) * 0.4 +
            df['credit_utilization_ratio'] * 0.3 +
            (1 - df['savings_rate']) * 0.2 +
            df['debt_to_income_ratio'] * 0.1
        )
        created_features.append('bankruptcy_risk_score')
        
        # 2. Fréquence retards (basé sur historique)
        retard_frequency = {
            'A30': 0.0,   # Pas de crédit
            'A31': 0.0,   # Tous payés à temps
            'A32': 0.1,   # Payés à temps jusqu'à présent
            'A33': 0.6,   # Retard dans le passé
            'A34': 0.9    # Compte critique
        }
        df['late_payment_frequency'] = df['historique'].map(retard_frequency).fillna(0.3)
        created_features.append('late_payment_frequency')
        
        # 3. Utilisation limite crédit
        df['credit_limit_usage'] = np.clip(df['taux_endettement_num'] / 100, 0, 1)
        created_features.append('credit_limit_usage')
        
        # 4. Score stabilité emploi
        stabilite_emploi = {
            'A71': 0.0,   # Chômeur
            'A72': 0.2,   # < 1 an
            'A73': 0.6,   # 1-4 ans
            'A74': 0.8,   # 4-7 ans
            'A75': 1.0    # >= 7 ans
        }
        df['employment_stability_score'] = df['anciennete_emploi'].map(stabilite_emploi).fillna(0.3)
        created_features.append('employment_stability_score')
        
        print(f"   ✅ {len(created_features)} indicateurs de risque créés")
        return df, created_features
    
    def _create_demographic_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des features démographiques"""
        created_features = []
        
        # 1. Segment âge-revenus
        df['age_income_segment'] = pd.cut(
            df['age'], 
            bins=[0, 25, 35, 45, 55, 100], 
            labels=['young', 'young_adult', 'adult', 'mature', 'senior']
        ).astype(str)
        
        # Combinaison avec les revenus
        df['age_income_combined'] = (
            df['age_income_segment'] + '_' + 
            pd.cut(df['revenus_estimes'], bins=3, labels=['low', 'medium', 'high']).astype(str)
        )
        created_features.append('age_income_combined')
        
        # 2. Concordance éducation-emploi (proxy via statut)
        statut_education_match = {
            'A91': 0.2,   # Homme divorcé/séparé
            'A92': 0.6,   # Femme divorcée/séparée/mariée
            'A93': 0.8,   # Homme célibataire
            'A94': 0.7    # Homme marié/veuf
        }
        df['education_employment_match'] = df['statut'].map(statut_education_match).fillna(0.5)
        created_features.append('education_employment_match')
        
        # 3. Facteur risque régional (basé sur le logement)
        regional_risk = {
            'A151': 0.3,  # Loue
            'A152': 0.1,  # Propriétaire
            'A153': 0.5   # Gratuit
        }
        df['regional_risk_factor'] = df['logement'].map(regional_risk).fillna(0.4)
        created_features.append('regional_risk_factor')
        
        print(f"   ✅ {len(created_features)} features démographiques créées")
        return df, created_features
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 3.2: Création des features d'interaction
        
        Crée les interactions entre variables selon les spécifications
        """
        print("\n🔗 ÉTAPE 3.2: CRÉATION DES FEATURES D'INTERACTION")
        print("=" * 55)
        
        df_interactions = df.copy()
        created_features = []
        
        # 1. Interactions numériques
        print("\n🔢 Interactions numériques...")
        df_interactions, num_features = self._create_numerical_interactions(df_interactions)
        created_features.extend(num_features)
        
        # 2. Interactions catégorielles
        print("\n📊 Interactions catégorielles...")
        df_interactions, cat_features = self._create_categorical_interactions(df_interactions)
        created_features.extend(cat_features)
        
        # 3. Interactions mixtes
        print("\n🔀 Interactions mixtes...")
        df_interactions, mixed_features = self._create_mixed_interactions(df_interactions)
        created_features.extend(mixed_features)
        
        self.feature_info['interaction_features'] = created_features
        print(f"\n✅ {len(created_features)} features d'interaction créées!")
        
        return df_interactions
    
    def _create_numerical_interactions(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des interactions numériques"""
        created_features = []
        
        # 1. Âge × Revenus
        df['age_income_interaction'] = df['age'] * df['revenus_estimes'] / 1000
        created_features.append('age_income_interaction')
        
        # 2. Dette × Revenus
        df['debt_income_interaction'] = df['montant'] * df['revenus_estimes'] / 10000
        created_features.append('debt_income_interaction')
        
        # 3. Score × Utilisation
        df['score_utilization_interaction'] = df['payment_history_score'] * df['credit_utilization_ratio']
        created_features.append('score_utilization_interaction')
        
        # 4. Montant × Durée
        df['amount_duration_interaction'] = df['montant'] * df['duree'] / 100
        created_features.append('amount_duration_interaction')
        
        print(f"   ✅ {len(created_features)} interactions numériques créées")
        return df, created_features
    
    def _create_categorical_interactions(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des interactions catégorielles"""
        created_features = []
        
        # 1. Éducation × Emploi (via statut × ancienneté)
        df['education_employment'] = df['statut'].astype(str) + '_' + df['anciennete_emploi'].astype(str)
        created_features.append('education_employment')
        
        # 2. Statut × Logement
        df['marital_housing'] = df['statut'].astype(str) + '_' + df['logement'].astype(str)
        created_features.append('marital_housing')
        
        # 3. Objectif × Montant (catégorisé)
        montant_categories = pd.cut(df['montant'], bins=3, labels=['low', 'medium', 'high'])
        df['purpose_amount'] = df['objet'].astype(str) + '_' + montant_categories.astype(str)
        created_features.append('purpose_amount')
        
        print(f"   ✅ {len(created_features)} interactions catégorielles créées")
        return df, created_features
    
    def _create_mixed_interactions(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des interactions mixtes"""
        created_features = []
        
        # 1. Catégorie âge × Revenus
        age_categories = pd.cut(df['age'], bins=[0, 30, 50, 100], labels=['young', 'middle', 'senior'])
        df['age_category_income'] = age_categories.astype(str) + '_income_' + \
                                   pd.cut(df['revenus_estimes'], bins=3, labels=['low', 'med', 'high']).astype(str)
        created_features.append('age_category_income')
        
        # 2. Stabilité emploi × Score
        df['employment_stability_payment'] = df['employment_stability_score'] * df['payment_history_score']
        created_features.append('employment_stability_payment')
        
        print(f"   ✅ {len(created_features)} interactions mixtes créées")
        return df, created_features
    
    def create_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ÉTAPE 3.3: Création des features temporelles
        
        Crée les features basées sur le temps selon les spécifications
        """
        print("\n⏰ ÉTAPE 3.3: CRÉATION DES FEATURES TEMPORELLES")
        print("=" * 55)
        
        df_temporal = df.copy()
        created_features = []
        
        # 1. Cycle de vie des comptes
        print("\n🔄 Features cycle de vie...")
        df_temporal, lifecycle_features = self._create_account_lifecycle(df_temporal)
        created_features.extend(lifecycle_features)
        
        # 2. Patterns saisonniers
        print("\n🌟 Features saisonnières...")
        df_temporal, seasonal_features = self._create_seasonal_patterns(df_temporal)
        created_features.extend(seasonal_features)
        
        # 3. Features de tendance
        print("\n📈 Features de tendance...")
        df_temporal, trend_features = self._create_trend_features(df_temporal)
        created_features.extend(trend_features)
        
        self.feature_info['temporal_features'] = created_features
        print(f"\n✅ {len(created_features)} features temporelles créées!")
        
        return df_temporal
    
    def _create_account_lifecycle(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des features de cycle de vie"""
        created_features = []
        
        # 1. Âge compte en mois (basé sur ancienneté emploi)
        df['account_age_months'] = df['account_age_average'] * 12
        created_features.append('account_age_months')
        
        # 2. Temps depuis dernier paiement (simulé)
        np.random.seed(42)
        df['time_since_last_payment'] = np.random.exponential(30, len(df))  # jours
        created_features.append('time_since_last_payment')
        
        # 3. Longueur historique crédit
        df['credit_history_length'] = df['account_age_months'] + np.random.normal(12, 6, len(df))
        df['credit_history_length'] = np.clip(df['credit_history_length'], 0, None)
        created_features.append('credit_history_length')
        
        print(f"   ✅ {len(created_features)} features cycle de vie créées")
        return df, created_features
    
    def _create_seasonal_patterns(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des features saisonnières"""
        created_features = []
        
        # Simulation de mois de demande
        np.random.seed(42)
        df['application_month'] = np.random.randint(1, 13, len(df))
        created_features.append('application_month')
        
        # Indicateur risque saisonnier
        seasonal_risk = {1: 0.1, 2: 0.1, 3: 0.2, 4: 0.3, 5: 0.4, 6: 0.5,
                        7: 0.6, 8: 0.5, 9: 0.4, 10: 0.3, 11: 0.2, 12: 0.8}
        df['seasonal_risk_indicator'] = df['application_month'].map(seasonal_risk)
        created_features.append('seasonal_risk_indicator')
        
        # Proximité vacances (juin-août, décembre)
        df['holiday_proximity'] = df['application_month'].apply(
            lambda x: 1 if x in [6, 7, 8, 12] else 0
        )
        created_features.append('holiday_proximity')
        
        print(f"   ✅ {len(created_features)} features saisonnières créées")
        return df, created_features
    
    def _create_trend_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """Création des features de tendance"""
        created_features = []
        
        # Simulation de tendances (en réalité, cela viendrait de données historiques)
        np.random.seed(42)
        
        # 1. Tendance revenus
        df['income_trend'] = np.random.normal(0, 0.1, len(df))  # -1 à 1
        created_features.append('income_trend')
        
        # 2. Tendance dépenses
        df['spending_trend'] = np.random.normal(0, 0.15, len(df))
        created_features.append('spending_trend')
        
        # 3. Tendance utilisation crédit
        df['credit_usage_trend'] = np.random.normal(0, 0.2, len(df))
        created_features.append('credit_usage_trend')
        
        print(f"   ✅ {len(created_features)} features de tendance créées")
        return df, created_features
    
    def engineer_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Pipeline complet de feature engineering
        
        Exécute toutes les étapes de création de features dans l'ordre :
        1. Features métier
        2. Features d'interaction  
        3. Features temporelles
        
        Args:
            df: DataFrame d'entrée
            
        Returns:
            DataFrame avec toutes les features créées
        """
        print("\n🚀 PIPELINE COMPLET DE FEATURE ENGINEERING")
        print("=" * 60)
        
        # Sauvegarde des colonnes originales
        original_columns = df.columns.tolist()
        
        # Étape 1: Features métier
        df_engineered = self.create_business_features(df)
        
        # Étape 2: Features d'interaction
        df_engineered = self.create_interaction_features(df_engineered)
        
        # Étape 3: Features temporelles
        df_engineered = self.create_temporal_features(df_engineered)
        
        # Rapport final
        new_features = [col for col in df_engineered.columns if col not in original_columns]
        
        print(f"\n🎯 RÉSUMÉ FEATURE ENGINEERING")
        print("=" * 35)
        print(f"📊 Features originales: {len(original_columns)}")
        print(f"🆕 Nouvelles features: {len(new_features)}")
        print(f"📈 Total features: {len(df_engineered.columns)}")
        
        # Stockage des informations
        self.feature_info['original_features'] = original_columns
        self.feature_info['new_features'] = new_features
        self.feature_info['total_features'] = len(df_engineered.columns)
        
        return df_engineered
    
    def get_feature_info(self) -> Dict[str, Any]:
        """Retourne les informations sur les features créées"""
        return self.feature_info
    
    def get_feature_importance_groups(self) -> Dict[str, List[str]]:
        """Retourne les groupes de features pour l'analyse d'importance"""
        return {
            'business_features': self.feature_info.get('business_features', []),
            'interaction_features': self.feature_info.get('interaction_features', []),
            'temporal_features': self.feature_info.get('temporal_features', [])
        } 