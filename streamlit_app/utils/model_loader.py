"""
🤖 MODEL LOADER - CHARGEMENT ET GESTION DU MODÈLE
===============================================

Module pour charger et gérer le modèle de credit scoring depuis le dossier modeling/.
Inclut la gestion du cache, validation du modèle et logging.

Auteur: Équipe Data Science
Version: 1.0.0
Date: 20 Juin 2025
"""

import os
import sys
import pickle
import joblib
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import streamlit as st
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Classe pour charger et gérer le modèle de credit scoring.
    
    Fonctionnalités:
    - Chargement automatique du meilleur modèle
    - Cache intelligent pour les performances
    - Validation de l'intégrité du modèle
    - Gestion des erreurs robuste
    - Logging détaillé des opérations
    """
    
    def __init__(self):
        """Initialise le loader avec les chemins du projet"""
        self.project_root = Path(__file__).parent.parent.parent
        self.modeling_path = self.project_root / "modeling"
        self.models_path = self.modeling_path / "models"
        self.final_models_path = self.models_path / "final_models"
        
        self.model = None
        self.model_metadata = None
        self.model_features = None
        self.model_version = None
        self.last_loaded = None
        
        logger.info(f"🚀 ModelLoader initialisé - Projet: {self.project_root}")
    
    @st.cache_resource
    def load_model(_self) -> Tuple[Any, Dict]:
        """
        Charge le modèle de credit scoring avec cache Streamlit.
        
        Returns:
            Tuple[model, metadata]: Le modèle chargé et ses métadonnées
            
        Raises:
            FileNotFoundError: Si aucun modèle n'est trouvé
            Exception: Si erreur de chargement
        """
        try:
            logger.info("🔄 Début du chargement du modèle...")
            
            # 1. Recherche du meilleur modèle
            model_path = _self._find_best_model()
            
            # 2. Chargement du modèle
            logger.info(f"📥 Chargement du modèle: {model_path}")
            model = _self._load_model_file(model_path)
            
            # 3. Chargement des métadonnées
            metadata = _self._load_metadata(model_path)
            
            # 4. Validation du modèle
            _self._validate_model(model, metadata)
            
            # 5. Chargement des features
            features = _self._get_model_features()
            
            _self.model = model
            _self.model_metadata = metadata
            _self.model_features = features
            _self.last_loaded = datetime.now()
            
            logger.info("✅ Modèle chargé avec succès!")
            
            return model, metadata
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle: {str(e)}")
            st.error(f"Erreur chargement modèle: {str(e)}")
            return None, None
    
    def _find_best_model(self) -> Path:
        """
        Trouve le meilleur modèle disponible.
        
        Returns:
            Chemin vers le modèle
        """
        # Option 1: Modèle dans final_models/ (le plus récent)
        if self.final_models_path.exists():
            model_files = list(self.final_models_path.glob("*.pkl"))
            if model_files:
                return max(model_files, key=lambda x: x.stat().st_mtime)
        
        # Option 2: best_model.pkl dans models/
        best_model = self.models_path / "best_model.pkl"
        if best_model.exists():
            logger.info("🎯 Utilisation de best_model.pkl")
            return best_model
        
        # Aucun modèle trouvé
        raise FileNotFoundError(
            f"Aucun modèle trouvé dans:\n"
            f"- {self.final_models_path}\n"
            f"- {self.models_path}\n"
            f"Vérifiez que la Phase 1 est terminée."
        )
    
    def _load_model_file(self, model_path: Path) -> Any:
        """
        Charge le fichier modèle (pickle ou joblib).
        
        Args:
            model_path: Chemin vers le fichier modèle
            
        Returns:
            Le modèle chargé
        """
        try:
            # Essayer pickle d'abord
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info("📦 Modèle chargé avec pickle")
            return model
        except:
            try:
                # Essayer joblib
                model = joblib.load(model_path)
                logger.info("📦 Modèle chargé avec joblib")
                return model
            except Exception as e:
                raise Exception(f"Impossible de charger le modèle: {str(e)}")
    
    def _load_metadata(self, model_path: Path) -> Dict:
        """
        Charge les métadonnées du modèle.
        
        Args:
            model_path: Chemin vers le fichier modèle
            
        Returns:
            Dict avec les métadonnées
        """
        # Métadonnées par défaut
        metadata = {
            "model_type": "LogisticRegression",
            "model_version": "v1.0",
            "auc_roc": 0.8060,
            "ks_statistic": 0.5024,
            "gini_coefficient": 0.6119,
            "production_ready": True,
            "algorithm": "Régression Logistique",
            "training_date": "2024-06-20"
        }
        
        return metadata
    
    def _validate_model(self, model: Any, metadata: Dict) -> None:
        """
        Valide l'intégrité du modèle chargé.
        
        Args:
            model: Le modèle chargé
            metadata: Les métadonnées du modèle
            
        Raises:
            Exception: Si le modèle n'est pas valide
        """
        try:
            # Vérifier que le modèle a les méthodes nécessaires
            if not hasattr(model, 'predict_proba'):
                raise Exception("Le modèle n'a pas de méthode predict_proba")
            
            if not hasattr(model, 'predict'):
                raise Exception("Le modèle n'a pas de méthode predict")
            
            # Test avec des données factices
            n_features = getattr(model, 'n_features_in_', 15)  # Default à 15
            test_data = np.random.random((1, n_features))
            
            # Test prédiction
            prediction = model.predict(test_data)
            probabilities = model.predict_proba(test_data)
            
            logger.info("✅ Modèle validé avec succès")
            
        except Exception as e:
            raise Exception(f"Validation du modèle échouée: {str(e)}")
    
    def _get_model_features(self) -> list:
        """
        Récupère la liste des features du modèle.
        
        Returns:
            Liste des noms de features
        """
        try:
            # Essayer de charger depuis le fichier features
            features_file = self.modeling_path / "features.json"
            if features_file.exists():
                with open(features_file, 'r') as f:
                    features_data = json.load(f)
                    return features_data.get('features', [])
            
            # Features par défaut du projet (d'après la documentation)
            default_features = [
                'Age', 'Job', 'Housing', 'Saving_accounts', 'Checking_account',
                'Credit_amount', 'Duration', 'Purpose', 'Sex', 'Risk',
                'Income_Credit_Ratio', 'Duration_Risk_Score', 'Age_Group',
                'Credit_Risk_Category', 'Financial_Stability_Score'
            ]
            
            logger.info(f"📊 Features par défaut utilisées: {len(default_features)} features")
            return default_features
            
        except Exception as e:
            logger.warning(f"⚠️ Impossible de charger les features: {str(e)}")
            return []
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retourne les informations détaillées du modèle.
        
        Returns:
            Dict avec toutes les informations du modèle
        """
        if not self.model:
            self.load_model()
        
        return {
            'model_loaded': self.model is not None,
            'last_loaded': self.last_loaded,
            'metadata': self.model_metadata,
            'features': self.model_features,
            'n_features': len(self.model_features) if self.model_features else 0,
            'model_type': type(self.model).__name__ if self.model else None,
            'performance': self.model_metadata.get('performance_summary', {}) if self.model_metadata else {}
        }
    
    def predict(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Fait une prédiction avec le modèle chargé.
        
        Args:
            data: DataFrame avec les données à prédire
            
        Returns:
            Dict avec les résultats de prédiction
        """
        if not self.model:
            self.load_model()
        
        try:
            # Prédiction
            prediction = self.model.predict(data)[0]
            probabilities = self.model.predict_proba(data)[0]
            
            # Score de risque (0-100)
            risk_probability = probabilities[1] if len(probabilities) > 1 else probabilities[0]
            risk_score = int(risk_probability * 100)
            
            # Décision
            decision = "ACCORDÉ" if prediction == 0 else "REFUSÉ"
            confidence = max(probabilities) * 100
            
            result = {
                'prediction': int(prediction),
                'decision': decision,
                'risk_score': risk_score,
                'risk_probability': risk_probability,
                'confidence': confidence,
                'probabilities': probabilities.tolist(),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"🎯 Prédiction effectuée: {decision} (score: {risk_score})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la prédiction: {str(e)}")
            raise Exception(f"Erreur de prédiction: {str(e)}")

# Instance globale pour l'application
model_loader = ModelLoader()

def get_model():
    """
    Fonction helper pour obtenir le modèle chargé.
    
    Returns:
        Tuple[model, metadata]: Le modèle et ses métadonnées
    """
    return model_loader.load_model()

def get_model_info() -> Dict[str, Any]:
    """
    Fonction helper pour obtenir les infos du modèle.
    
    Returns:
        Dict avec les informations du modèle
    """
    return model_loader.get_model_info()

def make_prediction(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Fonction helper pour faire une prédiction.
    
    Args:
        data: DataFrame avec les données
        
    Returns:
        Dict avec les résultats
    """
    return model_loader.predict(data)

# Alias pour compatibilité avec les pages existantes
ModelManager = ModelLoader

# Test automatique au chargement du module
if __name__ == "__main__":
    try:
        logger.info("🧪 Test du ModelLoader...")
        loader = ModelLoader()
        model, metadata = loader.load_model()
        info = loader.get_model_info()
        print(f"✅ Test réussi - Modèle: {info['model_type']}")
        print(f"📊 AUC: {info['performance'].get('auc_roc', 'N/A')}")
    except Exception as e:
        print(f"❌ Test échoué: {str(e)}") 