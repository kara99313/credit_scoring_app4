"""
Inference Pipeline for Credit Scoring System

This module handles model inference and predictions.

Author: Credit Scoring Team
Created: 2024
"""

import sys
import pandas as pd
import numpy as np
import logging
import joblib
from pathlib import Path
from typing import Dict, Union, Optional

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))


class InferencePipeline:
    """Pipeline d'inférence pour les prédictions"""
    
    def __init__(self, config: Dict):
        """
        Initialisation du pipeline d'inférence
        
        Args:
            config: Configuration du projet
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.model_info = None
        
    def run(self, model_path: Optional[str] = None, 
            input_data_path: str = None, 
            output_path: str = "predictions.csv") -> pd.DataFrame:
        """
        Exécute le pipeline d'inférence
        
        Args:
            model_path: Chemin vers le modèle (None = utilise le meilleur modèle)
            input_data_path: Chemin vers les données d'entrée
            output_path: Chemin de sauvegarde des prédictions
            
        Returns:
            DataFrame avec les prédictions
        """
        print("\n🔮 PIPELINE D'INFÉRENCE")
        print("=" * 40)
        
        # 1. Chargement du modèle
        print("\n📦 1. Chargement du modèle...")
        self._load_model(model_path)
        
        # 2. Chargement des données
        print("\n📊 2. Chargement des données...")
        df = self._load_data(input_data_path)
        
        # 3. Prédictions
        print("\n🎯 3. Génération des prédictions...")
        predictions_df = self._make_predictions(df)
        
        # 4. Sauvegarde
        print("\n💾 4. Sauvegarde des résultats...")
        predictions_df.to_csv(output_path, index=False)
        
        print(f"✅ Prédictions terminées!")
        print(f"📁 Résultats sauvegardés: {output_path}")
        print(f"📊 Nombre de prédictions: {len(predictions_df)}")
        
        return predictions_df
    
    def _load_model(self, model_path: Optional[str] = None):
        """Charge le modèle entraîné"""
        
        if model_path is None:
            # Utiliser le meilleur modèle par défaut
            model_path = Path("models") / "best_model.pkl"
        else:
            model_path = Path(model_path)
        
        if not model_path.exists():
            raise FileNotFoundError(f"Modèle non trouvé: {model_path}")
        
        # Chargement du modèle
        self.model_info = joblib.load(model_path)
        self.model = self.model_info['model']
        
        print(f"   ✅ Modèle chargé: {model_path}")
        print(f"   ✅ Version: {self.model_info.get('version', 'N/A')}")
        print(f"   ✅ AUC-ROC: {self.model_info.get('metrics', {}).get('auc_roc', 'N/A')}")
    
    def _load_data(self, input_data_path: str) -> pd.DataFrame:
        """Charge les données d'entrée"""
        
        data_path = Path(input_data_path)
        if not data_path.exists():
            raise FileNotFoundError(f"Fichier de données non trouvé: {data_path}")
        
        df = pd.read_csv(data_path)
        
        print(f"   ✅ Données chargées: {len(df)} échantillons")
        print(f"   ✅ Features: {len(df.columns)} variables")
        
        return df
    
    def _make_predictions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Génère les prédictions"""
        
        # Préparer les données (supprimer la cible si présente)
        if 'cible' in df.columns:
            X = df.drop(columns=['cible'])
            has_target = True
        else:
            X = df
            has_target = False
        
        # Prédictions
        y_pred = self.model.predict(X)
        y_proba = self.model.predict_proba(X)[:, 1]
        
        # Conversion en score de crédit (300-850)
        credit_scores = self._convert_to_credit_score(y_proba)
        
        # Détermination de la classe de risque
        risk_classes = self._determine_risk_class(y_proba)
        
        # Recommandations
        recommendations = self._generate_recommendations(y_proba, y_pred)
        
        # Création du DataFrame de résultats
        results_df = pd.DataFrame({
            'prediction': y_pred,
            'probability_default': y_proba,
            'probability_no_default': 1 - y_proba,
            'credit_score': credit_scores,
            'risk_class': risk_classes,
            'recommendation': recommendations
        })
        
        # Ajouter les données originales
        for col in X.columns:
            results_df[f'input_{col}'] = X[col].values
        
        # Ajouter la vraie cible si disponible
        if has_target:
            results_df['actual_target'] = df['cible'].values
            
            # Calculer l'accuracy si la cible est disponible
            accuracy = (y_pred == df['cible']).mean()
            print(f"   ✅ Accuracy sur les données: {accuracy:.4f}")
        
        print(f"   ✅ Prédictions générées: {len(results_df)}")
        print(f"   ✅ Taux d'approbation: {(y_pred == 0).mean():.2%}")
        print(f"   ✅ Taux de rejet: {(y_pred == 1).mean():.2%}")
        
        return results_df
    
    def _convert_to_credit_score(self, probabilities: np.ndarray) -> np.ndarray:
        """
        Convertit les probabilités en scores de crédit (300-850)
        
        Args:
            probabilities: Probabilités de défaut
            
        Returns:
            Scores de crédit entre 300 et 850
        """
        # Inverser les probabilités (plus la probabilité de défaut est élevée, plus le score est bas)
        inverted_proba = 1 - probabilities
        
        # Normaliser et convertir en score 300-850
        credit_scores = 300 + (inverted_proba * 550)
        
        return credit_scores.astype(int)
    
    def _determine_risk_class(self, probabilities: np.ndarray) -> np.ndarray:
        """
        Détermine la classe de risque basée sur les probabilités
        
        Args:
            probabilities: Probabilités de défaut
            
        Returns:
            Classes de risque
        """
        risk_classes = np.where(
            probabilities < 0.1, 'Très Faible',
            np.where(probabilities < 0.2, 'Faible',
                    np.where(probabilities < 0.4, 'Moyen',
                            np.where(probabilities < 0.6, 'Élevé', 'Très Élevé')))
        )
        
        return risk_classes
    
    def _generate_recommendations(self, probabilities: np.ndarray, 
                                predictions: np.ndarray) -> np.ndarray:
        """
        Génère des recommandations basées sur les prédictions
        
        Args:
            probabilities: Probabilités de défaut
            predictions: Prédictions binaires
            
        Returns:
            Recommandations
        """
        recommendations = []
        
        for prob, pred in zip(probabilities, predictions):
            if pred == 0:  # Pas de défaut prédit
                if prob < 0.1:
                    recommendations.append("Approbation automatique")
                elif prob < 0.2:
                    recommendations.append("Approbation avec conditions standards")
                else:
                    recommendations.append("Approbation avec conditions renforcées")
            else:  # Défaut prédit
                if prob > 0.6:
                    recommendations.append("Rejet automatique")
                else:
                    recommendations.append("Examen manuel requis")
        
        return np.array(recommendations) 