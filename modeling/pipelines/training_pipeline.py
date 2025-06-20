"""
Training Pipeline for Credit Scoring System

This module implements the complete training pipeline according to 
the specifications defined in PROJET_COMPLET_SPECIFICATION.md - ÉTAPE 5

Author: Credit Scoring Team
Created: 2024
"""

import os
import sys
import pandas as pd
import numpy as np
import logging
import joblib
from pathlib import Path
from typing import Dict, Tuple, Optional, Any
from datetime import datetime

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.calibration import CalibratedClassifierCV
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    logging.warning("MLflow not available. Experiment tracking disabled.")


class TrainingPipeline:
    """
    ÉTAPE 5: Pipeline d'entraînement du modèle
    
    Implémente l'entraînement selon l'architecture définie :
    - Optimisation des hyperparamètres
    - Évaluation des performances
    - Calibration du modèle
    - Sauvegarde et versioning
    """
    
    def __init__(self, config: Dict):
        """
        Initialisation du pipeline d'entraînement
        
        Args:
            config: Configuration du projet
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configuration par défaut
        self.model_config = config.get('model', {})
        self.default_params = {
            'C': 1.0,
            'penalty': 'l2',
            'solver': 'lbfgs',
            'max_iter': 1000,
            'random_state': 42,
            'class_weight': 'balanced'
        }
        
        # Paths
        self.data_path = Path("data/processed")
        self.models_path = Path("models")
        self.models_path.mkdir(exist_ok=True)
        
        # Métriques
        self.metrics = {}
        self.best_model = None
        self.best_params = None
        
    def run(self, experiment_name: Optional[str] = None, 
            hyperparameter_tuning: bool = True) -> Dict[str, Any]:
        """
        Exécute le pipeline d'entraînement complet
        
        Args:
            experiment_name: Nom de l'expérience MLflow
            hyperparameter_tuning: Activer l'optimisation des hyperparamètres
            
        Returns:
            Dictionnaire contenant les résultats d'entraînement
        """
        print("\n🚀 ÉTAPE 5: PIPELINE D'ENTRAÎNEMENT DU MODÈLE")
        print("=" * 60)
        
        # 1. Chargement des données
        print("\n📊 1. Chargement des données...")
        X_train, X_test, y_train, y_test = self._load_and_split_data()
        
        # 2. Configuration MLflow
        if MLFLOW_AVAILABLE and experiment_name:
            self._setup_mlflow(experiment_name)
        
        # 3. Entraînement du modèle
        print("\n🔧 2. Entraînement du modèle...")
        if hyperparameter_tuning:
            model = self._train_with_hyperparameter_tuning(X_train, y_train)
        else:
            model = self._train_basic_model(X_train, y_train)
        
        # 4. Évaluation
        print("\n📈 3. Évaluation du modèle...")
        metrics = self._evaluate_model(model, X_test, y_test)
        
        # 5. Calibration
        print("\n⚖️ 4. Calibration du modèle...")
        calibrated_model = self._calibrate_model(model, X_train, y_train)
        
        # 6. Sauvegarde
        print("\n💾 5. Sauvegarde du modèle...")
        model_path = self._save_model(calibrated_model, metrics)
        
        # 7. Génération du rapport
        print("\n📋 6. Génération du rapport...")
        report_path = self._generate_report(metrics, model_path)
        
        results = {
            'model': calibrated_model,
            'model_path': model_path,
            'metrics': metrics,
            'report_path': report_path,
            'best_params': self.best_params
        }
        
        print(f"\n✅ Pipeline d'entraînement terminé avec succès!")
        print(f"📊 AUC-ROC: {metrics.get('auc_roc', 'N/A'):.4f}")
        print(f"🎯 Accuracy: {metrics.get('accuracy', 'N/A'):.4f}")
        print(f"💾 Modèle sauvegardé: {model_path}")
        
        return results
    
    def _load_and_split_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Charge et divise les données"""
        
        # Chargement des données transformées
        data_file = self.data_path / "credit_engineered_transformed.csv"
        if not data_file.exists():
            raise FileNotFoundError(f"Fichier de données non trouvé: {data_file}")
        
        df = pd.read_csv(data_file)
        
        # Séparation des features et de la cible
        X = df.drop(columns=['cible'])
        y = df['cible']
        
        # Division train/test
        test_size = self.config.get('model', {}).get('test_size', 0.2)
        random_state = self.config.get('model', {}).get('random_state', 42)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, 
            stratify=y
        )
        
        print(f"   ✅ Données chargées: {len(df)} échantillons")
        print(f"   ✅ Train: {len(X_train)} échantillons")
        print(f"   ✅ Test: {len(X_test)} échantillons")
        print(f"   ✅ Features: {len(X.columns)} variables")
        
        return X_train, X_test, y_train, y_test
    
    def _train_with_hyperparameter_tuning(self, X_train: pd.DataFrame, 
                                         y_train: pd.Series) -> Any:
        """Entraîne le modèle avec optimisation des hyperparamètres"""
        
        print("   🔍 Optimisation des hyperparamètres...")
        
        # Grille de paramètres
        param_grid = {
            'C': [0.01, 0.1, 1.0, 10.0, 100.0],
            'penalty': ['l1', 'l2', 'elasticnet'],
            'solver': ['liblinear', 'lbfgs', 'saga'],
            'max_iter': [1000, 2000, 3000],
            'class_weight': [None, 'balanced']
        }
        
        # Modèle de base
        base_model = LogisticRegression(random_state=42)
        
        # GridSearchCV
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=5,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        )
        
        # Entraînement
        grid_search.fit(X_train, y_train)
        
        self.best_params = grid_search.best_params_
        self.best_model = grid_search.best_estimator_
        
        print(f"   ✅ Meilleurs paramètres: {self.best_params}")
        print(f"   ✅ Meilleur score CV: {grid_search.best_score_:.4f}")
        
        return self.best_model
    
    def _train_basic_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> Any:
        """Entraîne un modèle de base sans optimisation"""
        
        print("   🔧 Entraînement du modèle de base...")
        
        # Paramètres par défaut
        params = {**self.default_params, **self.model_config.get('params', {})}
        
        # Entraînement
        model = LogisticRegression(**params)
        model.fit(X_train, y_train)
        
        self.best_model = model
        self.best_params = params
        
        print(f"   ✅ Modèle entraîné avec paramètres: {params}")
        
        return model
    
    def _evaluate_model(self, model: Any, X_test: pd.DataFrame, 
                       y_test: pd.Series) -> Dict[str, float]:
        """Évalue les performances du modèle"""
        
        # Prédictions
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        # Métriques de classification
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'auc_roc': roc_auc_score(y_test, y_proba)
        }
        
        # Métriques métier
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        
        metrics.update({
            'specificity': tn / (tn + fp) if (tn + fp) > 0 else 0,
            'sensitivity': tp / (tp + fn) if (tp + fn) > 0 else 0,
            'precision_0': tn / (tn + fn) if (tn + fn) > 0 else 0,
            'precision_1': tp / (tp + fp) if (tp + fp) > 0 else 0
        })
        
        # Calcul KS Statistic
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        ks_stat = np.max(tpr - fpr)
        metrics['ks_statistic'] = ks_stat
        
        # Calcul Gini
        metrics['gini_coefficient'] = 2 * metrics['auc_roc'] - 1
        
        self.metrics = metrics
        
        print(f"   ✅ AUC-ROC: {metrics['auc_roc']:.4f}")
        print(f"   ✅ Accuracy: {metrics['accuracy']:.4f}")
        print(f"   ✅ Precision: {metrics['precision']:.4f}")
        print(f"   ✅ Recall: {metrics['recall']:.4f}")
        print(f"   ✅ F1-Score: {metrics['f1_score']:.4f}")
        print(f"   ✅ KS Statistic: {metrics['ks_statistic']:.4f}")
        print(f"   ✅ Gini Coefficient: {metrics['gini_coefficient']:.4f}")
        
        return metrics
    
    def _calibrate_model(self, model: Any, X_train: pd.DataFrame, 
                        y_train: pd.Series) -> Any:
        """Calibre le modèle pour améliorer les probabilités"""
        
        print("   ⚖️ Calibration du modèle...")
        
        # Calibration avec validation croisée
        calibrated_model = CalibratedClassifierCV(
            model, 
            method='isotonic',  # ou 'sigmoid'
            cv=3
        )
        
        calibrated_model.fit(X_train, y_train)
        
        print("   ✅ Modèle calibré avec succès")
        
        return calibrated_model
    
    def _save_model(self, model: Any, metrics: Dict[str, float]) -> str:
        """Sauvegarde le modèle entraîné"""
        
        # Création du nom de fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        auc_score = metrics.get('auc_roc', 0)
        
        model_filename = f"credit_scoring_model_{timestamp}_auc{auc_score:.4f}.pkl"
        model_path = self.models_path / model_filename
        
        # Sauvegarde avec joblib
        model_info = {
            'model': model,
            'metrics': metrics,
            'params': self.best_params,
            'timestamp': timestamp,
            'version': '1.0'
        }
        
        joblib.dump(model_info, model_path)
        
        # Sauvegarde du meilleur modèle
        best_model_path = self.models_path / "best_model.pkl"
        joblib.dump(model_info, best_model_path)
        
        print(f"   ✅ Modèle sauvegardé: {model_path}")
        print(f"   ✅ Meilleur modèle: {best_model_path}")
        
        return str(model_path)
    
    def _generate_report(self, metrics: Dict[str, float], model_path: str) -> str:
        """Génère un rapport d'entraînement"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"training_report_{timestamp}.txt"
        report_path = Path("reports") / report_filename
        
        # Création du répertoire reports
        report_path.parent.mkdir(exist_ok=True)
        
        # Génération du rapport
        report_content = f"""
RAPPORT D'ENTRAÎNEMENT - MODÈLE DE CREDIT SCORING
=================================================

Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Modèle: {model_path}

PARAMÈTRES OPTIMAUX:
{'-' * 20}
{self._format_params(self.best_params)}

MÉTRIQUES DE PERFORMANCE:
{'-' * 25}
AUC-ROC: {metrics.get('auc_roc', 'N/A'):.4f}
Accuracy: {metrics.get('accuracy', 'N/A'):.4f}
Precision: {metrics.get('precision', 'N/A'):.4f}
Recall: {metrics.get('recall', 'N/A'):.4f}
F1-Score: {metrics.get('f1_score', 'N/A'):.4f}
Specificity: {metrics.get('specificity', 'N/A'):.4f}
Sensitivity: {metrics.get('sensitivity', 'N/A'):.4f}

MÉTRIQUES MÉTIER:
{'-' * 17}
KS Statistic: {metrics.get('ks_statistic', 'N/A'):.4f}
Gini Coefficient: {metrics.get('gini_coefficient', 'N/A'):.4f}

INTERPRÉTATION:
{'-' * 15}
- AUC-ROC > 0.7: Modèle acceptable
- AUC-ROC > 0.8: Bon modèle
- AUC-ROC > 0.9: Excellent modèle
- KS > 0.3: Pouvoir discriminant acceptable
- Gini > 0.4: Pouvoir prédictif acceptable

STATUS: {'✅ MODÈLE ACCEPTABLE' if metrics.get('auc_roc', 0) > 0.7 else '⚠️ MODÈLE À AMÉLIORER'}
"""
        
        # Sauvegarde du rapport
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"   ✅ Rapport généré: {report_path}")
        
        return str(report_path)
    
    def _format_params(self, params: Dict) -> str:
        """Formate les paramètres pour le rapport"""
        return '\n'.join([f"{k}: {v}" for k, v in params.items()])
    
    def _setup_mlflow(self, experiment_name: str):
        """Configure MLflow pour le tracking"""
        if not MLFLOW_AVAILABLE:
            return
        
        mlflow.set_experiment(experiment_name)
        mlflow.start_run()
        
        # Log des paramètres
        if self.best_params:
            mlflow.log_params(self.best_params)
        
        # Log des métriques
        if self.metrics:
            mlflow.log_metrics(self.metrics)
        
        print(f"   ✅ MLflow configuré: {experiment_name}") 