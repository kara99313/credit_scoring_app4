"""
Variable Transformation Module for Credit Scoring System

This module implements comprehensive variable transformations according to 
the specifications defined in PROJET_COMPLET_SPECIFICATION.md - ÉTAPE 4

Author: Credit Scoring Team
Created: 2024
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, List, Any, Optional
from sklearn.preprocessing import (
    StandardScaler, RobustScaler, MinMaxScaler, QuantileTransformer,
    LabelEncoder, OneHotEncoder, TargetEncoder
)
from sklearn.feature_selection import (
    VarianceThreshold, SelectKBest, chi2, f_classif,
    SelectFromModel, RFE
)
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')


class VariableTransformer:
    """
    ÉTAPE 4: Transformations Variables
    
    Implémente les transformations selon l'architecture définie :
    - Encodage catégoriel (one-hot, target, label)
    - Scaling numérique (standard, robust, minmax)
    - Sélection de features (variance, corrélation, statistique, modèle)
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialisation du Variable Transformer
        
        Args:
            config: Configuration pour les transformations
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Stockage des transformers entraînés
        self.fitted_transformers = {}
        self.feature_names = []
        self.selected_features = []
        self.transformation_info = {}
        
        # Configuration par défaut selon spécifications
        self.default_config = {
            'categorical_encoding': {
                'method': 'mixed',  # one_hot, label, target, mixed
                'high_cardinality_threshold': 10,
                'rare_category_threshold': 0.01
            },
            'numerical_scaling': {
                'method': 'robust',  # standard, minmax, robust, quantile
                'handle_outliers': True
            },
            'feature_selection': {
                'methods': ['variance', 'correlation', 'statistical', 'model_based'],
                'variance_threshold': 0.01,
                'correlation_threshold': 0.95,
                'statistical_tests': ['chi2', 'f_classif'],
                'model_based_selector': 'lasso',
                'k_best': 30
            }
        }
        
        # Merge avec la config fournie
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
            elif isinstance(value, dict):
                self.config[key] = {**value, **self.config.get(key, {})}
                
    def categorical_encoding(self, df: pd.DataFrame, target: Optional[pd.Series] = None, 
                           fit: bool = True) -> pd.DataFrame:
        """
        ÉTAPE 4.1: Encodage des variables catégorielles
        
        Applique les stratégies d'encodage selon la configuration :
        - One-hot encoding (faible cardinalité)
        - Target encoding (haute cardinalité)
        - Label encoding (variables ordinales)
        """
        print("\n🔤 ÉTAPE 4.1: ENCODAGE DES VARIABLES CATÉGORIELLES")
        print("=" * 60)
        
        df_encoded = df.copy()
        encoding_info = {}
        
        # Identification des variables catégorielles
        categorical_cols = df_encoded.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"📋 Variables catégorielles détectées: {len(categorical_cols)}")
        
        for col in categorical_cols:
            if col in df_encoded.columns:
                print(f"\n🔄 Encodage de '{col}'...")
                
                # Nettoyage des valeurs manquantes
                df_encoded[col] = df_encoded[col].fillna('missing')
                
                # Gestion des catégories rares
                df_encoded, rare_categories = self._handle_rare_categories(df_encoded, col)
                
                # Choix de la stratégie d'encodage
                unique_values = df_encoded[col].nunique()
                threshold = self.config['categorical_encoding']['high_cardinality_threshold']
                
                if unique_values <= threshold:
                    # One-hot encoding pour faible cardinalité
                    df_encoded, encoder = self._apply_onehot_encoding(df_encoded, col, fit)
                    encoding_info[col] = {
                        'method': 'one_hot',
                        'unique_values': unique_values,
                        'encoder': encoder,
                        'rare_categories': rare_categories
                    }
                    print(f"   ✅ One-hot encoding appliqué ({unique_values} catégories)")
                    
                else:
                    # Target encoding pour haute cardinalité
                    if target is not None:
                        df_encoded, encoder = self._apply_target_encoding(df_encoded, col, target, fit)
                        encoding_info[col] = {
                            'method': 'target',
                            'unique_values': unique_values,
                            'encoder': encoder,
                            'rare_categories': rare_categories
                        }
                        print(f"   ✅ Target encoding appliqué ({unique_values} catégories)")
                    else:
                        # Label encoding si pas de target
                        df_encoded, encoder = self._apply_label_encoding(df_encoded, col, fit)
                        encoding_info[col] = {
                            'method': 'label',
                            'unique_values': unique_values,
                            'encoder': encoder,
                            'rare_categories': rare_categories
                        }
                        print(f"   ✅ Label encoding appliqué ({unique_values} catégories)")
        
        self.transformation_info['categorical_encoding'] = encoding_info
        print(f"\n✅ Encodage catégoriel terminé: {len(categorical_cols)} variables traitées")
        
        return df_encoded
    
    def _handle_rare_categories(self, df: pd.DataFrame, col: str) -> Tuple[pd.DataFrame, List[str]]:
        """Gestion des catégories rares"""
        threshold = self.config['categorical_encoding']['rare_category_threshold']
        value_counts = df[col].value_counts(normalize=True)
        
        rare_categories = value_counts[value_counts < threshold].index.tolist()
        
        if rare_categories:
            df[col] = df[col].replace(rare_categories, 'rare_category')
            
        return df, rare_categories
    
    def _apply_onehot_encoding(self, df: pd.DataFrame, col: str, fit: bool) -> Tuple[pd.DataFrame, OneHotEncoder]:
        """Application du one-hot encoding"""
        if fit:
            encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
            encoded_data = encoder.fit_transform(df[[col]])
            self.fitted_transformers[f'onehot_{col}'] = encoder
        else:
            encoder = self.fitted_transformers[f'onehot_{col}']
            encoded_data = encoder.transform(df[[col]])
        
        # Création des noms de colonnes
        feature_names = [f"{col}_{cat}" for cat in encoder.categories_[0][1:]]  # drop first
        
        # Remplacement dans le DataFrame
        df = df.drop(columns=[col])
        encoded_df = pd.DataFrame(encoded_data, columns=feature_names, index=df.index)
        df = pd.concat([df, encoded_df], axis=1)
        
        return df, encoder
    
    def _apply_target_encoding(self, df: pd.DataFrame, col: str, target: pd.Series, fit: bool) -> Tuple[pd.DataFrame, TargetEncoder]:
        """Application du target encoding"""
        if fit:
            encoder = TargetEncoder(smooth='auto')
            df[f'{col}_encoded'] = encoder.fit_transform(df[[col]], target)
            self.fitted_transformers[f'target_{col}'] = encoder
        else:
            encoder = self.fitted_transformers[f'target_{col}']
            df[f'{col}_encoded'] = encoder.transform(df[[col]])
        
        # Suppression de la colonne originale
        df = df.drop(columns=[col])
        
        return df, encoder
    
    def _apply_label_encoding(self, df: pd.DataFrame, col: str, fit: bool) -> Tuple[pd.DataFrame, LabelEncoder]:
        """Application du label encoding"""
        if fit:
            encoder = LabelEncoder()
            df[f'{col}_encoded'] = encoder.fit_transform(df[col])
            self.fitted_transformers[f'label_{col}'] = encoder
        else:
            encoder = self.fitted_transformers[f'label_{col}']
            df[f'{col}_encoded'] = encoder.transform(df[col])
        
        # Suppression de la colonne originale
        df = df.drop(columns=[col])
        
        return df, encoder
    
    def numerical_scaling(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        ÉTAPE 4.2: Scaling des variables numériques
        
        Applique les stratégies de scaling selon la configuration :
        - Robust scaling (robuste aux outliers)
        - Standard scaling (normalisation standard)
        - MinMax scaling (mise à l'échelle 0-1)
        """
        print("\n📊 ÉTAPE 4.2: SCALING DES VARIABLES NUMÉRIQUES")
        print("=" * 55)
        
        df_scaled = df.copy()
        
        # Identification des variables numériques
        numerical_cols = df_scaled.select_dtypes(include=[np.number]).columns.tolist()
        
        # Exclusion de la variable cible si présente
        if 'cible' in numerical_cols:
            numerical_cols.remove('cible')
            
        print(f"📋 Variables numériques détectées: {len(numerical_cols)}")
        
        if not numerical_cols:
            print("⚠️ Aucune variable numérique à scaler")
            return df_scaled
        
        # Choix du scaler selon la configuration
        method = self.config['numerical_scaling']['method']
        
        if method == 'robust':
            scaler = RobustScaler()
        elif method == 'standard':
            scaler = StandardScaler()
        elif method == 'minmax':
            scaler = MinMaxScaler()
        elif method == 'quantile':
            scaler = QuantileTransformer(output_distribution='normal')
        else:
            scaler = RobustScaler()  # Par défaut
            
        print(f"🔧 Méthode de scaling: {method}")
        
        if fit:
            scaled_data = scaler.fit_transform(df_scaled[numerical_cols])
            self.fitted_transformers['numerical_scaler'] = scaler
        else:
            scaler = self.fitted_transformers['numerical_scaler']
            scaled_data = scaler.transform(df_scaled[numerical_cols])
        
        # Remplacement des données
        scaled_df = pd.DataFrame(scaled_data, columns=numerical_cols, index=df_scaled.index)
        df_scaled[numerical_cols] = scaled_df
        
        self.transformation_info['numerical_scaling'] = {
            'method': method,
            'features_scaled': numerical_cols,
            'scaler': scaler
        }
        
        print(f"✅ Scaling numérique terminé: {len(numerical_cols)} variables scalées")
        
        return df_scaled
    
    def feature_selection(self, df: pd.DataFrame, target: pd.Series, fit: bool = True) -> pd.DataFrame:
        """
        ÉTAPE 4.3: Sélection de features
        
        Applique les méthodes de sélection selon la configuration :
        - Variance filter (suppression variance faible)
        - Correlation filter (suppression haute corrélation)
        - Statistical selection (tests statistiques)
        - Model-based selection (importance des features)
        """
        print("\n🎯 ÉTAPE 4.3: SÉLECTION DE FEATURES")
        print("=" * 45)
        
        df_selected = df.copy()
        original_features = df_selected.columns.tolist()
        
        # Exclusion de la variable cible
        if 'cible' in original_features:
            original_features.remove('cible')
            
        print(f"📋 Features initiales: {len(original_features)}")
        
        selection_info = {
            'original_features': len(original_features),
            'selection_steps': []
        }
        
        methods = self.config['feature_selection']['methods']
        
        # 1. Variance Filter
        if 'variance' in methods:
            print("\n🔍 Application du filtre de variance...")
            df_selected, variance_info = self._apply_variance_filter(df_selected, fit)
            selection_info['selection_steps'].append(variance_info)
            
        # 2. Correlation Filter
        if 'correlation' in methods:
            print("\n🔗 Application du filtre de corrélation...")
            df_selected, correlation_info = self._apply_correlation_filter(df_selected, fit)
            selection_info['selection_steps'].append(correlation_info)
            
        # 3. Statistical Selection
        if 'statistical' in methods:
            print("\n📊 Application de la sélection statistique...")
            df_selected, statistical_info = self._apply_statistical_selection(df_selected, target, fit)
            selection_info['selection_steps'].append(statistical_info)
            
        # 4. Model-based Selection
        if 'model_based' in methods:
            print("\n🤖 Application de la sélection basée modèle...")
            df_selected, model_info = self._apply_model_based_selection(df_selected, target, fit)
            selection_info['selection_steps'].append(model_info)
        
        # Mise à jour des features sélectionnées
        final_features = [col for col in df_selected.columns if col != 'cible']
        selection_info['final_features'] = len(final_features)
        selection_info['selected_features'] = final_features
        
        self.selected_features = final_features
        self.transformation_info['feature_selection'] = selection_info
        
        print(f"\n✅ Sélection terminée: {len(original_features)} → {len(final_features)} features")
        print(f"📉 Réduction: {((len(original_features) - len(final_features)) / len(original_features) * 100):.1f}%")
        
        return df_selected
    
    def _apply_variance_filter(self, df: pd.DataFrame, fit: bool) -> Tuple[pd.DataFrame, Dict]:
        """Application du filtre de variance"""
        threshold = self.config['feature_selection']['variance_threshold']
        
        # Colonnes numériques seulement
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'cible' in numerical_cols:
            numerical_cols.remove('cible')
            
        if not numerical_cols:
            return df, {'method': 'variance', 'features_removed': 0, 'features_kept': len(df.columns)}
        
        if fit:
            selector = VarianceThreshold(threshold=threshold)
            selector.fit(df[numerical_cols])
            self.fitted_transformers['variance_selector'] = selector
        else:
            selector = self.fitted_transformers['variance_selector']
        
        # Sélection des features
        selected_mask = selector.get_support()
        selected_features = [col for i, col in enumerate(numerical_cols) if selected_mask[i]]
        removed_features = [col for i, col in enumerate(numerical_cols) if not selected_mask[i]]
        
        # Application de la sélection
        df = df.drop(columns=removed_features)
        
        info = {
            'method': 'variance',
            'threshold': threshold,
            'features_removed': len(removed_features),
            'features_kept': len(selected_features),
            'removed_features': removed_features
        }
        
        print(f"   ✅ Variance filter: {len(removed_features)} features supprimées")
        
        return df, info
    
    def _apply_correlation_filter(self, df: pd.DataFrame, fit: bool) -> Tuple[pd.DataFrame, Dict]:
        """Application du filtre de corrélation"""
        threshold = self.config['feature_selection']['correlation_threshold']
        
        # Colonnes numériques seulement
        numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'cible' in numerical_cols:
            numerical_cols.remove('cible')
            
        if len(numerical_cols) < 2:
            return df, {'method': 'correlation', 'features_removed': 0, 'features_kept': len(df.columns)}
        
        if fit:
            # Calcul de la matrice de corrélation
            corr_matrix = df[numerical_cols].corr().abs()
            
            # Identification des features hautement corrélées
            upper_triangle = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
            high_corr_pairs = np.where((corr_matrix > threshold) & upper_triangle)
            
            # Sélection des features à supprimer (garder la première de chaque paire)
            features_to_remove = []
            for i, j in zip(high_corr_pairs[0], high_corr_pairs[1]):
                feature_to_remove = corr_matrix.columns[j]  # Supprime la seconde feature
                if feature_to_remove not in features_to_remove:
                    features_to_remove.append(feature_to_remove)
                    
            self.fitted_transformers['correlation_features_to_remove'] = features_to_remove
        else:
            features_to_remove = self.fitted_transformers['correlation_features_to_remove']
        
        # Application de la suppression
        df = df.drop(columns=features_to_remove)
        
        info = {
            'method': 'correlation',
            'threshold': threshold,
            'features_removed': len(features_to_remove),
            'features_kept': len(numerical_cols) - len(features_to_remove),
            'removed_features': features_to_remove
        }
        
        print(f"   ✅ Correlation filter: {len(features_to_remove)} features supprimées")
        
        return df, info
    
    def _apply_statistical_selection(self, df: pd.DataFrame, target: pd.Series, fit: bool) -> Tuple[pd.DataFrame, Dict]:
        """Application de la sélection statistique"""
        k_best = self.config['feature_selection']['k_best']
        
        # Préparation des données
        feature_cols = [col for col in df.columns if col != 'cible']
        X = df[feature_cols]
        
        if fit:
            # Choix du test statistique selon le type des features
            if X.select_dtypes(include=[np.number]).shape[1] > 0:
                selector = SelectKBest(score_func=f_classif, k=min(k_best, len(feature_cols)))
            else:
                selector = SelectKBest(score_func=chi2, k=min(k_best, len(feature_cols)))
                
            selector.fit(X, target)
            self.fitted_transformers['statistical_selector'] = selector
        else:
            selector = self.fitted_transformers['statistical_selector']
        
        # Sélection des features
        selected_mask = selector.get_support()
        selected_features = [col for i, col in enumerate(feature_cols) if selected_mask[i]]
        removed_features = [col for i, col in enumerate(feature_cols) if not selected_mask[i]]
        
        # Application de la sélection
        df = df[selected_features + (['cible'] if 'cible' in df.columns else [])]
        
        info = {
            'method': 'statistical',
            'k_best': k_best,
            'features_removed': len(removed_features),
            'features_kept': len(selected_features),
            'removed_features': removed_features
        }
        
        print(f"   ✅ Statistical selection: {len(selected_features)} meilleures features gardées")
        
        return df, info
    
    def _apply_model_based_selection(self, df: pd.DataFrame, target: pd.Series, fit: bool) -> Tuple[pd.DataFrame, Dict]:
        """Application de la sélection basée modèle"""
        method = self.config['feature_selection']['model_based_selector']
        
        # Préparation des données
        feature_cols = [col for col in df.columns if col != 'cible']
        X = df[feature_cols]
        
        if fit:
            if method == 'lasso':
                estimator = LassoCV(cv=5, random_state=42)
            else:
                estimator = RandomForestClassifier(n_estimators=100, random_state=42)
                
            selector = SelectFromModel(estimator, threshold='median')
            selector.fit(X, target)
            self.fitted_transformers['model_selector'] = selector
        else:
            selector = self.fitted_transformers['model_selector']
        
        # Sélection des features
        selected_mask = selector.get_support()
        selected_features = [col for i, col in enumerate(feature_cols) if selected_mask[i]]
        removed_features = [col for i, col in enumerate(feature_cols) if not selected_mask[i]]
        
        # Application de la sélection
        df = df[selected_features + (['cible'] if 'cible' in df.columns else [])]
        
        info = {
            'method': 'model_based',
            'estimator': method,
            'features_removed': len(removed_features),
            'features_kept': len(selected_features),
            'removed_features': removed_features
        }
        
        print(f"   ✅ Model-based selection: {len(selected_features)} features importantes gardées")
        
        return df, info
    
    def transform_all_variables(self, df: pd.DataFrame, target: Optional[pd.Series] = None, 
                              fit: bool = True) -> pd.DataFrame:
        """
        Pipeline complet de transformation des variables
        
        Exécute toutes les étapes de transformation dans l'ordre :
        1. Encodage catégoriel
        2. Scaling numérique
        3. Sélection de features
        
        Args:
            df: DataFrame d'entrée
            target: Variable cible (optionnelle)
            fit: Si True, entraîne les transformers
            
        Returns:
            DataFrame transformé
        """
        print("\n🔄 PIPELINE COMPLET DE TRANSFORMATION DES VARIABLES")
        print("=" * 65)
        
        # Sauvegarde des informations initiales
        initial_shape = df.shape
        
        # Étape 1: Encodage catégoriel
        df_transformed = self.categorical_encoding(df, target, fit)
        
        # Étape 2: Scaling numérique
        df_transformed = self.numerical_scaling(df_transformed, fit)
        
        # Étape 3: Sélection de features (si target fournie)
        if target is not None:
            df_transformed = self.feature_selection(df_transformed, target, fit)
        
        # Rapport final
        final_shape = df_transformed.shape
        
        print(f"\n🎯 RÉSUMÉ TRANSFORMATION DES VARIABLES")
        print("=" * 45)
        print(f"📊 Shape initiale: {initial_shape}")
        print(f"📈 Shape finale: {final_shape}")
        print(f"🔄 Réduction features: {initial_shape[1] - final_shape[1]}")
        
        # Stockage des informations finales
        self.feature_names = df_transformed.columns.tolist()
        self.transformation_info['final_shape'] = final_shape
        self.transformation_info['feature_reduction'] = initial_shape[1] - final_shape[1]
        
        return df_transformed
    
    def get_transformation_info(self) -> Dict[str, Any]:
        """Retourne les informations sur les transformations appliquées"""
        return self.transformation_info
    
    def get_selected_features(self) -> List[str]:
        """Retourne la liste des features sélectionnées"""
        return self.selected_features
    
    def get_feature_names(self) -> List[str]:
        """Retourne la liste des noms de features finaux"""
        return self.feature_names 